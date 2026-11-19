# Independent strict-C red-team, 2026-11-19 run 8

**PROVED:** The particular universal canonical SA3 pseudomarginal assignment from the run-6 research is **not extendible** to a four-variable joint already on the SAT source
[
F=C(a,b,c)\land C(a,b,d).
]
Here a,b,c,d are four distinct names. Direct enumeration verifies **50 complete satisfying assignments** (one is (0,1,2,2)). All four canonical SA3 scopes are individually normalized and their 300 pair-marginal cells agree.

## Sharp exact certificate

Canonical SA3 tables use denominator 750. The original clause on abc forces
[
750\mu_{abc}(0,1,2)=25.
]
The clause on abd forces (mu_{abd}(0,1,t)=0) for (t\in\{0,1,3\}).
The scope acd has linked pairs ac and ad. If cd is unlinked, the canonical wedge coupling has (R_{2,2}=R_{2,4}=0), so (mu_{acd}(0,2,2)=mu_{acd}(0,2,4)=0). If cd is linked by any other clause, its canonical table is uniform on original C; both of those triples are forbidden and again have zero mass.

Every nonnegative joint distribution must satisfy
[
\mu_{abc}(0,1,2)\le\mu_{acd}(0,2,2)+\mu_{acd}(0,2,4)
 +\sum_{t\in\{0,1,3\}}\mu_{abd}(0,1,t).
]
The canonical tables demand (25/750\le0), impossible. The result persists in any larger source containing two original clauses with a pair of common names. This is **minimum by variable and physical-clause count** for nonextension of this recipe: with at most 3 names an SA3 family is already a joint; with 0 or 1 original clause, uniform C coloring of that clause and independent uniform colors on all other names extends the recipe.

**Scope firewall:** SA4 is feasible for SAT F (uniform probability on the 50 satisfying assignments). The exact result refutes only a specific attempted SA3-to-SA4 lift, not the original universal SA3 theorem or the SA4 hierarchy. A previous 5-name forest nonextension example remains stronger in incidence-girth terms.

## Independent eight-clause audit

Audited the original strictly ternary source:
```
C(0,2,3) C(0,2,4) C(1,2,5) C(1,5,6) C(3,4,6)
C(0,7,8) C(1,7,8) C(0,1,9)
```
Every clause has three distinct variable names. Split private sets after shared names (0,1) into {2,3,4,5,6}, {7,8}, {9}. Independently enumerated **every** private tuple for all 25 shared assignments; block masks in (E,A,B) order were (110),(101),(011). The full source has **zero** assignments and incidence girth 4. The exact counts after deleting physical clause index 0..7 are

```
340, 340, 80, 120, 460, 240, 240, 600.
```

All eight complete original-C deletion witnesses were replayed independently with a quadratic predicate, including testing that the deleted clause was false. Precisely **2,420** full colorings violate exactly one clause. These finite rare-witness counts do not force global exhaustive search because the source-aware factorization has only two boundary variables.

## Girth-10 challenge: incomplete, not proof

On the previously reported 149-name/168-original-C incidence-girth-10 source SHA256 `6191abe310a44142a39a3647f225c40232034f19a65b91f39b47edd295f4dc42`, a distinct C++ original-R/GAC implementation returned **INCOMPLETE** after 30,000,001 visited nodes, 16,383,958 failed branches, ~47.3 seconds. The prior single-solver UNSAT report was therefore neither independently confirmed nor falsified.

The standard-library Python small-fixture audit ran 1,055,914 original-C predicate evaluations, 8.71 s, 277,605 bytes tracemalloc-traced allocations. This is not formal writable-space and does not imply generic time bounds. All input, failed local assignments, complete deletion witnesses and output were counted in the finite test. No free polarity advice, supplied correct paths or shortcut oracles.

**OPEN:** independent static UNSAT certificate for 149/168; exact resource-preserving all-z obstruction-cover discovery for general strict-C sources; transfer to unrestricted P versus NP.

Reproducibility archive: `T5C_RedTeam_SharpSA3_ExactCritical8_Run8_20261119.zip` supplied in the conversation, SHA256 `aceda62135bb6f5d416ee5236d3009c2ad866674b764c39b930fd7db0ab21961`. Scripts: `independent_audit.py`, `independent_replay.py`, distinct C++ GAC code, original source records, `results.json`, independent logs and SHA256SUMS.

Related published background: Thapper/Živný, SIAM J Computing 46 (2017), DOI 10.1137/16M1079245; Buss/Williams, Computational Complexity 24 (2015), DOI 10.1007/s00037-015-0104-9.

**P versus NP remains OPEN.**