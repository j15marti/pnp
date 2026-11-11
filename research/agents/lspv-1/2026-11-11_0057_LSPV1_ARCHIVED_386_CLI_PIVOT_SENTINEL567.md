# LSPV-1/567: archived /386 full-CLI sentinel-pivot acceptance asymmetry

**2026-11-11 00:57 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and falsifiers, specified before experimental witness replay

**Candidate.** The unchanged original archived /386 **mathematical core** permits an otherwise valid final strict RES pivot of exactly positive 999999, but the original standalone **CLI** rejects every such packet solely because its first built-in negative-control mutation changes nothing. The simultaneous RES parent swap with pivot negation supplies a same-DAG, same-cost CLI-accepted witness. This is evidence for **P2-D1**, not a new operation or a lower bound for the missing full historical R_mix341.

F1: original checker disallows a fresh wire 999999 or duplicate-input paid DEF gate. F2: both bridge facets or derived final units violate signed strict Resolution, source binding, or count-once payment. F3: the CLI rejects both pivot orientations or accepts both, or the semantic core rejects the positive version. F4: source, owner, chronological parent, facet or underpayment corruptions go undetected.

## Primary sources and corpus

Authoritative for this **restricted sibling only**: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986, original source-bound nested K4 packet results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json, Git blob 08aa169b5db49b2ddd1cb5a9b6890fcc3b790916. The declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex gives semantic five-rule tariffs but **no recovered unified five-rule accepted-byte dispatcher**. The surviving /341 checker, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, dispatches only SOURCE/AND3/XOR, whereas the archived /386 checker accepts SOURCE/DEF/RES. Do not combine these languages.

Reviewed both root trackers (proof1.txt Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt prewrite blob 8927e4ba0c54ba701ceac55e918203fcdf675e1a), issue #3 and current peer tail, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-1/539-549, /563-566, LSPV-2/549-551, LSPV-3/544 and /561-564, LSPV-4/535-537, LSPV-5/482, latest five-role handoff and original archived checker and packet. In particular **LSPV-4/535 already discovered a different CLI no-op control for zero-owner packets**, and LSPV-3/564 already proved the **core** RES orientation involution. This run constructs the previously unverified positive-pivot 999999 CLI counterexample and same-paid-cost recovery; neither prior discovery is claimed as new.

Primary literature searched: Cook and Reckhow, Journal of Symbolic Logic 44 (1979), 36-50, DOI 10.2307/2273702 (proof-system cost and verification); Cousot and Cousot, POPL (1977), DOI 10.1145/512950.512973 (sound abstraction); Clarke et al., Journal of the ACM 50 (2003), 752-794, DOI 10.1145/876638.876643 (CEGAR). None supplies the archived checker semantics; those are determined only by the pinned original program.

## Theorem 567.1: universal positive-terminal-pivot full-CLI rejection (PROVED/RESTRICTED)

For **every** JSON packet P for which the original archived /386 checkProof(P,{control:true}) accepts and whose final RES record has pivot equal to the JavaScript number 999999, the original archived /386 CLI invoked on P rejects, independently of all other input fields.

**Proof.** The CLI first accepts P using checkProof, then runs its fixed list of eleven hostile mutations. The first copies P and executes the statement that sets the final record's pivot to 999999. As the final pivot is already 999999, this produces an unchanged packet. checkProof necessarily accepts that copy. Hence corrupt returns false and the outer check requiring rejection fails with the exact error "accepted a corrupted proof". This proof is a direct read of the original unchanged source, with no statistical hypothesis. QED.

The theorem concerns the wrapper language, **not** the core mathematical proof calculus. No claim that an invalid or unsound refutation becomes mathematically sound follows from bypassing the wrapper.

## Lemma 567.2: charged signed identity-bridge witness (PROVED/RESTRICTED)

Consider the original /386-accepted nested K4 proof with 17 genuine SOURCE clauses, six free facets of two paid owners, 51 paid RES, 74 records and W=53. Its final RES has singleton parents [6] and [-6] and pivot +6. Declare one new globally fresh owner (id 2) with wire z=999999 and truth table z=(x_6 AND x_6)=x_6. The original checker accepts the owner as [2,999999,6,6]. Its canonical free facets include [6,-999999] and [-6,999999].

Replace only the final RES step by the two RES premises and terminal RES:

$$
[6],[-6,z]\ \vdash_{\operatorname{RES}(6)} [z],\qquad
[-6],[6,-z]\ \vdash_{\operatorname{RES}(-6)} [-z],
$$

$$
[z],[-z]\ \vdash_{\operatorname{RES}(z)} \square.
$$

Two free DEF views, two additional paid RES, and one paid DEF owner increase the original logical cost by **exactly three**; the previous terminal RES is replaced, not charged again. Both signed orientations of the final RES are legal in the mathematical checker, with identical W=53+2+1=56, identical source, owner bank, complete shared DAG, owner obligations and completed contradiction:

$$
W_{386}=N_{\rm RES}+N_{\rm distinct\ paid\ owner}=53+3=56.
$$

The +z packet places parents of final RES in [unit z, unit -z] order with pivot +999999. It is **core ACCEPT / full CLI REJECT** by Theorem 567.1. Exchanging those two parent IDs and changing the final pivot to -999999 produces a packet with **core ACCEPT / full CLI ACCEPT**. This latter CLI acceptance is computational evidence on this exact 78-record packet, not a universal wrapper normal-form theorem.

The source is independently checked UNSAT by exhaustive evaluation of all 128 original 7-variable assignments. Both packets keep all 17 original SOURCE clauses and every paid owner in sink ancestry. The 78 records comprise 17 SOURCE, eight free DEF records, and 53 RES. Six DEF records, all 53 RES and all 17 SOURCE records are in terminal ancestry. Two unused facets are still accepted and are zero additional paid work. A paid owner is charged exactly once, regardless of how many facets are displayed or reused.

## Original-body execution and falsification results

In hosted V8 the **unchanged** /386 mathematical checkProof and the unchanged full CLI body with all eleven bundled negative checks were evaluated; only virtual filesystem, structuredClone interface, and an **output-only SHA digest** were adapted. No checker rule, pivot test, source guard or internal hostile mutation was edited.

| Exact packet | Core | Full CLI | Paid W | Records |
| --- | --- | --- | ---: | ---: |
| Original 74-record nested K4 | ACCEPT | ACCEPT | 53 | 74 |
| Bridge z=999999, final pivot +999999 | ACCEPT | **REJECT** (no-op hostile mutation) | 56 | 78 |
| Identical proof, parent-swapped terminal pivot -999999 | ACCEPT | **ACCEPT** (11 hostile tests) | 56 | 78 |
| Nearby fresh z=1000000, final pivot +1000000 | ACCEPT | ACCEPT (11 hostile tests) | 56 | 78 |

Four independent corruptions of the negative-pivot accepted witness were rejected by the authentic core: incorrect final signed orientation, non-owner defining facet, forged original source, and paid-total undercharge. The native CLI accepted negative pivot and nearby-positive packets with 4,899 original assertion groups each. The positive sentinel packet's core returned paid=56, def=3, res=53, sources=17, oddModels=0, evenModels=8, guardFalseModels=64, identical to negative orientation. All 128 source valuations were exhaustively tested independently; zero satisfy.

**Execution limitation:** No operating-system Node subprocess was executed in the hosted run. A separate standalone dependency-free Node script invoking the true operating-system checker subprocess, including SHA-256 output, is published for LSPV-5 to run. Thus hosted-V8 full-CLI evidence is not described as native-process execution.

## P2-C3 / P2-B1 dependency ledger

An abstract cost-sound **core** RES orientation quotient may identify +z and -z representations while retaining signed parent port meaning and all paid-node identities. The **CLI** accepted-byte language cannot use this quotient as equality of acceptance without additional authenticated wrapper conditions. For a core cost lower bound, the wrapper's synthetic negative-test failure cannot exclude the +z legal core proof. Conversely, if defining the actual proof calculus as the full CLI language, this rejection must be represented and its semantics justified. Mixing those two languages without a transfer theorem changes Wbar by assumption.

P2-D1 **OPEN**: only a sibling original /386 CLI/core distinction is authenticated; unified historical source-bound RES/AND3/GF(2)/LOCAL-CONVERT/DEF/CASE/contexts/discharge remains missing. P2-C3 **OPEN**: no every-legal-native-rule alpha/gamma and cost-sound completed-goal preservation for R_mix341. P2-B1 **OPEN**: no general full-calculus superpolynomial lower bound. P2-B2/B3 **OPEN**: no same-fixed-calculus polynomial-proof transfer from arbitrary SAT decision algorithms. P1-01/03/04 **OPEN**.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** this result narrows the authenticated sibling wrapper semantics, but changes no unrestricted node status. No rewrite or downgrade of either proof chain is justified. No historical tariff, ownership, title, task, Pacific schedule, or TWO Route A / THREE Route B assignment is changed.

## Exact reproducibility artifacts / next target

- Program: experiments/arc/lspv1_567_native_cli_pivot_sentinel.cjs, pins original Git blobs; runs core and full real Node subprocess when executed in checkout.
- Raw hosted-V8 evidence: results/raw/arc/2026-11-11_0057_LSPV1_567_ARCHIVED_CLI_SENTINEL_RAW.json.
- Positive core-only packet: results/raw/arc/2026-11-11_0057_LSPV1_567_PIVOT999999_CORE_ONLY_PACKET.json.
- Negative signed accepted packet: results/raw/arc/2026-11-11_0057_LSPV1_567_NEGATIVE_PIVOT_CLI_ACCEPT_PACKET.json.

**Single next test:** LSPV-5 independently runs the original Node.js CLI on both byte-exact packets, checks the SHA and the eleven built-in negatives, and challenges all cost/source claims. LSPV-3 investigates whether any **same** source-authenticated archived checker validates a RES-to-AND3 or DEF-to-LOCAL-CONVERT edge. No full R_mix341 parser was found. P versus NP remains **OPEN**.