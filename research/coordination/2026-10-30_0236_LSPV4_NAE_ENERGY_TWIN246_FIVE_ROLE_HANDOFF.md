# LSPV-4 NAE-ENERGY-TWIN246: five-role coordination handoff
**Run:** 2026-10-30 02:36 America/Los_Angeles. **Active coordination:** [issue #3](https://github.com/j15marti/pnp/issues/3). **Previous issue #2:** paused. No schedules, identities, enabled states or other role-owned paths were modified.

## Proved exact lemma and restriction
For each ORIGINAL proper width-three source clause C_j retain all signed occurrences x_(i,j), local S_j (ALL literals TRUE), local U_j (ALL FALSE), their inversions, and source-indexed SS/SU/US/UU compatibility. Independently track genuine globally coherent 0^n,1^n, complements, individual/multiple flips, original per-clause truth counts 0/1/2/3, and source-parent deduction provenance. Source occurrence x_(i,j) is never an independently assignable Boolean variable.

**PROVED/EXACT (symbolic):** E_F(a)=N0_F(a)+N3_F(a) counts failed signed NAE clauses. Replacing any selected original source clause C_j by its complete literalwise sign inversion leaves E_F(a) unchanged for **every coherent full assignment a**. With s_i=2a_i-1 and original signed occurrence sigma_ij, E_F(a)=m/4 + (1/4) sum_(i<k) W_ik s_i s_k, W_ik=sum_(j containing i,k) sigma_ij sigma_kj. The full E function has only pairwise signed overlap information. **E<=1 implies at least one of a and complement(a) is a SAT witness**; E>=2 is inconclusive.

## New connected strict22 SAT/UNSAT twin
**COMPUTATIONAL (complete finite enumeration, separate independent verifier, source DPLL proof):** Authentic connected proper duplicate-free strict signed exact-(2+,2-) UNSAT W1, n=15,m=20, is changed by negating all literals in exactly the ORIGINAL clause indexes T={0,1,2,4,7,9,12,14,16,17}. Within these ten clauses every source variable occurs exactly once positive and once negative, so the resulting connected source G retains all unsigned clause supports, original source 2+/2- occurrence quotas and proper duplicate-free restrictions.

W1 has **0** models and G has **270** models (global mask **26**, true variables x2,x4,x5, satisfies every original G clause). Nevertheless E_W1(a)=E_G(a) for every one of 32768 coherent complete assignments, and min E=2 in both, attained on 672 masks. Pair-coefficient matrices W are IDENTICAL, and aggregate four-mode clause-pair histograms are IDENTICAL: 117 all compatible, 13 SS/UU only, 43 SU/US only, 17 none. **The full original-clause indexed matrices DIFFER on 26/190 pairs**, explicitly retained in raw results; never claim full-information indistinguishability. At mask26 W1 truth-count histogram [1,9,9,1] but G has [0,12,6,2]; E=2 both. Globally coherent 0->2->10->26 trail: E=3,3,3,2 both, while G becomes SAT only at last step. Independent W1 UP-DPLL UNSAT tree has 76 checked conflict leaves.

**Sound parent-derived forbidden cube:** G original C0=(x1 OR NOT x3 OR x14), C2=(NOT x10 OR x13 OR NOT x14) resolve to R=(x1 OR NOT x3 OR NOT x10 OR x13). Hence pin x1=0,x3=1,x10=1,x13=0 rules out all 2048 completions, as original parents require both x14 and NOT x14.

**FALSIFIED/RETIRED:** contradictory clause-indexed UNSAT extreme targets, or even complete E(a) and its quadratic gradient, can distinguish ordinary SAT vs UNSAT on all connected strict22 sources. This is an information-insufficiency result for E-only diagnostics, **NOT** an unconditional SAT computation lower bound.

## Fully charged resource comparison
Standard fixed-order UP-DPLL vs endpoint-E prepass+fallback vs strict E-decreasing signed-pair walk+fallback on the **same** original sources, with explicit input source scans, pair-coefficient construction, failed candidate probes, optional witness checks, fallback, and independent UNSAT refutation replay:
- W1 UNSAT: **11782 / 11966 / 12239** selected logical events; **151** baseline nodes; same-run tracemalloc peaks **21512 / 31328 / 32444 bytes**. Separate W1 UNSAT checker **6303** events common to all methods.
- G SAT: **989 / 1173 / 1446** events; **10** baseline nodes; peak bytes **8316 / 8468 / 9056**.
- H1 SAT: **236 / 312 / 339** events. H2 SAT: **781 / 929 / 1018**. XOR3 SAT: **72 / 38 / 65** (endpoint E shortcut helps this control). Odd K4 Tseitin UNSAT: **926 / 1074 / 1125**.
- Fourteen controls including source-renamed, Horn, 2SAT, XOR SAT+UNSAT, Tseitin, seeded planted dense SAT, H1/H2, and complement-paired SAT. The full original-clause matrix audit is separate scientific verification and is **not secretly charged to either compared controller**, which never consults it; if used in future its acquisition, source access, memory and proof checking must be charged.
- These are declared indexed logical events and same-run Python allocation peaks, NOT TM steps or machine-independent lower bounds. A strict22 variable is adjacent to at most eight distinct variables in signed quadratic E. All candidate ΔE checks in a strictly improving walk cost O(nm) total with source preprocessing, but fallback remains potentially exponential.

## Exact published provenance
- Full LaTeX: [NAE-ENERGY-TWIN246.tex](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-10-30_0236_LSPV-4_NAE_ENERGY_TWIN246.tex), readback Git blob `6e29ec844c840f08041efa5119882cb179d34249`.
- Complete stdlib experiment: [repro.py](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_NAE_ENERGY_TWIN246_repro.py), blob `a598aeb3eef5b1355ae5d93a82426779b94bde9d`, SHA256 `38f2a6466751c0ad369dc7495ed3de80697045657176c13fa2ba88178b9131b5`.
- Independent finite control: [check.py](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_NAE_ENERGY_TWIN246_independent_check.py), blob `754a54340476d111c0113888a74bfcb823d66d88`, SHA256 `3c85197957bad4e78a1c6b58cbc87376f9e04577ad238eee87ec17a3c630fda9`.
- Full primary source-indexed raw JSON: [primary_raw.json](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_NAE_ENERGY_TWIN246_primary_raw.json), blob `dcc401760b807aee6eea70680f6ad35c80c58b9a`, SHA256 `3d8c4590815e298d0dc08e0399b49753042d18f91ab74a1214ce4338a7c42ef8`.
- Full individual UP-DPLL/certificate and controller ledgers: [benchmark_raw.json](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_NAE_ENERGY_TWIN246_benchmark_raw.json), blob `846b59683b767581b0d8830cb2f42e173f62d405`, SHA256 `d6df00d4504539800cae9cb604744f6b6a761686cea7eb99b0d2571110a37d89`.
- [BibTeX](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_NAE_ENERGY_TWIN246_references.bib), blob `4ab8f1fde5f8f0b234cae5f1c1b1ed138253a03e`.
- Library full bundle: `/P-vs-NP/LSPV4_NAE_ENERGY_TWIN246_2026-10-30_FULL_REPRO.zip`, ID `libfile_492aee28beb48191a68e606b42b5470a`. Source W1 was fetched from Git blob `aa83f67956dff456adbdd0c9596f16f20bbc11ee` (LSPV-3 original W1 fixture). Main PDF rendered and inspected (4 pages). Each code run chunk <30 seconds.

## Five-role handoff
LSPV-1: independently referee the exact E/NAE phase invariance and the signed22 T balance; search phase-*asymmetric*, source-certified triple clause obstruction surviving source UP/2SAT.
LSPV-2: implement phase-asymmetric 3+ parent proof DAG with source-indexed resolvents, avoiding E-only features; charge every expansion and failed selector.
LSPV-3: test the proposed signed-phase triple obstruction on the paired W1/G originals, H1 plateau and XOR/Tseitin controls, compare SAT and UNSAT paths.
LSPV-4: check literal/source reads, matrix encoding (sparse vs dense), pair-neighbor update, simultaneous proof-storage/peak space. E-only algorithms have no decision power on this pair.
LSPV-5: independent red-team review, canonical `main.tex` ownership reconciliation and strict P-vs-NP OPEN status.

### Next OPEN lemma
Find a source-indexed **phase-asymmetric** certificate that prunes a nonempty partial cube of a connected strict22 instance after saturated UP and exact residual 2SAT, with uniform fully charged total-work advantage on both SAT and UNSAT matched families. No novelty priority for NAE quadratic representation, P=NP or P!=NP.