% not LaTeX: short markdown audit note (matches neighbouring universal-solver notes)
# VIRTUAL-INPUT16-THRESHOLD-SHARPEN1 | 2026-10-20 ~15:00 KST
P versus NP OPEN. No load-bearing arrow closed.

CORPUS REVIEWED: root main.tex, AGENTS.md, newest MAIN (VIRTUAL_ORDINARY_INPUT16), UNIVERSAL_SOURCE_REPLAY1 note+summary, git log of last 3h. No new LSPV-numbered reports in this window; activity is hourly Grok review annotations plus the ARC/FLMV/MMW two-spine work.

COMPUTATIONAL (exact rationals, scripts/virtual_input16_threshold_check.py, runs <1s):
1. d(241/200) = 11642479/23232400 > 1/2: CONFIRMED (matches MAIN16).
2. Fixed point of t' = max(11/10, 3/5 + g + t/2) is max(11/10, 6/5+2g); strict entry below tau=241/200 iff g < 1/400: CONFIRMED.
3. d is decreasing on [1,1.3] (checked on 1/100 grid).

NEW SMALL OBSERVATION (algebra only, CANDIDATE as a statement about the ARC route; arithmetic itself exact): the 1/400 bound is an artifact of the rational choice tau=241/200. The FLMV k=2 space-exponent d(c) exceeds 1/2 exactly when c < c*, where c* is the real root of c^3+c^2-c-2=0 (from (c+2)/c^2 - c = 1), c* = 1.2055694.... Hence the same lemma needs only g < (c*-6/5)/2 = 0.0027847... (about 1/359) instead of 1/400, a ~11% wider generator-slack window. Verified: f(241/200)<0, f(1.205569)<0, f(1.205570)>0.

Caveat: this widens only an inequality inside a hypothetical; it does not construct the generator G, the total SAT-derived Q_x, or the uniform hereditary all-input stage, which remain OPEN. Hutter-replay and MMW short-query absorption caveats from UNIVERSAL_SOURCE_REPLAY1 are untouched.

STALE/OVERSTATED: main.tex header stack of ~hundreds of identical Grok review lines adds no content; recommend LSPV-5 collapse it into one line (not edited here; outside authorized region). MAIN16 notes root main.tex had a literal placeholder at that time; current blob not re-audited here.
