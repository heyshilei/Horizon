# Horizon 每日速递 - 2026-11-16

> 从 158 条内容中筛选出 9 条重要资讯。

---

**AI 创作者雷达**
1. [llama.cpp 发布 b12441 版本：修复 WebGPU Flash Attention 掩码及内存估算问题](#item-ai-creator-1) ⭐️ 5.0/10
2. [llama.cpp 发布 b12438 版本](#item-ai-creator-2) ⭐️ 5.0/10
3. [llama.cpp 发布 b12436 版本：修复 Vulkan 32 位编译问题](#item-ai-creator-3) ⭐️ 5.0/10
4. [llama.cpp 发布 b12435 版本，优化 Vulkan 后端确定性](#item-ai-creator-4) ⭐️ 5.0/10
5. [llama.cpp 发布 b12433 版本](#item-ai-creator-5) ⭐️ 5.0/10
6. [Solana 移除 Beta 标签](#item-ai-creator-6) ⭐️ 5.0/10
7. [OKX 与币安创始人因 10 月行情爆发口水战](#item-ai-creator-7) ⭐️ 5.0/10
8. [比特币与 AI 板块走势分析](#item-ai-creator-8) ⭐️ 5.0/10
9. [新加坡与德国测试跨境支付以降低结算风险](#item-ai-creator-9) ⭐️ 5.0/10

---

## AI 创作者雷达

<a id="item-ai-creator-1"></a>
### [llama.cpp 发布 b12441 版本：修复 WebGPU Flash Attention 掩码及内存估算问题](https://github.com/ggml-org/llama.cpp/releases/tag/b12441) ⭐️ 5.0/10

开源项目 llama.cpp 于 2026 年 11 月 16 日发布了 b12441 版本。该版本主要修复了 WebGPU 后端中未包含头部维度的 flash attention 掩码问题，避免了多头掩码产生错误结果，并将参数缓冲区扩展至 256 字节以容纳新字段。同时，新版本调整了共享内存估算与向量 KV 瓦片（tile）规则，解决了特定配置下超出工作组存储限制的问题。

github · github-actions\[bot\] · 11月16日 14:22

**「为什么值得注意」** 此次更新直接修复了 WebGPU 后端在处理带有多个头（head）的 flash attention 掩码时的计算错误，并优化了特定量化组合下的内存溢出问题，提升了 WebGPU 在本地大模型推理时的稳定性和兼容性。

**「内容切入角度」** 可做角度：从 llama.cpp b12441 版本对 WebGPU 闪电注意力的修复切入，关注本地大模型在浏览器或 WebGPU 运行时中的兼容性与性能调优进展。

---

<a id="item-ai-creator-2"></a>
### [llama.cpp 发布 b12438 版本](https://github.com/ggml-org/llama.cpp/releases/tag/b12438) ⭐️ 5.0/10

开源大模型推理项目 llama.cpp 于 2026 年 11 月 16 日发布了 b12438 版本。该版本的主要更新内容为在 jinja 模块中支持了 json sort\_keys=true（对应 PR \#32366）。同时，官方提供了覆盖 macOS、Linux、Android、Windows 等多平台、多硬件后端的预编译二进制文件与相关构建支持。

github · github-actions\[bot\] · 11月16日 12:49

**「内容切入」** 可做角度：从 llama.cpp 最新版本对 jinja 模板中 json sort\_keys=true 的支持切入，探讨该功能如何帮助开发者在本地大模型推理中更好地控制格式化输出与工具调用时的参数稳定性。

---

<a id="item-ai-creator-3"></a>
### [llama.cpp 发布 b12436 版本：修复 Vulkan 32 位编译问题](https://github.com/ggml-org/llama.cpp/releases/tag/b12436) ⭐️ 5.0/10

开源大模型推理工具 llama.cpp 发布了 b12436 版本。本次更新主要修复了 Vulkan 的 32 位编译问题（\#32275）。版本同时提供了面向 macOS、Linux、Android 以及 Windows 等多个平台的预编译二进制文件与后端支持。

github · github-actions\[bot\] · 11月16日 12:19

**「内容切入」** 可做角度：从 llama.cpp b12436 版本对 Vulkan 32 位编译的修复切入，探讨跨平台大模型推理在不同架构与老旧环境下的兼容性适配挑战。

---

<a id="item-ai-creator-4"></a>
### [llama.cpp 发布 b12435 版本，优化 Vulkan 后端确定性](https://github.com/ggml-org/llama.cpp/releases/tag/b12435) ⭐️ 5.0/10

llama.cpp 项目于 2026 年 11 月 16 日发布了 b12435 版本。本次更新主要针对 Vulkan 后端进行了修改，使 radix top-k 的平局选择（tie selection）变为确定性行为，避免了以往因线程调度导致保留列不确定的问题。同时，该版本对 AMD、Intel 和 Nvidia 的相关着色器进行了性能优化。

github · github-actions\[bot\] · 11月16日 11:38

**「内容切入」** 可做角度：从 llama.cpp 最新 b12435 版本切入，关注其 Vulkan 后端如何通过调整子群组计数与排序逻辑实现 top-k 选择的确定性，分析这对跨硬件推理的一致性意味着什么。

---

<a id="item-ai-creator-5"></a>
### [llama.cpp 发布 b12433 版本](https://github.com/ggml-org/llama.cpp/releases/tag/b12433) ⭐️ 5.0/10

llama.cpp 项目于 2026 年 11 月 16 日发布了 b12433 版本。该版本修复了在 AMD 设备上使用特定数据类型时，MUL\_MAT\_ID 算子因奇数 src0 列数引发的中止问题（\#32385）。此前该算子在处理不超过 8 个 token、且 src0 为 F32、F16 或 BF16 类型时会默认使用 MMVF，由于 MMVF 要求偶数的 ne\[0\]，导致在混合专家模型（MoE）专家权重上使用秩为 1 的 LoRA 时出现崩溃。新版本限制了仅在偶数 ne\[0\] 时使用 MMVF，其他形状则采用原有的降级方案。

github · github-actions\[bot\] · 11月16日 11:16

**「为什么值得关注」** 该修复直接解决了在 AMD 硬件上运行 MoE 模型结合 LoRA 适配器时会导致程序异常中止的已知缺陷。它提升了 AMD 设备在特定模型架构运行时的稳定性。

**「内容切入点」** 可做角度：梳理 llama.cpp 近期针对异构硬件（如 AMD ROCm）及混合专家模型兼容性的适配进展。

---

<a id="item-ai-creator-6"></a>
### [Solana 移除 Beta 标签](https://www.coindesk.com/tech/2026/11/16/solana-drops-beta-label-after-more-than-six-years) ⭐️ 5.0/10

区块链网络 Solana 在经历六年多的运行后，正式去掉了“Beta”（测试）标签。这一变动标志着该网络在经历多年的测试阶段后进入了一个新的发展阶段。具体的技术改进或受影响的生态细节尚未在当前信息中披露。

rss · CoinDesk · 11月16日 13:03

**「为什么值得关注」** 维持了六年多的“Beta”标签被移除，标志着 Solana 核心开发团队对该网络长期稳定性的正式确认。这改变了外界对其处于测试阶段的认知。

**「内容切入角度」** 可做角度：梳理 Solana 运行六年多以来移除“Beta”标签的背景，探讨其主网成熟度与过去网络稳定性的演变。

---

<a id="item-ai-creator-7"></a>
### [OKX 与币安创始人因 10 月行情爆发口水战](https://www.coindesk.com/markets/2026/11/16/bitcoin-s-slide-reopens-an-old-feud-between-crypto-s-most-powerful-founders) ⭐️ 5.0/10

比特币近期出现价格下跌，重新引燃了加密货币行业高管之间的旧日恩怨。OKX 创始人徐明星（Star Xu）公开指责币安导致了过去两年中发生在 10 月的市场崩盘。目前双方的言论主要停留在高层争端层面，具体的市场影响与因果关系尚无定论。

rss · CoinDesk · 11月16日 12:55

**「为什么在当下值得注意」** 随着比特币近期价格下滑，行业头部交易所创始人的公开指责将过往的竞争矛盾直接推到了台前，放大了市场对当前行情波动的情绪反应。

**「内容切入角度」** 可做角度：从 OKX 与币安创始人的公开言论出发，盘点头部交易所高管公开摩擦的背景及其对市场情绪的潜在映射。

---

<a id="item-ai-creator-8"></a>
### [比特币与 AI 板块走势分析](https://www.coindesk.com/daybook-us/2026/11/16/bitcoin-was-supposed-to-gain-as-ai-faltered-but-it-crashed-here-s-why) ⭐️ 5.0/10

根据 2026 年 11 月 16 日发布的一篇报道，比特币在原本预期因人工智能板块走弱而上涨的背景下，反而出现了下跌。文章探讨了导致这一价格下跌的具体原因及相关市场背景。受影响的主要是加密货币市场的投资者以及关注宏观资产轮动的群体。目前材料中未包含更多可验证的详细价格数据或技术指标。

rss · CoinDesk · 11月16日 12:09

**「为什么值得关注」** 该报道揭示了加密货币与人工智能板块之间预期的资产轮动失效，这为观察当前宏观市场风险偏好提供了最新的现实案例。

**「内容切入点」** 可做角度：梳理市场此前对“AI 走弱资金流向加密货币”的预期，并结合本次比特币下跌的实际情况，探讨宏观资产联动的复杂性。

---

<a id="item-ai-creator-9"></a>
### [新加坡与德国测试跨境支付以降低结算风险](https://www.coindesk.com/business/2026/11/16/singapore-germany-test-cross-border-payments-to-reduce-settlement-risk) ⭐️ 5.0/10

新加坡与德国于 2026 年 11 月 16 日开始测试跨境支付，旨在降低结算风险。该测试涉及两国的相关支付结算环节，具体受影响的机构和场景以官方后续公布为准。

rss · CoinDesk · 11月16日 11:47

**「为什么值得关注」** 两国金融或支付管理机构在当前时间节点启动跨境支付测试，反映出跨国结算风险的控制正受到实际关注，已发生的变化是测试的正式开展，其长远影响仍有待观察。

**「内容切入角度」** 可做角度：梳理新加坡与德国此次跨境支付测试的具体背景与结算机制，探讨其在降低跨国交易结算风险方面的潜在作用。

---

