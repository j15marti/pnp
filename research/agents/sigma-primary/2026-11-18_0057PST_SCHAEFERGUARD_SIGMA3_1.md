# SCHAEFERGUARD-SIGMA3-1 | 2026-11-18 00:57 PST

**Status:** PROVED/EXACT scoped complexity classifications (independent peer review pending); COMPUTATIONAL: 26,683 CPython checks, zero failures; unrestricted A→Phi(A) OPEN; P versus NP OPEN.

## PROPOSE four mechanisms, then SEARCH
1. Try semantic recognition of any of Horn, dual-Horn, bijunctive, affine instead of just affine.
2. Select an existentially committed representation globally, not adaptively after each universal challenge.
3. Add uniquely forced post-challenge Tseitin traces and check whether classification becomes easier.
4. Audit semantic-recognition cost, source parsing, encoding, replay, parent-sized guest calls, same-machine workspace and hereditary closure.

**SEARCH:** Read project AFFINECERT_PI2_1, TRACEMOVE_SIGMA2_1, GRAPHPAIR_SHARE1, SIGMA24 wheel-frontier repair, and LSPV-4/397 guarded Horn-consequence results. The affine-only Π₂ theorem and classical Schaefer polymorphism facts were already known; this is a project-specific four-class and Σ₃ unification, not an external originality claim. Primary literature: Schaefer 1978, FLMV 2005, Williams 2024 and Hemaspaandra 2004.

## Theorem 1: Three-bit all-four-class semantic guard
For arbitrary Boolean circuit F(v,z), define MID(g) iff a three-bit guard g is not 000 or 111. Form the ordinary circuit C_F(g,v,z)=MID(g) OR F(v,z), adding O(1) gates. Define visible projected relation R_F={(g,v): exists z C_F(g,v,z)}. Then R_F is in **at least one** of the four classes defined respectively by closure under bitwise AND, bitwise OR, coordinatewise majority-of-three and triple XOR **iff** forall v exists z F(v,z).

Proof: When QBF true, R_F is the entire cube, closed under all four ops. If false, fix v0 such that no z satisfies F(v0,z); exactly six guards are feasible at v0. Closure counterexamples at the *same v0* are:
- AND(001,010)=000, forbidden.
- OR(110,101)=111, forbidden.
- MAJ(110,101,011)=111, forbidden.
- XOR(001,010,100)=111, forbidden.

Therefore recognizing membership of an arbitrary circuit's existential projection in the four-way union is **Π₂^P-complete**. Hardness is the constant-gate reduction from Π₂-complete forall v exists z F. Membership: nonclosure for each fixed op is Σ₂, witnessed by 2–3 visible feasible tuples and private witnesses followed by a universal absence-of-output-witness check; closure is Π₂. Finite union of Π₂ classes remains Π₂. The four classes are only the nontrivial operation-closure families; do not conflate them with 0-valid and 1-valid Schaefer cases. Syntactically promised source formulas are different from arbitrary semantic existential projections.

## Theorem 2: Global Σ₃ selection
For arbitrary C(x,g,v,z), ask whether one fixed x exists so R_{C_x} is in the four-way union. This problem is **Σ₃^P-complete**. Membership: existentially guess x, then run the Π₂ predicate. Hardness: take arbitrary exists x forall v exists z F(x,v,z) and build C= MID(g) OR F(x,v,z), applying theorem 1 pointwise for each fixed x.

**Hostile witness-order control:** For 2-bit x,v, F(x,v,z)=[x!=v] AND [z=parity(v)] has a unique z whenever a pair is feasible. Yet exists x forall v exists z F is false; forall v exists x,z F is true. Unique locally determined response is no certificate for global x. Adding deterministic private t forced to equal g0 XOR v0 leaves the projection exactly R_F, so unique Tseitin gate traces do not erase the Π₂/Σ₃ certification obligation.

## Executable audit, finished
Independent stdlib Python, seeded 202611180057, **26,683 assertions passed, 0 failures**. Exhaustively tested all 256 F truth tables with 2 universal v and 1 private z; 81 satisfy forall v exists z F, exactly those whose projected relation is all-four closed. 1,200 random Σ₃ truth tables with 2 global x, 2 universal v, 1 private z: 924 true; 257 false originals become true under the illegal x-after-v reorder. Tested 120 actual AND/OR/NOT gate DAGs over 7,680 complete assignments with reconvergence/fanout/dangling padding, 2,880 deterministic Tseitin trace projection checks, and symbolic padded-decider resource inequalities. Full local ZIP: SIGMA_SCHAEFERGUARD_20261118_0057PST_bundle.zip (REPORT.md, HANDOFF.md, audit.py, results.json and verified SHA256SUMS.txt). These are finite tests, not same-machine FLMV measurements.

## Resource ledger, limitations, handoff
Assume P=NP, fix arbitrary correct polynomial-time Circuit-SAT decider A with unknown K,L. Target remains K'<=max(11/10,3/5+K/2), L'<=max(1/2,L/2). Adding a guard only creates an O(N) source, NOT a small-child compiler. Π₂/Σ₃ completeness does not imply superpolynomial runtime under P=NP; polynomial-hierarchy collapse does not give the required exponents. Actually executing delayed A_D on Theta(N)-size input can cost Omega(N^D), above target for integer D>=2; a code-aware bypass remains possible.

Charge acquisition and verification of semantic projections; gate encoding and source-address access; guest input materialization/indexing; strategy construction; full parent calls; simultaneously retained memory; source replay; maximum addressed work-tape position; recursion and hereditary closure; native FLMV machine transfer. Do not assume a free universal splitter or promote a bounded interface to a general SAT lower bound.

**NEXT:** Use MID(g) OR F(v,z) as a unified four-clone sentinel. Retain fast **syntactic** Horn/dual-Horn/2-CNF/affine terminals, but charge **semantic** recognition. Test also GRAPHPAIR, odd-wheel low-width source repair, latent UNSAT, AFFINECERT and padded deciders. Seek an all-input, source-backed, truly hereditary, half-size ordinary-Circuit-SAT compiler with fully charged calls. Arbitrary A→Phi(A) OPEN; P versus NP OPEN.

References: [1] Schaefer STOC 1978 https://doi.org/10.1145/800133.804350 ; [2] Fortnow et al. JACM 2005 https://doi.org/10.1145/1101821.1101822 ; [3] Williams STOC 2024 https://doi.org/10.1145/3618260.3649723 ; [4] Hemaspaandra 2004 https://arxiv.org/abs/cs/0406006 .

VERIFICATION_SENTINEL_SCHAEFERGUARD_SIGMA3_1_20261118_0057PST_26683