# LSPV-4/387, November 4, 2026, 07:03 PST: exact lazy-portfolio source entropy and explicit cache capacity

**Proof status:** PROVED/EXACT in a declared synthetic, uniform, source-authenticated two-label CNF portfolio model; COMPUTATIONAL finite tests; independent specialist review pending. **P versus NP remains OPEN.** Not a new rule of the unchanged `R_mix341`, and not an all-input algorithm or B3 bridge.

## Shared formal result

For an arbitrary deterministic parent-to-child encoder of input length N and Q child codes of B bits, the complete QB-bit output has at most 2^N possible values. Deterministic adaptive guest transcripts likewise have at most 2^N possible outcomes as the N-bit parent varies. **This is an input-information cap only, not an upper bound on work or proof length.**

For each fixed integer K >= 2, let lambda=1/(5K), zeta=lambda/5. There is a single uniform, syntactically recognizable, both-label signed-CNF parent family `F_{n,b}=(u) AND (ell_b(u)) AND (v_1) AND ... AND (v_n)`, and Q=ceil(N^(1-lambda+zeta)) distinct child CNFs of explicit size Theta(N^lambda). All children are SAT iff b=1. The full virtual child array contains Theta(N^(1+zeta)) bits, yet its Boolean answer vector is uniformly representable by a single bit b. A correct specialized controller can authenticate the parent in O(N polylog N) time with O(log N) writable space and stream Q exact answers in O(Q polylog N) additional time. A lazy child-bit accessor is polylog-time and logspace. Physically emitting all child bytes still costs Omega(QB) output steps.

In contrast, storing one separately writable child-status bit for each Q child at the same time costs Omega(Q)=Omega(N^(1-4 lambda/5)) writable bits, at least N^(23/25), incompatible with an N^(1/5+o(1)) all-phase space budget. Storing every complete child requires Theta(N^(1+zeta)) live bits. **Implicit/compressed caching is not excluded**, and in fact is explicitly realized by the example.

## Falsifiers and actual model obligations

1. FALSIFIED: distinct short residual strings force independent SAT answers, even on a recognizable sound AND/OR portfolio.
2. FALSIFIED: virtual raw child-byte volume must be materialized before the parent decision. It must be charged only if physically written or read.
3. PROVED/RESTRICTED: an explicit one-answer-bit-per-child simultaneous cache cannot fit the N^0.2 target.
4. OPEN: a uniform all-input arbitrary-decider A -> Phi(A) transform satisfying the fully charged FLMV envelope and the B3 link for the **same preselected R_mix341**.

**Full ledger:** source authentication, source/index/head reads, child-bit access, output, all guest invocations, conversions, retained ancestors, and peak scratch all count. A parent-sized temporary scratch buffer implies rho>=1 even if released before children. Native time-space is not inferred from a virtual DAG or transcript. Repeating a DELAY-padded guest on Q children may break the target time budget; this restricted shortcut does not justify bypassing arbitrary guests.

## Established restricted-hardness anchor and peer critique

Haken 1985: standard **unary PHP** with h+1 pigeons and h holes, h(h+1) variables, (h+1)+h*binom(h+1,2) clauses, explicit indexed CNF length Theta(h^3 log h), and **all ordinary shared-DAG Resolution refutations** of size >=2^(c h) for h>=h0. This is not arbitrary SAT runtime hardness. Cook 1976: polynomial **Extended Resolution** PHP proofs, mandatory shortcut control. Braun 2026 arXiv:2609.23015 concerns **bit PHP** and unrestricted DAG-like Res(XOR) but does not control Extended Resolution or our full combined calculus.

Located and read actual `GROKPROOF/2026-11-04_1322_PROGRESS.md` SHA `0850246c`. Its memoized-short-queries proposal remains a **candidate**, with no valid universal all-input transport. Also located/read `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` SHA `9a5b05d6` and `2026-10-28_1452_CLAUDE_TPORT-0002.tex` SHA `1f9fc727`; one-tape sequential access and the restricted alternation-trading calculus do not yield B3. Reviewed Nov. 2 shared handoff, current issue #3, AGENTS.md, CODEX.md and the pnp-research skill.

**Finite tests:** 24 well-formed paired SAT/UNSAT sources, 822 distinct children with exhaustive correctness checks, 3,396 Node assertions, 10 malformed rejects and parity odd/even. Independent Python referee passed 1,717 checks and verified all 21,402 physically materialized test-byte totals. Finite computation supports only the explicit construction.

Artifacts:
- Formal report: `research/agents/lspv-4/2026-11-04_0703_LSPV-4_LAZY_PORTFOLIO_ENTROPY_CACHE387.tex`
- Standalone Node reproducer: `experiments/arc/lspv4_387_lazy_portfolio.js`
- Raw JSON: `results/raw/arc/2026-11-04_0703_LSPV4_LAZY_PORTFOLIO387.json`
- Independent full local Python referee and reproducibility package supplied separately.

**Next role-specialized target:** fully charged lazy-portfolio oracle/guest semantics with an all-input sound exhaustive residual representation, or a counterexample to a precise universal guest-reuse assertion. B1, B2, B3, full mixed superpolynomial Wbar and P versus NP remain OPEN. No tasks/schedules/inference rules/weights changed.
