# SIGMA3-MIX54: Parsimonious mixed-gate strategies and the Herbrand validation barrier

Date: 2026-11-18, Asia/Seoul. Research status: PROVED/EXACT **restricted**, independent formal review pending; COMPUTATIONAL 86,692 finite assertion groups; CONDITIONAL SAT resource ledger. P versus NP remains OPEN. No all-input hereditary exponent contraction was proved.

## Proposal, project search, prior-art boundary
Four candidates: (1) composition of Horn and affine continuation services, (2) unique complete gate traces, (3) uniform cheap Herbrand candidate strategies, (4) globally committed Skolem and hostile prefix/parity/high-treewidth controls. Original files reviewed: `research/agents/lspv-3/2026-10-31_0529_LSPV-3_HORN_AFFINE_MIXED_GATE274.tex`, `research/main/2026-10-31_0548_MAIN_MIXED-COMPATIBILITY-REFEREE241.tex`, `research/coordination/2026-11-11_AFFINE_TABLE_COMPOSITION2_HANDOFF.md`, and the earlier Sigma3 strategy handoffs. **Mixed Horn/XOR NP-hardness is known and was already established in the project; no new generic hardness theorem is claimed.** The incremental scoped result is the parsimonious, unique-per-input trace and exact cheap-counterstrategy certification statement.

Primary sources: Schaefer (1978) https://doi.org/10.1145/800133.804350; Balabanov et al. (AAAI 2015) https://doi.org/10.1609/aaai.v29i1.9750; Fortnow et al. (JACM 2005) https://doi.org/10.1145/1101821.1101822.

## Exact construction
For every 3CNF F(x)=AND_j(ell_j1 OR ell_j2 OR ell_j3), add occurrence-falsity bits f_jk. A positive literal x_i has affine equation f_jk XOR x_i=1; a negative literal NOT x_i aliases f_jk=x_i. Make two AND gates a_j=f_j1 AND f_j2 and v_j=a_j AND f_j3. Encode AND(c,a,b) using the **Horn** clauses (NOT a OR NOT b OR c), (a OR NOT c), (b OR NOT c); put each zero-output condition v_j=0 in the **affine** subsystem. This uses 6m Horn clauses, at most 4m affine equations, and at most n+5m total variables. It can be encoded by a uniform linear-to-quasilinear bit compiler for standard binary-indexed source clauses.

All wires have a unique consistent complete gate trace for **each** committed x. The full system H AND E has that trace iff x satisfies F, proving a parsimonious reduction:
```
#SAT(H AND E) = #SAT(F).
```
For every **fixed** x, H and E are each satisfiable independently, even when their common join fails. This is a useful control for separate easy-component certificate schemes, not a SAT time lower bound. The representation has declared affine equations, not a strict-proper-3CNF-only promise.

## Stronger quantified-strategy validation lemma
Let B_j(x,z_j) be the local gate equations for clause j plus v_j=0, and let
```
Phi_F = exists x  forall j in [m]  exists z_j  B_j(x,z_j).
```
Then Phi_F is true iff SAT(F), and a valid local z_j, whenever it exists, is unique.

A uniform source-only compiler can build a circuit J_F(x) that returns the first falsified clause index, or the first clause if none is falsified. The circuit has O(N polylog N) size and can be constructed in N^{1+o(1)} time. For each x,
```
B_{J_F(x)}(x,.) is UNSAT iff F(x)=0.
```
Consequently, **checking that this explicitly constructed cheap Herbrand candidate wins against ALL x is coNP-complete**, by source-preserving reduction from UNSAT(F); its invalidity is certified by a satisfying assignment x. Every true instance has an O(N polylog N)-size Skolem policy after finding x, and every false instance has an O(N polylog N)-size Herbrand policy J_F. SMALL STRATEGY EXISTENCE and CHEAP POLICY CONSTRUCTION do not make GLOBAL VALIDITY FREE. This proves neither unconditional superpolynomial computation nor general strategy lower bounds.

Prefix trap: F=(x) AND (NOT x) is UNSAT, so exists x forall j is FALSE, whereas forall j exists x can pass each clause independently.

## Quantitative, SAME-REALIZATION ledger
Under P=NP fix one deterministic SAT solver A with time N^{K+o(1)}, workspace N^{L+o(1)}, K>=1. Materialized source authentication and compilation are N^{1+o(1)} time and space. Direct decision via A: N^{K+o(1)} time, N^{max(1,L)+o(1)} peak writable space. True witness x by n<=N full-size SAT self-reduction calls: N^{K+1+o(1)} time, same peak writable space. False label requires the ACTUAL UNSAT decision from A, not a free negative witness; after classification construct J_F in N^{1+o(1)} time. The per-fixed-(x,j) continuation can use O(1) Boolean constraints, after paying the indexed source and x reads; but this **does not** yield overall coefficient lambda<1, because full-size acquisition still costs at least the displayed baseline for this algorithm. No claim excludes a different algorithm. Query number, rereads, live input/child, witness storage, output circuit, and verification are explicitly charged. Neither an all-input hereditary compressor nor a forbidden joint time-space pair is exhibited.

## Host-language tests and scope
Seed 5411182026. 424 input formulas (396 SAT, 28 UNSAT); each x checked for separate H/E satisfiability, canonical trace and clauses, J_F equivalence; 4 tiny instances exhaustively enumerated over all mixed variables; adaptive challenge order tested with fixed x. Additional controls: 650 Gaussian-elimination GF(2) versus independent brute force, 720 high-treewidth K_(k,k) parity/integer-flow constructions with nonlinear AND observations, identity z=y, and quantified prefix swap. **86,692 recorded assertion groups, zero discrepancies.** Host Python tests are not native FLMV steps, asymptotic proofs, or independent mathematical peer review.

SHA256 local auditor: `d04009c6e1027c5e21162d5e1fe12c3d1a191eafbb429874a960f44a7d33f3f5`.
SHA256 raw JSON: `6e50871cbdf41c919450d1643f60d7457cfded4253e87828f7f44cfddbaaf0a8`.
Research bundle SHA256: `2ca171e66293fb879e247fe6eb0943560a97b43cf9e0dc65e0f32bf7b72eec91`.

Four gates: DISJ PASS (no rank hardness inference); relativization OPEN for global proof; simultaneous DTISP OPEN; deterministic configuration consistency PASS (upper bound only); algebrization/natural-proof transfers not claimed.

## One next experiment
A source-authenticated, separator-bounded mixed-continuation policy must construct a **verified common boundary assignment or exact empty-intersection proof**, accounting for acquisition and validation, and preserve global x and both response polarities. Adversarial input: the above uniquely extended parsimonious mixed family plus SAT-dependent indirect addressing and expander nonclosure. Target: genuine power-short child N^{lambda+o(1)}, lambda<1, all-input heredity and a single-machine forbidden joint time-space pair. All missing arrows OPEN.

END_SIGMA3_MIX54_20261118