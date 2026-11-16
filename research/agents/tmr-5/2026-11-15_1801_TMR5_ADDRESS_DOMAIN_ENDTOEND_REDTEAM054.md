# TMR-5/054 | Independent C1f address-domain and exact-count integration audit

**Pacific timestamp:** 2026-11-15 18:01 PST. **Owner:** TMR-5, PNP Machine Bottleneck Redteam. **Status:** PROVED/EXACT for the elementary address-guard lemma, RESTRICTED; independently executed COMPUTATIONAL finite replay. Mathematical peer review and Lean kernel verification OPEN. P versus NP OPEN.

**Authority:** `research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md` (main blob `8451d955f6cd5397de0895f8ebb46e30818842c3`); compatible A/B/C SAT-compression directive. This run did NOT read or edit retired proof trackers or modify another agent's living manuscript. A separate TMR-5/053 W-bar report was posted to issue #3 from branch `ccr-1695bd63-ysu7ts`; it is not asserted to be merged and is a separate proof-system track.

## Exact chain and research target

The strongest current Track C COMPLETE conditional chain is TMR-1/056 **C1f-BINARY**:

binary input x for H in NTIME(2^n) -> Jahanjou-Miles-Viola local 3-CNF source and full address-to-clause decoder D_x -> a candidate witness circuit A_N for every named variable -> a clause-violation circuit G_x on clause ADDRESS bits -> shared-gate functional count-preserving Tseitin CNF and all-input promise normalizer -> pinned finite-stack exact #SAT theorem -> ordinary physical simulation -> all-violations count zero / positive -> nondeterministic hierarchy contradiction under hypothetical small A_N.

**Chosen dependency C1f-ADDRESS:** for every m>=1, v>=1, ell>=max(1,ceil(log2 m)), total decoder D:{0,1}^ell -> (three signed v-variable literals), and a fixed assignment a in {0,1}^v, correctly distinguish the authentic first m clauses from arbitrary outputs on unused addresses. Define
```
BAD_a(i) = 1 iff all three literals in D(i) are false under a.
LEGAL_m(i) = 1 iff 0 <= i < m.
G_a(i) = LEGAL_m(i) AND BAD_a(i).
```
Prove exactly that #G_a equals the number of violated ORIGINAL clauses, and connect its output to a count-preserving 3-CNF and the source-to-hierarchy pipeline.

**Pre-search falsifiers:** (F1) a false clause on an unused address creates a spurious positive count; (F2) a gate's auxiliary assignment introduces additional satisfying extensions or loses an intended extension; (F3) legal-address detection, source parsing and arbitrary circuit access exceed the alleged gate budget; (F4) the JMV primary source already defines all 2^ell addresses as legitimate clauses, making a claimed failure of JMV itself false.

## New exact lemma and smallest lawful counterexample

**C1f-ADDRESS exact lemma (PROVED/EXACT, restricted).** Let D be total as above and let phi be the conjunction of the first m decoded clauses. For every fixed a,
```
#G_a = sum_{i=0}^{m-1} BAD_a(i),
#G_a = 0 iff a satisfies phi.
```
For any standard binary shared-gate circuit realization of G_a, a functional four-truth-row-per-gate Tseitin encoding with output pinned to one has exactly #G_a satisfying assignments, even with fan-out and repeated operands. The TMR-1 promise totalizer preserves that count.

**Proof.** Each of the 2^ell index assignments contributes one to #G_a precisely when its binary value is smaller than m and the selected clause is false. This is the displayed sum, with no multiplication for padding. Every gate z=f(u,v) is constrained by the four clauses (u != b) OR (v != c) OR (z == f(b,c)), for b,c in {0,1}; exactly the matching input pair forces z. Induction in topological order gives exactly one gate extension for every index. The positive output unit admits it iff G_a is true. Thus the compiled #CNF equals #G_a without double-counting. All input bits, auxiliary variables and gate constraints are explicit, not free side information.

**Smallest faulty unguarded interface.** Take v=1, m=1, ell=1. The authentic clause D(0)=(x_1 OR x_1 OR x_1), the unused decoder output D(1)=(NOT x_1 OR NOT x_1 OR NOT x_1), and alleged witness a=(1). Then phi is satisfiable and its sole valid clause is satisfied. Nevertheless unguarded `BAD_a` has exactly ONE accepting address (1) and a functional count-preserving CNF returns 1 instead of zero. Adding `LEGAL_1` restores exact count zero. This **falsifies the extension to arbitrary partially specified clause decoders**, not the pinned JMV theorem.

**Primary-source resolution of F4:** Jahanjou, Miles and Viola, *Local Reductions*, March 31, 2014, Theorem 1, explicitly specify `D:{0,1}^ell -> {0,1}^{3v+3}`, with `|phi|=2^ell` for the constant-locality construction at T>=2^n. Their complete address universe needs no extra range mask. In contrast, a generic m-clause source with m<2^ell must guard invalid addresses or define them as tautologies. Our counterexample is not claimed against TMR-1's actual JMV use. Primary original: https://eccc.weizmann.ac.il/report/2013/099/revision/3/download/ (Theorem 1, page 2). The pinned Anthropic `eth/MainResults.lean` blob `1c62a550fa1e4cbec65bb7112f92ad67589afddc` and `eth/Solution.lean` blob `176892178e49792ae41368c13bb4973bae035b29` were re-read from `anthropics/formal-math` commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Their source proposition and proof entry agree with TMR-1's description, but a Lean v4.33.1 kernel build and transitive `#print axioms` remain UNEXECUTED.

## Fully charged two-level ledger and remaining interface

**Symbolic uniform compiler, conditional on the original JMV D and hypothetical small W:** If D has g_D actual shared fan-in-two gates and the witness bit function A has s gates, build BAD by three shared or copied A evaluations on D's decoded literal indices, literal signs and a constant number of Boolean gates. Add an unsigned ell-bit comparison i<m, implementable with O(ell) fan-in-two gates by a prefix comparison circuit. The ordinary gate bound is
```
G <= g_D + 3s + O(ell+v+1).
```
The source read, range metadata, JMV junta-support recovery queries, clause-bit parsing, D wiring, A copies, and output gate are not free. For JMV's full domain m=2^ell, LEGAL is constant true, and this addition is unnecessary. For ell=n+O(log n), v=O(n), and g_D=O(n), the added mask is O(n); TMR-1's conditional leading coefficient 36C eta d is unchanged. Existing C1a-d compiler yields V=ell+G+O(1), m'<=4V and exact #CNF; the pinned algorithm, only if independently validated, yields T=2^((12C+o(1)) V/sqrt(log V)), with physical workspace at most O(T+B_C+B_A). The hierarchy inference requires one uniformly specified nondeterministic machine to both guess A and run this counter. The pinned count theorem is still a critical OPEN source/kernel premise. The algorithm's large writable-space upper bound does not enter FLMV small-space exclusions.

**Executed finite independent model:** The published JS actually *materializes a small explicit decoder truth table*, computes each fixed witness's violated-address set, then builds shared gates for address equality, OR, legal-domain filtering and a final AND. It exhaustively evaluates each address, constructs four clauses for EVERY truth-table gate, checks unique canonical extensions and flips each auxiliary gate value to reject erroneous extensions. This test's preprocessing is exponential in ell in general. It is **not** evidence that a succinct JMV decoder was efficiently compiled, nor a native TM cost microtrace. For its concrete explicit sources, one actual run has source acquisition O(2^ell v), emitted gate list O(2^ell ell), enumeration plus clause checks O(2^ell G^2) conservatively, and peak O(2^ell ell+G^2+v) writable words in the JS representation. Both resources belong to the same implementation. This distinction prevents silently replacing a compressed D with a free expanded truth table.

**Native Node v22 execution:** revision `tmr5-address-mask-chain054.v1`, xorshift-like LCG seed 20261115, 1,260 witness/source tests, 166,600 assertions, 626,060 checked functional Tseitin clause instances, 153,994 gate-flip negative-extension checks, 294 cases exhibiting actual unmasked phantom-address counts (including the explicit minimal falsifier), zero failed assertions. Bounded tests are COMPUTATIONAL. Code Git blob `4b955c4bb9cbe2c648f7e189bb013777314c16f6`, raw Git blob `253112fb68d435fd30a68125be68145676b97e43`. These match the locally executed source/output Git blobs exactly. No Lean, native Turing microcode, pdflatex or repository preflight was executed: there is no GitHub-connected local checkout, and the container's git DNS request failed.

## Four mandatory verification gates

| Gate | Verdict | Reason |
|---|---|---|
| DISJ sanity | **PASS (restricted)** | The identity charges only actual violated addresses and does not infer work from assignment rank. A compact DISJ circuit is allowed. |
| Relativization | **PASS lemma / OPEN separation** | The identity and functional compiler relativize; no unrestricted P-vs-NP consequence is asserted. Any NP theorem still needs its precise nonrelativizing step, algebrization and Natural Proofs checks. |
| Simultaneous DTISP | **PASS model ledger / NOT APPLICABLE to FLMV** | One actual finite checker has disjoint construction/evaluation work and a simultaneous memory ledger. TMR-1's prospective counter uses its own same-run upper bound; it does not satisfy or invoke an FLMV forbidden time-space pair. |
| Deterministic configuration counting | **PASS upper-bound guard** | For a total deterministic read-only-input machine T<=2^{O(S+log N)}. No lower bound or quantum/randomized extension is inferred. |

Horn, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarkies, independent products, all valid index masks, auxiliary-variable choices, cache/recompute, local bases over their proper fields, unique-solution rank-one collapse, randomized XOR isolation and compact circuit shortcuts remain legal. /341 is FAIL as full UNSAT authority; /386 is RESTRICTED.

## Ranked current dependency map

| Rank | Complete chain | Status and unclosed arrow |
|---|---|---|
| 1 | **TMR-1/056: binary H -> JMV local decoder -> W -> bad-address #SAT -> standard solver -> E^NP lower-bound** | **PASS** for the address identity and pinned source shape. **CONDITIONAL** for the formal exact-count theorem and its fully trusted kernel/transitive imports; source-to-E^NP inference restricted to infinitely-often Omega(N sqrt(log N)), not NP or superpolynomial. |
| 2 | **TMR-3/055, unmerged PR #169 plus TMR-5/052:** canonical CVP source -> genuine work cells -> exact P-complete output | **PASS restricted** for physical macro replay; general adaptive checkpoint provider and improved nonassociative evaluator **OPEN**. TMR-3/056 draft PR #174 is a separate charged succinct QBF tree and cheap-source control, not this missing interface. |
| 3 | **TMR-4/056:** authentic shared circuit + supplied live-frontier schedule -> FBDD -> exact decision/count/rank | **PASS restricted**, schedule discovery and unrestricted circuit transfer **OPEN**. |
| 4 | **TMR-2/056:** canonical seven-pin DIMACS -> discovered even-cycle frontier DP -> exact #CNF | **PASS restricted**, broader dynamic invariant and arbitrary shared-circuit interface **OPEN**. |

**ONE next load-bearing target:** independently rebuild the pinned Anthropic Lean `MainResults.mainTheorem` with its transitive import tree and `#print axioms` on the specified toolchain, then verify that FinTM2 finite-stack timing/input/output semantics match C1e. Until this gate closes, C1f is CONDITIONAL even though its address semantics now pass. An NP-level bridge remains OPEN.

**Publication:** own living manuscript `main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex`, this additive report, `experiments/tmr/tmr5_address_mask_chain054.js`, `results/raw/tmr/2026-11-15_1759_TMR5_ADDRMASK054_NODE_RAW.json` and compact `research/agents/tmr-5/handoff.md`. Repo-wide CI not executed. Other manuscripts, retired trackers and agent schedules untouched.
