# SIGMA REDTEAM30: shared-cutset selector and unpadded-source firewall

**Timestamp:** 2026-11-18 14:00 UTC (06:00 PST).  
**STATUS:** PROVED/EXACT only for the restricted selector identity and source-geometry arithmetic; COMPUTATIONAL 334,683 primary and 174,330 independent assertions, zero failures. All-input hereditary Circuit-SAT contraction OPEN. P versus NP OPEN; external mathematical peer review pending.

## PROPOSE / SEARCH

Directly checked the primary project's [LOCALDUAL-SIGMA3-1 (04:55 PST)](https://github.com/j15marti/pnp/blob/main/research/agents/sigma-primary/2026-11-18_0455PST_LOCALDUAL_SIGMA3_1.md), [PATHCUT-1](https://github.com/j15marti/pnp/blob/main/research/agents/sigma-primary/2026-11-18_0303PST_SIGMA_PATHCUT_1.md), and [SIGMA29](https://github.com/j15marti/pnp/blob/main/research/agents/sigma-redteam/2026-11-18_1216Z_SIGMA29_STREAMING_SEPARATOR_FIREWALL.md). Proposed adversaries: add exactly ONE post-universal shared existential c to the private-witness LOCALDUAL compiler; compare (a) global SAT guest, (b) exact q² local selector guests; charge original source bytes, q-entry offsets, physical materialization, every negative SAT reply, delayed solver work; test whether small q is compatible with an unpadded source.

Primary literature: Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, https://doi.org/10.1145/1101821.1101822 ; Bubeck and Kleine Büning, *Bounded Universal Expansion for Preprocessing QBF*, SAT 2007, https://doi.org/10.1007/978-3-540-72788-0_24 ; Kattermann, Hofstadler, Seidl, *Definition-Based Dependency Schemes*, SAT 2026 (published 2026-07-16), https://doi.org/10.4230/LIPIcs.SAT.2026.22 .

## A. Exact shared-c negative challenge (restricted QBF identity)

Phi := EXISTS x FORALL y EXISTS c,z_1,...,z_q AND_i C_i(x,y,c,z_i), where z_i are strictly private but c is shared. For fixed x and c let D_i[x,c](y) := AND_{a in {0,1}^{|z_i|}} NOT C_i(x,y,c,a). Each D_i is an ordinary Circuit-SAT guest over the original globally named universal y pins.

For one-bit c, fixed x fails iff EXISTS y [(OR_i D_i[x,0](y)) AND (OR_j D_j[x,1](y))]. By finite distributivity this is OR_{i,j} SAT_y(D_i[x,0] AND D_j[x,1]). Thus Phi is true iff some fixed x makes ALL q² physical pair SAT guests UNSAT. All source identifiers for universal variables shared across the two factors must refer to the SAME guest pins. Incorrectly allowing separate y_i can change UNSAT to SAT.

For b shared bits the literal disjunction of selectors requires q^(2^b) guest combinations. This is exact algebra, not a complexity lower bound.

Explicit non-affine false positive against illicit private c: C_1=(c OR y) AND (z_1 OR NOT z_1); C_2=((NOT c) OR y) AND (z_2 OR NOT z_2). Each factor individually has responses for every y, but at y=0 the required shared c is contradictory. Adaptive c positive: C_i=(c=y) AND (z_i OR y), where true FORALL y EXISTS c,z_i but false EXISTS c FORALL y EXISTS z_i. Universal reindexing adversary: C_1=c OR NOT y, C_2=NOT c OR y; a pair negative guest has D_1[y,c=0]=y and D_2[y,c=1]=NOT y; sharing y makes it UNSAT whereas independently renamed y_1,y_2 would make it SAT.

## B. Exact literal-method density/budget mismatch

Use the LOCALDUAL sufficient caps: N actual source bits, q<=N^theta, each factor ell_i<=N^(lambda-delta+o(1)), |z_i|<=delta log N, physical expanded child |D_i|<=N^(lambda+o(1)), |x|<=beta log N. For a FACTOR-ONLY UNPADDED encoding with O(q polylog N) tags and no external filler, source bits must satisfy

N <= O(q N^(lambda-delta) polylog N) <= N^(theta+lambda-delta+o(1)),

hence **theta>=1-lambda+delta** is necessary.

The literal q² pair evaluator with a materialized q-entry source-offset table has charged upper bounds

K_pair <= max(1+beta, beta+2theta+lambda, beta+2theta+lambda*K);
L_pair <= max(theta,lambda,lambda*L).

At beta=1/50, lambda=1/2, delta=1/20, the factor-only source demands theta>=11/20=.55. Saturated literal pairs yield guest exponent **1.12+K/2**, compared with the primary comparison target **.60+K/2**: a .52 exponent gap. At K=3 this is 2.62 versus 2.10. q offsets alone cost space N^.55, outside the nominal .50 workspace target for small L. The literal pair transformation has self-contraction threshold K>2.24, though it can contract for sufficiently large K; it does NOT establish the desired uniform bound.

Attempting to cap guest-count cost at beta+2theta<=.60 would demand theta<=.29, incompatible with dense theta>=.55. At theta=.28, ell_i<=N^.45, total authentic factor bits <=N^.73+o(1): the missing N^.27 exponent necessarily reflects padded or uncharged source information in the factor-only model. Even delta=0 leaves density theta>=.50 and pair threshold theta<=.29 incompatible.

This **does not rule out** a compressed global guest, cross-factor gate sharing with fully charged physical encoding, source-dependent simplification, a different target bound, or arbitrary SAT algorithms. It only invalidates an unwarranted extrapolation of LOCALDUAL's exponent to a literal all-pairs extension for unpadded dense input.

For balanced all-tautological, output-connected factors, every pair SAT guest is UNSAT, so a literal evaluator that runs through all pairs invokes every guest. Taking a correct hypothetical P=NP polynomial SAT solver A and adding unconditional m^D delay (D at least A's base exponent) yields reached cost Omega(N^(beta+2theta+lambda D)) with full-size physical guests. The local harness explicitly generated q² negative guests for q=2,3,5,8 and billed each by its serialized byte length. With source blowup N=n^alpha, multiply the N exponents by alpha when comparing original-input runtimes.

## C. Positively certified exception

If a separately verified **total and unique** definition enforces shared c=f(x,y), e.g. the syntactic equality c=y, direct substitution reduces to the truly private-witness LOCALDUAL case with no q² selector expansion, provided building f in each factor is physically small and charged. Source-certified explicit definitions are not an algorithm for semantically discovering all such definitions in arbitrary succinct circuits.

## BUILD: actually executed independent checks

Primary audit: **334,683 assertions, zero failures**, seed 202611181350. Exhausted 65,536 ordered pairs of Boolean (y,c,z_i) factor relations. Fixed Σ1 true: 22,687; c fixed before y Σ2 true: 34,911; adaptive shared-c Σ3 true: 42,849; illegally factor-split c true: 50,625. Thus 12,224 Σ2-over-Σ1 cases; 7,938 Σ3-over-Σ2 cases; **7,776 local-c false positives**. Both relations non-affine in 41,616 pairs. Every true source had a checked Skolem response, every false source a checked selector counterchallenge.

Also tested 360 randomized physical AND/OR/NOT circuit pairs, actually serialized pinned/expanded pair guests and finite SAT evaluated their outputs, then checked equivalent double-NOT circuits, with 5 erroneous local-c positives; 1,600 two-bit-c controls; 1,000 definitional c=y repairs; structured non-affine, gate-trace, shared-universal-pin, finite oracle-profile, RAM-address and all-negative reached-call controls.

Independent checker, with different projected-bitset/strategy implementation: **174,330 assertions, zero failures**; independently reproduced all 42,849 correct Σ3 positives and 7,776 local-c false positives across the same 65,536 pairs. These two test populations overlap; counts are not disjoint.

Reproducible local package: SIGMA_REDTEAM30_PACKAGE.zip, with full mathematical report, audit.py, independent.py, results.json, independent_results.json, HANDOFF.md, README.md, SHA256SUMS.txt. ZIP SHA256 **f5e846746e6527fae2fd05d78ab00fa1a9c33260af1c1fa0e5e2e696317b4e4f**. Exact finite reruns passed; no native FLMV-machine resource measurements are claimed.

## T/S/R and hereditary audit

R<=T for unit-cost distinct-access counting does NOT bound largest addressed work-tape position (six touches can reach index 2^40). Work space and input random-access indexing must be counted in the exact lower-bound machine model, not presumed from sparse RAM address counts. Offset table, acquisition, parsing, globally identical y wire pins, output serialization, all guest copies, quantifier-strategy commitment, negative solver answers, hypothetical full-parent calls, and recursive use of transformed children must be fully charged. The pair SAT guests are not guaranteed to belong to the same source class; unrestricted all-input hereditary closure is MISSING. Oracle-defined gate semantics are not interchangeable across oracle worlds.

**HANDOFF:** Try an explicitly certified functional shared cutset c=f(x,y) retaining half-size guests. Alternatively, invent a source-indexed shared-y negative SAT guest avoiding both q² reached calls and parent-sized materialization while keeping source unpadded. Red-team every attempt with two-bit shared c, non-affine contradiction, global-y aliasing, late gate traces, paired SAT/UNSAT sources, indexed RAM vs FLMV work address, padding, synthetic delayed solvers and recursive closure. No claim P!=NP.

VERIFICATION_SENTINEL_SIGMA30_SHARED_C_DENSITY_20261118_1400Z
