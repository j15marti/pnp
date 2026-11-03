# SAME-SUPPORT-ALIAS-COMPILER-REFEREE313

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 05:48 PST**

**Status:** PROVED/RESTRICTED stronger-representation substitution lemma; FALSIFIED a concrete per-node exact-materialization lemma; COMPUTATIONAL exhaustive finite audit and independent proof replay. B1, B2, B3, a superpolynomial worst-case minimum, and P versus NP remain OPEN. No task identity, title, enabled state, ownership, schedule, calculus, rule, encoding, or weight changed.

## Exact obstruction and falsified lemma

REFEREE312 proved the safe restricted upper bound

$$
W_{L_3}(F)\le W_E(F)\le24W_{L_3}(F)+O(1)
$$

by materializing an exact CNF basis for every explicit at-most-three-variable factor. Its report explicitly did **not** claim that 24 or per-node materialization is globally necessary. The concrete stronger candidate tested here was:

> **PER-NODE-EXACT candidate lemma.** Whenever a semantic factor label `Q` is consumed by another semantic factor inference, a sound compiler must first derive a CNF whose models are exactly `Q`.

This lemma is false, even without auxiliaries or a semantic oracle. An already authenticated stronger predecessor representation can be carried through a semantic-only region at zero new inference-node cost.

Keep the preselected `Rmix341` unchanged. Let `E` be its strict non-tautological binary Resolution plus paid, conservative, source-independent signed two-input `VARDEF` fragment. Let `L3` be the declared local subgrammar whose exact factor inputs and outputs share at most three named variables. Source clauses are free; every distinct paid inference node has unit weight; shared DAG nodes count once. Optimizer discovery remains excluded from the logical minimum and separately charged as machine work.

## Same-support alias lemma

Let a semantic factor node have declared support `K`. Suppose its authenticated compiled parents have conjunction `Gamma` with model relation `S` on exactly the same support, while the node label denotes `Q`, and soundness gives

$$
S\subseteq Q.
$$

For any further semantic continuation relation `T` on the same support,

$$
S\cap T\subseteq Q\cap T.
$$

Therefore `Gamma` itself is a sound stronger representation of the `Q` node for every downstream inference whose justification is semantic consequence on that same support. No inference is needed merely to change the compiler's bookkeeping label from `Gamma` to `Q`. By induction, a maximal same-support factor-only region needs no internal exact-factor materialization.

At a typed exit this certified scheme stops aliasing and invokes an authenticated compiler. Exits include a strict declared-support change, a clause required as an operand by native Resolution or `VARDEF`, and the final contradiction. REFEREE312 still supplies cost at most 24 for an exact three-variable factor exit; DPLL-IMPLICATE-PRUNE358 supplies cost at most seven for a local false exit. This report does **not** prove those boundaries intrinsically costly: a later joint compiler may derive only the exact exit clause needed or safely carry a larger-support invariant.

This is syntactic proof compilation, not a free semantic step. Every carried clause was already an authenticated source or derived line. The implication `S subset Q` is already the justification attached to the legal `L3` node. The compiler adds no clause, no correctness axiom, no SAT label, and no instance-specific rule.

## Explicit encoded counterexample

Let `S` be the singleton relation `000`, represented by the free authenticated units

$$
(\neg x),\quad(\neg y),\quad(\neg z).
$$

Let `Q` be even parity, mask 105. The legal semantic node `S implies Q` can be aliased by retaining the three units. Let `T` be odd parity, mask 150, represented by its four width-three blocker clauses. Although REFEREE312's independent exact output-basis accounting assigns cost 24 to materializing `Q`, `S conjunction T` contains the clause `(x or y or z)` and refutes in three strict Resolution nodes:

$$
(x\vee y\vee z),\ (\neg x)\ \vdash\ (y\vee z),
$$

$$
(y\vee z),\ (\neg y)\ \vdash\ (z),
$$

$$
(z),\ (\neg z)\ \vdash\ \bot.
$$

Repeating the same semantic even-parity label 1, 2, 4, 8, 16, or 32 times does not alter the three-node compiled refutation. These deliberately redundant chains falsify PER-NODE-EXACT as a compilation necessity; they do **not** show that a shortest `L3` derivation contains redundant nodes or reduce the coefficient between proof minima.

The opposite label control uses singleton `001` with the even-parity factor and also refutes in three nodes. The positive controls `000 conjunction even` and `001 conjunction odd` have their respective singleton models. Thus the shortcut is not an all-UNSAT promise or a parity-label confusion.

A strict support-drop control starts from

$$
(x\vee y)\land(x\vee\neg y)
$$

on support `{x,y}` and outputs `(x)` on support `{x}`. The published certificate pays one genuine Resolution node. Merely relabeling the two source clauses as a unary factor would retain the hidden name `y` and is outside this typed alias lemma.

## Four falsifiers and dispositions

1. **PER-NODE-EXACT:** every semantic factor must be exactly materialized before another semantic consumer. **FALSIFIED** by the stronger-representation invariant and explicit three-node parity control.
2. **Hidden-variable carry:** the same zero-cost alias automatically remains valid after a declared support drop. **REJECTED for this theorem.** The compiler stops at that boundary; the one-node projection certificate pays for the unary exit. No intrinsic lower bound on every larger-support scheme is claimed.
3. **Syntactic-consumer substitution:** a set of stronger clauses may be inserted as though it were the exact single parent clause of a native Resolution node. **REJECTED.** Native operands must be authenticated clauses; an exit clause is derived before that consumer.
4. **Free final false:** since the carried representation is semantically empty, the compiler may label it contradiction at zero cost. **REJECTED.** The explicit roots are replayed strict Resolution empty clauses. Semantic emptiness alone is not a proof node.

## Exhaustive audit and hostile controls

The producer checked all 6,561 entailed pairs `S subset Q` among the 256 three-variable relations and all 256 continuation relations `T` for each pair:

$$
6{,}561\cdot256=1{,}679{,}616
$$

independent instances of

$$
S\cap T\subseteq Q\cap T.
$$

A separately written no-import Node verifier repeated all checks from the raw masks, reconstructed the even/odd CNFs, replayed both three-node parity refutations and the one-node projection certificate, and checked 63 semantic nodes across the six chain lengths. Twelve malformed records and five deliberately corrupted proofs were rejected.

Final raw SHA-256:

`2910a0226c5a417ba6ef05da12eb61e29acc6e80e2dee628c2eb202fd720d169`

## Correct transfer classification

| Obligation | Disposition | Reason |
|---|---|---|
| B1 pointwise | OPEN | The alias lemma compiles one local semantic region; it does not translate every total correct SAT decider on every UNSAT input. |
| B2 worst-case | OPEN | No theorem bounds the maximum fixed-calculus minimum by any decider's worst-case runtime. |
| B3 weakest conditional bridge | OPEN | `SAT in P` still does not imply polynomial `Wbar` for the same preselected `Rmix341`. |

The LSPV-1 ER2 universal-reflection report was refereed independently. Its equivalence says, for a fixed externally correct polynomial-time decider `A`, that polynomial `E` proofs of its universal mask family are equivalent to polynomial all-instance `E` boundedness. The proof pays for evaluator definitions and original-source authentication and does not infer correctness from the rejecting trace. No concrete soundness flaw was found in that scoped equivalence. It explicitly leaves the missing implication from bare `SAT in P` to short universal-family proofs open, so it does not prove B3.

An algorithm fast on this parity control would at most destroy a pointwise-family claim. It would not refute B2 or B3, and no such inference is made.

## Work, space, and encoding ledger

| Phase | Measured record |
|---|---:|
| Python producer wall time | 0.163668512 s |
| Python producer peak host RSS | 10,112 KiB |
| Node verifier wall time | 0.009121025 s |
| Node verifier peak host RSS | 42,164 KiB |
| Producer source bytes | 11,532 |
| Verifier source bytes | 7,725 |
| Raw JSON bytes | 18,814 |

These are host observations, not Turing-machine, proof-search, or FLMV bounds. The logical controls pay three, three, and one inference nodes. Region discovery, semantic-table iteration, parsing, mask operations, proof emission, source/index/head access, scheduling, validation, serialization, and all simultaneously live records remain actual machine work. A scheduled realization retains the all-phase envelope

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\}.
$$

The best derivation may still be chosen freely for `W_R`; the exhaustive alias audit is discovery/verification work and is not charged to that minimum.

## Literature and repository review

Exact web queries included `resolution proof subsumption stronger clause proof compression semantic resolution`, `extended resolution proof simulation substitution stronger CNF representation`, the project-specific same-support compiler terms, and `github.com/openai SAT resolution proof checker CNF minimization`.

- The standard Resolution rule and proof-DAG accounting are reviewed in [The Relative Strength of #SAT Proof Systems](https://doi.org/10.1007/s10817-026-09757-w). The present result uses ordinary semantic transitivity and does not claim a new general subsumption calculus.
- [Semantic Relevance](https://doi.org/10.1007/978-3-031-10769-6_13) records the standard connection between semantic consequence and derivation of a subsuming clause; it supports treating stronger authenticated information carefully rather than importing an arbitrary weaker clause for free.
- Certified preprocessing literature, including [Certified SAT solving with GPU accelerated inprocessing](https://doi.org/10.1007/s10703-023-00432-z), treats subsumption and self-subsuming Resolution as proof-relevant transformations.
- The public [`peitl/short-proof`](https://github.com/peitl/short-proof) tool computes shortest Resolution proofs under a declared proof system. It is relevant to the distinction between local compilation controls and unrestricted mixed minima; it was not used as an oracle here.

Project GitHub searches re-read the verified 12:04 shared handoff, issue #3 peers, LOCAL-TRUTHTABLE-ER2-COMPILER359, DPLL-IMPLICATE-PRUNE358, REFEREE310--312, and ER2-UNIVERSAL-REFLECTION-COMPLETENESS361. A repository-scoped `github.com/openai/math` search for `resolution proof checker CNF substitution` returned no matching implementation. Search absence is not evidence of novelty.

## Artifacts and next exact gap

- Producer: `experiments/arc/lspv5_313/support_alias_compiler_referee313.py`
- Independent verifier: `experiments/arc/lspv5_313/verify_support_alias_compiler_referee313.js`
- Raw ledger: `results/raw/arc/lspv5_313/support_alias_compiler_referee313.json`
- Five-role handoff: `research/coordination/2026-11-03_0548_LSPV5_TO_FIVE_ROLE_SAME-SUPPORT-ALIAS-COMPILER-REFEREE313.md`

Next: optimize authenticated exits from a stronger carried representation directly to the exact clauses actually demanded by native consumers, allowing shared intermediate clauses and conservative auxiliaries. To improve a bound between **minimum** proof costs, one must additionally normalize a shortest `L3` proof so that the number and type of exits are controlled; redundant semantic chains do not suffice. Separately, the decisive global gaps remain a mixed-rule-resistant superpolynomial `Wbar_R` family and B3 for the same fixed calculus.

**P versus NP remains OPEN.**

