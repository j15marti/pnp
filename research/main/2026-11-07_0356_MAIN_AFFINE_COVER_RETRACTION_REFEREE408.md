# LSPV-5/408 — affine terminal-cover retraction beyond branch trees

**2026-11-07 03:56 PST | Route B independent red team | PROVED/RESTRICTED abstract binary-GF(2) theorem; COMPUTATIONAL independent controls | historical R_mix341, all-mixed hardness, B1/B2/B3, and P versus NP remain OPEN**

## IDEA -> SEARCH -> ITERATE

### Initial claim and precise falsifiers

Hypothesis: a branching tree is unnecessary for the affine retraction behind `[P2-L5-407]`. Let $E$ be authenticated common affine rows. Let a finite collection of consistent affine contexts cover the entire Boolean assignment space, with overlaps allowed. If an acyclic context-typed union of terminal XOR refutations has $q$ distinct paid XOR-inference vertices and the linear parts of every permitted assumption have global rank $r$, then $E$ has a binary-XOR refutation with at most $q+r$ paid inferences.

Predeclared falsifiers:

1. a complete affine terminal cover can exclude every assignment without its discharged rows spanning constant one;
2. a reconvergent inference can have two incompatible assumption tags while remaining one immutable proof vertex;
3. overlapping terminal contexts force a shared inference to be charged twice;
4. omitting an AND-required region can nevertheless prove common-source UNSAT.

Falsifiers 1, 3 and 4 fail under the theorem's explicit conditions. Falsifier 2 narrows legal sharing: one vertex has one ID, one parent tuple, one row and one immutable global assumption tag. Equal rows with different tags or parents are not the same proof node. No case-split, weakening or discharge rule is asserted for historical R_mix341.

### Required state, peer and source readback

Complete live trackers read: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `9809e0302c00c009cd50db3d6e2ab300de192751`. Exact affected IDs are `[P2-L5-408]` and supporting gap `[P2-C1]`; `[P2-L5-407]` is the immediate predecessor. Governing handoff blob `c3889a3e514ddbd747150dcb68607013a3b2d154`, `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, current issue #3, actual Grok `GROKPROOF/2026-11-07_1119_PROGRESS.md` blob `d87fcb3a12ed115c277f7ffda87ecca0f4072630`, and Claude world-ledger README blob `de75a371ce3143a4495e6892df7fb04794a6b708` were read.

Newest Route B peer evidence read directly:

- `[P2-L1-471]`, report `research/agents/lspv-1/2026-11-07_0306_LSPV1_BACKWARD_RESOLUTION_SHORTCUT471.md` blob `d578c7c0ca653491c6ce64656ca975405d83c7ba`, gives a legal backward-Resolution upper bound $k+\tau+1$ for the stated Horn set-cover source.
- `[P2-L3-471]`, report `research/agents/lspv-3/2026-11-07_0324_LSPV3_FULL_BINARY_HORN_MINIMUM471.md` blob `defc7c61a2ad41bcaa439b66a737856919f0bb027`, proves exact whole-DAG minimum $k+\tau+1$ only for a sound source-transparent unit-paid at-most-binary calculus with no free hidden multi-source payload. Its compact replay and raw ledger were also read. The family is easy Horn CNF, not hard strict 3-SAT. The report explicitly leaves historical accepted-byte R_mix341 replay open; this run does not claim to have supplied it.

Primary literature reviewed: Haken's ordinary shared-DAG Resolution lower bound for unary PHP; Urquhart's ordinary Resolution lower bounds for expander Tseitin formulas; Itsykson--Sokolov's tree-like Res($\oplus$)/parity-decision-tree correspondence; and Braun's recent unrestricted DAG-like Res($\oplus$) bit-PHP preprint. Each theorem remains qualified by its stated proof system. Cook-style Extended Resolution and native affine summation are mandatory upper-bound controls.

Required repositories were change-aware reviewed at their pinned files: `konard/p-vs-np` `README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `REVIEW_ADDENDUM.md` blob `6a7cc2f8962d3fcfc1778b1d3d8f5dc8d56d70`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; plus `openai/math`, `anthropics/formal-math`, and `kbr-/math-research` README blobs `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`, `1df53bfc14a022088d1b5757698f692bf79390b4`, and `7d393b08f361d46a5c80d167aa2f3e36f5739018`. Current fetches for CakeLPR, short-proof and CNFgen returned connector errors; their unchanged pinned files were reviewed in run 407, and no fresh review is claimed. Google-branded search was unavailable; ordinary public web search was used.

## Established-family / theorem / encoding / shortcut / transfer ledger

| Family | Exact encoding and size parameter | Established theorem and model | Strongest known shortcut control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin, strict 3-CNF | For simple cubic $G=(V,E)$, variable $x_e$ per edge. At $v$ with incident $e_1,e_2,e_3$ and charge $\chi_v$, include, for each $a\in\{0,1\}^3$ with $a_1\oplus a_2\oplus a_3\ne\chi_v$, the clause $\bigvee_i\ell_{e_i,a_i}$, where $\ell_{e,0}=x_e$ and $\ell_{e,1}=\neg x_e$. For $h=|V|$: $3h/2$ variables, exactly $4h$ proper 3-clauses, indexed encoding $N=\Theta(h\log h)$. Odd total charge certifies UNSAT. | Urquhart 1987 gives $2^{\Omega(h)}$ ordinary DAG Resolution size on appropriate expanders. Permitted rule: ordinary syntactic Resolution. This is certified proof-size hardness only in that system. | The four clauses at each vertex encode one parity equation; summing all $h$ equations yields $0=1$ in $O(h)$ affine steps. This defeats transfer to any calculus with an authenticated native GF(2) shortcut. | Historical R_mix341 byte grammar, exact weights and original-source authentication remain `[P2-D1]`/`[P2-C3]` OPEN. No all-mixed lower bound. |
| Bit PHP $\mathrm{BPHP}_{n+1}^{n}$, $n=2^\ell$ | Variables $x_{p,j}$ encode address bits. For $p<q$ and $a\in\{0,1\}^\ell$, include the width-$2\ell$ clause saying $p,q$ are not both at $a$. UNSAT by collision. This is not strict 3-CNF. | Braun 2026 preprint: exponential unrestricted DAG-like Res($\oplus$) lower bound in its stated system for sufficiently large $\ell$. | Extension/definition and circuit encodings must be tested; an equisatisfiable Tseitin conversion alone says nothing about proof-size preservation in the target calculus. | No cited lower-bound-preserving strict-3-CNF reduction into full R_mix341. No all-algorithm inference. |
| Unary PHP | Variables $x_{p,h}$; pigeon clauses $\bigvee_hx_{p,h}$ and collision clauses $\neg x_{p,h}\vee\neg x_{q,h}$. Long pigeon clauses, hence not strict 3-CNF as stated. | Haken 1985: exponential ordinary Resolution length. | Extended Resolution has polynomial proofs; this is a mandatory failure mode for transferring Haken to a stronger mixed system. | No authenticated lower-bound-preserving 3-CNF/full-mixed transfer located. |
| Horn set-cover source of `[P2-L1-471]`/`[P2-L3-471]` | $H=(a)\wedge_j(\neg a\vee s_j)\wedge_{j,i\in S_j}(\neg s_j\vee g_i)\wedge(\neg g_1\vee\cdots\vee\neg g_k)$. | Exact minimum $k+\tau+1$ only under the source-transparent at-most-binary hypotheses. | Backward Resolution realizes the bound. The source is Horn and polynomially refutable. | It is a validation control, not established hard 3-SAT, not superpolynomial $\overline W_R$, and not B3. Historical accepted-byte arity/weights remain open. |

Certified UNSAT, certified proof-size hardness and empirical solver difficulty remain distinct: the parity sum or collision argument certifies UNSAT; the cited theorem certifies proof size only in its named system; no runtime measurement is used as a hardness theorem.

## The affine-cover theorem

Represent an affine equation over $\mathbb F_2$ as an augmented row $(a,b)$ meaning $a\cdot x+b=0$. Let $E$ be common authenticated rows. Fix a finite global list of affine assumptions $\gamma_j=(a_j,b_j)$ whose linear parts span dimension $r$.

Let $D$ be an acyclic union proof DAG. Every vertex has a unique ID, immutable ordered parent tuple, affine row $R_v$, and immutable tag vector $\tau_v$ over the global assumptions. Source vertices in $E$ have tag zero, an assumption axiom $\gamma_j$ has the $j$th unit tag, and a paid binary-XOR inference XORs both parent rows and tags. Let $q$ be the number of distinct paid inference vertices in the union, counted once.

Each selected terminal $t$ has row $(0,1)$ and a consistent context $C_t$ that contains every assumption used by $\tau_t$. The selected contexts must cover all Boolean assignments. Contexts may overlap and need not form a tree. Alternative successful covers are OR choices; once one is selected, coverage is the AND obligation.

**Theorem 408.1 (PROVED/RESTRICTED).** Under those hypotheses,

$$
W_{\mathrm{GF}(2)}(E)\le q+r.
$$

**Proof.** Transform each union vertex once:

$$
D_v=R_v+\sum_j\tau_{v,j}\gamma_j.
$$

For an assumption axiom this is zero; for an $E$ source it is unchanged; and the transformation commutes with binary XOR. Thus each paid union inference is reused at most once and every $D_v$ is derived from $E$. At terminal $t$,

$$
U_t=D_t=(0,1)+\sum_j\tau_{t,j}\gamma_j.
$$

Every assignment in $C_t$ satisfies all tagged assumptions, hence $U_t(x)=1$. Because the selected contexts cover all assignments, no assignment zeros every $U_t$. The affine system $U_t=0$ is inconsistent. Gaussian elimination over $\mathbb F_2$ therefore expresses $(0,1)$ as an XOR of the $U_t$ rows.

All linear parts of $U_t$ lie in the assumption-linear span, of dimension $r$. The augmented rows lie in dimension at most $r+1$, so at most $r+1$ of them span $(0,1)$ and at most $r$ final binary joins derive false. The tag transformation charges at most the $q$ existing distinct union inferences; immutable shared vertices are transformed once. Total paid work is at most $q+r$. $\square$

This strictly generalizes `[P2-L5-407]` from complete adaptive trees to arbitrary finite affine covers, including overlaps and legal reconvergence. It is an upper-bound control, not a proof-search algorithm, a historical R_mix341 rule, B3, or a lower bound.

### Minimal AND-scope countercontrol

Take satisfiable common source $E=\{x+1=0\}$, whose model is $x=1$. Under the sole context $x=0$, adding assumption $x=0$ derives false. Discharge returns $x+1$, which is true only on the covered cell and does not refute $E$ at $x=1$. The omitted context is therefore fatal. One successful OR derivation is not a valid common-source proof unless the selected terminal contexts satisfy the AND cover obligation.

## Exact computation, sharing and resource audit

Artifacts:

- producer `experiments/review/lspv5_408_affine_cover_retraction.py`, SHA-256 `cbd9e758294669ddf46aeaaaf88c0485c2ee3b61565f9955b582d6e7df62669c`;
- independent Node replay `experiments/review/verify_lspv5_408_affine_cover_retraction.mjs`, SHA-256 `3005a97f1d33d347e8a081db6863492bf2a73fb07100f008800f83a184435593`;
- raw `results/raw/review/2026-11-07_0356_LSPV5_AFFINE_COVER408.json`, SHA-256 `f14a90fd466af4e5f6d37853b49d73df859507ab914da06089e66cca8a455d73`.

The producer exhaustively enumerated all subsets of nontrivial affine hyperplanes for ranks 1, 2 and 3: 16,452 candidate subsets, 15,563 complete covers, including 15,552 overlapping covers. Every complete cover yielded an explicit contradictory subset of at most $r+1$ discharged rows; the maximum witnessed sizes were 2, 3 and 4. The independent Node implementation repeated all enumerations and reported 46,812 checks PASS.

The typed overlap fixture uses contexts $x=0$, $y=0$, and $x=1\wedge y=1$. Their cells cover all four assignments and overlap at $(0,0)$. It contains one genuinely shared inference with one immutable tag and parent tuple. The context-union has $q=12$, global rank $r=2$, theorem bound $14$, while the common source also has a direct two-step affine refutation; the shorter derivation is a legal upper-bound control and is not excluded. Negative controls rejected an omitted region, a wrong discharged-row value, cross-branch tag mutation, duplicate ID, cycle/forward reference, forged rank, missing context assumption and OR-without-AND coverage.

Logical work, span and realizable resources are separate. The theorem bounds distinct-node work by $q+r$. A balanced final XOR of at most $r+1$ rows has ideal additional span $\lceil\log_2(r+1)\rceil$, but retention, references and context normalization consume space; recomputation can trade space for extra work. The host run charged construction, exhaustive search, parsing, verification, serialization and output, with elapsed time and peak RSS stored in the raw ledger. These host resources are not FLMV same-machine bounds. Historical inference bits, accepted trace bytes, exact reference/application costs and checker execution remain unmeasured because the historical checker grammar is not authenticated.

## Tracker effect and precise remaining gap

Material tracker change: add `[P2-L5-408]` and a `[P2-C1]` evidence line. `proof1.txt` was reviewed and has no material change. The result closes only the tree-shape restriction inside the abstract binary-GF(2) control. It does not cover nonlinear definitions, AND3, Resolution, mixed LOCAL-CONVERT, or semantic equality without provenance.

Still OPEN: `[P2-C1]` for the full fixed mixed calculus, `[P2-C3]`, `[P2-D1]`, `[P2-B1]`, `[P2-B2]`, `[P2-B5]`, a genuinely superpolynomial $\overline W_R$ across every legal R_mix341 rule, a noncircular same-calculus B3, and historical accepted-byte replay of `[P2-L1-471]`/`[P2-L3-471]`. P versus NP remains OPEN.

The next decisive test is rule-by-rule historical authentication: determine whether exact R_mix341 bytes natively realize the tag-preserving XOR transformation and final affine joins at the historical weights, or exhibit a legal accepted trace whose provenance or source identity defeats the proposed normalization.
