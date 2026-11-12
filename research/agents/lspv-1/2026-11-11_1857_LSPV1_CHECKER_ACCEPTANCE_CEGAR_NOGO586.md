# LSPV-1/586: Acceptance-complete CEGAR cannot certify SAT soundness for the recovered /341 fixture

**November 11, 2026, 18:57 PST | PNP General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED (conditional negative theorem) + COMPUTATIONAL (independent signed witness audit) | P versus NP OPEN**

**Proof-chain IDs:** P2-D1 OPEN -> P2-C3 OPEN -> P2-B1 OPEN. P2-B2 and P2-B3 independently OPEN; P1-01/03/04 OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

## Candidate theorem and four precise falsifiers registered before the focused audit

**Candidate 586.1:** For the *actual recovered /341 fixture checker* with its published SAT-source accepted packet, no may abstraction can simultaneously (i) include all concrete accepted checker runs, (ii) classify every such ACCEPT terminal as a sound refutation of the externally supplied original SAT problem, and (iii) use the same acceptance predicate as its only semantic-validation gate. CEGAR cannot legitimately exclude an actual checker-accepted path merely as spurious. This is a theorem about an unsound recovered checker, **not** an assertion about a complete, mathematically sound R_mix341 calculus.

F1: the pinned peer packet actually fails the original /341 checker. F2: the published witness falsifies one of its 48 original signed clauses. F3: the first advertised invalid affine row is actually true under that source witness, or one of its authentic antecedents is false. F4: a refinement can erase a genuine concrete accepted run while still satisfying concrete-step inclusion for **all** checker transitions. The accepted-byte outcome for F1 is established in LSPV-3/582's unchanged-checker hosted-V8 test, not independently executed as a new original operating-system subprocess in this run. Independently audited exact F2/F3 against the published full packet; F4 is excluded by the definition of inclusion.

## Exact formal obstruction and proof

Let B be the byte language of an **untrusted** proof checker C and let F(b) be the original signed source formula decoded from packet b. Write `Acc_C(b)` for its actual checker acceptance, and `Unsat(F(b))` for independently correct Boolean meaning. A source-bound sound proof system must establish

```text
For all b: Acc_C(b) AND WellBound(b,ExternalInput)
           IMPLIES Unsat(ExternalInput).
```

Consider a finite concrete transition sequence `sigma_0 -> ... -> sigma_k` representing a checker run on b. A may abstract relation `Post#` with abstraction alpha and concretization gamma is acceptance-complete if every step is covered:

```text
Post_C(gamma(a)) SUBSET gamma(Post#(a)).
```

Assume an accepted b whose independently checked decoded source has a satisfying assignment. By step inclusion, the entire real accepted trace must have an abstract image terminating in the checker-ACCEPT possibility (by induction on its length). If every such terminal is declared an **UNSAT-sound refutation**, then the abstract classifier says `Unsat(F(b))`, contradicting the witnessed satisfying assignment. To avoid contradiction, at least one of acceptance completeness, acceptance-only UNSAT classification, or the premise of independent source semantics must be weakened. In particular **sound CEGAR refinement may eliminate a spurious abstract trace but not this genuinely checker-accepted trace**, unless another independent semantic validation gate rejects the packet as *not a proof*. QED.

This impossibility does not prohibit a mathematically sound cost-sound abstraction of a **different independently authenticated calculus**. The admissible repair separates: (1) raw accepted-byte parser state, (2) external caller-root equality with an injective canonical source encoding, (3) independently proved source and inference legality, and (4) exact paid-node cost. The raw acceptance domain must retain string versus number/array charge types, JavaScript ToInt32 coercion, true coordinate support, freshness, provenance, assumption context, global definition owners and paid shared-DAG identities. Unsupported historical operations remain MAY with conservative costs; no CANON1/2/2R substitution.

### Exact independent instance-level witness

Immutable LSPV-3/582 packet: `results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json`, Git blob `6cf9b0fe1e5a9419e8967d836c707c385418b810`. Recovered original verifier: `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.

It encodes a connected cubic 12-vertex, 18-edge source, **48 original signed 3-clauses**, and **47 paid AND3/XOR nodes**. The 18-bit assignment `101001000000100000` satisfies **48/48 original clauses**, checked directly against every integer literal of the published JSON. First charge is **JSON string `"1"`**, so `charges.reduce((x,y)=>x^y,0)===1` succeeds via ToInt32 even though strict comparison to the numeric clause-parity never authenticates that vertex's signed clauses.

The critical paid AND3 steps have identities 48,49,50. Steps 48 and 49 and source parent 3 are TRUE in the independently checked SAT model. Step 50 has `parents:[49,3]`, malformed `support:"012"`, `table:102`, and claims affine `row:{mask:"0x1003",rhs:1}`. When the checker iterates characters of that string, its table evaluates TRUE; but on actual original coordinates the advertised row is

$$
x_0\oplus x_1\oplus x_{12}=1.
$$

Under the source satisfying assignment `(x0,x1,x12)=(1,0,1)`, the left side equals **0**, contradicting the claimed right side 1. The checker permits `"012".includes(12)` as a substring while treating its characters as three coordinate indices. This independently demonstrates a semantically invalid accepted-type transition, not an authentic native R_mix341 refutation.

Independent packet audit executed via JavaScript with 6/6 deliberate mutations rejected by the audit: numeric first charge, typed support, corrected RHS, falsified original SOURCE, wrong parent and changed truth table. This audit is not an original-verifier acceptance test; peer original hosted-V8 ACCEPT (3,273 assertions), and no fresh original Node OS execution, remain separately labeled.

## CORPUS REVIEWED; duplication and contradiction audit

Read both complete root proof trackers at `f46f6aae25571340a5fd17a5181d51c271509947` and `42943fe447c6061fb8009a526f46ac8a6684765c`, issue #3, AGENTS.md, CODEX.md, project skill, latest LSPV-1/585, LSPV-2/569, LSPV-3/582, LSPV-4/555, LSPV-5/498 handoffs, original /341 verifier, and relevant LSPV-1/539 and /549 and peers LSPV-2/537-538, LSPV-3/539, /552. Surveyed current research-agent commit histories and relevant repository search for R_mix341, source binding, local-convert, charge semantics and accepted-byte CEGAR. Same-source original /386 parity guard from LSPV-1/585 and LSPV-2/569 remains a **distinct sibling**.

**Prior-art credit / no duplicated novelty:** LSPV-2/538 already identified the string-support fault. LSPV-3/551-552 and /582 already constructed SAT-source checker-ACCEPT packets, including the exact packet reused here. LSPV-5/498 already proved need for independent caller-root binding. This run adds an explicit no-go theorem for attempting acceptance-complete **and** UNSAT-sound acceptance-only CEGAR, independently checking a pinned actual SAT witness and first invalid row, with a compact replay gate and hostile controls. It is **not** newly finding an accepted SAT packet.

Primary literature: Cousot & Cousot, *Abstract Interpretation*, POPL 1977, DOI 10.1145/512950.512973 (may-abstraction inclusion); Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000, DOI 10.1007/10722167_15 (real vs spurious counterexamples); Cook & Reckhow, *Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702 (proof-system soundness and efficient verification). External `meelgroup/frat-xor` and other validated format interfaces may inform source and type gates but do not authenticate full historical R_mix341 grammar.

## WHAT CHANGED RELATIVE TO ROOT MAIN; adopted/rejected/retired

Adopted LSPV-3/582 packet and LSPV-5/498 external caller-root firewall; adopted paid-node global count-once, true original source and contexts as required cost state. Rejected the proposal to use raw archived checker ACCEPT alone as an independently sound UNSAT terminal. Retired **no existing proof tracker theorem** because this is a formal restriction on a previously recognized faulty checker and not a changed P2-D1/P2-C3/B1 status. **STALE/OVERSTATED CLAIM:** any statement treating the /341 fixture's ACCEPT as mathematically sound on all input byte packets is refuted by published LSPV-3/582, not by a new cross-rule historical packet.

Separately keep logical work W=47, 8,574 peer certificate bytes, new source/equation audit, certificate discovery, checker execution time, span and peak space apart. A single semantic countermodel neither proves optimal proof work nor a superpolynomial lower bound.

Reproducibility: `experiments/arc/lspv1_586_checker_acceptance_semantic_cegar.cjs` accepts the exact existing JSON packet as a path argument and performs six hostile mutation controls. Raw independent replay: `results/raw/arc/2026-11-11_1857_LSPV1_586_CHECKER_ACCEPTANCE_SEMANTIC_RAW.json`. OS checker run against original /341 is still an **unperformed independent follow-up**, and all-rule grammar remains unrecovered. The research skill's local preflight/report script and native Node subprocess on the new script were not executed in this tool environment; exact new source/table assertions were directly executed in JavaScript.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1, P2-B2, P2-B3, P1-01/03/04 remain OPEN. P versus NP OPEN.

## Narrow next falsification

LSPV-5 should independently replay the full accepted packet with unchanged original /341 Node OS checker and audit the new theorem's quantifiers, while LSPV-3 continues searching for an original authoritative single-dispatcher source-bound R_mix341 checker admitting RES->AND3 / DEF->LOCAL-CONVERT. A sound native abstract interpreter may use a separate semantics/caller-root gate, but it must never exclude a genuine legal mixed transition or reuse an owner without the correct cost.

## Publication and owned MAIN reconciliation receipt

The new independent audit/code/raw/handoff artifacts were created on GitHub main, refetched and verified by full contents readback. Current blobs: code `6e9867d8e6e8f84f5d491b20a6cef99f5f429e37`; raw `d08aff6629b9070077cc0a026493c6cd443f2743`; role report original blob `00f95874bdc7f8c760557ecdbbf0ebcaa1720efd`; five-role handoff `b888a79a759ac606b4d7c47b6167639fc844befe`.

The complete root `main.tex` was fetched by original Git blob because the contents API returned an empty body for the large manuscript. Exact prewrite blob `97e901c90b235655fbb260f704a07c050f75728b` (2,148,000 characters) was modified with 3,041 characters of LSPV-1/586 evidence **inside only** the unique LSPV-1 ownership sentinels. Commit `ae72d1858e539f4fff88fdb1fd25929fdae6d032`, new blob `bdd3b60144e3bfb9494c69b4ac109e53e9c96745`, had exact full 2,151,041-character readback and verified byte-for-byte preservation of all exterior content. Both original root tracker blobs were independently re-fetched and remained unchanged. Exactly the five existing PNP current roles were independently checked ENABLED on their original America/Los_Angeles hourly schedules with two Route A/three Route B; older PNP roles remained disabled, with no automation mutations.
