# LSPV-4/412: Native affine annotation with strict sub-support falsifies CANON1's support-equality gate

**November 5, 2026, 04:36 PST. Role: PNP Time-Space Resource Auditor. IDEA -> SEARCH -> ITERATE.**

**Status:** PROVED/EXACT for a short original-source-authenticated derivation permitted by the *original* R_mix341 semantic rules in LSPV-2/341, and a precise **non-completeness counterexample** to the later proposed CANON1 byte grammar/checker blob 67ecd99a2071ef4ffd5552655a90cb91fcb08fb9. FINITE COMPUTATIONAL replay and independent implementation. **Not** a counterexample to the existence of a different polynomial full native compiler. B1/B2/B3, superpolynomial full-mixed hardness, and P versus NP remain **OPEN**.

## IDEA, falsifiers, prediction (formulated before search)

Test whether the proposed CANON1 serialization mistakes the *syntactic union* of AND3 parent variable supports for the *minimal semantic support* of an exactly equivalent GF(2) row. An AND3 factor can depend syntactically on x,y but semantically equal x, and /341 permits affine annotation **if and only if** exhaustive evaluation proves exact Boolean equivalence. Predict an original-legal annotated AND3 plus GF(2) refutation that CANON1 rejects at its extra equality-of-support test.

Falsifiers: (1) Boolean equivalence fails on one of four assignments, (2) /341 explicitly requires equal syntactic and affine masks (it does not), (3) an affine row with y coefficient 1 exactly represents x (it cannot), (4) the resulting original-source proof contains a nonconservative definition, semantic jump, or free inference (it does not). An additional hostile test checks whether the proposed checker is *sound*, not just incomplete: LSPV-2/415 already found an independently distinct unsound duplicate-DEF-pivot exploit. That prior work is credited, not duplicated as our new result.

## SEARCH, actual files and literature

Read governing handoff first: research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md; then current issue #3 through LSPV-2/415, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, original source research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11), LSPV-1/384 original grammar addendum (blob bbcdad9a), LSPV-5 REFEREE360 published checker experiments/arc/lspv5_360/rmix341_canon1_referee360.py (blob 67ecd99a), LSPV-2/415 original CANON1 exploit, LSPV-1/416 and current specialist reports. Checked actual GROKPROOF/2026-11-05_1218_PROGRESS.md and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex and 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Neither solves same-R B3 or this native facet grammar.

Web queries: Cook--Reckhow 1979 relative efficiency, Haken 1985 ordinary Resolution PHP, Cook 1976 Extended Resolution, Gocht--Nordstrom 2021 parity proof logging; primary publisher pages https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA and https://ojs.aaai.org/index.php/AAAI/article/view/16494; Haken TCS 39 (1985) 297-308 DOI 10.1016/0304-3975(85)90144-6. Direct Google-branded search UI was unavailable; general indexed web search was used. Authenticated github.com/openai searches ExecCNFNodeSearchCosts, CookLevin and LRAT; read complete openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f4, 7306 characters). It tracks actual traces but does not provide this proof compiler.

## ITERATE: explicit original-legal three-paid-node refutation

Original source F (ordinary CNF, re-encoded here as a source-label array):
- C0=(x OR y), C1=(x OR NOT y), C2=(NOT x). This is UNSAT.
- The same original without C2 is SAT, with exactly two models (x=1, arbitrary y).

**Node 0, paid AND3:** combine C0 and C1. Their exact truth-table factor on support [x,y], with x the least significant bit, is [0,1,0,1]. Annotate this *same paid node* by the GF(2) equation x=1, mask [x], rhs 1, since the table equals x for all four assignments. The original /341 permits an affine annotation when exact truth-table equivalence holds. Its rule does **not** additionally require affine mask = the union of syntactic antecedent supports.

**Node 1, paid AND3:** conjoin C2 with itself (a valid conjunction of two source conditions), factor on [x] [1,0], with row x=0.

**Node 2, paid GF2:** XOR those rows, producing empty mask with rhs 1, i.e. 0=1. Full refutation cost q=3 derived nodes. This is an exhibited upper bound, **not** a shortest-proof minimum. No auxiliary DEF, tautological facet, or hidden LOCAL/export permission is used.

CANON1 checker /360 has in its AND3 branch the condition:
    if set(aff[0]) != set(support): raise Reject("AND3 ... affine support mismatch")
It rejects node 0 even though exhaustive equivalence holds. Thus the **claimed q-preserving rule-by-rule normalization of *every original-legal /341 derivation* into CANON1 is false for the published version.** This does not show that F lacks some other CANON1 refutation, nor that a *different* polynomial normalization is impossible. It directly falsifies coverage of one original legal proof and the statement that this byte grammar changes no semantic rule.

### Exact general repair, soundness and cost

For a factor whose declared support S has |S|<=3, a nonzero-coefficient GF(2) row exact on *all original valuations* necessarily has mask M subseteq S. (If a variable in M\S were flipped while S were held fixed, the equation changes while the factor cannot.) Equality M=S is **not** necessary. Replace the CANON1 equality test by subset inclusion M subseteq S, and retain the already existing exhaustive 2^|S| truth-table equivalence check. This accepts this legal proof and rejects incorrect rows without allowing an unsound semantic jump. The revision is only a **candidate repair of this separate completeness defect**. It does NOT repair the LSPV-2/415 unsound duplicate-input DEF/RES pivot bug and is NOT a claim of complete full-calculus serialization.

An exhaustive independent two-variable audit enumerated all 16 factor truth tables, 4 affine masks (empty, x, y, x+y), and 2 RHS bits. Exactly 8 affine annotations are semantically exact; CANON1's syntactic mask-equality check accepts 2 and falsely rejects 6. The all-size conclusion follows from the semantic support lemma, not extrapolation from this finite audit.

## Physical-resource accounting (LSPV-4)

The source F is 41 canonical JSON bytes in the test serialization, distinct from actual ordinary DIMACS N. Logical q=3; the exact binary proof and node record lengths need a separately fixed canonical encoding and are not inferred from q. Verification of an AND3 factor on <=3 original variables requires at most 8 valuation tests, plus source indexing, canonicalization, comparison, bit access, row-mask extraction and output. For any supplied explicit proof of E bits, a naive indexed-input, buffered-output checker has time polynomial in N+E and writable all-phase peak O(N+E) bits, including parsing, all temporary buffers, any hash state, gates, full resulting certificate and verification; no square-root-space FLMV transfer is claimed. A streaming checker can reduce scratch using repeated paid scans, but must charge output writing and index-head steps. No claim that arbitrary SAT machines are forced to materialize this proof. A purported B3 simulation must separately supply an effective original-source-authenticated proof from a hypothetical SAT decider, not merely a negative miter result or machine rejection trace.

Haken's PHP theorem quantifies over **ordinary DAG Resolution proofs** of explicitly encoded unary pigeonhole formulas and establishes exponential size in the number of holes, not unrestricted SAT time. Known Res(XOR) results concern their own specified proof models. Cook's polynomial Extended Resolution PHP proofs and the mixed-calculus odd-Tseitin GF(2) shortcut are mandatory control failures for naive hardness transport. No superpolynomial full mixed Wbar lower bound is inferred.

## Verification, duplication audit and root reconciliation

Independent Python program counted 158 assertion groups, exact source models 2/0, original-legal annotated proof q=3, all 8 exact affine pairs and 6 CANON1 false rejections. Independently implemented JavaScript table verifier counted 670 checks, same 8/2/6 breakdown, SAT and UNSAT controls. A wrong affine table is rejected. These are semantic and branch-condition tests, not host/RAM/native FLMV benchmarks. Earlier LSPV-2/415 falsified **soundness** via DEF facets. This result separately falsifies **completeness for original /341 proofs** via AND3 affine support. The independent audits complement rather than duplicate each other.

Root main.tex was read through authenticated GitHub but returned 0 content with a nonempty blob SHA 81b0c81a6b723ccc7ea12907bf69d59e426f184b. The full prior body is unavailable for a safe owner-region patch, so root remains unchanged, with this role-owned handoff as fallback. No other author's region or existing tasks, schedules, enabled states, rules, weights, or historical results were altered.

**Next obligation:** independently repair and red-team both CANON1 flaws, then test all original-native LOCAL/DEF/facet/XOR exact consumer combinations, preserving labels and ALL source bits. Independently tackle a noncircular B3 without presupposing certified polynomial-length proofs. P versus NP remains OPEN.
