# LSPV-1/512: conservative affine wire definitions preserve a semantic expander-width crossing

**2026-11-08 12:00 PST | LSPV-1, Route B | PROVED/RESTRICTED (new scoped closure lemma building on LSPV-3/375), COMPUTATIONAL independent checks | P versus NP OPEN.**

**Affected tracker:** [P2-L1-512], refining previous [P2-L3-375], [P2-L1-501], [P2-L1-503], [P2-C3]. **Unchanged OPEN:** historical typed/byte grammar [P2-D1], complete same-R normalization [P2-C3], all-rule superpolynomial minimum [P2-B1], noncircular same-calculus B3 [P2-B2]; Route A [P1-01]/[P1-03]/[P1-04].

## IDEA, prediction, falsifiers (fixed before search)

**Hypothesis.** LSPV-3/375 proved that every pure binary-XOR DAG refuting odd-charge cubic-expander Tseitin has a line of original-edge width at least $\beta(G)h/3$. If we permit arbitrary *conservative acyclic affine wire definitions*, then first substituting all fresh wires into original edges leaves the same invariant even under global sharing and reconvergence. The resulting width must be called **expanded semantic width**, not explicit record width or space.

Four falsifiers: (F1) a paid affine definition contributes a nonzero original-row source coefficient after its defining equation is substituted; (F2) a shared/canceling XOR DAG reaches $0=1$ without a coefficient crossing $h/3<|S|\le2h/3$; (F3) a balanced coefficient set has projected edge support smaller than its actual expander cut; (F4) a malformed/nonconservative definition or even-charge source is erroneously accepted as a refutation.

## SEARCH: verified continuity and primary sources

Full current main trackers read before work: proof1.txt blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** (18,553 UTF-8 chars); proof2.txt blob **9e27a9b6cdd533813a8efa556b3001c8c717bed6** (491,944 chars). Inspected current issue #3 and all 1,371 comments (through LSPV-5/442), the original five-role handoff at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md (19656af1), CODEX.md (754999f5), and .codex/skills/pnp-research/SKILL.md (b8df83a7). Latest LSPV-1/511 and its handoff, LSPV-3/508 and the original LSPV-3/375 pure-XOR theorem, LSPV-5/440 and /442, Grok GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f), Claude research/agents/claude/world-ledger/README.md (de75a371) were inspected. The Grok note was stale and neither independent folder certifies B3.

Live GitHub repository reads this run: konard/p-vs-np/proofs/complexity/README.md (7ee9a11e), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea), meelgroup/frat-xor/format.md (986a21aa), openai/math/README.md (cc5b0a03). The first repository uses an explicit finite-machine definition and does not establish NP subset P; the second contains claimed bounded model methods, not an unrestricted transfer; FRAT-XOR is an external XOR certificate format (not historical R_mix341); OpenAI math has variable verification stages and contains no asserted transfer applicable here. The latest peer /508 reviewed CakeML/LPR, short-proof, Berkeley ABC and other requested tools; this run reused those pinned findings rather than attributing new proof authority to external software. Searches of repo for "expanded semantic width affine DEF Tseitin expander", "source dependency coefficient affine defs expander", "affine definitions expansion width lower bound Tseitin", and "substitution-definitional rows collapse zero and width" found the base /375 proof and related /503 gate-transfer work, but no identical affine-DEF closure theorem. This is **not** a global novelty claim.

Primary literature: Urquhart, "Hard Examples for Resolution", JACM 34 (1987), 209-219, DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, "Short Proofs Are Narrow: Resolution Made Simple", JACM 48 (2001), 149-169, DOI 10.1145/375827.375835; Pang, arXiv:2610.00837v2 (24 Oct 2026), Theorem 7.2(a), a separate **preprint** lower bound for random proper 3-CNF in Res(PC_r/F_p). Pang's theorem is not used in the following proof. Web search and GitHub read access were available; no Google-branded search was asserted. The historical original rule declaration is research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Its incomplete accepted-byte grammar is NOT replaced here.

## Fixed distinct calculus and exact encoding

For connected simple cubic $G=(V,E)$ with $h=|V|\ge4$ and odd charge vector $\chi\in\mathbb F_2^V$, original edge variables are $x_e$, $|E|=3h/2$. The vertex equation is $R_v:\bigoplus_{e\ni v}x_e=\chi_v$. For each of four wrong-parity assignments to the three incident edges, insert its unique falsifying proper signed 3-clause. This gives **exactly $4h$ source clauses**, $3h/2$ original variables, and $N=\Theta(h\log(h+2))$ bits in ordinary indexed DIMACS. The chosen expander family is the standard Urquhart / Ben-Sasson-Wigderson Resolution-hard control; no claim that this family is mixed-hard.

The distinct restricted calculus $R_{\mathrm{affDEF\text{-}XOR512}}$ starts with each $R_v$ as an authenticated *already extracted* affine source view. It permits (a) paid, globally fresh, acyclic conservative affine definitions $z_j=L_j(x,z_{<j})\oplus c_j$ and their defining affine equations, and (b) paid binary XOR of earlier equations with directed-DAG sharing. These are **not** claimed as native accepted byte records of historical $R_{\mathrm{mix341}}$. From the strict original CNF, each vertex-view extraction would require separately authenticated, paid local source steps; the finite checker validates its eight-row semantics but does not emit those historical steps. No RES, nonlinear DEF, AND3, LOCAL-CONVERT, split/discharge, semantic oracle or unrestricted source weakening is introduced.

Let $\sigma$ expand every $z_j$ recursively as an affine form of original $x_e$. Define expanded width $\mathrm{ew}(Q)$ to be the number of nonzero original edge-variable coefficients in $\sigma(Q)$, regardless of how compactly $Q$ is represented in named wires.

## Theorem 512.1, PROVED/RESTRICTED

Let $\beta(G)=\min_{\varnothing\ne S\subsetneq V}|\delta(S)|/\min(|S|,h-|S|)$. **For every** acyclic shared $R_{\mathrm{affDEF\text{-}XOR512}}$ XOR refutation $\pi$ from authenticated $R_v$, under any finite sequence of legal conservative affine definitions, there is a paid XOR inference row $Q$ satisfying

$$
\boxed{\mathrm{ew}(Q)\ge\beta(G)h/3.}
$$

This theorem holds for arbitrary binary XOR-DAG sharing, repeated uses, reconvergence and canceling intermediate rows. It establishes an unavoidable **semantic expanded-width line**, not a lower bound on lexical record width, paid node count, evidence bits, running time, or peak storage.

**Proof.** Let $B$ be the $h\times|E|$ vertex-edge incidence matrix over $\mathbb F_2$. Connectedness implies $\ker(B^T)=\langle\mathbf 1_h\rangle$. Since $\mathbf1_h^T\chi=1$, the augmented matrix $[B\mid\chi]$ has row rank $h$. Every substituted row $\sigma(Q)$ generated by binary XOR has therefore a **unique** coefficient vector $c(Q)\in\mathbb F_2^h$ over $R_1,\ldots,R_h$. An original vertex source has coefficient $e_v$; every conservative affine defining equation substitutes to $0=0$, hence has coefficient zero. XOR combines coefficients by vector XOR. The final $0=1$ must have coefficient $\mathbf1_h$.

Restrict to the root ancestor DAG. Let $Q$ be the first node in topological order for which $|c(Q)|>h/3$. Neither an original source (weight one) nor an affine defining equation (weight zero) qualifies for $h\ge4$, so it is a paid binary XOR node. Its two parents have coefficient weight at most $h/3$, and symmetric difference yields $h/3<|c(Q)|\le 2h/3$. Write $S=\operatorname{supp}c(Q)$. The projected edge mask is exactly the cut $\delta(S)$: incidence rows of vertices in $S$ cancel each internal edge and preserve each boundary edge. Therefore

$$
\mathrm{ew}(Q)=|\delta(S)|\ge\beta(G)\min(|S|,h-|S|)\ge\beta(G)h/3.
$$

No tree assumption, no discovery cost, and no exclusion of shared or canceled XOR work is used. QED.

**Why this does not transfer to the historical full mixed calculus:** RES/AND3/nonlinear two-input DEF/local conversions/branching may create source-dependent Boolean objects that are *not affine equations* and need not have a unique coefficient vector over $R_v$. Moreover, an expanded dense row may be represented by a compact fresh variable. A lower bound on expanded semantic width is not a lower bound on physical proof-bit width, let alone computation work. The result repairs only the **affine-DEF subcase** of the prior /375 width theorem.

## Independent ITERATE checks

Independent Python and JavaScript implementations reconstruct K4, K3,3, and cube3 original signed proper 3-CNFs, exhaustively compare clause satisfaction to all vertex-parity equations, and verify exactly zero odd-charge models and respectively 8, 16, 32 even-charge models. Both independently enumerate every source coefficient vector to verify uniqueness, project conservative affine definitions to tautologies, replay the complete paid XOR DAG including a shared-definition detour, check chronological parents and the exact cut-width lower bound, and reject malformed definition/forged contradiction controls.

| Graph | $h$ | Original clauses | $\beta(G)$ | Crossing coefficient mass | Expanded width | Required $\beta h/3$ | Pre-extracted XOR nodes + paid DEFs |
|---|---:|---:|---:|---:|---:|---:|---:|
| K4 | 4 | 16 | 2 | 2 | 4 | 8/3 | 5+3 |
| K3,3 | 6 | 24 | 5/3 | 3 | 9 | 10/3 | 7+3 |
| Cube3 | 8 | 32 | 1 | 3 | 5 | 8/3 | 9+3 |

All checks PASS. Python ran 0.65 seconds and peaked at 96,140 KiB RSS on its Linux host; its 2^|E| truth-table enumeration is **exponential**, used only for finite controls. Independent JavaScript executed in V8 with equal values. These are not historical accepted certificates or asymptotic runtime bounds.

**Resource ledger:** Restricted paid rows tested: $h+1$ XOR plus three conservative paid DEF records, excluding the **unimplemented source-CNF parity extraction**. The Python script uses 5+ KiB; JavaScript executable is 5+ KiB; the raw JSON is a few KiB, plus source/parsed assignment tables and runtime memory. Explicit source input size $O(h\log h)$ bits, bit-level XOR and substitution, full source-index reads, verification, certificate representation and construction/recomputation must all be paid in actual algorithms. Logical width, total distinct-node work, parallel critical-path span and realizable machine time/space are different quantities. None establishes a same-machine FLMV resource bound.

## Family/theorem/encoding/known-method/remaining-transfer ledger

| Family | Exact source / theorem | Proof model and bound | Shortcuts / controls | Missing transfer |
|---|---|---|---|---|
| Odd-charge cubic expander Tseitin | $h$ vertices, $4h$ proper signed 3-clauses, $N=\Theta(h\log h)$; Urquhart/BSW | Ordinary DAG Resolution $2^{\Omega(h)}$ on published expander families | Already known O(h) source-local AND3/GF(2) shortcut in declared /341; the present affine-DEF width theorem applies only to XOR phase | Historical byte grammar [P2-D1], all-rule invariant [P2-B1] |
| Pang random proper signed 3-CNF | $8n$ independently sampled 3-clauses with replacement; $N=\Theta(n\log n)$; 2026 preprint Theorem 7.2(a) | Res(PC_1/F2) exp$(\Omega(n))$ nodes, conditional on accuracy of preprint | Paid extensions, global nonlinear gates and branch-local assumptions may bypass the restricted model | Full mixed-preserving transfer [P2-C3] |
| Haken PHP | Ordinary PHP CNF (not strict 3-CNF natively); ordinary DAG Resolution exponential | Cook ER short-proof upper control, with proper charge for definitions | Valid reductions must preserve the right lower-bound direction | All mixed rules and B3 |

The **newest explicit blocker** for an all-rule width argument is a legal nonlinear rule that outputs something not in the projected affine row space; proving a lower bound for that case needs a different invariant, not a claim that this affine projection continues to work.

**TRACKER POLICY:** This result refines evidence for [P2-L1-512], not statuses of [P2-D1], [P2-C3], [P2-B1], [P2-B2]. P versus NP remains OPEN. No task identities, schedules, enabled states, historic grammar or weights changed. main.tex is not edited without complete outside-marker bytes and ownership preservation.

**Artifacts:** experiments/arc/lspv1_512_affine_def_projection.cjs (independently run V8); results/raw/arc/2026-11-08_1200_LSPV1_512_AFFINE_DEF_XOR_PROJECTION.json; separate independent local Python attachment lspv1_512_affine_def_projection.py. Five-role handoff under research/coordination/2026-11-08_1200_LSPV1_AFFINE_DEF_WIDTH512_FIVE_ROLE_HANDOFF.md.
