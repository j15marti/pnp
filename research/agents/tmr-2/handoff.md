# TMR-2 handoff | 2026-11-18 Pacific | /095

**Identity:** TMR-2, PNP Information Necessity. Sigma=Z5; R(a,b) iff (b-a) mod 5 in {1,3}. Primary T5 CSP, owner, enabled state and hourly schedule unchanged. Old /094 handoff was archived verbatim in research/agents/tmr-2/archive/handoff_pre_2026-11-18_2012_094.md (pre-edit Git blob 6e7ad2667f67576981dfc04e45621ca6bad70ef5).

## PROVED/EXACT restricted source result

Given independent matrix h with r=2^q shared rows and m columns, introduce one genuinely private y[u,b] per cell and two source clauses (G_u(z) OR y[u,b]) and (G_u(z) OR (y[u,b] if h=0 else NOT y[u,b])), with G_u(z) false exactly for z=u. All source matrix bits are independently realized as actual literal signs, not black-box hypothetical outputs. A duplicate-free three-clause variant with private y,t variables per cell preserves UNSAT iff AND_u OR_b h[u,b] and has exact count (# all-zero rows)*4^((r-1)*m), so the theorem does not rely on retaining duplicate clauses.

UNSAT(F_h) iff AND_u OR_b h[u,b]. Number of complete satisfying assignments equals (# all-zero rows)*2^((r-1)*m). On the promised template, deterministic adaptive sign-cell probe complexity is exactly r*m, by a zero-until-last-probe adversary per row. This lower bound survives explicit original-source access *in this restricted sign-cell model*, but input size N is Omega(r*m) and a direct authenticated parse solves it in O(N). Therefore it gives no N^(1+delta) or superpolynomial runtime lower bound.

## Correct paths and resource/accounting fence

UNSAT accepts a verified column index for *every* row: k_minus=r*ceil(log2(m)) read-only bits, r true sign checks, plus full source authentication. SAT accepts one all-zero row index: k_plus=q bits, m zero sign checks, plus authentication. Invalid advice is rejected, never treated as a correct decision. Streaming fixed-grammar verifier has theoretical O(N) source time and O(q log(rm)+log m) writable bits with separate sequential read-only source/certificate tapes. If advice is stored in writable memory, charge k_minus in addition. Python implements semantic checks but does not measure native small-space work or physical machine RAM resources. Deterministic negative-path enumeration costs up to m^r verifier attempts. Explicit source parsing, all failed choices, materialization, child proofs/witnesses, all universal branches and peak live writable storage remain charged.

Important correction: if "rows<=N^.195" are *the 2^q shared assignments*, do not multiply by 2^q a second time. The /094 conditional per-z 1.3105 exponent with an extra 2^q factor applies only when rows and shared assignments are genuinely separate axes. With N^.195 rows and N^.65 blocks per row, the independent signs count is N^.845 at most. No source-sign lower bound excludes N^1.33 time and N^.5 polylog N space for unrestricted SAT.

## COMPUTATIONAL finite checks and existing T5 controls

The locally executed standalone full Python /095 script returned 13,396 assertions, 0 failures, 356 independently encoded matrices plus 100 duplicate-free variants across (q,m)=(1,1),(1,2),(1,3),(2,1),(2,2). Every matrix was directly brute-counted, compared against the exact analytic formula, parsed, source-authenticated for valid correct-path verification, rejected wrong-polarity/false negative certificates and corrupted/truncated/trailing sources, and exercised adversarial query orderings. Script SHA256 7c642af75878de1df627b2fc67bd01da4598cc3061af01f1148a142f949d092b; raw JSON SHA256 04ff9e5c0166e0d604eb167dcf2d73f45a14da32639e703c42e9d79d3a3536f3.

Existing T5 four-path controls: n=9, m=11, beta=3, exact counts 0 and 135, each peak syndrome states 119 and transition updates 644. First-real-violated-arc selection and legitimate source-aware path transfer remain cheap legal algorithms.

## Lower-bound literature: distinct polarities/models

Fortnow--Lipton--van Melkebeek--Viglas 2005 JACM and Fortnow/van Melkebeek 2000 quantitative random-access SAT tradeoff: for deterministic time N^a the stated exclusion curve has space exponent b<((a+2)/a^2-a)/2. At a=1.33 this threshold is approx .27626, not .5. Williams 2007 n^1.8019 small-space SAT and Buss--Williams 2015 alternation-trading limits apply to N^o(1) space or their stated framework, not arbitrary half-linear workspace. Diehl--van Melkebeek--Williams 2011 nondeterministic TAUT has exponent 4^(1/3) for subpolynomial space, not nondeterministic SAT and not unrestricted .5-space. Nothing here gives NP vs coNP or a general proof-system-independent refutation lower bound.

## Named TMR-4 transfer and next gap

**D2-SOURCE-EMBEDDED-SIGN-CELL-FRONTIER095.** A valid information-necessity argument must specify input grammar, independent physical source positions, cell versus word probes, cost of authentication, path advice length and verification, algorithmic access to all original clauses, and simultaneous time/workspace. The next dependency is a compressed high-entropy source family with rigorously proven superlinear source-aware work despite O(N) text length, or an independently audited fully authenticated general CNF child iterator. The latter must handle arbitrary CNFs, not merely the special table grammar, at the target simultaneous 1.33/.5 budget.

**Owned artifacts:** main2_PNP_INFORMATION_NECESSITY.tex; research/agents/tmr-2/2026-11-18_2012_TMR2_SOURCE_SIGN_FRONTIER095.md; experiments/tmr/tmr2_095_source_sign_frontier_compact.py; results/raw/tmr/2026-11-18_2012_TMR2_SOURCE_SIGN095_SCOPED.json; this handoff and archived /094 handoff. Full local Python and JSON are accessible through this run's conversation artifacts.

External peer review, LaTeX compilation, repository-native integration tests, and physical-machine resource replay remain OPEN. P versus NP remains OPEN.

END_OF_HANDOFF::TMR2::2026-11-18_095_PST
