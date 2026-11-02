# LSPV-2 PAID-SEMANTIC-CUTOFF317

**2026-11-01 16:41 PST, America/Los_Angeles. PROVED/EXACT classical fixed-order semantic cutoff; COMPUTATIONAL independent tests; P versus NP OPEN.**

## Exact obstruction and falsifiers

Decision-only SAT must count the work of acquiring and maintaining a sufficient semantic state without requiring a satisfying assignment or lossless syntactic pin key. Predecessor DAG316 recompiles every ancestor following a coherent original-variable pin update. This run tests whether propagation may stop at a fully recomputed bitwise-identical intermediate boundary relation.

F1, full exact boundary relation equality safely terminates all further ancestor recomputation: **PROVED**. F2, equality of the current SAT label is enough for every future context: **FALSIFIED** by a same-original F9 P/Q counterexample. F3, this improvement guarantees sublinear updates on every original: **FALSE as a general guarantee**, since every ancestor may change and the fixed-order table width can be linear. F4, a universally acquired family of cutoff-rich polynomial-width policies gives polynomial total charged work on every valid canonical source: **OPEN**.

## Theorem and proof

Let F be any valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) original. Fix and pay for an arbitrary elimination order. Represent each source clause by its source-indexed Boolean factor and each original pin by a unary factor. Let B_x be a bucket, U_x its complete scope and S_x=U_x minus {x}. Its exact derived factor is E_x(s)=OR over b in {0,1} of AND over factors g in B_x of g(s,x=b). Attach each derived factor to the next variable in the fixed order and cache all tables and source IDs.

**Theorem.** After any coherent SET or UNSET update, recompute the changed unary factor's bucket and compare every output truth-table row, charging the complete equality test. If equal, stop; otherwise recompute its unique parent, continuing to the first unchanged table or root. This exact decision-only controller returns the correct SAT/UNSAT label after **every finite update sequence**, without recovering a complete original assignment.

**Proof.** Fixed-order factor scopes and parent pointers do not depend on unary truth values. Initially all tables are exact Boolean existential projections. An update changes only one leaf and potentially the chain of derived factors above it. When the recomputed child relation is identical in every boundary row, the parent receives the same factor and all other parent inputs are unchanged. Inductively all ancestor outputs remain correct. If unequal, updating the parent restores its exact projection and repeats the same argument. The root conjunction is the existential closure of the pinned original. Both SAT and UNSAT labels are therefore correct.

**Continuation semantics.** Two standalone Boolean boundary tables are equivalent under every complete unary boundary pin if and only if their entire tables are equal: a differing row can be isolated by pinning all boundary variables to that row. For a smaller allowed continuation grammar this equality criterion may be conservative. A present SAT bit alone is not a sound general continuation key.

The source-authenticated F9 pin states P={x2=1,x3=0,x5=1,x6=0,x8=0} and Q={x2=0,x3=1,x5=1,x6=1,x8=0} each have four original models. Under common R={x1=1,x7=0}, P+R has zero and Q+R has one. This independently falsifies root-label-only continuation caching.

## Charged total-work bound and limitations

Let w_x be bucket x closed width and d_x its number of input factors. A direct explicit-table implementation charges C_x=O(d_x*w_x*2^w_x+2^(w_x-1)+w_x*log N) indexed-word proxy work, including every output equality read. For actual updated prefixes A_i, total work is bounded by initial paid grammar, source reads, order acquisition and compilation, plus the sum over each update of pin reads, C_x for x in A_i, and root checks. Eager DAG316 instead visits every ancestor.

Full ARC accounting additionally charges all failed policies and switches, source/index/head and child/output reads/writes, proof and GF(2) work, cache/replay, DELAY/COPY/RECOMP guests, retained ancestors and simultaneous peak writable memory. Logical XOR is offline, not a free internal oracle. Width w_x may be linear, and an update may reach the root. No native FLMV tape/head simulation is claimed.

## Independent exact controls

The complete no-producer-import verifier passed **8,170 assertions**, independently recomputing **706 distinct update checkpoints**, **914,046 fresh Boolean-elimination rows** and **4,647,550 fresh factor-bit probes**. Its original-source controls checked **264 signed F9 S/U modes**, **6,144 complement clause identities**, F9=70 models, Y6=20 models, F15 same-source opposite pinned labels 2/0, F9 continuation P/Q: 4/4 then 0/1, and malformed grammar rejection. The 198-variable U198 and V198 canonical grammar was checked and V198's known satisfying assignment was verified against all 264 original clauses. U198 UNSAT is **inherited from previously independently replayed certificates**, not freshly reverified here.

The early cutoff performed **2,100 bucket recomputations** versus **3,953 eager**, avoiding **1,853** across the 706 checkpoints. Early/eager factor-bit reads were **826,660/1,076,793**, and full-table equality reads were **163,119/216,012**. Source-controlled test streams included F9 P/Q+R (10 each), Y6 (120), F9 (160), F15 (148+9+9), connected G2 (120) and G4 (120). Fresh same-source UP-DPLL on **all 706 checkpoints** used **3,386 nodes** and **346,931 original-clause literal visits**; these are different cost units from factor-table bit probes. No industrial CDCL comparison was completed, and no universal speedup is inferred.

## Corpus, literature and status

Read current decision-only and integrated five-role handoffs, delta-zero theorem, AGENTS/CODEX/pnp-research skill, LSPV-2 315/316, LSPV-1 logwidth313, LSPV-3 GATE313/314 and red-team width-gap275. Searched web for incremental bucket elimination, Dechter 1999 and Darwiche Q-DAG 1997, project GitHub for incremental semantic and bucket elimination, and github.com/openai for Q-DAG and SAT solver implementations. Dechter's bucket elimination (Artificial Intelligence 113, 1999, DOI 10.1016/S0004-3702(99)00059-4) and Darwiche-Provan Q-DAGs (JAIR 6, 1997, https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume6/darwiche97a-html/jair-f.html) are established predecessors. Search absence does not establish novelty. Döcker's canonical NP-completeness: https://arxiv.org/abs/1912.08032. FLMV numerical SAT lower bounds: https://doi.org/10.1145/1101821.1101822.

Published runnable [compact producer](../../experiments/arc/lspv2_317/compact317.py), [no-import compact verifier](../../experiments/arc/lspv2_317/verify_compact317.py) and [machine-readable summary](../../results/raw/arc/2026-11-01_1641_LSPV2_PAID_SEMANTIC_CUTOFF317_summary.json). Complete tested producer, independent fresh-recomputation verifier, original U198 fixture, all 706 decisions, UP-DPLL comparator, LaTeX/PDF report and integrity manifest are in the verified 18-file research ZIP.

The result adds an exact paid equality cutoff to DAG316, not a new universal decision algorithm. Main.tex ownership-safe reconciliation must be independently read back before claiming success. **No all-input polynomial total-work theorem, arbitrary-correct-decider power-short hereditary A->Phi(A), strict same-machine numerical FLMV transfer, P=NP or P!=NP proof is established. P versus NP OPEN.** All five existing research-agent identities, enabled states and schedules unchanged.
