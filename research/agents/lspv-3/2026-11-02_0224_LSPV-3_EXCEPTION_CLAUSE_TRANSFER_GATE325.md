# LSPV-3 GATE325: Paid exception-clause transfer for same-original SAT/Circuit-SAT

**2026-11-02 02:24 PST. PROVED/EXACT restricted; independently COMPUTATIONAL; external review pending. P versus NP OPEN.**

## One exact obstruction and three falsifiers

The connected canonical cyclic F9 family G_t admits a polynomially acquired 2x2 boundary transfer for every coherent original pin (prior GATE324), despite its exponential ordered cofactor and antichain widths (prior GATE323/324). Does a few genuinely cross-block original source-clause edits defeat this decision-only escape? Tests: F1, directly reuse G_t transfer after edits, **FALSIFIED**; F2, use fully paid finite inclusion-exclusion for the exceptional clauses, **PROVED**; F3, two cross-block edits force exponential work for every SAT decider, **FALSIFIED by a polynomial restricted terminal**. This does not settle all-input complexity.

## Exact theorem

Let F be a grammar-validated proper, duplicate-free Döcker monotone 3-SAT-(2,2) original on n=9t **numbered original variables** and 12t original clauses. Let G_t be the authenticated cyclic F9-splice template. Compare original clauses as unordered signed triples. Put D=G_t\F, A=F\G_t, H=G_t\D, k=|A|=|D|. H retains the exact two-bit cyclic interface across blocks; A may be arbitrary long-range original clauses. For every coherent original-variable cube p and subset J of A, let q_J force every signed literal of clauses in J FALSE, taking Z_J=0 if pins conflict. Otherwise acquire by source enumeration the 2x2 integer local matrices W_i^(p+q_J), checking each of the 4*256 private/boundary original-variable assignments against the 12 original source-clause slots in block i. Set Z_J=trace(product_i W_i).

**Theorem:** #SAT(F|p) = sum_(J subset A) (-1)^|J| Z_J. In particular SAT iff this nonnegative integer is positive; when it is zero the source-authenticated local tables plus checked alternating sum constitute a complete counted UNSAT certificate.

**Proof:** An assignment satisfying H and p satisfies F iff it satisfies all clauses in A. Expand the indicator product over C in A of (1-[C false]); each J term is the number of assignments satisfying H,p and every C in J false. The forced literal pins give q_J, or zero if incompatible. Factor H's original-source clauses over private blocks conditional on adjacent boundary bits. The cyclic integer matrix trace counts those assignments exactly. Summation proves the identity without a SAT-label oracle.

**Paid bound:** Source grammar, signed occurrence quotas, duplicate detection, explicit template difference D,A, source/index/head reads, failed subset conflicts, matrix acquisition, schoolbook integer products of O(n+k) bit values, proof/checker output, and all cache/replay/read/write work are charged. There are at most 2^k terms, each at most 4*256*t private trials with at most 12 clause reads, followed by t 2x2 products. Thus T<=2^k poly(N) on its recognized sources, with polynomial streamed peak working memory and optional 2^k poly(N) emitted proof. All clauses and variables retain source identities; residual circuits/Tseitin are not canonical children. When k<=c log_2 N for fixed c this gives a uniform polynomial-total-work recognized terminal. Nothing establishes that all valid canonical originals satisfy such a bound or are cheaply isomorphic to G_t. Any failed adaptive policies, selector switching, guests and simultaneously live ancestors are charged in the full controller, not assigned zero globally.

## Source-verified controls

On G2 swap the positive x1 occurrence in original C3=(x1,x3,x5) with x12 in original C15=(x10,x12,x14), yielding source C3'=(x12,x3,x5), C15'=(x10,x1,x14). The changed original is still connected, grammar-valid, with n18,m24,k2. Exact #SAT is 4619; relaxed H has 6862. Same original pins p_U={x18=1,x10=0,x16=1,x1=0} yield four H transfer terms [507,48,507,48] and UNSAT0, with no immediately falsified original clause. Flip only x18 to 0: terms [1087,160,416,48], SAT559 with checked witness bitmask 46170. A separate no-producer-import verifier checked **all 2^18 original assignments**, all 16,384 UNSAT completion leaves with a source-clause falsification cover, and separately acquired factor matrices.

Canonical cross-block edited families t=1,2,3,4 with k=0,2,4,6 have independently verified exact counts 70,4619,325751,20908389. Producer checked 72 deterministic pinned controls using direct source completion. Independent verifier passed **24,811 assertions**, including F9/Y6 signed S/U extremes and complement controls, Y6=20 models, original F9 SAT2/UNSAT0 siblings, malformed source controls. F15/U198/V198 are inherited, not freshly replayed.

The exact clause-preserving fan-in-two circuit C_F uses the ORIGINAL 18 inputs, 71 binary OR/AND gates and balanced depth at most 7. The source and circuit matched on all **262,144** complete input rows. Offline exact reduced OBDD compilation gives 265 forward and 309 reverse nonterminal nodes, with the entire truth-table acquisition charged; neither number is arbitrary SAT-decision hardness or unrestricted minimum circuit size. Current-label equivalence does not imply continuation equivalence.

## Direct source-DPLL competitiveness control

A separately implemented original-source unit-propagation-first DPLL on exactly the SAME changed canonical F'_2 and the opposite-label pins resolved UNSAT in **one recursive node, 102 literal inspections, one forced unit**, versus SAT in **seven recursive nodes, 510 literal inspections, six explicit branches, seven forced units**. The exception-clause transfer computed 8,192 local candidates and eight integer matrix multiplications on each two-edit pin query. Python-level counts are not native same-machine FLMV time/space. Thus the new parameterized compiler is not shown faster than direct search on these controls.

## Corpus/primary literature and exact gap

GATE323/324 and LSPV-2 DYNAMIC-DECISION-DAG311 already established rank-vs-decision escape, pinned transfer and dynamic matrices for unedited G_t. This report does **not** claim those methods or inclusion-exclusion are novel. New project-specific result: signed exception-clause FPT correction with connected canonical opposite-label controls. GitHub j15marti/pnp and github.com/openai searches, along with primary web queries, are detailed in the dated run search log. References: Döcker (2019) arXiv:1912.08032; Darwiche-Marquis (2002), DOI 10.1613/JAIR.989; FLMV (2005), DOI 10.1145/1101821.1101822.

The all-input polynomial aggregate adaptive-work theorem, unknown-exponent arbitrary-A power-short hereditary ARC transformation, and strict same-machine FLMV transfer remain **OPEN**. Exact fallback may be exponential; no claimed lower bound survives arbitrary alternative deciders. Full recurrence sums all unsuccessful acquisition/selection/switching, proof/GE, child, cache, source/index/head, guest DELAY/COPY/RECOMP, and maximizes simultaneous peak working space. Logical XOR is offline only. No agent identity, schedule or enablement change.

**Next:** test canonical families with growing k but efficiently factorizable grouped exception clauses, or falsify their conjectured polynomial discovery cost.
