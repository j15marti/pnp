# LSPV-3/508 five-agent Route B handoff (2026-11-08 11:25 PST)

**Status:** PROVED/RESTRICTED constructive all-k paid-CAST upper control; COMPUTATIONAL original-source negative controls; unrestricted P versus NP OPEN.

**Affected tracker:** [P2-L3-508] advances restricted upper evidence under [P2-D3]/[P2-C3] and composes [P2-L3-504] with [P2-L3-507], without authenticating [P2-D1] or changing OPEN [P2-B1]/[P2-B2]. No change to Route A [P1-01]/[P1-03]/[P1-04].

Using the original signed cubic odd-charge Tseitin strict 3-CNF family with 4h source clauses, independently replace ANY positional subset S of k clauses, 0<=k<=4h, with the previous source-retracting three-clause/two-fresh-variable gadget. In the separately declared typed R_CAST507(w) (fixed positive CAST fee w), derive the removed original clause by two RES plus one paid CAST for each gadget; combine four clauses per vertex using three AND3 and the h vertex parity rows using h-1 XOR. The exhibited weighted work is

$$
W_{\mathrm{constructed}}=4h+2k-1+kw,\qquad
D\le4+w+\lceil\log_2h\rceil\ (k\ge1).
$$

The upper includes all k conversion fees and permits a balanced, shared-DAG schedule. It is **NOT** a global minimum for k>1, and it is **NOT** accepted by the historical R_mix341 checker. For k=4h and w=1, verified K4/K3,3/cube work/span are (63,7), (95,8), (127,8). Independent full Python replay: 45 valid proofs, 45 corrupted rejections, 486 original-clause deletion SAT witnesses, 60 DIMACS mismatches rejected, 30 SAT/UNSAT controls. The compact published executable independently verifies 45 work/span pairs and 45 corrupt DAGs. Source-retracting Resolution hardness for H_S stays in its own ordinary Resolution model per [P2-L3-504].

**LSPV-1:** Audit the exact quantifier scope: all subsets S, fixed w per calculus, no all-rule lower or B3 conclusion. **LSPV-5:** Try proving the necessary number of CASTs is <k using sharing, DEF or other legal shortcuts in a clearly declared grammar; challenge any claimed exact minimum. **LSPV-3:** Authenticate actual historical accepted-byte RES-to-factor LOCAL-CONVERT, paid facets and private/exported DEF wires; the distinct CAST rule is not evidence of historical acceptance. **LSPV-2/LSPV-4:** Use the source family as upper-bound and same-machine resource accounting controls only; never infer FLMV contraction from ideal W.

Paths: research/agents/lspv-3/2026-11-08_1125_LSPV3_ALL_K_PAID_CAST508.md; experiments/arc/lspv3_508_paid_cast_replay.py; results/raw/arc/2026-11-08_1125_LSPV3_508_PAID_ALL_K_RAW.json. Existing five agents, their schedules, enabled states, 2A/3B route allocation, historical grammar/weights and main.tex are unchanged.