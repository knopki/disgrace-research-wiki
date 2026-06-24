---
title: Knowledge Neurons
created: 2026-06-21
updated: 2026-06-21
type: concept
tags:
  - architecture
  - interpretability
  - paper
  - training
sources:
  - "[Knowledge Neurons in Pretrained Transformers](raw/papers/2021-04-dai-knowledge-neurons/dai2021knowledgeneurons.md)"
confidence: high
---

## Definition

**Knowledge neurons** are specific intermediate neurons in the feed-forward network (FFN) layers of a [[transformer|Transformer]] that are responsible for expressing particular factual knowledge. Introduced by Dai et al. (Microsoft Research / Peking University, ACL 2022), the concept provides a mechanism-level answer to how pretrained Transformers store and retrieve factual knowledge. ([Dai et al., 2021](raw/papers/2021-04-dai-knowledge-neurons/dai2021knowledgeneurons.md))

## Knowledge Attribution Method

Building on the [[ffn-key-value-memories|FFN as Key-Value Memories]] framework (Geva et al., 2021), Dai et al. view the two FFN linear layers as keys (first layer) and values (second layer). To identify which intermediate neurons encode a given relational fact `<h, r, t>` (e.g., `<Ireland, capital, Dublin>`):

1. **Cloze task:** Feed a knowledge-expressing prompt with the tail entity masked (e.g., "The capital of Ireland is [MASK]") and measure the model's correct-answer probability.
2. **Integrated gradients:** Compute attribution scores via `Attr(w_i) = w_i · ∫_0^1 ∂P(α·w_i)/∂w_i dα`, where w_i is the i-th FFN intermediate neuron at layer l. Riemann-approximated with m=20 steps.
3. **Refinement:** Generate n diverse prompts for the same fact, take the coarse set (attribution > threshold), then retain only neurons shared by ≥p% of prompts. This filters out "false-positive" neurons that encode syntactic/lexical information rather than the factual relation.

The method identifies ~4.13 knowledge neurons per relational fact on average in BERT-base-cased. ([Dai et al., 2021](raw/papers/2021-04-dai-knowledge-neurons/dai2021knowledgeneurons.md))

## Key Findings

### Layer Distribution
Knowledge neurons are concentrated in the **topmost layers** of BERT (layers 9-12 for BERT-base's 12 layers). This aligns with findings from [[ffn-key-value-memories|Geva et al.]] and Tenney et al. (2019) that higher layers encode more semantic information.

### Exclusivity
- Intra-relation fact pairs (same relation, different entities) share 1.23 knowledge neurons on average.
- Inter-relation fact pairs (different relations) share **almost no** knowledge neurons (0.09).
- This suggests knowledge neurons are relation-specific, not generic feature detectors.

### Causal Effect on Knowledge Expression
| Manipulation | Correct probability change |
|---|---|
| Suppress knowledge neurons (set to 0) | **−29.03%** (baseline: −1.47%) |
| Amplify knowledge neurons (double) | **+31.17%** (baseline: −1.27%) |

Baseline method (neuron activation as attribution) produces neurons with negligible causal effect, confirming that the integrated-gradients attribution identifies causally relevant neurons.

### Prompt Activation
Knowledge neurons are selectively activated by knowledge-expressing prompts. On the BINGREL dataset (crawled from Bing):
| Prompt type | Average neuron activation |
|---|---|
| Containing head + tail entities (expresses fact) | 0.485 |
| Containing only head entity | 0.019 |
| Randomly sampled | −0.018 |

Top-2 activating prompts from open-domain text reliably express the correct relation; bottom-2 activating prompts (same entities, different relation) do not.

## Applications

### Fact Updating
Modify FFN(val) value slots for the top ~4 knowledge neurons of a fact: `FFN(val)_i = FFN(val)_i − λ1·t + λ2·t'`, where t is the original tail entity embedding and t' is the target.
- **Change rate:** 48.5% (prediction shifts away from original)
- **Success rate:** 34.4% (new entity becomes top prediction)
- Intra-relation perplexity increase: 8.4
- Inter-relation perplexity increase: 7.2 (moderate collateral effect)
- Random neurons: only 4.7% change rate, 0.0% success rate

### Relation Erasing
Zero out 20 most common value slots for a relation. For sensitive relations (place_of_birth, country_of_citizenship, occupation, work_location):
| Relation | Pre-erasure PPL | Post-erasure PPL | Diff |
|---|---|---|---|
| place_of_birth (P19) | 1450.0 | 2996.0 (+106.6%) |
| occupation (P106) | 2279.0 | 5202.0 (+128.2%) |
| Other relations | 120.1-143.6 | 121.6-151.9 (+1.1 to +10.1%) |

The erased relation's perplexity doubles while other relations remain largely unaffected.

## Limitations (per the authors)

- Examined only fill-in-the-blank cloze task; implicit knowledge usage (reasoning, generalization) remains unexplored.
- Single-word [MASK] blanks; multi-word extensions needed.
- Interactions between knowledge neurons not studied.
- Limited to factual knowledge; other knowledge types not evaluated.

## Significance

Knowledge neurons provide the first direct causal link between specific FFN neurons and particular factual knowledge in pretrained Transformers. The work bridges [[ffn-key-value-memories|Geva et al.'s structural framework]] (FFN = key-value memories) with causal intervention — not only can we identify where facts live, we can manipulate them. This opens directions in model editing, privacy (erasing sensitive knowledge), and mechanistic interpretability of factual recall in language models.

## Cross-Links

- [[ffn-key-value-memories|FFN as Key-Value Memories]] — the structural framework (keys detect patterns, values predict tokens) that knowledge attribution builds on
- [[transformer|Transformer]] — the architecture whose FFN layers host knowledge neurons
- [[backpropagation|Backpropagation]] — the training algorithm that embeds knowledge into FFN parameters
- [[superposition|Superposition]] — the broader phenomenon of how neural networks represent more features than dimensions, related to the composition of knowledge neuron activations
- [[bert-attention-analysis|BERT Attention Analysis]] — concurrent interpretability work on BERT's attention heads
- [[rome-model-editing|ROME]] — model editing method that directly manipulates MLP weights via rank-one updates; compared against and outperforms Knowledge Neurons on COUNTERFACT
