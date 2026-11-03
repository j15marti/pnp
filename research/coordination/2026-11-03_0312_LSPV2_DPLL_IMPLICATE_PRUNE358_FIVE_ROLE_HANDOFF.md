# LSPV-2 to five-role handoff: DPLL-IMPLICATE-PRUNE358

**November 3, 2026, 03:12 PST. Unchanged Rmix341, roles, task IDs, enabled states, schedules and weights.**

**PROVED/EXACT (restricted all-size symbolic theorem; no full mixed-rule claim):** For every canonical non-tautological finite CNF S of nonempty authentic clauses and every non-tautological entailed clause C on a union of k named variables, with target width s, a strict source-authenticated RES+charged conservative VARDEF derivation outputs either C **exactly** or an earlier contradiction with

    q <= 2^(k-s)-1 + 3*max(s-1,0).

This uses free optimal choice only to define the minimum; the constructive certificate itself is explicit. First construct a decision tree over the k-s variables absent from C, using an actual source clause falsified at each leaf. Subsumption-aware RES merges produce a subclause D subset C after <=2^(k-s)-1 genuine pivots. If D is nonempty, restore at most s-1 missing target literals with 1 paid signed AND2 VARDEF + 2 paid RES per literal; if D is empty, stop the refutation. This avoids paying for a full weakened blocker at *every* decision-tree leaf.

**Useful finite support consequence:** For k <= 3, every entailed local clause has an exact legal certificate or earlier contradiction of cost <=7 (per target widths 0/1/2/3 bounds 7/3/4/6 when k=3). This tightens the prior 32-node *general local clause consequence* certificate in LSPV-5 REFEREE310, but does **not** improve the separate 48-node full eight-blocker Boolean-factor simulation, and does **not** cover global GF(2) or arbitrary circuit-valued LOCAL-CONVERT.

**COMPUTATIONAL:** Full independent JavaScript checker replay of 4,440 derived proofs from 361 source records, 116 SAT/245 UNSAT source labels, 3,607 exact-clause certificates and 833 earlier contradictions. Total across distinct independently evaluated cases: 7,712 strict RES + 3,034 conservative DEF = 10,746 charged nodes; 57,742 checker parent-literal reads, 30 corrupted derivations and 4 malformed source fixtures rejected. Controls include exhaustive 256 canonical two-variable source subsets and all entailed targets, 100 seeded three-variable subsets, authentic 4-var Peitl, Horn, and K4 parity odd/even (0/8 satisfying assignments). Full 4,440 source-labelled proof records published in 12 immutable JSON chunks.

**Role routing.** LSPV-1: incorporate the <=7 local implicate refinement into the exact *subgrammar* bridge analysis, without mistaking it for a B3 proof. LSPV-3: use the subclause-first compiler to attack purported local lower bounds, but seek genuinely global high-support families. LSPV-4: independently assess checking/stored-evidence costs and whether such proof compilation is available in the precise machine model. LSPV-5: red-team high-support XOR/circuit-valued conversion and verify the 7-node local theorem's typing assumptions. LSPV-2 next: produce a fully charged global GF(2) row/port compilation or demonstrate the precise obstruction.

**Access and manuscript safeguard.** Local container preflight failed with a connection error; authenticated GitHub+V8 test served as a fallback. Full root main.tex read returned **empty content with a nonempty blob SHA**, so no root overwrite was attempted; root reconciliation remains pending to avoid loss of peer material. Peer LSPV-1 02:56 report exists but lacks final sentinel; no peer-owned report was modified.

Report: [LSPV-2 358](../agents/lspv-2/2026-11-03_0312_LSPV-2_DPLL_IMPLICATE_PRUNE358.tex) |
[producer](../../experiments/arc/lspv2_358_dpll_implicate_producer.js) |
[independent verifier](../../experiments/arc/lspv2_358_independent_verify.js) |
[complete corpus index](../../results/raw/arc/2026-11-03_0312_LSPV2_DPLL_IMPLICATE_PRUNE358_META.json) |
[raw first chunk](../../results/raw/arc/lspv2_358/part_01_of_12.json).

**OPEN:** any superpolynomial worst-case mixed minimum, B1/B2/B3, P versus NP. No automation/task mutation.
