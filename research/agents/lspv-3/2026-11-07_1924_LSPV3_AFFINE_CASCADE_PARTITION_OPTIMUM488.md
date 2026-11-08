# LSPV-3/488: sharp adaptive affine-flat partition lower bound for the nested AND cascade

**2026-11-07 19:24 PST | Route B, LSPV-3 | PROVED/RESTRICTED (symbolic), COMPUTATIONAL (finite replay). Historical R_mix341, P2-D1/P2-C3/P2-B1/P2-B2 and P versus NP remain OPEN.**

**Relevant existing nodes:** [P2-F13], [P2-L3-485], [P2-L3-487], [P2-C3], [P2-D1], [P2-B1], [P2-B2]. **New evidence:** [P2-L3-488]. Cross-route [P1-01] and [P2-A2] unchanged.

## IDEA and four falsifiers registered before search

Hypothesis: LSPV-3/487's (g+1) first-zero affine **subcube** partition is *optimal even among arbitrary affine-subspace partitions* of the original input cube, provided every named intermediate output must be affine on every cell. The full-rank static (2^g) anchor coset partition is not minimal; this is a precise lower bound for a **partitioning relaxation**, not a claim about minimum refutation DAG work.

Falsifiers: (1) a two-cell affine-flat partition of the 3-input AND cascade linearizing both named wires; (2) two disjoint affine subspaces of (mathbb F_2^n) which cannot be strictly separated by an affine linear functional; (3) an affine restriction of an (n)-variable AND that has exactly one 1 on a flat of dimension at least two; (4) first-zero guards failing to partition or failing to linearize *every* intermediate cascade output.

## SEARCH and continuity (source-authenticated scope)

Read complete root `proof1.txt` (startup blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (startup blob `70b3f85c70cdfd553cda733f44c5c201d20b5903`), issue #3 and current role comments; historical five-role refocus `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (blob `c3889a3e514ddbd747150dcb68607013a3b2d154`), `AGENTS.md` (blob `19656af102604d5f0a721d548cf2e4e72a063561`), `CODEX.md` (blob `754999f50de93cdb693ed37bc8110d31e9e698ef`), research skill (blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`), original historical LSPV-2/341 `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`), LSPV-3/487 (blob `cb3542017daf76e6c74da1c53b1efb7ecd7c2f0e`), LSPV-1/493 (blob `14391fc9604c9389bd30cdcd747393e0fd2d1fd2`), and LSPV-5/423 representation referee. Actual independent `GROKPROOF/2026-11-08_0320_PROGRESS.md` (blob `72edb3140d8ed798d0905a827f85d3428728e396`) and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`) were read. Neither authenticates a full historical mixed byte parser.

Required external change-aware reads: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` (scoped Lean results, no P-versus-NP theorem); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (restricted proof/optimization ledger); `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (external XOR/certificate grammar); `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab` (Resolution-only minimum); `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` (verified checker, not proof producer); `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`, `anthropics/formal-math/README.md` blob `1df53bfc14a022088d1b5757698f692bf79390b4` (independent research, not historical grammar). Exact repository default-branch paths checked; these external sources give no accepted-byte authentication for /341.

Indexed literature queries: affine subspace partitions of the Boolean cube; subcube-partition complexity of AND; Pang, *A Degree--Size Relation for Resolution over Polynomials* (arXiv:2610.00837, posted 2026-09-30, preprint); Filmus et al., *Irreducible Subcube Partitions*, Electronic J. Combin. 30(3), P3.29 (2023), DOI 10.37236/11862 (includes partitions into affine subspaces); Haken's Resolution PHP and Cook ER shortcuts; Urquhart expander Tseitin. The affine-separator lemma is elementary and may be prior art; **no originality claim**. Google-branded search was unavailable; indexed web search was used. No PDF was analyzed, no native /341 checker or Lean kernel executed.

## ITERATE: sharp affine-flat partition theorem (PROVED/RESTRICTED)

Let (g\ge1), (n=g+1), and (x=(z,a_1,\ldots,a_g)\in\mathbb F_2^n). Define the conservative binary AND cascade

$$
w_0=z,\qquad w_i=a_iw_{i-1}=z\prod_{j=1}^i a_j,\quad 1\le i\le g.
$$

An **admissible affine partition** is a finite partition (\mathbb F_2^n=A_1\sqcup\cdots\sqcup A_L) into nonempty *affine subspaces*, not arbitrary semantic agreement regions, such that on every (A_j) **every** named output (w_1,\ldots,w_g) agrees with an affine function of the ORIGINAL (n) inputs. No assumptions about syntactic legal branch rules in historical R_mix341 are made.

**Lemma 488.1, affine-flat partition codimension bound (PROVED/EXACT elementary):** In any partition of (\mathbb F_2^n) into (L) nonempty affine subspaces, every cell (A) satisfies

$$
\operatorname{codim} A\le L-1.
$$

*Proof.* Write (A=a+U). For each other cell (B=b+V), disjointness implies (b-a\notin U+V). Hence there is a linear functional (h_B) annihilating (U+V) and satisfying (h_B(b-a)=1). Define the affine separator (\ell_B(x)=h_B(x-a)). It vanishes on all (A) and equals one on all (B). Since the other cells cover the complement of (A),

$$
A=\bigcap_{B\ne A}\{x:\ell_B(x)=0\}.
$$

An intersection of (L-1) affine hyperplanes has codimension at most (L-1). QED.

**Lemma 488.2, singleton-one affine restriction:** Let (f(x)=\prod_{j=1}^{n}x_j) over Boolean inputs, the conjunction with exactly one 1. On any affine flat (A) containing the all-ones point, if (f|_A) is affine, then (\dim A\le1).

*Proof.* On any (d\)-dimensional affine flat, an affine Boolean function has either 0, (2^{d-1}), or (2^d) ones. Since (f) has *exactly one* 1 globally and that point lies in (A), for (d\ge2) no such affine restriction is possible. QED.

**Theorem 488.3, EXACT optimum in the declared affine-flat partition model:**

$$
\boxed{\min L=g+1.}
$$

*Lower bound.* The final named gate (w_g=z\prod_{j=1}^g a_j) is the (n)-variable AND function, with unique all-ones input. Let (A_\star) be its partition cell. By Lemma 488.2, (\dim A_\star\le1), hence (\operatorname{codim} A_\star\ge n-1=g). Lemma 488.1 then gives (L\ge g+1).

*Upper bound.* Use LSPV-3/487's (g+1) guards

$$
\Gamma_j=\{a_1=1,\ldots,a_{j-1}=1,a_j=0\},\quad 1\le j\le g,
\qquad \Gamma_{g+1}=\{a_1=\cdots=a_g=1\}.
$$

They are disjoint, exhaustive, nonempty affine subcubes. On (\Gamma_j), (w_i=z) for (i<j), and (w_i=0) for (i\ge j); on the final guard, all (w_i=z). Every named gate is therefore affine. (L\le g+1). QED.

This sharpens the prior /487 **upper bound** into an exact **partition count**, and extends its optimality guarantee from subcube guards to *all affine flats*. It is **NOT** an information-theoretic, mixed-proof-DAG or algorithmic lower bound. Semantic agreement covers with nonlinear membership predicates (LSPV-1/493) are a different relaxation; full fixed R_mix341 may avoid any affine partition, use RES/ER/GF(2) shortcuts, share lemmas and/or choose another derivation. In particular, (L=g+1) need not equal (W_R(F)).

## Independent finite validation and falsifier outcomes

Independent Python producer `lspv3_488_affine_partition_independent.py` (offline archive) enumerated all affine flats as spans/cosets, checked affine parallelogram identities on EVERY named wire, and solved exact set-partition by depth-limited search for (n=2,3,4,5). Number of flats: **11, 51, 307, 2,451**; admissible flats: **10, 39, 184, 1,089**; exact optima **2, 3, 4, 5**. It examined 13,188 cell/assignment incidences; host wall 10.5744 s; Python tracemalloc allocation peak 2,431,738 bytes (NOT all-process peak/RSS). Odd-charge original strict3 (K_4) Tseitin control: 16 source clauses, 0 models; even-charge control: 16 clauses, 8 models.

Independently written JavaScript **published bytes** `experiments/arc/lspv3_488_affine_partition_independent.cjs` (blob `29b888d78d7d4121d3656dc1dbb06310514854eb`) enumerated affine flats by repeated parity-hyperplane intersections, not the Python span enumeration. V8 replay passed **102 assertions** and four negative-input/invalid-clause controls, independently reproducing flat counts, admissible counts, affine guards and 0/8 source models. The very first V8 replay found a genuine JavaScript 32-bit `1<<32` full-cube mask bug at (n=5); it was corrected, then reread and the **exact revised published bytes** replayed successfully. This is an implementation falsifier repaired, not hidden. Full results: `results/raw/arc/2026-11-07_1924_LSPV3_488_AFFINE_PARTITION_OPTIMUM.json` (blob `33af1f29b21d5c79be064e34fc66a6834eda0423`).

All four mathematical falsifiers failed in the DECLARED model; the JS overflow falsifier succeeded against the first implementation and was fixed. No historical native cert acceptance, original-source mixed inference proof, polynomial normalizer, branch discharge or source-retracting B3 reflection was established. The symbolic proof is independent of exhaustive searches.

## Established hard-family and shortcut ledger

- Pang (2026 preprint) uses random proper strict 3-CNF (F(n,3,8n)) sampled with replacement from the (8\binom n3) possible proper 3-clauses, at (m=8n) and variable count (n). It reports exponential lower bounds in the specified syntactic (\mathrm{Res}(\oplus))/constant-degree Res(PC) proof models (with explicit PC degree hypotheses); verify theorem and grammar before invoking it. Ordinary bit-index encoding is (O(n\log n)) for the sampled clauses; alternate formal encoders may have (O(n^2)) bytes/bits as audited by LSPV-5/423. Neither encoding alone proves mixed lower-bound preservation.
- Haken's PHP: exponential ordinary DAG Resolution, but Cook's extended Resolution gives polynomial proofs; no safe lower-bound transfer to historical paid DEF calculus without full typed simulation.
- Odd-charge cubic expander Tseitin: exponential ordinary Resolution on appropriate expanders, but LSPV-2/341 proves (4h-1) paid work in its *declared* mixed calculus via local AND3 extraction and GF(2). This is a mandatory inexpensive mixed upper-bound control, not a general hard family.
- This run's affine-partition cascade is a surgical validation of the /487 shortcut, **not** a replacement for any established hard 3-SAT family.

## Resource / ownership / next implication

This run constructs a symbolic partition with (g+1) cells. The finite exhaustive optimizer is a host experiment, not a physical efficient solver. Charge source/index reads, gate construction, truth-table testing, all failed partition candidates, duplicate-flat caches, memory allocations, serialization, GitHub reads/writes, and replay in any implemented cost analysis. Distinguish (g+1) semantic cells from the prior (3g-2) **exhibited** paid distinct nodes under a different facet-addressable DEF+RES grammar. No weighted critical-path, realized peak native-machine space, or proof construction time bound follows. Route A (s'\le\max(\rho,\eta,\lambda,\lambda s)) remains conditional and unchanged.

**Next role LSPV-3 target:** A single accepted historical byte-certified RES-created clause -> DEF facet -> LOCAL-CONVERT -> AND3 input with source provenance, globally fresh IDs, original-variable support and legal contexts. LSPV-1 should not replace syntactic guarded proof translations with this partition count. LSPV-5 should test non-affine membership and alternative mixed proofs. No edits to tasks, schedules, role ownership, historical rule grammar/weights, or protected root main.tex. Root main.tex complete bytes unavailable, so no safe edit.

**Publication status:** role report, published JS, raw, handoff to be independently read back; shared tracker change [P2-L3-488] only if final optimistic SHA merge succeeds. The historical four principal dependencies [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. P versus NP OPEN.
