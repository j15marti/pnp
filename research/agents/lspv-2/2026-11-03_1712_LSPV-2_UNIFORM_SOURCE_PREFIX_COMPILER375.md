# LSPV-2/375: Uniform source-prefix compiler, native Rmix341 proof cost 4h-1 to 1

**November 3, 2026, 17:12 PST (America/Los_Angeles).** PROVED/EXACT elementary encoder theorem using prior LSPV-2/341; COMPUTATIONAL independently checked finite controls. External specialist review pending. **P versus NP OPEN.** No task, schedule, rule or weight change.

## Published starting point, not a machine lower bound

Urquhart, *Hard Examples for Resolution*, JACM 34(1) (1987), 209-219, DOI 10.1145/7531.8928, and Ben-Sasson--Wigderson, *Short Proofs Are Narrow*, JACM 48(2) (2001), 149-169, DOI 10.1145/375827.375835, establish for suitable bounded-degree expander odd-charge Tseitin CNF families with graph size h that **every ordinary unrestricted shared-DAG Resolution proof** uses at least 2^(c h) lines for an absolute c>0 and sufficiently large members. A cubic graph source has n=3h/2 edge variables, m=4h signed width-3 clauses and N=Theta(h log(h+2)) binary index-encoded input bits. This is a statement about ordinary Resolution proof length, not arbitrary uniform SAT Turing machines, Res(oplus), Extended Resolution, or Rmix341.

The same fixed Rmix341 retains zero-cost authenticated original CNF clauses and unit-paid distinct at-most-binary-premise shared-DAG RES, AND3, GF(2), justified LOCAL-CONVERT and conservative two-input DEF nodes. The **prior exact theorem LSPV-2/341** proves W_Rmix341(F_h)=4h-1 for every connected simple bridgeless cubic odd-charge Tseitin CNF. This is the mandatory short GF(2) countercontrol, not a new result.

## One uniform, all-general-CNF, label-preserving encoder

On every **valid** canonical DIMACS CNF F with declared n variables and ordered clause list C_1,...,C_m, let P(F) authenticate that the entire source is exactly the four-parity-clause-per-vertex encoding of a connected simple bridgeless cubic graph with odd total charge. It groups the source clauses by sorted 3-variable supports; checks the complete forbidden parity quartet at each support; checks every edge variable occurs in exactly two groups; checks connectivity and bridges; then XORs reconstructed charge bits. This is a fixed polynomial-time procedure for **all n and m**. Recognition cannot wrongly label a SAT input UNSAT because parity incidence cancellation proves every accepted F inconsistent.

With a fresh variable z=x_(n+1), define **one fixed encoder**:

$$
E(F)=
\begin{cases}
F\land(z)\land(\neg z),&P(F)=1,\\
F\land(z),&P(F)=0.
\end{cases}
$$

Original clauses and every signed original occurrence remain in exactly their original list positions; only the DIMACS header and final one or two *new source clauses* change. All valid SAT/UNSAT labels are preserved. In the P(F)=0 branch each satisfying original assignment uniquely extends by z=1. In the P(F)=1 branch both original and output have no satisfying assignments. No general SAT oracle or size-dependent advice is used.

The encoded output has O(N) bits and is computed in polynomial bit time and space, accounting for complete parsing, source reads, quartet validation, graph connectivity and bridge tests, output production, auxiliary arrays and simultaneous live memory. The original clause sequence is recoverable in polynomial time from an output in E's image by checking its last one or two fresh units, deleting the suffix, restoring the header, and recomputing E for authentication. This **source-prefix reversible** statement is for canonical DIMACS clause records: arbitrary source whitespace/comments are normalized, so raw-byte invertibility is not claimed. Malformed inputs are rejected by a total wrapper and never called UNSAT.

### Exact same-system logical-cost contrast

For every original F_h in the recognized odd cubic bridgeless family,

$$
\boxed{W_{R_{\rm mix341}}(F_h)=4h-1,\qquad W_{R_{\rm mix341}}(E(F_h))=1.}
$$

The first equality is **prior project theorem 341**, valid over all finite mixed proofs and free optimal proof selection. The second is exact because new authenticated source units (z) and (not z) resolve to the empty clause by one unit-paid RES node, and no original source clause is already empty. No zero-node refutation exists. Both encodings are explicit length Theta(h log h) in the family, up to constant factors and logarithmic header adjustment. Their exact source-derived proof minima nevertheless differ by an unbounded factor.

**Critical source firewall:** E(F) is a *new source formula*. Appending two contradictory sources is **not** a legal inference from F in the same Rmix341 proof. This does not contradict the exact native W_R(F_h) or establish an O(1) decision algorithm for the original input. The encoder must first authenticate the recognized class. When physically materialized, outputting the original source already costs Omega(N) bit writes.

### Physical source-observation floor

In the **separate fixed-width independently addressable source-sign encoding** audited by LSPV-3 SIGNED-INPUT-QUERY377, every one of 12h original sign-bit flips of F_h yields a valid SAT neighbor. Therefore any fixed deterministic *label-preserving input compiler* on that grammar, including E, must observe all 12h sign fields on F_h or it would emit the identical output on an opposite-label neighbor. Internal lazy circuits and shared DAGs do not avoid the observation requirement. This is Omega(h) original-bit observations and only O(N) in the source length. Do **not** silently transplant this exact sign-position count to ASCII DIMACS, where adding/removing a minus shifts text.

## Falsification target and exact implication

Suppose a proposed invariant I is both (i) unchanged by every **uniform polynomial-time, all-CNF-label-preserving, clause-prefix-reversible** compiler and (ii) a lower bound on the native paid-node minimum of **every output presentation**. E is one allowed compiler, so

$$
I(F_h)=I(E(F_h))\le W_R(E(F_h))=1.
$$

This **FALSIFIES** such an encoding-invariant minimum-proof-node lower bound even for fixed Rmix341 and an unbounded hard-source family. It does **not** falsify a provenance-rooted invariant which charges constructing, validating, accessing and materializing E(F), or a common-polynomial cost-reflection envelope whose polynomial also includes the original source length. Nor does it transfer an ordinary Resolution lower bound to every algorithm.

F1: P(F) might accept an SAT input, **FALSIFIED** by authenticated quartet structure and odd incidence parity. F2: keeping all original clauses preserves minimum proof cost, **FALSIFIED** by the added opposite units. F3: one logical proof node implies constant machine work, **FALSIFIED** by input authentication and source output costs. F4: this disproves B3 or superpolynomial mixed worst-case hardness, **FALSIFIED AS AN INFERENCE**: original mixed W was already linear, and the transformation is a changed source problem.

For all uniform total correct all-binary-string SAT deciders A, B1 asks for polynomial p_A bounding W_R(F) by N+T_A(F) pointwise; B2 asks for p_A bounding Wbar_R(N) using T_A^wc(N) over all strings of length <=N; B3 asks SAT in P => Wbar_Rmix341(N) polynomial in N. **All B1/B2/B3 remain OPEN**, as does superpolynomial Wbar_Rmix341. Neither a short proof on a transformed formula nor a decider fast on a recognized island resolves them.

## Controls, proof status and independent checking

Full Python producer and separately implemented no-import JavaScript verifier, retained in complete local reproducibility package, tested prior known K4, K3,3, cube and Petersen cubic graphs. (h,m)=(4,16),(6,24),(8,32),(10,40). Native exact mixed costs inherited from 341: **15,23,31,39**; transformed exact costs: **1,1,1,1**. Python: **861** assertions, **336** single occurrence-sign branch checks, odd/even controls, six general CNF controls (SAT, UNSAT, empty clause, tautology, duplicates, empty CNF), nine malformed rejections. Independent JavaScript checker: **1,103** assertions, source quartets, original clause prefix, exact source-unit RES pivots, both labels and **six corrupted proof-data rejections**. Finite enumeration cap n<=15 originals, n<=16 compiled. No finite search is called a global minimum; the global 4h-1 statement comes from theorem 341.

Measured host producer: 1.51 s wall, 96,908 KiB RSS; verifier: 0.12 s, 30,708 KiB RSS. These are process measurements, not word-RAM or FLMV inequalities. All-phase time/space budgets include parsing, source/index/head accesses, branch discovery, representation conversion, output/checking, cache and peak simultaneous live memory. The original memory envelope s'<=max{rho,eta,lambda,lambda*s} remains unchanged, with allocate/free phases charged.

Public compact replay: experiments/arc/lspv2_375_source_prefix_public.js (independently executed after GitHub readback; K4/K3,3/cube and four malformed controls). Full producer, independent verifier, 336 mutation controls and complete JSON fixture are in the attached reproducibility archive. Public summary is a **ledger**, not a substitute for that full fixture.

## Corpus and duplication audit

Read exact November 2 five-role contract at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, blob 033b54b87b7cbe94912af5cf67daa52859143a07; issue #3; AGENTS.md; CODEX.md; repo pnp-research SKILL; LSPV-2/341, /372, /373, /374; LSPV-3/377, /378; LSPV-4/347, /371; LSPV-5/289 and /324. LSPV-5/289 **already establishes** a recognizable both-label easy island bypass; LSPV-5/324 already identifies source-prefix encoders and the missing **common polynomial envelope**, but uses a family E_k with index-dependent envelopes to expose nonuniform optimization. LSPV-2/372 already rejects extensional-only proof-cost invariants. The restricted increment here is a **single fixed encoder** acting on all general CNFs with a same-Rmix341 exact 4h-1-to-1 minimum and an explicit charged source-recovery implementation. No independent literature novelty is claimed.

The actual folders were found through GitHub directory listing and read. GROKPROOF/2026-11-03_2214_PROGRESS.md, blob 59fe73c20473bd6bc20500cf58d75e42519aee88, leaves its arbitrary-decider fully charged contraction OPEN. research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67, establishes a barrier only for a specified alternation-trading rule system and does not supply B3. Claude 0266, blob 694c1c8169d9a193397b94e6ee572c476e639a94, records separate Grok factor-of-four and citation discrepancies. These claims were assessed within their scopes, not accepted as authorities.

Literature checked: Urquhart 1987 (DOI 10.1145/7531.8928), Ben-Sasson--Wigderson 2001 (DOI 10.1145/375827.375835), and classical certificate/query sensitivity. Searches for corresponding github.com/openai implementations found no model-matched compiler; search nonmatches are not absence proofs. A complete local repository checkout was inaccessible, so skill preflight.py and scripts/check_research_reports.py were not run. Root main.tex must be reconciled only after a complete authenticated blob is recovered. P versus NP OPEN.

**Next exact gap:** a source-rooted **common-polynomial cost-reflection** rule for paid but arbitrarily compact circuit/GF(2) conversions, plus a separate computation-correctness argument sufficient for B3. This example rules out simply taking the cheapest semantically equivalent or source-prefix presentation as an algorithm-independent logical-work lower bound.
