# TMR-5/033: Fixed-source paid-envelope audit and exact three-component tariff

**2026-11-14 21:51 PST | FIXSRC061/FIXSRC062 | PNP Machine Bottleneck Redteam**

**Scientific status:** PROVED/RESTRICTED for the exact hidden-source AND-of-ORs query system, with a complete symbolic proof below and independent executed small-instance tests. The new fixed-source strengthening and three-column tariff are pending independent mathematical peer review. Finite tests are COMPUTATIONAL. Unrestricted same-machine transfer, superpolynomial initial potential, and P versus NP remain OPEN.

## 1. Candidate and predeclared falsifiers

**Claim:** The paid Bellman-envelope theorem in TMR-4/037 survives retaining a single immutable source throughout each trace, but its value changes at intermediate transcripts. This produces a genuinely source-aware obstruction and an exact three-column tariff. It still cannot certify the known worst-case decision-tree cost at the initial state.

Falsifiers fixed before corpus/source review:

1. A paid read from a single fixed source violates the source-aware unit tariff or terminal condition.
2. The source-forgetting MAY envelope is incorrectly interpreted as the same-source envelope; an authentic transcript shows strict inequality.
3. A public equality, affine summary, or compact gate makes a certificate cheaper than the selected independent-bit interface permits.
4. An adaptive input adversary is incorrectly treated as one fixed all-length SAT hard family or as a free source reply controlled by the algorithm.

## 2. Prior-work and primary-source ledger

**Controlling directive:** research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, verified Git blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. All five current TMR identities and schedules retained. The 2026-11-13 TMR replacement directive, AGENTS.md, CODEX.md, research skill, both proof trackers, current issue #3, all current TMR handoffs, and original relevant TMR-2/036, TMR-4/037, TMR-1/036, TMR-3/036, TMR-5/032 reports/code/results were inspected.

**Existing results, not claimed as new:** TMR-2/036 proved that the worst-case deterministic adaptive query complexity of the public AND-of-q OR-of-q function is q squared, that the best compatible certificate cost is q initially, and that the exact two-column tariff is lambda_B+(q squared-q+1)lambda_W <= 1. TMR-4/037 proved the greatest paid cost-consistent minorant E_f on any finite nonnegative-cost graph, and showed E_W=B on the source-forgetting MAY query graph. The October LSPV-3/076 predecessor already separated worst-case decision depth from certificate cost. TMR-1/036 and TMR-3/036 showed why authenticated affine/Tseitin SAT computations can evade native Resolution proof-size measures and why physical machine transfers require independent proof. TMR-5/032 independently falsified a length-independent fusion tariff under an authentic additional paid operation.

**Methodological primary literature checked, no theorem silently imported:** P. Cousot and R. Cousot (1977), *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL pp. 238-252, DOI https://doi.org/10.1145/512950.512973, supplies the abstract-interpretation setting but no cost theorem is borrowed. N. Nisan (1991), *CREW PRAMs and Decision Trees*, SIAM J. Comput. 20(6), 999-1007, DOI https://doi.org/10.1137/0220062, supplies background on decision-tree model separations; the particular q-by-q claim is proved below. E. Ben-Sasson and A. Wigderson (2001), *Short Proofs Are Narrow*, JACM 48(2), 149-169, DOI https://doi.org/10.1145/375827.375835, is retained only for the unrelated ordinary-Resolution expander control, not transferred to this oracle.

**Genuinely new relative to TMR-2/036 and TMR-4/037:** an exact Bellman-envelope formula with one immutable source x, the identity E_W^MAY=min_x E_W^x, the sharp factor-q intermediate-state loss due to forgetting x, the exact three-component (B,W,D_x) tariff cone and optimum, an explicit witness that B may rise after a paid read, and the quantified max-min versus min-max separation. These are exact restricted consequences, not claims about arbitrary SAT machines.

## 3. Qualified state system and source-retention requirement

Fix integer q>=1 and m=q^2. The complete source is one immutable binary vector x in {0,1}^m. Its Boolean predicate is

$$
f_q(x)=\bigwedge_{r=1}^{q}\left(\bigvee_{j=1}^{q}x_{rj}\right).
$$

The concrete configuration is C=(q,x,sigma,tau,halt), where sigma belongs to {?,0,1}^m, each observed coordinate equals the actual x coordinate, tau is a redundant tag, and halt is permitted only when the observed partial transcript already forces the correct value for **every** completion. A paid READ(i) reveals the actual fixed bit x_i, costs one and changes one unknown transcript coordinate; optional free tag flips or free repeats of a cached observation do not alter sigma; a paid NOP leaves it unchanged. Both TRUE and FALSE completed goals have zero residual obstructions. No choice of source answer, formula-syntax inspection, free parity extension, or advice is allowed within this **restricted** protocol. All of those are MAY operations at the unrestricted SAT transfer gate.

A transcript has forced FALSE if one row has q observed zeros, and forced TRUE if all q rows have an observed one. Let A(sigma) be the rows without any observed one and u_r(sigma) the number of unread fields of active row r. On an undecided sigma define

$$
W(\sigma)=\sum_{r\in A}u_r,\qquad
B(\sigma)=\min\left(|A|,\min_{r\in A}u_r\right).
$$

At a completed goal set W=B=0. These are the peer's worst-case and compatible-certificate components.

**New source-fixed component:** for a transcript sigma consistent with the *same fixed* source x, put

$$
D_x(\sigma)=
\begin{cases}
|A(\sigma)|,& f_q(x)=1,\\
\min\{u_r(\sigma):r\in A(\sigma),\ x_{r1}=\cdots=x_{rq}=0\},& f_q(x)=0,
\end{cases}
$$

and D_x=0 at terminals. For a FALSE source, the minimization set is nonempty, and all such rows are active unless the goal is already forced. D_x is the shortest remaining number of **source-consistent** paid observations if the path selector is allowed to know x. It is a lower bound on the query cost of any actual correct algorithm on that source, not a uniform algorithm with free access to x.

## 4. The fixed-source Bellman-envelope theorem

For a complete concrete graph G_x, every legal READ reveals its unique actual bit x_i. Let

$$
E_W^x(\sigma)=\min_{\pi:\sigma\to^*\sigma'}\left(\operatorname{price}(\pi)+W(\sigma')\right),
$$

with the empty path allowed and all authentic paid and zero-cost operations included. Then, for every q, x, and compatible transcript,

$$
\boxed{E_W^x(\sigma)=D_x(\sigma).}
$$

**Proof:** For a source TRUE, any forcing certificate must read a positive bit in each currently active row and therefore requires at least |A| reads; exactly this many sufficient coordinates exist in the fixed x. For source FALSE, forcing FALSE requires reading all remaining bits of some actual all-zero row; exactly min u_r such bits suffice. No opposite-label transcript can be forced while staying consistent with x. This proves D_x equals the minimum terminal-reaching path cost.

For each legal READ sigma->sigma', an optimal terminal path from sigma' may be prefixed by the read, yielding D_x(sigma)<=1+D_x(sigma'). Every free TAG/cached-repetition step leaves D_x unchanged. Moreover 0<=D_x<=W, and D_x(goal)=0. Hence D_x<=cost(path)+W(endpoint) along every path, so D_x<=E_W^x. Conversely a genuine shortest source-consistent certificate path to a completed terminal costs D_x, where W=0, so E_W^x<=D_x. QED.

This result is an exact all-step tariff for the selected fixed-source graph. It does not require free source-bit knowledge to execute any algorithm; the existence of an optimistic path is used only to bound what an all-edge potential can claim.

## 5. Source-forgetting MAY envelope, sharp error, and nonmonotone B

The MAY graph obtained by forgetting x permits both answer edges for every unread coordinate. Every finite transcript path is compatible with at least one fixed total source. Consequently,

$$
\boxed{E_W^{MAY}(\sigma)=\min_{x\succeq\sigma}E_W^x(\sigma)
=\min_{x\succeq\sigma}D_x(\sigma)=B(\sigma).}
$$

The last equality follows by completing the unknown coordinates to force TRUE with one positive value in each active row, or to force FALSE by completing one active row with zeros. The cheapest such completion costs B. This independently verifies TMR-4/037 **at its original MAY scope** while identifying the information discarded by its abstraction.

**Sharp source-retention gap:** for every q>=2, observe q-1 zeros in the first row but leave its last coordinate unobserved; let the fixed source's last coordinate there be ONE, and let a second completely unread row contain q actual zeros. Then B=1 because a different compatible source could finish the first row with zero, whereas the actual FALSE source requires q reads of the second row. Thus D_x=q and B=1. Since every fixed source always has a terminal certificate of at most q additional reads, and B>=1 on undecided states,

$$
\boxed{\max_{x,\sigma:\,\sigma\text{ undecided and consistent}} D_x(\sigma)/B(\sigma)=q.}
$$

The bound is attained and is therefore exact. At the completely unread initial state, however, for **every** fixed x,

$$
D_x(?^m)=B(?^m)=q,\quad W(?^m)=q^2.
$$

Source retention repairs an intermediate-state loss but **does not raise the initial lower bound**.

**New hostile control:** B need not be monotone under a paid read. With q=3, sigma=(?00,???,???), the TRUE-compatible minimal certificate has B=1. If the first missing bit really equals one and it is read, row one becomes satisfied and B becomes 2; hence Delta_B=-1. This is legal and not a spurious CEGAR artifact. Local tariff soundness needs an **upper bound on discharge**, not a false requirement that every component always decreases.

## 6. Exact all-source, three-column nonnegative tariff cone

Use reduced-product vector (B,W,D_x) and tariff weights lambda_B,lambda_W,lambda_D>=0. For any genuine paid READ:

- Delta_B<=1 (but may be negative).
- 0<=Delta_D<=1.
- 0<=Delta_W<=D_q, where D_q=q^2-q+1.

For the last bound, a nonterminal READ that does not finish has Delta_W at most q by clearing one active row on a read-one, or one on a read-zero. If a read-zero finally refutes a row, the pre-read state has only one unknown bit there and at most q-1 other active rows of q unknown bits each, so Delta_W<=1+(q-1)q=D_q. At the authentic state with q-1 observed zeros in one row, all other fields unread, and the actual final source bit also ZERO, the last paid read yields

$$
(\Delta B,\Delta W,\Delta D_x)=(1,D_q,1)
$$

at cost one. This single row proves necessity; the component upper bounds prove sufficiency. Thus the **complete tariff cone across all actual source strings and transcripts** is

$$
\boxed{\lambda_B+D_q\lambda_W+\lambda_D\le1,\qquad
\lambda_B,\lambda_W,\lambda_D\ge0.}
$$

Free TAG or cached reread edges have zero discharge, and every completed goal has potential zero. The initial value is

$$
\Phi_0=q(\lambda_B+\lambda_D)+q^2\lambda_W.
$$

Its exact maximum over the cone is

$$
\boxed{\max\Phi_0
=\max\left(q,\frac{q^2}{q^2-q+1}\right)=q.}
$$

With **length-independent** nonnegative weights valid for all q, lambda_W must be zero, and lambda_B+lambda_D<=1. Source awareness alone therefore cannot rescue q^2 as a deterministic all-edge Lipschitz potential, much less produce a superpolynomial initial potential.

The exact rule matrix is given in the separate FIXSRC062 JSON and the raw all-edge exhaustive q<=3 execution. This symbolic all-q derivation is the proof; the enumeration is a finite audit.

## 7. Quantifier-order theorem: adversarial decision depth is not a path tariff

Let A range over deterministic correct coordinate-query decision trees for this one q, and Q_A(x) count paid distinct reads. Then

$$
\boxed{\max_x\min_{A\text{ correct}}Q_A(x)=q,\qquad
\min_{A\text{ correct}}\max_xQ_A(x)=q^2.}
$$

**Proof of first equality:** Every correct protocol must inspect a certificate: on a TRUE source one observed positive bit per row, and on a FALSE source all q zeros of some row. Thus Q_A(x)>=q. For any preselected x, tailor a decision tree to query precisely one such size-q certificate first, verify its observed values, and run a fully correct fallback otherwise. The resulting tree is correct on all x and uses q reads on that preselected x. The choice of tree depends on x and is nonuniform in this minimum; it is **not** one algorithm for all x or lengths.

**Proof of second equality:** An adversary against any deterministic query policy answers zero to the first q-1 previously unread fields queried in each row, then answers one at the last field of that row. No row becomes all observed zero, so the algorithm cannot output FALSE. No row yields an observed one before all its q fields have been read, so it cannot output TRUE until all q^2 coordinates have been read. The completed adaptive transcript specifies a single consistent TRUE input x, providing the required x for that algorithm. Reading every bit is a matching upper bound. QED.

This is a legitimate forall-algorithm exists-input **restricted query** lower bound. Its adversarial quantifier does not itself transfer to syntax-aware encoded SAT input. Ordinary SAT algorithms may examine formula structure, use Gaussian elimination or learning, and maintain arbitrary polynomial workspace.

## 8. Native executions, audit details, and hostile controls

**Independent native CPython implementation** (local source and raw captured, not yet a GitHub byte-for-byte replay): 1,779,307 assertions, zero failures, exhaustive q=1..3 over 4^m source/transcript pairs, source-fixed shortest-path and paid-envelope recurrences, all fixed-source edges, and q=2..8 sharp witnesses. Executed in one bounded chunk, with deterministic controls. No SMT or Turing-machine compiler was invoked.

**Independently authored V8 implementations, published exactly as executed:** FIXSRC061 verified 2,750,268 checks, zero failures, including 262,144 source/transcript pairs, all 19,683 compatible q=3 abstract transcripts, and 970,578 q=3 fixed-source READ edges; it independently reconstructed fixed-source terminal shortest paths and paid Bellman envelopes. FIXSRC062 separately checked all 971,004 legal paid READ edges for q=1..3, the three-column discharge bounds, the simultaneous saturating edge, and the exact initial LP extreme-point objective; zero failures. The q=3 admissible minima include Delta_B=-1, demonstrating a real increase.

Published:
- experiments/tmr/tmr5_fixed_source_envelope061.js
- results/raw/tmr/2026-11-14_2151_TMR5_FIXSRC061_V8_RAW.json
- experiments/tmr/tmr5_fixed_source_tariff062.js
- results/raw/tmr/2026-11-14_2151_TMR5_FIXSRC062_V8_TARIFF.json

**Model-changing controls:** A public promise that all q^2 source bits are equal makes one paid read sufficient, so it cannot be ignored when expanding the actual transition system. An authenticated algebraic or compact circuit description of the source also changes what information is already available. A syntactically positive CNF is trivially satisfiable as SAT even though evaluating an unrelated hidden AND-of-ORs assignment may take q^2 black-box reads. Reading formula syntax, adaptive preprocessing, learning, and caching are authentic unrestricted-machine operations and MUST NOT be erased by refinement. No prescribed proof DAG, /341, or /386 is used.

## 9. Integrated ranked dependency verdict

| Priority | Claim/arrow | Verdict and precise scope |
|---|---|---|
| 1 | TMR-4/037 general paid Bellman-envelope greatest-minorant theorem | PASS/RESTRICTED, independently rederived for finite nonnegative graphs; no full SAT transfer |
| 2 | TMR-4/037 E_W^MAY=B and TMR-2/036 B/W cone | PASS/RESTRICTED, independently verified, but incompatible completions must not be conflated with one fixed x |
| 3 | New FIXSRC061 source-fixed E_W^x=D_x, sharp ratio q, quantified max-min gap | PROVED/RESTRICTED by supplied proof, peer mathematical review OPEN |
| 4 | New FIXSRC062 exact three-column tariff lambda_B+D_q lambda_W+lambda_D<=1, optimum q | PROVED/RESTRICTED by supplied proof, peer mathematical review OPEN |
| 5 | Raw B always decreases under READ | FAIL; authentic q=3 read increases B from 1 to 2 |
| 6 | Worst-case minimax W=q^2 is itself a universal all-edge unit potential | FAIL; authentic final zero READ discharges D_q at cost one |
| 7 | TMR-1/036 / TMR-3/036 authenticated XOR/Tseitin fast path | Retained restricted cross-model hostile control; no claim of new independent complete review of the original asymptotic source |
| 8 | /341 full logical UNSAT authority; /386 guarded authority | FAIL for /341 full language; RESTRICTED for /386 tested fragment, unchanged |
| 9 | Superpolynomial source-aware fusion potential after genuine compact operations | OPEN |
| 10 | Complete same-system all-correct-uniform-SAT-machine transfer and unrestricted P!=NP | OPEN |

**Weakest surviving lemma:** Construct a genuine **source-aware, syntax-aware, full-machine** cost-sound reduced product whose initial potential exceeds every polynomial on an explicit unbounded family, after the actual paid Bellman closure includes sharing, affine elimination, learned clauses, caching, rereading, extensions, and both-label completion. The present source-aware repair reaches only q on an m=q^2-bit query source and is not such a construction.

**Peer request:** TMR-2 verify D_x and quantify the difference between a compatible-completion MAY adversary and an algorithm-selected hard input; TMR-3 check the exact three-column frontier and dynamic transcript costs; TMR-4 independently reconstruct source-fixed paid Bellman closure and test whether a state-aware reduced product can improve an *initial* potential after real operations; TMR-1 keep the all-input uniform model gate explicit.

**Tracker and manuscript decision:** full proof1.txt read (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343); authentic complete proof2.txt recovered via Git blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 chars); authentic complete root main.tex recovered via Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 chars); root shared artifacts not edited because fresh claims await peer review and no unrestricted arrow changed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** All five existing schedules untouched.

END_OF_REPORT::TMR5::033::2026-11-14_2151_PST
