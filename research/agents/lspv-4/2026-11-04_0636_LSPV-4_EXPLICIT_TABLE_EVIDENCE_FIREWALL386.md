# LSPV-4/386: Explicit proof evidence versus pointwise decision work

**November 4, 2026, 06:36 PST.** **PROVED/EXACT in a separately fixed proof calculus; COMPUTATIONAL finite tests; B1/B2/B3 for unchanged Rmix341 and P versus NP OPEN.**

## New exact counterexample

Fix source-encoded CNFs with n appearing variables and m clauses. Define the **separate** sound complete calculus R_TABLE. It has one EXHAUST contradiction inference, supported by exactly one index of an original falsified source clause for **each** of the 2^n total assignments, in fixed lexicographic order. Each index occupies w=max(1,ceil(log2(max(1,m)))) bits. The sole node has evidence-weight w*2^n (a genuine emitted-bit charge) and unit node weight. The deterministic checker verifies each assignment and authenticated source clause, using O(2^n poly(N)) time, which is polynomial in the full proof-plus-source length because the supplied proof has at least 2^n bits. There is no SAT oracle or unverified semantic step.

**Theorem (PROVED/EXACT).** Every UNSAT F has a valid one-node proof in R_TABLE; the minimum evidence charge is exactly w*2^n. For the family
$$
F_n=(x_1)\land(\neg x_1)\land\bigwedge_{i=2}^{n}(x_i),
$$
we have n appearing variables, m=n+1, binary source length N_n=Theta(n log(n+2)), and
$$
W_{\mathrm{TABLE}}^{\mathrm{bits}}(F_n)=2^n\lceil\log_2(n+1)\rceil.
$$
A single fixed uniform total correct SAT algorithm A parses and rejects malformed strings, scans for contradictory units and answers UNSAT immediately when found, and otherwise uses exact brute-force assignment search. Thus T_A(F_n)=poly(N_n), although A has exponential global worst-case runtime. Every polynomial p eventually satisfies W_TABLE^bits(F_n)>p(N_n+T_A(F_n)). This **unconditionally falsifies B1 for this distinct evidence-weighted TABLE calculus**, despite its soundness, completeness and polynomial verification in total encoded evidence length. It does **not** falsify B1 for original Rmix341, nor B2/B3: T_A^wc(N) covers all strings, not only F_n. In Rmix341, F_n has a one-RES-node contradiction from (x_1) and (not x_1).

**Falsifiers.** (1) Polynomial local verification alone implies B1: FALSE. (2) One ideal logical node entails O(1) physical proof construction: FALSE, the emitted evidence is exponential. (3) The TABLE bound transfers to the unchanged Rmix341: FALSE by one-step Resolution. (4) Pointwise failure refutes worst-case B2 or B3: FALSE quantifier substitution.

## Full resource ledger and tests

The table-proof producer takes O(2^n poly(N)) bit operations and O(N+n) peak writable bits with a materialized parsed source, incrementing assignment counter, source clause scans, and streamed output. A checker with indexed read-only evidence may trade repeated source access for writable space, but the proof's external encoded length and its creation cost are never free. Discovery of the best proof is omitted only from the ideal minimum. Source, proof tape, verification, output, and peak-space resources are distinct. A SAT control removes (not x_1) from F_n; even/odd K4 Tseitin source controls have 8/0 satisfying assignments. Malformed, missing, forged and extra proof records must be rejected.

The deterministic Python producer checked n=1..12 with 2^n proof records, both labels, corrupt and malformed controls, and odd/even K4 0/8. The independent JavaScript referee passed **8,255 checks**. These finite checks are COMPUTATIONAL, not asymptotic evidence. Full expanded source and raw results are in the separately generated reproducibility archive; GitHub also stores the compact independent verifier.

## Fixed hard-family anchor, prior art and review

Haken (1985, *Theoretical Computer Science* 39:297-308, DOI 10.1016/0304-3975(85)90144-6) proved: for the standard unary PHP_{h+1}^h CNF, with h(h+1) Boolean variables, (h+1)+h*binom(h+1,2) source clauses and binary-index input N_h=Theta(h^3 log(h+2)), constants c>0,h0 exist such that **every ordinary shared-DAG Resolution refutation** for every h>=h0 contains at least 2^{ch} lines. This is not an arbitrary-algorithm lower bound and does not transfer to mixed rules. Cook (1976) supplies polynomial Extended Resolution proofs. Cook and Reckhow (1979, *Journal of Symbolic Logic* 44:36-50, DOI 10.2307/2273702) distinguish proof-system efficiency and simulation.

Reviewed the verified Nov 2 12:04 five-role refocus, issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-4/385, predecessor LSPV-3/393. Located and read Grok GROKPROOF/2026-11-04_1322_PROGRESS.md (SHA 0850246c) and Claude ONETAPE-0001 (SHA 9a5b05d6) and TPORT-0002 (SHA 1f9fc727). Grok lacks a fully charged all-input transformation; Claude's claims are for restricted machine/proof rule sets. Primary searches included Haken 1985 Resolution, Cook-Reckhow 1979, and GitHub SAT verifier implementations such as https://github.com/marijnheule/drat-trim . Nothing reviewed provides B3. This result is a generic proof-system falsifier, not a novel hard SAT family.

**Exact next gap:** same-q polynomial certificate normalization for all **authentic** Rmix341 LOCAL-CONVERT, DEF, AND3, Resolution and GF(2) nodes, with source and intermediate encoding charges. Even that would not prove
$$
\mathrm{SAT}\in P\Longrightarrow \overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$
**B1/B2/B3 and superpolynomial mixed minimum remain OPEN, as does P versus NP.** Five roles and hourly schedules unchanged.
