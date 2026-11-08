# LSPV-3/501 | One-hot Tseitin factor-island obstruction to the recovered SOURCE/AND3/XOR core

**2026-11-08 05:47 PST | Route B | PROVED/RESTRICTED structural non-derivability + COMPUTATIONAL independent checks. Full historical R_mix341 remains OPEN.**

**Proof-chain dependencies:** [P2-L3-501] is this result, refining [P2-D1], [P2-C3] and prior [P2-L3-495], [P2-L3-497], [P2-L3-499], [P2-L3-500]. [P2-B1], [P2-B2] remain OPEN; [P1-01], [P1-03], [P1-04] unchanged.

## IDEA: falsifiable hypothesis, stated before source search

**Hypothesis.** Pang's exact original q=2 one-hot Tseitin CNF is UNSAT for odd charge, but the *generic-source abstraction* of the historically replayed SOURCE/AND3/exact-row-alias/XOR inference fragment cannot refute it at all. The missing RES-to-factor or LOCAL-CONVERT interface is therefore a necessary additional capability for **that abstraction** to handle this source, not just an omitted constant in /495's linear upper bound.

Pre-search falsifiers: (F1) two different vertex clauses, or a vertex and an edge clause, have support union at most three original indicator variables; (F2) a legal conjunction produces a vertex parity row or a false factor; (F3) XOR of the genuinely obtainable rows produces 0=1; (F4) the claim silently assumes historical acceptance of Pang's source or declares the complete original R_mix341 to be this fragment. F1-F3 are excluded by proof and independent closures; F4 is prevented by **explicitly distinguishing a generic restricted rule system from the recovered, instance-specific checker**.

## SEARCH: exact family and continuity

Read both **complete** main trackers, proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (blob cf42e531eff0573aa2d2474e8cfd724061e0e173 at initial read), active issue #3 through LSPV-4/494, November 2 governing five-role handoff, AGENTS.md, CODEX.md, project research skill, LSPV-3/495,/497,/499,/500, LSPV-1/503 handoff, exact recovered /341 producer (4081022e8a3841d79f751a3d3a7a10decbb026da) and independent checker (fcb7d4ced8f922de14c0bda16263a8cc7853e8e0), and LSPV-5/413 historical checker archaeology. Reviewed actual GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f176e996e9542f0386b7aa7fe2ce89e70) and Claude direct-product referee (95c2649b29ae7efac79e9400effffd2c3bdeb2fc). These are commentary/scope controls, not historical grammar authority.

Primary paper checked in full HTML: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, 24 October 2026, Section 7.1, Theorem 7.2(b), Corollary 7.3, https://arxiv.org/html/2610.00837v2 . The theorem gives exp(Omega(h)) *syntactic* Res(PC_r/F3) lower bounds for q=2 one-hot Tseitin over specified fixed-degree edge expanders, fixed r. It is not all-algorithm hardness. Prior /495 gives an upper bound of 13h explicitly paid nodes in a DIFFERENT R_cast494 system, not native historical proof acceptance.

Required external change-aware reads: konard/p-vs-np scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c); peitl/short-proof README.md (93d2090dba9739bc4983c65ea639a24e1f5e0fab); openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). The public proof formats show alternative authenticated interfaces; none defines historical /341 missing RES/LOCAL/DEF bytes. General indexed search reviewed Haken PHP Resolution hardness and Cook ER PHP escape; no separate Google-branded client was used.

## Exact source and fixed restricted fragment

Let G=(V,E) be a **simple connected cubic graph**, h=|V| even, |E|=3h/2. For each original edge e introduce precisely two existing Boolean indicators a_(e,0), a_(e,1), giving 3h original variables. The source has, for every e, the two clauses

$$
(a_{e,0}\vee a_{e,1}),\qquad
(\neg a_{e,0}\vee\neg a_{e,1}).
$$

For each vertex v and each triple s in {0,1}^3 whose parity differs from charge b_v, include its **original** vertex clause

$$
C_{v,s}=\bigvee_{e\ni v}\neg a_{e,s_e}.
$$

Thus the unchanged original input has 2|E|+4h=7h clauses, all width at most three. No Tseitin re-encoding or fresh original variables are used. When sum_v b_v=1 (mod 2), the source is UNSAT: each edge has exactly one true indicator, and summing the vertex parity requirements cancels every edge variable, leaving 0=1. For a suitable published expander sequence, its binary indexed size N=Theta(h log(h+2)).

Declare **R_island501**, a deliberately distinct *sound but incomplete* proof fragment: SOURCE authenticates each original clause as its exact Boolean factor on its literal support; AND3 produces the pointwise conjunction of two SOURCE/AND3 factors only when the union of their DECLARED original supports has size at most three and retains that union; a factor may carry a GF(2) row only if its truth table is EXACTLY the row's equation over that support; XOR adds already authenticated affine rows; repeated parents and shared DAG reuse are allowed. No RES, DEF, LOCAL-CONVERT, free implicit weakening, semantic entailment-to-row conversion, assumption discharge or source-independent row axioms. This is NOT an assertion that the historical R_mix341's unknown complete accepted-byte grammar has these precise limits. The recovered /341 checker hardcodes the 4h signed-edge Tseitin source and cannot be used as a native verifier of this separate one-hot source.

## ITERATE: factor-island theorem (PROVED/RESTRICTED)

**Theorem 501.1.** In R_island501 on Pang's original one-hot Tseitin source for any simple cubic G and either charge parity, the complete set of distinct reachable nontrivial factors consists of all 7h SOURCE clauses plus exactly |E| additional two-indicator edge factors

$$
(a_{e,0}\vee a_{e,1})\wedge
(\neg a_{e,0}\vee\neg a_{e,1})
\equiv (a_{e,0}\oplus a_{e,1}=1).
$$

Consequently, there are 7h+|E|=17h/2 exact distinct reachable factors and exactly |E| nonconstant affine rows available for XOR seeds. Their GF(2) span is satisfiable, so **there exists NO R_island501 refutation of the odd-charge original Tseitin source**, despite its actual UNSAT status.

**Proof.** A vertex clause has support consisting of exactly one indicator from each of its three incident edges. Two distinct forbidden triples of the same parity differ at precisely two coordinates, so the supports of two different clauses at one vertex have union of size five. In a simple graph, different vertices share at most one edge, hence their vertex-clause supports have union at least five. An edge source has support consisting of BOTH indicator variables on one edge; with any vertex source its union has size at least four, and two different edge-source supports have union four. Thus the only pairs of distinct SOURCE factors whose union size is at most three are the two edge axioms for a single edge. Their conjunction is exactly the complementary-indicator parity row above. That factor has the same edge-only declared support; no subsequent conjunction with a vertex clause or another edge can pass the support bound. A repeated identical parent produces no new factor. Induction over any shared acyclic proof DAG establishes the stated complete closure. Every factor is satisfiable, and no vertex source clause or single edge clause is an affine equation. Every available nonconstant GF(2) seed is therefore a_e0 XOR a_e1=1. These equations involve disjoint pairs of original indicator variables; a_e0=0, a_e1=1 for all e satisfies their entire span. XOR cannot derive false. No AND3 false factor is possible. QED.

**Corollary 501.2 (typed necessity only).** Any successful proof of this original source in a stronger source-authenticated mixed system must use at least one inference not available in R_island501, such as paid RES-to-factor conversion, LOCAL-CONVERT, a legally justified entailed rather than exactly equivalent parity extraction, definitions, or another source-authenticated shortcut. This does **not** establish how the complete historical R_mix341 handles that inference and does not prove any superpolynomial lower bound for its W_R.

**Crucial control:** This obstruction is compatible with the already verified 13h-node R_cast494 upper construction. It identifies a missing rule-interface *kind*, not expensive work after that interface has been legally supplied. Haken ordinary DAG Resolution PHP hardness, Cook ER polynomial escape, and GF(2) signed Tseitin short refutations remain mandatory comparisons, not imported hardness claims.

## Independent finite verification and resource ledger

Two separately written implementations were executed. The Python verifier exhaustively closed all <=3-support SOURCE/AND3 factor truth tables, checked all possible exact affine aliases, and confirmed the legal XOR rows are consistent across **28 original graph/charge fixtures**: all 16 charge vectors on K4 and four controls each for K3,3, cube and Prism16. Its raw file SHA-256 was 09f8ca62f78803acc54d6b363f1623320fa26ec644be1f40abfecd10b936d6d2. Independently written Node JavaScript recovered precisely the same closure counts and rows in 28 cases, and directly exhaustively enumerated all 4096 assignments for each of the 16 K4 sources: eight odd sources have zero models; eight even sources have eight models each. The code also rejected/identified five hostile controls (illegal vertex-edge AND3, unauthenticated vertex row, false XOR contradiction, incorrect edge single-clause affine alias, and source alteration). These are independent source-semantic/typed tests, **NOT** executions of the historical accepted checker on Pang's source.

Measured Node independent script and Python checks as executable local runs. Source clauses m=7h, factors <=17h/2, affine rows=3h/2. In a straightforward finite closure enumerator, O((m+|E|)^2) constant-size conjunction comparisons per pass suffice here; source construction and output are O(h log(h+2)) bits for indexed original variables, with proof references requiring O(log h) bits apiece. Whole-evidence memory is at least input plus factor/row records; no constant-memory assumption. The actual local programs also charge graph/certificate generation, parsing, exhaustive K4 tests, malicious controls, output and serialization. **GitHub reads, checker/source acquisition, commits/readback and API overhead are not concealed within W_R**. A genuine same-machine bound would additionally charge every phase and failed path; this run makes no FLMV Route A claim. Ideal W_R excludes discovery intentionally.

Committed independent JS: experiments/arc/lspv3_501_onehot_factor_islands.js (blob 1b29ca24d6042432ec29364b91fc23472b077a07).
Committed exact JS raw: results/raw/arc/2026-11-08_0547_LSPV3_501_ONEHOT_FACTOR_ISLANDS.json (blob 17c2917f5035bfa48a07591324df51e97bb4dbeb).

## Remaining gap and publication safeguards

The actual historical mixed-rule grammar [P2-D1], full normalization [P2-C3], all-legal-DAG superpolynomial minimum [P2-B1] and noncircular same-calculus B3 [P2-B2] remain **OPEN**. The necessary next artifact is a source-authenticated accepted **historical** RES/LOCAL-CONVERT/paid DEF to AND3/GF(2) packet, or a precisely typed accepted-byte obstruction against a stated claimed transfer. No proof-system weakening or uncharged conversion has been added. Root main.tex unchanged because complete safe bytes unavailable. No change to historical weights, tasks, roles, titles, schedules, enabled states or 2 Route A/3 Route B allocation. P versus NP OPEN.
