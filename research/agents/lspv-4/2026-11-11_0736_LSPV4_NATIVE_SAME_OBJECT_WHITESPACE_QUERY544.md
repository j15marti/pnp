# LSPV-4/544: Original /386 same-object whitespace exact-byte resource theorem

**2026-11-11 07:36 PST | PNP Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## One candidate theorem and four falsifiers

**Candidate:** For a source-authenticated original archived /386 accepted byte packet, arbitrarily many trailing ASCII JSON spaces leave the parsed proof object, original signed SOURCE, all globally paid owners, full shared DAG, and native logical W unchanged. Nevertheless, each added byte is acceptance-sensitive for exact-byte language membership. Any deterministic verifier with individual random-access byte queries that recognizes the same original accepted-byte language must inspect every added position on an accepted padded packet. This theorem is about **supplied-certificate acceptance**, not optimal proof size or SAT decision time.

F1: the unchanged original checker rejects padded inputs or changes its 31 paid units. F2: Node JSON.parse maps trailing whitespace into a different proof object. F3: replacing a single added space by ! still accepts. F4: the resource argument silently charges extra bytes as native paid proof work or claims the **minimum** W_R grows.

F1-F3 fail by source analysis and authenticated finite replay. F4 is explicitly excluded by the exact tariff ledger. Mandatory cheap GF(2), extension variable, learned-lemma branch reuse, retention/recomputation, large-ID, compact affine row and abstract-overcharge controls remain OPEN for the missing historical all-rule calculus; no unverified rule is excluded.

## Authority, corpus, prior work and duplicate check

Original archived /386 checker source: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. Original accepted 3,080-byte K4 packet: results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json, Git blob **25b5c1f95734f6eae36bdbb4a17c948c00753cff**. Original CLI checks SOURCE, globally paid conservative AND2 owners, genuine zero-extra-paid DEF facets, strict binary RES and eleven bundled negative controls. It is a recovered sibling checker, **not** the full historical R_mix341 dispatcher.

Read complete proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (blob 7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3), issue #3 and latest peer comments, AGENTS.md, CODEX.md, pnp-research skill, original /386 and /341 checker code, current handoffs, relevant LSPV-2/539-549 and /555-558, LSPV-3/544 and /567-571, LSPV-4/531-543, LSPV-5/487-488R1 and the earlier LSPV-1/571-573. Surveyed the five agent directories, coordination and raw experiment results. Root main.tex was inspected for the owned LSPV-4 region and earlier overlapping proof/report claims.

**Novelty limit.** LSPV-4/532 proved sensitive-byte query cost in a separate canonical full-affine-row test grammar; /533 proved a shortest-certificate representation bound only in that grammar. LSPV-5/488 already showed ignored JSON-field padding with unchanged W and N, and corrected overreading /543's 2N reference-slot bound as a claim about all accepted-input byte lengths. LSPV-2/557-558 and LSPV-1/572 showed noncanonical same-object accepted encodings. The narrower increment here is a **same parsed object**, *exact original full CLI* family with an unbounded number of individually decisive trailing bytes and a deterministic decision-tree lower bound. JSON whitespace syntax and the decision-tree adversary are established basic techniques, not newly discovered principles.

Primary literature reviewed: Cook and Reckhow's proof-system relative-efficiency framework [1]; Cousot and Cousot's concrete/abstract semantics [2]; Baek-Carneiro-Heule's FRAT proof-format-specific parsing and elaboration results [3]. FRAT, DRAT and FRAT-XOR/XLRUP are **FAILED TRANSFERS** as definitions of this historical checker. Decision-tree query cost is an exact transfer only in the specified per-byte query model; it is not a transfer to arbitrary Turing-machine SAT lower bounds.

## Theorem 544.1: native-accepted constant W with exact-byte Omega(k) queries

Let b denote the exact archived accepted K4 seed above, including its original terminal LF. For every integer k>=0 define

$$
b_k=b\Vert {\tt 0x20}^{k},\qquad L(k)=3080+k.
$$

For each k for which the original Node checker can represent and finish processing the byte string, its actual accepted-byte program satisfies

$$
\mathrm{Accept}_{386}(b_k)=1,\qquad
J(D(b_k))=J(D(b)),
$$

$$
W(b_k)=30_{\mathrm{RES}}+1_{\mathrm{owner}}=31,\qquad
N_{\mathrm{records}}(b_k)=49,\quad R_{\mathrm{parents}}(b_k)=60,
$$

$$
B_{\mathrm{evidence}}(b_k)=8(3080+k)\quad\text{bits}.
$$

D is Node Buffer UTF-8 decoding and J is its actual JSON.parse. Exact original source, defined gates, signed clauses, inference references, paid counters and terminal goal are identical as *parsed objects*, not merely semantically equivalent formulas.

**Query lower bound.** Let V be any correct deterministic verifier for the original complete CLI accepted-byte language, with known input length and read-only random-access access to *one byte per query*, without a free syntax oracle, preverified checksum or canonical-encoding promise. Then on accepted b_k,

$$
\boxed{Q_V(b_k)\ge k}.
$$

Thus serial one-byte-query time is at least k byte-probe steps. This is **not** a circuit-depth or unrestricted parallel-span bound, since k independent probes could in principle run simultaneously.

**Proof.** JSON permits ASCII spaces after a complete top-level JSON value. Consequently b_k and b parse into the identical value. In the original program the complete original checker, its 11 structuredClone corruption tests, owner checks, SOURCE checks, RES checks and payment counters depend on this parsed object alone; the file's SHA-256 is diagnostic output after acceptance, not a check input. Thus all those checks accept with W=31. For every added index j, replacing only byte j (a space) by ! yields a non-whitespace byte after the completed JSON document; JSON.parse throws and the original CLI rejects. If V accepted b_k without querying position j, its adaptive observations would be identical on the rejected neighboring packet. Determinism would force an incorrect acceptance. Every one of the k positions must therefore be queried. QED.

**Physical-model caveat.** An actual Node implementation has finite byte, array and heap limits; this is a quantified per-input family under successful execution, not a lower bound for an unbounded real computer. The original fs.readFileSync allocates a raw Buffer of size L(k), and content is used again by the diagnostic SHA after proof checking. This is an original-program **Buffer allocation** of L bytes, not a physical RSS measurement. It does not imply a universal verifier needs Omega(k) writable RAM: a read-only-input checker may rescan at logarithmic workspace as in /541. Removing redundant whitespace from a *supplied* accepted packet preserves W and yields a shorter accepted certificate; thus there is no lower bound on shortest proof length.

## Finite original-checker replay and hostile controls

Fetched and Git-blob-pinned the exact unchanged original 6,345-byte archived checker body. Executed its original mathematical proof checks and all eleven built-in hostile controls per positive under hosted V8 Function invocation. Adapters only supplied filesystem input, a **diagnostic-only** SHA placeholder and JSON-semantic structuredClone of the ordinary JSON proof objects. This is **not** a separate OS Node subprocess and no physical heap/time measurement was made.

| Extra trailing spaces k | Exact input bytes | Paid W | Proof records | Original checks | Original bundled hostiles | Original accept |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 3080 | 31 | 49 | 3750 | 11 | YES |
| 1 | 3081 | 31 | 49 | 3750 | 11 | YES |
| 16 | 3096 | 31 | 49 | 3750 | 11 | YES |
| 128 | 3208 | 31 | 49 | 3750 | 11 | YES |
| 2048 | 5128 | 31 | 49 | 3750 | 11 | YES |

**18,750 original assertion groups and 55 original bundled negative cases passed.** Every input parsed to the exact same object. All **128 of 128** single-space-to-! neighbor mutations were rejected by the host JSON parser. Four representative positions 0,1,63,127 were separately submitted to the entire original checker body and rejected at JSON.parse. Prior /540-/543 native original-source and invalid-pivot hostile controls remain applicable to this same seed.

Committed standalone executable audit experiments/arc/lspv4_544_native_json_whitespace_query_audit.cjs pins both original Git blob SHAs, runs **unchanged OS Node checker subprocesses** for k in 0,1,16,128,2048,8192, tests all 128 JSON neighbors and five original-CLI hostile cases including wrong SOURCE. **That standalone OS script was written but not executed in this hosted run.** The executed hosted-V8 raw ledger is results/raw/arc/2026-11-11_0736_LSPV4_544_NATIVE_WHITESPACE_QUERY_RAW.json. No random seeds or statistical sampling.

## Exact charge, verification, retention and recomputation ledger

| Authenticated operation | Native paid charge W | Evidence bits / reference application | Sequential verification / parallel inference span | Retention, retrieval, recomputation and peak writable space |
|---|---:|---|---|---|
| Original signed SOURCE | 0 | Exact original clause, provenance source vertex, no premises | Native sequential source validation; leaf of DAG | In the original JS, input record plus a clause reference in known; a read-only verifier may rescan |
| New conservative AND2 paid owner | 1 once globally | Four fields ID, output z, input a,b; gate freshness and availability | Source-code map checks; one gate-dependency stage | Globally retained owner/definition set; multiple facets cost no new W |
| Genuine defining DEF facet | 0 extra | Owner ID and true signed facet; no parents | Definition look-up; no extra paid deduction span | One record/known slot in the original; repeated or shared facet costs zero native W |
| Strict binary RES | 1 per record | Two earlier parent indices, signed pivot, exact canonical resolvent | Two parent retrievals and resolvent check; one additional DAG node depth | Result in known; recomputation/rescan costs physical operations, not native W |
| Trailing ASCII whitespace | 0 | k additional sensitive bytes; parsed record set unchanged | At least k serial single-byte probes for exact membership, unbounded parallelism can reduce span | Original content Buffer has L(k) bytes; 49 dat.records and 49 known slots remain fixed |
| 11 built-in original CLI mutations | 0 | Clones of decoded object, not extra proof rules | 11 sequential corruption test attempts | Transient clones, no claim 11 copies live simultaneously |

The actual logical charge for every b_k is **one globally paid owner plus 30 distinct RES nodes = 31**; 60 parent references and all true facet uses carry no *additional* logical tariff. The original /386 executable separately keeps dat.records and known arrays with at least 2*49=98 indexed reference entries in this family. No double-counting is allowed when merging proof cones: the previously proved /540 owner-incidence intersection must be subtracted before summing subproof charges.

**Exact resource firewall.** Any scalar abstract path charge which both (i) majorizes each physical input-byte probe and (ii) is bounded by actual native W on *every* concrete path is impossible on this family for k>31. Indeed Q>=k>W=31. The repair is to keep distinct resource dimensions: W_native, T_verify, Q_byte, parallel span, live retention, peak writable space and discovery. A sound completed-proof abstraction can map each b_k to its original parsed proof at **equal native charge** W#=31, while recording separate physical Q>=k. It does not yield an all-rule stepwise alpha/gamma for R_mix341.

## Corpus reconciliation and open obligations

**Adopted:** /540 original accepted shared-owner K4 packet, /541 verifier-versus-proof-space firewall, /543 original reference-slot semantics, /488 independent OS verification and parser-field padding control, /558 original raw-byte noncanonical accepted-language controls. **Rejected/retired:** transfer of the separate /532-/533 artificial mandatory-affine-row bound to the historical calculus; identification of native logical proof work with file size, verification time, heap allocation or SAT decision time; first-key-only parser assumptions. **Changed relative to root main.tex:** new *same parsed object* constant-W, arbitrary trailing-byte sensitivity and exact deterministic per-byte query lower bound for the recovered /386 sibling checker only. No historical source, rule weights or global proof status changed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt and proof2.txt were completely read but not edited. [P2-D1], [P2-C3], [P2-B1] stay **OPEN**. [P2-B2] and [P2-B3] stay separately OPEN. P1-01/P1-03/P1-04 and P versus NP remain OPEN.

**Next test:** find an original, historically authoritative **single-dispatcher** accepted packet connecting genuine RES to AND3 or paid DEF to LOCAL-CONVERT, with actual cross-rule corrupted-port rejects. Its full fixed weights, source binding and contextual legality must be authenticated before an all-calculus cost-sound abstract transformer and a nonreachability attempt can proceed.

## Primary literature

[1] S. A. Cook and R. A. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44 (1979), 36-50. https://doi.org/10.2307/2273702

[2] P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977. https://doi.org/10.1145/512950.512973

[3] S. Baek, M. Carneiro and M. J. H. Heule, *A Flexible Proof Format for SAT Solver-Elaborator Communication*, TACAS 2021, 59-75. https://doi.org/10.1007/978-3-030-72016-2_4
