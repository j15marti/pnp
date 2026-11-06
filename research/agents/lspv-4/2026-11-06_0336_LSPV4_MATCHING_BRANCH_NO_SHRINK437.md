# LSPV-4/437 | Matching-edge splitting fails to shrink Tseitin 3-CNF

**2026-11-06 03:36 PST | Route A primary | PROVED/RESTRICTED mathematical theorem; COMPUTATIONAL finite checks | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE and falsifiers

**Hypothesis.** Even after the LSPV-4/435-436 authenticated reversible port and LSPV-2/440 certified graph source, a natural SAT-child generator based on branching and unit propagation might fail the required $N^{1/2}$ child-length premise. We test this on a **published hard-in-Resolution family**, not an invented SAT challenge.

Four falsifiers stated before search: F1, matching-edge assignments create units that cascade; F2, some branch deletes most untouched clauses; F3, size comparison silently changes the size baseline or assumes arbitrary encodings are incompressible; F4, known algebraic shortcuts defeat a general algorithmic-hardness interpretation. The proof excludes F1-F3 **only for the declared literal-preserving compiler/encoding**. F4 indeed defeats any claim against all algorithms and is retained as a legal upper control.

## Certified family and theorem ledger

Ben-Sasson and Wigderson, *JACM* 48(2), 2001, Def. 4.1, Lemma 4.2, Thm. 4.4, Cor. 4.5, and Urquhart 1987, establish exponential **ordinary shared-DAG Resolution** proof-size lower bounds for odd-charge Tseitin contradictions on suitable growing connected cubic expanders. This is not a SAT machine lower bound, not an Extended Resolution bound and not a full historical $R_{\mathrm{mix341}}$ bound.

For a connected cubic graph $G_H$ with $H$ vertices, $M=3H/2$ edges, a Boolean edge variable per edge, ordered incident edge IDs $a_v<b_v<c_v$, charges $\chi_v$, and $\ell_0(x)=x$, $\ell_1(x)=\neg x$, the **original proper 3-CNF** is exactly the $4H$ clauses

$$
C_{v,p,r}(\chi)=\ell_p(x_{a_v})\lor\ell_r(x_{b_v})\lor\ell_{p\oplus r\oplus1\oplus\chi_v}(x_{c_v}),\qquad(p,r)\in\{0,1\}^2.
$$

It asserts $x_{a_v}\oplus x_{b_v}\oplus x_{c_v}=\chi_v$, and is UNSAT exactly when $\bigoplus_v\chi_v=1$. It is already strict 3-CNF, so no further 3-CNF reduction is used. The test-packet encoding is 8-bit magic, unary $H$ and $M$, $H$ charges, $3H$ incident IDs of fixed width $w=\lfloor\log_2 M\rfloor+1$, and $12H$ signed literal fields each of width $w+1$:

$$
N=8+(H+1)+(M+1)+H+3Hw+12H(w+1)=\Theta(H\log H).
$$

This augmented packet *counts* metadata on the supplied input; its original CNF literal body alone is $12H(w+1)$ bits. Finite K4/cube/Petersen/Mobius tests do not certify expander hardness.

## Theorem 437.1 (PROVED/RESTRICTED, complete combinatorial proof)

Fix **any matching** of $k$ edges. A maximal matching in a cubic graph has at least $3H/10$ edges: a selected edge can forbid only itself and up to four incident neighboring edges, and the graph has $3H/2$ edges. Hence every $k\le 3H/10$ is feasible. For every assignment to the $k$ matched edge variables, exactly $2k$ distinct vertices have one fixed incident edge, and the other $H-2k$ vertices have none.

In every affected vertex's four forbidden-parity clauses, fixing exactly one edge variable satisfies exactly two clauses and reduces exactly two to binary clauses. At every untouched vertex, all four ternary clauses remain unchanged. No residual unit or empty clause exists, so ordinary unit propagation has nothing to do. Thus **all $2^k$ cases**, SAT or UNSAT, contain exactly

$$
\boxed{4(H-2k)\text{ original width-three clauses }+4k\text{ width-two clauses; zero units}.}
$$

There is no hidden branch-choice, omitted AND case, or incompatible-context lemma reuse. For an actual UNSAT refutation using case splits, all cases must be discharged unless another legal refutation avoids the split.

## Corollary 437.2: no $N^{1/2}$ child from this compiler

Choose $k=\lceil(3/5)\log_2 N\rceil$, feasible for sufficiently large $H$. Then $q=2^k=\Theta(N^{3/5})$, but the explicit, literal-preserving residual still has at least

$$
L\ge12(H-2k)(w+1)=\Omega(N)
$$

signed source-literal bits. Densely renumbering the $M-k=\Theta(H)$ surviving variables preserves $\Theta(\log H)$ bits per ID in the declared fixed-width representation. In particular, **$L=N^{1/2+o(1)}$ does not follow from this branching and unit-propagation construction**.

Directly writing $q$ residuals uses $\Omega(qN)=\Omega(N^{8/5})$ bit-output work. Materializing even one complete residual on a work tape incurs physical high-water $\Omega(N)$; all concurrently require $\Omega(qN)$. These are explicit-materialization costs only, not lower bounds for arbitrary lazy representations, smarter preprocessing, algorithms or proof systems. A shared immutable core and $O(k\log H)$ branch masks can avoid copies but do not magically shorten the guest-visible expanded formula. Consequently, the contraction budget $N^{3/5+t/2}$ cannot be justified by claiming these children are $N^{1/2}$ long.

## Legal shortcuts and resource ledger

The original vertex equations XOR to $0=\bigoplus_v\chi_v$: an authenticated source admits a direct, efficiently verifiable GF(2) SAT/UNSAT decision, and a spanning-tree assignment for even charge. This is the strongest relevant **upper bound** on the family, not a trick to exclude. Cook Extended Resolution, Haken PHP ordinary Resolution, branch sharing and source-aware preprocessing remain mandatory controls. Historical $R_{\mathrm{mix341}}$ receives no new split/discharge rule.

**Original acquisition/authentication:** read and validate all original bits, source indexes, graph/tree annotation, and malformed encodings. LSPV-2/440 proves $O(N\operatorname{polylog}N)$ validation time and $O(\log N)$ physical writable space when a read-only annotation is *supplied*, not when built for raw arbitrary CNF. **Policy selection/failures:** charge every attempted matching and rejected approach. **Descriptors:** $q$ branch labels, $k$ bits each; cache/reference accesses paid. **Materialization/output:** $\Omega(N)$ per explicit residual, $\Omega(qN)$ total. **Propagation:** no units on these branches, but checking itself is not free. **Guest:** no justified reduction to size $N^{1/2}$, all calls count; no general runtime lower bound follows. **Joining:** for UNSAT, AND all required branches; for SAT, one valid witness suffices. **Space:** use all-phase simultaneous head/index/work-tape high-water, parent/child buffers and retention/recomputation, not the number of live logical DAG nodes. Host measurements below are not native FLMV traces.

The FLMV arithmetic is still conditional: $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ would yield $\beta(6/5)-1/2=1/90$, **if** a recursively iterable all-input same-machine transformation existed. It remains OPEN.

## Reproducibility (COMPUTATIONAL)

The original Python producer constructed 14 exact odd/even 3-CNFs on K4, cube, Petersen, and finite Mobius ladders of 20, 64, 128 and 256 vertices. For $k\le4$, **all 124 matched-edge assignment branches** were checked. Python recorded **124 UP controls, 124 GF(2) elimination controls, 55,548 unchanged-clause assertions and 14 encoding checks**. An independent Node.js verifier reconstructed input hashes and clause counts and checked satisfiability by **graph-component parity rather than Gaussian elimination**, passing **567 assertions**. For K4: $N=252,k=1$, 8 ternary and 4 binary residual clauses. For cube: $N=614,k=1$, 24/4. For Petersen: $N=765,k=1$, 32/4. For Mobius 64: $N=7722,k=4$, 224/16; Mobius 256: $N=38538,k=4$, 992/16. All measured parity-control outcomes matched. The Mobius ladders are scaling/semantic controls, *not* certified expander-hard inputs. Earlier LSPV-2/440 malformed/corrupted tests are inherited controls, **not rerun here**.

## Actual literature, code and peer review inspected

Primary Ben-Sasson/Wigderson 2001 PDF visually inspected at journal pp.155-156 for Def. 4.1, Thm. 4.4 and Cor. 4.5; Urquhart 1987 DOI 10.1145/7531.8928; FLMV 2005 DOI 10.1145/1101821.1101822. Project: historical five-role handoff blob `033b54b8`, current issue #3 (including LSPV-2/440 and LSPV-3/445 comments), LSPV-2/439 blob `b98d6e84`, LSPV-2/440 blob `d04f60c6`, LSPV-4/436 blob `86f38465`, Grok `GROKPROOF/2026-11-06_0920_PROGRESS.md` blob `6b32bc30`, Claude `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` blob `b7150bb9`. Both required external repos: `konard/p-vs-np/proofs/complexity/README.md` blob `7ee9a11e` (one-tape model differs from FLMV); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea` (model-specific proofs). Additional actual sources: `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd19`, `meelgroup/frat-xor/README.md` blob `38a137bc`, `openai/math/README.md` blob `cc5b0a0`. Indexed web and authenticated repository search ran; direct Google-branded search was unavailable. No claim of proof of P vs NP or formal CI verification.

**Advance:** a literal-preserving matching-restriction+unit-propagation compiler cannot supply shrinking children on a standard known hard-in-Resolution family. **Verification:** complete proof for this restricted compiler, independent finite reviewer PASS, native FLMV trace not obtained. **OPEN:** existence of an ALL-INPUT, both-label, malformed-aware, source-authenticated recursively iterable same-machine contraction for *every* correct uniform polynomial SAT decider, with true costs. Route B fixed-mixed superpolynomial minimum and noncircular B3 remain separate OPEN gaps. **P versus NP OPEN.**
