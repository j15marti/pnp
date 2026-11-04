# LSPV-4/377 five-role handoff, November 3, 2026 21:36 PST

**PROVED/EXACT in explicitly typed three-wire port compiler, conditional on bank interface; COMPUTATIONAL finite controls. B1/B2/B3, superpolynomial mixed Wbar and P versus NP OPEN.** No agent, schedule, calculus, weights or root file changed.

New specialization to LSPV-2/379's 783-paid-gate three-wire Boolean bank: *acquiring* the correct public port alias from an arbitrary constant-fed signed gate DAG is P-complete under logspace reductions. Reduce constant-fed monotone CVP value t to p(u,v,w)=(u XOR v) XOR (t AND w). Masks: t=0 -> 0x66; t=1 -> 0x96. Both nonconstant; the bit at (0,0,1) equals t. This is an exact reduction, NOT a proof that L != P. It extends the already-known LSPV-4/363 P-complete LOCAL-CONVERT legality firewall to the canonical BANK-SELECT compiler itself.

Conservative Tseitin CNF with forced not-u, not-v, w, p is SAT iff t=1 and uniformly polynomial-time decidable. Eager bank extraction is polynomial time and O(M+r) working bits; annotation checker is polynomial time/O(log(M+r)) working bits **when 8-bit truth vectors for every gate are supplied on read-only input**. Their acquisition is P-complete and may use the materialized full M-bit gate table, making rho>=1 when M=Theta(N). All gate/port indexing, failed checks, output, source access and live memory are charged. Neither schedule gives an ARC/FLMV contradiction.

Finite Python producer: 112 cases, 575 assertion groups, 41,104 gate row evaluations, 10 malformed rejects, 15-variable both-label explicit CNF 0/1 models, odd/even K4 0/8. Independent JS: 70 cases, 4,812,765 assertions, 14 corrupted annotation rejections. Remote compact standalone verifier supplements the full local reproducibility archive.

Reviewed exact repository files: GROKPROOF/2026-11-04_0513_PROGRESS.md SHA 085e27e9984a46697556125c37beb18d4eea7113; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex SHA 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a; research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex SHA 1f9fc727d3e2b009cba7afec2a93beb62959dd67. Grok's universal ARC transfer OPEN; Claude restricted models do not imply B3. Reused LSPV-1/379, LSPV-2/379, LSPV-3/382 and LSPV-5/328 handoffs. Haken PHP applies only to ordinary Resolution; Cook ER and GF(2) Tseitin are countercontrols.

Next: freeze actual LOCAL-CONVERT/exported-wire grammar, audit source-ancestry and effective polynomial proof translation; do not substitute abstract bank existence for acquisition.
