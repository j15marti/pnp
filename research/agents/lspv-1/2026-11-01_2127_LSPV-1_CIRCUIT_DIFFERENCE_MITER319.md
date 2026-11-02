# LSPV-1 CIRCUIT-DIFFERENCE-MITER319

**November 1, 2026, 21:27 PST (America/Los_Angeles)**. Formal Proof Lead. **PROVED/EXACT** elementary source-indexed miter and gate count under a declared architecture; **KNOWN THEOREM** general circuit equivalence via SAT and prior canonical cofactor-independence hardness; **COMPUTATIONAL** independent exhaustive checks. External mathematical review pending. **P versus NP OPEN.**

## Obstruction and four falsifiers

A source-authenticated short forward circuit C_F(a) evaluates F on a supplied original assignment a. Deciding whether some a makes C_F(a)=1 remains the SAT problem. Two adaptive residual states can share their current SAT answer, and even exact model counts, without having the same Boolean function under future pins. F1: two separate forward cofactor evaluators are mandatory to test exact equivalence, **FALSIFIED** by the shared-core miter. F2: equal sibling SAT labels and #SAT guarantee future equivalence, **FALSIFIED** on a single valid original. F3: a linear evaluation miter makes its existential Circuit-SAT query polynomial, **INVALID**. F4: a source-private gate count is a general SAT decision lower bound, **INVALID** under factoring, OBDDs, 2SAT, source-aware algorithms and other representations.

## Theorem 319A: same-original shared-core cofactor XOR miter

**Quantifiers.** For EVERY valid unpinned proper duplicate-free Döcker monotone 3-SAT-(2,2) original F with n original names and m=4n/3 original three-literal same-sign clauses, and EVERY original variable x, let f_b(z)=F(z,x=b) on the other n-1 original inputs. Malformed strings reject and noncanonical residual/circuit/Tseitin representations are not target-language children.

Precisely two source clauses contain +x and two contain -x. Let H_x be the conjunction of the other m-4 source clauses, preserving their original IDs. Let R^+_1,R^+_2 be the two source remainders obtained by deleting +x, and R^-_1,R^-_2 those obtained by deleting -x. Define A=R^+_1 AND R^+_2 and B=R^-_1 AND R^-_2. As Boolean functions on ALL z,

```
f_0(z) = H_x(z) AND A(z)
f_1(z) = H_x(z) AND B(z)
D_x(z) = f_0(z) XOR f_1(z)
       = H_x(z) AND ((A(z) AND NOT B(z)) OR ((NOT A(z)) AND B(z))).
```

Under a **strict source-private shared-core architecture** with fan-in-two AND/OR binary gates, free signed-wire unary NOT, no between-source-clause factoring and exactly one shared core H_x, the explicit gate constructor outputs

```
core H_x:       2(m-4) clause OR gates + (m-5) AND gates = 3m-13
remainders:     4 binary OR gates
A and B:        2 binary AND gates
XOR(A,B):       2 binary AND gates + 1 binary OR gate
output AND:     1 binary AND gate
TOTAL:          g_miter(F,x) = 3m-3 = 4n-3 binary gates.
```

Each gate has a source-clause provenance ID or a declared join identity; the output is acyclic. This is **exact only within this chosen literal clause-private circuit architecture**, not the unrestricted Boolean circuit minimum and not necessary work for an arbitrary correct decider. A completely duplicated two-cofactor source-private construction plus XOR would have 2(3m-9)+3 = 6m-15 gates in that more restricted architecture. For coherent p avoiding x, substitute the pins into the same source-derived DAG and optionally paid-simplify it; there are at most 3m-3 gates.

**Proof.** Under x=0 all negative-x source clauses are covered, while positive-x source clauses reduce to their two-literal remainders; under x=1 the reverse holds. Nonincident source clauses are identical in both branches. Factoring their common conjunction through Boolean XOR proves the identity for every complete z. The gate count follows from precisely four incident clauses and three original literals per clause. No assignment reconstruction, SAT-label oracle, exact minimizer or semantic key is used. QED.

**Corollary 319B: exact forward/reverse Shannon semantics.** F=(NOT x AND f_0) OR (x AND f_1); existential elimination is f_0 OR f_1; universal elimination is f_0 AND f_1. The siblings are equivalent under **all** future original-variable assignments iff D_x is UNSAT. One verified SAT assignment of D_x supplies a distinguishing future context. An exact complete UNSAT refutation of D_x permits a sound semantic merge. Neither the cofactor SAT labels nor their model counts alone imply D_x=0.

**Prior theorem, no novelty claim.** LSPV-2 COFACTOR-CONTINUATION-BARRIER319 (18:12 PST) ALREADY proved coNP-completeness of exact original-source variable independence, using valid canonical F disjoint-union Y6. The new 319A contribution is the explicit shared-core **3m-3 gate accounting** with full source provenance and same-original independent forward/circuit and both-label controls. It is a specialization of known combinational equivalence checking, NOT an unrestricted circuit lower bound.

## Same-original SAT/UNSAT and semantic-collision controls

F9 is the valid 9-variable 12-clause original with positive supports (156),(238),(135),(469),(247),(789) and negatives of (468),(167),(234),(358),(129),(579). Y6 is the valid 6-variable 8-clause original with positive supports (123),(145),(246),(356), negatives of (124),(136),(235),(456). F9 has 70 models, Y6 has 20 models and precisely 10 under either y1 assignment. H15=F9 disjoint-union Y6 is one valid original with 15 variables and 20 clauses, containing 1,400 models; pivot x10 is its copied y1.

| Same original; pivot | Coherent other-variable context | #SAT(x=0) | #SAT(x=1) | #D_x | Strict miter gates |
|---|---|---:|---:|---:|---:|
| Y6, x1 | none | 10 | 10 | 12 | 21 |
| F9, x1 | none | 40 | 30 | 46 | 33 |
| F9, x7 | x2=0,x3=0,x6=1 | 0 | 1 | 1 | 33 |
| H15, x10 | none | 700 | 700 | 840 | 57 |
| H15, x10 | F9 pins x1=0,x3=0,x5=1,x6=0,x7=0,x8=0 | 20 | 20 | 24 | 57 |
| H15, x10 | same F9 pins except x1=1 | 0 | 0 | 0 | 57 |

The SAME canonical F9 pinned SAT case has two complete original-source models; changing only the pinned x1 produces an UNSAT residual with zero models. Thus H15 has both current-label sibling SAT/UNSAT adversarial controls, AND equal-current-SAT/count siblings that are continuation-inequivalent. The F9 x7 row provides directly opposite-label siblings on one original with one common parent.

The standalone gate-DAG producer exhaustively checked all suffix assignments on all six rows, including 16,384 H15 original-suffix assignments and 57 original-ID-attributed gate evaluations per assignment. A separately written **no-producer-import independent verifier** passed **399,752 assertion groups**, including pointwise checking of every gate graph, disjoint tensor-product identities, 264 clause-pair S/U compatibility modes, 6,144 F9 assignment/complement identities, and six malformed structures. A separate Elias-gamma/fixed-width binary grammar test rejected **496/496** one-bit source-payload mutations and nine truncation/trailing errors. No U198/V198 certificate was freshly re-run in this scoped proof; prior authenticated labels are inherited, not evidence for these miter counts.

**Actual comparator (not native FLMV).** Original-source UP-DPLL on F9 with common x2=0,x3=0,x6=1 used one node/37 literal probes for UNSAT x7=0 and one node/96 probes for SAT x7=1. On H15 with SAT F9 pins, x10=0/1 used 3/4 nodes and 218/232 literal probes; with UNSAT F9 pins both x10 values used one node/34 probes. Gate counts, exhaustive row counts, DPLL literal probes and indexed-TM steps are NOT interchangeable.

## Paid work, quantifier gap and ARC/FLMV firewall

For input bit length N=Theta(m log n), source grammar/range/uniqueness/quotas and signed-pair recognition must be paid, as must original-ID clause read/index/head movement, gate DAG construction (O(m) word gate emissions and O(m log n) written gate-index bits in a growing-ID encoding), exact semantic-equivalence solving, gate and proof checking, any failed policy, switching, caching, replay, child-output bit requests, DELAY/COPY/RECOMP guests, and simultaneously live index/ancestor/guest/output/GE/proof/storage. A materialized gate DAG takes Theta(m log n) actual writable bits; an arbitrary decider need not materialize it. The exhaustive finite checker is exponential in free original variables. XOR of physical/logical states remains OFFLINE unless computed and charged.

An exact work recurrence for a declared adaptive controller is

```
W_D(z) = c_source+grammar+index+head(z)
       + sum_attempted [c_discovery+policy+failed+switch](z,policy)
       + c_gate+GE+matroid+proof+cache+replay(z)
       + c_output+child+bit-access+guest(z)
       + sum_executedChildren W_D(child).
```

Shannon branches strictly reduce the number of free original variables along each path, so termination is proven, but total executed children can still be exponential. Peak writable space counts actual simultaneous materialized records, not a sum of per-branch peaks. Exact full-source SAT witness or complete UNSAT evidence is a stronger optional output contract, NOT a mandatory recovered-value requirement for an arbitrary one-bit decider.

P=NP constructive target:
`exists D exists c,C>0 forall binary u: D(u)=[u in canonical SAT] AND W_D(u)<=C(|u|+1)^c`.

P!=NP unrestricted lower-bound target:
`forall correct total D forall c>=0 forall C>0 forall N0 exists valid original F: |F|>=N0 AND W_D(F)>C(|F|+1)^c`.

NEITHER follows from 319A. Even a single miter semantic-equivalence query requires sound acquisition, normalization of its noncanonical output, source-bit random access, actual guest execution and space. No power-short compiler for arbitrary unknown K,L or separate model-matched numerical FLMV contradiction is established. A fixed-order OBDD or after-answer constant circuit is not a universal lower bound.

## Project and literature audit; next falsifier

Read the verified 19:50 five-role SAT/Circuit-SAT directive FIRST; then the decision-only directive, integrated signed-hypergraph handoff, saturated-cycle terminal theorem, issue #3, AGENTS/CODEX/pnp-research skill, LSPV-1 MINZERO317/SHANNON318, LSPV-2 COFACTOR319 and PAIR322/GROUP323, LSPV-3 FRONTIER319, LSPV-4 F9-OBDD321/2SAT323 and LSPV-5 MATCHING280. Project GitHub searches: `cofactor equivalence`, `cofactor miter`, `variable independence`, `3m-3`, `cofactor XOR`. Separate github.com/openai search: `BDD`, `SAT`, `cofactor`; no source-specific M22 implementation was found, not a novelty proof. Primary web searches: Döcker's canonical NP-completeness (https://arxiv.org/abs/1912.08032), Lang/Liberatore/Marquis *Propositional Independence* (https://doi.org/10.1613/jair.1113), Bryant 1986 OBDD (https://doi.org/10.1109/TC.1986.1676819), Fortnow/Lipton/van Melkebeek/Viglas FLMV (https://doi.org/10.1145/1101821.1101822), and Tseitin equivalence circuitry. The central miter is well-known; the role-local source-quota accounting and hostile controls are verified incremental work.

**ADOPT**: original-clause provenance and exact paid continuation-difference miter. **REJECT**: free minimum circuit, equal model-count implies future equivalence, any representation-only universal hardness claim. **OPEN**: polynomial all-input aggregate decision work, universal arbitrary-A hereditary power-short Phi(A), strict numerical SAME-MACHINE FLMV transfer. Next useful test: use this miter with paid source-Krom/affine/log-treewidth SAT oracles on recognized subclasses and compare against direct source-aware DPLL/CDCL; failed policy work must be included.

All five existing task IDs/titles/enablement/staggers are unchanged. P versus NP OPEN.

END_OF_VERIFIED_REPORT::LSPV1::CIRCUIT_DIFFERENCE_MITER319::P_VS_NP_OPEN
