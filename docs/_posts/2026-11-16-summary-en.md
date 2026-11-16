---
layout: default
title: "Horizon Summary: 2026-11-16 (EN)"
date: 2026-11-16
lang: en
---

> From 158 items, 9 important content pieces were selected

---

**AI Creator Radar**
1. [llama.cpp b12441 Released with WebGPU Flash Attention Fixes](#item-ai-creator-1) ⭐️ 5.0/10
2. [llama.cpp b12438 Released](#item-ai-creator-2) ⭐️ 5.0/10
3. [llama.cpp Release b12436](#item-ai-creator-3) ⭐️ 5.0/10
4. [llama.cpp 发布 b12435 版本，优化 Vulkan 后端确定性](#item-ai-creator-4) ⭐️ 5.0/10
5. [llama.cpp 发布 b12433 版本，修复 AMD 设备上的 MUL\_MAT\_ID 崩溃问题](#item-ai-creator-5) ⭐️ 5.0/10
6. [Solana Drops Beta Label](#item-ai-creator-6) ⭐️ 5.0/10
7. [Old Crypto Feud Reignites](#item-ai-creator-7) ⭐️ 5.0/10
8. [Bitcoin Crash Amid Market Context](#item-ai-creator-8) ⭐️ 5.0/10
9. [Singapore and Germany test cross-border payments](#item-ai-creator-9) ⭐️ 5.0/10

---

## AI Creator Radar

<a id="item-ai-creator-1"></a>
### [llama.cpp b12441 Released with WebGPU Flash Attention Fixes](https://github.com/ggml-org/llama.cpp/releases/tag/b12441) ⭐️ 5.0/10

llama.cpp has released version b12441 on November 16, 2026. The update includes a WebGPU fix for per-head flash attention masks, correcting an issue where shaders indexed masks without the head dimension and caused incorrect results for masks with ne\[2\] &gt; 1. It also adjusts shared memory estimates to prevent certain configurations, such as K f16 and V q8\_0, from exceeding workgroup storage limits.

github · github-actions\[bot\] · Nov 16, 14:22

**「Content Angle」** 可做角度：梳理 llama.cpp 在 WebGPU 后端上针对 flash attention 缓存与内存限制的具体修复，探讨其对跨平台推理稳定性的影响。

---

<a id="item-ai-creator-2"></a>
### [llama.cpp b12438 Released](https://github.com/ggml-org/llama.cpp/releases/tag/b12438) ⭐️ 5.0/10

The llama.cpp project has released version b12438, which includes Jinja support for json sort\_keys=true under pull request \#32366. The release provides precompiled binaries for macOS, Linux, Android, and Windows across various hardware backends such as CPU, CUDA, Vulkan, and ROCm. Official binary packages and source build artifacts are available directly through the GitHub release page.

github · github-actions\[bot\] · Nov 16, 12:49

**「Content Angle」** 可做角度：梳理 llama.cpp 版本 b12438 中 Jinja 模版对 json sort\_keys=true 的具体支持与影响，适合关注本地大模型推理及工具链更新的开发者阅读。

---

<a id="item-ai-creator-3"></a>
### [llama.cpp Release b12436](https://github.com/ggml-org/llama.cpp/releases/tag/b12436) ⭐️ 5.0/10

The llama.cpp project has released version b12436, published on November 16, 2026. This release includes a specific fix for Vulkan 32-bit compilation \(\#32275\). Pre-compiled binaries and archives are provided across macOS, Linux, Android, and Windows platforms supporting various hardware configurations such as CPU, CUDA, Vulkan, and ROCm.

github · github-actions\[bot\] · Nov 16, 12:19

**「Content Angle」** 可做角度：关注 llama.cpp 近期针对 Vulkan 32 位编译等底层兼容性问题的持续修复，了解其在跨平台硬件适配上的最新进展。

---

<a id="item-ai-creator-4"></a>
### [llama.cpp 发布 b12435 版本，优化 Vulkan 后端确定性](https://github.com/ggml-org/llama.cpp/releases/tag/b12435) ⭐️ 5.0/10

开源项目 llama.cpp 于 2026 年 11 月 16 日发布了 b12435 版本。本次更新主要针对 Vulkan 后端进行了改进，使 radix top-k 的平局选择（tie selection）实现确定性。通过调整 subgroup 协作、计数与列顺序排序，该改动让 Vulkan 后端的行为与 CUDA 和 Metal 保持一致，并优化了针对 AMD、Intel 和 Nvidia 设备的着色器。

github · github-actions\[bot\] · Nov 16, 11:38

**「内容切入」** 可做角度：从 llama.cpp b12435 版本对 Vulkan 后端 top-k 确定性的优化切入，探讨跨硬件后端（CUDA、Metal 与 Vulkan）在张量运算一致性上的技术细节与进展。

---

<a id="item-ai-creator-5"></a>
### [llama.cpp 发布 b12433 版本，修复 AMD 设备上的 MUL\_MAT\_ID 崩溃问题](https://github.com/ggml-org/llama.cpp/releases/tag/b12433) ⭐️ 5.0/10

开源项目 llama.cpp 于 2026 年 11 月 16 日发布了 b12433 版本。该版本修复了在 AMD 设备上使用特定的 F32、F16 或 BF16 类型时，\`MUL\_MAT\_ID\` 操作因奇数 \`src0\` 列而导致程序中止的问题。受影响的场景主要涉及在混合专家模型（MoE）专家权重上使用秩 1 的 LoRA。新版本通过限制仅在偶数 \`src0\` 列时使用 MMVF 并对其他形状启用现有回退机制来解决该崩溃。

github · github-actions\[bot\] · Nov 16, 11:16

**「为什么值得注意」** 随着越来越多的开发者在 AMD 硬件上运行大语言模型及进行 LoRA 微调，修复 MoE 专家权重相关的崩溃能直接提升在非英伟达硬件上进行复杂模型推理的稳定性。

**「内容切入角度」** 可做角度：从 llama.cpp 最新 b12433 版本对 AMD 设备运算逻辑的调整出发，探讨在本地多硬件部署大模型时，硬件兼容性与特定算子（如 MoE 架构的 LoRA）所面临的兼容挑战与修复进展。

---

<a id="item-ai-creator-6"></a>
### [Solana Drops Beta Label](https://www.coindesk.com/tech/2026/11/16/solana-drops-beta-label-after-more-than-six-years) ⭐️ 5.0/10

Solana has officially dropped its &quot;beta&quot; label after operating under it for more than six years. The network milestone marks a transition in how the core software status is designated. No additional technical specifications or performance metrics were detailed in the available announcement.

rss · CoinDesk · Nov 16, 13:03

**「Why Now」** The change is notable because the &quot;beta&quot; designation had been in place for over six years since the network&\#x27;s early development phases, signaling a symbolic step forward in maturity.

**「Content Angle」** 可做角度：梳理 Solana 运行六年多来从 beta 标签走向正式版本的演进背景与实际网络状态变化。

---

<a id="item-ai-creator-7"></a>
### [Old Crypto Feud Reignites](https://www.coindesk.com/markets/2026/11/16/bitcoin-s-slide-reopens-an-old-feud-between-crypto-s-most-powerful-founders) ⭐️ 5.0/10

OKX founder Star Xu blamed Binance for causing two years of October market crashes, reigniting a public feud between the executives of the two cryptocurrency exchanges. The dispute resurfaced amid a recent slide in bitcoin&\#x27;s price in November 2026. The reported claims highlight ongoing tensions among the leaders of major crypto platforms.

rss · CoinDesk · Nov 16, 12:55

**「Why Now」** The public exchange of blame comes as bitcoin experiences a price slide, bringing historical industry rivalries back into public view.

**「Content Angle」** Content angle: Examine how public disputes between major exchange founders coincide with broader market downturns and influence industry sentiment.

---

<a id="item-ai-creator-8"></a>
### [Bitcoin Crash Amid Market Context](https://www.coindesk.com/daybook-us/2026/11/16/bitcoin-was-supposed-to-gain-as-ai-faltered-but-it-crashed-here-s-why) ⭐️ 5.0/10

Bitcoin recently experienced a price crash despite expectations of gains amid fluctuations in the artificial intelligence sector. The event occurred around November 16, 2026, according to reports analyzing market movements. The decline affected cryptocurrency investors and market observers tracking the correlation between tech sectors and digital assets.

rss · CoinDesk · Nov 16, 12:09

**「Why Now」** This development is notable because it challenges prevailing assumptions about how cryptocurrency markets react when artificial intelligence sector momentum falters.

**「Content Angle」** Content angle: Examining the shifting correlation between artificial intelligence market trends and cryptocurrency price movements based on recent trading data.

---

<a id="item-ai-creator-9"></a>
### [Singapore and Germany test cross-border payments](https://www.coindesk.com/business/2026/11/16/singapore-germany-test-cross-border-payments-to-reduce-settlement-risk) ⭐️ 5.0/10

Singapore and Germany are testing cross-border payments aimed at reducing settlement risk. The initiative involves financial authorities from both regions exploring new payment mechanisms. Further details regarding specific timelines, technologies, or participating institutions were not specified in the available material.

rss · CoinDesk · Nov 16, 11:47

**「Why Now」** This cross-border test highlights ongoing efforts by international financial hubs to address friction and settlement risks in bilateral transactions.

**「Content Angle」** 可做角度：分析新加坡与德国开展跨境外汇或支付测试的具体技术路径及其对降低结算风险的实际意义。

---