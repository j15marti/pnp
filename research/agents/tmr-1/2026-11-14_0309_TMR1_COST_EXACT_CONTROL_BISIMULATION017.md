# TMR-1/017: a mechanically certifiable, cost-exact quotient of arbitrary finite Turing-machine control

**Pacific timestamp:** 2026-11-14 03:09 PST (America/Los_Angeles). **Role:** TMR-1 Machine Model Lead. **New scoped mathematical result:** CANDIDATE/RESTRICTED, with a complete local proof and independent TMR-5/TMR-4 review requested. **Executed finite evidence:** COMPUTATIONAL. **General 3-SAT superpolynomial lower bound:** OPEN.

## 1. Exact objective, declared machine model and what changed

The machine model remains ONE fixed finite, total, deterministic multitape decider $A$ for ALL binary input lengths. Let $L=|x|$ be the encoded source bit length, not clause count or variable count. There is a fixed finite control $Q$, a fixed finite number $h$ of read-only input heads (ordinary baseline $h=1$), endmarkers, a fixed finite number $b$ of locally moving writable work tapes, finite alphabets and fixed SAT, UNSAT and MALFORMED halting labels. The immutable source is part of each concrete execution's identity. Every physical transition costs one; moving any head, copying a symbol, parsing, encoding, caching, repeated reads and work-tape operations take physical transitions. Every visited writable cell counts toward $S_A(x)$. The construction does not alter the input grammar, assume correctness from a proof calculus, or assume a polynomial running time.

**Research target:** provide a *one-sided decidable certificate* that finite-control information may be erased with EXACT cost and terminal preservation for all inputs, without solving the uncomputable all-input semantic-inertness problem of TMR-4/017. The new theorem is an explicit bridge for this restricted operation on arbitrary machine programs, not a bridge from restricted SAT languages to unrestricted time lower bounds.

The novelty here is a project-specific formalization, explicit source-bound multitape proof and executable hostile controller. Classical finite-state partition refinement/strong bisimulation is prior art [1,2]. This does not claim to invent bisimulation theory.

## 2. The strong local control-congruence theorem (TMR1-SCQ17)

Let $R=\Sigma_{in}^{h}\times\Gamma^{b}$ be the finite alphabet of vectors seen simultaneously by the $h$ input heads and $b$ writable heads. For each nonhalting control state $q\in Q$ and $r\in R$, the finite table of $A$ returns a fixed tuple

$$
\delta(q,r)=(\alpha(q,r),q'(q,r)),
$$

where $\alpha$ specifies ALL work-tape writes, EVERY work-head and source-head displacement, any charged output action, and the unit transition cost. Halting states carry one of the three exact terminal labels. Requiring equality of actions even for symbol tuples that never arise on an actual run is deliberately conservative and makes the certificate independent of reachability or an SAT oracle.

Call a relation $\sim$ on control states a **strong local cost congruence** when: (i) related halting states have the same SAT/UNSAT/MALFORMED label and neither is related to a nonhalting state; (ii) for every $r\in R$, related nonhalting $q_1,q_2$ have identical full observable action $\alpha(q_1,r)=\alpha(q_2,r)$ and related successor controls $q'_1\sim q'_2$. A local head move disallowed at a source endmarker is never performed by the concrete execution; requiring equality on the complete table is still sufficient.

**Theorem.** From the EXPLICIT finite transition table of any fixed $A$ there is an effective partition-refinement algorithm computing the unique coarsest equivalence $\sim_*$ satisfying this condition. The source-bound quotient $A/\sim_*$ whose configurations retain $x$, every tape content, ALL head positions and the class $[q]$ has the following properties, for every source $x$ and every reachable concrete configuration $c$:

1. Its initial configuration is the projection of the exact concrete initial configuration. For each legal concrete transition $c\to c'$ of cost one, there is exactly the quotient transition $[c]\to[c']$ of cost one.
2. For every quotient transition at $[c]$, EVERY concrete representative $c$ of that same source/tapes/heads/control class has the SAME complete tape writes, all head moves and a successor in the designated quotient class. Therefore a path from the concrete initial state has an exact same-source concrete replay with identical step counts, not merely a MAY simulation.
3. Both SAT and UNSAT terminal classifications and the MALFORMED output are identical. In particular, for all $x$,

$$
T_{A/\sim_*}(x)=T_A(x),\qquad S_{A/\sim_*}(x)=S_A(x).
$$

The quotient is a mathematical abstraction of the original machine. An optional implementation must also CHARGE any program rewriting or encoding cost; this theorem does not treat its construction as an uncharged computation inside $A$.

**Proof (explicit).** Initially partition terminal controls by their terminal labels and put all nonterminal controls in a fourth block. Given a partition $P_i$, split the nonterminal blocks according to the vector, over every $r\in R$, of their exact observable actions and $P_i$-classes of successors. Retain terminal-label blocks. Each proper refinement increases the block count, so at most $|Q|-1$ proper refinements occur. At a fixed point two states in the same block have equal actions and next-state blocks for ALL local symbol vectors, so their block relation satisfies (i),(ii). Conversely any strong local congruence refines $P_0$; if it refines $P_i$, equality of actions and successor congruence imply it refines $P_{i+1}$. It therefore refines the fixed point. Thus $P_*$ is the **coarsest among all symbol-universal one-step strong local control congruences**, not among arbitrary source-reachable semantic abstractions.

For any concrete configuration with control $q$ the read symbol vector is determined by its exact immutable source, writable tapes and head locations. All controls in $[q]$ prescribe precisely the same writes and moves on this vector, with successor in the same next class. The property is maintained by induction across every step, including rereads, arbitrary work-tape reencodings, overwrites and recomputation. Terminal-label equality completes the proof of exact execution, time and writable-cell footprint. No input-specific reachability set, semantic SAT query or runtime oracle enters the construction. QED.

**Complexity of checking the certificate:** polynomial in the size of the explicitly enumerated transition table $|Q||R|$, for example at most $|Q|$ rounds of full-signature sorting/hashing. Since $R$ is the cross-product of the fixed alphabets and fixed tape count, these table entries are finite; no polynomial claim is made for an exponentially succinct machine description.

## 3. Precise restriction and relation to the undecidability obstruction

This theorem does not decide whether an arbitrary register is *semantically inert on reachable executions*. Its universal condition may reject a safe erasure if only unreachable register values produce different actions, or if two semantically equivalent sequences have different intermediate movements/costs. This loss of completeness is **necessary** for any proposed universal total exact-erasure decider by TMR-4/017, whose halting reduction I independently audited: a clocked simulation of an arbitrary $M$ is performed within $L$ paid input-head movements on a separate work tape, and a parity-controlled extra roundtrip is taken iff $M$ halted within those $L$ steps. The all-input exactness is then equivalent to nonhalting of $M$. That restricted reduction is mathematically sound under its declared ordinary multitape model and on *all binary sources*, including malformed strings; it is not a SAT-time lower bound. This serves as an independent mathematical peer confirmation of its exact unrestricted-input semantic-erasure limitation, not a confirmation of the unexecuted universal machine compiler.

For TMR-4/016's **inert** parity scan, registers can be merged if their later transitions have equal observable actions and equivalent successors. For its **gated** parity scan, gate actions differ and the certificate correctly rejects this merge. Thus no true physical detour is discarded and there is no replay-spurious shortcut for a quotient satisfying the new certificate. Preserving a full execution transcript and identifying an inert control bit is not the same as proving an *unavoidable* 3-SAT cost.

The strongest surviving implication is:

$$
\text{finite strong control congruence}
\Rightarrow\text{same-source all-step cost-exact quotient}
\Rightarrow d_{\rm quotient}(a_0,G)=T_A(x).
$$

The final equality is NOT a computable polynomial lower bound or an algorithm for finding the shortest abstract path. The graph can still have unbounded writable-tape states; defining a potential as the unknown actual distance would be circular for P versus NP. The missing implication, still **OPEN**, is an independently justified superpolynomial initial lower-bound potential for EVERY correct uniform $A$ at all polynomial exponents.

## 4. Hostile construction and actually executed finite testing

The self-contained source `experiments/tmr/tmr1_control_bisimulation017.cjs` was actually executed as its exact self-contained `audit` function in hosted V8, then that same function was serialized verbatim into the published Node-compatible source. Its immutable result is `results/raw/tmr/2026-11-14_0308_TMR1_CONTROL_BISIMULATION017_RAW.json`. GitHub readback verified both.

Two fixed finite-control, locally moving single-input-head deciders classify a genuine **restricted one-variable 3-CNF** language: input symbol 0 is the three-literal repeated-variable clause $(z\lor z\lor z)$, symbol 1 is $(\neg z\lor\neg z\lor\neg z)$. SAT iff all input clauses have the same sign, or there are no clauses; UNSAT iff both signs occur. This grammar permits repeated literals, so it is neither the original project's proper three-DISTINCT-literal source grammar nor NP-complete. All binary words are well-formed under this restricted grammar, so MALFORMED was NOT tested. Before the classifier the first controller performs a parity sweep and return but never uses parity. The second controller uses computed parity to force one additional fully charged source roundtrip. The source head always reads the current cell at positions $1,\dots,L$, not a neighboring bit.

The coarsest partitions and all transitions were mechanically checked. Inert control has 10 states and compresses to 8; its parity-differing scan/return states merge. Gated control has 12 states and compresses only to 11; the differently gated return states stay distinct. On the 2,047 exhaustive binary inputs of lengths $0\dots10$, quotient replay and the separate Boolean classifier oracle agreed exactly, with **21 SAT and 2,026 UNSAT**. There were **1,023 odd-parity sources**. The exact physical runtimes satisfy, with $q=L+1$,

$$
T_{\rm inert}(x)=3q+2,\quad
T_{\rm gated}(x)=3q+2+2q\cdot(\oplus_{i=1}^L x_i).
$$

There were 65,537 paid inert transitions, 86,017 gated transitions, 20,480 genuine detour transitions and 96 certified local action-pair comparisons. Five further length-24 and length-300 controls tested parity and repeated clauses. **Zero failed assertions.** These are COMPUTATIONAL finite tests on a restricted controller, not executions of an arbitrary compiled SAT machine. No independent OS-native Node/Python replay was executed this run.

**Falsifiers tried:** unused global parity, cost-relevant parity and replay-spurious cheap gate, genuine SAT and UNSAT labels, same-source current-cell reads, repeated clauses, long input padding, a classifier that can bypass any unnecessary scan. The theorem structurally permits arbitrary Horn, 2-SAT, affine/GF(2), bounded-treewidth DP, compact algebra, products, variable renaming, sharing, auxiliary variables and caching/recomputation in the unchanged underlying $A$, but these particular algorithms were NOT executed in this finite experiment. A user-supplied claimed lower bound that charges any of these optional operations remains unsupported.

## 5. Corpus, sources, tracker status, publication and next proof obligation

Read the authoritative TMR replacement directive first and again before publication (Git blob `47459817e66dccf1f3079e6c724c0fd2643e7bc4`); root proof1 complete 28,714 chars SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; root proof2 complete **1,051,196 chars recovered from authenticated Git blob** SHA `930c5eeddafce656717f28055a7a9a755f44737c`, not its blank `fetch_file` rendering; root `main.tex` complete 2,528,412 chars from authenticated Git blob SHA `31f68fe0fc5dcfb4f7947fb2dacd7d285074e2f5`; issue #3 through TMR-5/014; AGENTS.md; CODEX.md; pnp-research skill; all five latest TMR handoffs; original TMR-4/016, TMR-4/017, TMR-5/014, TMR-3/015, TMR-1/016, TMR-2/016; historical unchanged-checker-accepted literal order cost alias LSPV-5/523 at its original .tex path. The literal-order cost alias is genuine historical evidence, not a false abstract path. Neither historical owner allocation nor an obsolete checker obligation is restored. Full local repository preflight and XeLaTeX compilation were not run; no checkout of the entire repository is available in this connector run.

Primary scope sources, newly checked rather than inherited: [1] Paige and Tarjan, *Three Partition Refinement Algorithms*, SIAM Journal on Computing 16(6):973-989 (1987), https://doi.org/10.1137/0216062. [2] Kanellakis and Smolka, *CCS Expressions, Finite State Processes, and Three Problems of Equivalence*, Information and Computation 86(1):43-68 (1990), https://doi.org/10.1016/0890-5401(90)90025-D. [3] Cousot and Cousot, *Abstract Interpretation: A Unified Lattice Model*, POPL (1977), https://doi.org/10.1145/512950.512973. [4] Turing, *On Computable Numbers*, Proceedings of the London Mathematical Society (1936/37), https://doi.org/10.1112/plms/s2-42.1.230. [5] Fortnow, Lipton, van Melkebeek and Viglas, *Time-space lower bounds for satisfiability*, JACM 52(6):835-865 (2005), https://doi.org/10.1145/1101821.1101822, applies only to specified simultaneous time/small-space parameters, not arbitrary polynomial workspace.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The new locally decidable abstraction certifier does not settle any OPEN universal P=NP or P!=NP proof tracker node. Root `main.tex` was not modified because TMR-5 owns whole-document synthesis. No scheduled tasks were created, revived or changed.

**One next target:** TMR-5/TMR-4 should independently prove and replay the coarsest local control quotient's all-step cost equality, then investigate a strictly stronger EFFECTIVELY CERTIFIABLE program-specific invariant over bounded auxiliary work-tape summaries. It must preserve exact source binding and reject parity-dependent and literal-order-dependent genuine costs. A superpolynomial SAT necessity implication remains **OPEN**.

END_OF_REPORT::TMR-1::017::2026-11-14_0309_PST
