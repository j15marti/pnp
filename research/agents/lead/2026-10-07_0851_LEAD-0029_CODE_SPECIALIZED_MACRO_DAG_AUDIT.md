# LEAD-0029 — Code-specialized macro-DAG audit

Timestamp: 2026-10-07 08:51 PT
Agent: LEAD
Global status: **P versus NP remains OPEN.**

## Target

Continue PRE-A-MACRO-SHRINK1 after LEAD-0028. The surviving architecture must use the fixed code of a hypothetical polynomial-time exact SAT decider A non-black-boxly, but may not execute A on a current-scale SAT instance before genuine fractional contraction. LEAD-0028 showed that naive partial evaluation followed by Cook--Levin/Tseitin materialization retains the unknown exponent K.

This pass asks whether preserving the specialized computation as a DAG and quotienting repeated states can remove K.

## Literature check

Williams 2024 self-improvement remains the closest direct precedent: the theorem self-improves Circuit-SAT in parameter regimes above the P=NP endpoint, while extension all the way to the P=NP regime remains an explicit bottleneck/open direction.

Fortnow--Santhanam/Drucker-style instance-compression results remain warning signs rather than terminal contradictions under the assumption P=NP. Ogiwara--Watanabe sparse bounded-truth-table results likewise show that strong semantic pruning/compression has major consequences, but do not construct the required compiler.

## LOCAL-DAG-QUOTIENT-NOGO1 — PROVED/EXACT at stated generic-program scope

Consider a specialized deterministic polynomial computation with T=N^K useful transition states. A generic representation-level quotient may normalize semantically dead syntax, exact copies, delay chains, and interpreter scaffolding. However, there are polynomial computations whose T useful states have pairwise distinct local/source-dependent transition data.

Therefore an exact quotient whose only merge rule is equality of efficiently computed local structural/signature data has no generic guarantee of reducing the useful skeleton below T=N^K.

DEAD/COPY/DELAY normalization can remove wrapper-induced inflation but does not change this fact. A lossy fixed hash can force collisions, but hash collision does not certify continuation equivalence or equal SAT behavior.

This is **not** a lower bound on SAT and does not say every SAT decider has N^K irreducible states. It falsifies only the generic plan:

> specialize arbitrary A, then obtain a fixed-exponent compiler merely by generic DAG common-subexpression elimination, local bisimulation, or hashing.

## Finite audit — COMPUTATIONAL

For abstract useful skeletons T=N^K with K in {2,3,4}, wrappers DEAD_x8, COPY_x4, and DELAY_x8 inflated raw DAG sizes by constant factors. Exact wrapper normalization returned the T-node useful skeleton, whose measured exponent remained K. It never approached the target N^(2/3).

A separate 4096-state diagnostic used pairwise-distinct 128-bit state labels. Truncating to 8,12,16,24 bits produced 3840,1503,144,2 collisions respectively, but these were deliberately lossy and supplied no equivalence certificate. At 32/64 bits the finite sample happened to have no collision, which is not an exactness theorem. Exact 128-bit identity retained all 4096 states.

Raw result: results/wrapped_dag/2026-10-07_code_specialized_dag_audit.json

## WRAPPER-NORMALIZATION-BOUNDARY1 — PROVED/EXACT classification

Wrapper invariance has two distinct roles.

1. It is necessary hygiene: DEAD/COPY/DELAY/INTERP must not create a fake lower bound or fake state multiplicity.
2. It is not itself self-improvement: after quotienting representation artifacts, an arbitrary polynomial useful computation may still have exponent K.

Hence wrapper covariance can define the object to be compressed, but cannot supply the compression theorem.

## HASH-QUOTIENT-EXACTNESS1 — PROVED/EXACT guard

Let h be a noninjective hash of specialized computation states. Equality h(s)=h(t) does not imply equal future transition behavior, equal residual SAT function, or continuation equivalence. Thus replacing exact states by hash classes requires a separate collision-soundness theorem. Randomness/provenance cannot substitute for that theorem.

This is the code-DAG analogue of earlier HASH-MERGE1 and continuation-equivalence guards.

## Consequence

The surviving PRE-A-MACRO-SHRINK1 arrow is now narrower:

A successful compiler must exploit a **SAT-specific semantic self-improvement property of the code of A**. Generic program compression is insufficient; source-only/black-box Williams-landing shrinkage is already excluded by BLACKBOX-MACRO-NOGO1; naive time-unrolled specialization retains K by PARTIAL-EVAL-K-CARRY1.

A plausible next formal target is therefore:

### SAT-CODE-SELFIMPROVE1 — OPEN

Given the code of every hypothetical polynomial exact SAT decider A of unknown exponent K, construct, without executing a current-scale A call or materializing N^K steps, a SAT-specific ordinary representation/procedure whose recursively exposed SAT channels satisfy a Williams-landing fixed point independent of K.

The theorem must survive equivalent-program wrappers and must use something stronger than local execution-state identity. It may use the fact that A is correct on **all SAT instances**, not merely on the current source F.

This universal-correctness quantifier is the remaining source of structure not used by generic DAG compression.

## Proposed next attack

Exploit cross-input consistency of A:

1. choose a polynomially describable family of related SAT inputs F_z;
2. use the single fixed code A and its universal correctness on every F_z;
3. seek algebraic/functional identities among the specialized computations that force a compact common representation or fixed-exponent return map;
4. do not evaluate A(F_z) at current scale;
5. test 2-SAT, Horn, XOR/Gaussian, bounded-treewidth, padding, DEAD/COPY/DELAY/INTERP/RECOMP;
6. maximal-oracle test: identify precisely what code-level cross-input relation disappears when A is replaced by an opaque SAT oracle.

This is distinct from single-input trace/DAG compression: the candidate resource is a **cross-input code invariant forced by universal SAT correctness**.

## Status

- LOCAL-DAG-QUOTIENT-NOGO1: **PROVED/EXACT at generic-program scope**
- WRAPPER-NORMALIZATION-BOUNDARY1: **PROVED/EXACT classification**
- HASH-QUOTIENT-EXACTNESS1: **PROVED/EXACT guard**
- finite wrapper/hash audit: **COMPUTATIONAL**
- SAT-CODE-SELFIMPROVE1: **OPEN / LOAD-BEARING**
- PRE-A-MACRO-SHRINK1: **OPEN / LOAD-BEARING**
- P versus NP: **OPEN**
