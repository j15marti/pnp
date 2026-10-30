# SU05/Hadamard three-shift rank certificate (30 October 2026)

**Status:** exact finite algebraic statement; computational exhaustive certificate, independent proof-assistant review not performed. **Not** the complete SU09/vMS instance. P versus NP OPEN.

## Reviewed
Reconciled ORBITSLICE1, SYNCWEDGE1, WINDOWREC1, `experiments/product_span/vms_lde_hadamard_leaf.py`, source vMS Lemma 4.2 and RMV Definition 4.3, SU05 Hadamard conversion, later REACQ1, boundary-DAG accounting, and the ARC/FLMV proof tracks. The current root main promotes ARC/FLMV as principal; this is a supporting falsification control, not a redirection of the agents.

## Model
Fix p=17, primitive gamma=3, h=m=4, k=5. For each 4-bit word w, interpolate the unique polynomial f_w of degree <=3 satisfying f_w(j)=w_j for j=0,1,2,3. Define g_i(s,u)=<bin_5(f_w(gamma^(s+i) mod p)),u> over GF(2), for i=0,..,3.

## Finite full-rank certificate
For the fixed three shifts **R={0,5,8}**, and all 32 Hadamard seeds u for each shift, the 96-by-11 matrix of features (1,g_i,g_ig_j) has rank **11/11 for each of the 14 nonconstant w**. The constant 0000 and 1111 words have feature ranks 1 and 2. Exhausting all 16 singleton and 120 pair subsets of shifts shows no common one- or two-shift subset succeeds for all 14 nonconstant words. An independent computation from legal synchronous wedge rows agrees.

For w=0001, f_w(X)=6X+8X^2+3X^3 (mod 17). Eleven independent (s,u) feature rows occur at (0,0),(0,1),(0,16),(0,17),(5,1),(5,2),(5,3),(5,4),(5,6),(5,16),(5,18). In hexadecimal these rows are 001,215,009,71d,005,003,027,10d,16f,011,093 (constant bit first).

Additional exact finite sweep of spike-message cases: p=257,h=16,m=32,k=9 reaches W-rank 32 and exterior rank 496/496 after 18 consecutive shifts. For m=64 it reaches W-rank 64 and exterior rank 2016/2016 after 72 shifts. These are not vMS-legal asymptotic parameters.

## Proved structural controls
**Long-period lemma:** Let 1<=deg(f)=d<p-1. If the multiplicative orbit f(gamma^t) has period ell dividing p-1, then ell >= (p-1)/d. The polynomial f(gamma^ell X)-f(X) has p-1 roots and degree <p-1, hence zero. A nonzero degree-j coefficient forces (gamma^ell)^j=1, so (p-1)/ell divides j<=d. Injective binary labels preserve the period.

**Cheap-coordinate lemma:** Given public polynomial coefficients, g_i(s,u) is computed using modular exponentiation and Horner evaluation with O(d+log(s+i+2)) operations on O(log p)-bit words plus a binary-label inner product. Full feature rank and long period therefore coexist with inexpensive random-access output evaluation. Neither property is a SAT time lower bound.

## Source limitations and next gate
vMS RMV states p>Delta^100 and m<=Delta^(1/100), and Lemma 4.2 gives an existential local extractor. The finite tests above do not meet those asymptotic parameters or transcribe the complete PCPP, Boolean projections and adaptive calls. No claim is made about the uniquely active bit-level SU09/vMS final range. To reopen structural contraction, first source-transcribe that actual realized object, then rerun the complete rank certificate. This work does not supply the all-input, recursively closed, fully charged ARC/FLMV contraction.

Sources: Shaltiel and Umans, JACM 52(2), 2005; van Melkebeek and Mocelin Sdroievski, Computational Complexity 34:15, 2025, DOI 10.1007/s00037-025-00279-2; project ORBITSLICE1, SYNCWEDGE1 and REACQ1.