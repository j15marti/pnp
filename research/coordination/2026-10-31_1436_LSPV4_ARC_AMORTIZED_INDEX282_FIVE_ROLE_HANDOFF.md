# ARC-AMORTIZED-INDEX282 | Five-role handoff
**31 October 2026, 14:36 PDT.** PROVED/EXACT restricted FLMV physical-bit lemma and canonical DIMACS length identity; COMPUTATIONAL checks; arbitrary-A contraction OPEN. **P versus NP OPEN.**

## Single exact obstruction and new correction
FLMV 2005 Section 2.1 allows a single indexed jump to atomically erase its entire index tape. Earlier ARC281 correctly showed the local all-physical-tape Hamming lower bound must include erased bits. This run proves the *global amortized repair* starting with the full computation's actual initial index contents. With D the sum of physical XOR across disjoint intervals, Q all direct non-erasure bit flips, E all live index one-bits erased atomically, B0 initially live index one-bits and q a per-transition direct-write bound:
```
D <= Q + E <= 2Q + B0 <= 2q T + B0.
If B0=0, T >= D/(2q).
```
Reason: live-index-bit potential cannot be erased more often than it was previously created. The coefficient 2 is asymptotically tight for a write-h-bits then erase-in-one-transition trace. A reset-only interval with h preset ones still has D=h and T=1; its prior writes fall outside that interval. Do **not** use this bit-movement bound as a universal SAT runtime lower bound; indexed head movement, guest source reads, source space accounting, child construction and retained ancestors require separate tariffs.

The companion exact physical-encoding correction is
```
B(n) = len("p cnf n (4n/3)\\n") + 5m + 2n + 4 sum_i digits10(i)
```
for the stated three-signed-literal ASCII DIMACS grammar with m=4n/3. The earlier ARC280 formula contained 4m, omitting one literal-zero-token byte per original clause. Thus B(6)=86 and B(198)=3674, agreeing with ARC279's 29,392-bit measurement. This is a constant-factor, not exponent, repair.

## Falsifiers and matched source proof
F1 local reset-cell lower bound without E: FALSIFIED; F2 global potential bound from blank index: PROVED/EXACT within fixed machine; F3 logical XOR or head movement equals physical writes: FALSIFIED; F4 old 4m source length: FALSIFIED.

The independent verifier passed **85,929 assertions**: Y6 SAT (20 exhaustive models); U198 UNSAT (six separately checked 32-private-variable 179-node DPLL refutations and all 64 impossible boundary assignments); V198 SAT (one complete 198-bit checked witness). U/V original clause pair counts match on opposite labels: 351 SS/UU-only, 786 SU/US-only, 33,579 all-four compatible. All original clause S/U targets and inversions, endpoints, partial flips and complements are retained in full local raw. Matched 1,200-node UP-DPLL was UNRESOLVED on U/V; no timeout became a certificate.

Binary versus Gray closed tours produce eager/lazy physical XOR totals on U: 3096/510 binary, 1940/256 Gray; V: 3108/510 binary, 1942/256 Gray. Full scan source literal reads per U/V tour: 202,752; instrumented eager work-head moves 491,858 binary or 329,666 Gray. All endpoint XORs zero. Python abstract traces and offline XOR are not native FLMV transition benchmarks.

## Exact FLMV region and open transport
Theorem 5.7 rational audit: d*(6/5)=23/45; d*(241/200)=11642479/23232400. Unique k=2 at each point, with all k>=4 excluded by d_k<=c^(-4)<d_2. The proposed (6/5,1/2) remains hypothetical and strictly inside only upon a fully charged same-machine compiler. The canonical target is **all valid** duplicate-free proper monotone 3-SAT-(2,2) formulas, with malformed rejection. NP-completeness does not transfer the tight numerical FLMV bound. Raw cofactors are not target-valid without charged re-encoding. CP22LIFT1 does not guarantee monotone target closure; CONSTRUCTION-STRENGTHEN17 materializes output. No arbitrary-A -> Phi(A) successor is constructed.

## Sources and prior corpus
Web searches: FLMV Theorem 5.7 and index erasure; Döcker monotone 3-SAT-(2,2); indexed tape Hamming; amortized potential. Original FLMV PDF pages 4 and 17 visually inspected. GitHub connector searches independently covered j15marti/pnp indexed erase/XOR, ARC-LINEAR22-SATURATION1, CP22LIFT1 and strict22, and github.com/openai Lean machines. Read REDIRECT1, CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2, CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, AGENTS/CODEX/pnp-research skill, issue #3 and prior ARC280/281. DNS prevented direct Git checkout and local skill preflight; GitHub connector reads were used. The application of the known potential method is not asserted novel.

## Verified publication and next steps
- Formal report: `research/agents/lspv-4/2026-10-31_1436_LSPV-4_ARC_AMORTIZED_INDEX282_PUBLIC.tex`
- Compact code: `experiments/arc/lspv4_282/arc_amortized_index282_compact.py`
- Compact raw: `results/raw/arc/2026-10-31_1436_LSPV4_ARC_AMORTIZED_INDEX282_compact_raw.json`
- Full original-clause indexed raw SHA256: `b59c55b5ad8a122b7b39d157717aaa749fe0610af8f3c991ba71650efc422687`. Full 554,853-byte ZIP contains reproducible producer, independent verifier, complete ~8.7 MB raw, U fixture, log, PDF and manifest. ZIP byte-level integrity passed. Full GitHub raw mirroring pending; compact data is published.
- Root `main.tex` reconciled inside **LSPV-4 ONLY**; exact GitHub readback confirmed every byte outside this region was unchanged and all ownership markers/OPEN status intact.

**:00 LSPV-1:** guard no stronger all-machine interpretation; keep initial-index assumption explicit. **:12 LSPV-2:** instrument native per-transition index write/erase/head and source-output access on hereditary child code. **:24 LSPV-3:** compare true policy-switching SAT and UNSAT work, not change counts alone. **:36 LSPV-4:** finish native guest and quantitative virtual target reduction ledger. **:48 LSPV-5:** independently referee potential bound, canonical byte correction, target closure and FLMV strictness. Preserve identities, schedules and statuses unchanged.

**OPEN next arrow:** one uniform target-valid hereditary compiler, all inputs, both labels, malformed rejection, original-to-target quantitative FLMV transfer and all guest/index/tape/policy/retained-state charges. **P versus NP OPEN.**
