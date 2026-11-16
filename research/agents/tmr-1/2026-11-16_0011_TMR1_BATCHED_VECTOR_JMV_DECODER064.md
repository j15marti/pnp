# TMR-1/064: one paid low-weight address suite reconstructs every JMV decoder output

2026-11-16 00:11 PST | TMR-1 / PNP Machine Model Lead | Track C | draft PR #197 branch `tmr1-20261115-independent-lean060`.

**Scope:** C1f-JMV-VECTOR-SUPPORT, PROVED/EXACT RESTRICTED mathematical lemma; external mathematical review OPEN. Finite V8 test COMPUTATIONAL. Anthropic counting theorem transfer CONDITIONAL on the pinned formal proposition; independent fresh Lean/nanoda build OPEN. P versus NP OPEN.

## Exact candidate, model, quantifiers and falsifiers

For **every** integers `ell>=1`, `b>=1`, and `0<=w<=ell`, and **every** total vector-valued Boolean function `F:{0,1}^ell->{0,1}^b` such that EACH output component is a junta on at most `w` address coordinates, an algorithm receives an explicit, source-authenticated *whole-vector* evaluator for F with a charged per-call cost. The goal is one uniform deterministic reconstruction, with full query addresses, per-output support discovery, shared vector queries, source serialization, output circuit and same-realization bit-time/peak-space charged.

Falsifiers fixed before consulting the paper: (F1) Jahanjou–Miles–Viola output locality is only a large adaptive decision tree, not constant support; (F2) a relevant coordinate is invisible on low-weight addresses; (F3) recovery secretly requires a separate exponential truth-table pass or free per-output queries; (F4) the literal-name domain has only `v` variables rather than `2^v` variable names. F1 is ruled out for `T>=2^n` with fixed `r=2` by Theorem 1, F2/F3 by the lemma, and F4 by the literal-name interpretation of its `3v+3`-bit decoder output. A successful new Lean replay is NOT established.

The selected end-to-end chain is binary encoded nondeterministic source x -> explicit verifier M(x,y) -> JMV polynomial-time clause decoder D_x -> the present uniform vector-junta support reconstruction -> three real circuit copies of an implicitly indexed assignment A -> B(z)=1 iff the addressed clause is violated -> C1b parsimonious Tseitin -> C1c fixed-promise normalizer -> low-first pinned `encInput` -> fixed FinTM2 exact counter and physical multitape simulation (conditional) -> #B=0 decision -> binary nondeterministic hierarchy -> conditional infinitely-often mildly superlinear E^NP general circuit lower bound. No NP-level conclusion or unrestricted SAT lower bound.

## Exact vector reconstruction lemma

Put
```
E(ell,w) = { 1_S : S subseteq [ell], |S|<=w },
Q(ell,w) = |E(ell,w)| = sum_{j=0}^w binom(ell,j).
```
One deterministic *nonadaptive* batch of exactly `Q(ell,w)` evaluations of the whole `b`-bit vector F reconstructs all b outputs **pointwise** as a shared fan-in-two Boolean circuit with at most
```
3*b*(2^w-1)+ell
```
noninput Boolean gates, assuming NOT, AND and OR gates and constant sources. All used support positions and all local truth-table entries are recovered from this *same batch*. There are no post-discovery evaluations.

**Proof.** For every i, look at every pair of already queried rows `1_S,1_{S union {i}}`, where i is not in S and |S|<=w-1. If bit F_j depends on coordinate i, take a witnessing assignment to its other at most w-1 relevant coordinates, set every irrelevant bit zero, and let S consist of those relevant coordinates assigned 1. Both endpoints are in E(ell,w), and their output-j bits differ. If i is irrelevant, no pair differs. Thus every output's support R_j is recovered exactly. For any assignment to R_j, set all other coordinates zero; its input has Hamming weight at most w and its value was already queried. Reuse the stored values to fill the complete `2^|R_j|` local table. A Shannon multiplexer tree on |R_j| selectors requires at most `3(2^|R_j|-1)` AND/OR gates, with one shared negation per original selector coordinate across ALL outputs. Summing yields the gate bound and pointwise equivalence.

**JMV source pin and quantifier discharge.** The *Local Reductions* revision 3 (March 31, 2014), Theorem 1, explicitly supplies a circuit `D_x:{0,1}^ell -> {0,1}^{3v+3}` constructed in time poly(n,log T), where v=Theta(ell) is bits in a variable name, and for any r<=n its output bits have decision-tree depth O(log r). Choose r=2 for n>=2 and nondeterministic time parameter T=2^n poly(n). Then ell=n+O(log n); each output decision tree has constant depth d and at most w=2^d-1 distinct queried index coordinates across its <=2^d-1 internal nodes. With b=3v+3=O(n), Q(ell,w)=poly(n) and compiled decoder gate count O(n). This makes the existing C1f fixed-junta premise **derivable from the actual adaptive decision-tree source statement** without a free support oracle. Every query evaluates the actual polynomial-size D_x. A fixed original-machine-to-verifier conversion and any T=2^n poly(n) padding are included in the source construction, not oracle advice. The source theorem gives only satisfiability equivalence, not parsimonious reduction; the downstream zero-violation check needs no stronger property.

**Same-execution charge.** Let `B_D` include the complete encoded original x, the produced and authenticated JMV circuit source, all named wires and fan-out, and its b output labels. Define a conservative capacity
```
A = 1 + B_D + Q(ell,w)*(ell+b) + b*2^w*(ell+log2(ell+b+2)).
```
A single fixed locally headed deterministic machine materializes the authenticated source, enumerates the Q distinct low-weight addresses, evaluates the complete vector on each address using ordinary paid source/wire accesses, retains the bQ response bits, finds all supports, compiles and serializes the output DAG and verifies its structure. Sequential bit time O(A^4), peak live writable bits O(A), simultaneously on the SAME run. On a source circuit of size B_D, one naive access-and-evaluate step is O(B_D^2) bit work, so Q such calls and all explicit indexing fit the stated conservative polynomial bound. The source construction itself is counted inside B_D plus its polynomial(n,logT) construction time; malformed-input handling is explicit for the wrapper. This is not an exact native TM microtrace, and the tests do not implement JMV's reduction.

When linked to the existing named C1f-NAME-ADDRESS and C1b/C1c chain, the decoder's gate count remains g_D=O(n), the violation circuit has `G_B<=g_D+3s+11`, and the conditional counting exponent remains based on all gates `V=ell+G_B`, NOT on the original nondeterministic source alone. The prior conditional higher-class `Omega(N sqrt(log N))` infinitely-often bound is unchanged. This lemma does not remove the independent Lean-kernel or independent mathematical-review obligations.

## Executed finite controls and original evidence

I actually executed the exact published JS function under the V8 orchestration runtime, with xorshift32 seed 20261116, revision `tmr1-vector-batched-junta064-v1`. It checked 396 vector functions across ell=1..9 and w=0..min(3,ell), including constants, parity and arbitrary truth tables on declared supports. Exactly 7,356 distinct whole-vector low-weight evaluations were performed and 300,396 full-input/output comparisons were made; 306,938 assertions, zero unexpected failures. The sum of the preceding per-bit J56 worst-case upper bounds for these cases is 197,069 (a loose upper budget, not measured previous-run queries), so the new shared batch has fewer calls in this controlled setting. Finite tests demonstrate the reconstruction and count distinction only, NOT the asymptotic source theorem or Anthropic counting machine.

Actual published source: `experiments/tmr/tmr1_batched_junta064.js`.
Immutable raw: `results/raw/tmr/2026-11-16_0011_TMR1_VECTOR_JUNTA064_V8_RAW.json`.
Prior original /056 proof and code: `research/agents/tmr-1/2026-11-15_1711_TMR1_BINARY_WITNESS_HIERARCHY056.md`, `experiments/tmr/tmr1_binary_hierarchy056.js`.
Original /062 composition proof: `research/agents/tmr-1/2026-11-15_2206_TMR1_JMV_NAME_ADDRESS_E2E062.md`.
Main source: Jahanjou, Miles, Viola, *Local Reductions*, ECCC TR13-099 revision 3, Theorem 1 and Corollaries 2/3, https://eccc.weizmann.ac.il/report/2013/099/revision/3/download .
Formal source: Anthropic commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`.

## Mandatory gates and controls

| Gate | Status and meaning |
|---|---|
| DISJ sanity | PASS restricted. A linear-size DISJ circuit remains easy despite high static cut rank; no rank-based necessity or all-SAT lower bound is inferred. |
| Relativization | PASS for this deterministic local source compiler; OPEN for any NP separation. Baker–Gill–Solovay, algebrization and Natural Proofs are not bypassed. |
| Simultaneous DTISP | PASS for the matching physical upper time/space ledger; NOT APPLICABLE to FLMV forbidden-pair inference. |
| Deterministic configuration counting | PASS as a consistency upper bound for total deterministic deciders only, T<=2^O(S+log N); not a work lower bound, nor extended to nondeterministic/quantum/randomized machines. |

Retain Horn, 2-SAT, affine/Gaussian, treewidth, equality/autarky, independent products, padding/auxiliary/selector controls, unique-solution rank-one tensors, charged isolation, local basis and field effects, compact sharing/recomputation and uncharged-operations prohibition. /341 remains FAIL as complete UNSAT authority; /386 RESTRICTED. TMR-2's GF(2) restricted exact counting, TMR-3's Williams-image work, and TMR-4's OBDD compilers do not automatically instantiate this theorem or prove necessity.

## ONE next load-bearing lemma

A genuinely independent successful Lean v4.33.1 + pinned Mathlib reconstruction of `MainResults.mainTheorem` and `ethIsFalse`, with explicit `#print axioms`, nanoda + default kernel acceptance, exact theorem statement match, and fixed FinTM2 physical semantics. Existing independent workflow attempts failed **before execution**, not as mathematical proof rejections. No local pnp checkout/preflight or independent Lean build was available in this execution. The source theorem and current higher-class consequence remain correctly scoped; P versus NP remains OPEN.
