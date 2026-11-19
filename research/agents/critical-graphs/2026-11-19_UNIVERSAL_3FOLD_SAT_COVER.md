# Strict-C native critical-source audit: universal three-fold SAT cover

2026-11-19, independent critical-obstruction constructor, run 4. **P vs NP remains OPEN.**

## PROVED: universal SAT covering theorem

For **every** finite conjunction (F) of original strict-C clauses (C(x_0,x_1,x_2)), each with three distinct variable **names**, one can construct in deterministic linear time a genuine 3-fold covering of its bipartite incidence graph which is **SAT**, regardless of whether (F) was SAT or UNSAT.

Replace each original variable (v) with the three copies ((v,s)) for (s\in\mathbb{Z}_3). Replace each original physical clause ((x_0,x_1,x_2)) with three *original* strict-C physical clauses, indexed by (t\in\mathbb{Z}_3):

```
C((x0,t),(x1,t+1 mod3),(x2,t+2 mod3)).
```

Assign the full witness (w(v,s)=s\in\mathbb{Z}_5). The three values in each lifted clause are a cyclic permutation of ((0,1,2)), which satisfies **the original C predicate** (R(a,b)\Leftrightarrow (b-a)\bmod 5\in\{1,3\}), (C=(R(x,y)R(y,z)R(z,x))\lor(R(x,z)R(z,y)R(y,x))). For every original incidence at port (p\in\{0,1,2\}), (t\mapsto t+p\bmod 3) is a bijection on the fibers. Hence this is genuinely a covering graph, not a replacement of the predicate or an arbitrary source modification. The cover has (3n) variables, (3m) physical clauses and (9m) incidence edges, with all copied variable names distinct within clauses. Construction, output, witness and full original-C verification all cost (O(n+m)) words and time on direct-index RAM (output length (O((n+m)\log(n+m))) bits).

**PROVED:** If the incidence graph of (F) is connected and (F) is UNSAT, this three-fold *cyclic* covering graph is connected. Indeed a 3-sheet regular (\mathbb{Z}_3)-cover of a connected base has one or three components. If three, each component projects isomorphically onto the base and restricts the explicit lifted satisfying assignment to an original satisfying assignment. This contradicts UNSAT. Connectedness of the cover alone does **not** imply base UNSAT.

**PROVED:** Covering maps cannot reduce incidence girth: a simple cycle in the cover projects to a closed nonbacktracking base walk containing a base cycle no longer than itself. Thus (g(\widetilde F)\ge g(F)). Strict improvement is not guaranteed.

**FALSIFIED:** UNSAT/physical clause-criticality automatically persists under arbitrary finite incidence coverings, even connected ones preserving local degrees and nondecreasing incidence girth. Our construction always turns UNSAT into SAT, improving the previously documented source-specific 2- and 5-sheet SAT covers to a uniform factor-three construction. It does not prove all covers SAT or rule out individually proven UNSAT-preserving transformations.

## Source-independent reproducible audit

Original R-predicate C and the independently implemented cyclic-three-consecutive-colors interpretation agree on **125/125** tuples, each accepting **30/125**.

| Base source | n,m | Base girth | 3-cover n,m | Lift girth | Lift incidence components | Original C witness |
|---|---:|---:|---:|---:|---:|---:|
| Critical native-25 UNSAT | 25,25 | 8 | 75,75 | 8 | 1 | 75/75 true |
| Seed20 native-150 UNSAT (prior complete two-solver check) | 150,176 | 10 | 450,528 | 10 | 1 | 528/528 true |
| Three-clause intrinsic UNSAT | 4,3 | 4 | 12,9 | 4 | 1 | 9/9 true |
| One-clause SAT control | 3,1 | forest | 9,3 | forest | 3 | 3/3 true |

The earlier native-25 proof tree was independently rechecked during this run: **1,046 nodes, 600 contradiction leaves**, all **25 single-physical-clause deletion witnesses**, **600 retained C evaluations true**, **25 deleted C evaluations false**, and incidence girth **8**. The native-150 source has girth **10** and prior two independent exhaustive UNSAT solver results, but it is *not* clause-minimal and has no static replayable 150-source UNSAT certificate. Clause 0 is redundant. Its SHA256 is `ecb0b31b1487f8747b582d97de26e2c77e4e1b5e173d89c4c86097e0fcd402a8`.

Additional **256** seeded arbitrarily ordered source formulas, seed **2026111906**, contributed **33,189** verified lifted original-C clauses without discrepancies.

Canonical lift source+witness JSON SHA256:
- native25 `27a155cf9eab79b38cda3fc01d90b9b9c5ac011a0e88131ba66bb5e7e01499fb`
- native150 `9fda2a3c4f1c82a650de27c70f285c7afef22382914731383274cac1cc838856`
- minimal3 `c22182512dad4576005e98b502e31ab344a249b02701b4c58794322df3c35f7a`
- one-clause `b50b54fe8c7179846268cbed3d92704ee65dbf90ef723c5b8b2dda859532850a`

Reproduction archive attached to run as `T5C_Critical_Universal_3Cover_Run4_20261119.zip`, containing sources, Python generators/verifiers, full witnesses, experiment results, prior native-25 independent checker and proof tree, and SHA256 manifest.

## Literature and criticality firewall

Read prior repository files: `2026-11-19_NATIVE_STRICTC_GIRTH10_150_TWOSOLVER_THETA_COVER.md` and `2026-11-19_CRITICAL_2LIFT_RIGIDITY_5LIFT_SAT_ESCAPE.md`. Also inspected user library `t5_strict_research.pdf` (November 18, 2026) for predicates and finite scope. General background: Gross & Tucker (1977), *Generating all graph coverings by permutation voltage assignments*, Discrete Mathematics 18:273-283, https://doi.org/10.1016/0012-365X(77)90131-5; Exoo & Goedgebeur (2019), *Bounds for the smallest k-chromatic graphs of given girth*, DMTCS 21(3), https://doi.org/10.23638/DMTCS-21-3-9. No research-priority claim.

**OPEN:** Extract and statically certify a physically clause-minimal native strict-C **incidence-girth-10 UNSAT** subformula from the 150/176 seed20 source; emit an original-C satisfying witness for deleting **every** physical clause, and a source-uniform UNSAT proof-acquisition procedure. This SAT-cover result is a limitation on naive covering constructions, **not** a time-space lower bound, a low-row resource reduction, or proof of P != NP.
