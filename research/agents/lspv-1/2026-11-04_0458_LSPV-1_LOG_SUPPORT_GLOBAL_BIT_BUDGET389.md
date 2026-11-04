# LSPV-1/389: Logarithmic per-port support gives a global node-to-bit budget

**November 4, 2026, 04:58 PST, America/Los_Angeles.** **PROVED/EXACT as an elementary typed-interface metatheorem, independent specialist review pending; COMPUTATIONAL finite controls. CONDITIONAL/NOT APPLICABLE to any enlargement of the unchanged R_mix341 unless that enlargement is separately authorized.** Neither B1/B2/B3 nor a superpolynomial lower bound for the whole mixed calculus is proved. P versus NP remains **OPEN**.

## 1. Starting theorem and fixed original calculus

Haken (1985), *The Intractability of Resolution*, Theor. Comp. Sci. 39, 297–308 (DOI 10.1016/0304-3975(85)90144-6): for standard unary pigeonhole CNF \(P_h=\mathrm{PHP}_{h+1}^h\), with \(h(h+1)\) variables and \(m_h=(h+1)+h\binom{h+1}{2}\) clauses, there exist \(c>0,h_0\) such that **for every** \(h\ge h_0\), **every** unrestricted ordinary shared-DAG Resolution refutation has at least \(2^{ch}\) lines. Standard explicitly indexed signed source lists use \(N_h=\Theta(h^3\log(h+2))\) bits. With free sources, paid derived Resolution lines are at least \(2^{ch}-m_h\). The quantifiers and proof rules do **not** cover Extended Resolution, Res(\(\oplus\)), arbitrary uniform SAT machines or the project mixed calculus. Cook (1976) supplies polynomial Extended Resolution PHP proofs; odd Tseitin has a polynomial native GF(2) shortcut.

The **unchanged** \(R_{\mathrm{mix341}}\) is the original LSPV-2/341 blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`: zero-cost authenticated original CNF clauses; unit-paid distinct derived RES, bounded-original-support AND3, binary GF(2) XOR, one-root locally justified LOCAL-CONVERT and conservative two-input DEF nodes. Each derived node cites at most two source/ancestor nodes. LSPV-5/335 (blob \`d47094c22297ca89d40104156ff41323480a0734\`) has **already** proved, for the *literal private-root abstract-rule reading*, polynomial node-to-bit normalization \(O((N+q+2)^3)\) and an \(\Omega(L)\) cost to faithfully normalize a sensitive length-\(L\) supplied private circuit. This run **does not duplicate or supersede** that result and does not change the actual R's LOCAL-CONVERT support limit or wire rules.

## 2. A separate, strictly scoped typed-interface theorem

Fix in advance a sound typed refutational system \(\mathcal G\) with free authenticated source clauses, strictly positive unit weight per derived node, each node at most two antecedent-node pointers, and **at most a constant \(a\ge1\) public-port observations per paid node**. Some node records may contain an arbitrarily long *private* finite acyclic Boolean circuit. Its externally observed outputs may reference previously authenticated boundary wires. Every use and legality judgment is extensional in the **joint values** of those observed wires; names may be consistently alpha-renamed. Every globally reusable fresh independent wire must originate in a separately paid conservative DEF node. No uncharged universal entailment oracle, one-node bundled proof or instance-specific answer axiom is legal.

All non-circuit records are clauses, reduced affine masks, bounded tables, gate opcodes or constant-arity pointers over at most \(v+q\) authenticated original/paid variable names, where \(v\le N\) original distinct identifiers occur in the explicit \(N\)-bit source. Their conventional canonical serialization uses \(O((N+q+2)^3)\) bits altogether. This explicit grammar hypothesis is needed, not inferred from soundness.

For each original proof \(\pi\) with \(q\ge1\) paid nodes and source bits \(N\), let \(M=N+q+2\). Each circuit-output port **actually observed** by a later paid node or final contradiction has a known syntactic dependency set \(S_j\) of authenticated earlier boundary wires with

$$
|S_j|\le b:=\max(1,\lceil c\log_2 M\rceil)
$$

for one fixed constant \(c\ge0\). Its legal local truth/implication check is performed over these explicitly named \(S_j\), or is otherwise invariant under replacement by a Boolean circuit having identical truth values on **every** assignment of \(S_j\). This is an all-proof hypothesis, not a change to \(R_{\mathrm{mix341}}\) (whose original LOCAL-CONVERT support is constant).

**Theorem 389 (global logarithmic-support node-to-bit normalization).** For every \(N,q\) and every such finite valid \(q\)-node refutation \(\pi\), there exists a same-source, same-authenticated-dependency-DAG refutation \(\widehat\pi\) with at most \(q\) paid nodes and

$$
G(\widehat\pi)\le (aq+1)b2^b
$$

private Boolean gates across all replacement circuit payloads, where \(G\) excludes the original non-circuit records. Its complete canonical encoded bit length is bounded by

$$
\boxed{|\langle\widehat\pi\rangle|
\le K_{a,c} M^{\max\{3,c+2\}}\log_2(M+2).}
$$

Constants depend on the *fixed* grammar, \(a\) and \(c\), never on the original payload lengths, formula, proof or \(q\). When \(c=1\), this gives \(O(M^3\log M)\) evidence bits. Proof **search** and transforming a supplied exponentially long payload are not included.

**Proof.** Topologically traverse the paid outer DAG. Each paid continuation mentions at most \(a\) public ports, so at most \(aq+1\) output references are semantically live across the entire proof, including the terminal output. For each live output \(j\), inductively interpret its finite original private acyclic circuit as one Boolean function \(f_j:\{0,1\}^{S_j}\to\{0,1\}\). Its complete DNF, built as a disjunction of at most \(2^{|S_j|}\) signed minterms of width \(|S_j|\), needs at most \(|S_j|2^{|S_j|}\le b2^b\) constant-fanin gates; constants and a signed literal can use bounded size. Use fresh internal private names and replace all observed output aliases consistently. Thus the **joint vector** of all live ports equals the original on every boundary assignment, not only on a chosen satisfying assignment or at the root. By the extensional legal-rule hypothesis, every later local justification and condition is preserved, and no globally usable fresh independent variable is introduced. The original proof ancestry and each of its \(q\) charges remain.

There are at most \(aq+1\) observed outputs, proving \(G\le(aq+1)b2^b\). Since \(2^b\le 2M^c\) for \(c\ge0\) up to a harmless constant and \(b=O_c(\log M)\), \(G=O_{a,c}(M^{c+1}\log M)\). Canonical private gate IDs, paid DEF names and public aliases use at most \(O(N+\log(M+G+2))=O(N+\log M)\) bits per reference, including sparse declared-original identifiers. Hence the gates occupy \(O(M^{c+2}\log M)\) bits. Add \(O(M^3)\) bits for the unchanged non-circuit records and explicit source; the displayed bound follows. The construction is an *existence* proof and makes no polynomial-in-\(M\) claim for inspecting the original circuit payloads. QED.

**Corollary (bounded proof budget).** In any fixed sound, complete, effectively checked *typed fragment* where every valid proof satisfies these hypotheses and Resolution supplies completeness, existence of a refutation of cost \(\le q\) is decidable by finite enumeration of certificates of the displayed bound. Its exact minimum for valid UNSAT inputs and worst-case profile are computable, although search may be astronomical. This is LSPV-1/385's known finite-enumeration criterion applied to a broader **per-port logarithmic-support** class. No polynomial bound on \(q\), no B3 and no deterministic polynomial SAT decision time follows.

## 3. Four exact falsifiers

**F1: Long private payloads necessarily require long *minimal certificate bits*. FALSE under the typed hypotheses.** The DNF bank depends only on \(M\) and the observed port supports, not original payload length \(L\). It may take \(\Omega(L)\) or more work to read and compile the supplied record, consistent with LSPV-5/335.

**F2: Support bound \(b\) alone lower-bounds exponential work. FALSE.** The displayed \(b2^b\) is an *upper* bound for DNF, not a lower bound. Parity and many low-rank Boolean functions have compact circuits even with \(b\) large, as earlier affine controls show.

**F3: One node may observe exponentially many independent ports at no syntax cost and the \(aq+1\) bound still holds. FALSE.** Bounded charged observation arity is an explicit hypothesis. An uncharged, syntax-sensitive bundled port list requires separately accounting for its length; it is not automatically handled by a \(q\)-only measure.

**F4: The theorem legalizes growing-support LOCAL-CONVERT in the unchanged R_mix341. FALSE.** The project original specifies a constant-support local check and a single observable conclusion. The logarithmic-support theorem is a metatheorem about a larger typed class of possible interfaces and gives no permission to enlarge R. The literal full-R node-to-bit normalization from Red Team/335 already handles actual private-root semantics; the **remaining real gap is B3**, not simply another bit bound.

## 4. Quantifiers and physical ledger

Fix \(R=R_{\mathrm{mix341}}\), unchanged. \(W_R(F)=\min_\pi\sum_{v\in\pi\text{ paid}}1\) on valid UNSAT CNF; \(\overline W_R(N)=\max\{W_R(F):F\in\mathrm{UNSAT}, |\langle F\rangle|\le N\}\) with empty maximum zero. All three **OPEN** obligations are B1 \(\forall A\exists p_A\forall F\in\mathrm{UNSAT}:W_R(F)\le p_A(|F|+T_A(F))\); B2 \(\forall A\exists p_A\forall N:\overline W_R(N)\le p_A(N+T_A^{wc}(N))\) with \(T_A^{wc}\) maximized over **all binary strings** including malformed inputs; and B3 \(\mathrm{SAT}\in P\Rightarrow\overline W_R(N)=N^{O(1)}\) for the **same** fixed R. B1 implies B2 implies B3. An optimized logical proof is chosen freely, but that does not supply optimizer time.

For an explicitly supplied private DAG of \(L\) bits, a direct compiler reads \(L\), computes syntactic support, evaluates each of at most \(aq+1\) ports on \(2^b\) assignments (worst-case \(O((aq+1)2^bL)\) elementary gate operations plus indexed access, parsing and output), builds the DNF bank, checks types and emits \(\widehat\pi\). This can be exponential in \(M\) when \(L\) is. Eager storage of supplied gates has \(O(L)\) writable bits and potentially \(O(G(N+\log M))\) output bits; streaming or repeated evaluation changes the time–space tradeoff. No inference from paid outer nodes to physical runtime, output length, simultaneous peak space or FLMV lower bounds is made. Any all-phase child-space claim must use \(s'\le\max\{\rho,\eta,\lambda,\lambda s\}\) with \(\rho\) covering allocate-then-free phases.

## 5. Independent finite controls and limitations

A deterministic Python producer and a separately authored Node verifier checked six observed-port families with boundary sizes \(b=1,\dots,6\), seven correlated outputs each (AND, OR, XOR, weak threshold (ties accepted), alias, negated alias and signed conjunction), all \(2^b\) assignments, and matching DNF output vectors. Producer recorded 891 assertion instances and independent verifier passed 232 checks, including seven strict signed-CNF SAT/UNSAT/malformed cases and \(K_4\) odd/even parity 0/8 controls. Deterministic, no seed. This verifies Boolean-function compilation on toy interfaces only: **it is not a native end-to-end R_mix341 proof checker or an asymptotic proof by experiment**. Local hashes of producer, independent verifier and raw ledger are included in the collaboration handoff.

## 6. Corpus, novelty, and independent assessments

Recovered the 2026-11-02 12:04 shared refocus, active issue #3 through LSPV-3/391, \`AGENTS.md\` blob \`19656af1\`, \`CODEX.md\` blob \`754999f5\`, \`.codex/skills/pnp-research/SKILL.md\` blob \`b8df83a7\`, original LSPV-2/341 blob \`c87acd11\`, LSPV-1/380 blob \`d880acaa\`, /385, /386 blob \`82f85a2d\`, /387 blob \`3b1db2c5\`, /388 blob \`bbc39f5f\`, LSPV-3/391 blob \`816c4732\`, LSPV-4/382 and Red Team/334, /335 blob \`d47094c2\`. Existing LSPV-1/380 already proves heterogeneous \(r b2^b\) normalization **as a typed circuit construction polynomial in supplied evidence length \(L\)**; /386 gives an **all-proof** \(N+q\) bit cap for constant support. The incremental content here combines them for **logarithmic supports on each live port across an entire \(q\)-node proof**, with an \(N+q\)-only proof-bit cap. Earlier all-proof private-root full-R result /335 is stronger for the actual fixed three-variable grammar. No novel SAT-hard family or P vs NP claim.

Actual Grok assessment \`GROKPROOF/2026-11-04_1217_PROGRESS.md\` blob \`cae0560d\` still lacks a fully charged all-input ARC/FLMV compiler; its qualitative \(\Omega(\sqrt S)\) cut-search claim is not independently justified as a universal theorem, and LSPV-4/382 gives concrete cut-width falsifiers. Actual Claude report \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\` blob \`9a5b05d6\` is a restricted one-tape crossing-sequence result and not a B3 bridge. Research queries: project "logarithmic support proof node normalization", "support k O(log(N+q))", "semantic quotient collapse", "TQBF relativization B3", "blum speedup worst-case"; external Haken 1985, Cook 1976, Blum 1967 and Cook–Reckhow 1979. Discarded as already proved: QBF-relativization B3 (LSPV-1/360), semantic quotient collapse (Red Team/323), source-monotonicity/direct sum (Red Team/305). GitHub/openai general proof-checker search previously documented in /386 and /388; no available implementation was used here.

**What changed:** a new restricted log-support **all-proof bit compactness statement**, not a general SAT-time lower bound. **Next decisive mathematical target:** ask LSPV-5 to stress-test the all-proof port-count/hypothesis boundary; then focus LSPV-1 on the genuinely open B3 simulation of rejecting computations in the unchanged R_mix341. Proof translation must justify algorithm correctness/reflection. No task identities, schedules, enabled states, original weights or R rules are changed.

## References

[1] Haken A. *The Intractability of Resolution*. Theoretical Computer Science 39 (1985), 297–308. DOI 10.1016/0304-3975(85)90144-6.

[2] Cook SA. *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*. SIGACT News 8(4) (1976), 28–32.

[3] Cook SA, Reckhow RA. *The Relative Efficiency of Propositional Proof Systems*. J Symbolic Logic 44 (1979), 36–50.

[4] Project LSPV-1/380, /385, /386, /388; LSPV-5/REFEREE334, /335; and original LSPV-2/341 as cited above.
