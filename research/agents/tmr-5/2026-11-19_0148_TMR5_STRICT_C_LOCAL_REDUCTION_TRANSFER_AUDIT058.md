# TMR-5/058 independent audit: strict-C local reduction and the SAT time-space transfer gate

**2026-11-19 01:48 PST (America/Los_Angeles).** Role 5 (PNP Machine Bottleneck Redteam / independent audit role named in `research/coordination/2026-11-19_LOCAL3COL_C_LEAD_RESOURCE_HANDOFF.md`).
Audited object: proof lead report `research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md` at main `b58e96a5`.
P versus NP remains **OPEN**.

## Candidate, quantifiers, falsifiers

**Candidate (end-to-end chain).** For deterministic random-access Turing machines in the van Melkebeek model (indexed tapes; space = largest indexed position on non-input tapes; read-only input), strict-C satisfiability under a fixed-width indexed encoding is not in DTISP(n^{1.33}, n^{0.5}) and not in DTISP(n^{2cos(pi/7)-delta}, n^{o(1)}) for any delta>0. Chain: x in NTIME(n) language -> quasi-linear local CNF (KNOWN) -> clause-indexed fixed-width 3-CNF F -> lead's local map K(F) -> hypothesized C solver on virtual input -> NTIME(n) in DTISP -> contradiction with an alternation-trading refutation (KNOWN).

**Falsifiers tested.** (F1) a gadget/count error in the lead's construction; (F2) a non-local clause oracle (reads more than one source clause, or needs a materialized graph); (F3) the "near-linear output for every F" claim; (F4) the Buss–Williams number at epsilon=0.5, or a machine-model mismatch.

## Results

**F1 survived, PROVED/EXACT (independent derivation).** Hand derivation: V3=3+2v+8m, E3=3+3v+15m; H5 adds two apices, so E5=E3+1+2V3=10+7v+31m; one fresh head per edge gives V_C=V5+E5=15+9v+39m and M_C=E5. The head lemma: for u!=w exactly one of R(u,w), R(w,u) holds (d and -d mod 5 split {1,3} vs {2,4}); if R(u,w) with d in {1,3}, a head h needs (u-h)+(h-w)=-d in {2,4}, which is a sum of two elements of {1,3}. If u=w, both disjuncts need R(u,u), which is false. NAE(a,b,s) and NAE(not s,c,F) give s=F => a or b, s=T => c and not(a and b); their union is a or b or c. C has a 10-element affine symmetry group x -> ax+k, a in {1,4}, all k. That is translation plus reflection, and multiplication by 2 is not a symmetry.

**F2 survived, COMPUTATIONAL plus PROVED.** The oracle `edge_local` maps clause index i to a segment by arithmetic and reads at most one source literal. Measured: at most 5 literal-bit reads beyond a 22-bit header on the test widths, and it uses O(1) integer registers of O(log(v+m)) bits. It matched an independent name-based materialized builder on all 51,311 edges of 300 seeded formulas.

**F3 FALSIFIED as stated ("for every F", "near-linear output").** The output size is Theta((v+m) log(v+m)), not O~(|F|), because the header may declare unused variables. The smallest family: v=2^k-1, m=1, clause (x1 or x2 or x3), with source length 8k+17 bits in our encoding (57 bits at k=8, 177 bits at k=32). That source yields M_C=10+7v+31 C clauses: 1,826 at k=8 and 30,064,771,106 at k=32, so the output is exponential in |F|. Equisatisfiability and local access survive. **Local repair:** restrict the 3-CNF language to v<=3m, which the header check verifies in O(log) space. Every variable of a clause-indexed formula produced by the reduction occurs, so v<=3m holds there. Alternatively, accept padded inputs and charge size by v+m. The repair does not affect the transfer below, because every transferred F has v<=3m.

**F4 survived, KNOWN THEOREM (sources read this run).**
- Buss & Williams, *Limits on alternation-trading proofs for time-space lower bounds*, Comput. Complexity 24 (2015). Journal PDF from https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf, SHA256 `e64c1b2263177e1a5db9ae442b732469d9937a61d65dc0ed311864d7f46558c5`. Fig. 8.2 gives c=1.34070 at epsilon=0.5 as the maximal c with an alternation-trading refutation. Fig. 8.3 reports a refutation at 1.34070 (44 rounds, 406 triples) and none at 1.34071. At epsilon near 0, the paper proves 2cos(pi/7)≈1.8019 is optimal for alternation trading. DTISP(n^c,n^eps) is defined with n^{o(1)} slack.
- van Melkebeek, *A Survey of Lower Bounds for Satisfiability and Related Problems*, FnT-TCS 2(3) 2007, ECCC TR07-099, PDF SHA256 `d59b708e8ac7e3732e2a221a0afe25f308fff39b3d5dc4fcee11f856a63cb60a`. Lemma 2.3: every language in NT(n) Karp-reduces to SAT in time n(log n)^{O(1)}, and the i-th bit is computable in time (log n)^{O(1)} and space O(log n). Corollary 2.4: if NT(n) is not in DTS(n^d,n^e), then SAT is not in DTS(n^{d'},n^{e'}) for d'<d, e'<e. The text says the same holds for natural NP-complete problems with such reductions. The machine model is the random-access TM described in Section 2.2, with the space convention quoted above.

## Transfer theorem (CONDITIONAL on one clause-index normal form; independent external review OPEN)

Let strict-C-SAT_fw be the set of fixed-width encoded strict-C instances (a header, then M triples of variable indices) that are satisfiable over Z5.

**Claim.** If strict-C-SAT_fw is in DTISP(n^c, n^eps) on van Melkebeek random-access TMs, then NT(n) is in DTISP(n^{c+o(1)}, n^{eps+o(1)}). Hence strict-C-SAT_fw is not in DTISP(n^{1.33}, n^{0.5}) (indeed for every (c,eps) with an alternation-trading refutation in Fig. 8.2), and not in DTISP(n^{1.8019}, n^{o(1)}).

**Proof sketch.** Compose x -> F_x -> K(F_x). By premise P1, clause j of F_x is computable from (x,j) in polylog time and O(log n) space, and |F_x| = n polylog n with v<=3m. K's clause i needs O(1) arithmetic and at most one F-clause, so each bit of K(F_x) costs polylog time and O(log n) space. Run the hypothesized solver with its input tape replaced by this virtual oracle. Each input access is recomputed, giving time n^{c+o(1)}. Writable space is n^{eps+o(1)} plus O(log n) for the oracle, and the oracle keeps no retained state between accesses. Because K preserves satisfiability, the composite decides x. The polylog factors are absorbed by the n^{o(1)} convention. The DTISP contradiction is the cited refutation.

**Premise P1 (the one remaining sub-gate).** Lemma 2.3 is stated *bitwise* for some encoding of a CNF whose clauses have polylog size. K's oracle needs *clause-indexed* access to a 3-CNF. That follows if every clause is padded to one width L(n) (by repeating a literal), with Tseitin splitting into L-2 width-3 clauses and fixed arithmetic offsets. The construction text of Sec. 2.3.1 (fixed templates; Batcher network connections computable in polylog time and log space) supports this, but no published statement in that exact form was pinned this run. Status: CONDITIONAL, believed standard. Also check the clause-indexed statements in Fortnow–Lipton–van Melkebeek–Viglas, JACM 52 (2005), and Tourlakis (2001).

**Scope.** Deterministic random-access machines only, total deciders, and no randomized or quantum transfer. This is *not new mathematics beyond the gadget*: every problem with local quasi-linear SAT reductions inherits these exponents. Buss–Williams prove that this method cannot exceed 2cos(pi/7) at subpolynomial space, so the chain is capped well below any superpolynomial or P-vs-NP consequence. A "sound one-sided solver" counts only if it is uniformly clocked and decisive on every instance of its polarity, as the lead already notes.

## Direct strict-C-level refutations (COMPUTATIONAL; new relative to the lead)

The lead refuted UNSAT controls only at the 3-COLOR level. Here a generic generalized-arc-consistency backtracking solver ran on K(F). It uses only the 30-tuple C table and one translation fix, which is sound by symmetry, and no projection or graph knowledge.

| control | v | m | V_C | M_C | verdict | nodes |
|---|---|---|---|---|---|---|
| x and not x (x x x),(-x -x -x) | 1 | 2 | 102 | 79 | UNSAT | 1,541 |
| random UNSAT #0 | 1 | 3 | 141 | 110 | UNSAT | 5,381 |
| random UNSAT #1 | 1 | 4 | 180 | 141 | UNSAT | 31,013 |
| two-variable repeated literals | 2 | 4 | 189 | 148 | UNSAT | 27,557 |
| all 8 clauses on 3 variables | 3 | 8 | 354 | 279 | UNKNOWN (40,000-node budget) | 40,000 |
| first 7 of those 8 (SAT control) | 3 | 7 | 315 | 248 | SAT, assignment verified | 170 |

The all-8 control is not refuted at the C level within the 30-second stage rule. Its UNSAT status rests on the proved projection argument plus Boolean enumeration.

Malformed sources: all 9 were rejected (bad magic, truncation, trailing bit, index 0, index > v, m=0, v=0, width 0, field/length mismatch). The 300-formula corpus (seed 20261119, v in 1..5, m in 1..8) reproduces the lead's totals *exactly*: 286 SAT and 14 UNSAT sources, 51,311 edges, and 48,289 C clauses true under extended witnesses. The witnesses project back to satisfying Boolean assignments. This exact agreement means the sampling recipe coincided, so the run is a replication of the same corpus rather than a fresh sample. The gadget code was written independently.

## Four gates

- **DISJ:** PASS. No rank or communication quantity is used, and DISJ is not a reduction target.
- **Relativization:** NOT APPLICABLE to a separation. The bound is an inherited known theorem, and its method has the Buss–Williams ceiling. Algebrization and Natural Proofs are not engaged.
- **Simultaneous DTISP:** PASS. The statement is exactly a simultaneous bound, conditional on P1.
- **Configuration counting:** PASS as an upper-bound consistency check. Time n^{1.33} at space n^{.5} is far below 2^{O(S)}.

Controls: the gadget has incidence girth 6 (triangles), so there is no transfer to critical or high-girth promise families, as the lead stated. /341 is FAIL as full UNSAT authority, and /386 is RESTRICTED.

## Evidence

- Code: `experiments/tmr/tmr5_strict_c_local_reduction_audit058.py`, SHA256 `e7fda48b65c273cf3ba5dbc2affd87a2cdd0304606a1e1e70f25e583270f89e6`, git blob `af441a84c97188247f1eeece5dbc53a7dc48094d`. Revision `TMR5_STRICT_C_LOCAL_REDUCTION_AUDIT058_v1`; Python 3.11.18; 17.2 s.
- Raw: `results/raw/tmr/2026-11-19_0148_TMR5_STRICT_C_LOCAL_REDUCTION_AUDIT058_RAW.json`, SHA256 `2d57ac521f3bc7965a56e3629951d0a787b605f5d20a4a8c00a25d0afb6b8666`, git blob `346a6bcc01a26cb98f8ca0323003808c1cf511f6`.
- An earlier run with a 200,000-node budget took 49 s, over the stage rule. It also left the all-8 control UNKNOWN, and its output was discarded.
- Not executed: repository preflight, LaTeX build, the lead's own script (not in the repository), and any external SAT solver (none installed).

## Other inputs reviewed

The Google Doc "P vs. NP Proof Attempts" (66.7k characters) is a survey of six barrier trajectories: holographic, tensor network, IPS, GCT, algebraic proof complexity, and hardness magnification/locality. It contains no time-space or alternation-trading content that bears on this chain. I read the header and table and grepped the full text for DTISP/time-space/alternation terms. I did not read the remainder in full.

GitHub: repository search found `google-deepmind/formal-conjectures` (Lean conjecture statements). Code search outside this session's repository scope returned nothing, and no OpenAI or Google repository with SAT time-space content was found.

## One next lemma

Pin P1: a published clause-indexed 3-CNF form of the quasi-linear NTIME(n)->SAT reduction (FLvMV 2005 or Tourlakis 2001), or prove the padding and splitting step from Lemma 2.3's construction. That closes the chain at the KNOWN THEOREM level. Any *improvement* must beat the alternation-trading ceiling, which is OPEN.
