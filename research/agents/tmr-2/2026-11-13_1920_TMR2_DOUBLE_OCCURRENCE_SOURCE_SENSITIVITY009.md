# TMR-2/009: two-occurrence strict 3-CNF sensitivity and independent peer review

**Date:** 2026-11-13 19:20 PST (America/Los_Angeles). **Role:** NEW TMR-2 Information Necessity. **New result:** TMR2-DO9, **CANDIDATE pending TMR-5 independent review**. **Finite verification:** COMPUTATIONAL. **Previously proposed TMR-5/006 and TMR-1/009 no-unused-variable lemma:** favorable independent mathematical review at its explicitly restricted scope. **P versus NP and the unrestricted all-polynomial-exponent deterministic SAT time lower bound: OPEN.**

## Precise advance over original TMR-2/008 and peer /006, /009

TMR-2/008 gives sensitive literal bits when unused declared variable identifiers are legal. TMR-5/006 and TMR-1/009 place every declared identifier in a positive filler clause, using $K=\lceil U/3\rceil$ filler clauses for $U$ spare identifiers. I independently checked the even-parity flip and clause-deletion witness arguments, including $w$-bit validity, the nonzero target ID, original-ID retention, correct signs and both answer labels. They are correct **for the declared grammar** (every variable occurs at least once), conditional only on the proven clause-minimally UNSAT core theorem. This is mathematical peer review, not an instruction-level machine audit.

**New scope:** require every declared identifier to occur in **at least two literal positions**, in both the original UNSAT formula and **each** Hamming-one SAT neighbor. For any clause-minimally UNSAT proper 3-CNF core $F$ in which every original variable occurs in at least three literal positions, the following explicit double-cover filler achieves this stronger grammar while preserving all $Q=3M(w+1)$ independently sensitive core field bits. In particular cubic-prism Tseitin XOR3 cores have **eight** occurrences of each edge variable.

## Source model, embedding and exact lengths

A proper 3-CNF clause contains three distinct positive variable IDs; negation is a separate source bit. Encode as $1^N0\,1^D0$ followed by $D$ ordered three-literal records, each a polarity bit and a fixed-width $w=\lceil\log_2(N+1)\rceil$ ID. Valid IDs are $1,\ldots,N$ and every declared ID must occur at least twice. The encoded source has **exact** length

$$
L=N+D+2+3D(w+1).
$$

Given $F$ with $t\ge3$ occurring variables, $M$ clauses, minimum core variable occurrence at least three, set

$$
w=\lceil\log_2(2t+2)\rceil,\quad N=2^w-1,\quad
\rho(i)=2i+(\operatorname{popcount}(i)\bmod 2).
$$

Map each original identifier $i$ to $\rho(i)$. These are distinct positive even-Hamming-weight-parity IDs. Let $U$ denote the set of all other IDs, with $u=|U|=N-t\ge4$. Order $U$ as $u_0,\ldots,u_{u-1}$ and create the following **positive proper triple filler**, containing precisely $K=\lceil 2u/3\rceil$ distinct clauses:

* If $3\nmid u$, for $k=0,\ldots,K-1$ use $(u_{3k\bmod u},u_{(3k+1)\bmod u},u_{(3k+2)\bmod u})$.
* If $3\mid u$, use the $u/3$ disjoint triples beginning at offsets $3k$ and the $u/3$ distinct triples beginning at offsets $3k+1$, all indices modulo $u$.

When $3\nmid u$, $\gcd(3,u)=1$, so the start offsets are distinct and the triples are distinct for $u\ge4$. Flattened indices cover the cyclic sequence $0,\ldots,3K-1$, so every ID occurs two or three times. When $3\mid u$, the two offset partitions cover every ID once each, so every ID occurs exactly twice; no triple repeats for $u\ge6$. Thus all filler variables have occurrence at least two.

Let $G=\rho(F)\land H_U$ and $D=M+K$. The original $G$ is UNSAT and properly encoded. Core variables occur at least three times; filler variables occur at least twice.

## Same-length one-bit SAT neighbors: proof

For any original core clause $C$, clause minimality gives an assignment $\alpha_C$ satisfying $F\setminus\{C\}$, necessarily falsifying $C$. A flip of one polarity bit makes the selected literal true under $\alpha_C$; set all filler variables to true. All unaltered clauses and all filler clauses hold. Occurrence counts do not change.

A flip of one identifier bit in $\rho(i)$ changes even binary Hamming parity to odd, producing an ID $j\in U$. Since $\rho(i)>0$ has even nonzero Hamming weight, it has at least two set bits and a single flip cannot yield zero. The new $j$ is distinct from the other two original core IDs, so the altered clause remains proper. Under $\alpha_C$, choose $j$ to make the altered literal true, and assign every *other* filler ID true. Every positive filler triple containing $j$ has two independently true other literals; thus every filler clause holds. The former core ID still occurs at least twice, because its original occurrence count was at least three, and filler-ID counts only increase. Therefore **every declared ID still occurs at least twice on the modified source**. The unary headers, record count, width and every source bit other than the flipped field bit are unchanged. Every one-bit neighbor is a well-formed same-length SAT formula.

Thus $Q=3M(w+1)$ original literal-field positions are individually SAT/UNSAT distinguishing. For any fixed total correct deterministic multitape 3-SAT machine $A$ whose $h$ read-only source heads observe at most $h$ binary input symbols per transition, if a sensitive bit is unread on $G$, the source $G$ and its opposite-label one-bit neighbor induce identical concrete steps, including all input head positions, control and writable tapes. This contradicts both-label correctness. Accordingly

$$
T_A(G)+1\ge \frac{3M(w+1)}{h}.
$$

There is no imposed space bound, no one-pass or online requirement, no proof-calculus assumption, and no assumption that equal work tape contents alone imply indistinguishability. Rereading and arbitrary processing are permitted but all accesses cost transitions. The exact transfer to any nonlocal uncharged input interface is NOT provided.

## Density and the actual computational ceiling

Since $N<4t+3$, $u<3t+3$ and $K=\lceil2u/3\rceil\le2t+O(1)$, while minimum core occurrence three gives $t\le M$, on any unbounded such core family with $t\to\infty$,

$$
\liminf\frac{Q}{L}\ge\frac13.
$$

For the cubic prism $C_r\square K_2$, $t=3r$ and $M=8r$, so $K\le6r+O(1)$ and the stronger explicit constant is

$$
\boxed{\liminf_{r\to\infty}\frac{Q}{L}\ge \frac47.}
$$

This is weaker sensitivity *density* than the one-occurrence filler of TMR-5/006 ($8/11$), but proves a strictly **stronger occurrence-validity model**. The density bound does not assert that all filler or header bits are sensitive.

An authenticated cubic-prism XOR/Tseitin source retains a compact global parity test and a paid polynomial or symbolic linear-time fast path, with exhaustive fallback on arbitrary off-family inputs. Therefore $Q\le L$ and all first-observation information arguments are bounded above by linear input acquisition. This result does **not** establish a post-acquisition superlinear cost or a universal superpolynomial lower bound. Gaussian elimination, Horn, 2-SAT, bounded-treewidth dynamic programming, disjoint products, sharing, padding, renaming, auxiliary variables, caching and recomputation remain legitimate hostile controls, not excluded machine classes.

## Actually executed audit and controls

An independently authored **native Node.js** complete source-and-witness program (not a wrapper of the peer executables) was run on 2026-11-13 PST, with explicit source parser enforcing **minimum occurrence two**. Deterministic cases were $r\in\{3,4,6,8,12\}$ and two odd-charge positions per $r$, no random seed. The program regenerated each encoded source, verified all source lengths, generated $528$ clause-deletion witnesses with independent BigInt GF(2) elimination, built and parsed all **11,328 same-length one-bit SAT neighbors**, and checked actual satisfying assignments on each. Counts: $1,584$ sign flips, $9,744$ identifier flips, $11,328$ min-two grammar checks, $10$ odd-charge UNSAT inputs, $10$ filler-only mutation controls that cannot cure UNSAT, $5$ constructed even-charge SAT controls, and $512$ exhaustive small UNSAT core assignments. **Zero failures**. Maximum length $L=4054$ bits, $Q=2304$ sensitive bits; sampled sensitivity ratios $0.5581$ through $0.6572$. Every original edge variable occurred eight times and every dummy at least twice. Checkpointing not needed: the native Node audit finished in one short invocation.

Published reproducer: \`experiments/tmr/tmr2_double_occurrence009.cjs\`; immutable evidence: \`results/raw/tmr/2026-11-13_1920_TMR2_DOUBLE_OCCURRENCE009_RAW.json\`. Finite source events and algebraic witnesses are **COMPUTATIONAL**. Physical Turing-machine transition tables, full exhaustive fallback, 2-SAT/Horn/treewidth solvers and all-size SAT search were NOT executed. The read-only input-head observation transfer is a mathematical model argument, not an instrumented TM benchmark.

## Dependencies, literature and corpus reconciliation

Dependency chain: original graph XOR3 clause-minimality (TMR-5/005 and TMR-1/007) $\to$ even-parity embedding (TMR-2/008) $\to$ peer one-occurrence filler (TMR-5/006, TMR-1/009) $\to$ **new positive twice-covered filler** $\to$ min-two valid one-bit neighbors $\to$ deterministic source-read coupling $\to$ $\Omega(L)$ **only**. The last arrow to all-exponent deterministic 3-SAT computation remains **OPEN**.

Primary-literature context, exact scope: [1] N. Nisan, *CREW PRAMs and Decision Trees*, SIAM Journal on Computing 20(6):999-1007 (1991), DOI https://doi.org/10.1137/0220062. It studies block sensitivity and decision trees/parallel models, not unrestricted SAT time. [2] H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288(1):21-43 (2002), https://doi.org/10.1016/S0304-3975(01)00144-X. [3] Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), https://doi.org/10.1145/1101821.1101822; it excludes some **simultaneous bounded time/space** regimes, not every polynomial-space machine.

Read FIRST replacement directive SHA \`47459817e66dccf1f3079e6c724c0fd2643e7bc4\`; read root proof1.txt in full (28,714 chars, SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`); recovered **complete** root proof2.txt (1,051,196 chars) using the contents REST URL when ordinary file-fetch returned an empty body; read **complete** root main.tex (2,502,146 chars, currently SHA \`62c0c400a5eddfbdbdfa06fbabcf7bcee8b753be\`) from actual Git blob after ordinary file-fetch returned empty. Also read AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, latest issue #3 comments, all five current handoffs, original TMR-1/009, TMR-5/006, TMR-2/008 reports and TMR-1/009 source/raw. The replacement supersedes older LSPV priorities in root guides, not historical valid mathematics. Main.tex changed since TMR-2/008 through TMR-5 synthesis; no root ownership region was edited by TMR-2. Repository checkout and repo preflight unavailable, but native standalone Node executed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both roots were deliberately untouched. No schedules or tasks were touched.

**Next single target:** independent TMR-5 audit of the two-occurrence filler for all residue classes $u\bmod3$ and of the fixed-head coupling; then test how far input-necessity certificates can ever charge post-read processing under compact parity/affine encodings. The unrestricted-machine processing arrow remains OPEN.

END_OF_REPORT::TMR2::DOUBLE_OCCURRENCE009::2026-11-13_1920_PST
