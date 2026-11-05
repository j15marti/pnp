# LSPV-4/401: Flat LOCAL-CONVERT clause checker, exact support erasure and paid I/O

**November 4, 2026, 19:36 PST. PNP Time-Space Resource Auditor. IDEA -> SEARCH -> ITERATE.**

**Status:** PROVED/EXACT elementary lemma for a **flat, explicit clause-output fragment** of the unchanged R_mix341. COMPUTATIONAL finite controls. OPEN: full native circuit/exported-wire/paid-definition grammar, consumer-aware general proof translation, noncircular B3, superpolynomial full-mixed lower bound, and P versus NP. This work introduces no new rule or weight.

## IDEA (before search), assumptions, falsifiable prediction

Fix a prior, source-authenticated factor f depending only on original variables S with |S| at most 3 and a supplied explicit signed conclusion clause C of any width. Hypothesis: checking whether f entails C can be reduced to a constant-size truth-table problem without enumerating variables outside S; importantly, preserving C itself rather than emitting a stronger projected clause retains the exact RES pivot interface.

Falsifiers: (F1) an outside-S literal invalidates projection; (F2) complementary signed literals break projection; (F3) an inconsistent factor or empty conclusion gives a counterexample; (F4) replacing C by the projected subclause is always consumer-safe.

Predicted resource claim is a deterministic indexed-read-only-input checker using O(poly(M)) bit time and O(log M) writable space for this **single supplied check**, where M includes the full supplied factor record plus the entire conclusion. This does not claim an all-phase bound for general SAT solving.

## SEARCH (actual inspected sources, paths and queries)

First read the shared five-role handoff at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (Git blob c3889a3e) and current issue #3 through LSPV-1/406 and LSPV-2/406. Read the unchanged native original at research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11), plus research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md (bbcdad9a), research/agents/lspv-3/2026-11-04_1724_LSPV-3_PORT_COHERENCE_GRAMMAR406.md (4d2abf92), research/agents/lspv-4/2026-11-04_1836_LSPV-4_LOCAL_CONSUMER_REWRITE400.md (e01464b9), and research/agents/lspv-1/2026-11-04_1905_LSPV-1_FEASIBLE_ANTICHECKER_B3_406.md (2ab6034c). Also read AGENTS.md and recent issue comments including REFEREE351 and LSPV-3/407.

Actual external review: GROKPROOF/2026-11-05_0214_PROGRESS.md (af7530c7), and Claude's research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex plus research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Neither supplies B3. Grok's proposed white-box extraction still lacks the uniform resource contraction; Claude's time/space barriers do not yield native logical-proof simulation.

General web queries actually issued: "Cook Reckhow 1979 propositional proof systems polynomially bounded if NP coNP theorem"; "Krajicek Pudlak proof systems P=NP implies polynomially bounded resolution extended Frege no known relationship"; "Haken 1985 exponential resolution pigeonhole principle dag proof lower bound Cook extended resolution"; "local conversion proof system polynomial simulation extension variables gate definitions proof checking equivalence". Read Grochow (2023), arXiv 2306.02184, especially introduction and model of verifying circuit proofs; Braun (2026), arXiv 2609.23015, exact DAG-like Res(oplus) theorem and quantifiers. Searched authenticated github.com/openai for "ExecCNF"; read openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean blob e60f4d9. It cautions that literal-comparison costs are not necessarily unit bit costs. It is NOT a compiler for native R_mix341. Direct Google-branded UI unavailable; general web search was used, not direct Google.

Duplication: LSPV-4/363 and LSPV-1/384 already establish bounded-support circuit table checking. This specialization makes outside-support signed literal handling and exact consumer-visible clause identity explicit, with separate bit-I/O complexity. No academic originality is claimed.

## ITERATE: exact support projection

Let f be a Boolean factor on support S of at most 3 original variables, and C any finite signed disjunctive clause, including repetitions. Define C_S as the restriction of C to literals whose variable belongs to S.

**Lemma 401A (EXACT).** If C has a complementary literal pair then f entails C. Otherwise:

$$
f \models C \quad\Longleftrightarrow\quad f\models C_S.
$$

**Proof.** If f entails C_S, it entails C because C_S is a disjunctive subclause of C. Conversely, suppose f does not entail C_S. There is a valuation of S satisfying f and falsifying every literal of C_S. Since C has no opposing literal pair, every outside-S variable appearing in C may be assigned to make its literals simultaneously false. Extend arbitrarily to other variables. The resulting global valuation satisfies f but falsifies C. Contradiction. If f is inconsistent the implication holds vacuously on both sides, including C empty. If C is tautological its implication holds independently. QED.

**Algorithm 401B (EXACT / restricted native flat-output fragment):** parse and authenticate input factor table and signed variable IDs; test C for a complementary pair by nested scans; if none, retain only the at most six possible signed literals on S; check at most 8 truth-table rows. Accept and output **the original C verbatim**, not its support projection. This is necessary for the existing legal RES consumer on pivot y of (x OR y) and (NOT y). Replacing (x OR y) with (x) makes that consumer illegal even though the new clause is stronger.

**Full resource distinction.** Let M be the bit length of the immutable supplied factor + entire clause record + source references and type flags. Under a declared indexed read-only-input and append-only-output machine, storing at most three source variable IDs, eight truth bits, loop counters, and one signed literal uses O(log M) writable space. Nested scans for opposite literal pairs and source-literal comparisons give conservative O(M^3) bit-time including addressing, comparisons, input/head/index actions and verification. Exact output of C requires Omega(|C|) paid output bits; emitting it by rescanning avoids an O(|C|)-bit writable buffer. Any general derivation normalization has additional costs for gate/port construction, output DAG scheduling, ancestry, caches, failed policies, proof validation and all-phase peak rho. Here no claim is made that M is polynomially bounded in original source N or in paid node count q; no FLMV contraction is inferred.

**Grammar firewall.** /341 says LOCAL-CONVERT has one factor/equation premise and a constant-support implication truth-table check, with a clause or bounded-support circuit-condition output. The broad clause-output semantics above is mathematically sound. /341 does not fully serialize implicit circuit payloads, private/public exported wire IDs, assertion/definition ports, or payment for internally represented gates. No theorem about those unclear cases follows from 401A. This is not an authorization to modify the fixed rules.

## Independent verification and controls

Python producer at the locally retained reproducibility package used direct enumeration of all 32 full assignments over five variables. Independently authored JS referee at experiments/arc/lspv4_401_flat_local_clause_verifier.js uses independently structured all-assignment truth-mask checking. Both exhaustively checked all 278 Boolean factors of support k=0,1,2,3 against 243 non-tautological clause patterns over five variables: **67,554 pairs, 18,972 entailments and 48,582 counterexamples**. Additionally, 1,390 tautological clauses passed. SAT original (x) AND (x OR z) AND (NOT y) had 2 models; UNSAT (x) AND (NOT x) had 0; a four-row AND3 authentication passed; 3 malformed literal arrays and an illegal consumer pivot were rejected. This is a finite verification of an elementary general lemma, not proof of native circuit-port completeness or arbitrary machine resource lower bounds.

Raw independent JS summary: results/raw/arc/2026-11-04_1936_LSPV4_401_FLAT_LOCAL_CLAUSE.json. All literal signs remain occurrence-accurate. The programs are not claimed to simulate physical FLMV tapes; the O(log M) guarantee is for the mathematical checker described above.

## Established hardness and weakest B3 bridge

Haken (1985): for every sufficiently large h, every ordinary shared-DAG Resolution refutation of explicitly encoded unary PHP with h+1 pigeons and h holes has exp(Omega(h)) inference clauses. Its conventional signed-index CNF source is N_h=Theta(h^3 log h). This is a restricted proof-system lower bound, not arbitrary-machine time/space hardness. Cook's polynomial Extended Resolution proofs eliminate that particular lower bound in a stronger system. Braun (2026), arXiv:2609.23015, proves more than exp(n/(32768 ell^2)) clauses in DAG-like Res(oplus) for bit-PHP with n=2^ell and ell at least 32; it does not cover R_mix341. Tseitin odd-charge expander clauses have short native GF(2) proofs, as /341 explicitly checks.

**B3 OPEN:** SAT in P implies that there exists some polynomially bounded Cook-Reckhow proof system, but not necessarily the fixed R_mix341. Rejection of F by an arbitrary decider is not automatically a source-authenticated R proof of F's unsatisfiability. The local checker neither assumes nor proves such a reflection/normalization simulation. Needed: fully specified native exported-wire/LOCAL/DEF syntax, polynomial global source-retracting certificate translation with exact public interfaces and all physical charges, and a noncircular same-fixed-R implication under SAT in P.

**B1, B2, B3, superpolynomial Wbar_Rmix341, P versus NP remain OPEN.**

## Numbered references

[1] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic. 1979;44:36–50.
[2] Haken A. The Intractability of Resolution. Theoretical Computer Science. 1985;39:297–308.
[3] Cook SA. A Short Proof of the Pigeon Hole Principle Using Extended Resolution. SIGACT News. 1976;8(4):28–32.
[4] Grochow JA. Polynomial Identity Testing and the Ideal Proof System. arXiv:2306.02184. https://arxiv.org/abs/2306.02184
[5] Braun K. An Exponential Lower Bound for the Bit Pigeonhole Principle in Resolution over Parities. arXiv:2609.23015. https://arxiv.org/abs/2609.23015
