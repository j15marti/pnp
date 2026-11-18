# TMR-2/075b (supplemental): growing-alphabet tournaments and an adaptive explicit-search lower bound

Pacific run label: 2026-11-17 20:35 PST. Research identity: TMR-2 / PNP Information Necessity. Target: **growing-tournament CSP**, not the fixed-template T5 problem. Status: **PROVED/EXACT for a restricted adaptive exhaustive-prefix algorithm model; finite controls COMPUTATIONAL; unrestricted decision lower bound OPEN**. Independent mathematical review OPEN. P versus NP OPEN.

## Candidate and falsifiers, stated before source/corpus audit

Candidate D2-GROWING-TOURNAMENT-LOCAL-ENUMERATION: for growing alphabet size `k=n`, construct NO tournament-homomorphism inputs with many locally compatible partial assignments **for every adaptive source-variable order**. Test whether the resulting local search tree has superpolynomial size.

Falsifiers/controls: (1) target tournaments lacking universal extension signatures, especially the standard regular circulant; (2) a source-aware polynomial global invariant distinguishing YES/NO without enumerating partial assignments; (3) a reduction from pointwise partial-homomorphism counts to unrestricted SAT-decision time that silently forbids sharing, caching, global reasoning or changing algorithms; (4) a succinct input representation hiding an exponential table.

## Source-to-output model and quantifiers

An input is an explicitly encoded loopless target tournament `T` on `k` labeled symbols, plus an explicitly encoded loopless source tournament `H` on `n=k` vertices. Every unordered pair has exactly one oriented edge. The target requires `binom(k,2)` orientation bits; an endpoint-encoded source requires `Theta(k^2 log k)` bits. Let `L=Theta(k^2 log k)` for this concrete encoding. Decide whether a homomorphism `H -> T` exists. Because both are tournaments of equal size, every homomorphism is injective and hence an isomorphism. In particular `H_yes=T` is YES and any nonisomorphic `H_no` is NO.

The **restricted algorithm model** comprises deterministic complete no-merging assignment-tree solvers: at a partial injective homomorphism, choose any unassigned source vertex as a function of the entire actual input and existing path; branch once on **each** target label compatible with all already assigned vertices; reject NO only after every such branch is exhausted. Branching order is fully adaptive. This model permits normal exact source reads and arc tests but **does not permit global UNSAT certificates, node-state merging, algebraic shortcuts or answering NO before exhausting the tree**. The lower bound below applies only to this declared model.

## Theorem A: quantitative random-tournament extension property

Let `T` be a tournament with `k` vertices. For an anchor set `S` of size `s` and one of the `2^s` designated orientations from a fresh vertex to the anchors, write `X(S,eta)` for the number of unused target labels realizing that exact pattern.

For uniformly independently oriented target pairs,
```
X(S,eta) ~ Binomial(k-s, 2^{-s}).
```
Indeed the `s` required target pair orientations are independent for each unused candidate and the candidate trials are independent.

By the multiplicative Chernoff inequality and a union bound,
```
P[ exists s<=r,S,eta: X(S,eta)<(k-s)/2^{s+1} ]
 <= sum_{s=0}^r binom(k,s)*2^s*exp(-(k-s)/(8*2^s)).
```
Put `ell=log_2 k` and `r=floor(ell-4 log_2 ell)`. For sufficiently large `k`, `(k-r)/2^r >= (1-o(1))*ell^4`, whereas the logarithm of the number of tested signatures is `O(ell^2)`. The bound tends to zero. Therefore, **for all sufficiently large k, at least one T_k exists** in which every pattern of at most `r=(1-o(1))log_2 k` previous colors has at least `(k-s)/2^{s+1}` unused realizations.

This is an existential probabilistic-method construction. It is not a claim of polynomial-time deterministic generation or certification for all k.

## Theorem B: unconditional superpolynomial worst-case tree size in the restricted model

Choose such a target `T_k`. Let the NO source `H_no` be the transitive tournament of order `k`; `T_k` cannot be transitive because the extension condition for one anchor requires both incoming and outgoing neighbors. Thus there is no homomorphism `H_no -> T_k`. For contrast `H_yes=T_k` is YES.

All valid partial source homomorphisms are injective. After any `s<=r` source vertices have been assigned, the next source vertex's prescribed orientations to those colors form a signature of length `s`; the extension property supplies at least `(k-s)/2^{s+1}` fresh candidates **regardless of how the solver adaptively chose the variable**.

Consequently every complete no-merging assignment-tree solver visits at least
```
D_r >= product_{s=0}^{r-1} ((k-s)/2^{s+1})
    = (k)_r / 2^{r(r+1)/2}
```
distinct depth-`r` nodes on this NO instance. For `r=log_2 k-O(log log k)`,
```
log_2 D_r >= (1/2-o(1))*(log_2 k)^2.
```
Hence the worst-case work of every solver **within this precisely defined explicit-assignment model** is at least
```
2^{(1/2-o(1)) (log_2 k)^2}
  = k^{(1/2-o(1))log_2 k},
```
superpolynomial both in `n=k` and in the explicit encoded input length `L=Theta(k^2 log k)`. This is *not* a lower bound on general-purpose algorithms deciding tournament homomorphism or SAT.

## FINITE degree-preserving YES/NO controls

The actual executed standard-library Python audit used the deterministic `random.Random` seeds shown below. All anchor sets and all their orientation patterns were checked by exact integer bitmasks. For each tested target we also reversed a genuine directed three-cycle to create a NO source. Reversing the cycle preserves every vertex's outdegree. An isomorphism would preserve the multiset of directed-triangle incidences per vertex; the resulting pairs have different multisets, so they are provably nonisomorphic (without a claimed exhaustive isomorphism search).

| k | r | extension patterns checked | min extensions | NO-source compatible prefix counts at depths 0,1,2,3,4 |
|---:|---:|---:|---:|---|
| 31 | 1 | 62 | 8 | 1, 31, 465, 3,366, 11,643 |
| 63 | 2 | 7,812 | 4 | 1, 63, 1,953, 29,822, 224,476 |
| 127 | 3 | 2,667,000 | 1 | 1, 127, 8,001, 250,218, 3,879,536 |

Seeds: 2026111801, 2026111802, 2026111803. Deterministically recomputable pair hashes and directed-triangle fingerprint hashes are in the immutable raw JSON. Only the listed finite r values were exhaustively checked, not the full asymptotic quantitative Chernoff property.

A **critical negative control**: the standard regular cyclic tournament with winning offsets `1..(k-1)/2` already fails the all-pattern two-anchor extension property at anchor pair `(0,1)`, requested signature `1`, for tested `k=5,31,63,127`. The probabilistic existence theorem does NOT apply to this deterministic circulant construction without separate proof.

## Dynamic invariant and TMR-4 interface

Name: **D2-GROWING-T-LOCAL-EXTENSION-TREE-TRACE**. Live objects are: authenticated complete source/target tournament bit tables; the assigned source-vertex subset; injective source-to-target partial map; bitset of unused labels; each chosen next vertex; its exact s-bit neighbor-orientation signature; the remaining compatible-label bitmask; cached or recomputed prefix paths; the search-tree stack; and final YES/NO output.

A unit branching expansion creates at most one explicit child node. The lower bound counts mandatory node creations **only inside the no-merging complete assignment-tree model**. Permitted general-purpose transitions include target/source structural analysis, tournament-isomorphism algorithms, local or global algebraic transformations, dynamic programming, shared prefixes, caching, and a direct rejection rule; these are uncharged MAY transitions for the restricted-to-general transfer and invalidate any unrestricted claim.

## Same-realization resource ledger and scope

One complete explicit brancher's total work is at least the displayed number of child-node creations; each costs at least one physical operation. A standard deterministic depth-first implementation on an explicitly parsed source can keep the two O(k^2) bit adjacency tables and O(k log k) live path bits; it uses polynomial live workspace while potentially spending superpolynomial time. Parsing, source/target authentication, target-bit lookup, failed branches, source variable selection, caching, rereading and final output do not reduce the **unit node-creation lower bound in the restricted model**. This is not a forbidden simultaneous DTISP pair or a theorem about all physical machines.

## Four mandatory gates

| Gate | Status and reason |
|---|---|
| DISJ sanity | PASS restricted. No static-rank-to-general-work inference. DISJ compact circuits remain legal. |
| Relativization, algebrization, Natural Proofs | PASS only for elementary local combinatorics; OPEN for any all-algorithm P-versus-NP claim. No nonrelativizing step supplied. |
| Simultaneous DTISP | NOT APPLICABLE to a forbidden lower-bound pair. The same DFS realization has polynomial workspace and the restricted node-count lower bound; general transfer OPEN. |
| Configuration counting | PASS upper-bound guard only: deterministic total read-only-input computation has T<=2^{O(S+log L)}. Not a work lower bound and not a probabilistic/quantum claim. |

Cheap Horn, 2-SAT, affine/Gaussian, treewidth, equality, autarky, modules, selectors, padding, original-label multiplicity, compact circuits, variable-ordering, source-aware recognition, shared reasoning, and alternative algorithms remain legal on the general problem. The /341 full UNSAT authority is FAIL; /386 RESTRICTED.

## Pinned sources, evidence and next dependency

Source: Bang-Jensen, Hell and MacGillivray (1988), *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J Discrete Math, DOI 10.1137/0401029, for fixed-T5 NP-completeness only. Chernoff and finite random-tournament extension proof above are independently stated and do not import ETH or other conjectures.

Code (exact Python stdlib): `experiments/tmr/tmr2_growing_tournament_extension075.py`.
Raw (original executed Python run): `results/raw/tmr/2026-11-17_2035_TMR2_GROWING_TOURNAMENT075_RAW.json`.
Local runner SHA256 of independently executed working copy: `fc8d20cf7b9ae7270c5c4b70434e958411021502d9932496fa6e947b7ee6c816`. Uploaded source was formatting-equivalent but **not yet re-executed from its Git blob**; no false byte-equality claim. Raw SHA256 of local execution: `16cc557a36a050fc254edc63559473841ac21dfab378be1d854c45d9f074afb1`.
No local repository checkout/preflight, full LaTeX build, formal kernel audit or physical Turing-machine microtrace was executed. Finite checks are COMPUTATIONAL.

**ONE next dependency:** `D2-GROWING-T-SOURCE-AWARE-LB-BRIDGE` (OPEN): prove or refute a stronger lower bound after paying for polynomial-time source structural tests, tournament isomorphism/canonical labeling, equivalent-state merging and global inference, rather than assuming a complete explicit search tree. Separately test whether a source-authenticated **regular** growing tournament can satisfy comparable extension multiplicity, since the simplest circulant is a negative control.

P versus NP remains OPEN.
