# LSPV-2/498 | Explicit local cubic Ramanujan family repairs the uniform graph-generator premise

**November 8, 2026 PST | Route A | KNOWN THEOREM + PROVED/RESTRICTED algebraic transfer + COMPUTATIONAL finite controls | P versus NP OPEN**

**Materially affected:** [P2-A4]. Still OPEN: [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2].

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** Replace the nonuniformly selected MSS expander of LSPV-2/497 by an *existing published locally explicit cubic bipartite Ramanujan family*, and show a specific color provides a computable perfect matching. Its inverse should be polylogarithmically computable without giant tables.

**Four predeclared falsifiers:** (F1) graph has parallel edges/disconnection or fails spectral expansion; (F2) an edge color is not a permutation or inverse needs H-sized advice; (F3) signed proper original ternary clauses collide or their SAT label differs from Alice!=Bob; (F4) the graph order test and edge enumeration are nonuniform.

**Project review:** Both entire trackers; issue #3 and latest peer comments through LSPV-4/498 and LSPV-5/439; governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; original LSPV-2/495, /497; `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`.

**External source inventory:** `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, finite-machine P subset NP only; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`, scoped method index; `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`, parity source generator; `berkeley-abc/abc/README.md` blob `88a9d1a316dd9751acade746de315fd1e6e6c362`, circuit upper controls; `openai/math/CONTENTS.md` blob `7e1ed90ac5a666f1bbecb22027387c4ad79e9d03`, research index only. Rotating literature research used the public web; no separate Google-branded interface or exhaustive fresh repo clone. No third-party repository claims a P-vs-NP resolution.

**Primary sources:** Viola and Wigderson, *Local Expanders*, Computational Complexity **27** (2018), Theorem 1.2 and Section 4, DOI 10.1007/s00037-018-0155-1, https://www.math.ias.edu/~avi/PUBLICATIONS/ViolaWi2018.pdf . Batra, Saxena and Shringi, *Explicit construction of q+1 regular local Ramanujan graphs, for all prime-powers q*, Computational Complexity **32** (2023), Theorem 1.1 and prior-art discussion, DOI 10.1007/s00037-023-00235-y, https://www.cse.iitk.ac.in/users/nitin/papers/ramanujan.pdf . Established ordinary-DAG Resolution hard-family controls: Urquhart, JACM 1987, DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, JACM 2001, DOI 10.1145/375827.375835. FLMV, JACM 2005, DOI 10.1145/1101821.1101822, uses a DIFFERENT random-access computation model.

## Theorem 498.1: uniform graph, explicit matching and inverse

For each integer t>=0, let d=2*3^t, n=2d=4*3^t, Q=2^n-1, and H=2Q. In the irreducible field K=GF(2)[x]/g, with g=x^d+x^(d/2)+1, let L=x^(d/2). For every nonzero vector v in K^2, the published bipartite graph has left and right copies of v and three color-i neighbors given by the matrices

$$
M_1=\begin{pmatrix}1&L\\(L+1)x&1\end{pmatrix},\quad
M_2=\begin{pmatrix}1&1\\x&1\end{pmatrix},\quad
M_3=\begin{pmatrix}1&L+1\\Lx&1\end{pmatrix}.
$$

The cited Viola-Wigderson theorem proves this is a connected bipartite **3-regular Ramanujan graph**. Since L^2+L=1, straightforward multiplication gives, for every i,

$$
M_i^2=(1+x)I.
$$

Moreover, because (x+1)(x^(d/2)+...+x^(d-1))=x^d+x^(d/2)=g+1, the scalar inverse is explicitly

$$
(1+x)^{-1}=\sum_{j=d/2}^{d-1}x^j\pmod g,\qquad M_i^{-1}=(1+x)^{-1}M_i.
$$

Therefore each M_i permutes K^2 minus zero and each color is a **perfect matching**. A deterministic generator can recognize permitted H by checking that H/2+1 is a power of 2 and n=log2(H/2+1) has form 4*3^t, then compute both neighbor and inverse maps in poly(n) time and space from polynomials of degree d. Since n=Theta(log H), both costs are polylog(H). No per-H tables, nonuniform graph selection, giant source arrays or oracle are required. The spectral theorem supplies a uniform edge-expanding subsequence; an individual finite eigenvalue calculation is NOT the theorem.

## Theorem 498.2: authenticating the existing signed strict-3CNF family

Use LSPV-2/495 and /497 without changing their source semantics. Number the left vertices by j=0,...,Q-1, represented by the nonzero n-bit vectors j+1. Right vertex r has color-i left neighbor M_i^-1(r+1)-1. Color 1's matching index is j. Left/right matching edge identifiers are respectively 2j+1+a_j and 2j+1+b_j; colors 2/3 use shared stable nonmatching identifiers H+2j+1 and H+2j+2. Sort each local triple and emit four original strict proper signed width-three clauses for a parity equation, with one odd charge at left j=0 and all other charges even.

The exact specialized binary format of /497 has 8 magic bits, unary H, unary 2H, 12H sign/ID fields of width W+1, W=ceil(log2(2H+1)), and two trailer bits. Its length is

$$
N=3H+12+12H(W+1)=\Theta(H\log H).
$$

The source can be authenticated a packet at a time by recomputing graph neighbors/inverses, reading the first matching ID to recover each a_j or b_j, regenerating all four signed clauses, and checking every bit. Then compare matching bits using indexed reads. Under the exact *declared specialized source grammar*, source membership and SAT iff a!=b are decided in O(N polylog N) time and polylog(N) writable space, with no stored a/b arrays. If an input is outside the grammar, this classifier returns OUTSIDE, **not a general-CNF malformed verdict**. On a=b, the original odd-charge cubic-expander Tseitin 3-CNF is preserved by variable renaming and has published exponential **ordinary DAG Resolution** refutation size; with a!=b it is SAT (prior /495 rank proof). This does NOT transfer hardness to arbitrary SAT algorithms, historical R_mix341, Extended Resolution or native FLMV computation. The graph family is a sparse infinite subsequence, which is sufficient for the restricted family construction.

## COMPUTATIONAL verification

Independent Python bit-polynomial implementation: 21,521 assertions, H=30 cubic graph, 45 edges, 120 source clauses, N=2622 bits, 300 source tests (200 SAT/100 UNSAT) checked by GF(2) rank; nontrivial singular value <=2.30277564<2sqrt(2). An additional 120 sampled nonzero vertices at field degree d=6 checked inverse maps and distinct neighbors. Independently authored Node GF(4) implementation: 90,722 assertions, 200 source tests (100 SAT/100 UNSAT), exact regenerated-source classifier and **all 2622 single-bit corruptions rejected**. Seed 20261108. The Python and Node runs are independent host tests, NOT native indexed FLMV machine measurements or proof of asymptotic expansion. The host implementations store entire graph tables and strings; only the symbolic streaming algorithm has the stated small-space bound. Source/index reads, graph inverse computations, output and state overlap are charged in the symbolic accounting; physical FLMV simulation remains OPEN.

## ITERATE / proof status

The literature corrected /497's use of **MSS existence alone** for graph generation: the 2018 locally explicit degree-three graph plus an explicit edge-color inverse closes precisely that missing restricted premise for a specific infinite family. The original bound, streaming comparison, legal GF(2) shortcut and all-source failure remain correctly scoped. Fastpath with unchanged arbitrary guest fallback still fails against padded deciders by LSPV-2/497. No all-input source decomposition, exponent-oblivious A->Phi(A), native time-space simulation or recursive closure has been constructed.

**TRACKER CHANGE REQUIRED:** add this restricted uniformity evidence to [P2-A4] only; do not modify the statuses of [P2-A2], [P2-A5] or the Route B open nodes. Root main.tex remains untouched if not fully readable/owned. P versus NP OPEN.
