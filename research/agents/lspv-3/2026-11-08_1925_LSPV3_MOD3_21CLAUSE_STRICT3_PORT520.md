# LSPV-3/520: Delete redundant one-hot AMO clauses to obtain a published-hard proper strict 3-CNF, with an exact original-source RES recovery macro

**2026-11-08 19:25 PST | Route B, LSPV-3 | PROVED/RESTRICTED analytic transfer and local GF(2)-affine obstruction; COMPUTATIONAL independent checks; historical R_mix341 and P versus NP OPEN.**

**Proof-chain IDs:** New [P2-L3-520]; directly refines [P2-L1-518], [P2-L1-522], [P2-C3], [P2-D1], [P2-D3], [P2-F6]. The load-bearing [P2-B1] and [P2-B2] remain **OPEN**, as do P=NP nodes [P1-01], [P1-03] and [P1-04]. This entry addresses a *published restricted hard family* and a source-preserving transfer, not all-rule R_mix341 hardness.

## IDEA before SEARCH: prediction and four falsifiers

**Hypothesis.** For cubic modulo-3 Tseitin on one-hot edge indicators, the 3-element at-least-one clause on each edge plus the 18 signed forbidden vertex triples per vertex already imply all at-most-one clauses. Deleting all binary AMO clauses from the *standard published-hard CNF* therefore produces an **exact, proper, original-variable strict-3CNF subformula** that is still UNSAT, with the original lower bound transferring in the correct direction simply by clause inclusion. Furthermore, a source-authenticated ordinary Resolution macro can reconstruct every deleted AMO clause at constant paid cost. The local mod-3 vertex relation has no nontrivial GF(2)-affine consequence beyond the three one-hot parity equations.

Registered falsifiers: F1, a multi-hot satisfying assignment surviving all local forbidden triples and three at-least-one clauses; F2, one clause of the compressed family is not proper signed width three, or its source is not a literal subset of Pang's defined CNF; F3, some AMO requires an uncharged source, improper oriented RES, auxiliary DEF or implicit weakening, or the proposed 12-step macro fails; F4, the claimed exponential bound belongs to another proof system, or the local GF(2) row carries a mod-3 charge not accounted for in the rank argument. None fired in the stated model. Historical checker byte acceptance is *not* tested.

## SEARCH and continuity, actual sources and scopes

Both entire root trackers were read: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 bytes) and `proof2.txt` blob `061aee5ffdf27393ff5ea96c807f2da91efd5367` (592,669 bytes, at prepublication review). Issue #3 and the governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (blob `c3889a3e514ddbd747150dcb68607013a3b2d154`), `AGENTS.md`, `CODEX.md`, and `.codex/skills/pnp-research/SKILL.md` (blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`) were examined. Original historical prose is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`): at most two named premises, unit charge for RES, full-width RES, typed AND3/XOR/LOCAL/DEF. Its recovered verifier `experiments/arc/lspv2_341_independent_verify.js` (blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`) does not authenticate full mixed RES/DEF/LOCAL accepted bytes.

Direct peer work reused, not duplicated: LSPV-1/518 (blob `407ca3822d21387a4710d8ec41aebc831cda7856`) uses two shared padding clauses per standard binary AMO; LSPV-1/522 (blob `ab0cd2db22f67ed57486d5048fc804813a39d5b0`) derives nine separate local vertex output clauses with 18 paid RES; LSPV-3/519 (blob `2c4fedf2f649c167f764d35d1eefaba64802755e`) supplies a different Q_n matching strict3 conversion. Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md` (blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`) and Claude `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` (blob `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9`) contain independent restricted-model cautions, not the present interface.

**Primary paper read in full HTML:** Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, revised **2026-10-24**, §7.1 definition and Theorem 7.2(b), https://arxiv.org/abs/2610.00837 . It defines standard `Tseitin_q(G,b)` with unique-value ALO/AMO and signed flow-conservation clauses. On fixed-degree regular edge expanders, for distinct primes p,q and fixed r, it establishes exp(Omega(h)) DAG size in Res(PC_r/F_p). This is a **2026 preprint** and the theorem is not authority about R_mix341. The earlier linear PC degree is as cited by Pang to Alekhnovich--Razborov and Ben-Sasson--Galesi--Impagliazzo--Pudlak.

Change-aware external corpus: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; and `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`. None is an authenticated historical mixed port. Google-branded search was not available; primary arXiv text and public web search were used.

## ITERATE: exact signed proper 3-CNF family (no auxiliary variables or padding)

Let G=(V,E) be any connected, simple, cubic oriented graph, h=|V|, m=3h/2, with charges b(v) in Z_3 satisfying sum_v b(v) != 0 mod 3. For each edge e introduce three **original** Boolean atoms x_{e,0},x_{e,1},x_{e,2}. Add one at-least-one source clause per edge:

$$
A_e=x_{e,0}\lor x_{e,1}\lor x_{e,2}.
$$

For each vertex v with three distinct incident edges e_1,e_2,e_3 and orientation signs s_{v,i} in {+1,-1}, include precisely the 18 signed forbidden clauses

$$
C_{v,a_1,a_2,a_3}=\neg x_{e_1,a_1}\lor\neg x_{e_2,a_2}\lor\neg x_{e_3,a_3}
\quad\text{whenever}\quad
\sum_{i=1}^{3}s_{v,i}a_i\not\equiv b(v)\pmod 3.
$$

Call the conjunction `T_core(G,b)`. It has **exactly 18h+m=39h/2 proper signed strict 3-clauses on 3m=9h/2 Boolean variables**, and canonical DIMACS bit length N=Theta(h log(h+2)) for an indexed expander family. No new variables or source OR gates are introduced. The standard Pang one-hot Tseitin CNF additionally has three binary AMO clauses per edge and therefore 24h clauses. Crucially, `T_core` is a **literal clause subset** of this standard CNF, not an equisatisfiable formula generated by an unproved hardness-preserving gadget.

**Theorem 520.1, local forcing and global exactness (PROVED/RESTRICTED).** At any vertex, all three ALO clauses and all 18 forbidden triples imply that each of the three incident edge groups has exactly one true atom. Indeed ALO makes each group nonempty. If one group had two distinct values a,a', fix true values in the other two groups; at most one of a,a' satisfies the signed modular sum, so a false forbidden triple would have all three atoms true. Hence all groups are one-hot. The remaining clauses then enforce the exact signed Z_3 flow equations. Summing around oriented edges gives 0=sum_v b(v) !=0, so `T_core(G,b)` is UNSAT. If the total charge is zero, the connected incidence system has rank h-1 over F_3 and precisely 3^(m-h+1) one-hot satisfying assignments. The source is therefore exact on SAT and UNSAT labels.

**Theorem 520.2, lower bound transfers in the valid direction (PROVED/RESTRICTED, conditional only on published theorem's stated premises).** For any fixed, source-monotone propositional proof calculus S in which proof steps are unaffected by *adding* extra source clauses,

$$
W_S(T_{\rm core}(G,b))\ \ge\ W_S(\mathrm{Tseitin}_3(G,b)),
$$

because a refutation from the clause **subset** `T_core` is also a refutation from the standard formula. Taking S = Res(PC_r/F_2), fixed r, and the cubic edge-expanders within Pang's Theorem 7.2(b) yields exp(Omega(h)) DAG-size lower bounds in that **fixed restricted calculus** on genuine original-source proper strict 3-CNF. In binary encoded length N=Theta(h log h), this reads exp(Omega(N/log N)) along this family. This inference needs **no** preservation theorem for an equisatisfiable gadget; clause-subset inclusion provides the correct proof simulation. It does **not** transfer into the complete stronger R_mix341, which permits charged DEF and other algebraic interfaces.

**Theorem 520.3, 12-RES source recovery macro (PROVED/RESTRICTED).** Fix a vertex, an incident target edge e, and distinct values a,a'. Let f,g denote the other incident edge groups. For each f-value b and each g-value c, choose t in {a,a'} that violates the signed vertex equation, and use the **original** source clause (not x_{e,t} OR not x_{f,b} OR not x_{g,c}). Resolve the three such clauses successively against the original source A_g on its three positive pivots, costing three oriented RES nodes, to derive

$$
\neg x_{e,a}\lor\neg x_{e,a'}\lor\neg x_{f,b}.
$$

Do this for b=0,1,2 (nine nodes); resolve these three outputs against the original A_f (three further oriented RES nodes). The exact final clause is

$$
\neg x_{e,a}\lor\neg x_{e,a'}.
$$

Thus **every omitted standard AMO** has an original-source-authenticated 12-node ordinary RES derivation, with no DEF, weakening, case-split, oracle, LOCAL, or invented multi-premise inference. Every internal clause is derived by correctly oriented full-width binary Resolution and may have width four; original **source clauses**, not intermediate proof lines, are required to have width three. With 3m AMOs, the entire standard input can be recovered in <=36m=54h paid RES steps (before optional sharing). These are valid *ordinary Resolution rule* certificates, not accepted-byte historical checker executions.

**Theorem 520.4, exact one-hot affine-hull obstruction (PROVED/RESTRICTED).** For q>=2 consider the one-hot encoded 3-input relation a+b+c=t in Z_q as a set V_q of q^2 Boolean vectors in F_2^(3q). Its GF(2)-affine hull has dimension

$$
\operatorname{affdim}_{\mathbb F_2}(V_q)=3(q-1)-\mathbf 1_{2\mid q}.
$$

Proof: any affine equation on one-hot vectors restricts to functions A(a)+B(b)+C(t-a-b)=d in F_2. Subtracting the a=0 and b=0 equations shows the common difference E(x)=C(t-x)+C(t) is a group homomorphism Z_q -> F_2. It is zero if q is odd and has precisely one nonzero choice if q is even. The three one-hot group-parity equations are always independent; in the even case there is one further equation given by parity of the selected labels. This proves the dimension formula. Signed orientations and charge are coordinate permutations, so the result remains true for all local vertex types. For **q=3**, the only affine GF(2) consequences over the original nine Boolean atoms are the three per-edge parity=1 equations; no GF(2) row on these original atoms conveys the mod-3 charge. This **does not** exclude nonaffine AND3/RES, paid DEF, auxiliary equations, or global shared proofs. It is a local exact-affinity port obstruction, not a mixed-system lower bound.

## Independent executable checks and falsification

Executed standalone Python `lspv3_520_modq_affine_port.py` locally, and separately implemented Node.js `lspv3_520_modq_affine_compact.cjs`. Python: all **24** charge/orientation strict3 local sources; each has 21 proper clauses, 9 models, affine rank 6, and every individual original clause deletion gains models (13 models after one forbidden deletion, 58 after one ALO deletion). **216** exact original-source 12-RES AMO packets accepted; **648** corrupted packet variants rejected; **102** independent general-modulus affine-hull controls q=2..13; **5,409** assertion groups. K4 original-source graph: 78 strict3 clauses, 18 variables, zero satisfying one-hot assignments for nonzero total charge (0- and 0-? controls: charges (1,0,0,0) and (2,0,0,0)), and 27 for zero total charge. The local onehot forcing theorem upgrades onehot enumeration to all Boolean assignments. Independently authored Node program: 24 strict3 cases, 216 exact RES certificates, 648 negative controls, 48 modulus cases q<=9 and **58,488** internal assertions. Python source, original K4 DIMACS and full raw JSON are separately preserved as run artifacts. No official historical mixed byte checker and no CakeML checker were run; their acceptance must not be inferred.

**Resource separation:** 12 distinct binary RES nodes per local AMO, each with at most two named parents and no free multi-hint step. Literal and node IDs occupy O(log h) bits in the global indexed family; each macro has constant 12 nodes and O(log h) bits per identifier, and all source AMOs can be recovered with O(h) logical nodes and O(h log h) explicit trace bits. Construction, source parsing, graph incidence/orientation authentication, source/index reads, lookup, recording, verification, output and peak arrays are additional physical work. The Python and Node assertion counts are finite tests, not Turing-machine time/space bounds. Free optimal proof choice may find much shorter proofs; this is a legal upper control only.

## Publication, dependencies, remaining gap

The new reliable contribution is a *strict 3-CNF subformula with exact lower-bound-monotone transfer* from published opposite-characteristic hard Tseitin, together with a concrete original-source ordinary-Resolution backfill and sharp local GF(2)-affinity obstruction. Existing LSPV-1/518's padded encoding remains correct at its prior scope; this is an alternative without padding or extra variables, not a claim that /518 failed.

Historical port/accepted-byte semantics [P2-D1], complete mixed normalization [P2-C3], full mixed superpolynomial Wbar_R [P2-B1], and noncircular B3 [P2-B2] are **OPEN**. The established Res(PC_r/F2) lower bound cannot be promoted to the stronger R_mix341, which may possess polynomial ER-like shortcuts. No algorithm-independent computation lower bound or P versus NP resolution is claimed. The exact five-agent allocation, schedules, enabled states, historical rules/weights and other agents' files were not modified.
