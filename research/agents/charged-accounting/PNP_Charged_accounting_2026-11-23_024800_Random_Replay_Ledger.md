# Random bits, cumulative descriptions, and repeated charges

23 November 2026, 02:48 PST (America/Los_Angeles). PNP Charged Accounting.
**RANDOM-REPLAY-LEDGER1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT**, restricted model accounting and explicit counterexample; independent review pending.
P versus NP **OPEN**.

## Dependency and claim

Discovery's checkpoint report [1] correctly warns that randomized replay requires consumed coin bits. This run supplies the explicit same-execution ledger and a zero-error counterexample to extending the deterministic minimum-description ceiling unchanged. The replay upper bound itself was already stated in [1]; it is not claimed as new. The new deliverable is its necessity as a model distinction, with actual events, a full-cost wrapper on the calibrated map family, and the reuse correction for repeated descriptions of the same random string.

Fix a machine A before choosing an input or random stream. The model is the project's finite-alphabet, single-head, unit-motion writable tape, now optionally permitting one independent fair bit per charged transition. Input/work/output and retained seeds occupy that tape; no free external source, clock or uncharged random tape is allowed. Configurations are charged after transitions. The fresh-coin source is specified probabilistically, not part of the finite stored configuration; its unread independent future bits are not included in C_t. The deterministic model is the zero-coin specialization.

Four falsifiers: omit consumed coins from replay; condition on a full seed without charging its description; charge the same coin-generation event at every later snapshot with reuse one; or infer problem hardness from optional random padding. All four are rejected below.

## Replay ceiling with complete information

For every fixed A, input x of length N, and finite realized run, let R_t be the number of random bits consumed through transition t, with actual prefix omega_[R_t]. Supply a self-delimited encoding of x, t, R_t and these bits to a fixed replay interpreter. Each transition is determined and C_t is reconstructed. No oracle or efficient shortest-description algorithm is required. Consequently,

K(C_t | A) <= N + R_t + O_A(log(N+R_t+t+2)),

CM_min <= O_A(TN + sum_(t=1)^T R_t + T log(N+T+2)).       (1)

Here R_t<=t, hence CM_min=O_A(T(N+T+log(N+T+2))). Input length and transition index are paid fields. A supplied s-bit seed generating all choices instead gives O_A(T(N+s+log(N+T+2))); a long pseudorandom expansion does not create fresh independent description bits.

The physical ledger remains S=O_A(N+T) and CM_phys=O_A(T(N+T)). For deterministic A, (1) reduces to the existing O_A(T(N+log(T+2))) ceiling. Under a fixed cap T<=K N^a, a>=1, the deterministic ceilings remain S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)). The general fresh-coin description ceiling is instead O(N^(2a)). This does not change the deterministic count-map circuit bound O(N^a log N) or any deterministic transport theorem.

## A fixed zero-error machine showing why the distinction matters

Use the authenticated map family in the transport report [2], not a new formula family. It has n=8r-1, m=10r, w=ceil(log2(8r)) and

N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

Its explicit source contains unary n, gamma(m+1), ordered signed triples, both local witness assignments and the release-variable identifier. It is UNSAT exactly when the two encoded maps f,g agree. Both labels occur. Section 9 of [2] proves a fully paid O(N^2)-time, O(N)-span sole-tape guard and family decision procedure, including exact pattern/ID/witness/end validation. Its theorem retains internal-review-only status.

First define the total language L_map consisting of recognized canonical sources with SAT label. A deterministic machine D applies that guard, returns the appropriate label on an admitted source, and rejects every guard miss. Thus D decides L_map on all strings in O(N^2) time. This auxiliary language is explicitly not claimed NP-complete. Alternatively, on valid nonfamily SAT inputs use a total exhaustive fallback; this gives an all-SAT-correct solver with a polynomial guarantee only on the admitted family.

Build one uniform zero-error randomized machine A as follows. Run D and cache its single verdict at the origin without yet halting. Retain the original input. Clear the O(N) negative work region if needed, compute L=max(2,N)^3 in binary, then generate L independent bits into a dedicated track at cells -1,...,-L. Put delimiters at the origin and left end. Return the head to the origin without erasing the random track, then write the cached verdict and terminator and halt.

There is no hidden random-access counter: use a second track holding a marked O(log L)-cell binary counter beside the head. For each new random cell, update the counter by a full local sweep and shift that counter block left one cell, leaving the coin track unchanged. This takes O(log L) unit transitions per generated bit. Moves, shifts, carry work, initialization, counter bits and the return trip are paid. Computing N from the actual finite input and its binary cube costs polynomially less than the O(N^2) guard for large N; forged declarations do not control allocation. Small inputs are handled by fixed control.

For all inputs of L_map, for every random stream, the resulting pathwise tariff is

T=O(N^2+L log L)=O(N^3 log N),
S=O(N+L)=O(N^3),
CM_phys=O((N^2+L log L)(N+L))=O(N^6 log N),
CM_min<=O(N^6 log N).                                  (2)

All random outcomes produce the correct answer. The full-SAT fallback version has these bounds on the map family; outside it, no polynomial time guarantee is asserted. Its ordinary exhaustive fallback remains exponential. This distinction prevents a family algorithm from masquerading as P=NP.

## Actual residence events and the minimum-description lower bound

Fix any one input x, hence N and L. Let R be the uniform L-bit generated string. Select exactly L actual return-trip transitions, after generation and before origin output. Their timing and head locations depend on x and N but not on the values in R. At every selected post-transition configuration C_j, the marked coin track still contains all of R. Therefore R -> C_j is injective, with exactly 2^L equiprobable configurations.

For each fixed j, shortest prefix descriptions of those configurations form a prefix-free code. Kraft's inequality gives E_R K(C_j|A)>=H(C_j)=L. Summing the L distinct actual events yields

E_R CM_min,A(x) >= L^2 = Omega(N^6).                    (3)

This is a same-run residence sum, not time times an unrelated peak. No empirical estimate of Kolmogorov complexity is used. Likewise every selected configuration spans at least L cells, giving CM_phys>=L^2 pointwise. The argument is valid on either label.

Equations (2)-(3) refute the universal randomized extension CM_min=O(T(N+log T)): its proposed right side is only O(N^4 log N). More concretely, A has a fixed pathwise cap T<=K N^4, yet its expected CM_min is Omega(N^6), which cannot satisfy the deterministic a=4 ceiling O(N^5). This is a counterexample to the extended resource claim on a polynomial-time total decision machine, not a lower bound on the complexity of L_map.

Replacing every generated bit by zero produces a deterministic machine with the same movement schedule, correct verdict and physical span, but with descriptions reconstructed from x and t. Omitting the entire padding phase gives back D. Thus the high information residence is optional and supplies no compulsory SAT work.

## Shared compulsory-work ledger: the reuse factor is L

For clarity, instantiate the requested entropy formula on the actual padded execution. Let j range over the L return snapshots; U_j=R; B_j=(A,x,L,j,public schedule), excluding R. Let Pi_j be the same chronological L-bit coin record for each j. It is fixed-length and therefore conditionally prefix-free, and it exactly decodes U_j. Let E_j be the set of the L actual earlier coin-generation transitions. Then b=1, h_j=0, and rho=L, because every coin-generation transition is reused in all L records.

Thus sum_j H(U_j|B_j)=L^2, but the valid whole-execution formula gives only

E[T] >= L^2/(1*L)=L.

Setting rho=1 would falsely turn repeated retention into new generation. The real L^2 cumulative-description bound uses distinct return configurations as in (3), not fresh coin records at each return step. If the ledger is restricted to the post-generation suffix, the earlier generation events are unavailable; putting the retained R into B_j makes H(U_j|B_j)=0. No decoder may query that retained string for free while omitting it from both side information and events.

This explicitly distinguishes a code for the whole state, source discrimination, random generation, and unavoidable decision work. The padded machine creates R because its fixed program elects to, not because correctness requires R. The missing necessity premise is still a proof about every permitted correct solver after paid joint preprocessing.

## Primary-source check and fresh official searches

Fresh literature queries:
- Beame Kornerup cumulative memory complexity randomized algorithms space 2301.05680
- prefix Kolmogorov complexity expected length uniform random string incompressibility

Read Beame and Kornerup, *Cumulative Memory Lower Bounds for Randomized and Quantum Computation*, arXiv:2301.05680v2, 26 June 2023, §2 [3]. Their leveled branching-program CM sums log layer widths, with arbitrary query patterns and a read-only-input abstraction. It is not the per-realized-configuration prefix complexity used here. No sorting, matrix, quantum, or generic transfer theorem is imported into Boolean SAT. Kraft's counting argument is given directly above; search snippets on incompressibility are not used as unverified theorem imports.

Fresh GitHub searches used the exact query "random bits space complexity" separately within anthropics, openai, xai-org, google, google-research and google-deepmind. xAI first returned HTTP 429 with a six-second retry interval, then a later retry returned no results. This transient failure did not block the run. Results and scope:
- anthropics/formal-math, commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/MainResults.lean search excerpt: input encoding and zero-random-bit specialization; no new CM theorem. Broader ETH claims not imported.
- openai/math, commit 4eaee87548250b2682affda7d05d947c05554bae: fetched lean/OAI/Computability/RandomMean/Main.lean, blob 3a704090bf1117948a4afa153266b55f20b85e13. Correct-probability/count statements explicitly index finite random bit functions. No dependency/kernel build or SAT/CM theorem transfer performed.
- xai-org: no matching result after retry; no exhaustive absence claim.
- google/or-tools, commit 5bd5b1a0884af6c7a0d384d33723b1236b1a98ed, ortools/util/random_subset.h search excerpt: sampling routine, not a compulsory-work theorem. Google Highway random generator excerpts were likewise not a proof.
- google-research/google-research, commit 87e25a5ba04d2c4cf0108f0cec96d648fe2b945a: quantum_sample_learning and factoring_sqif README excerpts concern other tasks; no exact tape-ledger theorem found.
- google-deepmind/formal-conjectures, commit 2207c54d0dbe960de591d280f997b195bf3f6e28: fetched FormalConjecturesForMathlib/Computability/Complexity.lean, blob 9371e7702155d651bbd32ccff3e3bddf4146dcc6. It supplies complexity definitions, not certification of the needed resource necessity. No formal build was run.

Official ownership was checked through the organization pages and their publisher domains: verified anthropics/anthropic.com and openai/openai.com; x.ai/news/grok-os linking xai-org; Google's official organization guidance at opensource.google/documentation/reference/github/where; google-research and google-deepmind profiles linked to research.google and deepmind.com. These pages were freshly retrieved; prior run's ownership checks supply the matching provenance. No Verified badge is claimed for the latter two. Product-name third-party repositories were not treated as official.

## Recovery, limits, and receiving dependency

Starting revision: 4736fc0fdeb5ad7906558f32daaf477f0d79bea6. Recovered governance, repository research instructions, dynamic continuation, exact transport model/encoding/upper bound/static ceiling, T5 §§5-6 and 15, all six handoffs, own forest audit and original Discovery checkpoint report. The current issue's latest three comments were checked. Duplicate search "random coins minimum description cumulative padding" returned no matches; branch-name search "charged" returned none. Neither query is an exhaustive repository/draft audit.

This run is a symbolic proof and counterexample, not a finite experiment. No old experiment was repeated, no shortest-description value was computed, and no native parser/tape or proof-assistant kernel implementation is claimed. No complete checkout was available for preflight. Historical manuscripts and other roles' files remain untouched. The calibrated permutation-family theorem is unchanged and retains its single-tape/internal-review scope.

DISJ/both-label sanity PASS via the recognized map family. Same-execution DTISP PASS in the displayed tariff. Deterministic configuration gate PASS only with its original deterministic premise; the randomized extension without coins is FALSIFIED. Relativization/algebrization/Natural Proofs progress toward separation remains OPEN; none is claimed. The original affine/Tseitin, complement, private-leaf, forced-domain and cache controls remain intact. The construction creates no counting-to-decision implication.

**Next owner Bounds, receiving Synthesis:** any proposed high-description obligation must rule out merely self-generated randomness and establish its necessity from correctness for every solver. Use deterministic ceilings for deterministic runs, and explicit coin/seed descriptions for randomized extensions. **Redteam bypass target:** remove or deterministically replace the random-padding phase and check that the authenticated cached decision survives unchanged. Discovery receives the completed accounting of its coin warning. The first unresolved mathematical premise remains unavoidable computation after complete source acquisition and joint caching.

[1] [Discovery checkpoint error mass](https://github.com/j15marti/pnp/blob/7bcd01e1df3ae0d345a8b20fb799d206a436f490/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-23_015200_Checkpoint_Error_Mass.md).
[2] [Transport model and polynomial control](https://github.com/j15marti/pnp/blob/4736fc0fdeb5ad7906558f32daaf477f0d79bea6/research/main/Charged_UNSAT_Transport_2026-11-21.md), §§2,5,9-11.
[3] [Beame–Kornerup primary PDF](https://arxiv.org/pdf/2301.05680), v2, §2.
