# CLEANCORE-EXT1 — Extension-Map Structure After Low-Degree Mediator Elimination

**Date:** 2026-10-05  
**Repository:** `j15marti/pnp`  
**Global status:** **OPEN. P versus NP remains open.**

This note extends CLEANCORE-EVAL1 from complete chain-state compatibility to the stronger partial-extension response map.

For an eliminated clean-core chain CSP (F), define

[
operatorname{EXT}_F(ho)=1
]

iff the partial chain-state restriction (ho) extends to a complete satisfying assignment.

Each chain challenge coordinate has eight possibilities:

[
{*}cup S,
]

where (*) means unassigned and (S) is the set of seven satisfying states of a type-1 chain.

The complete response table therefore has (8^k) possible challenge strings for (k) chains.

The purpose of this experiment is not to infer a lower bound from one representation. It is to compare multiple exact finite structural/evaluator diagnostics on the **same instances** and hostile controls.

---

## 1. Families

Five families were tested.

### CLEAN

Random low-degree externally mediated cores:

- (k) type-1 chains;
- (2k) outside mediators;
- mediator degree (2,3,) or (4);
- both mediator polarities occur;
- every mediator clause couples literals from two distinct chains;
- mediators are then eliminated exactly using MED-ELIM1.

### 2SAT control

Random 2-CNF constraints on one representative bit of each chain-state variable.

The 7-state chain alphabet remains in the challenge interface, but the cross-chain constraint depends only on the chosen representative bit.

### PATH control

Adjacent-chain 2-CNF constraints only. The primal graph is a path and hence has treewidth/pathwidth 1.

### INDPROD control

Independent disjoint chain pairs. This tests direct-product structure without global interaction.

### XOR control

Random low-density linear equations over (mathbb F_2) on one representative bit per chain.

Extension is evaluated by canonical Gaussian elimination. This is the mandatory control showing that nontrivial continuation/communication structure does not imply hard centralized computation.

---

# 2. Exact finite metrics

For every generated instance the experiment records:

1. primal interaction graph edge count;
2. **exact treewidth** by complete elimination-order search;
3. **exact pathwidth / vertex-separation number** by subset dynamic programming;
4. exact balanced edge-expansion value at a floor-half cut;
5. reduced ordered **8-ary MDD** size for the partial-extension function;
6. MDD maximum layer width;
7. for (kle6), maximum over balanced cuts of:
   - number of distinct partial-extension communication rows;
   - (mathbb F_2) rank of the partial-extension communication matrix;
   - matrix density.

For MDDs, only a finite collection of variable orders is searched:

- natural order;
- ascending degree;
- descending degree;
- random sampled orders.

Thus the reported MDD number is an upper bound on the optimal reduced ordered MDD size, not a minimum over all orders.

Communication cuts are exhaustive over balanced partitions for (kle6).

Three deterministic seeds were used for each family at each (k=4,5,6,7).

Raw results:

`results/source_reduction/2026-10-05_clean_core_extension_profiles.csv`

Reproducible script:

`experiments/source_reduction/clean_core_extension_profiles.py`

---

# 3. Clean-core finite profile

Averaging the three CLEAN instances:

| (k) | mean treewidth | mean pathwidth | mean balanced expansion | mean best sampled EXT-MDD nodes | mean best MDD width |
|---:|---:|---:|---:|---:|---:|
| 4 | 3.00 | 3.00 | 2.00 | 50.7 | 30.0 |
| 5 | 4.00 | 4.00 | 3.00 | 103.0 | 47.0 |
| 6 | 5.00 | 5.00 | 3.00 | 369.0 | 163.7 |
| 7 | 5.67 | 5.67 | 3.89 | 599.0 | 252.0 |

Over these four sizes, the mean best-sampled MDD node counts fit approximately

[
1.55(2.38)^k,
]

with finite log-linear (R^2approx0.973).

This is **COMPUTATIONAL finite evidence only**. No asymptotic claim is made.

---

# 4. Partial-extension communication profile

For (kle6), every balanced variable cut was examined and the cut with maximal (mathbb F_2) rank was retained.

For CLEAN:

| (k) | mean distinct rows | mean (mathbb F_2) rank |
|---:|---:|---:|
| 4 | 34.3 | 30.3 |
| 5 | 51.3 | 47.3 |
| 6 | 200.7 | 151.7 |

For (k=6), a balanced side has

[
8^3=512
]

possible partial challenges.

Thus the finite CLEAN examples retained hundreds of distinct continuation profiles across a balanced cut.

Again this is a communication/representation fact, not a centralized runtime lower bound.

---

# 5. Hostile controls at (k=6)

Averaged over the same three-seed protocol:

| family | treewidth | pathwidth | mean EXT-MDD nodes | mean MDD width | mean distinct rows | mean (mathbb F_2) rank |
|---|---:|---:|---:|---:|---:|---:|
| CLEAN | 5.00 | 5.00 | **369.0** | **163.7** | **200.7** | **151.7** |
| 2SAT | 2.33 | 2.33 | 6.0 | 1.33 | 4.0 | 3.0 |
| PATH | 1.00 | 1.00 | 8.0 | 2.0 | 4.67 | 3.33 |
| INDPROD | 1.00 | 1.00 | 6.0 | 1.0 | 8.0 | 8.0 |
| XOR | 2.00 | 2.00 | 13.7 | 4.0 | 13.7 | 10.7 |

The CLEAN instances are substantially larger on all measured continuation/evaluator diagnostics.

The most important control is XOR:

[
oxed{
	ext{nontrivial communication rank}

otRightarrow
	ext{hard extension evaluation}.
}
]

The XOR extension problem has a compact exact evaluator by Gaussian elimination.

Thus rank is retained only as one coordinate in SRAS, never as a time lower bound by itself.

---

# 6. Width correlation

Across all 60 tested instances, descriptive Spearman correlations were:

[
ho(mathrm{treewidth},mathrm{MDD nodes})approx0.696,
]

[
ho(mathrm{balanced expansion},mathrm{MDD nodes})approx0.609,
]

and

[
ho(mathrm{MDD nodes},mathrm{GF2 cut rank})approx0.838
]

on instances where communication matrices were computed.

Within CLEAN alone:

[
ho(mathrm{treewidth},mathrm{MDD nodes})approx0.876,
]

[
ho(mathrm{balanced expansion},mathrm{MDD nodes})approx0.867.
]

These are small-sample descriptive diagnostics, not statistical evidence for asymptotic scaling.

---

# 7. Interpretation

The experiment supports a real finite structural distinction:

[
oxed{
	ext{mediator-eliminated CLEAN extension maps}
}
]

have much richer balanced-cut continuation structure and much larger sampled reduced decision diagrams than the easy controls.

The distinction is plausibly related to the interaction graph becoming nearly clique-like at these tested densities.

But this does **not** establish representation-independent hardness.

Known knowledge-compilation results already warn that OBDD/DNNF size can be governed by treewidth/pathwidth while other algorithms exploit different representations. Likewise, Tseitin/XOR systems provide direct examples where branching-program or OBDD models can be large even though Gaussian-algebraic algorithms are efficient.

Therefore the observed MDD/cut growth is best understood as:

[
oxed{
	ext{evidence that a simple separator/decision-diagram summary is insufficient}
}
]

not evidence that no polynomial global summary exists.

---

# 8. Literature alignment

The experiment matches several known representation-specific phenomena.

Amarilli, Monet, and Senellart show singly-exponential dependence of structured knowledge-compilation size on treewidth/pathwidth for bounded-arity/degree monotone CNF/DNF settings, with matching lower bounds in their declared compilation classes.

Glinskih and Itsykson relate treewidth to exponential read-once branching-program lower bounds for Tseitin formulas while also recording pathwidth-based upper bounds.

Razgon's 2024 ECCC work gives further bounded-repetition branching-program results parameterized by treewidth-related quantities.

These results justify treewidth/pathwidth and cut structure as useful **representation diagnostics**. They do not transfer to unrestricted SAT runtime.

The finite CSP dichotomy theorem of Bulatov/Zhuk is another useful next lens: after mediator elimination, the chain system is a fixed finite-domain constraint language. Determining whether the induced language has tractable polymorphisms could reveal a compact algebraic evaluator or certify NP-completeness of the CSP language. Either outcome would sharpen the structural classification, though NP-completeness itself of course does not prove (P
e NP).

---

# 9. SRAS consequence

CLEANCORE-EVAL1 showed that complete-assignment mediator compatibility lies in the UNIVERSAL-EVALUATOR branch because mediators eliminate locally.

CLEANCORE-EXT1 shows that the stronger partial-extension family does **not** collapse comparably under the tested separator/decision-diagram representations.

The SRAS state can therefore be refined to:

[
oxed{
	ext{cheap mediator elimination}
	o
	ext{induced 7-state CSP}
	o
egin{cases}
	ext{compact algebraic/global evaluator},\
	ext{separator/knowledge-compiled evaluator},\
	ext{HARD-EVAL candidate}.
end{cases}
}
]

The current finite data reject neither of the first two branches in a representation-independent sense.

---

# 10. Most useful next test

The next experiment should classify the **constraint language itself**.

For every eliminated mediator resolvent, convert the induced clause into a relation on one to four 7-state chain variables. Collect the finite relation language

[
Gamma_{m clean}.
]

Then:

1. enumerate the actual relation types generated by the mediator construction;
2. test closure under simple candidate polymorphisms;
3. search for affine, majority, Maltsev, semilattice, near-unanimity, and related tractable signatures;
4. compare with the XOR/2-SAT controls;
5. if no tractable signature survives, map the language as closely as possible to the finite-domain CSP dichotomy classification.

This can expose a compact global evaluator that the MDD experiment misses.

If the language instead lands on the NP-complete side of the CSP dichotomy, that does not prove (P
e NP), but it would show that the mediator-eliminated clean core has retained general NP-hard expressive power rather than accidentally collapsing into a known tractable algebraic class.

---

# 11. Strict ledger

## PROVED/EXACT
- exact treewidth/pathwidth calculations for the finite generated graphs;
- exact balanced expansion for those graphs;
- exact reduced-MDD semantics for each sampled order;
- exact balanced-cut communication rows and (mathbb F_2) ranks for (kle6);
- Gaussian evaluation for XOR controls.

## COMPUTATIONAL
- all numerical growth profiles above;
- approximate (2.38^k) CLEAN EXT-MDD fit;
- descriptive correlations.

## FALSIFIED/RETIRED AS INFERENCES
- large MDD (Rightarrow) unrestricted runtime hardness;
- large communication rank (Rightarrow) unrestricted centralized runtime hardness;
- high treewidth alone (Rightarrow) unrestricted SAT lower bound.

## SURVIVING CANDIDATE
The mediator-eliminated 7-state extension language has no polynomial-size/polytime reusable evaluator available to arbitrary source-transparent computation.

**Status: OPEN.**

---

## References

- A. Amarilli, M. Monet, P. Senellart, *Connecting Width and Structure in Knowledge Compilation*, 2017.
- A. Amarilli, F. Capelli, M. Monet, P. Senellart, *Connecting Knowledge Compilation Classes and Width Parameters*, 2018.
- L. Glinskih, D. Itsykson, *On Tseitin formulas, read-once branching programs and treewidth*, ECCC TR19-020, 2019.
- I. Razgon, *The splitting power of branching programs of bounded repetition and CNFs of bounded width*, ECCC TR24-160, 2024.
- D. Zhuk, *A Proof of the CSP Dichotomy Conjecture*, 2017.
- A. Bulatov, *A dichotomy theorem for nonuniform CSPs simplified*, 2020.

---

## Bottom line

The stronger extension-map experiment **did not find the compact mediator-level collapse** that defeated the complete-state challenge.

At the tested sizes, CLEAN has a distinct high-width/high-cut/high-MDD profile.

But the XOR hostile control and known knowledge-compilation results prevent promoting that profile to unrestricted hardness.

The next structural question is now very concrete:

[
oxed{
	ext{What finite 7-state constraint language does mediator elimination actually generate?}
}
]

and

[
oxed{
	ext{does that language admit a tractable universal evaluator/polymorphism?}
}
]
