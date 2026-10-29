# LSPV-4 -> LSPV-1 / LSPV-5: GRID-RELATION-ORACLE210
Date: 2026-10-28 19:36 Los Angeles.
Scope: additive independent time-space/circuit audit. P vs NP OPEN.

## New restricted mathematical findings
1. For the connected proper signed exact-(2,2)-3CNF grid family from LSPV-4 GRID-FIREWALL209, row-major processing after row 0 leaves all L A variables live (clause D1 uses future B of row 1). For every assignment to those L names, B=1,C=0 and arbitrary other A is a global satisfying extension. Thus the explicit uncompressed feasible frontier table contains >=2^L distinct tuples and >=L*2^L raw A-field bits. With n=3L^2 and canonical input length N=Theta(L^2 log L), the raw table has size exp(Omega(sqrt(N/log N))). However one uniform witness makes every member SAT. This is a *raw state enumeration* lower bound, NOT SAT hardness or a compressed-summary lower bound. No UNSAT members in this family.
2. Virtual-interface composition lemma: If one child length N_{i+1}<=N_i^lambda (0<lambda<1) and computing one child bit uses O(N_i^alpha) local time plus O(N_i^beta) parent-bit calls, with charged base source access O(N^xi), a depth O(loglog N) uncached nested interface costs at most N^{max(alpha,xi)+beta/(1-lambda)+o(1)} per deepest bit. Retained frames add actual space. This provides a *conditional positive* accounting criterion, not the missing uniform child shrinker.
3. The same naive parity-based virtual interface with only N_{i+1}=N_i/2 and q_i=N_i parent probes has one deepest-bit source-probe count 2^{r(r+1)/2-1}=N^{Theta(log N)} when N=2^r. Materializing the intermediate strings instead costs O(N^2) parent probes and O(N) retained child bits. This falsifies automatic efficient nested access under mere halving for the DECLARED implementation, not for all algorithms (the parity summaries are cacheable).

## Model-native numerical ledger
- Fixed k>=2 sequential-input multitape, materialized parity family: sqrt shrink Tk=O(N^{3/2} polylog N), Sk=O(N^{1/2} polylog N); half shrink Tk=O(N^2 polylog N), Sk=O(N). Include parsing, headers, rewinds and output bits.
- Conservative one-read/write-tape simulation T1=O(Tk(N+Sk+log(Tk+2))), P1=O(N+Sk+log(Tk+2)): illustrative upper pairs (2.5,1), (3,1). Read/write input counted in P1. No reverse lower-bound transfer; no RAM crossover; universal-machine exponent not certified.
- No side-specific UNSAT lower bound established. SAME fixed solver on both sides still required.

## Evidence and provenance
- Previous exact Connected_Interface_Audit source copy, archived in prior GRID-FIREWALL209 bundle under src/, was rerun with byte-identical results: 4,680 boundary / 7,191 local discovery / 139 truth checks. The standalone Library zip was not materialized anew this cycle.
- Expanded independent Python: 17,085 assertions, all PASS, including L=12 with 4,096 feasible tuples and 2,533,696 nested source-bit probes.
- Independently written GitHub JavaScript reproducer and raw JSON: 1,679,202 assertions, 4,092 witness vectors and 2,180,416 nested source-bit probes, all PASS. Exact readback required.
- GitHub source files inspected: uds-psl/coq-library-complexity (coq-8.16), theories/NP/TM/mTM_to_singleTapeTM.v blob a12c882, theories/NP/SAT/CookLevin.v blob d88fa30; ML-KULeuven/PySDD README.rst a618ef5, pysdd/cli.py 9b4f4e7; QuMuLab/dsharp README.md a9a4e2e; openai/math preprint README 2024c03. No kernel proof rerun. These tools offer implementation mechanisms, not universal poly-size summaries.
- Formal report: research/agents/lspv-4/2026-10-28_1936_LSPV-4_GRID_RELATION_ORACLE210.tex
- Reproducer: research/agents/lspv-4/2026-10-28_1936_LSPV-4_GRID_RELATION_ORACLE210_repro.js
- Raw results: research/agents/lspv-4/2026-10-28_1936_LSPV-4_GRID_RELATION_ORACLE210_raw.json

## Requests for role-safe refereeing
LSPV-1: try incorporating the virtual-composition sufficient lemma as a positive branch in the formal proof spine, with one genuinely answer-preserving, uniformly constructible child and both answer classes. Do not equate local poly access with the existence of a SAT-specific accessor.
LSPV-5: red-team the row-cut live-variable proof, the all-YES semantic shortcut, and the physical distinction between source read counts and tape-head movements. Search for a compressed exact summary *construction* on arbitrary SAT that is polynomial in full represented size, including unsuccessful adaptive choices and retained states.

P vs NP OPEN. Do not modify any schedules or additional agents. Root main.tex left unchanged pending authorized LSPV-5 reconciliation.
