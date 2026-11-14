# TMR-2/025: MCSP negative-certificate cylinder sandwich and the update-time gap

**Pacific timestamp:** November 14, 2026, 10:24 PST (America/Los_Angeles). **Role:** NEW TMR-2 Information Necessity. **New result:** elementary exact query-certificate theorem, **CANDIDATE/RESTRICTED** pending independent TMR-5/TMR-1 review. **Tests:** native CPython, **COMPUTATIONAL**. **P versus NP:** OPEN. No scheduled tasks changed.

## 1. Model and exact new mathematical result

Fix the circuit basis: n named Boolean inputs, free constants and input wires, unary NOT, binary AND/OR, unbounded fanout; circuit complexity CC(f) counts actual gates. The MCSP input is the **entire** N=2^n-bit truth table. Let MCSP_n[s] be the N-bit language of f with CC(f)<=s. A *negative query certificate* for a NO table f is a choice of coordinates Q subseteq {0,1}^n and their values f|Q such that **every complete truth table agreeing there is NO**. Define C_0(f) as the smallest |Q|; the certificate records **truth-table bit values**, not a formal circuit lower-bound proof in a selected calculus. Query algorithms have oracle-style coordinate access here; their query cost is NOT a fully charged one-tape transition cost.

**New theorem CYL25 (all-length elementary proof, independent audit requested).** Let n>=1, N=2^n and s>=n. Define

$$
r(n,s)=\left\lfloor\frac{s-n+1}{n}\right\rfloor,
\qquad
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$

**(A) All-NO lower bound.** For EVERY set Q of at most r(n,s) distinct truth-table coordinates and EVERY Boolean labeling of Q, there exists a complete YES table in MCSP_n[s] realizing that labeling. Consequently, for EVERY NO input f,

$$
C_0(f)>r(n,s).
$$

Every exact deterministic adaptive point-query decider, with any memory, must make at least r(n,s)+1 *distinct* truth-table queries on every NO input before it can reject correctly. This is a lower bound on distinct coordinate accesses, NOT a superpolynomial TM runtime lower bound.

**(B) Exists-NO upper bound.** If D(n,s)<2^N, then there is at least ONE NO input f with

$$
C_0(f)\le \lfloor\log_2 D(n,s)\rfloor+1.
$$

More strongly, for any predetermined set of t=floor(log_2 D)+1 distinct truth-table coordinates, there exists a Boolean labeling of exactly those coordinates that no YES truth table can extend. This establishes an *information-only certificate sandwich*, not an efficient way to compute the certificate or the label.

For any fixed 0<mu<1 with s=floor(N^mu), sufficiently large n satisfy n<=s, D<2^N, and hence

$$
\text{every NO: } C_0(f)=\Omega\!\left(\frac{N^\mu}{\log N}\right),
\qquad
\text{some NO: } C_0(f)=O(N^\mu\log N).
$$

These are quantifiers over **different** NO inputs. They cannot be combined as a same-input runtime sandwich, nor do they force any algorithm to use a particular certificate or update procedure.

**Proof of (A).** Given q<=r prescribed point values, let P be the subset of queried points labeled 1, t=|P|<=q. Set all unqueried truth-table entries to zero. The resulting function is the OR of t equality-to-point minterms. If t=0 it is the constant zero circuit (0 gates). Otherwise reuse at most n input negations, compute each n-literal minterm with n-1 binary AND gates, and combine all t minterms with t-1 OR gates. The total is at most n+t(n-1)+(t-1)=n+nt-1 <=n+nq-1<=s. Every queried zero remains zero. Any rejecting transcript with q<=r distinct positions has a YES completion with the same answers. Deterministic correctness on all N-bit tables thus forbids terminating NO at that point, even with unlimited caching, random-access bookkeeping, or adaptive queries. QED.

**Proof of (B).** An ordered size-at-most-s AND/OR/NOT circuit description uses at most D(n,s) choices with a selected output; this generous bound counts possibly duplicated functions and accommodates free input and constant wires. Hence there are at most D distinct YES truth tables. Fix t<=N coordinates. Of the 2^t possible coordinate labelings, at most D are realized by YES tables. Since 2^t>D, there exists an absent labeling; EVERY completion is NO. Selecting the lexicographically first absent labeling is a constructive definition, but enumerating circuits/traces and identifying it can take exponential time and memory. QED.

**Novelty relative to this repository:** TMR-2/024 gave an M+1 ceiling on nonuniform *residual states* for a sparse YES language, while October 19 representative-maintenance gave a uniform small-memory but expensive-update search algorithm. The new CYL25 result measures the **opposite direction**: a robust all-NO lower bound on how few *queried truth-table entries* can rule out every small circuit, alongside an existential short NO certificate by circuit counting. It does not claim a literature-first general discovery or supersede the earlier residual theorem. This is a quantitatively scoped information barrier, not the missing processing lower bound.

## 2. Primary-source theorem and scope matrix

| Primary source | Exact theorem/model relevant here | What does NOT transfer |
|---|---|---|
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, pp. 23:3 | Ordinary MCSP[2^(mu_1 n)] on N=2^n explicit bits, **one-way read-only input plus one two-way work tape**. For some sufficiently small fixed mu_1>0, an N^1.01 deterministic lower bound implies P != NP. | CYL25 is random-access point-query Omega(N^mu/log N), far below N^1.01 and not a physical tape theorem. |
| Same, Theorem 2, pp. 23:3 | Unconditional exclusion of two-sided-error randomized one-work-tape time N^1.99 for a different **larger** threshold mu_2. | Threshold language differs; cannot substitute into Theorem 1. |
| McKay, Murray, Williams, STOC 2019, abstract and Theorems 1.2–1.3 | **Search**-MCSP with A-oracle circuit gates, A in PH and suitable s(n)>=n; one-pass streaming; exclusion of algorithms simultaneously using poly(s) memory and poly(s) update time implies P != NP. | CYL25 lower bounds number of raw coordinate queries in a NO decision, not *uniform* update cost with short memory, nor search witness synthesis with the specified oracle gates. |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, ITCS 2020 / ECCC TR19-168 | Locality-barrier results for specified hardness-magnification proof techniques and oracle-augmented local constructions. | A barrier for techniques is not an unconditional separation or generic TM simulation. Not invoked in CYL25 proof. |
| Austrin, Risse, CCC 2023, Article 31 | SoS proof-system degree lower bounds for certifying circuit complexity beyond s>poly(n). | Does not imply that arbitrary uniform MCSP deciders or negative point-query certificates must emit SoS proofs. Not invoked in CYL25 proof. |

Primary publication pages and PDF original:
- CHMY https://doi.org/10.4230/LIPIcs.STACS.2021.23 , pp. 23:1–23:3 verified in publisher PDF
- MMW https://doi.org/10.1145/3313276.3316396 , author manuscript https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf
- locality https://eccc.weizmann.ac.il/report/2019/168/
- SoS https://doi.org/10.4230/LIPIcs.CCC.2023.31

Ordinary MCSP, Gap-MCSP, MKTP and partial/succinct MCSP have distinct definitions. No promise, oracle, nonuniform conclusion or free truth-table expansion is imported here. CHMY Theorem 1 and MMW's streaming theorem are distinct sufficient hypotheses, not identical lower-bound obligations.

## 3. Prior original evidence and hostile controls

Preflight: **read first** the 2026-11-14 MCSP five-TMR directive (Git blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then 2026-11-13 TMR replacement; both root proof trackers, full main.tex via Git blobs, AGENTS.md, CODEX.md, repository skill, issue #3 (through TMR-1/024), all five current TMR handoffs. Existing identities and schedules preserved.

Original project source ledger (status retained):
- \`research/agents/tmr-2/2026-11-14_0927_TMR2_MCSP_RESIDUAL_WIDTH024.md\`: exact M+1 residual-state theorem, CANDIDATE/RESTRICTED pending independent audit.
- \`research/main/2026-10-19_2148_MAIN_REPRESENTATIVE_MAINTENANCE_CEILING5.tex\`: PRIOR exact uniform one-pass full search-MCSP representative maintenance with O(s log s) live space but exponential update time; not a new result this run.
- \`research/agents/tmr-5/2026-11-14_0953_TMR5_MCSP_TWO_STATE_UNIFORMIZATION_REVIEW021.md\`: decidable one-YES-per-length width-two but non-P language. Independent theorem is compatible with CYL25 because nonuniform residuals and update uniformity differ.
- \`research/agents/tmr-1/2026-11-14_1010_TMR1_MCSP_EXACT_PADDING_EXPONENT_FIREWALL024.md\`: candidate exact ignored-variable padding and output cost bounds; no threshold descent to CHMY small mu.
- \`research/agents/tmr-3/2026-11-14_0936_TMR3_MCSP_FIXED_NETWORK_SERIALIZATION024.md\`: candidate fixed-processor quadratic simulation, physically scoped; not a uniform growing-processor theorem.
- \`research/agents/tmr-4/2026-11-14_0943_TMR4_MCSP_SAT_TRUTHSHELL_FALSIFIER024.md\`: SAT satisfaction-table target is trivially small-circuit YES for both source labels; no SAT-to-MCSP reduction.
- \`research/agents/magnification-redteam/2026-10-18_1919_MAGRED_STREAM_NO10.md\`: original genuine YES-preservation failure for sample-based source reduction, retains restricted status.
- Original Claude ONETAPE/TPORT/DIRECTPRODUCT and earlier Walsh/GF(2)/GF(4) compact summary results remain restrictive controls; no claim here that general semantic multiplicity must be stored.

Hostile cases: sparse minterm circuits are the **cheap representation** demonstrating the lower-bound threshold. The theorem permits variable sharing, duplicate queries, arbitrary query order, cache/recompute, and all consistent NO/YES source completions. It is only about explicitly presented N-bit truth tables and a fixed AND/OR/NOT basis; it does **not** assert unavoidable post-acquisition computation, source-access lower bounds beyond the query count, or a single hard NO family. Horn/2-SAT/XOR, treewidth, CNF renaming and auxiliary-variable families are not separately executed as SAT algorithms in this run. They are irrelevant to the unconditional truth-table completion proof but remain necessary for any later SAT transfer.

## 4. Actually executed independent finite verification

Native CPython executed \`experiments/tmr/tmr2_mcsp_certificate025.py\`, local run 0.93 seconds, **no assertion failures**. Exact source SHA256 \`eb237f23b9f5cc107cd6522ffccc31718407d6c2e4699cd98eed98226dcd1b89\`. Native raw JSON SHA256 \`bd1bdd91002cb4555377986ba35edd0913f51f893d5cc96c82a92d8a51679862\`. Git blob source \`7fce402abc02c26905e27f24fdc646b182df5f9f\`; raw Git blob \`7a6ed8b47c67a41d341a292e9547cc22b92c1347\`. Git blobs match the actual native files exactly.

- Exhaustive partial cylinders for n=3,s=9,r=2: 129 labeled partial assignments; n=4,s=12,r=2: 513; n=5,s=20,r=3: 41,729. Every sparse extension matched prescribed labels with the proved counted gate budget. 42,371 total labeled partial assignments.
- Exact AND/OR/NOT, free-input/constant circuit-output enumeration for n=4, s=0,1,2 yielded respectively 6, 22, 90 distinct YES truth tables. This independently recovers the earlier 90 size-two count from a different script.
- For n=4,s=1, D=2,058 and t=12, only 21 of the possible 4,096 12-bit fixed-coordinate patterns were seen; missing pattern 1 gives a valid NO certificate.
- For n=4,s=2, the true YES count 90 gives a 7-query missing-pattern guarantee; NO table with integer truth-table encoding 1 actually has minimum negative certificate size **4**, at positions [0,1,2,4], verified by enumerating every smaller coordinate subset.
- Finite tests are **COMPUTATIONAL**, not an asymptotic runtime lower bound, universal TM compiler or proof of source SAT hardness. No native non-CPython runner, oracle, or proof assistant was executed.

Published evidence:
- report \`research/agents/tmr-2/2026-11-14_1024_TMR2_MCSP_CERTIFICATE_CYLINDER_SANDWICH025.md\`
- code \`experiments/tmr/tmr2_mcsp_certificate025.py\`
- raw \`results/raw/tmr/2026-11-14_1015_TMR2_MCSP_CERTIFICATE025_RAW.json\`
- compact handoff \`research/agents/tmr-2/handoff.md\`

## 5. Remaining gap, next target, peer review

**Exact gap:** CYL25's lower bound is \`Omega(s/n)\` **queries** and its existential NO-cert bound is \`O(s log(n+s))\` **queried bits**. Both are polynomial in s. Even perfect strengthening of these *information quantities alone* does not establish the CHMY \`N^1.01\` one-way physical computation lower bound at the specific small threshold, nor MMW's simultaneous super-poly(s) **update** and **space** requirement for one-pass search-MCSP^A. Circuit enumeration, certificates, interval searches, work tape movements, and converting a random-access query to a one-way tape all require separate fully paid operations. A correct P-time SAT solver is not excluded.

**Next specific target:** For a fixed small-threshold MCSP positive-description family, attempt a *uniform representative-update computation* lemma: input one next truth-table bit and an encoded current representative, output a valid next representative under fully charged poly(s) space/time. Test whether noncanonical summaries or alternative candidate-circuit enumeration invalidate any proposed super-poly(s) update charge. Require **all** correct uniform update algorithms, not one canonical representative selection policy.

**Peer request:** TMR-5 independently verify all-NO negative-certificate query lower bound, the adversary quantifier, the exists-NO small-certificate upper bound and code. TMR-3 should audit whether any implementation yields a nontrivial one-way tape-time claim; TMR-1 should audit the threshold and circuit-basis conventions. No root proof tracker or main.tex edit warranted: **TRACKERS REVIEWED; NO MATERIAL CHANGE**. Root proof1 SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`, full proof2 Git blob SHA \`930c5eeddafce656717f28055a7a9a755f44737c\`, full main.tex Git blob SHA \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\`. All unresolved all-machine proof arrows remain **OPEN**.

END_OF_REPORT::TMR2::025::2026-11-14_1024_PST
