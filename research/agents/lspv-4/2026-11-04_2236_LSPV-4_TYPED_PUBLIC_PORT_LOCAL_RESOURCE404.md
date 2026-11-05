# LSPV-4/404: Typed public-port LOCAL implication and fully charged verification

**November 4, 2026, 22:36 PST. IDEA -> SEARCH -> ITERATE completed.**
**PROVED/EXACT (declared source-authenticated paid-DEF public-port fragment), COMPUTATIONAL finite tests, ORIGINAL NATIVE GRAMMAR and B3 OPEN.** No change to the fixed R_mix341/341 rules, weights, role, schedule, or other authors' manuscript regions.

## IDEA, assumptions, falsifiers

**Hypothesis before search:** For a source-authenticated AND3 factor A over at most three ORIGINAL variables S, followed by any number t of distinct, already paid, acyclic, deterministic two-input DEF gates reading only S and prior named gates, the LOCAL consequence check for an arbitrary signed clause C of named public gate outputs and external original variables needs only eight rows plus paid scanning of the full explicit gate bank and clause. It must retain C unchanged for downstream pivots.

**Falsifiers:** (F1) an internal DEF gate secretly depending on external original variable w; (F2) duplicate/forward/invalid public gate names; (F3) contradictory external sign pair; (F4) SAT, UNSAT and malformed source; (F5) private wire consumers with unclear public export permission; (F6) huge uncharged implicit payload.

## SEARCH: actual literature and project sources

Read the governing shared handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md first, issue #3 (current peer comments through LSPV-2/409, LSPV-3/411, LSPV-1/410, LSPV-4/403, REFEREE354), AGENTS.md, CODEX.md, the repository pnp-research skill, original R_mix341 definition research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11), LOCAL addendum research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md (blob bbcdad9a), LSPV-3/406, LSPV-4/363, /401, /403, LSPV-2/409, LSPV-3/411. Original source grammar does NOT decide how a paid DEF output can be exported as a typed LOCAL clause literal or GF(2) row, nor how private facet selectors are serialized. This theorem is conditional on that exported-port permission.

**Actual independent assessments reviewed:** GROKPROOF/2026-11-05_0515_PROGRESS.md (blob f348f7bb); research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727) and 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Neither closes the grammar or B3.

**Literature queries in general web search:** "Cook Reckhow relative efficiency propositional proof systems 1979 original pdf"; "Raz Tzameret resolution over linear equations 2008 proof system GF2"; "Gocht Nordstrom certifying parity reasoning efficiently pseudo Boolean proofs 2021"; "P equals NP does extended resolution have polynomially bounded proofs open"; "Haken intractability of resolution 1985 pigeonhole principle polynomial extended resolution Cook 1976". Opened Cambridge journal publisher account of Cook-Reckhow (1979) and the Weizmann institutional article/abstract of Raz-Tzameret (2008). Full AAAI 2021 publisher page was blocked by an anti-bot check, though the indexed bibliographic record was available. Direct Google-branded search unavailable; used general indexed web instead.

**Authenticated OpenAI GitHub searches:** ExecCNFNodeSearchCosts, CookLevin, LRAT at github.com/openai. Fetched and read ALL of openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f4). The formalized bound charges an actual node setup and visit trace on the same execution, but is not a compiler to native R_mix341. The LRAT matches were unrelated substring hits.

**Prior art:** LSPV-4/401 proves the one-factor, wide original-clause case. LSPV-3/406 proves conservative uniqueness of fresh DEF and warns about alias collisions. LSPV-3/411 proves 4 paid gates suffice for any three-original-input public output under its standalone typed fragment. LSPV-2/409 proves conditional old DEF facet recovery for strictly Resolution consumers, assuming addressable facets. LSPV-4/363 already treats P-complete verification of arbitrary uncharged nested LOCAL circuit payloads under hypothetical interpretation U. This run only establishes the missing **multi-public-output clause implication with external free original literals**, and does not claim academic originality or full native normalization.

## ITERATE: precise theorem with proof

Let S be a set of s<=3 original variables. From two source conditions supported on S, exact native AND3 produces already-authenticated factor A(S). A finite acyclic bank D of t *separately paid* conservative DEF nodes introduces fresh named gate outputs z_1,...,z_t; each gate computes a total Boolean function of two inputs in S or earlier z. Under every assignment a to S there is exactly one extension d(a) to these outputs. Let C be a finite signed clause over variables in S, the named outputs z, and arbitrary distinct additional original variables W disjoint from S which do NOT occur in any gate input. C's typed public-port eligibility is an explicit assumption, not a ratified original R_mix341 byte rule.

Define C_in by deleting literals on W. A complementary pair of literals makes C tautological.

**Theorem 404.1 (multiport exact local test):** If C contains a complementary pair, A∧D entails C. Otherwise,

$$
\boxed{ A\wedge D\models C\ \Longleftrightarrow\
\forall a\in\{0,1\}^S,\quad A(a)=1\ \Longrightarrow\ C_{\rm in}(a,d(a))=1. }
$$

**Proof:** Forward: each model of A∧D has gate outputs d(a), so passing the projected test implies a literal of C_in and hence C. Reverse: if an a satisfies A while C_in is false, assign each external original variable in W to falsify its occurrences in C. This simultaneous assignment exists because there is no opposite-signed pair. Extend D uniquely by gate order. Then A∧D is true and C false. If A is inconsistent, implication is vacuous. QED.

**Sound portable example:** Original SAT sources (x1) and (x1∨x2); one paid AND3 produces factor x1. Separately paid DEF z=x1 XOR x2. Under the declared public-port completion, LOCAL clause (z∨x2) is valid, since when x1=1 we have z=¬x2. Change the paid gate to z=x1 AND x2 and that same clause is invalid at x1=1,x2=0. The complete consumer-visible C must be retained to preserve downstream Resolution pivots. Nothing here declares a fully legal original native 3-node proof: whether LOCAL can name z is still unresolved.

**Falsifier found:** The first generator accidentally allowed an inside gate to read external original x4. The independent 4-input evaluator and 3-input projection disagreed. A concrete failing fixture was A=(x2∨x3)∧(¬x3), g5=IMP(x3,x2), g6=XNOR(¬x4,¬x3), C=¬g6∨¬x2∨¬x4. This refutes a *broader* unqualified projection lemma. The actual refined theorem forbids outside gate inputs; the corrected grammar checker rejects that fixture and the rerun passed. This is not a counterexample to legal native R_mix341.

## Verification: two independent semantic implementations

The exact executable experiments are at:
- experiments/arc/lspv4_404_exported_public_clause_checker.js
- experiments/arc/lspv4_404_independent_truthvectors.js

Seed 4042026. The first generated **770** paid-gate network/source pairs with 1..7 gates and two source clauses: **690 SAT and 80 UNSAT**. For **26,950** candidate signed output clauses, a complete four-original-variable enumerator and an independently calculated 8-row gate-truth-vector checker agreed: **14,829 valid and 12,121 invalid**. The instrumented reference made 1,277,159 individual brute gate evaluations versus 862,400 projected row-gate evaluations. Eight malformed record variants were rejected. Positive XOR export, negative AND mutation, inconsistent AND3 parent and an outside-variable tautology all passed.

The independently written second test enumerated **all 256 possible 3-input parent factors times all 256 possible 3-input public-output functions**, and 16 signed clauses for each pair: **1,048,576 exact checks**, with **335,302 entailed** and **713,274 not entailed**. This includes functions not expressible by one DEF gate, but every Boolean three-input function is known to admit a paid 4-gate representation in the LSPV-3/411 standalone fragment. These finite results are COMPUTATIONAL; the general claim is proved symbolically above. Both code files and raw results were committed and individually read back.

## Paid physical time and all-phase space

For supplied explicit N source bits, E gate-bank/certificate bits and L output-clause bits: parse and check source and support references; validate fresh DEF order and all gate types; inspect all source and gate input fields; evaluate up to 8 rows per gate; check outside complement and output literals; authenticate all retained original-source IDs and consumer-visible conclusions; and serialize the whole L-bit clause. A conventional buffered implementation takes polynomial O(poly(N+E+L)) time and O(N+E+L) writable memory. A conservative bit-Turing-machine implementation using explicit rescans and buffering gives O((N+E+L+2)^3) bit-time, O((N+E+L+2)^2) all-phase peak writable bits. A full transcript authentication necessarily reads its explicit evidence; emitting C costs Ω(L) output bits, but **no universal SAT decider is required to inspect a supplied certificate**. With q=t+2 paid nodes and canonical name encodings, the flat explicit DEF fragment has E=poly(N+q). With opaque/unpaid nested LOCAL payloads this fails, as previously shown under interpretation U. The host tool's evaluations are not physical FLMV-machine measurements. The all-phase rho bound must include parsing, buffered materialization, index and guest state, verification and output. No FLMV exponent improvement is claimed.

**Hard-family and B3 firewall:** Haken (1985) lower-bounds **every ordinary shared-DAG Resolution refutation** of explicit signed unary PHP_(h+1)^h by 2^{Ω(h)} lines; h(h+1) Boolean source variables and encoded N=Θ(h^3 log h), no DEF, GF(2), AND3 or LOCAL. Cook's 1976 polynomial Extended Resolution proofs and the /341 exact 4h−1 mixed odd-cubic-Tseitin refutation are mandatory compact-alternative controls. Raz-Tzameret's Res(lin) has a different line grammar. Restricted hardness cannot be promoted to R_mix341 or arbitrary SAT time. No raw reject trace is an R_mix341 refutation absent proved correctness/reflection. The required noncircular weakest bridge

$$
\mathrm{SAT}\in P\Longrightarrow\exists C,k\ \forall N:\quad \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k
$$

is **OPEN**, as are B1, B2, superpolynomial full mixed Wbar and P vs NP.

## Outstanding native question and safe publication

**Next exact obligation:** decide, without changing R, whether a LOCAL conclusion may carry a typed reference to an already paid DEF output as an assertion-usable literal and whether paid DEF equations are exported as addressable GF(2) rows. Then combine this multiport source test with /409's old-facet replay and /411's four-gate public-function synthesis, checking all old consumers. If native selection is forbidden, reject this semantic fragment as a native compiler, not the fixed calculus.

Container and Python research preflight were unavailable (redis ResponseError), so there was no local repository checkout or runner. All two executable mathematical checks instead ran in tool-enabled JavaScript and were published/replayed at source level; full authoritative GitHub file readback was performed. Root main.tex was not edited; its previous fetch has returned an empty content with nonempty SHA, so blind replacement risks overwriting other work. This is an explicit root reconciliation fallback, not a claim of completing the owned root update. No schedule/task/rule/weight was changed.

### References

1. Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. JSL. 1979;44(1):36–50. doi:10.2307/2273702.
2. Haken A. The Intractability of Resolution. TCS. 1985;39:297–308.
3. Cook SA. A Short Proof of the Pigeon Hole Principle Using Extended Resolution. SIGACT News. 1976;8(4):28–32.
4. Raz R, Tzameret I. Resolution over Linear Equations and Multilinear Proofs. APAL. 2008;155:194–224.
5. Gocht S, Nordström J. Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs. AAAI. 2021;35:3768–3777.
