# LSPV-2/456: Moving-frontier FLMV guest compiler
**2026-11-06 17:14 PST | Route A | PROVED/RESTRICTED; COMPUTATIONAL | P versus NP OPEN**

## Falsifiers and repair
Proposed repair to LSPV-2/455 and LSPV-4/453: instead of one global common separator, use many different bounded interfaces along a sequence of signed 3-CNF blocks. Falsifiers: a local transition needs 2^(2w) rather than 2^w assignments; retaining all messages may exceed space; branch-local truth may leak across incompatible assumptions; and certified hard expander sources may require a large *individual* frontier. The corrected bound is w <= (1/20) log_2 N, rather than the earlier single-separator (1/10) log_2 N.

## Theorem 456.1 (PROVED/RESTRICTED)
An authenticated special sublanguage of original strict signed 3-CNF has

$$
F=\bigwedge_{i=1}^{h}F_i(X_i,Z_{i-1},Z_i),\qquad Z_0=Z_h=\varnothing.
$$

Private variable sets X_i and connector sets Z_j are pairwise disjoint; every original clause is stored in exactly one contiguous block. A self-delimiting *leading* header and canonical increasing disjoint ID ranges certify these properties with N^(1+o(1)) sequential time and N^o(1) writable scratch. All header bits, names, literals, scans and head operations count in N. Assume h <= N^(1/2+o(1)), every complete block encoded length L_i <= N^(1/2+o(1)), and w=max_i |Z_i| <= (log_2 N)/20+o(log N).

For EVERY fixed total correct polynomial-time general CNF-SAT decider A on the FLMV random-access machine, with guest time L^(t+o(1)) and writable space L^(s+o(1)), a finite same-machine wrapper correctly decides both SAT and UNSAT on this restricted structural sublanguage with

$$
t'\le\max\left(\frac{11}{10},\frac35+\frac t2\right),\qquad
s'\le\max\left(\frac12,\frac s2\right).
$$

Proof: fully authenticate the source, then maintain only two frontier arrays, each of at most 2^w Boolean entries. Initialize M_0(empty)=1. For every block and outgoing assignment b compute

$$
M_i(b)=\bigvee_{a}\left[M_{i-1}(a)\wedge
\operatorname{SAT}(F_i|_{Z_{i-1}=a,Z_i=b})\right].
$$

Every cofactor is a paid, physically materialized general CNF guest input, with explicit signed clauses and charged input-index, parsing, output and scratch costs. Induction proves that M_i(b) means a consistent satisfying extension of the entire prefix with boundary b; OR represents a choice of predecessor and AND requires all matching obligations. The final answer is M_h(empty). No cross-context lemma reuse, free input oracle or uncharged optimization.

Total guest calls q <= h*2^(2w) <= N^(3/5+o(1)); every guest length is at most N^(1/2+o(1)). Local validation, rereads, child construction and joining cost at most N^(1+2w/log_2 N+o(1)) <= N^(11/10+o(1)). Simultaneous high-water writable space includes two frontier arrays, one source block, one child, guest work/index tapes and all temporary buffers and is N^(max(1/2,s/2)+o(1)). This is a mathematical same-model construction for the special grammar, NOT a native FLMV instruction trace. In a chain with h-1 different singleton connectors, the union of named interfaces has h-1 variables, so the compiler covers source partitions not covered by the prior O(log N) GLOBAL-common-separator promise. This is established frontier/junction-tree dynamic programming specialized to the present exponent ledger; no priority is claimed for dynamic programming.

## Certified hard family and transfer limit (PROVED/RESTRICTED)
Take odd-charge Tseitin contradictions on connected cubic expander graphs G_H with H vertices and edge expansion |delta(U)| >= epsilon |U| for |U|<=H/2. This is the established native 3-CNF family of Ben-Sasson and Wigderson JACM 2001 Definition 4.1, Theorem 4.4, Corollary 4.5, following Urquhart JACM 1987. At vertex v with incident edges a<b<c, the FOUR original signed clauses are

$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee
\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),\quad p,q\in\{0,1\},
\quad \ell_0(x)=x,\ \ell_1(x)=\neg x.
$$

There are 3H/2 variables, 4H clauses, 12H original occurrences, N=Theta(H log H) explicit binary input bits. Odd total charge certifies UNSAT. The lower bound is 2^Omega(H) size in ordinary shared-DAG Resolution, NOT in historical R_mix341, Extended Resolution, GF(2), or arbitrary machines. In fact direct GF(2) charge summation is easy.

For any order of intact vertex-clause packets into blocks of o(H) vertices, choose the first prefix U with |U|>=H/3. For large H, H/3<=|U|<=H/2. Each crossing edge contributes an original variable present on both sides, so every packet-preserving running-intersection path interface at that cut must retain the cross-edge variable. Therefore

$$
w_{\rm packet\ path}\ge|\delta(U)|\ge\epsilon H/3
=\Omega(N/\log N).
$$

This violates w <= (log_2 N)/20. The obstruction concerns only syntactic source-packet layouts; derived algebraic summaries, a white-box solver and all-input transformation remain possible.

## Independent finite controls, provenance and remaining work
Python produced 72 exact signed original 3-CNF sources, 24 SAT and 48 UNSAT, with 368 assertions PASS and 8 corrupt structural-promise records rejected. Independent Node.js reconstructed all original signed clauses and K4 parity packets, compared all 72 SHA-256 hashes, evaluated the full parents and the cofactor joins by independently written DPLL, enumerated local witnesses, and passed 756 checks with 524 matching guest calls. K4 is ONLY a finite source/sign control, not a certified asymptotic-hard family. JSON fixtures are not native-machine space measurements; the theorem's streaming grammar uses a leading header and canonical disjoint ranges. No original historical mixed-calculus certificate was checked.

Actually reviewed project LSPV-2/455, LSPV-4/453, historical LSPV-2/213 and BLOCK-TRANSFER-STREAM212, LSPV-1/135, Grok REWIRE and Claude ONETAPE files, governing handoff, issue #3, AGENTS.md, CODEX.md and project skill. External actual files: konard/p-vs-np/proofs/complexity/README.md (blob 7ee9a11e), blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md (4aba9d94), FRAT-XOR README (38a137bc), mockturtle README (c1d2b0c4), openai/math README (cc5b0a03). Primary author PDFs FLMV Corollary 5.8 and Ben-Sasson/Wigderson section 4.1 and their page images were inspected. Web literature search was used; Google-branded search, native FLMV execution and independent external tool builds were unavailable.

**OPEN:** All-input, both-label, malformed-aware solver-dependent interface acquisition; effective recursive same-machine Phi(A) for EVERY correct polynomial SAT guest; full fixed R_mix341 lower bound and noncircular B3. P versus NP remains OPEN.

Sources: FLMV (2005), DOI 10.1145/1101821.1101822; Ben-Sasson/Wigderson (2001), DOI 10.1145/375827.375835; Urquhart (1987), DOI 10.1145/7531.8928; Fomin et al. (2015), DOI 10.1137/1.9781611973730.43. Extended local reproducibility package includes full proof, Python producer, independent JS verifier, raw 72-source ledger and SHA-256 manifest.
