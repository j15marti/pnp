# Strict-C global obstruction covers: GF(5) marginal false zero and source-bound certificates

**2026-11-19 America/Los_Angeles | New independent obstruction-cover agent**
**Status:** PROVED algebraic identities and sound restricted specialist; FALSIFIED GF(5) sum-as-existential; COMPUTATIONAL finite controls; OPEN unrestricted complexity.

## Predicate and exact cover

Strict T5 is R(a,b) iff (b-a) mod 5 in {1,3}; C(x,y,z) requires a directed 3-cycle in either direction. C has 30 accepted ordered tuples out of 125. The historical S, Q and P predicates remain distinct.

Let F(z,x_1,...,x_B)=AND_j F_j(z,x_j), with disjoint private sets, and define the **existential** Boolean support E_j(z)=[exists x_j F_j(z,x_j)]. Global UNSAT is exactly
`forall z, OR_j (1-E_j(z))=1`, equivalently `W(z)=product_j E_j(z)` being the zero **function** on F5^k. A row index without its negative certificate, or success on non-exhaustive listed rows, is not a global UNSAT explanation.

## GF(5) marginalization falsifier (PROVED)

Take the connected strict-C block C(z,a,b) AND C(z,a,c), with three private variables a,b,c. Fix z to any color. The C(z,.,.) link graph is a 4-vertex path, whose degrees are 1,2,2,1; consequently the number of completions is 1^2+2^2+2^2+1^2=10. It is SAT for **each** shared z but its ordinary GF(5) sum of satisfying private assignments is 10=0 for **each** z. Therefore sum-product marginalization in characteristic five is not sound existential projection, even on connected two-clause blocks.

For any nonempty strict-C satisfiable source, translations and reflections of the five-letter tournament preserve C and act freely on satisfying assignments (a reflection fixes only one letter but any C clause uses three). Therefore #SAT is divisible by 10. Counting modulo 2,5,10 cannot distinguish SAT from UNSAT. The connected two-clause fixture has 50 full SAT assignments and five D5 orbits, so even count-of-orbits mod 5 can be zero on SAT.

The correct cancellation-free support identity is
`E_j(z)=1-product_{x_j in F5^{m_j}} (1-T_j(z,x_j))`,
where T_j is the 0/1 strict-C local truth indicator. This is exact but has up to 5^{m_j} factors, **not** a polynomial-time acquisition claim. Global UNSAT is equivalently W=0 in the quotient function ring F5[z]/(z_i^5-z_i), not ordinary formal polynomial PIT.

## Two source-verifiable global UNSAT templates (PROVED)

1. **Primal K6:** each C source clause forces all three variable-name pairs disequal. If the primal co-occurrence graph has a K6, those six variables would need six different colors. A proof comprises six names and 15 original clause indices, one demonstrating each pair. Verifier checks the exact source clauses. The automated, no-advice specialist returns UNSAT+certificate or UNKNOWN.
2. **Three-completions capacity:** original clauses C(a,b,e), C(a,c,e), C(a,d,e), C(b,c,d) on five distinct names. The fixed-color pair (a,e) has at most two different C-completing colors, while C(b,c,d) requires three different colors. Four original source clause indices and five names certify UNSAT for **all** shared assignments. This is the already classified strict-C type-1 minimal obstruction, now used as a source-bound universal-cover certificate. Its primal graph is K5, which is 5-colorable, so primal-coloring alone cannot detect this strict-C failure.

For private-head graph edge blocks, exactly E_uv(z)=(z_u-z_v)^4 in F5. Thus W_G=product_{edges uv}(z_u-z_v)^4 is precisely the Boolean graph 5-coloring indicator. K6 gives a short symbolic cover; K6-e has exactly 120 valid shared colorings, yet sum_z W_{K6-e}(z)=120=0 mod 5. Zero arithmetic sum is not zero support.

## Executed tests and falsifiers

Standard-library primary and fresh independent programs checked C/S/Q/P counts 30/40/60/20; all 125 C triples for D5 invariance; all 25 projected head pairs; 10 extensions for every shared z in the connected two-C block; and its 50 witnesses in 5 orbits of size 10.

**K6 private-head C encoding:** 21 variables, 15 clauses; 15,625 exhaustive shared rows; 234,375 original pair tests; no uncovered row; 120 one-bad-block rows for each of 15 blocks; 15 complete C deletion colorings verified against the 14 retained C clauses each. Each block is indispensable in an original-block cover, but the global pigeonhole proof is short.

**Strict-C capacity Type1:** five variables, four clauses, all 3,125 assignments exhaustively checked UNSAT; each of the four deletions has a full C-valid witness, with unique-bad-block row counts 20,20,20,90. The source-bound capacity certificate passes verification.

**Mycielski^3(C5):** rebuilt 47 base vertices/236 edges to a 283-variable, 236-clause private-head C source. The K6/capacity specialist correctly returns UNKNOWN; previous published source records, not this experiment, establish its critical UNSAT status. Historical H9/H33 are directed-edge R controls and are not silently relabeled C.

Independent replay used a separate explicit tournament table, checked 25 random source index/tuple permutations, 15 deleted-edge UNKNOWN controls, 19 full deletion witnesses and 222 retained C clause checks. Python tracemalloc and elapsed times were recorded, but are **not** machine lower bounds. Source access, validation, output and replays were charged.

A balanced-index deterministic implementation of these finite-pattern searches has upper time O(m log(n+m)+n^6 log(n+m)) and writable workspace O(n+m) words; the executed Python implementation uses hash sets. A repeated-read variant trades to O(n^6 m) time and logarithmic writable space, with source read-only and proof streamed. No general complete UNSAT specialist is claimed.

## P vs NP resource firewall

In the N^0.195-row, N^0.65-block, N^0.35-private-size layout, straightforward sequential full child decisions with exponent alpha cost N^{max(1,1.195,.845+.35 alpha)+o(1)} and require alpha <=97/70 for time N^{1.33+o(1)}. A SAT witness seed does not verify negative children or supply that exponent. Non-exhaustive rows are not a universal cover; source proof construction, child calls both polarities, failed attempts, verification and output must be paid. A uniform polynomially verifiable small UNSAT certificate for every CNF would entail NP=coNP; no unrestricted lower bound follows from these finite obstructions or restricted proof-complexity results. P vs NP OPEN.

## Provenance and next test

Prior strict source PDF: `t5_strict_research.pdf` (user Library), sections 2, 4-7. Prior project's source-readback: `research/agents/lspv-3/2026-11-19_0039_LSPV3_STRICT_C_CRITICAL_GIRTH_FIREWALL.md`; mounted prior C package used as structural control. The exact-title original strict research ZIP was not recovered this run. Literature: Gottlob-Greco-Scarcello (arXiv:1711.05216), Lauria-Nordström (CCC 2017, DOI 10.4230/LIPIcs.CCC.2017.2), Chang-Huang-Zhu (Discrete Math. 1999).

Local self-contained reproduction ZIP: `T5C_Global_Cover_GF5_Cancellation_20261119.zip`; SHA256 `c5f532a142d9b1be6d32b676d09c14a64e9ba6cbef1b9ae39943f9ef97546f20`. Contains `strict_c_global_cover_audit.py`, `independent_replay.py`, sources, all 19 deletion witnesses, raw results, full report and per-file SHA256 manifest.

**Next blocker:** derive a complete, source-verifiable bounded-width projected relation calculus that can compose negative child certificates across all z while paying full extraction/replay/space costs; test on growing-girth critical C with neither of these finite obstruction templates. Do not conflate its cost with a P vs NP proof. No existing schedules, enabled state or manuscript ownership changed.
