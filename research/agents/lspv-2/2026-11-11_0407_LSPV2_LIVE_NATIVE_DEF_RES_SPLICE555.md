# LSPV-2/555: Native /386 live defining-facet Resolution splice

**2026-11-11 04:07 PST | Historical Route A | PROVED/RESTRICTED symbolic transformer lemma + COMPUTATIONAL original-code differential replay | P versus NP OPEN**

## Construction and falsifiers

**Candidate:** The recovered /386 checker permits a zero-additional-charge defining facet and two actual paid Resolution steps to reconstruct an identical original SOURCE clause and place the entire detour within the terminal refutation cone, not merely an unused dead subproof. Repeat the detour k times, keeping source, gate owner, source provenance, and final empty sink fixed.

Four falsifiers: F1, real defining facet rejected or owner overcharged; F2, Resolution pivot/resolvent differs from the claimed exact clause; F3, inserted nodes are not ancestors of the terminal sink or break downstream dependencies; F4, wrong facets, pivots, source, parent pointers, or paid summary pass the original checker. Original-code tests exclude F1-F3 on all five positives and reject seven specified F4 corruptions.

## Historical source and scientific scope

Original archived /386 mathematical and complete CLI checker: experiments/arc/lspv2_386_independent_verify.js, original Git blob **338305c0ce101704205e57543756b8127074a986**. Accepted positive prior /554 K4 certificate: results/raw/arc/2026-11-11_0316_LSPV2_554_ACCEPTED_GATE_ORDER_012.json, original blob **afd43c6cdc2e40fefc3c9623bb14fdf8e5b89865**.

This sibling checker recognizes SOURCE, free DEF facets belonging to globally paid AND2 owners, and strict RES. It internally reconstructs guarded signed K4 source clauses from a graph and charge; it does not implement a separately bound external source-hash input, AND3, GF(2), LOCAL-CONVERT, branches, discharge, or a true RES-to-AND3 port. It is **not** the authoritative lost full R_mix341 calculus.

Read both root proof trackers, issue #3 and current comments, root main.tex, AGENTS.md, CODEX.md, repo-scoped skill and the actual relevant LSPV-2/539-554 reports and five-role handoffs. Reviewed peer LSPV-1/569 normal form and LSPV-4/540 free facet owner incidence; LSPV-4/540 already proved real DEF-to-RES edges in separate subproof cones. This run's incremental contribution is the **repeated active terminal-cone** splice and its inverse-on-image normal form. No existing theorem is retired.

Primary literature: Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, *J. Symbolic Logic* 44 (1979) 36-50, DOI 10.2307/2273702, for system-specific proof cost; Clarke, Grumberg, Jha, Lu and Veith, Counterexample-Guided Abstraction Refinement, CAV 2000, DOI 10.1007/10722167_15, for spurious-path refinement; original DRAT-trim implementation at https://github.com/marijnheule/drat-trim for proof-record checker precedent. None reconstructs the lost historical grammar.

## Theorem 555.1: exact source-preserving live-splice transport

Let P be an accepted archived /386 mathematical proof with a globally paid owner z=a AND b, a legal checked defining facet

$$
D_1=(a\lor\neg z),
$$

and an original signed SOURCE clause S=(\neg a\lor\neg b\lor L), where L denotes any remaining disjunction. Assume this source and D1 occur before the first paid RES, all later consumers of S may be redirected chronologically after the splice, and S lies in the final empty-clause dependency cone. The checker also recognizes the same owner's true facet D2=(z\lor\neg a\lor\neg b).

Add one zero-paid D2 record before the first RES. For each representable integer k>=1, add k successive two-RES pairs before the old first RES:

$$
T_j=\operatorname{RES}_{a}(D_1,S_{j-1})
      =(\neg z\lor\neg b\lor L),
$$

$$
S_j=\operatorname{RES}_{\neg z}(T_j,D_2)
      =(\neg a\lor\neg b\lor L)=S,\quad S_0=S.
$$

Substitute S_k for every later reference to the original S and reindex all prior parent records chronologically. Then the original mathematical checker accepts P_k, including the same final empty clause. Every new RES node is in the sink cone, every SOURCE record and paid owner identity is preserved, and

$$
N_{\rm records}(P_k)=N_{\rm records}(P)+1+2k,
\qquad W_{386}(P_k)=W_{386}(P)+2k.
$$

**Proof:** Both facets are from the same already declared owner, and facet records incur no additional owner charge. The displayed complementary pivot signs satisfy the exact original RES implementation, and both derived clauses are its canonical resolvents. By induction S_j=S, so replacing the original SOURCE parent by S_k does not change any old downstream derived clauses or the empty sink. Because that original SOURCE was in the sink cone and all its references are retargeted, the new sink cone includes S_k, T_k, ..., S_1, T_1 and both facets. Only the 2k new RES nodes add logical charge. All original source/RES counters are adjusted exactly. QED, restricted to this checker and the explicit structural preconditions.

**Inverse-on-image normal form:** For packets constructed by this splicer, delete the one extra facet and all k detour pairs, reverse the chronological parent substitution and change the summary counters back. This exactly recovers accepted P, reducing W by 2k. This is not a universal normal-form theorem for arbitrary native proofs.

## Native accepted-byte evidence

The 3,039-byte base packet has 17 SOURCE records (16 guarded K4 signed clauses and guard unit), three paid gate owners, 3 free DEF facets and 28 paid RES (W=31). Gate owner 0 is [0,8,1,4]. The chosen SOURCE record is [-1,-4,-5,-7]. Its original DEF facet D1 is [1,-8], and the new free facet D2 is [-1,-4,8]. The new two-step active derivation is:

$$
[1,-8],[-1,-4,-5,-7]\ \overset{\rm RES_{1}}{\longrightarrow}\
[-4,-5,-7,-8],
$$

$$
[-4,-5,-7,-8],[-1,-4,8]\ \overset{\rm RES_{-8}}{\longrightarrow}\
[-1,-4,-5,-7].
$$

The actual accepted k=1 packet contains 51 records, 17 SOURCE, four zero-paid facets, 30 paid RES, three paid owner IDs, W=33, and 3,213 UTF-8 bytes (LF). Its canonical Git blob is **aeeb555c4dcf7f510a9a501c8afc609b629a9298**.

The unchanged mathematical and complete original CLI checker bodies were executed in hosted V8, adapting only file reads, cloning and the printed digest output. Five positives ACCEPT; seven invalids REJECT; all five positives pass the original eleven bundled corruption tests. **19,873 original checker assertion groups** passed across positives.

| k | Verdict | Packet bytes | Records | Paid RES | W | Sink depth | Every splice sink-live |
|---:|:---:|---:|---:|---:|---:|---:|:---:|
| 0 | ACCEPT | 3039 | 48 | 28 | 31 | 7 | n/a |
| 1 | ACCEPT | 3213 | 51 | 30 | 33 | 9 | yes |
| 2 | ACCEPT | 3334 | 53 | 32 | 35 | 11 | yes |
| 4 | ACCEPT | 3576 | 57 | 36 | 39 | 15 | yes |
| 16 | ACCEPT | 5028 | 81 | 60 | 63 | 39 | yes |

Hostile rejection corpus: false defining facet; incorrect first pivot; incorrect second pivot; incorrect second resolvent; forward/future parent; wrong paid total; forged original SOURCE.

**Reproduction:**
- Executable experiments/arc/lspv2_555_live_def_res_splice.cjs, blob **49543130d987250db056eb719027659d81999b86**. Syntax-parsed; pins checker/seed SHA, reproduces 12 byte-exact variants and invokes original checker as real OS Node subprocesses when run from a complete checkout with optional --emit DIR.
- Positive packet results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json, blob **aeeb555c4dcf7f510a9a501c8afc609b629a9298**.
- Hosted-original-body raw results results/raw/arc/2026-11-11_0407_LSPV2_555_ACTIVE_DEF_RES_HOSTED_V8_RAW.json, blob **5c1e7a9bb3a1e42766c1e0ee6c3bfe2433156613**.

The complete standalone OS Node subprocess suite is published but **has not been executed here**. There is no fabricated OS test or unmeasured timing. Tests are deterministic, not randomized.

## Abstraction, CEGAR, model bridges and proof-chain audit

The exact /386 abstract state for this transport must retain paid owner identities independent of facet record occurrences; source occurrence provenance; chronological parent indices; new and previously declared wire ownership; all distinct paid RES identities; and the final shared sink cone. Adding the true D2 costs zero, each legitimate RES costs one. An abstract checker that charges every repeated facet one paid gate overcharges a concrete legal history, violating W_abstract<=W_concrete. An abstraction treating a semantic copy of S as an unconstrained source/zero-cost accepted rule is a permissive MAY relation with spurious proof paths. Exact pivot, parent and owner checks refine that relation without deleting the actual native shortcut.

Count-once logical work W is separate from certificate byte count, construction/acquisition time, verification time, shared-DAG span and peak space. The observed sink depths increase by 2k here, but no machine runtime lower bound follows. Native SAT-decision and P != NP transfer remain unresolved. Other mandatory potential shortcuts include GF(2), extension, learned clauses, branching with AND obligations and correct discharge. They are neither excluded nor silently charged by this sibling audit.

**Cross-domain classification:** Restricted exact theorem for this checker only; CEGAR is an analogy pending exact alpha/gamma proof for full R_mix341; a checker-proof-length to arbitrary deterministic SAT runtime claim is a failed/unproved transfer. Relativization, algebrization and Natural Proofs obstacles are not resolved by this finite checker experiment.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt or proof2.txt. [P2-D1] full historical grammar, [P2-C3] full calculus cost-soundness, [P2-B1] all-rule superpolynomial lower bound and separate [P2-B2/B3] bridge remain OPEN. P versus NP remains OPEN.

**Next falsifier:** execute the original CLI via the newly published OS Node runner, and locate a single authoritative checker accepting a genuine source- and cost-authenticated RES-to-AND3 or DEF-to-LOCAL-CONVERT shared transition with positive proof and two negative port tests. All five automations, weights, routes and ownership boundaries unchanged.
