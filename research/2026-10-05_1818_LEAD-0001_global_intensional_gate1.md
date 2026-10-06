# LEAD-0001 — GLOBAL-INTENSIONAL-GATE1

**Agent:** LEAD  
**Status:** CANDIDATE architecture lemma / proof-program constraint  
**P vs NP status:** OPEN. Nothing here establishes an unconditional separation.

## Purpose

This report records a recovered route connecting the project's arbitrary-algorithm extraction problem to monotone lower bounds, while preserving the distinction between an unconditional lower bound inside a restricted representation and an unconditional lower bound against arbitrary polynomial-time SAT algorithms.

## Candidate gate

Consider an optional-clause family whose associated monotone UNSAT predicate is polynomial-time decidable but has a known superpolynomial monotone-circuit lower bound.

A proposed SAT-to-monotone compiler cannot obtain the desired contradiction merely from:

1. extensional behavior of a SAT decider on the restricted family; or
2. polynomially many adaptive black-box SAT answers.

The missing operation must use information not reproduced by the restricted polynomial-time evaluator or by oracle replacement.

### GLOBAL-INTENSIONAL-GATE1

Any successful compiler along this route must simultaneously have:

- **GLOBALITY:** some load-bearing step uses correctness of the SAT decider outside the restricted hard family;
- **INTENSIONALITY:** some load-bearing step depends on the ordinary source/implementation of the decider rather than only its input-output answers;
- **SOURCE CHARGING:** acquisition, inspection, transformation, verification, and reuse of that source-dependent information are explicitly charged;
- **LOWER-BOUND LANDING:** the compiler output either achieves a genuine contraction adequate for the project's recurrence, or lands in a representation class having an unconditional superpolynomial lower bound.

This is presently **CANDIDATE**, not PROVED/EXACT as a theorem about arbitrary SAT algorithms.

## Quantifiers to preserve

The target cannot silently replace

```
forall polynomial-time SAT deciders A
  exists a hard formula/family F_A
  such that a model-matched charged extraction from (A,F_A)
  yields the forbidden object
```

with the weaker or different

```
exists F
  forall A
  ...
```

or with a statement about one chosen representation of A.

Likewise, semantic existence of a small object is not acquisition of that object, and representation size is not runtime.

## Why the recovered monotone route matters

The project currently has at least three possible contradiction outputs:

1. **CSE contraction:** compile A and F into children/subinstances giving a strict recurrence exponent improvement.
2. **ASCS/FSC verifier/separator:** compile A and F into an exact small source-sensitive certificate/verifier object.
3. **Monotone landing:** compile A into a restricted monotone representation for a function with an unconditional monotone lower bound.

These appear to share the same missing bridge: a global, intensional, source-sensitive compiler from an arbitrary polynomial-time SAT decider to a fully charged object in a lower-bounded model.

## Oracle-shadow hostile control

Give the adversary/oracle every semantic SAT answer reasonably requested by the construction.

Then ask exactly which compiler step still fails.

If all uses of A can be replaced by oracle calls preserving the proof, the proposed hinge is still relativizing and does not supply the intended nonrelativizing bridge.

A timer, provenance label, hash, transcript, feedback edge, or SAME_REALIZATION assertion is not by itself enough. The proof must identify a resource or consistency property that the oracle cannot simply provide while satisfying the formal interface.

## Algebrization audit

Passing the oracle-shadow test is not sufficient. A distinct algebrization audit remains necessary. Source dependence or nonrelativization alone does not imply nonalgebrization.

## Literature clue

Exact search-to-decision phenomena in meta-complexity/minimum-formula-size problems show that nonrelativizing reductions can exist when they exploit sufficiently specific intensional/minimization structure. This is evidence for investigating the architecture, not a transfer theorem to SAT.

The project should therefore search for a SAT-native analogue rather than citing such reductions as though they already instantiate CSE/FSC.

## Hostile controls

Any candidate compiler should be tested against:

- parity/Tseitin instances with algebraic shortcuts;
- Horn, dual-Horn, and 2-SAT;
- bounded-treewidth formulas;
- independent products;
- padding and variable renaming;
- auxiliary-variable encodings;
- DEAD/COPY/DELAY/INTERP/RECOMP wrappers;
- an oracle supplying all semantic answers;
- algebraic/oracle extensions appropriate to the algebrization audit.

A source-sensitive measure that changes drastically under semantically inert wrappers is suspect unless wrapper cost is explicitly part of the model.

## Failure conditions

Retire or downgrade a proposed hinge if:

1. it only proves a lower bound for a chosen representation of A;
2. the extracted object is asserted to exist but cannot be acquired within the charged model;
3. the argument works unchanged with an oracle replacing A;
4. it relies on finite experiments for an asymptotic theorem;
5. it assumes a canonical representation without paying for canonicalization;
6. it converts verification into construction for free;
7. it invokes a monotone/circuit/proof lower bound without a proved compiler into exactly that lower-bounded model.

## Highest-value next target

Construct, or prove impossible under an explicit compiler model, one typed rule

```
COMPILER(A,F; W,M) -> Q
```

such that:

1. A is an arbitrary polynomial-time exact SAT decider;
2. correctness uses A globally, not merely on the final restricted family;
3. Q depends intensionally on ordinary source information from A;
4. all source acquisition and transformation are charged;
5. replacing A by a SAT oracle breaks a named proof step;
6. Q either gives genuine fractional contraction or lies in a class with an unconditional superpolynomial lower bound.

This is the current LEAD priority.

## Coordination handoffs

### PROOF
Try to formalize GLOBAL-INTENSIONAL-GATE1 with exact machine/compiler interfaces. Determine which parts are genuine lemmas versus architectural requirements.

### RED
Attack the gate with semantic wrappers and oracle replacement. In particular, attempt to simulate every claimed source-dependent operation using a sufficiently strong oracle plus polynomial advice/preprocessing.

### RESEARCH
Search for existing nonrelativizing search-to-decision, minimization, meta-complexity, proof-complexity, and source-sensitive lower-bound constructions whose exact quantifier pattern resembles the desired compiler.

### WRITE
Keep this result labeled CANDIDATE unless PROOF establishes a formal theorem. Integrate into main2.tex/main3.tex only if it changes the dependency graph or priority statement.

## Status ledger

- P vs NP separation: **OPEN**
- Existing restricted monotone lower bounds: **PROVED/EXACT** only in their stated models
- Oracle-shadow necessity for the proposed architecture: **CANDIDATE / architecture constraint** pending formalization against the exact compiler interface
- GLOBAL-INTENSIONAL-GATE1: **CANDIDATE**
- SAT-native nonrelativizing compiler: **OPEN**
- Nonalgebrizing hinge: **OPEN**
