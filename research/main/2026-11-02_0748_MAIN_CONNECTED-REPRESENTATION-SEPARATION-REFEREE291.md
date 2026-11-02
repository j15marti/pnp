# LSPV-5 Formal Proof Red Team — CONNECTED-REPRESENTATION-SEPARATION-REFEREE291

**Run time:** 2026-11-02 07:48 PST  
**Status:** PROVED/EXACT RESTRICTED, independently reproduced; no universal lower bound.  
**P versus NP:** OPEN.  
**Task identity, enabled state, hourly Pacific stagger, role ownership, and schedules:** unchanged.

## Exact obstruction

The same connected canonical original can have exponentially many exact fixed-cut continuation states while its SAT-existence bit is computable after paid source recognition by a constant-width existential boundary summary. Therefore a forward/reverse full-function rank, OBDD, antichain, or evaluator-size lower bound does not transfer to necessary SAT-decision work without a separately proved representation-to-arbitrary-machine theorem.

The target remains only valid duplicate-free proper Döcker monotone 3-SAT-(2,2) originals. Malformed strings are rejected. Pinned residuals and circuits are controls, not canonical children.

## Falsifiers

1. **F1 — connectivity kills product growth.** Falsified. For the connected cyclic F9-splice originals \(G_t\), fixing every splice variable \(x_{5,i}=0\) exposes \(K^{\otimes t}\), and an explicit rank-nine minor proves \(\operatorname{rank}_{\mathbb F_2}M_t\ge 9^t\).
2. **F2 — exponential exact continuations force hard SAT decision.** Falsified on this family. The exact dominance frontier is \(10^t\), yet a paid \(2\times2\) Boolean-support transfer decides every coherent pinned residual by Boolean-semiring multiplication.
3. **F3 — the bad order is intrinsic.** Falsified finitely on the same connected \(G_2\): reduced OBDDs have 1132/1373 nodes in the two prescribed bad orders but 204/229 in natural/fully reversed orders.
4. **F4 — a one-bit answer circuit proves cheap source decision.** Rejected. After the answer is acquired, a constant 0/1 circuit is trivial; source grammar, family recognition, semantic-summary acquisition, proof/witness checking, and output remain charged. Conversely, the 35-gate F9 evaluator and large OBDD do not prove hard decision.

## Restricted theorem independently proved

Let \(G_t\) be \(t\ge2\) renamed F9 blocks with the positive clause \((x_{1,i},x_{5,i},x_{6,i})\) changed to \((x_{1,i},x_{5,i+1},x_{6,i})\), cyclically. This preserves every two-positive/two-negative quota, proper monotone triples, duplicate freedom, and makes the source incidence graph connected.

For the cut \(A_t=\{x_{1,i},x_{2,i},x_{3,i},x_{4,i}\}\), \(B_t=V\setminus A_t\), the full truth matrix has rank at least \(9^t\). The independent producer and verifier reconstructed the rank-nine seed and the published minor rows
\((1,3,4,5,6,9,11,12,13)\) and columns \((2,3,4,5,7,8,9,10,14)\).

For every coherent pin map \(p\), define the paid exact existential continuation table
\[
S_i^p(u,v)=1 \iff \exists\text{ private assignment of block }i
\text{ satisfying its twelve source clauses under }p,x_{5,i}=u,x_{5,i+1}=v.
\]
Then
\[
\operatorname{SAT}(G_t\mid p)=1
\iff \operatorname{tr}_{\mathbb B}\left(S_0^pS_1^p\cdots S_{t-1}^p\right)=1.
\]
This follows by gluing adjacent boundary values around the cycle; each accepting product term is exactly a globally consistent choice of boundary bits with independent private witnesses, and every global witness induces one such term. The result is exact **decision continuation equivalence**, not equality of model counts or witness maps. Integer matrices \(W_i^p\) retain the paid exact count continuation when needed.

This Boolean support theorem was already present in project REFEREE270/QUOTIENT310 and the anonymous-cycle recognition theorem in REFEREE274. This run is an independent referee and integrated separation, not a novelty claim.

## Same-original and malformed controls

| Control | Exact result |
|---|---:|
| F9 grammar/models | valid / 70 |
| F9 circuit | 35 fan-in-two gates, depth 6, all 512 outputs equal CNF |
| F9 minimum/natural/maximum OBDD over all \(9!\) orders | 52 / 66 / 80 |
| F9 same-source pins \(x_2=x_3=0,x_6=1\), then \(x_1=0/1\) | 1 / 0 models |
| F9 SS/SU/US/UU feasible pair modes | 37 / 49 / 49 / 37 (264 total) |
| malformed original strings | 6/6 rejected |
| connected \(G_2\) grammar/models | valid, connected / 4614 |
| \(G_2\) evaluator | 71 gates, depth 7, all 262,144 outputs equal CNF |
| \(G_2\) bad cut | rank 184; 189 forward and 346 reverse cofactors |
| \(G_2\) OBDD orders | 1132 left-first; 1373 right-first; 204 natural; 229 fully reversed |
| dominance frontier \(t=1,2,3\) | \(10,100,1000\) |

On one connected \(G_2\) original, pins
\(p_U=\{x_8=1,x_6=0,x_1=0,x_{15}=0,x_{11}=0,x_{13}=0\}\)
give zero models with local count matrices
\(W_0=[[0,7],[0,7]]\), \(W_1=[[3,5],[0,0]]\) and zero Boolean trace.
Changing only \(x_6\) to one gives 38 models, matrices
\(W_0=[[6,6],[4,4]]\), \(W_1=[[3,5],[0,0]]\), and nonzero Boolean trace. The witness mask is 166066 and was checked against all original clauses. Thus both labels use the same canonical source; only the residual pin differs.

The F9 52-node value is the exact minimum only in the declared reduced ordered read-once branching-program model. The 35/71-gate circuits are explicit unshared CNF evaluators, not unrestricted circuit minima. Post-answer constant circuits are excluded from acquisition lower-bound claims.

## Full work and peak-space charge

For an authenticated \(G_t\), local support acquisition uses at most \(4\cdot2^8=1024\) boundary/private trials per block. Each trial checks twelve three-literal source clauses, so a direct ledger is at most \(36{,}864t\) literal tests plus boundary setup. Boolean \(2\times2\) multiplication is constant work per block. Source length is \(L=\Theta(t\log t)\).

\[
T_D \le C_{grammar}+C_{source/index/head}+C_{recognize}+C_{acquire/certify}
+C_{selector/failed/switch}+C_{BoolProduct}+C_{proof/cache/replay/output}
+C_{DELAY/COPY/RECOMP}.
\]

The direct recognized-family algorithm is polynomial total work. Peak writable space counts the simultaneously live source/index representation, recognition state, current private assignment, local table, running product, proof/witness, caches, and guests. A materialized implementation uses \(O(L)\) source/index space plus constant decision tables; the inherited anonymous-cycle implementation gives logarithmic writable recognition space under its declared access model. Delayed or recomputed guests are still charged even if logical XOR is zero.

Offline diagnostics are not free SAT-machine work. Measured producer phases were 1.485 s / 10,240 KiB peak RSS for F9 and 21.055 s / 279,484 KiB for G2; the no-import verifier used 6.926 s / 278,356 KiB and passed 20 assertions. The large RSS comes from exhaustive truth/BDD tables and is not the recognized-family decision cost.

## Exact remaining gap

The theorem covers a recognized connected family, not all valid target originals. It supplies no uniform polynomial-total-work controller for arbitrary canonical inputs, no universal arbitrary-decider \(A\mapsto\Phi(A)\), no power-short hereditary canonical-child construction, and no strict numerical **same-machine** transfer to the FLMV forbidden region. Fixed-order rank, OBDD size, antichain size, or evaluator gates do not fill any of these gaps. Treewidth DP, affine/Horn/2SAT recognition, gate sharing, alternate orders, source recognition, and DELAY/COPY/RECOMP remain admissible falsifiers of any proposed universal inference. P versus NP remains OPEN.

## Literature and repository search ledger

Primary queries included “Bryant graph-based algorithms Boolean function OBDD variable ordering communication matrix rank lower bound”, “Wegener branching programs binary decision diagrams communication complexity”, and “Fortnow Lipton van Melkebeek Viglas time space lower bounds satisfiability”. Sources found: Bryant, *IEEE Transactions on Computers* 35(8), 1986, DOI 10.1109/TC.1986.1676819; Wegener, *Branching Programs and Binary Decision Diagrams*, SIAM, 2000, DOI 10.1137/1.9780898719789; FLMV, *JACM* 52(6), 2005, DOI 10.1145/1101821.1101822; Döcker, arXiv:1912.08032. These support restricted OBDD/circuit or SAT time-space models, not the missing transfer.

Project GitHub queries: `CONNECTED_RANK_FORWARD_REVERSE_ESCAPE_GATE323`, `EXISTENTIAL_ANTICHAIN_TRANSFER_GATE324`, `DECISION_SEMANTIC_QUOTIENT310`, `DECISION-SUPPORT-TRANSFER-REFEREE270`, and `ANONYMOUS_CYCLE`. They located the prior rank, antichain, Boolean-support, quotient, and recognition results; the new run therefore makes no novelty claim. Searches scoped to `github.com/openai` for OBDD/circuit-SAT implementations found unrelated `openai/math` circuit material and no implementation used here. A general GitHub search found standard BDD libraries emphasizing order sensitivity; no external code was imported.

## Artifacts

- `experiments/review/lspv5_291/connected_representation_referee291.py`
- `experiments/review/lspv5_291/verify_connected_representation_referee291.py`
- `results/raw/review/2026-11-02_0748_LSPV5_CONNECTED-REPRESENTATION-SEPARATION-REFEREE291_raw.json`
- `results/raw/review/2026-11-02_0748_LSPV5_CONNECTED-REPRESENTATION-SEPARATION-REFEREE291_verify.json`

No tasks were created, rescheduled, enabled, disabled, or renamed.
