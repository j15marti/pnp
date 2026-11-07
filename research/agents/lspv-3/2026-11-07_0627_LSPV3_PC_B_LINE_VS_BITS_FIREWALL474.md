# LSPV-3/474: Linear polynomial-calculus proof lines versus exponentially large explicit evidence

**2026-11-07 06:27 PST | Route B | PROVED/RESTRICTED for a DISTINCT multilinear Boolean-quotient calculus PC_B; COMPUTATIONAL original-source tests; P versus NP OPEN.**

**Tracked:** [P2-D1], [P2-D2], [P2-B1], [P2-C3], [P2-B2], [P2-L3-473]; new [P2-L3-474]. **Historical accepted-byte R_mix341, its weights, B3 and unrestricted Wbar_R are NOT resolved.**

## IDEA: one repair and four falsifiers

Hypothesis: Even on an established family with proof-system-specific lower bounds, minimizing the number of inference lines in a *different* Boolean-algebraic calculus need not control explicit proof bits or any physical time/space schedule. A source-authenticated linear-line construction should reveal a concrete model/cost boundary.

Predeclared falsifiers: (1) hidden use of polynomial-by-polynomial multiplication instead of declared paid MUL-by-original-variable and binary LIN; (2) a source axiom not derivable from its exact signed strict-3CNF clause; (3) a nonconstant or incorrect final line on odd-charge UNSAT sources or a false contradiction on an even-charge SAT source; (4) any uncharged Boolean reduction silently attributed to fixed historical R_mix341 or ordinary sparse PC.

## SEARCH: established source families and known systems

**Exact 3-CNF encoding.** For a connected cubic graph G=(V,E) with h vertices, put one Boolean variable x_e on each edge, n=3h/2. For each vertex v and each of the four incident-edge assignments whose parity differs from a charge chi(v), add the proper signed width-three clause falsified by exactly that assignment. Hence m=4h original clauses and explicit literal-index encoding N=O(h log h) bits. The formula is UNSAT for odd total charge, and SAT for even charge on connected graphs. K4, K3,3 and cube below are **finite controls, not individually certified asymptotically hard expander instances**. Ordinary shared-DAG Resolution, Cook's extended Resolution, GF(2) Tseitin shortcuts, AND3 and all legal shared-DAG strategies remain mandatory controls.

**Literature read.** M. Mikša and J. Nordström, *A Generalized Method for Proving Polynomial Calculus Degree Lower Bounds*, Journal of the ACM 71(6), art. 37 (2024), DOI 10.1145/3675668, defines PC/PCR size as the sum of expanded monomial occurrences, and separately defines *length* as the count of lines. Their §2.2 notes that converting multilinear PC into standard PC may need exponentially many Boolean-axiom applications, so the two models must NOT be silently equated for size/work. Earlier CCC 2015 DOI 10.4230/LIPIcs.CCC.2015.467. Haken, *The Intractability of Resolution* (1985), is restricted to Resolution/PHP; Chvátal–Szemerédi, *Many Hard Examples for Resolution* (1988), concerns random 3CNF in ordinary Resolution. No cited restricted lower bound establishes hardness against all SAT algorithms.

**Project continuity actually read:** both complete root trackers; issue #3; AGENTS.md, CODEX.md, repo pnp-research SKILL; historical Nov. 2 worst-case-minimum handoff; LSPV-3/473 report/handoff; LSPV-1/473 and /476; LSPV-5/410; GROKPROOF/2026-11-07_1220_PROGRESS.md; research/agents/claude/world-ledger/README.md. **External exact files read:** konard/p-vs-np scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea; meelgroup/frat-xor format.md blob 986a21aa and cake_xlrup/README.md blob c71de809; tanyongkiam/cake_lpr README.md blob e94f45e9; openai/math README.md blob cc5b0a03. These supply techniques/proof-format contrasts, but not accepted historical R_mix341 bytes. Search keywords: "multilinear polynomial calculus boolean axioms size", "Tseitin parity characteristic polynomial calculus", "resolution hard random 3-CNF". Google-branded independent search was unavailable; web research search was used. Neither official external checker nor native /341 checker was executed.

## ITERATE: explicit new scope and proof

Define a **distinct** calculus PC_B(K) for any fixed field K over the Boolean quotient ring R=K[x_1,...,x_n]/(x_i^2-x_i). A line is its unique multilinear polynomial. Original source clause C_j becomes source polynomial c_j=product of its three falsity indicators: x_i for negative literal, 1-x_i for positive literal. Original source axioms are available as initial lines; their parsing/encoding is externally charged. **Only paid rules** (unit weights in this distinct experiment) are binary `LIN(P,Q;a,b)=aP+bQ` and unary `MUL(P;i)=x_iP`. Multiplication is automatically reduced to multilinear form by the DISTINCT rule semantics. It is not authorized as a free historical R_mix341 operation.

**Theorem 474.1 (PROVED/RESTRICTED).** Every UNSAT strict 3-CNF with m>=1 source clauses admits a PC_B(K) source-indexed refutation with at most 8(m-1) paid inference lines. This is an upper bound on this **distinct** calculus, not the full mixed-system minimum.

**Proof.** Start with P_1=c_1 and set Q_j=P_(j-1)c_j, P_j=P_(j-1)+c_j-Q_j. Construct Q_j by multiplying P_(j-1) successively by the three literal-falsity factors. Factor x_i costs one MUL. Factor 1-x_i costs MUL to obtain x_iQ and LIN to subtract it from Q, so at most six paid steps. Two additional LIN steps produce P_j. The identities hold in R:
$$
P_j=1-\prod_{i=1}^j(1-c_i).
$$
Since F is UNSAT, for every Boolean assignment at least one c_i=1, so P_m evaluates identically to 1. Multilinear evaluation on the Boolean cube is injective over any field, hence P_m=1 syntactically in R. Every reference is earlier in the acyclic source-authenticated DAG. QED.

**Theorem 474.2 (PROVED/RESTRICTED).** For k disjoint positive strict 3-clauses, this specific ordered construction has exactly 7^k+1 distinct monomials in P_k over GF(3). Indeed each factor 1-c_i has seven nonconstant monomials and no constant term; on disjoint supports their product has 7^k distinct monomials without cancellation; outer 1 adds one. This is exponential *explicit evidence in a particular linear-line construction*, NOT a lower bound on every possible proof. Appending an eight-clause contradictory core on three fresh variables yields an UNSAT full source retaining this costly prefix in this ordering, but a different refutation can use the tiny core and avoid the cost.

## Independent original-source certificate checks

Python stdlib producer serialized every signed original clause, SOURCE, MUL and LIN line with original source index, earlier references and full GF(3) multilinear coefficients. An independently implemented Node.js verifier rebuilt the signed original local Tseitin CNF, reconstructed clause polynomial axioms using truth-table Möbius inversion, verified every line with separate dense GF(3) arithmetic, checked original DIMACS SHA256, enumerated all source assignments and tested corruptions. **1,447,235 assertions passed; 48 corruption controls rejected.** The public self-contained compact JavaScript replay passed 9,373 checks and three source deletion controls.

| Graph/charge | n original vars | m original 3-clauses | SAT models | Paid PC_B lines | Peak monomials/line | Cumulative monomials |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| K4 odd | 6 | 16 | 0 | 96 | 33 | 1,297 |
| K4 even | 6 | 16 | 8 | 97 | 52 | 1,573 |
| K3,3 odd | 9 | 24 | 0 | 148 | 450 | 20,546 |
| K3,3 even | 9 | 24 | 16 | 149 | 511 | 27,504 |
| cube odd | 12 | 32 | 0 | 200 | 2,162 | 65,791 |
| cube even | 12 | 32 | 32 | 201 | 4,095 | 119,417 |

Odd terminal polynomials are 1. Even terminal polynomials are not 1 and are NOT refutations. Prefix monomial counts k=1..5 were 8,50,344,2402,16808, exactly 7^k+1. Full 1.9MB original-source fixtures, Python producer, separately implemented Node verifier, raw result ledger and hashes are retained in the downloadable reproducibility archive. Published GitHub code is a separate compact replay, not the authoritative historical checker.

## Actual work, evidence bits, span and semantic limits

A source is m clauses and n original variables. The constructed logical DAG has m initial source lines and <=8(m-1) paid lines. Each explicitly expanded line can contain up to 2^n monomials; direct variable masks use n bits each, plus field coefficients and reference/operation bits. A safe explicit certificate upper bound is O(m 2^n(n+log m)) bits; naive explicit manipulation costs at most O(m n 2^n) bit/word operations up to conventional index factors for fixed coefficients. Sequential logical critical-path span O(m), not minimum span. Materializing and retaining the entire proof may take O(m 2^n n) simultaneous bits; recomputing changes machine-time/peak-space tradeoffs, not the ideal DAG minimum. Construction, failed attempts, parsing, source/index/head reads, conversion, storage, retrieval, checking, publication, and all-phase peak space are charged for implemented algorithms. The finite producer's elapsed time and RSS are in the archived raw ledger.

**Scientific boundary:** Boolean reduction x_i^2=x_i is built into PC_B; ordinary PC requires explicit Boolean axioms with potentially expensive normalization; historical R_mix341 has not authenticated these rule bytes. Thus neither a size lower bound for another proof system nor this distinct calculus's short proof is automatically a result about W_Rmix341, machine time, or B3. This is a typed non-equivalence warning, **not a LEGAL native counterexample**. The fixed weights, five agents and root main.tex are untouched.

**Status:** KNOWN theorem = published PC/Resolution model-specific facts; PROVED/RESTRICTED = above explicit quotient-calculus lemmas; COMPUTATIONAL = original-source fixtures and independent checker; OPEN = [P2-D1], [P2-C3], [P2-B1], [P2-B2] and P versus NP. Next target: authenticate historical R_mix341 accepted source, paid DEF facets and LOCAL-CONVERT output records, testing whether any of the quotient arithmetic is legally native with exact bit/node overhead.