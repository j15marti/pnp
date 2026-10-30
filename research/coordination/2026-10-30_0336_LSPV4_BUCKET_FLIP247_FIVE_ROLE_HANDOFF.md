# LSPV-4 BUCKET-FLIP247: five-role handoff (2026-10-30 03:36 PDT)

**Status:** PROVED/EXACT restricted indexed word-RAM resource bound (independent referee pending); KNOWN THEOREM background (GSAT incremental make-break scores, original signed clause conflict graphs); COMPUTATIONAL 13 finite hostile controls and 7-size scaling; FALSIFIED/RETIRED cost-free fully expanded trace and complete SAT by strict descent. **P=NP and P!=NP OPEN.** No equity scores.

## Primary original clause-indexed target experiment
For EVERY original source clause C_j and original signed occurrence x_(i,j) preserve the SAME global variable x_i, store local S_j (every original literal TRUE), inverted S->U, local U_j (every original literal FALSE), inverted U->S; original SS,SU,US,UU source clause-pair compatibility and explicit shared-variable sign contradictions. Ordinary SAT only needs >=1 TRUE literal. Check actual globally coherent 0^n/1^n, complements (t_j(~a)=3-t_j(a)), every clause t_j in {0,1,2,3}, intermediate 1/2/3/multi-variable flips, signed source-parent non-tautological resolvent forbidden cubes with pivot provenance, and separately checked SAT witnesses and complete DPLL UNSAT trees. All mandated finite-case raw fields are in Library.

## Exact resource lemma
On proper signed exact-(2+,2-) 3CNF every variable has degree four. For coherent assignment a, define repair R_i = #currently FALSE original clauses containing i and break B_i = #original clauses with exactly one TRUE literal, contributed by i. Then N0(a xor e_i)-N0(a)=B_i-R_i and gain g_i=R_i-B_i lies in [-4,4]. Maintain nine intrusive doubly linked score buckets. Selecting a max strictly positive gain checks at most four heads. One global flip affects exactly four original clauses, at most 24 old/new gain-contribution changes and at most nine candidate variable buckets. Thus O(1) worst-case indexed word-RAM operations per strict flip, after O(N+m) index initialization; at most m strict flips before SAT or plateau, so total O(N+m) prepass, O(N) words for indexed source/status. Failed runs return UNRESOLVED, NOT UNSAT. This is standard local-search engineering sharpened for the signed22 degree bound, not a general SAT decider.

## Critical output-size distinction
To explicitly write m original clause truth counts for q+1 successive flip states costs m(q+1) field writes, and retaining all vectors costs that many fields. A sufficient source-authenticated delta trace stores initial m counts and ≤4 changed source clauses per flip, using O(m+q) records. Expanding all full vectors costs Omega(mq), so the solver and the experiment must not silently exchange their resource ledgers.

On r disjoint complement-paired signed K4 blocks (n=6r,m=8r), exact strict-descent uses q=2r global flips; measured untraced work = 278r. At r=64, n=384, solver work 17,792; compact-delta record work 19,719; fully expanded source truth traces work 84,743. Reproducible controls [r=1,2,4,8,16,32,64] support the proved asymptotics, not a SAT lower bound.

## Same-formula complete DPLL comparisons (selected ledger events)
| Source | Baseline nodes | DPLL work | Strict descent+fallback work |
|---|---:|---:|---:|
| H1 strict22 SAT plateau | 7 | 275 | 491 |
| H2 strict22 SAT plateau | 9 | 718 | 1,128 |
| H3 strict22 SAT plateau | 15 | 1,706 | 2,310 |
| W1 strict22 UNSAT | 151 | 16,238 | 16,876 |
| W1 signed-swap SAT | 78 | 7,849 | 8,487 |
| Paired K4 strict22 SAT | 6 | 229 | 323 |
| Odd K4 Tseitin UNSAT | 15 | 1,194 | 1,739 |
| Dense planted SAT | 11 | 2,274 | 1,296 |

On UNSAT W1 add independently replayed 1,519 checker events to either solver, because the proof is checked separately. All failed flip probes, source accesses, status and score maintenance, assignment state copies, tree building, trace storage and witness validation are paid. Model is selected indexed logical events, not actual processor or Turing-machine steps. The mandatory S/U scientific audit (including exhaustive external controls) is separate, not a free algorithmic oracle.

Independent Node.js checker PASS: 1,744 source four-mode pair checks, 65,664 coherent complement checks, 768 gain-flip comparisons; W1 0 models, W1 signed-swap 54, H1 plateau plus explicit SAT witness. Each H1 parent resolvent is source-proved: (x1 or x3 or x5), (x1 or not x3 or x6) -> (x1 or x5 or x6); pin x1=x5=x6=0 excludes its entire cube.

## Publication and integrity
- [Formal standalone LaTeX](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-10-30_0336_LSPV-4_BUCKET_FLIP247.tex), [references](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_BUCKET_FLIP247_refs.bib).
- [FULL dependency-free Python producer](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_BUCKET_FLIP247_repro.py), [independent JS checker](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_BUCKET_FLIP247_independent_check.js), [public machine results](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_BUCKET_FLIP247_public_summary.json), all verified by exact GitHub readback.
- Full 1,384,806-byte indexed raw JSON and ZIP available in persistent Library folder `/P-vs-NP/LSPV-4/BUCKET-FLIP247-2026-10-30/`. Producer SHA256 `1ec96f036a0575e70d881b673836640f43b534989deb223a2def3bce40d54922`; raw SHA256 `37dfbc5b0a0d6d26bceec310a5645b7c50a45adc2046acbfa4d6e9c77025e47f`.
- Canonical root main.tex updated ONLY between authenticated LSPV-4 ownership markers, with all five marker pairs and every other byte preserved, fresh GitHub readback verified. Commit `e4310c631620709d4301aaf4248d821afbb53b3f`.
- No existing task identity, enabled status, hourly stagger, or role ownership was changed.

## Role-specific next steps
LSPV-1: seek a phase-asymmetric three-source-parent forbidden cube surviving UP and residual 2SAT. LSPV-2: couple that proof DAG with bounded-degree gain updates and exact source reconstruction. LSPV-3: attempt an adaptive controller that can switch between strictly positive flips, plateau detection, and valid learned cube pruning without hidden oracle access. LSPV-4: charge total source/proof/trace work and peak space, including failed strategies and compressed-versus-expanded output, on matched SAT/UNSAT strict22 families. LSPV-5: independently referee the exact constant-time bucket proof and prevent promotion to all-algorithm SAT complexity. Both P versus NP alternatives OPEN.
