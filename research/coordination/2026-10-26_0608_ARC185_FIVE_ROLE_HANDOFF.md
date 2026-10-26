# ARC185 five-role formal proof handoff, 2026-10-26 06:08 PDT

**Mode:** LSPV-1 formal proof lead. Scientific spine remains adaptive source-authenticated UNSAT certificates plus circuit constructions, only as a route to a fully charged all-ordinary-input ARC/FLMV or exactly hypothesized van Melkebeek contradiction. Exactly five existing hourly staggered research roles remain; no schedule/task state was changed. `P != NP` and ARC-EDGE-90 are OPEN. Peer-review pending.

## New exact link and separate firewall

`PAIR2` authenticates original proper 3-CNF clauses `(a OR b OR z)` and `(a OR b OR NOT z)` by original DIMACS byte offsets and derives `(a OR b)` without calling a full-parent SAT solver. `QUAD1` authenticates all four `(a OR (+/-)y OR (+/-)z)` clauses and derives the unit `a`. Streamed two implication paths `x -> NOT x` and `NOT x -> x` give a sound UNSAT proof. Source scan + verified proof stream admits symbolic `T=O((N+P) polylog(N+P))`, `S=O(log(N+P))` indexed/work bits with a separate, read-only/one-way proof stream. This is verifier time, not certificate discovery cost, not actual Python space.

The connected minimally UNSAT proper signed 3-CNF family `F_n=Pad((x1) AND conjunction_i (NOT xi OR x(i+1)) AND (NOT xn))`, `n>=2`, has exactly `2n+3` variables, `2n+6` ternary clauses, physical length `Theta(n log n)`, a global clause-hitting set lower bound `floor(n/2)`, and a zero-branch source-authenticated certificate of exactly `2n` implication edges (`O(n log n)` proof bits). Every single source ternary deletion becomes SAT, with an explicit model. Therefore the user's new global clause-hitting falsifier is real even on connected minimally UNSAT inputs, while such global width DOES NOT lower-bound all adaptive/local proofs.

Aspvall-Plass-Tarjan's implication graph criterion supplies complete `O(q log N)` proof coverage for the **proper-3CNF padded-2CNF image only**, never all ordinary UNSAT. No parent `A` query, free SAT label, or forged source offset. Source verifier checks both SAT rejection and UNSAT coverage on this restricted image.

**Exact negative target firewall:** Every proper clause-monotone ternary CNF categorically excludes direct PAIR2 and QUAD1 source patterns: complementary pad signs force at least one mixed-sign clause. Hence even the original 198-variable 264-clause Döcker monotone exact-(2,2) UNSAT source cannot be handled by the bare rule grammar. The W1 15-variable, 20-clause proper signed exact-(2,2) UNSAT source also has zero PAIR2 pairs (exhaustively checked), although it is not clause-monotone. Role-3's richer adaptive BRANCH/EMPTY/PATH grammar may still certify both; no impossibility is asserted for it.

## Reproduction and separate cost facts

Program: `research/agents/lspv-1/2026-10-26_0608_ARC185_local_offset_resolution.py` (SHA256 `3f666934ebaab41109593f69e7c79475e15df1977d67bf1557d10c0d368e2b7a`).
Raw: `research/agents/lspv-1/2026-10-26_0608_ARC185_local_offset_resolution_raw.json` (SHA256 `e33257f118afac5296f114bfa7da6df764b99ce9fe7fa8bde471cefe1ee240cb`).
Report: `research/agents/lspv-1/2026-10-26_0608_LSPV-1_ARC_LOCAL_SOURCE_RESOLUTION185.tex`.
Bib: `research/agents/lspv-1/2026-10-26_0608_ARC185_references.bib`.

Standard-library Python reran twice, identical JSON SHA. 4,107 assertions, zero failures. Eleven formula sizes `n=2..160` in declared reproducible list; all source ternary deletions had independently replayed explicit SAT witnesses, and n<=5 deletions underwent exhaustive SAT truth tables. 210 seeded random 2CNF controls, 97 SAT/113 UNSAT; every UNSAT had two authenticated implication paths, no SAT instance did; 2,100 sampled assignment-equivalence checks. Original W1 exhaustive 2^15 UNSAT and grammar validation; three forged proof classes rejected. Two real restriction and properization levels followed UNSAT 16->14->12 and SAT 12->10->8 ordinary proper ternary clause counts; children are NOT exact-(2,2), no asymptotic power shrinkage. Independent original Döcker source connector check: 264 monotone clauses, 198 variables two occurrences per polarity, zero PAIR2 pattern. Physical work/space not measured.

## Precise unfilled edges

1. **All ordinary UNSAT:** Prove (or falsify with a concrete lower-bound argument for a precisely defined proof grammar) a machine-uniform cap `forall F in UNSAT, exists authenticated proof pi with P<=N^{b+o(1)}`, without implying a shortcut from a restricted proof system to arbitrary SAT algorithms. The present grammar is inadequate on untouched monotone exact-(2,2) even as a *syntax*.
2. **Guest and selector:** A hypothetical deterministic all-ordinary SAT `A` under `P=NP` has unknown simultaneous exponent `(K,K)`. No `d=1.802,s=o(1)` seed. Prove a charged K-dependent compiler with true child length, source references and local-access indexes, same-machine time/peak space, or retire the route.
3. **Theorem transfer:** van Melkebeek 2007 Theorem 1.3 is **OR** of `(c-1)d<1` and `cd(d-1)-2d+1<0`, requiring both a total co-nondeterministic all-SAT time `N^c` machine and a separate simultaneous deterministic time `N^d`/space `N^e` machine. The present restricted proof relation satisfies neither all-input premise. FLMV uses its own matched indexed-input random-access model and a simultaneous pair on one deterministic program. No circuit-size or proof-width-to-decision complexity transfer established.

## Requested role checks, without modifying schedules or task prompts

- **LSPV-2, circuit and compilers:** Supply a source-locally indexed certified algebraic/implication rule that also applies to untouched monotone exact-(2,2), or show an explicit signed regularizer from this grammar that preserves local byte-offset access with fully paid expansion. Do not substitute the fixed-record witness verifier for a decision circuit.
- **LSPV-3, adaptive certificate coverage:** Integrate PAIR2/QUAD1 as source-authenticated pre-restriction reasoning rules into `BRANCH/EMPTY/PATH`; challenge W1/U/connected expanders, certificate existence and uniformly bounded volume; test SAT rejection and two hereditary levels.
- **LSPV-4, resources:** Independently implement read-only byte-offset proof checker in the exact indexed FLMV TM, verify proof one-way semantics, all source/work writes including unchanged writes, address/control arithmetic, proof cap and actual peak stack; add full descendant/properizer output costs where relevant.
- **LSPV-5, referee/root synthesis:** Audit the minimality witnesses, `floor(n/2)` global hitting bound, 2SAT path criterion and exact monotone PAIR2 exclusion. Preserve `OPEN` and source/target typing. Check whether the new rule is a genuinely useful source-derivation bridge or subsumed by existing proof systems without added ARC value.
- **LSPV-1:** Maintain same-machine ARC proof DAG. No other scientific spines are activated. Role-owned `main.tex` update only, fresh SHA, other regions byte-preserved. Do not claim a peer accepted the handoff.

## Corpus/provenance limitations

Directly read originals: LSPV-2 `CIRCUIT-OBLIVIOUS-INVERSE-SORT166`, LSPV-3 `ADAPTIVE-SOURCE-POINTER-STREAM131`, LSPV-4 `ARC-PINNED-CIRCUIT-OUTPUT-FLOOR131`, LSPV-5 `BACKDOOR-CAP161`, LSPV-1 `ARC-CANONICAL-SELECTOR-AUTH184`, root `main.tex`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, original 198-var source. Primary published sources: Aspvall-Plass-Tarjan 1979; Döcker 2019 arXiv:1912.08032; FLMV JACM 2005; van Melkebeek ECCC TR07-099 Theorem 1.3; Ben-Sasson-Wigderson JACM 2001. Exact named Continuation PDF/source bundle not recovered in accessible Library search. GitHub repository shell checkout not available and no claim of repository preflight script success.

END_HANDOFF::ARC-LOCAL-SOURCE-RESOLVE185