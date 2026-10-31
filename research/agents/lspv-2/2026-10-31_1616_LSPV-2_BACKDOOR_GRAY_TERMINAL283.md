# LSPV-2 BACKDOOR-GRAY-TERMINAL283
2026-10-31 16:16 America/Los_Angeles (PDT). Role: LSPV-2 Circuit and Reduction Builder.

**Status: PROVED/EXACT elementary syntax identities pending independent mathematical review; COMPUTATIONAL same-source controls. All-target hereditary arbitrary-A ARC and quantitative FLMV transfer OPEN. P=NP and P!=NP OPEN.**

## One obstruction and four falsifiers

Target **every valid** duplicate-free proper clausewise-monotone 3-SAT-(2,2) input in Döcker's established NP-complete language, rejecting malformed binary strings. Every variable has two positive and two negative occurrences, every clause is a distinct pure-signed triple. The structural obstruction is that small *raw* original-variable restrictions cannot enter syntactic Horn, dual-Horn or 2-SAT, but this does not imply slow adaptive solving.

F1: Can restricting fewer than n/3 source variables leave raw Krom/Horn/dual-Horn? **FALSIFIED** by signed untouched-clause counting. F2: Does the previously known n/3 generic Horn lower bound specialize sharply to monotone exact22? **STRENGTHENED** to 2n/3 for static strong Horn and dual-Horn backdoors, using double incidence, classical backdoor criteria. F3: Does Gray-coded true-count XOR distinguish the matched U198 UNSAT and V198 SAT? **FALSIFIED**. F4: Does certified SAT component peeling yield an FLMV-power-short child? **FALSIFIED on the tested pairs**, with no general conclusion against other compilers.

## Exact target-wide syntactic theorem

For any valid source F with n variables, m=4n/3 original triples, and 2n/3 clauses of EACH sign, choose any set T of k original variable identifiers and any coherent restriction b on T. Without propagation or re-encoding, at least max(0,2n/3-2k) **unchanged** original positive triples and the same number of negative triples survive: a selected variable touches only two clauses of each polarity. For k<n/3, there remains both a positive and a negative triple in every cofactor, excluding syntactic Horn, dual-Horn and Krom. A strong Krom backdoor needs at least n/3 selected variables, while a strong Horn backdoor needs at least two hits per positive triple, i.e. k>=2n/3; dual-Horn is symmetric. This is a classical-style source-incidence argument, independently of SAT label. It does not apply to unit propagation, dynamic backdoor depth, affine re-encoding, source-aware recognition, arbitrary A, or semantic solution difficulty. LSPV-3 STRICT22-BACKDOOR-SELECTOR-GATE271 already proved the general clausewise criterion and n/3 generic bound; **no novelty claim** is made for those.

## Exact XOR-encoding lemma and proof provenance

For each coherent assignment a define t_j(a) in {0,1,2,3}; let g(t)=t XOR (t>>1), and G(a)=concatenation of the 2-bit Gray fields g(t_j). In strict22 every original variable occurs in four **distinct** source triples. Flipping it changes all four counts by 1, and thus d_H(G(a),G(a XOR e_i))=4 exactly. Complementing every variable maps t to 3-t and gives d_H(G(a),G(~a))=m. Ordinary binary 2-bit counts give complement distance 2m. These are only **count fields**, not the richer logical record (assignment, SAT flag) used in LSPV-5 XOR-ACTIVITY-IDENTITY-REFEREE251, and not physical writable tape events. Opposite-sign original clauses can yield width-four non-tautological resolvents, whose falsifying partial cubes are excluded with indexed parent clauses; this is established ordinary resolution.

## Same-source both-label and physical tests

Source Y6: n=6,m=8, SAT (20 models). U198: n=198,m=264, UNSAT by independently replayed original-source 64-interface-row refutation. V198: target-valid two-occurrence legal switch from U198, SAT by complete original-source witness. Capped UP-DPLL found Y6 SAT in 4 nodes/111 literal tests; U/V both unresolved at 3,000 nodes and 3,016,607 literal tests each, NOT UNSAT classifications.

Independent verifier: **PASS**, 109 sampled original-source backdoor masks, 69,460 SS/SU/US/UU pair modes, 536 signed original clause extremes with inversions, 448 local resolvent truth-table checks, 1,182 logical checkpoints, 108,324 event-sourced physical child-emitter events, 6,981 actual materialized data-bit writes, one deliberate corrupted index event rejected and previous complete U198 NO refutation replay PASS.

Count-only Gray full-inversion path cumulative/endpoint XOR: Y6=24/8; U198=792/264; V198=792/264. Binary count-only: Y6=32/16; U/V=1,056/528. For 64 chosen-variable settings, Gray-order cumulative count XOR=252 for all three; binary-order=296 on Y6, 412 on U/V.

A certified **restricted** target-to-target component emitter takes U198+Y6->U198 (UNSAT) and V198+Y6->V198 (SAT), with child grammar and witness/proof lift checked. Each 6,832-bit parent produces a 6,632-bit physically emitted child, **not** M<=sqrt(N) (sqrt(6832)<83). Both paid emitters recorded 6,600 source-bit indexed reads, 40,930 index 0->1 writes, 84,906 cumulative physical XOR (including index resets), 3,046 physical endpoint XOR, 203,399 selected construction-operation proxies *excluding* separately acknowledged 816 literal discovery probes, and minimum 6,645 simultaneously allocated child+index bits. Host formula arrays, maps, proof, event logs and interpreter memory exceed these lower diagnostic allocations; these Python figures do NOT prove native FLMV TM upper bounds. All index resets are declared atomically and cannot be naively charged as one-bit native writes. Logical count changes do not entail materialized physical changes.

## Search, duplications and limitations

Primary work reviewed: Döcker arXiv:1912.08032; Darmann-Döcker arXiv:1908.04198; Dreier-Ordyniak-Szeider JCSS 2024; FLMV JACM 52(6) 2005. Project exact files: REDIRECT1, CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted affine MCSP only), CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1 (easy large-backdoor SAT orbit), AGENTS, CODEX, pnp-research skill, previous LSPV-2 276/278/279/281/282, LSPV-3 271, LSPV-5 XOR referee and issue #3. Search of github.com/openai/math found Lean SubexponentialSAT infrastructure explicitly not asserting the solver exists. No novel unconditional lower bound inferred from research search.

**OPEN**: uniform every-valid-target, connected-instance, hereditary, both-label, physically power-short ordinary SAT child compiler with exact indexed child-bit access, fully charged policy discovery, failed attempts, source/index/guest/ancestor/cache work and same-machine peak workspace; separately a quantitatively valid SAT-to-Döcker-target FLMV lower-bound transport. The proposed K'<=max(11/10,3/5+K/2), L'<=max(1/2,L/2) is CONDITIONAL.

Report TeX/PDF, full Python producer and **independent** verifier, raw U/V original sources, complete U198 refutation, witnesses, compressed source S/U/compatibility data, complete XOR/physical event streams, independent results, provenance ledger and manifest are in downloadable archive `LSPV2_BACKDOOR_GRAY_TERMINAL283_2026-10-31.zip`. Repository publication contains this substantive text, an independent small JS spot check, and a compact machine summary. GitHub CI and full repo preflight were unavailable without local clone; GitHub authenticated API was used for exact readback. Historical agents/schedules not modified.

END_OF_VERIFIED_REPORT::LSPV-2::BACKDOOR_GRAY_TERMINAL283::P_VS_NP_OPEN
