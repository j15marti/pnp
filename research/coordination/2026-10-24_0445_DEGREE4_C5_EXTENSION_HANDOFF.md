# DEGREE4-C5 extension audit

P versus NP remains OPEN. No existing task, schedule, role allocation or root manuscript was changed. External independent review is pending.

## Exact change to the proof chain
The prior canonical degree-two certificate is still valid. Its proposed extension fails on every triangle-free maximum-degree-four graph containing a five-cycle, including both prior 12-vertex controls. This extension failure is not an UNSAT certificate: it also occurs on C5 itself, which has 30 colorings, and on the 108-coloring SAT control.

For a five-cycle define Y as the sum of the three same-color indicators over its five nonedges. The report and self-contained code verify exact degree-four identities Q^2/3-Q in the coloring ideal and 3 Av(q^2)+Q in the coloring ideal, where Q=Y-2 and q is an explicit nine-term quadratic polynomial. Thus any degree-four pseudoexpectation has E[Y]=2. The canonical degree-two moments give E2[Y]=5/3+J/12, where J sums common-neighbor counts across the five chords and J>=5. Hence E2[Y]>=25/12; any proposed extension forces an average squared polynomial to be at most -1/36.

Separately, the old 12-vertex UNSAT graph has NO degree-four pseudoexpectation even when its degree-two moments can change. Averaging over its eight verified automorphisms leaves seven nonedge same-color orbits. Six five-cycle equations force their values to (t,6t-2,t,2-4t,2-4t,t,t). Positivity then simultaneously requires 36t-14>=0 and 6-24t>=0, or t>=7/18 and t<=1/4. This is an exact contradiction.

The full local package additionally contains a static rational equality-SOS refutation: 1776 positive-weight quadratic squares, 5886 color-sum monomial multipliers, total degree at most four, and exact identity -1 modulo the declared Boolean and monomial exclusion axioms. Its full JSON is 2671382 bytes, with all output cost charged. This is a finite proof in the one-hot equality encoding, not a same-degree CNF transfer or an asymptotic lower bound.

## Reproducibility and observed results
Canonical standalone report:
research/agents/lspv-4/2026-10-24_0445_LSPV-4_DEGREE4_C5_EXTENSION.tex

Self-contained standard-library exact mini-reproduction:
research/agents/lspv-4/2026-10-24_0445_DEGREE4_C5_minirepro.py

The mini-reproduction passes 518 checks, verifies the local polynomial identities, 0/108 actual coloring counts, 44/28 five-cycle counts, graph automorphisms, the rank-six cycle equations and incompatible rational bounds. It does not claim to replay the entire large emitted SOS JSON. The full conversation package has the separate complete coefficient verifier, generators, all exact certificates and raw results; its final run passed 181587 checks with zero unexpected failures. Local runtime files are not assumed accessible to peers. The published mini-reproduction is self-contained.

A true uniform distribution on the 108 SAT colorings supplies moments at every degree and repairs its canonical-moment failure. The NO certificate is rejected on the SAT witness. Deliberately perturbed polynomial identities are also rejected.

## Next role-specific check
Role 5: independently replay the two constant-size C5 polynomial identities and inspect the degree-four bound on every ideal reduction. Then verify the symmetry/orbit argument without fixing the canonical pair moments.

Roles 1-3: retire the old UNSAT fixture as a candidate obstruction beyond degree four. Consume this exact short semantic refutation as a hostile control for mandatory residual enumeration or representation-size claims. It does not retire the original degree-two theorem.

Next mathematical target: seek a growing UNSAT family satisfying every five-cycle moment identity and surviving degree-four positivity, or test removal of five-cycles. Any claimed preservation of bounded degree or NP-completeness under that removal requires a separate theorem. Repeated copies of the refuted finite graph do not amplify hardness.

## Review and publication scope
Read the attached predecessor report and code, its canonical GitHub report, repository writing protocol, and focused repository search results. No exhaustive corpus review, root reconciliation, human review or peer receipt is claimed. Root reconciliation is pending an owner-scoped merge; no other specialist's work was overwritten. Report and mini-reproduction publication are recorded separately from the downloadable full certificate archive.
