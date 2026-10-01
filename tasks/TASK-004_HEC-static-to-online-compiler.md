# TASK-004 — Static-to-HEC Compiler

**Status:** OPEN / load-bearing transfer target  
**Project:** P vs NP / Heterogeneous-Epoch Challenge SAT (HEC-SAT)

## Goal

Given an arbitrary deterministic static SAT decider

[
A:{0,1}^*	o{0,1}
]

running in time (n^k), construct a model-preserving transformation that yields an HEC / chronogram-style solver whose:

- cut-state size,
- reread budget,
- post-challenge work,
- probe complexity,
- and recomputation cost

are quantitatively controlled by the resources of (A).

The same execution / SAME_REALIZATION discipline must be preserved.

## Why this is the next theorem

The HEC restricted-model core already proves:

1. **State/result separation:** with (K) independent payload bits and an (r)-bit free semantic side channel, exact future random-access recovery requires a worst-case cut state of at least
   [
   sge K-r.
   ]

2. **Free SAT answer corollary:** giving the current SAT decision bit away for free still leaves
   [
   sge K-1.
   ]

3. **Witness side information:** an explicitly transmitted (w)-bit witness/result string can remove at most (w) bits from the worst-fiber state requirement:
   [
   sge K-w.
   ]

4. **Multi-epoch direct sum:**
   [
   sge sum_e K_e-r
   ]
   in the declared no-reread model.

5. **Adaptive masking:** if (R_t) is fresh independent uniform and (b_t) is determined from prior history,
   [
   Y_t=R_toplus b_t
   ]
   remains conditionally uniform; heterogeneous gate computations can therefore alter timing/routing without generating entropy.

6. **Unresolved-selector amplification:** (u) unresolved selector bits choosing among (2^u) independent payload coordinates yield
   [
   sge 2^u-r,
   ]
   subject to the explicit entropy/input-size guard.

7. **Quantum robustness:** Nayak random-access-code bounds prevent asymptotic compression of the random-access state interface into (o(K)) qubits at constant decoding advantage.

These are restricted-model statements. They do **not** yet imply a lower bound for ordinary static SAT.

## Exact missing implication

[
oxed{
	ext{ordinary static SAT decider}
Longrightarrow
	ext{HEC/chronogram solver with controlled state and post-challenge cost}
}
]

This is the transfer that must be proved or falsified.

## Required attacks

Any proposed compiler must survive:

- full static input visibility;
- arbitrary random access to the input;
- rereading;
- recomputation;
- preprocessing;
- pointer jumping;
- memoization;
- compression;
- INTERP / RECOMP wrappers;
- DEAD / COPY / DELAY wrappers;
- auxiliary variables and alternate encodings;
- Gaussian/Tseitin controls;
- Horn / 2-SAT / bounded-treewidth controls;
- semantic-oracle replacement;
- algebraic-oracle replacement.

## Candidate subtargets

### A. Store-or-recover theorem

Seek a theorem of the form

[
S_{mathrm{cut}} + wQ_{mathrm{post}} + C_{mathrm{recompute}}
ge Omega(H)
]

for SAT-derived epoch payload (H).

### B. Pointer-chained staticization

Compile future challenge relevance into a static pointer-chasing dependency so that all data are present at time zero but useful access remains sequentially dependent.

### C. Result-oblivious state lower bound

Strengthen the model so the correct current SAT answer is free, yet future readiness still requires maintained information.

### D. Multi-epoch anti-batching

Use chronogram / online-communication techniques to prove costs add across epochs rather than collapsing to the cost of only the hardest epoch.

## Falsification criterion

If an arbitrary polynomial-time SAT solver can systematically bypass the HEC cut by reading, preprocessing, or recomputing future-relevant information at polynomial cost, record the exact bypass and treat it as a required feature of any future compiler.

## Non-goals

- Do not infer static SAT hardness from the restricted HEC lower bounds alone.
- Do not count exponentially many fresh random bits as a compact exponential lower bound.
- Do not replace true randomness with a short pseudorandom seed and then invoke cryptographic hardness.
- Do not use wall-clock deadlines as a P-vs-NP separator.
- Do not identify NDTM witness existence with deterministic internal state.

## Source artifact

See:

`research/explorations/random-challenge/2026-10-01_HEC-SAT_PROVED-CORE.tex`

## Deliverable

Produce either:

1. a rigorous compiler theorem with exact quantifiers and resource preservation; or
2. a concrete counterexample / bypass demonstrating why ordinary static SAT escapes the HEC boundary.

Either outcome is useful.
