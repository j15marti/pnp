# TMR-4/049: bounded-knapsack exact tariff for repeatable heterogeneous multi-ID fusion

**2026-11-15 09:36 PST | PNP Cost-Sound Abstraction | KNAPFUSE049**

**Status:** **PROVED/RESTRICTED** symbolic theorem for the precisely defined *preauthenticated singleton-batch record authority*; 381,513 exact finite assertions are **COMPUTATIONAL**, independent mathematical peer review **OPEN**. The all-decider SAT transfer and superpolynomial initial gap are **OPEN**. **P versus NP remains OPEN.**

## 1. Candidate and falsifiers declared before focused review

**Candidate:** TMR-1/048 permits arbitrarily repeatable price-one fusion of **one** unique unpaid gate and one batch. TMR-4/048 permits heterogeneous multi-gate fusion but only **once at the last-gate phase**. Combine the genuinely different permissions in ONE NEW, fully declared record authority: repeatable fusion can consume any allowed width from a finite catalogue B of distinct unpaid gate IDs and exactly one as-yet-unpaid *singleton* AND-scale batch per event. Conjecture that an exact bounded-knapsack fusion credit restores a nonnegative seven-component, all-state cost-sound tariff.

Predeclared falsifiers: **F1** authentic zero-cost VIEW changes the paid identity/AND ledgers or lowers the potential; **F2** a genuine price-one CHECK, BATCH, FUSE_b or HALT overdischarges the corrected potential; **F3** a real low-cost free/undeclared-wide/compact/affine/sharing operation or a non-singleton overlapping batch invalidates the proposed credit; **F4** using these preauthenticated atomic records as if they were actual source-authentic machine microsteps changes the resource model. F1 and F2 are refuted within the qualified grammar by proof plus finite replay. F3 has several **real expanded-system counterexamples** in §6. F4 remains **OPEN** and prohibits SAT lower-bound promotion.

## 2. Recovered source state and antecedents

Read the governing 2026-11-14 Fusion-Lipschitz refocus first (SHA \`54c9177fc211dfca6c94d89d6ebbf3f3908809d6\`), then the 2026-11-13 TMR replacement directive, full proof1.txt, authentic complete Git blobs of proof2.txt and canonical main.tex, issue #3 through TMR-3/048, AGENTS.md, CODEX.md, repository skill, and current five TMR handoffs. The ordinary file Contents responses for proof2/main were **blank**; genuine Git blob retrieval recovered respectively **1,051,196** and **2,545,859** characters. Current root blob SHAs: proof1 \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`; proof2 \`930c5eeddafce656717f28055a7a9a755f44737c\`; main.tex \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\`.

Direct original project materials: TMR-1/048's **repeatable one-gate** fusion rule and exact max(t,tau)+h Bellman result; TMR-4/048 and TMR-5/044's **single late heterogeneous** FUSE tariff; TMR-3/047's fixed-width late-fusion grammar; TMR-2/046's fractional/integral overlapping batch cover; TMR-4/035,/036,/037 zero SCC, directed closure and paid Bellman envelope; TMR-2/048's physical Cartesian-mutant read fusion; TMR-3/048's unequal multihead physical frontier; and LEAD-0029's original semantic-mass/representation falsifiers. These remain prior results with unchanged scopes. **New here** is a fully repeatable, heterogeneous **multi-gate width** catalogue, exact *bounded coin-knapsack* all-state closed form, complete genuine tariff rows and the overlapping-batch failure of naively inserting a set-cover number.

Methodological literature checked: Cousot and Cousot (1977), *Abstract Interpretation*, POPL, DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973); Bellman (1958), *On a Routing Problem*, DOI [10.1090/qam/102435](https://doi.org/10.1090/qam/102435); Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, DOI [10.2307/2273702](https://doi.org/10.2307/2273702). These establish context, **not** our new catalogue theorem or any SAT-machine lower bound.

## 3. Full qualified concrete authority and authentic zero-cost quotient

Fix one immutable, preauthenticated signed source F; a complete shared, authenticated gate/proof DAG D with exactly G distinct global gate IDs; a finite set J of q uniquely identified **singleton** AND-scale batch obligations, with q>=0; and a finite width catalogue B subseteq {1,...,G}, possibly empty. The fully preserved immutable fields also include source provenance, assumptions/discharge Gamma, definitions including affine facts, original/private/exported interfaces, fixed conjunction/branch/join obligations, and resource contract. They are **preauthenticated input to this logical record calculus**, not free machine-derived information.

The mutable complete state is C=(F,D,J,B,P,U,h,v,Gamma,Definitions,Interfaces), where P subseteq D is the globally **once-paid** set of gate IDs; U subseteq J contains exactly **unpaid singleton batch IDs**; h=1 is a distinct unfinished HALT; v in {0,1} is reversible metadata. All valid nonterminal states have h=1. The only h=0 state has P=D, U=empty. Fully completed goal: P=D, U=empty, h=0. A shared gate appearing at several scales is still one ID; **every** singleton batch and required AND obligation must be discharged.

The **exhaustive** rule grammar in the declared authority:

| Authentic rule | Preconditions | Effect | Cost |
| --- | --- | --- | ---: |
| VIEW / NOP | Any valid state | Toggle / retain v only | 0 |
| BAD_REQUEST | Nonterminal | Paid no-op for invalid/malformed request | 1 |
| CHECK(g) | h=1; g not in P | Add exactly g to P | 1 |
| BATCH(j) | h=1; j in U | Remove exactly j from U | 1 |
| FUSE_b(K,j) | h=1; b in B; K subset of D\P with \|K\|=b **distinct** IDs; j in U | In the SAME NONTERMINAL paid action add all K to P and remove j from U | 1 |
| HALT | h=1; P=D; U=empty | h:=0 | 1 |

A repeated FUSE may be genuinely legal if **different** gate and batch IDs remain. There is NO unpriced source access, tape-head positioning, variable-arity physical macro, semantic UNSAT authority, OR-branch cancellation, proof acquisition, Gaussian elimination, compact circuit compilation, or arbitrary SAT decision rule in this grammar. These are **MAY** operations in a wider machine and MUST be retained if physically real.

The actual zero-cost SCC at every ledger state is the reversible v=0/v=1 pair; all zero paths preserve P,U,h and the entire evidence/provenance and cost ledger. The canonical quotient alpha(C) forgets only v. Every actual zero VIEW/NOP maps to the empty quotient path of cost zero. Every paid concrete step maps to the identical quotient edge of exactly its actual cost. This constructs a finite cost-underestimating abstract path for **every** related concrete state and **every** authentic transition, with a related successor, preserved source/ledger and preserved completed goal. It is NOT a simulation of arbitrary SAT deciders.

## 4. Exact bounded-knapsack theorem and proof

Write t=G-|P| and u=|U|. For any finite B of positive integer widths, define the **bounded total fusion capacity**

$$
M_B(t,u)=\max\left\{\sum_{i=1}^{k}b_i:
0\le k\le u,\ b_i\in B,\ \sum_{i=1}^{k}b_i\le t\right\},
$$

where the empty choice contributes zero. Equivalently, the exact dynamic program is

$$
M_B(t,0)=M_B(0,u)=0,\qquad
M_B(t,u)=\max\left(M_B(t,u-1),
\max_{\substack{b\in B\\b\le t}}\{b+M_B(t-b,u-1)\}\right).
$$

All entries are nonnegative **integers**, hence exact rational values. Coin identities may repeat, but every occurrence consumes a **different authenticated batch ID** and b distinct globally unpaid gate IDs.

**Theorem 049-A, all-state Bellman equality.** For every valid state in this exact authority,

$$
\boxed{W_{\min}(C)=t+u-M_B(t,u)+h.}
$$

**Lower bound:** Any terminating authentic trace pays each of the t outstanding gate IDs either by an individual CHECK or in a FUSE, and each of the u outstanding batch IDs by a BATCH or in a FUSE. Let z be the sum of widths of all future FUSE events. The events use distinct gate and batch IDs, so z<=t, number of FUSE events<=u, and therefore z<=M_B(t,u). Every nonterminal paid trace has exactly (t-z) individual CHECK events plus u batch-consuming BATCH-or-FUSE events (possibly extra paid no-ops). Therefore its total cost is at least t+u-z+h >= t+u-M_B(t,u)+h. Zero-price VIEW operations cannot pay an ID.

**Attainment:** Choose an optimal bounded-knapsack list b_1,...,b_k realizing M_B(t,u), assign pairwise disjoint groups of b_i unpaid gate IDs and k different unpaid singleton batch IDs, and execute k authentic FUSE events. CHECK the remaining t-M_B(t,u) IDs, BATCH the remaining u-k singleton IDs, and pay the separate HALT if h=1. The exact cost is t+u-M_B(t,u)+h. This is a genuine legal same-authority completion, not an abstract invented shortcut. Hence equality holds from **all** quotient states, and the potential equals the greatest scalar lower-bound potential with terminal value<=0.

**Special cases and nontriviality:** For B={1}, M_B(t,u)=min(t,u), recovering **exactly** TMR-1/048's max(t,u)+h on singleton batches. For B={2,4}, (t,u)=(5,2), M=4 (not 5), and genuine optimal work is 5+2-4+1=4. For B={2,3}, (t,u)=(5,2), M=5 and work is 3. Arithmetic gaps depend on actual allowed widths and globally distinct unpaid identities, not semantic scale count.

## 5. Nonnegative reduced product, signed all-rule tariff and rational LP dual

The canonical **seven-coordinate** nonnegative obstruction is

$$
\mathbf p(\widehat C)=\left(0,0,u,0,t-M_B(t,u),0,h\right).
$$

Take the exact rational weight certificate

$$
\boxed{\lambda=(0,0,1,0,1,0,1),\qquad
\Phi(C)=u+[t-M_B(t,u)]+h.}
$$

Both active nonterminal coordinates are nonnegative because 0<=M_B(t,u)<=t. For any r:C->C' the signed component discharges are:

| Rule | Delta SEP | Delta Gamma | Delta Machine | Cost |
| --- | ---: | --- | ---: | ---: |
| VIEW/NOP | 0 | 0 | 0 | 0 |
| BAD_REQUEST | 0 | 0 | 0 | 1 |
| CHECK (t->t-1) | 0 | 1-M(t,u)+M(t-1,u) <=1 | 0 | 1 |
| BATCH (u->u-1) | 1 | -M(t,u)+M(t,u-1) <=0 | 0 | 1 |
| FUSE_b (t->t-b,u->u-1) | 1 | b-M(t,u)+M(t-b,u-1) <=0 | 0 | 1 |
| HALT | 0 | 0 | 1 | 1 |

Monotonicity M(t,u)>=M(t-1,u), M(t,u)>=M(t,u-1), and the **fusion-capacity recurrence** M(t,u)>=b+M(t-b,u-1) prove each tariff inequality for **every legal transition**. Signed negative discharges are essential. VIEW/NOP has zero vector discharge. All goals have Phi=0. Telescoping and the all-step simulation prove Phi(initial)<=every genuine paid completion cost.

Because authentic reachable unit CHECK, BATCH and HALT rows separately give lambda_Gamma<=1, lambda_SEP<=1, lambda_Machine<=1, and every other row has positive discharge <=1 in at most one coordinate, the **entire nonnegative active-weight cone** for this grammar is

$$
\boxed{0\le\lambda_{\rm SEP},\lambda_\Gamma,\lambda_{\rm Machine}\le1.}
$$

At a particular initial state the exact primal LP maximizes

$$
u_0\lambda_{\rm SEP}+(t_0-M_B(t_0,u_0))\lambda_\Gamma+h_0\lambda_{\rm Machine}.
$$

The rational primal \`(1/1,1/1,1/1)\` attains W. A matching exact dual assigns rational row multipliers \`(u_0/1,(t_0-M)/1,h_0/1)\` to the respective three authentic **unit-discharge** tariff inequalities, giving upper bound u_0+t_0-M+h_0. This is a row-wise rational LP certificate; independent cheapest genuine traces provide a second upper certificate. No floating-point solver is relied on.

**Physical difference:** Atomic FUSE_b performs b gate-record updates in ONE logical event. This is stipulated by the authority, not proved physically simulable for an arbitrarily large b at unit transition cost. Even bounded b may require prearranged heads and source/record authentication. The exact logical tariff does not count actual source bits, tape head travel, storage, retrieval, serializations, recomputation, or proof formation. A SAT decider need not produce the required output records at all.

## 6. Independently constructed legal shortcut controls

**Overlapping-batch failure, exact smallest illustrative trace.** A naive but incorrect generalization substitutes the *minimum set-cover number* tau_E(U) for u in M_B(t,u) when batches overlap. Take G=4, B={2}, J={a,b}, and E={{a},{b},{a,b}}. The true current tau_E(J)=1, so the naive tariff predicts 4+1-M_B(4,1)+1=4. A legal newly broadened grammar instead performs **FUSE_2(two gates,{a})**, then **FUSE_2(other two gates,{b})**, then **HALT**. Actual cost is **3**. On the FIRST genuine FUSE the naive potential is 4->2, violating its price-one tariff by **2>1**. Both paid events have distinct gate IDs and distinct genuine batch IDs. The failure is structural: an **extra nonminimum batch** may preserve a second profitable fusion opportunity. This is NOT a CEGAR-spurious trace and it does NOT invalidate the singleton-batch theorem.

**Other exact expanded-model falsifiers:**

- A genuine undeclared FUSE_4 for t=4,u=1,B={2} drops original potential 4->1 at price 1 (**3>1**).
- A genuine zero-price FUSE_2 for t=2,u=1,B={2} drops original potential 2->1 at price 0 (**1>0**).
- A compact/affine **direct terminal** at price one for t=4,u=2,B={2} drops potential 3->0 (**3>1**). Such a physical path, if real in an expanded authority, must be retained.
- Signed CHECK control t=4,u=1,B={4}: M=4 before CHECK, but zero at t=3, so genuine CHECK raises potential **2->5**. The legal signed discharge is -3, not an illegally clipped or absolute-valued positive charge.
- Duplicate gate IDs, reused paid gates or previously paid singleton batches cannot be smuggled into a valid FUSE; malformed requests are genuine price-one no-ops. Shared identities are never charged twice. Zero-price metadata cycles do not discharge AND obligations. q=0 and B=empty boundary cases are covered.

Horn, dual-Horn, Krom/2-SAT, affine/Tseitin Gaussian, bounded-treewidth DP, autarkies, equality clouds, compact extension circuits, proof sharing/reconvergence, learned clauses, padding, source rereads, caching, recomputation, arbitrary machine-program selection and alternate source encodings are all **conservative MAY** in the unrestricted model. None of their cheap computations is excluded by this restricted record proof. This is a feasibility audit for one rule grammar, not a general SAT complexity theorem.

## 7. Reproducible evidence and independent verification

Published **self-contained native JavaScript V8 executable**: \`experiments/tmr/tmr4_knapsack_fusion049.js\`, whose serialized \`audit()\` function is precisely the executed function. It uses exact BigInt numerator/denominator rational arithmetic, a dynamic bounded-knapsack recurrence independently cross-checked against brute enumeration, **full authentic gate-ID and batch-ID transition graphs** (not only count aggregates), Tarjan zero-price SCCs in the feature case, exact signed row-by-row rational verification, and a **separate all-state shortest-path Bellman enumeration**.

Executed exhaustive calibration across **128 configuration executions** (including repeated feature stress cases), G from 1 through 5 and q from 0 through 3, including empty and mixed width catalogues. **381,513 assertions; 11,428 nonterminal quotient states examined; 90,432 paid transitions; 22,856 zero-price quotient transition checks; zero failed assertions.** Exactly **20,290 negative-Gamma rows** were deliberately retained; **39,368 genuine FUSE rows** were checked. Finite evidence status is COMPUTATIONAL.

The published feature case G=5,q=2,B={2,4} has **258 concrete metadata-view states, 129 authentic zero-price SCCs and 1,193 complete quotient edges**. Exact primal and dual objectives are both **4/1**, with rational dual (2/1,1/1,1/1). One genuine four-step completion is CHECK, BATCH, FUSE_4, HALT. The machine-readable seven-column matrix contains **all 1,193 concrete quotient paid/zero rule rows**, plus 12 distinct signed row types and their multiplicities. A fresh independent matrix recheck is required before mathematical promotion. No native physical Turing machine or complete SAT proof compiler was executed.

## 8. Dependency ledger and next target

| Required arrow | Status |
| --- | --- |
| Exact qualified preauthenticated singleton-batch repeatable heterogeneous-FUSE grammar, zero SCC and all-step quotient simulation | **PROVED/RESTRICTED**, independent math review OPEN |
| Exact bounded-knapsack all-state Bellman identity and integer/rational tariff | **PROVED/RESTRICTED**, independent math review OPEN |
| Exact exhaustive small-model audit | **COMPUTATIONAL**, all assertions PASS |
| Naive extension to overlapping set-cover tau without tracking activation options | **FALSIFIED/RETIRED** by real two-FUSE trace |
| Native physical source + tape/head + gate-record compiler for heterogeneous FUSE | **OPEN** |
| Any superpolynomial SAT-specific initial fusion gap after algebraic/circuit/preprocessing quotients | **OPEN** |
| Same-system transfer to every total fixed deterministic SAT decider or one qualified native UNSAT proof authority | **OPEN** |
| /341 as general logical UNSAT authority; /386 guarded sibling | **FAIL**; **RESTRICTED**, unchanged |
| P versus NP | **OPEN** |

**NEXT:** TMR-4/050 should investigate **overlapping batch menus with intentional nonminimum covers** via a genuinely complete AND-ledger Bellman recurrence and test whether any useful nonlinear obstruction survives repeatedly fused compact operations in a fully source-authenticated physical program. TMR-1/2/3/5 should red-team the bounded-knapsack source/record interface and identify the earliest real physical multi-ID fusion shortcut.

Publication artifacts:
- \`research/agents/tmr-4/2026-11-15_0936_TMR4_REPEATABLE_KNAPSACK_FUSION_TARIFF049.md\`
- \`experiments/tmr/tmr4_knapsack_fusion049.js\`
- \`results/raw/tmr/2026-11-15_0936_TMR4_KNAPFUSE049_V8_RAW.json\`
- \`results/raw/tmr/2026-11-15_0936_TMR4_KNAPFUSE049_TARIFF_MATRIX.json\`
- \`research/agents/tmr-4/handoff.md\` (current entry prepended, old history preserved)

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No changes to either root proof tracker, root main.tex, TMR agent identities, ownership or schedules.
