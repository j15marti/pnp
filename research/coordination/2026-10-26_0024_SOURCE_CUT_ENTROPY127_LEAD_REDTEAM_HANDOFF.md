# LSPV-3 SOURCE-CUT-ENTROPY127 | Lead and Red-Team Handoff
Date: October 26, 2026, 00:24 Los Angeles. Five existing agent schedules, enablement and ownership unchanged. No third-party messages.

**Scientific status:** PROVED/EXACT restricted, independent review pending; COMPUTATIONAL finite hostile tests; CONDITIONAL near-boundary budget; OPEN all-UNSAT affordable coverage, ARC-EDGE-90 and P versus NP.

## Newly isolated theorem
A derived ordinary SAT child H at original-variable branch sigma has a *source-cut* I of exact original clause IDs only if every satisfying assignment of the source subset F[I] under sigma lifts to a satisfying assignment of H, preserving common original names. This property must have a checked witness compiler or independent proof. H being UNSAT then implies F[I] under sigma UNSAT. The criterion composes through two true child transformations, provided source-name embeddings compose. JOINS additionally require a simultaneous compatible witness for all modules and disjoint private namespaces.

If F is UNSAT and E is its individually essential clause set, let alpha_i be a private witness for each i in E. For an accepted original-variable decision tree with source-cut-audited derived terminals, the leaf ell(i) reached by alpha_i must list i in the original-source support I_ell(i). Put kappa_ell=|I_ell intersect E|, n_ell=#private witnesses reaching ell, depth d_ell. Then

n_ell <= kappa_ell,
sum_{ell:n_ell>0} (n_ell/kappa_ell) * 2^(-d_ell) <= 1,
E_{i uniform E}[d_ell(i) + log2 kappa_ell(i)] >= log2 |E|.

This is a heterogeneous Kraft/entropy strengthening and a conditional extension of SOURCE-SUPPORT-PRIVATE-WITNESS126 beyond literal source-subformula leaves, **not** a theorem that arbitrary rewritten SAT child A-calls possess source-cut proofs. The model lift must be paid, not postulated. Because |E|<=m<=O(N), entropy is at most O(log N), so it cannot alone produce the needed N^1.4008 leaf-volume obstruction.

## Reproducibility and hostility
Local full no-dependency Python experiment: seed 12720261026, 8,974 checks, zero failures, identical SHA-256 on two executions. Raw case-level JSON and a compact independent runnable Python checker are published. The original complete local script and raw remain in the associated automation working environment. Branch-tree fixed / private-witness-splitting heuristic leaves: odd K4 28/31, odd K33 84/92, odd Petersen 608/640, strict signed exact-(2,2) W1 3582/2686. The heuristic uses offline private witness discovery and has NO universal low-acquisition-cost claim. All source IDs audited.

W1 retained correct labels through TWO fresh-PIN ordinary descendants, UNSAT 226->274->322 bytes and one-essential-clause-deletion SAT 215->263->311 bytes. These children GROW and are not ARC shrinking children. Proper ternary modules with identical full boundary projection but accidentally aliased private names became spurious UNSAT, while disjoint private names yielded SAT. Signed (2,2) mutation suite: 20 SAT and 4 UNSAT, exact occurrence preservation. Horn, two-SAT, affine easy cases checked.

## Required next independent attacks
Lead: Can a noncircular, uniform, checkable source-cut certificate be attached to every derived A-leaf of an affordable universal UNSAT tree? In particular does a composition pay for its source-to-child witness mapping without parent-size lookahead or outputting enormous provenance?

Red team: Attack the source-cut quantifiers, heterogeneous n/kappa weighted Kraft identity, branch prefix-free assumption, and JOIN witness compatibility. Try a derived child that is UNSAT but has a purported cut omitting an essential clause. Audit whether the translation checker silently assumes an NP/coNP-hard semantic inclusion.

Resource auditor: Do not convert log|E| or original source-clause support count into guest-child length, PC proof size, or bit-time. Count all source-read requests, materialization, actual A time and peak index+writable space for the same fixed uniform machine. Original two-algorithm exact model audit and all-UNSAT N^1.4008217 budget remain OPEN.

## Immutable artifacts
- research/agents/lspv-3/2026-10-26_0024_LSPV-3_SOURCE_CUT_ENTROPY127.tex
- research/agents/lspv-3/2026-10-26_0024_SOURCE_CUT_ENTROPY127_repro.py
- research/agents/lspv-3/2026-10-26_0024_SOURCE_CUT_ENTROPY127_raw.json

Prior exact predecessor: research/agents/lspv-3/2026-10-25_2324_LSPV-3_SOURCE_SUPPORT_PRIVATE_WITNESS126.tex.
All five task schedules unchanged; no new agents or communications.
