---
source_url: https://link.springer.com/article/10.1007/s11571-023-10061-1
ingested: 2026-06-17
sha256: 3e33487f0737038b5689269ea8bb1b70626f0514678d1c074a368a406bb71f20
---

# On the Ability of Standard and Brain-Constrained Deep Neural Networks to Support Cognitive Superposition: A Position Paper

**Author:** Max Garagnani
**Published in:** *Cognitive Neurodynamics* (2024), Volume 18, pages 3383–3400
**DOI:** 10.1007/s11571-023-10061-1
**Type:** Open Access (CC BY 4.0) | Brief Communication
**Dates:** Received 31 January 2023; Revised 08 December 2023; Accepted 18 December 2023; Published 04 February 2024

---

## Abstract

The ability to coactivate (or "superpose") multiple conceptual representations is a fundamental function that we constantly rely upon; this is crucial in complex cognitive tasks requiring multi-item working memory, such as mental arithmetic, abstract reasoning, and language comprehension. As such, an artificial system aspiring to implement any of these aspects of general intelligence should be able to support this operation. I argue here that standard, feed-forward deep neural networks (DNNs) are unable to implement this function, whereas an alternative, fully brain-constrained class of neural architectures spontaneously exhibits it. On the basis of novel simulations, this proof-of-concept article shows that deep, brain-like networks trained with biologically realistic Hebbian learning mechanisms display the spontaneous emergence of internal circuits (cell assemblies) having features that make them natural candidates for supporting superposition. Building on previous computational modelling results, I also argue that, and offer an explanation as to why, in contrast, modern DNNs trained with gradient descent are generally unable to co-activate their internal representations. While deep brain-constrained neural architectures spontaneously develop the ability to support superposition as a result of (1) neurophysiologically accurate learning and (2) cortically realistic between-area connections, backpropagation-trained DNNs appear to be unsuited to implement this basic cognitive operation, arguably necessary for abstract thinking and general intelligence.

**Keywords:** Concept combination · Multi-item working memory · Brain-constrained modelling · Semantic representations · Artificial cognitive system · Cell assembly · General intelligence

---

## 1. Introduction

### Premise

The capacity of an (artificial or natural) cognitive system to recall and maintain simultaneously active in its working memory two or more internal representations is known as "superposition" in neurocomputational modelling (Greff et al. 2020; Milner 1974; Rosenblatt 1962; von der Malsburg 1986), "concept combination" in psychology and philosophy of mind (Costello and Keane 2001; Hampton 1991, 1997; Rips 1995; Wisniewski 1997), and "multi-item working memory" in cognitive neuroscience (Axmacher et al. 2010; Jensen and Lisman 2005; Lara and Wallis 2014; Yakovlev et al. 2005). This cognitive ability allows us to mentally combine instances of any two (or more) conceptual categories stored in semantic memory. For example, having previously acquired the concepts of "apple" and "car", one can conjure up a mental image combining two instances of these concepts. Crucially, this is possible even when the semantic categories were learned independently, i.e., no two samples of such concepts were ever "experienced together".

The present article focuses on the ability of a system to dynamically co-activate the representations of two previously acquired concepts while still maintaining such internal representations distinct and functionally separate.

**Definition of cognitive superposition (necessary and sufficient conditions):**

A neural network model is said to support cognitive superposition **if, and only if**:

1. It allows co-activation of any two vectors of hidden nodes' activities, associated with distinct input items **that were never presented together during the training phase**; and
2. During co-activation, the two activity vectors are combined in such a way that information about the identity and features of the original components is preserved.

The idea of superposition is closely linked to the concept of working memory (WM). WM has a limited capacity: the average person can maintain co-active only up to four or five items (Cowan 2001; Cowan et al. 2007); this capacity limitation significantly influences higher cognitive functions like reading, fluid reasoning, and general intelligence (Conway et al. 2003; Engle et al. 1999; Lara and Wallis 2014).

In what follows, it is assumed that a cognitive system encodes all items as patterns of activity (vectors) over a set of processing units. In standard (deep) NNs, an "internal representation" can be defined as a state of nodes' activities mapping an input-layer pattern to a corresponding output-layer pattern, a mapping typically acquired as a result of (gradient-descent) learning.

The requirement that the system must be capable to co-activate two internal representations while still maintaining these representations distinct is needed to ensure that the system does not fall prey to the well-known **binding problem** (Milner 1974), often referred to as the **"superposition catastrophe"** (Page 2000; Rosenblatt 1962; von der Malsburg 1986).

### Superposition is a Fundamental Cognitive Ability

Superposition operations underlie our mental capacity to create associations between multiple, previously and independently acquired concepts:

- **Mental comparison:** one must be able to activate two object representations during the same mental operation when comparing them.
- **Abstract reasoning:** problem solving, mental arithmetic, spatial and abstract reasoning, planning and complex decision making rely heavily on WM's ability to store and manipulate several items at once.
- **Language:** sentences can contain any arbitrary combination of two (or more) words referring to concepts which may have never been encountered together.
- **Social cognition:** recent evidence implicates superposition in theory of mind (Noguchi et al. 2022).
- **Visual perception:** addressing the superposition catastrophe has been associated with modelling brain mechanisms underlying visual object perception and recognition (Milner 1974; Rosenblatt 1962; von der Malsburg 1986).

---

## 2. Superposition Catastrophe in Standard Neural Networks

Modern Deep and Convolutional Neural Networks (D/CNNs) trained with gradient descent (backpropagation) exhibit features that reflect properties of the human neocortex, suggesting common underlying organizational and/or functional principles (Kriegeskorte 2015; LeCun et al. 2015). However, the analogy "DNN ≅ hierarchy of areas for sensory information processing" has been put under scrutiny: DCNNs cannot fully capture higher-level visual representations (Gale et al. 2020; Xu and Vaziri-Pashkam 2021a, 2021b); modern DNNs have been reported to be fragile (Jozwik et al. 2017), exhibit limited generalisation abilities (Greff et al. 2020) and fail to incorporate elements considered essential to attain human-like intelligence (Bishop 2021; Lake et al. 2017; Marcus 2018); cognitive superposition appears to be one of such crucial elements.

**The superposition catastrophe in DNNs:** simultaneously activating two (or more) of the learnt vectors in the input layer leads to a "blended" activation pattern in the output layer which is ambiguous, i.e., which might have been produced by more than just one combination of inputs.

**Prior attempts to overcome it:**

- **Bowers et al. (2014):** Used backpropagation-through-time to train a three-layer recurrent network on superposed input-output pairs. Some hidden nodes spontaneously acquired a high degree of selectivity. **Critical flaw:** items were co-activated *during training* — violates condition (B), which requires independently acquired representations.
- **Martin (2021):** Could not replicate Bowers' results — found no highly selective nodes emerged.
- **Temporal binding via oscillations:** Burwick (2006), Hummel and Biederman (1992), Shastri and Ajjanagadde (1993) and others proposed that cells encoding features of the same sensory item fire in synchrony, allocating distinct phases to distinct items. However, what these studies don't address is the exact neural mechanisms via which the brain might maintain such precisely timed synchronisation between distant, not directly linked neurons, and for long periods of time (several seconds), without suffering from cross-talk and interference.

---

## 3. Deep Brain-Constrained Hebbian-Learning Nets Support Cognitive Superposition

### Architecture

- **Six-area (six-layer) deep network** with structure, connectivity, and learning mechanisms closely mimicking cortical features.
- Each layer: 25×25 excitatory + 25×25 inhibitory graded-response cells.
- **Sparse, topographic, reciprocal projections** between areas (not all-to-all).
- **Learning rule:** "ABS rule" — local synaptic plasticity combining:
  - **LTP (Hebbian strengthening):** Links between coactive cells are strengthened.
  - **LTD (anti-Hebbian weakening):** Links between anti-correlated cells are weakened.

### Emergent Cell Assemblies (CAs)

- Sets of widely distributed, strongly and reciprocally connected cells.
- **Bistable:** "on" or "off" states (can self-sustain reverberant activity without external input).
- **Kernel + halo structure:** Core cells with strong reciprocal links; peripheral cells only weakly linked to the kernel.
- **Quasi-orthogonal:** Maximal overlap between any two CA circuits remains **below 5%** for a wide range of threshold γ values (see Fig. 2 bottom panel).
- **Disjoint circuits:** The activity states they induce are quasi-orthogonal (statistically uncorrelated).

### Proof-of-Concept Superposition (Fig. 3)

Using a 6-area model trained with Hebbian learning (3,000 presentations):

- CAs emerged spontaneously for 12 distinct input patterns.
- CA #5 was in a stable, self-sustained "on" state.
- At time t1, inputs were set to the pattern for CA #2.
- By time t4, CA #2 had fully ignited — both CAs #2 and #5 were simultaneously active.
- After external input removal (t5), CA #2 gradually faded while CA #5 remained self-sustained.
- **No blending or loss of identity:** The two circuits remained functionally distinct despite co-activation.

> "These are the first to document the superposition of CA circuits emerged spontaneously (i.e., via entirely unsupervised learning mechanisms) in a fully brain-constrained, multi-area neural network."

### Cell Assembly Properties

- **Self-sustained activity** → working memory correlate
- **Estimated size:** Thousands to tens of thousands of neurons → fault-tolerant
- **Robustness:** High degree of redundancy makes CA circuits extremely fault tolerant and resilient to noise
- In contrast, fully distributed architectures have each node's activity potentially having significant impact on output

---

## 4. Why Standard DNNs Fail to Support Cognitive Superposition

### Key Mechanism: Recruitment Learning

By means of both Hebbian and anti-Hebbian mechanisms, nodes become "recruited" (Valiant 2000) — selectively responsive to one (and only one) stimulus or item:

1. **LTP (Hebbian):** Strengthens connections between cells co-activated by same stimulus → gradually binds them into a CA circuit.
2. **LTD (anti-Hebbian):** Weakens connections between cells activated by different stimuli → separates distinct CAs.

**Result:** Emerging CA circuits consist of almost disjoint sets of cells.

### Why Backpropagation Fails

- Gradient descent redistributes error across **all** incoming links of a node → no single node becomes fully selective to a specific input item.
- Weights tend toward a **uniform distribution**, not bimodal (where a few are near 1.0 and the rest near 0.0).
- All cells projecting to a node remain involved in determining its response to every input.
- Distinct input–output pairs are learned as non-orthogonal patterns of graded activities distributed over the same (or significantly overlapping) sets of nodes.
- Superposition of any two such vectors produces a novel vector from which the original ones cannot be retrieved.

### Role of Sparse Connectivity

Sparse between-area projections on their own are not sufficient to guarantee quasi-orthogonal representations. Recent results with backprop-trained networks varying input patterns (Vanegdom et al. 2022) suggest that it is the **combination** of:
1. A local learning rule able to induce input selectivity
2. Sparse and topographic between-area projections

that enables quasi-orthogonal input-specific circuits to emerge in deep neural architectures.

### Additional Factors

The deep hierarchy itself contributes: patterns initially overlapping in the lowest layer are gradually "pulled apart" as activity propagates towards deeper layers, supported by recent modelling results (Henningsen-Schomers et al. 2023).

---

## 5. Summary and Concluding Remarks

### Three Core Claims

1. Superposition is a basic operation that any artificial system aiming at implementing human-like, general intelligence should support.
2. Deep, brain-constrained architectures with biologically realistic learning and connectivity exhibit the emergence of internal circuits (cell assemblies) which, by virtue of their structural properties (minimal overlap) and dynamics, provide a natural substrate for the implementation of superposition.
3. Backpropagation training of standard DNNs leads to internal representations that are generally non-orthogonal (i.e., patterns of graded activities uniformly distributed over the same hidden nodes), hence inadequate to support this function.

### Coexistence of Two Code Types

Graded (overlapping) and discrete (quasi-orthogonal CA) neural codes may coexist in the cortex:

| Code Type | Advantages | Disadvantages |
|-----------|------------|---------------|
| Graded (overlapping) | Smooth generalization based on similarity | Vulnerability to superposition catastrophe |
| Discrete (quasi-orthogonal CAs) | Robust, superposition-capable, noise-resistant | "All-or-none" response — poor similarity generalization |

### Empirical Evidence for CAs in Cortex

**Indirect support:**
- Synchronized neural activity during cognitive tasks (Buzsáki 2004; Canolty et al. 2010)
- Larger oscillatory responses to familiar vs. meaningless stimuli (Pulvermüller et al. 1995)
- Sparse coding in V1, auditory cortex, retrosplenial cortex (Olshausen & Field 1996; Liang et al. 2019; Mao et al. 2017)
- Orthogonal neural codes in neocortex (Flesch et al. 2022; Gennari et al. 2021)
- Place cells in hippocampus (Barnes et al. 1990; O'Keefe & Dostrovsky 1971)

**What remains elusive:** Direct proof of quasi-orthogonal CA circuits in cortex.

### Open Questions & Future Directions

1. **Superposition capacity and hierarchy depth:** Preliminary results show that as hierarchy depth increases, so does the maximal number of CA circuits the system is able to superpose. This capacity appears to asymptote, suggesting an architectural upper bound on the maximum number of coactive CAs — directly relatable to the limited capacity of human WM (Cowan 2001).
2. **Evolutionary implications:** Such computational results suggest that the significant expansion of cortical-association areas in humans could have been driven by the evolutionary advantage of better working-memory skills.
3. **Cognitive AI:** Exploring more biologically accurate, sparse connectivity and Hebbian mechanisms in deep NNs may be a fruitful future direction (Amit 2019; Bahroun et al. 2017; Bolcskei et al. 2019; Frenkel et al. 2021).

---

## References

Abeles M (1991) Corticonics - neural circuits of the cerebral cortex. Cambridge University Press

Amit Y (2019) Deep learning with asymmetric connections and hebbian updates. Front Comput Neurosci 13:18

Amit DJ, Brunel N (1997) Model of global spontaneous activity... Cereb Cortex 7(3):237–252

Arbib MA (2009) Evolving the language-ready brain. J Commun Disord 42(4):263–271

Artola A, Singer W (1993) Long-term depression of excitatory synaptic transmission and its relationship to long-term potentiation. Trends Neurosci 16:480–487

Artola A, Bröcher S, Singer W (1990) Different voltage-dependent thresholds for inducing long-term depression and long-term potentiation in slices of rat visual cortex. Nature 347:69–72

Bowers JS, Vankov II, Damian MF, Davis CJ (2014) Neural networks learn highly selective representations in order to overcome the superposition catastrophe. Psychol Rev 121(2):248–261

Braitenberg V (1978) Cell assemblies in the cerebral cortex. In: Heim R, Palm G (eds) Theoretical approaches to complex systems. Springer, pp 171–188

Buzsáki G (2010) Neural syntax: cell assemblies, synapsembles, and readers. Neuron 68(3):362–385

Conway AR, Kane MJ, Engle RW (2003) Working memory capacity and its relation to general intelligence. Trends Cogn Sci 7(12):547–552

Cowan N (2001) The magical number 4 in short-term memory: a reconsideration of mental storage capacity. Behav Brain Sci 24(1):87–114

Flesch T, Juechems K, Dumbalska T, Saxe A, Summerfield C (2022) Orthogonal representations for robust context-dependent task performance in brains and neural networks. Neuron 110(7):1258–1270

Garagnani M, Wennekers T, Pulvermüller F (2008) A neuroanatomically grounded Hebbian-learning model of attention-language interactions in the human brain. Eur J Neurosci 27(2):492–513

Garagnani M, Wennekers T, Pulvermüller F (2009) Recruitment and consolidation of cell assemblies for words by way of Hebbian learning and competition in a multi-layer neural network. Cogn Comput 1(2):160–176

Garagnani M, Pulvermüller F (2016) Conceptual grounding of language in action and perception. Eur J Neurosci 43(6):721–737

Hebb DO (1949) The organization of behavior. Wiley, New York

Henningsen-Schomers MR, Garagnani M, Pulvermüller F (2023) Influence of language on perception and concept formation in a brain-constrained deep neural network model. Philos Trans R Soc B 378(1870):20210373

Kriegeskorte N (2015) Deep neural networks: a new framework for modeling biological vision and brain information processing. Annu Rev Vis Sci 1:417–446

LeCun Y, Bengio Y, Hinton G (2015) Deep learning. Nature 521(7553):436–444

Martin N (2021) Selectivity in neural networks. PhD Thesis, University of Bristol

Milner PM (1974) A model for visual shape recognition. Psychol Rev 81:521–535

Noguchi W, Iizuka H, Yamamoto M, Taguchi S (2022) Superposition mechanism as a neural basis for understanding others. Sci Rep 12(1):2859

Page M (2000) Connectionist modelling in psychology: a localist manifesto. Behav Brain Sci 23(4):443–467

Palm G (1981) Towards a theory of cell assemblies. Biol Cybern 39(3):181–194

Pulvermüller F (2013) How neurons make meaning: brain mechanisms for embodied and abstract-symbolic semantics. Trends Cogn Sci 17(9):458–470

Pulvermüller F, Garagnani M (2014) From sensorimotor learning to memory cells in prefrontal and temporal association cortex. Cortex 57:1–21

Pulvermüller F, Tomasello R, Henningsen-Schomers MR, Wennekers T (2021) Biological constraints on neural network models of cognitive function. Nat Rev Neurosci 22(8):488–502

Rosenblatt F (1962) Principles of neurodynamics. Spartan, New York

Valiant LG (2000) Circuits of the mind. Oxford University Press

Vanegdom A, Nikolaev N, Garagnani M (2022) Standard feedforward neural networks with backprop cannot support cognitive superposition. Bernstein Conference 2022, Berlin

von der Malsburg C (1986) Am I thinking assemblies? In: Palm G, Aertsen A (eds) Brain theory. Springer, pp 161–176
