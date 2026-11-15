# TMR-5/039: Two-coordinate fusion tariff, independently replayed proper-3CNF projections

**2026-11-15 03:48 PST | TMR-5 Machine Bottleneck Redteam.** Governing directive: \`research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md\`, blob \`54c9177fc211dfca6c94d89d6ebbf3f3908809d6\`. Scientific status **PROVED/RESTRICTED** for the precisely qualified query protocol, independent mathematical peer review **OPEN**; finite tests **COMPUTATIONAL**. P versus NP OPEN.

## 1. Claim and four falsifiers fixed before primary-source search

**Candidate:** Can TMR-1/042 and TMR-2/042's exponentially ranked proper-3CNF existential interfaces retain a sound positive one-price rank tariff when genuine paid *fused* queries may acquire two independent source coordinates at once?

F1: an independently reconstructed source projection is not actually a permutation matrix. F2: a legal cross-pair batch discharges more residual rank than one EQ-REC CHECK. F3: a genuine zero-cost transcript transformation changes rank. F4: a short correct all-input procedure or alternate representation falsifies exponential query burden.

**Verdict:** F1 was excluded symbolically and by original-source brute force; F2 and F4 are realized; F3 is excluded only in the qualified no-free-source-access query protocol. This is not a claim that BATCH is legal in the *unchanged* TMR-1 EQ-REC record calculus.

## 2. Exact independent reconstruction of TMR-1/042 and TMR-2/042

TMR-1/042's four-clause ternary equality gadget is \((\neg X_i\lor Y_i\lor U_i)\land(\neg X_i\lor Y_i\lor\neg U_i)\land(X_i\lor\neg Y_i\lor V_i)\land(X_i\lor\neg Y_i\lor\neg V_i)\). Existentially eliminating \(U_i,V_i\) gives exactly \(X_i=Y_i\). Each NAE bridge admits a private third-variable extension for every endpoint assignment, and central NAE(A,B,C) has a witness. Therefore

\[
\exists_{U,V,A,B,C,Z}F_k(X,Y)\ \equiv\ \bigwedge_i(X_i\leftrightarrow Y_i).
\]

TMR-2/042's two signed twins NAE(\(x_i,y_i,z_i\)) and NAE(\(x_i,y_i,\neg z_i\)) existentially reduce to \(x_i\ne y_i\). Every pair-guard admits \(u_{ij}=1-x_i,a_{ij}=0,b_{ij}=1\), regardless of \(x_j\). Hence

\[
\exists_{Z,U,A,B}R_k(X,Y)\ \equiv\ \bigwedge_i(x_i\ne y_i).
\]

Both are \(2^k\)-order permutation matrices with **exact rational rank and 1-rectangle-cover \(2^k\)**, while both source families admit explicit polynomial-time witness construction. TMR-1's source has connected primal width two; TMR-2's has an unpeelable NAE 2-core. Neither property creates a hard SAT family. The independently authored verifier reconstructs *original ternary clause arrays*, rather than assuming matrices, and exhaustively eliminates their private variables for \(F_1,F_2,F_3,R_2\).

## 3. Qualified complete transition model

For public \(k\ge1,s\ge1\), and signed mask \(t\in\{0,1\}^k\), let the immutable hidden input be \(X,Y\in\{0,1\}^k\). Decide the **total both-label predicate**

\[
R_t(X,Y)=\bigwedge_{i=1}^k[Y_i=X_i\oplus t_i].
\]

This is an *ideal adaptive batch-coordinate-source-query system*, not a fixed finite-tape SAT decider, original source-bound proof checker, or EQ-REC authority. Complete configurations retain the immutable hidden source, public parameters, paid-coordinate history/transcript, internal computation/cache, a reversible representation-view bit, and output/terminal flag. Legal transitions are zero-price NOP, reversible VIEW and deterministic COMPUTE using only the public parameters and already read bits; cost-one QUERY(S) for any requested set \(S\) of at most \(s\) source coordinates (repeated reads and sharing allowed); zero-price HALT only if the acquired transcript forces the correct label on **all compatible sources**. All branch obligations to distinguish a positive source from a single-coordinate negative neighbor are retained. No zero step may reveal a previously unread input coordinate.

Authentic zero-price SCCs include the two views of a fixed transcript. Every zero-cost edge preserves the transcript and therefore every component below; one cannot identify distinct nonreversible free compute states as a single SCC. Paid query edges only add source knowledge. Unknown source access in real machines is conservative MAY, not prohibited by this restricted system.

## 4. True *conditional residual* rank and exact seven-column discharge

For a source-consistent transcript let \(r\) be the number of pairs \((X_i,Y_i)\) for which **neither** coordinate has been read, and let \(U\) be the number of unread individual coordinates. After conditioning the *positive-relation* matrix on all observed bits, an untouched pair contributes a rank-two signed permutation and any touched pair contributes a rank-one row, column or singleton. Kronecker rank multiplicativity gives **exact residual matrix rank** \(2^r\).

On a **positive** actual source define

\[
p(C)=(0,0,2^r-1,0,0,0,\lceil U/s\rceil);
\]

on a negative source put all components zero. This is an *analysis* potential allowed to depend on the immutable source label; it is **not** an oracle giving the algorithm its label for free. A correct deterministic adaptive algorithm cannot accept a positive source before reading all \(2k\) coordinates: flipping any unseen coordinate leaves the transcript unchanged but changes the true label. Thus \(p=0\) at every legal completed goal, positive or negative. Authentic free transitions have signed discharge zero.

When a paid QUERY reads \(b\le s\) newly acquired coordinates and first touches \(d\) fully unread pairs, its exact signed component row is

\[
\Delta_{SEP}=2^r-2^{r-d},\qquad
\Delta_{MACHINE}=\lceil U/s\rceil-\lceil(U-b)/s\rceil.
\]

The other five components vanish. All legal query rows satisfy \(0\le d\le \min(s,r)\), \(0\le\Delta_{MACHINE}\le1\) and

\[
\Delta_{SEP}\le D_{k,s}:=2^k-2^{k-\min(k,s)}.
\]

**Both maxima occur on the same legal paid transition:** read \(s\) source bits from distinct untouched pairs if \(s\le k\); for \(k<s<2k\), touch every pair with the \(s\) bits; for \(s\ge2k\), read the whole source. Repeats, rereads, caching, recomputation and false-source events do not overdischarge. Therefore the COMPLETE nonnegative exact two-coordinate tariff cone (other five weights zero) is

\[
\boxed{D_{k,s}\lambda_{SEP}+\lambda_{MACHINE}\le1.}
\]

Necessity is the authentic saturating edge; sufficiency follows for *every* event, including signed zero and free terminal rows. Machine-readable complete rule schema, signed rows and precise scope are in the accompanying tariff JSON.

## 5. Exact rational primal/dual and smallest legal shortcut

Set \(T=\lceil2k/s\rceil\), \(D=D_{k,s}\). The initial-potential LP is

\[
\max_{\lambda_{SEP},\lambda_{MACHINE}\ge0}
[(2^k-1)\lambda_{SEP}+T\lambda_{MACHINE}]
\quad\text{s.t.}\quad D\lambda_{SEP}+\lambda_{MACHINE}\le1.
\]

The **exact integer dual** \(y=T\) satisfies \(Dy\ge2^k-1\) and \(y\ge T\). For \(s<2k\), \(T\ge2\) and \((2^k-1)/D<2\); for \(s\ge2k\), \(T=1,D=2^k-1\). The primal rational witness \((0,1)\) has value \(T\), exactly matching the genuine total algorithm that reads all \(2k\) bits in \(T\) batches and compares them. Consequently

\[
\boxed{\Phi_0^{\max}=W_{\rm worst}=\lceil2k/s\rceil}.
\]

This is only a **linear query cost**, despite exponential initial communication rank.

**Smallest hostile fusion row:** for \(k=2,s=2\), initial \(p_{SEP}=3,p_{MACHINE}=2\). The authentic price-one QUERY(\(X_1,X_2\)) touches both previously unread pairs and has signed discharge \((\Delta_{SEP},\Delta_{MACHINE})=(3,1)\). The old *one-CHECK-per-pair-only* EQ-REC rank weight \(\lambda_{SEP}=1/2\) would charge \(3/2>1\). It therefore **FAILS if transplanted** to this enlarged dual-probe system, but does **not refute** the original restricted EQ-REC tariff (whose legal event inventory differs). The corrected \(k=2,s=2\) cone is \(3\lambda_{SEP}+\lambda_{MACHINE}\le1\). QUERY(\(Y_1,Y_2\)) then completes the positive source in exactly two total paid batches.

## 6. Independent execution and hostile controls

The *exact published V8 function* in \`experiments/tmr/tmr5_dualprobe_rank090.js\` was executed in native V8 before publication. It passed **2,308,451 assertions, zero failures**, enumerated **768,526 authentic paid BATCH edges** through \(k\le6, 1\le s\le\min(4,2k)\), identified 828 saturating rows, independently projected 100 original-source \(X,Y\) combinations from the complete F/R proper-3CNF clauses by brute-force hidden assignment, and tested 62 signed permutation masks. Every paid edge checks the exact-rational certificates \((1/D,0)\), \((1/(2D),1/2)\), and machine-only \((0,1)\), with integer cross multiplication. The original raw JSON was saved without modification. Separately, a *local-only native CPython* verification passed 3,845,510 assertions across the same 768,526 legal edges and independent all-input Bellman minimax for \(k\le3\); this local copy is **not claimed as published repository code**. Finite evidence is COMPUTATIONAL; all-size statements follow from the symbolic proofs.

Mandatory countercontrols: F equality reduces to Krom/2-SAT and its NAE leaves admit witnesses; R signed twins reduce to affine/XOR conditions even though the full source is non-Schaefer, has high treewidth and no NAE leaves. Gaussian elimination, Horn, dual-Horn, autarkies, bounded-treewidth dynamic programming, compact circuits, learning, extensions, variable renaming, padding, sharing, rereads, storage and reconvergence remain legal in a real SAT machine and are not assumed to require exponential time here. A physical multitape model must charge input-head travel, initialization and duplicated input tapes before pricing two arbitrary indexed bits at one step; this *oracle* does not supply that transfer. No CEGAR pruning or prescribed proof DAG is used. Historical \`/341\` is **FAIL** on its full accepted language, \`/386\` **RESTRICTED**; unchanged.

## 7. Ranked dependency map and next peer repair

| Item | Verdict |
| --- | --- |
| TMR-1/042 original equality projection and exact \(2^k\) rank | **PASS/RESTRICTED**, independently algebraically and finitely checked |
| TMR-2/042 original anti-equality projection and exact \(2^k\) rank | **PASS/RESTRICTED**, independently algebraically and finitely checked |
| Authentic transcript zero closure and all-step query tariff | **PASS/PROVED-RESTRICTED**, independent mathematical review OPEN |
| Old one-pair CHECK weight transferred without recalibrating cross-pair BATCH | **FAIL in enlarged model**, real cheapest query retained |
| Exponential raw rank as a source-query time lower bound | **FAIL on these controls**, exact worst-case \(T=\lceil2k/s\rceil\) |
| Finite-alphabet physical machine compilation and all-tape access costs | **OPEN** |
| SAT-machine same-system transfer and superpolynomial initial fusion-safe potential | **OPEN** |
| P versus NP | **OPEN** |

**Weakest surviving lemma:** a dynamic nonaffine fusion obstruction that survives *all* partially acquired source knowledge and cheap algebra/learning while paying for every genuine native physical step. TMR-1/2 should distinguish residual separator rank from unread correctness obligations and audit this query-row; TMR-3 must price input-head positioning, multiple tapes and true simultaneous reads; TMR-4 should replay the exact cone plus zero SCC in a conservative MAY transition system. Next TMR-5 redteam should target a legal signed learned-clause/extension event in a concrete SAT-relevant machine.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Recovered complete original proof1.txt (28,714 characters, SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`), proof2.txt (1,051,196 characters, SHA \`930c5eeddafce656717f28055a7a9a755f44737c\`) and canonical main.tex (2,545,859 characters, SHA \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\`). Read governing and replacement directives, current issue #3, AGENTS.md, CODEX.md, research skill, all five current TMR handoffs, original TMR-1/042 and TMR-2/042 reports/code/raw/matrices, TMR-3/042 and TMR-4/042 original reports and historical Lipschitz safeguards. No root edits or schedule changes.

## Sources (scope-specific, not a SAT lower-bound transfer)

1. TMR-1/042 report and original executable \`research/agents/tmr-1/2026-11-15_0308_TMR1_CONNECTED_TW2_EXPONENTIAL_RANK_TARIFF042.md\`, \`experiments/tmr/tmr1_eqrank_treewidth088.js\`.
2. TMR-2/042 report and original executable \`research/agents/tmr-2/2026-11-15_0312_TMR2_NAE_2CORE_RANK_GAUGE_FIREWALL042.md\`, \`experiments/tmr/tmr2_nae_2core_gauge087.js\`.
3. Goldreich, communication complexity lecture 21, https://www.wisdom.weizmann.ac.il/~oded/PS/CC/all.pdf, identity matrix rank versus deterministic EQ communication \(k+1\). Communication bits are not source queries or physical TM transitions.
4. Samer and Szeider, *A Fixed-Parameter Algorithm for #SAT with Parameter Incidence Treewidth* (2006), https://arxiv.org/abs/cs/0610174.
5. Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978, https://doi.org/10.1145/800133.804350.

**P versus NP OPEN.**