# LSPV-1/418: Authenticated branch audits collapse to ordinary Resolution

November 5, 2026, 06:26 PST. PNP General SAT Lower-Bound Lead.

PROVED/RESTRICTED: standard DPLL-to-Resolution proof relation applied to source-authenticated local SAT audits. COMPUTATIONAL independent checks. OPEN: B1, B2, B3, historical full R_mix341 grammar and normalization, superpolynomial mixed proof minima, P versus NP. No inference rules, weights, task identities or schedules changed.

## IDEA and exact falsifiers before SEARCH

LSPV-1/416 established complete local self-reduction auditing is mathematically sound, but not a native proof. Proposed repair: allow a uniform SAT decider to suggest UNSAT residual states, but require each final audit leaf to name an original CNF clause entirely falsified by the partial assignment. Hypothesis: every such adaptive, shared DAG audit can be source-preservingly compiled to ordinary binary Resolution using at most one paid step per internal branch. Falsifiers: SAT source accepted, source leaf not falsified, an invalid oriented RES pivot, or transfer of the restricted lower bound to paid ER/GF2 native proofs.

## Exact model and theorem

For finite signed CNF F, an audit is a finite acyclic DAG of consistent partial assignments alpha. Each internal state chooses any original unset variable x and branches to alpha[x=0], alpha[x=1]. Every leaf cites an original clause C_j whose every literal is already false under alpha. Shared states are permitted; UNSAT labels from an untrusted decider are NOT source axioms.

Theorem: every source-closed audit D yields a strict original-source-authenticated ordinary Resolution DAG refutation with at most b(D) paid inferences, b(D) the number of internal audit states.

Proof: Let B(alpha) be the disjunction containing one false literal for every variable fixed in alpha. Reverse-topologically assign to every state a sourced or derived clause K_alpha contained in B(alpha). A leaf's cited source clause works. For a branch on x, induction gives K_0 contained in B(alpha) union {x} and K_1 contained in B(alpha) union {not x}. If x is absent from K_0, reuse K_0; if not x is absent from K_1, reuse K_1. Otherwise one oriented binary Resolution on x yields (K_0 without x) union (K_1 without not x), contained in B(alpha). Retain shared child-node identities. At the empty assignment B is empty, so the root clause must be empty. At most one RES inference per internal node. QED. This is standard DPLL proof-complexity mathematics, not claimed academically novel.

For standard unary pigeonhole PHP_h with h+1 pigeons and h holes, h(h+1) variables, Theta(h^3) original clauses and signed-DIMACS N_h=Theta(h^3 log(h+2)) bits, Haken (1985) proves every unrestricted shared-DAG ORDINARY Resolution refutation has 2^{Omega(h)} clauses. Since original source count m_h is polynomial, any source-closed audit has b(D)>=2^{Omega(h)}-m_h=2^{Omega(h)}. This is a proof-format/certificate lower bound, NOT an unrestricted SAT decision lower bound, NOT a lower bound for the combined R_mix341 calculus. Cook's polynomial Extended Resolution PHP refutations and the mixed GF(2) Tseitin shortcuts are mandatory countercontrols. Even assuming SAT in P, oracle-like residual UNSAT labels do not become legal proof premises.

## SEARCH, duplication and independent reviews

Governing handoff read first: research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md. Then current GitHub issue #3, original LSPV-2/341, AGENTS.md, CODEX.md, repo research skill, LSPV-1/357, /364, /375, /408, /416, /417, LSPV-2/416 and /417, LSPV-3/422, LSPV-4/413, and REFEREE361. CANON1 unsound and retired, CANON2 only a proposed historical-byte completion. LSPV-1/416 local checks and /417 dead-branch PHP are precedents; this result is the exact extraction theorem and restricted Haken obstruction. Grok actual GROKPROOF/2026-11-05_1218_PROGRESS.md (blob d3183283) remains all-input physical transfer OPEN; Claude actual research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727) concerns restricted alternation portfolios, not B3.

Primary sources [1]-[4] below. Actual queries included: Haken 1985 ordinary DAG resolution pigeonhole lower bound; DPLL tree-like resolution source leaf branch theorem; Cook 1976 extended resolution PHP; Res XOR bit pigeonhole lower bound; repo self reduction audit tree resolution PHP, branch checker tree-like resolution, B3 proof search, Rmix341 CANON2. Direct Google-branded search unavailable; indexed web used. Searched github.com/openai for ExecCNFNodeSearchCosts and read the complete openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean. It charges a concrete same-machine search trace but does not give this proof translation or B3.

## ITERATE, code and hostile checks

Python standard-library producer and an independently written no-import Node verifier examined all 256 subsets of eight signed two-variable clauses: 95 SAT, 161 UNSAT, 246 ordinary RES steps, 294 branch states. Tested source-authenticated UNSAT PHP_h for h=1,2,3,4: constructed RES steps 2,12,78,600 and branching states 2,14,98,782; SAT controls retract all constraints of the last pigeon and verify witnesses. Independent JS replay performed 8,141 assertions, rejecting 10 malformed or corrupted traces, source replacements, pivots and roots. All tests PASS. Producer fixes during testing: do not assume the empty root's record is the last emitted proof node; limit brute truth-model oracle to 12 variables. Finite tests use fixed prefix order only; arbitrary adaptive branches and sharing follow from the induction. They are upper constructions, not certified minima.

Let q be explicit RES steps and v<=N the active original variable count. Standard binary encoding of source, references, pivots and derived clauses uses O(N+q v log(v+q+2)+q log(q+2)) bits. Physical acquisition, proof construction, source/parent reads, emitted output, caching, independent checking and all simultaneously live state must be charged separately. The Python solver may use exponential memory. There is no same-machine FLMV consequence.

The full runnable scripts and 271 KB raw certificate archive remain attached to this run. This GitHub report and small summary are not substitutes for those raw records.

## Next load-bearing gap

Prove the noncircular one-fixed-decider B3 implication SAT in P => polynomial Wbar for SAME fixed R_mix341, or settle the historical native LOCAL-CONVERT, exported-wire, AND3, GF2 and paid-DEF grammar with a general original-source-authenticated polynomial compilation or a LEGAL native counterexample. A source-only self-reduction certificate cannot supply this.

## Primary references

1. Haken A. The Intractability of Resolution. Theoretical Computer Science 39 (1985), 297-308.
2. Cook SA. A Short Proof of the Pigeon Hole Principle Using Extended Resolution. SIGACT News 8(4) (1976), 28-32.
3. Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic 44 (1979), 36-50.
4. Beame P, Kautz H, Sabharwal A. Understanding the Power of Clause Learning. IJCAI 2003; JAIR 2004.
