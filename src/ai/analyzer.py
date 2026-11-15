"""Content analysis using AI."""

import asyncio
import json
import logging
from typing import List, Optional
from pydantic import ValidationError
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn
from tenacity import retry, retry_if_exception_type, retry_if_not_exception_type, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

from .client import AIClient
from .classifier import ContentClassifier
from .prompting.analysis import analysis_system_prompt, analysis_user_prompt
from .utils import gather_ai_tasks, parse_json_response
from .errors import AIProviderUnavailableError
from ..models import ContentAnalysis, ContentItem
from ..processing.content import select_content, split_content
from ..processing.profiles import ProfileRegistry


class ContentAnalyzer:
    """Analyzes content items using AI to determine importance."""

    def __init__(
        self,
        ai_client: AIClient,
        profiles: ProfileRegistry,
        console: Optional[Console] = None,
        *,
        concurrency: int = 1,
        throttle_sec: float = 0.0,
    ):
        self.client = ai_client
        self.profiles = profiles
        self.classifier = ContentClassifier(ai_client, profiles)
        self.console = console or Console(stderr=True)
        self.concurrency = max(concurrency, 1)
        self.throttle_sec = max(throttle_sec, 0.0)

    @staticmethod
    def _parse_json_response(response: str) -> Optional[dict]:
        """Try multiple strategies to extract a JSON object from an AI response.

        Returns the parsed dict, or None if all strategies fail.
        """
        return parse_json_response(response)

    async def analyze_batch(self, items: List[ContentItem]) -> List[ContentItem]:
        """
        【已适配 Gemini 免费版优化的批量分析方法】
        将所有抓取到的资讯按每批 130 条切片打包，通过极少次数的 API 请求完成全部数据的打分与摘要。
        """
        if not items:
            return []

        batch_size = 130  # 每批 130 条，300条左右的内容仅需分 2 批发送
        all_analyzed_results = []
        
        # 1. 按照 batch_size 对 items 进行切片
        batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
            console=self.console,
        ) as progress:
            task = progress.add_task("Analyzing Batches", total=len(batches))

            for batch_idx, batch in enumerate(batches):
                # 2. 预先为每个 item 解析好对应的 profile（适配原项目的分类逻辑）
                for item in batch:
                    try:
                        await self.classifier.resolve(item)
                        if item.processing:
                            item.processing.artifacts.clear()
                    except Exception as e:
                        logger.error("Error resolving profile for item %s: %s", item.id, e)

                # 3. 构造轻量级 Payload 数组
                payload_list = []
                for idx, item in enumerate(batch):
                    content_text = ""
                    if item.content:
                        content_text = item.content[:200]
                    payload_list.append({
                        "id": f"{batch_idx}_{idx}",
                        "title": item.title,
                        "snippet": content_text
                    })

                # 4. 构造批量提示词
                system_prompt = "你是一个严谨的信息过滤与摘要助手。请严格返回一个合法的 JSON 数组，不要包含任何 markdown 代码块标记，直接输出 JSON。"
                user_prompt = f"""
下面是一批互联网资讯列表（共 {len(payload_list)} 条）。请逐条评估其价值，并严格输出一个 JSON 数组，格式如下：
[
  {{"id": "0_0", "score": 8.5, "summary": "这里写20-30字的中文精炼总结"}},
  {{"id": "0_1", "score": 4.0, "summary": "无价值内容打低分"}}
]

待评估数据：
{json.dumps(payload_list, ensure_ascii=False)}
"""

                try:
                    # 5. 调用 AI 客户端获取批量响应
                    response = await self.client.complete(
                        system=system_prompt,
                        user=user_prompt,
                    )
                    
                    # 解析返回的 JSON 结果
                    parsed_result = self._parse_json_response(response)
                    if isinstance(parsed_result, list):
                        result_map = {res.get("id"): res for res in parsed_result if isinstance(res, dict) and "id" in res}
                    else:
                        result_map = {}

                    # 6. 将分析结果写回每个 ContentItem 对象
                    for idx, item in enumerate(batch):
                        item_id = f"{batch_idx}_{idx}"
                        if not hasattr(item, 'processing') or item.processing is None:
                            from ..models import ContentProcessing
                            item.processing = ContentProcessing()

                        if item_id in result_map:
                            res_data = result_map[item_id]
                            try:
                                score_val = float(res_data.get("score", 5.0))
                            except (TypeError, ValueError):
                                score_val = 5.0
                                
                            item.processing.analysis = ContentAnalysis(
                                score=score_val,
                                reason=res_data.get("reason", "Batch analyzed"),
                                summary=res_data.get("summary", item.title),
                            )
                        else:
                            item.processing.analysis = ContentAnalysis(
                                score=5.0,
                                reason="Missing in batch response",
                                summary=item.title,
                            )
                        all_analyzed_results.append(item)

                except Exception as e:
                    logger.error("Error in batch analysis batch %d: %s", batch_idx, e)
                    # 异常降级兜底：确保整批数据不丢失
                    for item in batch:
                        if not hasattr(item, 'processing') or item.processing is None:
                            from ..models import ContentProcessing
                            item.processing = ContentProcessing()
                        item.processing.analysis = ContentAnalysis(
                            score=5.0,
                            reason="Batch analysis failed",
                            summary=item.title,
                        )
                        all_analyzed_results.append(item)

                progress.advance(task)

        return all_analyzed_results

    @retry(
        retry=retry_if_exception_type(Exception) & retry_if_not_exception_type(AIProviderUnavailableError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=2, max=10)
    )
    async def _analyze_item(self, item: ContentItem) -> None:
        """保留单条分析方法作为备用兼容接口。"""
        profile = await self.classifier.resolve(item)
        if item.processing:
            item.processing.artifacts.clear()

        content_parts = split_content(item.content)
        selected_content = select_content(
            content_parts.main,
            profile.definition.content.analysis_max_chars,
            profile.definition.content.sampling,
        )
        content_section = f"Content: {selected_content}" if selected_content else ""

        discussion_parts = []
        if content_parts.comments:
            discussion_parts.append(
                f"Community Comments:\n{content_parts.comments[:1500]}"
            )

        meta = item.metadata
        engagement_items = []
        if meta.get("score"):
            engagement_items.append(f"score: {meta['score']}")
        if meta.get("descendants"):
            engagement_items.append(f"{meta['descendants']} comments")
        if meta.get("favorite_count"):
            engagement_items.append(f"{meta['favorite_count']} likes")
        if meta.get("retweet_count"):
            engagement_items.append(f"{meta['retweet_count']} retweets")
        if meta.get("reply_count"):
            engagement_items.append(f"{meta['reply_count']} replies")
        if meta.get("views"):
            engagement_items.append(f"{meta['views']} views")
        if meta.get("bookmarks"):
            engagement_items.append(f"{meta['bookmarks']} bookmarks")
        if meta.get("upvote_ratio"):
            engagement_items.append(f"upvote ratio: {meta['upvote_ratio']:.0%}")
        if engagement_items:
            discussion_parts.append(f"Engagement: {', '.join(engagement_items)}")
        if meta.get("discussion_url"):
            discussion_parts.append(f"Discussion: {meta['discussion_url']}")
        if meta.get("community_note"):
            discussion_parts.append(f"Community Note: {meta['community_note']}")

        discussion_section = "\n".join(discussion_parts) if discussion_parts else ""

        user_prompt = analysis_user_prompt(item, content_section, discussion_section)

        response = await self.client.complete(
            system=analysis_system_prompt(profile),
            user=user_prompt,
        )

        result, failure = self._validate_analysis_response(response)
        if result is None:
            repair_response = await self.client.complete(
                system=analysis_system_prompt(profile),
                user=(
                    user_prompt
                    + "\n\nYour previous response did not satisfy the output contract "
                    f"({failure}). Analyze the item again and return only the required JSON object."
                ),
                temperature=0,
            )
            result, failure = self._validate_analysis_response(repair_response)

        if result is None:
            logger.warning(
                "Could not parse analysis response for %s after one repair attempt (%s), using defaults",
                item.id,
                failure,
            )
            if item.processing:
                item.processing.analysis = ContentAnalysis(
                    score=None,
                    reason="Analysis response parse failed",
                    summary=item.title,
                )
            return

        if item.processing:
            item.processing.analysis = result

    @classmethod
    def _validate_analysis_response(
        cls,
        response: str,
    ) -> tuple[Optional[ContentAnalysis], str]:
        parsed = cls._parse_json_response(response)
        if not isinstance(parsed, dict):
            return None, "response was not a JSON object"
        try:
            result = ContentAnalysis.model_validate(parsed)
        except ValidationError as exc:
            first_error = exc.errors(include_url=False)[0]
            location = ".".join(str(part) for part in first_error["loc"])
            return None, f"invalid field {location or '<root>'}: {first_error['type']}"
        if result.score is None:
            return None, "score is required by the analysis contract"
        return result, ""
