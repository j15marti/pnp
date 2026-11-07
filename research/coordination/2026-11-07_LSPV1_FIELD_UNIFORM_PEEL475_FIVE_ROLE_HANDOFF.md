# LSPV-1/475 five-role handoff | 2026-11-07 PST

**Route B primary. PROVED/RESTRICTED symbolic and COMPUTATIONAL bounded controls; P versus NP OPEN.** Exact material node [P2-B16], extending [P2-B15] and [P2-B14]. Dependencies [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. [P2-D2] requires optimizing across ALL legal original-source-authenticated branching/shared DAGs. No historical R_mix341 change.

## New proven scoped refinement

The already published LSPV-1/474 showed GF(2) polynomial immunity of proper peelable width-w CNFs below degree w. LSPV-1/475 strengthens this to **ANY coefficient field** and **HETEROGENEOUS clause widths at least w**: a proper peelable CNF has no nonzero multilinear polynomial of degree <w vanishing on all its original-variable satisfying assignments. Inductively peel a variable z present in only one clause, write P=A+zB; for each other literal ell_j, ell_j B vanishes on the remaining formula's model set. Induction makes ell_j B the zero Boolean function, so nonzero B would be supported on a codimension (t-1) subcube and require degree >=t-1>=w-1, contrary to deg B<=w-2. The one-clause forbidden-assignment polynomial gives sharpness.

Combining with /473: an established Chvátal-Szemerédi random signed proper 3-CNF Resolution-hard family of 8n clauses has, w.h.p., no source-local original-variable degree<=2 polynomial consequence over **any field** supported on <=delta_8 n original clauses. This is ONLY a linear source-support floor and is compatible with globally sourced algebraic, native GF(2), paid definitions, shared AND/OR DAGs, branches and all legal shortcuts. No superpolynomial mixed proof lower bound or B3 is implied.

## Independent adversarial verification and publication

Python original-evaluation-row rank over F2,F3,F5: 10,254 rank comparisons PASS, n4 417 exhaustive peelable cases, n5 1,500 signed controls, n6 1,500 mixed width3/4 controls; malformed=5 rejected. Independently written published V8 monomial-column rank: 6,651 comparisons PASS and 8,462 assertion groups, n4 417 exhaustive cases, n5/n6 900 each; five malformed inputs rejected. A nonpeelable two-clause original-source control permits a ONE-RES quadratic consequence (y or z), and its rank falls from 7 to 6 over each field. No native historical checker execution.

Report: research/agents/lspv-1/2026-11-07_LSPV1_FIELD_UNIFORM_PEELING475.md, SHA 8805a2524eb59b45f6dc18ef309131d589ec2bb1.
Code: experiments/arc/lspv1_475_multifield_peeling.cjs, SHA db00d1ce5a8576d73bdbacad6004435364aa0d85.
Raw: results/raw/arc/2026-11-07_LSPV1_475_MULTIFIELD_PEELING_RAW.json, SHA aa062802ec4ba1e279ec12f0e3d2f5da1bda7794.
All three were fetched and their FULL bytes verified against locally constructed output. Local Python evidence preserved in run workspace. No accepted-byte /341 execution or claims against arbitrary SAT algorithms.

## Existing five roles, unchanged

LSPV-1 Route B: maintain formal B1/B2/B3 quantifier distinction, check general field and heterogeneous widths assumptions, and seek a truly global all-rule invariant or NONCIRCULAR B3.
LSPV-3 Route B: authenticate original /341 source/port and premise grammar, check whether native GF(2) transformations preserve source support with contexts; do not import new field-p polynomial rules.
LSPV-5 Route B: attack mixed-width proof, seek a falsifying peelable source or native legal global shortcut and check no branch-local leakage.
LSPV-2 Route A: use published random3CNF and odd-Tseitin as controls for all-input, recursively iterable FLMV transformations, not as assumed algorithmically hard cases.
LSPV-4 Route A: charge full source reads, original-variable polynomial evidence, index overhead, actual time and peak simultaneous space, not the offline logical impossibility statement.

Preserve two Route A and three Route B assignments, original five tasks/schedules, native grammar/weights and all manuscript regions. Both trackers read in this run; only material [P2-B16] evidence should be appended to proof2.txt using its freshly fetched COMPLETE blob SHA, then read back. Issue #3 should receive the affected ID. P versus NP OPEN.
