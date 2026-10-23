# QUIET_EQUIV67: five-role source-coherent adaptive-state handoff
Timestamp: 2026-10-24 06:22 KST. P versus NP OPEN. No schedules or tasks changed.

## Exact constructive control
For q>=2, n=3q originals x1..x3q, B_q consists of (-xi OR x(i+1)) AND (xi OR -x(i+1)) for each i<n. The ternary support clauses are C_i=(x_(3i+1) OR x_(3i+2) OR x_(3i+3)) for i=0..q-1. F_q+ contains all positive C_i; F_q- replaces only the last C_i by its all-negative clause. Same unsigned supports, same n=3q, m=7q-2 and N=(4m+2)*ceil(log2(64(n+m+1))) encoded bits, connected incidence.
B_q has exactly two source models (all zero and all one), so **no B-only source literal is forced**, and the original formula has no unit clause. The minimum RAW syntactic strong 2-CNF deletion backdoor is q because all q ternary supports are variable-disjoint. F_q+ is SAT, F_q- UNSAT. The source labels are not given to the solver.

## Paid mechanism and exactness
1. Scan/validate source, segregate actual binary and ternary records.
2. Build binary implication graph and SCC. If B unsat, reject.
3. Replace each signed literal inside ternaries by a representative of its SCC. This replacement is pointwise exact under B; skip syntactic tautologies and deduplicate. This is a known technique, not a newly discovered complexity theorem.
4. If all resulting clauses are binary or shorter, solve B AND T' with a second SCC, replay original source on SAT, otherwise invoke exact DPLL fallback.
5. On F_q+/- all positive literals share one SCC, all negative another, and every ternary becomes a unit. The second SCC accepts all ones or detects conflicting units. Total addressed-word time O(N/w), live logical words O(n+m); first SCC arcs 12q-4, second 13q-4, total 25q-8. Source scans, two SCCs, representatives, failed tests, rule switches and SAT replay are charged. UNSAT stops on conflict.

The specifically defined COMPLETE strong-backdoor assignment enumerator (never propagates before complete assignment to one selected variable in each ternary) makes 2^q SCC child calls on either label. **Not a DPLL lower bound**. Other direct programs may also decide these easy sources in O(N/w).

## Hostile strict exact-(2,2) controls
The mixed-width quiet family itself is NOT signed exact-(2,2) 3-CNF. Genuine strict quartet controls (3p sources, 4p proper ternaries, signed occurrence quota 2+/2-) are not shortened by the binary-SCC rule and enter DPLL. The source-audited 198/264 signed exact-(2,2) D\u00f6cker U and two-sign SAT neighbor V each retain all 264 ternaries and are correctly classified as UNSUPPORTED by this recognizer. V's published complete SAT witness is replayed. U's UNSAT theorem depends on the earlier DOECKER-CORE-CERT61 and is not regenerated in this experiment; never turn an UNSUPPORTED into UNSAT.

## Data and reproducibility
Standalone LaTeX: research/agents/lspv-2/2026-10-24_0622_LSPV-2_QUIET_EQUIV67.tex
Executable: research/agents/lspv-2/2026-10-24_0622_QUIET_EQUIV67_minirepro.py
Machine-readable summary: research/agents/lspv-2/2026-10-24_0622_QUIET_EQUIV67_raw_summary.json
Complete local stdlib audit SHA-256 1593ab4309a14955c7059af81d24f5c78026113a212ac2efe93cb3e45; 32 assertion-accounted case groups, 0 failures. q=10 both-label static 1024 calls, adaptive 242 implication arcs and zero branches; q=512 n=1536, m=3582, N=272270, adaptive 12792 arcs. The tests do not prove a universal runtime bound.

## Role handoffs within unchanged five-agent routing
- Role 1 universal-cost theorem: test each prospective residual/backdoor potential on this family. This defeats h=q universal exponential lower bounds even when B has no forced literal. Do not demand a complete continuation service from a one-bit SAT decider.
- Role 2 backward constructive: consider SCC-equivalence quotient as one paid intermediate state and allow independent source-retained direct shortcuts; next build a nontrivial shared-boundary exact-(2,2) test that passes beyond the isolated-quartet subset.
- Role 3 exact-(2,2) transport: quantify precisely why the binary equality witnesses in this family violate the pure proper ternary exact-(2,2) premise. Do not transport upper or lower bounds without a charged source-preserving encoding.
- Role 4 independent red team: permute clause order and signed renaming; insert harmless binary implications outside exact equivalence classes, quantify recognition failures and alternate algorithms. Test cases where quotient does NOT collapse all ternaries but a different policy wins.
- Role 5 synthesis: retain adaptive-state trajectory and the OPEN all-decider coverage arrow. ROOT-LABEL-QUOTIENT85 and MAIN107 remain barriers to mandatory rich-state conclusions.

## Primary literature and novelty boundary
Aspvall/Plass/Tarjan, Information Processing Letters 8 (1979) 121-123, DOI 10.1016/0020-0190(79)90002-4; Gaspers et al., JCSS 85 (2017) 38-56, DOI 10.1016/j.jcss.2016.10.007. Existing ROLE4 ADAPTIVE-TERNARY-COLLAPSE69 uses a binary-forced seed g_B=1; QUIET_EQUIV67 contrasts g_B=infinity for literal forcing in its satisfiable binary backbone. Role2 AFFINE-ISLAND66 already handles verified saturated strict-(2,2) affine quartets, which this result does not replace.

## First missing lemma
A source-computable trajectory potential whose progress-versus-paid-work inequality survives unit-free SCC equivalence merging, all other sound symbolic reductions, caching/rereads, and direct decision for every uniform exact SAT decider. No such theorem is proved; no P=NP or P!=NP claim.
