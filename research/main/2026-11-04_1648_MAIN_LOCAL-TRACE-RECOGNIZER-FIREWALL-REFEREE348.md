# REFEREE348 — local-trace recognizer firewall

**PNP Independent Proof Red Team | November 4, 2026, 16:48 PST**  
**Status:** PROVED/EXACT proof-system counterexample; COMPUTATIONAL finite controls; not a theorem about `R_mix341`; B1/B2/B3, superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP OPEN.

## IDEA before search

REFEREE347 showed that exact-source authentication and fully charged verification do not make proof cost invariant across arbitrary sound systems: a verifier can recognize a fixed certified UNSAT family. A natural repair remained untested:

> Require a fixed finite opcode alphabet, exact-source authentication, bounded parent arity, nodewise local transitions, polylogarithmic node payloads, and fully charged polynomial verification.

The initial prediction was falsifiable: perhaps these restrictions prevent a verifier from hiding a family recognizer in one global semantic jump. The adversarial prediction was that they do not; a streaming computation trace should serialize the recognizer into ordinary local steps and still give polynomial certificates to Haken's canonical pigeonhole family.

Four registered falsifiers were:

1. a local transition might fail to authenticate every source symbol;
2. the recognizer state or one node might hide the full source/proof;
3. a SAT one-clause-deletion sibling might be accepted by the special or fallback branch;
4. linear logical transitions might conceal exponential construction, checking, output, or live space.

## Established lower-bound anchor: exact model and strength

For `h+1` pigeons and `h` holes, the standard unary CNF `PHP_(h+1)^h` has variables `x_(i,j)`, one width-`h` positive clause per pigeon, and one binary negative collision clause for every pigeon pair in every hole. It has

`h(h+1)` variables and `(h+1)+h*binom(h+1,2)` clauses.

Under explicit signed binary-index/DIMACS encoding its bit length is

`N_h = Theta(h^3 log(h+2))`.

Haken's theorem has the restricted quantifiers

`exists c>0 exists h0 forall h>=h0 forall ordinary shared-DAG Resolution refutations pi of PHP_(h+1)^h: |pi| >= 2^(c h)`.

The source clauses are authentic axioms and every inferred line is an ordinary binary resolvent. DAG sharing, clause width and pivots are unrestricted. There are no extension definitions, GF(2) rows, semantic consequence rules, family recognizers, or arbitrary machine transitions. Buss and Turan's primary exposition explicitly treats Resolution proofs as sequences or DAGs of source clauses and binary resolvents and notes polynomial Extended Resolution pigeonhole proofs. Therefore this is not an `R_mix341`, ER, Res(XOR), or unrestricted-machine lower bound.

## SEARCH

### Project, issue, peers, Grok and Claude

Read first:

- `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`;
- current issue #3 through LSPV-4/398;
- `research/main/2026-11-04_1548_MAIN_EXTENSIONAL-UNSAT-COLLAPSE-FIREWALL-REFEREE347.md`;
- `research/main/2026-11-03_1748_MAIN_RECOGNIZABLE-ISLAND-CERTIFICATE-ROOTING-REFEREE325.md`;
- `research/main/2026-11-04_0248_MAIN_NODE-BIT-NORMALIZATION-OPTIMAL-SYSTEM-FIREWALL-REFEREE334.md`.

The search changed the proposed contribution: broad recognizable-family bypass and fully charged streaming recognition were already established in REFEREE325/347 and LSPV-4's BPHP audits. The new target is the missing **nodewise-local trace strengthening**.

Current peer findings are compatible but do not imply the theorem here:

- LSPV-1/402 makes reconvergent monotone-port essentiality SAT-hard; it does not transport arbitrary proofs.
- LSPV-2/403 gives sharp `2^(k-c)-1` Resolution reflection for one clause exported from bounded support; arbitrary `LOCAL-CONVERT` remains open.
- LSPV-3/405 computes exact circuit support only from an authenticated bounded-width decomposition.
- LSPV-4/398 constructs `O(n)`-node Resolution proofs for 2CNF with polynomial physical resources but explicitly finds nonminimum outputs.

Current Grok `GROKPROOF/2026-11-04_2315_PROGRESS.md`, blob `f5b8ef62d441e5ea6cf5d28ed1df74cfd0474884`, proves only a restricted black-box output-volume bound and leaves white-box residual extraction open. Claude files actually read were:

- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

They concern derandomization gaps, restricted portfolios, or sequential-access lower bounds. None gives same-source `R_mix341` simulation or B3.

### Primary literature and actual queries

Actual general-web queries were:

- `Cook Reckhow proof system computation trace verifier local transition primary paper PDF`;
- `propositional proof systems locally checkable proof computation tableau proof complexity primary paper`;
- `Haken pigeonhole principle Resolution exponential lower bound Extended Resolution polynomial primary source`;
- `p-optimal proof systems recognizable language special proof system primary paper`.

Sources read rather than relying only on snippets:

- Cook and Reckhow, *On the Lengths of Proofs in the Propositional Calculus* (STOC 1974) and *The Relative Efficiency of Propositional Proof Systems* (JSL 1979): a proof system is a fixed polynomial-time map/verifier framework; p-simulation requires a uniform polynomial proof translator.
- Buss and Turan, *Resolution Proofs of Generalized Pigeonhole Principles* (1988), full author PDF: explicit CNF, binary Resolution DAG model, and exponential lower bounds; Extended Resolution/Frege/cutting planes are stated polynomial escapes.
- Haken, *The Intractability of Resolution* (TCS 1985), publisher theorem/abstract; the direct full text was blocked by the publisher.
- Messner and Toran, ECCC TR97-026: existence of a p-optimal system is a major open proof-complexity question, not an available common translator.

Direct Google-branded UI was unavailable. General web search was used, and this report does not claim a Google-specific search.

### OpenAI GitHub

Actual `github.com/openai` queries were:

- `proof certificate verifier trace transition`;
- `Cook Reckhow p-simulation`;
- `SAT execution trace verifier CNF`.

No applicable p-simulation or B3 compiler was found. Two relevant implementation files were read:

- `openai/math/lean/OAI/Computability/UniqueGames/Machines/MachineLemmas.lean`, blob `29d19cde16b89ec6dae9e7d3cb1a4e6c5a351d28`: it distinguishes actual transition traces from symbolic recurrence bounds and requires concrete execution witnesses.
- `openai/math/lean/OAI/Algorithms/SubexponentialSAT/RuntimeAssembly.lean`: it explicitly states that `ImplementationCertificates` are open obligations and constructs no satisfying primitive machine.

These are implementation clues and safeguards, not mathematical proof-system transfer theorems.

## ITERATE: fixed local proof system

### Definition of `P_trace348`

The input is an explicit newline-terminated signed DIMACS CNF. The verifier first parses the entire exact source and rejects malformed encodings. It then accepts either of two proof branches. The opcode alphabet is fixed once and has six symbols:

`START, SCAN, ACCEPT_PHP, TABLE_START, TABLE, ACCEPT_TABLE`.

All proof DAGs are chains, hence have parent arity at most one.

#### Special PHP branch

The `START` line supplies one integer `h`. For each byte position `i` of the exact source there is one `SCAN(h,i,b)` line. Its only parent is the preceding line. The local checker verifies:

1. the position is exactly the predecessor position plus one;
2. `b` equals the actual source byte at `i`;
3. `b` equals the next byte emitted by the fixed canonical generator for `PHP_(h+1)^h`.

`ACCEPT_PHP` is legal only after every source byte and every generated byte have been consumed simultaneously. The generator uses nested pigeon/hole/pair counters and decimal/binary-index output state. Its live state is `O(log N_h)` bits. No line contains the whole source, a Resolution proof, a SAT label, or an arbitrary semantic consequence.

#### Complete fallback branch

For an `n`-variable source, the proof contains one `TABLE(a,j)` line for every assignment `a=0,...,2^n-1` in exact lexicographic order. The checker authenticates source-clause index `j` and verifies that this clause is false under `a`. `ACCEPT_TABLE` is legal only after all assignments are covered.

This branch may be exponentially large. It is not excluded or treated as free: every assignment, index, source access, proof bit and check is charged.

### Theorem 348A — locality does not restore cross-system hardness

There exists one fixed uniform sound complete exact-source refutation system `P_trace348` satisfying:

1. six fixed opcodes and parent arity at most one;
2. nodewise local transition checking;
3. `O(log N_h)` payload per special-branch node;
4. polynomial-time verification in source-plus-proof length;
5. for every canonical unary `PHP_(h+1)^h`, an exhibited one-byte trace with `Theta(N_h)=Theta(h^3 log h)` nodes, `O(N_h log N_h)` compact binary evidence bits when every node explicitly repeats its position, `O(N_h polylog N_h)` bit verification work, and `O(log N_h)` streaming writable state beyond read-only source/proof;
6. every UNSAT explicit CNF has a fallback proof.

Nevertheless the same canonical sources require `2^Omega(h)` ordinary Resolution lines.

#### Proof

**Soundness of the special branch.** Acceptance implies byte-for-byte equality with the fixed canonical `PHP_(h+1)^h` generator. That CNF is UNSAT by the pigeonhole principle. Every position is consumed exactly once, so deletion, insertion, reordering, sign mutation, count mutation, early termination, or appended data is rejected.

**Soundness of the fallback.** If every assignment has an authenticated source clause that it falsifies, no assignment satisfies the source. A SAT formula has a satisfying assignment and therefore no legal `TABLE` line for that assignment.

**Completeness.** Every UNSAT finite CNF has at least one falsified source clause under every assignment, so the full table certificate exists.

**Local/cost bounds.** The canonical PHP source has `Theta(h^3)` literal/clause tokens and `N_h=Theta(h^3 log h)` encoded bits/bytes up to the fixed byte factor. The exhibited verifier takes one transition per encoded byte, hence `Theta(N_h)` nodes. Because the executable proof explicitly repeats an `O(log N_h)` position field, its compact binary length is `O(N_h log N_h)`; omitting derivable positions could improve this, but that optimization is not claimed. A materialized verifier may store the source/proof; a streaming verifier keeps only counters and current records, while still paying every read and any reread.

**Separation from Resolution.** Haken's theorem gives exponential ordinary-Resolution size on these identical sources. Thus no polynomial same-source translator from `P_trace348` special proofs to ordinary Resolution can exist. The fixed local verifier is a stronger proof system, not a cheaper encoding of ordinary Resolution. QED.

### Corollary 348B — what the failed repair teaches

Exact-source authentication, finite rule names, bounded parent arity, polylogarithmic node payload, local transition checking, and fully charged polynomial verification still do **not** define a representation- or proof-system-independent invariant.

To preserve a hard-family lower bound, one must additionally:

- fix the inference semantics, as the project does with `R_mix341`; or
- restrict to an exact-source p-simulation class already known to translate into that fixed system.

Calling rules “local” is insufficient: local computation steps can collectively implement any fixed polynomial-time family recognizer. This does not show that `R_mix341` contains the recognizer rules, and it does not lower its `Wbar`.

## Fully charged ledger

| Phase/object | Logical count | Physical charge |
|---|---:|---|
| source grammar | none | every source byte read; headers, counts, literal ranges and terminators checked |
| PHP scan | one node per source byte/token | `h`, position and byte fields; canonical generator transition and two byte comparisons |
| compact PHP proof | `Theta(N_h)` | `O(N_h log N_h)` compact bits with explicit positions; test JSON is larger but polynomial |
| scan construction/output | same order | `O(N_h polylog N_h)` conservative bit work including formatting |
| scan verification | same order | source parse, source reads, expected-byte generation, transition and final-length checks |
| scan peak space | not a node metric | `O(log N_h)` streaming counters plus read-only inputs; materialization is charged if used |
| fallback | `2^n+O(1)` nodes | every assignment, clause lookup, source read, output bit and validation step |
| optimizer discovery | excluded from `W` | exhibited proofs are directly generated; any implementable search remains separately charged |

An exponential intermediate representation is allowed and correctly charged in the fallback. It does not prove exponential peak space, because streaming/recomputation can trade space for time. Conversely, the short PHP trace is a genuine polynomial certificate in this stronger system, not a claim of fast general SAT.

## Verification

### Iteration failures and repairs

The first finite harness attempted to construct the complete fallback table for the larger satisfiable deletion siblings. That is both exponentially expensive and unnecessary for the intended SAT control. It was replaced by the exhibited satisfying assignment: at that assignment no authentic clause is falsified, so the required `TABLE` node cannot exist. This is an exact soundness blocker, not a sampled shortcut.

An initial K4 parity-control generator also failed the expected eight-model even-charge check because the parity expression did not mask each shifted bit. The generator was corrected to XOR the three individual masked bits, after which the even K4 control had exactly eight models and the odd-charge control had none.

Finally, the post-run accounting audit rejected the initial `Theta(h^3)` node and `O(N_h)` evidence claims. The implemented proof has one node per encoded byte and repeats positions, so the certified bounds are the weaker but correct `Theta(N_h)` nodes and `O(N_h log N_h)` compact evidence bits. All reported hashes and checks below come from the corrected rerun.

Producer:

`experiments/arc/lspv5_348/local_streaming_php_proof_system_referee348.py`

Independent no-producer-import JavaScript checker:

`experiments/arc/lspv5_348/verify_local_streaming_php_proof_system_referee348.js`

Raw ledger:

`results/raw/arc/2026-11-04_1648_LSPV5_348_LOCAL_STREAMING_PHP.json`

Finite controls:

- canonical PHP `h=1,...,8`, exact source hashes and complete local scan traces;
- six independent corrupt-trace mutations per PHP source;
- one-collision-deletion SAT siblings for `h=1,...,5`, each with an explicit witness and no falsified fallback clause;
- contradictory-unit, Horn-chain and odd-K4 UNSAT fallback certificates;
- satisfiable unit and even-K4 controls, with exactly eight even-K4 models;
- eight malformed encodings.

Python producer: **133 checks**. Independent JavaScript: **109 checks**. Raw SHA-256:

`d8f18b5e5bf043698c6bd333c85daf60c75f53a8a9fb1e9cfdcc83a98f1f4d4f`.

Finite enumeration and host execution validate only the explicit construction. Haken supplies the asymptotic Resolution lower bound; it was not regenerated.

## Exact classification and bridges

- **PROVED/EXACT:** Theorem 348A and Corollary 348B for `P_trace348` versus ordinary Resolution.
- **COMPUTATIONAL:** finite source, trace, fallback, paired-label, malformed and corruption controls.
- **FALSIFIED:** verifier locality, finite opcode count, unary parent chains, polylog payloads, or polynomial physical checking as repairs for cross-system hardness invariance.
- **NOT CLAIMED:** that `P_trace348` is a legal subsystem of `R_mix341`; that PHP is hard for `R_mix341`; that one easy recognizable family refutes B2 or B3.
- **OPEN:** exact full `R_mix341` grammar and node-to-bit normalization; same-source simulation of every hypothetical polynomial SAT decider; B1, B2, B3; superpolynomial `Wbar_Rmix341`; unrestricted SAT hardness; P versus NP.

For ordinary Resolution, the canonical-PHP recognizer plus complete fallback still refutes the pointwise B1 statement, but its exponential worst-case fallback does not refute B2 or B3. For `R_mix341`, all three bridges remain open.

## Next unresolved step

The representation-independent search should not be repaired by further verifier-shape restrictions. The coherent next target is model-relative:

1. freeze authoritative `LOCAL-CONVERT`, exported-wire and payload semantics for `R_mix341`;
2. prove polynomial node-to-bit normalization for every legal node;
3. identify a fixed source-rooted computation-trace subsystem that `R_mix341` actually simulates with polynomial overhead;
4. then test whether that subsystem covers every hypothetical polynomial-time SAT decider, which is the B3/reflection obligation.

Step 4 remains the decisive missing transfer. No task, schedule, enabled state, role assignment, rule or weight was changed.
