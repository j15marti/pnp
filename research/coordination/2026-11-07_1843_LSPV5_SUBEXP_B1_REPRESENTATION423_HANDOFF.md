# LSPV-5/423 handoff — duplicate-free Pang transfer

**Affected tracker IDs:** `[P2-B3]`, new `[P2-L5-423]`. `proof1.txt` unchanged.

PROVED/EXACT elementary repair: for Pang $F(n,3,8n)$, the duplicate-clause event has probability at most

$$\frac{\binom{8n}{2}}{8\binom n3}=\frac{3(8n-1)}{(n-1)(n-2)}\le\frac{48}{n}.$$

Thus Pang's a.a.s. hard event intersects the duplicate-free event a.a.s.; the hard subsequence embeds exactly into the OpenAI `Finset` CNF without relying on unproved hardness preservation under deduplication. Exact reconstruction of the formal encoder gives

$$L\le n+2+m(24n+16),$$

so at $m=8n$, $L\le192n^2+129n+2$ and the formalized runtime remains $2^{o(n)}$.

Conditional restricted conclusion: assuming Pang's recent preprint theorem and the inspected formal exact-counter theorem, B1 fails for the distinct fixed `Res(PC_r/F_p)` calculus when paid cost is polynomially related to Pang DAG size. This is not B2, B3, a historical-$R_{\mathrm{mix341}}$ lower bound, or P-versus-NP resolution.

Checks: Python 40,030; independent Node/BigInt 30,021; peer LSPV-1/492 replay 297. No Lean/Comparator or Pang proof replay. SAT/UNSAT, duplicate canonicalization and malformed controls passed.

Next LSPV-1/3: identify the exact fixed calculus/weight map and do not silently transfer Pang's restricted theorem across native mixed rules. Next LSPV-5: attack that map and any claimed historical-$R_{\mathrm{mix341}}$ consequence. P versus NP remains OPEN.
