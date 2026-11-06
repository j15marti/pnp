# Five-role handoff: LSPV-3/458 published random strict-3-CNF bounded-width closure

2026-11-06 13:38 PST | LSPV-3 primary Route B | PROVED/RESTRICTED combinatorial theorem + COMPUTATIONAL controls | P versus NP OPEN.

**Established family, not newly invented:** Pang's F(n,3,8n), 8n independent indexed proper signed width-three clauses sampled with replacement over n ambient labels. Pang arXiv:2610.00837v2 reports exponential DAG Res(PC_r/F_p) lower bounds at fixed p,r; Chvatal–Szemeredi established exponential ordinary Resolution hardness. Neither theorem implies full mixed R_mix341 hardness.

**Exact local upper-shortcut filter:** Put C=binom(n,3), m=8n, p=3(n-3)/(2C), q=p+3/(8C). Expected valid source-pair width-three RES lines equals binom(m,2)*p -> 288, so immediate shortcuts do NOT disappear. The probability that two source clauses have identical triple support is at most binom(m,2)/C=O(1/n). Beyond first-generation RES, any second strict RES step with all intermediate clauses of width <=3 must fall in one of three categories: two first lines share a source; a first line resolves with a third source; or two disjoint first lines resolve. Their event-count expectations are respectively m*binom(m-1,2)*p^2, binom(m,2)*(m-2)*p*q, 3*binom(m,4)*p^2*q. Sum plus support-duplicate mean is O(1/n). This proves that width<=3 strict RES closure has depth at most one from original source clauses a.a.s. Shared DAG reuse and all optimal pivot choices are allowed.

**CRITICAL LIMITATION:** This does NOT lower-bound full native R_mix341: unrestricted-width RES may leave width three and return; AND3, LOCAL-CONVERT, XOR, paid DEF, branches/shared reconvergence remain available. It does not authenticate the historical accepted-byte checker and is not B3 or a P-versus-NP result.

**Reproduction:** 12 seeded instances at n=128/512/2048/8192; independent Python producer and independent naive Node all-pairs checker with 13 controls PASS. Source + raw SHA256 are in role report. Full program, raw data, fixture, checker and manifest in conversation ZIP; condensed GitHub code/results are at paths below.

To LSPV-1 and LSPV-5 (Route B): attack the precise first *nonlocal* step invariant. Try proving a charged obstruction for temporary width>=4, native XOR/LOCAL/DEF; test known Cook ER and Tseitin shortcuts rather than excluding them. To LSPV-2 and LSPV-4 (Route A): the bounded-width closure limit is not a same-machine algorithm lower bound, and actual construction/search, caches, representations, and peak memory must be charged.

Keep exactly existing 2 Route A/3 Route B roles, schedules, titles, IDs, weights and grammar unchanged. No native SPLIT/DISCHARGE has been introduced. Use simple chat LaTeX and `$...$`, `$$...$$` in GitHub Markdown.

Role report: `research/agents/lspv-3/2026-11-06_1338_LSPV3_RANDOM3_LOCAL_RES_CLOSURE458.md`

Reproducer: `experiments/arc/lspv3_458_random3_local_closure_replay.py`

Raw summary: `results/raw/arc/2026-11-06_1338_LSPV3_458_RANDOM3_LOCAL_CLOSURE.json`

Root `main.tex` had blob SHA a1aecc4f but zero fetched bytes: left unchanged to preserve all other roles. The handoff is the durable synthesis route.