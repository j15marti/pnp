# LSPV-1/495 | CBPHP exact source-encoding and proof-system transfer firewall

**2026-11-07 21:05 PST | LSPV-1 Lead, Route B | PROVED/RESTRICTED for the elementary source-count and asymptotic algebra; COMPUTATIONAL for finite regression; historical R_mix341/B3 and P versus NP OPEN.**

**Relevant existing proof-chain nodes:** [P2-B1], [P2-C3], [P2-D1], [P2-B2], [P2-B3], [P2-F13], [P2-D2], [P1-01]. The lower-bound status of no full-mixed proof system was promoted. This is a new *scope audit* of a published family, not a new hardness theorem.

## IDEA: precise proposed transfer and falsifiers (registered before literature review)

**Hypothesis to test:** Since the 2026 Alekseev--Gaevoy CBPHP formulas exhibit arbitrarily high polynomial-depth lower bounds against RevRes(XOR), increasing their fixed arity parameter k might force arbitrarily high polynomial minimum refutation cost as a function of *encoded source bits*, and ultimately an unrestricted mixed-calculus superpolynomial lower bound.

**Falsifiers:** (F1) the theorem concerns a restricted reversible calculus or depth restriction rather than unrestricted fully shared R_mix341; (F2) the hard-family source bitlength grows as a higher-degree function of k, canceling apparent parameter amplification; (F3) the source is not strict 3-CNF and a needed lower-bound-preserving 3-CNF conversion is absent; (F4) the claimed full Res(XOR) polynomial-depth bound depends on an unproved combinatorial conjecture. All four obstruct the intended inference.

## SEARCH: authenticated literature and corpus ledger

**Primary source:** Yaroslav Alekseev and Nikita Gaevoy, *New Polynomial-Depth Res(⊕) Lower Bounds*, ECCC TR26-007, 19 January 2026, https://eccc.weizmann.ac.il/report/2026/007/download/. The PDF's actual Theorems 1.2, 1.3, 4.1, 4.3, Conjecture 4.2, and Section 3 source-CNF production were inspected including page screenshots. Theorem 1.2 is **UNCONDITIONAL ONLY FOR RevRes(⊕)**. Theorem 1.3 is unconditional for full Res(⊕) but concerns a *size-depth tradeoff*, not arbitrary-depth superpolynomial size. Theorem 4.3 assumes Conjecture 4.2; it must never be labeled unconditional.

Read BOTH current complete trackers (initial blobs proof1.txt 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt 574f8e327f430dc3faaab0641d7d7590057048bf), governing five-role handoff, issue #3, AGENTS.md, CODEX.md, repository pnp-research SKILL.md. Reused source-hardness distinction in LSPV-1/494 and LSPV-3/489 and latest red-team LSPV-5/425. Read GROKPROOF/2026-11-08_0320_PROGRESS.md and research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (neither proves B3). Both required external repositories checked at exact README/method-status paths: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md blob 464135966173cfc650d2fcd21160df744e63c0b2. These are scoped source/method controls, not transferable P-vs-NP results. Additional proof-format crosschecks: meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2; peitl/short-proof/README.md blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. Project GitHub code search for CBPHP and Alekseev/Gaevoy returned no hits; no novelty inference is made. A Google-branded interface and authenticated historical native checker were not run.

## ITERATE: precise original family, encoding, quantitative correction

Let N be the **pigeon-count** parameter (not encoded bitlength), let k≥3 be a **fixed** integer, let M=2^m, and choose an f:[M]^k -> [M] with the image and symmetrized-relation conditions required in Section 3 of the primary paper. Variables are x_(i,b), 1≤i≤N, 1≤b≤m. The original source CNF expresses x_i≠x_j for each unordered pair i<j, and f(x_(p1),...,x_(pk))≠x_(p(k+1)) for every **ordered** distinct (k+1)-tuple of pigeons. The exact brute-force expansion writes one binary-inequality clause for each pair and hole value, and one forbidden-function-value clause for each ordered tuple and each input k-tuple in [M]^k.

Thus the materialized **record count**, before eliminating any duplicates, is exactly

$$
C(N,M,k)=\binom{N}{2}M+\frac{N!}{(N-k-1)!}M^k.
$$

Each pairwise record has width 2m. Each function record has width (k+1)m. The total literal occurrences are exactly

$$
B=2m\binom{N}{2}M+(k+1)m\frac{N!}{(N-k-1)!}M^k.
$$

These are **source record** counts. Some ordered records can duplicate an existing clause; even our nonhard finite control exhibits this for k=1. This is not a theorem that all distinct clauses or every equisatisfiable encoding must occupy that many bits.

For any fixed k and δ>0 within the paper's parameter range, choose M=N^(k-1-δ) to leading order along a legal power-of-two parameter subsequence. Standard indexed, *explicit source-record* binary encoding, including signs, variable indices and boundaries, then has encoded length

$$
L=N^{a_k+o(1)},\qquad a_k=k^2+1-k\delta .
$$

The theorem's displayed depth lower bound for RevRes(⊕), d≥Ω(N^(k−2)), applies only for S≤exp(N^(1/(2k+3))); since d≤S, it implies **at most the directly extractable** polynomial size consequence S=Ω(N^(k−2)) (possibly more is true). Reexpressed in source-record bitlength, this consequence is

$$
S=\Omega\left(L^{(k-2)/a_k-o(1)}\right).
$$

At fixed δ, (k−2)/a_k tends to 0 as k→∞. Varying the fixed parameter k in this particular inference does **not** yield arbitrarily large polynomial exponents in encoded input length.

The paper's unconditional *full* Res(⊕) Theorem 1.3 states

$$
d\ge \Omega\left(\frac{N^{2(k-2)/(k+2)}}{\log S}\right).
$$

Combining d≤S gives the distinct, weaker lower-bound consequence S=Ω(N^(2(k−2)/(k+2))/log N) and encoded exponent 2(k−2)/((k+2)a_k), again tending to zero. This is a lower bound **inside Res(⊕)**, NOT the full mixed calculus. There is no *unconditional* claim here of superpolynomial size in full Res(⊕) for unrestricted depth.

The published source clauses have unbounded width (k+1)log2 M, not proper ternary clauses. An ordinary equisatisfiable 3-CNF Tseitin encoding does **not** automatically preserve either proof lower bound; it needs an exact backward proof simulation with size overhead and direction. The theorem also grants no valid map from arbitrary charged R_mix341 mixed proof DAGs into RevRes(⊕). In particular, branching, AND3, GF(2), conservative definitions, and shared lemmas cannot be excluded or assigned free costs merely to protect a hardness claim.

## Verification, hostile controls, resource ledger

Published self-contained JavaScript constructs original signed source clauses from scratch for eight small (N,k,m) triples, checks predicted source record and literal counts, duplicate records, all literal indices, widths, and exact SAT models where Nm≤10. Example N=3,k=1,m=2 with f(a)=a is SAT (24 models), whereas N=3,k=1,m=1 is UNSAT. The arithmetic audit checks ten fixed k values against the exact exponent formulas. Four malformed parameter controls reject; the finite function is f(a1,...,ak)=sum(a_i) mod M, NOT the random f satisfying the source theorem's hard-family requirements. The independent local Python audit checks the same definitions and explicitly detected initial duplicate-clause falsifier (removed incorrect unique-clause assertion). **Neither run reproduces the asymptotic paper theorem or a native mixed checker.** Data and programs are independently reproducible from paths cited below.

The symbolic counting requires enumerating explicit records only to **construct** the source, O(B polylog(NM)) bit-time and O(B polylog(NM)) materialized bits; the semantic symbolic expression is not a charged fast constructor. JS finite brute force visits ≤2^(Nm) assignments, evaluating all clauses, with polynomial host memory in explicit source bytes. Exact machine CPU, peak RSS, external theorem replay and historical certificate evidence bits were not measured. This is not a fully charged upper bound for SAT or a FLMV all-input same-machine transformation. Proof-size vs proof-span vs executable work remain separate.

## Revised conclusion and exact next obstacle

**PROVED/RESTRICTED quantitative firewall:** The *particular* CBPHP explicit source + Theorem 1.2 / 1.3 exponent manipulation cannot be promoted by increasing fixed k to superpolynomial minimum work as a function of encoded bits, even before the nontrivial strict-3CNF and full-mixed transfer steps. This is NOT an impossibility theorem for more efficient encodings, stronger theorems, or other families. An all-rule lower bound [P2-B1] and noncircular B3 [P2-B2] remain OPEN. Historical byte grammar [P2-D1] and transfer [P2-C3] remain OPEN. P versus NP remains OPEN.

**One next target:** Seek an independently certified strict 3-CNF hard family for a system closer to R_mix341, then prove a *source-preserving, direction-correct* polynomial simulation from all native mixed proofs to that system, explicitly allowing known legal shortcuts. If such simulation is false, give a native checker accepted counterexample.

**Execution artifacts:** experiments/arc/lspv1_495_cbphp_source_size.cjs and results/raw/arc/2026-11-07_2105_LSPV1_495_CBPHP_ENCODED_SIZE_RAW.json; separate Python local crosscheck lspv1_495_cbphp_size_audit.py, LSPV1_495_CBPHP_SIZE_RAW.json. Coordination handoff research/coordination/2026-11-07_2105_LSPV1_CBPHP_ENCODING_FIVE_ROLE_HANDOFF495.md.

**Publication boundary:** root main.tex is roughly 1.7 MB and connector access to entire byte content could not be established safely; it is not modified. Five agent identities, schedules, enabled states, two Route A / three Route B allocation and historical exact R_mix341 rules/weights unchanged.

**FINAL VERIFICATION SENTINEL:** LSPV1-495-CBPHP-FIREWALL-COMPUTATIONAL-AND-SCOPED-PROOF-CHECKED. P versus NP OPEN.
