# TMR-5 / OBSERVATION-OPTIMALITY-REVIEW001: independent all-machine abstraction audit and exact potential ceiling

**Research time:** 2026-11-13 13:48 PST (America/Los_Angeles).  
**Role:** NEW TMR-5 Machine Bottleneck Redteam and synthesis, under the superseding 2026-11-13 12:49 PST directive.  
**Status:** independent mathematical verification of TMR-4's exactly scoped observation theorem; new general optimal-potential corollary **CANDIDATE pending independent TMR-1/4 review**; finite replay **COMPUTATIONAL**; unrestricted superpolynomial SAT time lower bound **OPEN**; P versus NP **OPEN**.

## Target and predeclared falsifiers

Target: independently verify TMR-4's observation-only cost abstraction against the full fixed-uniform multitape machine model, then determine whether *any* admissible lower-bound potential on that abstract graph can outperform the proposed hitting-set potential.

F1: an actual machine transition (copy, reread, work-tape arithmetic, or head reposition) has no abstract edge with cost at most its physical transition cost. F2: a correct SAT/UNSAT halt occurs without hitting some valid opposite-label input difference. F3: overlapping differences can be charged independently. F4: an alternative admissible abstract potential exceeds the purported shortest-path bound. F5: communication or one-pass restrictions have been smuggled into an unrestricted machine claim.

F1, F2 and F4 fail by the independent arguments below. F3 is an actual counterexample to naive additive accounting. F5 is avoided by retaining a strictly observation-only result.

## Exact model and independent TMR-4 review

Use the exact signed proper 3-CNF encoding of TMR-1, length $L$ in bits, one fixed total correct finite deterministic multitape decider $A$ for every length, and a read-only two-way input with fixed finite work tapes and unit-cost transitions. A must decide both valid SAT and valid UNSAT correctly, and reject malformed strings. Let $x$ be valid with known semantic label $b$ and let $Y=\{y_1,\ldots,y_r\}$ consist of valid same-length opposite-label inputs. Set $D_i=\{j:x_j\ne(y_i)_j\}$, all nonempty.

**Independent initial/all-transition/terminal verification.** Enrich each real configuration *for analysis only* with ghost set $H$ of observed original-input coordinates. Let $U(H)=\{i:H\cap D_i=\varnothing\}$. Initial $H=\varnothing$ maps to full $U$. A real transition reading coordinate $j$ maps to the abstract MAY edge deleting every $i$ with $j\in D_i$, at abstract cost 1 if something is deleted and 0 otherwise; any other real transition maps to a 0-cost stutter. Thus every real step has an abstract representative of cost at most its real unit time, irrespective of the physical machine's chosen representation. If a correct real execution halted with $i\in U$, replacing input $x$ by $y_i$ would preserve the entire deterministic trace because no changed coordinate was read, but force the same output on opposite labels. Contradiction. Both terminal labels are preserved by the separate fixed semantic label $b$, not by an input-label oracle available to $A$. The argument uses full input binding and read-only access; it does not require streaming, proof production or a specific reasoning system.

Consequently the abstract minimum accepting-path cost $d_G(U_0)$ is at most $T_A(x)$. The shortest abstract path reads a minimum hitting set of the $D_i$, so $d_G(U_0)=\tau(D)$, where $\tau(D)$ is the minimum number of input coordinates meeting every $D_i$. The existing TMR-4 symbolic argument is correct within these precise premises. Scope is **PROVED/RESTRICTED after independent symbolic audit**, not any SAT-runtime separation theorem. Finite tests are separately COMPUTATIONAL.

## TMR5-O1: optimum among every admissible observation potential

**CANDIDATE theorem (complete independent proof, awaiting TMR-1/4 second review).** Fix the *full* TMR-4 MAY graph $G(D)$ with states indexed by $U\subseteq[r]$, all possible coordinate-read edges, and stutters. Let $\Phi$ be *any* real-valued function on this graph satisfying

$$
\Phi(U)\le c(U,V)+\Phi(V)\quad\text{for every abstract edge }U\to V,
\qquad \Phi(\varnothing)\le0.
$$

Then

$$
\Phi([r])\le\tau(D)\le L.
$$

Moreover, the potential $\Phi_*(U)=\tau(\{D_i:i\in U\})$ satisfies all these inequalities, with $\Phi_*(\varnothing)=0$. Therefore

$$
\sup_{\Phi\,\text{admissible}}\Phi([r])=\tau(D)\le L.
$$

**Proof.** Take a minimum hitting set $J$ of size $\tau(D)$. Starting from full $U=[r]$, traverse the graph's freely permitted coordinate-read MAY edge for each $j\in J$, in any order. The resulting state is empty because $J$ hits all differences. Its path cost is at most $|J|=\tau(D)$. Repeatedly applying the potential inequality and the terminal bound gives $\Phi([r])\le\tau(D)$. For the matching lower bound on the *best possible* potential, any $J$ hitting the differences not yet removed after one coordinate read can be augmented by the read coordinate, so $\tau(U)\le 1+\tau(V)$, including equality on 0-cost stutters. Thus $\Phi_*$ is feasible with initial value $\tau(D)$. All $D_i$ are subsets of the $L$ bit positions, so taking $J=[L]$ proves $\tau(D)\le L$. QED.

**Meaning:** This is not merely a weakness of the *particular* hitting-set formula. No different potential can beat $L$ while retaining this graph's unrestricted input-coordinate-read MAY transitions and observation-only state. A future superpolynomial argument must introduce independently justified obligatory post-acquisition computation costs or a different information domain. Introducing artificial high cost on some read edge violates cost-underestimation; removing a genuine cheap abstract path is unsound. The lemma does not rule out all abstract-interpretation approaches, and does not establish $T_A(x)\le L$.

## Original strict-3CNF checks and hostile controls

For TMR-2's exact five-bank $E_n(a,b)$, the gadget

$$
(\ell\lor u\lor v)\land(\ell\lor u\lor\neg v)
\land(\ell\lor\neg u\lor v)\land(\ell\lor\neg u\lor\neg v)
$$

is equivalent to $\ell$. Its first $4n$ clauses force $x_i=a_i$, and the second $4n$ force $x_i=b_i$, hence SAT iff $a=b$. Each of the $2n$ independent four-sign-bit flips on a diagonal $E_n(a,a)$ reverses a single forcing gadget and makes the formula UNSAT. The changed source bits are disjoint. This independently verifies the semantic and first-read premises used by TMR-2 and TMR-4, under the exact $N=5n$, $M=8n$, $L=13n+2+24n(1+w)$ encoding with $w=\max(1,\lceil\log_2(5n)\rceil)$.

The overlapping sets $D_1=\{0,1\}$, $D_2=\{1,2\}$ have $\tau=1$, not 2, since reading coordinate 1 resolves both. Five singleton differences require exactly five reads, attaining $\tau=L=5$. Adding a 0-cost MAY edge from nonempty $U$ directly to goal makes any positive old potential violate the abstract inequality. Such an edge is allowed only if justified by an actually possible machine step; deleting a genuine physical shortcut is not a legal repair.

## Independently executed program

**Reproducer (published):** `experiments/tmr/tmr5_observation_independent.cjs`.  
**Raw (published):** `results/raw/tmr/2026-11-13_1348_TMR5_OBSERVATION_REPLAY.json`.

Ran a fresh independent JavaScript V8 implementation, not the TMR-4 script: 6,939 families of nonempty coordinate differences at lengths $L=1,\ldots,5$ with up to three potentially overlapping sets; 52,566 abstract states, 254,898 all-edge potential inequalities and 52,566 independent shortest-path / hitting-set equalities. Also exhaustively classified 20 independent proper-3CNF $E_n(a,b)$ sources for $n=1,2$ by direct assignment enumeration, including 20 opposite-label single-gadget flips and 33,024 raw assignment trials. All checks passed without randomness. This is hosted V8 arithmetic/semantic replay, not a native OS Node execution, a physical TM simulator or an asymptotic proof. The full program constructs its own clauses and hitting-set solver.

## Peer dependency audit

- **TMR-1 N1 pointwise nonuniformity:** symbolic construction survives. A different finite controller with an exponentially large hardwired depth-$L$ trie can classify each specific length in $L+O(1)$ and use a correct fallback for all other lengths. This is not a single all-length uniform machine. The quantifier distinction is essential.
- **TMR-1 N2 source-copy escape:** symbolic construction survives with one additional work tape, $O_A(L+T_A)$ time and $S_A+L+O_A(1)$ visited work cells. It falsifies a mandatory physical *original*-tape reread bound, not a total computation-time bound.
- **TMR-2 necessity:** the changed-coordinate indistinguishability and exact proper-3CNF equality gadget survive the fresh independent finite and symbolic audits. The $2n$ lower bound is only linear in $n$.
- **TMR-3 sweep tradeoff:** the diagonal communication-transcript injection proof is coherent **under its complete-one-way-sweep and paid-reset model**; each diagonal's variable-length transcript includes termination and every work configuration, and messages can be spliced across identical communication histories. No native physical sweeping-machine execution was independently replayed here. Its extension to arbitrary two-way input access and other representations is OPEN. This audit does not promote an unrestricted theorem.

**Model barriers:** Random-access indexed input reading, unrestricted rereads, source copying, Gaussian-elimination XOR shortcuts, Horn and 2-SAT recognition, bounded-treewidth dynamic programming, compact decision circuits, shared state, auxiliary variables, padding and renaming all remain admissible. Neither the large number of assignments nor a prescribed resolution proof/transcript can substitute for a proved necessary physical cost. The original LSPV-5/167 crossing argument and LSPV-4/487 indexed equality escape were reviewed as restricted-model historical evidence, not promoted to unrestricted machine theorems. No ETH/SETH, oracle or nonuniform answer table is inserted into an unconditional result.

## Integrated proof dependencies

D0 (KNOWN): uniform total machine, correct both-label SAT language, fixed bit encoding, actual time and writable-space charges.

D1 (INDEPENDENTLY VERIFIED, SCOPED): input-copy counterexample N2; nonuniform per-length minimization counterexample N1; same-machine $S_A\le b_A(T_A+1)$.

D2 (INDEPENDENTLY VERIFIED, SCOPED): input-coordinate necessity, $2n$ strict-3CNF equality family, and all-machine observation abstract simulation.

D3 (INDEPENDENTLY VERIFIED, SCOPED): all admissible potentials in the observation-only MAY graph satisfy $\Phi(U_0)\le \tau(D)\le L$. Observation-only abstraction is insufficient for an unbounded polynomial-exponent lower bound.

D4 (RESTRICTED/CANDIDATE): TMR-3 same-input $T(S+1)$ sweep tradeoff under a prescribed access model. Missing unrestricted transfer.

D5 (OPEN): independently defined obligatory post-observation computation/reconstruction charge under arbitrary compact representations, with a complete all-transition cost-sound map.

D6 (OPEN): a lower bound on that charge defeating **every** polynomial exponent for every single fixed total correct decider, on arbitrarily large valid inputs.

D7 (CONDITIONAL): D5+D6 plus cost soundness would imply P != NP. A correct all-input polynomial decider would instead imply P=NP. Neither established.

**Tracker decision:** Both root `proof1.txt` and `proof2.txt` were read in complete authoritative form, including Git-blob recovery for the 1,051,196-character second tracker. The scoped review and maximal-potential no-go add a new research fact but do not alter root P1-01/03/04 or P2-00/A2/D1/C3/B1/B2/B3 status. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The current TMR directive supersedes obsolete role assignments appearing in historical trackers, without deleting that provenance.

## Original / primary references

[1] H. Buhrman, R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288(1), 2002, 21-43. https://doi.org/10.1016/S0304-3975(01)00144-X . Decision-tree certificate complexity is a known antecedent, not originality claimed here.

[2] P. Cousot, R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977, 238-252. https://doi.org/10.1145/512950.512973 . Exact dataflow overapproximations and program semantics, not a general SAT lower bound.

[3] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, 835-865. https://doi.org/10.1145/1101821.1101822 . Their simultaneous random-access time/space exclusions under small workspace budgets do not rule out arbitrary polynomial-time algorithms with arbitrary polynomial workspace.

## Execution / publication safeguards

The superseding 12:49 PST directive was read FIRST and rechecked before shared writes. Both complete root proof trackers, the complete 2,479,448-character root main.tex, issue #3, AGENTS.md, CODEX.md, repository research skill, all four newest TMR handoffs and original substantive reports were fetched. Large files were recovered through the original blob SHA where the contents API was incomplete. No old tasks, ownership or schedules were revived. Code and raw were published to main and await readback confirmation below. No full project preflight, LaTeX compile, OS Node test or physical TM simulator was executed. No unreviewed assertion is promoted to unrestricted P != NP.

**Next target:** TMR-2 and TMR-3 propose a candidate *unavoidable* post-copy global-consistency operation that survives arbitrary input rereads and compact algebra. TMR-4 must provide a cost-underestimating path for every real transition, including the proposed shortcut. TMR-1 proves the exact fixed-machine quantifier bridge; TMR-5 tests an explicit fast counteralgorithm and independently replays any claimed bound.

END_OF_REPORT::TMR5_OBSERVATION_OPTIMALITY_REVIEW001::2026-11-13_1348_PST
