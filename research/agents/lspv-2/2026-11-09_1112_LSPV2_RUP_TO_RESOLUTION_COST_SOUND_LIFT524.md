# LSPV-2/524: Cost-sound RUP-to-Resolution block lifting and expander-Tseitin class lower bound

**2026-11-09 11:12 PST | LSPV-2 Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

Affected [P2-L2-524]; refines still-OPEN [P2-A2], [P2-A4], [P2-A5]. Related [P2-L2-523], [P2-L3-538], [P2-L5-465], [P2-C3], [P2-D1], [P2-B1], [P2-B2]. All historical R_mix341 rules and weights remain unchanged.

## IDEA and falsifiers

Candidate: overapproximate a no-new-variable RUP proof-record addition by ANY acyclic source-rooted ordinary Resolution block with at most v paid inference nodes, costing one abstract record. This allows extra spurious blocks, so proving budgeted nonreachability can give a valid class-relative negative result.

F1: a valid RUP addition cannot be explained by at most v Resolution nodes plus one weakening. F2: eliminating weakening in the shared DAG creates more paid nodes or unsound pivots. F3: the chosen published expander-Tseitin family is not original strict 3-CNF or its cited lower bound is only tree/regular Resolution. F4: an allowed RAT, new-variable definition, GF(2), or unrestricted SAT decider has been silently excluded from the same declared calculus. F1–F3 are disposed of by the proof and original theorem, while F4 is an explicit limitation of the declared RUP-only system.

## Theorem 524.1 (PROVED/RESTRICTED)

Fix v≥1 and a signed CNF source F over variables 1,...,v. Consider any sound, finite RUP-only addition sequence C_1,...,C_r=empty, consisting of non-tautological clauses on original variables, where UP on F, preceding additions and the negated literals of C_i reaches conflict. No RAT, PR/SR, ER, GF(2), free semantic oracle or uncharged auxiliary introduction is permitted. Previously learned clauses may be reused globally.

Every such r-record refutation has an original-source-authenticated ordinary shared-DAG Resolution refutation with at most vr distinct paid Resolution nodes, no weakening. Therefore

$$
W_{\mathrm{RUP\ records}}(F)\ge \frac{W_{\mathrm{Res}}(F)}{v}.
$$

**Proof.** For one RUP check, record the ordered UP propagations and their antecedent reason clauses. Start at the conflict clause D and process propagations in reverse. If the current clause contains the complement of a propagated literal u, resolve D with the reason for u on pivot u. The resolvent remains falsified by earlier assignments. At most v distinct variables are propagated, so at most v Resolution steps occur. After processing all propagated assignments, remaining literals are falsified by the initial assumptions (negated target literals), so the derived clause D' is a subclause of C_i. Add a single temporary weakening D'⇒C_i to preserve all later exact learned-clause references. The complete finite proof is acyclic and source-rooted.

Eliminate all weakenings without increasing the paid Resolution count by induction through the DAG. Represent each original clause by itself and each later node K by a stronger K'⊆K. A weakening becomes a pointer to its stronger parent. For an original Resolution inference A∨x, B∨¬x ⇒ A∨B, if both strengthened parents still contain the complementary pivot, resolve them normally. Otherwise reuse the pivot-free parent, which already is a subclause of the original resolvent. Every new node is source-supported, every dependency remains earlier, and the final stronger subclause of the empty clause is the empty clause. Thus ≤vr Resolution inferences suffice. QED.

The abstract MAY system allows each unit-cost RUP step to be ANY at-most-v Resolution block, whether or not a concrete UP trail exists. Thus every concrete RUP transition has an abstract representative of the same cost; every concrete empty goal is represented. The abstract distance satisfies the same Resolution-derived lower bound. This is sound overapproximation, not a claim that every abstract path is realizable. The RUP/Resolution simulation is conceptually established in proof-complexity literature; no outside novelty is claimed for the equivalence.

## Published hard-family ledger and exact encoding

Use a family G_h of connected simple 3-regular expanders with h even vertices and linear edge expansion, with one fixed odd-parity vertex-charge vector. Each graph edge is an original Boolean variable, giving v_h=3h/2. At each vertex write the FOUR distinct proper signed width-three clauses that exclude exactly the wrong-parity assignments of its incident edge variables. There are precisely m_h=4h original 3-clauses and canonical indexed encoded length N_h=O(h log(h+2)). Odd total charge makes the source UNSAT.

Ben-Sasson and Wigderson, JACM 48(2), 2001, Definition 4.1, Lemma 4.2, Theorem 4.4 and Corollary 4.5 (attributed to Urquhart, 1987), prove an exponential size lower bound for unrestricted ordinary DAG Resolution on these expanders:

$$
W_{\mathrm{Res}}(F_h)\ge 2^{ch}
$$

for all large h and some c>0, after discounting the O(h) source leaves when necessary. Combining with Theorem 524.1:

$$
\boxed{W_{\mathrm{RUP\ records}}(F_h)\ge 2^{ch}/(3h/2)=2^{\Omega(h)}.}
$$

A proof-producing solver **required to output this restricted RUP log** must spend at least that many serial write actions. This says nothing about arbitrary SAT deciders. GF(2) Gaussian elimination refutes these same parity constraints in polynomial time; parity is a mandatory legal shortcut in stronger calculi. This strict-3-CNF statement needs no unproved 3-CNF reduction.

## Concrete and abstract transitions, replay and counterexamples

Concrete state tracks exact original source bytes/hash, source IDs, original variable count, learned clause IDs and order, RUP UP trail and reason indices, paid record count, and goal. A RUP addition is accepted only after authenticated UP replay. Abstract state tracks an acyclic Resolution DAG, its source and shared learned references, and unit-cost abstract block history. A block may freely choose any valid Resolution derivation of ≤v new nodes from existing clauses and source premises; its concretization overapproximates RUP possibilities.

A spurious candidate one-record RUP empty proof on odd K4 Tseitin is rejected: UP from original source stops without contradiction. A genuine full proof is generated by Davis–Putnam variable elimination, with 31 RUP additions and an 80-node pure Resolution replay. The K4 graph is a *finite control*, not an asymptotically certified expander.

A genuine one-record RUP empty refutation exists for the Horn implication chain H_n, while its pure binary Resolution proof requires n paid nodes. This is exactly the macro/micro accounting obstruction in [P2-L2-523], and it is retained rather than refined away. The satisfiable source (x1),(¬x1∨x2),(¬x2∨x3) has a valid nonempty RUP addition (x2∨x3) whose reverse-UP derived subclause is (x2); a Horn-3 UNSAT extension certifies explicit weakening removal in a proof DAG. No SAT source is incorrectly certified UNSAT.

## Independent replay and cost ledger

Locally implemented Python original-source checker, UP trace extractor, source-rooted Resolution/Weakening DAG compiler and strengthening eliminator passed **1,848 assertion groups** across Horn n=1..12, K4 odd/even signed proper 3CNF, one strict subclause case, seven malformed CNF controls, three corrupt RUP proofs, and source deletion. Original Python SHA-256 of odd K4 source: ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096.

Independently written JavaScript published at experiments/arc/lspv2_524_rup_resolution_lift_independent.mjs passed **1,328 semantic assertions** in a V8 replay after substituting only its Node-specific SHA-256 routine. The real Node crypto SHA operation was **not executed in V8**; SHA equality between languages is not claimed. Both independently recovered: odd K4, six variables, 16 clauses, 31 RUP additions, 80 pure Resolution inference nodes, 1,101 clause scans, 80 unit assignments, 2,456 proof-output ASCII bits, and 47 peak source-plus-learned database clauses. Python counted 3,432 literal tests versus 2,745 under JS's shorter-circuit scan policy. Python also measured 5,791 serialized JSON pure-proof bytes.

Resource accounting: unit-cost **logical** RUP record versus at most v logical Resolution inference nodes per expansion; explicit RUP proof output bits, all UP reason scans, source authentication, scratch assignments, DAG nodes and references, proof verification, output and cache retention are separate. Naive explicit output encoding may use O(rv² log(m+rv+2)) bits. These host-language counters are not a certified bit-time/peak-space implementation on the same FLMV machine. There is no general SAT-solver-to-RUP-output conversion and no polynomial-space implication from guest time alone.

## IDEA -> SEARCH -> ITERATE and previous-work audit

Read full root proof1.txt and proof2.txt, Nov 9 abstract-interpretation five-role refocus, issue #3 through LSPV-5/465, AGENTS.md, CODEX.md, project SKILL.md; actual LSPV-2/523, LSPV-1/539, LSPV-3/538, LSPV-5/465, Grok Nov 9 progress, Claude world ledger, and original MODELBRIDGE-0010. Prior /523 established only a Horn macro-vs-micro transfer barrier; /538 source-partition ceiling and /465 paid-label ceiling do not supply the RUP block theorem. MODELBRIDGE-0010's arbitrary-program reachability and normalizer barriers remain active.

Primary research: Ben-Sasson & Wigderson 2001 paper, actual Theorem 4.4 and Corollary 4.5 read and PDF-page inspected; Heule original DRUP description and its authentic RUP checker conditions; D'Silva/Haller/Kroening POPL 2013 ACDCL; Giacobazzi/Ranzato/Scozzari JACM 2000 complete shells; CEGAR literature. These papers supply established model definitions or methodology, not a universal Route A theorem.

Repository files verified: konard/p-vs-np README blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research README f397a7747eaca82df3d754d0a4b4bab1fe10f814, METHOD_INDEX 18d693ea71dfa433370eb7afbebc3106e32f03e5 and public Glucose3/RUP baseline 9e09b19aba57973ed8867794741c5006d47ed3b7. Other examined files: marijnheule/drat-trim README eb6ffcc4a85ff1c74a5995b6caae4372381dcd47; meelgroup/frat-xor format 986a21aa92b62f844ef1fce852193142c41b2b1f; MassimoLauria/cnfgen Tseitin generator 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; openai/math README cc5b0a03bca6c742f045d683b6647a6f44ef2cae. The requested pysathq/pysat README returned 404. No historical R_mix341 or native DRAT/FLMV executable was run.

The iteration replaces an unsound one-to-one RUP→Resolution step charge with cost-sound blocks containing ≤v internal Resolution inferences, adding a paid-global-sharing and weakening-elimination proof. Known hard source and genuine easy shortcuts are both retained. Unlike /523, this establishes an asymptotic lower bound **only for the fixed RUP-only certificate class**, with explicit source and model mapping.

## Publication, main status and remaining implication

Role-owned report, published independent executable and raw artifact are stored separately. The five-role handoff, root tracker and authorized main.tex region update require their own readback, noted in the associated coordination entry. This report does not assert publication of unverified companion writes.

**Remaining:** [P2-A2], [P2-A4], [P2-A5] OPEN. For every fixed uniform total correct polynomial-time SAT decider A with unknown exponents, the project still lacks an effective recursively iterable SAME-machine all-input SAT/UNSAT/malformed transformation with fully charged t'≤max(11/10,3/5+t/2) and s'≤max(1/2,s/2). Nor is a full native historical R_mix341 [P2-D1]/[P2-C3] lower bound or noncircular [P2-B2] established. No theorem forces arbitrary deciders to output RUP logs. All five roles, schedules, enabled states, 2 Route A/3 Route B allocation and historical weights remain unchanged. **P versus NP remains OPEN.**

### Post-replay abstract-interface clarification (same run)

For a **literal exact** transition correspondence, the abstract block must be interpreted as at most $v$ paid ordinary Resolution nodes **plus at most one zero-Resolution-cost weakening** exporting the recorded RUP clause $C$ from its derived subclause $D\subseteq C$. A raw Resolution-only block exporting exactly $C$ is not always available, as the explicit $x_2\vee x_3$ control demonstrates. Thus the correct MAY calculus is **Res + free interface-weakening**, not exact-clause-export pure Res. The complete-DAG strengthening induction in Theorem 524.1 eliminates all such weakenings without increasing the total paid Resolution node count, so any abstract goal path of $r$ blocks still yields a pure Resolution refutation with at most $vr$ paid nodes. The abstract block charge of one is a *RUP record* charge, not a historical R_mix341 rule weight. No proof status changes.
