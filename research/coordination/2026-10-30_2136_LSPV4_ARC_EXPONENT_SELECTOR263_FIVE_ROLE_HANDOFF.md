# LSPV-4 ARC-EXPONENT-SELECTOR263 | 2026-10-30 21:36 PDT
**Status:** restricted conditional computability reduction PROVED/EXACT in report, independent mathematical review pending; finite COMPUTATIONAL; universal ARC and P versus NP OPEN. No scheduler changes.

## Four falsifiers
F1: arbitrary correct polynomial SAT guest code admits a computable exact eventual exponent classifier (false conditional on SAT in P by a two-counter halting reduction).
F2: finite timings reveal the eventual exponent (false, a halting-after-40 CM2 wrapper mimics a nonhalting one on smaller budgets).
F3: time padding necessarily consumes polynomial writable space (false: binary counters and bounded CM2 simulation use O(log N) extra FLMV counted space).
F4: F1 failure prevents any code-oblivious all-input ARC compiler (not established; invalid extrapolation).

## Exact specialist contribution
For any fixed polytime exact SAT decider A with a finite runtime exponent K, choose fixed integer D>K+2. For arbitrary two-counter machine M, compile B_M which scans source length N, simulates M for N steps, delays >=N^D steps if not halted, then calls A on the unchanged source. Every B_M is a correct total polynomial SAT decider, same-source YES/NO. Its extra counted space is O(log N). If M halts, B_M has eventual worst-case time O(N^K); if not, it requires Omega(N^D). Thus a total program-code selector deciding membership in O(N^{D-1}) among promised polynomial SAT deciders would solve the undecidable CM2 halting problem. Conditional on SAT in P only. This is a classical halting-technique specialization, not an arbitrary SAT lower bound or obstruction to a K-oblivious compiler.

## FLMV exact audit
d*(6/5)=23/45, d*(241/200)=11642479/23232400, both k=2 with exact k>=4 tail bounds. Same-machine simultaneous strict time and space. (6/5,1/2) remains only a conditional fixed point.

## Controls
Producer: 1,312,668 complement/pair checks; independent Python formulation run locally: 1,312,240 checks on the authenticated 15-variable/20-clause W1/S15 pair. W1 zero models and DPLL nodes 151/work 11555, S15 861 models and DPLL nodes 9/work 784. Pair matrix and per-occurrence targets are in raw; also XOR3 and Horn SAT/UNSAT, complete endpoints, flips, resolution proof cubes. Adding full pair/endpoint diagnostic increased selected work to 13385 (W1) and 2614 (S15). Instrumented event counts, not native FLMV TM transitions; no industrial CDCL comparison.

## Corpus / dependencies / handoff
Read 09:48 REDIRECT1, CONTRACT1, AGENTS, CODEX, pnp-research skill, current root main, AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted semantics only), CONSTRUCTION-STRENGTHEN17 (missing strict22 bit-emitter), ARC-LINEAR22-SATURATION1 (easy global orbit countercontrol), recent LSPV-1/2/3/5 issue #3 results and LSPV-4 COVER-GATE-SCOPE262. Primary: FLMV 2005 JACM Theorem 5.7 and machine model, Dudenhefner 2022 FSCD Definition 2 and Theorem 6, Blum 1967 JACM.
**Single open arrow:** one K-oblivious, all-input, hereditary, both-label-correct Phi producing truly power-short ordinary-SAT children with paid source, selector, failed routes, output-bit access, guest head/index operations, ancestor retention, replay, peak combined space and strict FLMV exponents. Continue precisely this direction. Preserve original clause S/U as hostile controls, not main route. P versus NP OPEN.

Artifacts:
- research/agents/lspv-4/2026-10-30_2136_LSPV-4_ARC_EXPONENT_SELECTOR263.tex
- research/agents/lspv-4/2026-10-30_2136_LSPV4_ARC_EXPONENT_SELECTOR263_repro.js
- research/agents/lspv-4/2026-10-30_2136_LSPV4_ARC_EXPONENT_SELECTOR263_independent_check.py
- results/raw/arc/2026-10-30_2136_LSPV4_ARC_EXPONENT_SELECTOR263_raw.json

END_OF_VERIFIED_HANDOFF::LSPV4_ARC_EXPONENT_SELECTOR263::P_VS_NP_OPEN
