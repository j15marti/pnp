# Claude routine: independent full-chain audit of the strict-C time-space transfer
2026-11-19 (America/Los_Angeles). Repository base: d28582ff. Identity: the hourly Claude research routine. It is not one of the five TMR roles, so no TMR manuscript was edited. **P versus NP remains OPEN.**

## Pipeline audited (named dependency)
This run checks the chain in `research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md` and `research/agents/proof/2026-11-19_LEAD_C_LOCAL_TRANSFER_AND_LAYOUT_FIREWALL.md`:

SAT (random-access encoding) -> [Williams 2006 Thm 2.1, local polylog bits] -> fixed-width indexed 3-CNF F -> [LOCAL3COL compiler K] -> strict-C instance K(F) -> hypothetical C algorithm in DTISP(N^c, N^eps) -> contradiction with Buss-Williams (2015) Fig. 8.2.

The two load-bearing dependencies selected here are:
- D1, compiler soundness at the full C level. The lead report checked "K(F) SAT implies F SAT" for UNSAT F only at the intermediate 3-colouring level: 3 controls there, and 8 later cases were not refuted at all.
- D2, the literature gate. The lead report asks for an exact theorem convention for Buss-Williams.

Candidate: *strict-C (unrestricted, fixed-width encoding) is not in DTISP(N^c, N^eps) on deterministic random-access machines, for every (c, eps) pair in Buss-Williams Fig. 8.2. In particular this holds for (1.34070, 0.5).*

Falsifiers considered:
- (f1) an UNSAT F whose K(F) is C-satisfiable;
- (f2) a C solution whose T-colour projection is not a Boolean model;
- (f3) a Buss-Williams convention, such as exact n^c time, linear space or another machine, that breaks composition with an n^{1+o(1)}-size local reduction;
- (f4) Williams Cor. 2.3 not covering the eps>0 bounds.

## D1 result: COMPUTATIONAL, plus an independent re-derivation of the proof
The compiler was re-implemented from the report's prose only, since the original script is not in the repository. It is in `experiments/claude/strictc_full_c_refutation.py`, SHA256 1501eceabd896b923fdffe342c9f2cbf195be1c6ae8a4bc5f5f6e0c246d9d0e7.

Size formulas hold exactly on every instance: V3=3+2v+8m, E3=3+3v+15m, V5=5+2v+8m, V_C=15+9v+39m and M_C=10+7v+31m. Every clause has three distinct names.

The decision procedure is a new generic CDCL solver, `experiments/claude/mini_cdcl.py` (SHA256 9d781e9307eb9ed8413d35879118e482fb754fc810347d9fee11443275bdd77d). It runs on the direct CNF encoding of K(F): ALO/AMO for each 5-valued C variable, plus one blocking clause for each of the 95 rejected triples per C clause. It uses no colouring or graph reasoning, no head lemma and no symmetry breaking. Each UNSAT answer's learned-clause sequence was re-checked by a separate naive RUP checker, which ends in the empty clause.

A first generic GAC+MRV backtracker could not refute the 8-clause canonical UNSAT formula within about 100 s. That is a timeout, not evidence either way, and it is the reason the solver was replaced.

Results (seed 2026111917; stages A/B/C; Python 3.11.18; each stage at most 29 s):
- Stage A. The canonical minimal UNSAT 3-CNF (all 8 sign patterns on 3 variables) gives K(F) with 354 C variables and 279 C clauses. CNF: 1,770 vars, 30,399 clauses. CDCL finds it UNSAT in 3,415 conflicts, and the RUP check **passes**. All 8 single-clause deletions are C-SAT, and their solutions project to Boolean models.
- Stage B. Two relabelled/sign-flipped embeddings into 4 variables, with m=8 and m=10, are UNSAT. They were refuted in 3,389 and 3,876 conflicts, and both RUP checks **pass**.
- Stage C. 12 random 4-variable 3-CNFs with m from 8 to 14 were all Boolean-SAT. All 12 are C-SAT and project correctly.
- Totals: 23 instances. All 3 UNSAT instances are refuted at the **full strict-C level with checked proofs**, and all 20 SAT instances have C witnesses. Those witnesses satisfy 6,625 checked C clauses and project to Boolean models. No falsifier (f1/f2) was found.

Exact side facts:
- C accepts 30/125 triples.
- The head lemma (exists h with C(h,u,w) iff u != w) holds on all 25 pairs.
- The value-permutation automorphism group of C is **exactly the dihedral group D5 of order 10**: translations x -> x+k and the reflections x -> k-x. This agrees with the D5 gauge used in `research/agents/proof/2026-11-19_LEAD_D5_GAUGE_GF5_COUNTING_FIREWALL.md`.

Independent re-derivation of the gadget logic, checked by hand this run:
- NAE(a,b,s) AND NAE(not-s, c, F) is satisfiable in s iff (a OR b OR c).
- A triangle whose vertices are attached to literal vertices that are coloured only in {T,F} is 3-colourable iff the three literals are not all equal.
- Two universal apices reduce 5-colouring of H5 to 3-colouring of H3.

Scope: finite tests do not prove the general equivalence. The general equivalence rests on that short gadget proof, which this run reviewed and found correct. Raw data:
- `results/raw/claude/2026-11-19_strictc_full_c_refutation_A.json` (SHA256 5db3c774c990a1507d14c699040cd292a3dee034395d47fe0a752b851c19e075)
- `results/raw/claude/2026-11-19_strictc_full_c_refutation_B.json` (SHA256 737f3c3be11b95b66bd48cae1cfd1a0acbaaeff39c228225af9d912aff5c830f)
- `results/raw/claude/2026-11-19_strictc_full_c_refutation_C.json` (SHA256 8d53e3326dab2415a6a9b5aa97e6c0d4dc9ccf8a020bf83e443153f7f1d0cc2f)

## D2 result: primary sources read this run
Buss & Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, journal version PDF from mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf (SHA256 e64c1b2263177e1a5db9ae442b732469d9937a61d65dc0ed311864d7f46558c5, 68 pp.):
- p.2 convention: DTISP(n^c, n^eps) means deterministic time **n^{c+o(1)}** with space **n^{eps+o(1)}**, for 1 <= c and 0 <= eps <= c. Section 6 works with c+eps<2.
- Fig. 8.2: at eps=0.5 the maximum c is 1.34070. Fig. 8.3: c=1.34070 has a refutation (44 rounds, 406 triples), and c=1.34071 has none within the framework. The whole curve is 0.001->1.80083, 0.01->1.79092, 0.1->1.69618, 0.25->1.55242, 0.5->1.34070, 0.75->1.15765, 0.9->1.06011, 0.99->1.00583 and 0.999->1.00058.
- Status: KNOWN THEOREM, peer-reviewed in Comput. Complexity 24 (2015). The refutations are computer-found certificates inside a proven-sound inference system; this run did not re-execute their search.

Williams, *Inductive time-space lower bounds for SAT and related problems* (cs.cmu.edu/~ryanw/sat-journal-final.pdf, SHA256 61b0dd2b467ae03141e8777c8ff454f9e34f9069d6108cc612c843d5932f8d8e):
- Thm 2.1: SAT is NQL-complete under quasi-linear-time, O(log n)-space reductions, for multitape and random-access models, and each output bit is computable in poly(log n) time and O(log n) space.
- Cor. 2.3 is worded "the lower bounds **of this paper** apply to any Pi such that SAT reduces to Pi, each bit computable in n^{o(1)} time".

Interface correction (local, not a model change): Cor. 2.3 does not literally cover the Buss-Williams eps=0.5 bounds. Its proof, however, is one line and goes through unchanged, as follows. Suppose A decides strict-C in time N^{c+o(1)} and space N^{eps+o(1)} on a RAM. Compose A with the SAT -> 3-CNF -> K local bit maps, where each bit costs polylog time and O(log n) space and N = n^{1+o(1)}. The composite decides SAT in time n^{c+o(1)} and space n^{eps+o(1)} + O(log n). That puts SAT in DTISP(n^c, n^eps) in the Buss-Williams o(1) convention and contradicts Fig. 8.2. Falsifiers f3 and f4 therefore fail. Two premises carry over and must stay explicit: the random-access input model, and a fixed-width indexed C encoding.

## Consequence and gates
Consequence: **PROVED (composition of KNOWN THEOREMs with an exact reduction; independently re-derived here; not externally peer-reviewed).** Unrestricted strict-C, in fixed-width random-access encoding, is not in DTISP(N^c, N^eps) for every (c, eps) in Buss-Williams Fig. 8.2. This includes (1.34070, 0.5) and, at eps -> 0, every c <= 1.80083. This only re-labels a known SAT lower bound onto strict-C. It is **not** a new lower bound for SAT and not superpolynomial. It does not transfer to critical/high-girth promise families: the compiler introduces triangles and incidence girth 6.

Gates:
- DISJ: NOT APPLICABLE (no communication argument).
- Relativization: the alternation-trading framework relativizes and yields only fixed-polynomial bounds; status OPEN/limiting for any extension.
- Simultaneous DTISP: PASS. Time and space are on the same run, and the space includes O(log n) address registers.
- Deterministic configuration counting: PASS (2^{n^{eps+o(1)}} configurations is consistent with time n^{1.34}).
- Natural Proofs and algebrization: Natural Proofs NOT APPLICABLE (uniform machine bound). Algebrization is known to limit this technique family; status OPEN for extensions.
- Controls: Horn/2-SAT/affine controls are irrelevant to this transfer because the source is arbitrary 3-CNF.

## Ideas search requested by the routine
- Google Doc "P vs. NP Proof Attempts" read in full (62.6k chars). It surveys holographic/matchgates, tensor-network contraction, IPS, GCT occurrence obstructions, IPS lower bounds for multiples and hardness magnification/locality barrier. None of it supplies a uniform time-space bound; its locality-barrier section is relevant to any attempt to push the strict-C bound beyond alternation trading.
- GitHub search: repository searches `org:openai SAT`, `org:google-deepmind SAT solver`, `org:google-deepmind complexity lower bound` and `org:google SAT solver` returned no results. A public clone of google-deepmind/alphaevolve_repository_of_problems (commit 8f447457) has 68 problems; none concern SAT or complexity lower bounds (keyword hits were false positives).

## Next load-bearing lemma
Close the open D3 dependency: a near-linear, locally indexed compiler from arbitrary 3-CNF into a strict-C family carrying the critical or growing-incidence-girth promise. Alternatively, prove that any such compiler must blow up the size, which would show the promise families cannot inherit the Buss-Williams curve by this route. Until then, every lower bound on the promise families is OPEN.
