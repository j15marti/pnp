# LSPV-2/576: exact tree-like Resolution minimum for signed guarded K4

**2026-11-12 07:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/EXACT finite restricted theorem + COMPUTATIONAL unchanged original checker | P versus NP OPEN**

## Candidate, four falsifiers and provenance

**Candidate:** Strengthen LSPV-2/575's min-28 result over 5,040 deterministic Davis–Putnam elimination orders to an exact lower bound over **ALL tree-like strict non-tautological binary Resolution refutations** of its independently authenticated signed 17-clause guarded K4 source. This removes the elimination-order restriction, **not** the tree-like restriction.

F1: a non-DP tree-like refutation with <=27 paid inferences exists. F2: an exact signed non-tautological Resolution rule violates our proposed finite potential. F3: the source-bound 28-RES upper witness is rejected by the unchanged archived checker. F4: source forgery, underpayment, forward parents, or an unknown mixed tag are accepted. All were tested within the stated restricted semantics and none occurred.

Original unchanged /386 checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986. Independent 17-clause original: results/raw/arc/574_k01_SIGNED_SOURCE.cnf, SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c. Original source-bound seed: results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, Git blob 318c52d99977ea4e91bc8554051138a700c1dc94. Every ordered signed SOURCE clause in the generated proof was checked against the external source bytes. The /386 checker handles SOURCE, paid AND2 gate owners, zero-additional-cost DEF facets and strict Resolution; it is **not** the full historical R_mix341 checker.

## Exact 2,187-clause potential-certificate theorem

Let U be all non-tautological signed clauses over variables 1,...,7. Every variable can be absent, positive or negative, so |U|=3^7=2,187. Source leaves are free. Each exact signed non-tautological binary Resolution inference is unit paid. A *tree cost* counts every derived inference occurrence, including recomputation, not merely distinct shared DAG nodes.

For each C in U let d(C) be its minimum binary-Resolution derivation-tree cost (or infinity if no derivation). Original source clauses have d=0; non-source clauses minimize d(A)+d(B)+1 over legal opposite-sign pivot parents A,B. Set h(C)=min(28,d(C)), treating infinity as 28. We construct and independently check the complete vector with

    h(each original source)=0,
    h(empty)=28,
    h(Res(A,B,p)) <= h(A)+h(B)+1.

The last inequality was checked on exactly **711,298** legal oriented non-tautological parent/pivot transitions whose parents both have h<28. Every parent with h=28 makes the inequality trivial because every h<=28. This is an exhaustive finite condition over ALL possible legal strict Resolution transitions in the seven-variable language, not just a chosen proof search schedule.

**Theorem 576.1 (PROVED/EXACT, finite tree-like Resolution):**

    W_tree_RES(F_guarded_K4)=28.

**Proof.** For any derivation tree, induct bottom-up: source leaves have h=0 and no charge, and each legal inference satisfies h(conclusion)<=h(parent_1)+h(parent_2)+1. Consequently the potential of a root clause is bounded by the total number of paid inference occurrences in its tree. The empty clause has h=28, so every refutation tree costs at least 28. Conversely, the explicit accepted signed-source certificate has 28 Resolution records arranged without sharing any derived intermediate (each of its 27 nonterminal derived nodes has fan-out 1). It has 29 source leaf uses, reusing the 17 free original SOURCE identities. Hence a 28-inference tree exists, and the bound is sharp. QED.

**Falsification guard:** The separately authored Python verifier deliberately increases h(empty) to 29 and finds violating Resolution transitions, confirming the inequality tests do not automatically pass a false stronger bound.

## Actual source-authenticated original-checker computation

The independent Python reference enumerator and JavaScript implementation produced identical certificate SHA-256 c753ef947e94d09dd278cfa958eb0eb7badbe3878ac9103be7f8549d8d289bac (2,883 UTF-8 bytes with final LF) and potential-vector SHA-256 82a2ad521043ff5e1e71e08904d57e88cf50f8e97abf1e3585e115243c0ff5dc (5,258 bytes). The enumerator considered 2,138,326 pivot-oriented candidate resolvents, including 1,427,040 tautological outcomes, and found 1,331 clauses reachable within 28 tree inferences. The full cost histogram is in the raw file.

The **unchanged archived /386 original checker** was executed via actual operating-system Node.js subprocesses. One 45-record certificate (17 SOURCE, 28 RES, 1 separately paid unused AND2 owner) was **ACCEPTED**, completing 3,542 original-checker assertion groups including its 11 built-in hostile checks. Four reference-replayer corruptions were **REJECTED** (underpay, forged source, forward parent, unknown AND3); a separately written Node.js replayer additionally rejected a wrong-pivot control. These are actual original-checker executions, not a new reference grammar substituted for native acceptance.

The original full CLI witness work **W=29** consists of R=28 plus one unused paid gate owner needed for that wrapper's built-in mutation test. This is NOT proof that the complete native minimum equals 29. The exact lower bound 28 is restricted to *tree-like Resolution work alone*. Certificate bytes, source bytes, logical work, proof construction time, native verification time, span and peak physical space are separate; no native FLMV theorem is claimed.

## Prior art and literature

The tree derivation cost recurrence is a finite exact specialization of known Resolution proof-search methods, not a new general proof complexity algorithm. Sources checked: Davis–Putnam, A Computing Procedure for Quantification Theory, JACM 7 (1960), DOI 10.1145/321033.321034; Peitl–Szeider, Finding the Hardest Formulas for Resolution, JAIR 72 (2021), DOI 10.1613/jair.1.12589; Cousot–Cousot, Abstract Interpretation (POPL 1977), DOI 10.1145/512950.512973. Prior project /575 supplied the same 28-step upper witness class, /341 documents historical declared semantics, /553 and /412 prove incomplete historical checker coverage and parent grammar ambiguity, /539–549 and /570–574 record essential parser/provenance/CEGAR controls. Checked the required external repositories konard/p-vs-np, blkph0x/p-vs-np-proof-research, meelgroup/frat-xor, and peitl/short-proof; their formats/results are distinct and cannot authenticate R_mix341.

## Published and reproducible evidence

- Executable NON-AUTHORITATIVE reference enumerator and original OS checker replayer: experiments/arc/lspv2_576_tree_min.py. Run from repository root: python3 experiments/arc/lspv2_576_tree_min.py . /tmp/lspv2_576_output
- Compact raw: results/raw/arc/2026-11-12_0712_LSPV2_576_TREE_MIN_COMPACT.json.
- Complete accepted-byte W29 packet, 2,187-element potential, separate independent verifier, JS reproducer and OS outcomes are in the accompanying evidence archive.

## Material status and coordination

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Read BOTH full root proof chains, issue #3 and latest comments, AGENTS.md, CODEX.md, pnp-research skill, /341, historical /539–549 and later reports, current role handoffs and exact peer evidence. The new restricted finite-minimum certificate does not close [P2-D1], full [P2-C3], [P2-B1] or separate [P2-B2]/B3. All unauthenticated native mixed transitions remain MAY in a sound full-system abstraction. No modification to main.tex: other ownership regions and the full system status are unchanged.

Exactly five existing PNP research automations were checked **enabled** with Pacific timezones, original identities, schedules, fixed historical weights and TWO Route A / THREE Route B labels. No automation was created or changed.

The next decisive missing original evidence is a single source-bound historical checker accepting a genuine RES-to-AND3 or paid DEF-to-LOCAL-CONVERT dependency, with corrupt-port controls. **P versus NP remains OPEN.**
