# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-07-11 | Total pages: 88

## Entities

- [[microsoft|Microsoft]] — Corporation behind Azure, GitHub Copilot; analyst describes elite partnership programs (MVP, TAP, Partner Engagement Board) and AI transformation via dual programming → AI operator model

- [[vladimir-ivanov|Vladimir Ivanov]] — Turboplanner author; wrote on AI parallelism advantage

- [[frank-rosenblatt|Frank Rosenblatt]] — American psychologist, inventor of the Perceptron, foundational contributor to neural networks and deep learning

- [[stephen-robertson|Stephen Robertson]] — British IR researcher; architect of the probabilistic model of IR and lead developer of BM25 ranking function and Okapi system
- [[karen-sparck-jones|Karen Sparck Jones]] — British computer scientist, introduced IDF (inverse document frequency) and co-developed the Robertson-Sparck Jones relevance weight with Stephen Robertson

- [[anthropic|Anthropic]] — AI safety research company; published Toy Models of Superposition foundational interpretability work
- [[openai|OpenAI]] — American AI research organization; developer of GPT models, ChatGPT, DALL-E, Sora, and OpenAI Codex
- [[codex|Codex]] — OpenAI's GPT model fine-tuned on GitHub code; introduces HumanEval benchmark and pass@k metric for functional correctness; powers GitHub Copilot
- [[dario-amodei|Dario Amodei]] — Co-founder and CEO of Anthropic; AI researcher, proponent of democratic AI leadership, author of *Machines of Loving Grace* and *The Adolescence of Technology*
- [[deepmind|DeepMind]] — British AI research lab (acquired by Google, 2014); contributor to scaling laws (Chinchilla) and automated LM safety evaluation (red teaming)
- [[flan|FLAN (Finetuned Language Net)]] — 137B instruction-tuned language model by Google Research; demonstrates that instruction tuning on 62 NLP datasets enables zero-shot generalization to unseen tasks, outperforming zero-shot GPT-3 on 20/25 datasets
- [[geoffrey-hinton|Geoffrey Hinton]] — British-Canadian cognitive psychologist and computer scientist; one of the "godfathers of deep learning"; co-popularised backpropagation (1986), introduced knowledge distillation (2015), inventor of dropout; Turing Award (2018), Nobel Prize in Physics (2024)

- [[noam-shazeer|Noam Shazeer]] — Google researcher; co-inventor of the Transformer, foundational formulations of Sparsely-Gated MoE and Multi-Query Attention, and proposed GLU variants (SwiGLU, GEGLU, ReGLU) that became the default Transformer FFN activation

## Concepts

- [[alibi|ALiBi (Attention with Linear Biases)]] — position method eliminating positional embeddings; biases query-key attention scores with a linearly decreasing distance penalty; enables training on short sequences (L=512/1024) with extrapolation to 10,000+ tokens; 11% faster and 11% less memory than sinusoidal at same perplexity (Press et al., UW / FAIR / AI2, ICLR 2022)

- [[attention-head-pruning|Attention Head Pruning]] — Voita et al. (2019) show most Transformer encoder self-attention heads can be pruned; the surviving heads play specialized interpretable roles (positional, syntactic, rare words)

- [[bert-attention-analysis|BERT Attention Analysis]] — Clark et al. (2019) systematic analysis of BERT's 144 attention heads: syntactic specialization (dobj 87%, det 94%, pobj 76%), [SEP] as learned no-op, coreference in head 5-4 (65%), attention probing achieves 77 UAS; heads cluster by layer
- [[bfs|Breadth-First Search (BFS)]] — graph traversal algorithm exploring level by level; mechanics, complexity, disconnected graphs, applications, and relevance to LLM reasoning analogies

- [[perceptron|Perceptron]] — first neural network architecture; linear binary classifier invented by Rosenblatt that learns through trial and error

- [[innate-parallelism|Innate Parallelism]] — LLMs structurally generate parallel code by architectural design
- [[semantic-fractal|Semantic Fractal]] — how LLMs represent code as branching semantic vectors, not linear instructions
- [[human-sequential-bottleneck|Human Sequential Bottleneck]] — human cognition is linear, making parallel programming disproportionately hard
- [[in-context-learning|In-Context Learning]] — paradigm where language models adapt to tasks purely through conditioning context without gradient updates; systematically defined and studied at scale by GPT-3 across zero-shot, one-shot, and few-shot settings; meta-learning framing where pre-training is the outer loop and in-context conditioning is the inner loop
- [[instruction-tuning|Instruction Tuning]] — technique improving zero-shot learning by fine-tuning LMs on diverse NLP tasks verbalized as natural language instructions; introduced by FLAN (Wei et al., Google, ICLR 2022); bridges pretrain-finetune and prompting paradigms; benefits emerge only at sufficient scale (≥68B)
- [[self-instruct|Self-Instruct]] — framework for bootstrapping instruction-following from a model's own generations; generates 52k diverse instructions from 175 seed tasks, achieving 33% absolute improvement on SuperNI and nearly matching InstructGPT_001 without human annotations (Wang et al., UW/AI2, ACL 2023)
- [[vibe-coding|Vibe Coding]] — programmer shifts from implementation to directing intent, delegating parallel logic to AI
- [[ai-resource-leveling|AI Resource Leveling]] — AI performs resource leveling with understanding of project technology, not just load balancing
- [[skill-scheduling|Skill Scheduling]] — AI-driven flexible qualification management for project staffing
- [[semantic-interference|Semantic Interference]] — contradictory prompt instructions cause LLMs to produce incoherent "semantic mush"
- [[distributional-semantics|Distributional Semantics]] — Firth's principle that word meaning is entirely determined by context; validated by LLM embeddings
- [[word-embeddings|Word Embeddings]] — how LLMs represent concepts as vectors in high-dimensional space, superposition catastrophe
- [[retrieval-augmented-generation|Retrieval-Augmented Generation (RAG)]] — architectural pattern grounding LLM responses in externally retrieved knowledge; introduced by Lewis et al. (FAIR, NeurIPS 2020) as a hybrid parametric (BART) + non-parametric (DPR index) memory architecture with two marginalisation formulations (RAG-Sequence, RAG-Token)
- [[rlhf|RLHF (Reinforcement Learning from Human Feedback)]] — technique for fine-tuning language models with human preferences as reward signal; InstructGPT demonstrated 1.3B model outperforming 175B GPT-3
- [[reward-model-overoptimization|Reward Model Overoptimization Scaling Laws]] — empirical scaling laws characterizing how proxy reward model optimization degrades ground-truth performance via Goodhart's law; functional forms for BoN and RL, smooth coefficient scaling with RM parameters (Gao, Schulman & Hilton, OpenAI, 2022)
- [[rome-model-editing|ROME (Rank-One Model Editing)]] — method for editing factual associations in GPT via rank-one MLP weight updates; locates decisive mid-layer MLP computations via Causal Tracing and inserts new facts with both generalization and specificity (Meng et al., MIT / Northeastern / Technion, NeurIPS 2022)
- [[knowledge-graph|Knowledge Graph]] — structured entity-relationship knowledge base for grounding AI answers
- [[knowledge-neurons|Knowledge Neurons]] — specific FFN neurons causally responsible for expressing particular factual knowledge in pretrained Transformers; identified via integrated gradients attribution (Dai et al., Microsoft, ACL 2022)
- [[corpus-linguistics|Corpus Linguistics]] — branch of linguistics building annotated text corpora; foundational to NLP training data and RAG knowledge bases

- [[pcam|Purpose Centric Agent Methodology (PCAM)]] — agent management paradigm shifting from deterministic plans to purpose-driven guidance; six principles for autonomous goal-oriented agent architecture, plugin-based scalability, and multi-agent feedback loops

- [[grace|GRACE (Graph-RAG Anchored Code Engineering)]] — framework for deterministic LLM code generation in large contexts; dual-purpose semantic markup serving both generative models (top-down synthesis template) and RAG agents (indexed navigation map); ten principles including Intent-First Architecture, Observable AI Belief State, and Governed Autonomy

- [[flex-prompting|FLEX (Few-shot Logit-Enabled XML Prompting)]] — methodology for reliable SLM control using structured XML prompts, few-shot examples, and logit-based verification; validated on Qwen3-0.6B for agentic tool selection
- [[entities/gpt-3|GPT-3]] — 175B parameter autoregressive language model; demonstrated that scaling up LMs dramatically improves task-agnostic [[in-context-learning|in-context learning]] performance; systematic evaluation across zero/one/few-shot settings on dozens of NLP benchmarks; first systematic data contamination analysis for large-scale LMs
- [[glu-variants|GLU Variants (GEGLU, SwiGLU, ReGLU)]] — gated feed-forward variants replacing the Transformer FFN activation; GEGLU and SwiGLU achieve best perplexity; SwiGLU became the default FFN activation in post-2022 LLMs (LLaMA, PaLM, Gemma, Mistral, Qwen)



- [[gelu|Gaussian Error Linear Unit (GELU)]] — activation function introduced by Hendrycks & Gimpel (2016); probabilistically motivated xΦ(x) with smooth curvature; default activation in BERT and GPT due to improved gradient flow and empirical gains over ReLU/ELU


- [[hallucination-detection-slm|SLM-based Hallucination Detection]] — framework using multiple SLMs (Qwen2 + MiniCPM) for post-hoc hallucination verification of LLM responses in RAG context; sentence-level decomposition, P(yes) token probability, per-model normalization, harmonic mean aggregation

- [[humaneval|HumanEval]] — benchmark of 164 hand-written programming problems for measuring functional correctness of code synthesis from docstrings; introduced by OpenAI with [[codex|Codex]]; uses pass@k unbiased estimator; created to avoid data contamination by not scraping existing sources


- [[polysemantic-neurons|Polysemantic Neurons]] — neurons that respond to multiple unrelated features; explained by the superposition hypothesis

- [[privileged-basis|Privileged Basis]] — architectural property where activation functions make basis directions special, encouraging feature-neuron alignment

- [[concepts/rational-unified-process|Rational Unified Process (RUP)]] — iterative software development process framework by Rational/IBM; use-case driven, architecture-centric, with four life-cycle phases and six best practices
- [[red-teaming|Automated Red Teaming of Language Models]] — using one LM to automatically generate adversarial test cases and detect harmful behaviors in another LM; introduced by Perez et al. (DeepMind, 2022); uncovered tens of thousands of offensive replies, data leakage, and distributional bias in a 280B Gopher chatbot

- [[cognitive-superposition|Cognitive Superposition]] — ability of a cognitive system to co-activate multiple independently acquired representations; backprop-trained DNNs fail at it, brain-constrained networks succeed via cell assemblies

- [[belief-state-geometry|Belief State Geometry]] — linear representation of posterior distributions over hidden states in the transformer residual stream; encodes information about the entire future, not just next-token prediction

- [[positional-encoding|Positional Encoding]] — sinusoidal encoding that gives transformers "3D semantic vision" by fusing position and meaning in a multi-scale coordinate system

- [[contract-programming|Contract Programming]] — Design by Contract adapted for AI-assisted coding; preconditions, postconditions, invariants as semantic shields for LLM agents

- [[semantic-anchors|Semantic Anchors]] — stable comment markers (`# ANCHOR:`) that give AI agents precise semantic coordinates for patching code, overcoming the line-number problem caused by positional encoding
- [[semantic-superposition|Semantic Superposition]] — prompt engineering paradigm leveraging LLMs' ability to hold multiple hypotheses simultaneously, delaying semantic collapse for BFS-like parallel reasoning
- [[superposition|Superposition]] — phenomenon where neural networks represent more features than dimensions by tolerating interference between non-orthogonal feature directions

- [[backpropagation|Backpropagation]] — fundamental algorithm for training multi-layer neural networks by propagating error gradients backwards through the network
- [[byte-pair-encoding|Byte Pair Encoding (BPE)]] — subword tokenization algorithm learning a fixed-size vocabulary of variable-length character sequences; introduced BPE to NLP and became the foundation of all modern LLM tokenizers (Sennrich, Haddow & Birch, ACL 2016)
- [[bert|BERT]] — bidirectional encoder-only Transformer pre-trained via masked language modeling and next sentence prediction
- [[lstm|LSTM]] — recurrent architecture with gating mechanisms that solved the vanishing gradient problem for sequential data
- [[residual-connection|Residual Connection]] — skip connections enabling training of very deep networks by creating gradient highways through the network
- [[scaling-laws|Scaling Laws (Neural Language Models)]] — empirical power-law relationships between language model performance and model size, dataset size, and training compute
- [[transformer|Transformer]] — architecture using self-attention and positional encodings that superseded RNNs and became the foundation of modern LLMs
- [[kv-caching|KV Caching]] — inference optimisation caching Key/Value states in auto-regressive transformers to avoid redundant recomputation
- [[matryoshka-representation-learning|Matryoshka Representation Learning (MRL)]] — training technique producing a single embedding whose first m dimensions form a standalone effective representation for any m ∈ [d]; enables up to 14× compute savings in classification and retrieval via coarse-to-fine nesting (Kusupati et al., UW/Google, NeurIPS 2022)
- [[multi-query-attention|Multi-Query Attention (MQA)]] — attention variant sharing keys and values across all heads to reduce KV cache size and memory bandwidth; Shazeer (2019) achieves 12× decoder speedup
- [[grouped-query-attention|Grouped-Query Attention (GQA)]] — interpolation between MHA and MQA; partitions query heads into G groups each sharing one K/V head; uptrained from MHA checkpoints at 5% compute; quality ≈ MHA at ~5× MQA speed; used in LLaMA 2/3, Mistral (Ainslie et al., Google, EMNLP 2023)
- [[mixture-of-experts|Mixture-of-Experts (MoE)]] — neural architecture scaling capacity via sparse expert activation; decouples parameter count from computational cost; foundational formulation by Shazeer et al. (2017) with noisy top-k gating, 137B parameter models; evolved into Switch Transformer and modern MoE LLMs
- [[switch-transformer|Switch Transformer]] — MoE Transformer substituting dense FFN with k=1 single-expert routing; 7× pretraining speedup over T5, trillion-parameter models; introduced selective bfloat16 precision and expert capacity (Fedus, Zoph & Shazeer, Google, JMLR 2022)
- [[mamba|Mamba / SSM]]

- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — training paradigm replacing language CoT with reasoning directly in the continuous latent space of an LLM; enables emergent BFS-like reasoning
- [[sparse-transformer|Sparse Transformer]] — OpenAI architecture replacing quadratic attention with O(n√n) sparse factorized patterns; first to demonstrate self-attention on 1M+ token sequences
- [[speculative-decoding|Speculative Decoding]] — inference acceleration algorithm generating multiple tokens per serial model invocation by drafting candidates with a fast approximation model and verifying them with the target model in parallel; guarantees identical output distribution; 2–3× walltime speedup on T5-XXL without retraining or architecture changes (Leviathan, Kalman & Matias, Google, ICML 2023)
- [[longformer|Longformer]]
- [[lora|LoRA (Low-Rank Adaptation)]] — parameter-efficient fine-tuning method freezing pre-trained weights and injecting trainable low-rank matrices into Transformer layers; reduces GPT-3 175B trainable parameters by 10,000× with zero inference latency (Hu et al., Microsoft, ICLR 2022)

 — linear-complexity attention combining sliding window and task-specific global attention; processes documents up to 4K-16K tokens without chunking; SOTA on WikiHop, TriviaQA, arXiv summarization

- [[big-bird|BigBird]] — linear-complexity attention combining random, window, and global tokens; first sparse-attention model with proven universal approximation and Turing completeness (Google Research, NeurIPS 2020); extends to DNA sequence analysis

- [[bm25|BM25]] — family of term-weighting functions for probabilistic IR; unified BM11/BM15 with tunable document length normalization; became the standard ranking function in Lucene, Elasticsearch, and Solr; introduced by Robertson et al. at TREC-3 (1995)

- [[s4-structured-state-spaces|S4 (Structured State Space Sequence Model)]] — first computationally practical deep SSM; NPLR parameterization reducing SSM computation from O(N²L) to Õ(N+L); SotA on LRA (86.09% avg, first to solve Path-X), raw speech (98.32%), and competitive with Transformers on WikiText-103 while 60× faster at generation; foundational to Mamba (Gu, Goel & Ré, Stanford, ICLR 2022 Outstanding Paper HM)

- [[flash-attention|FlashAttention]] — IO-aware exact attention algorithm using tiling to reduce GPU HBM↔SRAM reads/writes; first Transformer to beat chance on Path-X (16K) and Path-256 (64K) (Dao et al., Stanford, NeurIPS 2022)
- [[rotary-position-embedding|Rotary Position Embedding (RoPE)]] — position encoding via rotation matrices that encodes absolute position while naturally incorporating relative position dependency; dominant PE in post-2023 LLMs (LLaMA, Mistral, Qwen, Gemma) (Su et al., Zhuiyi Technology, arXiv 2021)
- [[switch-transformer|Switch Transformer]] — Mixture-of-Experts architecture simplifying MoE to single-expert routing; enables trillion-parameter sparsely-activated models with constant compute cost; foundational to modern MoE LLMs (Fedus et al., Google, JMLR 2022)
- [[v4a-diff-format|V4A Diff Format]] — context-based, line-number-free diff format designed for LLM agent patch application; used by OpenAI GPT-4.1 for SWE-bench Verified (55% SOTA for non-reasoning models)
- [[chain-of-thought|Chain-of-Thought Prompting (CoT)]] — prompting technique that instructs LLMs to articulate intermediate reasoning steps; introduced by Wei et al. (Google, NeurIPS 2022) demonstrating CoT as an emergent ability of model scale; improves math/logic performance for large models (100B+) but harms SLM accuracy by 15–30%+
- [[self-consistency|Self-Consistency]] — decoding strategy replacing greedy decoding in CoT with sample-and-marginalise over diverse reasoning paths; GSM8K +17.9%, SVAMP +11.0%, AQuA +12.2% on PaLM-540B; unsupervised, no training required (Wang et al., Google, ICLR 2023)
- [[constitutional-ai|Constitutional AI (CAI)]] — method for training harmless AI assistants via self-critique, revision, and RLAIF using a written constitution; replaces human harmlessness labels with AI feedback guided by ~10-15 principles; achieves Pareto improvement in helpfulness-harmlessness tradeoff (Bai et al., Anthropic, arXiv 2022)
- [[direct-preference-optimization|Direct Preference Optimization (DPO)]]
- [[ffn-key-value-memories|Transformer FFN as Key-Value Memories]] — transformer feed-forward layers operate as unnormalized key-value memories where keys detect input patterns and values induce output distributions; lower layers capture shallow patterns, upper layers semantic ones (Geva et al., EMNLP 2021)
- [[sentencepiece|SentencePiece]] — language-independent subword tokenizer training directly on raw text without pre-tokenization; implements both BPE and Unigram LM segmentation with subword regularization (Kudo & Richardson, Google, EMNLP 2018)
- [[truthfulqa|TruthfulQA]] — benchmark of 817 questions measuring LLM truthfulness; largest models show inverse scaling (less truthful as they grow); introduces imitative falsehoods concept and GPT-judge automated metric (Lin, Hilton & Evans, ACL 2022)

## Raw Sources

### Articles

- [AI угрожает программистам могуществом параллелизма](raw/articles/2025-06-30-ivanov-ai-ugrozhaet-programmistam-moguschestvom-parallelizma/ivanov2025aimenace.md) (Vladimir Ivanov, 2025-06-30)
- [Контрактное программирование: Ваш семантический щит в эпоху искусственного интеллекта](raw/articles/2025-07-05-ivanov-kontraktnoe-programmirovanie-vash-semanticheskii-schit-v-epo/ivanov2025contractdev.md) (Vladimir Ivanov, 2025-07-05)
- [AI в управлении проектами — теперь Resource Leveling уже работает](raw/articles/2025-07-01-ivanov-ai-v-upravlenii-proektami-teper-resource-leveling-uzhe-rab/ivanov2025aiinpm.md) (Vladimir Ivanov, 2025-07-01)
- [Семантическая интерференция. Или нажать «газ и тормоз» сразу в промптах](raw/articles/2025-07-01-ivanov-semanticheskaya-interferenciya-ili-nazhat-gaz-i-tormoz-srazu/ivanov2025semanticinterference.md) (Vladimir Ivanov, 2025-07-01)
- [Вектора GPT или почему для GPT ваше слово — пустота без контекста](raw/articles/2025-07-02-ivanov-vektora-gpt-ili-pochemu-dlya-gpt-vashe-slovo-pustota-bez-kon/ivanov2025gpgvectors.md) (Vladimir Ivanov, 2025-07-02)
- [Генерация с дополненной выборкой (RAG)](raw/articles/rag-wikipedia.md) (Wikipedia, 2026)
- [Knowledge Graph (Google)](raw/articles/knowledge-graph-google-wikipedia.md) (Wikipedia, 2026)
- [Дистрибутивная семантика](raw/articles/distributional-semantics-wikipedia.md) (Wikipedia, 2026)
- [Корпусная лингвистика](raw/articles/corpus-linguistics-wikipedia.md) (Wikipedia, 2026)
- [Frank Rosenblatt](raw/articles/frank-rosenblatt-wikipedia.md) (Wikipedia, 2026)
- [История ИИ: бунтари, гении и научные войны, которые сформировали наш мир](raw/articles/2025-07-03-ivanov-istoriya-ii-buntari-genii-i-nauchnye-voiny-kotorye-sformirov/ivanoc2025istoriya.md) (Vladimir Ivanov, 2025-07-03)
- [Позиционные кодировки: «объемное зрение» GPT и секреты AI-агентов](raw/articles/2025-07-04-ivanov-pozicionnye-kodirovki-obemnoe-zrenie-gpt-i-sekrety-ai-agento/ivanoc2025encodings.md) (Vladimir Ivanov, 2025-07-04)
- [Design by Contract](raw/articles/design-by-contract-wikipedia.md) (Wikipedia, 2026)
- [Кот Шрёдингера в голове у GPT: Как суперпозиция смыслов меняет правила игры с ИИ](raw/articles/2025-07-06-ivanov-kot-shredingera-v-golove-u-gpt-kak-superpoziciya-smyslov-men/ivanov2025superposition.md) (Vladimir Ivanov, 2025-07-06)
- [KV Caching Explained](raw/articles/2023-kv-caching-explained/joaolages2023kvcache.md) (João Lages, Medium, 2023-10-08)
- [OpenAI](raw/articles/openai-wikipedia.md) (Wikipedia, 2026)
- [За кулисами Microsoft: тайные элитные партнерские программы и ИИ-трансформация](raw/articles/2025-07-10-ivanov-za-kulisami-microsoft-tainye-elitnye-partnerskie-programmy-i/ivanoc2025microsoft.md) (Vladimir Ivanov, 2025-07-10)
- [Rational Unified Process](raw/articles/rational-unified-process-wikipedia.md) (Wikipedia, 2026)
- [Difference between BFS and DFS](raw/articles/2019-bfs-vs-dfs-gfg.md) (GeeksforGeeks)
- [Breadth First Search or BFS for a Graph](raw/articles/2012-bfs-gfg.md) (GeeksforGeeks)
- [Методология PCAM: Превращаем AI-агентов из рабов в партнеров](raw/articles/2025-09-11-ivanov-metodologiya-pcam-prevraschaem-ai-agentov-iz-rabov-v-partner/ivanov2025pcam.md) (Vladimir Ivanov, 2025-09-11)
- [GRACE: Фреймворк создания кода LLM в больших контекстах](raw/articles/2025-09-13-ivanov-grace-freimvork-sozdaniya-koda-llm-v-bolshih-kontekstah-s-uc/ivanoc2025grace.md) (Vladimir Ivanov, 2025-09-13)
- [Причины наблюдаемого провала малых SLM против LLM на MoE в AI-агентах](raw/articles/2025-09-14-ivanov-prichiny-nabludaemogo-provala-malyh-slm-protiv-llm-na-moe-v/ivanov2025slmvsllm.md) (Vladimir Ivanov, 2025-09-14)
- [Оптимизация управления ИИ агентами на SLM через FLEX](raw/articles/2025-09-18-ivanov-optimizaciya-upravleniya-ii-agentami-na-sml-cherez-metodolog/ivanov2025flex.md) (Vladimir Ivanov, 2025-09-18)
- [Преодоление галлюцинаций в Mamba-моделях](raw/articles/2025-09-21-ivanov-preodolenie-gallucinacii-v-mamba-modelyah-eksperimentalnoe-i/ivanov2015hallucinations.md) (Vladimir Ivanov, 2025-09-21)
- [Семантическая разметка GRACE как нативный интерфейс для Mamba-моделей](raw/articles/2025-09-21-ivanov-semanticheskaya-razmetka-grace-kak-nativnyi-interfeis-dlya-m/ivanov2025gracemamba.md) (Vladimir Ivanov, 2025-09-21)
- [GPT-4.1 Prompting Guide](raw/articles/2025-04-14-openai-gpt41-prompting-guide.md) (OpenAI, 2026)

### Papers

- [Toy Models of Superposition](raw/papers/2022-09-elhage-toy-models-superposition/anthropic2022toy.md) (Anthropic Transformer Circuits Thread, 2022)
- [Constitutional AI: Harmlessness from AI Feedback](raw/papers/2022-12-bai-constitutional-ai/bai2022constitutional.md) — PDF at [2212.08073.pdf](raw/papers/2022-12-bai-constitutional-ai/2212.08073.pdf) (Yuntao Bai et al., Anthropic, arXiv 2022)
- [Self-Instruct: Aligning Language Models with Self-Generated Instructions](raw/papers/2022-12-wang-self-instruct/wang2022selfinstruct.md) — PDF at [2212.10560.pdf](raw/papers/2022-12-wang-self-instruct/2212.10560.pdf) — bootstraps instruction-following via model's own generations; 33% absolute gain on SuperNI, near InstructGPT_001 without human annotations (Yizhong Wang et al., UW/AI2, ACL 2023)
- [Scaling Laws for Reward Model Overoptimization](raw/papers/2022-10-gao-reward-model-overoptimization/gao2022rewardmodeloveropt.md) — PDF at [2210.10760.pdf](raw/papers/2022-10-gao-reward-model-overoptimization/2210.10760.pdf) — establishes scaling laws for reward model overoptimization in RLHF; functional forms for BoN and RL, smooth coefficient scaling with RM parameter count; synthetic gold-RM setup (Leo Gao, John Schulman, Jacob Hilton, OpenAI, 2022)
- [Fast Inference from Transformers via Speculative Decoding](raw/papers/2022-11-leviathan-speculative-decoding/laviathan2022speculativedecoding.md) — PDF at [2211.17192.pdf](raw/papers/2022-11-leviathan-speculative-decoding/2211.17192.pdf) — introduces speculative decoding: accelerates autoregressive model inference by generating multiple tokens per serial invocation via draft-verify with a fast approximation model; 2–3× walltime speedup on T5-XXL without retraining or output distribution changes (Leviathan, Kalman & Matias, Google, ICML 2023)
- [Training Compute-Optimal Large Language Models]
- [Training language models to follow instructions with human feedback](raw/papers/2022-03-ouyang-instructgpt/ouyang2022instructgpt.md) — PDF at [2203.02155.pdf](raw/papers/2022-03-ouyang-instructgpt/2203.02155.pdf) (Long Ouyang et al., OpenAI, NeurIPS 2022)
- [On the ability of standard and brain-constrained DNNs to support cognitive superposition](raw/papers/2024-02-garagnani-cognitive-superposition/garagnani2024superposition.md) (Max Garagnani, Cognitive Neurodynamics, 2024)
- [Transformers Represent Belief State Geometry in their Residual Stream](raw/papers/2024-05-shai-belief-state-geometry/shai2025belief.md) (Adam Shai et al., NeurIPS 2024)
- [Training Large Language Models to Reason in a Continuous Latent Space](raw/papers/2024-12-hao-coconut/hao2025coconut.md) — abstract, full PDF, and plain-text at [hao2025coconut.md](raw/papers/2024-12-hao-coconut/hao2025coconut.md) (Shibo Hao et al., FAIR at Meta / UC San Diego, arXiv, COLM 2025)
- [Generating Long Sequences with Sparse Transformers](raw/papers/2019-04-child-sparse-transformer/1904.10509.pdf) — abstract and details at [child2019sparse](raw/papers/2019-04-child-sparse-transformer/child2019sparse.md) (Rewon Child et al., OpenAI, 2019)
- [Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned](raw/papers/2019-05-voita-attention-heads/voita2019attention.md) — PDF at [1905.09418.pdf](raw/papers/2019-05-voita-attention-heads/1905.09418.pdf) (Elena Voita et al., Yandex / UvA / Edinburgh, ACL 2019)
- [What Does BERT Look At? An Analysis of BERT's Attention](raw/papers/2019-06-clark-bert-attention/clark2019bertattention.md) — PDF at [1906.04341.pdf](raw/papers/2019-06-clark-bert-attention/1906.04341.pdf) (Kevin Clark et al., Stanford / Facebook AI, BlackBoxNLP 2019)
- [Scaling Laws for Neural Language Models](raw/papers/2020-01-kaplan-scaling-laws/kaplan2020scaling.md) — abstract and PDF at [2001.08361.pdf](raw/papers/2020-01-kaplan-scaling-laws/2001.08361.pdf) (Jared Kaplan et al., OpenAI/arXiv, 2020)
- [GLU Variants Improve Transformer](raw/papers/2020-02-shazeer-glu-variants/shazeer2020gluvariants.md) — PDF at [2002.05202.pdf](raw/papers/2020-02-shazeer-glu-variants/2002.05202.pdf) — introduces GLU variants (GEGLU, SwiGLU, ReGLU) for Transformer FFN layers; GEGLU and SwiGLU achieve best perplexity; SwiGLU became the default activation in post-2022 LLMs (Noam Shazeer, Google, arXiv:2002.05202, February 2020)

- [Longformer: The Long-Document Transformer](raw/papers/2020-04-beltagy-longformer/beltagy2020longformer.md) (Iz Beltagy et al., Allen Institute for AI, 2020)
- [Language Models are Few-Shot Learners](raw/papers/2020-05-brown-gpt3/brown2020gpt3.md) — PDF at [2005.14165.pdf](raw/papers/2020-05-brown-gpt3/2005.14165.pdf) — introduces GPT-3 (175B) and the systematic study of [[in-context-learning|in-context learning]] across zero/one/few-shot settings; demonstrates scaling LMs improves task-agnostic performance; includes data contamination analysis and broader impacts discussion (Brown et al., OpenAI, NeurIPS 2020)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](raw/papers/2020-05-lewis-rag/lewis2020rag.md) — PDF at [2005.11401.pdf](raw/papers/2020-05-lewis-rag/2005.11401.pdf) — introduces RAG combining BART-large (parametric) with DPR Wikipedia index (non-parametric); two formulations (RAG-Sequence, RAG-Token); SOTA on three open-domain QA benchmarks (Lewis et al., FAIR / UCL / NYU, NeurIPS 2020)
- [Big Bird: Transformers for Longer Sequences](raw/papers/2020-07-zaheer-big-bird/zaheer2020bigbird.md) (Manzil Zaheer et al., Google Research, NeurIPS 2020)
- [SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference](raw/papers/2025-02-zhang-spargeattention/2502.18137.pdf) — details at [zhang2025spargeattn](raw/papers/2025-02-zhang-spargeattention/zhang2025spargeattn.md) (Jintao Zhang et al., Tsinghua/UC Berkeley, ICML 2025)
- [Small Language Models are the Future of Agentic AI](raw/papers/2025-06-belcak-slm-agentic-ai/belcak2025slm.md) — PDF at [2506.02153.pdf](raw/papers/2025-06-belcak-slm-agentic-ai/2506.02153.pdf) (Peter Belcak et al., NVIDIA Research, arXiv June 2025)
- [CoT Harms Performance of Rather Smaller Language Models](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md) — PDF at [shim2024cotharms.pdf](raw/papers/2024-10-09-ship-cot-harms/shim2024cotharms.md) (Jihoo Shim, Shin Dong Ho, Jeongwon Kim, IEOM 1st World Congress 2024)
- [Hallucination Detection with Small Language Models](raw/papers/2025-06-24-cheung-hallucination-detection-slm/2506.22486.pdf) — details at [cheung2025hallucination.md](raw/papers/2025-06-24-cheung-hallucination-detection-slm/cheung2025hallucination.md) (Ming Cheung, dBeta Labs, IEEE ICDE Workshop 2025)
- [Attention Is All You Need](raw/papers/2017-06-vaswani-attention-is-all-you-need/1706.03762.pdf) — details at [vaswani2017attention](raw/papers/2017-06-vaswani-attention-is-all-you-need/vaswani2017attention.md) (Ashish Vaswani et al., Google Research/NIPS, 2017)
- [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](raw/papers/2022-05-dao-flashattention/2205.14135.pdf) — details at [dai2022flashattention.md](raw/papers/2022-05-dao-flashattention/dai2022flashattention.md) (Tri Dao et al., Stanford, NeurIPS 2022)
- [Matryoshka Representation Learning](raw/papers/2022-05-kusupati-matryoshka-representation-learning/kusupati2022mrl.md) — PDF at [2205.13147.pdf](raw/papers/2022-05-kusupati-matryoshka-representation-learning/2205.13147.pdf) — introduces MRL: multi-granularity embedding via O(log(d)) nested losses; up to 14× smaller embedding for same accuracy and 128× theoretical speedup for adaptive retrieval (Aditya Kusupati et al., UW / Google Research / Harvard, NeurIPS 2022)
- [RoFormer: Enhanced Transformer with Rotary Position Embedding](raw/papers/2021-04-su-roformer/2104.09864.pdf) — details at [su2021rope.md](raw/papers/2021-04-su-roformer/su2021rope.md) (Jianlin Su et al., Zhuiyi Technology, arXiv 2021)
- [Knowledge Neurons in Pretrained Transformers](raw/papers/2021-04-dai-knowledge-neurons/dai2021knowledgeneurons.md) — PDF at [2104.08696.pdf](raw/papers/2021-04-dai-knowledge-neurons/2104.08696.pdf) — introduces knowledge neurons via integrated gradients attribution; demonstrates that FFN intermediate neurons causally encode specific factual knowledge; achieves 34.4% fact-update success rate with ~4 neuron edits (Damai Dai et al., Microsoft / Peking University, ACL 2022)
- [Transformer Feed-Forward Layers Are Key-Value Memories](raw/papers/2020-12-geva-ffn-key-value/geva2021ffnkeyvalue.md) — PDF at [2012.14913.pdf](raw/papers/2020-12-geva-ffn-key-value/2012.14913.pdf) (Mor Geva et al., Tel-Aviv Univ / AI2 / Cornell Tech, EMNLP 2021)
- [Evaluating Large Language Models Trained on Code](raw/papers/2021-07-chen-codex/chen2021codex.md) — PDF at [2107.03374.pdf](raw/papers/2021-07-chen-codex/2107.03374.pdf) — introduces Codex, GPT fine-tuned on GitHub code; HumanEval benchmark; pass@k metric; powers GitHub Copilot (Mark Chen et al., OpenAI, arXiv 2021)
- [Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](raw/papers/2021-08-press-alibi/press2022alibi.md) — PDF at [2108.12409.pdf](raw/papers/2021-08-press-alibi/2108.12409.pdf) — introduces ALiBi, a position method that biases attention scores with a distance-proportional penalty instead of using positional embeddings; enables training on short sequences and extrapolating to long ones; 11% faster and 11% less memory than sinusoidal at same perplexity; ICLR 2022 (Ofir Press, Noah A. Smith, Mike Lewis, UW / FAIR / AI2)
- [Finetuned Language Models Are Zero-Shot Learners](raw/papers/2021-09-wei-flan/wei2021flan.md) — PDF at [2109.01652.pdf](raw/papers/2021-09-wei-flan/2109.01652.pdf) — introduces instruction tuning and FLAN (137B); demonstrates zero-shot FLAN outperforms zero-shot GPT-3 on 20/25 datasets; ICLR 2022 (Jason Wei et al., Google Research, arXiv:2109.01652, September 2021)
- [TruthfulQA: Measuring How Models Mimic Human Falsehoods](raw/papers/2021-09-lin-truthfulqa/lin2021truthfulqa.md) — PDF at [2109.07958.pdf](raw/papers/2021-09-lin-truthfulqa/2109.07958.pdf) — benchmark of 817 questions measuring truthfulness; inversely scales with model size (larger models less truthful); introduces imitative falsehoods and GPT-judge; best model 58% vs human 94% (Stephanie Lin, Jacob Hilton, Owain Evans, Oxford/OpenAI, ACL 2022)
- [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](raw/papers/2021-01-fedus-switch-transformers/2101.03961.pdf) — details at [fedus2022switch.md](raw/papers/2021-01-fedus-switch-transformers/fedus2022switch.md) (William Fedus et al., Google, JMLR 2022)
- [SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference](raw/papers/2025-02-zhang-spargeattention/2502.18137.pdf) — details at [zhang2025spargeattn](raw/papers/2025-02-zhang-spargeattention/zhang2025spargeattn.md) (Jintao Zhang et al., Tsinghua/UC Berkeley, ICML 2025)
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](raw/papers/2023-05-rafailov-dpo/rafailov2023dpo.md) — PDF at [2305.18290.pdf](raw/papers/2023-05-rafailov-dpo/2305.18290.pdf) (Rafael Rafailov et al., Stanford, NeurIPS 2023)
- [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](raw/papers/2023-05-ainslie-grouped-query-attention/ainslie2023gqa.md) — PDF at [2305.13245.pdf](raw/papers/2023-05-ainslie-grouped-query-attention/2305.13245.pdf) — introduces grouped-query attention (GQA): groups of query heads share K/V heads, interpolating MHA↔MQA; uptraining recipe converts MHA checkpoints at 5% compute; quality ≈ MHA at ~5× MQA speed; adopted by LLaMA 2/3, Mistral (Ainslie et al., Google Research, EMNLP 2023)
- [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](raw/papers/2018-10-devlin-bert/1810.04805.pdf) — details at [devlin2018bert.md](raw/papers/2018-10-devlin-bert/devlin2018bert.md) (Jacob Devlin et al., Google AI Language, NAACL 2019)
- [Neural Machine Translation of Rare Words with Subword Units](raw/papers/2016-06-sennrich-bpe-subword/1508.07909.pdf) — introduces BPE for subword tokenization; details at [sennrich2016bpe.md](raw/papers/2016-06-sennrich-bpe-subword/sennrich2016bpe.md) (Rico Sennrich, Barry Haddow, Alexandra Birch, ACL 2016)
- [Red Teaming Language Models with Language Models](raw/papers/2022-02-perez-red-teaming/perez2022redteaming.md) — PDF at [2202.03286.pdf](raw/papers/2022-02-perez-red-teaming/2202.03286.pdf) — introduces automated LM-based red teaming; generates adversarial test cases to discover harmful behaviors (offensive content, data leakage, contact info exposure, distributional bias) in a 280B Gopher chatbot; compares zero-shot through RL methods against human adversaries (Ethan Perez et al., DeepMind / NYU, arXiv 2022)
- [Distilling the Knowledge in a Neural Network](raw/papers/2015-03-hinton-distillation/hinton2015distill.md) — PDF at [1503.02531.pdf](raw/papers/2015-03-hinton-distillation/1503.02531.pdf) — introduces knowledge distillation via temperature-parameterised softmax, soft target regularisation, and specialist models (Geoffrey Hinton, Oriol Vinyals, Jeff Dean, Google, NIPS 2014 Workshop, 2015)
- [Gaussian Error Linear Units (GELUs)](raw/papers/2016-06-hendrycks-gelu/hendrycks2016gelu.md) — PDF at [1606.08415.pdf](raw/papers/2016-06-hendrycks-gelu/1606.08415.pdf) — introduces GELU activation function xΦ(x) with probabilistic motivation from stochastic regularizer expectation; default activation in BERT and GPT; also introduces SiLU (Dan Hendrycks, Kevin Gimpel, arXiv 2016)
- [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](raw/papers/2017-01-shazeer-sparsely-gated-moe/shazeer2017moe.md) — PDF at [1701.06538.pdf](raw/papers/2017-01-shazeer-sparsely-gated-moe/1701.06538.pdf) — introduces the Sparsely-Gated MoE layer with noisy top-k gating, importance/load losses, and 137B parameter models; foundational paper for all modern MoE architectures (Noam Shazeer et al., Google Brain, ICLR 2017)
- [Okapi at TREC-3](raw/papers/1995-01-robertson-okapi-trec3/okapi_trec3.pdf)
- [SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing](raw/papers/2018-08-kudo-sentencepiece/kudo2018sentencepiece.md) (Taku Kudo, John Richardson, Google, EMNLP 2018)
- [Fast Transformer Decoding: One Write-Head is All You Need](raw/papers/2019-11-shazeer-multi-query-attention/shazeer2019multiquery.md) — PDF at [1911.02150.pdf](raw/papers/2019-11-shazeer-multi-query-attention/1911.02150.pdf) — introduces Multi-Query Attention (MQA), sharing keys and values across attention heads to reduce KV cache memory bandwidth by factor h; 12× decoder speedup with minimal quality loss (Noam Shazeer, Google, arXiv:1911.02150, November 2019)

- [LoRA: Low-Rank Adaptation of Large Language Models](raw/papers/2021-06-hu-lora/hu2021lora.md) — PDF at [2106.09685.pdf](raw/papers/2021-06-hu-lora/2106.09685.pdf) — freezes pre-trained weights and injects trainable low-rank decomposition matrices, reducing GPT-3 175B params by 10,000× with zero inference latency (Edward Hu et al., Microsoft, ICLR 2022)
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](raw/papers/2022-01-wei-chain-of-thought/wei2022cot.md) — PDF at [2201.11903.pdf](raw/papers/2022-01-wei-chain-of-thought/2201.11903.pdf) — introduces chain-of-thought prompting with intermediate reasoning steps; demonstrates CoT as emergent ability of model scale; PaLM 540B achieves SOTA on GSM8K surpassing finetuned GPT-3 (Jason Wei et al., Google Research, NeurIPS 2022)
- [Locating and Editing Factual Associations in GPT](raw/papers/2022-02-meng-rome/meng2022rome.md) — PDF at [2202.05262.pdf](raw/papers/2022-02-meng-rome/2202.05262.pdf) — introduces Causal Tracing to localise factual associations to mid-layer MLP modules processing the subject's last token; develops ROME (Rank-One Model Editing) for inserting new facts via rank-one MLP weight updates; introduces the COUNTERFACT dataset; ROME achieves S=89.2 on GPT-2 XL, simultaneously maintaining generalization (PS=96.4) and specificity (NS=75.4) where other methods sacrifice one or the other (Kevin Meng et al., MIT / Northeastern / Technion, NeurIPS 2022)
- [Large Language Models are Zero-Shot Reasoners](raw/papers/2022-05-kojima-zero-shot-cot/kojima2022zeroshot.md) — PDF at [2205.11916.pdf](raw/papers/2022-05-kojima-zero-shot-cot/2205.11916.pdf) — introduces Zero-shot-CoT; demonstrates that "Let's think step by step" elicits chain of thought reasoning without few-shot examples; evaluated on 12 reasoning datasets with 17 model variants (Takeshi Kojima et al., University of Tokyo / Google Research, NeurIPS 2022)
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models](raw/papers/2022-03-wang-self-consistency/wang2022selfconsistency.md) — PDF at [2203.11171.pdf](raw/papers/2022-03-wang-self-consistency/2203.11171.pdf) — replaces greedy decoding in CoT with sample-and-marginalise over diverse reasoning paths; GSM8K +17.9%, SVAMP +11.0%, AQuA +12.2%, StrategyQA +6.4% on PaLM-540B; unsupervised, no training required (Xuezhi Wang et al., Google, ICLR 2023)

## Comparisons

- [[bfs-vs-dfs|BFS vs DFS]] — Standard comparison of graph traversal algorithms BFS and DFS; reference anchor for LLM reasoning analogies
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — side-by-side comparison of Belcak et al. (NVIDIA, pro-SLM+heterogeneous) and Ivanov (pro-MoE/cost-field-flattening) positions; benchmarks, market data, and synthesis
- [[ffn-memory-vs-moe|FFN as Key-Value Memories vs Mixture-of-Experts]] — comparison of two perspectives on the transformer FFN layer: Geva et al.'s interpretability lens (FFN = key-value memory) vs MoE's architectural scaling strategy (sparse expert networks); dimensions include level of analysis, sparsity type, interpretability, and parameter scaling

## Queries
