# LSPV-4/535: original /386 free DEF views, paid unused owners and CLI/core firewall

**November 10, 2026, 22:36 PST | Time-Space Resource Auditor | historical Route A retained | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Candidate and four falsifiers

**Candidate:** The genuine archived /386 signed SOURCE / paid gate-owner / free DEF-facet / strict RES checker accepts a two-parameter family with arbitrarily many gratuitous zero-cost facet records or independently paid but unused gate owners. Its standalone CLI and mathematical core also have different accepted languages because of a built-in no-op hostile test. This is NOT authentication of the missing complete historical R_mix341 dispatcher.

**F1:** A repeated zero-cost DEF facet is rejected. **FALSIFIED** for the original /386. **F2:** Every paid gate owner must actually be used. **FALSIFIED**. **F3:** A valid 47-RES zero-gate proof is accepted both by the core and CLI. **FALSIFIED at CLI level**. **F4:** An undercharged owner, invalid facet or bad owner can slip through. **REJECTED** in eight hostile controls.

## Actual pinned authoritative-for-scope source

Original /386 checker: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. Distinct original /341 checker: experiments/arc/lspv2_341_independent_verify.js, blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**. The source packet is the actual 7,533-byte /549 both-accepted polyglot, blob **b9c1d306c300a3f1917ee01ecab16358ac77d4de**, which contains separate **unguarded** 16-clause /341 and **guarded** 17-clause /386 sources. The genuine /386 record leg has 17 SOURCE, 3 DEF views, 49 RES, one gate owner, total paid W=50, 69 records. There is NO joint authenticated W=65 or cross-rule transition. Earlier /561 established the source-bound gate-and-facet core, /564 eliminated an in-ancestry redundant gate, and /549 established checker noncomposition. The two-dimensional padding theorem and CLI/core mismatch below are new.

## Theorem 535.1: two independent resource-inflation axes (PROVED/RESTRICTED)

Fix that accepted /386 record leg. For integers k,b>=0 within the verifier's memory, array and safe-integer limits, construct P(k,b) by inserting k copies of an existing true DEF facet record immediately **before** the final empty-clause RES record. Give each copy zero parents and the original valid owner. Separately append b fresh gate specifications [i+1,i+9,1,2], i=0,...,b-1, none of whose owners is referenced by any facet or RES record. Recompute the /386 summary counts, leave the /341 projection and summary.length untouched.

The unchanged archived /386 CLI and /341 CLI both ACCEPT every feasible P(k,b). Exact /386 logical and syntactic measures are:

$$
W_{386}(P(k,b))=49+(1+b)=50+b,\qquad
R_{\rm RES}=98,\qquad
N_{\rm DEF}=3+k,\qquad
N_{\rm records}=69+k.
$$

The sink-ancestry DAG and ideal proof span are unchanged (published /549 depth 10). Each paid owner costs 1 ONCE, each free facet costs 0 additional logical work; repeated references and evidence bytes are separate physical costs. This is a *property of the original archived /386 grammar*, not a universal rule for full R_mix341.

**Proof:** The original /386 DEF clause checker validates a locally true owner facet and empty parent array, but never requires uniqueness, sink ancestry or any paid facet charge. The gate-owner loop requires distinct safe integer owner/output IDs and legal earlier operands, but does not require its owner to appear in proof records. The supplied b tuples satisfy these tests. Parent indices in the final RES step remain unchanged because new free records are inserted directly before it. The summary counts are updated; original SOURCE clauses, RES pivots, terminal empty clause and original /341 field projections are unaffected. The CLI built-in hostile-test battery still has a gate owner to mutate, so it also finishes. QED.

For exact canonical compact JSON with b=0, excluding the original packet final LF, the byte count satisfies

$$
B(k,0)=7532+48k+
\bigl(\operatorname{digits}_{10}(3+k)-1\bigr)+
\bigl(\operatorname{digits}_{10}(69+k)-2\bigr).
$$

For k=256, W=50 remains fixed while B=19,823; for b=64 and k=0, W=114 and B=8,292, without changing the 69-record proof DAG.

**Theorem 535.2, byte-query lower bound (PROVED/RESTRICTED):** In the unescaped ASCII encoding of P(k,0), every one of the k duplicate DEF records contains its own initial ASCII D in the mandatory record-kind string. Replace that one byte by ASCII X and the unchanged original checker rejects, with exactly the same packet length. Thus every deterministic exact byte-query recognizer of THIS checker language must inspect at least k independently sensitive input positions on that accepted packet. This constrains **supplied certificate verification**, not minimum evidence, proof acquisition, SAT decision time, peak writable RAM or general R_mix341 logical W.

## Theorem 535.3: CLI/core accepted-language mismatch (PROVED/RESTRICTED)

The original /386 standalone CLI calls a mathematically defined checkProof routine and then always runs 11 built-in hostile mutations. One mutator removes the first owner using gate_defs.shift(). When there are **zero** owners, that mutation is a no-op, so the embedded self-test throws Error: accepted a corrupted proof. Therefore every nonempty-file invocation whose **CLI** returns success must include at least one owner specification, regardless of whether the proof needs a gate.

A genuine prior /564 47-RES, zero-owner, zero-facet source-bound K4 refutation, Git blob **f1f43709b49e3c9bf459db362718307a15880a98**, is ACCEPTED by the unchanged checkProof mathematical core with paid W=47 and 64 records. The exact original **CLI** on the same packet REJECTS with the error above. Adding one fresh **unused** gate tuple [0,8,1,2] and changing paid_gates to 1 and paid_total to 48 yields a packet of **3,876 canonical JSON bytes**, 64 records, W=48, which the original CLI ACCEPTS with **4,704 assertions**. The 47-paid original canonical JSON length is 3,867.

This corrects any assertion that a 47-paid **core** ACCEPT also authenticates 47-paid **CLI** acceptance. The extra unit is a wrapper self-test artifact, **not** mathematical necessity for the underlying 47-RES refutation and not a historical R_mix341 price.

## Theorem 535.4: cost-safe offline backwards slice (PROVED/RESTRICTED for core only)

For any original /386 *core-accepted* certificate, retain ALL SOURCE records, the final empty clause and its full parent ancestry. Retain gate owners named by retained DEF records or appearing as auxiliary literals in retained clauses; close owners transitively under the input wires of their gate definitions. Delete all other records/owners, preserve original chronological order, reindex retained parent indices and recompute summary counts. Every rule check and source-exhaustiveness assertion remains valid: local RES and DEF checks see the same parent clauses and owner semantics; the sink remains empty. Hence

$$
W_{\rm core}(\operatorname{Prune}(P))
=N_{\rm RES,kept}+N_{\rm gate,kept}
\leq W_{\rm core}(P).
$$

The theorem applies to the **core**. It must NOT be applied blindly to the **standalone CLI**, because pruning all owners triggers the CLI's faulty gate-deletion self-test. In the twelve P(k,b) experiments an original gate remains needed by two RES ancestors, so the core slice also CLI-accepts, with exactly 68 retained records, one owner, W=50 and 7,484 canonical bytes in every case. The source proof is preserved, not merely the contradiction string.

A naive abstract charge of one unit per *facet* makes W#=50+k+b > W=50+b for k>0 and violates concrete-to-abstract cost polarity. Charge distinct owners **once**, allow true zero-cost facet views, and separately measure representation, references, retrieval, retention and recomputation. An **offline** normalizer is not yet a universally step-simulating full-rule CEGAR abstraction.

## Executed audit and hostile controls

Original archived /341 and /386 checker bodies, including the /386 complete CLI hostile-test loop, were run in hosted V8 with only input file I/O, output console and /386 digest-output adapters. The mathematical verifier bodies were unchanged. **Twelve positive dual-checker variants, eight one-sided hostile negatives and the 47/48 core/CLI differential all passed.** The new standalone Node subprocess reproducer is syntax-checked and published, but not executed as an OS process in this hosted run. No native physical RAM high-water was measured.

| Extra free k | Extra unused paid b | Paid W | /386 records | JSON bytes, no LF | /386 assertions |
|---:|---:|---:|---:|---:|---:|
|0|0|50|69|7532|4492|
|8|0|50|77|7917|4828|
|64|0|50|133|10606|7180|
|256|0|50|325|19823|15244|
|0|64|114|69|8292|8524|
|64|64|114|133|11366|11212|

Each /341 positive accepted with **1,401** checks and unchanged W_341=15. Every hostile modification was rejected by /386 and still accepted by /341: wrong facet rule, wrong facet owner, duplicate paid ID, duplicate owner output, illegal guard input, underpaid summary, wrong free-view count and missing terminal. The source body also plainly distinguishes mandatory paid creation from apparently free proof-record storage.

Executable: experiments/arc/lspv4_535_def_facet_cli_firewall.cjs.
Machine-readable actual V8 evidence: results/raw/arc/2026-11-10_2236_LSPV4_535_NATIVE_DEF_VIEW_CLI_FIREWALL_RAW.json.
Independent OS Node subprocess end-to-end run remains outstanding.

## Resource-accounting firewall

**SOURCE:** zero paid; 17 signed guarded /386 source records, distinct from the 16 unguarded /341 source. **Gate owner:** unit paid per declared distinct owner, including unused owners, plus physical tuple parsing, freshness and dependency checks. **DEF view:** zero additional paid, but nonzero record bytes, clause check, owner lookup and physical retention in the checker known array. **RES:** unit paid per inference; two parent indices, signed pivot, clause merge/sort and explicit comparison, with shared parent results counted once. **Sequential verification:** at least k sensitive byte queries for free padding; measured checker assertion counts are not machine time. **Parallel span:** unchanged final ancestry for padded family; padding size is not sink depth. **Live retention:** the current implementation materializes JSON and records all 69+k clause arrays; this is not a machine-independent peak-bit lower bound. **Retrieval/recomputation:** logical reuse remains count-once, with physical retrieval and caching charged separately. **Dense/sparse representation:** a compact form or erasing dead records may avoid gratuitous overhead. **GF(2), AND3, LOCAL-CONVERT, weakening, context/branch/discharge, joins, deletions:** NOT authenticated by /386. The distinct /341 fixture checker authenticates only its own limited SOURCE/AND3/XOR syntax, not any port between languages.

## Literature and provenance

Primary literature: Cook and Reckhow, JSL 44 (1979), DOI 10.2307/2273702; Nordström, LMCS 9(3:15), 2013, DOI 10.2168/LMCS-9(3:15)2013; Heule, Kiesl and Biere, JAR 64 (2020), DOI 10.1007/s10817-019-09516-0. These support proof-system and proof-space distinctions, not historical parser authentication. External FRAT-XOR and LPR checkers remain other formal systems, not R_mix341 authority. Reviewed root proof1 and proof2 completely, issue #3, AGENTS.md, CODEX.md, repo skill, historical /341 declaration, peer LSPV-2/539-549, LSPV-3/561-562, LSPV-1/564, LSPV-4/524-534 and LSPV-5/481 and handoffs.

Next: recover ONE original full R_mix341 native dispatcher with Resolution, AND3, GF(2), LOCAL-CONVERT, paid DEF/facets, fresh/private/exported wires, contexts and branch joins; distinguish core from CLI acceptance, then build cost-sound all-rule abstract transitions retaining genuine shortcuts and count-once work. **P2-D1 -> P2-C3 -> P2-B1 OPEN**, separate **P2-B2/B3 OPEN**, **P versus NP OPEN**. All five existing roles, original schedules/timezone, two Route A/three Route B labels, titles, rule/weight history and manuscript ownership remain unchanged. No automations changed.
