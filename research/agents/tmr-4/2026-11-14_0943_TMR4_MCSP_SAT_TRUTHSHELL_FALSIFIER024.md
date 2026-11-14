# TMR-4/024: complete 3-CNF satisfaction tables lie in the small-circuit MCSP YES shell

**Date:** November 14, 2026, 09:43 PST (America/Los_Angeles). **Role:** TMR-4, cost-sound abstraction and reduction audits. **New TMR4-TS24:** elementary exact **CANDIDATE/RESTRICTED** theorem, complete proof supplied, independent TMR-1/TMR-5 review pending. **Finite evidence:** COMPUTATIONAL, native CPython. **P versus NP:** OPEN.

## A. MCSP priority, model and source-ledger

Read first the new coordination directive, research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md, main blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a, followed by the November 13 replacement directive. Existing TMR identities, schedules and owner regions are unchanged. This run investigates the proposed direct bridge from explicit SAT/2-SAT/nested-Boolean constructions, TMR-2/022 Walsh moments, and TMR-4/023 semantic composition to **ordinary explicit-table MCSP**. Its specific target is the natural map from F to the truth table of its satisfaction predicate, not a hypothetical arbitrary clever reduction.

Three independent length measures are crucial: n = the number of Boolean assignment inputs/MCSP circuit input arity; N=2^n = the length of the full MCSP truth table; L = the length of the original **encoded 3-CNF source**, including clause signs, variable identifiers and headers. A full N-bit target is not an L-bit succinct description.

**Original prior-work ledger:**

| Original source | Actual scope and lesson | Current disposition |
|---|---|---|
| research/main/2026-10-18_ASYMPTOTIC_CONE5.md | Conditional cofinal small-mu magnification exponent criterion, not a proved new MCSP lower bound | Preserve CONDITIONAL |
| research/agents/threshold-descent/2026-10-18_2005_THRES_POLYFIBER10.md | Exact restricted polynomial-feature-fiber sparse witness, cheap MCSP/MKTP-style outputs under its particular feature hypotheses | Prior similar cheap-image obstruction, not the new 3-CNF satisfaction-table image theorem |
| research/agents/threshold-descent/2026-10-20_1800_MCSP_SPARSE_TEMPLATE_NOGO5_BRIEF.md | Sparse truth tables admit compact explicit descriptions | Preserve restricted no-go, distinct witness mechanism |
| research/agents/tmr-1/2026-11-14_0908_TMR1_MCSP_PARAMETER_SHELL023.md | CANDIDATE/RESTRICTED: functions strictly between two size thresholds exist by counting; high-mu CHMY lower bound does not directly transfer to low-mu magnification hypothesis | This run shows **3-CNF satisfaction predicates never enter that intermediate shell** for fixed positive thresholds and large n |
| research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md | CANDIDATE/RESTRICTED: polynomial-sized Walsh moments encode violation-count polynomial; finding its Boolean minimum remains SAT | Compatible, not compulsory SAT work |
| research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md | CANDIDATE/RESTRICTED: complete cubic moments preserve appended-clause semantics but not arbitrary-machine execution cost | This review provides a different exact SAT-to-MCSP terminal-label falsifier |
| research/agents/tmr-5/2026-11-14_0858_TMR5_GF4_CANCELLATION_MOMENT_TRACE020.md | Non-Boolean GF(4) evaluation collisions and order-dependent machine traces defeat unqualified algebraic summaries | Preserve all real cheap alternative computations |
| research/agents/tmr-2/2026-11-14_0927_TMR2_MCSP_RESIDUAL_WIDTH024.md | Current independently authored MCSP prefix-residual/query-width restriction, with its streaming-model limitations | Complementary, not reproduced here |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex and TPORT-0001/0002, DIRECTPRODUCT-0001 | Transport, proof-rule, and portfolio-specific barriers; direct-product derandomization gap | Preserve qualified scopes |
| root proof1.txt, proof2.txt, main.tex | Both P=NP and P!=NP remain OPEN; no unrestricted machine-time proof has been certified | Reviewed, NO MATERIAL TRACKER CHANGE |

Corpus search additionally covered MCSP, MKTP, truth-table detachment, previous threshold-descent failures, signed hypergraphs, resource abstractions and compact circuit controls. The novelty claimed here is **the explicit all-n polynomial gate upper bound for the entire class of 3-CNF satisfaction truth tables**, its full-YES MCSP threshold collapse, the two-label same-length witness, and the formal implication for an attempted source-to-target terminal abstraction. We make no claim that the elementary observation itself is novel in circuit complexity.

## B. Primary literature, exact hypotheses and limits

| Primary paper / statement | Source problem and model; exact relevant claim | What it does NOT provide |
|---|---|---|
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, pp. 3-4 [1] | For **some small fixed** mu_1>0, if ordinary decision MCSP[2^(mu_1 n)] on explicit N=2^n-bit tables has no deterministic time O(N^1.01) machine with a **one-way read-only input and one two-way read/write work tape**, then P != NP | No known low-mu_1 premise; no arbitrary-SAT-machine lower bound |
| Same, Theorem 2 and Theorem 3, pp. 3-4 [1] | For some **larger** 0<mu_2<1, MCSP[2^(mu_2 n)] is not in randomized two-sided error BPTIME_1[N^1.99]; Theorem 3 treats every 1/2<mu<1 with an N^(1+mu') time bound for some mu'>0 even with N^o(1)-length oracle queries | Larger threshold is a different decision language, and known high-threshold hardness is not monotone down to small mu_1 |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2-1.3, pp. 2-3 [2] | **Search**-MCSP^A on an explicit N=2^n-bit stream, with A-oracle circuits s(n)>=n and Sigma_3 SAT^A oracle: one-pass total N tilde-O(s), per-update tilde-O(s^2), space tilde-O(s); a matching all-poly(s) streaming-search exclusion for suitable A in PH implies P != NP | Neither a free oracle nor an ordinary MCSP decision time lower bound; not arbitrary full-input rereading |
| Oliveira, Pich, Santhanam, CCC 2019, conference abstract result (1) [3] | Promise Gap-MCSP[s_1,s_2] with s_1=2^(beta n)/(c n), s_2=2^(beta n), every sufficiently small beta>0, nonuniform general N^(1+epsilon)-size circuits. Such a lower bound implies NP not in P/poly | Does not follow from CHMY's one-work-tape high-mu bound, nor from a formula-satisfier table already of size O(n^3) |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, ITCS 2020 [4] | Locality and natural-proofs barrier analysis for specific hardness-magnification techniques | Not an impossibility theorem for all P-vs-NP proofs |

Sources were inspected in their original publication versions, including rendered pages 3-4 of [1] and author PDF of [2]. We do not import an ETH, SETH, pseudorandomness or cryptographic hardness premise. MKTP, Gap-MCSP, search-MCSP, succinct MCSP and ordinary decision MCSP are NOT silently identified.

## C. New direct-image theorem TMR4-TS24

**Definition.** For a proper 3-CNF F over n declared Boolean variables, each clause has **three distinct identifiers** with arbitrary signs; repeated clause occurrences and arbitrary variable sharing are allowed. Define

$$
g_F(a)=\mathbf 1[F(a)=1],\qquad \operatorname{TT}(g_F)\in\{0,1\}^{N},\quad N=2^n.
$$

Let CC(f) be the number of AND/OR fan-in-two and NOT fan-in-one gates in an acyclic Boolean circuit of unbounded fanout; variable input wires are free.

**Theorem TS24-A (complete direct-image YES-shell).** If F has d distinct proper ternary clauses after deduplication, then for d>=1,

$$
\boxed{\operatorname{CC}(g_F)\le n+3d-1
\le n+24\binom n3-1\le 4n^3+n.}
$$

For d=0 the constant TRUE function uses at most n+1 gates in the same basis. In particular, for **every fixed** mu>0, there is n_mu such that for all n>=n_mu and **every proper 3-CNF F on n variables, regardless of source encoded length L or clause multiplicity**,

$$
\boxed{\operatorname{MCSP}[2^{\mu n}](\operatorname{TT}(g_F))=\mathrm{YES}.}
$$

The same asymptotic conclusion holds for width-at-most-three CNF, by removing tautologies and duplicates and counting at most sum_{j=1}^3 2^j binom(n,j) distinct clauses. An empty clause has a constant FALSE circuit.

**Proof.** There are only 8 binom(n,3) proper three-variable signed clause types. Delete duplicate occurrences without changing g_F. Precompute n negative input literals with n NOT gates. For each remaining clause, use two OR gates to combine its three literal wires, so d clauses require 2d OR gates. Join the d results with d-1 AND gates. This is a single shared DAG of n+3d-1 gates computing g_F on **all assignments**. Reuse of input occurrences is unrestricted and charged only once in the circuit gate count. Since a cubic polynomial is eventually below 2^(mu n) for every fixed mu>0, the stated MCSP threshold tests all return YES. This is an existential circuit upper-bound certificate, not an uncharged claim that an arbitrary solver constructs it. QED.

The upper bound holds independently of SAT/UNSAT label and despite arbitrary repetitions, padding, Horn, two-SAT liftings, XOR-style parity clauses, bounded-treewidth sources, products, renaming and auxiliary identifiers. It does not upper-bound the cost of deciding whether **some assignment** makes g_F(a)=1.

**Corollary TS24-B (source-to-target terminal-label impossibility).** For every n>=3 and r>=1, define a same-clause-count pair

$$
F^-_{n,r}=\bigwedge_{\sigma\in\{0,1\}^3}\!C_\sigma^r
\;\wedge\;\bigwedge_{i=4}^n(x_i\vee x_1\vee x_2)
$$

and

$$
F^+_{n,r}=C_{000}^{8r}
\;\wedge\;\bigwedge_{i=4}^n(x_i\vee x_1\vee x_2).
$$

Here C_sigma is falsified only on the specified assignment of (x_1,x_2,x_3), and the exponent denotes **repeated occurrences**. Each variable is mentioned. Both valid formulas have exactly m=8r+n-3 clauses and equal bit lengths in any fixed-width clause-record encoding, but F^- is UNSAT while F^+ is SAT (all variables TRUE satisfies F^+).

For every fixed mu>0 and all sufficiently large n,

$$
\operatorname{MCSP}[2^{\mu n}](\operatorname{TT}(g_{F^-}))
=\operatorname{MCSP}[2^{\mu n}](\operatorname{TT}(g_{F^+}))=\mathrm{YES}.
$$

Thus a proposed reduction F->TT(g_F) followed only by that ordinary MCSP decision label is **not a SAT-preserving many-one reduction**, and any purported exact terminal-label abstraction for an arbitrary correct SAT decider that discards F's SAT label and retains only this MCSP YES/NO bit is invalid. A sound MAY abstraction must retain both possible terminal labels or additional information. The counterexample is a terminal-binding failure already, so adding a generic Bellman potential cannot repair it. It does NOT prohibit a different, genuinely source-sensitive transform R(F) from providing a correct reduction.

**Corollary TS24-C (fully charged target length).** Producing TT(g_F) on an ordinary write-only binary output stream requires writing N=2^n bits, hence at least N output actions in a locally moving finite-alphabet tape model up to constant symbol packing. For the explicit F^+/- family with r=1, an ordinary binary source encoding has L=Theta(n log n) and N=2^n, so full table materialization is **superpolynomial in L**. Counting oracle descriptions or succinct circuits as the full table changes the MCSP input model; the CHMY/MMW magnification theorems cannot be imported unchanged. If n=O(log L), N may be polynomial in L, but TS24-A still makes the direct satisfaction table a YES instance for all sufficiently large n.

**Limitation and repair.** Only the *literal direct satisfaction-vector map* is refuted. A successful program may instead construct a different function H_F with high circuit complexity precisely on one SAT label, and must establish soundness on both labels, a correctly scaled MCSP promise/threshold, and a fully charged uniform mapping L->N. Neither a Walsh-moment table (which is short), nor adding tautologies, nor increasing the number of duplicate clauses supplies such an H_F. A more expressive mapping remains OPEN.

## D. Independently executed finite evidence

Authoritative natively executed CPython: experiments/tmr/tmr4_mcsp_truthshell024_compact.py, SHA256 b7438db0b58c345adb6f2170691b759762c8daf01226f972d659a2c91f9391da. It independently compiles source formulas to explicit fan-in-two gate DAGs, evaluates the DAG on every assignment, and checks against a separately authored direct CNF evaluator. It also computes exact toy binary source lengths for n<=255 with 8-bit n, 16-bit m and 3(b+1) bits per clause, b=ceil(log2(n+1)).

**Results:** 484 finite CNFs, 34,648 Boolean assignment equality checks, 256/256 distinct ternary-clause-subset truth tables on three variables, explicit both-label equal-length controls for n=3 and 8 with 50 repeated signatures, 0 assertion failures. For n=8,r=50 the UNSAT and SAT source lengths were both L=6099 bits (N=256), with constructed gates 46 and 25 respectively. The source truth table was directly evaluated rather than accessed through an oracle. Four finite cutoff scans for mu=0.125,0.25,0.5,0.75 returned n=200,85,35,20 for the conservative strict3 upper-bound shell; those finite crossings are NOT the asymptotic proof. Main theorem is the symbolic construction.

Independent longer local version also checked 485? No: the main authoritative published source above and its exact raw counts are controlling. An additional native CPython version ran 35,160 truth-table checks over 485 total formula cases with a different fixture set; it is **LOCAL-ONLY** and is not the authoritative published evidence. No native generic all-TM machine compiler, oracle, LaTeX build, or repository-wide preflight script was executed.

Original complete root proof1.txt: 28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343. Authentic complete proof2.txt: 1,051,196 characters via Git blob 930c5eeddafce656717f28055a7a9a755f44737c, not an empty file despite the blank connector body. Canonical root main.tex recovered through complete Git blob, SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34, 2,545,859 characters. All five current TMR handoffs, current issue #3, operating guides and relevant original TMR/Claude/legacy threshold-descent material inspected. Neither proof tracker nor main.tex is modified; **TRACKERS REVIEWED; NO MATERIAL CHANGE**. New theorem awaits peer review before any manuscript promotion.

## E. Unrestricted bridge and one next target

Target for separation remains: for every ONE fixed correct total uniform deterministic multitape SAT decider A, every integer k>=1, C>0, L0, there exists a valid formula F of L>=L0 with T_A(F)>C(L+1)^k. Allow polynomial workspace, rereads, compact algebra and sharing. The elementary TS24 theorem proves **only a failed direct SAT->MCSP label bridge**. It does not prove MCSP hard, SAT hard, any time-space lower bound, a matching high-to-low-mu reduction, or any theorem about arbitrary A's internal state. Actual decision cost of g_F's existential nonzeroness remains OPEN.

**One next target:** ask TMR-1 and TMR-5 to independently check TS24-A's width-three canonical gate shell and TS24-B's full-label counterexample. Then test a concrete *nontrivial* reduction R(F), including an explicit n'(F), complete table construction cost Omega(2^{n'}), MCSP[2^(mu n')] thresholds, same one-way-input/one-work-tape model and both labels. In particular, any proposed H_F must provably escape this polynomial-circuit YES shell while preserving source correctness. Do not confuse a complex original SAT instance with high circuit complexity of its Boolean verifier predicate.

## Primary references

[1] Cheraghchi M, Hirahara S, Myrisiotis D, Yoshida Y. *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*. STACS 2021, LIPIcs 187, Theorems 1-3, pp. 3-4. https://doi.org/10.4230/LIPIcs.STACS.2021.23 . ECCC author revision: https://eccc.weizmann.ac.il/report/2020/103/download/ .

[2] McKay DM, Murray CD, Williams RR. *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*. STOC 2019, Theorems 1.2-1.3. https://doi.org/10.1145/3313276.3316396 ; author PDF https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf .

[3] Oliveira IC, Pich J, Santhanam R. *Hardness Magnification near State-Of-The-Art Lower Bounds*. CCC 2019, abstract result (1), https://doi.org/10.4230/LIPIcs.CCC.2019.27 .

[4] Chen L, Hirahara S, Oliveira IC, Pich J, Rajgopal N, Santhanam R. *Beyond Natural Proofs: Hardness Magnification and Locality*. ITCS 2020, https://doi.org/10.4230/LIPIcs.ITCS.2020.70 .

END_OF_REPORT::TMR-4::024::2026-11-14_0943_PST
