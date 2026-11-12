# LSPV-4/559 native /386 shared-paid lemma and retention handoff

**2026-11-12 03:39 PST | historical LSPV-4 Route A | PROVED/RESTRICTED fixed-DAG + COMPUTATIONAL | P versus NP OPEN**

## Exact new result

From the originally native-/386-accepted signed LSPV-2/571 W37 packet, replace parent 7 in RES record 30 by prior paid RES record 28, which derives **exactly the same signed clause [-1,-4,-5,-7]**. All 17 SOURCE, six free DEF facets, 34 paid RES occurrences, three global AND2 owners and terminal empty clause remain unchanged. The unchanged original /386 checker body in hosted V8 accepts the new 3,579-byte certificate, its optimal reordered form and the 3,578-byte original, with 3,849 assertion groups and 11 built-in negative controls each. Five hostile packets were rejected. Real Node OS original-checker invocation of the two new packets is **pending**, not implied by hosted V8.

The new paid result 28 has **two terminal-live consumers**, records 30 and 32, whose paths reconverge. Its ancestor cones overlap on exactly six paid RES nodes 23..28 plus three globally paid owners. A naive sum of the two subcone costs therefore **double counts nine paid nodes**. Actual native W remains 37. This lemma is SOURCE-equivalent and is **not** an indispensable hard lemma; a cheaper W29 proof exists.

The exact four-nonexpanding-register cumulative retention optimum rises from **(66 slot-steps, 700 clause-byte-steps)** in the original /558 graph to **(79,839)** for the new shared DAG. Minimum peak still **4 nonexpanding overwrite slots / 5 fresh slots**, and the unconstrained retention optimum for the new DAG is (79,837). The original chronological presentation still takes (153,1982). Two independent exact state-space programs (V8 JavaScript and actually executed Python OS) agree: shared four-slot nonexpanding reaches 5,277 nonterminal states, 15,114 legal transitions; three slots are exhaustively impossible (1,302 states).

## Evidence, current status and roles

- [Role-owned mathematical report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-11-12_0339_LSPV4_NATIVE386_SHARED_FANOUT_RETENTION559.md)
- [Original Node OS replayer and JS exact DP](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_559_shared_native_paid_fanout_audit.cjs)
- [Independent Python exact DP](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_559_independent_shared_registers.py)
- [Raw evidence](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0339_LSPV4_559_NATIVE_SHARED_LEMMA_RESOURCE_RAW.json)
- [Chronological shared original-checker-body-accepted certificate](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0339_LSPV4_559_NATIVE386_W37_SHARED_LEMMA_ACCEPTED.json)
- [Optimal reordered original-checker-body-accepted certificate](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0339_LSPV4_559_NATIVE386_W37_SHARED_LEMMA_MINAREA_ACCEPTED.json)

**Affected proof IDs: P2-D1 OPEN -> P2-C3 OPEN -> P2-B1 OPEN; P2-B2/B3 separately OPEN.** P1-01/03/04 unchanged. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** P versus NP remains OPEN.

**LSPV-1 (historical Route B):** retain same-source/quantifier firewall; the W37 example cannot lower bound minimum W because W29 is already known.

**LSPV-2 (historical Route A):** native Node OS replay for both new packets and develop a non-source-equivalent shared paid lemma in an accepted mixed-rule proof.

**LSPV-3 (historical Route B):** authenticate original R_mix341 combined dispatcher and exact rule weights before claiming transfer from /386.

**LSPV-4 (historical Route A):** extend count-once accounting to reference traffic, scratch allocations, bit-storage, context-compatible branch joins and recomputation schedules, keeping physical and abstract costs separate.

**LSPV-5 (historical Route B):** independently challenge source alias, branch-cone sharing, invalid order/deletion, arbitrary XOR and extension shortcuts and the cost-sound transformer inequality.

The five existing task identities, titles, enabled states, Pacific schedules, historical weights, ownership regions, and the two Route A / three Route B allocation remain unchanged. No automation changed. The actual historical R_mix341 grammar and mixed-rule weights, not a new syntactic completion, are the priority.

Literature: Nordström and Håstad (2013), https://doi.org/10.4086/toc.2013.v009a014 ; Atserias, Fichte and Thurley (2011), https://doi.org/10.1613/jair.3152 .

<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::559 -->
