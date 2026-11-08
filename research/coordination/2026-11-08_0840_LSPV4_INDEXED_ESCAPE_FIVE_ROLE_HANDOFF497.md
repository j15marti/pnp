# Five-role handoff | LSPV-4/497 indexed escape on connected Resolution-hard diagonal
**November 8, 2026 08:40 PST | Route A primary, LSPV-4 resource auditor | P versus NP OPEN**

**Affected candidate node [P2-L4-497]; evidence refines [P2-A4].** [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-B1], [P2-B2], [P2-D1], [P2-C3] remain OPEN.

Building directly on the exact original, duplicate-free signed strict3 source in LSPV-2/495, the first literal ID in each four-clause vertex packet is always its unique matching variable (ID <= H). The other two IDs exceed H. For each pair j, an indexed original-order source decoder scans both halves for ID in {2j+1,2j+2}; SAT iff the two found IDs differ in any pair. This gives symbolic native FLMV WORK-logspace $O(H^2\log^3N)$ time, $O(\log N)$ space for PROMISED originals, with $N=\Theta(H\log H)$. Reordering right and left packets by matching index changes no clauses, preserves the hard ordinary Resolution UNSAT diagonal and fixed-left-then-right streaming reduction, and yields $O(H\log^3N)$ time, $O(\log N)$ space. **This does not construct, authenticate, or decide arbitrary 3CNF sources**, nor execute any hypothetical solver. No native FLMV instruction-level executable was run.

A nonmonotone *valid* perfect matching K3,3 control makes naive same-index comparison wrong: matching (0,5),(1,3),(2,4), right packet order 3,4,5; 8 false positives on equal words. Paired ordering or explicit matched-ID lookup is mandatory. Original-source rank/model controls passed all 548 tested pairs, with Python 32,918 assertions, Node 20,922; malformed trailer unchanged by promise decoder, so no total malformed claim.

LSPV-2: test proposed adaptive code-aware A->Phi(A) against this fast-indexed escape and explicitly charge public graph recognition, source reordering and all guest phases. LSPV-1/3/5: retain Haken/Urquhart Resolution hardness, GF(2)/ER paid shortcuts and context-aware shared-DAG controls; this is neither a mixed R_mix341 lower bound nor B3. P versus NP remains OPEN. All five identities, 2A/3B assignments, fixed grammar/weights and schedules unchanged.

Full report: research/agents/lspv-4/2026-11-08_0840_LSPV4_CONNECTED_TSEITIN_INDEXED_ESCAPE497.md
Code: experiments/arc/lspv4_497_indexed_original_escape.cjs
Raw: results/raw/arc/2026-11-08_0840_LSPV4_497_INDEXED_ESCAPE_RAW.json
Root main.tex blob 68188a24badda635a5983fda1c381cdb694fd497 was unreadable (zero content returned), therefore not edited.
