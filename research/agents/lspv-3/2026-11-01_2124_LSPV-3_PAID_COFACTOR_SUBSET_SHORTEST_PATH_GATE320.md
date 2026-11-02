# LSPV-3 GATE320: Paid cofactor subset shortest path and strict greedy counterexample

**2026-11-01 21:24 PST, America/Los_Angeles.** PROVED/EXACT elementary **restricted** reduced-OBDD theorem, independently verified finite SAT/UNSAT experiments. External review pending. **P versus NP OPEN.**

## Universal obstruction and four falsifiers

A fan-in-two circuit C_F(x)=F(x) evaluates a supplied assignment cheaply, but Circuit-SAT asks whether an accepting original assignment EXISTS. Exact Shannon continuation functions are not free; acquiring and comparing them may be exponential. The following candidate claims were tested: (1) exact cofactor layer costs telescope to the reduced OBDD node count (PROVED in the declared model); (2) picking the uniquely cheapest next layer minimizes total nodes (FALSIFIED); (3) forward and reverse cofactor class counts are identical when source crossing width agrees (FALSIFIED); (4) minimum OBDD size is necessary SAT decision work (NOT SUPPORTED, contradicted as an inference by cheap DPLL controls and expensive compilation).

## Exact representation-specific theorem

For an original Boolean function F over V, subset S, and all coherent assignments a to S, let Q_F(S) be the set of distinct pointwise suffix functions F|a on V\S. For v outside S set

c_F(S,v) = |{ g in Q_F(S): g|v=0 != g|v=1 }|,

where equality refers to full **future continuation behavior**, not the SAT bit or a syntactic pin key. In a fully reduced OBDD with fixed variable order pi, shared nodes, exactly two terminals, and no complemented edges:

nodes(F,pi) = sum_{k=0}^{n-1} c_F(S_k,pi[k+1]), where S_k={pi[1],...,pi[k]}.

**Proof.** Every prefix assignment denotes one suffix cofactor. If that function is independent of the next variable v, reduction skips the v node. If dependent, it yields the ordered pair of distinct low/high suffix functions. Two such nodes merge exactly when their parent cofactor functions are equal, because their low/high pairs are equal. Hence the number of unique v nodes is c_F(S,v). Sum over the order. This yields the subset-lattice Bellman equations

D_min(V)=D_max(V)=0;
D_min(S)=min_{v outside S}[c_F(S,v)+D_min(S∪{v})];
D_max(S)=max_{v outside S}[c_F(S,v)+D_max(S∪{v})].

This is a source-indexed restatement of established Shannon/OBDD reduction and optimal ordering techniques, not an unrestricted hardness result. **The costs c_F are not supplied by any semantic oracle.**

## Precise falsification on a valid canonical same original

The authenticated F9 original has 9 original variables, 12 distinct monotone 3-clauses, each variable exactly two positive and two negative source occurrences, and 70 complete satisfying assignments. Source validation and five malformed controls pass. Exhaustive ordered reduced-OBDD results:

| Formula | Optimal nodes | Worst nodes | Lexicographic one-step greedy | Complete orders verified |
|---|---:|---:|---:|---:|
| F9 | 52 | 80 | 62 | 9! = 362880 |
| Y6 | 19 | 25 | 22 | 6! = 720 |

F9 best order is (2,6,7,9,8,4,3,1,5); immediate-width greedy yields (1,2,3,5,4,8,7,6,9). After the previously processed **prefix set** S={x2,x3,x4,x5,x6}, the remaining variables are x1,x7,x8,x9. Their exact [immediate nodes, optimal future nodes, sum] are:

x1 [17,22,39]; x7 [18,22,40]; x8 [16,26,42]; x9 [17,22,39].

Thus choosing **x8, the unique least-cost immediate move**, is three OBDD nodes worse than choosing x1 or x9 and then proceeding optimally. Full subset enumeration finds **75** F9 prefix subsets with such a strict local-greedy failure. This is a finite counterexample to myopic order selection, not a proof against every adaptive solver.

At the **same source cut** S={x1,x2,x4,x6,x8,x9} versus its complement {x3,x5,x7}, exactly 9 original clauses cross either way; nevertheless there are **22** distinct Boolean cofactors after pinning S and **8** after pinning its complement. Clause crossing count is a sufficient ceiling, not a necessary number of semantic states.

## FULL cost of the tested semantic acquisition

The producer does not get a SAT-label or equality oracle: it checks 2^n original complete assignments, builds the 3^n coherent pin profiles and the 4^n cofactor truth-table bits, tests all n2^(n−1) subset-order edges and calculates the finite DP. Measured explicit work:

| Item | F9 | Y6 |
|---|---:|---:|
| Original-source complete evaluations | 512 | 64 |
| Coherent pin profiles | 19683 | 729 |
| Cofactor table bits generated | 262144 | 4096 |
| Explicit dependence comparisons | 164700 | 2366 |
| Subsets | 512 | 64 |
| Candidate next-variable edges | 2304 | 192 |

The conservative charged construction uses O(poly(N,n)4^n) bit-time and O(poly(N,n)2^n) live writable bits with a streamed cofactor table and retained edge costs/DP. The **first truth-table pass already decides SAT/UNSAT**. Therefore the 52-node resulting best OBDD cannot be claimed to be an inexpensive SAT decider.

**Same-original both-label control:** Common coherent pins (x3,x5,x6,x7,x8)=(0,1,0,0,0) and x1=0 yield **2** complete SAT extensions; the only change x1=1 yields **0**. The latter has eight exhausted original-clause-falsified completion leaves. An independent UP-first DPLL run on original F9 has **one** recursive node on each pinned label, with 40 SAT versus 34 UNSAT literal inspections. The UNSAT derivation uses source C2 to force x2=1, source C6 to force x9=1 and source C11 as the resulting contradiction. F9 264 source clause-pair SS/SU/US/UU extreme compatibility entries and all 6144 full assignment-complement clause identities were checked. Y6 has exactly 20 models. F15/U198/V198 are inherited controls, not freshly replayed in GATE320.

**Independent testing:** Standalone full producer, separate no-producer-import verifier with a different tuple-valued cofactor implementation and exhaustive enumeration of **all 363600** F9 and Y6 orders, and original-source UP-DPLL code are bundled in the completed ZIP. No-import verifier passed **29 grouped assertions**, with no discrepancy. The GitHub compact source is an additional independent, self-contained recheck. Counts are **Python operations, not native FLMV indexed-machine steps**. Physical XOR was not measured; logical XOR remains OFFLINE.

## All-input recurrence and precise OPEN obligation

For every actual source-authenticated typed state R, total work is

T(R) = T_grammar/source/index/head + T_discover/represent/equality
     + T_all_failed_policies/choose/switch + T_gate/GE/proof/cache/replay
     + T_child/output/bit_access/reencode + T_guest_DELAY/COPY/RECOMP
     + Σ_{executed descendants R'} T(R').

Measure simultaneous peak writable/index/ancestor/cache/guest/proof/output space, not a sum of incompatible individual maxima. Recode/replay, grammar verification and policy acquisition are never free. Here the measured cofactor acquisition itself has exponential worst-case upper cost. This does **not** show it is necessary for an arbitrary correct SAT decider, and it does **not** yield an all-input polynomial total-work bound.

The canonical target is **all** valid duplicate-free proper Döcker monotone 3-SAT-(2,2) ORIGINALS; malformed strings reject. Ordinary Shannon/cofactor states and Tseitin circuits are NOT canonical hereditary children. The fully charged arbitrary-A power-short A->Phi(A) and strict numerical **SAME-MACHINE** FLMV SAT-to-canonical reduction remain unproved. Both P=NP and P!=NP remain OPEN.

## Source and literature audit

Read FIRST: verified 19:50 five-role redirect, decision-only handoff, LSPV-3 GATE319, LSPV-4 321, LSPV-2 322/323, LSPV-3 HWB-OBDD-BARRIER68, and issue #3. Web queries included: 'optimal OBDD variable ordering dynamic programming', 'Bryant 1986 graph based algorithms', 'Bollig Wegener improving variable ordering NP-complete', 'Darwiche Marquis compilation map', and 'Amarilli width structure knowledge compilation'. Authenticated project GitHub searches found cofactor/OBDD prior code including lspv4_279 and earlier HWB controls. OpenAI organization GitHub cofactor and BDD searches returned unrelated OpenAI math/analysis code, no matching OBDD solver; search absence does not establish novelty. Direct raw.githubusercontent.com access from the experimental container failed DNS resolution; repository access used the GitHub connector.

References: (1) Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE TC 35, 677–691, 1986, DOI 10.1109/TC.1986.1676819. (2) Bollig & Wegener, *Improving the Variable Ordering of OBDDs Is NP-Complete*, IEEE TC 45, 993–1002, 1996, DOI 10.1109/12.537122. (3) Darwiche & Marquis, *A Knowledge Compilation Map*, JAIR 17, 229–264, 2002, DOI 10.1613/JAIR.989. (4) Amarilli et al., *Connecting Width and Structure in Knowledge Compilation*, arXiv:1709.06188. (5) Fortnow, Lipton, van Melkebeek & Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52, 835–865, 2005, DOI 10.1145/1101821.1101822. (6) Döcker, *Monotone 3-SAT-(2,2) Is NP-Complete*, arXiv:1912.08032.

**Governance:** Preserve all five existing enabled tasks/IDs/titles/hourly Pacific offsets. Root main.tex may be reconciled only inside LSPV-3 ownership markers after full authenticated blob readback. P versus NP OPEN.
