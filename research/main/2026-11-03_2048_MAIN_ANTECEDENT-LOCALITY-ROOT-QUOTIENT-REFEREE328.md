# ANTECEDENT-LOCALITY-ROOT-QUOTIENT-REFEREE328

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 20:48 PST**

**Status:** PROVED/EXACT semantic-jump counterexample and conditional root-only quotient theorem; COMPUTATIONAL finite controls; authoritative machine grammar still incomplete. B1, B2, B3, a superpolynomial worst-case minimum for the fixed full calculus, and P versus NP remain OPEN. No task, schedule, state, identity, ownership boundary, calculus rule, weight or root file was changed.

## Outcome first

The published `R_mix341` wording does **not** license the feared one-step inference from an arbitrary UNSAT source to false. Its `LOCAL-CONVERT` rule has one already-derived local parent and requires an explicit constant-support implication check. A satisfiable parent cannot imply false. The source CNF is a collection of separately authenticated clause leaves, not one free conjunction node.

However, the audit found an exact boundary that must be made machine-formal:

1. If `LOCAL-CONVERT` may consult the whole source as an uncharged semantic antecedent, every UNSAT formula has a one-node refutation. Bounded output support does not help.
2. If it is genuinely local and circuit internals are private, any arbitrary circuit payload on at most three original inputs can be replaced at the same paid node by its eight-bit root truth table. Logical minimum node count is then representation-independent between the two presentations.
3. Physical cost is not invariant: an explicit private circuit can contain arbitrarily many sensitive payload bits at fixed paid-node count. Evidence length, construction, access, verification and output must be charged separately.

This supplies both a concrete counterexample to an overbroad semantic rule and a surviving restricted representation-independence theorem. Neither is P != NP.

## Fixed calculus audit

The authoritative source is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

- Input is explicit signed DIMACS CNF; malformed encodings are rejected.
- Original clauses are free individually source-labelled leaves.
- Each distinct derived DAG node costs one and has at most two antecedent identifiers.
- `RES` is ordinary binary clause Resolution.
- `AND3` conjoins two conditions with combined support at most three original variables into an exact eight-row factor.
- `XOR` adds two already authenticated GF(2) equations.
- `LOCAL-CONVERT` is unary: from one already-derived local factor/equation it derives a clause or bounded-support Boolean circuit condition only when an explicit constant-support truth-table check proves implication.
- `DEF` pays one node for a fresh, total, conservative two-input Boolean gate; it does not assert the gate output.
- Hidden equivalence tests, answer axioms, unrestricted auxiliary arity and zero-cost derived nodes are excluded.

The unresolved machine syntax is narrower: the maximum circuit payload inside `LOCAL-CONVERT`, the definition of support through named wires, whether internal wires are private, and the exact serialization/checker are not fixed. Thus the 341 source-ancestry theorem and finite certificates stand, but a physical-runtime theorem for the full prose calculus does not yet have one authoritative proof language.

## Lemma 1: antecedent-locality is the semantic-jump firewall

Let a unary conversion record `(P,Q)` be legal only when its explicit already-derived parent satisfies `P => Q`.

**PROVED/EXACT.** A conversion to `Q=false` is legal iff `P` is already unsatisfiable. Therefore a satisfiable local parent cannot be the source of a new contradiction. Conservative definitions do not change this: defining a wire that computes false does not assert that wire.

Conversely, consider the hostile global rule

> from the whole input source `F`, output any one-variable clause `z` whenever the semantic side condition `F => z` holds.

For any CNF `H`, introduce fresh `z` and use `F_H = H AND (not z)`. Then

`F_H => z` iff `H` is UNSAT.

If `H` is UNSAT, the hostile rule derives `(z)` and one strict Resolution with the source `(not z)` closes. If empty output is admitted, `H => false` closes in one node. This rule is uniform, effective by exhaustive search and sound, but it makes all UNSAT proofs constant size. It is exactly the forbidden semantic oracle. A small output interface—even one bit—does not prevent the collapse; explicit local ancestry does.

For a clause-minimally UNSAT source with `m` leaves, the existing binary-ancestry argument still gives `q >= m-1` for every sound source-transparent completion: a `q`-node contradiction root can have at most `q+1` distinct source leaves. This is representation- and algorithm-independent but only linear.

## Lemma 2: root-only circuit quotient

Fix constant `c` (in the current local fragment, `c=3`). Define two **conditional completions**, not rule changes:

- `U_root(c)`: a legal local conversion may serialize any finite acyclic circuit over at most `c` authenticated original inputs, but only its root Boolean relation is visible downstream; internal wires cannot be referenced.
- `T(c)`: the same record carries only the canonical `2^c`-bit root truth table.

Both retain the same explicit parent and accept exactly when row enumeration verifies `P => root`.

**PROVED/EXACT.** For every source `F`,

`W_U_root(c)(F) = W_T(c)(F)`.

Proof: topologically replace every `U_root` output by the truth table obtained by evaluating its root on all `2^c` assignments. The parent relation, conclusion relation, implication result, downstream root references and DAG topology are unchanged, so the paid-node count is unchanged. Conversely, a truth table has a finite circuit realization and is a legal `U_root` payload. The transformations give both inequalities. This argument permits arbitrary adaptive proof choice, shared outer DAGs and temporary payload growth. It fails if uncharged internal wires are visible downstream.

Hence exponential circuit syntax is not intrinsically necessary in the private-root fragment: the compact table is an exact alternative. This is a logical proof-existence statement, not a claim that an arbitrary supplied long payload can be normalized without reading it.

## Lemma 3: physical payload separation

Use authenticated satisfiable local parent `P=x`. For `k>=1`, let a serialized payload have root

`C_b = x AND b_1 AND ... AND b_k`,

where each `b_i` is an explicitly encoded constant bit. The conversion is legal on `b=1^k`; flipping any unread bit makes it illegal. Every deterministic exact validator therefore reads all `k` constant positions on the legal record. A canonical fan-in-two presentation has `2k+1` gate records while the logical skeleton remains two paid nodes in the existing control.

Thus no polynomial in paid node count alone bounds all of:

- intermediate/payload encoded length;
- construction and serialization;
- bit access and updates;
- exact validation;
- output time.

Peak space is only simultaneous live storage. A streaming validator may use much less than payload length and pay rereads/recomputation; no `Omega(k)` writable-space claim is made. Exponential materializations are allowed at their actual costs, while the `2^c` truth table is a compact exact alternative under the private-root hypothesis.

This strengthens the correct interpretation of REFEREE315, blob `66a184474eb04f07b130af031e3cae500c38bf44`: payload sensitivity separates ideal node cost from physical work but does not collapse sound implication and does not lower-bound arbitrary SAT time.

## Established hard-family anchor: exact scope

Haken's 1985 theorem concerns the standard unary pigeonhole-principle family `PHP(h+1,h)` in **ordinary unrestricted shared-DAG Resolution**: for all sufficiently large `h`, every Resolution refutation has at least `2^(c h)` lines for some constant `c>0`. The explicit signed CNF has `h(h+1)` variables and ASCII DIMACS length `Theta(h^3 log h)`. It is a proof-system lower bound, not an arbitrary-machine SAT lower bound. Haken's article itself notes polynomial Extended Resolution proofs; Cook--Reckhow's extended systems permit iterated abbreviations. [Haken 1985](https://doi.org/10.1016/0304-3975(85)90144-6); [Cook--Reckhow 1979](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf).

Mandatory countercontrols:

- polynomial Extended Resolution/Frege PHP shortcuts block direct transfer;
- LSPV-2/378 shows even source retention, deletion witnesses and total conservative source extensions do not preserve ordinary-Resolution hardness;
- odd bridgeless cubic Tseitin CNFs have exact `R_mix341` cost `4h-1` through authenticated AND3/GF(2), despite expander Resolution hardness;
- a circuit-valued local checker may inherit Circuit Value complexity in its payload, but Ladner's P-completeness theorem is not a SAT lower bound. [Ladner 1975](https://doi.org/10.1145/990518.990519).

No exponential-overhead backtranslation is used as evidence of machine hardness.

## Quantifier and B-bridge audit

For the same preselected fully specified calculus `R`:

- **B1:** for every one fixed uniform total correct SAT decider `A`, there is a polynomial `p_A` such that every UNSAT `F` satisfies `W_R(F) <= p_A(|F|+T_A(F))`.
- **B2:** for every such `A`, `Wbar_R(N) <= p_A(N+T_A^wc(N))` for every `N`.
- **B3:** `SAT in P` implies `Wbar_R(N)` is polynomial for every `N`.

With monotone polynomials, B1 implies B2 implies B3. None is proved for the full fixed calculus. The root quotient says the **logical** B statements are equivalent between `U_root(c)` and `T(c)`; Lemma 3 says this does not make physical checker time equivalent for an arbitrary presentation. A global semantic completion would make B1--B3 trivial while making a superpolynomial `Wbar` impossible, so it cannot be used in the target lower-bound program.

No per-input hardcoded label, per-`N` optimizer, nonuniform advice family or machine-correctness axiom is used. Free after-the-fact choice of a minimum derivation remains allowed.

## Four falsifiers and outcomes

1. **Whole-source semantic antecedent plus one-bit output.** FALSIFIES the invariant: `H AND not z => z` iff `H` is UNSAT; constant proof cost results.
2. **Arbitrary private circuit payload.** Does not change logical minimum relative to the canonical table, but FALSIFIES node-count domination of evidence/checking work.
3. **Named-wire/semantic-support shortcut.** OPEN for the authoritative grammar. LSPV-3/382 proves fixed-`k` essential-support recognition of arbitrary succinct circuits coNP-complete; a syntactic authenticated cone is needed or a separate proof must be supplied.
4. **GF(2), DEF, sharing and lazy representations.** They remain permitted compact alternatives. They shorten Tseitin/PHP-style proofs but do not assert unproved outputs; expanded trees and dense tables are never forced when shared/lazy representations suffice.

## Finite replay

The standalone producer exhaustively compared all 256 three-input root functions against all 256 antecedent truth tables: 65,536 implication-presentation pairs, plus root reconstruction, semantic-jump, payload-sensitivity, malformed-record and K4 both-label controls. Total: **67,850 assertions**. A separately written Node verifier made **32 assertions** over the emitted ledger. Odd/even K4 counts were `0/8`; eight malformed/global-source records were rejected. The measured Python host run used 8,832 KiB peak RSS in one replay; it is an experimental upper cost, not a native-machine lower bound.

Artifacts:

- `experiments/arc/lspv5_328/local_convert_root_quotient_referee328.py`
- `experiments/arc/lspv5_328/verify_local_convert_root_quotient_referee328.js`
- `results/raw/arc/lspv5_328/local_convert_root_quotient_referee328.json`

## Current project, Grok and Claude review

Current peer files actually read:

- LSPV-1/378: `research/coordination/2026-11-03_1955_LSPV1_CLAUSE_DELETION_FIBRE378_FIVE_ROLE_HANDOFF.md`, blob `1113a55e1c0e7776d3b6daae588c31a81e4ab594`; source ancestry gives a linear floor, with opaque conversion caveated.
- LSPV-2/378: `research/coordination/2026-11-03_2009_LSPV2_TOTAL_EXTENSION_SPEEDUP378_FIVE_ROLE_HANDOFF.md`, blob `8a920b61db4dfe59ec7d6c4986115163554b22e5`; conservative extensions defeat direct Haken transfer.
- LSPV-3/382: `research/coordination/2026-11-03_2024_LSPV3_SEMANTIC_SUPPORT_LOCALITY382_FIVE_ROLE_HANDOFF.md`, blob `5e5aeca8d0374dfbbd107be755d63a3d8d2ce419`; semantic essential support is coNP-complete for fixed bound.
- LSPV-4/375: `research/coordination/2026-11-03_1936_LSPV4_STREAM_LAZY_INVOLUTION375_FIVE_ROLE_HANDOFF.md`, blob `ba7ac84ebbbfa0fcfe3ff3cc923e486b1418120c`; lazy/stream recoding defeats ordinary-Resolution representation invariance but charges random access.
- LSPV-5/327: `research/coordination/2026-11-03_1948_LSPV5_TO_FIVE_ROLE_UNIFORM-GENERATOR-COLLAPSE-REFEREE327.md`, blob `2a707656de930988b487cbaa5f522f3513bd6509`; a polynomially charged uniform horizon generator is exactly ordinary P, so that route restates B3.

Current Grok `GROKPROOF/2026-11-04_0413_PROGRESS.md`, blob `09396ad9a5bfccfb575845a492e1a91b6c43f56b`, explicitly leaves the all-input fully charged ARC/FLMV transformation open. Claude DIRECTPRODUCT, TPORT and ONETAPE were read at `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` (`95c2649...`), `2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727...`) and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6...`). They concern restricted direct-product/portfolio/tape models and supply neither full-rule semantics nor B3. These are evidence, not authority.

The scoped `github.com/openai` search for Resolution/LRAT checking found no relevant fixed-calculus implementation; absence is not novelty evidence.

## Exact next gap

Publish one authoritative machine grammar for `LOCAL-CONVERT` fixing: parent typing, transitive original-variable support, internal-wire privacy/export, payload serialization, circuit size, proof tags and the checker. The weakest safe choice is the private-root canonical truth-table completion, or separately paid authenticated DEF wires. Then determine whether every legal full mixed proof has a polynomial encoded normal form and separately attack B3. Until that is done, the logical 341 theorems remain valid in their declared source-transparent model, but no physical-runtime transfer should cite an underspecified payload.

P versus NP remains **OPEN**.
