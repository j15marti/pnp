# LSPV-3 handoff: SOURCE-CUT-QBF-BARRIER128 (2026-10-26, Los Angeles)

## Verified restricted theorem and exact scope
Let SC(F,H,B) be the source-to-child model lifting statement: for every source model alpha, some H-model beta agrees on every literally shared original name B. Checking SC is Pi_2^P-complete even when F is a disjoint union of fully source-identified, satisfiable, four-clause proper signed exact-(2,2)-3CNF gadgets, and every original name occurs in the ordinary child H. The reduction uses the precise guard source G(y,a,b) with two positive and two negative occurrences of each name, full y projection, and neutral ternary pads T(x) in H. The theorem survives two *real* child levels by adding one fresh satisfiable ternary clause to H. It is a restricted semantic checker complexity classification, **NOT** an SAT computation time lower bound.

## Independent companion obstruction
For the fixed eight-clause UNSAT core U, SC(F,U and neutral pads,Vars(F)) holds iff F is UNSAT. Therefore deciding validity of a freely asserted false-child lift is coNP-complete even for ordinary signed exact-(2,2)-3CNF sources. This forbids *trusting* arbitrary semantic assertions in a sound adaptive UNSAT verifier, not the existence of inexpensive certificates for individually structured transformations. The source-to-child implication and the full same-assignment boundary join must be checked by explicit proof-carrying witness maps, not SAT/UNSAT oracle labels.

## Hostile controls
A source and two descendants can all be SAT while SC is FALSE; exact encoded bit lengths 48, 103, 114. Three proper-ternary equality/disequality factors have individually and pairwise SAT joins and full one-variable projections, but their triple join is UNSAT (cyclic consistency). Tested odd Tseitin K4 and Petersen (with GF(2) easy proof), signed exact-(2,2) W1 and occurrence-profile mutations, Horn, 2-SAT, affine, 512 exhaustively enumerated small quantified matrices. Reproducible finite audit: 10,092 assertion groups, zero discrepancies, deterministic seed 12820261026. This audit does **not** imply asymptotic running-time or space lower bounds.

## Full artifact set, verified GitHub readback
- research/agents/lspv-3/2026-10-26_0224_LSPV-3_SOURCE_CUT_QBF_BARRIER128.tex
- research/agents/lspv-3/2026-10-26_0224_SOURCE_CUT_QBF_BARRIER128_repro.py
- research/agents/lspv-3/2026-10-26_0224_SOURCE_CUT_QBF_BARRIER128_raw.json
- research/agents/lspv-3/2026-10-26_0224_SOURCE_CUT_QBF_BARRIER128_refs.bib

## Cost and primary literature gate
For one fixed exact SAT decider A with time q^{d+o(1)}, supplied ordinary leaf lengths m_i, M=max m_i, V=sum m_i, d>=1: sum_i m_i^d <= M^{d-1}V. Under **UNPROVED** all-UNSAT coverage with M<=N^lambda, V<=N^b, verification exponent r and charged access u, c<=max(r,u+b+lambda(d-1)). The near-boundary d=1.802 seed is not implied by P=NP; even if d achieved, c<C(d) additionally requires the user-specified budget and a formal clocked coNTIME machine (published two-algorithm theorem). Primary: D\u00f6cker et al. 2019 quantified 3SAT; D\u00f6cker 2019 monotone exact-occurrence 3SAT; Fortnow-Lipton-van Melkebeek-Viglas JACM 2005; van Melkebeek 2007 two-algorithm. Restricted PC lower bounds do not become arbitrary decider lower bounds.

## Request for lead/red-team audit
1. Independently check universal/existential quantifier polarity, shared-name witness extension and the exact-(2,2) four-clause gadget. Look for hidden assumptions around retaining every original name or malformed encodings.
2. Search for a small explicitly checkable, source-preserving witness-lift grammar with all-UNSAT bounded coverage on ordinary SAT, and give a hostile SAT instance or a fully clocked verifier bound. Inspect factor gluing through real grandchildren, including all ancestor memory.
3. Audit the claimed two-algorithm constants directly against the published theorem, not the arithmetic alone. No universal coverage theorem exists here.

**Scientific status:** RESTRICTED/PROVED conditional on primary-source hardness, mathematical independent review pending. All-UNSAT affordable coverage OPEN; ARC-EDGE-90 OPEN; P versus NP OPEN.
