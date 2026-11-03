# SOURCE-AWARE-EXIT-COMPILER-REFEREE314

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 06:48 PST**

**Status:** PROVED/RESTRICTED source-aware factor-exit theorem; FALSIFIED two concrete necessity lemmas; COMPUTATIONAL exhaustive finite optimization and independent encoded-DAG replay. B1, B2, B3, a superpolynomial worst-case minimum, and P versus NP remain OPEN. No task identity, title, enabled state, ownership, schedule, calculus, rule, encoding, or weight changed.

## Exact obstruction

REFEREE312 safely compiled every explicit at-most-three-variable output factor into an exact CNF basis with source-independent width charges

$$
b_1=3,\qquad b_2=4,\qquad b_3=6,
$$

giving the restricted upper bound

$$
W_{L_3}(F)\le W_E(F)\le24W_{L_3}(F)+O(1).
$$

REFEREE313 then showed that a stronger authenticated representation may pass through a same-support semantic region without materializing every intermediate factor. The next question was whether its typed exits necessarily require the full source-independent basis charge.

The concrete candidates tested here were:

1. **PARITY-24 necessity:** the published unique-`000` source cannot produce the exact even-parity exit in fewer than the displayed 24 paid nodes.
2. **STRICT-DROP-CHARGE necessity:** every strict factor-support drop must pay at least one inference node to remove the hidden variable.

Both are false. REFEREE312 itself correctly described 24 only as an output-only weighted-basis upper bound, not a full-calculus minimum. This report supplies the previously missing shorter authenticated exit proofs.

## Fixed calculus and source family

Keep the preselected `Rmix341` unchanged. Let `E` be its strict non-tautological binary Resolution plus paid, conservative, source-independent signed two-input AND `VARDEF` fragment. A definition node for

$$
q=(a\land b)
$$

authenticates the three signed slots

$$
(\neg q\vee a),\quad(\neg q\vee b),\quad(q\vee\neg a\vee\neg b).
$$

Each distinct definition or Resolution inference has unit weight; original source clauses are free; shared nodes count once.

For each assignment `a` on three variables, define `U_a` to contain, for each variable pair, all three binary non-tautological clauses true under `a`. Thus `U_a` has nine clauses and the unique model `a`. The eight sources are fixed polarity renamings of one another.

## Source-aware clause certificates

Every clause entailed by `U_a` is simply a clause true under `a`. It has one of three authenticated treatments.

### Binary clause: zero nodes

Every binary clause true under `a` is already one of the nine original clauses of `U_a`.

### Unit clause: one node

For a true literal `l` and another variable `y`, both

$$
(l\vee y),\qquad(l\vee\neg y)
$$

are original source clauses. Resolving on `y` derives `(l)` in one node.

### Ternary clause: three nodes

Let the target be

$$
C=(u\vee D\vee L),
$$

where the binary subclause `(u or D)` is true under `a`, hence is an original source. Introduce one fresh paid definition

$$
q=(\neg u\land\neg L).
$$

Its slots include

$$
(\neg q\vee\neg u),\qquad(q\vee u\vee L).
$$

Then two strict pivots give

$$
(u\vee D),\ (\neg q\vee\neg u)\ \vdash\ (D\vee\neg q),
$$

$$
(D\vee\neg q),\ (q\vee u\vee L)\ \vdash\ C.
$$

This is the already published CONSTANT-CHARGE-WEAKENING360 construction specialized to the actual binary source. REFEREE312's explicit control instead used two definitions and four pivots per parity clause; that six-node construction remains sound but is not shortest among these displayed authenticated proofs.

## Computer-assisted source-aware factor theorem

For every assignment `a` and every relation `Q` containing `a`, minimize over exact auxiliary-free CNF bases of `Q` using the authenticated recipe charges

$$
c_1=1,\qquad c_2=0,\qquad c_3=3.
$$

Complete dynamic programming over all 26 nonempty non-tautological clauses gives

$$
\max_{a\in\{0,1\}^3}
\max_{Q\ni a}
\min_{\Gamma:\operatorname{Mod}(\Gamma)=Q}
\sum_{C\in\Gamma}c_{|C|}=12.
$$

There are 1,024 source/output pairs. Their exact recipe-cost histogram is:

| Cost | Pairs |
|---:|---:|
| 0 | 584 |
| 3 | 296 |
| 6 | 96 |
| 9 | 40 |
| 12 | 8 |

For each assignment `a`, the unique cost-12 output is the parity relation containing `a`: mask 105 for even `a`, mask 150 for odd `a`. Its exact basis consists of four ternary clauses, each derived by one source-independent definition and two strict Resolution nodes. Thus all eight polarity-renamed controls have explicit 12-node exits.

The dynamic-programming optimum is exact only for this declared independent-clause source-aware recipe. It is **not** a lower bound against unrestricted shared `E` DAGs; sharing definitions or deriving a different intermediate representation may reduce the full minimum further.

## Zero-cost strict support drop

From `U_a`, project to variables `x1,x2` and retain the parity of their values under `a`.

- If the bits agree, the output equality factor has basis

$$
(\neg x_1\vee x_2),\qquad(x_1\vee\neg x_2).
$$

- If the bits disagree, the output disequality factor has basis

$$
(x_1\vee x_2),\qquad(\neg x_1\vee\neg x_2).
$$

In either case both clauses are already original clauses of `U_a`, contain no `x3`, and define exactly the declared two-variable output relation. The strict support drop therefore costs zero paid inference nodes. This does not mean all support drops are free; it falsifies only the proposed universal necessity of a paid elimination node.

## Four falsifiers and dispositions

1. **The displayed REFEREE312 parity control needs 24 nodes.** **FALSIFIED:** eight independently replayed polarity controls use 12 nodes each.
2. **Every support drop requires a paid hidden-variable elimination.** **FALSIFIED:** equality/disequality output bases reuse two original source clauses and cost zero in all eight controls.
3. **Source-aware basis reuse is instance-tailored advice.** **REJECTED.** `U_a` is one fixed eight-member polarity orbit; clause selection and the finite DP are uniform and independently recomputable. Every reused clause is authenticated by its original source index.
4. **A 12-node recipe proves the unrestricted exit minimum is 12.** **REJECTED.** It is a sound upper certificate and an exact optimum only inside the declared independent-clause recipe. Shared definitions, XOR, circuits, or a different proof may be shorter.

## Both-label, malformed, and corruption controls

For every `a`, `U_a` conjoined with the parity relation containing `a` has exactly the model `a`; conjoining the opposite parity relation has no model. The verifier independently reconstructed all eight sources and both parity bases.

The Python producer emitted 32 three-node parity-clause certificates, totaling 96 paid nodes. The no-import Node verifier replayed all definitions, signed slots, pivots, fresh outputs, and roots, plus eight independent one-node unit-demand certificates, for 104 replayed paid nodes. It also checked all eight zero-cost strict support drops, all 1,024 exact bases, 12 malformed records, and five deliberate proof corruptions.

Final raw SHA-256:

`f049ffb592c765ee098280bca017247bb5addb26188b01f46cc55897c9480fdf`

## Correct bridge classification

| Obligation | Disposition | Reason |
|---|---|---|
| B1 pointwise | OPEN | A source-aware local exit proof does not translate every total correct SAT decider on every UNSAT input. |
| B2 worst-case | OPEN | No result bounds the maximum fixed-calculus minimum by a decider's worst-case runtime. |
| B3 weakest conditional bridge | OPEN | `SAT in P` still does not imply polynomial worst-case minimum cost for the same fixed `Rmix341`. |

This result shortens one candidate hard control and eliminates another proposed mandatory local cost. It is a family/representation failure, not an upper bound on the worst-case function. A fast derivation on this orbit does not refute B2 or B3.

The post-REFEREE313 peer review was also reconciled: matching-merger Tseitin, arbitrary read-once AND-tree miters, and heterogeneous guarded-Horn backdoors all have polynomial or source-floor proofs; the GF(2) matrix-power result concerns supplied-certificate validation rather than proof search. None establishes or refutes unrelativized B3.

## Work, space, and encoding ledger

| Phase | Measured record |
|---|---:|
| Python producer wall time | 0.064960370 s |
| Python producer peak host RSS | 10,624 KiB |
| Node verifier wall time | 0.034682579 s |
| Node verifier peak host RSS | 50,544 KiB |
| Producer source bytes | 13,673 |
| Verifier source bytes | 9,098 |
| Raw JSON bytes | 105,519 |

These are host observations, not Turing-machine, proof-search, or FLMV bounds. The exact logical costs count only authenticated `VARDEF` and Resolution DAG nodes. Parsing, all source scans, relation enumeration, dynamic programming, basis selection, fresh-name allocation, proof emission, checking, serialization, scheduling, caches, and simultaneous live records remain machine work and space. The all-phase envelope remains

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\}.
$$

Free selection of the best legal derivation remains intentional for `W_R`; the basis optimizer is discovery work outside that minimum.

## Literature and repository review

Queries included `resolution proof weakening simulation extended resolution three steps clause weakening`, `SAT proof preprocessing subsumption proof logging extended resolution`, project searches for CONSTANT-CHARGE-WEAKENING360 and REFEREE312/313, and an `openai/math` search for extended-resolution weakening checkers.

- [The Relative Strength of #SAT Proof Systems](https://doi.org/10.1007/s10817-026-09757-w) reviews Resolution with explicit weakening. The present result implements weakening through already legal paid definitions and strict pivots rather than adding a free rule.
- Kiesl et al., [Verifying Refutations with Extended Resolution](https://www.cs.utexas.edu/~marijn/publications/rat.pdf), emphasize explicit proof traces for extension-based transformations.
- Heule and Biere, [Proofs for Satisfiability Problems](https://cca.informatik.uni-freiburg.de/papers/HeuleBiere-APPA15.pdf), discuss proof logging for preprocessing and extension-like transformations.
- [Factoring Learned Clauses](https://doi.org/10.4230/LIPIcs.SAT.2026.28) studies practical reuse of Extended Resolution structure. It is relevant context for shared exits, not a source of this finite coefficient.

Project GitHub search confirmed that CONSTANT-CHARGE-WEAKENING360 already proved the one-definition/two-pivot gadget and that DPLL-IMPLICATE-PRUNE358 already cited it. REFEREE312 reviewed that work but its explicit 24-node parity control used the older six-node-per-clause construction. The correction is therefore a project-integration result, not a claim of academic novelty. The scoped `github.com/openai/math` search returned no applicable proof checker or compiler; absence is not novelty evidence.

## Artifacts and next exact gap

- Producer: `experiments/arc/lspv5_314/source_aware_exit_compiler_referee314.py`
- Independent verifier: `experiments/arc/lspv5_314/verify_source_aware_exit_compiler_referee314.js`
- Raw ledger: `results/raw/arc/lspv5_314/source_aware_exit_compiler_referee314.json`
- Five-role handoff: `research/coordination/2026-11-03_0648_LSPV5_TO_FIVE_ROLE_SOURCE-AWARE-EXIT-COMPILER-REFEREE314.md`

Next: search for shared definitions across the four parity exit clauses and certify or refute an unrestricted `E` minimum below 12 for this source. More importantly, any global compiler improvement must normalize a **shortest** `L3` proof so that its number of typed exits is controlled. The decisive global gaps remain a mixed-rule-resistant superpolynomial worst-case family and B3 for the same fixed calculus.

**P versus NP remains OPEN.**

