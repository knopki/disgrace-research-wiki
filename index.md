# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-06-16 | Total pages: 52

## Entities

- [[microsoft|Microsoft]] — Corporation behind Azure, GitHub Copilot; analyst describes elite partnership programs (MVP, TAP, Partner Engagement Board) and AI transformation via dual programming → AI operator model

- [[vladimir-ivanov|Vladimir Ivanov]] — Turboplanner author; wrote on AI parallelism advantage

- [[frank-rosenblatt|Frank Rosenblatt]] — American psychologist, inventor of the Perceptron, foundational contributor to neural networks and deep learning

- [[anthropic|Anthropic]] — AI safety research company; published Toy Models of Superposition foundational interpretability work
- [[openai|OpenAI]] — American AI research organization; developer of GPT models, ChatGPT, and InstructGPT/RLHF
- [[dario-amodei|Dario Amodei]] — Co-founder and CEO of Anthropic; AI researcher, proponent of democratic AI leadership, author of *Machines of Loving Grace* and *The Adolescence of Technology*

## Concepts

- [[bfs|Breadth-First Search (BFS)]] — graph traversal algorithm exploring level by level; mechanics, complexity, disconnected graphs, applications, and relevance to LLM reasoning analogies

- [[perceptron|Perceptron]] — first neural network architecture; linear binary classifier invented by Rosenblatt that learns through trial and error

- [[innate-parallelism|Innate Parallelism]] — LLMs structurally generate parallel code by architectural design
- [[semantic-fractal|Semantic Fractal]] — how LLMs represent code as branching semantic vectors, not linear instructions
- [[human-sequential-bottleneck|Human Sequential Bottleneck]] — human cognition is linear, making parallel programming disproportionately hard
- [[vibe-coding|Vibe Coding]] — programmer shifts from implementation to directing intent, delegating parallel logic to AI
- [[ai-resource-leveling|AI Resource Leveling]] — AI performs resource leveling with understanding of project technology, not just load balancing
- [[skill-scheduling|Skill Scheduling]] — AI-driven flexible qualification management for project staffing
- [[semantic-interference|Semantic Interference]] — contradictory prompt instructions cause LLMs to produce incoherent "semantic mush"
- [[distributional-semantics|Distributional Semantics]] — Firth's principle that word meaning is entirely determined by context; validated by LLM embeddings
- [[word-embeddings|Word Embeddings]] — how LLMs represent concepts as vectors in high-dimensional space, superposition catastrophe
- [[retrieval-augmented-generation|Retrieval-Augmented Generation (RAG)]] — architectural pattern grounding LLM responses in externally retrieved knowledge
- [[rlhf|RLHF (Reinforcement Learning from Human Feedback)]] — technique for fine-tuning language models with human preferences as reward signal; InstructGPT demonstrated 1.3B model outperforming 175B GPT-3
- [[knowledge-graph|Knowledge Graph]] — structured entity-relationship knowledge base for grounding AI answers
- [[corpus-linguistics|Corpus Linguistics]] — branch of linguistics building annotated text corpora; foundational to NLP training data and RAG knowledge bases

- [[pcam|Purpose Centric Agent Methodology (PCAM)]] — agent management paradigm shifting from deterministic plans to purpose-driven guidance; six principles for autonomous goal-oriented agent architecture, plugin-based scalability, and multi-agent feedback loops

- [[grace|GRACE (Graph-RAG Anchored Code Engineering)]] — framework for deterministic LLM code generation in large contexts; dual-purpose semantic markup serving both generative models (top-down synthesis template) and RAG agents (indexed navigation map); ten principles including Intent-First Architecture, Observable AI Belief State, and Governed Autonomy

- [[flex-prompting|FLEX (Few-shot Logit-Enabled XML Prompting)]] — methodology for reliable SLM control using structured XML prompts, few-shot examples, and logit-based verification; validated on Qwen3-0.6B for agentic tool selection


- [[hallucination-detection-slm|SLM-based Hallucination Detection]] — framework using multiple SLMs (Qwen2 + MiniCPM) for post-hoc hallucination verification of LLM responses in RAG context; sentence-level decomposition, P(yes) token probability, per-model normalization, harmonic mean aggregation


- [[polysemantic-neurons|Polysemantic Neurons]] — neurons that respond to multiple unrelated features; explained by the superposition hypothesis

- [[privileged-basis|Privileged Basis]] — architectural property where activation functions make basis directions special, encouraging feature-neuron alignment

- [[concepts/rational-unified-process|Rational Unified Process (RUP)]] — iterative software development process framework by Rational/IBM; use-case driven, architecture-centric, with four life-cycle phases and six best practices

- [[cognitive-superposition|Cognitive Superposition]] — ability of a cognitive system to co-activate multiple independently acquired representations; backprop-trained DNNs fail at it, brain-constrained networks succeed via cell assemblies

- [[belief-state-geometry|Belief State Geometry]] — linear representation of posterior distributions over hidden states in the transformer residual stream; encodes information about the entire future, not just next-token prediction

- [[positional-encoding|Positional Encoding]] — sinusoidal encoding that gives transformers "3D semantic vision" by fusing position and meaning in a multi-scale coordinate system

- [[contract-programming|Contract Programming]] — Design by Contract adapted for AI-assisted coding; preconditions, postconditions, invariants as semantic shields for LLM agents

- [[semantic-anchors|Semantic Anchors]] — stable comment markers (`# ANCHOR:`) that give AI agents precise semantic coordinates for patching code, overcoming the line-number problem caused by positional encoding
- [[semantic-superposition|Semantic Superposition]] — prompt engineering paradigm leveraging LLMs' ability to hold multiple hypotheses simultaneously, delaying semantic collapse for BFS-like parallel reasoning
- [[superposition|Superposition]] — phenomenon where neural networks represent more features than dimensions by tolerating interference between non-orthogonal feature directions

- [[backpropagation|Backpropagation]] — fundamental algorithm for training multi-layer neural networks by propagating error gradients backwards through the network
- [[lstm|LSTM]] — recurrent architecture with gating mechanisms that solved the vanishing gradient problem for sequential data
- [[residual-connection|Residual Connection]] — skip connections enabling training of very deep networks by creating gradient highways through the network
- [[scaling-laws|Scaling Laws (Neural Language Models)]] — empirical power-law relationships between language model performance and model size, dataset size, and training compute
- [[transformer|Transformer]] — architecture using self-attention and positional encodings that superseded RNNs and became the foundation of modern LLMs
- [[kv-caching|KV Caching]] — inference optimisation caching Key/Value states in auto-regressive transformers to avoid redundant recomputation
- [[mamba|Mamba / SSM]] — state space model architecture with constant-memory state (~24 MB); RAG-driven self-correction via belief state overwriting demonstrated experimentally

- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — training paradigm replacing language CoT with reasoning directly in the continuous latent space of an LLM; enables emergent BFS-like reasoning
- [[sparse-transformer|Sparse Transformer]] — OpenAI architecture replacing quadratic attention with O(n√n) sparse factorized patterns; first to demonstrate self-attention on 1M+ token sequences
- [[longformer|Longformer]] — linear-complexity attention combining sliding window and task-specific global attention; processes documents up to 4K-16K tokens without chunking; SOTA on WikiHop, TriviaQA, arXiv summarization

- [[big-bird|BigBird]] — linear-complexity attention combining random, window, and global tokens; first sparse-attention model with proven universal approximation and Turing completeness (Google Research, NeurIPS 2020); extends to DNA sequence analysis

- [[spargeattn|SpargeAttn]] — universal training-free sparse attention operator accelerating any model inference via two-stage online filter, self-similarity judge, and HilbertCurve permutation; integrates with SageAttention quantization (Zhang et al., Tsinghua/UC Berkeley, ICML 2025)

- [[flash-attention|FlashAttention]] — IO-aware exact attention algorithm using tiling to reduce GPU HBM↔SRAM reads/writes; first Transformer to beat chance on Path-X (16K) and Path-256 (64K) (Dao et al., Stanford, NeurIPS 2022)
- [[rotary-position-embedding|Rotary Position Embedding (RoPE)]] — position encoding via rotation matrices that encodes absolute position while naturally incorporating relative position dependency; dominant PE in post-2023 LLMs (LLaMA, Mistral, Qwen, Gemma) (Su et al., Zhuiyi Technology, arXiv 2021)
- [[switch-transformer|Switch Transformer]] — Mixture-of-Experts architecture simplifying MoE to single-expert routing; enables trillion-parameter sparsely-activated models with constant compute cost; foundational to modern MoE LLMs (Fedus et al., Google, JMLR 2022)
- [[v4a-diff-format|V4A Diff Format]] — context-based, line-number-free diff format designed for LLM agent patch application; used by OpenAI GPT-4.1 for SWE-bench Verified (55% SOTA for non-reasoning models)
- [[chain-of-thought|Chain-of-Thought Prompting (CoT)]] — prompting technique that instructs LLMs to articulate intermediate reasoning steps; improves math/logic performance for large models but harms SLM accuracy by 15–30%+

## Raw Sources

### Articles

- [AI угрожает программистам могуществом параллелизма](raw/articles/2025-06-30-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/) (Vladimir Ivanov, 2025-06-30)
- [Контрактное программирование: Ваш семантический щит в эпоху искусственного интеллекта](raw/articles/2025-07-05-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/) (Vladimir Ivanov, 2025-07-05)
- [AI в управлении проектами — теперь Resource Leveling уже работает](raw/articles/2025-07-01-ai-v-upravlenii-proektami-teper-resource-leveling-uzhe-rab/) (Vladimir Ivanov, 2025-07-01)
- [Семантическая интерференция. Или нажать «газ и тормоз» сразу в промптах](raw/articles/2025-07-01-semanticheskaya-interferenciya-ili-nazhat-gaz-i-tormoz-srazu/) (Vladimir Ivanov, 2025-07-01)
- [Вектора GPT или почему для GPT ваше слово — пустота без контекста](raw/articles/2025-07-02-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/) (Vladimir Ivanov, 2025-07-02)
- [Генерация с дополненной выборкой (RAG)](raw/articles/rag-wikipedia/) (Wikipedia, 2026)
- [Knowledge Graph (Google)](raw/articles/knowledge-graph-google-wikipedia/) (Wikipedia, 2026)
- [Дистрибутивная семантика](raw/articles/distributional-semantics-wikipedia/) (Wikipedia, 2026)
- [Корпусная лингвистика](raw/articles/corpus-linguistics-wikipedia/) (Wikipedia, 2026)
- [Frank Rosenblatt](raw/articles/frank-rosenblatt-wikipedia/) (Wikipedia, 2026)
- [История ИИ: бунтари, гении и научные войны, которые сформировали наш мир](raw/articles/2025-07-03-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/) (Vladimir Ivanov, 2025-07-03)

- [Позиционные кодировки: «объемное зрение» GPT и секреты AI-агентов](raw/articles/2025-07-04-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/) (Vladimir Ivanov, 2025-07-04)

- [Design by Contract](raw/articles/design-by-contract-wikipedia/) (Wikipedia, 2026)
- [Кот Шрёдингера в голове у GPT: Как суперпозиция смыслов меняет правила игры с ИИ](raw/articles/2025-07-06-kot-shredingera-v-golove-u-gpt-kak-superpoziciya-smyslov-men/) (Vladimir Ivanov, 2025-07-06)
- [KV Caching Explained](raw/articles/kv-caching-explained/) (João Lages, Medium, 2023-10-08)

- [OpenAI](raw/articles/openai-wikipedia.md) (Wikipedia, 2026)

- [За кулисами Microsoft: тайные элитные партнерские программы и ИИ-трансформация](raw/articles/2025-07-10-za-kulisami-microsoft-tainye-elitnye-partnerskie-programmy-i/) (Vladimir Ivanov, 2025-07-10)
- [Rational Unified Process](raw/articles/rational-unified-process-wikipedia/) (Wikipedia, 2026)
- [Difference between BFS and DFS](raw/articles/bfs-vs-dfs-gfg/) (GeeksforGeeks)
- [Breadth First Search or BFS for a Graph](raw/articles/bfs-gfg/) (GeeksforGeeks)
- [Методология PCAM: Превращаем AI-агентов из рабов в партнеров](raw/articles/2025-09-11-metodologiya-pcam-prevraschaem-ai-agentov-iz-rabov-v-partner/) (Vladimir Ivanov, 2025-09-11)
- [GRACE: Фреймворк создания кода LLM в больших контекстах](raw/articles/2025-09-13-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/) (Vladimir Ivanov, 2025-09-13)

- [Причины наблюдаемого провала малых SLM против LLM на MoE в AI-агентах](raw/articles/2025-09-14-ivanov-prichiny-nabludaemogo-provala-malyh-slm-protiv-llm-na-moe-v/) (Vladimir Ivanov, 2025-09-14)
- [Оптимизация управления ИИ агентами на SLM через FLEX](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/) (Vladimir Ivanov, 2025-09-18)
- [Преодоление галлюцинаций в Mamba-моделях](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/) (Vladimir Ivanov, 2025-09-21)
- [Семантическая разметка GRACE как нативный интерфейс для Mamba-моделей](raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/) (Vladimir Ivanov, 2025-09-21)
- [GPT-4.1 Prompting Guide](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md) (OpenAI, 2026)

### Papers

- [Toy Models of Superposition](raw/papers/2022-09-elhage-toy-models-superposition/) (Anthropic Transformer Circuits Thread, 2022)
- [Training Compute-Optimal Large Language Models](raw/papers/2022-03-hoffmann-chinchilla/) (Jordan Hoffmann et al., DeepMind, arXiv, 2022)
- [Training language models to follow instructions with human feedback](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md) — PDF at [2203.02155.pdf](raw/papers/2022-03-ouyang-instructgpt/2203.02155.pdf) (Long Ouyang et al., OpenAI, NeurIPS 2022)
- [On the ability of standard and brain-constrained DNNs to support cognitive superposition](raw/papers/2024-02-garagnani-cognitive-superposition/) (Max Garagnani, Cognitive Neurodynamics, 2024)
- [Transformers Represent Belief State Geometry in their Residual Stream](raw/papers/2024-05-shai-belief-state-geometry/) (Adam Shai et al., NeurIPS 2024)
- [Training Large Language Models to Reason in a Continuous Latent Space](raw/papers/2024-12-hao-coconut/) — abstract, full PDF, and plain-text at [index.md](raw/papers/2024-12-hao-coconut/hao2025coconut.md) (Shibo Hao et al., FAIR at Meta / UC San Diego, arXiv, COLM 2025)
- [Generating Long Sequences with Sparse Transformers](raw/papers/2019-04-child-sparse-transformer/1904.10509.pdf) — abstract and details at [child2019sparse](raw/papers/2019-04-child-sparse-transformer/child2019sparse.md) (Rewon Child et al., OpenAI, 2019)
- [Scaling Laws for Neural Language Models](raw/papers/2020-01-kaplan-scaling-laws/kaplan2020scaling.md) — abstract and PDF at [2001.08361.pdf](raw/papers/2020-01-kaplan-scaling-laws/2001.08361.pdf) (Jared Kaplan et al., OpenAI/arXiv, 2020)
- [Longformer: The Long-Document Transformer](raw/papers/2020-04-beltagy-longformer/beltagy2020longformer.md) (Iz Beltagy et al., Allen Institute for AI, 2020)
- [Big Bird: Transformers for Longer Sequences](raw/papers/2020-07-zaheer-big-bird/zaheer2020bigbird.md) (Manzil Zaheer et al., Google Research, NeurIPS 2020)
- [SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference](raw/papers/2025-02-zhang-spargeattention/2502.18137.pdf) — details at [zhang2025spargeattn](raw/papers/2025-02-zhang-spargeattention/zhang2025spargeattn.md) (Jintao Zhang et al., Tsinghua/UC Berkeley, ICML 2025)
- [Small Language Models are the Future of Agentic AI](raw/papers/2025-06-belcak-slm-agentic-ai/belcak2025slm.md) — PDF at [2506.02153.pdf](raw/papers/2025-06-belcak-slm-agentic-ai/2506.02153.pdf) (Peter Belcak et al., NVIDIA Research, arXiv June 2025)
- [CoT Harms Performance of Rather Smaller Language Models](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md) — PDF at [shim2024cotharms.pdf](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.pdf) (Jihoo Shim, Shin Dong Ho, Jeongwon Kim, IEOM 1st World Congress 2024)
- [Hallucination Detection with Small Language Models](raw/papers/2025-06-24-cheung-hallucination-detection-slm/2506.22486.pdf) — details at [index.md](raw/papers/2025-06-24-cheung-hallucination-detection-slm/cheung2025hallucination.md) (Ming Cheung, dBeta Labs, IEEE ICDE Workshop 2025)
- [Attention Is All You Need](raw/papers/2017-06-vaswani-attention-is-all-you-need/1706.03762.pdf) — details at [vaswani2017attention](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md) (Ashish Vaswani et al., Google Research/NIPS, 2017)
- [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](raw/papers/2022-05-dao-flashattention/2205.14135.pdf) — details at [index.md](raw/papers/2022-05-dao-flashattention/dai2022flashattention.md) (Tri Dao et al., Stanford, NeurIPS 2022)
- [RoFormer: Enhanced Transformer with Rotary Position Embedding](raw/papers/2021-04-su-roformer/2104.09864.pdf) — details at [su2021rope.md](raw/papers/2021-04-su-roformer/su2021rope.md) (Jianlin Su et al., Zhuiyi Technology, arXiv 2021)
- [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](raw/papers/2021-01-fedus-switch-transformers/2101.03961.pdf) — details at [fedus2022switch.md](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md) (William Fedus et al., Google, JMLR 2022)
- [SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference](raw/papers/2025-02-zhang-spargeattention/2502.18137.pdf) — details at [zhang2025spargeattn](raw/papers/2025-02-zhang-spargeattention/zhang2025spargeattn.md) (Jintao Zhang et al., Tsinghua/UC Berkeley, ICML 2025)

## Comparisons

- [[bfs-vs-dfs|BFS vs DFS]] — Standard comparison of graph traversal algorithms BFS and DFS; reference anchor for LLM reasoning analogies
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — side-by-side comparison of Belcak et al. (NVIDIA, pro-SLM+heterogeneous) and Ivanov (pro-MoE/cost-field-flattening) positions; benchmarks, market data, and synthesis

## Queries
