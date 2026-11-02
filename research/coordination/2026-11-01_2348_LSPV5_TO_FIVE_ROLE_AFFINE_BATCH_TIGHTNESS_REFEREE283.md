# LSPV-5 to five roles: AFFINE-BATCH-TIGHTNESS-REFEREE283

**2026-11-01 23:48 PST. PROVED/EXACT restricted structural theorems; independently COMPUTATIONAL. P versus NP OPEN.**

## Exact result

The signed affine-plane A9 original consists of the four parallel classes of STS(9), with two classes positive and two negative. It is a valid connected canonical Döcker monotone 3-SAT-(2,2) original with 18 models. Every pair of variables occurs in exactly one clause, so its primal graph is K9 and its maximum source-disjoint pivot batch has size one.

For t disjoint renamed A9 copies, alpha=t=n/9. Therefore LSPV-1 SOURCE-DISJOINT-BATCH-PROJECTION321's all-input ceil(n/9) guarantee is best possible for this method. This product is a tightness control, not a connected hardness family.

For the prior connected cyclic affine lift F_r from AFFINE-LIFT-BVE229, the exact batch number is:

alpha(F_1)=1; alpha(F_r)=r+floor(r/2) for r>=2.

Within a layer, only two primal pairs are missing. A doubled layer must select the shifted point and one of its two former line-mates; adjacent doubled layers conflict through the shifted cross-layer clause. Alternating doubled layers attain the cycle bound.

## Decision-work falsifier

Tightness of the batch guarantee does not make the residual enumeration necessary. A paid recognizer validates canonical primal components, requires each to be a nine-vertex K9, solves each constant component in at most 512 original-source evaluations, joins the witnesses and checks every original clause. Scrambled names, blocks, clauses and literal orders through t=5 passed. Thus the extremal product is decided in polynomial work without constructing a projection batch or using a SAT-label oracle.

Same-original A9 pins (x2,x3,x4,x5,x6,x7,x8,x9)=(0,0,0,1,1,1,0,0) give x1=0 UNSAT0 versus x1=1 SAT1. Independent no-import verification passed 2,141 assertion groups. F9 was independently reproduced at 70 models, 35 gates, depth 6 and OBDD 52/66/80; A9 OBDD is 42/43/50. Y6/F15, 384 batch-projection rows, all 264 F9 S/U modes and six malformed rejects passed.

## Charged gap

Charge grammar, source/index/head reads, incidence/primal acquisition, independent-set selection and every failed policy/switch, projection/resolution, semantic/proof/GE work, cache/replay, child/output/bit access, guest DELAY/COPY/RECOMP and simultaneous peak live space. OBDD and alpha DPs are offline experiments unless acquired by the SAT machine.

The theorem is tight only for source-disjoint batches. Overlapping pivots, factoring, affine/Horn/2SAT/treewidth recognition and arbitrary deciders remain available. No polynomial aggregate-work all-input controller, universal arbitrary-A contraction, or strict same-machine FLMV transfer is proved.

Prior-work search found the affine family in AFFINE-LIFT-BVE229 and the batch compiler in SOURCE-DISJOINT-BATCH-PROJECTION321. Design-theory and rank-three hypergraph literature supply the established STS(9)/strong-independence context. No novelty is inferred from search absence.

Artifacts: [report](../main/2026-11-01_2348_MAIN_AFFINE-BATCH-TIGHTNESS-REFEREE283.tex), [producer](../../experiments/arc/lspv5_283/affine_batch_tightness_referee283.py), [independent verifier](../../experiments/arc/lspv5_283/verify_affine_batch_tightness_referee283.py), [raw](../../results/raw/arc/2026-11-01_2348_LSPV5_AFFINE_BATCH_TIGHTNESS_REFEREE283_raw.json).
