% WORSTCASE REPORT::0001::2026-11-07
# WORSTCASE-0001: dichotomy for the bridge SAT in P => W_R(N) <= poly(N)

**P versus NP remains OPEN.** Nothing below proves a lower bound. No role, schedule or task changed.
Target: W_R(N) = max over UNSAT F, |F|<=N of min over refutations pi of F in R of cost_R(pi). Strategy discovery is free.

## Corpus reviewed (bounded survey)
Repo tree, AGENTS.md, LSPV-1/376 (Haken anchor for Res, Cook/Buss poly Extension/Frege PHP proofs defeat transfer),
LSPV-1/474 handoff (quadratic-span floor; B1/B2/B3 open; "SAT in P does not supply a same-calculus R_mix341 refutation"),
world-ledger pointer (equivalent-to-P=NP statements are reformulations). No prior file states the dichotomy below
in this form (grep for W_R(N) finds only LSPV-1 reports).

## Result 1 (KNOWN, Cook-Reckhow 1979): free strategy search is already built into W_R
For any R with poly-time checkable derivations and cost_R <= poly(|pi|), W_R is the nondeterministic minimum proof size.
Charging nothing for search is therefore not a relaxation; it is the standard definition. Consequence: W_R superpoly for ONE
fixed R shows only that R is not polynomially bounded. It does NOT give NP != coNP (that needs every proof system) and
does NOT give P != NP. So the bridge is genuinely necessary, and it is the only link from W_R to P vs NP.

## Result 2 (CANDIDATE, short proof): the bridge is a p-simulation statement
Assume P = NP. Then UNSAT is in P, and the system D(x,w)=x if x in UNSAT (decided by the poly-time algorithm) is p-optimal
with proofs of length |F|. Hence for fixed R:
  [SAT in P => W_R poly]  holds  iff  R is polynomially bounded in the world P = NP.
It is not implied by Cook-Reckhow (they give some poly-bounded system, not R). For R = Extended Frege the bridge follows
if a poly-time SAT algorithm with PV/S^1_2-provable correctness exists (Cook's PV<->EF correspondence; Krajicek-Pudlak)
-- cited from memory, exact form to be verified -- so the unconditional bridge for EF is open and is a proof-theoretic
statement, not a computational one. For Resolution, the bridge is FALSE-LOOKING in the P=NP world: Haken-type
exponential bounds are unconditional, so "SAT in P => W_Res poly" would force P != NP (contrapositive use is valid but
circular as a route: the bridge for Res is refuted by theorem, equivalent to P != NP being already known, so Res cannot be R).
(Statement: W_Res superpoly unconditionally, hence the bridge for Res holds only vacuously if P != NP.)

## Result 3 (CANDIDATE): dichotomy for choosing R
(a) Deterministic-step calculus (each inference is one forced machine step; optimal sequence = the single run):
    bridge is trivial, but W_R(N) = worst-case time of the best machine in the allowed family, so "W_R superpoly" is a
    restatement of P != NP (non-uniform flavour: min over sequences per formula = advice). Reformulation, not progress.
(b) Nondeterministic-choice calculus (Frege/EF/Res/PC/mixed): lower bounds are proof complexity; bridge becomes the
    p-simulation question of Result 2, which is open for Frege/EF and refuted-by-theorem for weak systems.
The project target "weakest sufficient bridge" is therefore: find R strong enough that [P=NP => R poly-bounded] is
PROVABLE, yet weak enough that W_R superpoly is not an unproved-equivalent of P != NP. Candidate window: R between EF
(bridge needs provable correctness) and systems with a built-in deterministic-run rule.

## Literature check (this run, web search; not verified against primaries)
- No 2026 superpolynomial Frege/EF lower bound found; best known unconditional is Omega(n^2) for Frege/EF (secondary source, low confidence).
- Alekseev, "A Lower Bound for Polynomial Calculus with Extension Rule", Theory of Computing 22 (2026): exponential bit-size
  for the binary value principle in an EF-simulating algebraic system -- relevant to the algebraic-reasoning survival test; transfer to EF itself NOT given.
- Filmus-Pitassi-Santhanam: a 2^{n^{omega(1/d)}} depth-d Frege lower bound would give a superpoly Frege lower bound (barrier-type reduction).
- A 2024 arXiv paper (2405.02232) links EF superpoly lower bounds to NP not in P/poly under provable-circuit-lower-bound hypotheses.
Status: ANALOGY/CANDIDATE; each needs a fixed-R transfer theorem before use.

## Assignments suggested to the five roles (additive)
1 Lower-Bound Lead: state a candidate R_* and prove/refute [P=NP => R_* poly-bounded] via an explicit simulation of a poly-time decider.
2 Reduction Builder: check whether R_mix341 p-simulates a deterministic-run (tableau) rule at poly cost; if yes it is case (a).
3 Hypergraph/Certificates: test Alekseev-style binary value principle on the signed-hypergraph families.
4 Resource Auditor: charge proof-encoding bits and peak memory for any simulation of Result 2.
5 Red Team: attack Result 2 (is D really p-optimal? is the quantifier on N vs |F| correct?) and the PV-provability citation.

**OPEN:** bridge for any fixed natural R; superpoly W_R for any R beyond Res/bounded-depth; P vs NP.
% END_OF_VERIFIED_REPORT::WORSTCASE::0001
