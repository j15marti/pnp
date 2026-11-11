# LSPV-4/545: Native /386 proof-DAG rescheduling versus paid recomputation

**2026-11-11 08:36 PST | PNP Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## One resource theorem and falsifiers

**Candidate.** For the archived /386 SOURCE/paid-AND2-owner/free-DEF-facet/strict-RES mathematical checker, topologically permuting an accepted chronological shared inference DAG and reindexing its ordered RES parent references preserves every original signed SOURCE, rule, deduction and fixed logical charge. Actual proof execution can have a smaller peak live-paid-result count under the same native W. A separate concrete accepted tree-unfolded certificate can reduce peak live paid results further by genuinely **paying for every repeated RES occurrence**.

F1: unchanged original complete checker rejects the remapped proof. F2: parent remapping silently changes a signed SOURCE or double-counts the once-paid owner. F3: the genuine unfolded proof is rejected or incorrectly charged as 103. F4: unmapped parents, forward reference, invalid SOURCE, corrupted paid total or terminal pivot sentinel is accepted. None occurred: all three positive packets accepted; all five hostiles rejected. GF(2), AND3, LOCAL-CONVERT and full mixed-rule transfer remain *untested* because the historical joint checker is still missing.

## Authority and corpus reconciliation

Original checker: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. Original signed bridge packet: results/raw/arc/2026-11-11_0756_LSPV1_574_BRIDGE_PACKET.json, Git blob **1efb525f0c84dfffb626c00e592f4952cc796c69**. The packet, from LSPV-1/574, has a connected 10-vertex cubic graph with one bridge, 15 edge variables, an in-band guard, 40 signed vertex SOURCE clauses plus guard unit, 102 actual paid RES deductions and one terminal-unused yet paid AND2 definition owner. Four mandatory original SOURCE records are absent from the final contradiction cone, although all 102 RES are terminal-live. Total W=102+1=103, 143 records.

Root proof1.txt read, blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b**. Root proof2.txt read, blob **7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3**. Also read issue #3 and current comments, AGENTS.md, CODEX.md, the pnp-research skill, current five-role handoffs, actual original checker and accepted packet, the historical /341 declared mixed calculus, LSPV-4/523 and /539-/544, LSPV-1/574, LSPV-2/559 and LSPV-5/489. Previous LSPV-4/523 already constructed three-slot schedules for the distinct /341 AND3/XOR **tree** corpus. This run's new concrete result concerns a genuinely shared /386 RES DAG and an authenticated Native CLI with a different grammar. Source binding to a separately supplied external DIMACS file is still absent from the original /386 (LSPV-2/559); no foreign proof grammar is silently substituted. The relevant primary literature on proof pebbling and space-length tradeoffs [1-3] does not supply the missing historical R_mix341 dispatcher.

## Theorem 545.1: order invariance at exact native W

Let P be an accepted parsed /386 mathematical proof. Permute its SOURCE, DEF and RES record identities so each remapped parent precedes its original conclusion, every record occurs exactly once, and the original empty-clause sink remains last. Leave the original SOURCE clause multiset and SOURCE provenance, gate definition declaration order, orientations, pivots, signed clauses, and payment counters unchanged. Replace each parent record index with the new index of the same old parent.

Then the resulting P' is mathematically accepted with

$$
W_{386}(P')=W_{386}(P)=N_{\mathrm{RES}}+|\mathrm{Owners}|.
$$

**Proof.** SOURCE provenance and complete source membership do not depend on proof-record order. Paid gate-owner declarations are outside the record array and unchanged. DEF facets remain valid views of the same owners. Topological induction shows every RES deduction receives its unchanged two prior signed parent clauses in the same oriented positions, and has the same canonical resolvent. All source and counter checks and final empty clause survive. Each RES record is still charged exactly once, and each globally declared owner once. QED.

The full **executable** has extra negative-control implementation restrictions (nonempty gates and terminal pivot not positive 999999, LSPV-1/571 and LSPV-4/542). Both hold in the original packet and the remappings, so all three explicitly executed certificates pass that actual full CLI. The theorem is *not* an assertion that arbitrary JSON byte manipulation or every different checker accepts.

## Theorem 545.2: exact fixed-order no-recomputation paid-result liveness

Resource model: original SOURCE clauses can be retrieved as read-only premises; a RES conclusion uses one fresh non-overwriting writable paid-result slot at creation; the RES conclusion is retained through its final consumer and cannot be recomputed for free; the new conclusion is created before expired paid parents are released. No branch or GF(2) primitive is assumed. For chronological record order \(\sigma\), the mandatory live set immediately before a paid RES operation comprises exactly earlier paid RES results with at least one remaining future use. The exact fixed-order fresh-slot peak is

$$
S_{\mathrm{fresh}}(\sigma)
=\max_{\text{RES step }i} \bigl(1+|\mathrm{LiveBefore}_{\sigma}(i)|\bigr).
$$

Removing a paid result earlier makes one later reference impossible without a new paid recomputation; retaining it later adds no benefit. Thus immediate last-use release is optimal **for each fixed order** in this explicit fresh-result/no-recompute storage model. The result does not assert globally minimal space over all schedules, overlapping in-place writes, alternate compact representations or physical machines. SOURCE retrieval and signed literals, parent indices, parsing buffers and contexts require separate physical resource accounting.

## Three actually accepted certificates and exact resource evidence

A deterministic seeded greedy topological-order search enumerated **20,000** candidate schedules with fixed LCG seed **424242**, choosing the best measured peak and breaking ties by cumulative retention. Best trial: **9849**, yielding 14 paid fresh slots rather than the original 33, with **the same W=103**.

Next, unfold the terminal shared RES DAG into a binary tree. Keep all 41 original SOURCE records exactly once, and retain the paid owner exactly once, but copy each repeated RES derivation into a *new paid chronological certificate record*. Sethi-Ullman-style dynamic programming selects the lower-peak depth-first evaluation order of its two child derivations while preserving the original oriented RES parent slots. The recursive tree expression needs eight fresh paid-result slots in the specified model. It contains **304** genuine paid RES records, thus W=304+1=305. A backwards dependency multiplicity computation independently counts 304 RES computations and 305 SOURCE premise retrievals in the unfolding.

| Authenticated packet | Original 143-record shared DAG | Reordered 143-record shared DAG | Unfolded 345-record RES tree |
|---|---:|---:|---:|
| SOURCE records | 41 | 41 | 41 |
| Paid RES records | 102 | 102 | 304 |
| Paid AND2 owners | 1 | 1 | 1 |
| **Total native logical W** | **103** | **103** | **305** |
| RES parent references | 204 | 204 | 608 |
| **Peak fresh live paid-result slots** | **33** | **14** | **8** |
| Peak stored-plus-new signed literal slots | 198 | 76 | 34 |
| Sum of retained paid slot-steps | 2024 | 717 | 1104 |
| Compact JSON encoded bytes | 9379 | 9368 | 22761 |
| Dependency span, paid RES levels | 12 | 12 | 12 |
| Original full checker | ACCEPT | ACCEPT | ACCEPT |
| Original full checker assertions, each fresh invocation | 11806 | 11806 | 28242 |
| Original internal hostile cases passed | 11 | 11 | 11 |

For fair byte comparison the 25,773-byte pretty-printed original source packet is *also* counted in compact serialization (9379). All three shared/expanded accepted packets retain the **exact same** 41 signed original SOURCE clauses and the original gate owner; the external source was not substituted.

**Original CLI authority:** The unchanged original checker source body was executed under hosted V8 with only file-input, structuredClone and output-only digest adapters. All **three** positives passed, with **51,854** original checker assertions and **33** original bundled adversarial controls. The five additional hostiles rejected are: wrong paid counter, positive-999999 terminal pivot, invalid original SOURCE, forward parent, and topological reorder with stale parent indices. The archived checker itself stores all parsed record clauses: **14 and 8 are not claims about actual V8 heap or measured peak process RSS**. The standalone Node.js reproducer was published and syntax validated, but real OS subprocess replay of the new script has **not** been executed in this run.

### Full resource ledger and abstraction firewalls

| Rule/resource | Native logical charge | Physical obligations and scope |
|---|---|---|
| SOURCE | 0 | original signed 41 SOURCE records and source occurrence authentication; input bytes, lookup/readback and parser charge not free |
| RES | 1 per occurrence | two signed ordered references, pivot validation, clause construction, old/new ID lengths and reference retrieval; 204 or 608 references |
| AND2 DEF owner | 1 per distinct owner | one paid owner globally even when unused in terminal cone; conservative fresh wire, valid definition; not charged per facet |
| DEF view | 0 additional /386 charge | physical bytes, validity checks, storage; none in this bridge packet |
| Sequential verifier work | independent of W | 11806 versus 28242 checker assertions, not CPU-time lower bounds |
| Parallel dependency span | 12 RES levels | input parsing, source bindings, controller and scheduling work separate |
| Retention | no-recompute model | explicit fresh-paid-slot counts 33/14/8; signed literals and indices charged separately |
| Recomputation | each RES rededuction costs 1 | unfolded packet 304 RES; no free semantic duplicate RES derivations |
| Peak writable memory | not measured | original Node materializes raw bytes, known clause array, clones for adversarial tests; abstract slots are not bytes/RSS |
| Branches, joins, discharge | unauthenticated in /386 | no invented context tariffs or legal mixed-rule extensions |
| GF(2), AND3, LOCAL-CONVERT | not accepted in /386 | compact affine rows and cheap XOR remain genuine potential shortcuts in the **still missing full** R_mix341 calculus |

A cost-sound all-rule P2-C3 abstraction must include each *concrete* transition and preserve contradiction reachability and an abstract path no dearer than the corresponding concrete path. The 14-slot native path has W=103, while the **different** 8-slot unfolded concrete path pays W=305. Treating the unfolded 304 deduction uses as an unpaid shortcut in the 103-unit proof would be unsound. Nor does a proof-execution schedule establish bounds on proof discovery or minimal \(W_R\) for arbitrary algorithms. There is no superpolynomial lower bound.

## Artifacts, current proof nodes and handoff

- Role-owned standalone reproducibility code: experiments/arc/lspv4_545_native_schedule_tradeoff.cjs
- Exact original-CLI-accepted reordered proof: results/raw/arc/2026-11-11_0836_LSPV4_545_REORDERED_BRIDGE_ACCEPTED.json
- Exact original-CLI-accepted expanded proof: results/raw/arc/2026-11-11_0836_LSPV4_545_UNFOLDED_BRIDGE_ACCEPTED.json
- Independent hosted original-code raw evidence and indexed permutation: results/raw/arc/2026-11-11_0836_LSPV4_545_NATIVE_SCHEDULE_TRADEOFF_RAW.json
- Five-role coordination: research/coordination/2026-11-11_0836_LSPV4_NATIVE_RES_SCHEDULE_FIVE_ROLE_HANDOFF545.md

**Affected IDs:** P2-D1 (original checker grammar is still only partial); P2-C3 (restricted realizable count-once transformation, but entire obligation OPEN); P2-B1 (OPEN). P2-B2 and P2-B3 separately OPEN. P versus NP OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE:** no claim closes a load-bearing node of either proof1.txt or proof2.txt.

All five roles, titles, schedules, time zones, historical weights, ownership boundaries, and TWO Route A/THREE Route B assignment remain unchanged. The main.tex reconciliation must preserve everything outside the existing LSPV-4 ownership markers and use full blob SHA conflict-safe readback. A missing historical combined checker blocks full-calculus closure, not restricted /386 schedule theorems.

## References

1. Nordström J. Pebble Games, Proof Complexity, and Time-Space Trade-offs. *Logical Methods in Computer Science*. 2013;9(3). https://doi.org/10.2168/LMCS-9(3:15)2013
2. Nordström J, Håstad J. Towards an Optimal Separation of Space and Length in Resolution. *Theory of Computing*. 2013;9:471-557. https://doi.org/10.4086/toc.2013.v009a014
3. Ben-Sasson E, Nordström J. Understanding Space in Proof Complexity: Separations and Trade-offs via Substitutions. arXiv:1008.1789 (2010). https://arxiv.org/abs/1008.1789
4. Cousot P, Cousot R. Abstract interpretation: a unified lattice model for static analysis by approximation of fixpoints. POPL 1977. https://doi.org/10.1145/512950.512973
