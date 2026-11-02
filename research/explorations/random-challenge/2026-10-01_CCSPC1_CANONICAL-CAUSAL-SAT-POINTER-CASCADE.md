# CCSPC-1 — Canonical Causal SAT Pointer Cascade

**Timestamp:** 2026-10-01 11:26 PT  
**Status:** FORMALIZED COMPONENT / CANDIDATE auxiliary model.  
**Global status:** P versus NP remains OPEN.

## 1. Purpose

CCSPC is a reusable component for the CRS-PPC branch.

It captures the following idea:

- a deterministic computation follows one realized path through a very large family of SAT instances;
- the next SAT instance depends on the canonical result of the current one;
- fresh exogenous randomness arrives only after the current result exists;
- that fresh randomness selects which part of the current computation becomes relevant and/or which next codebook entry is chosen;
- the resulting path is sequentially adaptive even though the latent codebook may have exponentially many possible continuations.

The component is **not** based on the claim that an NDTM must enumerate every latent branch. That claim is false for ordinary nondeterminism.

## 2. Uniform codebooks

For level (i), let

[
C_i:{0,1}^{ell_i}	o {	ext{finite }k	ext{-CNF formulas}}
]

be a uniform codebook generator.

Given an index (pin{0,1}^{ell_i}), the formula

[
Phi_i=C_i(p)
]

must be constructible with all costs charged.

A literal exponentially large lookup table with free constant-time access is not permitted unless explicitly modeled as advice/oracle access.

## 3. Canonical SAT result

For each formula (Phi), define a deterministic canonical result

[
operatorname{CanSAT}(Phi).
]

One concrete choice is

[
operatorname{CanSAT}(Phi)=
egin{cases}
0Vert 0^m,& Phi	ext{ is UNSAT},\
1Vert operatorname{LexMaxSAT}(Phi),& Phi	ext{ is SAT}.
end{cases}
]

The exact canonicalization may be changed in later work, but it must satisfy:

1. **Uniqueness:** every formula has one prescribed output;
2. **Semantic correctness:** the output determines the correct SAT status;
3. **Witness-choice independence:** different satisfying assignments do not define different legal next states.

The role of canonicalization is to block the easy escape in which an NDTM chooses whichever satisfying witness yields the most convenient downstream pointer.

Canonicalization does **not** by itself prove hardness.

## 4. Exogenous source

Let

[
G=(R_1,R_2,ldots),qquad
R_tstackrel{mathrm{i.i.d.}}{sim}mathrm{Bernoulli}(1/2)
]

be the CRS-PPC causal source.

At level (i), only after the current canonical SAT result has been produced is a fresh block

[
B_i=(R_{	au_i+1},ldots,R_{	au_i+b_i})
]

captured, where (	au_i) is the charged completion time of the relevant current computation.

The Fresh Snapshot Lemma applies when (	au_i) is a causal stopping time.

## 5. Delayed audit and next-pointer rule

Let

[
T_i=operatorname{CanSAT}(Phi_i).
]

The fresh block (B_i) is converted into an audit selector

[
q_i=A_i(p_i,T_i,B_i).
]

The audit asks for a value

[
V_i(q_i)
]

associated with the just-completed level-(i) computation.

Examples include:

- a value at a node of a dependency DAG;
- an intermediate canonicalization bit;
- a derived pointer-state value;
- a restricted-computation value that could have been stored or must now be recomputed.

The answer to the delayed audit is denoted

[
Y_i=V_i(q_i).
]

The next pointer is

[
oxed{
p_{i+1}=F_i(p_i,T_i,B_i,Y_i).
}
]

The next formula is then

[
oxed{
Phi_{i+1}=C_{i+1}(p_{i+1}).
}
]

Thus one realized trajectory has the form

[
p_i
	o
Phi_i
	o
T_i
	o
B_i
	o
q_i
	o
Y_i
	o
p_{i+1}.
]

## 6. Full cascade

For (z) levels,

[
p_1
	o Phi_1
	o T_1
	o B_1
	o q_1
	o Y_1
	o p_2
	o cdots
	o p_z
	o Phi_z
	o T_z.
]

The latent number of possible paths may be enormous. If level (i) has (2^{b_i}) possible fresh blocks, the latent trajectory count can be as large as

[
2^{sum_i b_i}.
]

This semantic branching count is **not** itself a runtime lower bound.

Only one path is realized.

## 7. Primary resource target

The purpose of the delayed audit is to make the solver face a STORE-versus-RECOMPUTE obligation after the current challenge becomes known.

The candidate charged resource is

[
oxed{
mathcal R_{
m CCSPC}
=
S_{
m data}
+
S_{
m pointer}
+
wQ_{
m reread}
+
C_{
m recompute}
+
C_{
m sequential}.
}
]

A successful lower-bound theorem would force a large value of (mathcal R_{
m CCSPC}) for every correct realization in the declared model.

## 8. Why canonicalization matters

Without canonicalization, a satisfiable (Phi_i) may have witnesses

[
w_i^{(1)},w_i^{(2)},ldots.
]

An NDTM could choose whichever witness induces the easiest continuation.

Canonicalization replaces the relation

[
exists w:Phi_i(w)=1
]

with a unique required transition value

[
T_i=operatorname{CanSAT}(Phi_i).
]

This removes witness-choice freedom from the pointer rule.

It does **not** prevent an NDTM from executing the same deterministic canonicalization procedure used by the DTM.

Therefore CCSPC must never be justified by saying:

> the DTM follows one branch while the NDTM must follow all branches.

For the same input and resources,

[
DTIME(t)subseteq NTIME(t).
]

An NDTM may always simulate the DTM.

## 9. Complexity-class guard

For polynomially many levels, polynomial-size formulas, and polynomial-time-uniform codebooks:

- arbitrary witness transitions are compatible with NP-style stagewise guessing;
- exact adaptive SAT-bit transitions naturally resemble (P^{NP});
- canonical optimization/search transitions naturally resemble (FP^{NP})/OptP-style computation;
- under the counterfactual (P=NP), polynomially many adaptive NP-oracle computations collapse to polynomial time.

Therefore a polynomial-depth CCSPC does **not** become NEXP merely because its latent branch tree is exponential.

### NEXP regimes

NEXP can arise legitimately only after changing the resource scale, for example:

1. a succinct description represents an exponentially large SAT object;
2. the realized cascade depth is exponential;
3. the required output explicitly ranges over exponentially many trajectories.

These are separate exponential-resource constructions, not consequences of ordinary polynomial-depth branching.

## 10. Alternation guard

If the task is strengthened from one realized random trajectory to correctness for **every** challenge sequence, the quantifier pattern begins to resemble

[
orall B_1exists T_1
orall B_2exists T_2
cdots.
]

Polynomially many genuine alternations are structurally closer to alternating polynomial time / PSPACE than to NP.

True randomness itself is not a universal quantifier; this is only a separate strengthened control problem.

## 11. Exact role of (G)

(G) contributes:

- unpredictability of future challenges;
- causal ordering;
- anti-preselection of future audit locations.

(G) does **not** contribute:

- more than (O(T)) fresh entropy in (T) elapsed time at constant rate;
- an unconditional superpolynomial lower bound by itself;
- an obligation for nondeterminism to enumerate every latent path.

A private OTP/permutation derived from (G) is only a challenge-map transformation and adds no independent entropy.

## 12. Hostile controls

Every CCSPC proposal must survive:

1. **DTM simulation:** an NDTM can run the DTM verbatim.
2. **Stagewise witness guessing:** if (T_i) is not canonical, nondeterminism may choose a convenient witness.
3. **Static reread:** after a challenge is revealed, one random-access reread may answer it unless the dependency itself is expensive.
4. **Pointer jumping:** precomputed doubling/composition tables may shortcut long pointer chains.
5. **Memoization:** repeated subcomputations may collapse.
6. **Group compression:** simple shift/permutation histories may compress to one group element.
7. **Full-input staticization:** revealing all future randomness can enable preprocessing.
8. **Easy controls:** Horn, 2-SAT, bounded treewidth, affine/Tseitin, and formulas with compact summaries.
9. **Semantic oracle:** current SAT answers may be supplied for free.
10. **Algebraic oracle:** algebraically encoded intermediate relations may be supplied directly.
11. **DEAD/COPY/DELAY/INTERP/RECOMP wrappers.**
12. **Input-size normalization:** explicit books or payloads must be charged at their true size.

## 13. Immediate theorem targets

### CCSPC-A — Canonical-Transition Anti-Guessing Theorem

Find a canonical response relation for which, after the fresh challenge is known, producing the unique valid response cannot be reduced to ordinary stagewise NP witness guessing.

This must not contradict the fact that an NDTM can simulate any deterministic procedure used by the DTM.

### CCSPC-B — Delayed-Audit Store/Recompute Theorem

For an explicit dependency-DAG family,

[
mathcal R_{
m CCSPC}ge L(n)
]

even when the current SAT decision bit is free.

### CCSPC-C — Anti-Batching / Sequentiality Theorem

Prove that fresh (B_i) arriving only after (T_i) prevents preprocessing or batching from computing the future pointer sequence substantially faster than resolving the required dependency chain.

### CCSPC-D — Staticization Theorem

Convert the online/random cascade into a solver-independent fixed problem without exposing future challenge information in a way that destroys the lower bound.

### CCSPC-E — Static-SAT Compiler

For every hypothetical deterministic exact SAT decider

[
Ain TIME(N^k),
]

derive a SAME_REALIZATION CCSPC computation with fully charged preprocessing, state, reread, recomputation, and sequential costs.

This is the load-bearing bridge to ordinary SAT.

## 14. Relationship to CRS-PPC

CCSPC is a **component inside CRS-PPC**, not a replacement for it.

CRS-PPC supplies:

- the causal source (G);
- stopping-time freshness;
- state/result separation;
- STORE/TRACK/REREAD/RECOMPUTE accounting;
- staticization and arbitrary-algorithm bridge targets.

CCSPC supplies:

- a canonical SAT-dependent pointer transition;
- a growing/stacked codebook of SAT instances;
- delayed random auditing of the preceding computation;
- a precise separation between one realized path and exponentially many latent paths.

## 15. Strict status

**PROVED/EXACT guards**
- only one path is realized;
- exponential latent branching alone is not a runtime lower bound;
- an NDTM can simulate the DTM;
- polynomially many explicit SAT stages do not imply NEXP;
- canonicalization removes arbitrary witness-choice freedom but does not by itself create hardness.

**CANDIDATE**
- canonical SAT pointer cascade;
- delayed audit forcing STORE/RECOMPUTE;
- anti-batching from post-result random challenges.

**OPEN / load-bearing**
- CCSPC-A through CCSPC-E;
- a solver-independent static lower bound;
- a nonrelativizing/nonalgebrizing final hinge.

## 16. Short reusable definition

> **CCSPC:** A polynomial-depth causal computation in which a uniform codebook maps the current pointer to a SAT instance, a unique canonical SAT result is computed, fresh post-result randomness selects a delayed audit of the just-completed computation, and the audit response together with the canonical result and fresh randomness determines the pointer to the next codebook. The intended lower-bound resource is STORE/TRACK/REREAD/RECOMPUTE/SEQUENTIAL work, not the number of latent branches.

