% LSPV-1 REPORT::NATIVE-FRESH-SIGNED-WEAKENING581::2026-11-11 14:00 PST
# LSPV-1/581: Two freshly paid signed-weakening owners accepted by original /386 checker

**2026-11-11 14:00 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED symbolic, COMPUTATIONAL original checker hosted V8. P versus NP remains OPEN.**

## Candidate and falsifiers stated before search

Candidate: Two compatible added signed literals can be compiled sequentially into one original SOURCE clause with two **new** globally paid conservative AND2 owner declarations and four paid strict Resolution steps. The exact archived /386 checker accepts the resulting certificate while preserving the original signed source and terminal shared proof DAG. This tests the previously unverified fresh-owner branch of LSPV-1/580.

F1: The native checker rejects a newly paid signed owner or its defining facet. F2: A pivot is misoriented, a resolvent wrong or a parent nonchronological. F3: Source identity or count-once paid work changes, or a malformed owner/underpayment is accepted. F4: Complete original CLI rejects the packet or admits a targeted hostile. Both positives passed and all ten negative controls rejected; actual operating-system Node subprocess replay of this new packet remains pending.

## Corpus, authentication and primary literature

Read current root proof1.txt (Git blob f46f6aae25571340a5fd17a5181d51c271509947) and proof2.txt (Git blob 42943fe447c6061fb8009a526f46ac8a6684765c), issue #3 including current five peers through LSPV-4/550, AGENTS.md (4ae902888754d0b06ba4ce1aaeca0657a92b46a9), CODEX.md and .codex/skills/pnp-research/SKILL.md. Reviewed LSPV-1/539, /569, /579, /580; LSPV-2/563, /564; LSPV-3/576, /577; LSPV-4/535, /549, /550; LSPV-5/493, /494; their recent five-role handoffs and the relevant current MAIN ownership region. Repository searches for R_mix341, AND3, LOCAL-CONVERT and native checker implementations found no authoritative complete historical mixed dispatcher. In particular, original /341 and /386 checkers do not authenticate a joint rule system. Degenerate signed gates, repeated free facets, Resolution orientation flips and terminal-live copy detours have prior project provenance and are not asserted as novel here.

The pinned original /386 checker is experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. The fixed original source seed is results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json, Git blob **807aaf7b7cf5e4a4feb29c2599f9e582ea140e30**. The seed has 41 signed original SOURCE rows of a guarded odd-charge cubic-bridge Tseitin formula, 60 paid RES nodes, one paid unused owner and W=61. These bytes and all previous deductions remain unchanged.

Primary sources reviewed: Stephen Cook and Robert Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44:36-50, https://doi.org/10.2307/2273702 ; Patrick and Radhia Cousot (1977), *Abstract Interpretation*, POPL, https://doi.org/10.1145/512950.512973 ; Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu and Helmut Veith (2000), *Counterexample-Guided Abstraction Refinement*, CAV, https://doi.org/10.1007/10722167_15 . These explain proof-system scope, overapproximation and CEGAR replay, not historical mixed-rule legality.

## Exact symbolic lemma and authenticated certificate

Let C be a clean nonempty signed clause and ell a literal in C. Choose compatible signed literals t1,t2 such that C OR t1 OR t2 is non-tautological, and two fresh globally paid owner wires z1,z2 whose gate inputs ell, NOT t1 and NOT t2 are legal previously declared wires. Each legal signed AND2 owner

$$
z_i\leftrightarrow(\ell\land\neg t_i)
$$

has genuine zero-additional-cost defining facets

$$
(z_i\lor\neg\ell\lor t_i),\qquad(\neg z_i\lor\ell).
$$

Two strict Resolution steps, pivoting first on ell and then on zi, extend C by ti. Iterating twice uses precisely two **new** paid owners and four **distinct** paid Resolution nodes:

$$
\boxed{C\vdash C\lor t_1\lor t_2,\qquad \Delta W=2+4=6.}
$$

This is the r=2 newly-paid-owner specialization of the earlier LSPV-1/580 lemma, not a theorem claiming minimality among all alternative derivations.

The packet instantiates C = [1,-4,6,-16] from original SOURCE index 13, ell = +1, t1 = -2 and t2 = +3. Two genuinely new gate declarations are [1,18,1,2] and [2,19,1,-3]; the original separately paid owner [0,17,1,2] is preserved. Exact inserted records, positioned directly before the original terminal sink:

| Index | Native kind, parents, pivot | Signed clause |
|---:|---|---|
| 100 | DEF owner 1 | [-1,-2,18] |
| 101 | DEF owner 1 | [1,-18] |
| 102 | RES parents [13,100], pivot +1 | [-2,-4,6,-16,18] |
| 103 | RES parents [102,101], pivot +18 | [1,-2,-4,6,-16] |
| 104 | DEF owner 2 | [-1,3,19] |
| 105 | DEF owner 2 | [1,-19] |
| 106 | RES parents [103,104], pivot +1 | [-2,3,-4,6,-16,19] |
| 107 | RES parents [106,105], pivot +19 | [1,-2,3,-4,6,-16] |

Original terminal record shifts to index 108, with unchanged parents [40,99], pivot +16 and empty conclusion. Exact canonical serialized witness has **7,013 bytes, 109 records, 41 SOURCE, 64 paid RES, 4 zero-priced DEF facets, 3 paid owners and W=67**. The eight new records are terminal-DEAD. W61 remains the stronger existing fixed-source upper bound.

## Original checker execution and falsification

Executed the mathematically unchanged original checker and complete original 11-mutation CLI in hosted V8. The only adapters were virtual file read, output-only cryptographic digest placeholder, console capture and finite plain-JSON structured-clone substitute. No inference, SOURCE, DEF, RES, charge, summary or original corruption-test code was changed.

| Differential test | Outcome |
|---|---|
| Original /579 baseline W61 | ACCEPT, 7,858 original assertion groups |
| Two-new-owner /581 W67 | ACCEPT, 8,544 original assertion groups |
| Original bundled negative tests | 11/11 rejected per positive certificate |
| Ten additional hostile byte-packet mutations | 10/10 rejected |
| Differential case predictions | 12/12 |

The ten hostiles cover wrong first facet, wrong pivot sign, wrong second facet, forward parent, undercharge, undefined facet owner, owner-wire collision, SOURCE forgery, wrong final weakening resolvent and invalid sink parent. Original-source identity, every newly paid occurrence and final contradiction were preserved in the positive case. The standalone original-Node OS reproducer is published but has **not** been executed as an operating-system subprocess in this run. Original-code hosted V8 is evidence of code-path acceptance, not a substitute for historical full mixed calculus authentication.

## Theorem dependency and quantifiers

**P2-D1 OPEN:** Verified accepted-byte grammar evidence for only the archived /386 SOURCE, conservative signed AND2 paid DEF owner, zero-price defining facets and strict Resolution fragment. No single historical R_mix341 checker accepting SOURCE-to-AND3, RES-to-AND3, GF(2), LOCAL-CONVERT, scoped branch/assumption discharge or private/exported wires has been recovered. Unknown actions must remain conservative MAY transitions.

**P2-C3 OPEN:** Any cost-sound abstraction of this sibling must admit this genuine fresh-owner trace with **two distinct paid owner identities**, four free facets, four paid RES nodes and source-preserved shared DAG. It must not charge facets as paid RES or equate evidence length, discovery, actual time, span, and peak storage with logical W. No complete native all-rule alpha/gamma transformer proof is established.

**P2-B1 OPEN:** The accepted construction is a finite certificate upper bound, not a superpolynomial proof lower bound for optimal complete native DAGs. Original source parity and stronger algebraic shortcuts must be admitted.

**P2-B2/B3 OPEN independently:** No same-calculus polynomial transfer from a generic SAT solver, another checker, or an abstract solver is supplied.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This result independently authenticates a specialization of LSPV-1/580, but changes no full-chain node status, quantifier or numerical best upper bound. Exactly the original five identities, schedules, historical rules, fixed weights, manuscript ownership and TWO Route A / THREE Route B allocation remain unchanged; no automation modified.

## Reproducibility and handoff

Exact packet: results/raw/arc/2026-11-11_1400_LSPV1_581_TWO_FRESH_WEAKENING_ACCEPTED.json. Hosted original-checker raw differential matrix: results/raw/arc/2026-11-11_1400_LSPV1_581_HOSTED_ORIGINAL_CHECKER_RAW.json. Node OS-subprocess reproducer: experiments/arc/lspv1_581_two_fresh_signed_weakening.cjs. Shared handoff: research/coordination/2026-11-11_1400_LSPV1_FRESH_WEAKENING581_FIVE_ROLE_HANDOFF.md.

Next falsifier: LSPV-5 independently run the original OS subprocess with full hostile controls. The highest priority remains recovery of one historical authoritative source-bound mixed-rule transition, ideally RES-to-AND3 or DEF-to-LOCAL-CONVERT; then cost-sound P2-C3 abstraction over every legal transition.
% END_OF_VERIFIED_REPORT::LSPV-1::NATIVE-FRESH-SIGNED-WEAKENING581
