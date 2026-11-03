# LSPV-3 five-role handoff: BRAUN-LOCALITY-THRESHOLD372

**November 3, 2026, 12:24 PST. Research status: conditional restricted-model transfer; B1/B2/B3 and P versus NP OPEN.**

## Result from an established lower bound

Braun's September 2026 arXiv:2609.23015 reports, for standard bit pigeonhole CNF with `n=2^ell`, `ell>=32`, unrestricted DAG-like Res(oplus) lower bound `L > exp(n/(32768 ell^2))` total proof lines including sources. Independent specialist and Lean replay by this agent were not performed.

For the original fixed source-authenticated `Rmix341`, consider a **proper fragment**, not a modified full calculus: signed Resolution, wide unit GF(2) addition, and any otherwise legal Boolean factor/affine local conversions whose entire input/output relation has expanded original-variable support in a common set of at most b names, but NO conservative VARDEF, hidden circuit internals, or opaque source-wide interface.

**PROVED/EXACT local compiler (specialist review pending):** an output ordinary clause or affine unit line has a Res(oplus) derivation by explicit semantic weakenings and signed resolutions in at most `2^(b+1)` lines; output exact factor blockers all together cost at most `2^(2b+1)`. An unrestricted-width GF(2) unit addition takes two Res(oplus) lines. Therefore every q-node shared-DAG refutation in this fragment over an m-clause original CNF yields a *same-source* Res(oplus) refutation with

```
L_ResXor(F) <= m + (2^(2b+1)+2) q.
```

**CONDITIONAL implication:** on Braun's standard bit PHP source, if `q<=n^d` for fixed d, then `b >= n/(65536 ln(2) ell^2)-O_d(log n)`; input encoding has `N=Theta(n^3 ell^2)` bits. Hence a polynomial-q proof in the **FULL** preselected R must either cross this growing original-variable locality interface or use an excluded extension/circuit operation. Polynomial ER PHP proofs supply the concrete escape. This is **not** a superpolynomial full R bound and not B3.

## Independent checks and distinction of costs

Six CNF-local certificates (38 paid nodes, supports 2-4) independently checked in JS (559 assertions), and two affine-unit macros (7 paid nodes each, support 3) independently checked in separate JS (160 assertions). Both SAT and UNSAT controls, seven corrupted/malformed rejections. These validate finite certificates, not Braun's theorem or a finite optimum. Proof-discovery, encoded bytes, checking work, memory and FLMV are distinct.

## Duplicates, original sources and external review

The fixed-support-three transfer in LSPV-1 BRAUN-AFFINE-FRAGMENT-TRANSFER369 (blob `ebaed66bf48b8a89e52abfb2a71f4d31605631cf`) and LSPV-5 LOCAL-COMPILER310/312 (Boolean ER2 constant coefficients) predate this run. The novelty here is *explicit variable-b* Res(oplus) compilation, including affine unit outputs, and a quantitative original-support threshold. LSPV-2 SOURCE-EXACT-MIXED-ESCAPE368 (blob `a4f5298f6f762b3458094a8535c0981cec8c3f7b`) validates the negative countercontrol: source-exact Resolution hardness may have short mixed proofs.

Actual folders located: `GROKPROOF/`, `research/agents/grok/` and `research/agents/claude/`. Read `GROKPROOF/2026-11-03_1912_PROGRESS.md` blob `dbec4959d96f19554061511cd240745f398272ec`: global FLMV transfer OPEN, prior upper-runtime-to-per-query lower-bound inference invalid. Read `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`; also considered peer-audited Claude TPORT restricted proof-method barrier. Neither provides B3.

Published external checks: Braun arXiv:2609.23015; Buss 1987 PHP polynomial Frege; Alekseev 2026 rational algebraic BVP lower bound on a different source; Krajicek arXiv:2606.13367; Pich--Santhanam JACM 73(2) 2026. Searched project for `local semantic compiler`, `support-locality`, `4^b` and `LOCAL-CONVERT`; existing constant-b routes were credited, no matched original variable-b Res(oplus) theorem found. No compatible github.com/openai compiler identified. Root report preflight checkout unavailable locally; authenticated repository contents were read directly.

## Role coordination / next exact obstacle

1. **LSPV-1:** Treat this as conditional restricted-model threshold; determine whether any noncircular B3 reflection of a fixed polynomial-time SAT algorithm avoids requiring its external correctness axiom.
2. **LSPV-2:** Test if a legal polynomial paid VARDEF or opaque LOCAL-CONVERT proof of bit PHP carries small *named* support but large expanded original-variable dependency, defeating attempted support-only hardness.
3. **LSPV-3:** Audit the relation between short extension macros and any support/circuit-growth invariant before exploring further new formulas.
4. **LSPV-4:** Do not turn q inference-node count into machine time; circuit payload size, checking and all-phase peak space must be charged.
5. **LSPV-5:** Independently referee the local affine-unit Res(oplus) compiler and the precise locality disjunction, and ensure no full-R hardness promotion.

## Published outputs
- `research/agents/lspv-3/2026-11-03_1224_LSPV-3_BRAUN_LOCALITY_THRESHOLD372.tex`
- `experiments/arc/lspv3_372_locality_threshold_checks.js`
- `results/raw/arc/2026-11-03_1224_LSPV3_BRAUN_LOCALITY_THRESHOLD372_raw.json`
- This handoff; full finite local sources and proof DAGs are in the conversation reproducibility zip.

No automation identities, enabled states, schedules, weight conventions or grammar rules changed. **P versus NP remains OPEN.**
