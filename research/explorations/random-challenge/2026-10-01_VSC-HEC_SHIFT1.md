# VSC-HEC SHIFT1 — Variable-Exponent Shifted-Chronogram HEC

**Timestamp:** 2026-10-01 09:14 PT  
**Status:** P vs NP remains OPEN.  
**Labels:** PROVED/EXACT in the declared online/no-reread model; COMPUTATIONAL for finite tests; FALSIFIED/RETIRED for simple shift accumulation and uncharged static rereading; CANDIDATE for pointer/pebbling chronograms.

## 1. Model

For epoch e, choose a construction parameter d_e in N that is fixed independently of n and define

- K_e = n^(d_e)
- X_e in {0,1}^(K_e)

A chronogram later reveals a bijection pi_e on [K_e], or a sequence of such bijections. A future challenge asks for

Q(e,j) = X_e[pi_e(j)].

The deterministic machine is cut to state S before the relevant future transformation/challenge is fully revealed. A free semantic side channel Z takes at most 2^r values.

The exponent d_e is a parameter of the construction, not a function of n. It may be selected after fixing the hypothetical polynomial-time SAT solver exponent k, provided the resulting construction remains polynomial-size in its actual input representation.

## 2. PROVED/EXACT: late bijections preserve the no-reread state bound

If the old payload cannot be reread after the cut and the late-revealed bijection family lets the challenge reach every coordinate of a K-bit payload, then within each fixed side-information fiber Z=z, two distinct payloads cannot share a cut state.

Therefore

s >= log_2 max_z |Z^{-1}(z)| >= K-r.

A cyclic shift is already transitive on coordinates. Thus a single fixed challenge position combined with an unknown late shift realizes ordinary INDEX and yields the same K-r lower bound.

This is a useful challenge mechanism, but not yet a static-SAT lower bound.

## 3. PROVED/EXACT: transformation-history compression

Let all epoch transformations lie in a group G_K with efficient composition and an l_G(K)-bit representation. A history

pi_1,...,pi_E

has the same final action as the single product

Pi = pi_E o ... o pi_1.

Therefore the transformation history itself can be tracked in l_G(K) bits; it does not force state proportional to E.

### Cyclic shifts

For shifts sigma_e,

Pi(j) = j + Sigma (mod K),  Sigma = sum_e sigma_e (mod K).

Only ceil(log_2 K) tracking bits are needed, independent of the number of epochs.

### Affine maps

Over F_q, maps x -> a x + b compose to one map x -> A x + B. The whole history is summarized by one pair (A,B), requiring O(log q) bits.

**Status change:** repeated cyclic or affine shifting is FALSIFIED as an accumulating-hardness mechanism. It remains useful only as delayed addressing.

## 4. PROVED/EXACT: static random-access reread collapse

If, after the shift is known, the original payload remains accessible by ordinary random access, the machine can compute the requested address a=pi(j) and read X[a] directly.

Thus there is an explicit upper bound:

- retained payload state: 0 bits
- post-shift payload probes: 1
- address work: O(log K) bits/operations, aside from the cost of computing pi(j)

Therefore the statement "late shift forces Omega(K) stored payload bits" does **not** survive unrestricted static rereading.

This is the strongest hostile result from the test. A useful Static-to-HEC theorem must either charge rereads or make the target address itself expensive to obtain.

## 5. PROVED/EXACT: literal polynomial payloads normalize to at most linear information burden

If an epoch literally contains K=n^d independent bits, then the actual input length N satisfies N >= K. The HEC information lower bound s >= K-r is therefore at most linear in the literal payload length.

Choosing a larger constant d changes the polynomial scale in the base parameter n, but does not by itself produce a superpolynomial lower bound as a function of the actual expanded input length N.

Hence d is useful as a calibration/diagonal parameter only if a future compiler can generate an n^d-scale obligation from an input whose representation exponent grows more slowly than d.

## 6. PROVED/EXACT: repeated shifts saturate at payload information

For a single K-bit payload, arbitrarily many late bijections cannot force more than K bits of payload information, because storing X itself is an exact K-bit upper bound.

Chronogram transformations can prevent prespecialization or batching, but cannot manufacture information. Independent new epoch payloads are required for additive sum_e K_e information bounds.

## 7. COMPUTATIONAL tests

Reproducible script:

`experiments/hec_shifted_chronogram/run.py`

Seed: `20261001`.

### 7.1 Exact state-fiber enumeration

Exhaustive enumeration for K=1,...,8 gave:

| K | no side info | one parity bit free |
|---:|---:|---:|
|1|1|0|
|2|2|1|
|3|3|2|
|4|4|3|
|5|5|4|
|6|6|5|
|7|7|6|
|8|8|7|

This exactly matches s >= K-r for r=0 and r=1.

### 7.2 Static reread hostile control

| K | no-reread + free SAT bit | retained payload with static reread | post-shift payload probes |
|---:|---:|---:|---:|
|16|15|0|1|
|64|63|0|1|
|256|255|0|1|
|1024|1023|0|1|
|4096|4095|0|1|
|16384|16383|0|1|

This is an exact algorithmic bypass, not merely empirical evidence.

### 7.3 Shift compression diagnostic

zlib was used only as a diagnostic, not as a theorem. For random strings of lengths 1024, 4096, and 16384, compressed size stayed essentially at raw size under random cyclic shifts. Periodic controls stayed highly compressible under shifts. Thus shifting did not create information or destroy intrinsic compressibility.

### 7.4 Group-history composition

Random cyclic-shift histories were tested at K=17,64,257 and E=4,16,64. Every history exactly collapsed to one cumulative offset.

Random affine histories were tested over F_17 and F_257 at E=4,16,64. Every history exactly collapsed to one pair (A,B).

The summary size was independent of E.

### 7.5 Exact black-pebbling toy test

Exact breadth-first search over black-pebbling configurations produced:

| graph | nodes | space | minimum moves |
|---|---:|---:|---:|
| pyramid h=3 | 6 | 4 | 8 |
| pyramid h=3 | 6 | 6 | 6 |
| pyramid h=4 | 10 | 5 | 15 |
| pyramid h=4 | 10 | 8 | 12 |
| binary tree depth 2 | 7 | 4 | 10 |
| binary tree depth 2 | 7 | 7 | 7 |
| binary tree depth 3 | 15 | 5 | 25 |
| binary tree depth 3 | 15 | 8 | 22 |

These finite tests establish no asymptotic theorem. They validate the STORE-vs-RECOMPUTE experiment harness.

## 8. Literature transfer

### EXACT / object-level relevance

- Pătraşcu–Demaine: cell-probe lower bounds and dynamic information-transfer tradeoffs.
- Alman–Wang–Yu: online communication complexity prevents batching by requiring answers before future query pieces arrive.
- Ponzio–Radhakrishnan–Venkatesh: pointer-chasing round/communication tradeoffs for sequential address dependence.
- Pebbling: exact abstract model for storing intermediate values versus recomputing them.

### Highly relevant recent analogue

Larsen–Simkin, *Time/Space Tradeoffs for Generic Attacks on Delay Functions* (TCC 2025), studies F^T against adversaries with bounded advice, oracle access, and parallel queries. Their tradeoffs between precomputed advice and sequential evaluation are structurally close to the HEC STORE/TRACK/RECOVER objective.

This is an oracle/delay-function theorem, not an unconditional SAT theorem.

### Restricted static SAT analogue

Pebbling contradictions and substitution constructions yield static bounded-width CNFs with strong time/space tradeoffs for resolution and stronger bounded-depth proof systems. This demonstrates that a dynamic store/recompute DAG can be compiled into a static SAT formula while retaining tradeoffs for specified proof systems.

It does **not** imply a lower bound for arbitrary SAT algorithms.

Beame–Jayram–Saks also obtain nontrivial time-space tradeoffs for branching programs and related RAM models, while Fortnow proves a model-independent forbidden near-linear-time/sublinear-space region for SAT. These are important controls on what a successful HEC transfer theorem might plausibly look like, but they do not exclude arbitrary polynomial-time SAT.

## 9. Candidate successor: Pointer-Pebbling Chronogram HEC (PPC-HEC)

Simple shifts should be replaced by data-dependent address evolution, for example

a_(t+1) = F_t(a_t, xi_t),

where xi_t is an epoch result or payload-dependent bit, and the dependency DAG is chosen to have a proven pebbling/time-space tradeoff.

The desired resource is no longer merely payload storage:

S_data + S_map + w Q_reread + C_recompute + C_sequential >= L(n,d).

The target address itself must require traversing or maintaining a dependency graph. Otherwise one random-access reread defeats the HEC state bound.

### Mandatory hostile controls

1. full preprocessing of the pointer map;
2. pointer jumping / composition;
3. compact group summaries;
4. memoization across challenges;
5. Gaussian/affine shortcuts;
6. INTERP / RECOMP wrappers;
7. a semantic oracle supplying current SAT answers for free.

## 10. Exact remaining P-vs-NP hinge

Even a strong PPC-HEC pebbling theorem remains restricted until one proves a model-preserving implication

arbitrary static SAT decider
  -> PPC-HEC computation with controlled preprocessing/state/reread/recompute costs.

The present tests sharpen rather than close this transfer barrier.

The useful new conclusion is:

**a successful compiler must force sequential address acquisition, or an equivalent pebbling obligation; late permutation alone is insufficient.**

## 11. Status ledger

**PROVED/EXACT**
- late-bijection no-reread bound;
- group-history compression;
- static one-reread bypass;
- literal-payload normalization;
- shift-saturation upper bound.

**COMPUTATIONAL**
- exhaustive state-fiber checks;
- group-composition checks;
- compression controls;
- small-DAG exact pebbling.

**FALSIFIED/RETIRED**
- cumulative cyclic-shift hardness;
- cumulative affine-shift hardness;
- plain late-shift storage lower bound under unrestricted static rereading.

**CANDIDATE**
- data-dependent pointer/pebbling chronogram;
- variable exponent d as a diagonal calibration parameter;
- static pebbling-formula experiments.

**OPEN**
- compact amplification with representation exponent below obligation exponent;
- arbitrary-algorithm Static-to-PPC-HEC compiler;
- nonrelativizing/nonalgebrizing endgame.

## References

- M. Pătraşcu and E. D. Demaine, “Logarithmic Lower Bounds in the Cell-Probe Model,” SIAM J. Comput. 35(4), 2006.
- J. Alman, J. R. Wang, H. Yu, “Cell-Probe Lower Bounds from Online Communication Complexity,” STOC 2018.
- S. J. Ponzio, J. Radhakrishnan, S. Venkatesh, “The Communication Complexity of Pointer Chasing,” JCSS 62(2), 2001.
- T. Dryja, Q. C. Liu, S. Park, “Static-Memory-Hard Functions and Nonlinear Space-Time Tradeoffs via Pebbling,” 2018.
- J. Alwen, J. Blocki, K. Pietrzak, “Depth-Robust Graphs and Their Cumulative Memory Complexity,” EUROCRYPT 2017.
- K. G. Larsen, M. Simkin, “Time/Space Tradeoffs for Generic Attacks on Delay Functions,” TCC 2025.
- P. Beame, T. S. Jayram, M. Saks, “Time–Space Tradeoffs for Branching Programs,” JCSS 63(4), 2001.
- L. Fortnow, “Time–Space Tradeoffs for Satisfiability,” JCSS 60(2), 2000.
- J. Nordström, “Pebble Games, Proof Complexity, and Time-Space Trade-offs,” LMCS 9(3), 2013.
- E. Ben-Sasson, J. Nordström, “Understanding Space in Proof Complexity: Separations and Trade-offs via Substitutions,” arXiv:1008.1789.
