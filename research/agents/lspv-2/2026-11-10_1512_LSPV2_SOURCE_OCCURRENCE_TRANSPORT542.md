# LSPV-2/542: Source-occurrence transporter over a separately typed native fragment

**November 10, 2026, 15:12 PST | LSPV-2 SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED lemma + COMPUTATIONAL control. P versus NP OPEN.**

## Candidate and four falsifiers

**Candidate:** Retain an original /341 SOURCE/AND3/XOR certificate byte for byte, and bind it to an independently supplied strict signed-3CNF original source whose clause occurrence order differs. Transport a certified signed-clause occurrence bijection into the pre-existing source-bound reference checker LSPV-2/539. Preserve every paid identity, dependency and shared DAG, and classify unknown rule bytes as MAY rather than as invalid full-calculus rules.

F1: a clause permutation breaks semantic correctness or paid cost; F2: a sign mutation is mistakenly treated as a permutation; F3: a genuine paid redundant AND3 is excluded; F4: a checker-accepted SAT-source forgery or unauthenticated RES/LOCAL-CONVERT is treated as a valid cheap refutation. All four passed the explicit restricted controls.

## Precise precedence and source scope

LSPV-2/537 authenticated the recovered /341 SOURCE/AND3/XOR fixture corpus; /538 exposed an accepted false support-string AND3; /539 **already** constructed a separate typed source-bound fragment checker with positionwise source equality and accepted redundant paid work; /540 and /541 identified parser/normalization pitfalls. LSPV-3/551 **already** published an accepted SAT-source packet and /554 established the two-goal operational/semantic no-go. The only new research object here is an **occurrence-bijection transporter extending /539** to independent signed original-source orderings. These earlier results are not relabelled as new discoveries.

Historical original producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, blob 4081022e8a3841d79f751a3d3a7a10decbb026da.
Historical limited checker: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0.
Independent reference checker: experiments/arc/lspv2_539_strict_fragment_reference.cjs, blob fc91a6f33d0d010d6225365a3d9ce72a090af21f.
Original previously accepted SAT-source control packet: blob 706947c767361e7c979b8208677eb983d33838f4.
New executable: experiments/arc/lspv2_542_source_permutation_transporter.cjs, blob c50c1620cf8bcbce26dd78f748f94b1e980211b8.

The recovered verifier is a fixture tester, **not** an authoritative parser for the complete declared R_mix341, which includes Resolution, LOCAL-CONVERT, paid DEF/facets, exported/private wires, context branching, discharge, joins, weakening and deletion. Unknown operations remain unauthenticated, not eliminated. The full original tariff and formal rule scope are preserved.

## Theorem 542.1 (PROVED/RESTRICTED)

Let F be the original strict proper signed 3-CNF carried in a separately well-typed SOURCE/AND3/XOR proof packet P accepted by REF-539, with m original SOURCE clause occurrences. Let F' be a separately supplied strict proper signed CNF whose *multiset of signed clause predicates* agrees with that of the packet, even if clause occurrence or within-clause literal order differs. Construct a mapping phi by grouping external clauses by their sorted signed triple, consuming exactly one external occurrence for each original SOURCE label, and verifying that all groups are exhausted.

The mapping phi is a bijection, preserving exact signed clause predicates, hence

$$
\bigwedge_{j=1}^{m}C_j \equiv \bigwedge_{j=1}^{m}C'_{\phi(j)}.
$$

For **reference semantic replay only**, reconstruct the packet-order source listing and invoke the already proved sound REF-539 typed checker. Every SOURCE predicate still follows from F', each derived AND3 is its verified parents' truth-table conjunction, each attached affine alias is pointwise equivalent, and each GF(2) XOR is an exact consequence. Shared references reuse the same proposition. Therefore a REF-539 terminal 0=1 proves F' UNSAT.

The certificate packet raw bytes and original SOURCE IDs are untouched. The external source byte stream and its SHA-256 are tracked separately, and phi is recorded. The original proof's paid IDs, dependencies, logical weight and dependency span are identical:

$$
W_{\mathrm{ref}}(P,F')=W_{\mathrm{ref}}(P,F)=|\operatorname{PaidDistinct}(P)|.
$$

This is a count-once cost for the **same reference proof**, not a lower bound on the optimal full-R_mix341 proof. Multiset indexing and normalization must be charged in any eventual machine runtime; no free uniform compiler or machine-space claim follows.

A restricted exact abstract state is (source hash, raw certificate hash, phi, verified typed DAG, paid IDs, goal tag). For verified typed transitions, alpha/gamma preserve the reference goals and assign equal one-unit paid inference costs, with zero additional inferential payment for reuse. For an encountered unauthenticated RES/LOCAL-CONVERT record with otherwise parseable fields, the executable emits UNAUTHENTICATED_MAY and abstract cost floor zero. **This is NOT sound coverage of the complete historical byte grammar**, because unknown valid full-native source/context/definition forms might fail earlier reference parsing. Full P2-C3 remains OPEN.

## Executable differential tests

The published transporter was independently fetched and evaluated alongside the original producer, original fixture verifier and REF-539. Exact original JavaScript bodies were executed in isolated V8 with Node I/O and crypto adapters. No stubbed crypto digest is presented as a measured SHA256, and no OS Node full-repository execution or full-calculus parser was performed.

**20 deterministic controls**: the seven authentic odd-charge cubic Tseitin fixtures (K4, K3,3, cube, Petersen, prism6, prism16 and bridged K4x2), each with an original and externally permuted signed-clause source, yield 14 valid reference outcomes. A legal 16-paid K4 redundant AND3 with the permuted external source also passes. A wrong source sign, corrupt AND3 truth table and previously published genuinely SAT-source forged packet fail the separate reference semantics. RES and LOCAL-CONVERT records remain MAY. Totals: **15 VERIFIED_SEPARATE_FRAGMENT, 2 UNAUTHENTICATED_MAY and 3 rejected/exception controls**.

On K4 source permutation, s0 maps to external clause occurrence 1 and s1 maps to occurrence 0; 15 paid nodes and the raw packet remain unchanged. The genuinely redundant 16th paid inference passes the separate reference, whereas the recovered historical fixture checker rejects it due solely to the fixed 4V-1 length guard. The original unmodified checker on all seven original fixtures accepted **30,714 assertion groups**; the previously published two-fixture genuinely SAT-source forgery was also **accepted, 2,273 assertion groups**. This records an operational/semantic distinction already known from /551 and /554.

The byte-level raw ledger contains original exact K4 certificate bytes, canonical and permuted independent source bytes, a 16-paid redundant certificate, full Git blob pins and per-control outcomes:
results/raw/arc/2026-11-10_1512_LSPV2_542_SOURCE_PERMUTATION_RAW.json.

## Literature, repository search and guards

Read both root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (preflight blob 6338814517505963386646c288a4ecb47c68bb77), current issue #3, AGENTS.md, CODEX.md, repository skill, recent /554, assumed-time and abstract-negative handoffs; actual LSPV-2/537-541, LSPV-3/549, /551, /554 and LSPV-4/526 evidence; old MODELBRIDGE-0010. Change-aware originals: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2, blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5. Neither identifies a full /341 historical native parser.

Primary literature checked: Cook and Reckhow (1979), Relative Efficiency of Propositional Proof Systems, DOI 10.2307/2273702; D'Silva, Haller and Kroening (2013), Abstract Conflict Driven Learning, DOI 10.1145/2429069.2429087; Giacobazzi, Ranzato and Scozzari (2000), Making Abstract Interpretations Complete, DOI 10.1145/333979.333989. Their general theorems do not authenticate local project bytes.

The local OS preflight could not run because git clone failed name resolution; verified GitHub connector reads and V8 executions were used. An owned-only main.tex edit requires a complete current blob and unchanged outside-content check. Preserve all existing roles, tasks, schedules, allocation and tariff. Status remains [P2-D1],[P2-C3],[P2-B1], separate [P2-B2]/B3 OPEN; P versus NP OPEN. Next: recover an authoritative native RES/LOCAL-CONVERT/DEF/branch accepted packet and checker, not another invented reference grammar.
