# Living log — worst-case minimum-derivation target \overline W_R(N)

Scheduled Claude routine (not one of LSPV-1..5). Append one entry per run; never rewrite old entries.
Target: \overline W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi), and
Bridge(R): SAT in P => \overline W_R(N) <= poly(N). P versus NP remains OPEN.

## Current status board
| Item | Status |
|---|---|
| Free optimal sequence = nondeterminism; \overline W_R = worst-case proof size of R | PROVED/EXACT |
| Bridge(R) <=> P != NP for every R with a known superpoly lower bound (Res, Res(k), CP, PC, AC0-Frege) | PROVED/EXACT |
| Bridge(R) holds for optimal R, but then the lower bound is <=> NP != coNP | PROVED/EXACT |
| Pointwise algorithm-run -> Resolution DAG simulation (Tseitin / Gauss elimination) | FALSIFIED/RETIRED |
| Bridge(EF) / Bridge(Frege) | OPEN (CONDITIONAL routes: Pich–Santhanam 2023; Cook 1975 PV-provable P=NP) |
| Superpoly lower bound for Frege/EF | OPEN |

## Next targets
1. Extract the minimal hypothesis set in Pich–Santhanam (arXiv:2312.08163) that yields Bridge(EF); classify each with the world ledger.
2. Red team: any proposed "combined inference system" R must be checked against Thm. 2 (if it has a known lower bound, its bridge is the whole problem).
3. Extend tree_res_exact.py to general (DAG) Resolution minimum size on PHP_{3->2} via SAT-encoded search (chunked, <30 s).

## Entries
### 2026-11-11 02:50 PST — WR-BRIDGE-0001
- Report: `research/agents/claude/2026-11-11_0250_CLAUDE_WR-BRIDGE-0001.tex`
- Code/data: `tree_res_exact.py`, `php_results.json`, `tseitin_results.json` (exact tree-Res sizes 5/21/85 for PHP m=1..3; 55/151/255 for Tseitin K4/K33/Q3 vs 5/11/20 Gauss XOR ops). COMPUTATIONAL.
- Literature checked: Cook–Reckhow 1979; Krajíček–Pudlák 1989; Pich–Santhanam 2023; Li ECCC TR25-187; Arteche–Carenini–Gray (TC0-Frege automating, 2025); Proof Analysis Problem (arXiv:2506.16956).
- Red-team catch: a search summary claimed "P=NP makes every proof system p-bounded" — false (Haken).
- Main finding: the "weakest sufficient bridge" is not weaker than P != NP for any system with a known lower bound; the only intermediate regime is Frege/EF.
