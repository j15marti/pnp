# TMR-4/019: locally certified mirror-tape erasure beyond all-symbol congruence

**America/Los_Angeles:** November 14, 2026, 04:47 PST. **Owner:** TMR-4, new Cost-Sound Abstraction agent. **Mathematical status:** CANDIDATE/RESTRICTED, explicit proof below, independent TMR-1/TMR-5 review requested. **Experiments:** COMPUTATIONAL. **P versus NP:** OPEN.

## 1. Substantive incremental result

TMR-4/018 gives an effective *universal-symbol* strong-congruence test for erasing writable alphabet information. This run constructs a **strictly more permissive, yet mechanically certifiable, inductive relational quotient**. A bit on a first work tape may actually govern an expensive gate, so erasing it fails the universal-symbol criterion, but its value is deterministically recoverable from a separately retained, exactly mirrored second work tape. The erasure is cost-exact **on every actual run** when the tape-equality invariant and every real transition are checked. A minimal off-invariant counterexample shows why the stronger theorem needs the invariant rather than unconstrained MAY choices.

The result extends conservative exact abstraction methods for **given** finite-machine programs. It does not force an arbitrary 3-SAT machine to maintain duplicated tapes, nor yield a superpolynomial SAT lower bound.

## 2. The certified inductive-tape-erasure theorem

Fix one finite total deterministic multitape machine $A$, serving all binary source lengths, a fixed immutable input $x$ of encoded length $L$, a finite control, locally moving original input and work heads, fixed finite work alphabets, and terminal labels SAT, UNSAT, MALFORMED. Every real transition costs one. For each work tape count all visited writable cells, regardless of whether a symbol is later erased. No algorithm-specific advice or oracle is allowed.

Consider designated writable tapes $B,C$ with identical alphabet (including physical blank), initially identical on every cell, aligned heads, and matching visited footprints. Define the global *mirroring invariant* $I$ by:

1. The complete content of $B$ equals that of $C$ cellwise.
2. Their work heads have identical positions.
3. The remaining source, control, heads, tapes and visited-cell footprints have their original concrete values.

An effective sufficient certificate checks **each control state, each input-symbol vector, each other work-symbol tuple and each diagonal pair $(b,b)$**, without requiring execution reachability. It requires that both heads move identically and both writes are equal, and that both terminal labels are represented faithfully. Unreachable off-diagonal symbol pairs $(b,c)$ with $b\ne c$ need not satisfy the criterion. If the program has other control or tape components, their original transitions and costs are retained, including any read from $B$ that selects a branch.

Let $\pi_I$ erase the symbol *content* of $B$ but retain its physical dummy head and visited-cell footprint, retaining $C$ exactly. Define an abstract source-bound machine $\widehat A$ by replacing all reads of $B$ in the finite transition table by the corresponding read of $C$ while on the certified diagonal. The abstract machine performs the same cost-one step and the same physical head movements; writes to the dummy tape may use the fixed abstract blank.

**Theorem IM19 (candidate, scoped):** When the stated finite certificate holds, every initial concrete configuration belongs to $I$; every concrete transition from a configuration in $I$ stays in $I$; and each such step has a unique cost-one abstract transition with

$$
\pi_I(\delta_A(c))=\delta_{\widehat A}(\pi_I(c)).
$$

Conversely, each abstract transition from a related state replays from every related concrete state within $I$. By induction, all real computations, their physical source rereads, control/other work contents, both SAT/UNSAT terminal labels and MALFORMED labels, original head trajectories and visited writable cell sets are preserved. Consequently, for every input and one fixed machine,

$$
T_{\widehat A}(x)=T_A(x),\qquad S_{\widehat A}(x)=S_A(x).
$$

The space equality counts the abstract *dummy physical work tape*. Removing that physical tape rather than only its information would require a separate charged implementation and need not preserve identical visited-cell counts.

**Proof:** At the blank initial state the two full tape functions and heads agree, hence $I$. Suppose $I$ holds. The two scanned letters coincide because heads and cell contents coincide. The finite diagonal-transition certificate guarantees equal next writes and equal head displacements; all unscanned cells remain equal. Therefore $I$ is inductive. As each current $B$ letter is exactly the retained $C$ letter, it is uniquely determined by the abstract configuration. On diagonal states the concrete and abstract transition tables choose exactly the same action, next control, output label, original input movement, other-tape writes and dummy-head displacement. The commuting square follows. Uniqueness of a concrete representative's erased content within $I$ yields reverse exact replay. Induction over the finite halting execution gives equal terminal result, transition count and visited-cell sets. This is stronger than existential forward simulation and is exact for this syntactic class. QED, subject to independent peer audit.

**Coverage and certification boundary:** The diagonal checks are finite because the machine has finite control and finite alphabets; they concern all symbol combinations in the finite transition table, not all input lengths or an uncomputable global reachability set. They apply only when two work tapes are genuinely mirrored by all transitions on $I$. An arbitrary machine's complex semantic equality, moving shared encoding or changing work-tape layout may lack such a finite local certificate. This is consistent with TMR-4/017's undecidability of complete all-input cost-inert register erasure.

## 3. Nontrivial all-length physical controller

A restricted proper 3-CNF sign stream contains successive triples of bits, each triple identifying one clause over the three distinct variables $x_1,x_2,x_3$; its triple denotes the assignment the clause forbids. A finite controller marks the eight excluded assignments in an eight-bit control mask. At the end, an incomplete triple is MALFORMED, all eight assignments excluded means UNSAT, and otherwise the formula is SAT. This is a regular restricted language, not an NP-complete encoding of unrestricted 3-SAT.

Before that classifier, a fixed one-input-head controller scans the source rightward, updating a writable parity bit $b$ on tape $B$ and an equal bit $c$ on tape $C$ on each current-cell observation of a 1. The heads of $B,C$ are physically positioned at visited cell zero throughout, and both are written in the same transition. It returns the actual input head to the left marker, takes an extra outward-and-return physical roundtrip **iff $b=1$**, and finally classifies the source by rereading its original cells. Both bits start at their physical blank symbol 0.

The physical gate reads $b$. The proposed quotient deletes the *value* of $B$ and reads $c$ at that gate. Universal-symbol WSQ18 rejects the erasure because the gate gives different actions on the off-diagonal work-symbol pair $b=1,c=0$. The new invariant certificate succeeds: every reachable tape pair is diagonal, including at the gate. The erased bit is operationally recoverable, not computationally or informationally independent. This is a genuine cost-relevant bit erasure that was excluded by the predecessor's all-symbol check.

Let $q=L+1$ be the number of physical head movements from left endmarker to right endmarker, and $z(x)=\bigoplus_{i=1}^L x_i$. The concrete and refined quotient runtime, including the final terminal transition, is exactly

$$
T(x)=3q+1+2qz(x),\qquad S(x)=2.
$$

In particular, the two fixed-mirror-tape machine uses no free source lookahead, answer lookup or SAT oracle. Its only source symbol read at each transition is the symbol under the original physical input head. The work-tape equality is not obtained by assuming SAT hardness.

## 4. Full abstract-edge potential and hostile counterexample

For this controller, the source-aware inductive abstract-state domain includes the complete source $x$, exact input-head position $p$, retained $c$, classifier mask/pending bits and phases $S$ (outward scan), $R$ (return), $D/E$ (optional extra outward/return), $A$ (classification) and $H$ (terminal). It keeps precisely the states satisfying the proved source consistency: in $S$ at $p$, $c$ is the parity of the data cells already scanned, namely $x_1,\ldots,x_{p-1}$; in every later phase $c=z(x)$. These are inductive *proof predicates*, not zero-cost operations performed by the running machine. Every actual execution is included.

For every abstract edge in this explicitly restricted source-consistent graph, define

$$
\begin{aligned}
\Phi(S,p)&=3q-p+1+2qz(x),\\
\Phi(R,p)&=p+q+1+2qz(x),\\
\Phi(D,p)&=3q-p+1,\quad
\Phi(E,p)=p+q+1,\\
\Phi(A,p)&=q-p+1,\quad
\Phi(H)=0.
\end{aligned}
$$

Every edge has cost one and satisfies **equality** $\Phi(a)=1+\Phi(a')$, including the parity-dependent return gate. The boundary checks are: from $S,q-1$ to $R,q$, both potentials differ by one; from $R,1$ to $A,0$ on even sources, they differ by one; from $R,1$ to $D,0$ on odd sources, $\Phi(R,1)=3q+2=1+\Phi(D,0)$; from $D,q-1$ to $E,q$, from $E,1$ to $A,0$, and from $A,q$ to $H$, each difference is one. Ordinary local head moves also decrease $\Phi$ by one. Thus $\Phi(H)=0$ and the all-edge Bellman condition is proved. Initial value is exactly $3q+1+2qz(x)$.

The use of $z(x)$ in the *mathematical certificate* must not be mistaken for a free parity oracle for a new SAT algorithm. Its input parity can be computed by the paid scan already present. Moreover this potential is only linear in encoded length and gives no universal superpolynomial lower bound.

**Minimal failed unconditional erasure:** At return gate with physical head $p=1$, work cells $b=1,c=0$, the concrete transition chooses detour $D$ but the erased transition depending on $c$ chooses classifier $A$. These physical configurations are outside $I$. An unconstrained MAY quotient forgetting $b$ must allow both. On odd sources, its cheap $A$ branch is not replayable and understates actual time by exactly $2(L+1)$. This is a legitimate source-bound refinement because the discarded off-diagonal branch is proved unreachable by a complete inductive invariant. Unlike historical checker witnesses, no genuine accepted concrete execution is deleted.

## 5. Executed tests and precisely stated limits

**Hosted V8 directly executed source, published in self-contained Node-compatible form:** 4,139 source strings, all 4,095 binary inputs of length 0 through 11 plus 44 deterministic longer controls. SAT 626, UNSAT 1, MALFORMED 3,512, parity-even 2,069, parity-odd 2,070. The evaluator performed **194,952 concrete paid transitions and 194,952 matched abstract transitions**, with **194,952 current-cell observations**, 194,952 checked Bellman equalities, zero assertion failures and exact $S=2$ in each run. It found eight on-diagonal gate symbol cases and eight off-diagonal gate counterexamples. The unconstrained MAY abstraction would admit 2,070 unreplayable cheap detours, understating 47,752 physical transitions in aggregate. It explicitly tested the all-eight-clause UNSAT control, a four-clause signed XOR-pattern control, many duplicate clause products, malformed-length inputs and long rereads.

**Independently authored local-only CPython implementation:** Ran exhaustive length 0..11 and 44 *different* longer controls; 4,139 inputs, 195,738 charged concrete and abstract transitions, SAT 607, UNSAT 20, MALFORMED 3,512; 2,076 odd-source MAY shortcuts omit 48,538 transitions; zero failures. Its exact code/raw remain local-only, so these counts are supporting independent COMPUTATIONAL evidence, not shared reproducible evidence. It is not a wrapper around the hosted JS. The two evidence totals differ because their longer fixture lists differ.

Published and reproducible shared artifacts:
- [Self-contained executable](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr4_inductive_mirror019.cjs), executed as a V8 function and serialized to a Node-compatible script; not natively run under Node.
- [Raw hosted V8 evidence](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0444_TMR4_INDUCTIVE_MIRROR019_RAW.json).

The arbitrary-machine certificate is a symbolic finite-transition-table construction, not a compiled universal TM simulator. Horn, 2-SAT, unrestricted GF(2), bounded-treewidth DP, disjoint product and auxiliary-variable cases were not run as physical arbitrary-3SAT machines. They are allowed by the general machine model, but this restricted classifier does not establish any lower bound against them. Reencoding, caching, sharing, preprocessing and arbitrary polynomial writable workspace remain admissible. Finite evidence is COMPUTATIONAL.

## 6. Literature, original historical results, corpus and reconciliation

Primary results checked against original publication records:
1. Patrick and Radhia Cousot, *Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints*, POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973. Classical approximation/fixpoints, not a uniform SAT lower bound.
2. Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu and Helmut Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15. Spurious-path replay/refinement methods, not proof that a particular abstract path is spurious without concrete source audit.

Original, materially relevant project documents read: TMR-4/018 work-symbol quotient and physical executable; TMR-1/017 finite-control quotient; TMR-4/017 undecidable all-input erasure; TMR-5/015 source-read correction; original historical LSPV-5/514 edge-suffix normalizer (pinned recovered /341 checker only) and LSPV-5/523 independently confirmed literal-order cost alias. The latter is an actually checker-accepted packet, NOT an abstractly spurious trace. Historical evidence is preserved without promotion to a theorem about unrestricted machines. Other legacy R_mix341 cases are not an ownership priority.

Authoritative directive: research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md, initial and pre-publication SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Full proof1.txt received, 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343. Complete proof2.txt recovered through Git blob, 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c, because the ordinary contents endpoint returned blank despite nonempty blob. Complete canonical main.tex reviewed through current Git blob SHA 91b4e582c16cb7f60c9aa1ea2aebf09cd4caa2c6, 2,530,965 characters. AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, five newest TMR handoffs and issue #3 through TMR-2/018 were reviewed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root main.tex edit: whole-document synthesis is TMR-5's responsibility unless an authorized TMR-4 region is confirmed. No schedules created, revived or modified. No full generic compiler, LaTeX compilation, or repository preflight OS script was executed. All existing OPEN load-bearing arrows remain OPEN.

## 7. Single next target

TMR-5/TMR-1 should independently verify the all-state *diagonal transition* certificate and the ordinary-machine implementation's charged dummy-tape footprint, including the odd-source gate and all Bellman edges. Then seek proof-carrying finite relational invariants for movable, shared, multiply indexed work-tape representations; distinguish a true theorem for each supplied certificate from any claim that certificates exist for all correct SAT deciders. Neither P=NP nor P!=NP follows from this result.

END_OF_REPORT::TMR-4::019::2026-11-14_0447_PST
