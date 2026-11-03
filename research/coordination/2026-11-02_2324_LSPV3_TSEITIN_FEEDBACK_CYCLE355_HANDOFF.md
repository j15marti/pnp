# LSPV-3 TSEITIN-FEEDBACK-CYCLE355 | November 2, 2026, 23:24 PST

**PROVED/EXACT graph theorem, unchanged Rmix341 and source-independent VARDEF interpretation; COMPUTATIONAL independent finite checks. B1/B2/B3 and P versus NP OPEN.** No changes to identities, schedules, enabled states, source accounting or preselected calculus.

## New exact backdoor theorem

For every finite connected cubic graph G=(V,E) with odd parity charge, let F(G) be its canonical width-exactly-three Tseitin clause encoding (four signed clauses per vertex). A set B of edge variables makes unit propagation refute **every** restriction F|alpha for alpha on B if and only if the residual graph G-B is a forest. Therefore

$$
b_{UP}(F(G))=|E|-|V|+1.
$$

Proof: UP is leaf elimination on the residual parity graph. A forest always has some inconsistent tree component because the total remaining charge stays odd under arbitrary fixed edges. If any cyclic component survives, choose the fixed-edge values to make all tree components consistent, using independence of a proper subset of incidence-matrix rows of the connected quotient graph. Cyclic components then retain a nonempty 2-core and UP cannot refute. This proof covers **all** variable sets and assignments, not only a heuristic search.

If G is also 2-vertex-connected, every original source is indispensable: any forbidden pattern at v extends to a satisfying solution on G-v, giving a SAT witness for deletion and every occurrence-sign flip. Binary proof-ancestry yields W_R>=4|V|-1. Three supported AND3 deductions at each vertex, local affine aliases and |V|-1 GF(2) combinations give W_R<=4|V|-1 in unchanged Rmix341. Hence **exact global mixed minimum W_R=4|V|-1** including adaptive DAG sharing and conservative extensions.

For growing prism graphs G_r=C_r x K_2, r>=3, source bit length N=Theta(r log r), **b_UP=r+1=Theta(N/log N)** but **W_R=8r-1=O(N)**. This retires growing UP-backdoor size as a sufficient predictor of hard mixed proofs. It is a FAMILY FAILURE, not evidence against worst-case B2/B3.

## Finite controls and artifact status

K4, prism3, prism4: exact UP backdoors 3/4/5; exact paid mixed nodes 15/23/31; deleted clauses SAT 16/24/32; sign-flip SAT controls 48/72/96; matched even-charge SAT model counts 8/16/32 and odd-charge UNSAT. Every one of 22/130/794 smaller-variable subsets has a nonrefuting assignment and every assignment to an exhibited minimum feedback set refutes. Independent Python producer + no-import Node referee passed 4,548 assertions; standalone published Node reproducer 39,260 assertions. Malformed DIMACS and forged typed parity proof tests rejected.

Logical node counts, explicit source bits, proof JSON bytes, verification work and optimizer discovery were recorded separately, with no machine time-space lower bound. Source bytes 163/239/340; proof JSON bytes 1426/2135/2868. The same machine all-phase peak-space envelope and its full rho remain applicable.

## Corpus and next gap

Read 12:04 directive, issue #3, AGENTS/CODEX/skill, current root main blob, previous mixed Tseitin341/342/345 and UP354, LSPV1 backdoor354/355, LSPV4 cycle slack353 and LSPV5 affine-minimality306. Original classical backdoors and Tseitin are credited. This theorem adds the exact feedback-edge/UP characterization, not a novel GF2 mixed upper bound. Peer roles should try the same graph-quotient invariant in genuinely **nonaffine** gadget families, and reject any invariant that is defeated by paid local affine aliases or conservative definitions. Separately prove B3 for the same fixed R.

## Verified outbox

- [Formal report](../agents/lspv-3/2026-11-02_2324_LSPV-3_TSEITIN_FEEDBACK_CYCLE355.tex)
- [Standalone Node reproducer](../../experiments/arc/lspv3_355_feedback_compact.js)
- [Raw numeric control ledger](../../results/raw/arc/2026-11-02_2324_LSPV3_TSEITIN_FEEDBACK_CYCLE355_public.json)
- Local full producer, independent referee, witness-rich JSON and reproducibility archive available as a conversation artifact.

No root manuscript material outside LSPV-3 ownership may be changed. P versus NP remains OPEN.
