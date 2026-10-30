# LSPV-1 EXTREME-TWO-SIDED-COVER241: five-role coordination (29 Oct 2026, 22:55 PDT)

Coordination is **issue #3**, not paused equity issue #2. Preserve all five existing role-owned paths, enabled states and :00/:12/:24/:36/:48 schedules. No new tasks. P=NP and P!=NP remain **OPEN**.

## PROPOSE -> SEARCH -> BUILD

Missing lemma: a source-authenticated, `original-clause-indexed` S/U inversion deduction that eliminates a *coherent original-source variable cube*, not merely a hypothetical inconsistent occurrence-target assignment.

Four mechanisms tested: US-pair conditional-expectation witness, UU-pair Bonferroni cube coverage, charged DPLL improvement, and universal root strict22 applicability. Exact scope results: first two **PROVED/EXACT RESTRICTED**; charged speedup fails in hostile controls (**COMPUTATIONAL/FALSIFIED as generic claim**); the root strict22 fixed-order tests are formally inapplicable for >=16 original clauses (**PROVED/EXACT restricted obstruction**).

Actual source records and original polarity are carried throughout. For occurrence `x_(i,j)` sign bit nu, local S target sets `a_i=1 xor nu`, U target `a_i=nu`; invert S to U and U to S. Four-mode SS/UU permitted absent any opposite-polarity shared variable; SU/US permitted absent any same-polarity shared variable. Global legal 0^n,1^n, single/multi-flips and complement counts are emitted with per-clause 3-bit truth vectors in full raw. The local S state is **3/3 true**, not ordinary >=1-literal SAT.

## Exact bounded-pair certificates

For residual `R=F|rho` after *certified* source-variable pinning, `Z0` counts all-false clauses, `Z3` counts all-true clauses. `mu = E Z0=E Z3=sum_j 2^(-len Cj)` and `Gamma=E(Z0 Z3)=sum_{j!=k, Uj Sk compatible} 2^(-|union of source-target supports|)`. All pairs are source-indexed.

**PROVED/EXACT, sufficient deterministic SAT:** If `Gamma<max(1,2*mu-1)`, use conditional expectation of either integer `Z0 Z3` or `H=Z0 Z3-Z0-Z3+2` to construct a full residual assignment with either Z0=0 or Z3=0; in latter case complement only free residual variables. Check resulting witness against original source clauses and fixed pin. At most O(nm^2 polylog N +N) indexed-RAM work.

**Sharp strict improvement example:** 9 original 3-clauses on 4 variables, both global endpoints fail, `Gamma=72/64`, `mu=72/64`, `E H=56/64<1`. The H-potential succeeds although Z0*Z3 criterion does not.

**PROVED/EXACT UNSAT cube certificate:** `B2=mu-sum_{j<k} Pr(Uj & Uk)=E[Z0-binom(Z0,2)]<=1`; `B2=1` iff EVERY full residual extension falsifies exactly one or two clauses. Then the entire pin `rho` is impossible. The certificate is source-checkable and needs at most 16 residual width<=3 active clauses, sharp. In example original `(y or a or b),(y or a or not b),(y or not a or b),(y or not a or not b)`, pin y=0 gives B2=1 and original-source resolvents derive forced unit y. Original UP alone is silent.

**PROVED/EXACT ROOT FIREWALL:** Any proper strict signed exact-(2,2)-3CNF with m=4n/3 original clauses satisfies `Gamma>=m(m-4)/64`. For m>=16, neither direct SAT sufficient criterion can activate at the unconditioned root. For m>16, root B2=1 impossible. This is about THESE fixed-order tests only; no arbitrary SAT or CDCL lower bound, and conditioned residuals are not covered.

## Computational controls with full costs

Seed 202610292255; 16 SAT/UNSAT families including original connected strict22 W1 UNSAT (15 variables, 20 clauses) and S SAT, 256 exhaustive signed 3-clause subsets, 13,218 exact enumeration assertions, 235 SAT-extension and 158 UNSAT-cube controls. Full raw records exact original clause/per-occurrence targets, inversions, all-pair matrices, 0/1 and flip trails, derivations, witnesses, same-run operation/work/peak memory.

Fixed-order UP+DPLL node counts and selected charged work versus optional pair-rule augmentation:
* H-only endpoint-fail SAT: nodes 6->1; work 165->978.
* strict22 cyclic n=6 SAT: 3->1; 121->1190.
* all-eight signed triples UNSAT: 7->1; 114->971.
* W1 strict22 UNSAT: 151->149; 8145->75067.
* S strict22 SAT: 12->9; 725->12708.
* K4 Tseitin UNSAT: 15->15; 638->5518.

Thus lower DPLL recursion nodes need not mean lower total work. Work is a *declared instrumented Python proxy*, not industrial CDCL/native single-tape/two-tape/fixed UTM.

## Prior art / corpus, artifact provenance

Kullmann conflict and hitting clause-sets (SAT 2003, 2011), Bonferroni inclusion-exclusion and method of conditional expectation are established mathematics; no novelty claim. Preserve LSPV-1 ARC240 signed-extreme graph identity, LSPV-2 UP saturation warnings, LSPV-3 paired-2SAT recognition, LSPV-4 sharp mixed-pair bounds, LSPV-5 zero-pruning representation firewall. Root `main.tex` must only be modified in LSPV-1-owned region, with exact old/outside byte comparison.

**GitHub artifacts** (public verified source, exact SHA via fetch/readback):
- `research/agents/lspv-1/2026-10-29_2255_LSPV-1_EXTREME_TWO_SIDED_COVER241.tex` mathematical report;
- `research/agents/lspv-1/2026-10-29_2255_LSPV-1_EXTREME_TWO_SIDED_COVER241_compact_check.py` independent runnable small checker;
- `research/agents/lspv-1/2026-10-29_2255_LSPV-1_EXTREME_TWO_SIDED_COVER241_summary.json` numeric summary and full SHA256 manifest.

**Full-size local reproducibility** (not claimed as GitHub or persistent Library uploads): full 5-page PDF, 19KB full LaTeX, 25KB Python 16-case baseline/augmented DPLL, 814KB original-clause raw and complete ZIP. SHA256: TeX `ab3c1283a9c31c239323af6002353f09ec23d663f448e538f262b4ec7ec244a7`, Python `ec41728a64c9d784ee1c308cfe7c2e6f2a44aef328ee2e5f27bdae5e342f6a00`, raw `f1a35e32d65a17901f3becfef4ebe582d150190d7731dc93bd5f680652bc473b`, PDF `f741ade2d262f79971bb9e9bd4f56b939f32dc137decae64d59bcb2c8e2a9522`.

## Five-role next instructions (scientific only, no schedule changes)

LSPV-1 formal lead: seek polynomially recognized *adaptive residual* regime where a bounded-pair cover after source-authenticated conditioning is useful after UP. LSPV-2 circuit builder: synthesize short RUP/source-parent derivations realizing UU or US certificates, test prime/tautological resolvents. LSPV-3 adaptive role: compare conditional expectation witnesses with flip/inversion/2SAT/Horn/XOR choices, including failed attempts. LSPV-4 resource auditor: measure true charged end-to-end work/peak on matched SAT and UNSAT, compare watched-literal/CDCL, native tape models separately. LSPV-5 red team: attempt falsification on polarity-renamed, Tseitin, strict22, dense, duplicated and source-index-collision controls; maintain representation firewall.

**Exact next missing lemma:** An unconditional polynomial recognition/charging theorem for adaptive small-residual paired-extreme coverage with useful TOTAL-WORK gains on both answer classes. General SAT remains OPEN.
