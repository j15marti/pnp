# MINIMAL-CORE-SOURCE-COVERAGE75

Timestamp: 2026-10-22 23:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis extends FULL-COVER-CHILD-FIREWALL74 from grouped SAT children to two proposed source-aware repairs: extracting a small UNSAT core and emitting an ordinary resolution certificate. On the explicit full-cover family, every source block is essential. Thus every block-core is the full parent, and every standard explicit resolution refutation must touch all `2^k` source clauses. A third repair—an exact source-membership circuit—has no fixed-power sublinear representation on all truth-table sources by counting, but this only obstructs that representation strategy, not arbitrary SAT decision.

## Repairs fixed before source review

1. **Small UNSAT core:** scan the parent once, retain only a short contradictory subset, and recurse on that child.
2. **Resolution certificate:** replace the parent by a short derivation of incompatibility and verify or encode the derivation in smaller SAT children.
3. **Indexed forbidden-value circuit:** compile the source into a small circuit `C(a)` saying whether interface value `a` is forbidden, then query `exists a: not C(a)`.

The fixed falsifier was the Firewall74 family containing one block for every interface value. The first two repairs fail if deletion of any source block restores satisfiability. The third fails as a universal representation repair if arbitrary dense source tables require near-linear exact membership circuits.

## Repository sources reviewed after fixing the repairs

1. `research/main/2026-10-22_2248_MAIN_FULL_COVER_CHILD_FIREWALL74.md`: every proper block conjunction is SAT, while the full cover is UNSAT.
2. `research/main/2026-10-22_2148_MAIN_INTERFACE_ADAPTIVITY_BARRIER73.md`: detached membership and prefix queries retain exponential cost; source-aware semantic structure is the remaining escape.
3. `comments/grok-4.7/2026-10-22/2026-10-22_2319_GROK_REVIEW.tex`: independent review confirms that exact all-input heredity and fully charged source-aware compression remain OPEN.

## Construction

Let `U={0,1}^k`, `m=2^k`, and for each `a in U` let

`C_a = OR_(i=1)^k (s_i != a_i)`.

The clause `C_a` is false exactly on assignment `a`. Define

`F_k = AND_(a in U) C_a`.

The explicit long-clause encoding has size `N=Theta(mk)`. Replacing each long clause by a standard block-local proper-3CNF/Tseitin gadget preserves the projection onto `s` and retains size `Theta(mk)`.

## Lemma 75A — unique-deletion witnesses and full block core

`F_k` is UNSAT. For every `a in U`, deleting block `C_a` yields a formula whose unique shared-interface witness is `a`.

**Proof.** Every assignment `x` falsifies its corresponding clause `C_x`, so the full formula is UNSAT. After deleting `C_a`, assignment `a` satisfies every remaining clause because `a != b` for every remaining `b`. No other `x` satisfies the residual formula because its own clause `C_x` remains. QED.

Therefore every UNSAT block-core of `F_k` contains all `m` source blocks. In a proper-3CNF realization with block-local auxiliary variables, deleting an entire block still permits `a` and independent satisfying auxiliary traces for all remaining blocks. Hence the block-core conclusion survives the representation change.

**Status: ESTABLISHED for the explicit family.**

### Consequence for ARC

A child obtained solely by extracting an UNSAT source-block subset has `m` blocks and length `Theta(N)`. It cannot meet `N^beta` for any fixed `beta<1`. Small-core extraction is therefore **RETIRED as a generic ARC repair**.

This does not exclude a derived semantic constraint that is not a source subset.

## Lemma 75B — resolution source coverage

Every resolution refutation of the long-clause formula `F_k` uses every input clause `C_a`.

**Proof.** Let `S` be the input clauses actually used as axioms in a refutation. Resolution is sound, so `S` is UNSAT. Lemma 75A says every proper subset of the input clauses is SAT. Therefore `S` is the full source. QED.

The same argument applied blockwise to a functional proper-3CNF encoding shows that a refutation must use at least one clause from every source block: if it omitted an entire block, the remaining source clauses would be satisfiable.

Under a standard explicit proof encoding, a refutation therefore contains at least `m` source-axiom occurrences/references. Since `m=N/Theta(log N)`, its explicit size is `N^(1-o(1))`, larger than `N^beta` for every fixed `beta<1`.

This lower bound is tight to logarithmic/encoding factors. Pair clauses that differ only in their last literal and resolve them, producing the full `(k-1)`-variable family; repeat. The canonical refutation has `2m-1` clauses total and `Theta(mk)=Theta(N)` literal occurrences.

**Status: ESTABLISHED for standard explicit resolution and source-block references.**

### Scope firewall

- A proof format with range axioms, macros or an implicit generator is a different representation. Its short syntax may conceal a full-source validation pass or a succinct regularity argument.
- The full-cover family is easy by source inspection; a deterministic algorithm can recognize the complete canonical cover in polynomial time.
- Resolution proof size is not a lower bound against arbitrary SAT algorithms.
- The canonical proof has a short uniform indexed generator, so large materialized proof length does not imply HIGH ordinary KT.

Thus resolution certificates are **RETIRED as a generic explicit-child contraction**, not as a possible source-specific reasoning tool.

## Lemma 75C — exact membership-circuit counting barrier

Consider dense subsets `T subseteq U` and the exact membership functions `f_T(a)=1 iff a in T`. There are `2^(Omega(m))` such functions. The number of fan-in-two Boolean circuits with `k` inputs and `s` gates is at most

`2^(O(s log(k+s)))`.

Consequently some dense `f_T` require

`s = Omega(m/log m)`.

If the explicit dense block source has size `N=Theta(mk)`, this is `Omega(N/(log N)^2)=N^(1-o(1))`, exceeding `N^beta` for every fixed `beta<1`.

**Status: ESTABLISHED nonuniform counting barrier for exact membership representation.**

It does **not** lower-bound SAT decision. For this cover language the compiler only needs the one-bit question `T=U?`, and may exploit source syntax without constructing the entire membership function. Thus the counting result retires only the demand for an exact universal membership circuit.

## Circuit-SAT and witness-map comparison

- Each clause/block has a functional gate trace once `s` is fixed, but traces for different blocks share the same primary variables. Independent traces do not manufacture a common witness.
- For the complete cover, the semantic function of the entire circuit is simply constant false, so gate minimization can compress it dramatically after recognizing the source pattern.
- Tseitin uniqueness preserves the primary-witness map; it does not turn the linear-size explicit resolution proof into a runtime lower bound.
- Arbitrary dense membership tables may resist fixed-power circuit compression by counting, but no explicit hard family or class separation follows.

Circuit-SAT remains a representation and hostile-control experiment, not a third P-vs-NP spine.

## COMPACT-HISTORY20 diagnostic

The canonical resolution history has `Theta(N)` materialized size but a short indexed generator. This is the same distinction emphasized by COMPACT-HISTORY20: output/history lower bounds do not imply unrestricted computation time against succinct explicit transition or generation circuits. No native-machine time lower bound is claimed.

## Two P-vs-NP route ledger

### SAT to ordinary MKTP/MCSP

- **ESTABLISHED:** explicit proof/core materialization is nearly linear on this family.
- **RETIRED:** transferring that materialization cost to HIGH ordinary KT.
- **OPEN:** a deterministic total both-label SAT-to-ordinary-MKTP construction meeting the required threshold, indexed runtime, same-machine and source costs.

The full-cover formula and its proof are uniform and therefore natural KT-LOW controls.

### ARC/FLMV

- **ESTABLISHED restricted:** every source-subset UNSAT core is the full parent; standard resolution touches every source block.
- **RETIRED:** small extracted cores or ordinary explicit resolution proofs as generic `N^beta` children.
- **OPEN:** a genuinely derived, source-aware semantic constraint of length `N^beta`, exact on all inputs and hereditary under recursion, with aggregate probes, output, validation and peak space charged.
- **CONDITIONAL:** the verified baseline/retuned FLMV contradiction once that transformer exists.

## Independent P-vs-RP ledger

- **ESTABLISHED restricted:** local acceptance/witness sets can be individually nonempty with empty global intersection; digest/query bounds require explicit source-channel accounting.
- **RETIRED:** using resolution/core size, arbitrary truth-table circuit counting, random hashes or finite experiments to infer `P != RP` or `P=RP`.
- **OPEN (`P != RP`):** an actual RP language outside every deterministic polynomial-time machine.
- **OPEN (`P=RP`):** a uniform deterministic simulation for every promised RP machine.

For a promised RP verifier, deterministic simulation needs to hit one accepting original tape on YES inputs; it need not materialize an UNSAT refutation for each NO input. Lemmas 75A-C therefore do not resolve the RP question.

## Finite audit

`experiments/review/2026-10-22_minimal_core_source_coverage75_audit.py` checked:

- all `1,398,100` clause/assignment pairs through `k=10`, verifying that deletion of `C_a` leaves witness `a`;
- every level of the canonical resolution refutation through `k=10`;
- exact node and literal-count identities;
- fixed-power source-touch arithmetic for four `beta` values through `k=64`.

Result: **1,404,454 checks, zero failures.** This is a finite implementation audit; the lemmas are proved above.

## Five-role status and next discriminating tests

| Role | Status | Single next experiment |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Compute indexed ordinary KT for the canonical resolution proof and confirm that its short generator defeats materialization-based HIGH claims. |
| :12 P!=RP | **OPEN** | On the actual WRAPPER verifier, separate original random-tape access from proof/certificate bits and run a direct deterministic bypass control. |
| :24 ARC/FLMV | Core/proof repairs **RETIRED generically** | Attempt one non-subset derived constraint and publish its source coverage, maximum encoded length and validation cost. |
| :36 P=RP | **OPEN** | Test one structured hitting-set candidate against verifier replacement and dummy random bits; do not require NO-instance resolution proofs. |
| :48 synthesis | Lemmas 75A-C **ESTABLISHED restricted** | Reject any “small certificate” that hides a macro expansion, full-source validation, or an implicit parent-label call. |

## Conclusion

The full-cover family has no small source-subset UNSAT core, and ordinary explicit resolution cannot avoid touching every source block. Exact forbidden-membership circuits also fail to compress every dense source table to fixed-power sublinear size. These results narrow the next ARC attempt to genuinely derived semantic constraints, while simultaneously showing why proof output length cannot supply the MKTP or time lower bound. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
