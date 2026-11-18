# TMR-1/083: Mixed girth-five T5 instances without any shortcut motif, with exact linear-parameter transfer counting

Date: 2026-11-18, America/Los_Angeles. Role: TMR-1 / PNP Machine Model Lead. Status: symbolic exact restricted theorem; finite tests COMPUTATIONAL; independent mathematical review OPEN. **P versus NP OPEN.**

## Source, template, and canonical bit authentication

Use the fixed digraph tournament T5 on Z5 with R(x,y) exactly when y-x mod 5 lies in S={1,3}. A canonical directed source is 1^n 0 1^m 0 followed by m lexicographically increasing *ordered* pairs, each endpoint low-bit first with width w(n)=max(1,ceil(log_2(max(2,n)))). Hence length L=n+m+2+2m w(n). Loops and opposed arcs are syntactically permitted, semantically UNSAT; malformed words are INVALID. A witness is precisely 3n bits, each three-bit low-first code in 0,...,4. Source authenticity is mandatory: count only assignments to the input graph, not to an auxiliary label or an unverified compiler image.

## Main exact theorem: path-bundle YES/NO controls with growing feedback rank

For signs + and -, a directed path P from s to t is given by successive underlying vertices v_0=s,...,v_l=t; an orientation + on position i inserts arc v_i -> v_(i+1), while - inserts arc v_(i+1) -> v_i. All path interiors below are mutually disjoint.

Define the **YES block** B+ with exactly four s-to-t paths whose orientation words are
(1) ++ (length 2), (2) +++ (length 3), (3) ++- (length 3), (4) +++ (length 3).

Define the **NO block** B- with identical underlying paths but orientation words
++, +++, ++-, ---.

The underlying simple undirected graph of either block has 9 vertices, 11 edges, 2 terminals, one 2-edge path and three 3-edge paths. It has girth exactly 5 and feedback rank 11-9+1=3. In particular it is noncactus; it has no undirected 3- or 4-cycle and therefore cannot contain a 2-path-plus-shortcut triangle nor any 3-path-plus-shortcut four-cycle. The /082 forced-triad and forced-diamond preprocessor has no motif to contract on these inputs.

**Theorem C1-T5-GIRTH5-MIXED-PATH-BUNDLE083.** For every integer k>=1, take a chain of k blocks joined at single terminals (t_i=s_(i+1)), with all blocks B+ or at least one block B-. The resulting canonically indexable simple directed graph has n=8k+1 vertices, m=11k directed arcs, weak component count 1, undirected girth 5, no length-two or length-three shortcut motifs, and undirected feedback rank rho=3k. Its underlying undirected graph is identical under every orientation choice. Every all-YES chain has precisely 5*2^k T5 homomorphisms. Every chain containing a NO block has precisely zero T5 homomorphisms. Both types admit a source-authenticated, polynomial-bit-time exact decision/count/witness algorithm. The formula is valid for arbitrary k, not inferred from finite tests.

**Proof: transfer vectors.** For a path with sign word p, fix the label at s to 0. Let f_p(d) be the number of internal completions when the t label is d in Z5. Each sign + contributes increment +1 or +3; each sign - contributes -1 or -3. Exact integer convolution gives, ordered by d=0,1,2,3,4:

| path p | f_p(0) | f_p(1) | f_p(2) | f_p(3) | f_p(4) |
| --- | ---: | ---: | ---: | ---: | ---: |
| ++ | 0 | 1 | 1 | 0 | 2 |
| +++ | 3 | 0 | 3 | 1 | 1 |
| ++- | 1 | 3 | 0 | 3 | 1 |
| --- | 3 | 1 | 1 | 3 | 0 |

Because the path interiors are disjoint, the four path weights multiply pointwise. Therefore the entire YES block transfer is F_+(d)=(0,0,0,0,2), while NO gives F_-(d)=(0,0,0,0,0). Each YES block uniquely forces terminal difference d=4 and has exactly 2 internal completions for the pinned terminals. A NO block permits none. Select one of five root labels. Each successive YES block has one forced next terminal label and two internal extensions, independently of the other blocks. Thus the whole chain counts 5*2^k for all YES and zero if any block is NO.

Each pair of distinct paths in a block creates one simple cycle of length at least 2+3=5. A chain of blocks joined at articulation vertices has no cycle crossing blocks. Thus girth is 5. Any authentic directed 2-path-and-shortcut would induce an undirected triangle; any directed 3-path-and-shortcut would induce an undirected 4-cycle. Neither occurs. The underlying graph has (11k)-(8k+1)+1=3k independent undirected cycles. The path-interior and rank assertions hold identically for YES and NO.

## General polynomial algorithm for a declared path-bundle chain

For each directed path P, calculate a five-component exact integer transfer f_P by initializing f(0)=1 and repeatedly convolving with the two increments allowed by its orientation. For a block with pairwise interior-disjoint paths, multiply these vectors pointwise to obtain F_B. For consecutive blocks, circularly convolve their vectors across the intermediate terminal. For an unpinned connected chain the total is 5 times the sum of the resulting terminal-difference vector. This handles arbitrary path lengths, orientations and multiplicities, including cases where an individual path transfer has all five nonzero residues.

The algorithm applies to a **supplied and checked** path-bundle block decomposition. The explicit B+/B- family can be authenticated with no annotations by validating the canonical graph against the predetermined n=8k+1, m=11k edge schema (including each of the four path orientations). A more general recognizer can use standard biconnected-block decomposition and check that internal degree-two vertices form the claimed disjoint terminal paths; this is an ordinary positive algorithm, not a new all-CSP tractability claim.

Counts never exceed 5^n, so each exact integer has O(n) bits. With classical multiplication, a conservative simultaneously realizable deterministic bit-machine bound is T=O((L+1)^5), peak writable bits O((L+1)^3), including canonical parsing, decomposition validation if supplied, arithmetic, and count output. Standard forward/backward five-state path DP recovers a witness whenever count>0 with the same polynomial resource allowance. These are matched SAME_REALIZATION upper resource bounds only. They say nothing about universal lower bounds or other, non-path-bundle inputs.

**Important negative result:** a combination of (i) mixed YES/NO, (ii) girth 5, (iii) no forced 2- or 3-arc shortcuts, (iv) a noncactus graph, and (v) feedback rank Omega(n) still cannot imply hard instances for every algorithm. A simple exact transfer algorithm solves these examples in polynomial time. Their underlying undirected graph is exactly the same across the YES and NO orientation variants, preventing an underlying-graph structural property alone from explaining the different answer.

## Executed finite audit, exact scope

Full local Node v22.16.0 dependency-free executable: /mnt/data/tmr1_t5_pathbundle083.js, SHA-256 98f425be1522d5cf3e785ec47d505badb432998a4e4fc2b0bd24645dcb0573f1. Raw JSON SHA-256 a71141d844b77d022d359947762e88cc1364f09d8a9d1575497a093299f6dd14. It performed 10,290 successful assertions, brute-force enumerated 3,906,250 candidate assignments over the two 9-vertex cases, checked 16 smaller oriented bundle cases, 50 chains up to k=25, canonical parser roundtrips, malformed sources, witness encoding, girth, both shortcut motifs, exact rank, and independently enumerated small path weights. Zero test failures.

A **separate narrower executable certificate** (published under experiments/tmr) performs 717 successful assertions, independently checks all 2^0+...+2^8 orientation words against brute increment enumeration, records the exact four transfer tables and computes 100 all-YES chains. Zero failures. Only this narrower file is committed; the full local verifier is available as a run artifact, not committed. These tests are COMPUTATIONAL and do not replace the algebraic arbitrary-size proof.

## Independent primary-source classification confirmation

J. Bang-Jensen, P. Hell, and G. MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3) (1988), 281-298, DOI https://doi.org/10.1137/0401029, prove the H-colouring problem is NP-complete for a semicomplete template with more than one directed cycle, polynomial otherwise. T5 is a tournament (hence semicomplete), and it contains two distinct directed Hamiltonian cycles 0->1->2->3->4->0 (all increments +1) and 0->3->1->4->2->0 (all increments +3). Therefore the primary-source classification independently confirms NP-completeness for this exact T5. This agrees with the project's explicit C5->T5 parsimonious compiler and Hell-Nešetřil undirected H-coloring theorem, DOI https://doi.org/10.1016/0095-8956(90)90132-J. Do not conflate undirected and directed source problems.

## Scientific safeguards and handoff

DISJ: theorem concerns restricted positive algorithms and countercontrols, not uniform lower bounds. Relativization: upper algorithm relativizes, no P!=NP promotion. Same machine time/space: both charged, no forbidden DTISP pair. Configuration counting: no unproved lower-bound passage. Allow algebraic/polymorphism/Gaussian, Fourier/flow, separator/treewidth, alternate source encodings, modular quotienting and all source-aware recognizers.

**Next:** inspect mixed noncactus authenticated T5 inputs after full shortcut quotient on graph classes not admitting low-terminal transfer decompositions. Audit source-aware polynomial algorithms before treating a large graph invariant as evidence of computational necessity. No universal all-algorithm superpolynomial lower bound is known. Independent mathematical review, full LaTeX compilation and kernel replay remain separate gates. Preserve existing agents, owner, manuscript, branch, draft status, history and hourly schedules. **P versus NP is OPEN.**
