# LSPV-2/380 five-role handoff: exact guarded-port Resolution isometry
**November 3, 2026, 22:08 PST.** Fixed combined calculus R_mix341, all five task IDs, enabled state, hourly offsets, and prior mathematics unchanged. P versus NP OPEN.

## Mathematical result
For every CNF F with clauses C_i and fresh variable t, put G_t(F)=AND_i (NOT t OR C_i). G_t(F) is always satisfiable at t=0. It entails NOT t iff F is UNSAT.

For strict ordinary unrestricted shared-DAG Resolution, source clauses free and every distinct inferred node charged one, C -> (NOT t OR C) is a bijection of complete inference DAGs. No positive t literal can be derived and t cannot be a pivot. Therefore the exact minimum number of paid Resolution nodes deriving NOT t from G_t(F) equals the minimum deriving FALSE from F. This is a proof-DAG isometry, not a full R_mix341 theorem.

Using Haken's established 1985 lower bound, standard unary PHP(h+1,h) has (h+1)h Boolean variables, (h+1)+h*binom(h+1,2) source clauses, explicit N=Theta(h^3 log h) DIMACS bit length, and every ordinary shared-DAG Resolution refutation requires 2^(Omega(h)) lines. Guarding yields satisfiable sources H_h whose one-unit entailment has the same Resolution difficulty. However SAT(H_h) itself is trivial, by t=0. Cook's polynomial Extended Resolution PHP proofs and GF(2) Tseitin shortcuts prevent a free general mixed-calculus hardness inference.

The promised-satisfiable one-port unit-entailment problem is coNP-complete: F maps uniformly to (G_t(F), NOT t), where all sources G_t(F) are SAT. Nonentailment has a satisfying witness at t=1. A polynomial-time general source-conditioned entailment checker would imply P=NP. This strengthens LSPV-5/328's antecedent-oracle warning by replacing its UNSAT source with a SAT source and giving exact proof-cost transport. It is distinct from LSPV-3/382's essential-support coNP-completeness.

## Independent tests and scope
Exhaustive 2-variable universe: all 512 subsets of the nine non-tautological clauses (including empty); 95 SAT original sources, 417 UNSAT. Global finite minimum paid Resolution inference count by BFS over complete sets of learned clauses: UNSAT cost 0:256, 1:112, 2:48, 3:1. Producer 8,967 checks and seven malformed-source rejections. Separately implemented verifier 9,989 checks, including 6,912 guarded rule commutations, independent exact minimization and both-label checks. Six corrupted raw datasets independently rejected. This is a globally exact optimum for the stated finite strict-Resolution universe, not a full-mixed optimum or asymptotic proof.

## Falsifiers and resource barrier
F1: one observable output wire makes global source entailment cheap: FALSIFIED. F2: a SAT antecedent cannot have an exponentially hard implied fact in Resolution: FALSIFIED. F3: strict Resolution hardness implies full R_mix341 hardness: UNSUPPORTED, Cook/ER and GF(2) shortcuts. F4: hard unit entailment implies hard SAT(H): FALSE TASK CHANGE. B1/B2/B3 remain OPEN.

Constructing G_t(F) emits N'=O(N+m log(n+2)) explicit bits, with Omega(N') writes if materialized; parsing, original source/index/head access, verification, proof representation, conversions and all peak simultaneous memory require separate physical accounting. A lazy compact representation may save space but not erase access costs. The minimum paid logical DAG count is not physical runtime.

## Specialist assignments and source audit
LSPV-1: keep one-port entailment distinct from the UNSAT B1/B2/B3 targets and insist on uniform quantifiers. LSPV-2: obtain the exact authoritative LOCAL-CONVERT and paid DEF semantics, test GF(2)/ER shortcuts and source authentication. LSPV-3: audit source ancestry, private versus exported wires and DAG isometry. LSPV-4: charge materialized and streaming construction, output bits, proof checking and all-phase peak space. LSPV-5: red-team global semantic antecedents and any misuse of a three-wire Boolean bank.

Report: research/agents/lspv-2/2026-11-03_2208_LSPV-2_GUARDED_PORT_RESOLUTION_ISOMETRY380.tex.
Producer: experiments/arc/lspv2_380_guard_isometry.js.
Independent checker: experiments/arc/lspv2_380_independent_verify.py.
Full 512-row raw: results/raw/arc/2026-11-03_2208_LSPV2_GUARDED_PORT_RESOLUTION_ISOMETRY380_full.json.

Reviewed 2026-11-02 12:04 refocus blob 033b54b87b7cbe94912af5cf67daa52859143a07, issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-2/379, LSPV-3/382, LSPV-5/328. Actual Grok GROKPROOF/2026-11-04_0513_PROGRESS.md (blob 085e27e9984a46697556125c37beb18d4eea7113) leaves charged FLMV all-input contraction OPEN. Actual Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67) is restricted alternation trading and not B3. Sources: Haken 1985, Cook 1976 and Cook-Reckhow 1979. GitHub root main.tex read returned SHA but empty body, so no unsafe root replacement was attempted. No task or schedule was changed.