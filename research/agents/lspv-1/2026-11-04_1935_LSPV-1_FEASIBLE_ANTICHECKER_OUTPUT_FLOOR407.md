# LSPV-1/407: Explicit Antichecker Output Floor and Conditional B3 Cost Audit

**November 4, 2026, 19:35 PST. PNP General SAT Lower-Bound Lead (LSPV-1).**  
**Classification:** PROVED/EXACT elementary bounded-circuit lookup lemma; COMPUTATIONAL independent finite checks; CONDITIONAL consequence for Pich-Santhanam antichecker hypothesis; **OPEN** B1, B2, B3, superpolynomial full-mixed worst-case Wbar, P versus NP. No rule, cost, schedule or agent changed.

## IDEA before SEARCH: falsifiable hypothesis

The immediately preceding LSPV-1/406 proved a conditional route from Pich-Santhanam's *unproved* feasible-antichecker hypothesis AC_k to polynomial worst-case refutation cost for the unchanged R_mix341. Test whether the explicit antichecker alternative could be generated much faster than the circuit bound s=n^k it must defeat.

Prediction: Every finite sample S of m distinct n-bit inputs with supplied n-bit verified outputs can be memorized by a shared binary-gate circuit with at most (2n-1)m gates. Consequently any explicit sample antichecker against *all* size-s circuits requires m>s/(2n-1) and Omega(s) written sample bits for s=n^k.

Falsifiers chosen first: (F1) gate budget violated; (F2) a sampled input gets the wrong memoized output; (F3) SAT witnesses unverified or invalid source instances; (F4) alternative globally correct SAT-search-circuit branch improperly excluded; (F5) confusion of encoded input bits n with number of CNF variables.

## SEARCH: sources actually read and duplication checks

Read the governing Nov. 2 12:04 PST directive at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e), current issue #3 through REFEREE351 and LSPV-1/406, LSPV-2/406, LSPV-3/407, LSPV-4/400, and AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md.

Fixed original calculus: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11): free authentic original signed CNF clauses, unit-cost binary RES, at-most-three-original-support AND3, binary GF(2) row XOR, bounded local LOCAL-CONVERT, and one charged fresh conservative two-input DEF. The original rule text still does **not** fix the serialization, public exported-wire identity or internal gate-payment policy for LOCAL-CONVERT. Do not silently complete it.

Duplicate audit: LSPV-1/357 already proves a one-sided reflection sufficient condition and a Gödelian unprovable-correct-decider counterexample. LSPV-1/406 already applies a *conditional* Pich-Santhanam feasible antichecker hypothesis to the native RES+DEF fragment. REFEREE317/350/351 already separate Cook-Reckhow systems, native typed proof interfaces and B3. None of these records states the quantitative lookup-output lower floor (407.1), although this memorization construction is elementary and not claimed novel to the wider literature.

Read primary [1], Pich-Santhanam ECCC TR23-199 (December 9, 2023), **Theorem 10, pp. 25–26** and proof, at https://eccc.weizmann.ac.il/report/2023/199/download. This theorem assumes one P-time generator f_k, a fixed S^1_2 proof of its *whole* all-length assertion, and an alternative of either a correct SAT search circuit or an explicitly represented antichecker carrying authenticated satisfiable witnesses, defeating every search circuit of size at most n^k. Theorem 10 concludes EF non-p-bounded implies infinitely-often n^k SAT circuit hardness. The **September 2023 Oxford author's manuscript** https://users.ox.ac.uk/~coml0742/papers/eopt.pdf has different theorem numbering: its Theorem 10 concerns discrete logarithms. Both primary PDFs were opened and their relevant page images inspected, preventing a mistaken cross-version theorem identification. The 2026 JACM publication (DOI 10.1145/3801091) was noted; its numbering should not be substituted without inspection. Primary [2] Cook-Reckhow, [3] Lipton-Young anticheckers, and Haken 1985 ordinary-Resolution versus Cook 1976 polynomial Extended-Resolution PHP shortcuts were reviewed.

Actual web queries: "Pich Santhanam Towards P != NP Theorem 10 antichecker"; "ECCC TR23-199 theorem 10 PDF"; "Lipton Young anticheckers size circuit memorization lower bound set size"; "circuit memorization m examples size O(mn) anti checker". **Direct Google-branded interface unavailable**; general web queries and primary original PDFs used, not a purported Google UI session.

Authenticated github.com/openai searches: "ExecCNFNodeSearchCosts", "ImplementationCertificates". Fully read openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean, blob 1ced21f4, and RuntimeAssembly.lean, blob 41df76f4; the latter explicitly leaves primitive implementation certificates open. They are execution-cost formalizations, not proof of AC_k or same-R B3. Actual Grok read: GROKPROOF/2026-11-04_2315_PROGRESS.md (blob f5b8ef62). Actual Claude reads: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727) and 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Their separately restricted lower bounds do not give AC_k or B3.

## ITERATE: exact elementary theorem

For each integer n>=1, each finite set S of m **distinct** strings in {0,1}^n, and every supplied map w:S -> {0,1}^n, there is a shared fan-in-two NOT, AND, OR Boolean circuit C_S with n inputs and n outputs such that

$$
\forall x\in S,\quad C_S(x)=w(x),
\qquad \#\mathrm{gates}(C_S)\le (2n-1)m.
$$

**PROOF.** If m=0, output zero constants with no gates. Otherwise precompute all n input negations. For each a in S use n-1 AND gates to form equality indicator E_a(x), true precisely when x=a, from appropriate positive or negated input literals. For each output bit t, output the OR of E_a for those a having w(a)_t=1, or constant zero if none. Each bit needs at most m-1 OR gates. Thus total cost <=n+m(n-1)+n(m-1)=(2n-1)m. Exactly one indicator fires on each sampled input. QED. This is a hardcoded finite sample circuit, *not* a uniform all-input SAT solver.

If all a in S are **valid satisfiable n-bit SAT instances** with checked n-bit padded satisfying witnesses w(a), and S is a genuine antichecker that defeats **every** n-input, n-output fan-in-two Boolean search circuit with at most s gates, then necessarily

$$
\boxed{m\ \ge\ \left\lfloor\frac{s}{2n-1}\right\rfloor+1.} \tag{407.1}
$$

For s=n^k, k>=3 fixed, this requires m=Omega(n^(k-1)); an **explicit list** of the distinct n-bit sampled SAT inputs writes at least n*m=Omega(n^k) bits before witnesses and graph metadata. Thus any honest bit-machine generator writing the complete explicit antichecker must take Omega(n^k) steps **on the antichecker branch**. This is a necessary condition, not tightness, existence, or any unrestricted SAT lower bound. Compressed symbolic sample sets require a different serialization/evidence analysis.

**Conditional corollary, separate from 407.1.** Suppose a single uniform f_k meets the *full, externally correct* Pich-Santhanam AC_k two-branch requirement and has total **output-inclusive** running time o(n^k) on unary 1^n. Then for all sufficiently large n it cannot take the explicit-antichecker branch, so it outputs an explicit SAT search circuit for all n-bit instances. Generate this circuit and evaluate it on the input to obtain one uniform polynomial-time SAT decider. The output size is at most the generator's time, so those circuits have o(n^k) encoded size. If the separate, unproved **S^1_2-provable** universal correctness clause of AC_k also holds, ECCC Theorem 10 makes EF polynomially bounded; standard EF-to-ER and paid original-source RES+DEF translation make Wbar_Rmix341 polynomially bounded. No LOCAL-CONVERT operation is used in this conditional upper transfer.

If the generator is merely "polynomial time" with degree >=k, this argument does not force its solver branch. Bare SAT in P does **not** imply AC_k or its formal S^1_2 proof. A hypothetical compression requiring substantial uncharged output expansion also voids the stated bit-output condition.

## Executable checks and costs

GitHub-readback Python producer builds real shared NOT/AND/OR DAGs, counts paid binary gates and replays all sample outputs. It enumerates **625 = 5^4** partial two-bit singleton-witness functions (missing witness denotes UNSAT for that input) plus **512** deterministic seeded distinct-sample tests for n=1..8. **1,137 cases, 9,572 producer assertions**, highest observed gate count **138**. Independent Node/JavaScript validator uses direct selector algebra, with **3,263 checks** across all 625 partial relations, and four deliberately corrupt raw records rejected. Actual signed-CNF SAT, UNSAT and tautology controls have respectively 1, 0 and 2 satisfying assignments; six malformed sample cases and a forged gate reference were rejected. Seed 202611041935. The theorem is symbolic; finite checks do not establish asymptotic B3 or any machine hardness.

Distinct costs: lookup gate count <=(2n-1)m; encoded netlist bits O(mn log(mn+n)); writing an *explicit sample list* >=nm bits; parsing/verification >=input and certificate reads; materialized peak memory may be Theta(mn log(mn)), with streaming/recomputation trading time and space. No finite optimum for original R_mix341 was claimed and no optimizer discovery cost was hidden.

**PRESERVED SEPARATIONS.** Haken's exponential PHP bound is for **ordinary explicit shared-DAG Resolution only**, with h+1 pigeons, h holes and polynomial signed source bits. Cook's ER proofs are polynomial, and odd Tseitin has native GF(2) shortcuts. None of those restricted lower bounds transfers to arbitrary SAT machines or the complete mixed calculus. Native LOCAL-CONVERT exported-wire grammar and full source compiler remain OPEN. The new AC_k output floor is about a separately declared finite search-circuit model, not a new legal native inference.

**Next exact missing step:** a genuinely all-length, fixed S^1_2-provable feasible antichecker generator, or a different **noncircular** same-R B3 implication, plus the other agents' native LOCAL-CONVERT port grammar audit. B1, B2, B3, full-mixed superpolynomial Wbar, and P versus NP remain OPEN.

### References

[1] J. Pich and R. Santhanam. *Towards P != NP from Extended Frege Lower Bounds*. ECCC TR23-199, December 2023, Theorem 10, pp. 25-26. https://eccc.weizmann.ac.il/report/2023/199/download. Journal of the ACM 73(2), 2026, DOI 10.1145/3801091.

[2] S. A. Cook and R. A. Reckhow. *The Relative Efficiency of Propositional Proof Systems*. J. Symbolic Logic 44(1), 1979.

[3] R. J. Lipton and N. E. Young. *Simple Strategies for Large Zero-Sum Games with Applications to Complexity Theory*. STOC, 1994; arXiv:cs/0205035.

[4] A. Haken. *The Intractability of Resolution*. Theoretical Computer Science 39 (1985):297-308.

[5] S. A. Cook. *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*. SIGACT News 8(4), 1976.
