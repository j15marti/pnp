# CLAUDE IPS-AGGREGATION-0001 | 2026-11-19 | Falsifier for the "CNF -> single axiom -> 1/f" arrow

**Role and ownership.** Hourly Claude routine; NOT one of the five TMR identities. No TMR manuscript
(main1..main5), historical root file, retired tracker (proof*.txt), handoff, schedule or issue was
edited. This is an additive role-neutral report with code and raw data kept separate. P versus NP
remains OPEN. Independent review: OPEN.

## Source reviewed

Google Doc "P vs. NP Proof Attempts" (id 1b2SYjJJJVjMwap-5wURTFbUMn212lwFnYhq2k5Sqdds), read in
full (about 58k characters after stripping span markers) on 2026-11-19. It surveys six attempts:
IA holographic/matchgates, IB tensor-network SVD, IC IPS synthesis, IIA GCT occurrence obstructions,
IIB IPS functional lower bounds / non-commutative IPS, IIC hardness magnification / locality.
Attempts IA, IIA, IIC restate known barriers (Cai-Lu-Xia; Buergisser-Ikenmeyer-Panova;
Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam locality) and are not re-audited here.

## Selected end-to-end arrow (from the doc's IC/IIB pipeline)

    encoded UNSAT 3-CNF phi -> aggregate f_w = sum_j w_j f_j (w_j > 0, nonvanishing on cube)
      -> any IPS_LIN' refutation of {f_w = 0, x^2 - x = 0} yields g = 1/f_w on {0,1}^n
      -> roABP / evaluation-dimension lower bound on g -> "hardness of refuting phi".

The last arrow is load-bearing for using functional lower bounds (FSTW 2021) on CNFs.

**Candidate.** Evaluation-rank of 1/f_w tracks refutation hardness of phi.
**Falsifiers stated before computing.** (F1) a trivially refutable phi with exponential rank of
1/f_w; (F2) rank depends on weights (doc asserts exponential weights are needed); (F3) rank produced
entirely by a Horn/2-SAT satisfiable component; (F4) order dependence of the width.

## Results

**Lemma 1 (PROVED/EXACT, char 0; self-proved, review OPEN).** For k >= 1, c > 0 and any positive
reals w_1..w_k, the 2^k x 2^k matrix M[y,z] = 1/(c + sum_i w_i y_i z_i), y,z in {0,1}^k, has rank
2^k over Q/R.

*Proof.* M[y,z] = G(y AND z) with G(t) = h(sum_{i in t} w_i), h(s) = 1/(c+s). Moebius inversion on
the subset lattice gives G(y AND z) = sum_{u subset y AND z} G^(u), so M = Z D Z^T with Z[y,u] =
[u subset y] unitriangular and D = diag(G^(u)). Here G^(u) is the iterated forward difference
Delta_{w_{i1}}...Delta_{w_{ij}} h(0) = integral over prod [0,w_i] of h^(j)(t_1+...+t_j), and
h^(j)(s) = (-1)^j j!/(c+s)^{j+1} has strict sign for s >= 0. Hence every G^(u) != 0 and D is
invertible. QED. (Uses complete monotonicity of 1/(c+s); in characteristic p the entries may
vanish, so no positive-characteristic claim.)

**Theorem 2 (PROVED/EXACT restricted).** Let phi_G = (x0) AND (NOT x0) AND
AND_{ab in E(G)} (NOT x_a OR NOT x_b), a <=2-CNF on n+1 variables. Then:
(a) phi_G has the degree-1 linear Nullstellensatz certificate 1*(1-x0) + 1*x0 = 1 (O(1) size,
    width 1 in every order); resolution refutes it in one step.
(b) For every positive weight vector w and every variable order pi, every roABP (in order pi) that
    agrees with 1/f_w on {0,1}^{n+1} has width >= 2^{nu_pi(G)}, where nu_pi(G) is the largest
    induced matching of G crossing some prefix cut of pi. So every roABP-IPS_LIN' refutation of the
    single aggregated axiom f_w = 0 has that width.
(c) If G is the perfect matching {(i, k+i)} and pi lists x_1..x_k before x_{k+1}..x_{2k}, the width
    is >= 2^{n/2}. If G is a d-regular edge-expander with expansion h (explicit families exist, e.g.
    Margulis/Gabber-Galil, LPS), then for EVERY order nu_pi >= h floor(n/2)/(2 d^2), giving
    2^{Omega(n)} in every order.

*Proof of (b).* Width-r roABP evaluations across a prefix cut factor through dimension r, so r >=
rank of the Boolean evaluation submatrix. Restrict x0 = 0 (clause (x0) falsified, contributes c =
w_(x0) > 0; clause (NOT x0) satisfied) and set every R-variable outside a crossing induced matching
to 0, which satisfies all clauses touching them. Inducedness leaves exactly the matching clauses,
each falsified iff y_i = z_i = 1, so the submatrix is Lemma 1's matrix with k = nu. (c): a prefix with
floor(n/2) R-variables has >= h floor(n/2) crossing edges; greedy selection removes <= 2d^2 edges
per chosen edge. QED.

**Consequences.** F1, F2, F3 CONFIRMED: aggregation makes a one-step-refutable CNF exponentially hard
for the single-axiom functional method, for unit, power-of-two and arbitrary positive weights (the
doc's "exponential weights are required" claim is wrong about where rank comes from), and the rank is
generated entirely by an anti-monotone 2-CNF that is simultaneously Horn, 2-SAT and satisfiable.
F4 CONFIRMED for the matching graph: in the interleaved order with unit weights the measured width is
about k/2+1, so order-robust claims need the expander version (c). The arrow
"rank(1/f_w) -> refutation hardness of phi" is **FALSIFIED/RETIRED** as a general transfer. Functional
lower bounds remain valid for the aggregated single axiom only; CNF hardness needs multi-axiom
methods that handle non-unique multipliers (the doc's own "pole cancellation" remark, now sharpened:
the failure occurs even with no cancellation needed, because the cheap certificate ignores R).

## Computational evidence (COMPUTATIONAL; finite tests, not asymptotic proofs)

Script `experiments/claude_ips_aggregation/verify_aggregation_rank.py`, SHA-256
107cc6e70467c67f7663100b16341d1148a4c430361e7a58397c62c603da7e2a, Python 3.11.18, seed 20261119,
exact rank over GF(2^61-1) (a lower bound on Q-rank). Raw output
`results/raw/claude_ips_aggregation/2026-11-19_aggregation_rank.json`, 11.0 s.
T1 matching cut, k = 1..6, unit/powers-of-two/random weights: rank = 2^k in all 18 cases, before and
after the x0 restriction. T1b interleaved order max prefix rank (unit; powers2): k=2: 2;4, k=3: 4;4,
k=4: 4;8, k=5: 6;8, k=6: 6;16. T2 random 3-regular G, n = 8/10/12, min over 4 random orders of the
maximum prefix rank: 14/22/60. NOT executed: exhaustive minimum over all orders, Q-rank by exact
rationals, the repository preflight.

## Gates

DISJ: PASS as a control. The obstruction is a disjointness/intersection-pattern matrix, which shows the
measure registers DISJ structure, not SAT hardness. Relativization, simultaneous DTISP,
deterministic-configuration counting: NOT APPLICABLE (algebraic proof-system statement, no machine,
oracle or time-space claim). Algebrization/Natural Proofs: NOT APPLICABLE (restricted roABP model with
known lower bounds). No runtime claim is made from rank.

## GitHub survey (OpenAI / Google orgs)

Repository search (default branches): `google-deepmind/formal-conjectures` has Lean statements
`FormalConjectures/Millennium/PvsNP.lean`, `Paper/DisjointNPPairs.lean`,
`Paper/PudlakFiniteDomainConjectures.lean`. Pudlak's finite-domain/DisjNP conjectures connect to the
Cook-program side of IC/IIB and are a possible target for TMR-1 source verification. Bodies were not
read beyond search fragments because of the session's repository scope. Also present:
`google-deepmind/alphaevolve_repository_of_problems` (no complexity-lower-bound problem found), and
`openai/math` and `prm800k` (not relevant). Searches of `google-research` and `openai` for SAT, proof
complexity and circuit lower bounds returned nothing.

## Suggested integration (for owners via issue #3; not applied)

TMR-2 and TMR-5: add phi_G as a standard "trivial-UNSAT plus Horn/2-SAT padding" control for any
invariant computed after weighted aggregation of clauses. Next lemma: decide whether a multi-axiom
roABP-IPS_LIN' width lower bound for some explicit CNF follows from a min-rank over the affine space of
valid multiplier tuples (g_1..g_m), which is the correct object once aggregation is removed.
