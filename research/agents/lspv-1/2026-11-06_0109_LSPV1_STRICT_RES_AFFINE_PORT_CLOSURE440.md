# LSPV-1/440: Strict Resolution cannot export one semantically implied guarded parity blocker
**2026-11-06 01:09 PST | Route B | PROVED/RESTRICTED finite exact saturation. Historical full R_mix341, B1/B2/B3 and P vs NP OPEN.**

## Idea, falsifiers, search and revision
LSPV-1/439 derived an exact subsuming clausal cover of a guarded parity constraint from source-indexed split clauses and paid edge-owner facets, but did not prove that all canonical row clauses can be manufactured by weakening-free binary RES, even with an additional two-input XOR owner. Test F1: missing canonical blocker is already Resolution-derivable; F2: blocker is not entailed; F3: adding XOR owner eliminates the problem; F4: historical LOCAL-CONVERT accepts the semantic row in its unchanged native grammar. Exhaustive closure falsifies F1/F3 and Boolean evaluation falsifies F2; F4 remains OPEN, not silently replaced by a new rule.

Governing handoff read at historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8; issue #3, /341, /438–/439, LSPV-3/436 and /441, LSPV-5/379, Grok 2026-11-06_0515 and Claude ONETAPE actually reviewed. Required external files read: konard/p-vs-np/scripts/proof_status.json @ 93b77ed; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md @ 18d693e; meelgroup/frat-xor/format.md @ 986a21aa; peitl/short-proof README @ 93d2090; openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean @ 1ced21f. Primary literature Cook–Reckhow (1979), Urquhart (1987), Ben-Sasson–Wigderson (2001), Pich–Santhanam (2026). Indexed web search available; distinct Google-branded service and authoritative historical checker unavailable.

## Declared reduced clausal subsystem, NOT the historical native byte grammar
Variables g,w1,w2,w3. For each even-parity b=(b1,b2,b3), let L_i(bi)=w_i if bi=0, and NOT w_i otherwise. Let

$$
U_1=\{g\vee L_1(b_1)\vee L_2(b_2)\vee L_3(b_3): b_1\oplus b_2\oplus b_3=0\}
\cup \{\neg g\vee\neg w_i: i=1,2,3\}.
$$

Four guarded source-derived clauses plus three signed edge-owner facets; these are *derived-port assumptions*, not newly free original 3-CNF axioms. Define four extra signed owner facets X encoding the conservative binary XOR gate z=w1 XOR w2 (one clause for each incorrect triple of values). Historical owner-qualified facet indexing remains unresolved.

**Exact theorem 440.1.** Let Cl_RES(A) be the least superset of A closed under ALL non-tautological strictly oriented binary Resolution, with no weakening, splitting, semantic oracle or extra rules. Then

$$
|\mathrm{Cl}_{\mathrm{RES}}(U_1)|=13,\qquad
|\mathrm{Cl}_{\mathrm{RES}}(U_1\cup X)|=87.
$$

Starting with 7 and 11 axioms respectively, complete rounds add (3,3,0) and (15,36,25,0) new clauses. The independent verifier enumerates every complementary pivot on every pair in each final closure, proves closure under strict RES and identifies the missing clauses. Induction over any proof DAG implies no arbitrarily long strict RES derivation from these exact axioms can derive a clause outside the closure.

All four canonical clauses involving negative g of the 4-variable parity row
$$w_1\oplus w_2\oplus w_3\oplus g=1$$
are semantic consequences of U1 but none occurs in Cl_RES(U1). After adding the XOR owner X, three of the four canonical blockers for the 3-variable equation
$$z\oplus w_3\oplus g=1$$
are derivable. The remaining semantically implied clause

$$
\boxed{\neg g\vee\neg w_3\vee z}
$$

is **not** in Cl_RES(U1 ∪ X). It is already subsumed by the facet \(\neg g\vee\neg w_3\). One weakening step would derive it, but weakening is not the historical RES rule. Merely *being implied* does not produce an exact canonical row via strict Resolution.

U1 and U1∪X are **satisfiable**, each with five models: four odd-parity w triples when g=0 and w=000 when g=1, with uniquely determined z in the latter formula. This is an exact finite **clause production impossibility**, not a UNSAT proof-size lower bound, not an all-rule historical R_mix341 counterexample. The seven clauses require earlier source and owner derivations; they are not free formula axioms. OTHER legal mixed inferences may bypass the obstruction.

## Executed verification
Independent Python producer enumerated complete 13/87 clause closures, all strict RES pivots and 4/5-variable truth tables, then constructed the known original proper 3-CNF K4 odd/even Tseitin controls (16 clauses, 6 variables; 0 vs 8 satisfying assignments). Separately authored Node verifier reconstructed source clauses from their parity condition, independently re-enumerated closure, checked all final pairwise pivots and model entailments, and passed **2,903 assertions**, including negative controls. The Node test initially rejected an incorrectly selected *test* assignment; corrected assignment g=1,w3=1 falsifies its designated facet, after which all checks passed. Executions did NOT run a historical R_mix341 checker. Complete signed clause tables, Python/Node executables and SHA-256 manifest are in the locally delivered reproducibility archive; GitHub compact verifier and raw count JSON provide a supplementary replay.

## Hard-family and shortcut ledger
- Cubic expander odd-Tseitin: h even vertices, 3h/2 edge variables, exactly four signed width-three clauses per vertex, 4h clauses and Θ(h log(h+2)) binary-indexed bits. Source UNSAT from sum of vertex parity rows. For suitable expanders, established 2^{Ω(h)} **ordinary unrestricted shared-DAG Resolution** lower bound (Urquhart 1987; Ben-Sasson–Wigderson 2001). Historical /341 has 4h−1-node **mixed** AND3/GF(2) refutation, so no all-mixed hardness from this family.
- Guarded /436 strict 3-CNF K(F_h): 8h+4 proper three-clauses, 11h/2+3 variables. Earlier /435–/436 prove lower-bound preservation in ordinary Resolution by explicit substitution/restriction; /438–/439 show algebraic guarded edge-gate shortcut *conditional on native ports*. This report blocks one naive clausal export, not every mixed shortcut.
- Braun 2026 bit-PHP: n=2^ell, collision width 2ell before strict 3-CNF private-chain transformation. Reported bound > exp(n/(32768 ell²)) in DAG-like Res(XOR) for ell>=32, without extensions. Cook ER and LSPV-5/379 and LSPV-3/441 proposed FACET-A/GATE-LOCAL polynomial derivations are mandatory upper controls; equisatisfiability of a 3-CNF chain is not proof-size lower-bound preservation.

## Resource, quantifier and status firewall
In fixed sound complete effective historical R, W_R(F) minimizes the sum of weights of ALL distinct paid nodes over ALL legal shared/refutation DAGs; Wbar_R(N) maximizes over all valid UNSAT source encodings with ≤N bits. Our restricted closure does NOT evaluate W_R. Ideal choice is free, while implemented discovery, input/source reads, parsing, facet lookup, memory, output, checking, failed attempts, caching and recomputation are paid in time/space. Host measurements cannot imply same-machine FLMV bounds.

**B1/B2/B3 OPEN.** The noncircular required B3 remains SAT∈P ⇒ Wbar_Rmix341(N)=N^{O(1)} for this SAME fixed calculus; neither a SAT oracle's answer nor a semantically valid parity row supplies its native certificate. Full-mixed superpolynomial Wbar and P vs NP OPEN. Do not change role ownership or root main.tex.

Sources: /341 blob c87acd11; /439 dcfc1942; /3/436 4d3cfc1; /3/441 437bf093; Cook–Reckhow 1979 DOI 10.2307/2273702; Urquhart 1987 DOI 10.1145/7531.8928; Ben-Sasson–Wigderson 2001 DOI 10.1145/375827.375835; Pich–Santhanam JACM 2026 DOI 10.1145/3801091; FRAT-XOR format blob 986a21aa.

**Next exact gap:** source-authenticated, bounded-cost historical LOCAL/DEF row-to-GF(2) export or a formally legal counterexample to a precisely stated proposed transfer. The restricted no-weakening obstruction has been certified; native interface remains OPEN.
