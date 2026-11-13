# TMR-3: SAME-INPUT-MULTIPASS-TRADEOFF001

**2026-11-13 13:34 PST, America/Los_Angeles.** New TMR-3 Time-Space Tradeoffs agent, j15marti/pnp main. **CANDIDATE symbolic proof, independent TMR-5 review pending; COMPUTATIONAL bounded evidence; P versus NP OPEN.**

## IDEA: resource target and hostile falsifiers

Find a lower bound on *one and the same* correct execution relating information retained, repeated input sweeps, and actual time, rather than multiplying worst-case time from one input by worst-case space from another. The family is the complete encoded strict proper 3-CNF equality construction of TMR-2, not a new or selected hard SAT family.

F1: distinct positive inputs might produce identical communication transcripts; F2: input-dependent pass counts and workspace might defeat same-input counting; F3: omitted control/work-head positions might hide information; F4: free input resetting or arbitrary input access might invalidate scan costs; F5: a similar crossing/communication proof was already published in project history. F1-F3 are handled by a complete scoped symbolic argument below; F4 is an actual unrestricted-model transfer failure; F5 is acknowledged as prior art, with a new *variable-pass same-input product* on the TMR-2 encoding rather than a claim of first discovery.

## Exact strict proper 3-CNF source and fixed machine

Take n>=1 and a,b in {0,1}^n. TMR-2's first 4n clauses force x_i=a_i with the four-clause proper-3CNF gadget

$$
U(\ell;u,v)=(\ell\lor u\lor v)\land(\ell\lor u\lor\neg v)
\land(\ell\lor\neg u\lor v)\land(\ell\lor\neg u\lor\neg v).
$$

The following 4n clauses independently force x_i=b_i. Five disjoint variable banks x,p,q,r,s give N=5n variables and M=8n clauses. The source begins with the explicit unary header 1^N 0 1^M 0; each literal contains one sign bit and a w=max(1,ceil(log2(5n)))-bit zero-based variable identifier. Thus its bit length is

$$
L(n)=13n+2+24n(1+\max(1,\lceil\log_2(5n)\rceil))
=\Theta(n\log(n+1)).
$$

The left clause segment depends only on a, the right only on b; the public header and exact split are shared. The original gadget satisfies U(ell;u,v) iff ell, hence E_n(a,b) is SAT iff a=b. Source construction and first-read lower bound are credited to TMR-2/001; equality and sequential crossing arguments predate this work.

Define the restricted deterministic complete-sweep model M_sweep. One fixed finite total deterministic machine has a single read-only source head and a fixed number b0 of sequential writable tapes with finite alphabets. Each input sweep starts on the left and visits the complete source through its right endmarker, observing symbols only while moving right. A reset between sweeps may return to the left, but all transitions are paid and NO input symbol may be inspected during reset. Halt/output occurs after completing a sweep. Number p_M(x) of sweeps may depend on input x. T_M(x) counts every machine transition. S_M(x) counts all visited work-tape cells on the *same complete execution*, including temporary sign stores, counters, work-head locations, buffers and all touched writable cells. A general correct all-input 3-SAT program is eligible only when it follows this sweep regime on the E_n family. Indexed input jumps, nonmonotone observations, input-copy shortcuts and arbitrary mixed movement are outside the theorem's restriction.

## Theorem TMR3-SWEEP-1: same-input pass-space product

**CANDIDATE (complete elementary symbolic proof, independent review pending).** For every fixed correct M in M_sweep there is c_M>0 such that for every n>=1 there exists a *single satisfiable* source x_n=E_n(a_n,a_n) satisfying

$$
p_M(x_n)(S_M(x_n)+1)\ge c_M n.
$$

Consequently the SAME input satisfies

$$
T_M(x_n)(S_M(x_n)+1)\ge c_M L(n)n
=\Omega_M\left(\frac{L(n)^2}{\log(L(n)+2)}\right).
$$

**Proof.** Alice holds a and can generate the complete left part of E_n(a,b); Bob holds b and the complete right part. Each sweep of M is simulated by Alice then Bob, with Alice sending Bob the complete finite control and all writable-tape contents, visited-cell interval endpoints, and work-head positions at the public input boundary. At the end of the sweep, if another sweep is required, Bob sends the same complete configuration back to Alice, who resets the source head without observing any input symbols. With p completed sweeps there are 2p-1 such boundary messages, ending with Bob's decision.

Let S be total visited writable cells on that very execution. Fixed alphabet and fixed b0 imply that each complete boundary state has a uniquely decodable binary encoding in at most d_M(S+1) bits for a fixed d_M: it stores all S cell symbols, finite control, each work-head coordinate of O(log(S+1)) bits, and work-tape endpoints. The source-head position is the known shared boundary. Encode each variable-length message using a self-delimiting header, including message order, termination, and the number of messages. Then the complete binary serialized transcript tau(a,b) has length

$$
|\tau(a,b)|\le D_M p_M(E_n(a,b))(S_M(E_n(a,b))+1)
$$

for one constant D_M depending only on the fixed program/model, not on n,a,b. Note: this is a communication-simulation *upper bound*, NOT a second physical runtime charge.

For all a the diagonal E_n(a,a) is SAT and M accepts. The 2^n accepting transcripts tau(a,a) are pairwise distinct. Otherwise, if a != b and tau(a,a)=tau(b,b), splice Alice's phases from (a,a) with Bob's phases from (b,b). Equal complete boundary states make the deterministic simulation consistent in every phase and produce acceptance of E_n(a,b), an UNSAT source. Contradiction. This argument remains valid when positive executions use different p or S because an identical complete serialized transcript has the same message boundaries, number of phases and termination.

Only 2^n-1 binary strings have length strictly less than n. Hence one diagonal a_n has |tau(a_n,a_n)|>=n. The previous upper bound yields p_M(x_n)(S_M(x_n)+1)>=n/D_M. Each complete full-input sweep necessarily takes at least L(n) sequential read transitions; resets and computation only add time. Thus T_M(x_n)>=L(n)p_M(x_n), and multiplying by S_M(x_n)+1 proves the stated SAME-INPUT product. QED, subject to independent formal review.

For every specific M and n the witness a_n can depend on M and n. No particular explicit a_n is claimed universally hard, and no worst-case time/space maxima from different machines are combined.

## Explicit upper-bound and adversarial controls

On the **rigid equality promise**, a fixed sequential-sweep implementation captures B selected prefix signs in a B-bit buffer during each complete pass and compares them to the corresponding suffix signs later in that pass. Repeating over ceil(n/B) blocks yields p=ceil(n/B), S=O(B+log L), T=O(p L polylog L), with all binary offset/index computations, reading, rewinds, and buffers charged. B=n gives one pass, S=O(n); B=Theta(log n) gives O(log L) writable cells and O(n/log n) passes. The relation pS=Omega(n) is tight up to counters/constants and exact encoding overhead. An all-input decider must additionally authenticate this promise and execute a correct exhaustive fallback on other formulae. No polynomial worst-case general SAT algorithm is claimed.

**Critical failed transfer:** An unrestricted indexed-read-only-input program checks the canonical source and compares 2n known sign positions with regenerated addresses in O(L polylog L) time and O(log L) writable cells; it need not make ceil(n/B) complete sequential sweeps. The same indexed escape is already documented on a separate K4 equality source by LSPV-4/487. TMR-1's charged source-copy simulator is another reason not to identify original-input rescans with total necessary work. General deterministic Turing machines may interleave backward source moves, copy/transform input, keep algebraic summaries, or compute without the promised pass structure; the present theorem does not cover those machines. The theorem is NOT a representation-independent lower bound and does NOT imply P != NP.

Any class-wise lower bound must survive Horn, 2-SAT, affine/XOR/Tseitin Gaussian elimination, bounded treewidth, sharing, disjoint products, auxiliary variables, renaming, padding and recomputation. Here those are recognized as easy countercontrols, not asserted hard families. A prescribed pebbling DAG or algebraic representation is not forced on an arbitrary decider.

**Literature firewall:** FLMV 2005, Journal of the ACM 52(6):835-865 [1] proves near-linear deterministic SAT time-space exclusions in its specified random-access TM model (for c<golden ratio there is a positive excluded space exponent). It does not bound unknown arbitrarily large polynomial time and space. Guruswami and Onak's multipass-streaming work [2] likewise employs communication lower bounds under explicit pass restrictions. The existing project's LSPV-5/167 used crossing-sequence averaging on a separate sequential head/gap model, so this report claims neither new communication-complexity methodology nor an unrestricted strengthening. The incremental focus here is the *variable* p and S, one-input witness, and exact TMR-2 encoded 3-SAT family.

## Executed tests and reproducibility

Runner path: experiments/tmr/tmr3_multipass_equal3_tradeoff.cjs. Raw path: results/raw/tmr/2026-11-13_1328_TMR3_MULTIPASS_EQUAL3_RAW.json. The published runner was refetched from GitHub and rerun in fresh V8 successfully.

Actual exhaustive finite checks: 1,364 ordered a,b sources for n=1..5, 6,372 retained-sign-batch comparisons, 258 distinct positive transcript signature checks, 516 four-sign-bit opposite-label flips, 20 complete brute-force source satisfiability checks for n<=2, 37,263 assertion groups, and an omitted-sign transcript-collision falsifier. All PASS. Encoded lengths 111, 268, 401, 630, 787 verified. No randomness. For n>2, opposite-label testing used exact sign-block structure and the proved unit-gadget identity rather than 5n-variable exhaustive SAT. This virtual source-sweep emulator is a JS experiment, NOT an OS physical multitape TM trace. Full project preflight/check_research_reports, native Node OS runner, and independent TMR-5 proof review not executed. Finite checks support only COMPUTATIONAL evidence.

## Historical corpus, exact change and peer assignments

Read authoritative new five-role directive first and rechecked before publication; root proof1 (full readable content), proof2 (1,051,196 characters recovered by Git blob), root main.tex (2,479,448 characters recovered by Git blob), issue #3 current comments, AGENTS.md, CODEX.md, pnp-research SKILL.md, TMR-1 and TMR-2 current handoffs and source reports, original LSPV-5/167, LSPV-4/487, LSPV-5 2026-11-09 FLMV model audit, and relevant source-search hits. TMR-3/4/5 predecessor handoffs were absent at this read. The historical LSPV work remains evidence, not an active role directive.

- TMR-1: review the quantified restricted-machine bridge, and do not convert this theorem to the unrestricted target by redefining a pass.
- TMR-2: pursue input-aware *repeated* information necessity surviving rereads, input copying and arbitrary algebraic encoding. The new theorem cannot supply it.
- TMR-4: try the sweep transcripts as a cost-underestimating model only on the declared subclass; any general-machine abstraction must include each omitted head move/representation change.
- TMR-5: independently falsify variable-length transcript injectivity, head-state serialization, source splicing, same-input product, and the duplication/strictness relative to LSPV-5/167.

**Root proof trackers:** P1-01/P1-03/P1-04 and P2-00/A2/D1/C3/B1/B2/B3 remain OPEN. TRACKERS REVIEWED; NO MATERIAL CHANGE. TMR-5 has not authorized a root main.tex TMR-3 region; no change to root manuscript. No agent or schedule modification. All historical reported quantitative bounds retain their original model conditions. P versus NP OPEN.

**Single next target:** find a counterexample or repaired all-transition boundary-accounting method under genuinely unrestricted alternating two-way input access and arbitrary cached/alternative representations. A mere conversion of per-sweep information bounds into an arbitrary-machine time lower bound is NOT permissible.

## References

[1] L Fortnow, RJ Lipton, D van Melkebeek, A Viglas. Time-Space Lower Bounds for Satisfiability. J ACM. 2005;52(6):835-865. https://doi.org/10.1145/1101821.1101822. Original journal abstract inspected.

[2] V Guruswami, K Onak. Superlinear Lower Bounds for Multipass Graph Processing. CCC 2013 / Algorithmica 2016. https://arxiv.org/abs/1212.6925. Original article abstract inspected, applied only as a model-appropriate methodological comparison.

[3] Original project LSPV-5 CROSSING-AVERAGE-QUANTIFIERS167, research/agents/lspv-5/2026-10-26_1648_LSPV-5_CROSSING_AVERAGE_QUANTIFIERS167.tex, blob ae957bc2713c9f21f71c5d9c06cac41e846db6a9. Prior stronger/different sequential-gap crossing argument; no novelty claim for equality.

[4] Original project LSPV-4 INDEXED-EQUALITY-ESCAPE487, research/agents/lspv-4/2026-11-07_2236_LSPV4_INDEXED_EQUALITY_ESCAPE487.md, blob 86c431e06250b1c5cceda129df0a420cd3578f13.

[5] New TMR-2 INPUT-BLOCK-SENSITIVITY001, research/agents/tmr-2/2026-11-13_1315_TMR2_INPUT_BLOCK_SENSITIVITY001.md, blob ccd5734076e214fa68f696eaa21a0448bc6bd21e.

[6] Original project LSPV-5 2026-11-09 random-access time-space theorem audit, research/agents/lspv-5/2026-11-09_1914_LSPV5_MANUAL_RANDOM_ACCESS_TIME_SPACE_THEOREM_AUDIT.md, blob 0f92369fdacb7eb6ff1e7f2fb26320f4291c982e.

END_OF_REPORT::TMR-3::SAME-INPUT-MULTIPASS-TRADEOFF001::2026-11-13_1334_PST
