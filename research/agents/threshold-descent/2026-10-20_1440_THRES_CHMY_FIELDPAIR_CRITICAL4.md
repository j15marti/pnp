# CHMY-FIELDPAIR-CRITICAL4: exact covariance, aliasing, and the unresolved additive critical window

Date: 2026-10-20 14:40 Asia/Seoul. Role: :00 MCSP one-tape threshold-descent specialist. **P versus NP OPEN.**

**Scientific status:** the finite-field pair/collision lemmas and the undersized-field false-NO reduction theorem below are **PROVED/EXACT** within their stated, modified public-seed input-insertion model, with independent review PENDING. Exhaustive finite checks are **COMPUTATIONAL**. No cofinal MCSP threshold descent, standard-model SAT-to-MKTP totalizer, or unrestricted complexity separation is established.

## 1. Current state and previous no-gos

Read the project-governed `2026-10-19_1518_PROOF_PORTFOLIO_REALLOCATION1.tex`, `2026-10-19_AGENT_CONTINUITY_GITHUB_FALLBACK1.md`, new `2026-10-20_TWO_SPINE_REASSESSMENT_AND_HOURLY_ASSIGNMENTS.md`, root `main.tex` status, AGENTS/CODEX/research skill, live shared Docs log, and peer reports `CHMY-FKBASEERASURE1`, `CHMY-LAST-ADDITIVE-YES-CARDINALITY1`, `CHMY-ADDITIVE-CRITICALWINDOW2`, `CHMY-MULTIPORT-MASK-FLOOR3`, `DETREE-POLYFIBER13`, `POLYFIBER10`, `SEEDPORTFOLIO22`, `MAIN_SOURCE_REFERENCE_FLOOR15`, and `MAIN_VIRTUAL_ORDINARY_INPUT16`.

The earlier single-slot analysis proves (under near-pairwise masks) that *late* insertion fails source-YES and *early* insertion erases some source-NO; the remaining window has length approximately `beta log2 N`. The multiport report already proves that fixed redundant additive ports do not gain a new exponent via cancellation. **Neither result supplies a two-promise-correct descent.** Current top-level priority is the independently specified total SAT-to-ordinary-MKTP next-block interface; the field-mask route remains a relevant falsification experiment, not a third proof program.

## 2. Four attacks fixed before fresh primary-source consultation

1. **Actual inner-product mask pair:** calculate two-coordinate probabilities from its finite-field definition rather than treating coordinates as independent.
2. **Critical-window exposure:** derive an exact second moment and evaluate whether detecting a sparse opposite-label perturbation is probable near `t = mu log2 N`; contrast union bounds with Paley-Zygmund.
3. **Field-period resonance:** use powers at positions congruent mod `2^h-1` to find a minimal source support on which all masks are identical. Determine when this can contain a genuine source MCSP-NO by circuit counting.
4. **Hostile controls:** reused masks across layers, source-dependent seeds, output-length changes and postprocessing; never promote a seed-coupling failure to an actual fast/slow-machine theorem.

## 3. Primary sources and model restrictions

- Cheraghchi, Hirahara, Myrisiotis and Yoshida, STACS 2021, DOI `10.4230/LIPIcs.STACS.2021.23`, Theorem 2 (conference) and ECCC TR20-103 rev.1. The randomized lower bound is in the one-way read-only-input plus one read/write work-tape model at a **large** MCSP threshold. Their full Forbes-Kelley style PRG uses an independently sampled private initial layer, additive terms and nearly independent masks. **Injecting an arbitrary MCSP input into an additive slot is a new attempted reduction, not the original CHMY PRG.**
- Oliveira, Pich and Santhanam, Theory of Computing 17(11) (2021), DOI `10.4086/toc.2021.v017a011`, assume a family of **nonuniform circuit** Gap-MCSP lower bounds for all sufficiently small beta, not the above one-tape lower bound.
- McKay, Murray and Williams, STOC 2019, DOI `10.1145/3313276.3316396`, use a distinct oracle-assisted one-pass search-MCSP/MKTP setting; no automatic transfer.

The following is for one **specified finite-field mask primitive** used in CHMY-related constructions. It is not the entire CHMY almost-k-wise mask distribution. Let `Q=2^h` and let `a,b` be independent uniform in `F_Q`. Fix any binary basis and define for positive integer `j`,

`T(j) = parity( repr(a^j) AND repr(b) )`.

The binary dot product is nondegenerate. Every layer draws a fresh independent pair `(a,b)`; coordinate outputs *within* a layer need not be independent.

## 4. Exact pair theorem (PROVED/EXACT in this model)

For distinct positive `j,k`, put `d=gcd(|j-k|,Q-1)`. Then

`p = P[T(j)=1] = (Q-1)/(2Q)`,

`r_jk = P[T(j)=T(k)=1] = (Q-1+d)/(4Q)`.

**Proof.** If `a=0`, both powers vanish. For each nonzero `a`, `a^j=a^k` iff `a^(j-k)=1`, which holds for precisely `d` elements of the cyclic multiplicative group of order `Q-1`; then the shared nonzero linear form is one with probability `1/2` over uniform `b`. For the remaining `Q-1-d` choices, `a^j,a^k` are distinct nonzero vectors over `F_2`, hence linearly independent and jointly one with probability `1/4`. Sum the cases and divide by `Q`. QED.

**Aliasing corollary.** For all `j,k>=1` congruent modulo `Q-1`, `T(j)=T(k)` for every seed, not only with high probability. For `S` contained in one such residue class, the product of `t` independently generated masks is constant across `S`, with survival probability exactly `p^t` for **all of S together**, regardless of its cardinality. Two `Q-1`-separated differing coordinates therefore have detection probability `p^t`, not the independent-coordinate heuristic `1-(1-p^t)^2`.

## 5. Exact critical-window second moment (PROVED/EXACT)

For nonempty set `S` of positive coordinates and `t>=1` independent field-mask layers define

`Z = sum_{j in S} product_{i=1}^t T_i(j)` and `k=|S|`, `lambda=k p^t`.

Then for every finite `Q,k,t`,

`E Z = k p^t = lambda`,

`E Z^2 = k p^t + 2 sum_{j<l in S} r_jl^t`.

Consequently

`lambda^2 / E Z^2 <= P[Z>0] <= min(1,lambda)`.

The lower inequality is Cauchy-Schwarz/second moment; the upper is union/Markov. This exact formula records within-layer field correlations rather than discarding them. It bounds the distinguishability obtainable from a **coupling comparison**, not the performance of an unrestricted MCSP decider. For a common public seed, outputs of the additive insertion map for inputs differing on `S` are equal exactly when `Z=0`.

If `max S < N`, `Q>N`, and `Q/(N t)->infinity`, then for all pairs `d<=N-1` and

`r_jl / p^2 = 1 + [Q(1+d)-1]/(Q-1)^2 <= 1 + O(N/Q)`.

Hence `E Z^2/lambda^2 <= 1/lambda + exp(O(tN/Q))`. In particular, if `lambda->infinity`, `P[Z>0]->1`. If `lambda` tends to a fixed positive constant and `Q/(Nt)->infinity`, then `P[Z>0]>=lambda/(1+lambda)-o(1)`. If `lambda->0`, the union bound gives `P[Z>0]->0` with no pairwise assumption.

This establishes an exact sensitivity crossover near `t = log_2 k` (with `p` replacing `1/2`), not a rescued MCSP reduction. In the previously unresolved window, the simple zero-vs-sparse-NO coupling ceases to provide small TV when `lambda` is large; that failure of one attack is not evidence of target-YES preservation or a good solver.

## 6. NEW undersized-field MCSP-NO obstruction (PROVED/EXACT, conditional on size)

Fix `0<mu<1`, `s=floor(N^mu)` and a complete fixed fan-in-two Boolean basis. The number of N-bit functions of circuit size `<=s` is at most `2^{C s log2(n+s+2)}` for an absolute constant C. Let field size `Q=2^h` and suppose the coordinate range `{1,...,N-1}` contains a residue class mod `Q-1` with `k > C s log2(n+s+2)` positions. Then there is a source function `f_NO` supported entirely on that residue class with `CC(f_NO)>s`; `f_YES=0` has `CC(f_YES)<=s`.

For the *modified* one-slot additive input-insertion map `Phi(f;z)=H(z) XOR (B(z) AND f)`, with `B` the product of `t>=2` independent field masks, one has

`Pr_z[Phi(f_NO;z)=Phi(f_YES;z)] = 1-p^t >= 3/4`.

**Proof.** There are `2^k` different functions supported on the residue class, more than the total circuit-description count, so some exceeds size `s`. Every coordinate of the residue class has the same mask bit in each layer; their full mask product vanishes with probability `1-p^t`. The additive base `H` cancels pointwise under a shared seed. Thus the total variation of `(z,Phi(f_NO;z))` versus `(z,Phi(f_YES;z))` is exactly `p^t<=1/4`. Any classifier with both errors `<=1/3` must have acceptance-gap `>=1/3`, impossible. QED.

For example, the cardinality condition eventually holds with any `Q <= N^{1-mu-epsilon}` for fixed `epsilon>0` and the source index range sufficient to host the residue class. **This is a necessary field-size caution for this particular proposed descent**, not an obstruction to CHMY's actual almost-k-wise PRG, which must be checked against its own chosen field parameters. It also does not cover source-dependent seeds or length-changing maps.

## 7. Bounded executable audit

Executable: `experiments/review/2026-10-20_CHMY_FIELD_CRITICALMOMENTS4_audit.py` (Python standard library). Deterministic; timestamp-seed metadata `202610201440`; *exhaustive* over every pair `(a,b)` for `h=3,4,5,6`, and over all independent layer seeds on the six listed finite supports. All finite-field multiplications, power lookups, inner products, pair formulas, second moments, collision histograms and hostile reused-mask controls are recomputed, not inserted from claimed prior data.

Raw JSON: `results/raw/separation/2026-10-20_CHMY_FIELD_CRITICALMOMENTS4.json`.

- 20 exact field-coordinate pair rows for Q in {8,16,32,64}.
- 6 exhaustive independent-layer survival experiments; independent seed sequences include 262,144 for Q=8,t=3 and 65,536 for Q=16,t=2.
- 2 correlated/reused-layer hostile controls.
- 1,810,112 recorded check operations; **zero failed assertions**.
- For Q=8, coordinates {1,8} and two layers, `P(Z>0)=49/256`, `P(Z=0)=207/256`; these two coordinates are exactly aliased. For Q=8 and S={1,2,3,4}, two layers, `P(Z>0)=941/2048`.

The small examples check probability identities; they do **not** instantiate full CHMY seed security or demonstrate an actual high-MCSP-complexity truth table with only 8 or 16 bits. The asymptotic NO construction instead uses circuit counting.

## 8. Uniformity, resource charge, and status

This is an *impossibility* for a stated attempted source-to-source map, not an algorithm or a valid lower-bound transfer. The unmodified CHMY PRG is untouched. If a target construction ever survives semantics, one must still count **at least N sequential source arrivals, N written output bits**, independent masks/additive/private-layer seeds, output-index generation, input/output bit traffic, source read/replay, one work-tape head movement, retained mask/seed state, amplification, verifier acquisition and decision uniformity. No independent work-tape runtime upper bound is claimed here. If the output were a different length N', those counts and exponent conversion must be redone, not hidden under a rescaled beta. The construction provides no `beta'<=lambda beta`, `g'>=rho g` with `rho>lambda`; P versus NP is OPEN.

### Explicit statuses

- **PROVED/EXACT (scoped; independent review pending):** finite-field pair formula, aliasing, moment relation, undersized-field opposite-promise collision theorem.
- **COMPUTATIONAL:** exhaustive finite mask audits; all assertion checks passed.
- **FALSIFIED/RETIRED:** assumption of coordinate independence inside a mask when `j-k` has large gcd with `Q-1`; proposed input injection using a field too small to avoid opposite-label periodic fibers.
- **OPEN:** actual-CHMY full-seed critical-window two-promise descent, original mask parameter instantiation, one-work-tape/PH-low model transfer, cofinal parameter slope, standard-model total SAT-to-MKTP generator, all-algorithm lower bound.

### Role handoff

- **:00** determine the actual CHMY indexed field/small-bias generator parameter ensuring distinct enough coordinates, then attack the `lambda=Theta(1)` critical window with signed public-seed TV and source YES preservation jointly. Alternative priority: construct a *total ordinary* MKTP target with source-local short-query generator and both labels, no N-bit source pointer.
- **:12** audit whether candidate next-block queries are genuinely ordinary short strings, not a pointer to the original SAT source; measure adaptive query access.
- **:24** any ARC child indexed-bit representation must charge parent reads, generator workspace, replay and all ancestor live states on the same random-access model.
- **:36** repeat field-pair test with actual CHMY mask source and test boundary j=0, reused masks, source-dependent seeding, periodic a powers; challenge the claimed circuit description counting constant.
- **:48** retain only field-primitive restricted theorem; do not promote generator or magnification. P versus NP OPEN.

Root `main.tex` is not edited because it has been repeatedly observed as truncated/ownership-marker deficient. New immutable report, code and raw files are intended for verified GitHub publication with shared Docs fallback if blocked.