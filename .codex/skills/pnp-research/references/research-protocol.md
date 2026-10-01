# Research protocol and guard ledger

This reference expands the mandatory workflow in `SKILL.md`.

## 1. Formal claim card

Before attacking a serious claim, write a claim card:

```text
Claim ID:
Status before run:
Desired conclusion:
Exact quantifier prefix:
Input family:
Machine/model:
Resource measure:
SAME_REALIZATION IDs:
Minimum sufficient predecessor:
Known dependencies:
Known barriers:
Easy controls:
Wrapper controls:
Oracle replacement:
Algebraic-oracle replacement:
What would falsify it:
```

Do not begin with an informal slogan when a formal claim can be written.

## 2. Falsification ladder

Attack a new invariant in this order where applicable:

1. trivial satisfiable/unsatisfiable examples;
2. Horn / dual-Horn;
3. 2-SAT;
4. affine/Tseitin;
5. bounded treewidth;
6. independent products;
7. renaming / complementations;
8. padding / auxiliary-variable encodings;
9. DEAD / COPY / DELAY;
10. INTERP / RECOMP;
11. maximal semantic oracle;
12. algebraic oracle.

If a low-level attack breaks the claim, minimize the counterexample and stop trying to prove the stronger statement.

## 3. Arbitrary-algorithm transfer test

For every restricted structural lower bound, ask:

```text
What theorem forces an arbitrary exact SAT algorithm to instantiate
this object/resource in the same execution?
```

If the answer is only “all known algorithms do,” “the formula contains it,” or “the object exists,” the transfer is OPEN.

## 4. Acquisition accounting

Whenever the proof uses an object (Q,D,W,Pi,ho,ldots), separately account for:

- representation;
- construction/acquisition;
- verification;
- indexing;
- update;
- transport;
- storage;
- replay/recomputation;
- output.

Existential availability is not free acquisition.

## 5. Primitive-trace rule

Do not model a foreign algorithm (K) as a unit-cost escape.

Inline its real execution:
[
C_0^K\to C_1^K\to\cdots\to C_\ell^K.
]

A proposed battery/potential must be independently defined. The tautological quantity
[
\Phi^*(S)=\text{optimal remaining runtime from }S
]
is circular and cannot be a lower-bound invariant.

Optional failed shortcuts are not unavoidable cost because an arbitrary solver may skip them.

## 6. Relativization ledger

For every load-bearing arrow:

1. replace the ordinary machine by an oracle machine;
2. give the oracle every extensional semantic answer reasonably requested;
3. identify the exact proof line that fails or survives;
4. distinguish substantive failure from a definition that simply refuses oracle operations.

“Uses source code” is not by itself a nonrelativization theorem.

## 7. Algebrization ledger

If the argument survives ordinary oracle replacement only because it uses a finite internal computation, test whether low-degree/algebraic extension access restores the missing power.

Record the exact operation that algebraic access would need to emulate.

Nonrelativizing does not imply nonalgebrizing.

## 8. Quantifier audit

Write the complete prefix when adaptivity or oracle truth conditions matter.

Especially audit transformations of:
[
\exists\;\forall\;\exists
]
predicates when SAT YES and SAT NO semantics introduce witness/universal blocks.

Do not use qualitative class collapse to claim a quantitative near-linear simulation unless the compilation theorem supplies the required size/time bound.

## 9. Computational evidence

A table of finite ranks, runtimes, or counts is evidence about those instances only.

Good computational outcomes include:

- finding the first counterexample;
- identifying a stable algebraic identity worth proving;
- checking a symbolic derivation;
- measuring an exact finite rank/minor;
- verifying a hostile control;
- testing parameter bookkeeping.

Bad promotion pattern:

```text
holds for n <= 12
therefore asymptotically true
```

Never make that inference.

## 10. End-of-run record

Every substantive run should be reducible to:

```yaml
target:
mode:
quantifiers:
model:
same_realization:
primary_literature:
claim_attempted:
new_result:
status:
experiments:
hostile_controls:
relativization:
algebrization:
wrappers:
falsified:
open_arrows:
artifacts:
next_target:
```

This can appear in prose or LaTeX; the semantics should remain explicit.
