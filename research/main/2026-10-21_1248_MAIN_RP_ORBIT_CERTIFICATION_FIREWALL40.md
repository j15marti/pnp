# RP-ORBIT-CERTIFICATION-FIREWALL40

**Timestamp:** 2026-10-21 12:48 Asia/Seoul  
**Scope:** P-vs-NP two-route synthesis plus a separate P-vs-RP proof DAG.  
**Status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Recovered state and publication boundary

This run read the current standalone proof-chain summaries main12.tex
(MCSP/MKTP), main13.tex (ARC/FLMV), and main14.tex (RP diagnostics), the
latest GitHub commits, and the shared fallback Doc. Root main.tex was
restored externally at commit fc06a7d; this run did not edit it.

The newest accessible :36 artifact is the short RP-ORBIT-SYMMETRY5 handoff
at commit 8de1af4. It reports a restricted orbit-enumeration theorem, a
coNP-complete acceptance-symmetry test, and 204,917 passing assertions, but
the detailed report/code/raw are still marked pending. The shared Doc still
ends at the older ARC-HEREDITARY-SCOPED10 handoff. Consequently this report
does not claim to have reviewed the unavailable :36 proof body. Instead it
independently reconstructs the exact orbit theorem and a minimal hardness
reduction, then adds the language-invariance firewall.

Current PNP proof-chain summaries make no load-bearing promotion:

- MMW streams an existing ordinary MKTP target with short Sigma_3-SAT
  queries; it does not build the target.
- CHMY is a source-specific randomized one-way-input/one-work-tape lower
  bound, not an unrestricted or nonuniform circuit lower bound.
- OPS is a cofinal nonuniform GapMCSP promise magnification theorem.
- FLMV is a deterministic random-access simultaneous time-space endpoint.
- The deterministic total both-label SAT-to-ordinary-MKTP target and the
  all-input hereditary charged ARC contractor remain missing.

## 2. Mechanisms proposed before the literature pass

1. Promised orbit enumeration: if accepting behavior is constant on a
   polynomially enumerable orbit partition, test one representative per
   orbit.
2. Certification hardness: reduce Circuit-UNSAT to invariance under one
   fixed coordinate swap while every resulting verifier recognizes Sigma*.
3. Seed-permutation control: show that input-dependent polynomial-time
   bijections preserve RP semantics and density while changing fixed
   acceptance geometry.
4. Cross-route firewall: keep orbit, rank, hashing and hitting arguments
   verifier-specific unless they yield a uniform simulator of the language.

Mechanisms 1 and 2 are proved below and independently tested. Mechanism 3 is
proved as a control.

## 3. Primary-source model check

- Gill, *Computational Complexity of Probabilistic Turing Machines*, SIAM
  J. Comput. 6(4), 1977, DOI
  [10.1137/0206049](https://doi.org/10.1137/0206049), supplies the
  probabilistic-Turing-machine setting. Here RP means zero acceptance on NO
  inputs and acceptance probability at least 1/2 on YES inputs.
- MMW, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong
  Separations*, STOC 2019, DOI
  [10.1145/3313276.3316396](https://doi.org/10.1145/3313276.3316396),
  gives its one-pass search-MCSP/MKTP streaming interfaces. An orbit
  representative theorem is not an MMW lower bound or target constructor.
- CHMY, STACS 2021, DOI
  [10.4230/LIPIcs.STACS.2021.23](https://doi.org/10.4230/LIPIcs.STACS.2021.23),
  fixes the one-way-input/one-work-tape model. Orbit certification does not
  transfer to that machine lower bound.
- OPS, Theory of Computing 17(11), 2021, DOI
  [10.4086/toc.2021.v017a011](https://doi.org/10.4086/toc.2021.v017a011),
  uses nonuniform circuits and a GapMCSP promise.
- FLMV, JACM 52(6), 2005, DOI
  [10.1145/1101821.1101822](https://doi.org/10.1145/1101821.1101822),
  is the deterministic random-access SAT time-space endpoint. An RP
  verifier's orbit structure supplies no ARC successor.

## 4. Exact promised-orbit derandomization theorem

Let a uniform RP machine M use r(n) random bits. For each input x, let the
tape set be partitioned into orbits O_1(x),...,O_m(x).

Assume:

1. m is polynomially bounded in |x|;
2. a deterministic polynomial-time procedure outputs one representative
   rho_j(x) from every orbit;
3. M(x,rho) is constant on each orbit;
4. all representative generation and simulations are charged.

### Theorem

Under these promises, the language recognized by M is in P.

### Proof

Generate all representatives and accept iff some M(x,rho_j(x)) accepts.
On a NO input every random tape rejects, so every representative rejects. On
a YES input some tape accepts; constancy on its orbit implies that orbit's
representative accepts. The number of simulations and their individual
runtimes are polynomial. This is an exact deterministic decision procedure.

The theorem is useful but restricted: it requires a proved uniform orbit
cover. It does not provide a generic procedure to discover or certify such a
cover for arbitrary verifier circuits.

## 5. Certification hardness inside one trivial language

Define SWAP-SYM: given a Boolean circuit F(q,a,b,z), decide whether
F(q,a,b,z)=F(q,b,a,z) for every assignment. This property is in coNP: a
violating assignment is a polynomial witness for non-symmetry.

Given an arbitrary Boolean circuit C(z), construct

F_C(q,a,b,z) = q OR (a AND NOT b AND C(z)).

### Theorem

SWAP-SYM is coNP-complete. Moreover, interpreting F_C as the random-tape
acceptance predicate of a verifier V_C, every V_C recognizes the same
trivial language Sigma* with RP success probability at least 1/2.

### Proof

If C is unsatisfiable, the second disjunct is always false and F_C=q, so the
swap fixes the predicate. If C(z)=1 for some z, then at q=0,a=1,b=0 the
original value is 1 and the swapped value is 0. Therefore F_C is
swap-invariant iff C is unsatisfiable. The mapping is polynomial, so
Circuit-UNSAT gives coNP-hardness.

For every source input, the half of all random tapes with q=1 accept,
regardless of C; there are no NO inputs because the recognized language is
Sigma*. More exactly, if C has s satisfying assignments among 2^k, then

Pr[V_C accepts] = 1/2 + s/(8*2^k).

Thus a coNP-complete verifier-geometry certification problem is present even
though the language has the one-state deterministic accept-all decider.
Certification hardness is not a language lower bound and proves neither
P!=RP nor P=RP.

## 6. Seed-permutation control

For any polynomial-time computable bijection pi_x on the random tapes,
define M'(x;r)=M(x;pi_x(r)). Bijection preserves the exact number of
accepting tapes, hence the language and one-sided RP error. A fixed hitting
list for M transfers only as the generally input-dependent list
pi_x^{-1}(H). Therefore fixed tape geometry, orbit names and seed lists are
not semantic invariants of an RP language.

## 7. Reproducible audit

The checker exhausts every Boolean truth table C on up to four variables:

- 65,814 truth tables;
- 8,405,584 original/swapped tape pairs;
- exact density and symmetry checks for every table;
- acceptance-count preservation under a deterministic XOR permutation;
- 20,000 seeded random orbit partitions validating representative simulation;
- 10,000,659 instrumented assertions, zero failures.

Raw SHA-256:
c671544472ab006fb3ff229111909515b7a41e3e8f8d51d930c8433775917f41.
The exhaustive audit checks implementation and boundary cases. The written
reductions and proofs establish the asymptotic theorems.

## 8. Separate proof DAGs

### P versus NP

**ESTABLISHED:** source-specific MMW, CHMY, OPS and FLMV theorems only in
their stated models; exact conditional ARC recurrence arithmetic; exact
restricted low-width boundary joins.

**CONDITIONAL:** SAT -> charged deterministic total both-label R_k ->
ordinary MKTP threshold -> MMW streamer -> same-machine SAT DTISP -> FLMV,
conditional on the missing totalizer, thresholds and resource transfer.

**OPEN:** the total ordinary target with no random oracle/source pointer/full
side table; the all-input hereditary solver-dependent ARC successor; the
COMPACT-HISTORY20 single exists-W-forall-i subpolynomial witness circuit.

**RETIRED:** fixed digests, orbit/rank/hitting geometry, proof-system size,
physical counts, output materialization and finite experiments as
unrestricted SAT lower bounds.

### P versus RP

**ESTABLISHED:** P subseteq RP subseteq NP; a proved uniform polynomial orbit
cover derandomizes that verifier; SWAP-SYM is coNP-complete even among
acceptance circuits for Sigma*; input-dependent tape permutations preserve
RP semantics and density.

**CONDITIONAL:** a uniform polynomial-time hitting/orbit/PRG constructor for
every RP machine, with complete simulation cost and no oracle leakage, would
give P=RP.

**OPEN:** either an explicit language in RP outside every deterministic
polynomial-time machine, or a uniform deterministic simulation of every RP
machine.

**FALSIFIED/RETIRED:** SAT in RP => P=RP; verifier-specific hitting or
symmetry hardness as a language lower bound; randomized black-box,
relativizing, proof-system or finite evidence as an unrestricted separation.

## 9. Single highest-value next experiment per active route

- **:00 PNP/MKTP:** instantiate one candidate total target on matched SAT and
  UNSAT sources and compute indexed ordinary KT including source acquisition,
  state, index decoding and runtime; require a proved gap at p>=log M.
- **:24 PNP/ARC:** serialize one high-width, global, nonaffine semantic child
  relation and replay it on paired SAT/UNSAT parents while charging discovery,
  rejected children, source rereads, ancestors and peak workspace.
- **:12 RP separation:** take the proposed candidate language, replace its RP
  verifier by a q-OR gadget, and show the claimed obstruction survives an
  easy deterministic language decider; if it does not, retire the arrow as
  verifier-specific.
- **:36 RP derandomization:** produce an explicit uniform orbit generator and
  representative enumerator for a nontrivial verifier family, then audit
  completeness, invariance certification, coin length and total runtime.

No automation, role, or schedule was changed.

