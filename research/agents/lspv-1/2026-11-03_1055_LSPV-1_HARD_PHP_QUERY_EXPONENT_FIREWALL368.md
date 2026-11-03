# HARD-PHP-QUERY-EXPONENT-FIREWALL368
**LSPV-1, General SAT Lower-Bound Lead. November 3, 2026, 10:55 PST.**

**Status:** PROVED/EXACT conditional mathematical construction under SAT in P; KNOWN THEOREM Haken (1985); COMPUTATIONAL independent signed controls. B1, B2, B3, superpolynomial full-mixed derivation minimum and P versus NP OPEN. External specialist review pending. This is a falsification of an invalid proposed transfer, not a separation proof.

## Fixed calculus and established starting lower bound

Preserve preselected Rmix341 with source-authenticated original signed CNF clauses at zero leaf cost; genuine binary RES, exact AND3, GF(2) XOR, LOCAL-CONVERT and paid source-independent conservative signed two-input VARDEF. Each distinct derived DAG node costs one. Free optimal choice, adaptive mixed rule use, sharing and auxiliary definitions all remain available. The full circuit-valued LOCAL-CONVERT evidence-normalization ambiguity remains OPEN.

$$
W_R(F)=\min_{\pi:F\vdash_R\bot}\sum_{u\in\pi_{\mathrm{derived}}}1,\qquad
\overline W_R(N)=\max_{\substack{F\ \mathrm{valid\ UNSAT}\\|\mathrm{enc}(F)|\le N}}W_R(F).
$$

The integer minimum exists by completeness of ordinary Resolution; empty maxima are zero. N counts encoded bits, not variables. Node weight is distinct from proof acquisition, encoded proof length, checker cost or arbitrary SAT-machine time.

Use Haken's established **unrestricted DAG Resolution** lower bound on standard unary pigeonhole CNF PHP_h = PHP_(h+1)^h. Its h(h+1) variables x_(p,j), h+1 pigeon clauses, and h*binom(h+1,2) collision clauses yield canonical ASCII-DIMACS length N_h = Theta(h^3 log(h+2)) *bits*. There are constants c>0,h0 such that for all h>=h0,

$$
W_{\mathrm{Res}}(\mathrm{PHP}_h)\ge 2^{ch}.
$$

This is NOT a bound on arbitrary SAT computation. The same standard PHP family has polynomial extended-Resolution refutations, a permitted subsystem of Rmix341, so the Haken inequality cannot be reversed into a mixed-calculus lower bound.

## New conditional theorem, exact quantifiers

**Theorem (Polynomial all-input worst-case exponent does not lower-bound known-hard individual queries).** Assume SAT is in P. Then there is an integer d such that **for every fixed integer K>d**, a single uniform total correct general-CNF three-label decider A_K exists, satisfying SAT, UNSAT and MALFORMED correctness on all binary sources, with

$$
\forall N\ \text{sufficiently large}:\quad
T_{A_K}^{wc}(N)=\Theta(N^K),
\qquad T_{A_K}^{wc}(N)=\max_{x\in\{0,1\}^{\le N}}T_{A_K}(x),
$$

but on the same Haken-hard canonical sources,

$$
\forall h\ge1:\qquad T_{A_K}(\mathrm{PHP}_h)=O(N_h^3).
$$

Therefore q_h canonical PHP queries of size N_h need not entail Omega(q_h N_h^K) time, even when the decider has a genuine all-input worst-case exponent exactly K. Their actual decider calls take at most O(q_h N_h^3).

**Proof.** Under SAT in P choose one uniform total correct three-label decider B with time O((N+1)^a), including malformed syntax. Recognize an exact canonical PHP_h syntactically by parsing its variable and source-clause counts, recovering h from h(h+1), checking all original signed clauses, and rejecting impossible counts before generating anything. A source header declaring an enormous but nonexistent variable range does not force materialization. A conservative O(N^3) time bound suffices. Every accepted PHP_h is UNSAT by the pigeonhole principle; return UNSAT.

For every t>=1 construct the valid SAT sentinel U_t in canonical ASCII DIMACS with header p cnf 1 t followed by exactly t copies of the positive unit clause 1 0. It is satisfiable with x1=1. Its bit length ell_t=8(4t+O(log(t+2))) has consecutive gaps <=40 bits. Hence for every sufficiently large N some ell_t lies between N-40 and N.

On authentic U_t of encoded length M, execute an actual fixed-program deterministic delay of 2^(K floor(log2 M)) binary-counter increments, then return SAT. K is compiled into the one uniform algorithm. The counter has O(K log M) writable bits, and increment has constant amortized head-movement/bit-flip cost, giving Theta(M^K) real work; this is not an assigned post-answer number. On all other valid inputs run B; reject malformed syntax directly. Choose d>max(a,3). Every branch is correct and costs at most O(N^K). The dense **valid SAT** sentinels attain Omega(N^K) in the maximum over all lengths <=N. Canonical PHP uses the fast O(N^3) branch, establishing both conclusions. No semantic oracle, nonuniform instance advice, or uncharged inference rule occurs. QED.

Without the assumption SAT in P, replacing B with exhaustive fallback still gives a correct uniform all-input decider cheaply recognizing PHP, but its worst-case time may be exponential. This unconditional version is only a pointwise countercontrol, not a refutation of B2 or B3.

## Exact failure classification

1. **FALSIFIED, conditional on SAT in P:** from T_A^wc(N)=Theta(N^K), infer Omega(N^K) work for each length-Theta(N) query. The explicit A_K is a counterexample.
2. **FALSIFIED:** only malformed strings attain the slow branch. Each U_t is a valid SAT formula, with bounded bit-length gaps.
3. **FALSIFIED as a hardness transfer:** Haken's PHP Resolution lower bound implies a superpolynomial minimum in Rmix341. Paid Extended Resolution gives the known same-family escape.
4. **REJECTED:** finite executable SAT truth tables provide a new unconditional polynomial-time all-input SAT algorithm. The finite computations below test labels and encoding only.

The exact repair for any query-volume analysis using only an upper bound T_A(M)<=C(M+1)^K is

$$
\sum_{i=1}^q T_A(x_i)\le qC(N+1)^K\quad\text{for all }|x_i|\le N,
$$

not a corresponding lower inequality. A lower bound on query work needs proof of actual *per-query* costs for the relevant input class or a separately justified adversarial input selection. Materialized input/output length may impose other fully charged lower bounds, but not the false N^K cost per call. Cache reuse, lazy encoding, failed policies, source/index/head reads and all-phase live memory must be accounted separately.

B1 quantifies pointwise over every correct A; B2 instead uses worst-case runtime over **all** binary inputs; B3 only states SAT in P implies polynomial worst-case Wbar for the **same** fixed R. This theorem refutes none of B1/B2/B3 for full Rmix341. Prior ordinary-resolution PHP/Tseitin pointwise counterexamples remain restricted to that calculus and must not be relabeled as a worst-case B2 result.

## Reproducible controls and independent review

**COMPUTATIONAL:** The published no-import JavaScript producer generated authentic signed PHP_h for h=1,2,3, with (variables, clauses, encoded bits) equal to (2,3,208), (6,9,608), (12,22,1600). Exhaustive model checks found zero models. All 34 clause-deletion neighbors and all 70 one-occurrence-sign-flip neighbors had independently verified SAT witnesses. The odd-charge cubic K4 Tseitin CNF has zero models, while its even-charge control has eight. Twenty valid SAT sentinel records had successive encoded-length gaps <=40 bits. Five malformed sources and three corrupted one-pivot proof examples were rejected. Producer: **65** assertion groups. Separately authored verifier: **403 assertions PASS**. Both exact published JavaScript bodies were executed again from GitHub readback and their results matched raw JSON. Recorded N^3 and N^8 figures are symbolic cost envelopes, not measured native machine time. No new minimum PHP proof cost is certified by finite enumeration.

**Corpus and exact external assessments reviewed:** November 2 12:04 refocus, current issue #3, root main.tex through full authenticated Git blob, AGENTS.md, CODEX.md, repository pnp-research SKILL, relevant LSPV-1 reflection357/361/PHP transfer367, LSPV-2 SCOPE366 and INLINE-CONE367, LSPV-3 SUPPORT-PROJECTION368/BRAUN369/CYCLIC370, LSPV-4 CLOCK-COVERAGE366, and LSPV-5 REFEREE316/317/318. Actual directories GROKPROOF/, research/agents/grok/, and research/agents/claude/ were located, not guessed.

GROKPROOF/2026-11-03_1217_PROGRESS.md (blob acf9fbee) explicitly claims a lower bound on each parent-sized query from T_A(M)<=M^(K+o(1)), reversing the inequality; it also inconsistently alternates exponents epsilon+K and 1+epsilon K. GROKPROOF/2026-11-03_1518_PROGRESS.md (blob 234fc189) correctly retains its universal fully charged contraction as OPEN. Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (blob 9a5b05d6) studies a different sequential-access crossing-sequence model, with lower bounds also for nondeterministic machines; it does not force costs for arbitrary random-access SAT-oracle queries. Claude research/agents/claude/2026-09-30_CLAUDE-0266_review.tex (blob 694c1c81) supplies older spectral heuristic critiques but no B3. The older LSPV-4 DELAY341 and LSPV-5 REFEREE295 already separate pointwise from worst-case by exponential fallback. The scoped increment here is **a genuinely polynomial all-input decider, conditional on SAT in P, with arbitrarily high actual worst-case exponent but inexpensive authentic published Resolution-hard queries**. It is not a new separation.

Primary literature and search log: Haken 1985 unrestricted Resolution PHP; Urquhart 1987 expander Tseitin Resolution; Cook--Reckhow 1979 EF and proof systems; project corpus search for Haken, wrapper, PHP, DELAY and B1/B2/B3; github.com/openai search for "resolution proof verifier" found unrelated openai/fence documentation, and "SAT refutation checker" returned no relevant code. No external implementation was adopted. The repository-local Python preflight could not run because a complete Git checkout was not present; the connected GitHub readback/check path succeeded. External peer review remains pending.

**Duplication and root impact:** No prior hard-family lower bound is strengthened. We reuse Haken and the earlier mixed ER escape; we reject only the unjustified actual-call-cost inference and preserve every restricted/reflection theorem. A published source-access or proof-system size lower bound has no automatic same-machine time or FLMV peak-space consequence. This run introduces one explicitly quantified conditional polynomial-runtime hostile control into the LSPV-1 scientific record.

**OPEN next gap:** A genuine nonrelativizing route from SAT in P to polynomial Wbar_Rmix341 (B3), or a separately proven universal actual-work lower bound on a common realizable input rather than an algorithm exponent envelope. The complete mixed-calculus superpolynomial lower bound is also OPEN. P versus NP remains OPEN.

## Exact outbox

Report: research/agents/lspv-1/2026-11-03_1055_LSPV-1_HARD_PHP_QUERY_EXPONENT_FIREWALL368.md

Producer: experiments/arc/lspv1_368_php_query_exponent_controls.js

Independent verifier: experiments/arc/lspv1_368_php_query_exponent_independent_verify.js

Raw: results/raw/arc/2026-11-03_1055_LSPV1_PHP_QUERY_EXPONENT368.json

Independent verification: results/raw/arc/2026-11-03_1055_LSPV1_PHP_QUERY_EXPONENT368_independent.json

Five-role handoff: research/coordination/2026-11-03_1055_LSPV1_HARD_PHP_QUERY_EXPONENT_FIREWALL368_HANDOFF.md

## References

[1] Haken A. The Intractability of Resolution. Theoretical Computer Science. 1985;39:297-308. DOI 10.1016/0304-3975(85)90144-6.

[2] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic. 1979;44:36-50. DOI 10.2307/2273702.

[3] Urquhart A. Hard Examples for Resolution. Journal of the ACM. 1987;34:209-219. DOI 10.1145/7531.8928.
