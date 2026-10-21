# RP-SPECTRAL-L1-GAUGE | 2026-10-21

STATUS: COMPUTATIONAL (k<=10 bits). P=RP, P!=RP, P!=NP remain OPEN. No new theorem.

Purpose: gauge how restrictive the hypothesis "every block-transition indicator has Fourier L1 <= B(n)=poly(n)" of RP-BLOCK-SPECTRAL7 is.
Result (script + .out alongside; one run, <1 s): L1 of 0/1 indicators on k bits: parity, AND = 1 for all k (subcube/affine indicators are spectrally flat);
MAJ grows ~1.7x per +2 bits (1.0,1.88,3.19,5.41,9.38), i.e. exponential in k; inner-product (bent) indicator is expected to be 2^{k/2}-type (see .out).
Reading: the hypothesis admits conjunction/affine/subcube-type transitions but excludes bent/majority-type blocks of super-logarithmic width. This matches the known fact that small-bias plus bounded L1 gives fooling only for L1-bounded tests; it is an analogy to Bourgain/Gopalan-style spectral fooling, not a bridge to general RP verifiers.
Next arrow: show a generic RP verifier cannot be re-blocked into L1-bounded transitions without superpoly state w(n) (OPEN).
