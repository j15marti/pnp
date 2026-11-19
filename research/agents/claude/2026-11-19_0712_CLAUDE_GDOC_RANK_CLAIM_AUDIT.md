# Claude hourly routine: audit of the Google Doc "P vs. NP Proof Attempts" + OpenAI/Google repository survey

Run: 2026-11-19 07:12 UTC (scheduled routine; not one of the five TMR identities). Branch `ccr-8d8a5ce7-39wor1`, base `b124b964`.
No TMR manuscript was edited (ownership rule in AGENTS.md). Retired trackers proof*.txt were not read. P versus NP remains OPEN.

## 1. Source reviewed

Google Doc `1b2SYjJJJVjMwap-5wURTFbUMn212lwFnYhq2k5Sqdds`, title "P vs. NP Proof Attempts" (read in full, ~58 KB after stripping span markup).
Six trajectories: IA holographic/matchgates, IB tensor-network contraction with SVD truncation, IC IPS certificate synthesis,
IIA GCT occurrence/multiplicity obstructions, IIB IPS functional lower bounds / non-commutative IPS, IIC hardness magnification
and the locality barrier. Section 4 proposes a "Reciprocal Barrier Principle".

Status of the document's cited theorems: they are KNOWN THEOREMS from the literature it cites (Cai-Lu-Xia; Grochow-Pitassi;
Forbes-Shpilka-Tzameret-Wigderson; Bürgisser-Ikenmeyer-Panova; Dörfler-Ikenmeyer-Panova; Li-Tzameret-Wang; Chen-Jin-Williams;
Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam locality barrier). Not independently re-verified against primary PDFs this run.
The doc itself proves nothing new and claims no resolution.

## 2. Candidate and falsifiers

Candidate (from doc Sec. 2.2 and Sec. 4): "the evaluation matrix of an unsatisfiable or #P-hard constraint system across variable
bipartitions exhibits full rank 2^Omega(n)", i.e. cut rank of the solution/count tensor is a hardness witness for SAT.

Falsifiers stated before running:
F1 UNSAT or unique-SAT instances have cut rank 0 or 1 (repo control "unique-solution rank one").
F2 A polynomial-time family (2-SAT / affine) attains full cut rank 2^{n/2}.
F3 Full rank of the linear-IPS functional 1/f depends on aggregating all clauses into one axiom; per-clause multipliers can be much lower rank.

## 3. Executed evidence (COMPUTATIONAL, finite n = 16, balanced cut 8|8)

Code `experiments/claude/doc_rank_claim_audit.py`; raw `results/raw/2026-11-19_CLAUDE_DOC_RANK_AUDIT_raw.json`;
run `python3 -I experiments/claude/doc_rank_claim_audit.py <out>`, 1.9 s, Python 3.11.18, numpy 2.4.6. Seeds 0..11 (A), 1001 (B).
Ranks are exact over GF(2^31-1) (a lower bound on rank over Q; not asserted equal).

A. Random 3-CNF, n=16, m=68 (ratio 4.25): cut rank of the solution indicator is 0 for all 4 UNSAT seeds (3,6,9,11),
1 for unique/two-solution seeds, and at most 6 overall (seed 7: 35 solutions, rank 6).
B. Planted unique-solution 3-CNF: 1 solution, cut rank 1.
C. 2-SAT equality matching x_i <-> x_{i+8}: 256 solutions, cut rank 256 = maximum. Polynomial-time family.
D. UNSAT seed 3, linear-IPS functional g = 1/f on {0,1}^16: rank 256 (full) both for f = #falsified clauses and
for f = sum_j 2^{j-1}[C_j falsified] (mod P). Canonical multi-axiom certificate g_j = [C_j is the first falsified clause]
(sum_j g_j f_j = 1 on the cube): 53 nonzero multipliers, max per-multiplier cut rank 22, sum 400.

## 4. Conclusions with status

FALSIFIED (as a general principle; exact finite counterexamples, PROVED in the trivial sense): "full cut rank of the solution/count
tensor is necessary or sufficient for hardness." UNSAT gives rank 0 (no lower bound can come from the final object), and 2-SAT attains
full rank. Whatever the doc's Sec. 2.2 argument needs must be about INTERMEDIATE contraction tensors under a fixed order (treewidth
bounds of Markov-Shi type are upper bounds on contraction cost; they are not lower bounds on all algorithms). No unrestricted runtime
claim from rank, consistent with AGENTS.md.

COMPUTATIONAL/CONSISTENT: 1/f for a single aggregated non-vanishing axiom is full rank, consistent with the known FSTW-type
roABP-IPS_LIN' functional bounds. But per-clause multipliers have cut rank <= 22 at n=16, quantitatively illustrating the doc's own
"pole cancellation" caveat: single-axiom functional lower bounds do not transfer to CNF refutations through this aggregation.
This is not an roABP-IPS upper bound (variable order, width of sum_j g_j y_j, and asymptotics not analyzed).

## 5. Verification gates (for the audited candidate)

DISJ sanity: FAIL for the candidate (cut rank of DISJ-type equality is full yet easy, cf. C). Relativization: NOT APPLICABLE
(static algebraic measure, not a machine argument). Simultaneous DTISP: NOT APPLICABLE (no time-space claim). Deterministic
configuration counting: NOT APPLICABLE. Natural Proofs: cut rank is constructive and large, so as a circuit-lower-bound property it is
natural; algebrization not assessed.

## 6. OpenAI / Google GitHub survey (via GitHub code search; files not cloned)

openai/math: Lean `lean/OAI/Probability/RandomSAT/*` ("for every fixed clause size >= 3 the proper-clause satisfiability probability has a
positive finite limiting threshold"), preprints "A Limiting Satisfiability Threshold for Every Fixed Clause Size" (2026-09-25) and
"Computing the Random 3-SAT Threshold" (2026-09-27), `lean/OAI/Computability/MaxCut/Games/NP.lean`. Relevance: random k-SAT
thresholds pin the regime where average-case hardness conjectures live; they give no worst-case lower bound. UNVERIFIED by this run.
google-deepmind/formal-conjectures: `FormalConjectures/Millennium/PvsNP.lean` (statement only), `Paper/PudlakFiniteDomainConjectures.lean`
(Pudlák's finite-domain conjectures, proof-complexity adjacent, `sorry`), `Arxiv/0805.3777/TensorRank.lean` (max tensor rank of
3x3x5 = 6, Lean proof linked). A Lean-formal statement of P != NP could serve TMR-1 as a pinned target statement. UNVERIFIED.
No repository in either org was found claiming a SAT lower bound.

## 7. Next load-bearing lemma (suggested, for TMR-2/TMR-4 consideration via handoff)

Make sigma F3 precise: for the canonical first-falsified certificate of a random 3-CNF, bound the roABP width of sum_j g_j(x) y_j in
a fixed variable order as a function of n, and compare with the 2^{Omega(n)} single-axiom bound. If it is 2^{o(n)}, the doc's IIB
route via aggregated 1/f is dead for CNFs; if 2^{Omega(n)} for every order, it is a genuine (restricted, roABP-IPS_LIN) CNF lower bound
— a KNOWN-type result to check against Forbes-Shpilka-Tzameret-Wigderson before any claim.
