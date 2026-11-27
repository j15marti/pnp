# Track 3 | Fused probing, prefix syzygies, and permutation transport
2026-11-27. Ground-Up UNSAT Bounds. P versus NP OPEN; no public release.
 
## 1. Authentication and scope
Read governing E/B directive 869007811cfe4a6b703e7f111111b820f3afcb03, shared UNSAT directive b1e93ffb3f7698009554e3a6fe19c20e0d06067a, identifiers 67fe81e50ce5c54a67966d5dda1bb0843b84da3c, registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c, release gate fc87c43ad1a247e4133b931911f7cfa4afeb17c0, AGENTS blob 2426c9197cdad0e8cd3b13f5b58bc86ffb4c2ae2 (including operative section 4A at commit 7a4cc13032ca2e51af42c878684c4a36723b7b4e), CODEX blob 15639f62a254aa9cd36a949b9f9d81985e5ed538, skill blob 6f37fc1a1713b01abd91794d5523fb05a57efa2f; issue 328 checked at startup, before imports and before publication, latest comment 7227828852 at final check, including user-authorized 4A redirection 7227825314. No local checkout or repository preflight; no manuscript reassignment, schedule change, or public repository edit.

Pinned corpus e315349cd6c1fe3fa696504859f28312f6aab69a and compiler 21b9d53fb8166c819b24e708656c742cd3c24f10. Executed compiler, recomputed exact SHA-256 and length (native, CNF and map hashes match registry; prior JS SHA implementation checked on empty and abc vectors, not independent OS crypto). Native-only discovery used network, not source map or reference UNSAT proof; separate provenance-assisted CNF comparator. Exact original IDs:
* EB-JOINT-24@e84a0ab6dc6f / STRICT-EB4-v1:sha256:e84a0ab6dc6f74deb8daeea2ccd41cca90e3d1294411877a813471760897c209; N=5363624 bits; vertices 0..18930, ports 0..75723, edges 0..37861. CNF-JOINT-24@68d21d234f32 / DIMACS-CNF-v1:sha256:68d21d234f32956200617b3a714d9f81f992cf2fa373f1285d639d6a703fa22b; N=13416; variables 1..24, clauses 1..170. Native/map/CNF bytes 670453/382840/1677.
* EB-RANDOM-3CNF-40@8a18e86479df / STRICT-EB4-v1:sha256:8a18e86479df916ea5c7fdd760ccd561e4fea3737a94517ab8dc2d28cc7e6bdb; N=5027816 bits; vertices 0..17764, ports 0..71059, edges 0..35529. CNF-RANDOM-3CNF-40@cfaccaa692ef / DIMACS-CNF-v1:sha256:cfaccaa692ef736e2b5eaadde2eda83ca7351e30cf066237fbe5c63eedb55e67; N=17480; variables 1..40, clauses 1..184. Native/map/CNF bytes 628477/358445/2185.

All root contradictions: guard EMPTY, residual ROOT. Internal gauge carrier 11=0 uses global complement symmetry, not an unconditional fixed original port. Carrier ID min original port+1; exact signed root map and projection trace reproducible from certificates and pinned checker. Do not import arbitrary consequences across gauges. No mismatch/import-stop triggered. Source-only parents none; cooperative parents listed below.

## 2. Native projection and complementary lanes
Native helper 303d735ba73855b69b47df734d4d3686f760b215 (previous T3_native_transport_replay/native.js), peer helper 519ccfbb027d840dd3f9e9c3fea78d68f8e7e099b (peer.js). Signed BFS for E and edges; exact integer B=2 support table via all local words; local forbidden-word CNF; resolution elimination with pair cap 128, width cap 8, nonincreasing active clause count. All resolvents of an accepted pivot included, tautologies discarded, canonical duplicates collapsed. Independent set-based projection replay. For accepted elimination, existential projection is exact and active variable+clause count strictly decreases; rejected pivot not a progress theorem.

|Event or size|JOINT|RANDOM|
|---|---:|---:|
|BFS arcs|184582|173234|
|local words|12608|11776|
|carriers|643|593|
|peak clauses|3941|3681|
|eliminations|617|553|
|candidate pairs|11432|10922|
|incidence literal scans|5201714|4473594|
|replay pairs|10742|9985|
|full clause replay scans|1317455|1118721|
|residual clauses|291|367|
|residual carriers|26|40|
|baseline DPLL nodes|23|61|
|baseline discovery clause scans|10942|48490|
|baseline discovery literal inspections|22156|116088|
|source CNF comparator DPLL nodes|41|63|
|source CNF comparator scans|9038|24953|

Unary probing: if unit propagation conflicts under v=b, add its negation as unit by RUP; otherwise each propagated literal l permits binary clause not(v=b) OR l by RUP. Reclose. Source-only JOINT 22 records through first empty, 25733 discovery scans (including trailing-loop bug), full independent replay 11717, trimmed replay 6709. RANDOM unary alone no additions at fixed point (78 probes, 57986 scans); fallback 61 DPLL nodes, 48490 scans, 61 RUP steps verified in 36932 scans. DPLL proof records and certificate IDs below. Parent peer T3 RUP certificates independently replayed in full (scope, factor projection, support, entailment, RUP), only distinct nonempty first-half clauses whose carriers remain live imported under same gauge; root closure after every import, no peer final contradiction imported.

|Cooperative accounting|JOINT|RANDOM|
|---|---:|---:|
|parent bytes|55065|51383|
|parent projection words|13488|11776|
|parent factor scans|217826|186300|
|parent entailment rows|4886|5167|
|parent RUP scans|10253|41490|
|imported live clauses|5|14|
|reclosure scans|2986|10486|
|hybrid discovery scans|638|78952|
|hybrid RUP through first empty|1|41|
|trimmed independent checker scans|638|24967|

RANDOM hybrid unary solved without DPLL. Initial nested-loop bug: continued probing after first empty on JOINT solo and RANDOM hybrid, so some original final status fields were UNKNOWN despite valid earlier empty. Append-only trim at first empty replayed exactly, original full sequences also verified. Never counted trailing records as necessary. Initial results.json write hit call limit; no claim it exists. Corrected proof files and this ledger preserve results.

## 3. New fused pair-to-unary closure
Pair-only lane tries two Boolean pins; conflict by UP proves negated guard as a width-two RUP clause. Root UP after each addition, unary probes deferred to end of sweep. At 2,000,001 clause scans (2M cap), both UNKNOWN; JOINT 1052 probes, 1043 additions, 298080 checker scans, peak 1334 clauses; RANDOM 1253 probes, 805 additions, 391874 checker scans, peak1172. Control (not a OR not b OR c) AND (not a OR not b OR not c): unary probes do not find a binary consequence, pair guard a=b=1 yields not a OR not b, checked. This is a rule-specific comparison, not hardness.

Fused lane: initial unary failed-literal pass; pair guard RUP; after each binary insertion immediately check complementary binary pairs and failed unary probes at its endpoints; root reclosure. New proof certificates checked by independent literal-array RUP verifier. No DPLL invoked in either terminal lane.

|Source-only fused lane|JOINT|RANDOM|
|---|---:|---:|
|probe trials|21|525|
|binary additions|0|18|
|unit additions|11|8|
|empty|1|1|
|RUP steps|12|27|
|discovery clause scans|18540|447105|
|discovery literal inspections|38822|1123747|
|checker clause scans|6118|34051|
|checker literal inspections|12174|80282|
|peak clauses|303|394|

Fused succeeds at same 2M scan cap where deferred pair-only lane stalled. It is slower than baseline DPLL in terminal clause scans, not claimed net speedup or minimum proof. No universal coverage. No complete fixed point claimed for capped pair-only lane. No exact physical time/space measurement.

Scoped proof of polynomial numeric credit: on fixed chart of r live Boolean variables, at most L=1+2r+4*binom(r,2) distinct non-tautological width <=2 clauses (including empty); deduplicate. Each accepted learned clause decreases L minus the number of acquired such clauses. One complete pass costs at most O(r^2) probes plus reclosure and immediate endpoint probes; O(r^2) productive passes plus at most one no-progress pass. Each UP requires at most r+1 sweeps, on O(N+r^2) explicit clauses of width <=8. Replaying each learned clause by negating it and UP is sound by RUP. All failed probes charged; literal/index representations use O(log N) bits; deterministic full scans instead of free hashing give a fixed polynomial bit bound, and polynomial live storage. A standard serial tape simulation by full scans is polynomial; CM <= T*S on that execution. This is a fixed-chart stage, not an arbitrary residual-transfer credit. Exact DP decreases n+m before this stage. If both stall, another certified terminal or global contraction must be acquired; no proof of universal cooperative progress. Unit/pair credit and T2 rank/row credit may complement each other but chart changes and multiple live branches cannot replenish credit freely. Potential may be used as a lexicographically phased fixed-stage budget, not a global theorem. Finite pair-probe order effect motivates randomized candidate discovery with exact deterministic checking; fingerprint lane below directly tests model sensitivity. Neither a favorable random seed nor a finite success establishes universal progress.

## 4. Exact certificate pins and broadcasts
All listed new files in this directory were created append-only and read back by exact commit. Root IDs and source pins above are inherited in this table, all guard EMPTY/residual ROOT. Certificate IDs are CERT-v1:sha256:<digest>.
|file|commit|SHA256|
|---|---|---|
|JOINT-24.certificate.trimmed.json|d454492d22a107d93174653d4de48e0b1ad72bb2|962e0525996ea751506a44ff2d78f1442be7df148753c41c034730e984bf3db9|
|JOINT-24.hybrid.trimmed.json|d1f067dfdab79bdb45550970c2231c1d16df399a|206f8dc4e5b836eee8f14b06ee4d3d6e41de3f5922a188e3eb2affe981c50f74|
|RANDOM-3CNF-40.certificate.trimmed.json|5ba6d7277b8a5d43a9dbc48d4b958173b5995676|9a71a1cee712ac505ccff08411fd57ba66b54f8c6a21951dc3dde07d76bba7e1|
|RANDOM-3CNF-40.hybrid.trimmed.json|06b845697c1837e19a913d82cda6b9abe84fc87a|7a8e4a960910ed03bff83903761318d267c9db29e24b773be72058092bad821a|
|JOINT-24.fused-probe.json|d7bc29b4b4d97706a70099b21e47b06e27709978|0680cf34750e4ee17222c88a5f3a192811581b1f1deb445b1cca09244ec291ef|
|RANDOM-3CNF-40.fused-probe.json|cc955c7958f06c4cada0563ed00de6c393dcfce4|a27ed4ad28df73b7177f86e855c5738bfa1e6f88f87e56a67432557e7c18a136|

Code probe.js 30970509f04ed303ea07babef4600d4232c60dd3; pair-probe.js 21e769efa39e1192d8d487605067ccb896c569a9; partial proof files JOINT-24.pair-probe.json 11de183b17e0cab28e5ce981b9932518beec7c51 and RANDOM-3CNF-40.pair-probe.json 5fe393eabacbc0bb50f134dcdfdb0908b782360b; fused-probe.js dc71d8845e58db780e4280018913e7eedf15e678. Fused proof bytes 3986/3832. Hybrid parents CERT-v1:sha256:e9cc262ab1878891075098950611caf6306a0e7dc91b35f7b5b0f654fe14fb66 (#7225739103, pin 5f886529e0affe5a6329b1d019170a2f61a32e60), CERT-v1:sha256:bc5604d6f69adeafdd5a77db0193c8f81186ec96f548f7e944ff1798971d3a48 (#7225739612, pin 88dab009c7b89b93965ced660beca916108027f4). Broadcast comments #7227747812, #7227748341, #7227789952, #7227790376.

## 5. T1 independent replay and parallel-prefix syzygy
RANDOM native root ID and scope as above; parent T1 CERT-v1:sha256:8b5d088fab3dd98f1e9a10da85caaf053183ea2cb4ca722f7887c42e8019754b (#7227554625, pin 8c6c5c3494db0de454ed090c30f602213c68767f). Verified certificate hash, native hash, independent signed normalization and exact local B tables, replayed 1 pin and 554 eliminations, 171 final factors, 11776 initial rows, 44402 projection checks, 15047 factor candidates and 6702 support rows for local base entailment (not trusting factor IDs). All 358 DAG nodes (98 base, 260 resolution), max width4, DAG depth27, replayed. Local identities tested on 5146 exhaustive local assignments.

In Boolean ring over F2, let h_i indicate clause i is false. For resolution parents a,b, h_i=h_i h_a+h_i h_b: on false resolvent exactly one parent false by complementary pivot. Let P_i=product_{j<i}(1+h_j), with empty product 1. Then P_i h_i=0 for every derived clause because the parent complements occur in P_i. Telescoping first-failure partition sum_i P_i h_i=1 because final empty-clause indicator is 1. Thus sum_{base i} P_i h_i=1. This is a checked syzygy in acquired residual representation, not a direct low-degree original-port identity. Source correctness follows checked projection and weakening, complement gauge discharge.

Parallel prefix doubling computes all prefixes in O(s log s) exact one-bit AND gates and O(log s) depth after acquiring a topological list of s indicators. For 358 nodes: 9 rounds, 2711 AND gates, vs naive 63903 prefix-product upper bound; clause indicator depth <=2 for width4, final 98-term XOR balanced tree depth7; include one gate per base product and charge input indexing. 512 first-failure and 1024 prefix sample words all passed; local identities exhaustively checked. No inference of uniform polynomial proof acquisition from evaluation depth. Prior T2 first-failure idea #7226011294 is conceptual, no imported deductions from it.

Files t1-syzygy-audit.js 3ad184ab948dc54dc44eb56906866e6bb9209d18; t1-syzygy-results.json a63dc9dfde4eef6fa0528c7d9b9fc59e0f6bfb64; RANDOM-T1-prefix-syzygy.certificate.json d2c6b456ac9d2b0c65a5a954fda7983cb289b0e1, CERT-v1:sha256:ef28a820668a38f7506891ed78e98a470b9829c87a0d527bb9ff9ab3dda012a4. Broadcast #7227821144.

## 6. Secondary MFC-13 and replay
Read peer original report research/proof-spine-2026-11-26/closure-exceptional-syndrome/2026-11-27_0855_T3_replay/report.md at 62760844323adb1f308f60e621f7d869a1bbb3e2 (earlier ES01 pin 967f8109c272b3b1224f36a4dbb256832df2634b reported there). Fixed five-plane atom (15,32),(13,17),(14,36),(11,53),(10,39), target29. Enumerated all 3^5=243 choices, convolution on 64 states, sole missing29. Reciprocal lift span(u,v) -> span(a,b+u), span(b,a+v) with fresh private zero target: private equations alpha1=beta2, alpha2=beta1 force exact bijection of nonzero coefficient pairs to original (x1,x2). All 243 original words checked for depths0..5, 5 to160 owners, ambient6 to316, 38880 leaf-owner inspections at depth5, all sums identical. Provided history, no provenance-free recognition or arbitrary guard test. Fixed atom size, not growing arbitrary MFC family. Code/raw as in section5. No new canonical MFC instance broadcast. Nov26 replay correction: deterministic transcript is function of source, not necessarily polynomial-time recoverable. A faithful replay in polynomial(actual T+N) does not give fixed polynomial(N) without bound on T. Did not rerun all Nov26 variants.

## 7. Permutation transport extension and precision audit
Replay pinned transport-access.js 97378ed252e791646a0723b42f6a38f31a7e3a43, 29 prior schedules; r256 D=18287 cuts, M=2816 map bits per side, full buffer one crossing and 94146 travel; remote local38994 plus2816 reads. Family F(pi,sigma) has implications X_i->Y_pi(i) and X_i->not Y_sigma(i), plus OR X_i; UNSAT iff pi=sigma, otherwise singleton X_i and corresponding Y bit witness. Prior proper-3CNF compiler n=8r-1,m=10r. Recomputed registered instance PERM-256-UNSAT@2418f3e87116 / PERM-TRANSPORT-BITSTRING-v1:sha256:2418f3e871160a56ffeca60cd9ab0dacadea1f09d87f6be3013f52549132d527; N=98336 logical bits; hash over exact ASCII 0/1 serialization, no LF; vars1..2047, clauses1..2560, logical bits0..98335; source manifest 229ca31c8e4859a0b430d9bd004cf5c56caa13b5, generator pin above, guard EMPTY/residual ROOT. Parent earlier transport theorem #7226147908 (scope extension, not advice).

Original fixed-state one-tape theorem: for each cut, deterministic splicing requires distinct diagonal crossing transcripts; r! diagonals, h=log2(r!), expectation Omega(h) crossings for fixed control. Sum D=Theta(N) cuts => worst-case Omega(N^2) time; same execution input-inclusive CM Omega(N^3). Restricted model, not general bound. No transition-level TM simulator executed.

New fixed-sweep complete-state theorem. Deterministic read-only locally moving input head, q publicly fixed alternating full sweeps, complete mutable state (including control, work tape/head metadata) transmitted at each middle cut, no hidden timing, remote source access or free external storage. For one cut, if two distinct diagonal inputs have identical q state transcripts, splice their left/right halves and induct across sweeps: off-diagonal SAT hybrid has the same rejecting transcript, contradiction. Thus transcripts injective over r! possibilities. If each transmitted state is <=s bits in a fixed-size encoding, q*s>=log2(r!). For variable-length prefix-free complete-state codes, concatenated q states are prefix-free; entropy under uniform diagonal implies expected total bits >=h at each cut. Summing cuts counts distinct crossing events, yielding E[CM_state]>=D*h, even excluding read-only input. For fixed number contiguous work tapes, complete state can be encoded within O(S_work+1) at known sweep/cut, so Omega(D*h)=Omega(N^2) work-plus-control CM in this discipline. Not valid for hidden addresses/timing or unrestricted remote access. r256 q=1 needs >=1684 bits, q=4 >=421. Not an unrestricted superpoly result.

Probabilistic lane: choose prime p>4r, compare two map polynomials degree <r evaluated at uniformly random field point. On diagonal always agrees, on off-diagonal at most r-1 roots, false UNSAT <1/4. O(log r) bits state, one pass after charged prime selection via trial division (prime exists below 8r by Bertrand), exact field arithmetic; uniform point by rejection sampling expected O(log r) random bits, bounded trials may return UNKNOWN. Fingerprint agreement is NOT a certificate. Exact deterministic alternative uses r distinct points in r sweeps; no reliance on hash collisions. Random-access exact bitwise comparison O(N) probes and O(N log N) address traffic, uniform O(log N)-depth XOR/OR circuit. Full encoding/permutation validation separately polynomial. Streaming fingerprint operates on promised valid pairs; does not solve arbitrary input. Exact finite precision, no semantic oracle. Randomized and deterministic results kept distinct.

All 576 pairs at r4 and 90 seeded pairs per size r8..256, total1116, all field points per pair, 193752 evaluations. Max observed roots 3/6/12/27/33/21/11 for primes17/37/67/131/257/521/1031. All collision bounds and exact evaluations passed; all552 r4 SAT witnesses plus5 per other size checked; no claim every larger sampled encoding independently witness-checked. Reproducible seeds in runner; not uniform success-rate evidence. Files fingerprint.js 2688762e7d3afa35f56b38bda4abbb0f6164eea8, fingerprint-results.json b838e46cd2b01e8adea33056bca1791ab75ba6cb; permutation-sweep-transport.certificate.json 27745fa12d75d0691a7fc5e58963d8a5528cdd18, CERT-v1:sha256:42889411db75696cb8a1a61b0c9063f24567e45979800e6e682f95fc86d4babe. Broadcast #7227828852. No registry overwrite or new claim for sampled unregistered permutations.

## 8. Cost and release ledger
Discovery, repeated normalizations, independent checks, failed attempts and parent imports are not amortized away. Three full projection discovery repetitions alone cost >=15605142 /13420782 incidence literal scans on JOINT/RANDOM; five projection replays >=6587275/5593605 full clause scans, plus T1 separate factor replay. Different scan kinds not equal-cost bit events; no single 10M total cap. Terminal caps per lane only. Parent artifact reading and communication bytes, SHA, generator, original IDs, proof copying and indexing separately charged; host measured physical bit time, peak heap and CM unavailable. Native benchmark work is finite experimental evidence, not minimal complexity; exact no-branch stage has scoped polynomial resource upper bounds, fallback DPLL only finite capped results, arbitrary live-branch ledger open. No net aggregate speedup from cooperation proven. Independent replay implementations are not external peer review of universal theorem.

Checks: DISJ/guard integrity PASS scoped native certificates; unrestricted transfer FAIL for physical transport via random access; relativization/algebrization/natural proofs OPEN/not invoked as general separation arguments; DTISP restricted fixed-sweep and one-tape only; deterministic configuration recovery not a polynomial replay bound. No universal proof of collective progress across spines or of unrestricted superpolynomial lower bound. Explicit public release blockers: no fixed polynomial global progress on all valid E/B inputs, no unrestricted superpoly theorem, no complete independently audited proof. No pvsnp publication.

## 9. Research search log
Fresh primary literature search: Hennie (1965) crossing sequences, NASA bibliographic record; Roughgarden communication complexity lecture notes on equality/rectangles; SAT preprocessing handbook search, bounded variable elimination and probing; Heule/Hunt/Wetzler clausal proof-checking paper, DRAT checker. No PDF or kernel build claimed. Fresh external searches: official Anthropic formal-math repository README (blob 8e775b8f647333a7ab2d388a5c0343c168c0177c), OpenAI math README (blob 9dc39b832c0b6d9416c18a9c8d396bcda80ce351), Google DeepMind formal-conjectures README (blob 29ba0c01538ecfbd8ef0f5383200f6230014073f), Google OR-tools stable ortools/sat/probing.h (blob d42750653dbfc50e18b9f6ae67a54391878bf6ea), specialist marijnheule/drat-trim README (blob eb6ffcc4a85ff1c74a5995b6caae4372381dcd47). xAI/Grok SAT formal proof search found no pertinent solver/checker implementation. External formal math artifacts not used as proof premises; no independent replay of them. Internal search CHARGED-UNSAT-TRANSPORT1, static ratio docs at 62760844323adb1f308f60e621f7d869a1bbb3e2, transport branch results tmr1-headtransport096-20261115 and tmr4-mcsp-transport-026-20261114; partial branch search only, not exhaustive. MFC search, T1 peer reports and issue 328 checked. Further native queue not executed in this run. 

Next proof target under AGENTS 4A: cooperative epoch must guarantee either exact terminal or strictly decreasing global credit; analyze stalled cases with independent seeded probe-order trials, charge all trials, and seek deterministic polynomial hitting family or conditional success bound. Current fixed-chart clause credit alone does not certify coverage. Preserve exact guards and original N.
