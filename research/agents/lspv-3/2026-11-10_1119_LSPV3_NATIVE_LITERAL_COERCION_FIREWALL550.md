# LSPV-3/550: Native /341 SOURCE-literal coercion and decision-sensitive accepted bytes

**2026-11-10 11:19 PST | LSPV-3 Hypergraph & Proof Certificates | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected nodes:** [P2-D1], [P2-D3], [P2-C3] and new restricted evidence [P2-L3-550]. [P2-B1], [P2-B2], B3 and both unrestricted proof spines remain OPEN. This report authenticates behavior of the actual recovered *SOURCE/AND3/XOR test-fixture verifier*, not a full historical $R_{\mathrm{mix341}}$ proof grammar.

## IDEA, four falsifiers, model

**Candidate:** The recovered native /341 verifier accepts noninteger JSON values in *semantically active original signed-literal slots* through JavaScript numerical coercion, even though its published theorem assumes integer-valued source literals. This admits arbitrarily padded accepted bytes at fixed paid logical proof work and yields a direct raw-byte-query lower bound for recognizing the accepted test language.

Precommitted falsifiers: F1, exact integer type guards on original source-literal slots reject all such substitutions; F2, preserving numeric coercion changes checked factor tables or proof ancestry; F3, changing the underlying signed integer value is still accepted, so coercion equivalence is unsound; F4, padded accepted literal tokens have zero positions that can be changed without changing acceptance. F1-F2 failed, F3 and F4 were excluded by negative controls.

**Exact source:** Original 2026-11-02 /341 producer, repository path experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, blob 4081022e8a3841d79f751a3d3a7a10decbb026da. Original independent checker, experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Original declared semantics, research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb.

## SEARCH, precedence and scope

Reviewed both *complete* root proof trackers (startup proof1 SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2 SHA c920eaea9e74fefa314e0ca0291cc9b537052a02), issue #3, AGENTS.md, CODEX.md, the pnp-research skill and both November 9 abstract-negative/FLMV handoffs. The local preflight script was unavailable because there was no full local Git checkout. Read relevant original LSPV-3/491 and /549, current LSPV-1/553, LSPV-5/413, /419 and /435, GROKPROOF 2026-11-10_1523 progress and the Claude world ledger.

**Precedent not duplicated:** LSPV-5/419 established that several *metadata* fields are ignored and the core graph and source fields are partly checked. LSPV-5/415-416 found **ID** numeric/lexical aliases. LSPV-5/435 found ignored branch annotations. LSPV-1/553 proved that the recovered checker has only AND3/XOR dispatch and a hard-coded proof length, so it is incomplete for declared RES, LOCAL-CONVERT, DEF and arbitrary paid DAGs. Here the new observation is **source-literal numeric coercion in an actual checked semantic field**, and the accepted-language byte-query theorem below. The strong wording “all charge and literal fields are strictly typed” is not supported by the original executable.

Change-aware original external reads: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; openai/math and the Claude world ledger as scope controls. Those external formats do not supply missing native rules.

Primary literature: Cousot and Cousot, *Abstract Interpretation*, POPL 1977 (DOI 10.1145/512950.512973), for sound concrete/abstract transitions; Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 1979 (DOI 10.2307/2273702), for polynomial verification versus proof length. FRAT-XOR has explicit record formats but is distinct from historical /341. No primary external theorem determines this repository-specific parser behavior.

## Theorem 550.1: exact original-literal coercion fiber

Let $V$ be the unchanged original recovered verifier and $P$ an accepted fixture. Choose one original signed integer literal $a\ne0$ from its source clause array and substitute a JSON value $z$ with JavaScript coercion

$$
\mathrm{ToNumber}(z)=a.
$$

Keep source and proof IDs, graph, parents, paid nodes, AND3/XOR data and other fields fixed. Then the returned verifier object and check count are exactly unchanged:

$$
V(P[z/a])=V(P).
$$

**Proof from the actual code.** Every read of original clause-literal values passes through Math.abs(x)-1, x<0, lit>0 or lit<0, or through Math.abs(x) comparisons with numbered graph-edge incidences. Clause truth tables are reconstructed from these converted values; source factors contain only the resulting support and table. No typeof, Number.isInteger, strict original-literal identity test, original-source byte hash or raw-literal serialization is applied to these source slots. The helper validateCNF checks *separate hardcoded parser controls*, not the original fixture clause array. Therefore equal ToNumber values give identical source incidence, forbidden-pattern sets and factor tables. Topological induction over the unchanged shared AND3/XOR DAG gives identical inference tables, rows, ancestry, deletion witnesses, final contradiction and count. QED.

Examples: numeric 1 may be replaced by JSON strings "1", "+1", "0001", " 1 ", "1e0", "0x1"; arrays [1], [[1]]; or JSON boolean true. Signed -1 may be replaced by "-1". These are invalid *strict integer-typed JSON source-literal fields*, though they represent identical signed CNF clauses under coercion. Exact original verifier acceptance does **not** imply that the full, undeclared historical R_mix341 grammar intended these representations.

## Theorem 550.2: an accepted fixed-paid-DAG family with k sensitive evidence bytes

The accepted original seven-fixture packet contains K4 with 16 original proper signed 3-clauses and 15 paid nodes, and 321 paid nodes in aggregate across seven fixtures. Replace the first source literal number 1 by a JSON string containing k leading zero bytes followed by digit 1:

$$
L_k=0^k1.
$$

For every supported length k, ToNumber(L_k)=1, so the recovered verifier accepts the altered packet P_k without changing any proof node, original *semantic* CNF, or returned checker result. Its raw encoded byte length increases by k+O(1). For every one of the k zero positions, changing only that ASCII 0 to ASCII 2 changes its ToNumber to a different positive number (or infinity) and causes the exact original checker to reject with “Verifier: signed incidence mismatch.”

**Decision-tree proof:** Consider any exact deterministic byte-probe recognizer of the *same recovered accepted-packet language*. On accepted input P_k it must query every one of those k positions. If it fails to read position j, changing the byte there leaves its execution transcript identical but changes acceptance. Thus

$$
Q(P_k)\ge k.
$$

The theorem is about recognizing this accepted *byte language*, with constant paid work and a fixed underlying original semantic formula. It does not bound SAT decision time, proof search, or the entire mixed calculus. A physically finite parser only handles lengths within its implementation limits. This result directly rules out charging *all explicit evidence* as a function only of distinct paid node count and canonical semantic source size; evidence bytes and source-read costs need a separate ledger.

## Theorem 550.3: additional nonbinary charge acceptance

The recovered verifier computes an XOR of its charge vector using JavaScript bitwise XOR, implicitly coercing operands to 32-bit integers, and tests source-clause forbidden-pattern parity with strict non-equality but does not require charge values in {0,1}. On the original K4 packet, changing the first charge 1 to the JSON string "1", boolean true, array [1], real 1.75 or integer $1+2^{40}$ leaves the bitwise XOR aggregate equal to 1 and all original source patterns accepted. Replacing charge pair (1,0) by (3,2) also succeeds. The checked source clauses, genuine XOR contradiction and proof cost are unchanged. This is a **charge-schema typing defect**, not an unsound refutation of a satisfiable source. A fixed full grammar must type-charge the vector or derive the true charge from the canonical source.

## Cost-sound restricted abstraction and explicit limit

Fix the graph, source IDs, original numeric literal values, complete proof DAG, fixed paid IDs, contexts, annotations and all nonliteral fields. For the accepted original-literal coercion fiber, let alpha project a packet to its canonical signed integer clauses *while retaining* the entire DAG, source IDs, paid-node history and row/assumption fields. Let gamma include all supported raw literal encodings with the same ToNumber numeric values and identical other fields. Then P belongs to gamma(alpha(P)), the original SOURCE factor constructor commutes with alpha by Theorem 550.1, all unchanged AND3/XOR steps commute, terminal acceptance is preserved, and the abstract charge is exactly equal to the concrete distinct-node charge.

This is an **exact restricted quotient**, not the complete P2-C3 abstract transition system. In particular the projection drops raw source bytes, SHA authentication, encoded evidence length and implementation time. It must not be used to claim those resources are small. General charge normalization beyond the explicitly tested fixed-source fiber is also not established. Missing RES, LOCAL-CONVERT, DEF, branching, discharge and private/exported wire grammar remain conservatively **UNKNOWN**, never omitted.

## COMPUTATIONAL checks and publication scope

Fetched the exact original producer and checker source blobs, evaluated their unchanged function bodies in V8 with only CLI input/output wrappers replaced. The original seven fixtures yield exactly 30,714 checks. Tested 27 mutants: **19 accepted** with exactly identical full returned verifier objects and check counts, **8 rejected** at the expected source, charge or proof consistency guard. All seven lengths k=1,2,4,8,16,32,64 were accepted and all **127 individually edited zero-byte neighbors rejected**. All-source literals converted to JSON strings also passed. A 4,096-zero accepted literal provides an evidence-growth control. Direct independent K4 truth-table enumeration gives 0 satisfying assignments for odd-charge source and 8 for the even-charge control.

**Actually executed raw V8 record:** results/raw/arc/2026-11-10_1119_LSPV3_550_NATIVE_SOURCE_COERCION_RAW.json, Git blob beb7d4b1241bd56536473602adccc8dd450ada55.

**Published native Node reproducer:** experiments/arc/lspv3_550_native_literal_coercion.cjs, Git blob 7ff819168cfa51e7462e0a4a6c733472cdf770bd. It pins the two original blob SHAs, calls the original Node producer and verifier as child processes, independently checks signed-CNF truth tables and strict source types, and runs the same controls. The **new Node reproducer was not executed in this run**; its existence and Git readback alone must not be misrepresented as authoritative CLI execution. No complete historical checker was found or run.

No automation, schedule, identity, rule or fixed weight was changed. The next load-bearing artifact is an authoritative accepted byte example for RES->AND3, LOCAL-CONVERT, paid DEF owner/facets, exported/private wire references or branching/discharge. Until then [P2-D1], [P2-C3], [P2-B1], [P2-B2], B3 and P versus NP remain OPEN.

