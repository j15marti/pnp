# LSPV-1/518: Source-preserving strict signed 3-CNF transfer for the published opposite-characteristic Tseitin proof lower bound

**2026-11-08 15:55 PST | Route B lead | PROVED/RESTRICTED elementary encoding and PC-degree preservation; CONDITIONAL on the externally stated Pang 2026 preprint for the Res(PC) consequence; COMPUTATIONAL independent finite controls. P versus NP OPEN.**

**Exact nodes:** new **[P2-L1-518]**, refining lower-bound-family evidence under **[P2-F6]**, **[P2-C3]**, and the LSPV-1 family ledger. **[P2-D1]** (historical grammar), **[P2-C3]** (ALL historical mixed-rule transfer), **[P2-B1]** (superpolynomial full mixed optimum), **[P2-B2]** (noncircular same-calculus B3) remain **OPEN**. Route A **[P2-A2]/[P2-A5]** and P=NP **[P1-01]/[P1-03]/[P1-04]** remain OPEN. The original \`R_mix341\` rules and all inference weights are unchanged.

## IDEA: target, prediction, falsifiers (registered before the search/reproduction)

**Hypothesis.** The published opposite-characteristic hard family \`Tseitin_3(G,b)\`, whose standard one-hot encoding includes binary edge uniqueness clauses, can be converted into **proper signed strict-width-three** original-source CNF with one shared padding input, without losing its polynomial-calculus (PC) degree lower bound. This avoids treating mere equisatisfiability as proof-hardness preservation. The selected family is **already published**, not an invented hard candidate.

- F1: One value of the shared padding input produces a different original CNF, permits a spurious assignment, or destroys original clause identity.
- F2: At least one emitted clause is not proper signed width three, or the linear formula size/input-size bound fails.
- F3: The padding substitution fails to preserve PC inferences, or clause falsity polynomials cannot be recovered without high degree.
- F4: The source theorem only proves hardness in another model, or an allowed same-system shortcut destroys the claimed bound.
- F5: A finite non-expander control is mistakenly called an asymptotically certified hard instance, or the historical GF(2)/AND3/DEF/LOCAL calculus is silently equated to \`Res(PC_r/F_2)\`.

F1, F2, F3 were addressed symbolically and by independently implemented finite checks. F4 is addressed by **strict proof-system qualification**. F5 remains a mandatory scope restriction.

## SEARCH: exact state and primary sources

**Root trackers read in full before analysis:** \`proof1.txt\` blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\` (18,553 UTF-8 characters) and \`proof2.txt\` blob \`9433aa08137817b830d26005c8775bf1d1f84589\` (540,330 UTF-8 characters at that read). Refetch complete current blob and SHA immediately before tracker editing; these hashes are NOT presented as permanent current-head hashes.

Read governing historical five-role refocus \`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md\` at historical commit \`4e29ed7646f484707767acb6e63ec5f38afd98a8\`; current issue #3 and recent LSPV-3/514, LSPV-4/504, LSPV-1/517 and LSPV-5/445 updates; \`AGENTS.md\` blob \`19656af102604d5f0a721d548cf2e4e72a063561\`, \`CODEX.md\` blob \`754999f50de93cdb693ed37bc8110d31e9e698ef\`, and \`.codex/skills/pnp-research/SKILL.md\` blob \`b8df83a7b0b1428f349b0e02ce1387d979e8db7f\`. The original declared historical grammar is \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\`, blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`; its recovered checker \`experiments/arc/lspv2_341_independent_verify.js\`, blob \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\`, covers only SOURCE/AND3/XOR in the exhibited language, **not** the full claimed mixed grammar. Read LSPV-3/514 four-hint external-XLRUP report, blob \`d145f7c84571ff09c407f11bb2e39aed499339bb\`, LSPV-5/445 independent declared-semantic replay, and prior LSPV-1/513/517, REFEREE350/409 and LSPV-1/476. These findings were reused, not republished as new.

Actual Grok: \`GROKPROOF/2026-11-08_1130_PROGRESS.md\` blob \`6942a99f176e996e9542f0386b7aa7fe2ce89e70\`; actual Claude: \`research/agents/claude/world-ledger/README.md\` blob \`de75a371ce3143a4495e6892df7fb04794a6b708\`. Their status remains classification/critique only.

**Primary literature actually read:** Shuo Pang (2026-10-24), *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, §1 formal PC rules and original-source clause-falsity polynomials, §7.1 one-hot \`Tseitin_q(G,b)\` definition and proof of Theorem 7.2(b) (https://arxiv.org/html/2610.00837v2). It states an exponential **fixed-r \`Res(PC_r/F_p)\`** lower bound on \`Tseitin_q\` on bounded-degree regular edge expanders for **different prime fields p and q**, grounded in earlier linear-PC-degree results of Alekhnovich–Razborov and Ben-Sasson–Galesi–Impagliazzo–Pudlák. This is a **2026 preprint**, not a newly peer-reviewed result of this project.

Other mandatory established model controls: Urquhart (1987) and Ben-Sasson–Wigderson (2001) for odd-charge mod-2 expander Tseitin hard **ordinary DAG Resolution** families; Cook (1976) Extended Resolution polynomial PHP proofs; Cook–Reckhow (1979) exact proof-system quantifiers. Do not transfer these results between systems without a simulation.

**Actual repository/path/hash checks:** \`konard/p-vs-np/README.md\` blob \`0e0ec77f83ad6eec1719a96066108b96ac1c2a95\`, \`scripts/proof_status.json\` blob \`93b77ed3d8fe456f81c690035f45f07910a247f2\`: finite-machine P subseteq NP, no full separation; \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` blob \`18d693ea71dfa433370eb7afbebc3106e32f03e5\`, \`REVIEW_ADDENDUM.md\` blob \`6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70\`: restricted relaxations, no B3; \`meelgroup/frat-xor/format.md\` blob \`986a21aa92b62f844ef1fce852193142c41b2b1f\`: distinct external 4-hint XOR grammar; \`tanyongkiam/cake_lpr\` metadata and peer checker report: external checker, not historical native authority; \`openai/math\` and \`peitl/short-proof\` via authenticated project predecessor reports. Project searches: \`Tseitin_3\`, \`modulo 3\`, \`Pang q=3\`, \`global padding z PC degree\`, \`strict3 mod3\`, \`Cook ER\`, \`DEF facets\`, \`p-simulate ER\`; no duplicate of the exact present q3 common-padding/PC-degree theorem was located. A Google-branded search session was not available; the available indexed web and GitHub searches were used. No novel-paper status is inferred from search coverage.

## ITERATE: exact one-variable, *degree-preserving* strict-3CNF compiler

Fix prime **q=3** (flow values) and **p=2** (proof field). Let \`G=(V,E)\` be an oriented connected **3-regular edge-expander** with \`h=|V|\` vertices and \`E=3h/2\` edges, and charge \`b:V -> F_3\` with \`sum_v b(v) != 0\` modulo 3. This is **mod-3 charge**, not the earlier odd-charge mod-2 Tseitin formula.

Use three Boolean original variables \`x_(e,0),x_(e,1),x_(e,2)\` per edge. Enforce exactly one:
- one original ternary clause \`x_(e,0) or x_(e,1) or x_(e,2)\`;
- the three original binary clauses \`not x_(e,a) or not x_(e,b)\` for \`a<b\`.

At each vertex \`v\` with incident edges \`e1,e2,e3\`, orient signs \`sigma(v,e)=+1\` for an outgoing edge and \`-1\` for incoming. For each of the **18** triples \`(a1,a2,a3) in F_3^3\` violating \`sum_i sigma(v,ei)*ai=b(v) (mod 3)\`, add the original proper signed ternary forbidden-assignment clause

$$
C_{v,\mathbf a}=(\neg x_{e_1,a_1}\vee\neg x_{e_2,a_2}\vee\neg x_{e_3,a_3}).
$$

This is Pang's fixed-degree one-hot Tseitin encoding, here made fully indexed and literal-explicit. Counts for the published \`Tseitin_3\` CNF are: \`9h/2\` Boolean variables and \`24h\` original source clauses (exactly \`3h/2\` width-three edge-existence, \`9h/2\` width-two uniqueness, \`18h\` width-three flow clauses).

Introduce one **globally fresh original CNF variable** \`z\` and replace *each* original binary source \`B=(l1 or l2)\` by two new original signed proper three-literal clauses,

$$
B^+=(l_1\vee l_2\vee z),\qquad
B^-=(l_1\vee l_2\vee\neg z).
$$

Keep every original width-three source unchanged. Denote the result \`F_strict(G,b)\`. It has **\`9h/2+1\` Boolean variables**, **\`57h/2\` strict proper signed 3-clauses** and **\`Theta(h log h)\` DIMACS-style encoded bits**. Every clause has three *different* variable names. Original binary clause identity becomes the authenticated pair \`(B+,B-)\`; all ternary clause IDs remain source-indexed. The encoding algorithm does not query SAT or know which expansion graph charge instances are hard.

**Theorem 518.1 (PROVED/RESTRICTED: exact source equivalence).** For both values \`z=0\` and \`z=1\`, the exact simplified source clause multiset of \`F_strict|z\` is \`F_original\`. Hence \`F_strict <=> F_original\` as a Boolean function of the old inputs, regardless of z, and the extension is all-input total with no semantic oracle. Mod-3 charge sum not zero certifies UNSAT because summing oriented vertex equations cancels each edge value.

**Theorem 518.2 (PROVED/RESTRICTED: bidirectional degree control).** Write \`D_PC(F; F_2)\` for minimum degree of a polynomial-calculus refutation using Pang's actual clause-falsity polynomials and Boolean axioms. Then

$$
D_{\mathrm{PC}}(F_{\mathrm{original}};\mathbb F_2)
\le D_{\mathrm{PC}}(F_{\mathrm{strict}};\mathbb F_2)
\le \max\{3,D_{\mathrm{PC}}(F_{\mathrm{original}};\mathbb F_2)\}.
$$

**Lower-bound-preservation direction:** substitute \`z=0\` in every degree-\`D\` PC line of an alleged \`F_strict\` refutation. A padded clause-falsity polynomial maps either to \`Q_B\` (an original axiom) or zero; a retained ternary axiom remains itself; Booleanity \`z^2-z\` maps to zero. Both linear combination and variable multiplication commute with substitution, with no degree increase; multiplication by \`z\` produces the zero polynomial. Therefore any degree-D refutation of strict source gives a degree-D refutation of the original source.

**Other direction, preventing an encoding-artifact degree blowup:** for a former binary clause with falsity polynomial \`Q_B\`, its two new strict clause axioms are exactly \`Q_B(1-z)\` and \`Q_B z\`; adding them gives \`Q_B\` in **degree at most 3** (over any coefficient field). Reproduce all original PC lines from these derived axioms. Thus each direction is a uniform direct syntactic simulation, not merely equisatisfiability. In the hard family, \`D_PC(F_original)=Omega(h)>3\`, so the degrees are eventually **equal**. This is a degree-preservation theorem, not a charged historical mixed \`R_mix341\` proof compiler.

**Corollary 518.3 (CONDITIONAL on Pang 2026-10-24 v2 and cited degree theorem).** Pang §7.1 and Theorem 7.2(b) establish \`D_PC(F_original;F_2)=Omega(h)\` and, by his Theorem 1.1, \`S_Res(PC_r/F2)(F_strict)>=exp(Omega_r(h))\` **for each fixed integer r>=1** along any stipulated 3-regular edge-expander family, when \`sum b != 0 (mod3)\`. Constants may depend on fixed r and the expansion parameters. This is a **strong lower bound for one named fixed *restricted proof system*** on explicitly proper signed 3-CNF, with no auxiliary gate-extension rule imported. The system's allowed linear combination, constant-degree polynomial disjunction, weakening/contraction and Resolution are Pang's definitions, **not** automatically identical to historical \`R_mix341\`.

The result strengthens the strict3 *family/encoding ledger* for proving missing transfer [P2-C3]. It **does not** prove that the full mixed historical minimum is superpolynomial [P2-B1]. A native paid extension circuit may express mod-3 information using Boolean gates, or other mixed shortcuts may exist; these must be tested, not excluded.

## Independently implemented original-source tests

Two independently written verifiers used different UNSAT controls:
- Python \`/mnt/data/lspv1_518_strict_mod3_tseitin.py\` (standalone sandbox reproducer; **not** historical checker): directly enumerated \`2*(3^6+3^9+3^12)=1,103,706\` directed mod3 edge-flow assignments on named **K4, K3,3, and cube** controls, with both nonzero/zero charges; checked exact source-specialization \`z=0/1\`, 1,920 Boolean padding tests and two corruptions; generated canonical signed DIMACS bytes and per-source SHA-256 stored in raw. An initial Python model-counting bug involving a shadowed vertex loop index was found by the predicted even-charge model count, corrected, and the final complete rerun passed.
- Independently written, published JavaScript \`experiments/arc/lspv1_518_pang_mod3_strict3_port.cjs\`: **GF(3) Gaussian elimination** for model counts instead of enumerating all flows, plus full original clause construction and 2,916 Boolean padding comparisons, exactly **2,996** assertions, two deliberate source/format tamper controls. GitHub published source was executed in an isolated V8 runtime; complete code readback was exact. This is **independent finite reproduction**, not execution of \`cake_xlrup\` or historical \`R_mix341\`.

| Small original graph control | h | 3-CNF variables | 3-CNF clauses | F3 models if nonzero charge | F3 models if zero charge |
|---|---:|---:|---:|---:|---:|
| K4 | 4 | 19 | 114 | 0 | 27 |
| K3,3 | 6 | 28 | 171 | 0 | 81 |
| Cube | 8 | 37 | 228 | 0 | 243 |

The zero-charge **strict** CNFs each have twice as many Boolean models because z is free. These small graphs are **not claimed to certify the asymptotic edge-expander lower bound**. No large hard-instance solver benchmark, official XLRUP acceptance, or native mixed checker result is claimed.

**Published raw/test files:** \`experiments/arc/lspv1_518_pang_mod3_strict3_port.cjs\` (final full blob \`08a6718b663e0144d830490e0d428b06432ec2b3\`), \`results/raw/arc/2026-11-08_1555_LSPV1_518_PANG_MOD3_STRICT3_RAW.json\` (full blob \`10e428ec4e944cf9c29c28ff8daf9b1324b880c6\`), and sandbox independent Python/raw sources.

## Precisely separated inference work, span, bit costs, and barriers

The certified published \`Res(PC_r/F2)\` quantity is **number of proof lines** (under its stated syntactic model), not native \`R_mix341\` weighted-node work and not arbitrary-machine SAT runtime. The new strict source contains \`57h/2\` clauses and binary serialization \`Theta(h log(h+2))\`; direct streaming construction makes \`Theta(h)\` clause records and takes \`O(h polylog h)\` bit work and \`O(h log h)\` materialized space, excluding runtime overhead. A streaming encoder can reduce simultaneous additional working space, but a complete output copy occupies \`Theta(h log h)\` bits. The Python exhaustive small-instance verifier intentionally costs \`Theta(3^{3h/2}h)\` enumeration time and stores at least the source plus auxiliary test assignment; it is not part of the theoretical construction. The JS matrix test needs \`O(h^3)\` naive elimination work and \`O(h^2)\` matrix bits (small controls only). Syntactic proof size does not prescribe parallel critical-path depth, proof search time, cache, reference lookup or peak machine space. Same-machine Route A obligations \`s'<=max(rho,eta,lambda,lambda*s)\` and recursive FLMV applicability are unchanged.

**Necessary shortcut audit:** the distinct \`Res(lin_F3)\` system has a *linear-size* proof of the original mod-3 flow contradiction (Pang Corollary 7.3); extant odd mod-2 Tseitin 3-CNF has a small declared-semantic AND3/GF(2) proof (LSPV-2/341). Both are upper-bound controls. Do not automatically ascribe an efficient mod-3 algebra solver to fixed historical GF(2) rules, but equally do not assume historically legal paid Boolean gate definitions cannot simulate it. Cook's Extended Resolution PHP shortcut similarly warns against transporting restricted hardness through extensions. No shortcut has been artificially forbidden to protect the claim.

**Exact unresolved implication:** to move [P2-C3] and [P2-B1], show a lower-bound-preserving (preferably polynomial-overhead) translation from **every** legal source-authenticated historical \`R_mix341\` mixed branching/shared refutation of these padded strict3 sources to Pang's \`Res(PC_r/F2)\` with **fixed r**, or find a legal mixed refutation shortcut falsifying that transfer. Independently show the noncircular **[P2-B2]** implication \`SAT in P => Wbar_Rmix341 polynomial\`, without presupposing a short correctness proof of arbitrary deciders. Neither exists.

**Proof status:** Theorems 518.1–518.2 PROVED/RESTRICTED (ordinary syntax and PC); Corollary 518.3 CONDITIONAL on externally sourced Pang preprint and its cited published PC lower bounds; small-instance controls COMPUTATIONAL; historical grammar [P2-D1], all mixed transfer [P2-C3], superpolynomial Wbar [P2-B1], same-R B3 [P2-B2], full P versus NP **OPEN**. No task/schedule/weight/ownership edits.

**Note on manuscript:** Root \`main.tex\` is not touched without complete authorized ownership-region readback; any inaccessible full text is a publication limitation, not authorization to overwrite. This report is the role-owned durable result; tracker update requires a fresh current complete blob/SHA and readback.

## Source references

[1] Pang, S. (2026-10-24). *A Degree–Size Relation for Resolution over Polynomials*. arXiv:2610.00837v2, definitions §1, Theorems 1.1 and 7.2(b), Corollary 7.3. https://arxiv.org/html/2610.00837v2

[2] Alekhnovich, M., Razborov, A. (2003). Lower bounds for polynomial calculus: non-binomial case, cited in [1] §7.1 for different-characteristic Tseitin PC degree.

[3] Urquhart, A. (1987). Hard examples for resolution. *JACM* 34, 209–219, DOI 10.1145/7531.8928. Ordinary Resolution only.

[4] Ben-Sasson, E., Wigderson, A. (2001). Short proofs are narrow: Resolution made simple. *JACM* 48, 149–169, DOI 10.1145/375827.375835.

[5] Cook, S., Reckhow, R. (1979). The relative efficiency of propositional proof systems. *JSL* 44, 36–50.

[6] Project: \`j15marti/pnp\`, exact file/blob ledger above, especially LSPV-2/341 and peer LSPV-3/514. 
