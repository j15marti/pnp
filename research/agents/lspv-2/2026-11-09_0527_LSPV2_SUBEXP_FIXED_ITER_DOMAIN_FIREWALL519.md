# LSPV-2/519 | Subexponential guest bound is outside the polynomial FLMV contraction domain

**2026-11-09 05:27 PST | Route A primary | PROVED/RESTRICTED elementary upper-envelope calculation; COMPUTATIONAL independent finite controls | P versus NP OPEN.**

**Exact proof-chain IDs:** [P2-A2] universal solver-dependent transformation, [P2-A4] complete physical resource charges, [P2-A5] recursively iterable same-machine closure remain OPEN. Cross-chain [P1-01], [P1-03], [P1-04] and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. [P2-L1-534] is relevant recently published peer evidence, not a proved B3 implication for R_mix341.

## IDEA: target and four falsifiers

**Initial hypothesis:** the October 25, 2026 reported subexponential exact #k-SAT solver can be useful as an algorithmic upper-bound control, but its published upper bound **does not itself meet the quantified input type** of the existing Route-A transformation, which takes a FIXED polynomial-time SAT decider with FIXED FINITE exponents. Even *formally extending* the polynomial-exponent recurrence to the size-dependent exponent of that published upper bound will not produce a constant forbidden-FLMV exponent after any fixed finite number of iterations.

Predeclared falsifiers: **F1** the source actually supplies a fixed polynomial worst-case time exponent for all 3-SAT inputs; **F2** the project's Route-A theorem has already been proved for arbitrary subexponential deciders with changing exponents; **F3** a fixed number of halving steps sends an unbounded initial exponent envelope below a fixed constant; **F4** the argument incorrectly promotes an upper running-time envelope to an actual lower bound. F1 and F2 are unsupported by read sources, F3 is false by explicit algebra, and F4 is a valid qualification explicitly preserved.

## SEARCH: project continuity, primary research and external repositories

Both **complete** current root trackers were fetched: proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters); proof2.txt SHA e7b992dc1137644a95c8f484ad42b7130a1e0e90 (724,924 characters). Examined issue #3 (1,475 comments at review, including LSPV-1/534 and LSPV-3/533), governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md, CODEX.md, and .codex/skills/pnp-research/SKILL.md. Peer resource note LSPV-4/519: research/coordination/2026-11-09_0436_LSPV4_KT_DENSE_FANOUT_FIVE_ROLE_HANDOFF519.md. Also read actual GROKPROOF/2026-11-09_1230_PROGRESS.md (0ee19c6b2fdf92b64427ab737fe563346779c828) and research/agents/claude/world-ledger/README.md (de75a371ce3143a4495e6892df7fb04794a6b708).

Duplicate/prior-art checks included LSPV-2/486 (post-step exponent additive-loss frontier, fafa6a656014c68266a26e464633a2999e501369); LSPV-2/479 (promised exponent extractor no-go, 8b4c8b549ae7445aecb21f2afd7a21cbac4f799a); LSPV-2/484 (rare full-size fallback defeats contraction, 27c5474c0828388d7fffd9836646791b85b1842f); LSPV-2/507 (trace trie); LSPV-2/518 (KT blind linking matrix); LSPV-1/534 (uniform conditional subexponential all-CNF reduction, different fixed proof system). The fixed-point 6/5, exact 1/90 margin and critical root have been known in this project; none is claimed novel.

Original published research: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), DOI 10.1145/1101821.1101822, establishes **polynomial** time/space exclusions in a specified random-access indexed-machine model. OpenAI, *The Exponential Time Hypothesis is False*, dated October 25, 2026, https://github.com/openai/math/tree/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026 and scope note https://github.com/openai/math/blob/main/lean/docs/378.md, declares one fixed k-CNF exact-count machine with a subexponential time bound and polynomial all-prefix visited tape space. Actual checked source: openai/math lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean, whose theorem compiled_exact_count_and_sat imports further proof modules; lean/ComparatorChallenges/SubexponentialSAT.lean (a8d5ff3a3e80323675b1f2d1ea611560b783e9ca) is **a comparator challenge statement containing sorry**, not the proof. No independent Lean build, axioms/assumptions audit or machine replay was performed in this run. Anthropic, anthropics/formal-math/eth/MainResults.lean, contains **definitions only**; its companion claims were not independently built. Neither gives a polynomial all-input SAT algorithm.

Mandatory change-aware external reviews: konard/p-vs-np/README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-machine-model P subset NP, not P vs NP); blkph0x/p-vs-np-proof-research/README.md blob f397a7747eaca82df3d754d0a4b4bab1fe10f814 and METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped algorithms and certificate audits, no universal compiler). Related implementation controls read: MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (distinct external XOR proof system); berkeley-abc/abc and lsils/mockturtle repository metadata. Queries included "subexponential guest contraction finite iteration", "fixed iterations subexponential", "ETH subexponential polynomial exponent", "source-only FLMV", "solver dependent wrapper", and recent primary-paper web searches. The public web search was accessed; a distinct Google-branded client was not.

## ITERATE: a precise, restricted fixed-depth envelope theorem

**Theorem 519.1 (PROVED/RESTRICTED; arithmetic only).** Let n=2^p with p increasing and let N(n)=n(p+1), a representative bitlength scale for a sparse original width-three CNF with Theta(n) clauses and binary variable names. Consider the explicitly *hypothetical advertised upper function*

$$
U(N,n)=(N+1)^d\,2^{C n(\log_2\log_2 n)^2/\sqrt{\log_2 n}},\qquad C>0,\ d\ge0,
$$

with a fixed C,d, and define its upper-bound log-exponent u_0(n)=log_2 U(N(n),n)/log_2(N(n)+1). The actual runtime of the claimed algorithm might be MUCH SMALLER than U; u_0 is not a lower bound.

Elementary calculation gives

$$
u_0(n)=d+\Theta\!\left(\frac{n(\log\log n)^2}{(\log n)^{3/2}}\right)\longrightarrow\infty.
$$

Now consider the **formal upper-envelope recurrence**, which is NOT established as a legal application to this guest,

$$
u_{j+1}=\max\left\{\frac{11}{10},\frac35+\frac{u_j}{2}\right\}.
$$

For u_0>6/5 its exact equality-envelope iterates are

$$
u_j=\frac65+\frac{u_0-6/5}{2^j}.
$$

For each FIXED j, u_j(n) tends to infinity. Thus no fixed-depth application of **this formal arithmetic recurrence to this published upper envelope alone** establishes a constant polynomial exponent or reaches the FLMV forbidden region.

Let ccrit be the unique positive root greater than 6/5 of

$$
c^3+c^2-c-2=0,\quad c_{\rm crit}=1.2055694304005903\ldots,
$$

so beta(ccrit)=1/2 for beta(c)=((c+2)/c^2-c)/2. The equality-envelope necessary number of steps to enter the strict space-s=1/2 region is

$$
j(n)>\log_2\!\left(\frac{u_0(n)-6/5}{c_{\rm crit}-6/5}\right)
=\log_2 n-\frac32\log_2\log_2 n
  +2\log_2\log_2\log_2 n+O(1).
$$

This grows as Theta(log n). **It is not a constructive stage schedule:** the existing Route-A theorem, if it were proved, would apply only to individually FIXED polynomial-time machines with constant exponents; it cannot be iterated on input-size-dependent exponents without a new uniform theorem that specifies code construction, input parsing, all-phase same-machine resources, uniformity of iteration, and correctness. This calculation does NOT exclude a different algorithm, compiler, or a genuinely polynomial bound on the 2026 machine; it says that the displayed subexponential *upper-bound certificate* cannot by itself serve as the hypothesized Route-A polynomial input. Nor does this arithmetic settle P vs NP or ETH validity.

**Correction to the initial idea:** An initial phrase "the subexponential SAT machine is necessarily non-polynomial" would be invalid, because a superpolynomial *upper bound* is consistent with a faster actual implementation. The revised theorem speaks ONLY of what can be inferred from the published numerical upper envelope.

## Established 3-CNF hardness and shortcut ledger

Use the *established* connected cubic odd-charge Tseitin family on a growing bounded-degree expander G_H. Each of H graph vertices v has three incident original edge variables. Encode the parity charge at v by the four proper signed ternary clauses that forbid the opposite-parity local assignments. Exact source: 3H/2 variables, 4H clauses, 12H signed literal occurrences, N=Theta(H log H) bits for explicit binary literal IDs. Global odd component charge certifies UNSAT. Urquhart (1987), *Hard Examples for Resolution*, JACM 34(1):209-219, establishes exponential **ordinary shared-DAG Resolution** hardness for suitable expander families. This is NOT all-algorithm hardness or a lower bound for historical R_mix341.

**Known permitted upper shortcut:** extract vertex equations and XOR all H equations in GF(2), obtaining the explicit 0=1 witness in polynomial work; component parity also gives an efficient SAT/UNSAT classifier and connected-component computations. Source parsing, algebra, exported facets, proof transfer to the fixed calculus and all machine costs are separate obligations. Reingold undirected-connectivity based source-only logspace recognition already appears in LSPV-2/441 and LSPV-4/485, not rediscovered here. No resolution-to-3CNF lower-bound transport is used because this source is already strict 3-CNF.

For finite source regression only, original proper K4 Tseitin CNFs have 6 edge variables and 16 clauses, and all 16 charge patterns were tested, eight SAT/eight UNSAT. K4 is **not** a certified asymptotic hard instance.

## Independent finite experiments and resource ledger

Python with 120-digit Decimal arithmetic executed 73 explicitly counted assertion groups, verified the exact critical beta identity, tested representative p=12,16,24,32,48,64,96,128, and rejected six malformed K4 packets while classifying all 16 proper original K4 sources by exhaustive 64-assignment truth search. Independent JavaScript passed 537 assertion groups, ran a separate canonical DIMACS parser and truth evaluator, and obtained the identical minimum-step sequence: **18,22,29,37,52,68,99,131**. For p=128, eight formal steps still leave exponent envelope about 4.264e34; this is *numerical upper-envelope arithmetic*, NOT an actual solver runtime measurement. SHA-256 of the first original K4 ASCII source: d2947ac9567bd6ed42c5557f2abaccfc69b745b1cdfe29ee7ad761761ea73273.

Executed host work: Python parses and brute-forces at most 16*64=1024 tiny assignments, computes eight critical iteration rows and six format negatives; JavaScript performs the same independent family classification. Both use ordinary host interpreters and bounded number arithmetic. Neither executes an alleged large input, a native FLMV primitive, a general SAT fallback, a full R_mix341 accepted proof, or the OpenAI/Anthropic formal machines. Consequently we assert **NO** measured same-machine time exponent, peak indexed WORK/INDEX high-water, recursive child count, native original-source index/head reads, guest simulation, reference costs or output amortization. Any actual Route A program must charge source, code construction, all child creation/virtual port decoding, guest calls, restart/failure, trace acquisition, caches, memory, verification, output, and simultaneous physical high-water; in particular s'<=max(rho,eta,lambda,lambda*s) including allocate-then-free phases. There is no free optimal derivation or semantic oracle hidden in this experiment.

Executable independent JavaScript: experiments/arc/lspv2_519_subexp_fixed_iter_independent.js, readback blob 571d5eae130d90026c3945011fa07be645813e6f. Raw: results/raw/arc/2026-11-09_0527_LSPV2_519_SUBEXP_FIXED_ITER_RAW.json, readback blob 567cae5ae7d547d09aa5c1e63e4b9e689cf6fb80. The separately executed Python script plus expanded raw data are preserved in the local reproducibility ZIP. No random seeds were used.

## STATUS, files and handoff

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The result is a formal-use/domain caution based on already established recurrence mathematics and does not change node status, dependency or evidenced universal physical applicability. Consequently no tracker edit is warranted. The live root main.tex fetch returned blob fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba but ZERO readable content, so root was **not** partially overwritten. All historical R_mix341 grammar/weights and the FIVE existing 2A/3B agent roles, schedules and enabled states were preserved.

**Actual advance:** explicit arithmetic firewall for the new 2026 subexponential #SAT claims, with independent finite original-source regressions, not a new SAT algorithm or all-machine lower bound. **Precise remaining gap:** construct a total, correct, exponent-oblivious A -> Phi(A) for EVERY fixed POLYNOMIAL SAT decider A on the SAME FLMV machine, prove all-input t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) with fully charged conversion and recursive closure. [P2-A2], [P2-A4], [P2-A5] remain OPEN; Route B full mixed minimum and noncircular B3 remain OPEN. **P versus NP remains OPEN.**
