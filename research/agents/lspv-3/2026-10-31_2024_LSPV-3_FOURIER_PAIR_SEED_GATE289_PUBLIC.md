# LSPV-3 GATE289: Fourier-blind first-order policy and sharp pair-seeded SAT certificate

**31 October 2026, 20:24 PDT.** **PROVED/EXACT (restricted mathematics, independent external review pending); COMPUTATIONAL (finite controls); P versus NP OPEN.** The one universal adaptive parameterized residual-SAT/ARC-to-FLMV objective remains unchanged. This report treats only valid duplicate-free proper Monotone 3-SAT-(2,2) of Döcker; it does not substitute an all-positive easy subfamily for the NP-complete target.

## Exact obstruction and four falsifiers

The unresolved problem is a fully charged, source-authenticated, both-label-correct hereditary arbitrary-decider transformation `A -> Phi(A)`, including strategy discovery, rejected attempts, original-source and child-bit access, index tapes, output and peak retained workspace. A restricted SAT shortcut does not discharge that contract.

**F1, global first-order energy is a useful root variable selector: FALSIFIED.** For any valid formula define `V(x)` as the number of falsified original clauses and `z_i=(-1)^{x_i}`. Every degree-one Fourier coefficient of V vanishes since each original variable appears exactly twice with each sign.

**F2, a two-variable conditional-expectation certificate works on all smallest canonical sources: PROVED.** Every valid n=6 source has m=8 clauses. Choose a pair of distinct variables occurring together in any original clause, set them to opposite Boolean values, then greedily minimize conditional expected violated-clause count. This constructs a complete SAT witness.

**F3, the same fixed two-variable threshold certificate works on n>=9: FALSIFIED.** If `c_ij` is the unsigned number of original clauses containing variables i,j, then `c_ij<=4`. For all valid n>=9, m>=12 and every <=2-coordinate seed has `E[V|seed]>=(m-4)/8>=1`. No such seed ever triggers the strict `E<1` SAT certificate.

**F4, minimizing the pairwise quadratic approximation guarantees a witness or cheap computation: FALSIFIED.** The valid K33 nine-variable SAT control has 252 global quadratic minimizers, 234 nonsatisfying and 18 satisfying. On n=6, the certified policy used 240 counted literal positions per source versus mean 90.616 UP-first DPLL literal probes, before shared grammar checking.

## Restricted exact theorem

Let `c_ij` be the number of original clauses containing i and j, and `d_ijk` be the number of positive clauses on triple i,j,k minus the number of negative clauses on that triple. Exact source identity:

`8 V(x) = m + sum_(i<j) c_ij z_i z_j + sum_(i<j<k) d_ijk z_i z_j z_k.`

Proof: the falsification indicator of a positive triple is `(1+z_i)(1+z_j)(1+z_k)/8`, and that of a negative triple is `(1-z_i)(1-z_j)(1-z_k)/8`. For each variable the linear contributions cancel as 2 minus 2. Pair contributions are positive regardless of clause sign. Therefore `E[V]=m/8`, `E[V|x_i=0]=E[V|x_i=1]=m/8`, and fixing a pair in opposite spin states yields `E[V|pair]=(m-c_ij)/8`.

For a partial assignment p, compute `E[V|p]` exactly by summing `2^{-k}` over original clauses with no already true literal and k unfixed literals. If this expectation is <1, choose each remaining variable value that does not increase the conditional expectation. The final nonnegative integer number of violations is <1, so zero. The full original-source witness is checked independently. This is the standard method of conditional expectations, not a novel general SAT algorithm.

A general restricted **linear seed-acquisition boundary** follows: a seed of r assigned variables touches at most 4r original clauses. At least m-4r untouched clauses each contribute 1/8, so `E[V|p]>=(m-4r)/8`. For `E[V|p]<1` it is necessary that `r>(m-8)/4=n/3-2`. On any 198-variable target source this particular certificate needs at least **65 assigned variables** before possibly firing. This is **not** a universal solver-time lower bound, nor a bound on a different SAT certificate.

## Independently verified same-target controls

All 75 possible valid four-triple positive clause sets on six variables were enumerated, paired independently with all 75 possible negative sets, yielding **5,625 valid original formulas**. Independent exhaustive evaluation of **360,000 assignment-source pairs** found all formulas SAT, with 18 to 26 witnesses each and 119,250 aggregate witnesses. The independent verifier also reconstructed the conditional-expectation witness for every source.

UP-first DPLL used **22,420 nodes** and **509,716 literal probes** in total. The pair-seeded conditional-expectation policy used **1,350,000 conditional and final-witness literal positions** in total. The latter excludes grammar authentication, and the two counts are not native FLMV transitions.

Source controls: Y6 (SAT, n=6), H6 paired (SAT, n=6), K33 (SAT, n=9), CUBE12 (SAT, n=12), **U198 (UNSAT, n=198)**, **V198 (SAT, n=198)**. U198's original modular UNSAT certificate was independently replayed using **3,666 refutation nodes** plus all 64 boundary assignments. V198's complete witness was checked against 264 original clauses. The separate capped 1,200-node DPLL runs on both were reported UNRESOLVED, never mislabelled UNSAT.

All 69,674 original clause-pair SS/SU/US/UU compatibility rows, 1,716 occurrence S/U targets and their inversions, coherent all-zero/all-one statuses, intermediate flip trails, and independently calculated Walsh coefficients were checked. The independent verifier passed **4,736 exact Walsh coefficients** and **18 malformed target encoding controls**. Original signed occurrences are never treated as independent Boolean variables. The mixed same/opposite shared-variable obstruction cannot occur within a pair of monotone original clauses.

**Offline XOR adjunct:** on a complete monotone variable sweep, source-indexed logical XOR totals are `n+5m` in binary count coding and `n+4m` in Gray coding, giving 46/38 for Y6 and 1518/1254 for U198 and V198. A native physical FLMV writable/index tape `d_phys` was **not measured**, so these are not arbitrary-machine time lower bounds.

## Resource and model firewall

Source-grammar verification, duplicate checking, first-clause pair acquisition, nine conditional scans on the six-variable cases, witness checking, failed tests on larger sources, policy switching and complete fallback are charged. The matched source's SAT/UNSAT labels do not follow from degree-one coefficients, root expectations, or endpoint XOR. The n=6 certificate is a terminal easy subfamily, not a hereditary target-preserving power-short child on every valid input. Döcker's NP-completeness alone does not transfer the numerical FLMV forbidden region. No arbitrary-A -> Phi(A) compiler or first-bit efficient SAT-to-target FLMV transfer is proved.

## Search and duplication audit

Web/primary searches: `Döcker monotone 3-SAT-(2,2) NP complete`; `Fortnow Lipton van Melkebeek Viglas SAT time space`; `Fourier expansion CNF number of unsatisfied clauses`; `FourierSAT A Fourier Expansion-Based Algebraic Framework`; `method of conditional expectations SAT clauses`. Primary papers: [Döcker 2019](https://arxiv.org/abs/1912.08032), [FLMV 2005](https://doi.org/10.1145/1101821.1101822), [Kyrillidis et al. FourierSAT AAAI 2020](https://doi.org/10.1609/aaai.v34i02.5515).

Separate connected GitHub searches: `j15marti/pnp` for `first-order Fourier`, `balanced monotone Fourier`, `clause energy pair coupling`, and `ARC-LINEAR22-SATURATION1`; `openai/math` for `SAT solver` and `Fourier SAT`. Closely related prior project artifacts include GATE283 XOR order, GATE288 grammar scan, LSPV-4 TARGET-SHANNON-ROUNDING280, REDIRECT1, CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2, CONSTRUCTION-STRENGTHEN17 and ARC-LINEAR22-SATURATION1. The Fourier method is established, and a failed repository phrase search is not novelty evidence.

**Full reproducibility:** local complete archive `2026-10-31_2024_LSPV-3_FOURIER_PAIR_SEED_GATE289_COMPLETE.zip` (13 files, complete 5-page PDF/TeX, full experiment and independently implemented verifier, all fixtures, original U198 certificate dependency, V198 witness, full 5,625-source raw table and 69,674 pair records, manifest). SHA-256 `27f57f56a9a541567685a3e0d23fb3cf8182bea17023f77bc541c9e50027ae93`. The complete raw-data mirror to GitHub is pending if not separately committed; the verified conversation archive is the documented fallback.

**Next target:** test whether source-implicit higher-order conditional-expectation/backdoor certificates can be discovered without linear source-state storage or exponential seed search, while preserving both target labels and charging all failures. The universal ARC contraction and FLMV transfer remain OPEN; P versus NP remains OPEN.
