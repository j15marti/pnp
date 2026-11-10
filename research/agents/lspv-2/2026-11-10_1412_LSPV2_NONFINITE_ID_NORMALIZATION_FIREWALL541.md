# LSPV-2/541: Native JSON nonfinite IDs defeat parse-stringify certificate normalization

**November 10, 2026, approximately 14:12 PST | SAT-Circuit Reduction Builder, historical Route A | PROVED/RESTRICTED checker-specific lemma and COMPUTATIONAL controls | P versus NP OPEN**

## IDEA and four falsifiers

Candidate: The immutable recovered historical /341 SOURCE/AND3/XOR fixture checker accepts two distinct nonfinite numeric proof or SOURCE identities created by valid JSON exponent notation. A naive JSON parse-stringify pass collapses those identities, rejects an originally accepted packet, and therefore cannot be substituted for the full accepted-byte transition relation in a cost-sound lower-bound abstraction.

Predeclared falsifiers: F1, ECMAScript JSON.parse rejects 1e400 or -1e400; F2, the actual recovered checker rejects the altered identities; F3, JSON.stringify preserves distinct Infinity and -Infinity keys; F4, a changed original signed clause, different proof DAG structure or different inference count is responsible for any verdict difference. All four are ruled out in the executed original-code differential controls.

## Exact historical files, encoding, and scope

Pinned immutable original producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, Git blob 4081022e8a3841d79f751a3d3a7a10decbb026da. Pinned recovered original fixture checker: experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0.

The baseline packet is the original odd-charge K4 Tseitin formula: six edge variables, 16 original signed proper ternary CNF clauses, 15 distinct paid AND3/XOR inferences and original-source signed proof ancestry. The checked packet has one fixture. The original checker is NOT an authenticated parser for the complete historical R_mix341, despite the prose listing Resolution, LOCAL-CONVERT, paid DEF, defining facets, fresh/exported/private wires, contexts, branching, weakening, discharge, join and deletion. Those remain unknown native accepted-byte operations, not disallowed operations.

ECMAScript JSON.parse converts the valid numeric JSON tokens 1e400 and -1e400 into Number values positive and negative Infinity. JavaScript Map distinguishes those keys. ECMAScript JSON.stringify converts nonfinite Number values into JSON null, collapsing both. This behavior is specified by ECMA-262, Structured Data (https://tc39.es/ecma262/2022/multipage/structured-data.html) and Map SameValueZero key semantics. It is not a new historical proof rule.

## Theorem 541.1: Checker acceptance is not preserved by naive JSON canonicalization

Let C be the exact pinned recovered fixture checker, and define

$$
N(b)=\operatorname{JSON.stringify}(\operatorname{JSON.parse}(b)).
$$

Then there exists a valid JSON UTF-8 proof packet b with

$$
C(b)=\mathrm{ACCEPT},\qquad C(N(b))=\mathrm{REJECT}.
$$

Proof by explicit counterexample: Starting with the authentic accepted standalone K4 packet, replace EVERY string occurrence of paid node ID d0 with the numeric JSON token 1e400, and every occurrence of d1 with -1e400. All definition IDs and parent references are modified consistently. Original signed source clauses, graph, proof rules, all truth tables, parity equations, paid inference count, source labels, source ancestry and sink remain unchanged. The original checker accepts the modified raw JSON because the parsed Map identities positive and negative Infinity remain distinct. On N(b), both IDs and parent references become null; the second definition fails at the original fresh inference ID guard. Thus N(b) is rejected.

An independent SOURCE-provenance variant replaces every s0 ID occurrence by 1e400, and every s1 occurrence by -1e400, including their references. It also passes the original checker. After N, the duplicate null SOURCE IDs violate its original unique source ID guard. Again the underlying signed formula and 15 paid inference records are unchanged.

This is a constructive theorem for the recovered fixture checker, not proof of a legal general R_mix341 refutation, not evidence of SAT hardness and not an impossibility theorem for an identity-aware renaming canonicalizer.

## Theorem 541.2: A verdict-preserving parse-stringify pass can expand certificate bytes

In the accepted K4 packet, change the source charge vector from [1,0,0,0] to [1,1e-6,0,0]. The original checker accepts because its bitwise XOR coerce operation reads this small nonzero charge as zero. JSON.parse obtains the finite Number 0.000001, and JSON.stringify prints the longer decimal representation. The output packet remains accepted but has **four additional ASCII bytes**. Hence an assumed nonincreasing explicit certificate-bit-length cost cannot follow from checker acceptance alone. The experiment does not show that a shortest possible accepted encoding needs the longer form.

## Reproducible original-code and independent results

- Executable original-code runner: experiments/arc/lspv2_541_nonfinite_identity_replayer.cjs.
- Independent Python JSON/identity control: experiments/arc/lspv2_541_independent_json_semantics.py.
- Full raw accepted/rejected packets and check diagnostics: results/raw/arc/2026-11-10_1412_LSPV2_541_NONFINITE_IDENTITY_RAW.json.

The unmodified recovered producer and checker mathematical bodies ran in isolated V8 with only Node file-input/stdout adapters replaced. Original repository blobs were separately authenticated through GitHub. Original seven-fixture regression passed **30,714** assertion groups. The 13 targeted raw-byte packets included **eight original ACCEPT and five original REJECT**. Exactly two accepted packets became rejected after parsed-object reserialization: the nonfinite pair of paid IDs (fresh inference ID diagnostic), and the nonfinite pair of original SOURCE IDs (unique source ID diagnostic). In addition, valid finite numeric ID pairs 100 and -100 survive; duplicate paid Infinity or null IDs, a dangling parent, an invalid terminal/charge control and a malformed exponent are rejected. The charge 1e-6 accepted packet expands by four bytes. All accepted ID controls preserve 16 original source clauses and 15 paid nodes.

The independently executed Python 3 control passed **16 assertions** about numeric overflow, positive/negative infinity distinctness, null-key collision under the explicitly defined conversion, finite ID stability, and strict JSON serialization rejection. It is not itself the historical checker.

Execution guard: the published Node CLI's actual SHA-256 and original Git blob validation have NOT been executed as a native OS Node process in an original local repository checkout. The exact committed audit function was run from GitHub-fetched source in V8 with SHA outputs deliberately omitted. The raw result ledger contains no invented SHA-256 values, but Git blob checks validate original code provenance. No FLMV machine, complete historical full-rule checker or R_mix341 lower-bound optimizer was executed.

## Sound abstract interpretation, CEGAR and resource polarity

A checker-relative concrete state must distinguish raw byte certificate b from parsed object p, preserve the SameValueZero identity partition of all source and shared paid IDs (including Infinity vs -Infinity), the authenticated independent signed-CNF source bytes/hash, semantic node types, ordered inference edges, first-paid history and, in the still-unrecovered complete calculus, live contexts, owner definitions/facets, global freshness, exported/private wires and branch discharge.

Define an abstraction alpha that retains parsed typed identity classes and whole shared-DAG source/owner dependencies, with a concretization gamma containing every accepted raw-byte representation compatible with those classes. The abstract successor of every admitted concrete step must include its projection at cost no GREATER than concrete charged cost, and every completed concrete refutation must remain a represented abstract goal. A naive serializer that merges positive and negative infinity into null and then replays only this normalized packet EXCLUDES an accepted concrete path, violating the required transition overapproximation. Keep original byte costs and first-creation shared-node charges separate, and keep missing full-calculus operations as conservative MAY transitions until authenticated.

CEGAR control: coarse normalization pretends the two distinct numeric identities can be a single null identity; its normalized witness fails concrete original-checker replay at freshness, while the genuine raw witness passes. Refining identity classes to retain the signs of nonfinite values restores the accepted path. This is a transition-representation refinement, not a proof of the mathematical soundness of the historical fixture checker. Its previously established SAT-source forgeries remain a separate problem.

Paid logical work is 15 for the original K4 proof and stays 15 for the accepted mutations; proof bytes, checker wall time, discovery, parallel span and physical peak memory are distinct. No free semantic oracle or extra historical rule weight is introduced.

## Literature, corpus reconciliation, novelty and exact obligations

Read both complete root trackers, issue #3 and recent peer comments, AGENTS.md, CODEX.md, pnp-research skill, November 9 governing handoffs, original /341 producer/checker and declared calculus, LSPV-2/537-540 and peer LSPV-1/553-556, LSPV-3/539-548 and /551-553, LSPV-4/525, plus earlier MODELBRIDGE-0010 through the current coordination corpus. Direct external repository checks: konard/p-vs-np scripts/proof_status.json SHA 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor format.md SHA 986a21aa92b62f844ef1fce852193142c41b2b1f; and tanyongkiam/cake_lpr README.md SHA e94f45e9aa000cd9ada12f4c771ac9daf28fe53c. None supplies the complete /341 native dispatcher. Primary methodological sources: Cousot and Cousot (1977), POPL, and Cook and Reckhow (1979), JSL. External FRAT-XOR and LPR define DIFFERENT proof languages.

LSPV-2/540 already established duplicate decoded JSON key shadowing; this new test instead shows **non-colliding raw and parsed numeric Map identities** collapse ONLY under a serializer transformation. LSPV-1/556 ghost affine rows and LSPV-3/551-553 satisfiable-source acceptance are separate prior findings, not claimed new. Adopted the authentic original execution and true XOR shortcuts; rejected only the *naive* normalization as a universal native proof preprocessor; retired no prior sound theorem or historical rule.

Material evidence [P2-L2-541] supports still-OPEN native grammar [P2-D1] and cost-sound complete abstraction [P2-C3]. [P2-B1] full-calculus superpolynomial minimum and separate noncircular [P2-B2]/B3 remain OPEN; [P1-01], [P1-03], [P1-04] remain OPEN. Root main.tex may be reconciled only in LSPV-2 ownership; no edits to others' regions. All five task identities, titles, schedules, time zones, enabled states, 2 Route A / 3 Route B labels, fixed historical rule grammar and weights remain unchanged.

**Next exact target:** Find the genuine all-rule native dispatcher and an externally source-bound valid RES-to-AND3, LOCAL-CONVERT, paid DEF/facet and discharged-branch accepted byte corpus; extend the replayer only after authentication. **P versus NP remains OPEN.**
