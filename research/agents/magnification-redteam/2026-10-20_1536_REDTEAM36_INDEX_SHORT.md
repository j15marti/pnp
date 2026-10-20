# REDTEAM36 scoped INDEX/MKTP theorem (2026-10-20 15:36 KST)
P versus NP OPEN. Active routes: MCSP/MKTP and ARC/FLMV only.

For m data bits x and selector j arriving last, define U(l;a,b) as all four clauses (l OR ±a OR ±b). This proper-3CNF block is equivalent to literal l. The formula F(x,j) consists of U(v_i;a_i,b_i) for x_i=1 (U(not v_i) otherwise), followed by U(v_j;c,d). With 3m+2 variables, 4m+4 clauses and ordered binary encoding n=Theta(m log m), F(x,j) is satisfiable precisely when x_j=1. A deterministic one-pass SAT decider must retain m-O(1) memory bits, since all 2^m prefix strings require distinct joint states. Bounded-error public-coin randomization requires at least m(1-h2(error)) bits.

Conditional result: Suppose unbounded fixed k admit deterministic total ONE-WAY-SOURCE, in-order ordinary SAT-to-MKTP transducers R_k, of target length M=n^(a+o(1)) and threshold p=M^(1/k+o(1)), using n^(rho+o(1)) space for common rho<1, with exact opposite-label semantics. Under P=NP, MMW Theorem 4.2 gives a one-pass MKTP decider with short Sigma3 SAT queries. PH=P gives one fixed polynomial query solver of unknown exponent D. Stream R_k into it, counting all live state. Choose fixed k large enough that aD/k<1. The composed one-way SAT decider uses n^(max(rho,aD/k)+o(1))=o(n/log n) space, contradicting the INDEX family. Thus existence of such a cofinal transducer would imply P!=NP. NO SUCH R_k IS ESTABLISHED. This is a conditional result and classical INDEX-style lower bound, not a new unrestricted SAT lower bound.

The proof does not apply to random-access input for ARC/FLMV, nor to uncharged readable output buffers, hidden source advice, variable ordering, or external timer input. Compact shared W, two-promise CHMY transport, deterministic Ilango standardization and arbitrary-decider ARC remain OPEN.

Audit: 8194 proper-3CNF formula/index instances tested, 16388 SAT/proper assertions, 8188 prefix-distinguishability checks, 2880 large-time affine controls; no failures.
Sources: MMW STOC 2019 Theorem 4.2; Kremer-Nisan-Ron 1999; CHMY STACS 2021; FLMV JACM 2005.
Handoff :00 test real streaming R_k; :12 fixed unknown query exponent; :24 random-access model guard; :36 attacks on source advice, output channel; :48 preserve conditional status.
