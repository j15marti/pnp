# SIGMA REDTEAM16, 2026-10-17 15:40 UTC
STATUS: PROVED/EXACT restricted hashed witness game; COMPUTATIONAL 82,477 checks passed, zero failures; arbitrary Circuit-SAT resource contraction OPEN.

PROPOSE: test public random hashes against witnesses chosen after salt; add exhaustive QBF, non-affine circuits, equivalent circuit padding, and fully charged RAM/time-space accounting.

SEARCH: repository SIGMA3-COMMITHASH46, SIGMA3-HORIZON50, SKETCHBARRIER15, PADLIFT-STRATEGY7; Carter-Wegman 1979, Valiant-Vazirani 1986, FLMV 2005, Williams STOC 2024.

EXACT RESULT: The committed game choosing distinct a,b and one q with q=a and q=b is false. Replacing q by two challenge-dependent witnesses checked only through one shared public hash is true exactly when h(a)=h(b) for some a!=b. For an r-bit hash over w-bit states, r<w guarantees such a collision for every hash. Uniform random GF(2) linear hashes have collision probability 2^(-r) for a pair chosen BEFORE the hash, but adaptive witnesses chosen AFTER the hash collide with probability 1 when r<w. Gaussian elimination constructs the collision in polynomial time.

EXACT r=w=4 CONTROL: fixed-pair collision 1/16; post-hash adaptive collision 709/1024. All 74,668 enumerated binary matrices match GF(2) rank probabilities.

BUILD: Python standard library, fixed seed 20261033. 82,477 exact assertions, 900 Gaussian witnesses, 800 salt controls, 2,000 stacked-hash trials, 450 random gate circuits and 450 equivalent padded circuits; 130/130 UNSAT circuits were falsely accepted by the locally re-witnessed gate Sigma3 relaxation. 256 exhaustive three-quantifier Boolean relations checked independently.

RESOURCE: The proposed conditional envelope at lambda=1/2, beta=1/20, acquisition exponent 1.1 is max(1.1,0.55+K/2+delta) with guest-bit overhead delta. Parent-size guest calls, source decoding, strategy advice, recursive closure, memory-address convention and oracle simulations remain unproved. FLMV c=6/5 gives d=23/45; it does not certify a universal solver.

HANDOFF: require exact injectivity on reachable traces, charged emit_child and bit_child, and the same property on recursive descendants. Hash timing must be specified before applying collision error estimates. No proof of P!=NP is claimed.