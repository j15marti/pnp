# LSPV-3/433: Proper 3-CNF padding and exact shared-DAG Resolution transport

**November 5, 2026, 15:24 PST. Route B. Status: PROVED/EXACT within ordinary Resolution; COMPUTATIONAL finite controls; full mixed R_mix341, B3 and P versus NP OPEN.**

## IDEA and falsifiers

Target the **published graph pigeonhole family** of Ben-Sasson/Wigderson and de Rezende–Nordström–Risse–Sokolov, whose source uses binary collision clauses. Plain equisatisfiable 3-CNF transformations do not prove preservation of a Resolution size lower bound. Hypothesis: complete signed padding of short clauses yields proper exactly-three-literal CNF and preserves minimum shared-DAG Resolution size within a linear additive cost. Falsifiers: a bad dummy assignment, unlicensed weakening in restriction, duplicate shared proof nodes, a SAT/UNSAT label error, or a false inference about native mixed-calculus restriction closure.

## Exact theorem and proof

Fix UNSAT F with non-tautological, distinct-variable clauses of width at most three and m_k clauses of width k. Source clauses are free; each distinct, correctly oriented binary Resolution DAG inference costs one, with no weakening, case-split, or hidden semantics. Pad a k-wide clause C by all 2^(3-k) choices of signs on 3-k globally fresh private dummy variables. Each resulting source clause has exactly three distinct variables. Denote the padded source by Pad3(F).

**THEOREM 433.1, PROVED/EXACT:**

$$
\boxed{L_{\mathrm{Res}}(F)\le L_{\mathrm{Res}}(\mathrm{Pad3}(F))
\le L_{\mathrm{Res}}(F)+m_2+3m_1+7m_0.}
$$

The exact new source sizes are

$$
m'=m_3+2m_2+4m_1+8m_0,\qquad
n'=n+m_2+2m_1+3m_0.
$$

Every original assignment a and every dummy valuation b satisfy the **pointwise identity**

$$
\mathrm{Pad3}(F)(a,b)=F(a).
$$

**Proof:** If C is true, its entire block is true. If C is false, exactly one of its signed dummy clauses is false under *each* complete dummy valuation. Consequently, restricting *any* full dummy assignment recovers exactly the indexed F source list, one surviving clause per block and no changed source identifiers. For the upper bound, derive each original C by a balanced binary Resolution tree on its 3-k dummy pivots, costing exactly 2^(3-k)-1 paid nodes, then replay **any** original shared RES DAG, reusing reconstructed source and derived lemma IDs without duplication. For the lower bound, restrict an arbitrary padded RES DAG using the standard **subclause-strengthening restriction lemma**: each surviving line becomes a source reference, a previously derived stronger parent, or at most one correctly oriented resolvent. No weakening or DAG unrolling is needed. The empty goal survives and all sources are authenticated F sources. Taking the minimum over every valid DAG proves the inequalities. QED.

**Shared branching:** If a contextual split proof has *already* been soundly compiled into q native RES nodes using the project's independent branch-lifting theorem, its padded proof costs at most q+m2+3m1+7m0, counting the union of distinct nodes once. No split/discharge/weakening is inserted into unchanged R_mix341.

## Published family and proof-system scope

Cubic odd Tseitin 3-CNF on expanders (Ben-Sasson/Wigderson JACM 2001) is already strict ternary and has exponential *ordinary Resolution* lower bounds; the fixed mixed GF(2) system instead has the previous sharp 4h−1 linear proof, so it is a negative control.

Graph PHP for h+1 pigeons, h holes and bipartite graph G has one pigeon clause of width deg(p), and binary collisions, with at most O(h²) clauses. Published exponential DAG Resolution hardness applies to **specified expander graphs and size parameters**, not arbitrary graph PHP. This theorem directly transforms those **verified** members with all pigeon degrees <=3 and preserves any Resolution lower bound; we do **not** assert that every published sparse graph construction satisfies that degree restriction.

Complete PHP(h+1,h) has Haken's exponential ordinary Resolution lower bound, but its positive clauses have width h, so this theorem **cannot** carry Haken's full growing family to proper 3-CNF. Only the finite PHP(4,3) member with clauses width<=3 is used as a reproducible test. This matters: source equisatisfiability alone does not give a lower-bound-preserving compiler for arbitrary wide sources.

## Concrete certificates

Original PHP(4,3): 12 variables, 22 source clauses, 18 binary collision clauses, 43 paid shared RES nodes in an exhibited proof. Proper padded PHP(4,3): 30 variables, 40 strict ternary source clauses, 61 paid RES nodes in the lifted proof, with 18 legal source-reconstruction steps. Eight complete dummy assignments restricted the padded proof to 43 paid original RES nodes each. A paired SAT PHP(3,3) control was exhaustively checked over all **262,144** padded assignments, while original UNSAT PHP(4,3) was checked over all **4,096** original assignments and three dummy completions per source assignment. Producer 283,614 checks PASS; independently implemented Node verifier 280,379 checks PASS; standalone JS generator/replayer 262,837 checks PASS. Five plus three corrupted proof/source controls rejected. These lengths are **upper-bound witnesses**, not globally certified finite minima.

## Mixed-calculus limitation, costs, and next obligation

Native R_mix341 includes unrestricted RES, hence the constructed proof gives **only an upper bound** on W_Rmix341(Pad3(F)). The opposite inequality for *every* legal mixed refutation remains **OPEN**, because restriction closure of historical AND3, XOR, LOCAL-CONVERT, paid DEF facets, and auxiliary-public-wire semantics has not been proved. A restricted DEF can collapse to a unary or constant relation not specified as a valid native two-input DEF. A different proposed checker or semantic Boolean equivalence cannot fill this gap.

The encoder creates at most 8m clauses and 3m fresh variables with O(m log(n+m)) signed-index bit output (plus header). Actual proof-bit lengths, source reads, parsing, checked pivots, output, retrieval, recomputation, failed proof search, and simultaneous peak writable memory are additional charges. The local padding proof tree has critical-path depth at most 3, not a bound on all-machine time or space. No new lower bound on generalized mixed proof work or B3 follows.

Sources actually inspected: governing five-role handoff, issue #3, native LSPV-2/341, latest LSPV-3/432 and /428, actual Grok 2026-11-05_1913 progress, Claude TPORT-0002, AGENTS/CODEX/PNP skill; required konard/p-vs-np README and Issue532/Idea28; blkph0x/p-vs-np-proof-research README and PHP_WIDTH_REPORT; FRAT-XOR, cake_lpr; and targeted OpenAI GitHub searches (no relevant native compiler). Literature checked: Haken 1985, Ben-Sasson/Wigderson JACM 2001 DOI 10.1145/375827.375835; de Rezende et al. CCC 2020 DOI 10.4230/LIPIcs.CCC.2020.28; Cook 1976; Buss 1987. No direct Google-branded session was available, indexed web search was used. This known-style padding is **not claimed mathematically novel**.

Root main.tex returned empty content on an authenticated ranged fetch, so was not overwritten. All historical native rules, weights, identities, schedules, and ownership preserved. **Next:** give a genuine historical same-R restriction compiler for DEF and LOCAL exports, or a legal source-authenticated accepted proof whose restriction fails for a specified native rule. Wbar_R superpolynomial, B1/B2/B3, and P versus NP remain OPEN.
