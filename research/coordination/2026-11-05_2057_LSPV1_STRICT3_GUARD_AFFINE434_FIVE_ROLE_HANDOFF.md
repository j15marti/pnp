# LSPV-1/434: Strict-3CNF guarded affine-hull firewall, five-role handoff
**2026-11-05 20:57 PST, America/Los_Angeles. Route B LSPV-1 lead.** Scientific status: PROVED/RESTRICTED semantic and ordinary strict-Resolution claims (independent specialist review pending); COMPUTATIONAL reproducible finite checks; historical full-mixed lower bound, B3 and P versus NP OPEN. Preserve exactly five agent identities, 2 Route A / 3 Route B, all fixed weights, schedules and history.

## Target, idea and falsifiers
Beginning with **published ordinary-Resolution-hard cubic expander odd-Tseitin proper 3-CNF**, test whether LSPV-1/432's affine-hull SAT-search acquisition already supplies paid source-authenticated mixed proof. F1: guard 3CNF fails exact projection; F2: affine hull has hidden extra equations; F3: even-charge positive control forces a guard; F4: SAT-oracle negative answer is improperly treated as a native proof step. F1–F3 falsified by symbolic construction and executed finite controls. F4 remains the decisive B3 gap.

## Rigorous scoped result
For proper signed 3CNF F=AND_i(a_i OR b_i OR c_i), introduce shared g, private y_i and exact strict-3 source
$$
G_3(F)=\bigwedge_i[(g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)].
$$
For every assignment x, there exists y with G3(g=0,x,y) iff F(x). When F is UNSAT, G3 is SAT and its complete model affine hull is **exactly the single hyperplane g=1**, dimension n+m; all n original and m auxiliary coordinate directions occur in model differences. If F is SAT, its affine hull is the full ambient space. This is a semantic statement, not a cheap R_mix341 inference.

For any SAT source G containing g **only positively**, with G entails g, and H=G|g=0, strict oriented shared-DAG Resolution satisfies
$$
L_{\mathrm{Res}}(G\vdash g)=L_{\mathrm{Res}}(H\vdash\bot).
$$
Erase g from every line of a G derivation (never pivoted), or lift H source lines retaining their original g occurrence; topology and paid distinct Resolution nodes are preserved in both directions. **DO NOT CLAIM** the strict3 splitting H has the same ordinary Resolution complexity as unsplit F: equisatisfiability does not imply lower-bound preservation. Nor does the restricted isometry cover all native AND3/GF2/LOCAL/DEF.

Published hard-anchor ledger: odd cubic Tseitin on suitable expanding h-vertex graphs has 4h proper width3 original clauses, 3h/2 original edge variables, Theta(h log h) encoded bits; Urquhart and Ben-Sasson/Wigderson ordinary unrestricted shared-DAG Resolution lower bound 2^Omega(h). Known native semantic mixed AND3/GF2 construction has only 4h-1 paid nodes, preventing full-mixed hardness transfer. Transformed G3 has 8h strict3 clauses, 11h/2+1 variables, Theta(h log h) bits; no Resolution-hardness transfer to cofactor asserted.

## Checks and resource firewall
Python full original-source producer: **298,490** assertions; Node full independent original-source K4 certificate checker: **2,196** assertions, **six** rejected malformed/corrupt controls; independent compact Node: **298,220** assertions. Odd source K4/K33/Cube guarded G3 (source clauses 32/48/64, variables 23/34/45) has exact model affine ranks 22/33/44; even controls ranks 23/34/45. Exhibited strict RES goal-(g) proof has 47/99/215 paid nodes (not proved optimal). The full local reproducibility ZIP contains executable Python, independent Node checker, raw sources/JSON, K4 47-node certificate and checksums. Public summary JSON and standalone compact JS reproduce principal controls, not the historical native checker.

Actual host producer ~1.08 s / ~96,780 KiB observed max RSS; native-TM work and all-phase peak space are not inferred. Paid node minima exclude discovery by intentional relaxation; real construction/search/index reads/restarts/output/checking/recomputation/retention incur cost. Original R_mix341 private/exported-wire and LOCAL grammar and noncircular B3 remain OPEN.

## Role handoff
LSPV-1: focus noncircular B3 and historical rule authentication; do not promote affine-hull acquisition to proof without an accepted source-bound derivation. LSPV-3: independently replay original K4 certificate, audit strict3 source-to-cofactor restriction and any full-mixed legal shortcut. LSPV-5: try counterexample to positive-only-g strict-Resolution isometry, negative controls and hidden definitional/LOCAL gates; do not infer full mixed hardness from syntactic guard. LSPV-2 and LSPV-4 (Route A): use these as known shortcut/semantic-decision controls only, preserving all-input same-machine recursively iterable FLMV contraction requirement; no new task changes.

New files: `research/agents/lspv-1/2026-11-05_2057_LSPV-1_STRICT3_GUARD_AFFINE_FIREWALL434.md`; `experiments/arc/lspv1_434_strict3_guard_compact.mjs`; `results/raw/arc/2026-11-05_2057_LSPV1_STRICT3_AFFINE_GUARD434_summary.json`; and this handoff. Root `main.tex` returned existing SHA but **no readable bytes**; it was not edited. P versus NP OPEN.
