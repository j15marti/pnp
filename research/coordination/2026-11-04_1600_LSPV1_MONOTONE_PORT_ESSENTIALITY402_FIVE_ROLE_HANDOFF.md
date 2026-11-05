# LSPV-1 / 402 coordination, 2026-11-04 16:00 PST

PROVED/EXACT, pending independent review: Essentiality of a named input in monotone shared fan-in-two AND/OR circuits is NP-complete under logspace reductions. Given signed CNF H, introduce flags a_i,b_i; set G=AND_i(a_i OR b_i), B=OR_i(a_i AND b_i), Q=B OR OR_{clauses D} AND_{literals ell of D} falseflag(ell), and C=Q OR (t AND G). The port t is essential exactly if H is SAT. No hardness for full Rmix341 or arbitrary SAT deciders follows.

IDEA: test syntactic monotone support under reconvergence. SEARCH: project directives, issue #3, all five current roles, primary SAT/CVP literature, Grok 2026-11-04_2315, Claude ONETAPE-0001, OpenAI math SAT cost Lean source. ITERATE: disjoint-cone support is exact (existing LSPV-3/404), but reconvergent semantic support is NP-complete. Direct branded Google unavailable; general web/GitHub were searched.

COMPUTATIONAL: all 256 proper signed two-variable CNFs (95 SAT, 161 UNSAT), 8,210 Python assertions, 6,626 paired cofactor evaluations; 5,322 independent JavaScript checks; even/odd K4 Tseitin 8/0 models, malformed/corruption controls. Code, report and raw records at:

research/agents/lspv-1/2026-11-04_1600_LSPV-1_MONOTONE_RECONVERGENT_PORT_ESSENTIALITY402.tex
experiments/arc/lspv1_402_monotone_port_producer.py
experiments/arc/lspv1_402_monotone_port_independent.js
results/raw/arc/2026-11-04_1600_LSPV1_MONOTONE_PORT402_raw.json

LSPV-1: B1/B2/B3 and one-policy bridge; LSPV-2: native mixed gate and affine shortcuts; LSPV-3: exact named-port/auxiliary semantics; LSPV-4: fully charged work/space; LSPV-5: adversarial audit of the reduction and invalid computational inference. Existing task identities, enabled states, schedules, original mixed rules and weights unchanged.

Root main.tex returned a blob SHA but zero content; no potentially destructive edit was attempted. B1/B2/B3, superpolynomial worst-case full Rmix341 lower bound, and P versus NP remain OPEN.
