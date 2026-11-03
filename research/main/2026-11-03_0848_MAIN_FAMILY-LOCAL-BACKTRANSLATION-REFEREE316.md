# FAMILY-LOCAL-BACKTRANSLATION-REFEREE316

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 08:48 PST**

**Status:** PROVED an exact weakest family-local minimum-domination lemma; PROVED that the established Haken pigeonhole lower bound cannot satisfy even that weakest transfer into the unchanged `Rmix341`, relative to the declared inclusion of paid ER2; COMPUTATIONAL independent both-label, XOR, and malformed-schema controls. B1, B2, B3, a superpolynomial `Wbar_R`, and P versus NP remain OPEN. No task, schedule, state, ownership, calculus, rule, encoding, or weight was changed.

## Established lower bound first

Let `Q` be ordinary DAG Resolution and let `PHP_n` be the standard CNF with `n+1` pigeons and `n` holes:

- variables `x_{i,j}`: `n(n+1)`;
- `n+1` pigeon clauses of width `n`;
- `n * binom(n+1,2)` binary collision clauses;
- explicit binary/DIMACS-style encoded length `N_n = Theta(n^3 log(n+2))`.

Haken (1985) proves that for some constant `c>0`, every Resolution refutation of `PHP_n` has at least `2^(cn)` derived clauses for all sufficiently large `n`. Haken's theorem is about Resolution proof length on this family, not unrestricted SAT time.

Cook--Reckhow (1979) give polynomial-size Extended Resolution proofs of these pigeonhole formulas. In the current project model, paid conservative fan-in-two definitions and Resolution form the declared ER2 fragment of `Rmix341`. Hence on the identical source family

`W_Rmix341(PHP_n) <= W_ER2(PHP_n) = n^O(1)`, while `W_Q(PHP_n) >= 2^(cn)`.

This is the exact transfer obstruction; no new hard family is needed.

## Weakest family-local transfer lemma

Fix any restricted proof calculus `P`, the unchanged mixed calculus `R`, and a same-source UNSAT family `F_n` of encoded length `N_n`. The weakest numerical premise needed to import an established lower bound on this family is

`T0: W_P(F_n) <= C (N_n + W_R(F_n))^d`

for fixed `C>0` and integer `d>=1`. If `W_P(F_n)>=L(n)`, then algebra gives

`W_R(F_n) >= (L(n)/C)^(1/d) - N_n`.

No proof-search algorithm and no effective translator are needed: both sides already refer to after-the-fact minima. The useful hierarchy is

1. **T0:** direct domination of the two minima;
2. **T1:** one minimum-cost `R` proof has some bounded-cost same-source `P` proof;
3. **T2:** every `R` proof has some bounded-cost same-source `P` proof;
4. **T3:** a uniform efficient converter produces that `P` proof.

`T3 => T2 => T1 => T0`, and `T0` is the weakest item sufficient for the family lower-bound import. The proof is one line: choose a minimum `R` proof in T1, or use T0 directly, apply the `P` lower bound, and rearrange. This respects the user's free optimizer-choice convention.

For Haken, any one of T0--T3 would yield

`W_R(PHP_n) >= 2^Omega(n/d)`

and therefore, along the encoded lengths `N_n`,

`Wbar_R(N_n) >= exp(Omega((N_n/log N_n)^(1/3)))`

for fixed `d`. This would be a superpolynomial worst-case minimum lower bound. It would still not prove B3.

## Exact falsification on the same family

For `R=Rmix341`, Haken's family violates T0 itself. The left side `W_Q(PHP_n)` is exponential in `n`; the right side `C(N_n+W_R(PHP_n))^d` is polynomial in `n`, because `N_n` and the ER2 upper proof are polynomial. Therefore for every fixed `C,d`, T0 fails for all sufficiently large `n`.

This is stronger than saying that no efficient proof converter is known. Even an uncomputable, nonuniform, after-the-fact choice of a Resolution proof cannot make the two minimum costs polynomially dominate on this family. Consequently the Haken lower bound is an unusable starting theorem for `Rmix341` unless the calculus or source family is changed; neither was changed here.

The same warning applies to a restricted Tseitin lower bound. Odd-charge Tseitin CNFs can be hard in restricted Resolution-like systems, but the fixed mixed calculus admits the mandatory GF(2) cancellation route when its authenticated XOR rules apply. Summing all vertex equations cancels every edge twice and exposes `0=1`. That shortcut is a countercontrol defeating the attempted transfer, not a bridge to assume.

## Four falsifiers

1. **Because Resolution is a fragment of `R`, its lower bound transfers to `R`.** **FALSIFIED.** Fragment inclusion gives `W_R <= W_Q`, the wrong direction for a lower bound.
2. **It suffices that some long mixed proof backtranslates.** **FALSIFIED.** `W_R` selects the short ER2 proof; the obligation must control the minimum, as T0 does.
3. **An efficient converter is necessary for the minimum-cost implication.** **FALSIFIED.** T0/T1 are existential numerical statements; discovery remains free. Efficiency becomes relevant only for machine-work or B1-style production claims.
4. **Haken plus NP-completeness supplies B3.** **FALSIFIED as an inference.** Haken is restricted proof hardness; NP-completeness does not show that bare `SAT in P` yields polynomial `Wbar_R` for this same fixed `R`.

## Independent exact controls

The Python producer and an independent no-import Node verifier reconstructed rather than downloaded the standard PHP controls:

| Holes | UNSAT pigeons | Variables | Clauses | UNSAT models | Paired SAT models |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 2 | 3 | 0 | 1 |
| 2 | 3 | 6 | 9 | 0 | 2 |
| 3 | 4 | 12 | 22 | 0 | 6 |

The paired SAT count is `n!`, as required for bijections. These finite controls check source semantics only; they do not reprove Haken.

The mandatory K4 Tseitin control exhaustively checked all 64 edge assignments: zero charge has eight models (rank three), while one odd vertex charge has zero. The experiment treats this as an XOR semantic countercontrol, not as evidence for unrestricted hardness.

The transfer-schema validator accepted the source-preserving `R-to-P`, every-proof, polynomial-overhead condition and rejected eight independently reconstructed corruptions: reversed direction, existential-only proof quantifier, optimizer-output-only quantifier, changed source, unbounded overhead, nonpositive coefficient, zero exponent, and nonintegral exponent. The Node verifier made 46 assertions and reproduced every label and rejection.

Raw SHA-256: `b4e6df99d276b4ea1edabd8001d11ae6f66be28ab2c725ddc7d0c26a9c0173fa`.

## B1/B2/B3 referee classification

| Obligation | Status | Exact reason |
|---|---|---|
| Family-local T0 for Haken PHP -> `Rmix341` | **FALSIFIED** | Polynomial ER2 proofs versus exponential Resolution minima. |
| B1 pointwise | **OPEN** | No translation from every total correct SAT decider computation to `R` proofs was supplied. |
| B2 worst-case | **OPEN** | The failure of one restricted-theorem transfer neither proves nor refutes worst-case domination by each decider. |
| B3 weakest conditional bridge | **OPEN** | `SAT in P` still has not been shown to imply polynomial `Wbar_R` for this same fixed calculus. |
| Superpolynomial `Wbar_R` | **OPEN** | Haken and restricted Tseitin lower bounds are defeated by rules already present in `R`. |

An algorithm fast on PHP or Tseitin does not by itself refute B2/B3. Here the stronger fact is proof-theoretic: the fixed calculus has a polynomial proof on the Haken family, so that family cannot witness its worst-case lower bound.

## Grok, Claude, and peer review

The requested folders were located from the repository tree, not guessed: `GROKPROOF/`, `research/agents/grok/`, and `research/agents/claude/`. Exact files and default-branch blob versions reviewed in this run were:

| Path | Blob SHA | Independent assessment |
|---|---|---|
| `GROKPROOF/2026-11-03_1217_PROGRESS.md` | `acf9fbee7079af567db4847ce628c49da45c25b1` | Its restricted query-volume step reverses a runtime upper bound into a per-query lower bound; invalid. |
| `GROKPROOF/2026-11-03_1518_PROGRESS.md` | `234fc189b01fa163eb10e128556e9d22e085b755` | Restricted live-space observation; no representation-independent B3. |
| `GROKPROOF/2026-11-02_2045_ATTEMPT_ARC_CONSTRUCTION.md` | `130939f5d75a6b31a54f45455e7c271051fcbdc4` | Correctly leaves the universal all-input ARC construction open. |
| `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` | `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9` | Barrier only inside its alternation-trading rule set, not an `Rmix341` transfer. |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` | `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a` | Sequential-input crossing-sequence result; not the indexed FLMV model and not B3. |
| `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` | `79e4d4e7e0e3edff3aba8610852c45534bdde128` | Pseudorandom trap route depends on an unproved separation-strength assumption and is retired. |
| `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` | `694c1c8169d9a193397b94e6ee572c476e639a94` | Useful audit of older Grok arithmetic/reference mismatches; no same-calculus transfer. |

Current peer evidence was also checked at exact blobs: LSPV-2 HAKEN-ER2-NONPROJECTION364 `574644bd2c1f4ec18e3dd25236fc0de464611e69`, LSPV-3 BOUNDED-INTERFACE-TRANSFER367 `d63c29ed6a549ad46c8e325aa8a3f4d76a81332a`, and LSPV-4 GROK-QUERY-EXPONENT-FALSIFIER364 `2b2214f2e8a418cc613c651b10508ebff2f7e82b`. Their objections were independently checked; they were not treated as authority.

## Literature and repository searches

Queries covered Haken's Resolution/PHP lower bound, Cook--Reckhow proof simulation and Extended Resolution, Buss/Turan generalized PHP, Tseitin Resolution bounds, project occurrences of Haken/backtranslation/B3, and `github.com/openai` occurrences of Resolution/ER/Tseitin proof simulation.

- A. Haken, [The intractability of resolution](https://doi.org/10.1016/0304-3975(85)90144-6), TCS 39 (1985), proves the established PHP lower bound and notes polynomial Extended Resolution proofs.
- S. Cook and R. Reckhow, [The Relative Efficiency of Propositional Proof Systems](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf), JSL 44 (1979), defines relative proof-system efficiency and extended systems; it does not transfer a lower bound against a weaker calculus to a stronger one.
- S. Buss and G. Turan, [Resolution Proofs of Generalized Pigeonhole Principles](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/WPHP/paper.pdf), records the same exponential Resolution versus polynomial ER/Frege separation and extends the lower bound to generalized PHP.
- D. Itsykson, A. Riazanov, and P. Smirnov, [Tight Bounds for Tseitin Formulas](https://doi.org/10.4230/LIPIcs.SAT.2022.6), gives tight restricted-system Tseitin bounds; its explicit model restrictions are essential.

Project GitHub search found the three current peer audits above. Scoped OpenAI GitHub search found no applicable `Rmix341` proof-system theorem or checker; this absence is not novelty evidence.

## Work and all-phase space ledger

| Phase | Measured record |
|---|---:|
| Python producer wall time | 0.017830686 s |
| Python producer peak host RSS | 9,856 KiB |
| Node verifier wall time | 0.005809163 s |
| Node verifier peak host RSS | 43,960 KiB |
| PHP assignments enumerated | 4,694 |
| Tseitin assignments enumerated | 128 |
| Producer source bytes | 7,621 |
| Verifier source bytes | 4,026 |
| Raw JSON bytes | 4,639 |

These are host measurements, not FLMV bounds. Parsing, formula construction, enumeration, schema validation, serialization, and independent replay were charged. Optimizer discovery is intentionally not charged to `W_R`. The existing all-phase envelope remains `s' <= max{rho, eta, lambda, lambda*s}`. XOR state differences were offline diagnostics only; no free internal oracle was used.

## Artifacts and next transfer target

- Producer: `experiments/arc/lspv5_316/family_local_backtranslation_referee316.py`
- Independent verifier: `experiments/arc/lspv5_316/verify_family_local_backtranslation_referee316.js`
- Raw ledger: `results/raw/arc/lspv5_316/family_local_backtranslation_referee316.json`
- Five-role handoff: `research/coordination/2026-11-03_0848_LSPV5_TO_FIVE_ROLE_FAMILY-LOCAL-BACKTRANSLATION-REFEREE316.md`

The next useful search is now narrow: start from an established lower bound whose proof model already covers every `Rmix341` rule, or prove T0 directly on a family without ER2/XOR/LOCAL-CONVERT shortcuts. Separately, prove the still weaker conditional bridge B3 for the same fixed calculus. Formula generation is justified only to test one of those exact obligations.

**P versus NP remains OPEN.**
