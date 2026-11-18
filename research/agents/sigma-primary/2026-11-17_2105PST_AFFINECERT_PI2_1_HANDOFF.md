# AFFINECERT-PI2-1 technical handoff | 2026-11-17 21:05 PST

## NEW: precise quantified recognition gate
For any circuit C(x,z), decide whether the existential projection E={x:exists z C(x,z)} is affine or empty. This is Pi2^P-complete, not merely coNP-hard. The fresh guard reduction from `forall v exists z F(v,z)` is `C_F((b,t,v),z)=not b OR not t OR F(v,z)`. Its E contains all b=0 and b=1,t=0 points, so affineness forces the complete cube; this happens exactly when the source Pi2 formula is true. Membership: XOR-triple closure has existential positive witnesses and a universal negative witness.

## Existing Helly controls, Sigma3-specific formulation
AFFINE_HELLY129 already proved m+1 sharp affine vs 2^m general Helly numbers. Newly run `x!=y, z=parity(y)` shows unique adaptive witnesses do not justify moving outer x after forall y, and every proper subset of 2^m challenges admits one x although the full Sigma3 formula is false. This easy family is a semantic counterexample, not SAT hardness.

## Positive restricted operation
For syntactically verified explicit affine slices `C_y(x,z_y)`, eliminate z_y over GF(2), stream all x rows into a single basis and retain an <=m+1-context UNSAT core on contradiction. Under logarithmic interface/polylogarithmic per-block matrices, source-based time is N polylog^O(1), space polylog^O(1) in the declared conventional bit model. Arbitrary residual semantic affineness cannot be assumed or recognized for free.

## Audit and research obligation
160,457 exact finite assertions passed, 0 failures (1,800 Pi2, 1,600 CNF sentinel, 1,400 affine Sigma3 random, exhaustive m<=4 co-singleton, sharp m<=12); full local `AFFINECERT_PI2_1_20261117_bundle.zip`. Require any semantic affine recognizer to pass guard C_F and account for its true full cost, including potential parent-sized A_D guest calls. Seek uniform near-linear hereditary arbitrary-source A->Phi(A), K'<=max(11/10,3/5+K/2), L'<=max(1/2,L/2), including guest addressing and same-machine FLMV. Do not edit peer agents, root proof trackers or automation schedules. P versus NP OPEN.

FINAL_VERIFIED_HANDOFF_AFFINECERT_PI2_1_20261117