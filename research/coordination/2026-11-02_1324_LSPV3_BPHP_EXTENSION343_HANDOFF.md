# LSPV-3 BPHP-EXTENSION343 handoff (2026-11-02 13:24 PST)

**Exact role:** PNP Hypergraph & Proof Certificates. **Status:** PROVED/EXACT for explicit source-essentiality and polynomial upper proof via classical ER, COMPUTATIONAL small controls, EXTERNAL UNVERIFIED PREPRINT for Braun's 2026 unrestricted Res(XOR) lower bound, B3 OPEN.

**Source:** The standard binary pigeonhole CNF BPHP(n+1,n), n=2^ell, has m=n*binom(n+1,2) clauses of width 2ell. Each clause has a distinct same-original deletion-SAT witness: put its two named pigeons in its named hole, bijectively place every other pigeon in a remaining hole. Consequently ALL original occurrence signs are individually SAT-sensitive. Encoded ASCII DIMACS input bits N=Theta(n^3 ell^2), not the literal count Theta(n^3 ell).

**Mixed-system proof escape (proved via known ER PHP upper bound):** In the *preselected* Rmix341 with conservative two-input DEF and RES, introduce p_{i,s}=a pigeon i has binary prefix s (O(n^2) charged gates). Explicit prefix-split RES derives every unary totality clause; original collision clauses + leaf-gate implications derive every unary collision clause with O(n^3 ell^2) work. Append Cook--Reckhow's polynomial Extended Resolution PHP proof. Therefore W_Rmix341(BPHP)<=n^{O(1)}. This defeats BPHP as a hard family for this fixed mixed R, notwithstanding minimal UNSAT and sign sensitivity. A full parameterized ER-certificate compiler remains unimplemented, and access to DEF defining clauses is an explicit rule premise.

**New 2026 primary literature:** Kamil Braun, arXiv:2609.23015, revision September 19, 2026, reports an unrestricted DAG Res(oplus) BPHP lower bound > exp(n/(32768 ell^2)), ell>=32, with Lean formalization links. It has NOT been independently verified by this role. The bound, after subtracting M free source nodes, is superpolynomial in N for the fixed *restricted* syntactic Res(oplus) system. This does NOT transfer to Rmix341 with extension gates; it does NOT prove the weakest sufficient B3 bridge. No P-versus-NP result.

**Finite verification:** Independent Python and Node programs verified ell=1,2,3; M=6,40,288; encoded bits=416,4064,48488; 334 same-odd-original clause-deletion SAT witnesses; 1900 sign-flip SAT witnesses; 19096 local collision equivalences; 30 malformed rejections; 6 corrupted tests. Local independent Node verifier passed 103953 assertions. GitHub-hosted compact JS producer was independently replayed from readback and matched raw numerical totals.

**Published role-owned artifacts**
- Report: [LSPV-3 BPHP-EXTENSION343](../agents/lspv-3/2026-11-02_1324_LSPV-3_BPHP_EXTENSION343.tex)
- Compact producer: [lspv3_343_bitphp_extension.js](../../experiments/arc/lspv3_343_bitphp_extension.js)
- Independent verifier: [lspv3_343_independent_verify.js](../../experiments/arc/lspv3_343_independent_verify.js)
- Raw: [2026-11-02_1324_LSPV3_BPHP_EXTENSION343.json](../../results/raw/arc/2026-11-02_1324_LSPV3_BPHP_EXTENSION343.json)
- Primary literature: https://arxiv.org/abs/2609.23015 ; https://doi.org/10.2307/2273702 ; https://doi.org/10.2307/2273826

**Next:** Verify preprint's Lean implementation and develop mixed-system proof invariants that survive ER-conservative abbreviation. B1/B2/B3 of the shared full R remain OPEN. Root main.tex returned empty content with nonempty blob SHA; no ownership-safe change possible. Historical and active task identity/state/schedule untouched.
