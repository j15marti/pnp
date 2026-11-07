# LSPV-3/475 | Boolean-quotient identity firewall for compact all-CNF union circuits

**2026-11-07 07:24 PST | Route B / LSPV-3 | PROVED/RESTRICTED symbolic coNP-completeness reduction and formal-ring mismatch; COMPUTATIONAL independent finite checks. P versus NP OPEN.**

**Tracked exact nodes:** [P2-D1] (OPEN historical native grammar), [P2-D2] (ideal shared-DAG minimum), [P2-D3] (work versus bits), [P2-B1] (OPEN mixed all-rule lower bound), [P2-B2] (OPEN noncircular B3), [P2-C3] (OPEN native translation), [P2-L3-474] (previous PC_B evidence). New proposed evidence [P2-L3-475]. Route A all-input [P1-01]/[P1-03]/[P1-04] stays OPEN.

## IDEA, exact falsifiers stated before research

**Hypothesis.** LSPV-3/474's at-most-8(m-1)-line Boolean-quotient PC_B construction can be stored as O(m+n) arithmetic-circuit gates, but treating its compact terminal as the constant 1 requires a semantic Boolean-cube identity test that is coNP-complete EVEN FOR THAT FIXED CANONICAL CONSTRUCTION. Furthermore ordinary formal-polynomial PIT is not a valid substitute: for every nonempty proper strict-3CNF the unreduced circuit differs formally from 1.

**Falsifiers (predeclared):** (1) canonical circuit construction or source authentication needs exponentially many gates/bits; (2) some SAT instance has terminal 1 on all Boolean inputs, or an UNSAT source has a Boolean counterassignment; (3) ordinary formal-polynomial identity to 1 accidentally holds on a nonempty source; (4) a reported checker accepts changed source bytes, malformed original clauses, or changed gate op as the canonical proof. Any prior project statement of this exact restricted reduction also eliminates novelty, not its validity.

## SEARCH and continuity (actual files, pinned blobs)

Read both COMPLETE root trackers, current issue #3/comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, historical research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, previous LSPV-3/474 report, LSPV-1/477 and its five-role handoff, LSPV-5/411, GROKPROOF/2026-11-07_1220_PROGRESS.md, and research/agents/claude/world-ledger/README.md. Previous result [P2-L3-474] proves the expanded multilinear PC_B length/evidence divergence; **the coNP-complete terminal decision problem and distinct formal-PIT mismatch are the present narrower audit**. No historical accepted-byte R_mix341 proof was found/validated.

Required external GitHub review:
- konard/p-vs-np, scripts/proof_status.json at blob `93b77ed3d8fe456f81c690035f45f07910a247f2`: Lean theorem/proof-status index; no native R_mix341 or all-input SAT solver authentication.
- blkph0x/p-vs-np-proof-research, METHOD_INDEX.md at blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`: specifically scoped affine/locality claims, not same-system B3.
- meelgroup/frat-xor, format.md at blob `986a21aa92b62f844ef1fce852193142c41b2b1f`: XLRUP/XOR theory steps distinct from native mixed syntax; cake_xlrup XOR support limitation explicit.
- tanyongkiam/cake_lpr, README.md at blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`: verified LPR interface, not quotient identity.
- openai/math, README.md at blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`: research manuscripts explicitly include unformalized material; not proof authority.
Primary sources: Cook--Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems* (polynomial-time verification requirement); Grochow--Pitassi, *Circuit Complexity, Proof Complexity, and Polynomial Identity Testing*, JACM 65(6) (2018), DOI 10.1145/3230742; Grochow, *PIT and the Ideal Proof System*, arXiv:2306.02184 (2023); Chvátal--Szemerédi, *Many Hard Examples for Resolution*, JACM 35 (1988), DOI 10.1145/48014.48016. Web-indexed literature search was available; an independent Google-branded search interface was not used. The 2023 IPS/PIT result concerns **formal algebraic identities in its own proof system**, not a justification for treating Boolean-quotient identity here as ordinary PIT.

## ITERATE: new exact restricted theorem

Fix K=F_2 for the decision-complexity statement. Let F be any syntactically valid original-source **proper signed width-three CNF** with n variables and m>=1 clauses C_1,...,C_m. Define the original clause-falsity polynomial
$$
c_j(X)=\prod_{\ell\in C_j}\left(1-\operatorname{val}(\ell)\right),
\quad\operatorname{val}(x_i)=x_i,\ \operatorname{val}(\neg x_i)=1-x_i.
$$
Build the **deterministic canonical** arithmetic circuit U_1=c_1 and
$$
U_j=U_{j-1}+c_j-U_{j-1}c_j\quad (2\le j\le m).
$$
For each Boolean assignment a, induction on j gives U_j(a)=1 if and only if at least one of the first j original clauses is false. Thus
$$
U_m(a)=1-F(a)\quad\text{for every Boolean }a.
$$
Hence **Theorem 475.1 (PROVED/RESTRICTED, all-input exact reduction)**:
$$
F\in\mathrm{UNSAT}_{\mathrm{proper3CNF}}
\iff U_F=1\text{ as a function on }\{0,1\}^n.
$$
Every proper ternary source clause uses two multiplication gates to build c_j. Across the m clauses, the union transition uses three additional arithmetic gates per j>1, plus up to n shared complement gates. Therefore the DAG has at most 5m+n+O(1) gates, and an ordinary explicit indexed encoding uses O((m+n)log(m+n)+|F|) bits; reconstruction and syntactic source/premise checks are polynomial time. Consequently the language of **CANONICALLY CONSTRUCTED** U_F circuits (together with the authenticated original F) whose Boolean-cube value is identically 1 is **coNP-complete** by the standard proper-3SAT reduction. Membership in coNP has a Boolean assignment a with U_F(a) != 1 as an NP witness for nonmembership. This is not a lower bound under P != NP assumptions; it is unconditional completeness in the usual complexity-theoretic sense.

**Theorem 475.2 (PROVED/RESTRICTED, formal PIT mismatch).** For EVERY nonempty proper width-three source F and EVERY field K, the unreduced formal polynomial U_F-1 is nonzero in K[X]. By exact polynomial algebra,
$$
1-U_F=\prod_{j=1}^m(1-c_j).
$$
Every factor is a nonzero formal polynomial because c_j is nonconstant, and K[X] is an integral domain. Therefore the product is nonzero. In particular even for UNSAT F, ordinary **formal** PIT applied to U_F-1 would reject equality to zero; Boolean quotient identity and formal PIT are not interchangeable. A quotient-aware proof has to pay for valid Boolean reductions and a checkable constant-output certificate, use a native sound rule, or provide a proved checker for some other formalism.

**Verifier boundary.** Canonical circuit structure, hashes, source membership, intermediate gate arithmetic *syntax* and subproof references can be checked in polynomial time; this does not certify U_F=1 on all Boolean inputs. If a hypothetical deterministic polynomial-time checker accepted precisely these canonical terminal identities without additional certificates, the same reduction would decide strict 3SAT in P. That is a conditional equivalence, NOT a proof of P != NP, a generic verification lower bound, nor a flaw in sound PC_B with fully materialized lines. These are NOT historical R_mix341 native accepted-byte proofs and must not be counted as native 1-step identity rules.

## Established-family, theorem, encoding, methods and gap ledger

| Family/source | Exact encoding and size | Published model-specific theorem | Shortcut control | Remaining transfer |
|---|---|---|---|---|
| Chvátal--Szemerédi random strict 3CNF at constant density meeting theorem hypotheses | m=Theta(n) proper signed ternary clauses, N=Theta(n log n) bits | Exponential ordinary Resolution size with high probability for specified density; NOT all-mixed/all-machine | CNF-derived union circuit exists for every source, but terminal verification coNP-complete as a class | Original native all-rule R_mix341 Wbar and B3 OPEN |
| Odd-charge cubic-expander Tseitin strict 3CNF | Edge variables 3h/2; four proper signed clauses per vertex; m=4h, N=Theta(h log h) | Published exponential ordinary Resolution size on appropriate expanders; characteristic-dependent PC bounds only | Shared GF(2)/AND3 linear declared-semantic proof, plus U_F compact circuit | No transfer to full historical accepted bytes or B3 |
| K4, K3,3, cube finite odd/even Tseitin controls | m=16,24,32, n=6,9,12; both signs | Certified labels by enumeration only, NOT asymptotic-hard instances | Both labels, polynomial field points outside Boolean cube, corrupted source and circuit | Finite validation only |

## Reproduction and adversarial audit

Producer `lspv3_475_produce.py` and independently implemented `lspv3_475_independent.cjs` used different Boolean evaluators. Eight instances: odd/even K4, K3,3, cube; all-eight-clause UNSAT strict ternary core; single-clause SAT. Source labels independently enumerated on 9,360 original assignments; 37,440 field-specific evaluations in F2/F3/F5/F101 agreed with original CNF. The independent Node verifier passed 37,534 assertion groups and rejected 6 malformed source controls and 16 source/circuit mutation controls; eight non-Boolean F101 points with all x_i=2 yield U_F!=1, supporting the formal-ring mismatch (the full symbolic proof does NOT depend on finite evaluations). Node counts and SHA256 digests in the local reproducibility archive. Standalone executable under `experiments/arc/lspv3_475_quotient_circuit_firewall.cjs` is a compact regeneration, not the authoritative historical checker.

**Resource ledger:** Construction O((m+n)polylog(m+n)) machine time for indexed gates and O((m+n)log(m+n)+N) full emitted bits. Evaluating at one Boolean assignment O(m+n) field operations and O(m+n) intermediate values, or streaming/liveness analysis with retention tradeoffs; deterministic exhaustive terminal checking uses O(2^n(m+n)) operations, with variable-space enumeration and O(m+n) gate storage. This upper bound is not claimed optimal. Ordinary expanded multilinear proof lines can require exponential monomial occurrences ([P2-L3-474]); source/index/head parsing, hashes, writes and independent verification are additional actual phases. Weighted native R_mix341 node charges cannot be assigned to these external circuit gates. Ideal minimum still excludes derivation discovery but an implemented checker must pay all terminal validation phases. No native-checker or FLMV timing/space was measured.

## Status, no overclaim and handoff

**Actual advance:** an exact coNP-completeness reduction for the canonical compact PC_B terminal-validation problem and a universal formal-PIT nonidentity proof. Both are bounded to a DISTINCT circuit/quotient system. No proof that P != NP, no superpolynomial R_mix341 minimum-work lower bound and no B3 result.

**Next falsifier:** implement a fully original-source authenticated historical accepted-byte native definition/AND3/GF(2)/LOCAL-CONVERT certificate and test whether any purported Boolean-circuit identity shortcut is really an allowed paid native sequence; distinguish native valid proof from semantic circuit summary. Coordinate LSPV-1 and LSPV-5. Keep all five role assignments and fixed weights unchanged.

**Tracker handling:** [P2-L3-475] is a new scoped evidence entry to [P2-D3]/[P2-B2], not a change to OPEN load-bearing statuses; proof1 unchanged. Publication/readback and issue #3 metadata to be separately verified; root main.tex left unchanged absent safe complete read and ownership preservation. P versus NP remains OPEN.
