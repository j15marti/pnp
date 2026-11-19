# Strict-C local transfer: NTIME(n) -> clause-addressable CNF -> FW3 -> strict-C, with exact exponent slack

2026-11-19, America/Los_Angeles. Generic hourly "SAT lower bound" routine (not a TMR role; no TMR manuscript edited).
Base revision: `d55630ca024a4af03e8451ee77f4ddf757927393`. **P versus NP remains OPEN.**

## Named dependency advanced

The "last transfer gate" left OPEN by
`research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md` and
`research/coordination/2026-11-19_RESOURCE_RUN6_SAME_LANGUAGE_PINNING_HANDOFF.md`:
does the published SAT source model reduce to the fixed-width indexed 3-CNF (FW3) language with
polylog-local bits, so that known deterministic time-space lower bounds transfer to strict-C?
Also closes the computational gap that UNSAT controls had never been refuted at the full C level,
and that the compiler source code had not been committed.

Candidate (stated before search): for every d < 2cos(pi/7), strict-C in the fixed-width encoding
is not decidable by a deterministic random-access TM in time N^d and space N^{o(1)}.
Falsifiers considered: (F1) the known theorem is stated only for SAT under an encoding whose
clause boundaries are not locally addressable; (F2) the CNF clauses have unbounded width, so FW3
is not a direct target; (F3) polylog overheads break a boundary exponent pair; (F4) the C
reduction is not equisatisfiable in the UNSAT direction at the C level.
Outcome: F1 survives only as an explicit, narrow premise (P-CA below); F2 is closed by Lemma A;
F3 **is real** and corrects an earlier boundary claim (see Correction); F4 not observed.

## Sources consulted (primary)

1. R. Williams, *Inductive time-space lower bounds for SAT and related problems*, Comput. Complexity 15 (2006).
   PDF from https://people.csail.mit.edu/rrw/sat-journal-final.pdf, SHA256 `61b0dd2b467ae03141e8777c8ff454f9e34f9069d6108cc612c843d5932f8d8e`.
   Section 2.1 default model: random-access TM, read-only input, work tape, write-only index tapes (access cost O(log t)).
   Theorem 2.1: SAT is NQL-complete under quasi-linear-time, O(log n)-space reductions; each bit computable in polylog time and O(log n) space.
   Corollary 2.3: the lower bounds apply to any Pi such that SAT reduces to Pi with each bit computable in n^{o(1)} time.
2. D. van Melkebeek, *A survey of lower bounds for satisfiability and related problems*, FnT-TCS 2(3) (2006).
   PDF https://pages.cs.wisc.edu/~dieter/Papers/sat-lb-survey-fttcs.pdf, SHA256 `3bed6f5719eb84b475c27175cb9e2cd26d127cbc08726529dc19d83c73a16085`.
   Lemma 2.2 (every NTIME(n) language Karp-reduces to SAT in time n(log n)^{O(1)}; the i-th bit in time (log n)^{O(1)}, space O(log n));
   Corollary 2.1 (time-space bounds transfer with strict exponent slack d' > d, e' > e); Theorem 1.2 (Williams):
   SAT is not solvable by a deterministic random-access machine in time n^{2cos(pi/7)-o(1)} and space n^{o(1)};
   proof of Lemma 2.2 in Section 2.3.1 builds polylog-size clauses per computation step / sorting-network connection.
3. Buss and Williams (2015), as already cited in the repository reports (Figure 8.3 pair (1.34070, 0.5)); not re-read this run.

## Model and encodings (declared)

Machine: deterministic random-access TM of source 1, Section 2.1. DTISP(t, s) as there.
STRICTC-FW: input `1^w 0`, then N and M in w bits each, then M records of three w-bit names in [N];
YES iff some map names -> Z_5 satisfies C on every record, where R(a,b) iff (b-a) mod 5 in {1,3},
C(x,y,z) = R(x,y)R(y,z)R(z,x) or R(x,z)R(z,y)R(y,x) (30/125 triples). Records with repeated names are
malformed and rejected (the compiler never emits them). FW3 is the analogous fixed-width 3-CNF format.
The executed script uses a 32-bit header (finite-scope instantiation of the same layout).

## Premise P-CA (clause-addressable form of Lemma 2.2) — KNOWN at proof level, independent review OPEN

For every L in NTIME(n) there are W(n) = (log n)^{O(1)} with W >= 3, v(n), m(n) <= n(log n)^{O(1)}
(computable in polylog time), and a deterministic machine that on (x, j), j < m(n), outputs clause j of
a CNF phi_x as exactly W literals (shorter clauses padded by repeating a literal; extra clause slots filled
by repeating an existing clause) in time (log n)^{O(1)} and space O(log n), with x in L iff phi_x SAT.
This is what the construction in source 2 Section 2.3.1 produces (each constituent condition is a block of
polylog-size clauses indexed by step or network connection; the layout depends only on n).
The *statement* of Lemma 2.2 is bit-addressed in an unspecified encoding; reading it in clause-addressed
form uses its proof. This is the single remaining non-executed premise; it is not a new conjecture.

## Lemma A (PROVED/EXACT): width-W CNF -> FW3, one source call per output clause

Given clause-oracle access to a width-W CNF on v variables, m clauses, let v' = v + m(W-3), m' = m(W-2).
For t = j(W-2) + k, with fresh y_{j,q} = v + j(W-3) + q + 1:
k = 0 gives (l_0, l_1, y_{j,0}); 0 < k < W-3 gives (not y_{j,k-1}, l_{k+1}, y_{j,k}); k = W-3 gives (not y_{j,W-4}, l_{W-2}, l_{W-1}).
(W = 3 is the identity.) Standard chain: the conjunction of the W-2 clauses is satisfiable over the y's iff some
l_i is true, so FW3 is equisatisfiable, with one oracle call and O(log n)-bit arithmetic per clause.

## Lemma B (PROVED/EXACT, prior construction, re-implemented independently here)

For FW3 F with v' variables, m' clauses: K(F) has 15+9v'+39m' names and 10+7v'+31m' strict-C clauses
(H3: base triangle T,F,B; complementary pairs; per clause NAE(a,b,s) and NAE(not s,c,F) triangles; H5: two
universal apices; each edge {u,w} -> C(h_e,u,w), fresh h_e, using: exists h C(h,u,w) iff u != w).
F SAT iff K(F) SAT. Record i depends on at most one FW3 clause, located by segment arithmetic.

## Lemma C (PROVED): local bit access

By composition, bit p of the STRICTC-FW encoding of K(FW3(phi_x)) is computable from x in time (log n)^{O(1)}
and space O(log n): decode (record, field, bit) from p by division with w = O(log n)-bit numbers, call
c_clause (<= 1 FW3 call), which calls the clause oracle of P-CA at most once. Encoded length
N_bits = O(m W log n) = n (log n)^{O(1)}.

## Theorem (CONDITIONAL only on P-CA; otherwise from KNOWN THEOREMS)

Let d >= 1, e >= 0. If NTIME(n) is not contained in DTISP(n^{d'}, n^{e'}) for some d' > d, e' > e, then STRICTC-FW is
not in DTISP(N^d, N^e). In particular (source 2 Thm 1.2 at the NTIME(n) level, from which the SAT version is derived):
for every d < 2cos(pi/7) ~ 1.801, STRICTC-FW is not decidable by a deterministic random-access TM in time N^d and
space N^{o(1)}.

Proof. Given a decider A for STRICTC-FW in time N^d, space N^e, decide L in NTIME(n) by running A on the virtual
input K(FW3(phi_x)); serve each input-index query by Lemma C in polylog time, reusing one O(log n) scratch area.
SAME_REALIZATION ledger: time N^d (log n)^{O(1)} + (log n)^{O(1)} per input access <= n^d (log n)^{O(1)};
peak space N^e + O(log n) + index tapes O(log N) <= n^e (log n)^{O(1)}. Both lie inside DTISP(n^{d'}, n^{e'})
for any d' > d, e' > e, contradiction. Nothing is materialized; source x stays read-only.

**Correction (scope, local not model change).** The earlier repository phrasing "a strict-C decider with
N^{1.33+o(1)} time and N^{.5+o(1)} space contradicts Buss-Williams at (1.34070, 0.5)" is too strong at the space
boundary: the transfer costs polylog factors in space, so from an exclusion exactly at space exponent 0.5 one gets
STRICTC-FW not in DTISP(N^c, N^s) for c < 1.34070 and s < 0.5 strictly, not space N^{0.5+o(1)} (and not N^{0.5}
exactly) unless the source result itself is stated with that slack. Use strict inequalities in both exponents.

## Gates

DISJ sanity: PASS. The argument uses only NTIME(n)-hardness under local reductions; it yields nothing for easy
controls (2-colouring CSPs, Horn, 2-SAT, affine) for which no such reduction exists.
Relativization: PASS for the new step (a black-box input-access simulation, relativizes); the imported theorem is a
published result, not re-proved. No nonrelativizing claim is made.
Simultaneous DTISP: PASS, explicit same-run ledger above.
Deterministic configuration counting: PASS (2^{N^{o(1)}} configurations exceed N^d; no conflict).
Algebrization / Natural Proofs: NOT APPLICABLE (uniform time-space bound via indirect diagonalization, no circuit claim).
Status of P vs NP: unchanged OPEN. A bound below n^{1.81} is polynomial; nothing here is superpolynomial, and nothing
transfers to high-girth or clause-critical promise families (K(F) has triangles in H3 and girth-6 incidence).

## Executed evidence (COMPUTATIONAL, finite)

Script `experiments/strictc_local_transfer/strictc_transfer.py`, SHA256 `4f176de43de9f41d39b05d37fa012da9a3471052040c5e35d4f7a2ea618b96e3`,
CPython 3.11.18, standard library, seed 2026111917, argument 60, 13.7 s. Raw output
`results/raw/strictc_local_transfer/2026-11-19_run1.json`, SHA256 `992a1a0f1c78f89e6c8eb8674b98bc391500b1b1189c26b60d1f7c74171e1f5c`.
Checks: 30/125 C triples; exists-head projection iff u != w on all 25 pairs; D5 invariance; 67 source CNFs (7 hand
UNSAT controls, 60 random with W in {3,4,5}); FW3 equisatisfiable by brute force 67/67; random-access records equal
an independently written dictionary-based builder 67/67, and 200 sampled encoded bits per case equal 67/67;
max one source-clause oracle call per output record; sizes asserted equal 15+9v'+39m' and 10+7v'+31m'.
Independent GAC+DFS 5-colour CSP solver (sees only C records; sound D5 orbit representative T=0, F in {1,2}, justified
by D5 invariance and the T-F edge) agreed with the source on 64/64 decided cases: 60 SAT (solver witnesses satisfy all
C records and project to satisfying assignments of FW3 and of the wide source 60/60; Boolean witnesses extend to full
C colourings 60/60) and **4 UNSAT refuted at the C level** (first C-level UNSAT refutations in this pipeline, including a
W=4 chain case). Undecided within 60,000 nodes, disclosed: 3 UNSAT controls (v=2,W=4 four-clause; v=1,W=5; v=3 all
eight sign patterns). Max instance 381 names, 300 clauses. Finite tests are not asymptotic proofs.

## External idea survey (this routine's standing request)

User Google Doc "P vs. NP Proof Attempts" (62.6 kB Drive export; read this run: Section 1 with its overview table, all section headings, Sections 3.3 and 4; the bodies of Sections 2.1-3.2 were NOT read in full): surveys holographic/matchgate,
tensor-network, IPS, GCT, functional-IPS and hardness-magnification attempts with their known barriers. No item gives a
new uniform SAT lower bound; the magnification "locality barrier" item is consistent with the scope limits above.
GitHub: openai/math (HEAD `4eaee87548250b2682affda7d05d947c05554bae`) has a 2026-09-25 preprint "A Limiting
Satisfiability Threshold for Every Fixed Clause Size" plus Lean `OAI/Probability/RandomSAT` — average-case threshold
theory, not a worst-case lower bound; useful only as a random-instance control. google-deepmind/formal-conjectures
(HEAD `d8d031d4998c78575159ccab9a7a9e95ce043883`) has `FormalConjectures/Paper/DisjointNPPairs.lean` with Lean
`ComplexityTheory` NP/coNP definitions — a candidate host for formally stating Lemmas A-C (not attempted).

## One next load-bearing lemma

Discharge P-CA by an explicit clause-addressed rendering of source 2 Section 2.3.1 (step blocks plus Batcher network
comparator clauses with arithmetic index maps), or locate a primary source that states Lemma 2.2 clause-addressed;
then re-read Buss-Williams Fig. 8.3 to confirm it is an NTIME(n)-level exclusion with the slack convention above.
