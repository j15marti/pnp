# LSPV-4 366: fully clocked reflection specialization is a separate resource obligation

November 3, 2026, 10:36 PST. **PROVED/EXACT in stated clocked source-selector model; full Rmix341 B3 OPEN.** No task, schedule, identity, rule, weight or access change.

## Established theorem and why transfer is missing

Haken's 1985 result gives $2^{\Omega(h)}$ ordinary DAG Resolution lines for the canonical signed pigeonhole CNF (ASCII encoded length $\Theta(h^3\log h)$). Buss's short Frege proofs and paid Extended Resolution already prevent using that bound against the full Rmix341 directly. Odd Tseitin GF(2) shortcuts remain mandatory countercontrols. No arbitrary SAT-machine lower bound follows.

For a fixed total correct decider A, the bounded rejection-soundness CNF $H_{A,N,b}=V_N(x,y)\land\mathrm{Reject}_{A,b}(x,z)$ is UNSAT by **external correctness** of A. A rejecting trace alone is not correctness evidence. Existing LSPV-1 367 supplies a strict-Resolution witness-transparent one-hot original-clause selector (not all-general-CNF or all-mixed specialization).

**New exact clock firewall:** To specialize a reflection proof to every rejected original source F with encoded length at most N, the clock must cover the actual A(F) rejection time. Otherwise, after fixing source bits, the rejecting-tableau clauses themselves become contradictory and deleting them produces no authenticated original-source proof. In a strict-RES toy, the correct decision takes 6 steps: $b=5$ yields a spurious empty source after specialization, $b=6$ yields the original UNSAT $(y)\wedge(\neg y)$ with a one-node Resolution proof. A deliberately incorrect rejection of the SAT source $(y)$ makes reflection satisfiable, independently demonstrating that correctness cannot be inferred from the trace.

A conditional **sufficient B3 plan** is: for one fixed P-time A, choose its genuinely all-input polynomial worst-case clock $b_A(N)$; build an honest polynomial-size source $H_{A,N,b_A(N)}$; prove $W_{Rmix341}(H_N)\le\mathrm{poly}(N)$; and prove that *every* such mixed proof source-specializes and lifts to $F$ in polynomial paid nodes (including LOCAL-CONVERT/VARDEF). Then $\overline W_{Rmix341}(N)\le\mathrm{poly}(N)$. These last two premises remain **OPEN**, and Haken does not supply them. This is a quantitative conditional decomposition, not B3 itself.

## Results and falsifiers

Python producer: 86 counted checks, no-import JavaScript independent referee: 80. Tested 3 PHP UNSAT sources, 34 deletion SAT neighbors, K4 odd/even parity 0/8 models, 6 GF(2) restriction homomorphisms, 8 malformed CNF strings, 3 corrupted proof fixtures and wrong-answer decider controls. All passed. Machine peak host RSS ~96,328 KiB is not FLMV space; tableau materialization can force $\rho\ge1$ in $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$.

1. Underclocking yields an authenticated-source-lift failure even when the clocked reflection source is UNSAT.
2. Incorrect rejection yields a SAT reflection witness, so a trace without externally established correctness is insufficient.
3. Resolution proof hardness cannot dominate full mixed proof size without a valid reverse translator.
4. Full mixed restriction closure remains unproved, especially named internal LOCAL-CONVERT wires and constant/unary effects of VARDEF.

## External assessment source audit

Located actual repository files, not inferred folders: `GROKPROOF/2026-11-03_1217_PROGRESS.md` blob acf9fbee (per-query lower bound wrongly inferred from a worst-case upper bound), `GROKPROOF/2026-11-03_1518_PROGRESS.md` blob 234fc189 (universal transformation explicitly OPEN), Claude ONETAPE 2026-10-28_1521 blob 9a5b05d6 (sequential access), Claude TPORT 2026-10-28_1452 blob 1f9fc727 (restricted alternation trading), Claude 0266 blob 694c1c81 (BOOL predictor critique). None proves B3. Read and credited LSPV-1 REFLECTION367 blob 64f4e87a, LSPV-2 SCOPE366 blob fafa532f, LSPV-5 REFEREE317 blob cd933881, previous LSPV-4 OUTPUT365, November 2 12:04 handoff and current issue #3.

## Readback verified new role-owned artifacts

- Report: [LSPV4 clock resource theorem](../agents/lspv-4/2026-11-03_1036_LSPV-4_CLOCK_COVERAGE_REFLECTION366.tex)
- Standalone independent executable: [compact 80-assertion verifier](../../experiments/arc/lspv4_366_clock_coverage_compact.js)
- JSON results: [immutable public ledger](../../results/raw/arc/2026-11-03_1036_LSPV4_CLOCK_COVERAGE_REFLECTION366_public.json)

GitHub readback and execution of the exact published JavaScript passed. No root main.tex update claimed without safe full readback. **P versus NP remains OPEN.**
