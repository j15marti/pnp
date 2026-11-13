# LSPV-5/527 five-role handoff: native /386 polynomial Tseitin refutations (ER shortcut)

**13 November 2026, 11:48 PST | LSPV-5 Independent Proof Red Team | historical Route B | P versus NP OPEN.**

**New result [P2-L5-527], PROVED/EXACT restricted to /386 + COMPUTATIONAL.** /386 DEF gates nest and take negated inputs, so XOR costs three paid gates. Gaussian elimination along sorted XOR chains over vertex cuts yields W_386(odd cubic Tseitin(G)) = O(V*E) for every connected cubic G. Ten packets (K4 ... 40-vertex random cubic, W up to 32,903) were accepted by the unchanged /386 checker (blob 338305c0..., SHA-256 22d12f66...a113) as OS Node subprocesses, each with its own 11 corruption controls. The LSPV-2/604 DPLL scheme (my count reproduces its K4=28, cube=172) is overtaken at V=20 (13,452 vs 7,021) and at V=24 is 55,420 vs 12,736.

**Consequence:** odd cubic(-expander) Tseitin is RETIRED as a B1 hard family for /386 and for any R_mix341 reconstruction with nested DEF or GF(2) rules. B1 for such a calculus requires an Extended-Resolution-strength lower bound (none known for any family).

**Independent OS replays:** LSPV-1/620 PASS (k=6..10 ACCEPT with identical assertion counts; theorem 620.1 independently rebuilt and recounted: 64/16 and 128/32, rank identity k=6..64). LSPV-3/620 PASS/RESTRICTED: /341's changed-clause control is rejected by downstream "incorrect AND3 conjunction", not by source binding; LOCAL-CONVERT control shows rule absence, not unsoundness. LSPV-2/604 PASS as an upper bound (manifest SHA bc2001b4... reproduced); universal-B3 reading fails. LSPV-4/591 PASS/RESTRICTED: its RES-only per-instance obstruction is correct, but its F3 is realised in /386 -- the XOR-chain compiler is a native compilation of the same Gaussian-elimination decider, so W_386(F_h) <= c'(N_h+T_A(F_h))^2 and the transfer HOLDS for that (A,F_h) pair in /386.

- **LSPV-1 (B):** record that the bridge seesaw now bites on both sides: Resolution-class B3 is equivalent to P!=NP (corpus), and ER-strength calculi lose the known hard families.
- **LSPV-2 (A):** do not read DPLL-compiled W as native minimum; try the XOR-chain compiler on your /603-/604 sources and look for a cheaper chain order.
- **LSPV-3 (B):** add the 527 packets to the accepted-byte corpus as genuine cheap paths (not spurious).
- **LSPV-4 (A):** charge the 2.58 MB evidence, gate count and checker time separately from W; audit O(V*E) vs bytes.
- **LSPV-5 (B):** next, attack candidate families that resist ER-style simulation in /386 (e.g. random 3-CNF), or certify none survive.

Artifacts: research/main/2026-11-13_1148_MAIN_LSPV5_TSEITIN_ER_SHORTCUT_GATE_REPLAY527.tex; experiments/review/lspv5_527_*; results/raw/arc/2026-11-13_1148_LSPV5_527_*.

P2-D1, P2-C3, P2-B1, P2-B2/B3 OPEN. No automations, roles, schedules, weights or ownership changed. Written on branch ccr-1695bd63-baw92w (session push restriction), not directly on main.
