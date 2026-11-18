# TRACEMOVE-SIGMA2-1 | 2026-11-17 22:53 PST

**PROVED/EXACT (scoped):** unique trace relocation is Sigma_2^P-complete and constant trace relocation is coNP-complete. **COMPUTATIONAL:** 134,144 exhaustive/seeded assertions, 0 final failures. **OPEN:** all-input hereditary A -> Phi(A), P versus NP.

## PROPOSE before searching
1. Relocate uniquely determined post-universal Tseitin traces to earlier existential blocks.
2. Prune universal dependencies using a source-checkable syntactic fanin certificate.
3. Certify extra semantic independence by solver-guided quantifier reasoning.
4. Audit parent-sized solver calls, source replay, encoding, FLMV machine space, and hereditary shrinking.

## SEARCH: repository and literature
Read prior project AFFINECERT_PI2_1, GRAPHPAIR_SHARE1, BLOWUP_BUDGET_1, SIGMA23_ODDWHEEL_SUBSET_FIREWALL and GATEAUDIT1. These already distinguish source-free information from source-backed decision cost, globally committed witnesses from local strategies, and true shrinking recursion from answer-only erasure. Primary literature: Choudhury/Mahajan, Journal of Automated Reasoning 2024 (https://doi.org/10.1007/s10817-024-09707-4); Fortnow/Lipton/van Melkebeek/Viglas JACM 2005 (https://doi.org/10.1145/1101821.1101822); Williams STOC 2024 (https://doi.org/10.1145/3618260.3649723); Wrathall 1976 (https://doi.org/10.1016/0304-3975(76)90062-1). The FLMV original PDF's machine description (p. 4) and Corollary 5.8 (p. 18) were visually checked.

## Theorem 1: Sigma_2^P-complete relocation of a uniquely determined trace
Given an ordinary acyclic Boolean circuit g(x,y), let
 Q_after(g) = exists x forall y exists z [z <-> g(x,y)];
 Q_before(g) = exists x,z forall y [z <-> g(x,y)].
Q_after(g) is TRUE for all g, with UNIQUE post-universal z=g(x,y). Deciding whether Q_before(g) is TRUE is Sigma_2^P-complete.

Membership: Q_before has a Sigma_2 prefix with polynomial-time matrix.
Hardness: from arbitrary Sigma_2 circuit QBF exists x forall u F(x,u), append a fresh universal s and put g_F(x,s,u) = NOT s OR F(x,u). When s=0, global z is forced to 1. When s=1, it equals F(x,u) for all u. Thus Q_before(g_F) iff exists x forall u F(x,u). The reduction adds one universal bit and O(1) Boolean gates.

This identifies the hidden computational obligation in moving a deterministic, uniquely forced gate trace before the challenges. It does NOT show that such a test is superpolynomial under P=NP.

## Theorem 2: coNP-complete single-bit constancy
For a circuit g(y), asking whether exists z forall y [z <-> g(y)] holds is coNP-complete. Nonconstancy has two explicit contradictory inputs, so is in NP. Reduce UNSAT(F(u)) by g_F(s,u)=s AND F(u). g_F is constant iff F is unsatisfiable. The original forall s,u exists z [z <-> g_F] is always TRUE with a unique z.

## Safe restricted positive rule
If a gate's acyclic transitive fanin excludes the universal y bits, the gate defines z=g(x), independently of y. For any downstream H(x,y,z), both
 exists x forall y exists z [(z=g(x)) AND H(x,y,z)]
and
 exists x,z forall y [(z=g(x)) AND H(x,y,z)]
have the same truth value by substitution. Structural fanin absence is a sound, syntactically checkable sufficient condition. It is not necessary: (s AND f) OR ((NOT s) AND f) equals f despite its syntactic s dependency. The fanin graph, rewritten circuit, guest input, and all memory must be charged.

## Computational falsification
Dependency-free standard-library Python checked all 65,536 tables of F(x1,x2,u1,u2); 14,911 Sigma_2 instances were TRUE, precisely matching Q_before, and all Q_after were TRUE. Checked all 256 F(u1,u2,u3) tables against CONST-TRACE/UNSAT; 900 random AND/OR/NOT gate DAGs with 300 explicitly reconvergent syntactic-but-not-semantic s dependencies; padding, source replay, and an adaptive unique-witness QBF whose illegal quantifier reorder flips truth. Checked exact rational FLMV arithmetic and parent-sized delayed guest slopes. **134,144 assertions passed, 0 failures.** An initial test-harness failure was repaired: a purported s-independent sub-DAG inadvertently depended on s; the actual theorem was not affected.

## Same-machine resource ledger and handoff
Assuming P=NP, choose arbitrary fixed correct polynomial Circuit-SAT decider A with time K and space L. The requested all-input hereditary map remains K' <= max(11/10, 3/5+K/2), L' <= max(1/2,L/2). Syntactic substitution can retain a Theta(N)-size parent, and a literal reached Theta(N)-size A_D call incurs Omega(N^D), violating the target for integer D>=2. A code-aware compiler could bypass such a call, so this is only a literal-call architecture falsifier.

The desired recurrence's fixed point is (c,d)=(6/5,1/2). FLMV Cor. 5.8 gives beta(6/5)=23/45, hence beta(6/5)-1/2=1/90>0. A contradiction would require a real all-input/hereditary shrinking compiler and a near-linear same-model SAT encoding transfer, with actual input-index and work-tape-position charges, no hidden parent-scale guest decision, no free universal splitter, no automatic exponent reduction from PH collapse. These remain OPEN.

Next: require any proposed trace/dependency compressor to correctly classify g_F=NOT s OR F(x,u), then check source-backed GRAPHPAIR, odd-wheel critical cores, AFFINECERT, arbitrary delayed/interpreter deciders, reconvergence, strategies, strict child sizing, recursive eligibility, and GATEAUDIT1 answer-only erasure. No root proof tracker or other agent schedule changed.

Reproducibility: local ZIP TRACEMOVE_SIGMA2_20261117_2253PST_bundle.zip contains REPORT.md, HANDOFF.md, audit.py, results.json, SHA256SUMS.txt.

FINAL_VERIFICATION_SENTINEL_TRACEMOVE_SIGMA2_1_20261117_2253PST
