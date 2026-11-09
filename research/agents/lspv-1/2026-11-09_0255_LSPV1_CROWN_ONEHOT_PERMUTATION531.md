# LSPV-1/531 | Exact no-auxiliary two-boundary modular CNF via the known crown-graph biclique theorem

**2026-11-09 02:55 PST | Route B lead | KNOWN THEOREM applied to the established one-hot modular interface; PROVED/RESTRICTED derivation; COMPUTATIONAL finite controls | P versus NP OPEN.**

## Target, IDEA, falsifiers, SEARCH, ITERATE

Target: sharpen the exact *two-boundary* original-indicator CNF representation control, explicitly exempted from [P2-L1-530]'s b>=3 GF(2) affine-hull result and complementary to [P2-L3-530]'s *q=3,b>=3* signed-flat-CNF lower bound. This is a representation theorem, **not** a refutation minimum for R_mix341.

IDEA: for two q-state one-hot groups, the relation y=pi(x) for a permutation pi can be represented by logarithmically many no-auxiliary unrestricted-width CNF clauses and has an exact Sperner-type minimum.

Predeclared falsifiers: (F1) a legal clause falsifies a valid matching assignment; (F2) a wrong-charge assignment survives the constructed clauses; (F3) an unrestricted signed clause whose one-hot falsifying set is not a rectangle breaks the biclique reduction; (F4) some finite q<=4 permits a smaller clause cover than the Sperner bound. Additional scope falsifier: extrapolating this two-group conclusion to b>=3 q=3, restricted strict-width-three formats, native derivations, or arbitrary mixed-calculus minimum.

SEARCH inspected current project [P2-L1-530], [P2-L3-530], [P2-L5-457], the actual peer handoff and issue #3; Grok progress and a Claude TPORT manuscript; current README/phase notes of konard/p-vs-np and blkph0x/p-vs-np-proof-research; frat-xor format documentation, cake_lpr README and openai/math contents. External primary literature: S. Bezrukov, D. Fronček and S. Rosenberg, "On biclique coverings", Discrete Mathematics 308 (2008), 319-323, which explicitly proves the crown-graph bound and tightness; also recent Boolean-rank/crown-graph literature. This is **prior art**, not a newly discovered combinatorial theorem. Pang arXiv:2610.00837v2 remains the specified distinct restricted proof lower bound for the project hard family.

ITERATE: recovered the exact one-hot-CNF corollary and gave explicit unsigned original-indicator clauses. q=5 has **four** clauses, not five (a falsifier to extending the q=3 formula q^(b-1) as an exact all-q count). No change to the q=3,b>=3 theorem, because its field/arity assumptions are different.

## Theorem 531.1 (KNOWN crown-graph theorem, explicit one-hot-CNF application)

Let q>=2, let pi:[q]->[q] be any permutation, and let X_0,...,X_(q-1) and Y_0,...,Y_(q-1) be original Boolean indicator variables subject to exactly-one semantics for each group. Let k(q) be the **minimum number of non-tautological CNF clauses on these original indicators, with arbitrary signs and unrestricted width and no auxiliary variables**, whose conjunction on one-hot assignments accepts exactly pairs (x,pi(x)). Then

$$
\boxed{k(q)=\min\left\{k\ge 0:q\le {k\choose\lfloor k/2\rfloor}\right\}.}
$$

In particular k(2)=2, k(3)=3, k(4)=4, k(5)=4, and k(q)=log_2(q)+(1/2)log_2(log_2(q))+O(1). The formula is invariant under charge and orientation because y=+- (c-x) mod q is a permutation.

**Proof, lower bound.** The falsity set of any clause on valid one-hot assignments is a Cartesian rectangle S_j x T_j: an indicator literal in group X affects only x, and similarly for Y. For soundness, that rectangle avoids the perfect matching M={(i,pi(i))}. For completeness, the q(q-1) off-matching cells must be covered by the k rectangles. Put L_i={j:i in S_j} and R_i={j:pi(i) in T_j}. Matching avoidance says L_i intersect R_i=empty. Off-matching coverage says L_i intersect R_t is nonempty for i != t. If L_i subseteq L_t then L_i intersect R_t=empty, contradiction. Thus the q distinct sets L_i form an antichain in the k-subset lattice. Sperner's theorem gives q <= binom(k,floor(k/2)).

**Proof, upper bound.** Choose q distinct constant-weight subsets L_i of [k] of size floor(k/2). For each coordinate j let S_j={i:j in L_i}, T_j={pi(i):j not in L_i}. Let C_j be the OR of **positive original indicators** X_i for i outside S_j and Y_t for t outside T_j. On one-hot inputs C_j is false exactly on S_j x T_j. Every diagonal (i,pi(i)) satisfies C_j for all j. Every i!=t has some j in L_i\L_t by equal-weight incomparability, and then (i,pi(t)) falsifies C_j. Therefore these k clauses represent exactly the desired relation. Each constructed clause has width exactly q, and q state pairs are valid. QED.

This is precisely the biclique-cover number of the crown graph K_(q,q) minus a perfect matching; it is **not a proof-system lower bound**. It restricts only the count of no-auxiliary CNF clauses over original one-hot indicators at a two-group interface, allowing arbitrarily long clauses. Complete Boolean CNF adds the ordinary exactly-one source constraints separately; their bits and proofs are not free. The q-state relation can alternatively be materialized with q signed implications (some shorter), or with paid auxiliary circuits. For b>=3, the ternary q=3 lower bound [P2-L3-530] remains a different exact statement.

## Finite original-domain and hostile controls

The published Python verifier independently executed 60 q/charge/sign configurations for 2<=q<=11 and checked 3,030 one-hot pairs. The independently authored JavaScript V8 implementation repeated all 60 cases, tested all q^2 one-hot assignments for each, and performed exhaustive signed-clause enumeration and exact rectangle-cover dynamic programming for q=2,3,4. For q=4 it enumerated 3^8=6,561 literal patterns and found 50 unique nonempty sound falsity masks, with 4 clauses necessary. q=5 has a four-clause explicit construction.

The predicate explicitly checks both rejection of wrong-charge pairs and preservation of valid pairs. These are finite checks, not execution of the historical checker. Non-one-hot malformed inputs are outside the semantic promise and must be rejected by an independent complete source recognizer; unauthorized argument relabeling, source substitution, and missing clauses are not tolerated.

## Family / theorem / encoding / shortcut / missing-transfer ledger

- Established hard family: opposite-characteristic odd-charge modulo-three Tseitin on fixed-degree expanders. Pang (2026) proves an exponential lower bound in fixed-r syntactic Res(PC_r/F_2), with source/encoding conditions, not for arbitrary SAT algorithms or paid extension systems. The project strict-three conversion is separately recorded under [P2-L1-518], [P2-L5-447].
- Exact two-boundary interface here: q-state original one-hot indicators; two groups; relation y=pi(x); k(q) clauses of width q; source exactly-one constraints separately charged. This is a *projection/representation* statement, not an UNSAT problem.
- Known shortcut: biclique antichain/constant-weight-code clauses, including q=5 four instead of five; native ER/GF2/nonlinear definitions may perform better. Compare [P2-L1-529] and [P2-L3-530].
- Remaining transfer: complete historical R_mix341 grammar [P2-D1], all-rule mixed-proofs [P2-C3], superpolynomial worst-case minimum [P2-B1], noncircular B3 [P2-B2], all OPEN. No case-split or strengthening rules were added.

## Resource separation and execution

Constructed clauses: k(q)=Theta(log q), q literals/record, O(q log q) indicator occurrences, and O(q log^2 q) bits under binary identifiers (before fixed record overhead). The original two exactly-one groups need 2q Boolean indicators and, with the usual pairwise at-most-one encoding, O(q^2) source clauses; they are **not** included in the k(q) count. The test program's finite run measured semantic evaluations only; there is no asymptotic machine-time/peak-space claim for historical R_mix341 or a SAT algorithm. Any proof construction, parsing, clause/materialization, retrieval, checking, indexing and peak simultaneous storage must be paid before claiming an actual upper bound. Shared-DAG global work, critical path and storage scheduling are unaffected by a local CNF count.

**TRACKER STATUS:** new restricted evidence relevant to [P2-L1-530], [P2-L3-530] and [P2-C3]; all main proof obligations remain OPEN. No claims of P=NP or P!=NP. Fixed historical grammar/weights and 2 Route A / 3 Route B assignments unchanged.

## Sources

1. S. Bezrukov, D. Fronček, S. Rosenberg (2008), "On biclique coverings", Discrete Mathematics 308(2-3), 319-323, https://dspace.vsb.cz/items/b3ea04bd-19f4-4c37-9c7a-de54b1134146 .
2. S. Pang (2026), "A Degree--Size Relation for Resolution over Polynomials", arXiv:2610.00837v2, https://arxiv.org/abs/2610.00837 .
3. G. Emdin, A. Kulikov, I. Mihajlin, N. Slezkin (2022), "CNF Encodings of Parity", arXiv:2203.01082, https://arxiv.org/abs/2203.01082 .
