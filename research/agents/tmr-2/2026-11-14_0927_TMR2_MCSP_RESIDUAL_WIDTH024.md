# TMR-2/024: Exact MCSP prefix-residual ceiling and update-time firewall

**Pacific date:** November 14, 2026, 09:27 PST. **Role:** TMR-2 Information Necessity. **New scope:** CANDIDATE/RESTRICTED with complete elementary proof pending TMR-3/TMR-5 independent review. **Finite tests:** COMPUTATIONAL, native CPython. **Unrestricted P versus NP:** OPEN.

## 1. Exact problem, prior work and theorem ledger

This run first read research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md (SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), followed by the November 13 TMR replacement directive. For ordinary decision MCSP[s] the input is a complete N=2^n-bit truth table; n is the circuit input arity, N is the truth-table bit length, and L is a distinct SAT formula encoding length. The finite circuit basis here is fan-in-two AND/OR, unary NOT, unbounded fanout; size counts gates.

| Primary paper / theorem | Model and exact relevant claim | Transfer barrier |
|---|---|---|
| Cheraghchi, Hirahara, Myrisiotis, Yoshida (CHMY), STACS 2021, Theorem 1 | Decision MCSP[N^mu1], one-way read-only input and one two-way read/write work tape. For sufficiently small fixed mu1>0, deterministic time N^1.01 lower bound implies P!=NP. | The low-mu1 lower-bound premise remains OPEN. |
| CHMY, Theorems 2,3 and parameter bound | For a **larger** fixed mu2, randomized two-sided-error near-N^1.99 lower bound on the same specified one-work-tape interface, plus short-oracle/parameter variants for 1/2<mu'<mu<1. | Different size threshold means DIFFERENT decision language. High-mu2 lower bound does not meet low-mu1 magnification hypothesis. |
| CHMY, Theorems 4,5, Corollary 7 | MKTP branching-program results and **full-threshold-input MCSP** BP lower bounds, including read-once, co-nondeterministic or parity variants. | Full-threshold MCSP is not one fixed MCSP[s] slice; BP size is not physical TM time. |
| McKay, Murray, Williams (MMW), STOC 2019, Theorems 1.2,1.3 and Section 4 | One-pass **search**-MCSP^A on N=2^n input, s(n)>=n, Sigma3SAT^A oracle, oracle-relative total time N tilde-O(s), update tilde-O(s²), workspace tilde-O(s). Excluding **both** polynomial-in-s space and update for every uniform deterministic full search-MCSP^A machine with appropriate A in PH would imply P!=NP. | Oracle calls are not free in ordinary machines; space-only or decision-only bounds are insufficient. |
| Oliveira, Pich, Santhanam, Theory of Computing 2021 | Nonuniform circuit magnification for Promise Gap-MCSP with two explicit circuit thresholds and all sufficiently small beta, yielding NP not in P/poly under its stated hypothesis. | Gap/promise and nonuniform conclusion differ from CHMY. |
| Oliveira, Santhanam, FOCS 2018 | Small-threshold MCSP **formula** magnification. | Formula lower bound is not general TM time or unrestricted circuit lower bound. |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, ITCS 2020 | Locality and natural-proofs barriers for specified magnification proof methods. | A proof-method barrier, not an all-algorithm impossibility. |

Originals: CHMY https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23 ; MMW https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf ; OPS https://theoryofcomputing.org/articles/v017a011/ ; Oliveira-Santhanam https://eccc.weizmann.ac.il/report/2018/139/ ; locality paper https://eccc.weizmann.ac.il/report/2019/168/ . Source theorem models were checked; no cross-variant reductions are presumed.

**Original repository comparisons:**
- research/main/2026-10-19_2148_MAIN_REPRESENTATIVE_MAINTENANCE_CEILING5.tex (SHA 9262d06c51e8cc4690a77be92e4d6d9192cce595): PRIOR exact uniform one-pass full search-MCSP maintains one consistent circuit in O(s log s) space, but uses 2^{O(s log s)} update time.
- research/agents/magnification-redteam/2026-10-19_2347_REDTEAM_MINFREE_SIGMA2_MERGE17.md (SHA 6b716348721f87ad0331c1fdb1a2b56d7693d39b): PRIOR Sigma2^{P,A} oracle-relative representative replacement, no unconditional poly(s)-update.
- results/raw/separation/2026-10-19_2124_FULL_MCSP_PREFIX_CEILING15_MIN.json: PRIOR 40 and 90 YES functions independently confirmed in this run; full original narrative publication had been blocked.
- research/agents/threshold-descent/2026-10-18_1204_THRES_ENTROPY1.tex: injective/recoverable bounded-fiber entropy ceiling, not a many-to-one reduction no-go.
- research/agents/magnification-redteam/2026-10-18_1919_MAGRED_STREAM_NO10.md: NO-preserving coordinate sampling can destroy source YES completeness; preserve true accepted counterexamples.
- research/main/2026-10-18_ASYMPTOTIC_CONE5.md: cofinal slope-gain criterion only conditional on actual low-parameter bounds.
- Original Claude ONETAPE-0001 and DIRECTPRODUCT-0001: transport bottlenecks and unsupported unconditional HSG derandomization. Current TMR-1/023 shell, TMR-2/022 Walsh, TMR-3/023 GF4 factorization, TMR-4/023 moments and TMR-5/020 GF4 cancellation provide cheap compact-representation hostile controls.

**Genuinely new relative to this corpus:** an exact **all-cut, every-prefix, every-fixed-order** residual-equivalence ceiling with independently generated minimized OBDD widths and complete two-label transition replays. The broader space-only information ceiling and representative algorithm are PRIOR work, not new discoveries.

## 2. Exact positive-support residual theorem

Let a nonempty language Y subseteq {0,1}^N have M=|Y| accepting source strings. Fix ANY permutation pi of N source coordinates. After reading i bits in pi-order, define the future-language residual of prefix p as

$$
R_i(p)=\{z\in\{0,1\}^{N-i}:pz\in\pi(Y)\}.
$$

**Theorem RES24 (elementary proof, peer review pending).** At every cut i=0,...,N, all 2^i legal prefixes together have at most M+1 distinct right residuals. Their quotient defines an exact deterministic **ordered read-once branching program** of width <=M+1 at every layer and at most (N+1)(M+1) layer states total, for ANY fixed coordinate order, with correct YES and NO terminals.

**Proof.** If R_i(p) is nonempty, at least one y in Y begins with p. Different prefixes correspond to disjoint nonempty subsets of Y, so at most M different p have nonempty residual. All remaining prefixes have the same empty residual. Thus at most M+1 distinct residual sets occur. If R_i(p)=R_i(q), both outgoing transitions are well-defined: for b=0 or 1 the common residual after reading b is {z:bz in R_i(p)}. At final cut N, an accepting residual is exactly {empty string}; rejecting residual is empty. Hence all transitions and both terminal labels are exact. QED.

For ordinary fixed-threshold MCSP in our fan-in-two gate basis, the number M(n,s) of YES truth tables is bounded by the number of ordered gate descriptions:

$$
M(n,s)\le D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$

Consequently

$$
\log_2(\mathrm{width}) \le O(s\log(n+s)).
$$

At s>=n this is O(s log s); for a fixed small circuit exponent s=floor(N^mu), 0<mu<1, it is O(N^mu log N), which is polynomial in s. A **positive-prefix residual count/fooling set alone cannot prove a superpolynomial-in-s workspace requirement** for fixed-threshold ordinary MCSP in this specific read-once semantic-state model. All rejected NO sources share one empty terminal residual.

**Nonuniform-versus-uniform firewall.** A residual quotient is an EXISTENTIAL state graph and its transition table may require exponentially many description bits; uniform construction and updates are not free. Attaching a preselected witness circuit to each accepting terminal gives a nonuniform search-output automaton, not a uniform polynomial-update search-MCSP machine. The previous representative-maintenance theorem supplies uniform O(s log s) space but exponential update time. This theorem does **NOT** invalidate MMW's simultaneous update/workspace lower-bound research target, CHMY's one-way physical input/tape-time lower bounds, or unrestricted deterministic SAT lower bounds. Input rereading, hidden algebraic factorizations, and physically charged movement remain legal.

## 3. Independently executed tests and hostile controls

Exact reproducible native CPython script: experiments/tmr/tmr2_sparse_residual024.py, original SHA256 3a1ad5358f557f5deef29219c8c7aae45efb2dda9b0a0c0c4cc7b2d8ebf426d0. Finite explicit AND/OR/NOT circuit enumeration at n=2,3,4 and s=0,1,2,3; the tiny cases with s<n are grammar controls outside MMW's s>=n regime. For each case all prefixes at every cut are grouped by their **complete suffix languages**. Both zero and one successor transitions are replayed across all members of each class; all 2^N full source truth tables are independently assigned YES/NO labels.

Four further fixed-order controls at n=4,s=2 use forward, reverse, even-odd, odd-even source permutations. **Native executed:** 525,376 terminal classifications, 1,050,720 prefix transitions, zero failed assertions. For n=3,s=2, M=40 YES functions, maximum minimized width 16 and 60 total layered states. For n=4,s=2, M=90, maximum minimized width 43 and 315 layered states; odd-even ordering gives width 45 and 328 states, still <=91. Run took 0.412852 seconds in the recorded environment. Tests are COMPUTATIONAL, not a one-tape hardware timing theorem.

The exact native raw JSON, including every per-cut width, order control and scope limitation, is published as deterministic gzip/base64 under results/raw/tmr/2026-11-14_0927_TMR2_MCSP_RESIDUAL024_RAW.json.gz.b64, SHA256 of decoded JSON 19fa1d9745a9c5588488385aa4866a8d464a230b977f3e96b29a11da44a7bbf7. Reconstruct: base64 -d FILE | gzip -dc > out.json. The program writes ordinary readable JSON.

Cheap controls: Horn, 2-SAT, GF(2) Gaussian elimination, bounded-treewidth DP, signed clause Walsh summaries, products, padding, auxiliary variables, variable renaming, cache/recompute and factored circuits remain allowable for a general decider. This experiment did not implement all those algorithms; they are theoretical hostile families, not falsely counted test runs. No free random oracle, shared gate-expansion cost, source-index oracle or PH oracle was used.

## 4. Exact open implications and next target

**MMW gap (OPEN):** The hypothesis is about **uniform one-pass full search-MCSP^A** algorithms at s>=n, and excludes having BOTH poly(s) memory and poly(s) update time for an appropriate A in PH. Neither a positive-prefix count nor a nonuniform residual-width upper bound establishes the needed processing complexity. The real uniform low-memory, exponentially slow representative machine falsifies a space-only necessity claim.

**CHMY gap (OPEN):** Unconditional near-N^1.99 one-work-tape lower bounds concern **larger threshold mu2**, whereas magnification uses a deterministic N^1.01 lower bound at **smaller mu1**. An all-label, same-model, fully charged threshold descent or new low-mu lower bound is missing. Source sampling NO-side guarantees that reject genuine YES instances are not repairs.

**P versus NP gap (OPEN):** Neither theorem supplies an all-exponent lower bound for arbitrary total uniform deterministic 3-SAT deciders on encoded bit length L, allowing arbitrary polynomial workspace and charged rereads. An NP not in P/poly magnification conclusion requires its own nonuniform proof hypotheses.

**Next concrete task:** Derive or falsify a genuine **uniform transition-update computation** lower-bound candidate for one-pass search-MCSP with simultaneously polynomial work memory, permitting compact circuits, sharing and all polynomial preprocessing. Do not repeat positive support counting. **Peer request:** TMR-3 audit charged physical tape serialization and multi-machine ports; TMR-5 independently check the exact residual congruence, fixed-threshold vs full-threshold differences and MMW/CHMY premise matching.

## 5. Read and write integrity

Authoritative first directive and Nov13 replacement, both root proof1.txt (28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and FULL proof2.txt authentic Git blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c), root main.tex full blob (2,542,866 characters, SHA 5ec8fffb16ec9a7f262e60321bf5aad172d153d8), all five latest TMR handoffs, issue #3, AGENTS.md, CODEX.md, pnp-research skill, original previous reports named above inspected. No general lower bound or all-input polynomial SAT algorithm found. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex reserved for TMR-5 synthesis. Existing scheduled tasks and other roles unchanged.

END_OF_REPORT::TMR-2::024::2026-11-14_0927_PST
