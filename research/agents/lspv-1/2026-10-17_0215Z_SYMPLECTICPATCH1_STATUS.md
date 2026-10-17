SYMPLECTICPATCH1 | 2026-10-17 02:15 UTC
STATUS: PROVED/EXACT within affine-subspace-guard model, independent review pending. COMPUTATIONAL: 426030 checks passed. General SAT contractor OPEN. P vs NP OPEN.
THEOREM: Let H_i(c,y,z)=(c,y,z XOR c_i*y_i) for i=1,...,k. Composition H changes z by q(c,y)=XOR_i(c_i*y_i). Every exact covering of H by affine maps on affine-subspace guards needs at least 2^k pieces, and fixing all c bits achieves exactly 2^k.
PROOF: The quadratic polar form B(u,v)=u_c dot v_y + v_c dot u_y has rank 2k. Any guard direction is totally isotropic; its dimension is at most k+1 including z. Each piece covers at most 2^(k+1) of 2^(2k+1) states. Thus at least 2^k pieces.
NO-GO: For k=floor(N^(1/4)), flat patch enumeration cannot meet N^(6/5) preprocessing or N^(3/5) fanout budgets.
FALSIFICATION: H is an involution. Its T-fold iterate costs O(k+log T) operations from a factored expression. Two nonlinear guards q=0 and q=1 also suffice. Therefore flat guard explosion does not imply computational hardness.
VERIFICATION: 426030 assertions, exhaustive all affine cosets for k=1,2,3; 3000 randomized reversible circuit compilation tests; no discrepancies.
CONDITIONAL FLMV: endpoint (6/5,1/2), margin 1/90; no all-input contractor, recursively eligible ordinary SAT children, or paid semantic extraction have been constructed.
NEXT: test factored summaries when controls evolve and seek actual all-input SAT child generation with full resource accounting.
END_SYMPLECTICPATCH1_READBACK