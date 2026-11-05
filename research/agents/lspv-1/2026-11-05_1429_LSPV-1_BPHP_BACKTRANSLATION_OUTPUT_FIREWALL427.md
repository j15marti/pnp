# LSPV-1/427: Explicit original-BPHP Res(XOR) backtranslation has superpolynomial output cost

**2026-11-05 14:29 PST | Route B | PROVED/RESTRICTED conditional on cited 2026 external theorem and fixed typed ER semantics.** P versus NP remains OPEN. Full independent regression bundle is a local conversation artifact. This report does not establish a superpolynomial minimum in R_mix341 or the noncircular B3 bridge.

## IDEA -> SEARCH -> ITERATE

Initial falsifiable idea: use Braun's certified bit pigeonhole hard family and its strict 3-CNF chain to obtain a new mixed logical cost invariant. Falsifiers: (F1) a deleted 3-CNF facet cannot be satisfied; (F2) a paid binary-gate ER shortcut gives a short mixed proof; (F3) a polynomial-size original-source Res(XOR) proof can be compiled from a compact typed gate-RES proof; (F4) historical accepted byte grammar supports every asserted gate/facet reference.

Project SEARCH showed F1 and F2 were **already solved**, not novel: LSPV-1/340 proves all 3-CNF chain facets essential, LSPV-1/341 and LSPV-3/343 derive unary PHP via paid gates/RES, and LSPV-5/299 proves a syntactic ER_2-to-mixed simulation under typed exposed-defining-facet semantics. The revised idea tests F3 as an exact *reverse* proof-system normalization claim. F4 remains blocked by unspecified native R_mix341 facet/reference bytes. No previously established construction is rebranded as new.

## Family, original encoding, quantified theorem/model

Let n=2^ell, m=n+1, ell>=2 and b_(i,t) be the t-th hole-label bit of pigeon i. The **original bit-PHP** B_ell has one width-2ell clause per i<j and hole label z:

$$
C_{ijz}=\bigvee_{t<\ell}[b_{it}\ne z_t]\lor\bigvee_{t<\ell}[b_{jt}\ne z_t].
$$

It has M=n*binom(n+1,2) clauses. The **exact strict signed 3-CNF** G_ell replaces each ordered length 2ell clause (a_1,...,a_(2ell)) by fresh chain clauses:

$$
(a_1\lor a_2\lor y_1)\land
\bigwedge_{r=1}^{2\ell-4}(\neg y_r\lor a_{r+2}\lor y_{r+1})
\land(\neg y_{2\ell-3}\lor a_{2\ell-1}\lor a_{2\ell}).
$$

Counts: M_3=M(2ell-2) original strict-three facets; V_3=(n+1)ell+M(2ell-3) variables. ASCII signed decimal DIMACS input lengths are Theta(n^3 ell^2) bits for both original and chained formulas. Project /340 proved every chain facet essential and gave a SAT deletion witness; this does **not** preserve proof-size hardness under 3-CNF conversion.

**External theorem (Braun, arXiv:2609.23015, September 2026):** for ell>=32, every unrestricted shared-DAG Res(XOR) refutation of **original B_ell**, including source clauses in its size, has strictly more than

$$
L_ell=\exp\left(\frac{n}{32768\ell^2}\right)
$$

nodes. The model permits arbitrary DAG sharing and no regularity/depth bound, but has no charged conservative extension variables as in ER. The paper links Lean formalization; we have **not** independently checked the Lean kernel or expert mathematical correctness. This is an external model-specific claim, not an all-SAT-machine bound.

**Existing shortcut:** Cook's classical Extended Resolution PHP proof, combined with LSPV-1/341's polynomial gated extraction from strict G_ell to unary PHP, provides a polynomial-size typed binary-gate ER proof pi_ell of G_ell under /299's precise exposed-definition-facet semantics. The complete historical native byte grammar is not authenticated, so a native checker-accepted Cook-tail trace is **not claimed**.

## Explicit-output backtranslation firewall (conditional corollary)

For **every** putative compiler T which receives the original B_ell, its strict 3-CNF G_ell and a short typed gate-RES pi_ell, if T outputs a correct **explicit** Res(XOR) shared-DAG refutation of the **original B_ell**, then that output must contain >L_ell nodes, regardless of its internal algorithm, shared subcomputations, strategy choices, temporary exponential representations or search optimality. This follows immediately by applying Braun's exact lower bound to the completed output. Since input/proof are polynomial in n and ell, **no polynomial-output-size translation of this specified type exists**, conditional on both source theorems.

Any bit-output implementation must perform Omega(L_ell) output bit writes/time, and a fully materialized explicit proof stores Omega(L_ell) bits. Streaming output may use less peak space, so no general peak-space lower bound is claimed. Along N=|enc(G_ell)|=Theta(n^3 ell^2), output time is

$$
\exp\!\left(\Omega\left(\frac{N^{1/3}}{(\log N)^{8/3}}\right)\right).
$$

If counting paid non-source output nodes, subtract M original nodes; the asymptotic bound remains. This is a **legal counterexample to a precisely stated reverse R/ER -> original Res(XOR) polynomial normalization**, not a lower bound on R_mix341, no transfer from a lower bound on B_ell to Res(XOR) hardness on G_ell, and not evidence for B1, B2, B3 or P != NP.

For branching proof chains: all AND obligations and context assumptions must be discharged; a lemma Gamma |- C cannot leak to incompatible branches. Sharing counts once in a valid DAG. Braun's output target already permits full DAG sharing. Historical R_mix341 is not silently extended with split/discharge/weakening rules.

## Computational replay and distinct costs

A fresh Python producer and independent no-import JS checker rebuilt /340's **previously known** chain essentiality and strict Resolution reconstruction for ell=1,2,3 (2,4,8 holes), with ell=1 used **only as a width-two degenerate parser/recovery control**, not as an exact-width-three family member. Counts (original clauses, 3-CNF facets, variables, RES recovery nodes): (6,6,3,0), (40,80,50,40), (288,1152,891,864). Every deletion witness satisfies all other source facets; opposite-sign, malformed-header and corrupt-pivot controls were included. Independent JS passed **1,336,036 assertions**, including five malformed and three corrupt rejections. The separate output-parameter checker passed 21 assertions, with no claim of verifying Braun or Cook asymptotically. No authoritative native R_mix341 checker was run.

Ideal mixed paid-node cost, explicit evidence bits, bit writes/output time, verifier cost, construction/search work, weighted depth, peak space and retrieval/recomputation are **different measures**. Output-time lower bound concerns only a demanded Res(XOR) proof stream, and does not constrain a SAT machine which need not print such a certificate.

## Sources and limitations

Governing current handoff and issue #3, AGENTS.md, CODEX.md and repo pnp-research skill were read. Project prior /340 blob e25ebbe9, /341 handoff dfe88801, /343 blob b3138056, /299 blob 71e3f22b, /341 native grammar c87acd11, current LSPV-1/426, LSPV-3/430 and LSPV-5/370 were read. Actual Grok paths GROKPROOF/2026-11-05_1428_PROGRESS.md and 2026-11-05_1913_PROGRESS.md and Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex were read and provide no B3 theorem.

External GitHub pinned: konard/p-vs-np@ecedd2b45f1c524d85c00b2da27a9c140025550c; blkph0x/p-vs-np-proof-research@7dedc73f758dfbdc072e7aa29dfc08505761ebd5; meelgroup/frat-xor@18cd6bc17af10a9891c10a846ce966166f9fe0dc; openai/math@4eaee87548250b2682affda7d05d947c05554bae. Actual code searches: `extended resolution bit pigeonhole`, `bit pigeonhole proof extension`, `resolution pigeonhole`, `xor clause`, and project `BPHP extended resolution shortcut` and `Braun lower bound extension`. FRAT-XOR provides proof-checking infrastructure, not the project native checker or a B3 lemma. **Direct Google-branded interactive search unavailable**; indexed web and authenticated GitHub were used.

Primary sources: Braun, *An Exponential Lower Bound for the Bit Pigeonhole Principle in Resolution over Parities* (2026), https://arxiv.org/abs/2609.23015; Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution* (1976); Haken, *The Intractability of Resolution* (1985). For exact 3-CNF Resolution-hard family control, odd expander Tseitin is Resolution-hard (Urquhart 1987) but has the project verified 4h-1 mixed AND3/GF2 proof.

**Remaining gaps OPEN:** historical accepted DEF/facet/private/exported-wire byte grammar and a complete native Cook-tail replay; a truly superpolynomial full R_mix341 worst-case Wbar_R; noncircular B3, SAT in P => polynomial Wbar_R for this same R. Root main.tex was not edited because full byte-preserving content readback was not available.
