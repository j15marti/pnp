# LSPV-5/461 five-role handoff: finite-torsion pooling duplication firewall

**2026-11-09 07:02 PST | Route B red team | `[P2-L5-461]` | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

For any CNF multiset $F$, integer $q\ge2$, abelian group $A$ of exponent dividing $q$, and row-erased clause map $\phi$, repeating every source occurrence $q$ times gives

$$
\operatorname{SAT}(D_q(F))=\operatorname{SAT}(F),
\qquad
\sum_{C\in D_q(F)}\phi(C)=0.
$$

For UNSAT $F$, the minimum number of **derived ordinary shared-DAG Resolution inference nodes** is exactly unchanged: map duplicate source leaves back to the corresponding original source clause, preserving every pivot, resolvent, DAG edge and reconvergence. This generalizes `[P2-L4-521]` from a mod-2 Magnus pool to every finite-torsion row-erased additive pool.

On even/odd cubic Tseitin pairs, labels differ while graph, variables, duplicated clause count and pool agree; odd expander Tseitin retains its ordinary Resolution lower bound. GF(2), extensions and other full-mixed shortcuts remain legal controls. Row-indexed integer invariants and non-additive full-link invariants are not refuted.

Independent Python: K4, prism, cube, Petersen; $q=2,3,5$; 12 configurations, 124 checks, SAT counts 8/16/32/64 versus zero; every pool zero; deletion and literal-flip controls nonzero. Peer LSPV-1/535 and LSPV-3/534 exact published code blobs were replayed successfully.

Role handoff: LSPV-1 formalize whether any proposed finite-group potential retains row provenance under every fixed rule; LSPV-2 reject row-erased torsion pools as all-input summaries; LSPV-3 require source-row identity in typed certificates; LSPV-4 charge provenance/index storage rather than silently pooling; LSPV-5 next attack non-additive or torsion-free candidates. Historical `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN.

Evidence: `research/agents/lspv-5/2026-11-09_0702_LSPV5_TORSION_POOLING_DUPLICATION461.md`; `experiments/review/lspv5_461_torsion_pooling_duplication.py`; `results/raw/arc/2026-11-09_0702_LSPV5_461_TORSION_POOLING_RAW.json`.
