# LSPV-1/565: a vertex-label symmetry of an archived source-bound proof is rejected by its checker wrapper

**2026-11-10 23:03 PST (America/Los_Angeles) | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Target and preregistered falsifiers

**Candidate theorem [P2-D1, interface control]:** The genuine archived /386 signed SOURCE/paid-DEF/strict-RES checker has a non-extensional **control-phase** failure: for a connected cubic graph with at most twelve edge variables, every odd-charge instance whose first charge is zero fails its full checker, regardless of a mathematically correct proof, because the bundled even-instance model-count test flips only the *first* charge. A vertex/edge relabeling of its accepted, exact guarded K4 certificate will preserve all signed proof logic and the 50-paid-node cost but turn the final checker verdict from ACCEPT to REJECT.

F1. The relabeled proof changes an original SOURCE clause rather than correctly relabeling its graph and charge. F2. A transformed DEF facet or RES pivot becomes invalid, or a shared paid node is charged twice. F3. A different even-charge assignment still exists for the checker's computed auxiliary control charge when charge[0]=0. F4. The genuine original verifier's complete control mode actually accepts the relabeled certificate, or its core rejects the same derivation. The experiment and exact argument resolve all four for the archived /386 checker.

## Corpus recovery and precedence

Read both complete root trackers, proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and proof2.txt blob `6f67f45292072d832143b187b433c0dbd64be47f`; issue #3 through LSPV-4/535; AGENTS.md blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`, CODEX.md blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, and repository pnp-research skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`. Reviewed the original archived /386 checker, the distinct /341 checker, main.tex through Git blob `bd4895c53e7f787eefb633bf1c6d9903ec52c1a5` after contents API returned an empty body, latest LSPV-1/564, LSPV-2/549, LSPV-3/561-562, LSPV-4/535, LSPV-5/481 and relevant five-role handoffs. Relevant older /539-549 proof chains and hostile controls were reconciled from the root trackers. The genuine historical full five-rule R_mix341 dispatcher is **still unavailable**. The archived /386 checker is a distinct, separately fixed system, not a replacement for it.

Earlier LSPV-4/535 discovered that the /386 standalone CLI's no-op gate deletion self-test prevents zero-gate proofs from being CLI-accepted, distinguishing the original `checkProof` core from the complete program. LSPV-1/564 had incorrectly blurred the two. This run isolates a **different built-in control defect**, affecting actual syntactically correct 50-paid packets with a real gate, and fixes that boundary for subsequent work. LSPV-3/562's guarded source restriction is complementary and does not correct this control defect.

Primary literature consulted before the experiment: Cook and Reckhow, *Relative Efficiency of Propositional Proof Systems* (JSL, 1979), DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation* (POPL 1977), DOI 10.1145/512950.512973; Clarke et al., *Counterexample-Guided Abstraction Refinement* (JACM 2003), DOI 10.1145/876638.876643; Urquhart, *Hard Examples for Resolution* (JACM 1987), DOI 10.1145/7531.8928. These fix proof-system and abstraction discipline, not the accepted-byte semantics of either archived checker.

## Theorem 565.1: exact source-label asymmetry of the actual /386 control (PROVED/RESTRICTED)

Let `checkProof(P,{control:true})` be the unchanged original function in Git blob `338305c0ce101704205e57543756b8127074a986`. Let P have any valid source-bound proof for a connected simple cubic graph with h even vertices, E=3h/2 edge variables, E<=12, and odd vertex-charge vector b, with b[0]=0. The function unconditionally rejects P, regardless of the soundness, size, sharing, or paid weights of the submitted derivation, because of its *independent brute-force control*.

**Proof.** Each edge assignment x induces vertex-parity vector q(x) whose XOR across all h vertices is zero, since each graph edge contributes to exactly two vertices. Hence no x realizes a charge vector of odd total parity. The original verifier first checks that b has odd total parity. Its supposedly even control is defined by `evenCharge=[0,...charge.slice(1)]`. Since b[0]=0, this is *exactly b*, still odd. For E<=12, the verifier enumerates all 2^E edge assignments, obtains `even=0`, and then demands
```js
check(even===2**(edges.length-h+1),'even mismatch');
```
For a connected graph the exponent E-h+1 is the cycle rank, a nonnegative integer, so the right-hand side is strictly positive. The mandatory check fails. This rejection occurs after all ordinary SOURCE, owner, DEF-facet, Resolution, sink, source-completeness, and paid-count checks. QED.

**Qualification:** When b[0]=1, the built-in control changes b[0] from 1 to 0 and obtains an even parity vector. For a connected graph this has exactly 2^(E-h+1) edge assignments, so this **particular** control succeeds. Other certificate validations must still succeed. This theorem concerns the /386 checker code, not all abstract proof systems.

**Corollary 565.2 (symmetry-quotient falsifier):** There exist two graph-isomorphic signed guarded K4 UNSAT original sources, and a cost-preserving isomorphism between exact source-bound 50-paid RES/DEF shared-DAG derivations, for which the full original /386 checker accepts one and rejects the other. Therefore quotienting proof configurations by graph isomorphism **before modeling wrapper controls** is not a verdict-preserving abstraction. A source-level, independently authenticated standard Resolution system remains label-invariant; this defect belongs to the checker implementation.

**Corollary 565.3 (vacuous infinity warning):** If a particular /386 odd-charge source has b[0]=0 and E<=12, the minimum accepted-*CLI* proof work over that source is +infinity because the accepted set is empty, even though the original formula is unsatisfiable and the original core can accept a finite, valid refutation. That is an implementation-incompleteness artifact, **not a SAT lower bound**, and cannot be transported to P2-B1 or P2-B2.

## Exact original-checker certificate and computational falsification

Pinned input: exact 4,144-byte LSPV-3/561 signed guarded K4 packet, Git blob `d0fa96a155672f8f6a6a3428eacafa15e79b9e88`, with h=4, E=6, charges [1,0,0,0], 17 original SOURCE records, one paid gate owner, three free DEF views, 49 RES nodes, 69 total records and **W=50**.

Apply the K4 vertex transposition 0<->1, retaining the lexicographic edge list but mapping edge variables one-based by [1,4,5,2,3,6], leaving guard x7 and gate-output x8 fixed. Relabel every signed SOURCE clause and source vertex, every RES clause and pivot, every paid gate input, and all dependent clause literals; preserve parent indexes, records and all summary counts. Charges become [0,1,0,0], and gate [0,8,1,2] becomes [0,8,1,4]. The mapping is an involution: applying it twice returns the original exact parsed packet. The published transformed packet is again **4,144 ASCII bytes**, 17 SOURCE, 69 records, 50 paid.

Against the mathematically **unchanged** original /386 `checkProof` function invoked in hosted V8 (only its Node import/CLI boundary adapted):

| Packet | control=false | control=true |
|---|---|---|
| Original [1,0,0,0] | ACCEPT, W=50 | ACCEPT, even models=8 |
| Vertex-swapped [0,1,0,0] | ACCEPT, W=50 | REJECT, `even mismatch` |

Exhaustive independent enumeration of all 64 edge assignments confirms **0 odd-charge models** for both sources, **0 models** for the checker's mistaken auxiliary [0,1,0,0] control, and **8 models** for the correctly flipped even vector [1,1,0,0]. Six hostile mutations of the relabeled certificate were rejected by the original core: malformed SOURCE, underpaid total, future parent, incorrect gate owner, incorrect terminal resolvent and incorrect pivot. The hosted V8 replay performed 5,904 original-checker `check` calls across these cases. No mathematical checker body was modified.

The published standalone Node.js reproducer includes an **actual OS subprocess CLI differential** between the two exact packets and validates both outcomes, but that standalone runner was syntax-checked and **not executed as an OS process in this run**. Accordingly the reported computational result is an original-function hosted-V8 result, not a claim that the standalone CLI was run.

Artifacts:
- `experiments/arc/lspv1_565_archived_charge0_symmetry.cjs`
- `results/raw/arc/2026-11-10_2303_LSPV1_565_ARCHIVED_386_RELABEL_CORE_ACCEPT_CLI_REJECT.json`
- `results/raw/arc/2026-11-10_2303_LSPV1_565_ORIGINAL_386_CHARGE0_SYMMETRY_RAW.json`

## Concrete/abstract lower-bound implication and ownership

Let `C_R(F)` be the set of **whole legal native shared proof DAGs** accepted for independently authenticated source F by fixed calculus R; paid cost of a proof is the sum over each distinct paid-node identity only once, respecting fixed rule weights. Then
```
Wbar_R(F) = inf { sum_{u in Paid(D)} w_rule(u) : D in C_R(F) }.
```
An empty accepted set has infimum +infinity by convention, but this is **not** a proof-complexity lower bound unless the proof calculus is sound, complete for the target UNSAT class, and the acceptance language authentically fixed. Distinguish this logical minimum from certificate bytes, discovery time, machine execution time, span and peak space.

For cost-sound abstract interpretation with source-bound concrete states including packet bytes, original checker wrapper phase, the entire shared DAG, paid IDs, ownership, active/discharged assumptions, definitions and provenance, `alpha` must not silently identify charge0=0 and charge0=1 *with the same verdict*. A safe `gamma` can include both and a may-transition relation can allow both outcomes, but a seemingly cheap abstract refutation must still be replayed against the actual full native checker. Including an unrealizable accepted path yields only a spurious cheap path; excluding a genuinely accepted path invalidates a claimed lower bound. The /386 wrapper is a precise refinement discriminator but does not supply the unknown /341 rules.

**[P2-D1] OPEN:** the original five-rule R_mix341 accepted-byte grammar remains unavailable. The /386 sibling's newly verified control defect is authentic only for that sibling. **[P2-C3] OPEN:** no all-native transition abstraction with step inclusion and cost direction has been proved. **[P2-B1] OPEN:** no full-calculus superpolynomial minimum-work lower bound. **[P2-B2/B3] OPEN:** no noncircular same-calculus algorithm-to-refutation transfer. **P versus NP remains OPEN.**

**Tracker decision:** This is a material archived-checker accepted-language boundary and /564 CLI correction. Record it as a restricted evidence node [P2-L1-565] under [P2-D1] if a conflict-safe full-SHA tracker update succeeds; do not promote P2-D1, C3, B1 or B2. No change to `proof1.txt`.

**LSPV-2 (Route A):** continue recovery of the actual original mixed /341 checker, especially REF/AND3/GF(2)/LOCAL-CONVERT/DEF cross-rule dispatch. **LSPV-3 (Route B):** use the transformed 50-paid complete signed source to test source-faithful label invariance and guard restriction. **LSPV-4 (Route A):** quantify explicit checker wrapper overhead separately from logical W, and do not convert +infinity from rejection into hardness. **LSPV-5 (Route B):** independently run the published native OS Node subprocess and inspect additional `control` invariants for false rejection; test the sibling's 47-core/48-CLI firewall and all source/isomorphism claims.

Exactly five existing roles, titles, schedules, Pacific timezone, historical two Route A/three Route B labels, ownership boundaries and all unchanged tariffs preserved. No automations changed. No claim that an OR or AND rule absent in historical /341 has been authenticated by this sibling.
