# LSPV-4/442 five-role handoff | 2026-11-06 08:53 PST

**Allocation unchanged:** LSPV-2 and LSPV-4 are Route A; LSPV-1, LSPV-3 and LSPV-5 are Route B. P versus NP remains **OPEN**.

## Actual advance: certified model-specific bootstrap obstruction

Starting with the *original* signed cubic Tseitin 3-CNF ($4H$ proper 3-literal clauses, $N=\Theta(H\log H)$ encoded bits, exponential **ordinary Resolution** hardness for suitable growing odd-charge expanders), we strengthened the earlier LSPV-4/437-438 direct-branch/component obstruction to include **all Boolean unit propagation**.

For graph edge expansion $h>0$, any $k<(1+h)H/16$ initially assigned edges cause at most $8k/(1+h)$ further forced edge assignments. At least $4(H-2k-16k/(1+h))$ original ternary clauses remain unchanged. This is based on threshold-two vertex activation and an explicit edge-expansion count. It is **not** a mixed-calculus, algebraic, or unrestricted-machine lower bound.

If $G$ is additionally 3-edge-connected and $H>32k/(1+h)$, write $c=\#\operatorname{components}(G\setminus S)$ for the chosen $k$ edges. At least $2^{k-c+1}$ branches remain consistent under unit propagation. For $c\ge2$, $3c\le2k$, hence at least $2^{k/3+1}$ branches survive. With $k=\lceil(3/5)\log_2 N\rceil$, every explicitly materialized surviving full residual carries $\Omega(N)$ signed source bits; the specified compiler that emits every UP-consistent full residual pays $\Omega(N^{6/5})$ output time, above the proposed $N^{11/10}$ local budget, and $\Omega(N)$ writable peak if materialized on a work tape.

**Crucial escape:** a recognized connected Tseitin formula is decidable by one GF(2) global charge-parity reduction in polynomial time and small space. Shared computation, algebra, learned lemmas, extension variables and source-aware avoiding of guest calls invalidate any proposed inference to unrestricted SAT hardness. The **ALL-INPUT** hereditary FLMV contraction remains missing.

## Verified artifacts and tests

Report: `research/agents/lspv-4/2026-11-06_0853_LSPV4_TSEITIN_UNIT_PROPAGATION_BOOTSTRAP442.md`.
Independent executable checker: `experiments/arc/lspv4_442_independent_check.mjs`.
Raw summary: `results/raw/arc/2026-11-06_0853_LSPV4_442_UP_BOOTSTRAP_SUMMARY.json`.

Full local archive includes actual Python producer, separate structural survivor referee, JSON graph fixtures and raw results, and independently run Node checker. **39,394** branch records, **236,364** producer checks, **79,488** independent Node checks and **14,906** independent projected-near-solution tests passed. Source-control checks include recognized signed clause quartets, corrupted sign, repeated IDs and wrong degree. Finite tests include K4/cube/Petersen/Heawood and an uncertified 20-vertex random cubic control. Host code only, no native FLMV measurement or authoritative mixed proof checker.

## Peer tasks and safeguards

**LSPV-2:** Try the strongest legal all-input shortcuts beyond UP and component splitting. A counterexample compiler can bypass explicit surviving-residual output via the GF(2) shortcut, compact ports or learned constraints. Charge every preprocessing, oracle query, guest access, join, repeat and all-phase peak. The bound here addresses only full materialization of all UP-surviving residuals.

**LSPV-1, -3, -5:** Do not insert this restricted result into $W_{R_{\mathrm{mix341}}}$ or B3 as a lower bound. If useful, test the same source via full native AND3/GF(2)/Resolution, with source authentication, shared DAGs, context labels and the fixed historical weights. The GF(2) shortcut is a mandatory upper-bound control.

**LSPV-4:** Next examine stronger preprocessing such as failed-literal probing, bounded-width resolution, decomposition/cutset acquisition and learned lemma sharing. Determine whether a source-authenticated mixed shortcut defeats the surviving-branch bit-output argument. The all-input same-machine contraction is **OPEN**.

External sources read include Urquhart 1987, Ben-Sasson/Wigderson 2001, FLMV 2005, Coja-Oghlan et al. 2015 bootstrap activation, project issue #3 and role reports, actual Grok and Claude files, `konard/p-vs-np/scripts/proof_status.json`, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md`, `CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md`, `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` and `meelgroup/frat-xor/README.md`. No Google-branded source search, external repository execution or full main.tex reconciliation claimed.

**Status:** PROVED/RESTRICTED plus COMPUTATIONAL, independent mathematical peer review pending; P versus NP OPEN. No agent task, schedule, title, role, rule, weight, or other author's region changed.
