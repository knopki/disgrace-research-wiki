# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-07-15 | Total pages: 216

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

- [[memit-mass-editing|MEMIT (Mass-Editing Memory In Transformer)]] — scales model editing from single (ROME) to thousands of facts by spreading batched least-squares MLP updates across mediating layers ℛ; S=85.8 at 10k edits on GPT-J vs ROME 50.3 (Meng et al., MIT/Northeastern/Technion, ICLR 2023)

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
- [[hyde|HyDE (Hypothetical Document Embeddings)]] — zero-shot dense retrieval that pivots relevance modeling onto a generative instruction-following LM: generate a hypothetical answer, embed it, use the embedding for nearest-neighbour search; no training or relevance labels (Gao et al., ACL 2023)
- [[rlhf|RLHF (Reinforcement Learning from Human Feedback)]] — technique for fine-tuning language models with human preferences as reward signal; InstructGPT demonstrated 1.3B model outperforming 175B GPT-3
- [[g-eval|G-Eval (NLG Evaluation with LLM + CoT)]] — Microsoft framework using GPT-4 with auto chain-of-thought + form-filling + probability-weighted scoring to evaluate NLG outputs; Spearman ρ=0.514 on SummEval, surpassing prior SOTA; flags LLM-judge bias toward LLM-generated text (Liu et al., 2023)

- [[reward-model-overoptimization|Reward Model Overoptimization Scaling Laws]] — empirical scaling laws characterizing how proxy reward model optimization degrades ground-truth performance via Goodhart's law; functional forms for BoN and RL, smooth coefficient scaling with RM parameters (Gao, Schulman & Hilton, OpenAI, 2022)
- [[rome-model-editing|ROME (Rank-One Model Editing)]] — method for editing factual associations in GPT via rank-one MLP weight updates; locates decisive mid-layer MLP computations via Causal Tracing and inserts new facts with both generalization and specificity (Meng et al., MIT / Northeastern / Technion, NeurIPS 2022)
- [[knowledge-graph|Knowledge Graph]] — structured entity-relationship knowledge base for grounding AI answers
- [[knowledge-neurons|Knowledge Neurons]] — specific FFN neurons causally responsible for expressing particular factual knowledge in pretrained Transformers; identified via integrated gradients attribution (Dai et al., Microsoft, ACL 2022)
- [[corpus-linguistics|Corpus Linguistics]] — branch of linguistics building annotated text corpora; foundational to NLP training data and RAG knowledge bases

- [[decomposed-prompting|Decomposed Prompting (DecomP)]] — modular few-shot prompting paradigm: decompose complex tasks into simpler sub-tasks delegated to dedicated sub-task handlers; supports hierarchical/recursive decomposition and external API integration; outperforms CoT on symbolic reasoning, long-context QA, and open-domain multi-hop QA (Khot et al., AI2/Stony Brook/Edinburgh, ICLR 2023)

- [[pcam|Purpose Centric Agent Methodology (PCAM)]] — agent management paradigm shifting from deterministic plans to purpose-driven guidance; six principles for autonomous goal-oriented agent architecture, plugin-based scalability, and multi-agent feedback loops

- [[grace|GRACE (Graph-RAG Anchored Code Engineering)]] — framework for deterministic LLM code generation in large contexts; dual-purpose semantic markup serving both generative models (top-down synthesis template) and RAG agents (indexed navigation map); ten principles including Intent-First Architecture, Observable AI Belief State, and Governed Autonomy

- [[flex-prompting|FLEX (Few-shot Logit-Enabled XML Prompting)]] — methodology for reliable SLM control using structured XML prompts, few-shot examples, and logit-based verification; validated on Qwen3-0.6B for agentic tool selection
- [[sparse-autoencoders|Sparse Autoencoders (Feature Extraction)]] — dictionary-learning method decomposing MLP activations into an overcomplete set of monosemantic interpretable features; Bricken et al. (Anthropic, 2023) show features beat neurons on interpretability, are universal across seeds, and recover up to 94.5% of MLP loss
- [[entities/gpt-3|GPT-3]] — 175B parameter autoregressive language model; demonstrated that scaling up LMs dramatically improves task-agnostic [[in-context-learning|in-context learning]] performance; systematic evaluation across zero/one/few-shot settings on dozens of NLP benchmarks; first systematic data contamination analysis for large-scale LMs
- [[glu-variants|GLU Variants (GEGLU, SwiGLU, ReGLU)]] — gated feed-forward variants replacing the Transformer FFN activation; GEGLU and SwiGLU achieve best perplexity; SwiGLU became the default FFN activation in post-2022 LLMs (LLaMA, PaLM, Gemma, Mistral, Qwen)



- [[lost-in-the-middle|Lost in the Middle]] — LLMs use long context non-uniformly: performance peaks when relevant info is at the start (primacy) or end (recency) and degrades in the middle, yielding a U-shaped curve; Liu et al. (TACL 2023)

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
- [[mamba|Mamba / Selective SSM]] — Gu & Dao (2023) linear-time sequence model; input-dependent (selective) SSM parameters (S6) replace LTI dynamics, enabling content-based reasoning; 5× inference throughput vs Transformers, linear scaling in length, matches 2× larger Transformers on language; SotA on audio + genomics; first attention-free model to match a strong Transformer++ recipe

- [[chain-of-continuous-thought|Chain of Continuous Thought (Coconut)]] — training paradigm replacing language CoT with reasoning directly in the continuous latent space of an LLM; enables emergent BFS-like reasoning
- [[sparse-transformer|Sparse Transformer]] — OpenAI architecture replacing quadratic attention with O(n√n) sparse factorized patterns; first to demonstrate self-attention on 1M+ token sequences
- [[speculative-decoding|Speculative Decoding]] — inference acceleration algorithm generating multiple tokens per serial model invocation by drafting candidates with a fast approximation model and verifying them with the target model in parallel; guarantees identical output distribution; 2–3× walltime speedup on T5-XXL without retraining or architecture changes (Leviathan, Kalman & Matias, Google, ICML 2023)
- [[streaming-llm|StreamingLLM and Attention Sinks]] — training-free method for infinite-length LLM generation: keep KV of a few "attention sink" initial tokens + rolling window to stabilize attention past the pre-training window; 22.2× faster than sliding-window recomputation, stable to 4M tokens (Xiao et al., MIT/Meta/CMU/NVIDIA, ICLR 2024)
- [[longformer|Longformer]] — linear-complexity attention combining sliding window and task-specific global attention; processes documents up to 4K-16K tokens without chunking; SOTA on WikiHop, TriviaQA, arXiv summarization
- [[lora|LoRA (Low-Rank Adaptation)]] — parameter-efficient fine-tuning method freezing pre-trained weights and injecting trainable low-rank matrices into Transformer layers; reduces GPT-3 175B trainable parameters by 10,000× with zero inference latency (Hu et al., Microsoft, ICLR 2022)
- [[big-bird|BigBird]] — linear-complexity attention combining random, window, and global tokens; first sparse-attention model with proven universal approximation and Turing completeness (Google Research, NeurIPS 2020); extends to DNA sequence analysis

- [[bm25|BM25]] — family of term-weighting functions for probabilistic IR; unified BM11/BM15 with tunable document length normalization; became the standard ranking function in Lucene, Elasticsearch, and Solr; introduced by Robertson et al. at TREC-3 (1995)

- [[s4-structured-state-spaces|S4 (Structured State Space Sequence Model)]] — first computationally practical deep SSM; NPLR parameterization reducing SSM computation from O(N²L) to Õ(N+L); SotA on LRA (86.09% avg, first to solve Path-X), raw speech (98.32%), and competitive with Transformers on WikiText-103 while 60× faster at generation; foundational to Mamba (Gu, Goel & Ré, Stanford, ICLR 2022 Outstanding Paper HM)

- [[flash-attention|FlashAttention]] — IO-aware exact attention; tiling cuts GPU HBM↔SRAM reads/writes; FlashAttention-2 (Dao, 2023) reworks GPU work partitioning for ~2× over v1, reaching up to 73% of A100 peak / 230 TFLOPs/s; first Transformer to beat chance on Path-X (16K) and Path-256 (64K) (Dao et al., Stanford, NeurIPS 2022)
- [[ring-attention|Ring Attention]] — distributed exact attention removing the per-device memory ceiling on context length by overlapping KV-block communication with blockwise computation in a ring of hosts; context scales linearly with device count (30M+ tokens demonstrated); built on blockwise parallel transformers (Liu, Zaharia & Abbeel, UC Berkeley, arXiv 2023)
- [[paged-attention|PagedAttention & vLLM]] — OS-paging-inspired KV-cache memory manager (non-contiguous paged blocks, block-table mapping, copy-on-write sharing) and the vLLM serving engine; 2–4× throughput over FasterTransformer/Orca at equal latency; default block size 16 (Kwon et al., UC Berkeley/UCSD, SOSP 2023; arXiv:2309.06180)
- [[rotary-position-embedding|Rotary Position Embedding (RoPE)]] — position encoding via rotation matrices that encodes absolute position while naturally incorporating relative position dependency; dominant PE in post-2023 LLMs (LLaMA, Mistral, Qwen, Gemma) (Su et al., Zhuiyi Technology, arXiv 2021)
- [[yarn|YaRN (Yet another RoPE extensioN)]] — compute-efficient RoPE context-window extension; NTK-by-parts interpolation + attention temperature scaling; 10× fewer tokens / 2.5× fewer steps than Position Interpolation; >2× zero-shot extension via Dynamic-YaRN (Peng et al., Nous Research, arXiv 2023)
- [[switch-transformer|Switch Transformer]] — Mixture-of-Experts architecture simplifying MoE to single-expert routing; enables trillion-parameter sparsely-activated models with constant compute cost; foundational to modern MoE LLMs (Fedus et al., Google, JMLR 2022)
- [[v4a-diff-format|V4A Diff Format]] — context-based, line-number-free diff format designed for LLM agent patch application; used by OpenAI GPT-4.1 for SWE-bench Verified (55% SOTA for non-reasoning models)
- [[chain-of-thought|Chain-of-Thought Prompting (CoT)]] — prompting technique that instructs LLMs to articulate intermediate reasoning steps; introduced by Wei et al. (Google, NeurIPS 2022) demonstrating CoT as an emergent ability of model scale; improves math/logic performance for large models (100B+) but harms SLM accuracy by 15–30%+
- [[plan-and-solve|Plan-and-Solve (PS) Prompting]] — zero-shot CoT variant (Wang et al., ACL 2023) replacing "Let's think step by step" with a plan-then-solve trigger; PS+ adds variable extraction + calculation guidance; outperforms Zero-shot-CoT across 10 reasoning datasets on GPT-3
- [[coala|CoALA (Cognitive Architectures for Language Agents)]] — conceptual framework organizing language agents along memory (working/long-term), action space (internal reasoning/retrieval/learning + external grounding), and a propose-evaluate-select decision cycle; casts ReAct, Reflexion, ToT, Voyager, Generative Agents into one taxonomy (Sumers, Yao, Narasimhan & Griffiths, TMLR 2024)
- [[generative-agents|Generative Agents]] — believable simulacra of human behavior; LLM fused with a memory-stream + reflection + planning architecture (recency/relevance/importance retrieval, periodic reflection trees, recursive plan decomposition); Smallville sandbox of 25 agents demonstrates emergent information diffusion, relationship formation, and coordination (Park et al., Stanford/Google, UIST 2023; arXiv:2304.03442)

- [[react|ReAct (Reasoning + Acting)]] — prompt paradigm interleaving verbal reasoning traces with actions + observations; synergizes CoT-style reasoning and tool/environment interaction; best prompting method combines ReAct with CoT-SC (Yao et al., Princeton/Google, ICLR 2023; arXiv:2210.03629)
- [[reflexion|Reflexion (Verbal Reinforcement Learning)]] — verbal reinforcement framework where agents self-reflect on task failures and store reflective text in episodic memory for iterative improvement without weight updates; 91% pass@1 on HumanEval, +22% on AlfWorld, +20% on HotPotQA (Shinn et al., NeurIPS 2023)
- [[cot-faithfulness|CoT Faithfulness (Unfaithful Explanations)]] — Turpin et al. (2023) show CoT explanations are *systematically* unfaithful: input biasing (Answer-is-Always-A, sycophantic hints) shifts predictions up to -36% while the CoT rationalizes the biased answer without mentioning the bias; Lanham et al. (Anthropic, 2023) intervene on the CoT itself and find faithfulness inversely scales with model size
- [[self-consistency|Self-Consistency]] — decoding strategy replacing greedy decoding in CoT with sample-and-marginalise over diverse reasoning paths; GSM8K +17.9%, SVAMP +11.0%, AQuA +12.2%, StrategyQA +6.4% and ARC-challenge +3.9% (Wang et al., Google, ICLR 2023)
- [[least-to-most-prompting|Least-to-Most Prompting]] — addresses easy-to-hard generalization by decomposing complex problems into subproblems; SCAN 99.7% vs CoT 16% under length split (Zhou et al., Google Research, ICLR 2023)
- [[tot|Tree of Thoughts (ToT)]] — generalizes CoT from a single reasoning chain to a search tree of "thoughts" with LM self-evaluation (sure/maybe/impossible or vote) as heuristic and BFS/DFS + backtracking; Game of 24 4%→74%; Creative Writing, Mini Crosswords (Yao et al., Princeton/Google DeepMind, NeurIPS 2023)
- [[toolformer|Toolformer]] — self-supervised method teaching a 6.7B GPT-J to call external tools (QA, calculator, Wikipedia search, MT, calendar) via interleaved API calls; samples calls with in-context learning, filters by perplexity reduction, fine-tunes; beats GPT-3-175B on LAMA/math at 1/26th the size (Schick et al., Meta AI, NeurIPS 2023)
- [[constitutional-ai|Constitutional AI (CAI)]] — method for training harmless AI assistants via self-critique, revision, and RLAIF using a written constitution; replaces human harmlessness labels with AI feedback guided by ~10-15 principles; achieves Pareto improvement in helpfulness-harmlessness tradeoff (Bai et al., Anthropic, arXiv 2022)
- [[direct-preference-optimization|Direct Preference Optimization (DPO)]]
- [[ffn-key-value-memories|Transformer FFN as Key-Value Memories]] — transformer feed-forward layers operate as unnormalized key-value memories where keys detect input patterns and values induce output distributions; lower layers capture shallow patterns, upper layers semantic ones (Geva et al., EMNLP 2021)
- [[sentencepiece|SentencePiece]] — language-independent subword tokenizer training directly on raw text without pre-tokenization; implements both BPE and Unigram LM segmentation with subword regularization (Kudo & Richardson, Google, EMNLP 2018)
- [[truthfulqa|TruthfulQA]] — benchmark of 817 questions measuring LLM truthfulness; largest models show inverse scaling (less truthful as they grow); introduces imitative falsehoods concept and GPT-judge automated metric (Lin, Hilton & Evans, ACL 2022)
- [[factscore|FActScore (Fine-grained Atomic Evaluation of Factual Precision)]] — metric decomposing long-form generations into atomic facts and scoring the fraction supported by a knowledge source; ChatGPT 58.3% vs human ~88.8% on biographies; automated estimator with <2% error rate (Min et al., UW/Meta/AllenAI, EMNLP 2023)

- [[chain-of-verification|Chain-of-Verification (CoVe)]] — deliberation method reducing factual hallucination: draft → plan verification questions → answer them independently → revise; factored variants prevent copying the original hallucination; +28% FActScore on biographies (Dhuliawala et al., Meta AI, arXiv 2023)

- [[hallucination-nlg-survey|Survey of Hallucination in NLG (Ji et al.)]] — first comprehensive survey of NLG hallucination; unified intrinsic/extrinsic taxonomy, contributors (data + training/inference), metrics, and mitigation across summarization, dialogue, MT, data-to-text, VL; plus a 2024 LLM section

- [[hallucination-llm-survey|Survey on Hallucination in LLMs (Huang et al.)]] — redefines hallucination for LLMs as factuality vs faithfulness (instruction/context/logical inconsistency); three-stage causal analysis (data/training/inference), detection+benchmarks, cause-linked mitigation, and RAG limitations (TOIS)

- [[spargeattn|SpargeAttn]] — accurate and training-free sparse attention that uses a two-stage filter (query-aware Top-K with GQA-guided correction) to prune non-essential KV-pairs; zero fine-tuning, plug-in for any model, up to 4.5× KV-cache reduction, 2.1× decoding speedup (Zhang et al., Tsinghua/UC Berkeley, ICML 2025)
- [[knowledge-distillation|Knowledge Distillation]] — compression technique transferring knowledge from a large teacher model to a smaller student model by training on softened labels produced by the teacher's temperature-scaled softmax; introduced by Hinton, Vinyals & Dean (Google, NIPS Workshop 2014); forms the basis of modern LLM distillation methods (MiniLLM, Orca, DistilBERT)

## Raw Sources

See [[sources.md|Raw Sources Index]] for the full catalog of articles and papers.

## Comparisons

- [[bfs-vs-dfs|BFS vs DFS]] — Standard comparison of graph traversal algorithms BFS and DFS; reference anchor for LLM reasoning analogies
- [[slm-moe-agentic-ai|SLM vs MoE for Agentic AI]] — side-by-side comparison of Belcak et al. (NVIDIA, pro-SLM+heterogeneous) and Ivanov (pro-MoE/cost-field-flattening) positions; benchmarks, market data, and synthesis
- [[ffn-memory-vs-moe|FFN as Key-Value Memories vs Mixture-of-Experts]] — comparison of two perspectives on the transformer FFN layer: Geva et al.'s interpretability lens (FFN = key-value memory) vs MoE's architectural scaling strategy (sparse expert networks); dimensions include level of analysis, sparsity type, interpretability, and parameter scaling

## Queries
