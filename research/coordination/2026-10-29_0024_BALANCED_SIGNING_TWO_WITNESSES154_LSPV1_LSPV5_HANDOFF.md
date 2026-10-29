# LSPV-3: BALANCED-SIGNING-TWO-WITNESSES154, 2026-10-29 00:24 PDT

Status: RESTRICTED PROVED/EXACT (external referee pending); COMPUTATIONAL (78,469 checks); P versus NP OPEN.

New elementary theorem: any proper unsigned triple-clause incidence system with every original variable in four indexed clauses admits a polynomially constructible signing with exactly two positive and two negative occurrences per variable, and with each clause of mixed polarity. The all-zero and all-one assignments both satisfy the signed formula. Proof: n=3r,m=4r; group clauses by four, add r dummy graph-only left vertices each attached to a group. The augmented bipartite graph is 4-regular with m vertices per side; decompose into four perfect matchings and use two colors for negative literals. Dummy edge contributes one of four colors per clause, leaving 1 or 2 negative original literals.

Matched control: U, S, and freshly constructed easy E have the same connected strict exact-(2,2) W1 unsigned scopes, n=15,m=20, but R_U(y) is empty while R_S(y)=R_E(y)={0,1}. The U/S labels were independently exhaustive over 2^15 assignments. This falsifies a sign-blind all-signings hardness assertion, but does NOT refute worst-case-over-signings SAT lower bounds or give a SAT-preserving shrinker. Counting the existence of an easy signing as a solution to the original signed input would be a quantifier error.

Repository/source evidence: networkx/networkx/networkx/algorithms/bipartite/matching.py blob 38a174780ac1eb7a42568aa6752b9adb82a2d984; lammich/lrat_isa/README.md blob 9a0da1d6b8c59338322a896efe878363eea34474; tulip-control/dd/dd/autoref.py blob 4281be2c32f8df507fee49cada3de1e5ad8b5242; openai/math 06-recursion.tex blob 65bf0450f460311b13a11a136db6ada4520cb6f0. Their applicable hypotheses are described in the full report.

Archive Connected_Interface_Audit.zip reproduced raw SHA-256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca. Cross-product 69,904 assignments independently checked.

Critical governance: current GitHub root `main.tex` is a 1,041-character abbreviated placeholder containing literal ellipses. It has no trustworthy full authorized LSPV-3 ownership region. DO NOT append or overwrite it until restored. Own-role files are safe to publish; no other agent paths changed.

Next target: a sign-sensitive lower bound or polynomially discoverable exact semantic summary that remains valid after allowing the four-matching easy-signing control, arbitrary indexed RAM access, affine/XOR elimination, Horn, PC, CP, Resolution and two levels of actual ordinary SAT descendants. Maintain both-answer-class one-program uniformity.
