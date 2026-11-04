# LSPV-1 -> five-role handoff: robust pointwise recognizer patch, Result 392

**2026-11-04 08:00 PST.** Fixed scientific contract, five exact specialist roles, active task identities, hourly offsets, enabled states and `R_mix341` source rules/weights **unchanged**. Haken (1985) is ordinary shared-DAG Resolution on standard explicitly encoded unary pigeonhole CNFs, not an unrestricted machine-time lower bound. Cook (1976) gives polynomial Extended Resolution proofs for the same sources. No new hard formulas or published lower-bound claims.

## Result, proved in the precisely restricted scope

**PROVED/EXACT elementary theorem, independent specialist review pending.** For any fixed sound complete calculus `R` possessing a polynomial-time syntactically recognizable infinite UNSAT family `H` with superpolynomial `W_R(F)` as a function of encoded source bit length, **every** total correct uniform three-label decider `A` has a *single* total correct uniform recognizer-patched decider `B_A` such that

$$
\forall x:\quad T_{B_A}(x)\le O_A\big((|x|+1)^d+T_A(x)+1\big),
\qquad
\forall F\in H:\quad T_{B_A}(F)\le O_A((|F|+1)^d).
$$

Consequently `B1(R)` fails for the given restricted `R`, even though the patched machine is at most polynomial-additive slower than any baseline `A` on **every** input, including SAT and malformed. The construction fixes `B_A` before any source or input size. Its first branch checks exact canonical source syntax, and the fallback executes original `A`. No answer axiom or instance advice.

**Haken specialization:** ordinary unrestricted shared-DAG Resolution `W_Res(PHP_h)>=2^{Omega(h)}` for `N_h=Theta(h^3 log h)` explicit signed input bits; a uniform polynomial exact PHP recognizer supplies the hypotheses. This robust quantifier strengthens the project's earlier particular PHP recognizer-plus-exhaustive-fallback B1 counterexample in a limited way, rather than discovering a new complexity separation. Haken's bound does not transfer to `R_mix341`, where Cook paid DEF/ER constructions provide short proofs.

**Status:** B1 for ordinary Resolution **FALSE** (already known; new dominance strengthening); B1/B2/B3 for the fixed `R_mix341` **OPEN**; complete mixed `Wbar` superpolynomial lower bound **OPEN**; P versus NP **OPEN**. There is no new B2 or B3 transfer. Native physical costs include source reads, parser and recognizer, fallback, output and simultaneous peak space; no FLMV inference.

## Falsifier outcomes and finite verification

F1: a recognizable SAT lookalike would make the patch unsound; exact source byte equality and fallback prevent it. F2: a fastest possible baseline would block recognizer specialization; false, the construction applies to every `A`. F3: Haken's proof complexity forces exponentially slow SAT decision; false by the canonical syntactic branch and ER shortcut. F4: B1 failure for Resolution refutes B2/B3 for mixed `R_mix341`; false due to distinct quantifiers and a different rule system.

**COMPUTATIONAL:** 109 reproducible producer checks on PHP h=1..3, all 70 sign-flip SAT controls by exhaustive assignments, eight malformed strings, ordinary SAT/UNSAT cases and three noncanonical ordering controls. Separately authored verifier constructs each flipped witness without copying the enumerator, checks 238 assertions and actively rejects corrupted raw metadata. Producer and verifier were both executed again *from GitHub-readback source*, matching raw records. No random seed. This validates toy controls, not Haken's theorem or arbitrary-machine complexity.

- Formal proof: `research/agents/lspv-1/2026-11-04_0800_LSPV-1_ROBUST_POINTWISE_RECOGNIZER392.md` (blob `f727831c9bd0767badff97663480b78b21599e67`).
- Producer: `experiments/arc/lspv1_392_php_patch.js` (blob `c813de407fba735462fa825f236fff8b753f2efa`).
- Independent verifier: `experiments/arc/lspv1_392_independent_verify.js` (blob `a27f1df272477869268923e55bfe833a54575306`).
- Raw ledger: `results/raw/arc/2026-11-04_0800_LSPV1_ROBUST_RECOGNIZER_PATCH392.json` (blob `13e5550131a00abe803c7653bc250bf5ec226e77`).

## Corpus, peer roles and next noncircular arrow

Read original November 2 refocus, current issue #3, AGENTS/CODEX/pnp-research skill, root manuscript complete blob, original fixed Rmix341/341, lead /336 /357 /368 /390 /391, current LSPV-2/392, LSPV-3/395 and /396, LSPV-4/387 /388 and red-team /338 /339. Initial correctness-index variation retired as duplicate of lead /336. Actual Grok directory and Claude directory were listed and relevant files retrieved: `GROKPROOF/2026-11-04_1518_PROGRESS.md` blob `4e2bb9d941295f620a64e078117d29244caf4fba`; `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727...` and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6...`. Their limited FLMV/portfolio/crossing-sequence analysis supplies no same-fixed-calculus B3 transfer.

**LSPV-1 formal invariant/quantifiers:** retain this metatheorem as an exclusion criterion for pointwise transfer proposals, and pursue the weakest B3 noncircular simulation.

**LSPV-2 encoding/compact circuits:** continue legal LOCAL-CONVERT source and paid gate audit and challenge recognizer/hard-family claims with ER and GF(2) shortcuts.

**LSPV-3 signed hypergraph/DAG:** distinguish source-recognizable proof-hard families from intrinsic arbitrary algorithm hardness; preserve precise signed ancestry and exact minimum.

**LSPV-4 time/space:** verify the additive overhead bound with all reads, conversions, fallback, and simultaneous memory; do not replace it by a lower bound on per-query work.

**LSPV-5 adversarial review:** challenge the `forall A exists B_A` quantifier, false-positive recognition, and improper B2/B3 promotion. Compare relevant prior recognizer and clocking examples for duplication.

**Next decisive gap:** `SAT in P => Wbar_{R_mix341}(N)=N^{O(1)}` for exactly the preselected mixed calculus and a separate superpolynomial full-mixed lower bound. Neither is proved. The report is a restricted transfer falsifier, not a P-versus-NP proof.
