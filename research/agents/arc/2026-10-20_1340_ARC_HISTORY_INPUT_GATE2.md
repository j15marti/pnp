# ARC-HISTORY-INPUT-GATE2
Date: 2026-10-20 13:40 Asia/Seoul. Route 2/2 ARC/FLMV, additive COMPACT-HISTORY20. P != NP OPEN.

## PROPOSED FALSIFIABLE MECHANISMS
(1) hardwire every source input bit into a time-indexed circuit W and keep it within N^1/2 space; (2) supply source input read-only instead and charge every access; (3) use P=NP and Sigma2=P to acquire W in N^1.1 time; (4) use Williams square-root-space simulation to obtain both low time and space.

## SOURCE CHECK
Read governance COMPACT-HISTORY20, prior ARC gate1, AGENTS and current ARC main4/main5; primary Fortnow-Lipton-van Melkebeek-Viglas, JACM 2005 (author PDF https://lance.fortnow.com/papers/files/tst.pdf), Williams STOC 2025 (https://doi.org/10.1145/3717823.3718225). This is a scoped corpus review, not full repo audit. FLMV is a same-model simultaneous lower bound; Williams gives a low-space simulation without preserving original time.

## PROVED: HARDWIRED-INPUT CIRCUIT CAPACITY GATE
Fix a finite fan-in-two Boolean circuit basis, bounded fanout allowed, with no external input x, and a binary time index i. Require W_x(i) to output the i-th bit of an arbitrary N-bit string x for i in [N]. For sufficiently large N there exists x such that every such circuit has Omega(N/log N) gates, since the number of size-s circuits with O(log N) index inputs and N-indexed outputs is at most 2^{O((s+N)log(s+N))} under naive output wiring, which alone is too weak. Corrected proof: demand ONE output bit W_x(i), and count circuit descriptions of s gates plus one output: at most 2^{O(s log(s+log N))}; choosing s=cN/log N with sufficiently small c yields fewer than 2^N functions of the log N-bit index, hence some x needs Omega(N/log N) gates. This is a nonuniform counting existence theorem, NOT an explicit hard x family. In particular N/log N exceeds N^{1/2+o(1)}. If W must encode arbitrary x without source access, the target square-root-size hardwired representation is impossible on some x. This does not imply SAT hardness: W can instead receive x on a read-only input or need not reproduce all x bits.

## PROVED: ACCESS-OR-ENCODE MODEL DISJUNCTION
For this bit-selector task, either x is compiled into W (subject to the preceding worst-case circuit-counting obstruction), or x remains available externally and any claimed small-space simulation must charge its physical read-only input access and source identity. The dichotomy is about a specific representation contract, not all SAT solvers. It is not a universal time-space tradeoff: random access to read-only x can be cheap on the appropriate model.

## CONDITIONAL ARC LEDGER
For a SAT decider A of exponents t,s, let q=N^{3/5+o(1)} calls on explicit children of length N^{1/2+o(1)}. If a W generator takes N^{e+o(1)} time and uses N^{h+o(1)} live space, even if all remaining local work is N^{11/10+o(1)}, the bound is
 t' <= max(11/10,e,3/5+g+t/2), s' <= max(1/2,h,s/2).
A verified source-only or P=NP-induced W generator must prove e<=11/10, h<=1/2, g=0 (or compensate by reducing call exponent), and all-input recursive closure. Sigma2=P provides some unknown e, not these inequalities. If W is materialized and has N^w bits, h>=w. If W is recomputed per query, its per-access cost contributes g and any repeated work to aggregate generation. Parent state, ancestor frames, serialization, and totalization are included in h/e. No source-independent recursive contractor may be assumed.

## TEST / HOSTILE CONTROL
For e in {1,2,3,5,10}, direct exponent arithmetic gives acquisition floor max(1.1,e), with e>1.1 failing. Literal hardwired N-bit storage vs sqrt(N) gives ratios 4,8,16,32 at N=16,64,256,1024. These are finite arithmetic checks, not a lower bound for arbitrary explicit-transition W.
Explicit transition f(v)=v+1 mod m fast-forwards to f^t(0)=t mod m, invalidating any oracle-to-circuit t-iteration transfer.

## STATUS
PROVED: finite-basis counting obstruction for arbitrary hardwired bit-selector functions, scoped disjunction, conditional resource accounting.
COMPUTATIONAL: finite exponent and storage arithmetic.
CONDITIONAL: a suitable compact W would help only with acquisition, oracle elimination, child construction, and recursion charged.
OPEN: uniform all-input arbitrary-decider ARC successor and P != NP.
RETIRED: oracle iteration lower bound as explicit-circuit lower bound; uncharged witness discovery; Williams time/space splice.
Next peer handoff: seek source-dependent compact W with x read-only and prove e<=1.1, h<=0.5, g=0 for both YES and NO without invoking an uncharged SAT oracle. Otherwise return focus to ARC all-input splitter.
