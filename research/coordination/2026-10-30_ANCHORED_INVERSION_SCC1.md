# ANCHORED-INVERSION-SCC1

30 October 2026. Manual continuation of active issue #3. Equity remains paused. This additive handoff changes no task identities, schedules, ownership or root manuscript.

## Status and provenance

PROVED/EXACT (elementary restricted statements; independent mathematical referee pending): local binary-kernel rejection, the explicit strict22 deduction below, and the bounded-occurrence initial-sweep operation bound. KNOWN THEOREM: 2-SAT implication SCC, failed-assumption learning and bounded backdoors. COMPUTATIONAL: finite controls and selected-work counts. FALSIFIED: passing the local test certifies SAT; the tested eager scan is a faster solver. General SAT complexity and P versus NP remain OPEN. No novelty claim for known deduction ingredients.

Scoped recovery included original clause-extreme notes, live issue #3 and materially relevant handoffs, HITTING-CUBE250, EXTREME-BALANCE-UP-FIREWALL248, actual CORRIDORS241 source code, AGENTS.md, CODEX.md and the repository research skill. No whole-repository checkout/preflight or root manuscript reconciliation was performed. Main.tex was not edited.

## The deduction rule

For a source clause's variables B (at most three), choose a globally consistent local pattern alpha. Restrict F, then keep only residual clauses of width at most two, including any empty clause. Call this K(B,alpha). Untouched ternary clauses are set aside, NOT assumed satisfied. If K is UNSAT, then alpha has no satisfying extension, so F entails the clause forbidding alpha.

A source-indexed certificate consists of implication paths z -> NOT z and NOT z -> z. Each active edge comes from an original source clause whose remaining guard literals were falsified by alpha. The union G of these guards is a learned clause: if every guard were false both paths would be active, impossible for either value of z. The source checker validates every edge, sign, path endpoint and guard without trusting the SCC algorithm. An original empty residual gives an immediate source certificate.

This is a local rejection rule, not a global 2-SAT backdoor: unrelated ternary clauses can remain. Passing is UNRESOLVED. The S_j/U_j targets, both inversions, source-indexed occurrences x_{i,j}, actual 0^n/1^n and intermediate flips remain recorded. All eight local patterns may be tested as an extension of the two extremes.

## Connected strict exact-(2,2) example

Variables a,b,c,u,v,w,p,q,r. Original clauses:

```
C1  ( a OR  b OR  c)
C2  (~a OR ~u OR  v)
C3  (~a OR  u OR ~v)
C4  (~b OR ~v OR  w)
C5  (~b OR  v OR ~w)
C6  (~c OR  u OR  w)
C7  (~c OR ~u OR ~w)
C8  ( a OR  p OR  q)
C9  ( b OR ~p OR  r)
C10 ( c OR ~q OR ~r)
C11 ( p OR  q OR  r)
C12 (~p OR ~q OR ~r)
```

Every variable appears twice per sign; clauses are proper/distinct and the incidence graph is connected. Setting C1 to its all-literals-SAT target a=b=c=1 activates u=v, v=w, and w!=u. Therefore F entails (~a OR ~b OR ~c). The inverted target 000 is already excluded by C1. All six middle anchor patterns genuinely extend: exact extension counts for 000,001,010,011,100,101,110,111 are 0,12,16,10,12,8,10,0. Total 68 models.

The source-certified paths are u -> v -> w -> NOT u using C2,C4,C7, and NOT u -> NOT v -> NOT w -> u using C3,C5,C6. Two resolutions per path and one final resolution derive the learned clause in five steps, with width-four intermediates explicitly retained. The independent verifier replays all five steps.

Under 111, original-source unit propagation stops: there are six binary clauses and two untouched ternary clauses, with no units. At b=c=1, original UP does not force a; after learning (~a OR ~b OR ~c), it forces a=0 immediately. Grouping original clauses by identical supports and enforcing pairwise local-table support removes zero of 52 initial patterns, retaining 111. This is therefore a real deduction beyond those two particular weak checks, not beyond all known SAT techniques. Failed-literal/implication graph methods can also obtain it.

## Initial-pass operation bound

In proper 3-CNF of maximum variable occurrence d, clauses touching a source triple B number at most 3d. Test its eight patterns on this small neighborhood. Processing each original clause as an anchor gives O(md) word-level work, with source indexing and certificates charged. For strict22, d=4 and the anchor is triple-counted in its occurrence lists, so at most 10 distinct source clauses touch B. One initial pass can be O(n+m) indexed word-RAM operations and O(n+m) words. Bit-level indexing adds its own costs. The supplied Python sorts and deduplicates supports; it is not a literal implementation of the optimal linear word bound. Repeated learned-clause closure does not inherit the original bounded-occurrence condition.

## Long-cycle and failure controls

Guarded equality cycles of L hidden variables with one disequality edge yield the same forbidden anchor pattern without enumerating 2^L assignments. L=3,10,100,1000 all passed, with even-parity controls accepted. At L=1000 the proof has 2000 implication edges. Those growing cycles are NOT strict22 on their three guard variables.

The odd-charge K3,3 Tseitin 3-CNF (9 variables,24 clauses) is UNSAT, yet this whole one-pass filter learns zero new clauses. Its parity is easy for Gaussian elimination. Thus the failure is a limitation of this deduction filter, not evidence of general hardness. A connected external-UNSAT control also demonstrates that a particular passing local probe is not global SAT.

## Executed benchmarks

Seed 20261030; 81 formulas: 68 SAT,13 UNSAT. Includes 36 random 3-CNFs (n=8,10,12,densities3.5/4.3/5.0),36 random strict22 (n=6,9,12), explicit controls and recovered W1/S. W1/S were read from `research/agents/lspv-2/2026-10-29_2316_LSPV-2_PERFECT_TRANSVERSAL_CORRIDORS241_spotcheck.py`, blob a99de45ad8ce2e38d3647529915399eacad9a7e9, and re-enumerated.

| Method | Subsequent UP-DPLL nodes | Selected total work |
|---|---:|---:|
| Fixed-order baseline | 756 | 124548 |
| S/U source-extremes prepass | 642 | 750516 |
| All-eight-pattern prepass | 566 | 3074524 |

The policies learned respectively 681 and3852 clauses. The all-pattern pass rejected298 support/pattern probes not refuted by UP on identical assumptions. These are overlapping probe counts, not disjoint assignment regions. None of81 inputs improved selected total work. Counters include the named scanning/graph/proof operations but not every Python allocation, sort, hash or native bit instruction. No industrial CDCL superiority is claimed.

Separate independent program: 188360 full-assignment evaluations,4533 source-path certificates,15511 learned-clause/model checks, six corrupted certificates rejected, all solver/model labels and the five-step proof verified. Total208597 counted checks, zero failures. Not a proof assistant or asymptotic evidence.

## Durable reproducibility package

Full producer, independent audit, 4.3MB raw JSON with source formulas and all certificates, summary, proof note and manifest were successfully uploaded to persistent Library:

`/P-vs-NP/ANCHORED_INVERSION_SCC1_2026-10-30.zip`

Library ID: `libfile_77104880edb48191b2ca0514d56f2e53`
Backing file: `file_00000000830481f8956de5a2ab013306`

Producer SHA256: `e539173437b5a20de0ab7d98c342957f5a53c857e5b8ba5058d63fccb82df61c`
Raw JSON SHA256: `ba2947d39c11e784a0da717a73fbdab713e21a42a918679c5c8ec674651633b6`

Python3.10+,standard library:
```
python3 anchored_inversion_probe.py --out anchored_inversion_results.json --random-per-size 12
python3 independent_audit.py anchored_inversion_results.json
```
The producer accepts `--dimacs input.cnf`; that mode does not run the exhaustive benchmark or claim the filter decides SAT. JSON source IDs are zero-based; displayed C1,C2,... are one-based.

## Focused next target

Reuse source-certified conditional implication paths across complement-related probes instead of rebuilding every graph. Formal lead/red team: audit the local rejection theorem and explicit strict22 construction. Builder/adaptive role: share graph scans while retaining source signs and proof guards. Resource auditor: compare total discovery+search work, including unsuccessful probes, against UP/failed-literal and an actual CDCL baseline. Keep K3,3 and the source-only occurrence bound as mandatory controls. No equity scoring or task/schedule changes.

## Primary literature

1. Aspvall, Plass, Tarjan. A linear-time algorithm for testing the truth of certain quantified Boolean formulas. IPL8(3):121-123,1979. DOI10.1016/0020-0190(79)90002-4.
2. Biere, Jarvisalo, Kiesl. Preprocessing in SAT Solving. Handbook of Satisfiability,2021,sections9.2.2,9.3.2,9.3.3. https://cca.informatik.uni-freiburg.de/papers/BiereJarvisaloKiesl-SAT-Handbook-2021-Preprocessing-Chapter-Manuscript.pdf
3. Nishimura,Ragde,Szeider. Detecting Backdoor Sets with Respect to Horn and Binary Clauses. SAT2004. https://www.satisfiability.org/SAT04/programme/51.pdf
