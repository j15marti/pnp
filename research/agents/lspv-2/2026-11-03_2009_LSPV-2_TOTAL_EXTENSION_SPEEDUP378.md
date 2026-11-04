# LSPV-2/378: Conservative total extensions preserve every source witness but destroy Resolution hardness

**November 3, 2026, 20:09 PST (America/Los_Angeles).** Role: PNP SAT-Circuit Reduction Builder. **PROVED/EXACT** mathematical construction by combination of Haken/Cook known theorems with elementary source-witness lemma; **COMPUTATIONAL** independently reproduced finite witness tests; **OPEN** transfer to all legal Rmix341 rules, B1/B2/B3, general SAT machine hardness, P versus NP. This is not a new lower bound.

## Target and known certified anchor

Let \(P_h=\mathrm{PHP}_{h+1}^{h}\) be the standard *unary* pigeonhole contradiction on variables \(x_{ij}\), \(1\le i\le h+1,\ 1\le j\le h\). Its signed CNF contains occupancy clauses \(\bigvee_j x_{ij}\), and collision clauses \(\neg x_{ij}\vee\neg x_{kj}\), \(i<k\), in explicit ASCII DIMACS. There are \(v_h=h(h+1)\) original variables and \(m_h=(h+1)+h\binom{h+1}{2}=\Theta(h^3)\) original clauses; the bit length is \(N_h=\Theta(h^3\log(h+2))\).

**KNOWN THEOREM (Haken 1985):** There exist absolute \(c>0,h_0\) such that for every \(h\ge h_0\), every *unrestricted shared-DAG ordinary Resolution* refutation of the original clauses of \(P_h\) requires at least \(2^{ch}\) proof lines. With original clauses free and distinct derived resolvents unit-paid, \(W_{\rm Res}(P_h)\ge 2^{ch}-m_h=2^{\Omega(h)}\). This is not an Extended Resolution, \(\mathrm{Res}(\oplus)\), \(R_{\mathrm{mix341}}\), or arbitrary machine lower bound.

**KNOWN THEOREM (Cook 1976):** Unary PHP has polynomial-size Extended Resolution refutations. The explicit recursive reduction uses definitions \(q_{ij}\leftrightarrow (p_{ij}\vee (p_{i,h}\wedge p_{h+1,j}))\), in \(\sum_{k=2}^{h}k(k-1)=h(h+1)(h-1)/3\) fresh variables across levels, and a polynomial (often quoted \(O(h^4)\)) number of Resolution steps. A proof-size reference giving \(O(h^4)\) is Grosof–Zhang–Heule (2022). For this report **only polynomial size is needed**; exact constants and the full Cook proof's local derivation sequence have not been independently replayed. Each gate's four standard CNF clauses are
$$
(q\vee\neg a),\quad (q\vee\neg b\vee\neg c),\quad
(\neg q\vee a\vee b),\quad (\neg q\vee a\vee c).
$$
They enforce \(q=a\vee(b\wedge c)\). Acyclic gate order supplies a unique assignment to *all* auxiliary variables for each assignment to the original variables.

## New derived no-go lemma: source-fibre retention does not preserve proof hardness

**PROVED/EXACT (ordinary Resolution, after treating extension clauses as explicit additional premises).** There is an explicit family of acyclic total *functional* conservative extensions \(D_h(X,Y)\), each containing \(O(h^3)\) constant-width definition clauses and \(O(h^3)\) fresh variables, such that \(G_h=P_h\wedge D_h\) obeys all of:

1. **Literal exact source retention:** every original \(P_h\) clause appears unmodified in \(G_h\), with the same literal signs, and the original signed incidence hypergraph remains an induced source substructure.
2. **Unique complete source fibre:** for *every* assignment \(a\in\{0,1\}^{v_h}\), exactly one auxiliary assignment \(b\) satisfies \(D_h(a,b)\). This is stronger than merely preserving both SAT/UNSAT labels.
3. **Every original clause remains indispensable:** for each original clause \(C\in P_h\), \((P_h\setminus\{C\})\wedge D_h\) is satisfiable.
4. **No exponential size hiding:** \(|\operatorname{encode}(G_h)|=\Theta(h^3\log(h+2))\) bits, the same order as the original explicit source.
5. **Exponential-to-polynomial Resolution gap:**
$$
W_{\rm Res}(P_h)=2^{\Omega(h)},\qquad
W_{\rm Res}(G_h)=h^{O(1)}.
$$
These are proof-size claims for two *different* input CNFs, not a claimed free rewrite within ordinary Resolution or a runtime bound.

**Proof.** Cook's recursive gate list is acyclic, hence each original assignment extends uniquely through the gate definitions. Source retention and size follow by direct counting; each definition has four clauses involving at most three literals. To prove clause indispensability: removing an occupancy clause for pigeon \(i\) permits exactly the other \(h\) pigeons to occupy distinct holes, leaving \(i\) without a hole. Removing the collision clause for pigeons \(i,k\) and hole \(j\) permits precisely \(i,k\) to share \(j\), and assigns the remaining \(h-1\) pigeons injectively to the other \(h-1\) holes. Each assignment falsifies exactly the deleted original clause and extends uniquely to satisfy \(D_h\). Finally, take Cook's polynomial Extended Resolution refutation of \(P_h\). Move every fresh definitional clause to the source list at the outset. The remaining proof is an ordinary Resolution refutation of \(P_h\wedge D_h\), using no extension rule *inside that proof*, with polynomially many derived nodes. The original formula retains Haken's lower bound. QED.

**Generalization:** For *any* clause-minimally UNSAT family \(F_h\) possessing a polynomial-size Extended Resolution refutation, the same method creates an explicit total functional conservative extension \(D_h\) such that every original source clause is still deletion-essential but \(F_h\wedge D_h\) has polynomial-size *ordinary Resolution* refutations. The polynomial-size claim is relative to the size of the supplied ER proof, and an efficient uniform generator requires the ER proofs themselves to be uniformly constructible.

**Important restriction:** In the project-fixed \(R_{\mathrm{mix341}}\), paid auxiliary DEF, RES, AND3, GF(2) and LOCAL-CONVERT operations exist. A Cook-style gate may be expressible by two paid signed-AND2 definitions plus local clauses, so PHP is a mandatory **polynomial-extended-proof control** for any proposed mixed hardness family. However an actual *source-authenticated* \(R_{\mathrm{mix341}}\) Cook-proof compiler must still audit each permitted definition interface and exact legal inference. No new complete-\(R_{\mathrm{mix341}}\) minimum or certified global shortcut is asserted here.

## Transfer diagnosis and attempted falsifiers

F1. **Conservative total source extension preserves the Haken exponential Resolution lower bound**: **FALSIFIED** by \(G_h\). Totality, uniqueness and retention of every original source clause do not repair this.

F2. **Clause deletion essentiality survives total conservative gates**: **PROVED**, for all original clauses, including the signed occupancy/collision cases. Thus the previously proved source-arity floor \(m_h-1\) may survive without imposing anything exponential.

F3. **Gate descriptions, conversion or proof checking secretly require exponentially many bits**: **FALSIFIED** for this construction. \(\Theta(h^3)\) gates each have constant-arity semantics and \(O(\log h)\)-bit pointers; explicit output length \(\Theta(h^3\log h)\); constructing source and definitions costs polynomial bit work and polynomial live memory. Cook proof output, verification, and parsing are separately polynomial, not constant; a minimum node count alone does not dominate physical time.

F4. **The construction proves B1/B2/B3 failure, or arbitrarily fast SAT decision**: **FALSE inference**. It concerns ordinary Resolution on two inputs. It supplies neither an all-algorithm machine lower bound nor a counterexample to global worst-case B2/B3. For \(R_{\mathrm{mix341}}\), full mixed minimum-hardness and B3 remain open.

For each fixed uniform total correct binary-input SAT decider \(A\), including malformed inputs, the unchanged open obligations are:
$$
\mathrm{B1}:\ \forall A\ \exists p_A\ \forall F\in\mathrm{UNSAT}:
W_R(F)\le p_A(|F|+T_A(F)),
$$
$$
\mathrm{B2}:\ \forall A\ \exists p_A\ \forall N:
\overline W_R(N)\le p_A(N+T_A^{wc}(N)),
$$
and **B3 (primary)**: \(\mathrm{SAT}\in P\Rightarrow\overline W_{R_{\mathrm{mix341}}}(N)\le N^{O(1)}\), *for the same fixed system*. No implication from Haken to any of these is established; an exponential-cost backtranslation is invalid for this purpose.

## Finite tests and fully charged ledger

A standalone Python producer validated \(h=1,\ldots,6\): source clause counts, acyclic gates, exact four-clause semantics, an explicit SAT witness for deletion of **each** original clause, source rejection after the correct clause is restored, and extension uniqueness. It exhaustively enumerated all \(2^{v_h}\) original assignments for \(h\le3\), tested six malformed encodings, and checked odd/even \(K_4\) parity controls (0/8 models): **22,596 assertions**. An independently written standalone Node.js verifier passed **132,587 assertions** and independently agreed on source/auxiliary counts and deletion witnesses. These tests verify gate semantics and source essentiality, **not** the full Cook derivation or a shortest Resolution/ER/Rmix proof.

Ledger: logical node count \(q\), encoded proof length \(L_\pi\), source and gate construction bit work, symbol/index/pointer reading, checking, output, and peak live memory are distinct variables. A \(q\)-node shared proof is not automatically an \(O(q)\)-bit or \(O(q)\)-time physical execution. Materialization and verification of the exhibited polynomial gate list and an explicit polynomial proof are polynomial in \(h\), with \(\Omega(|\operatorname{encode}(G_h)|)\) writes when explicitly output. Exponential alternative intermediates are allowed but must be charged, and compact alternatives are not excluded. No FLMV machine-contraction claim follows.

## Peer assessments, duplication and literature ledger

Located directories by GitHub repository-contents listing, not inferred paths. Grok: \`GROKPROOF/2026-11-04_0116_PROGRESS.md\` (blob \`ca5a835356eb918b8cb4ab94d14de6174edeab03\`) and \`GROKPROOF/2026-11-03_1912PST_PROGRESS.md\` (blob \`66576e888e5c147c64264d4856089b6d3e7903e3\`) still report no universal fully charged all-input FLMV contraction. Claude: \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\` (blob \`1f9fc727d3e2b009cba7afec2a93beb62959dd67\`) concerns alternation-trading portfolio rules, not all SAT algorithms; older \`research/agents/claude/2026-09-30_CLAUDE-0266_review.tex\` (blob \`694c1c8169d9a193397b94e6ee572c476e639a94\`) notes previous invalid Fourier/influence shortcuts. Both are research evidence, not a correctness warrant.

Peer LSPV-1/378 \`research/coordination/2026-11-03_1955_LSPV1_CLAUSE_DELETION_FIBRE378_FIVE_ROLE_HANDOFF.md\` independently proved a **linear** original-clause-essentiality floor for total conservative extensions. The present theorem supplies an explicit polynomial-source, exact-unique-fibre **exponential Resolution-hardness escape** despite that floor. LSPV-2/377 already showed a global length-preserving syntactic involution; the incremental distinction here is *unchanged* original clauses, no lost deletion witnesses, *unique* conservative gate extensions, and polynomial output/certificate size. LSPV-3/381 reverse-affine-DAG checker avoids exponential unfolding; LSPV-5/327 charge-uniform-generator theorem is equivalent to SAT in P and therefore not a new B3 bridge. No published lower bound was regenerated.

Primary sources: Haken (1985), *The Intractability of Resolution*, TCS 39:297-308; Cook (1976), *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4):28-32; Grosof–Zhang–Heule (2022), arXiv:2207.11284 (Cook polynomial-size \(O(n^4)\) baseline and shorter DRAT construction). Project governance: \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, November 2 refocus directive; issue #3 read. GitHub public web returned 404 due access visibility, so authenticated GitHub connector was used. Search of relevant public \`github.com/openai\` implementations returned no applicable PHP proof compiler; no implementation claim inferred.

## Next specific gap

Audit the exact \(R_{\mathrm{mix341}}\) gate-definition rule to decide whether a *fully source-authenticated polynomial-cost Cook refutation* can be compiled with a separately checkable proof stream. Derive explicit per-node legality and encoded bit overhead, not just semantic satisfiability equivalence. The absence of this compiler does not weaken the proven ordinary-Resolution conservative-extension counterexample. B1/B2/B3 and P versus NP remain **OPEN**.
