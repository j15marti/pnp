# LSPV-4/480: Exact FLMV contraction exponent-slack audit and all-phase cache firewall
**2026-11-07 15:40 PST | Route A resource auditor | PROVED/RESTRICTED elementary exponent lemma; COMPUTATIONAL controls | P versus NP OPEN**

**Affected proof-chain node:** [P2-A4]. Related OPEN [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04]. Route B [P2-D1], [P2-B1], [P2-B2] unchanged. Do not reinterpret this numerical lemma as a SAT algorithm or universal complexity separation.

## IDEA -> SEARCH -> ITERATE
**Initial hypothesis:** The nominal recurrence leaves very unequal room for extra *physical* costs: substantial local-time slack, but only about 0.0028 exponent slack in the total number of child calls, about 0.0023 in child-size exponent, and 1/90 in space. A compiler retaining all its q distinct child answers in a materialized q-bit table violates the nominal space limit when q is Theta(N^(3/5)).

**Predeclared falsifiers:** (F1) the recurrence fixed point is not max(rho,a/(1-lambda)); (F2) beta is not decreasing around the target; (F3) the calculated call/size thresholds disagree with direct finite iteration; (F4) a claimed cache-space obstruction persists for a streaming, compressed, or recomputing implementation. F1-F3 were not found. F4 is an essential restriction: the obstruction applies to an *explicit* q-bit materialized answer array, not all valid implementations.

**Read actual project sources:** Complete proof1.txt and proof2.txt, issue #3 and recent comments, governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, research/coordination/2026-11-07_1440_LSPV4_EXPANDER_LAYOUT_FIVE_ROLE_HANDOFF479.md, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-2/477 and /478, GROKPROOF/2026-11-07_1920_PROGRESS.md, Claude ONETAPE-0001 and WORLD-LEDGER-0001. Root main.tex is very large and has not been authenticated as a complete readable blob; no root manuscript edit was attempted.

**SEARCH, source checks:** Fortnow--Lipton--van Melkebeek--Viglas, JACM (2005), Sections 2.1 and 5, specifically Corollary 5.8, primary author PDF https://lance.fortnow.com/papers/files/tst.pdf, PDF page 4 (machine) and page 18 (corollary) inspected by source screenshots. Van Melkebeek, survey TR07-099 (2007), https://eccc.weizmann.ac.il/eccc-reports/2007/TR07-099/ . Existing cubic-expander odd-charge Tseitin 3-CNF ordinary Resolution control: Ben-Sasson--Wigderson, JACM (2001), Cor. 4.5. This last theorem is a **Resolution proof-size** lower bound only and does not enter the recurrence calculation. In the direct original encoding, H graph vertices give 4H 3-clauses, 3H/2 edge variables, N=Theta(H log H); an independently authenticated GF(2) sum is a polynomial shortcut. No hardness transfer to arbitrary machine time is asserted.

**Repository evidence with exact paths:** konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3 (finite one-tape model, not an indexed-FLMV equivalence); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (bounded/promise research ledger, no universal transfer); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (exact graph-parity construction); meelgroup/frat-xor/README.md blob 38a137bc (certificates for separate proof format, not native R_mix341); openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (verification statuses, no applicable same-machine compiler). No Google-branded search interface; web search and GitHub connector actually used. No native FLMV machine execution or official mixed checker claimed.

**ITERATION:** Recast the desired resource claim as a *four-parameter quantified admissibility test* for all phases, and isolate an explicit table-materialization failure. This is a diagnostic for LSPV-2 rather than a proposed universal splitter.

## Theorem 480.1: exact eventual-entry budget (PROVED/RESTRICTED)
Consider a *fixed* deterministic all-input recursively iterable transformation on the same FLMV machine whose **fully charged** resource exponents satisfy, for some fixed a>=0, 0<lambda<1, rho>=1, eta>=0 and n^o(1) multiplicative factors,

$$
t_{j+1}\le \max\{\rho,a+\lambda t_j\},\qquad
s_{j+1}\le \max\{\eta,\lambda s_j\}.
$$

The displayed space law assumes **sequential depth-first calls with all retained caller frames counted**, not q simultaneously live guest states; sources, input index, output, parsing, local failed policies, conversion, retrieval, cache, replays, high-water, and copying are covered by rho and eta. Let

$$
t_\infty=\max\{\rho,a/(1-\lambda)\},\quad s_\infty=\eta,\quad
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right).
$$

For every pair of initial finite exponents (t_0,s_0), the equality-recursion *upper envelope* eventually enters the strict forbidden FLMV region if and only if

$$
\boxed{\eta<\beta\left(\max\{\rho,a/(1-\lambda)\}\right).}
$$

This is an iff for **eventual entry of the upper-envelope recurrence for all initial exponents**, NOT an equivalence for a particular realized algorithm, whose actual costs may lie strictly below these upper bounds.

**Proof:** For g(t)=max(rho,a+lambda*t), |g(u)-g(v)|<=lambda|u-v|. Its unique fixed point is max(rho,a/(1-lambda)); for h(s)=max(eta,lambda*s) the unique fixed point is eta. Hence equality iterates from any finite t_0,s_0 converge geometrically to (t_infty,eta). For c>0, beta'(c)=-(1+1/c^2+4/c^3)/2<0, so beta is continuous and strictly decreasing. If the displayed strict inequality holds, continuity supplies a neighborhood entirely inside s<beta(t), which all iterates eventually enter. If it does not hold, choose t_0=t_infty,s_0=eta: this is a fixed point and does not enter strictly. QED. Under the full **hypothetical** all-input, same-machine assumptions, such an interior point would contradict FLMV Cor. 5.8; therefore those assumptions cannot jointly hold for an algorithm-independent oracle-extensional solver, as already clarified by LSPV-2/478. Nothing here proves the transfer exists.

## Theorem 480.2: exact numerical phase budget
At (a,lambda,rho,eta)=(3/5,1/2,11/10,1/2), t_infty=6/5, beta(6/5)=23/45, margin=1/90. Let c_0 be the unique root >1 of

$$c_0^3+c_0^2-c_0-2=0,\qquad c_0=1.2055694304005903\ldots.$$

With the other nominal parameters fixed, the **strict** thresholds are:

| Changed parameter | Strict threshold | Permitted extra exponent |
|---|---|---|
| Total child-call exponent a | a < c_0/2 = 0.6027847152002952... | < 0.0027847152002952... |
| Maximum child-size exponent lambda | lambda < 1-(3/5)/c_0 = 0.5023098754249018... | < 0.0023098754249018... |
| Local time exponent rho | rho < c_0 | < 0.1055694304005903... from rho=1.1 |
| All-phase live space eta | eta < beta(6/5)=23/45 | < 1/90 from eta=1/2 |

If both eventual time and space exponents increase by the **same** delta, the root of beta(6/5+delta)=1/2+delta is delta=0.0037059012205234... . These are *one-at-a-time* margins unless otherwise stated; simultaneous costs must be evaluated using Theorem 480.1. Rounding to equality is invalid because strict entry is required.

**Physical cache firewall (PROVED/RESTRICTED):** A representation that explicitly materializes q=Theta(N^(3/5)) separate one-bit answers in simultaneously resident writable cells uses Omega(q)=Omega(N^(3/5)) working space, so violates eta=1/2 and, at t=6/5, exceeds beta(t)=23/45. This is a lower bound for that particular physical representation only. Streaming OR/AND, compressed answers, legal delayed recomputation, and independent source/guest indexing may avoid the table; no lower bound against these alternatives is inferred.

## All-phase ledger: what is proved versus still missing
**Exponents computed** from the abstract recurrence only: q=N^(a+o(1)), child length <=N^(lambda+o(1)), local time N^(rho+o(1)), retained total peak N^(eta+o(1)), including caller frames. Explicit child construction across q calls may consume N^(a+lambda+o(1)) time and must be in rho; at the nominal point a+lambda=11/10, right at local-time ceiling. A full q-answer table costs N^a live bits unless deallocated or compressed.

**Not established on the native FLMV machine:** source parsing, input/INDEX head relocation, address generation, large numerical IDs, intermediate full buffers, local failed policy search, prefix/certificate verification, guest work/index semantics, child materialization or virtual transducer, per-guest output, cache lookup, copy/replay/recomputation, physical high-water and simultaneous ancestor/child live sets. An abstract exponent ledger cannot substitute for a literal machine implementation. An algorithm must include each category in a specifically verified rho/eta bound; source-only, output-only and promise-grammar variants cannot claim [P2-A2].

**Finite controls (COMPUTATIONAL):** Independent Python Decimal/Fraction audit and JavaScript V8 audit each checked 3,000 pseudorandom parameter tuples for convergence, seven near-threshold adversarial tuples, 16 original signed K4 cubic Tseitin 3-CNF charge vectors (eight SAT with exactly eight models each, eight UNSAT), and four corrupted/out-of-family packet controls; **3,027 assertion groups each**, with no failures. Under t_0=s_0=1000, nominal entered at step 18 and a barely interior threshold example entered at step 29. These numerical checks neither prove native bounds nor certify a growing hard family.

## Role boundary and remaining gap
This algebraic resource budget strengthens [P2-A4] only as an independent **resource-feasibility test**, and is distinct from the already established LSPV-2/478 answer-only no-go. The governing exact R_mix341 grammar and weights are unchanged, and this report does not address Route B's all-mixed minimum or noncircular B3. The unresolved step is to provide a solver-**intensional**, all-input, recursively iterable, native FLMV construction whose actual ALL-PHASE exponents lie strictly inside this budget for every fixed total correct SAT decider. P versus NP OPEN.
