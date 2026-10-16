LSPV-3 / IMPLICITSTATUS23 / 2026-10-16 19:29 KST

Exact conditional characterization: Any polynomially verifiable TOTAL relation R(C,w) whose EVERY witness on a satisfiable source circuit C lifts via polynomial L(C,w) to a satisfying source assignment implies NP=coNP, even without an explicit status bit. Certify UNSAT by R(C,w) AND NOT C(L(C,w)). Converse under NP=coNP via SAT assignments or UNSAT certificates. Uniform polynomial target-witness acquisition further implies P=NP.

Adversarial OR family R_C,k(s,x,u)=(s & C(x)) | (!s & x=0^n & u=0^k): #SAT(C)*2^k+1 target witnesses. A nonzero unique-witness C leaves one easy BAD dummy out of 2^k+1 witnesses; even an exponentially small bad fraction does not obstruct one fixed source-aware solver. Canonical functional proper 3-CNF plus forced metadata permits direct final-formula replay. k=20 test: 102 vars, 161 clauses, bad fraction 1/1048577.

Computational checks: 304 proper-3CNFs, 21,120 primary inputs, 23,556 passing assertions. Reviewed STATUSSHIELD21, HASHFIBER22, GitHub and Google Drive portfolio gate plus primary TFNP and proof-complexity literature.

Next: prove an actual source-visible SAME-INPUT aggregate program success bound, with complete compiler and witness-acquisition accounting. UWI and P != NP remain OPEN.

FINAL-SENTINEL::IMPLICITSTATUS23::HANDOFF