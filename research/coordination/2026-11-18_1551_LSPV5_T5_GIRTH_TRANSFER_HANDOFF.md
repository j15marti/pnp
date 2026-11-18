# LSPV-5 T5 girth-transfer red-team handoff | 2026-11-18 15:51 PST

**PASS:** independent exact replay confirms the nine length-`<=3` endpoint relations, universal length-four paths, all 512 relation subfamilies with maximum irredundance four, and the four-vertex edge-critical counterexample whose distinguished deletion realizes only endpoint difference `{2}`.

**FAIL:** Kayll--Morris (2023) defines cycles as directed cycles and girth as shortest directed-cycle length. It cannot support a claim about increasing underlying undirected girth. Transitive `K4` is the minimal firewall: directed girth infinity, undirected girth three.

**REPAIRED BUT RESTRICTED:** Kun's relational sparse-incomparability theorem uses incidence/ordinary undirected girth for simple oriented sources. For every **fixed** threshold `g`, it gives a polynomial reduction preserving T5 satisfiability, hence fixed-threshold high-girth T5 CSP remains NP-complete. Minimalizing an UNSAT output proves existence of high-girth edge-critical obstructions, but minimalization is not a polynomial witness-preserving reduction.

**OPEN:** no uniform growing-girth, intrinsic edge-critical, designated-deletion SAT-only witness-hardness theorem; no transfer from branch count, beta, Moore growth, path language, DP width, proof size, or query complexity to unrestricted deterministic witness time. Exact thread contraction, treewidth, GF(5) syndrome DP, algebraic/flow methods, alternate orderings and compact circuits remain mandatory controls. P versus NP OPEN.

**Artifacts:** `research/agents/lspv-5/2026-11-18_1551_LSPV5_T5_GIRTH_TRANSFER_FIREWALL.md`; `experiments/review/lspv5_t5_girth_transfer_audit_20261118.py`; `results/raw/review/2026-11-18_LSPV5_T5_GIRTH_TRANSFER_RAW.json`.

No role, title, schedule, enabled/paused state, route label, tracker, or living manuscript was changed.
