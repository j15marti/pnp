# Stopped decoding of the saturated switch profile

22 November 2026, 09:10:51 PST. PNP Independent Counterexamples. STOPPED-PROFILE-AUDIT1 under DYNAMIC-COMPATIBILITY-OBLIGATION1.

PROVED/EXACT restricted bypass and source-code identity. Bounds' conditional theorem passes this independent same-project audit. The new stopped-profile extension awaits independent review. COMPUTATIONAL 8,190 switch strings and 1,024 local assignments. CONDITIONAL inherited compiled authentication tariff. P versus NP OPEN.

## Audited claim and first open premise

Audit target is Bounds' ACCUMULATED-DECODER-HISTORY1 at 37940ec7f14144d6d6a462ce0a222822b19e47f0, applied to Construction's connected Latin chain at dec4350c30459630faa060ddf3ddfba91c66507d.

The chain-rule theorem survives. If B_j is a function of the accumulated earlier records V_j, and U_j is decoded from B_j and Pi_j, earlier U values are functions of V_j. Thus
sum H(U_j|B_j) = sum H(U_j|V_j) + sum I(U_j;V_j|B_j)
<= H(U_vector|B_0)+sum I(U_j;V_j|B_j).
The final entropy is at most N for N-bit inputs, and at most one for repeated identical decisions. Conditional prefix-freeness and actual event reuse give the separate time inequality. These implications have the stated quantifier order and require no independent U_j.

This is an audit of the mathematical statement and its specified normalized scanner, with no kernel verification. A later source-dependent side view must still be recoverable from earlier accounted records. Bounds states that requirement explicitly. Its optional complete-prefix records reuse early events up to q times, as required. The counter retained in visible state cannot be silently omitted when arguing locality.

The first genuinely unresolved premise remains compulsory future information after arbitrary paid joint preprocessing on every fixed correct solver. No error was found that would retire the conditional theorem. The new result below shows that even its whole vector of prefix states has a short stopped record on its uniform prior. It also distinguishes a small entropy certificate from a short worst-case run.

## One fixed solver and both-label semantics

For every q>=1, Construction's q switches Z give v=8q+7 variables and m=9q+6 positive exact-one triples. A Latin block consists of (A_a,B_b,C_((a+b) mod3)) for a,b=0,1,2. A satisfying assignment selects exactly one of the three groups in full: each chosen name covers three rows, two names in different groups overlap, and nine rows must be covered exactly once. Ports A_0,A_1 therefore give equality. Ports A_0,B_0 give R={00,01,10}. Endpoint pin gadgets force both ports true. R squared is the full binary relation, and composing further copies of R preserves fullness. Hence D=SAT iff sum Z differs from one. Both labels occur at identical encoded length.

Fix a globally correct sole-tape solver A_stop. It first authenticates the complete canonical image and extracts its switch vector, with original input retained until the guard succeeds. Every failed candidate is charged. On failure it runs exact SAT enumeration on the retained valid input. On success it pays for normalization to a contiguous vector at addresses 2,...,q+1, with a public sentinel at q+2 and origin output cells 0,1. Clear all other input-dependent content and initialize a finite-state count to zero and the head at address2. A public encoding of q may remain beyond the vector. All movement and clearing belongs to the paid prefix.

The suffix scans right. At each switch bit it increments its count, capped at two. At the second one it stops scanning, returns to the origin and writes SAT. If it reaches the sentinel first, it returns and writes UNSAT exactly when its count is one. It may leave unread cells on tape. Output specification requires a terminated answer, not a globally blank tape. No untrusted trailing formula text may be ignored before authentication has completed.

For each input let R_q be the minimum of q and the position of its second one, treating a missing second one as infinity. The suffix reads exactly R_q switch cells, possibly one additional known sentinel, returns to origin, and halts. Finite control stores only the count and return phase. Therefore T_suffix<=2R_q+O(1), worst case O(q), and no repeated residual query is performed. This is one fixed uniform machine construction for all q, with exhaustive fallback preserving all-input correctness.

## Exact stopped record and entropy

Let U=(U_1,...,U_q) with U_j=min(2,sum_(i<=j) Z_i), independently defined from the source. Set B=(q,A_stop,public normalized layout and prior). All normalized cells outside the hidden vector, output cells, head and state are known from B. Let E consist of the actual first forward reads at addresses2 through R_q+1. Let Pi=Z_1...Z_(R_q). Set b=1,h=0,rho=1. Return reads and sentinel reads are actual charged transitions but add no record symbols.

The decoder reads Pi until the second one or q bits, calculates all prefix states up to that point, and fills every subsequent state with two. At fixed q this code is prefix-free. A string ending at its second one cannot extend to another valid record, and a string with fewer than two ones has length q. The record has fixed public interpretation and needs no separately supplied stop index, length or address list. Hence H(U|B)<=E|Pi|=E R_q<=E T_suffix.

For independent fair switch bits, every valid record p occurs with probability 2^(-|p|). The map between records and complete saturated profiles is bijective. Therefore H(U|q)=E R_q exactly. Also
Pr(R_q>=j)=Pr(the first j-1 bits contain at most one one)=j/2^(j-1).
Consequently, for every q>=1,

H(U|q)=E R_q=sum_(j=1)^q j/2^(j-1)=4-(q+2)/2^(q-1)<4.

This is a sharp expected record-length identity for the whole profile. Bounds' numerical value 3.921875 at q8 follows. Its upper estimate q is valid and can be sharpened to this expression on its specified uniform prior. The profile may be virtually decoded from the record without writing q outputs on A_stop's tape. Only its Boolean decision is physically required. Demanding q explicit outputs would change the task.

This supplies a legal stopped execution, and shows why q syntactic prefixes do not force q informative reads after preprocessing on that prior. The suffix does not promise to reconstruct the full q-bit source, whose entropy is q. It reconstructs a function of that source.

## Worst-case and cache falsifiers

Take the decision-balanced prior on Z=0^q and Z=0^(q-1)1. The profiles have entropy one, but A_stop reads all q bits on both. At the normalized checkpoints all visible state is identical and the hidden snapshots differ only at the last bit. Every deterministic correct continuation from those checkpoints must inspect that address on both runs, since until that read their transitions agree. From address2 this requires at least q-1 head moves. Thus bounded profile entropy does not imply bounded worst-case physical suffix time.

This lower bound is conditional on those common-state normalized checkpoints. A different paid preprocessor may carry D into its continuation and remove the last-bit ambiguity. In particular A_stop can be modified to accumulate the saturated count while extracting authenticated switch bits. After full validation finishes it retains D and returns to the origin, with no later information-acquisition scan. Compiler parsing, remaining validation and output travel still cost work. This fused variant defeats any claim that a second scan is universally compulsory. It does not defeat Bounds' statement about a specifically chosen scanner.

Four falsifiers were applied. Stopping after the first one would confuse a singleton with a later second switch. Stopping before complete source authentication could admit a malformed or nonfamily suffix. Supplying an uncharged stop index could invalidate the prefix code, but the present stop rule determines it. Claiming constant worst-case time from the uniform prior fails on the balanced pair above.

## End-to-end resource ledger

For the compiled family use v=8q+7,m=9q+6,t=5v+6m,r=3m,d=8t,c=26t+4r,g=max(3,2 floor((c+1)/2)+1),n0=d+(10c+1)g+2,m0=(20c+4)g,n=n0+m0+3,M=2m0+4,w=ceil(log2(n+1)). Physical fields are unary n and delimiter, gamma(M+1), signed triples, two n-bit witness strings and a w-bit release ID. Thus
N=3n+2+2 floor(log2(M+1))+3M(w+1)+w=Theta(q² log(q+1)).

For a direct source implementation, encode the canonical generator's IDs plus one in the packed format 1^v0 gamma(m+1) followed by m unsigned triples of width ceil(log2(v+1)). Its length L=Theta(q log(q+1)). Recover q=(v-7)/8 and require m=9q+6 with declarations bounded by the actual input length. For each ordered nine-row block regenerate both local templates using Construction's dense naming rule, compare every field, record its unique matching switch, then verify both endpoint gadgets and exact end. Reject this guard on any mismatch and use the original for exact fallback. At most two templates per block, O(log²(L+2)) arithmetic per identifier and O(L) scans per bit operation give a conservative O(L^3) sole-tape authentication/normalization bound and O(L) span. This source recognizer is symbolic and handles the canonical family only; valid reordered or renamed inputs may fall back. Source total T=O(L^3), S=O(L), both cumulative upper bounds O(L^4) independently, with exhaustive fallback O(2^v L^3+L^3). No unproved compiled tariff is needed for this direct-source bypass.

For compiled images the previously published authentication/inversion/regeneration tariff is O(N^4) time and O(N) span. Normalization by full-span copying, clearing and relocation is conservatively O(N²) time and O(N) span. This includes source retention until success, failed guards, addresses, counters, initialization, representation conversion, caches, sharing, and cleanup. These inherited compiled bounds remain CONDITIONAL pending native implementation review. The new suffix uses O(R_q+1) physical transitions and O(N) span. Thus its CM_phys is O(N(R_q+1)). Input-plus-time replay separately gives the same O(N(R_q+1)) upper bound on CM_min because total time on admitted images is polynomial. Expected suffix CM is O(N) under the fair prior and worst-case O(Nq). These are upper bounds on the same execution, with all unscanned retained cells charged.

Total admitted T=O(N^4), S=O(N), CM_phys=O(N^5), CM_min=O(N^5). Valid nonfamily fallback may cost O(2^n N^3+N^4). There is no all-input polynomial bound from this family. The stopped scan changes the post-authentication component, while acquisition still dominates the total tariff.

Under fixed T<=K N^a, a>=1, ceilings remain S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and separate count-map circuit size O(N^a log N). The stopped-profile demand is below four for its fair prior, against b rho K N^a with b=rho=1. The balanced pair has linear geometric work in q, still polynomial in N. Neither excludes all fixed polynomial exponents. The internally reviewed permutation calibration retains its single-tape quadratic-time/cubic-cumulative match and static Dh<=N²/8,Dh²<=N³/27.

DISJ sanity and simultaneous DTISP PASS for this restricted execution. Deterministic configuration counting PASS as a description upper bound. Relativization and unrestricted model transfer remain OPEN, with no Natural Proofs or algebrization claim. Full-state entropy, relocation, affine/Tseitin, complement, forced domains, private leaves and shared caches remain legal controls. The stopping rule uses exact Boolean relations and no hash-based semantic merging.

## Reproduction and searches

[Checker](../../../experiments/dynamic_redteam_stopped_profile_20261122.py) and [complete raw output](../../../results/raw/dynamic_redteam_stopped_profile_20261122.json) are included. The independent checker derives both local port relations from 1,024 assignments, then checks all 8,190 strings for q1 through12. It compares composed relation feasibility with the stopped decision, reconstructs every profile, verifies prefix-freeness and exact dyadic code probabilities, and verifies the exact rational expected-length formula and worst-case balanced pair. It uses no random seed. This is a new stopped-record algorithm and all-q symbolic proof, rather than a repeat of the earlier 510-input marginal-entropy test. Native tape transitions, compiler and kernel proof were not executed.

Fresh literature query was “negative binomial stopping second success expected number trials prefix code entropy Shannon 1948”. Textbook waiting-time results appeared. The finite expectation is proved directly above, without importing a stopping theorem. Read Shannon's corrected 1948 primary paper, section6 properties5–6, on the conditional chain rule and conditioning. Its discrete finite-variable hypotheses match the audited identity. [Primary PDF](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

Fresh connected GitHub searches in anthropics, openai, xai-org, google, google-research and google-deepmind used “saturated counter” “SAT”. Five were empty. OpenAI yielded a lexical false positive “saturated counterparts” in an algebraic-geometry Lean file at 4eaee87548250b2682affda7d05d947c05554bae, irrelevant to this lemma and not imported. Web fallback grouped the first three org domains with “early stopping SAT” and the last three with “satisfiability short circuit”. An Anthropic proof README was inspected at commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/proof/README.md. It distinguishes deciding and counting loops and describes subexponential SAT statements. No complete theorem dependency/build audit was performed, so those claims are not promoted or used to infer polynomial time. [Inspected file](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/proof/README.md).

Ownership checked using domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai), [xAI release](https://x.ai/news/grok-os), [Google policy](https://opensource.google/documentation/reference/github/where), [Google Research](https://research.google/resources/) and [DeepMind](https://deepmind.google/science/alphafold/). No applicable official saturated-scan implementation was found in this bounded search.

Recovered governance/skill, active continuation, transport model and matching/static bounds, relevant T5 entropy/accounting definitions, own prior anchor audit/handoff, Construction proof and generator, Bounds proof/code/raw, and latest issue324 messages. Repository duplicate search “second success entropy” found historical entropy controls rather than this stopped-profile identity. Connected selected-file recovery was used without a local checkout, so checkout preflight was unavailable. Existing manuscripts and role ownership were preserved.

ONE next dependency for Bounds, Accounting and Synthesis is to exhibit a later positive-information opponent family that survives fused authentication-and-decision caching for every fixed correct solver, with actual event membership and justified side information. The stopped profile and balanced-pair controls should be checked before promoting any recurrence. Construction receives the safe stopping condition after full authentication. The current conditional theorem passes; universal compulsory recurrence and P versus NP remain OPEN.
