# TMR-1 / SAME-MACHINE-PRODUCT-CEILING002

**Research date:** 2026-11-13 14:07 PST (America/Los_Angeles). **Role:** NEW TMR-1 Machine Model Lead in j15marti/pnp. **Status:** CANDIDATE algebraic bridge pending TMR-5 audit; TMR5-O1 independently reviewed PROVED/RESTRICTED at its specified graph scope; finite computation COMPUTATIONAL; general P versus NP OPEN.

## A. Source recovery and target

Read FIRST the binding 2026-11-13 12:49 PST TMR five-agent replacement directive, blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Read proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), the full proof2.txt from Git blob 930c5eeddafce656717f28055a7a9a755f44737c (ordinary contents returned a blank body), and root main.tex through its Git blob, as well as issue #3, AGENTS.md, CODEX.md, repository research skill and modes/protocol, latest TMR-1/2/3/4/5 handoffs and substantive reports. Also inspected historical Claude ONETAPE-0001 and LSPV-5/REFEREE325 recognizable-island report; source-recognition bypass and one-tape equality are **existing prior results**, not new claims. The latest TMR-5 handoff notes that TMR-5 has since inserted five distinct ownership regions in canonical root main.tex, preserving the older manuscript.

**Target of this run:** quantify what TMR-3's same-input restricted time-space product could imply about physical time even under a hypothetical valid unrestricted transfer. Independently review TMR-5's observation-potential optimality theorem O1, as its handoff requests. Do not pretend that either result proves a machine-independent superpolynomial lower bound.

**Predeclared falsifiers:** F1, time and space improperly borrowed from different machines/inputs; F2, the product forces superlinear or superpolynomial time under arbitrary polynomial space; F3, a different observation-only graph potential exceeds its shortest permissible path; F4, complete-sweep, streaming or communication restrictions silently imported into general two-way-input multitape computation.

## B. Model, length and exact quantifiers

Use the established exact proper 3-CNF binary grammar: a unary N header, a unary M header, then three signed zero-based variable indices per clause with width w=max(1,ceil(log2 N)), distinct variables within each clause, and no trailing bits. Input bit length is

$$
L=N+M+2+3M(1+w).
$$

A is one fixed finite total uniform deterministic multitape Turing machine, across **all** lengths, with one two-way read-only input tape, b_A>=1 fixed finite two-way writable work tapes, fixed finite controller/alphabet, rejecting malformed encodings, correctly accepting SAT and rejecting UNSAT. Charge every transition, input reading and reread, work-tape/head/index cell, source copying, buffering, algebra, preprocessing, caching and recomputation. No free oracle, hidden advice, proof-system restriction, or uncharged RAM model translation. T_A(F) denotes physical transitions and S_A(F) the sum of distinct writable work cells visited on the **same physical execution**.

The unchanged target, equivalent to the open P versus NP problem for this fixed NP-complete language, is

$$
\forall A\in\mathcal D_{\mathrm{3SAT}}\;\forall k\ge 1\;
\forall C>0\;\forall L_0\;
\exists F\text{ valid}:
|F|\ge L_0 \text{ and } T_A(F)>C(|F|+1)^k.
$$

The hard F may depend on A,k,C,L0. A different hardwired lookup machine for each length is not allowed. The number b_A of work tapes may depend on the program A, but is independent of the input size for a fixed A.

The elementary same-machine occupancy bound is

$$
S_A(F)\le b_A(T_A(F)+1),
$$

since each work head begins in at most one cell and moves into at most one new cell per transition.

## C. TMR1-R1: fully charged product-to-time extraction

**CANDIDATE theorem, complete symbolic derivation, submitted for independent review.** Fix A with b=b_A. Let alpha,beta>=0 be constants, alpha+beta>0, and suppose an independently justified lower bound holds **on one identical input F and computation**:

$$
T_A(F)^\alpha(S_A(F)+1)^\beta\ge G(|F|).
$$

For T_A(F)>=1,

$$
S_A(F)+1\le b(T_A(F)+1)+1\le(2b+1)T_A(F).
$$

Consequently,

$$
T_A(F)^{\alpha+\beta}\ge
\frac{G(|F|)}{(2b+1)^\beta},
\qquad
\boxed{
T_A(F)\ge
\left(\frac{G(|F|)}{(2b+1)^\beta}\right)^{1/(\alpha+\beta)}.
}
$$

**Proof:** Substitute the preceding workspace upper bound into the assumed product lower bound, divide by the constant factor, and take the positive fixed root. All quantities refer to the same A,F and trace; no combining worst-case time witnesses with different worst-case space witnesses. QED.

**Quantifier application, CONDITIONAL only:** To force T_A(F)>C(L+1)^k on an input F, it would be sufficient to establish on that same input

$$
T_A(F)^\alpha(S_A(F)+1)^\beta
>
(2b_A+1)^\beta C^{\alpha+\beta}(L+1)^{k(\alpha+\beta)}.
$$

A genuine all-algorithm bound beating every fixed polynomial on arbitrarily large valid inputs could thus transfer through this formula. **No such premise is known.** With fixed alpha,beta, a fixed-degree polynomial G yields only a fixed-degree polynomial lower bound on T, not a P versus NP separation. Letting exponents depend on L requires separate accounting.

## D. TMR1-R2: exact evaluation of the newest TMR-3 tradeoff

TMR-3/001, only for **complete sequential one-way source sweeps with paid resets**, gives some satisfiable diagonal source F_n in the TMR-2 strict proper 3-CNF equality family E_n(a,b), with

$$
L(n)=13n+2+24n(1+\max(1,\lceil\log_2(5n)\rceil))
=\Theta(n\log(n+1)),
$$

and a **same-input, model-restricted** product inequality

$$
T(F_n)(S(F_n)+1)\ge c_A L(n)n
=\Omega_A(L(n)^2/\log L(n)).
$$

**Counterfactual transfer audit:** Even if this very bound were somehow established for every correct unrestricted fixed multitape machine with its actual workspace, R1 with alpha=beta=1 would give merely

$$
T(F_n)\ge
\sqrt{\frac{c_A L(n)n}{2b_A+1}}
=\Omega_A(L(n)/\sqrt{\log L(n)}).
$$

This growth is **o(L(n))**, so the *extracted bound by itself* does not even force superlinear time. In its real complete-sweep model, TMR-3 already has the stronger direct T>=L from requiring one full input sweep. On arbitrary machines, the missing model transfer is independently OPEN.

A resource ledger with T=L, S=b(L+1) satisfies the normalized inequalities T(S+1)>=Ln and S<=b(T+1) for this family (because L>=n). This is **only a feasible pair of resource budgets, not an asserted globally correct SAT algorithm**. Additionally, the TMR-2 equality island is efficiently recognizable and decidable with complete-input rereads, as the prior reports explain. None of this falsifies TMR-3's carefully limited sequential-sweep theorem. It falsifies the proposed *conclusion* that a fixed-degree same-input product lower bound, by itself, advances the all-polynomial deterministic time barrier.

## E. TMR1-R3: second independent review of TMR5-O1

TMR-5/001 requests another role to audit its claim that the **maximum admissible potential** on the full TMR-4 observation-only MAY graph equals a minimum hitting-set cost. Fix a length-L input x and valid same-length opposite-label inputs y_i. Let D_i be their nonempty source-coordinate difference sets. Abstract state U records which D_i have not yet been hit. For every coordinate j, the full MAY graph has an edge removing all i with j in D_i, charged 1 if any is removed, otherwise 0; every stutter costs 0; goal U=empty. The graph is a cost-underestimating overapproximation and is not a concrete algorithm.

Let tau(U) be the smallest number of coordinate positions hitting every D_i for i in U. Any potential Phi satisfying Phi(U)<=c(U,V)+Phi(V) on **every** edge and Phi(empty)<=0 obeys a hard ceiling: choose a minimum hitting set J, follow the graph's MAY edge for each j in J, and telescope to get

$$
\Phi(U_0)\le\sum_{j\in J}c_j+\Phi(\emptyset)\le |J|=\tau(U_0).
$$

Conversely tau itself is admissible: a minimum hitting set after one read, augmented with that read coordinate, hits all the previously unresolved D_i. Zero-cost stutters do not reduce tau. Hence

$$
\boxed{
\sup_{\Phi\text{ admissible}}\Phi(U_0)=\tau(U_0)\le L.
}
$$

**Independent verdict:** This is a correct **PROVED/RESTRICTED** graph-theoretic theorem after TMR-1's second symbolic audit, not a general Turing-machine lower bound. It proves the L-bit ceiling for **all potentials on that exact full MAY graph**, not merely for the chosen hitting-set potential. It does not rule out an abstraction that genuinely captures unavoidable post-observation computation, and it does not assert T_A(F)<=L. No correct concrete computation is removed to inflate the graph cost. The terminal SAT/UNSAT label is held by the mathematical analyst, not supplied freely to A.

Adversarial controls: overlapping D1={0,1},D2={1,2} have tau=1, not 2; disjoint singleton differences attain tau=L; any zero-cost path from a non-goal state to goal immediately caps Phi there at zero. F3 is ruled out for the declared graph; alternative machine-state abstractions are outside the theorem.

## F. Reproducible exact audit

**Executed Python source:** experiments/tmr/tmr1_time_space_bridge_audit.py (Git blob 16dafc5be8764bece6066d1d313c2dac4b5a8375; source SHA-256 1aaaa0755b9368ccf392f7f09038f64bb60f4cf708aa0f05f6f0f2d3c0d4449c). **Immutable raw:** results/raw/tmr/2026-11-13_1402_TMR1_TS_BRIDGE_RAW.json (Git blob 033f08ad8b5fa41cc4e1cae72c54e73e50001c69; SHA-256 5265cf5d0cfd55d2ba35e39f78df1e0f14852ed7891db12529e797d780a685f8). Both were published and fetched back exactly from main.

One local Python process completed in **2.26 seconds**, standard library only, no randomness, with 494,590 deterministic check groups and zero failures:

| Audit type | Groups |
|---|---:|
| TMR-2 exact source lengths | 132 |
| Minimal integer T given b-tape occupancy and normalized product | 1,056 |
| Minimal T never exceeds encoded L | 528 |
| Fixed polynomial product pairs feasible with polynomial T and S | 120 |
| Exhaustive small integer same-machine implication grid | 230,917 |
| Independent MAY-graph shortest-path versus tau families | 6,939 |
| Every MAY-graph edge potential inequality | 254,898 |

Illustrative normalized c=1, b=2 values: at n=64, L=16,194, G=Ln=1,036,416, the least T allowed by the product+occupancy inequalities is 720; at n=2048, L=763,906, G=1,564,479,488, least allowed T is 27,968. These numbers **do not** estimate the unknown TMR-3 constant c_A or measure actual solver time.

The code exhaustively checks small resource budgets, varies fixed b among 1,2,4,8, tests polynomial exponent q=1..8, and independently computes shortest distances over small MAY graphs by relaxation rather than assuming tau. Model inclusion allows Horn, 2-SAT, XOR/Gaussian elimination, bounded treewidth, products, sharing, padding, renaming, source copying and recomputation; **these solver families were not themselves run in this numerical audit**. No native OS Turing-machine simulator, repository-wide Python preflight or LaTeX compiler was executed. The working container had no local repository checkout, so the repository preflight script could not run. The mathematical proofs are separate from finite verification.

## G. Dependencies and next falsifiable target

D0 **KNOWN:** fixed uniform total machine; encoded bit length; both-label correctness; charged physical transitions; b constant per machine. D1 **INDEPENDENT REVIEWED:** prior TMR-1 nonuniform slice and original-input-copy bypass. D2 **PROVED/RESTRICTED AFTER SECOND REVIEW:** TMR-4/5 full observation MAY graph and maximum admissible potential tau<=L. D3 **CANDIDATE / CONDITIONAL:** quantitative same-machine product extraction, correct algebra but missing any strong product premise. D4 **RESTRICTED:** TMR-3 complete-sweep product; arbitrary-source model transfer OPEN, and its polynomial strength is insufficient even if freely transferred. D5 **OPEN:** independently specified compulsory **post-observation** charged global-consistency/reconstruction operations that withstand all alternate representations. D6 **OPEN:** prove such cost exceeds every polynomial exponent on large valid inputs for every fixed correct A. D7 **CONDITIONAL:** D5+D6 plus all-transition cost soundness would yield P!=NP; a correct general polynomial SAT algorithm would instead yield P=NP. Neither is known.

**Peer requests:** TMR-2 define a post-read necessity not defeated by compact algebra or source copying. TMR-3 target a bound quantitatively strong enough to survive conversion S<=O(T), and prove its full two-way-input machine-model transfer. TMR-4 cost-soundly charge every actual computation edge without eliminating real shortcuts. TMR-5 independently verify R1/R2, accept the second review of O1, and integrate only qualified statements in its new TMR-owned main.tex section.

**Root tracker action:** Both proof1.txt and proof2.txt reviewed, no P1-01/03/04 or P2-00/D1/C3/B1/B2/B3 closure. TRACKERS REVIEWED; NO MATERIAL CHANGE. TMR-5 owns root main.tex synthesis; no root text was overwritten. No automation or other task modified.

## H. Primary sources and non-novelty disclosures

[1] Fortnow L, Lipton R, van Melkebeek D, Viglas A. Time-Space Lower Bounds for Satisfiability. Journal of the ACM. 2005;52(6):835-865. https://doi.org/10.1145/1101821.1101822 . Original publication explicitly excludes specified near-linear time/small-space regions on a random-access model, not all polynomial-space machines.

[2] Lynch N. On Reducibility to Complex or Sparse Sets. Journal of the ACM. 1975;22(3):341-345. https://doi.org/10.1145/321892.321895 . Complexity cores require the hypothesis that the language lies outside P; that cannot be assumed for 3-SAT. https://groups.csail.mit.edu/tds/papers/Lynch/jacm75.pdf .

[3] TMR-3/001, 2026-11-13 13:34 PST, restricted same-input multipass theorem; TMR-5/001, 2026-11-13 13:48 PST, observation graph independent audit. Earlier Claude ONETAPE-0001 and LSPV-5/REFEREE325 already address equal-input machine restrictions and recognizable easy islands. No priority or novelty claimed for those methods.

**Publication:** new report, independent code and raw, compact updated TMR-1 handoff. Readbacks are mandatory; issue #3 handoff will list exact verified locations. No all-machine lower bound has been proved.

END_OF_REPORT::TMR1_SAME_MACHINE_PRODUCT_CEILING002::2026-11-13_1407_PST
