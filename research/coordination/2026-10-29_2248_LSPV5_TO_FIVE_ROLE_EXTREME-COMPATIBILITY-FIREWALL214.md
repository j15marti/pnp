# LSPV-5 to five-role handoff: EXTREME-COMPATIBILITY-FIREWALL214

Timestamp: 2026-10-29 22:48 America/Los_Angeles  
Active coordination: GitHub issue #3  
Status: **PROVED/EXACT** restricted theorem; **COMPUTATIONAL** finite controls; **FALSIFIED/RETIRED** shortcut; P versus NP **OPEN**.

## One exact result

Let a DPLL node be one coherent partial assignment to the original shared variables. If a fully assigned source clause is in local extreme mode S (truth vector 111) or U (000), its occurrence demands are exactly the values already present in that assignment. Therefore every pair and every set of realized extreme modes is compatible. Adding only the SS/SU/US/UU compatibility matrix to a coherent source-variable DPLL search rejects no node and cannot shrink that search tree.

The matrix can still be useful as a representation firewall when a different procedure guesses clause/occurrence targets independently. Any claimed pruning benefit must charge that alternative state space and its reconstruction.

## Genuine source-level pruning

Opposite occurrences in source parents `(x OR A)` and `(not x OR B)` yield the non-tautological resolvent `A OR B`. Falsifying that resolvent certifies an impossible partial cube. Parent IDs, pivot, resolvent, and cube are retained and externally checked against every small-instance extension.

## Minimal hostile family

Take `r` duplicates each of

- `A=(x OR y OR z)`;
- `B=(x OR y OR not z)`.

Every one of the `r^2` cross pairs has all four extreme modes incompatible, yet the full formula is equivalent to `A AND B`, has six of eight models, and is solved immediately. Dense extreme-conflict structure can be created by duplication without increasing decision difficulty.

## Reproducible controls

Twelve families were checked: endpoint-failing SAT, duplicate supports, contradictory padded units, SAT/UNSAT XOR3, dense overlapping XOR with primal graph K6, Horn, padded 2-SAT, connected strict exact-(2,2), all eight sign patterns, planted dense SAT, and polarity renaming.

Exact checks:

- 777,337 pair extreme-mode checks;
- 89,344 multi-clause S/U checks;
- 15,520 coherent realized extreme-pair checks;
- 10,768 complement checks;
- 67,888 single-flip clause checks;
- 7,100 prohibited-cube extension checks;
- 967,957 total.

The compatibility guard rejected zero nodes and produced exactly the baseline DPLL node count on every control. On dense XOR K6 it increased instrumented work from 911 to 1,101 units. Bounded resolution sometimes reduced nodes but could lose after preprocessing: dense XOR stayed at 3 nodes while charged work rose 911 to 39,531. The padded contradictory-unit core improved 19 to 3 nodes and 589 to 573 units.

The baseline is fixed-order DPLL with saturated UP, not industrial CDCL. Work units are clause scans, literal reads, recursion/branch operations, propagation/conflict operations, compatibility checks, and resolution preprocessing—not tape crossings or native RAM bytes.

## Cross-role obligations

1. **LSPV-1:** Any middle-state upper bound must derive a source-level clause/cube, not merely reject unrealizable occurrence labels.
2. **LSPV-2:** Compare proposed extreme closure with UP absorption; report only consequences not already absorbed.
3. **LSPV-3:** In adaptive trails, separate avoided coherent DPLL nodes from avoided inconsistent clause-label states.
4. **LSPV-4:** Charge recognition, pair construction, resolvent construction, proof checking, and representation switches in the same execution.
5. **LSPV-5:** Continue duplicate/polarity/XOR hostile controls and referee every source-level consequence by exact extension checking.

## Next lemma

Find a polynomially recognizable partial-assignment regime where the signed-extreme graph plus a certified middle-state bound derives a non-tautological source clause not already absorbed by UP, and show net charged savings on both SAT and UNSAT controls.

