# LSPV-1/584: External-root-bound SOURCE multiplicity and terminal-cone normalization

**2026-11-11 17:02 PST (America/Los_Angeles) | PNP General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED symbolic statement + COMPUTATIONAL hosted-V8 replay | P versus NP OPEN**

## Single target, quantifiers, falsifiers

**Target 584.1.** In the exact, explicitly *proposed* external-root-bound, context-free SOURCE/strict-RES reference semantics extending LSPV-1/583, for every integer k >= 0, an accepted refutation of one fixed externally supplied UNSAT formula can contain k more individually well-typed but terminal-dead SOURCE records while retaining the same immutable root, identical terminal ancestors, identical distinct globally paid RES steps, and unchanged work. The source-record counter is not the number of distinct global SOURCE occurrences and is not a valid lower-bound parameter without ancestry/essentiality hypotheses.

**Falsifiers fixed before investigation:** F1: a satisfiable or occurrence-mismatched *caller* root is accepted when the packet declares a different root; F2: a redundant free SOURCE record causes reference-checker rejection or extra charged work; F3: padding a terminal-dead SOURCE record changes the terminal ancestry or unique global source identity count; F4: deleting unreferenced free SOURCE leaves changes the terminal result or paid work. The exact tested controls reject F1, and exhibit the nonoccurrence of F2-F4.

## Recovered authority, conflict/duplicate controls, literature

Both full root trackers were read at `proof1.txt` Git blob `f46f6aae25571340a5fd17a5181d51c271509947` and `proof2.txt` blob `42943fe447c6061fb8009a526f46ac8a6684765c`. Read issue #3 and latest cross-role notices (LSPV-1/583, LSPV-2/567, LSPV-3/580, LSPV-4/553, LSPV-5/498), AGENTS.md, CODEX.md, repository skill, and actual LSPV-1/539, LSPV-2/539, LSPV-3/539 and /549, LSPV-4/539, plus source-specific LSPV-1/542, /553 and LSPV-2/550-551 reports. Inspected the pinned original sibling /386 checker source (blob `338305c0ce101704205e57543756b8127074a986`) and exact LSPV-1/583 executable (blob `ecc0157627048fa481123ef1cb4835b9f4b4239e`). Searched the repository for SOURCE normalization, source essentiality, semantic MAY, mixed grammar and LOCAL-CONVERT.

**Prior claims retained, not rediscovered:** LSPV-1/574 distinguishes mandatory SOURCE presence from terminal SOURCE ancestry in the actual /386 sibling. LSPV-5/498 independently falsifies the naive /583 packet-only API by a satisfiable *caller* input and proposes an exact two-argument source-bound wrapper. LSPV-4/539 studies a clause/facet quotient in the separate /386 checker. LSPV-2/550-551 prove precision barriers for semantic MAY abstractions. LSPV-1/542 already constructs a different one-paid, polynomial-witness Tseitin macro; no new macro claim is made here. This run adds an **implemented caller-root repair and an unbounded free-SOURCE-multiplicity adversary against the actual LSPV-1/583 reference counter**, with a terminal-safe normalizer.

Primary scholarly boundaries: Cook and Reckhow (1979) [1] require an explicitly fixed sound polynomial-checkable proof system; Cousot and Cousot (1977) [2] require a sound abstract/concrete correspondence; Clarke et al. (2000) [3] distinguish genuine from spurious abstract paths; Urquhart (1987) [4] concerns ordinary Resolution on suitable Tseitin graph families, not this reference fragment or the unknown full mixed calculus.

## Exact source and accepted proof

Fix the *independent caller's* occurrence-indexed root
```
s0: [ 1, 2]    x OR y
s1: [-2]       NOT y
s2: [-1]       NOT x
```
which is UNSAT. Component A uses source occurrences s0 and s1 to derive [1] by one paid strict RES pivot 2. Component B supplies s2. The final cross-component strict RES on pivot 1 derives the empty clause. The unique globally paid node count is 2; this is the same typed refutation as LSPV-1/583. There are no assumptions, definitions, auxiliary owners, or unverified cross-rule transitions.

The implemented verifier is now explicitly `verify(packet, callerRoot)`. First, it constructs one injective canonical encoding of the ordered pairs `[source_id, signed_clause]` for both callerRoot and packet.external, rejects invalid/duplicated source IDs and malformed signed clauses, and requires exact encoding equality. Thus a packet proving a different UNSAT source cannot certify a caller's SAT formula. Every local source leaf is checked against that immutable root and every Resolution parent, signed pivot, conclusion and global paid ID is separately checked. This reference parser is **not** an authoritative historical native verifier and its input canonicalization may reject semantically equivalent but noncanonical caller encodings.

## Theorem 584.1: unbounded SOURCE-record inflation at fixed paid work

For each k >= 0, form P_k by appending k new, unique **record IDs** to Component A after its existing derivation. Every new record is free `SOURCE`, with `source_id=s0`, clause `[1,2]`, empty context, and no consumers. It repeats the same authenticated *external occurrence*, not a new axiom. Leave `callerRoot`, component source views, existing records, paid nodes, join, global terminal goal and weights unchanged.

The reference verifier's branch for a SOURCE record checks only membership of s0 in the component view and literal equality against s0 in the externally authenticated root. Each appended record satisfies both checks. Neither the type checker nor the work checker imposes a unique per-proof SOURCE-record ID for each global occurrence. Every new record has its own globally unique record ID. Parent chronology and paid identities are unchanged. Thus every P_k is accepted, with

$$
\#\mathrm{SOURCE\ records}(P_k)=3+k,\quad
\#\mathrm{distinct\ root\ occurrences}(P_k)=3,\quad
\#\mathrm{terminal\ SOURCE\ ancestors}(P_k)=3,
$$

$$
\boxed{W(P_k)=2\quad\text{for every }k\ge 0.}
$$

This is a symbolic all-k construction, not a large finite extrapolation. It **falsifies any putative lower-bound rule** `W >= #SOURCE-records - 1` absent an independently proved premise that *all those individual nodes are essential terminal ancestors*. It does **not** falsify the valid binary-ancestry counting bound `W >= #distinct terminal-live SOURCE nodes - 1` under the appropriate indegree/paid-incidence assumptions, nor the stricter source-complete /386 grammar.

## Theorem 584.2: no-consumer free-SOURCE deletion normal form

In this specific proposed context-free reference grammar, if a SOURCE record's ID appears nowhere in any later parent array, deleting that SOURCE record (and nothing else) preserves acceptance, caller-root authentication, the terminal clause, all derivations and exact paid work. No rule requires mandatory SOURCE record presence, and no rule reads a SOURCE record by hidden side channel. The chronological global IDs of all retained records remain distinct and earlier than their consumers. Iterating removes every unreferenced free SOURCE record in polynomial time without changing W. For the P_k family, the normalizer deletes exactly k records and returns the 3-SOURCE W=2 baseline.

**Boundary:** This is *not* a normal-form theorem for archived /386, whose checker expressly requires 4h+1 complete original SOURCE records, or for historical R_mix341 with unknown context, weakening, discharge, deletion, join or hidden source-presence rules. Source identity and local leaf identity must remain distinct in a future full C3 state until D1 authenticates those rules.

## Computational validation and exact scope

Published `experiments/arc/lspv1_584_external_root_source_multiplicity.cjs`; tested its actual published source in hosted V8 with a console adapter. Seven deterministic padding values k=0,1,2,4,8,16,64 all accepted, producing source-record counts 3,4,5,7,11,19,67, **each with exactly 3 unique global roots, 3 terminal SOURCE ancestors and 2 paid RES steps**. All seven safe-pruning round trips returned 3 SOURCE records at W=2. A cross-component duplicated s0 SOURCE record was also accepted with four record instances but only three root identities. Seven newly inserted independent caller mismatch controls rejected. All eleven original /583 malformed proof controls rejected, and the original 32 source-extension positives remained accepted. The root formula's exhaustive 2-bit evaluation has zero models; the caller-forged clause control changes it to a satisfiable formula. No randomness.

Raw output: `results/raw/arc/2026-11-11_1702_LSPV1_584_EXTERNAL_ROOT_MULTIPLICITY_RAW.json`. **Limitations:** the new standalone code is runnable under Node.js, but no separate operating-system Node subprocess execution is claimed. The program has not been submitted to the original /341 or /386 checker, neither of which authenticates this proposed context-free cross-component grammar.

## Quantifier and dependency ledger

- **P2-D1 OPEN.** Explicit external caller-root matching is implemented in a proposed source-bound SOURCE/RES reference, not the historical R_mix341 accepted-byte language. Full SOURCE/RES-to-AND3/GF(2)/LOCAL-CONVERT/DEF/branch/context/weakening/discharge/join/delete semantics remain unauthenticated.
- **P2-C3 OPEN.** The concrete state must distinguish external original occurrences, local SOURCE record identities, terminal ancestry, paid owners, contexts and exact weights. A scalar SOURCE-record counter is not cost-sound as a minimum-work lower-bound certificate without essentiality assumptions. No complete alpha/gamma or all-rule transition simulation is claimed.
- **P2-B1 OPEN.** No hard-family all-rule superpolynomial lower bound follows. Source padding changes evidence bits but not paid logical work; P_k is one finite easy formula.
- **P2-B2/B3 OPEN separately.** No transfer from polynomial machine time to minimum R_mix341 proof work is established. A reference proof checker is not a SAT decider.
- **P1-01/P1-03/P1-04 OPEN.** No all-input polynomial algorithm claimed.

Resource separation: the two paid RES identities are charged once globally. The k added SOURCE records are free only in *logical node work*. Serialized evidence length and parser/source validation time grow at least linearly with k; this result does not assert constant evidence bits, wall time, span, peak memory or discovery cost.

## Next five-role handoff and status

LSPV-2 (Route A): test any purported historical SOURCE reuse/duplicate prohibition and seek a real external-source-bound RES-to-AND3 accepted byte. LSPV-3 (Route B): audit context-local SOURCE identity and owner/facet effects before allowing cross-branch normalization. LSPV-4 (Route A): distinguish unique root-occurrence count from total source record count and terminal-ancestor count in resource ledgers. LSPV-5 (Route B): independently falsify caller binding, counter reporting and source no-consumer pruning, especially using duplicated signed clauses with different root occurrence IDs. LSPV-1 (Route B): maintain P2-D1 -> P2-C3 -> P2-B1 quantifier dependency and keep B2/B3 separate.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The counterexample refines an existing reference-checker guard but closes no load-bearing target. Both root proof trackers stay unchanged. Root main.tex LSPV-1-only reconciliation is a separate ownership-safe operation and must not silently strengthen OPEN nodes.

### References
1. S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44 (1979), 36-50. https://doi.org/10.2307/2273702.
2. P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977. https://doi.org/10.1145/512950.512973.
3. E. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000. https://doi.org/10.1007/10722167_15.
4. A. Urquhart, *Hard Examples for Resolution*, Journal of the ACM 34 (1987), 209-219. https://doi.org/10.1145/7531.8928.
