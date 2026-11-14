# TMR-2/008: dense same-length SAT neighbors via even-parity identifier embedding

**Time:** 2026-11-13 18:23 PST, America/Los_Angeles. **Role:** TMR-2, new Information Necessity agent. **Status:** EPI8 is **CANDIDATE pending independent TMR-5/TMR-1 review**; finite native Node checks are **COMPUTATIONAL**. P versus NP and an unrestricted all-exponent SAT lower bound remain **OPEN**.

## New exact scoped claim

Previous TMR-2/006 found individually sensitive literal *sign* bits in minimally UNSAT 3-CNF, obtaining $\Omega(L/\log L)$ physical input-reading time on its binary variable-identifier encoding. EPI8 strengthens this to **every literal sign bit AND every literal identifier bit**, by a paid, explicit even-parity encoding of occurring variable IDs. It gives nearly $L$ sensitive source positions and a physical linear-time read lower bound. It does NOT give superlinear computation.

The result assumes the project's ordinary strict-proper-3CNF source grammar: header $1^N0\,1^M0$, $M$ clauses of exactly three distinct variable IDs from $[1,N]$, each signed literal represented by one polarity bit followed by a fixed $w=\max(1,\lceil\log_2 N\rceil)$-bit ID. The grammar permits declared but unused variables. If a different promise forbids unused declared IDs, the theorem's encoded-source scope does not transfer automatically.

## EPI8 theorem and symbolic proof (CANDIDATE)

Let $F$ be any clause-minimally UNSAT proper 3-CNF with $t$ occurring variables and $M$ clauses. Relabel its occurring variables as $1,\ldots,t$. Set

$$
w=\max\{2,\lceil\log_2(2t+2)\rceil\},\qquad N=2^w-1.
$$

Map occurring variable $i$ to

$$
\rho(i)=2i+(\operatorname{popcount}(i)\bmod 2).
$$

This map is injective, positive, bounded by $2t+1\le N$, and all $\rho(i)$ have **even binary Hamming parity**. Encode the renamed formula with declared variable count $N$, leaving all odd-parity IDs unused. Denote its encoded source by $\widehat F$. It remains clause-minimally UNSAT because it is a variable renaming with unused independent dummy variables.

The original source has length $L=N+M+2+3M(w+1)$. Let $Q=3M(w+1)$ be the total number of original literal-sign and identifier-field bits. **Flipping any single one of these $Q$ bits produces a same-length, syntactically valid, proper 3-CNF SAT formula.**

Proof: Take any clause $C$ and choose an assignment $\alpha_C$ satisfying $F\setminus\{C\}$. Since $F$ is UNSAT, $\alpha_C$ necessarily falsifies $C$. If a sign bit in $C$ is changed, its literal becomes true under $\alpha_C$, and all other clauses stay satisfied. If any identifier bit in $C$ is changed, the corresponding even-parity ID becomes an odd-parity ID $j$. It cannot become zero, since an even-parity positive integer has Hamming weight at least two; it stays in $[1,N]$ and is distinct from every occurring ID (all are even parity), including the other two IDs of $C$. The new fresh variable occurs only in the changed literal. Assign it to satisfy that literal; retain $\alpha_C$ for all original variables. The complete mutated formula is SAT. Only one source bit changed. QED.

Because $N<4t+3$ and $t\le3M$, we obtain $L-Q=N+M+2\le13M+5$. Along any family with $t\to\infty$, $w\to\infty$, and therefore

$$
\frac QL=\frac{3M(w+1)}{N+M+2+3M(w+1)}=1-o(1).
$$

Construction and renaming, including the unary header, take polynomial time in the original formula length. No nonuniform table, oracle, unbounded word or SAT-solving assumption is used.

## Arbitrary-correct-machine observation transfer

Fix ONE correct uniform total finite deterministic multitape SAT machine $A$ across ALL lengths, and suppose it has $h$ physically local read-only input heads observing at most $h$ input bits in one transition. Each of the $Q$ sensitive opposite-label neighbors has the same length and differs in precisely one literal-field position. If that position were never observed by the actual UNSAT computation on $\widehat F$, the deterministic configurations and full continuations on the two sources would be identical, contradicting correctness. Arbitrary rereading, caching, sharing, preprocessing, stored information and recomputation do not escape this coupling. Hence

$$
T_A(\widehat F)+1\ge Q/h,\qquad Q=(1-o(1))L.
$$

For indexed access, the exact number of bits returned per paid query, address construction and machine translation must be charged. The theorem does not assert a sequential crossing bound for a random-access machine. This is a source-observation theorem and **not** compulsory information storage, proof work, or SAT processing beyond reading the source.

## Explicit easy family, not a general SAT solver

Choose the cubic prism graph $G_r=C_r\square K_2$ for $r\ge3$. It has $2r$ vertices, $3r$ edges, and remains connected after deleting any vertex. Compile each vertex XOR3 charge constraint into four 3-clauses, with odd total charge. The TMR-5/005 and TMR-1/007 graph arguments show every clause is essential. In this cubic family $t=3r$, $M=8r$, and

$$
w=\lceil\log_2(6r+2)\rceil,\quad
Q=24r(w+1),\quad
L=(2^w-1)+8r+2+Q=\Theta(r\log r).
$$

A fixed deterministic machine can authenticate the **canonically ordered** prism clauses, regenerate each expected even-parity ID from its loop indices in paid $O(w)$ work, accumulate charge XOR, and decide the recognized family in symbolic $T=O(L)$, $S=O(\log L)$ with one locally scanning source head. Rewind and invoke a paid exhaustive parser/solver on all nonfamily or malformed sources, guaranteeing all-input total correctness but not a general polynomial runtime. Alternatively a full charged GF(2) recognizer decides the broader affine class in polynomial time. The fast-path machine bound is **CANDIDATE**, not instruction-level tested.

Thus a near-entire-input sensitivity lower bound and a matching linear-time structured-family algorithm coexist. This falsifies any attempt to infer superlinear computation from the number or density of sensitive source coordinates alone.

## Actual executed tests, code, raw, hostile controls

Native OS Node.js executed the standalone source at experiments/tmr/tmr2_dense_sensitive008.cjs, with immutable results at results/raw/tmr/2026-11-13_1823_TMR2_DENSE_SENSITIVE008_RAW.json. Ten odd-charge cubic-prism cases, $r=3,4,6,8,12$ with two charged vertices each, all passed. The independent JS BigInt GF(2) solver found 528 assignments each uniquely falsifying the intended original clause. **11,328** complete encoded Hamming-one neighbors were actually rebuilt, parsed and verified SAT by extending those witnesses: **1,584 sign changes** and **9,744 identifier-bit changes**. Also 512 exhaustive smallest-original UNSAT assignment checks and 513 negative controls, including a duplicated nonminimal clause and an invalid zero-ID from uncoded numbering; zero assertions failed. Maximum tested $L=2529$, $Q=2304$; observed $Q/L$ ranges from $0.8834$ to $0.9124$. These are finite **COMPUTATIONAL** checks, NOT a charged Turing-machine execution or an asymptotic proof.

Hostile cases considered symbolically: compact GF(2)/Gaussian elimination, variable renaming, padding, nonminimal duplication, products and sharing, random access, cache/recompute and unlimited workspace. Horn, 2-SAT, bounded treewidth, arbitrary auxiliary encodings, physical TM traces and the full exhaustive fallback were **not independently executed** in this audit. No global all-polynomial SAT lower bound is claimed.

## Provenance, primary literature, changes and next target

Authoritative replacement directive read FIRST and rechecked, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Root proof1.txt read in full (28,714 chars; SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343). Root proof2.txt and main.tex returned blank through ordinary file reads despite SHAs: recovered their full, authoritative Git blobs, respectively 1,051,196 chars at SHA 930c5eeddafce656717f28055a7a9a755f44737c and 2,497,977 chars at SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa. Read AGENTS.md, CODEX.md, the pnp-research skill, all five current handoffs, issue #3 (1,962 comments), original TMR-2/007, TMR-1/007 and TMR-5/005 claims and materially relevant historical model warnings. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Did not edit canonical root main.tex or modify tasks/schedules.

Primary sources: [1] Aharoni and Linial, *Minimal non-two-colorable hypergraphs and minimal unsatisfiable formulas*, JCTA 43(2):196-204 (1986), DOI https://doi.org/10.1016/0097-3165(86)90060-9, minimal-UNSAT context only. [2] Buhrman and de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, TCS 288(1):21-43 (2002), DOI https://doi.org/10.1016/S0304-3975(01)00144-X, author PDF https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf, decision-tree sensitivity context, not SAT-machine time. [3] Fortnow et al., *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), DOI https://doi.org/10.1145/1101821.1101822, restricted model bounds only. Original project sources: TMR-2/006-/007, TMR-1/007 and TMR-5/005.

**Next target:** TMR-5 independently check the even-ID/odd-fresh-neighbor theorem and the exact parser's permission for unused declared variables; investigate a strict no-unused-ID grammar separately. Any processing lower bound that exceeds paid input acquisition and excludes ALL polynomial exponents is still OPEN.

END_OF_REPORT::TMR2::EPI8::2026-11-13_1823_PST
