# CLEANCORE-EXT1 — Extension-Map Structure After Low-Degree Mediator Elimination

**Date:** 2026-10-05  
**Repository:** \`j15marti/pnp\`  
**Global status:** **OPEN. P versus NP remains open.**

This note extends CLEANCORE-EVAL1 from complete chain-state compatibility to the stronger partial-extension response map.

For an eliminated clean-core chain CSP \(F\), define

\[
\operatorname{EXT}_F(\rho)=1
\]

iff the partial chain-state restriction \(\rho\) extends to a complete satisfying assignment.

Each chain challenge coordinate has eight possibilities,

\[
\{*\}\cup S,
\]

where \(*\) means unassigned and \(S\) is the set of seven satisfying states of a type-1 chain. Thus the explicit challenge table has \(8^k\) entries for \(k\) chains.

The purpose is not to infer hardness from one representation. It is to compare several exact finite structural/evaluator diagnostics on the **same instances** and hostile controls.

---

## 1. Families

Five families were tested.

### CLEAN
Random low-degree externally mediated cores:
- \(k\) type-1 chains;
- \(2k\) outside mediators;
- mediator degree \(2,3,\) or \(4\);
- both mediator polarities occur;
- every mediator clause couples literals from two distinct chains;
- mediators are eliminated exactly using MED-ELIM1.

### 2SAT
Random 2-CNF constraints on one representative bit of each chain-state variable.

### PATH
Adjacent-chain 2-CNF constraints only. The primal graph has treewidth/pathwidth 1.

### INDPROD
Independent disjoint chain pairs, testing direct-product structure without global interaction.

### XOR
Random low-density linear equations over \(\mathbb F_2\) on one representative bit per chain. Extension is evaluated by canonical Gaussian elimination. This is the mandatory control showing that nontrivial continuation/communication structure does not imply hard centralized computation.

---

## 2. Exact finite metrics

For every generated instance the experiment records:

1. primal interaction graph edge count;
2. **exact treewidth** by complete elimination-order search;
3. **exact pathwidth / vertex-separation number** by subset dynamic programming;
4. exact balanced edge-expansion value at a floor-half cut;
5. reduced ordered **8-ary MDD** size for the partial-extension function;
6. MDD maximum layer width;
7. for \(k\le6\), maximum over balanced cuts of:
   - distinct partial-extension communication rows;
   - \(\mathbb F_2\) rank of the partial-extension communication matrix;
   - matrix density.

For MDDs, only finitely many variable orders are searched: natural, ascending degree, descending degree, and sampled random orders. The reported MDD value is therefore an **upper bound** on the optimal ordered-MDD size, not an all-order minimum.

Communication cuts are exhaustive over balanced partitions for \(k\le6\).

Three deterministic seeds were used for every family and \(k=4,5,6,7\).

Raw results:

\`results/source_reduction/2026-10-05_clean_core_extension_profiles.csv\`

Reproducible script:

\`experiments/source_reduction/clean_core_extension_profiles.py\`

---

## 3. CLEAN finite profile

Averaging the three CLEAN instances:

| \(k\) | mean treewidth | mean pathwidth | mean balanced expansion | mean best sampled EXT-MDD nodes | mean best MDD width |
|---:|---:|---:|---:|---:|---:|
| 4 | 3.00 | 3.00 | 2.00 | 50.7 | 30.0 |
| 5 | 4.00 | 4.00 | 3.00 | 103.0 | 47.0 |
| 6 | 5.00 | 5.00 | 3.00 | 369.0 | 163.7 |
| 7 | 5.67 | 5.67 | 3.89 | 599.0 | 252.0 |

Over these four sizes, mean best-sampled MDD node counts fit approximately

\[
1.55(2.38)^k,
\]

with finite log-linear \(R^2\approx0.973\).

This is **COMPUTATIONAL finite evidence only**. No asymptotic claim is made.

---

## 4. Partial-extension communication profile

For \(k\le6\), every balanced chain cut was examined and the cut with maximum \(\mathbb F_2\) rank retained.

For CLEAN:

| \(k\) | mean distinct rows | mean \(\mathbb F_2\) rank |
|---:|---:|---:|
| 4 | 34.3 | 30.3 |
| 5 | 51.3 | 47.3 |
| 6 | 200.7 | 151.7 |

For \(k=6\), each balanced side has

\[
8^3=512
\]

possible partial challenges. The finite CLEAN instances therefore retain hundreds of distinct continuation profiles across a balanced cut.

This is a communication/representation result, not a centralized runtime lower bound.

---

## 5. Hostile controls at \(k=6\)

Averaged over three seeds:

| family | treewidth | pathwidth | mean EXT-MDD nodes | mean MDD width | mean distinct rows | mean \(\mathbb F_2\) rank |
|---|---:|---:|---:|---:|---:|---:|
| CLEAN | 5.00 | 5.00 | **369.0** | **163.7** | **200.7** | **151.7** |
| 2SAT | 2.33 | 2.33 | 6.0 | 1.33 | 4.0 | 3.0 |
| PATH | 1.00 | 1.00 | 8.0 | 2.0 | 4.67 | 3.33 |
| INDPROD | 1.00 | 1.00 | 6.0 | 1.0 | 8.0 | 8.0 |
| XOR | 2.00 | 2.00 | 13.7 | 4.0 | 13.7 | 10.7 |

The CLEAN instances are substantially larger on every measured continuation/evaluator diagnostic.

The most important hostile control is XOR:

\[
\boxed{
\text{nontrivial communication rank}
\not\Rightarrow
\text{hard extension evaluation}.
}
\]

The XOR extension problem has a compact exact evaluator by Gaussian elimination. Rank therefore remains only one SRAS coordinate.

---

## 6. Descriptive width correlations

Across all 60 tested instances,

\[
\rho_{\rm Spearman}(\mathrm{treewidth},\mathrm{MDD\ nodes})
\approx0.696,
\]

\[
\rho_{\rm Spearman}(\mathrm{balanced\ expansion},\mathrm{MDD\ nodes})
\approx0.609,
\]

and, where communication matrices were computed,

\[
\rho_{\rm Spearman}(\mathrm{MDD\ nodes},\mathrm{GF2\ cut\ rank})
\approx0.838.
\]

Within CLEAN alone,

\[
\rho_{\rm Spearman}(\mathrm{treewidth},\mathrm{MDD\ nodes})
\approx0.876,
\]

\[
\rho_{\rm Spearman}(\mathrm{balanced\ expansion},\mathrm{MDD\ nodes})
\approx0.867.
\]

These are small-sample descriptive diagnostics, not asymptotic or inferential claims.

---

## 7. Interpretation

The experiment supports a real finite structural distinction:

\[
\boxed{
\text{mediator-eliminated CLEAN extension maps}
}
\]

have much richer balanced-cut continuation structure and much larger sampled reduced decision diagrams than the easy controls.

The distinction is plausibly related to the interaction graph becoming near-clique-like at the tested densities.

But this does **not** establish representation-independent hardness.

Known knowledge-compilation results already show that OBDD/DNNF size can be governed by treewidth/pathwidth while another computational representation behaves very differently. Tseitin/XOR formulas are an especially important hostile control: branching-program/OBDD representations can be large while Gaussian algebra remains efficient.

Thus the measured growth is evidence that simple separator/decision-diagram summaries are inadequate, not evidence that every polynomial global summary is impossible.

---

## 8. Literature alignment

The experiment aligns with several representation-specific results:

- Amarilli, Monet, and Senellart connect bounded treewidth/pathwidth with singly-exponential structured knowledge-compilation size and matching lower bounds in declared compilation classes.
- Glinskih and Itsykson relate treewidth to read-once branching-program lower bounds for Tseitin formulas while giving pathwidth-based upper bounds.
- Razgon's 2024 ECCC work gives further bounded-repetition branching-program results parameterized by treewidth-related quantities.

These justify width and cut structure as diagnostics but do not transfer to unrestricted SAT runtime.

The finite-domain CSP dichotomy of Bulatov/Zhuk gives another useful next lens. After mediator elimination, the chain system is a finite-domain constraint language. Classifying its polymorphisms may expose a compact algebraic evaluator or place the language on the NP-complete side of the CSP dichotomy. NP-completeness itself would not prove \(P\ne NP\).

---

## 9. SRAS consequence

CLEANCORE-EVAL1 showed that complete-assignment mediator compatibility is in the UNIVERSAL-EVALUATOR branch because mediators eliminate locally.

CLEANCORE-EXT1 shows that the stronger partial-extension family does **not** comparably collapse under the tested separator/decision-diagram representations.

The SRAS branch can therefore be refined as

\[
\boxed{
\text{cheap mediator elimination}
\to
\text{induced 7-state CSP}
\to
\begin{cases}
\text{compact algebraic/global evaluator},\\
\text{separator/knowledge-compiled evaluator},\\
\text{HARD-EVAL candidate}.
\end{cases}
}
\]

The finite data do not eliminate the first two branches in a representation-independent sense.

---

## 10. Most useful next test

Classify the **constraint language itself**.

For each eliminated mediator resolvent, convert the induced clause into a relation on one to four 7-state chain variables. Collect the finite relation language

\[
\Gamma_{\rm clean}.
\]

Then:

1. enumerate the actual relation types generated by mediator elimination;
2. test closure under simple candidate polymorphisms;
3. search for affine, majority, Maltsev, semilattice, near-unanimity, and related tractable signatures;
4. compare with XOR/2-SAT controls;
5. map the language as closely as possible to the finite-domain CSP dichotomy.

If a tractable polymorphism exists, it may reveal the compact global evaluator that the MDD experiment misses.

If the language lies on the NP-complete side, that would show that mediator elimination retains NP-hard expressive power rather than accidentally collapsing to a known tractable algebraic class, but it still would not separate P from NP.

---

## 11. Strict ledger

### PROVED/EXACT
- exact treewidth/pathwidth for the generated finite graphs;
- exact balanced expansion for those graphs;
- exact reduced-MDD semantics for each sampled order;
- exact balanced-cut communication rows and \(\mathbb F_2\) ranks for \(k\le6\);
- Gaussian evaluation for XOR controls.

### COMPUTATIONAL
- all numerical profiles above;
- approximate \(2.38^k\) CLEAN EXT-MDD fit;
- descriptive correlations.

### FALSIFIED/RETIRED AS INFERENCES
- large MDD \(\Rightarrow\) unrestricted runtime hardness;
- large communication rank \(\Rightarrow\) unrestricted centralized runtime hardness;
- high treewidth alone \(\Rightarrow\) unrestricted SAT lower bound.

### SURVIVING CANDIDATE
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

But XOR and known knowledge-compilation results prevent promoting this profile to unrestricted hardness.

The next structural question is now concrete:

\[
\boxed{
\text{What finite 7-state constraint language does mediator elimination actually generate?}
}
\]

and

\[
\boxed{
\text{does that language admit a tractable universal evaluator/polymorphism?}
\]
