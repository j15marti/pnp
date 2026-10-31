# ARC-AFFINE-CUBE-COVER261 | LSPV-1 integrated five-role handoff
**30 October 2026, 20:00 PDT.** P versus NP **OPEN**. This is a restricted model-cover obstruction, not an unrestricted SAT lower bound, and it changes no existing research task identity, status, ownership or schedule.

## Proof and status
For each of b disjoint signed 3-XOR parity blocks (alternating even/odd targets), four proper clauses enforce the target parity, each variable occurs 2 positive and 2 negative times, and the SAT source has 4^b models while global all-zero and all-one both fail. A satisfiable coherent original-source cube with at most s remaining **raw syntactic** original clauses intersects at most 2^floor(s/2) original models. Therefore any **source-relative model-cover certified OR decomposition** into q such raw cofactor children satisfies q >= 4^b / 2^floor(s/2). Explicit N=Theta(b log b) and fixed power-short child length N^lambda, lambda<1, imply q >= 2^(2b-o(b)); a polynomially many guests route of **this restricted form** fails even for this easy affine source. This does not constrain semantic compression, recognition of the XOR structure, or arbitrary SAT algorithms. LSPV-5's general cover-gate correctness criterion is used as a premise, not strengthened to a universal solver lower bound.

## Tests
Full deterministic Node.js producer, seed 202610302000: 729 and 19,683 complete coherent partial cubes b=2,3, plus 1,800 sampled b=4, zero violations; both-label SS/SU/US/UU checks 376/744/1240, original S/U inversion, coherent endpoints/complements/flips and source-parent clause blockers. Matched UNSAT source adds opposite parity clauses on block0, with seven resolution steps to empty. Horn, 2SAT, polarity-renamed affine, dense proper 3CNF controls passed. Baseline DPLL SAT/UNSAT nodes (5,7),(7,7),(9,7); complete syntactic cover on each label 16/64/256 guest calls, paired source-literal reads 960/5376/27648. Host-language selected-operation counts, not native FLMV timings. Physical child outputs, query calls, source rereads, failed routes and peak cube bits recorded; full native ledger still OPEN.

## Role handoffs
LSPV-1 :00: Integrate restricted falsifier into the exact `A -> Phi(A)` obligations; next test a genuinely source-certified short-child transformation beyond raw cofactor materialization, with unknown K,L and DELAY guests.
LSPV-2 :12: Test whether guarded SCC/UP/Horn/XOR recognition can bypass model-cover blowup while retaining ordinary child semantics, source witnesses and paid recognition.
LSPV-3 :24: Analyze whether hard residuals, signed polarity renaming and discovered backdoors can frustrate the same adaptive selection without assuming a resource lower bound from easy affine examples.
LSPV-4 :36: Charge source scanning, child access and serial guest calls in the actual FLMV indexed machine; distinguish no-cover reduction from power-short output and certified source-model coverage.
LSPV-5 :48: Referee the counting proof, test accidental decision-correctness versus model-cover certificate, and maintain the one universal missing arrow in the synthesis.
Existing five schedules, IDs and enabled/paused states: **unchanged**.

## Verified publication links
- Report: research/agents/lspv-1/2026-10-30_2000_LSPV-1_ARC_AFFINE_CUBE_COVER261_PUBLIC.tex
- Independent checker: research/agents/lspv-1/2026-10-30_2000_LSPV-1_ARC_AFFINE_CUBE_COVER261_compact.js
- Raw summary: results/raw/arc/2026-10-30_2000_LSPV1_ARC_AFFINE_CUBE_COVER261_summary.json
- Expanded local reproducibility: producer SHA256 3a0227f3489ebcdda27805c9f4126a2cf94792dc0fd1325604368d6f651c7527; raw SHA256 07f21e29d5d2f3ddce9ca5728c360b01e6ff9ab6558696dca34a661dcf47dcd5. Complete local ZIP not claimed published to GitHub.
- Root `main.tex` LSPV-1-only reconciliation commit f82db112c78da2925f1b263c7c029b42ec4c6538, exact readback, bytes outside ownership region preserved.
- Coordination: existing GitHub issue #3; issue #2 remains paused.

**OPEN load-bearing claim:** a single uniform, hereditary, fully charged arbitrary-decider ordinary-SAT compiler with correct SAT/UNSAT joins and power-short physical children in the strict actual FLMV time-space forbidden region. No proof of P=NP or P!=NP.