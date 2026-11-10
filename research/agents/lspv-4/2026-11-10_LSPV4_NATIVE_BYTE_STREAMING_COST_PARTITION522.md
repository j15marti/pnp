# LSPV-4/522: exact SOURCE-byte read lower bound does not imply WORK-space lower bound; shared-DAG cost partition

**2026-11-10 America/Los_Angeles (PST)** | PNP Time-Space Resource Auditor | historical Route A label retained, current native-calculus-closure support. **PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Affected/dependent node IDs:** [P2-D1], [P2-D3], [P2-C3], [P2-B1], [P2-B2], evidence [P2-L3-550] and new [P2-L4-522]. This report does not claim a full-calculus rule or lower-bound closure.

## IDEA and four falsifiers

**Candidate resource invariant.** In an authenticated abstract refutation transition system, count each paid inference/definition by its *source-bound creation identity* exactly once. Allocate each paid creation's nonnegative fixed weight across component abstractions with total allocation at most the native weight; charge no second *logical inference* to a mere reference. Separately, do not infer WORK-space lower bounds from a certificate's many sensitive input bytes: a long byte-sensitive accepted-packet slice might be recognized by a streaming small-WORK machine.

F1. The original recovered historical /341 checker rejects all noncanonical padded semantically active original source-literal tokens. **False** for the pinned original verifier; positive witnesses below.

F2. Some zero position in the accepted source-literal token 0^k1 can be changed to 2 while retaining exact acceptance. **False** in 174 checked neighbors; the all-k numeric-coercion argument was already proved by LSPV-3/550.

F3. Any accurate recognizer of this same accepted-packet slice necessarily occupies Omega(k) writable WORK space. **False**: a fixed-template one-pass regular-language recognizer has constant finite control and O(log B) charged input-head coordinates at B bytes.

F4. Two legal compatible consumer references to one shared paid node require charging its inference cost twice. **False** by the identity-owned DAG lemma; the cost-2 view is a *separate mathematical test*, not authenticated historical CASE/WEAKEN syntax.

## SEARCH / provenance / precedence

Read complete root proof1.txt, blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, and proof2.txt (initial current-main snapshot c920eaea9e74fefa314e0ca0291cc9b537052a02, subsequently updated by peers; any write requires a NEW complete fetch/SHA). Inspected issue #3 through 2026-11-10 native-checker reports, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; November 9 abstraction handoff, LSPV-1/553, LSPV-2/537 and /341, LSPV-3/549 and /550 and their actual code/handoffs, LSPV-5/476, Grok 2026-11-06 progress and original Claude DIRECTPRODUCT-0001.

**Pinned exact project corpus:** producer experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, Git blob 4081022e8a3841d79f751a3d3a7a10decbb026da; native recovered checker experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; published historical declared rules research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. The checker is a *test-fixture verifier*, NOT the complete original-source-bound historical accepted-byte language: it accepts only SOURCE/AND3/XOR, enforces proof length 4V-1, ignores arbitrary external-source/context metadata and rejects an otherwise semantically legal redundant paid AND3.

**Previously established and not rediscovered:** LSPV-3/550 already proved that one original semantic SOURCE literal 1 can be encoded as JSON string 0^k1; every added 0 is byte-query sensitive under 0-to-2 mutation, yet the same original odd K4 CNF and same 15 native paid nodes remain. LSPV-5/415 established numeric-ID aliasing. LSPV-1/553 documented the incomplete dispatch/length guard. This LSPV-4 investigation independently replays and adds (i) a tight streaming time-versus-space countercontrol, (ii) explicitly partitioned distinct paid-node work and span, and (iii) a resource ledger distinguishing acceptance probes, proof bytes and work memory.

**External searches / change-aware reads:** konard/p-vs-np README (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95), scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research README (f397a7747eaca82df3d754d0a4b4bab1fe10f814), METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f). The first uses a stated finite-machine formalization; the second has restricted certificates; FRAT-XOR/XLRUP documents a *different* authenticated proof language and checker. None authenticates missing /341 opcode bytes. Primary literature searched: Cousot/Cousot 1977 on abstract interpretation, Keller et al. IJCAI 2016 on cost partitioning, Cook/Reckhow 1979 on proof verification, Haken 1985 on ordinary Resolution. No claim of executing Google-specific searches, full repo checkout, or a native FLMV interpreter.

## Theorem 522A: tight read/space separation on the SAME accepted native-341 packet slice

Fix the recovered K4 one-fixture accepted packet of **3,798 compact JSON bytes**, **16 original signed proper width-three source clauses**, and **15 distinct paid AND3/XOR nodes**, whose original checker yields **1,401 assertion groups**. Its original SOURCE literal slot is the numeric value +1. Let A and B0 be fixed exact byte strings including, respectively, the opening and closing quotes around that literal, with lengths 446 and 3,353 bytes. For k>=0 define

$$
P_k = A\,0^k1\,B_0,\qquad |P_k|=3800+k.
$$

The underlying semantic signed CNF, graph, edges, 16 source clauses, paid DAG and terminal contradiction are unchanged because the recovered JavaScript checker applies numeric coercion to the original source-literal slot (LSPV-3/550). Its behavior on these packets is identical.

For every of the k zero bytes, replacing that byte by ASCII 2 produces a packet not accepted by the recovered checker. Thus **any deterministic exact byte-query recognizer of the recovered checker language**, on P_k, makes at least k probes. This is the preexisting LSPV-3/550 indistinguishability lemma, independently audited here.

Now restrict to the fully specified regular slice

$$
\mathcal L_{\rm slice} = \{A\,0^k1\,B_0:k\ge 0\}
$$

on the promise that input is A followed by a {0,2}-string, 1 and B0, with expected fixed wrapper lengths or an end-marker. An exact left-to-right recognizer can match A in finite control, scan zeros while rejecting 2, verify the 1, match B0 and the terminal end-marker. Hence, for encoded length B,

$$
T_{\rm slice}(B)=\Theta(B),\qquad S_{\rm writable}(B)=O(1)
$$

in a sequential read-only-input model **when head coordinates are external**, or conservatively **O(log B)** if the indexed INPUT-head location is charged as a binary address. The fixed A and B0 live in the finite program, not an input-dependent advice table. The recognizer is uniform over k but only for this **fixed regular slice**, not every packet accepted by the original checker.

**Proof:** The fixed prefix/suffix matcher is finite-state; a single scan takes at most O(B) source steps. Each zero is a potential differing byte in an opposite-label packet, yielding Omega(k) worst-case source probes. Since B=3800+k, this is Theta(B). The finite-state machine need not store or reconstruct the 0^k string. A log-sized INPUT-head coordinate is sufficient even when counted. QED.

**Consequences:** There is no verification *time* bound that depends only on q=15 or canonical semantic CNF length for these exact accepted-byte inputs; B must remain an independent parameter. In contrast, the byte-probe theorem **does NOT** imply an Omega(k) writable-space lower bound for all exact recognizers. The actual recovered Node implementation uses readFileSync and JSON.parse to materialize the whole packet in host memory, but that is an **implementation cost**, not a native-language-intrinsic space bound. Neither result is a SAT decision-time lower bound.

## Theorem 522B: node-identity ownership and cost partition in any authenticated shared-DAG proof calculus

Fix any complete legal source-authenticated refutation DAG P and the actual fixed nonnegative weights w(v) on its distinct paid inference identities. Define c_i(v)>=0 for component abstractions i=1,..,r such that

$$
\forall v:\quad \sum_i c_i(v)\le w(v).
$$

Let the *concrete* construction trace charge a paid v once when its unique legal inference/definition node is first created, and assign zero **additional logical inference cost** to each subsequent reference (retaining any separate fixed reference/application tariff if the actual calculus requires one). If every concrete transition/goal maps to a legal abstract transition/goal and abstraction i charges at most c_i(v) on the first-creation event and no more than the actual reference tariff on reference events, then each abstract minimum h_i satisfies

$$
\boxed{\sum_i h_i\le W_R(F).}
$$

**Proof:** For any legal concrete refutation P, project its complete construction path to each component. Each projected goal is reached; therefore h_i is at most that path's abstract charge. Add component path costs, apply the per-*event* budget inequality at the single paid creation of each v, plus allocated reference tariffs if present. The result is at most the distinct-node concrete cost. Take the minimum (or infimum) over all legal concrete refutations. QED.

**Critical qualification:** This is a *sufficient proof obligation* on a fully authenticated calculus. It does NOT prove that any proposed abstraction includes every unknown historical RES, LOCAL-CONVERT, DEF, branching, discharge or other rule. One must never sum per-branch lower bounds without proving such a cost allocation; otherwise a shared lemma can be double-counted. Contexts are equally essential: a derived Γ|-C may be referenced under Γ' only if Γ is justified there or legally discharged. Unknown historical weakening/CASE rules are NOT added.

### Concrete count-once control on the real accepted K4 DAG

The actual accepted proof contains 15 uniquely paid nodes, of which the even/odd ID ownership partition contains **8** and **7**. The test registers two compatible, hypothetical *consumer views* of the same unconditional terminal DAG. Rechecking all 15 ancestors independently per view would report 30 logical charges, while the correct union-of-owners cost remains **15**; both references add **zero new inference nodes**. The two views are a separate contextual-resource test, **not an accepted historical branch certificate**. The weighted critical-path span of the original accepted DAG, with source depth 0 and 1 per paid AND3/XOR node, is **6**. Its distinct-node work is **15**. Native sequential verifier wall time and peak writable space are separate quantities and were not measured.

## Audited local native operations / full resource ledger

| Operation / representation | Historical declared logical charge | Explicit evidence and byte validation | Physical execution / span / retention |
| --- | --- | --- | --- |
| SOURCE original clause | 0 paid inferences | Arbitrary raw input token lengths; original checker coerces literal types; external original DIMACS binding NOT authenticated | Must read decision-sensitive source bytes; test-only Node fs+JSON creates an in-memory payload, not a native lower bound |
| AND3 with two parents, <=3 support | 1 declared weight | Parent IDs, support, 8-bit truth table, optional affine alias; actual emitted JSON bytes grow with IDs | Exact truth table O(8) primitive Boolean rows, plus token/ID scans and address work; 1 logical span edge after both parents, not O(1) verified bit-time |
| XOR of two affine rows | 1 declared weight | Two references, mask and RHS; mask may be sparse/large and BigInt parsing has bit length costs | Genuine GF(2) is a cheap shortcut for Tseitin; parsing, XOR bit scans, retrieval and source provenance are not unit-cost machine operations |
| REF / compatible reuse | No additional inferred node; any native reference tariff UNKNOWN | ID bits and context authentication must be read | Paid lookup/retrieval or replay in actual algorithms; keep all-live vs recompute schedules separate from ideal W |
| DEF/facets, RES, LOCAL-CONVERT, deletion, CASE/join/discharge/WEAKEN | Historical prose declarations vary; fully authenticated accepted bytes/weights OPEN | Abstraction must conservatively include ALL genuine variants until byte grammar pinned | Never infer costs from the /341 fixed-length fixture checker; zero-cost closures require termination/goal preservation and no unearned resource bound |

Independent full phases still to charge for any proposed construction/solver: acquisition/search/failed policies; raw source/ID/head reads; parse and conversion; all generated evidence bits; proof-node construction; every reference and cache join; guest/replay and recomputation; output; parallel span; instantaneous simultaneous live retention, incl. ancestor/child buffers and temporary expansion; deletion/GC and malformed inputs. **Logical W, raw evidence B, serial verifier time T, depth/span D and peak writable space S are distinct axes.**

The K4 GF(2) route is a mandatory cheap full-mixed-rule shortcut: the accepted certificate uses 3 AND3 per vertex and 3 XOR joins, so no Resolution-only expander hardness transfers to the declared mixed calculus. Ordinary Resolution lower bounds against expander-Tseitin require their published restrictions; polynomial ER/GF(2) options cannot be excluded.

## Actual verification and adverse controls

A readback-executed copy of the *published* LSPV-4/522 script extracted its same audit function and executed the exact original producer/verifier bodies in V8, replacing only Node command-line I/O wrappers. The published independent Node executable has **not** been run as an OS Node child process this turn.

- 188 original verifier invocations; 254 audit assertions; all passed.
- Positive k=0,1,2,7,31,127,1023,4095. Accepted packet sizes 3,800 through 7,895 bytes, each with 1,401 original verifier checks and 15 logically paid nodes.
- **174** individual zero-to-two corruptions rejected by both original checker and separate streaming recognizer. All positions exhaustively tested for k<=127, plus first/middle/last positions for larger k.
- Negative native mutants: AND3 table, XOR row, missing parent and signed original source each rejected. A redundant independently paid AND3 is refused by the recovered fixed-length guard, agreeing with LSPV-1/553.
- Independently enumerated original K4 odd-charge UNSAT (0 satisfying assignments) and even-charge SAT (8 satisfying assignments). Context compatibility controls test empty/compatible and incompatible scope; these are **NOT** historical CASE/WEAKEN acceptance checks.
- Exactly 15 distinct paid nodes, 8+7 component allocation, and weighted dependency span 6. No duplicate charging in the legal shared-DAG identity ledger.
- No certificate bit-time upper, actual heap RSS or native FLMV writable high-water was fabricated.

## Status and next exact gap

**PROVED/RESTRICTED:** The streaming regular-slice recognizer refutes converting LSPV-3/550's many sensitive bytes into a general writable-space lower bound. The identity-owner cost-partition lemma is exact for any already authenticated calculus satisfying its explicit per-transition premises. **COMPUTATIONAL:** published original-checker replay and hostile controls above.

**OPEN:** [P2-D1] accepted historical full byte grammar, [P2-C3] all-rule goal-preserving cost-sound abstract transformers, [P2-B1] superpolynomial worst-case full mixed minimum, and independent noncircular same-calculus [P2-B2]/B3. The critical next experiment is a complete externally source-bound RES/DEF/facet/LOCAL-CONVERT/CASE/branch-join native accepted-byte trace with *exact* fixed reference/application weights and measured ID/row access costs. If unavailable, mark each opcode UNKNOWN rather than replacing it with a test completion.

Root main.tex could not be safely edited: GitHub returned a SHA but zero readable bytes for the requested range, so outside-owned-region preservation cannot be authenticated. No agent identities/titles/schedules/time zones/enabled states, 2 Route A / 3 Route B labels, or historical weights were modified.

**Sources:** [1] Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973. [2] Keller et al., State-Dependent Cost Partitionings for Cartesian Abstractions in Classical Planning, IJCAI 2016, pp. 3161-3168, https://ijcai.org/proceedings/2016/448 . [3] Cook and Reckhow, JSL 1979, DOI 10.2307/2273702. [4] Haken, The Intractability of Resolution, Theoretical Computer Science 39 (1985), pp. 297-308. [5] LSPV-3/550, LSPV-1/553 and LSPV-2/537 primary project evidence cited above.
