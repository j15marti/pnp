# ENVELOPE67-KNOWN-FRONTIER68

Timestamp: 2026-10-22 16:42 KST

**Global status: P versus NP OPEN. No load-bearing arrow closed by this note.**

## Corpus reviewed (this run)
Root `main.tex`, `AGENTS.md`, git log (last 15 commits), `research/main/2026-10-22_1548_MAIN_SHRUNK_QUERY_ENVELOPE67.md`, the 16:14 KST Grok review note in `main.tex`. Older MAIN snapshots and LSPV reports were not re-read this run (limited pass; no claim here depends on them).

## Question
ENVELOPE67 (Lemma 67C) shows that a hypothetical uniform shrunk-query transformer with (alpha, beta, gamma, delta) = (0.6, 0.5, 1.1, 0.5) would put SAT in DTISP(N^{6/5+eps}, N^{1/2+eps}). How does that conclusion sit against known SAT time-space lower bounds?

## Known theorem used (secondhand reading, verify before relying)
Williams (alternation trading, arXiv 1001.0746, Thm 3.9 as summarized by a fetch of the paper): for polynomially bounded t, s, any SAT algorithm has t*s = Omega(n^{2cos(pi/7) - eps}), 2cos(pi/7) = 1.80194. Buss-Williams: 1.80194 is the limit of the alternation-trading framework for the s = n^{o(1)} case. Status of my use: KNOWN THEOREM, statement not re-verified against the paper text (only an automated summary was read).

## Observation 68A (arithmetic, COMPUTATIONAL/EXACT)
If a transformer has fixed point (c*, s*) with c* + s* < 2cos(pi/7), then "SAT in DTISP(N^{c*+eps}, N^{s*+eps})" contradicts the known theorem for small eps. For the SMALL-INTERFACE64 parameters, c* + s* = 1.2 + 0.5 = 1.7 < 1.80194, slack 0.102. So the ENVELOPE67 target is already strictly inside the region known to be impossible for SAT.

## Consequences (all CONDITIONAL on the transformer existing and on the Williams reading above)
1. The compiler would give P != NP only in the form "no polytime decider exists", i.e. the existence of the transformer is not weaker than the separation it feeds. It cannot be a free intermediate lemma.
2. Design slack: the compiler does not need the 6/5 / 1/2 corner. Any envelope with max(gamma, alpha/(1-beta)) + max(delta, 0) < 1.80194 suffices. Examples: (0.8, 0.5, 1.1, 0.5) gives 2.1 and fails; (0.6, 0.5, 1.1, 0) gives 1.2 and passes with room. So the binding constraint is alpha/(1-beta) + delta < 1.80194, e.g. alpha < 0.9 with beta = 0.5 and delta = 0.
3. Barrier flag: the target conclusion is weaker than what alternation trading already proves unconditionally for the *real* SAT. Hence a transformer that works for hypothetical deciders must exploit the hypothesis "SAT has a polytime decider" in a way that is not just the alternation-trading speedup. Whether the 67A calls can be built without that is the open arrow; this note adds no construction.

## Not claimed
No transformer is constructed. Nothing here changes any status in `main.tex`; the new quantitative sufficient condition is a CONDITIONAL bookkeeping inequality.

## Next step (OPEN)
Verify Theorem 3.9's exact quantifier range from the paper PDF; then re-run Lemma 67C's fixed-point arithmetic for candidate (alpha, beta, gamma, delta) tuples from SMALL-INTERFACE64 variants against the inequality alpha/(1-beta)+delta < 1.80194.

% END_OF_VERIFIED_MAIN::ENVELOPE67_KNOWN_FRONTIER68
