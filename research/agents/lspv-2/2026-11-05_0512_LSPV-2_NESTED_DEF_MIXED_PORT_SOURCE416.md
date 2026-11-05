# LSPV-2/416: Nested paid-DEF mixed-consumer proof and original source normalization

**November 5, 2026, 05:12 PST | PNP SAT-Circuit Reduction Builder.** Status: **PROVED/EXACT** restricted source-normalization lemma, **COMPUTATIONAL** finite CANON2 proof. Full historical native grammar, polynomial whole-R normalization, B1/B2/B3 and P versus NP **OPEN**. No change to R, costs, roles, tasks or schedules.

## IDEA: falsifiable proposals before search

Hypothesis H1: Two nested paid conservative two-input DEF gates, with strictly oriented RES consumers, can feed a complete authenticated chain of AND3, LOCAL-CONVERT and GF(2) ending in contradiction; all paid operations must be ancestors of the root. Prediction: 17 nodes, no private wire or free gate, independently verified under LSPV-5's **proposed CANON2** fixed-facet grammar. Historical /341 export legality remains conditional.

Hypothesis H2: CANON2 directly covers all well-formed original DIMACS literal sequences. Falsifier: a legal unsorted source clause, rejected by CANON2's canonical sorted-set parser. Repair: an external raw-input parser preserving source IDs and raw-byte provenance, with polynomial physical cost and no extra logical node.

Further hostile tests: altered external source, false GF(2) RHS, wrong paid-gate truth, SAT subformula, and dead paid nodes.

## SEARCH: corpus, actual independent reviews, literature

Read governing 2026-11-02_1204 five-role handoff first, issue #3 through REFEREE361, original LSPV-2/341 mathematical rules, AGENTS.md, CODEX.md, pnp-research skill, LSPV-2/415 SAT exploit, LSPV-3/421 oriented Resolution repair, LSPV-4/412 affine sub-support coverage fault, and actual LSPV-5/361 proposed-CANON2 checker (GitHub blob 7b6e8478). **CANON1 soundness is retired; CANON2 is a proposed completion, not the recovered historical byte specification.**

Actual Grok: GROKPROOF/2026-11-05_1218_PROGRESS.md (d3183283). Actual Claude: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727). Neither closes native wire typing or B3.

Primary literature: Haken (1985), lower bound on **ordinary Resolution** proofs of pigeonhole formulas, not on arbitrary SAT machines or extensions; Cook and Reckhow (1979), relative proof system size and simulations; Gocht and Nordström (AAAI 2021), certified parity in a *separate* pseudo-Boolean system; Varisat DIMACS manual and DRAT-trim input grammar, supporting unsorted literal sequences. Web queries: "DIMACS CNF literal order", "resolution proof checking repeated literals", "Haken resolution pigeonhole 1985", "Cook Reckhow 1979", "Gocht Nordstrom parity". **Direct Google-branded search unavailable**; indexed web used. Authenticated github.com/openai queries "ExecCNFNodeSearchCosts", "CookLevin", "DRAT LRAT", with full reads of openai/math Lean ExecCNFNodeSearchCosts.lean (1ced21f4) and CookLevin.lean (1e23a159). No same-fixed-R compiler found.

## ITERATE: exact mixed derivation

External original is 98-byte signed DIMACS (SHA-256 61311711b601d7d02a4d96fe4bfe70dc1edc7ff459fbceef592528ab68449600):

    c authenticated external bytes, literals deliberately unsorted
    p cnf 2 4
    2 1 0
    -2 1 0
    -1 0
    2 -1 0

Original source IDs, preserved across canonicalization: C0=(x OR y), C1=(x OR NOT y), C2=(NOT x), C3=(NOT x OR y). C0 and C1 imply x while C2 implies NOT x, so source UNSAT. C0,C1 alone are SAT with x=1.

Pay separately for a=x XOR y (a=3) and b=a XOR y (b=4), with truth table [0,1,1,0] each. Under the proposed CANON2 defining-clause selector interface, six ordinary **oriented** RES nodes derive (-x OR b) and (x OR -b). Two more RES nodes use C0,C1 to derive (y OR b) and (NOT y OR b), then one RES derives b and one derives x. AND3 of x and C0 gives exact two-original-variable factor x and annotation x=1. LOCAL converts that factor to clause x with exhaustive truth-row implication. AND3 of the resulting clause x and C1 gives affine row x=1; AND3 of C2,C3 gives x=0; GF(2) addition gives 0=1.

**Complete paid DAG: 2 DEF + 10 RES + 3 AND3 + 1 LOCAL + 1 GF2 = 17.** Every paid node is a root ancestor, so no unused gate inflates the result. Original supports of all AND3 and LOCAL steps are subsets of [x,y]; no hidden circuit wires, DEF-to-GF2 operand exports or soundness oracle are introduced. Distinct variables x,y have exactly one pair (a,b) of definition-consistent extensions. The machine-readable source/certificate is in results/raw/arc/2026-11-05_0512_LSPV2_MIXED_DEF_PORT416.json and independent no-dependency checker is experiments/arc/lspv2_416_mixed_port_verify.mjs. Separate local Python checker and independently written JavaScript checker validated the proof, the latter with 461 assertions, plus mutated-source/DEF/GF2 and both-label controls. The compact GitHub JS checker should be independently executed before assigning a fresh assertion count.

**Scope:** This is a concrete legal trace under the fixed-facet CANON2 completion; original /341 does not fully fix the facet byte selectors, so historical native legality is NOT established. The formula has a **2-node** ordinary-Resolution refutation; 17 is only an upper-bound certificate, not an exact minimum and not a hard instance. The full published CANON2 checker was read via authenticated GitHub, but not directly executed in the local container because raw GitHub DNS failed.

## PROVED/EXACT restricted source canonicalization lemma

For any well-formed strict DIMACS CNF with N raw encoded bytes, ordered clauses, terminated literals and valid header, replace each j-th literal sequence by its sorted distinct literal **set**, retaining both signs if tautological, and retaining **the original source ID j**. Boolean semantics of each source clause are unchanged by OR commutativity and idempotence. Thus every already-typed proof whose **only** CANON2 incompatibility is noncanonical source literal order/repetition and whose inference rules use clauses as Boolean sets preserves the original q paid nodes and the same root conclusion under this source change. Parsing, per-clause sorting, duplicate elimination, exact comparison with the *externally supplied* raw original and canonical serialization are all polynomial in N (at most O(N log N) token comparisons for sorting). They are charged actual operations, not inference nodes.

Concrete coverage falsifier: CANON2 canonical_clause([2,1],2,...) rejects legal original C0 before any proof step. A separate original-byte-aware canonicalization wrapper repairs this *input* issue, but does not change the historical native grammar or resolve arbitrary auxiliary consumers. A self-consistent SHA-256 within an attacker-supplied proof is **not** external-source authentication.

## Physical costs and B3

This test has q=17 paid logical nodes, N=98 raw DIMACS bytes, 48-byte canonical JSON source and 2,318-byte canonical JSON certificate (Python production). Parsing, raw input comparison, hashing, sort/dedup, selecting and indexing sources, building facets, materializing children, truth-table checking, emitted bytes, and peak memory all incur actual cost. Buffered verifier space is O(N+E) for explicit evidence E plus runtime overhead, not O(q) necessarily. Local allocation counts toward all-phase rho, and no FLMV or unrestricted runtime consequence is inferred.

**B3 still OPEN:** SAT in P yields a decider-specific polynomial Cook--Reckhow system, but to derive polynomial Wbar in the *same preselected R_mix341* one needs a polynomial proof-size simulation of that system (or another independently proved noncircular same-R transfer). This finite trace and source-order wrapper do not supply it; neither Haken PHP ordinary Resolution hardness nor Cook extended-resolution/Tseitin XOR controls imply unrestricted machine hardness. All schedules, roles, proof-system rules, and prior historical results preserved. Root main.tex was not changed because safe full-byte readback/owner-region preservation was not established.
