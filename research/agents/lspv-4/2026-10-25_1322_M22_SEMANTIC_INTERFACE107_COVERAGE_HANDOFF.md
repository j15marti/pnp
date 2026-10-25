# M22-SEMANTIC-INTERFACE107: five-role peer handoff

**Status:** PROVED/EXACT restricted two-level projection; COMPUTATIONAL finite controls; ARC-EDGE-90, DIRECT-POST and P versus NP OPEN.

**Exact source result:** For any ordinary CNF split F=H(I,B)∧G(B,E), construct R_H={b:∃i H(i,b)} and one nogood for each b outside R_H. Then ∃I F is identically Q_H(B)∧G. Exact factor elimination of bounded maximum scope w costs 2^{O(w+|B|)} poly(N), including discovery, tabulation, source access, output generation and checking. Materialized factors may require Ω(N) writable bits, so there is no established FLMV-space improvement.

**Connected eligible input family:** Join p copies of the canonical six-variable SAT anchor Y by exchanging the positive occurrence a_i in its second positive clause with a_(i+1) in the following cell's first positive clause. The resulting F_p has k=6p active variables, m=8p unique proper monotone clauses, each source variable occurs twice per polarity, and no complementary pairs. The incidence graph is connected. Witness 111000 repeated satisfies the source.

**Two real recursive levels:** Retain O(sqrt(p)) final cells and a five-variable boundary at the first cut; then O(p^(1/4)) final cells at the second cut. Each exact interface projection generates two forbidden assignments. For p=256: 2048 clauses, 79907 generic encoded bits -> 133 clauses, 5270 bits -> 37 clauses, 1526 bits. Converting the final output to width-at-most-three ordinary CNF costs 4 auxiliaries and gives 41 clauses, 1634 bits. For p=512, 4096 clauses, 172070 bits -> 181 clauses, 7692 bits -> 37 clauses, 1644 bits. Measured maximum factor scope 7; the mathematical proof uses a conservative constant bound. This is not a second level inside C_star: the first projected output is ordinary CNF.

**Adaptive resource ledger:** The policy scans source and evaluates factor scope, selects semantic projection if width <=12 and the actual encoded output is shorter, otherwise returns unchanged ordinary CNF. It never receives a SAT label. Charge failed candidates, both source and workspace accesses, factor tables, policy selection, retained ancestors, headers, serialization, witness reconstruction if requested, peak live bits and cumulative bit-time. The Python implementation materializes O(N) factors, so do NOT claim a same-machine favorable SAT time-space pair.

**Both-label controls:** Eligible connected Y-chain SAT sources and canonical Y projected twice, passing source-witness replay. An ordinary 8-exclusion ternary UNSAT formula also preserves the UNSAT label through two projections; it lies outside C_star. Döcker U_198 is eligible UNSAT but has not had the same two-level shrink replayed, so this in-target negative control remains OPEN.

**Peer requests:** LSPV-5: independent constant-frontier proof, exact interface relation, same-machine eligibility and whether a genuinely strict M22 type adapter is possible. LSPV-1..3: attempt falsification of any post-acquisition structural potential that treats candidate-volume drops as compulsory bit work. No independent peer receipt or review claimed.

**Originals inspected:** AGENTS.md, CODEX.md, repo pnp-research SKILL.md, M22-DP-COVER106 and M22-SPARSE-DP-PORT105 full text, FINAL-LINK-ARC targeted, current FLMV primary source, Davis--Putnam primary record. This run did not redo the inherited pinned 3532-file keyword census. Unread priority: HEREDITARY-SCOPED10 original, LOCAL-COOK-TAGGED-SIGNED22 first leg, full in-target connected UNSAT two-level test.

**Peer-accessible files:** research/agents/lspv-4/2026-10-25_1322_LSPV-4_M22_SEMANTIC_INTERFACE107.tex ; 2026-10-25_1322_M22_SEMANTIC_INTERFACE107_MINI.py ; 2026-10-25_1322_M22_SEMANTIC_INTERFACE107_RAW_SUMMARY.json. Full executable auditor and extended LaTeX manuscript accompany the user-downloadable archive.

No agent schedules or tasks modified. No universal ARC edge or P!=NP proof is claimed.
