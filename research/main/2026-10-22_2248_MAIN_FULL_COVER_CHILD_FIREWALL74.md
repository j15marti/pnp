# FULL-COVER-CHILD-FIREWALL74

Timestamp: 2026-10-22 22:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis proves a restricted obstruction to the proposed ARC repair by block grouping. On an explicit shared-interface family, every proper block conjunction is satisfiable although the full parent is unsatisfiable. Consequently a balanced conjunction tree first exposes `UNSAT` only at its parent-sized root. This is not an unrestricted SAT lower bound: the family is transparently decidable by inspecting its source.

## Repairs fixed before source review

1. **Wide grouping:** pack many interface blocks into each mixed SAT child, within the `N^beta` child-length budget.
2. **Balanced conjunction tree:** recursively merge groups so that incompatibility becomes visible at an internal node.
3. **Selector compression:** use a selector circuit to let one small child range over many groups.

Falsifier fixed in advance: one block forbids each complete shared-interface value. The repair fails if every proper group stays satisfiable and the first negative conjunction is the full parent.

## Sources reviewed after fixing the repairs

1. `research/main/2026-10-22_2148_MAIN_INTERFACE_ADAPTIVITY_BARRIER73.md`: detached point and prefix queries retain an exponential shared-interface cost; source-aware mixed children remain the open escape.
2. `research/agents/arc/2026-10-22_ARC_DISJ37.md`: answer-only joins have near-linear communication cost on a restricted family, but source inspection defeats the family and the all-input hereditary contractor remains open.
3. `comments/grok-4.7/2026-10-22/2026-10-22_2222_GROK_REVIEW.tex`: independent review leaves every load-bearing implication open and prioritizes a fully charged, source-aware semantic quotient.

## Model and construction

Let the shared interface be `U={0,1}^k`, with `m=2^k`. For each `a in U`, block `B_a` accepts exactly `U \ {a}`. Equivalently, over interface bits `s_1,...,s_k`, `B_a` is the clause

`OR_i (s_i != a_i)`.

Define

`F_k = AND_(a in U) B_a`.

For a proper-3CNF realization, replace each long clause by the standard linear Tseitin chain with fresh block-local auxiliaries. This preserves the projection onto the shared `s` variables and costs `Theta(k)` symbols/clauses per block. Thus the full encoded parent has length `N=Theta(mk)` and a child containing `g` uncompressed blocks has length `Theta(gk)`.

## Lemma 74A — full-cover child firewall

For every `T subseteq U`,

`SAT(AND_(a in T) B_a)` iff `T != U`.

**Proof.** The feasible shared assignments are exactly `U \ T`. If `T` is proper, choose any `s in U \ T`; it satisfies every block in `T`. If `T=U`, every assignment is forbidden by its corresponding block. QED.

**Status: ESTABLISHED for the explicit family and pure block conjunctions.**

### Consequences

- Every child formed by conjoining a proper subset of blocks is `SAT`.
- Any negative child formed solely by block conjunction must contain all `m` blocks and therefore has length `Theta(N)`, not `N^beta` for fixed `beta<1`.
- In a balanced conjunction tree, every non-root node is a proper subset and is `SAT`; the first `UNSAT` node is the root.
- Group width, tree balance and adaptive choice of proper subsets do not change this fact.

This closes the first two proposed repairs in the pure-grouping model.

## Lemma 74B — label-only indistinguishability

Fix `x in U` and replace `B_x` by the tautology, obtaining `G_x`. Then `G_x` is satisfiable, with witness `x`. Every proper-subset conjunction is satisfiable for both `F_k` and `G_x`. Hence any controller whose semantic evidence consists only of the SAT labels of proper-subset conjunction children receives the all-one label vector on both an UNSAT parent and a SAT parent.

**Status: ESTABLISHED label-only/source-oblivious barrier.**

The scope is essential. A controller that reads the source can notice the tautological block or the complete forbidden-row pattern. No runtime lower bound follows.

## Selector repair

A selector child of the form “there exists a selected group whose conjunction is satisfiable” computes a disjunction of group properties. On this family every proper group is satisfiable, so the selector child is satisfiable and cannot represent the full conjunction. A selector that enforces all groups must restore their shared-source coherence and the universal conjunction; without a new source-aware compression lemma, it merely repackages the parent.

**Status: RETIRED as a generic repair.** A specific selector construction with a proved `o(N)` encoding and exact conjunction semantics is not ruled out; constructing one is the actual open burden.

## Source-channel and Circuit-SAT controls

SOURCE-CHANNEL21's inequality is valid only for its restricted interface: after a `q`-bit digest and `t` replies of at most `b` bits, at most `2^(q+bt)` transcripts occur; `h` complete equality probes can positively identify at most `h` hidden assignments per transcript. Thus average success is at most

`min(1, h * 2^(q+bt-n))`,

and uniform success at least `1/2` requires `q+bt+log2(h) >= n-1`. But the present block family exposes all forbidden rows directly in its source, so a polynomial source scan escapes the restricted query model. This confirms, rather than removes, the source-channel caveat.

Circuit-SAT does not strengthen the obstruction. A bounded-fan-in comparator circuit for each `B_a`, or its functional Tseitin encoding, has a unique gate trace once the primary assignment is fixed; that uniqueness does not create a common primary assignment. Conversely, the regular family is easy to detect by gate/clause inspection. Gate sharing and unique traces therefore supply representation controls, not class separation.

## Relation to the two P-vs-NP routes

### Ordinary MKTP/MCSP magnification

The family has a short uniform generator and fast indexed evaluation. Its large explicit block list does not imply HIGH ordinary KT, because source description and per-bit generation time must be charged. Decision-tree, communication or output-size hardness cannot be transferred to ordinary KT.

- **OPEN:** deterministic total both-label SAT-to-ordinary-MKTP construction meeting the polynomial threshold and same-machine costs.
- **RETIRED:** using this full-cover firewall itself as a HIGH-KT target.

### ARC/FLMV contraction

The firewall excludes pure conjunction grouping as the missing hereditary contractor. The conditional FLMV arithmetic remains intact if a source-aware semantic compiler produces exact children within the baseline or retuned budgets.

- **ESTABLISHED restricted:** proper block conjunctions never expose the negative label.
- **RETIRED:** wide grouping and balanced grouping as generic exact repairs.
- **OPEN:** derived source-aware constraints that compress the global forbidden cover into strictly smaller, all-input, hereditary SAT children while charging acquisition, generation, output, recursion and peak space.
- **CONDITIONAL:** the previously verified FLMV endpoint once that transformer exists.

## Independent P-vs-RP ledger

- **ESTABLISHED restricted:** local nonempty acceptance sets may have empty global intersection; short digests are not complete states; independently sampled clause occurrences break witness coherence; SOURCE-CHANNEL21 bounds a deliberately source-limited equality-probe model.
- **RETIRED:** inferring `P != RP` from those black-box/query barriers, or inferring `P=RP` from one easy verifier family.
- **OPEN (`P != RP`):** exhibit an RP language outside every deterministic polynomial-time machine.
- **OPEN (`P=RP`):** uniformly derandomize every RP machine with all source/randomness/runtime charges.

SAT in RP would imply `NP=RP`, not by itself `P=RP`. No circuit, hash, finite audit or selected verifier here resolves either question.

## Finite audit

`experiments/review/2026-10-22_full_cover_child_firewall74_audit.py` checked:

- every proper block subset through `k=4`;
- 2,500 larger random and near-full proper subsets through `k=14`;
- all 65,518 nodes in balanced merge trees through `k=14`;
- satisfiable tautology controls;
- 18,300 SOURCE-CHANNEL21 arithmetic cases.

Result: **219,117 checks, zero failures.** The audit is finite evidence only; Lemmas 74A-B are proved above.

## Five-role status and next discriminating tests

| Role | Status | Single next experiment |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Construct both labels for one source-aware target and compute ordinary KT including generator runtime and totalization table cost. |
| :12 P!=RP | **OPEN** | Replace the easily scanned forbidden-row source by a uniformly generated candidate family, then run a direct deterministic-decider control before any lower-bound claim. |
| :24 ARC/FLMV | Lemmas 74A-B **ESTABLISHED restricted** | Attempt one derived cross-block constraint of encoded length at most `N^0.5` (or the retuned beta), and measure exact source coverage rather than block count. |
| :36 P=RP | General derandomization **OPEN** | Test whether a proposed state/digest is a true congruence under every hidden source and timer influence; reject it upon one collision with different successors. |
| :48 synthesis | Pure grouping **RETIRED** | Demand a source-aware semantic compression lemma and place its measured exponents on the verified FLMV feasibility surface. |

## Conclusion

Balanced or wide conjunction grouping cannot be the missing ARC repair: an explicit parent can be minimally incompatible at the complete block cover, leaving every strictly smaller grouped child satisfiable. This narrows the constructive target to genuinely derived, source-aware semantic constraints. It neither proves an unrestricted lower bound nor advances a class separation. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
