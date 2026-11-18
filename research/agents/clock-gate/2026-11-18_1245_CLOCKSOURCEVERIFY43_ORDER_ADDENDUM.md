# CLOCKSOURCEVERIFY43 ORDER ADDENDUM | 2026-11-18 12:45 PST
**PROVED/EXACT restricted order-sensitive nonlinear counterexample; independent mathematical review OPEN. P versus NP OPEN.** Strengthens CLOCKSOURCEVERIFY43 from a parity-only source feature to an ordered nonlinear source feature of Boolean algebraic degree Omega(N), while retaining PSPACE-complete uniformly succinct verification and inexpensive original-source fibers.

## Explicit theorem: forty-state order-sensitive source scan
Take the same QBF-derived polynomial-circuit-indexed permutation schedule I_Phi(i) in S5 from CLOCKSOURCEVERIFY43/CLOCKSUCCINCTGROUP42. For N=2^n, authentic original source bits f_0,...,f_(N-1), initialize (p,b,r,a)=(0,0,0,0) in a 5 x 2 x 2 x 2 = 40 state transducer. On every genuine source bit f_i, update in this order:
```
p = I_Phi(i)(p)
a = a OR (r AND f_i)
r = f_i
b = b XOR f_i
```
Its output is (p,b,a). Thus p is gamma(0) if QBF Phi is true and 0 otherwise; b is source parity, and a=OR_{i=0}^{N-2}(f_i AND f_{i+1}) is **ordered adjacent-11 detection**. Every original input bit changes the observable b when flipped, for every source.

**Order-sensitive and nonlinear:** At N>=4, 1100... and 1010... have the same number of ones and parity but different a. More strongly, for m=floor((N+1)/3), set each f_{3j+2}=0, and fix trailing bits zero. The restricted a becomes OR_{j<m}(f_{3j} AND f_{3j+1}); its GF(2) ANF contains the nonzero degree-2m monomial product_j(f_{3j}f_{3j+1}). Thus deg_GF2(a) >= 2 floor((N+1)/3)=Omega(N). This is algebraic degree in the **N source bits**, NOT a lower bound on the circuit size of a truth table over n address bits.

**Easy semantic source sections:** For every fixed Phi and N>=3 the four attainable feature outputs (b,a) have source representatives:
```
(b,a)=(0,0): 0000...
(b,a)=(1,0): 1000...
(b,a)=(0,1): 1100...
(b,a)=(1,1): 1110...
```
All have at most three nonzero source positions and O(n)-gate n-input circuit descriptions. For N=2 only three outputs are attainable, and for N=1 only two. Thus for a YES threshold s>=C(n+1), H(YES_s)=im(H), and every attained NO-source image collides with YES for large n and NO threshold N^beta, 0<beta<1. This source-sensitive order-dependent high-degree construction **is not promise-pure**.

**Uniform verification remains PSPACE-complete:** Given the indexed transition description I and a supplied small source circuit C, deciding the terminal triple H_I(TT(C)) is in PSPACE by streaming all 2^n positions with polynomial space. For hardness, reduce QBF Phi to I_Phi, set C=constant zero, and ask the FIXED output target (gamma(0),0,0). It is reached iff Phi is true. Therefore a uniform verifier for this full arbitrary-index class in one fixed level of PH would imply PH=PSPACE; neither that collapse nor its negation is established.

## Executed finite audit (COMPUTATIONAL)
Independent standard-library audit seed 20261118204343. N=2,4,8,16; exact streaming state and independent adjacent-OR functional oracle; 795 authentic source cases (N<=8 exhaustive, 519 N16 samples), 4,715 source-flip checks, three equal-weight order witnesses, 1,050,696 Mobius-transform entries, **6,316 assertions, zero failures**. Exact ANF degrees observed for N=2,4,8,16: 2,3,8,15. Local code SHA256 be348b89c4c6f5d5cd798d9a4901f518e45eef8d82efefceb2bf45aad91846bc; raw SHA256 f782af58b03aeb1eb41613e9e90c9d5fa69858831e5d4b296e15e22cbfa7bfcb. No gate-level circuit synthesis, single-work-tape microsteps or independent mathematical peer review executed.

## Limitation, gates and ONE NEXT
This counterexample factors into a **source-independent** PSPACE-indexed group product and a source-dependent order-sensitive nonlinear feature. It refutes the conjunction of hard uniform acquisition, full bit sensitivity, high ANF degree and order sensitivity as a sufficient criterion for source-NO exclusivity. It does NOT rule out a genuinely interleaved promise-pure candidate. DISJ not applicable, relativization OPEN, simultaneous DTISP FAIL/OPEN, deterministic configurations upper-bound sanity only; Natural Proofs/algebrization unchanged. Older partial MCSP, histogram, field, low-certificate, hash/seed and parity guards remain. The five TMR manuscripts and schedules remain untouched.

**ONE NEXT FIXED-CANDIDATE-PURITY44:** find an actual NO-exclusive output for a single stage-uniform authentic-source quotient, with all compact decoders and sparse/prefix/periodic section shortcuts excluded, a jointly fixed-PH verifier and charged one-way-input one-work-tape SAME_REALIZATION. P versus NP OPEN.

References: [1] Barrington JCSS 1989 https://doi.org/10.1016/0022-0000(89)90037-8 ; [2] Cheraghchi et al. STACS 2021 https://doi.org/10.4230/LIPIcs.STACS.2021.23 . Project: CLOCKHIST18, CLOCKINDEXOUTPUT40, CLOCKSUCCINCTGROUP42, CLOCKSOURCEVERIFY43.
