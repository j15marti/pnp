# UNIVERSAL-SOURCE-REPLAY1 | 2026-10-20 14:12 KST
P versus NP OPEN. Two active routes only.

PROVED restricted replay lemma: To reconstruct every bit x_i of any N-bit once-read source without further source access, retained deterministic synopsis a(x) is injective and requires >=N bits worst case. Hutter 2002 Section 8 caches streamed input/output for replay. Thus his literal stream adaptation supplies no N^(.5)-space implementation on arbitrary N-bit sources.

COUNTEREXAMPLE: Reading x_i before creating ordinary one-variable SAT query (z) or (z)&(not z) yields length-O(1) queries. All source reads must be charged; not every query includes N bits. PARITY(x) still needs N deterministic bit reads before its SAT answer can be emitted.

COUNTEREXAMPLE: Two certified constant-zero deciders, A runs n steps with O(log n) space, B writes a new tape cell each step and returns correct zero only after n^2 steps. Naive persistent-state 1:1 race returns in 2n-1 steps but B retains n-1 cells. Time-competitive race is not necessarily low-space. No claim against selective Hutter scheduler.

TESTS: 65536 N=3,b=2 synopsis maps (all collide), 3584 ordinary query tests, 1024 parity adversaries, 8 race sizes, zero failures. Full executable and raw in conversation bundle, NOT uploaded here.

Original primary Hutter https://arxiv.org/abs/cs/0206022. MMW https://dspace.mit.edu/entities/publication/d47cf035-39ca-4210-91e8-e5e3051d5deb. Unknown SAT/PH polynomial exponent C is not forced to be small by certified fastest selection. Original total SAT-to-MKTP target R_k and iterative same-run ARC contractor OPEN. P versus NP OPEN.
