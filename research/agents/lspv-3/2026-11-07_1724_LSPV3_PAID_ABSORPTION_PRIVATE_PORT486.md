# LSPV-3/486: Paid absorption copies of addressable private Boolean wires

**2026-11-07 17:24 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | Historical full R_mix341 and P versus NP OPEN.**

**Tracker IDs:** new evidence [P2-L3-486] refines [P2-F13] and open [P2-C3]. Historical [P2-D1], all-mixed superpolynomial [P2-B1] and same-calculus B3 [P2-B2] remain OPEN. Route A [P2-A2], [P2-A4] unchanged.

## IDEA and four falsifiers

After LSPV-5/421's exact private-output projection objection, investigate whether an **addressable but non-exported** private Boolean wire can be copied to a new public name using only paid, distinct-input two-input gate definitions and one oriented Resolution inference. Proposed repair: Boolean absorption.

Falsifiers: (1) copied wire not globally equivalent or not conservative; (2) copy requires repeated operand/constant; (3) legal oriented Resolution cannot derive its positive implication; (4) historical R_mix341 does not permit the private wire reference or output port. Falsifiers 1-3 are excluded for the distinct proposed E486 grammar. Falsifier 4 remains OPEN and is the crucial native interface question.

## SEARCH: project and external continuity

Read full root proof1 (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), full root proof2 (startup blob cc9990b77ca41a61f794b4cde1d98864c3fc5e14), issue #3 through comment 6715588094, governing 2026-11-02 five-role handoff (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md, CODEX.md, pnp-research skill, the historical /341 rule report (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), LSPV-3/485, LSPV-1/489 and /491, LSPV-5/413 and /421. Historical verifier experiments/arc/lspv2_341_independent_verify.js (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0) accepts SOURCE/AND3/XOR only, not RES/DEF/LOCAL. Actual Grok GROKPROOF/2026-11-08_0118_PROGRESS.md (blob 4fbcd3a1725be91c74d15f0c7fce7367ba40c82d) and Claude ONETAPE-0001 (blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a) were reviewed; neither supplies historical mixed grammar.

Mandatory repository deltas: konard/p-vs-np scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c); peitl/short-proof README.md (93d2090dba9739bc4983c65ea639a24e1f5e0fab); openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). Read actual format/scope, not just snippets. None authenticates historical /341. Indexed web literature search considered Cook-Reckhow 1979, Chvatal-Szemeredi 1988, Pang 2026; Google-branded search and native /341 execution were unavailable/not performed. No PDF was analyzed.

## ITERATE: exact paid copy theorem (PROVED/RESTRICTED)

**Distinct E486 calculus, not historical R_mix341:** two-input conservative AND/OR/XOR definitions with fresh named outputs, distinct earlier parent identifiers, each charged once with its complete defining 2/3-CNF facets; oriented binary Resolution with a named pivot and paid derived clause. Private intermediate wires are assumed *addressable as inputs* to subsequent DEF even when not previously exported.

**Lemma 486.1.** Let w be an earlier private Boolean wire and t any earlier distinct original input. Introduce two fresh paid outputs v,e:

$$
v=w\lor t,\qquad e=w\land v.
$$

For every original input and every extension of previous gates, e=w by the absorption identity. Both definitions have distinct inputs and fresh outputs; they are globally conservative and may share t across any number of copies.

The OR defining facet $(\neg w\lor v)$ and AND defining facet $(w\lor\neg v\lor e)$ resolve on positive/negative v to derive $(\neg w\lor e)$ with **one paid, oriented RES**. The opposite implication $(\neg e\lor w)$ is already an AND facet. Thus e iff w is supported by **two paid DEF, six defining facets and one paid RES**, without duplicate operands, a constant wire or an uncharged semantic jump.

Under context Gamma |- w, one additional paid RES with the proven implication derives Gamma |- e. Under Gamma |- not w, RES with the AND facet derives Gamma |- not e. Context-free definitions may be shared among branches; contextual units may not. No case split or discharge is added to historical R_mix341.

**Corollary 486.2.** For h addressable private Boolean wires and an earlier shared original input t, the copy construction adds exactly 2h DEF and h RES nodes plus 6h defining facets, and a further RES node per distinct scoped unit application. With unit weights this is 3h paid nodes before scoped applications. With symbolic historical weights this would be $2h w_{\rm DEF}+h w_{\rm RES}$, **only if** the historical grammar authenticated all ports and facets. Encoded certificate/ID bits O(h log(M+h)) for canonical bounded IDs; explicit facets are materialized and checked. An implemented compiler pays parsing, reads, authentication, memory, failed work, serialization and verification; ideal logical W_R excludes discovery intentionally.

**Precise obstruction:** If private wire identifiers cannot be referenced in a historical DEF argument, the *first* new OR gate cannot be expressed. Even when the proposed copy is legal, naming an output does not license its use as an AND3 factor, LOCAL-CONVERT result or GF(2) row. This is a conditional repair to [P2-L5-421], not a proof-to-proof normalization of arbitrary R_mix341 certificates.

## Finite original-source controls and resource ledger

Two independently implemented programs checked original **strict-3CNF K4 Tseitin** odd/even charge sources, each 16 three-literal clauses on six original edge variables. Exhaustive source counts: odd 0 SAT models; even 8 SAT models. All 64 original assignments per source uniquely extend through eight original nested/shared/reconvergent AND/OR/XOR gates and sixteen absorption-copy gates. The two even-source contexts Gamma+=(x1,x2) and Gamma-=(not x1) have two and four models, respectively: conditional e0 and not-e0 are justified, but global e0 is **not** entailed.

JS/V8: 4,482 assertions, six invalid controls rejected (wrong pivot, wrong polarity, unrecognized gate, repeated operand, forward-reference cycle, globally leaked unit). Separately written Python: 4,499 checks. Eight base DEF nodes own 26 facets; 16 copy DEF nodes own 48 facets; eight copy-implication RES and five scoped RES nodes give 24 DEF plus 13 RES = 37 distinct paid nodes in the declared unit-weight test grammar. The facets are explicit, not double-counted as extra paid inference nodes under E486. Ideal critical path through the base/copy/equivalence DAG is at most nine unit levels; realizable time/space is different. Python observed 0.0061 seconds and 96,012 KiB peak host RSS, not a TM complexity exponent. These witness counts are **constructive upper bounds, not certified minima**. Source parser and corrupt-certificate controls do not imply historical accepted-byte verification.

Code: experiments/arc/lspv3_486_absorption_copy_ports.cjs. Raw summary: results/raw/arc/2026-11-07_1724_LSPV3_ABSORPTION_COPY486_RAW.json. Independent Python reproduction is packaged in a downloadable fallback archive.

## Hard-family / theorem / transfer ledger

**Chvatal-Szemeredi 1988:** $n$ variables, $m=6n$ independent signed proper three-literal clauses, $\Theta(n\log n)$ encoded bits; exponentially long *ordinary shared-DAG Resolution* refutations with high probability under the paper's density assumptions, NOT mixed/all-algorithm hardness. **Pang 2026 arXiv:2610.00837v2 Thm 7.2(a):** random proper signed 3-CNF $F(n,3,8n)$; fixed syntactic Res(PC_r/F_p), exponential shared-DAG proof size a.a.s.; no reduction outside 3-CNF, but transfer into native mixed R_mix341 OPEN. **Odd cubic-expander Tseitin:** h graph vertices, 3h/2 variables, 4h strict 3-CNF clauses; exponential ordinary Resolution in the expander family, but linear GF(2)/AND3 shortcuts in the historical restricted exhibited K4-style model. **Cook Extended Resolution** and shared DAGs remain legal upper-bound controls where authenticated, never excluded from a worst-case minimum.

Primary sources: Cook--Reckhow 1979, https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf; Chvatal--Szemeredi JACM 35(4) (1988), DOI 10.1145/48014.48016; Pang arXiv:2610.00837v2, https://arxiv.org/abs/2610.00837. No proof-hardness preservation is claimed for equisatisfiable extensions.

**Remaining exact gaps:** [P2-D1] native accepted-byte grammar, [P2-C3] mixed RES-to-DEF-to-LOCAL-CONVERT-to-AND3 normalization and inaccessible private-wire references, [P2-B1] all-rules superpolynomial Wbar_R, [P2-B2] same-calculus noncircular B3. Root main.tex not changed due to failed complete safe retrieval. Roles/IDs/titles/schedules/enabled state and historical weights preserved. **P versus NP OPEN.**
