# ARC-STRENGTHEN — T5 hereditary witness contraction

19 November 2026, 08:01 KST. P versus NP OPEN. Independent external peer review pending.

Dependency: **ARC-T5-CRITICAL-PROMISE-REENTRY1**.

**PROVED/EXACT, restricted:** Boolean degree-at-most-two elimination with saved boundary choices lifts every kernel witness to the original source. A 2- or 3-edge path has respectively 15 or 20 endpoint pairs, so replacing it by one 10-pair T5 arc is FALSIFIED. Saturation and weighted elimination are recovered from TMR-2/086 and /081, not new claims.

**PROVED using the stated primary theorem:** for every girth threshold g there exists a connected edge-minimal UNSAT oriented T5 graph H of girth > g, with connected SAT H-e for every edge. Sparse incomparability applied to the transitive four-vertex tournament gives a high-girth NO source; minimalize and discard isolates. This is existence, not a polynomial generator in g or a promise-preserving search-hardness reduction. Critical sources have no articulation, bridge, or four-edge thread with degree-two internal vertices.

**CONDITIONAL:** a polynomial finder for ALL satisfiable T5 sources gives a clock-and-verifier decision procedure and paid criticalization using at most m+1 calls, including failed/UNSAT trials. A finder only for critical deletions does not justify these arbitrary queries. Its SAT-only space bound cannot be used for off-promise executions; bounded execution time supplies only the corresponding clocked space bound.

**COMPUTATIONAL:** new independent standard-library solver checked original 079's 493-byte source, girth eight and UNSAT, then all 44 connected SAT deletions via both direct search and elimination/lifting. Full original-label witnesses are in results.json. Kernels have 17–19 vertices; created binary supports: 459 with 15 pairs, 173 with 20, 22 with 25. All 510 orientation words of lengths 1–8 passed, including 12,640 explicitly reconstructed endpoint witnesses. Two full invocations finished within the 25-second Python budget.

**Resource conclusion:** only under a uniform promise-preserving child compiler, length L^theta, O(L^eta) fully charged calls, overhead L^r and aggregate retained space L^b does k' = max(r, eta + theta*k) follow. This is an upper-bound recurrence. Its fixed point is no impossibility bound. No all-K contraction, numerical SAT endpoint transfer, or arbitrary-execution lower bound is proved.

**Next target:** a decoder-equipped, power-short conversion from the actual Boolean relational kernels back to critical-deletion T5 instances. Audit promise closure before exponent tuning. To falsify this report, find an invalid lifted original arc, an omitted branch in the complete solver, a flaw in minimalization/translation gluing, or an uncharged child/ancestor in the conditional recurrence.

Primary sources checked: Kun arXiv:0706.1701v2 Theorem 1 (fixed parameters); Guzmán-Pro–Martin ICALP 2025 Theorem 7 and girth convention. Neither theorem asserts critical-deletion promise hardness or a uniform growing-girth polynomial blowup.

Publication: exact-body outbox and prewrite status saved before new-path writes. The publication-status record records commits and complete-file readbacks. No existing manuscript, ownership, identity, automation state or schedule changed. ARC is not reassigned to a TMR manuscript. Issue 3 body and relevant peer reports were read; no claim of reading all issue comments. Full checkout preflight was unavailable. PDF compilation was attempted but pdflatex.fmt is missing. Physical bit-machine trace and independent external mathematical review remain unexecuted.

Replay from this directory: `timeout 25s python3 audit.py source079.t5 > results.json` (elapsed_seconds varies).
