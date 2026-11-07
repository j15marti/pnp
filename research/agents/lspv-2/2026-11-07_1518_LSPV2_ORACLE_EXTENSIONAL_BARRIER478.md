# LSPV-2/478 | Adaptive answer-only oracle extensionality and the FLMV contraction barrier

**2026-11-07 15:18 PST | Route A primary | PROVED/RESTRICTED conditional-resource-model no-go + COMPUTATIONAL finite controls | P versus NP OPEN.**

**Proof-chain references:** [P2-A2] material restricted strategic firewall; existing arithmetic [P2-A3]; resource qualifications [P2-A4] and recursive applicability [P2-A5]; [P1-01], [P1-03], [P1-04] OPEN. No claim about the fixed historical R_mix341 minimum [P2-D1], [P2-B1], [P2-B2], or P versus NP is closed.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis, exact scope:** Could a single algorithm-independent adaptive transducer, given only the SAT/UNSAT/malformed answers returned by a total correct solver on smaller strings, produce the proposed all-input FLMV contraction? In this model, no code, trace, elapsed running time, head position, or other solver-specific data may influence the transducer. The allowed oracle is the same mathematical three-label function for every correct decider.

**Four predeclared falsifiers:** (F1) Different correct solvers could provide different answer transcripts on the same adaptively selected queries. (F2) A correct recursive substitution might not preserve SAT/UNSAT/malformed on every binary source. (F3) Resource recurrence might fail to enter the strict FLMV-forbidden time-space region. (F4) A generic oracle call/return interpreter might require extra native index-tape or writable WORK resources that invalidate the recurrence. F1 is excluded by oracle-function extensionality, F2 by induction under the all-input hypothesis, F3 by exact arithmetic, and F4 is a **genuine qualification**: this no-go assumes a *precharged native same-machine depth-first stack implementation*, not a free unspecified simulator. If F4 holds, the result cannot be applied to that implementation.

**Primary research actually inspected:** Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, Section 2.1 and Corollary 5.8, including direct PDF-page images: https://lance.fortnow.com/papers/files/tst.pdf . Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48(2), 2001, Definition 4.1, Theorem 4.4 and Corollary 4.5, page 156 screenshot: https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf . The latter yields an exponential **ordinary shared-DAG Resolution** size lower bound for odd-charge 3-regular expander Tseitin 3-CNF, not SAT-algorithm hardness. Both sources were searched using web search; no separate Google-branded interface was available.

**Current project actually read:** Complete proof1.txt (startup blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (startup blob 159dbd30b59db8175ec1cbcf9e577ae6670dc93d); current coordination issue #3 and newest peer comments through LSPV-1/488; governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md; AGENTS.md; CODEX.md; .codex/skills/pnp-research/SKILL.md; LSPV-2/476 and /477; LSPV-4/477; actual GROKPROOF/2026-11-07_1920_PROGRESS.md (blob 231561ce216699f286b705a0056584789ba9ee99); Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a); and Claude world-ledger README. Root main.tex returned zero readable content (blob 68188a24badda635a5983fda1c381cdb694fd497), so there is **no root manuscript edit**.

**External repositories actually inspected, exact refs:** konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e (single-tape finite-model P subset NP only); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea (restricted method index, no universal claim); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd19 (parity input generator); openai/math/README.md blob cc5b0a03 (mixed verification statuses); meelgroup/frat-xor/README.md blob 38a137bc (external XLRUP checker, NOT historical R_mix341); lsils/mockturtle/README.md blob c1d2b0c4 (circuit synthesis, no all-input contraction). Reused earlier /477 coverage of the larger solver/checker corpus without pretending these projects prove transfer.

**Iteration:** Strengthen the familiar *source-only splitter is excluded by FLMV* warning to cover **adaptive, answer-only SAT-oracle splitting**. Every total correct SAT decider has the same answer function, so an adapter that observes only those answers remains algorithm-independent even though its queries are adaptive. In contrast, a policy that reads instruction timing or code is not extensional; a finite padded-vs-fast control exhibits the distinction. The missing theorem is solver-*intensional*: safe access to computational structure plus full native charges.

## Theorem 478.1: adaptive oracle-extensional no-go (PROVED/RESTRICTED)

Fix one binary-encoded all-input three-label CNF-SAT predicate L. Suppose a single deterministic uniform oracle transducer Q is independent of the implementation/code of its oracle, receives **only** the exact answer L(y) for each query, and on every binary x of length N:

1. halts with L(x), including malformed encodings, for the genuine L oracle;
2. makes at most N^(a+o(1)) adaptive sequential calls, every queried string having length at most N^(lambda+o(1)), with a=3/5 and lambda=1/2; all sufficiently large inputs have strictly shorter children;
3. spends at most N^(rho+o(1)) local time, rho=11/10, and N^(eta+o(1)) all-phase simultaneous writable peak space, eta=1/2, including parsing, query generation/materialization, source/INDEX/head access, joins, outputs, references and all failed policies;
4. can be recursively invoked depth-first **on the original FLMV random-access machine**, with *all* suspended caller states, native tape/index handling, outputs, retaining/retrieving child messages and returns charged, at only N^o(1) multiplicative overhead in each level's time and space. This is a substantive **explicit extra hypothesis**, not a generic free machine-conversion assertion.

**Then such Q does not exist.** The statement is unconditional within this precisely restricted extensional/stack-charge model. It does **not** say no solver-intensional A -> Phi(A) transformation exists.

**Proof.** All correct total deciders answer every well-formed and malformed binary query identically, namely L(y). Thus Q's adaptive answer-only transcript is a function only of x and L, not of a chosen correct implementation A. Replace each oracle call recursively by Q on its smaller input, with an exact finite base procedure for remaining short lengths. Strict length decrease makes this a single uniform deterministic total all-input SAT decider by well-founded induction.

Let T(N) denote its *fully charged* depth-first time. By hypotheses (2)-(4) and absorbing polylogarithmic overheads,

$$
T(N)\le N^{\rho+o(1)}+
N^{a+o(1)}T(N^{\lambda+o(1)}).
$$

The depth-j exponent is at most a(1-lambda^j)/(1-lambda)+rho*lambda^j, so the total is N^{t_*+o(1)}, with

$$
t_*=\max\{\rho,a/(1-\lambda)\}
=\max\{11/10,6/5\}=6/5.
$$

The suspended-state stack is charged in (4). Its level-j space bound is N^{eta*lambda^j+o(1)}, hence simultaneous peak S(N)=N^{eta+o(1)}=N^{1/2+o(1)}, including the additive O(log log N) depth overhead.

FLMV Corollary 5.8 excludes deterministic time N^c and space o(N^{beta(c)}) for the corresponding nondeterministic-linear-time complete SAT encoding, with any fixed c>1 in its stated range, and

$$
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right).
$$

At c=6/5, beta(c)=23/45=1/2+1/90. Choose sufficiently small fixed epsilon>0 so beta(6/5+epsilon)>1/2+epsilon; the n^o(1) factors, standard quasi-linear/logspace encoding overhead, and native scheduler overhead are swallowed by epsilon. This contradicts the published SAT time-space bound. Q cannot meet all hypotheses simultaneously. QED.

**Resource qualification.** No purported implementation has been shown to satisfy the native stack clause (4). In particular, guest INDEX configurations, suspended work heads, writable high-water positions, child materialization, source retrieval and output copying cannot be silently mapped to a different RAM or counted as zero. This proof *excludes* an already fully charged answer-only implementation. It does NOT prove every candidate native compiler has those bounds or that all implementations are oracle-extensional.

## Hard-family and shortcut ledger

**Certified model-control:** Odd-charge Tseitin formulas on 3-regular expanding graphs, one variable per edge, 4 clauses per vertex, 3H/2 variables, 4H clauses, N=Theta(H log H) explicit binary-encoded bits. Ben-Sasson/Wigderson Cor.4.5 (ordinary Resolution only) proves size 2^Omega(H) for asymptotic expanders. Direct source is already strict 3-CNF, so no lower-bound-preservation conversion is asserted. GF(2) cancellation is a polynomial-time decision shortcut and may support short proofs in stronger permitted systems; all code-assisted reductions must admit it. Previous LSPV-2/475-/477 forest/cycle-defect reductions are restricted upper controls, not unrestricted decomposition. No new hard family is claimed.

## Independent finite computation (COMPUTATIONAL)

Published executable: experiments/arc/lspv2_478_answer_only_extensional_no_go.js (blob c9556c2f06d5126aa8f81b87b0116b175cae6d7a). Published raw: results/raw/arc/2026-11-07_1518_LSPV2_478_EXT_POLICY_RAW.json. JavaScript V8 exact-fraction assertions verify t*=6/5, beta(t*)=23/45 and the strict 1/90 gap. Across 1,030 deterministic toy-predicate inputs at lengths 16, 36, 64, 100, 256, an adaptive query algorithm received identical answers and exact query transcripts from fast and padded correct oracle implementations: 3,090 checks. Its input language is an explicitly three-label prefix/OR **toy**, NOT SAT. A timing-aware observer distinguishes the two implementations, confirming the extensionality assumption matters.

Separately, an original signed strict ternary 3-CNF K4 Tseitin generator and brute-force clause evaluator classify all 16 vertex-charge masks: 8 SAT and 8 UNSAT, with 8 corrupted SAT witnesses rejected and 3 malformed typed-source controls rejected. These finite signed tests are **not** a proof of the theorem. An independent Python fractions.Fraction check of the exact arithmetic was also executed locally (6/5,23/45,1/90). No historical R_mix341 checker or FLMV native machine executor was run.

**Machine ledger:** The mathematical theorem charges Q's entire local query/source/joins workload N^(11/10+o(1)), its <=N^(3/5+o(1)) recursive calls of <=N^(1/2+o(1)) bits, all parent suspension/child output states, recursively stacked WORK, INDEX access, retrieval and recomputation. These are explicitly ASSUMED bounds for a hypothetical Q, not observed runtime or memory of the JavaScript tests. The tests use host JavaScript in-memory strings and ordinary brute force; no native FLMV time or high-water claim is inferred. Proof-system logical nodes, inference evidence bits, and native R_mix341 weights are not used here.

## Status and next missing arrow

This refines [P2-A2] only: an adaptive **answer-only** oracle policy with already established all-input same-machine recursively stacked bounds would be self-sufficient and contradict FLMV. Prior project warnings against a generic source-only splitter remain valid, and the new proof does not establish the missing solver-intensional transformation. Any surviving proposal must state precisely which solver-dependent **intensional** datum is used (code, bounded trace, machine state, timing), prove total correctness of its use, and fully charge its same-machine acquisition/recursive execution. Potentially impossible code optimization is not a free assumption. [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] and P versus NP remain OPEN.

**Publication:** role-owned report/code/raw/handoff paths published independently with exact readback; no other role's manuscript text or governance task changed.

## Primary references

1. Fortnow, Lipton, van Melkebeek and Viglas. *Time-Space Lower Bounds for Satisfiability*. JACM 52(6):835-865 (2005). Section 2.1; Corollary 5.8. https://lance.fortnow.com/papers/files/tst.pdf .
2. Ben-Sasson and Wigderson. *Short Proofs Are Narrow: Resolution Made Simple*. JACM 48(2):149-169 (2001). Theorem 4.4 and Corollary 4.5. https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf .
