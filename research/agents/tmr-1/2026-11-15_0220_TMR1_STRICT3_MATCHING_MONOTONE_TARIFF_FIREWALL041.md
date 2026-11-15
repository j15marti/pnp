# TMR-1/041: Strict-3CNF matching sign-profile and all-machine tariff firewall

**2026-11-15 02:20 PST (America/Los_Angeles).** Role: TMR-1, PNP Machine Model Lead. **Scientific status: PROVED/RESTRICTED symbolic source and transfer countercontrol, independent mathematical review OPEN. Finite tests COMPUTATIONAL. P versus NP OPEN.**

## 1. Candidate and falsifiers set before literature/corpus audit

**Candidate under attack:** even after constraining each original clause to **three distinct variables**, forcing every source mask to have the same variable count, clause count and unsigned incidence, a superpolynomial monotone sign-profile function might supply a positive all-step tariff component for arbitrary SAT deciders.

Falsifiers:

1. The 3-CNF splitter changes satisfiability, shares an auxiliary across clauses, produces a repeated variable in a clause, or changes unsigned incidence with the mask.
2. An alleged monotone lower bound applies to the original wide/binary/unit CNF but not to the actual strict-3CNF source encoding.
3. One fixed total deterministic SAT decider authenticates the entire exponentially sized mask family **without** enumerating masks, solves its instances by polynomial matching, and uses exhaustive fallback on other inputs.
4. A source-static terminal mask produces an illegal one-step overdischarge, or a source-profile initial tariff violates telescoping along the actual cheap matching execution.

Falsifiers 3 and 4 defeat the proposed all-machine inference. Falsifiers 1 and 2 are discharged at the precise, restricted mathematical scopes below.

## 2. Original prior work and exact novelty

- **LSPV-3/383:** research/coordination/2026-11-03_2124_LSPV3_MONOTONE_MATCHING_SIGN_PROFILE383_FIVE_ROLE_HANDOFF.md; original research/agents/lspv-3/2026-11-03_2124_LSPV-3_MONOTONE_MATCHING_SIGN_PROFILE383.tex. This established the signed-mask monotone matching lower bound and polynomial matching shortcut for an **ordinary CNF** containing width-n, binary and unit clauses. Its source had n^3+n^2+2n clauses and 2n^2 variables. **Retained and credited, not rediscovered.**
- **LSPV-3/519:** research/agents/lspv-3/2026-11-08_1903_LSPV3_QN_MATCHING_STRICT3_PORT519.md converts a *different* hypercube perfect-matching minimal-UNSAT family to strict 3-CNF and proves restricted Resolution bounds. It is not a strict-3 conversion of the LSPV-3/383 sign-profile family.
- **TMR-1/035, /040; TMR-2/040; TMR-4/041; TMR-5/037:** preserve terminal-row fusion guards, compact circuit/witness escapes, the program-oblivious prefix-depth ceiling, and unrestricted transfer OPEN.
- **New relative to those artifacts:** one explicit **canonical, proper three-distinct-variable 3-CNF family** of 2^{n^2} source masks with **exact** formula counts, identical unsigned source-position incidence across *all* masks, a provably superpolynomial monotone SAT/UNSAT sign-profile function, and a *single* polynomial-time mask-authenticating correct SAT decider on **both SAT and UNSAT source members**. The resulting source-profile tariff collapse applies after the width-three conversion. This is a restricted-model negative result, not an unconditional SAT lower bound.

## 3. Explicit strict-3CNF family, machine model and exact size

Fix integer n>=3. Introduce x_ij (match edge chosen) and p_ij (edge enabled), 1<=i,j<=n. Let a in {0,1}^{n^2} mark **disabled** edges, with a_ij=1 disabled. The ordinary source contains:

1. Exactly-one x in each row and each column: one positive length-n clause and all pairwise negative binary clauses per row and column.
2. Each binary implication (NOT x_ij OR p_ij).
3. Each unit p_ij when a_ij=0, or NOT p_ij when a_ij=1.

Replace **each** original clause independently with a proper ternary gadget and globally fresh auxiliary variables:

- A unit (l) becomes the four clauses (l OR y OR z), (l OR y OR NOT z), (l OR NOT y OR z), (l OR NOT y OR NOT z).
- A binary (l1 OR l2) becomes (l1 OR l2 OR y) AND (l1 OR l2 OR NOT y).
- A ternary clause stays unchanged.
- For length k>=4, take distinct fresh y_1,...,y_{k-3} and use

$$
(l_1\vee l_2\vee y_1),\quad
(\neg y_{j-1}\vee l_{j+1}\vee y_j)\quad (2\le j\le k-3),\quad
(\neg y_{k-3}\vee l_{k-1}\vee l_k).
$$

The original clauses all involve distinct variables, and fresh auxiliaries are private to each original clause. Each gadget is satisfiable in its auxiliary wires **if and only if** its original clause is true. When the original clause is false, the binary and unit cases force contradictory helper values, and the long chain forces y_1=...=y_{k-3}=1 and then y_{k-3}=0. If an original literal is true, choose helper bits following the first true literal, obtaining a satisfying extension. Thus existential projection of the strict-3CNF onto x,p is exactly the ordinary source.

Call the resulting source H_{n,a}. It has **exactly**

$$
\boxed{V(n)=n^3+6n^2-6n\quad\text{variables},\qquad
M(n)=2n^3+6n^2-4n\quad\text{three-literal clauses}.}
$$

The calculation uses 2n length-n original clauses, n^2(n-1) row/column negative binary clauses, n^2 implication binaries, and n^2 sign-dependent units. For n>=3, the first class contributes 2n(n-2) ternary source clauses and 2n(n-3) fresh variables. The binary classes contribute 2n^2(n-1)+2n^2 ternary clauses and n^2(n-1)+n^2 helpers. The units contribute 4n^2 ternary clauses and 2n^2 helpers, in addition to 2n^2 original variables.

With dense indices 1,...,V(n), a fixed binary signed-literal encoding gives L(n)=Theta(n^3 log n) encoded source bits. The canonical source order is row gadgets, column gadgets, and per-edge implication/unit gadgets. **All 2^{n^2} masks have literally the same unsigned triple in every clause position**. Only the sign of the four occurrences of the relevant p_ij in each unit-gadget block changes. No clause has a repeated variable; the construction produces no duplicate signed clauses.

## 4. Theorem: exact matching predicate and superpolynomial monotone profile

**Theorem MATCHSTRICT081-A (PROVED/RESTRICTED, peer review OPEN).** For every n>=3 and a in {0,1}^{n^2},

$$
H_{n,a}\text{ is SAT}\iff\operatorname{Match}_n(\mathbf1-a)=1.
$$

**Proof.** Unit gadgets force p_ij=1-a_ij; implications force a selected x_ij to use an enabled edge. Exactly-one rows and columns force the selected edges to be a permutation matching. Conversely any perfect matching gives an x,p assignment satisfying the original CNF, and all independent gadgets have satisfying auxiliary extensions. No witness, auxiliary, or clause is uncharged in the input representation.

Define the UNSAT sign-profile Boolean function on the masks

$$
U_n(a)=\mathbf1[H_{n,a}\text{ is UNSAT}]=\neg\operatorname{Match}_n(\mathbf1-a).
$$

The primary Theorem 1 of Cavalar, Göös, Riazanov, Sofronova and Sokolov, *Monotone Circuit Complexity of Matching*, ECCC TR25-102 (2025, November 6 revision), proves that bipartite perfect matching on an n-by-n adjacency mask requires fan-in-two monotone AND/OR circuit size at least 2^{n^{1/3-o(1)}}. The model is a **nonuniform monotone Boolean circuit on n^2 graph bits**, not a physical machine or a CNF proof system. By De Morgan duality (swap AND and OR, exchange 0/1 leaves), monotone complexity of U_n has the **same** lower bound:

$$
\boxed{S_{\mathrm{mono}}(U_n)\ge 2^{n^{1/3-o(1)}}.}
$$

With the actual encoded length L(n)=Theta(n^3 log n) this is superpolynomial in L, but **only for a function computed by a specified monotone circuit class**. It does not yield a SAT-machine lower bound or an R-mixed proof lower bound. The 3CNF gadget transformation preserves the mask function exactly, so this transfer imports no restricted proof-size preservation assumption.

**Primary source:** https://eccc.weizmann.ac.il/report/2025/102/ , revised 2025-11-06; original ECCC PDF https://eccc.weizmann.ac.il/report/2025/102/download, printed page 1, Theorem 1. The printed theorem gives the precise 1/3-o(1) exponent.

## 5. One fixed both-label correct polynomial-on-family SAT machine

**Theorem MATCHSTRICT081-B (PROVED/RESTRICTED, independent physical compiler audit OPEN).** There exists one finite deterministic multitape machine D that correctly classifies **every** binary string as valid strict-3CNF SAT, valid strict-3CNF UNSAT, or malformed, and uses L^{O(1)} charged transitions on **every** H_{n,a}, for all n and masks a.

**Construction and proof.** Parse the ordinary dense signed-3CNF grammar (malformed inputs receive their declared classification). Count source clauses m. Search 3<=n<=m for m=M(n); there is at most one, since M(n) strictly increases. Regenerate the fixed canonical source clauses except the n^2 sign-unit blocks. At each sign-unit block compare its four exact source clauses with the all-enabled pattern or the all-disabled pattern; require consistency of all four signs and recover one mask bit. A mismatch rejects **template membership**, not SAT. The deterministic source comparison is polynomial and never enumerates 2^{n^2} masks. If authenticated, run ordinary augmenting-path bipartite matching on the recovered adjacency mask and output the exact SAT/UNSAT label. If not authenticated, run a fixed complete exhaustive solver on the original parsed input. Every successful early result is correct by Theorem A, and fallback is correct everywhere else. A source head moves locally, binary counters, parsing, source rereads, template construction, matching, buffering, output and all auxiliary work are charged. Standard direct finite-tape implementations of the enumerated polynomial scans and augmenting-path routine have a fixed polynomial transition bound, with constants independent of n,a. No oracle, advice or unit-cost unbounded word is involved. The exact exponent of a compiled physical machine is not asserted, and actual generated code is not itself a compiled Turing machine.

This is stronger than a constant-label family bypass: among the canonical source masks there are SAT and UNSAT members for every n>=3, yet **one fixed correct total decider** serves all of them in polynomial time.

## 6. Exact fusion-Lipschitz tariff consequence and model transfer status

For any concrete physical configuration C=(F,A,control,input head,work tapes/heads,paid history,interfaces,goal), the native local-head TM transitions have cost one; authentic zero-price SCC closure is the identity. For a nonnegative all-step potential Phi_D satisfying Phi_D(C)-Phi_D(C')<=1 on **every** transition of the *same* fixed correct machine D, and Phi_D(goal)<=0, telescoping along its cheap matching execution gives

$$
\Phi_D(C_0(H_{n,a}))\le T_D(H_{n,a})\le L(n)^{O(1)}
\quad\text{for all }a.
$$

Hence a source-profile component with initial value S_mono(U_n) cannot carry a fixed positive nonnegative tariff weight lambda_mono **without an authentic quotient or offset removing its superpolynomial initial contribution**, since otherwise

$$
\lambda_{\mathrm{mono}}2^{n^{1/3-o(1)}}\le L(n)^{O(1)}
$$

fails for all sufficiently large n. If instead a source-static masked component S_mono(U_n)1[nonhalt] remains frozen until a single unit-cost terminal transition, then that authentic transition has Delta_mono=S_mono(U_n); with an active-bit column Delta_active=1, its exact necessary row is

$$
\lambda_{\mathrm{mono}} S_{\mathrm{mono}}(U_n)+\lambda_{\mathrm{active}}\le1.
$$

For constant length-independent nonnegative weights this forces lambda_mono=0 as n->infinity. This is a **negative tariff falsifier**; it does not present a fabricated complete transition matrix, and does not assert every conceivable dynamical machine-aware obstruction fails. Any one positive source rank/mass claim must pass the *actual* matching path and terminal rule. The exact same-system arbitrary-decider simulation, superpolynomial initial gap, and P versus NP remain **OPEN**.

The old /341 authority remains **FAIL** on its full accepted language and /386 remains **RESTRICTED** to its guarded fragment. Neither is invoked.

## 7. Actual finite execution and hostile controls

**Exactly executed source:** experiments/tmr/tmr1_matching_strict3_profile081.py, SHA-256 6f6c7e48424c1d921dd6543bf1fa370c4762c6282ce1d6ccec58994e46442e60 before publication.

**Original raw stdout:** results/raw/tmr/2026-11-15_0215_TMR1_MATCHSTRICT081_NATIVE_RAW.json, SHA-256 8f494e7678a89d09cd516ca8aafe4863b0d132260a748089e9d1f184e16c1e5c.

Native CPython completed **4,318 assertions, zero failures**. It checked *all 512 masks* at n=3 with an independently coded exact 3CNF DPLL solver against perfect-matching truth, including 247 SAT and 265 UNSAT masks. It checked source incidence identity, exact variable/clause counts, proper ternary distinctness, absence of duplicate clauses and a canonical polynomial template recognizer on 52 masks at n=4 and 20 masks at n=5 (these two larger sets were **not** checked by full DPLL). Every width 1 through 7 gadget truth assignment and all its private auxiliary extensions were exhaustively checked. Partial sign-gadget mutation and deleted-source controls were rejected. Seed 41081 for deterministic sampled masks. No physical TM was compiled and no asymptotic conclusion is inferred from finite runs.

**Mandatory hostile controls:** equality/Horn/dual-Horn/Krom/affine source classes cannot validate a monotone-to-general runtime transfer; a real polynomial matching algorithm is the decisive shortcut. Strict-3CNF auxiliary extensions and shared gadgets are charged in the source length; source sign masks preserve unsigned incidence exactly but permit local fixed-format parsing. Alternate circuits, Gaussian elimination, matching, learned clauses, caching, rereading, arbitrary correct SAT machines and fallback are never deleted as illegal operations. The family is not asserted NP-hard as a promise or impossible to recognize.

## 8. Dependency map, primary provenance and next peer request

| Arrow | Status | Exact issue |
| --- | --- | --- |
| Unit/binary/long independent proper-3CNF gadgets preserve existential satisfiability | PROVED/RESTRICTED | Elementary explicit extension proof; native finite controls |
| Constant unsigned incidence and exact V(n),M(n) for all masks | PROVED/RESTRICTED | Fresh per-source gadgets and fixed ordering |
| SAT(H_{n,a}) iff Match_n(1-a) | PROVED/RESTRICTED | Exact source semantics |
| S_mono(U_n) >= 2^{n^{1/3-o(1)}} | KNOWN THEOREM + proved De Morgan transfer | ECCC TR25-102 Theorem 1, nonuniform monotone circuits |
| Uniform total correct SAT decider polynomial on canonical family | PROVED/RESTRICTED | Standard augmenting-path + authenticated parser; full physical compiler not executed |
| Fixed positive source-profile tariff valid on this same machine | FALSIFIED/RETIRED | Genuine cheap run and terminal overdischarge |
| Arbitrary-SAT-machine fusion potential with superpoly initial gap | OPEN | No dynamic all-step obstruction supplied |
| Same-system R proof bridge, all-machine SAT lower bound, P versus NP | OPEN | Restricted circuit complexity not an arbitrary-SAT lower bound |

**Peer request to TMR-2/3/4/5:** Independently replay the strict source gadget-count calculation and the all-mask source authentication, then attempt to design a *history-dependent* fusion component surviving the matching algorithm's actual paid transitions. TMR-3 should compile/charge a concrete finite-alphabet matching parser; TMR-4 should include this nonmonotone shortcut as genuine MAY behavior before solving any LP. TMR-5 should test a sign-block inconsistency that an implementation may mistakenly accept. TMR-1's next target is a positive dynamic obstruction or an independent validation of a genuinely complete rule-by-component tariff in a different qualified computation.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Governing directive, November 13 replacement, full proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, recovered full proof2 blob 930c5eeddafce656717f28055a7a9a755f44737c, recovered full main.tex blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34, issue #3, AGENTS.md, CODEX.md, repo skill, all five current TMR handoffs and the original related reports/code/data reviewed. No tracker or main.tex change justified; five existing schedules unchanged.
