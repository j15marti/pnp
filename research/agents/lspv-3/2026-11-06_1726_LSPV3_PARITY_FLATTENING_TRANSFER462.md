# LSPV-3/462 | Exact high-rank parity-flattening barrier and proof-transfer no-go
**2026-11-06 17:26 PST | Route B | PROVED/RESTRICTED (standard combinatorial result, model-specific corollary), COMPUTATIONAL; historical accepted-byte R_mix341, B3, unrestricted mixed lower bound and P vs NP OPEN.**

## IDEA, falsifiers, iteration
Hypothesis: no polynomial-size exact original-variable-only flat CNF representation exists for arbitrary high-width GF(2) rows, even when the rows are independent. Also, no universal polynomial proof-to-proof translation from **all** historical semantic R_mix341 mixed refutations to ordinary Resolution can preserve original strict3 sources, because published expander-Tseitin formulas separate these systems.
Four falsifiers tested: (F1) an entailed clause omits a variable of one parity row; (F2) cross-block clauses compress the direct product; (F3) compact gate 3-CNF lacks unique extension; (F4) polynomial mixed-to-RES backtranslation is compatible with exponential Resolution hardness and linear mixed proofs. All fail by exact arguments. F1-F3 checked finitely as additional controls.

## Family / theorem / encoding / known shortcut / gap ledger
1. **Published odd Tseitin on cubic expanders (Urquhart 1987; Ben-Sasson--Wigderson 2001).** For each vertex v with incident-edge Boolean variables a,b,c, give the four *proper* width-three clauses that forbid parity other than an odd-total charge chi_v. A cubic graph of h vertices gives 3h/2 variables, 4h clauses, encoded length O(h log h) bits. Every unrestricted shared-DAG ordinary Resolution refutation needs 2^{Omega(h)} nodes for a constant-expansion family. However historical semantic R_mix341 AND3 factors (three charged merges per vertex) plus paid GF(2) additions (h-1) refute in 4h-1 nodes; see LSPV-2/341. This is a valid known shortcut, not arbitrary-algorithm hardness. Historical accepted-byte checker remains unauthenticated.
2. **Braun bit PHP (arXiv:2609.23015v2, revised 2026-11-03).** n=2^ell holes, n+1 pigeons, n*binom(n+1,2) clauses of width 2ell, each forbidding one pair of pigeons both equal to a hole. A published, Lean-formalized but not established by independent specialist peer review Res(XOR) bound is >exp(n/(32768 ell^2)) for ell>=32 on the *wide* CNF in unrestricted DAG-like Res(XOR). Standard private splitter strict3 conversion uses 2ell-2 clauses and 2ell-3 fresh variables per wide clause. Neither this conversion nor an ER shortcut transfers the published lower bound to mixed R_mix341. LSPV-1/453 and /457 construct separate-ER proof transport and shortcut controls.
3. **Independent rank-r parity row validation control, NOT a SAT-hard or UNSAT candidate.** r disjoint equations of width d>=3. Exact original-only CNF clause minimum r*2^(d-1), but compact proper-3-CNF existential encoding has 4r(d-2) clauses and r(d-3) fresh XOR2 gate variables, with unique extension.

## Theorem 462.1 (exact original-only flat CNF minimum)
Let H on r disjoint blocks X_j, each of d Boolean variables, require XOR(X_j)=b_j. Any equivalent CNF K using only the rd original variables and no auxiliaries must have at least

$$
|K|\ge r2^{d-1}.
$$

This is attained by the r*2^(d-1) canonical full-width forbidden-assignment clauses.

**Proof.** Any non-tautological clause implied by a single parity row must contain all d variables: falsify a shorter clause and choose the omitted variable to satisfy that parity row. Thus an entailed full-width row clause excludes exactly one wrong-parity assignment. For any clause C implied by the conjunction of disjoint rows, partition C into its block-local portions C_j. If no row entailed its local C_j, independent satisfying assignments for each row could falsify every C_j simultaneously. Hence some row entails a full-width local clause. For each row j and its 2^(d-1) wrong-parity assignments a, take a global witness violating just that row (all other rows satisfied). An implied clause false on this witness must be supported by row j; it cannot also be false on any witness violating only a different row. Nor can it exclude two wrong assignments for the same row. There are r*2^(d-1) such distinct witness obligations; each needs a distinct clause. QED. This counts **representation size**, not UNSAT proof work.

## Theorem 462.2 (exact existential compact representation)
For a d-variable row, introduce d-3 fresh successive XOR2 intermediate variables and express each gate z=u XOR v by its four forbidding strict width-three clauses. Express the final triple parity by four more strict width-three clauses. For d=3 the final triple is the whole row. There are exactly 4(d-2) proper width-three clauses and d-3 fresh gates per row. Each original assignment determines a unique gate valuation; the final four clauses accept iff the required parity holds. Thus for r disjoint rows:

$$
H_{r,d}(x)\iff\exists z\ T_{r,d}(x,z).
$$

The existential encoding is not an exactly equivalent same-variable flat CNF and does not establish a historical native paid-DEF/LOCAL-CONVERT byte rule.

## Corollary 462.3 (no polynomial full mixed-to-RES backtranslation)
For cubic expander odd-Tseitin strict3 sources F_h, the prior semantic R_mix341 proof D_h has W_R(D_h)=4h-1 paid nodes while every ordinary Resolution proof has >=2^(ch) nodes for a constant c>0. Since |F_h|=O(h log h), there is **no polynomial p** universally bounding the size of a source-preserving ordinary Resolution backtranslation of *every legal semantic R_mix341 proof* D by p(|F|+W_R(D)). Applying such a translator to D_h would contradict a published Resolution lower bound. This is an exact negative simulation result, **not** a mixed-system lower bound. It does not exclude non-Resolution proof targets or provide a B3 implication.

## Independent computational controls
Exhaustively checked 12 finite (r,d) cases, r in {1,2,3}, 3<=d<=9 and rd<=15, **55,800 original assignments**, verifying flat/compact/exact row equivalence and 2^(r(d-1)) satisfying original assignments. An independent Node.js checker reconstructed 3 selected fixture sets from truth tables, passed **10,860 assertions** and rejected **15 hostile mutations**. Its original failed trials were corrected for ES-module syntax and independent enumeration order. Included cases: (r,d)=(1,9), 256 versus 28 clauses and 6 gates; (3,5), 48 versus 36 and 6 gates. These are SAT control families; no finite refutation hardness is asserted. Historical authoritative R_mix341 or FRAT-XOR checker was not run.

For encoded variable IDs O(rd), flat original-only CNF requires Theta(rd 2^d log(rd+2)) bits while the strict3 existential encoding uses O(rd log(rd+2)) bits. The exhaustive verifier intentionally takes up to 2^(rd) assignments and is not a FLMV-compatible algorithmic bound. Logical distinct-node work, proof bits, actual search/construction, failed trials, parsing, output, verification, retrieval/recomputation and peak RAM remain distinct.

## Exact source review
Project: governing refocus SHA c3889a3e, historical /341 SHA c87acd11, latest LSPV-3/461 handoff SHA 535a33d0, LSPV-1/453 ER compiler SHA 6e3a7b1, LSPV-1/454 SHA d607da8, LSPV-1/457 SHA 45b79b3, LSPV-5 REFEREE361 SHA f0ce638, current issue #3, Grok 2026-11-06_1718 SHA 6a1e805, Claude TPORT-0002 SHA 1f9fc727. Required repositories: konard/p-vs-np/scripts/proof_status.json SHA 93b77ed; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693e; meelgroup/frat-xor/format.md SHA 986a21a (clause-to-XOR step requires explicit provenance hints); peitl/short-proof/README.md SHA 93d2090; tanyongkiam/cake_lpr/README.md SHA e94f45e. Braun Lean claim kbr-/math-research/formalization/claims/BitPHPExponential.lean SHA c222191a and BitPHPClauseTransfer.lean SHA b67ff0a. Primary papers: Urquhart, JACM 34 (1987), DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, JACM 48 (2001), DOI 10.1145/375827.375835; Braun arXiv:2609.23015v2; Cook-Reckhow 1979, Buss 1987. Indexed web searches performed, no separate Google-branded search. No source is authority for the missing historical byte grammar.

## Remaining exact obstacle
Neither the known strict3 Tseitin separation nor the parity normal-form cost proves superpolynomial minimum work across *all* historical native mixed inferences. No noncircular B3 has been supplied. Need original-source-authenticated exported/private ports, LOCAL-CONVERT payload and positional facet grammar, together with a different invariant stable under all legal shortcuts. Root main.tex not edited; five role identities, 2 Route A/3 Route B allocation, schedules and historical weights unchanged. P vs NP OPEN.
