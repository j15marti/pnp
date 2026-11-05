# LSPV-2/419: extensional ORIGINAL-wire support is a coNP-complete predicate

**November 5, 2026, 07:35 PST. Role:** SAT-Circuit Reduction Builder / LSPV-2. **Status:** PROVED/EXACT for the explicitly declared extensional-support problem, COMPUTATIONAL finite checks, historical native grammar OPEN. **P versus NP OPEN.** No task identities, weights, schedule, role regions or enabled states modified.

## IDEA (before SEARCH)

Test whether the phrase "at most three original variables" in the original Rmix341/341 AND3/LOCAL semantics can be interpreted as the *essential support of an arbitrary nested paid-DEF output circuit* while retaining a polynomial-time exact checker. Falsifiers: a satisfiable G with fewer than four essential fresh y inputs in H_G; an unsatisfiable G with nonzero essential support; false equality of static and extensional support; or failure of the coNP reduction.

## SEARCH and reconciliation

Governing /1204 handoff read first; original /341 blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`; issue #3 through LSPV-2/418; role-owned /417 and /418; peer LSPV-1/419, LSPV-3/406 and /420--423, LSPV-4/414, LSPV-5 REFEREE314/318/363; AGENTS.md, CODEX.md, repository pnp-research skill. Actual Grok `GROKPROOF/2026-11-05_1218_PROGRESS.md` (blob `d3183283`) and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727`) inspected. Indexed web research opened Cook--Reckhow, Haken metadata, Raz--Tzameret ECCC TR07-078, and Vollmer ECCC TR07-045. Authenticated OpenAI GitHub search found `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean`, read blob `e60f4d98`; it has no native mixed proof normalization. Direct Google-branded search unavailable. No claim of a Google query was made. Root main.tex returned an existing SHA but empty body; left intact. Full local repo preflight was unavailable because container git access failed DNS resolution. Explicit constraints and partial scope recorded.

## ITERATE: proved theorem

Let `ESUP3` take an explicitly serialized acyclic Boolean gate DAG and ask whether its output function has at most three *essential original inputs* after expanding all nested conservative definitions. Then `ESUP3` is coNP-complete even with fixed SAT source-clause content `(w)`, with header variable bound adjusted to declare circuit inputs. This is **not** a claim that native LOCAL-CONVERT authorizes this extensional grammar.

Proof: complement NP witness = four distinct essential coordinates, each with a flip pair. From arbitrary CNF G form a paid two-input-gate circuit `H_G=G(x) AND y1 AND y2 AND y3 AND y4`, where the four fresh y variables are otherwise unconstrained originals. G UNSAT iff H_G is constant false (support zero); when G SAT each y coordinate is essential under a satisfying x. The construction is polynomial and uniform, and source `(w)` stays SAT. Original-source header length N is O(log n) for n declared variables, not zero or constant. Compact gate evidence length E and logical paid gate count t are polynomial in |G|, but not thereby a proof of UNSAT G.

A polynomial-time *exact* extensional-support checker for arbitrary nested gates would imply P=NP. Static transitive dependency support is polynomially checkable but can overapproximate: an explicit paid chain with 2(k-1) XOR gates computes x1 while depending syntactically on k originals. Thus a constant-support *truth-table* can only be taken as a native local verifier after the input/dependency/export grammar is pinned down or a separately paid equivalence proof is supplied.

## Verification and source-attested records

Producer: `experiments/arc/lspv2_419_essential_support_hardness.js`, blob `fa973cf781afda683f246f9e45b256aff874dea1`. Independently written verifier: `experiments/arc/lspv2_419_independent_support_verify.js`, blob `13b874144dc3c45a849957862fdde497921318d1`. Raw: `results/raw/arc/2026-11-05_0735_LSPV2_ESSENTIAL_SUPPORT_FIREWALL419_raw.json`, blob `99687423363369c5fa2704b1355f14beb8a14835`. Producer **3,286** checks, independent **1,534** checks. All 256 subsets of the eight width-three full clauses: 255 SAT, 1 UNSAT. Essential support histogram `0:1,4:1,5:6,6:30,7:218`. XOR cancellation controls k=2..7; five malformed fixtures and two independent mutated controls rejected. A first pass mislabeled the empty clause malformed; corrected it as a legal UNSAT clause, reran tests and updated source and raw SHA. Tests are finite; theorem uses independent mathematical proof.

**Report:** `research/agents/lspv-2/2026-11-05_0735_LSPV-2_ESSENTIAL_SUPPORT_FIREWALL419.tex` and same-stem `_refs.bib`. The report is a model boundary, not a legal original-local conversion proof, global minimum, or unrestricted computational lower bound.

## Physical ledger

Logical: t paid circuit definitions; original F remains SAT. Explicit evidence: E bits, all wire references and gate descriptions; source variable-bound header N=O(log n). Naive truth-table support checking has O(n 2^n E) gate-evaluation time and O(E+n) peak materialized bits. A static-cone checker is polynomial in E but inexact. Compact XOR and constant circuits provide alternatives, not free authenticated native proof translations. No conclusion about arbitrary SAT machine runtime or space.

## Immediate role assignments, not scheduler mutations

LSPV-1: distinguish a conditional coNP-hard LOCAL-type verifier from the different B3 requirement, and test whether any proposed B3 machine-to-proof compiler presupposes a semantic-wire equivalence oracle.

LSPV-2: return to exact /341 grammar, with native source/authenticated DEF equation and clause selectors, LOCAL output wires and internal circuit gate charging. Test whether static support is intended versus essential support, then build a legal consumer-preserving countertest or full polynomial compiler.

LSPV-3: audit whether the existing typed/gauge closure uses static or essential support and whether retyping any circuit output is supported by a paid, original-source-authenticated derivation.

LSPV-4: charge n, N, t, E and all construction/verification phases separately; specifically, reject an uncharged 2^n truth table hidden inside a single logical LOCAL node.

LSPV-5: adversarially distinguish semantic equality, native grammar legality and verifier acceptance; ensure constant-size local truth tables are never claimed for arbitrary nested circuit cones without a proof of bounded ORIGINAL support.

**B1, B2, B3, native full normalization, superpolynomial mixed Wbar and P versus NP: OPEN.**
