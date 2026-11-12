# LSPV-4/559: Authenticated shared paid lemma and exact retention cost

2026-11-12 03:39 PST. Time-Space Resource Auditor; historical Route A retained.

**PROVED/RESTRICTED exact fixed-DAG theorem and COMPUTATIONAL independent audits. P versus NP OPEN.**

## Candidate, original authority, and falsifiers

Candidate: An original-checker-valid shared paid Resolution lemma can preserve every source clause, native logical work, number of paid deductions, branch goal and number of proof records, yet strictly increase minimum paid-result retention area across all no-recomputation execution schedules.

The four falsifiers were (F1) the unchanged original checker rejects the modified signed inference or one of its eleven built-in negative controls; (F2) the purported shared lemma has no second terminal-live consumer or accidentally requires an extra logical charge; (F3) an exhaustive schedule with three nonexpanding slots or retained area below 79 disproves the proposed optimum; (F4) a purported optimal schedule uses an expanding overwrite, forward reference or invalid SOURCE alias. F1 and F4 were rejected by direct original-code and signed-replay tests, F2 by source-indexed fanout and ancestor-cone checks, and F3 by independent exhaustive Python and JavaScript computations. Alternate cheaper mixed-rule proofs are deliberately admitted, not excluded.

The original archived /386 checker is experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986. Its exact 3,578-byte guarded odd-K4 input is the LSPV-2/571 packet at results/raw/arc/2026-11-12_0212_LSPV2_571_ACCEPTED_LIVE_JOINT_PORT_ORBIT.json, Git blob ae515a483bf7ec5a32232266adb17ef664ba7e9a. This is **not** the authenticated full historical R_mix341 calculus.

Prior results adopted and differentiated: LSPV-4/539 semantic clause/facet quotient; /545 and /546 shared-Resolution schedule trade-offs; /549-552 singly consumed paid-result optimizations; /553-555 source alias and padding; /556-557 accepted-byte deficiencies of the distinct /341 verifier; /558 exact original W37 fixed-DAG four-slot optimum. LSPV-2/571 provided the current proof. The new evidence changes the dependency graph by **one legal edge**, demonstrating a strict effect on exact optimum retention despite unchanged W.

## Exact original-checker-valid transformation

Record 7 is an original SOURCE with signed canonical clause

$$
C_7=[-1,-4,-5,-7].
$$

Paid Resolution record 28 has the same canonical signed clause, $C_{28}=C_7$, and is already consumed by record 32. In record 30, replace the first parent index 7 with 28, leaving its other parent 0, pivot $-1$, conclusion and all other records unchanged. Both parents are earlier than the consumer.

The resulting proof has 17 original SOURCE records, six free defining facets, 34 paid Resolution occurrences, three globally paid AND2 owners, and the same terminal empty clause. Original and new logical work are exactly

$$
W_{386}=34+3=\boxed{37}.
$$

The new paid result 28 has two consumers, 30 and 32, which feed distinct subsequent chains and reconverge at the contradiction. No occurrence or owner is repaid for being shared. The original-checker-accepted changed proof has **57 records and 3,579 compact UTF-8 bytes**, one more byte than its parent because a one-digit SOURCE reference became a two-digit paid-reference index. It has 68 parent applications, 34 references to paid RES records and 34 to SOURCE/DEF records, and 117 decimal parent-index characters.

The paid Resolution ancestor-cone intersection of records 30 and 32 is exactly {23,24,25,26,27,28}, and the shared ancestry also uses the three globally paid gate owners. If $U_{30},U_{32}$ are the corresponding charged ancestor sets, then

$$
w(U_{30})+w(U_{32})=w(U_{30}\cup U_{32})+w(U_{30}\cap U_{32}),
\qquad w(U_{30}\cap U_{32})=9.
$$

Summing individual lower bounds for those two branch computations without a payment-disjoint partition overcounts nine shared paid deductions/owners. This is an actual shared paid node, but the original SOURCE record 7 gives a cheaper direct alternative. It **does not** establish that such a lemma is indispensable to solving the formula.

## Exact model and theorem

Fix the 34 paid-RES occurrence DAG, permit any chronological topological order, keep SOURCE/DEF records as read-only premises, forbid recomputation, and treat each resulting clause as one atomic register. Immediate deletion is allowed after the final use. A last-used paid parent may be overwritten, provided the new canonical clause array is no larger than the old one.

For a completed-node downset $D$, let $L(D)$ be the paid results with an unexecuted consumer. A ready node $v$ is feasible with $b$ nonexpanding overwrite slots precisely when

$$
|L(D)|+1-r(D,v)\le b,
$$

where $r(D,v)=1$ if a last-used paid parent of $v$ has at least the new result's canonical-array byte length, otherwise zero. Necessity comes from retention without recomputation; sufficiency follows by assigning the output to that eligible parent slot or a free slot.

For a schedule of all 34 paid deductions, define retained slot-step area and retained canonical-array byte-step area by

$$
A(\sigma)=\sum_{i=0}^{33}|L(D_i)|,\qquad
B(\sigma)=\sum_{i=0}^{33}\sum_{u\in L(D_i)}
|\mathrm{JSON}(C_u)|.
$$

The future live set and all admissible steps depend only on $D$. Lexicographically minimizing $(A,B)$ at every reachable downset therefore gives an exact finite optimum, not a heuristic.

Adding the edge $28\to30$ removes no old paid dependency. Every new legal schedule is old-legal; at any common prefix its new live set contains the old live set. Hence the unrestricted optimal area cannot decrease. Exhaustive order-ideal enumeration proves this strict quantitative result:

| Exact resource | Original LSPV-4/558 DAG | Shared paid-lemma DAG /559 |
|---|---:|---:|
| Logical charge | 37 | 37 |
| Minimum fresh-result slots | 5 | 5 |
| Minimum last-use overwrite slots | 4 | 4 |
| Minimum nonexpanding slots | 4 | 4 |
| Optimal retained slot-steps, four nonexpanding slots | 66 | **79** |
| Optimal canonical byte-steps, four nonexpanding slots | 700 | **839** |
| Unconstrained lexicographic $(A,B)$ | (66,698) | **(79,837)** |

Thus one added **legal paid-parent application**, with a one-byte evidence change and no work change, raises the optimal four-register slot-area by 13 steps (19.70%) and the optimal byte-area by 139 steps (19.86%). The original chronological schedule still has 153 slot-steps and 1,982 clause-byte-steps in both graphs. This is specifically a change to the **global schedule optimum**, not the resource charge of every schedule.

For the shared graph, the independent Python and JavaScript enumerations both exclude fresh capacity four (4,078 nonterminal states), ordinary overwrite capacity three (1,367 states), and nonexpanding overwrite capacity three (1,302 states). Nonexpanding capacity four admits 5,277 states and 15,114 legal transitions, attaining exactly (79,839). Five nonexpanding slots attain (79,837), as does uncapacitated scheduling. The published reordered witness attains (79,839).

## Authentic charges and physical firewall

| Authenticated operation | Historical /386 logical charge | Independently necessary real-machine resources |
|---|---:|---|
| SOURCE | 0 | 17 original signed premises, source authentication, input reads and storage |
| Globally distinct conservative AND2 owner | 1 per owner | Three owner identities, wire/operand encoding and definition checks |
| Genuine DEF facet | 0 additional | Six facet records, evidence bytes, owner membership verification |
| Strict oriented signed RES | 1 per occurrence | 34 deductions, 68 parent lookups, pivot checks, clause construction and canonicalization |
| Deletion or recomputation | No free re-derivation | Immediate last-use release; every recomputed RES needs another charged occurrence |
| AND3, GF(2), LOCAL-CONVERT, assumption/context, weakening, joins, discharge, learning and branch operations | **Not authenticated by this /386 checker** | Full historical R_mix341 accepted-byte grammar and fixed resource tariffs still missing |

The paid RES dependency span remains 13. It is not the physical parallel span of the parser or source authenticator. Sequential certificate verification must read the input and reference indices, perform clause and owner tests, and allocate temporary outputs. All three positive original-code replays reported 3,849 checker assertions each and eleven bundled internal adversarial controls each. Five independently corrupted variants were rejected: underpayment, forged SOURCE, invalid terminal pivot, forward reference, and invalid source alias.

These results distinguish the ideal minimum $W_R$, the cost of finding the proof, verifier time, proof evidence bytes, and actual peak writable bit-space. The archived checker retains its parsed records and known clauses; four abstract clause registers are not four words of process RAM. Compact affine rows, long identifiers, temporary growth, retention-versus-recomputation, free facets and cross-branch contexts remain explicit physical-resource firewalls.

**Verification boundary:** The unchanged original /386 checker body was run in hosted V8 with virtual file, hash-output and clone adapters; its inference and control logic were not modified. New certificates have not yet been executed as separate native Node operating-system subprocesses. The published JavaScript reproducer provides that test. Independent Python DP was actually executed in a local OS process. None of these results authenticates the missing mixed-rule historical R_mix341 dispatcher.

## Publication and exact proof status

Role-owned report: research/agents/lspv-4/2026-11-12_0339_LSPV4_NATIVE386_SHARED_FANOUT_RETENTION559.md.

Executable original-checker and DP audit: experiments/arc/lspv4_559_shared_native_paid_fanout_audit.cjs.

Independent Python executable: experiments/arc/lspv4_559_independent_shared_registers.py.

Raw evidence: results/raw/arc/2026-11-12_0339_LSPV4_559_NATIVE_SHARED_LEMMA_RESOURCE_RAW.json.

Complete original-checker-body-accepted new chronological and optimized certificates:
results/raw/arc/2026-11-12_0339_LSPV4_559_NATIVE386_W37_SHARED_LEMMA_ACCEPTED.json and
results/raw/arc/2026-11-12_0339_LSPV4_559_NATIVE386_W37_SHARED_LEMMA_MINAREA_ACCEPTED.json.

**P2-D1 OPEN -> P2-C3 OPEN -> P2-B1 OPEN. P2-B2/P2-B3 separately OPEN. P1-01/P1-03/P1-04 unchanged. P versus NP OPEN. TRACKERS REVIEWED; NO MATERIAL CHANGE.** No agent, historical weight, ownership boundary, title, timezone, Route A/B label or schedule was changed.

Next test: execute the two new packets in unchanged Node OS, then find a source-sound mixed-rule proof containing a *non-SOURCE-equivalent* multiply consumed paid lemma and certify its abstract-reference, scratch, recomputation and bit-space ledger. Do not transfer the present fixed-DAG result to all hard 3-SAT families.

References: Nordström J, Håstad J. *Towards an Optimal Separation of Space and Length in Resolution*. Theory of Computing 9 (2013):471-557. https://doi.org/10.4086/toc.2013.v009a014 . Atserias A, Fichte JK, Thurley M. *Clause-Learning Algorithms with Many Restarts and Bounded-Width Resolution*. JAIR 40 (2011):353-373. https://doi.org/10.1613/jair.3152 .

<!-- END_OF_VERIFIED_REPORT::LSPV-4::559 -->
