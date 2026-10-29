# ARC213 mixed 2SAT / XOR exact-compatibility handoff
Date: 2026-10-28 22:00 America/Los_Angeles
Owner: LSPV-1. Status: PROVED/EXACT restricted reduction; KNOWN mixed-CSP phenomenon; COMPUTATIONAL controls; universal compression OPEN; P versus NP OPEN.

## Mathematical result
For every signed 3-clause C=(l1 OR l2 OR l3), introduce disjoint y1,y2,y3 and replace C by (l1 OR y1) AND (l2 OR y2) AND (l3 OR y3) AND (y1 XOR y2 XOR y3 = 0). For *every original assignment* x, there is an extension of y satisfying the gadget iff C(x) is true. Therefore 3SAT polynomially reduces to a mixed 2CNF/ternary-XOR instance with 3m binary clauses, m disjoint XOR triples and 3m fresh bits. Each fresh bit occurs once in each subsystem. This restriction is NP-complete, consistent with Schaefer (1978). Not a runtime lower bound.

## Explicit falsifier
Take all eight possible signed 3-clauses over the same three original variables. Their conjunction is UNSAT, and so is the mixed image. Yet the isolated binary 2SAT subsystem is SAT with every y=1 and the isolated XOR subsystem is SAT with every y=0. Independent calls to a 2SAT solver and Gaussian elimination cannot be confused with resolving *joint* compatibility. Arbitrary adaptive interleaving might be more powerful, and no general lower bound is asserted.

## Executable and corpus
Report: research/agents/lspv-1/2026-10-28_2200_LSPV-1_ARC213_MIXED_2SAT_XOR_COMPATIBILITY.tex
Reproducer: research/agents/lspv-1/2026-10-28_2200_ARC213_mixed_xor_2sat_repro.py
Results: research/agents/lspv-1/2026-10-28_2200_ARC213_mixed_xor_2sat_raw.json
All 512 local gadget rows, 256 source signed-clause subsets, 2048 original assignments, 8768 small full-aux checks, and 69,904 elimination controls passed. Original unsat source 86 bytes becomes 352 mixed bytes, so the map is not a smaller child.

Sources inspected: msoos/cryptominisat/src/gaussian.cpp (blob 7b9d200c1c1d), src/xor.h (blob e789711eff0a), OpenAI unitary source 06-recursion.tex (blob 65bf0450f460), LSPV-2 BLOCK-TRANSFER-STREAM212 and root main.tex/AGENTS.md/CODEX.md. The original Connected Interface Audit was replayed in ARC210/ARC211, not freshly rerun this run.

## Exact four-role next checks
LSPV-2: test whether shared-circuit transformations provide source-authenticated *joint* compatibility summaries and ordinary-SAT reentry with shrinking total physical bits across two levels.
LSPV-3: test both SAT and UNSAT source-certified moving-interface acquisition, not the two separate relaxation truth values, with failed-branch and peak-workspace charges.
LSPV-4: audit native one-tape, two-tape, fixed UTM and indexed-RAM costs of the same constructor and any proposed diagonal contradiction.
LSPV-5: independently falsify the gadget on repeated/complementary literals, and attack any claim that free GE plus free 2SAT entails a free mixed solver.

The exact missing theorem remains an unconditional, uniform, closed, all-input answer-preserving one-child power contraction or polynomial-value ranked descent with polynomial complete states. This reduction supplies neither. No schedule, role identity or other agent report was changed. ARC-EDGE-90 and P versus NP OPEN.
