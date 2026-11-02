# LSPV-1 CIRCUIT-MINZERO-COFACTOR317

**2026-11-01 20:00 PST, America/Los_Angeles.** LSPV-1 Formal Proof Lead. **PROVED/EXACT elementary restricted theorems and coNP-completeness characterization, COMPUTATIONAL original-source controls, external referee pending. P versus NP OPEN.**

## Exact obstruction and falsifiers

**Universal obstruction:** A polynomial-size circuit evaluating F(x) for a *supplied* original-variable assignment does not decide the existential question "does any x make F(x)=1?". Syntactically minimizing the circuit *after the SAT answer is known* is not a free pre-decision operation. This run tests: (1) minimum equivalent circuit acquisition is always polynomial (a polynomial exact minimizer would imply P=NP); (2) F9's 35 clause-preserving gates are a general minimum (UNPROVED; only a restricted-model equality); (3) all Shannon cofactor paths remain hard even after source-authenticated simplification (FALSIFIED on an exact F9 SAT/UNSAT cofactor pair); (4) these restricted facts yield arbitrary-decider ARC/FLMV (UNPROVED).

## Theorem A: exact canonical MINZERO threshold

**Source:** every *valid, unpinned, duplicate-free proper* Döcker Monotone 3-SAT-(2,2) original F, with three distinct same-sign variables per clause, exactly two appearances in each polarity per variable, no duplicate source clauses; malformed binary strings reject.

Define mc(F) as the *minimum number of fan-in-two binary gates* in any circuit computing the exact Boolean function F(x) on every complete original-variable assignment. The fixed basis may include AND2/OR2/NAND2/XOR2, free input and 0/1 wires and free unary NOT/COPY, but no arbitrary source-dependent custom multi-input gate, and no free semantic oracle.

**Claim (PROVED/EXACT elementary):**

```
forall valid canonical F:    mc(F)=0  iff  UNSAT(F).
MINZERO22={valid canonical F with mc(F)=0} is coNP-complete.
```

**Proof.** Positive and negative clause counts are each 2n/3>0; m=4n/3. Therefore **both** 0^n and 1^n falsify F. UNSAT F computes constant 0, a free output wire, hence mc=0. Every circuit with zero binary gates computes a constant or a literal +/-x_i, even with unlimited unary NOT/COPY. A satisfiable canonical F cannot be constant 0; both endpoints reject so it cannot be 1, x_i or NOT x_i. Thus mc>=1. Membership is in coNP because the complement is malformed grammar (polytime checked) OR a satisfying full assignment (NP witness). For coNP hardness reduce from the complement of canonical SAT, which is coNP-complete because canonical SAT is NP-complete [1]. **Handle malformed strings explicitly:** map malformed input to the fixed certified canonical U198 UNSAT original, and well-formed input F to itself. This is a polynomial, total many-one reduction, and its output is always canonical valid. QED.

A polynomial-time algorithm returning a truly *globally minimum equivalent circuit* (or merely this zero-vs-positive gate threshold) on every canonical F implies P=NP. This is a conditional minimization-acquisition barrier and **not** a superpolynomial lower bound. No claim of novelty over general known circuit-equivalence / tautology complexity is made.

## Theorem B: honest source-gate bounds

Build a source-clause-ID-preserving acyclic evaluator C_F from the *same original input variables*: each positive three-literal clause uses OR2(OR2(a,b),c); each negative clause uses NAND2(AND2(a,b),c). A balanced AND2 tree over the m clause outputs uses m-1 gates. **Exactly 3m-1=4n-1 gates** and depth at most 2+ceil(log2(m)). This is a general *upper bound*. It is a tight lower bound only for the explicit clause-private/no-sharing/two-gates-per-three-literal and AND-combine-tree architecture. Writing the DAG, accessing source fields/index/head, and computing gate values are charged.

On F9 n=9, m=12, 70 models: **35 gates / depth 6**. All 9 input variables are essential (paired cofactor disagreements 46,44,52,50,40,52,40,38,40), so every unrestricted fan-in-two evaluator has >=8 binary gates by input-connectivity. **8 <= mc(F9) <= 35; the unrestricted exact minimum is unknown here.** This repeats/referees the earlier LSPV-4 F9-FORWARD-CIRCUIT-OBDD321, which also found fixed-order OBDD minimum/natural/maximum 52/66/80. No fixed OBDD or restricted gate measure implies arbitrary-decider time hardness.

## Theorem C: exact *same-original* forward/reverse cofactor minima

Use F9 with positive original clauses (156),(238),(135),(469),(247),(789) and negative clauses -(468),-(167),-(234),-(358),-(129),-(579). Apply *coherent original-variable pins* p={x3=0,x5=1,x6=0,x7=0,x8=0}. Source C2 forces x2=1, source C6 forces x9=1, and source C11 forces x1=0 when both are true; every other original clause is then satisfied. Thus **pointwise, with x4 free**:

```
F9|p = (NOT x1) AND x2 AND x9              exact minimum 2 binary gates
F9|p,x1=0 = x2 AND x9                      exact minimum 1 gate, 2 SAT completions
F9|p,x1=1 = 0                              exact minimum 0 gates, 0 completions
F9|p = (NOT x1 AND F9|p,x1=0) OR (x1 AND F9|p,x1=1).
```

The two/one/zero minima follow from 3/2/0 essential inputs and explicit AND constructions (free unary NOT). Eight complete assignments on the UNSAT x1=1 child each falsify an identified **ORIGINAL source clause**. Neither branch is a new canonical target original; it is an exact source-authenticated cofactor.

For *any* valid canonical F, the disjoint-union original G=F+shifted F9 is itself canonical. With the same five pins on its F9 component, the x1 sibling cofactor functions are exactly F(z) AND y2 AND y9 and constant 0; they agree iff F UNSAT. **Duplication firewall:** LSPV-2 COFACTOR-CONTINUATION-BARRIER319 already proved a stronger coNP-complete cofactor-independence problem on unpinned canonical originals via Y6; LSPV-1 COFACTOR-2SAT-CONTINUATION316 already proved a complete *restricted* polynomial 2SAT four-query guard. We do not claim novel general independence hardness or that an arbitrary SAT decider must perform these equivalence tests.

## Independent computation

The attached full producer and no-producer-import checker were executed in Python standard library. The independent checker passed **1,073,637 assertion units**. Complete original-clause versus explicit 2-input gate-DAG evaluation:

| Source | n | m | #SAT | gates | depth | counted full gate evaluations |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Y6 | 6 | 8 | 20 | 23 | 5 | 1,472 |
| F9 | 9 | 12 | 70 | 35 | 6 | 17,920 |
| F15 | 15 | 20 | 1,032 | 59 | 7 | 1,933,312 |

Independent direct cofactor checks for the valid original unions F+F9: 1,024/8,192/524,288 for Y6/F9/F15, all passed. F9 same-original SAT/UNSAT pins have 2/0 completions, eight complete source-indexed false-clause leaves on UNSAT; all **264** source clause-pair SS/SU/US/UU modes agree with exact enumeration (feasible 37/49/49/37), assignment/complement checks passed, six malformed original-source controls rejected. U198 UNSAT and V198 SAT original certificates are **inherited, not freshly rerun**. The gate-operation proxy is neither actual FLMV indexed-machine time nor a CDCL comparison.

## Fully charged all-input schema / missing proof

For a **single computable** controller D and executed source-indexed state z, let E(z) contain only children actually evaluated. Charge c(z) for full grammar/authentication, all source/bit/index/head reads, circuit build and gate/child output, exact semantic quotient acquisition/checking, failed policies and switching, 2SAT/Horn/XOR/GE/matroid/proof work, cache/replay, guest DELAY/COPY/RECOMP and restoration; c_edge(z,y) additionally charges output-bit translation and child access.

```
W_D(z) = c(z) + sum_{y in E(z)} [ c_edge(z,y) + W_D(y) ].
S_peak(F) = max_time(total simultaneously live writable ancestor/index/head,
                   gate/cofactor table, proof, selector/cache, output, guest).
```

Shannon SAT(z)=SAT(z|x=0) OR SAT(z|x=1), with both branches needed to establish UNSAT unless a separate complete refutation is obtained. Each exact-fallback recursive branch pins a new free original variable, giving decreasing f despite signed delta increases, **but total executed children may be exponential**. All failed choices and DAG equality tests are paid; semantic representatives are never free. An explicit SAT witness or complete UNSAT certificate is a stronger output contract and must be verified/charged separately. XOR of logical states is OFFLINE unless charged. Tseitin/circuit cofactors are noncanonical, not hereditary target children without a paid verified reencoder.

**OPEN**: exists ONE uniform D, c,C>0, for ALL binary s, correct canonical-language decision in W_D(s)<=C(|s|+1)^c, or alternatively a genuine fully charged arbitrary-correct-decider A->Phi(A) hereditary power-short unknown-exponent contraction with a separately proved **strict same-machine** FLMV transfer. Restricted circuit minimum, state count, certificate size, or post-UNSAT constant circuits prove neither.

## Prior art, searches, status

Read first verified 19:50 full five-role SAT/Circuit-SAT redirect; also decision-only handoff, integrated 01:48 handoff and 01:44 delta-zero theorem, issue #3, AGENTS/CODEX/pnp-research skill. Project GitHub searched `cofactor equivalence`, `Shannon expansion`, `minimum gate`, `minimization`; found LSPV-2 COFACTOR319, LSPV-1 2SAT316, LSPV-4 F9 forward/OBDD321, LSPV-3 HWB-OBDD68, MAIN Tseitin46/47. Primary web searched Döcker, Bryant, formula-variable independence, FLMV and circuit equivalence; separate github.com/openai search `BDD`/`circuit sat` found general Lean SAT/circuit formalizations but no source-matched theorem. Absence is not a novelty argument. Scientific status: new exact specialized threshold characterization and same-source cofactor minima; all-input P versus NP remains OPEN, external referee pending.

**Next falsifier:** seek a source-authenticated exact cofactor simplification guard beyond the residual-2SAT subclass whose *acquisition and proof checking* remain polynomial without assuming a best-policy or semantic oracle.

### Primary references

[1] Döcker, *Monotone 3-SAT-(2,2) Is NP-Complete* (2019), https://arxiv.org/abs/1912.08032.  
[2] Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE TC 35 (1986), DOI 10.1109/TC.1986.1676819.  
[3] Lang, Liberatore, Marquis, *Propositional independence: formula-variable independence and forgetting*, JAIR 18 (2003), DOI 10.1613/jair.1113.  
[4] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), DOI 10.1145/1101821.1101822.

END_OF_VERIFIED_REPORT::LSPV-1::CIRCUIT-MINZERO-COFACTOR317::P_VS_NP_OPEN
