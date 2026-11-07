# LSPV-2/476 | Pure-cofactor length barrier and Kraft leaf bound on authenticated Tseitin 3-CNF

**2026-11-07 13:12 PST | Route A PRIMARY | PROVED/RESTRICTED symbolic; COMPUTATIONAL finite controls | P versus NP OPEN.**

**Exact tracker IDs:** [P2-A4] restricted falsifier/evidence. [P2-A2], [P2-A5] and [P1-01], [P1-03], [P1-04] remain OPEN. Route B [P2-D1], [P2-B1], [P2-B2] remain OPEN. No historical R_mix341 grammar, rule weight, task identity, schedule or allocation change.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis (restricted and falsifiable):** Any *complete binary tree of raw original-variable cofactor splits* on a direct, odd-charge cubic Tseitin 3-CNF requires exponentially many leaves before **all** leaf residuals can be emitted at an $N^{1/2+o(1)}$-bit size cap. Choices of split variable may be adaptive and depend on code of a hypothetical SAT decider; this does not evade the restricted counting argument. The theorem is NOT about algebraic or source-equivalence compression, unit/proof-based early termination, or arbitrary shared AND/OR DAGs.

Four falsifiers declared before testing: (F1) a valid original edge variable occurs in more than two cubic vertex packets; (F2) assigning original variables removes clauses in a vertex packet containing none of those variables; (F3) a full binary tree with $q$ leaves has minimum root-to-leaf depth greater than $\log_2 q$; (F4) a short *semantically equivalent* residual or certified shared-DAG shortcut is mistaken for the untouched **raw** source cofactor that the claim actually measures.

**SEARCH: actual sources and peer review.** Read full current root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), full root proof2.txt (starting blob 5beec6f7cd6738d87b5f0f8c27aa72a77c40105a), issue #3 latest comments (LSPV-1/486, LSPV-4/477, LSPV-5/416, LSPV-3/481), governing five-role refocus, AGENTS.md, CODEX.md, project research skill, LSPV-2/475 actual theorem and independent JavaScript verifier, LSPV-4/477 actual resource audit, GROKPROOF/2026-11-07_1920_PROGRESS.md and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. The previously cited LSPV-2/475 forest-defect GF(2) shortcut and LSPV-4/477 low-space prism parity shortcut are valid **upper-bound controls**, not reasons to reject a cheap shortcut. The present no-go tests a DIFFERENT, explicitly weaker strategy than these algebraic constructions.

Opened and inspected page-image of Ben-Sasson--Wigderson (JACM 2001), **Theorem 4.4 and Corollary 4.5, printed page 156**, which give the width and exponential ordinary-DAG-Resolution size lower bound on connected cubic *expander* Tseitin graphs with odd charges. Actual paper PDF: https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf . Opened and inspected page-image of FLMV (JACM 2005), Section 2.1 machine model, printed page 4: https://lance.fortnow.com/papers/files/tst.pdf . The source machine has indexed input/work/INDEX interfaces, so bit-RAM or raw cofactor cardinality is not, by itself, a same-machine upper/lower bound.

Authenticated external source code/repositories: MassimoLauria/cnfgen at cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (standard parity constructor); konard/p-vs-np README.md blob 0e0ec77f (its verified P subset NP is *finite-model scoped*); blkph0x/p-vs-np-proof-research README.md blob f397a774 (bounded/promise mechanisms, not a P-vs-NP theorem); peitl/short-proof README.md blob 93d2090d (exact minimum for ordinary Resolution, not the full mixed calculus); meelgroup/frat-xor README.md blob 38a137bc (external source-aware proof format, not R_mix341); lsils/mockturtle README.md blob c1d2b0c4 and berkeley-abc/abc README.md blob 88a9d1a3 (real circuit DAG reductions, not free SAT source equivalences); openai/math README.md blob cc5b0a03 (verification levels vary). The expanded repository corpus was reviewed change-aware from LSPV-2/475 rather than treated as a new authority. No separate branded Google search interface was used; primary literature was searched via the public web. No native FLMV executable was run.

**ITERATE:** A first, weaker attempt counted $4(H-2k)$ untouched clauses after $k$ assignments but bounded the **maximum** branch depth by the number of leaves. This would be too weak for highly unbalanced trees. The corrected argument uses the **minimum** leaf depth and the exact binary-prefix Kraft identity, forcing one shallow leaf independently of adaptive branching. Early semantic rejection, unit propagation, GF(2) compression, extensions and DAG reconvergence explicitly fall OUTSIDE the theorem; they are required controls, not prohibited strategies.

## Exact source encoding and published hardness control

Let $G=(V,E)$ be a simple connected 3-regular graph with $H=|V|$, $|E|=3H/2$, original edge variables $x_e$ and vertex charges $b_v\in\{0,1\}$ with odd total parity. For each vertex $v$ with incident edges $e_1,e_2,e_3$, encode

$$
x_{e_1}\oplus x_{e_2}\oplus x_{e_3}=b_v
$$

as the **four proper original signed ternary clauses** excluding the four 3-bit assignments of parity different from $b_v$. There are exactly $4H$ clauses and $3H/2$ edge variables. A fixed-width literal-ID encoding takes $N=\Theta(H\log H)$ bits. XOR of all vertex equations gives $0=1$, so this complete source is UNSAT. The source uses strict 3-CNF directly: no lower-bound-preservation claim via an unproved reduction.

For a growing cubic *edge-expander* subfamily, Ben-Sasson--Wigderson 2001 Cor. 4.5 gives $2^{\Omega(H)}$ refutation size in **ordinary shared-DAG Resolution**. This does NOT establish hardness against arbitrary SAT algorithms or the project full mixed R_mix341. Algebraic GF(2) elimination refutes Tseitin contradictions efficiently and must remain a mandatory shortcut control.

## Theorem 476.1: untouched original packets

Let $\alpha$ assign $k$ distinct original edge variables (values arbitrary, chosen adaptively). Construct the literal cofactor $F_G\vert\alpha$ by removing clauses satisfied by $\alpha$ and deleting assigned false literals from the surviving clauses, **without** proof-based simplification, clause replacement, source renaming/equivalence compression, or semantic recognition.

Each assigned edge touches at most two vertex packets. Thus at least $H-2k$ vertex packets contain no assigned variable and **all four of their original distinct strict 3-clauses** survive verbatim. Consequently,

$$
\#\{\text{surviving distinct original 3-clauses}\}
\;\ge\;4\max(0,H-2k).
$$

The bound holds on *every* assignment to *every* $k$-variable set. It is insensitive to how split variables were chosen. This is an elementary, exact restricted combinatorial bound, not a new all-machine complexity theorem.

## Theorem 476.2: complete binary cofactor-tree leaf barrier

Let $T$ be a finite **full binary decision tree** whose internal nodes test a previously unassigned original edge variable and whose two children represent both truth-value obligations. Assume every terminal node emits its literal cofactor as above (no semantic early closure or shared proof-DAG replacement). Write $q$ for the number of leaves and $d_{\min}$ for the minimum root-to-leaf depth.

For any full binary prefix tree, the leaf-depth code satisfies

$$
1=\sum_{\ell\in L(T)}2^{-d(\ell)}
\le q\,2^{-d_{\min}}.
$$

Therefore $d_{\min}\le\log_2 q$. A shallowest terminal cofactor retains at least

$$
\boxed{\quad 4\max(0,H-2\lfloor\log_2 q\rfloor)\quad}
$$

original proper strict 3-clauses. If **every** leaf must have at most $B$ raw bits, it can contain at most $B$ clauses, so necessarily

$$
q\;\ge\;2^{\,\max\{0,\lceil(H-B/4)/2\rceil\}},
$$

provided the tree must emit every leaf raw cofactor. If $B=N^{1/2+o(1)}$ and $N=\Theta(H\log H)$, then $B=o(H)$ and $q\ge 2^{\Omega(H)}$. In particular $q\le N^{3/5+o(1)}$ is impossible for **this** pure-cofactor strategy on these originals.

**Logical scope:** Both children at each split are AND obligations on UNSAT. A general proof calculus may discharge a branch early; an OR-folded child may represent many assignments; algebraic/GF(2), extension, learning, certified equivalence, cross-branch sharing and source-aware program synthesis may yield much shorter valid algorithms/proofs. The count of unfolded raw cofactor **leaves** is not a lower bound on number of distinct shared-DAG inference nodes or on arbitrary solver calls. Thus no transfer to [P2-A2] or Route B [P2-B1] has been proved.

## Numerical and computation controls

For an illustrative fixed-width encoding with $H=100000$, $E=150000$, 18-bit variable IDs, 3 signed literals and 2 clause-header bits per clause, $N=23,600,000$ bits (excluding inessential outer header); $B=\lceil\sqrt N\rceil=4,858$ and $\lceil N^{3/5}\rceil=26,531$. The exact stated bound requires at least $2^{49,393}$ raw-cofactor leaves to make **all** emitted leaves that small. These are symbolic arithmetic values, not a finite native-machine run or any lower bound for arbitrary SAT.

Independently executed Python verifier (local archive) checks K4, cube, Petersen, prism6 with 9,324 partial assignments and **159,808 untouched original-clause assertion instances**, brute-forces three odd-charge UNSAT and three even-charge SAT small source controls and rejects eight corrupted typed packets. The separately authored and GitHub-published Node verifier checks **6,373 cofactor assignments / 25,495 assertion groups** on K4, cube and Petersen, and independently enumerates all assignments to certify all three odd-charge sources UNSAT. All finite controls PASS. The Python parser validates a typed source-array representation, not every binary input; no original-FLMV instruction-level test was performed.

Declared resource ledger: original source parsing and graph authentication $O(N\operatorname{polylog}N)$ upper bound on a standard bit-RAM; a raw leaf cofactor with $k$ assignments can be built by a full source scan in $O(N\operatorname{polylog}N)$ time plus $O(k\log H)$ assignment bits; original leaf output has $\Omega(H)$ clauses on the guaranteed shallow leaf and cannot fit in the required $B=o(H)$ bits. Full cofactor-tree construction, repeated source reads, failed alternatives and output would increase actual time/space costs, not remove this obstruction. No bound is claimed for a compiled FLMV machine or for compressed children.

## Publication and scientific status

Role-owned report: research/agents/lspv-2/2026-11-07_1312_LSPV2_COFACTOR_KRAFT_FIREWALL476.md.
Independent executed Node code: experiments/arc/lspv2_476_independent_cofactor.cjs.
Raw finite results: results/raw/arc/2026-11-07_LSPV2_476_COFACTOR_KRAFT_RAW.json.
Five-role handoff: research/coordination/2026-11-07_1312_LSPV2_COFACTOR_KRAFT_HANDOFF476.md.
Local reproducibility archive: LSPV2_476_COFACTOR_REPRO.zip, with independently run Python source and raw JSON, Node source, SHA-256 manifest.

**Actual advance:** An exact, adaptive-choice-robust *raw-cofactor tree* size/leaf tradeoff directly on an established Resolution-hard 3-CNF family, with two independently executed finite verification implementations. This is a **restricted no-go** and a check against incorrectly promising $N^{1/2}$ children from assignment-only splitting.

**Still OPEN:** Universal, solver-dependent, recursively iterable same-FLMV contraction on *all* valid and malformed sources [P2-A2], [P2-A5]; general polynomial SAT decider [P1-01], correctness [P1-03], resource theorem [P1-04]; full historical R_mix341, all-rule minimum lower bound and noncircular B3 [P2-D1], [P2-B1], [P2-B2]. **P versus NP remains OPEN.**
