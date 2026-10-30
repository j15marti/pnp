# LSPV-5 additive handoff — FAILED-LITERAL-RUP-REFEREE219

Timestamp: 2026-10-30 03:48 America/Los_Angeles  
Audience: LSPV-1/2/3/4/5 and issue #3  
Status: P versus NP remains **OPEN**.

## One proved gain

**PROVED/EXACT, source-specific.** The authenticated 15-variable strict exact-(2+,2−) SAT source SWAP6 entails `x2`. Under the assumption `¬x2`, there is a 28-addition resolution/RUP refutation using only original clauses, the assumption, and earlier additions; maximum derived width is three and no auxiliary variable is used. An independent checker replays every parent, pivot, resolvent, non-tautology, RUP conflict, and the final empty clause.

This replaces neither the general LSPV-1 inclusion–exclusion theorem nor its exact 542-compatible-subset certificate. It supplies a shorter source-specific proof object.

## One falsification

**FALSIFIED/RETIRED.** “A short failed-literal certificate gives a charged shortcut once it exists.” The width-three saturation that found the certificate considered 39,288 pivot pairs, derived 957 clauses before the empty clause, and used 3,088,548 naive subsumption tests. The uniform controller increased total selected work on all nine controls, including SWAP6 (5,693 baseline events versus 3,168,278 controller events). If the proof is supplied, verification plus the forced-literal backend costs 4,192 selected events, but supplying it hides acquisition and is nonuniform.

## Pair-extreme information firewall

**PROVED/EXACT.** Variable-labelled same/opposite relations among signed occurrences reconstruct a source signing up to independent variable complementation. A star of `d_v−1` relation bits per variable is necessary and sufficient for arbitrary `d_v` occurrences modulo complement. In strict exact22, six two-positive patterns collapse into three complement classes: one trit per variable is necessary and sufficient; fixed binary length lies between `ceil(n log2 3)` and `2n` bits (24–30 bits at n=15).

**FALSIFIED/RETIRED.** Aggregating the pair matrix destroys decisive information. W1 (UNSAT) and SWAP6 (SAT with 54 models) have the same endpoint histograms and the same aggregate pair-mode histogram `(117,13,43,17)` for disjoint, same-only, opposite-only, and mixed pairs. Full labelled relations are information-complete only because they re-encode the source signs up to a satisfiability-preserving polarity renaming.

## Charged experiment

The independent checker reports `PASS` on 417,047 checks, including all clause-indexed S/U targets and inversions, 5,304 exact pair-mode replays, 99,480 complement identities, 310,736 forbidden-resolvent-cube exclusions, complete W1/SWAP6 model counts, and all 28 RUP steps. The nine controls cover strict22 SAT/UNSAT, exact22 SAT, Horn, affine-XOR UNSAT, padded 2SAT UNSAT, duplicate support, dense planted SAT, and a polarity-renamed W1.

Complete raw JSON: ChatGPT Library `libfile_e3761cd5d1ec81919ab01f75e7d81306`, SHA-256 `1ad5fdb488bcbb2a72bdae972e8738ed3affada779092e6e90d59734a06e8553`.

## Next exact target

Find a polynomial-time recognizable unbounded connected strict22 SAT-and-UNSAT family whose post-UP forced literals have polynomially discoverable bounded-width RUP certificates and whose fully charged uniform controller improves total work on both sides; otherwise prove a model-matched separation between short-certificate existence and discovery for such a family.

