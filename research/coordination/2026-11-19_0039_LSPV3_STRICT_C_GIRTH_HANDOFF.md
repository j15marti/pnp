# Strict C handoff: criticality, incidence girth, complete deletion witnesses

**2026-11-19 00:39 PST | LSPV-3 / HYPERGRAPH-CERTIFICATES**
Research report: research/agents/lspv-3/2026-11-19_0039_LSPV3_STRICT_C_CRITICAL_GIRTH_FIREWALL.md
Executed independent compact code: experiments/t5/lspv3_strict_c_compact_control_20261119.py
Raw summary: results/raw/t5/2026-11-19_0039_LSPV3_STRICT_C_CRITICAL_GIRTH_AUDIT.json

**Strict convention:** directed triangle C, exactly 30/125 ordered triples. Q (60/125) and designated-head S (40/125) are distinct.

**PROVED/EXACT:** For simple G, the private-head one-C-per-edge lift is clause-minimal UNSAT exactly when G is edge-minimal non-5-colorable. Clause-incidence girth equals twice original undirected graph girth. Every deletion witness comes from a 5-coloring of G-e. Every full shared row is obstructed by a monochromatic edge. A critical graph makes each original block individually indispensable to a pointwise original-block cover.

**NEW GADGET FIREWALL:** The local S->C three-clause gadget preserves clause-criticality on private-head graph encodings but *forces incidence girth four*. C->S repetition also forces incidence girth four. Do not claim this local equivalence transports a growing-incidence-girth promise.

**KNOWN + PROVED TRANSFER:** High-chromatic high-girth graphs exist by Erdős. Greedy exact criticalization yields growing-incidence-girth strict C clause-critical graphs with full deletion witnesses, but finding them and their witnesses is not known to be polynomial. Explicit low-girth Mycielski^3(C_t) has v=8t+7, m=46t+6, direct C incidence girth8, three-gadget incidence girth4.

**COMPUTATIONAL:** 1,308 independently C-replayed full deletion witness vectors; 698,660 surviving original strict C clauses and 1,308 removed clauses checked by a second arithmetic predicate. Complete t5: direct236/236, triple708/708. Complete t7 direct328/328, triple36 sampled. Exact C(K6)-one-clause deletion count 76,800 via independent 5^6 scan. Original user archive verify_gadgets executed, passes C30 S40 and gadget extension histogram 85/10/20/10. Historical million-subset grid was not rerun.

**LIMITATIONS:** The Mycielski family has constant incidence girth8, not increasing. The high-girth extracted family lacks a proven polynomial generator or source-uniform deletion witness algorithm. Cover rank and girth do not imply arbitrary witness time. Specialized recognizers are not general SAT algorithms. Full local raw full-witness gzip and full two scripts preserved in the run's attached reproduction ZIP; the repository holds a concise independently executed compact script and summary. External peer review OPEN. No manuscript or schedule modified.

**Next blocker:** C-GIRTH-CRITICAL-WITNESS-ACQUISITION2. Construct an efficiently generated and authenticated growing-incidence-girth strict C clause-critical family, certify *each* deletion, and test whether GF(5), graph-coloring, flow, treewidth, compact witness or recoloring methods defeat every proposed intrinsic witness obstruction. Keep source access, failed discovery, all children and full output charged.

P versus NP OPEN.
