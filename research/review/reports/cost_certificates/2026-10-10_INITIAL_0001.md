# COST_CERTIFICATES-0001

Run date: 2026-10-10. Status: conditional mathematics and implementation audit; **P versus NP remains open**. No external writes were made by this agent. Parent agent owns publication.

Independent review: REDTEAM accepted the quantitative diagonalization argument, reproduced the 6-character collision, and verified the exact nonempty-seed independence. Its aggregate-closure repairs are incorporated: common uniform asymptotic envelope, strict child decrease above a fixed base threshold, and an exact terminating base solver. PFCERT output means halting with one final string; the NP envelope includes every string of length below two to remove irrelevant finite-length exceptions.

## Findings that change the next step

1. **Current `main9.tex` is ahead of the historical main2/main3 endpoint.** Its clean target is a charged, all-input, ordinary SAT-preserving successor of length `M^(2/3+o(1))`, constructed in `M^(1+o(1))` time and `M^(2/3+o(1))` writable space, from the assumed fixed polynomial SAT machine. Finite iteration removes its unknown finite time and space exponents. The resulting `(1,2/3)` pair contradicts Fortnow's near-linear-time/sublinear-space theorem under matched model assumptions. The constructor is unproved. Historical use of `2 cos(pi/7)` as a general time-space product bound must not be revived.
2. **K elimination is real conditional accounting.** Recovery7 and Recovery10 already prove aggregate closure with `C=max(1,r,(g+v-h)/(1-h))` when the physical access simulation and all-input successor closure exist. At `(r,v,h,p)=(6/5,11/10,1/2,1/2)`, `g=0` gives `(C,P)=(6/5,1/2)`. A positive conservative per-access exponent `g` gives `C>=6/5+2g`. This explains exactly why a short handle plus a repeated parent scan is insufficient.
3. **The older two-list PFCERT route has a valid short conditional implication, not a verifier construction.** A polynomial verifier accepting at most two distinct n-bit outputs per program `|p|<=n-2`, globally over all accepted polynomial witnesses, yields an NP envelope of size at most `2^n-2`. Complete coverage of all relevant time-bounded short programs and P=NP contradict Hirahara's P-immunity theorem. The same fixed universal machine, time bound and witness polynomial are essential. The route uses plain time-bounded `K^t`, not Levin `Kt`.
4. **New deduction: declare decompression time together with certificate length.** If witnesses have length at most `L(n)` and verification takes `q(n)`, a fixed procedure can enumerate the first n-bit string outside the envelope in at most `2^(2n+L(n)+O(1))*poly(n+L(n))*max(1,q(n))` direct-machine time. It has an `O(log n)`-bit description. Whenever the claimed decompression bound `t(n)` includes the universal simulation of this procedure, completeness contradicts its output. In particular, a universal claim for **every** superpolynomial `t` is false: `t(n)=2^(2^n)` defeats every polynomial-witness verifier. The slower-fixed-time proposal, for example `t(n)=n^(log n)`, is not refuted by this argument. This is an elementary quantitative obstruction, not a proof of P versus NP or a claimed literature novelty.
5. **The attached random generator ignores all nonempty cleaned seeds.** For identical random draws, every nonempty seed produces the same seven output characters. This is an exact code consequence, independently reproduced by REDTEAM. The two deterministic FNV tools have finite capacity and cannot by themselves supply an asymptotic history-distinguishability theorem.

Explicit certificate-degree consequence: if `L(n)<=n^a`, verification is polynomial, and the fixed universal simulator has polynomial-overhead degree `d`, then `B_U(n)<=2^(d*n^a+2*d*n+O(log n))`. Therefore completeness for `t(n)=2^(n^c)` is impossible whenever `c>max(a,1)`. No existence conclusion follows at equality or below.

## Charged certificate ledger

The following quantities must be separated in every proposed executable compiler.

| Object | Required bound or rule | Failure mode |
|---|---|---|
| Discovery | Charge successful and failed searches | A cheap verifier does not locate its certificate cheaply |
| Verification | Charge verifier operations on its full explicit input | A succinct assertion is not its semantic proof |
| Updates | Count all maintained indexes, dictionaries and witness changes | Data-structure operations disappear from proxy metrics |
| Replay | Count each actual regeneration and source traversal | Streaming output is later reused as free random access |
| Emission | Count complete encoded child bits, with multiplicity | Variable contraction is mistaken for bit-length contraction |
| Peak space | Sum simultaneous buffers, indexes, ancestors and certificates | Separate time and space witnesses are merged into one fictional algorithm |
| Semantic calls | Record actual query length and degree dependence | A parent-scale call reinstates `K` |
| Coverage | All roots and reached ordinary successors | A partial portfolio stops at UNKNOWN |

For NP-envelope existence, proof discovery is **not** required. If an executable transformation later needs a witness, however, its discovery is charged there. Even under P=NP, membership/search in a fixed level of PH yields some polynomial exponent, not a near-linear time or sublinear-space guarantee. This is the essential separation between the PFCERT and ARC routes.

## Attachment audit

The harness executes the JavaScript extracted from the original three HTML files; no original attachment was edited.

| File | Actual mechanism | Range/defect |
|---|---|---|
| generator.html | `Math.random()` pool, indexed deletions, randomized spacing | With nonempty cleaned seed, characters are random-pool positions 0,8,16,24,32,40,48; seed contents and positive seed length vanish |
| hash.html | 64-bit FNV-1a, remainder modulo `62^6` | At most 56,800,235,584 labels, about 35.7252 bits |
| hash_tool.html | 64-bit FNV-1a, remainder modulo `62^8` | At most 218,340,105,584,896 labels, about 47.6336 bits |

Exact seeded test: seeds `A`, `B`, `1234567890123456`, and `not-a-seed` all produce `b4tZ 6X1` under the harness's identical draws. Empty cleaned seeds follow a different selection pattern.

An explicit 6-character collision was found after 586,311 deterministic samples and reproduced by REDTEAM:

```text
pnp:4af52079e1a2cf84d4461513ff3e9756 -> kUWA9k
pnp:b7bf65d9c5ec956423bc6173a00eb836 -> kUWA9k
```

No 8-character collision search was performed. Pigeonhole bounds suffice asymptotically. Seven raw base-62 characters carry at most 41.6794 bits; the alternative space placement adds at most one bit if formatting is part of state. A sequence of labels can of course carry more information when represented as additional state, whose storage/access must be charged. Cryptographic collision resistance would not establish that a SAT decider must invert a hash or retain a prescribed history.

## Source recovery and completeness of this run

This is a targeted first review, not an assertion that every chat/file has been exhaustively read.

### Google Drive

Read in detail:

- [PVG-3-0001, Two-Valued PFCERT Suffices](https://docs.google.com/document/d/1mBkVtrjevgfNdkNeuUCoAVd9p-EIwM7QH3fcuwcbMUo/edit): exact bounded-image formulation, ambiguity budget, immunity alignment.
- [PVG-4-0001, 2-PFCERT Oracle Barrier](https://docs.google.com/document/d/1JVCcWJC4oQ-wQhOHMb_cuid0aQ6H7gCLUpjt2xG8vN8/edit): source-grounding is insufficient; oracle barrier handed to LOWER_BOUND agent.
- [PVG-5-0001, Minimal Path-A Spine](https://docs.google.com/document/d/1Kna4PvhYLjQ5Y_TCe_J1zCwO21FqEWNhQC9Y1bKsXyU/edit): minimal dependency graph and retirement of unnecessary sparsity/magnification machinery.
- [NONALG-0003](https://docs.google.com/document/d/1w8sE_27wVea0Ne24DEdZgkX8KABksf7MfwNrBqjfZKU/edit), substantial relevant sections: PH selection, globally sparse-envelope union failure, count certification, invariant existence, succinct-history and state-width gates.

PFCERT/FCERT/exponent/wrapper searches also recovered older reports. Twelve PFCERT search documents were cached under `sources/`; caching does not equal full independent verification. The `sources/` cache is working evidence and need not be republished as a duplicate of the complete research archive.

### GitHub

Repository: `j15marti/pnp`, observed default-branch search commit `b6948eb15a8afec37cc904120ce20b61b45a0dad`. Current fetches were default-branch reads; no immutable snapshot of the entire repository is claimed.

- Root `main2.tex`, `main3.tex`, `main4.tex`, `main5.tex`, `main8.tex`, `main9.tex` fetched. Relevant theorem and status sections were reviewed, not every line of all roots.
- Recovery7/Recovery10 manuscript additions and complete agent reports fetched; aggregate and access-cost derivations reviewed.
- ARC14 and ARC15 reports read for actual implementation limitations. ARC15 reports 12/13 declared formula coverage after verified SAT early exit, with remaining UNSAT UNKNOWN; shape metrics omit material time and memory work and do not constitute a joint bound.
- Most useful source paths: `research/agents/proof/2026-10-08_2349_RECOVERY-STRENGTHEN7.tex`, `research/agents/proof/2026-10-09_0254_RECOVERY-STRENGTHEN10.tex`, `research/agents/proof/2026-10-09_1940_ARC15.tex`.

### Chats

The agent's Personal Context search returned `Personal context is unavailable for this conversation.` Visible project context was used, but cannot replace complete chat retrieval. Parent reported successful independent personal-context retrieval and supplied repo location and current frontier. The remaining chat recovery is explicitly pending; it is not marked complete.

## Literature checked and relevance

1. Hirahara, **Unexpected Hardness Results for Kolmogorov Complexity Under Uniform Reductions**, STOC 2020 / [ECCC TR20-050](https://eccc.weizmann.ac.il/report/2020/050/). Primary PDF checked, including Theorem 3.9 and the distinction from Levin Kt. Supports the conditional PFCERT endpoint only; it does not construct the verifier.
2. Fortnow, **Time-Space Tradeoffs for Satisfiability**, JCSS 2000, [author PDF](https://lance.fortnow.com/papers/files/npvsnl.pdf). Primary theorem and random-access conventions checked. Supports the corrected `(1,2/3)` landing when the ordinary encoding and physical model match.
3. Feldman, Immerman, Sagiv and Shoham, **Complexity and Information in Invariant Inference**, POPL 2020, [primary preprint](https://arxiv.org/abs/1910.12256). General Hoare-query inference can need exponentially many queries even for polynomial-length invariants. A warning against conflating certificate size with acquisition, restricted to that inference model.
4. Hirahara, Kabanets, Lu and Oliveira, **Exact Search-To-Decision Reductions for Time-Bounded Kolmogorov Complexity**, CCC 2024, [publisher page](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2024.29). Search result and source metadata checked, not the complete proof. A relevant next retrieval for the exact discovery problem; not used as a theorem supplying the missing verifier.

## Priority work for the next run

1. Fix one candidate constructor on the current main9 strict-successor interface. Prove or falsify complete root-plus-successor coverage and measure every charged operation against original encoded length.
2. For implicit/shared children, derive an actual composed access schedule and peak-state ledger. At the older saturated aggregate point, prove exponent-zero access overhead or demonstrate a batch/cache bound that changes the conservative recurrence.
3. If pursuing PFCERT, choose a slow fixed superpolynomial `t`, a single explicit witness bound `L`, and a concrete verifier language. Prove the accepted-output union bound over all witnesses. Run the certificate-length diagonalization test before promoting completeness.
4. Keep conditional lemmas labeled conditional and positive finite SAT improvements labeled computational. The next theorem must add an all-input semantic construction, not another restatement of the endpoint.

## Deliverables

- `cost_certificate_spine.tex`: formal conditional equations and diagonalization boundary.
- `cost_certificate_refs.bib`: primary-source bibliography.
- `attachment_audit.js`: complete reproducible source-execution audit.
- `attachment_audit_results.json`: exact test outputs and attachment digests.
- This report and the reviewed-source cache.
