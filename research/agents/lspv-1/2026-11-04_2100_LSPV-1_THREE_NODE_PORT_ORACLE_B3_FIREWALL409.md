# LSPV-1/409 | Three-node DEF/affine-port test and oracle-relative B3 firewall
**2026-11-04 21:00 PST | General SAT Lower-Bound Lead.** Status: PROVED/EXACT only for explicitly defined alternative rule completions; KNOWN oracle-relative countermodel for ordinary Resolution; COMPUTATIONAL tests. Native R_mix341 grammar, B1/B2/B3, superpolynomial mixed worst-case minimum, P versus NP **OPEN**.

## IDEA before search: two falsifiable hypotheses
(1) Original /341 does not explicitly say whether a paid fresh XOR2 DEF's own defining equation is a public GF(2) row. Predict a trace of only three charged nodes distinguishing an export-enabled completion Splus and a private-row completion Sminus, with no hidden wire or SAT oracle. Falsifiers: exact original grammar settles export, the same trace is unsound under a SAT source, an illegal identifier reuse, or corrupted row is accepted.
(2) Test whether a universal decider-runtime-to-refutation-size B2/B3 derivation could be black-box/relativizing. Predict that an oracle deciding **all** SAT inputs in polynomial time coexists with Haken's exponential ordinary-Resolution PHP lower bound. Falsifiers: oracle is not globally polynomial, source encoding changes, or theorem claimed for full mixed R rather than ordinary Resolution.

## SEARCH and duplication check
Read governing November 2 handoff (Git blob c3889a3e), original /341 R_mix341 description in research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (c87acd11), current coordination issue #3, LSPV-1/408, LSPV-2/407, LSPV-3/410, LSPV-4/402, REFEREE352, AGENTS.md, CODEX.md, and the repo research skill. The original /341 has free authentic DIMACS sources and paid unit RES/AND3/XOR/LOCAL-CONVERT/DEF nodes with at most two antecedents, but **does not serialize** a DEF-to-AFFINE export selector or LOCAL public/private port encoding. LSPV-2/407 already gives a SIX-node grammar discriminator for three alternative completions. The present THREE-node record is a strictly shorter discriminator of its first undecided facet, **not** a new proof that the native grammar is complete.

Actually read GROKPROOF/2026-11-05_0315_PROGRESS.md (blob 2c21a1eb), Claude TPORT-0002 (1f9fc727) and Claude ONETAPE-0001 (9a5b05d6). These reports do not supply B3. General-web queries included "Baker Gill Solovay Relativizations of the P=?NP Question", "PSPACE complete oracle P^O NP^O equality", "Haken pigeonhole ordinary Resolution exponential", "Cook Reckhow relative efficiency proof systems", "Cook short pigeonhole Extended Resolution", "P=NP EF p-bounded". Primary publisher pages read: Baker--Gill--Solovay, SIAM J. Comput. 1975; Cook--Reckhow, JSL 1979; Buss 1987 Frege pigeonhole and Cook's author bibliography. Direct Google-branded search was unavailable, so general web and authenticated GitHub were used. Github.com/openai searches: "DEF GF2 row", "CookLevin", "ExecCNFNodeSearchCosts". Read the complete openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f44ad49370d1b812e862c03c3a91d7f836), a concrete execution/cost theorem, **not** arbitrary same-R proof translation.

## ITERATE A: a three-node typed-port discriminator
Let F be ANY proper signed CNF over original x,y. Introduce separately paid, globally fresh **conservative** binary gates a and b with identical inputs:
$$
D_a:\ a=x\oplus y,\qquad D_b:\ b=x\oplus y.
$$
The third paid node purports to XOR the defining GF(2) rows:
$$
(a+x+y=0)\oplus(b+x+y=0)\quad\Longrightarrow\quad a+b=0\quad(\mathrm{GF}(2)).
$$
**Splus** explicitly exports a fresh paid XOR/XNOR DEF's exact defining row to the typed GF(2) rule: it accepts this three-node record. **Sminus** keeps every DEF equation a private definitional facet, so its third XOR has no eligible public antecedent and is rejected. Both preserve the very same original-assignment projections and all other native narrative rules. Both are proposed DIFFERENT completions of an *under-specified* record grammar; neither is silently adopted as the actual R_mix341. A DEF never asserts that its output is TRUE. The conclusion concerns legal **proof-record syntax**, NOT a demonstrated difference of global minimum W_R(F).

The mutation b=NOT(x XOR y) correctly requires RHS 1 in the summed row; a+b=0 must then be rejected. Malformed input and duplicate-wire, forged-parent, wrong-mask and wrong-row tests also reject.

**COMPUTATIONAL:** Exhausted all 256 source subsets of eight proper non-tautological signed two-variable clauses, 95 SAT and 161 UNSAT. Python producer executed 782 assertion groups; the separately authored JS checker reconstructed all truth assignments with 920 assertion groups. Fourteen hostile malformed/corrupted controls rejected. Primary complete raw JSON SHA256 ddc335259f28bbf43b6c98cd469155dc48d6a87cc93c336160ae1aebfbec10fb. The three-node record is valid under Splus for every source model, not a refutation; accepting it for an UNSAT source is vacuously sound. Finite tests are not a new theorem about the untouched native rule.

## ITERATE B: genuinely worst-case ORACLE countermodel, restricted to ordinary Resolution
Let O=TQBF, a PSPACE-complete oracle. By the classical oracle construction and Savitch's theorem,
$$
P^O=NP^O=PSPACE.
$$
There is ONE fixed, total deterministic oracle machine A^O that parses and rejects malformed binary inputs and, on every valid encoded CNF F, writes the existential QBF (exists x_1 ... x_v)F(x), submits ONE oracle query, and returns its exact SAT/UNSAT answer. Parsing, query construction, indexed access and output cost polynomial oracle time on **ALL binary strings**. The oracle itself hides PSPACE work and is not an ordinary physical SAT algorithm.

Fix R_Res, authentic ordinary shared-DAG binary Resolution, one paid unit per derived resolvent. Haken (1985) proves that for every sufficiently large h every refutation of the explicit unary pigeonhole CNF PHP_(h+1,h) needs at least 2^(c h) nodes/lines for some c>0. This family has h(h+1) Boolean variables, (h+1)+h*binom(h+1,2)=Theta(h^3) signed clauses and bit-length N_h=Theta(h^3 log h) under a fixed signed binary-index literal-list encoding. Consequently, for **every** polynomial p, infinitely many h satisfy
$$
\overline W_{R_\mathrm{Res}}(N_h)>p\bigl(N_h+T_{A^O}^{wc}(N_h)\bigr).
$$
So even the *worst-case* analogue of B2, not merely pointwise B1, FAILS in this relativized oracle model for **ordinary unrelativized Resolution**. Likewise the implication SAT in P^O => polynomial Wbar_Res is false. This synthesis of KNOWN Haken/Baker--Gill--Solovay facts shows why a generic black-box transfer which continues to apply after giving machines SAT/TQBF oracles while leaving R fixed cannot prove the project's B3. It does **NOT** refute unrelativized B2/B3 for the stronger R_mix341 or provide any mixed superpolynomial lower bound. Extended Resolution has polynomial PHP certificates, and GF(2) provides shortcuts on odd Tseitin.

**COMPUTATIONAL control:** Exhaustively verified PHP_h UNSAT and one-collision-clause-deletion SAT for h=1,2,3. Six malformed source-size parameters rejected. Finite brute force does not verify Haken's asymptotic theorem and the abstract TQBF oracle was NOT executed.

## Cost and quantifier discipline
In Splus, the illustrative trace has q=3 charged nodes; evidence includes source, names, two full gate definitions and GF(2) mask/RHS. A canonical encoding uses O(N+q log(N+q)) bits on this fixed three-node template, with polynomial check time and space in the supplied evidence. No general q-to-bits normalizer is proved. The oracle-relative countermodel uses genuine uniform A^O and T_A^wc over SAT/UNSAT/malformed inputs. Its oracle-query length is polynomial but oracle computation is free **only inside the declared relativized model**. The quantified failure is an EXISTS oracle machine violating B2 in ordinary Resolution; it says nothing about unrelativized B3 for Rmix341, and it is not a lower bound on all physical algorithms. Neither ideal proof optimizer nor proof-discovery cost is charged to W_R.

## Exact next tasks
LSPV-2/LSPV-3 must extract and freeze a normatively authorized byte-level DEF-row export / LOCAL public-port / individual DEF-clause selector rule, then run this 3-node and prior 6-node test under **the exact same unchanged calculus**. LSPV-4 must charge all evidence bytes, checking, temporary buffers, source-index access and peak space. LSPV-5 challenge whether Splus and Sminus truly satisfy original narrative and the oracle quantifiers. LSPV-1 remains responsible for noncircular *unrelativized same-system* B3, requiring a mechanism beyond oracle decision answers or rejecting traces. B1/B2/B3, full mixed superpolynomial Wbar_R, and P versus NP remain OPEN.

## Numbered primary references
[1] Haken, A. (1985). The Intractability of Resolution. Theoretical Computer Science 39, 297-308.
[2] Cook, S. A. (1976). A Short Proof of the Pigeon Hole Principle Using Extended Resolution. SIGACT News 8(4), 28-32.
[3] Cook, S. A.; Reckhow, R. A. (1979). The Relative Efficiency of Propositional Proof Systems. JSL 44, 36-50. https://doi.org/10.2307/2273702
[4] Baker, T.; Gill, J.; Solovay, R. (1975). Relativizations of the P=?NP Question. SIAM J. Computing 4, 431-442. https://doi.org/10.1137/0204037
[5] Buss, S. R. (1987). Polynomial Size Proofs of the Propositional Pigeonhole Principle. JSL 52, 916-927.
[6] Prior project: LSPV-2/407 report, LSPV-3/410 handoff, REFEREE352 and LSPV-1/408. Exact paths above.
