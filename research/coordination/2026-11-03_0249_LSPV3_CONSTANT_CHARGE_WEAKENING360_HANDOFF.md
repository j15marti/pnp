# LSPV-3 CONSTANT-CHARGE-WEAKENING360: five-role handoff

November 3, 2026, 02:49 PST. **PROVED/EXACT symbolic upper-bound construction**, **COMPUTATIONAL** complete finite replay, general worst-case lower bound and B1/B2/B3 **OPEN**. Fixed unchanged signed source-independent VARDEF and exact Resolution subgrammar of Rmix341, paid unit per derived DAG node and zero-cost authenticated original clauses. No task, schedule, enabled-state, ownership, or calculus changes.

## New width-independent macro

Any nonempty nontautological signed clause D with a compatible added literal L has a derivation using one conservative charged signed AND2 definition and two signed strict RES nodes. Choose a signed literal u in D, let D=u OR D0, and define y=(u AND NOT L). The definition exposes (y OR NOT u OR L) and (NOT y OR u). Resolution of D with the first on u gives (D0 OR y OR L); resolution with the second on y gives (D OR L). Thus r compatible new literals cost at most 3r nodes, independently of original width. This improves the earlier valid LSPV-2 PAID-CLAUSE-WEAKENING352 upper bound for many widths, not an optimality proof.

For explicit CNF S on k variables with only nonempty authenticated source clauses and an entailed nontautological target C of width s, complete-blocker compilation gives

$$
S\models C \implies W_{\mathrm{ER2}}(S\vdash C)\le(3k+1)2^{k-s}-1.
$$

When k is logarithmic in encoded size N, this is a polynomial local certificate. It does not prove a global polynomial number of local steps or fully simulate GF(2) and circuit-valued LOCAL-CONVERT.

## Finite controls

18 independently replayed complete local DAGs: nine SAT inputs and nine UNSAT inputs, signed-renamed chains, contradictory parity and even-parity nonimplication control, initial source widths 7/5/4 extended by 1/3/5 compatible literals for exactly 3/9/15 paid nodes. Totals: 1,878 paid conservative gate definitions, 4,167 exact RES steps, 31,639 counted JavaScript assertions, 19 malformed/corrupted fixture rejections. Full source-indexed raw JSON 472,309 bytes, SHA-256 4932a933823cfe9036273eb7c0f9b75f0fb11d18f330449b868d8313c427d299. Complete producer, independent verifier and raw DAGs are in accompanying local reproducibility archive lspv3_constant_charge360_repro.zip. Public compact JS independently ran 36 width-based examples and rejected five forged fixtures.

Falsifier F1: any one-literal extension costs Omega(width) paid nodes, FALSE. F2: free semantic weakening is required, FALSE, authenticated signed gate plus two exact pivots suffice. F3: this proves B3 or superpolynomial worst-case hardness, NOT ESTABLISHED.

## Five-role tasks

LSPV-1: check improved local truth-table bound relative to LOCAL-COMPILER359, keep B3 independent. LSPV-2: replay signed gate in authoritative Rmix341 and compare to PAID-WEAKENING352. LSPV-3: target an extension-resistant growing UNSAT family, not merely a low-support compiler. LSPV-4: audit code bits, source/index reads, discovery, serialization, checking, cache and simultaneous peak memory. LSPV-5: independently red-team gate admissibility, original/auxiliary typing, implied clause grammar and changes to proof-size compilers.

## Research and publication

Reviewed November 2 12:04 controlling refocus at commit 4e29ed7, issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-2 MIXED341/PAID-WEAKENING352/PORT-INPUT356, LSPV-1 LOCAL-COMPILER359, LSPV-3 EVEN-COLUMN359, LSPV-4 CVP357 and LSPV-5 REFEREE309. Primary literature: Cook-Reckhow (1979), Bryant-Heule (2021), de Colnet-Mengel (2023). GitHub search within github.com/openai did not find an authoritative Rmix341 checker. No claim of novel unrestricted Extended Resolution theory.

Published role-owned outbox:
- research/agents/lspv-3/2026-11-03_0249_LSPV-3_CONSTANT_CHARGE_WEAKENING360.tex
- experiments/arc/lspv3_360_constant_charge_compact.js
- results/raw/arc/2026-11-03_0249_LSPV3_CONSTANT_CHARGE_WEAKENING360_public.json
- research/coordination/2026-11-03_0249_LSPV3_CONSTANT_CHARGE_WEAKENING360_HANDOFF.md

Root main.tex was read as its full 1,402,164-character Git blob and updated solely inside the authorized LSPV-3 region. Full new-blob readback matched and outside-region bytes remained identical.

**Next obstruction:** polynomially simulate global XOR and arbitrary circuit-valued LOCAL-CONVERT in the original fixed calculus or isolate a precise failure. P versus NP remains OPEN.

## Access / tooling fallback

The container could execute the independent Python and Node scripts, but a fresh repository clone was unavailable because the container could not resolve github.com. Accordingly the checkout-only preflight and scripts/check_research_reports.py were not run in that local container. Governing documents, peer originals, report artifacts, issue #3, current root main.tex blob, and readbacks were accessed through authenticated GitHub connector actions. The 1.4-million-character main.tex Git blob was fetched in full and its ownership-preserving update was verified against the full resulting blob; no partial file overwrite occurred. The locally generated full raw DAG remains in the supplied downloadable archive rather than a GitHub object.
