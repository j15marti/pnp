# LSPV-2 AFFINE-NONLINEAR-BRANCH371 (2026-11-03 14:12 PST)

**Status:** PROVED/EXACT for a finite-fanin affine-first circuit decomposition and a scoped syntactic proof translation, with external specialist review pending; CONDITIONAL lower-bound corollary assuming Braun 2026; COMPUTATIONAL finite verification. Superpolynomial full-Rmix341 minimum, B1, B2, B3 and P versus NP remain OPEN.

## Established theorem and fixed calculus
Retain the preselected Rmix341, with source-authenticated CNF clauses at zero cost and distinct shared-DAG inference nodes at unit cost: RES, exact AND3, arbitrary-support binary GF(2) XOR, justified LOCAL-CONVERT, and conservative charged two-input gate DEF. Inputs include malformed binary encodings, valid SAT, and valid UNSAT; malformed sources are rejected. W_R(F) is minimum distinct paid-node count and Wbar_R(N) the worst-case minimum over UNSAT CNF binary encodings up to N bits.

For ell >=32 and n=2^ell, Braun's September 2026 bit-PHP Res(XOR) preprint, Theorem 1.1, reports that the standard original source B_ell, with m=n*C(n+1,2) clauses and signed ASCII-DIMACS N=Theta(n^3 ell^2), requires more than exp(n/(32768 ell^2)) total shared-DAG Res(XOR) lines. The original PDF printed page 3 (definition of affine cuts and semantic weakening and the theorem) was inspected. The preprint's Lean 4 proof has not been independently kernel-replayed and external review remains pending. It is a restricted proof-system statement, not a deterministic SAT time lower bound.

## Model-scoped new construction
Consider only the actual Rmix341 proofs whose DEF instructions are paid fresh conservative binary Boolean gates with authenticated slots, whose other semantic factors are extensional over at most three exposed named original-or-paid-gate wires, and whose LOCAL-CONVERT conclusions do not expose uncharged internal wire names to later inference. This is a proper proof subgrammar, not a change in Rmix341. The full circuit-valued LOCAL-CONVERT semantics remains an open issue.

A binary gate is affine iff f(u,v)=c XOR (a AND u) XOR (b AND v), with c,a,b in {0,1}; precisely eight of sixteen truth tables are affine. Let g_nl count nonaffine charged DEF gates, q all paid nodes (including arbitrarily many affine DEF gates), r ordinary RES nodes, x native GF(2) nodes, J other semantic nodes, and k_j the maximum affine rank of all exposed original-input forms at local semantic node j after previous nonlinear gate outputs have been fixed. Write k_* = max k_j, or zero when J is empty. The fixed local-wire grammar has k_j <=3.

**Lemma (PROVED/EXACT, scoped circuit syntax):** Every acyclic conservative two-input DEF circuit with g_nl nonaffine gates and arbitrarily many affine gates can be specialized by an adaptive binary decision tree with at most 4^g_nl terminal branches. Every test is an affine equation in the original inputs, and every output on each branch is an affine form or constant. Process gates topologically: affine gates preserve affine forms with no test, while a nonlinear gate branches on its two current affine inputs, creates at most four children, and becomes constant. Exact GF(2) elimination drops inconsistent/forced branches. The leaves partition the original assignments.

**Theorem (PROVED/EXACT within stated proper proof subgrammar; specialist review pending):** Every such proof of original UNSAT F with m source clauses gives a refutation of the SAME original F in DAG Res(XOR), with total lines

$$
S_⊕(F) ≤ m + 4^{g_nl} (m+2r+2x+ Σ_{j∈J} 2^{k_j+1}+2).
$$

Consequently,

$$
S_⊕(F) ≤ 2^{2g_nl+k_*}(4m+8q+8).
$$

Proof: on each terminal affine branch, substitute the exact affine/constant values for all DEF outputs. Defining clauses become tautological; RES becomes an affine cut or a sound degenerate weakening, XOR additions take at most two native Res(XOR) lines, and each other extensional local node expands into canonical assignment-blocking clauses on at most k_j independent affine forms with at most 2^{k_j+1} lines. Guard the restricted refutation by the disjunction of complements of its affine branch tests; original source guards are obtained by charged semantic weakenings. Derive a blocker at each leaf; glue sibling blockers using legal complementary-affine cuts. There are at most 4^g_nl leaves and one less internal cuts. Shared DAG costs once per translated branch. Input/proof bits, checking work and machine memory are separate. No source-independent definition axiom is imported into the target.

**Conditional consequence of Braun:** Every covered proof of standard bit-PHP obeys

$$
2g_nl + k_* + log_2(4m+8q+8) > n/(32768 ell^2 ln 2).
$$

For polynomial q and k_*≤3, necessarily g_nl=Ω(n/ell²). For g_nl=o(n/ell²) and bounded k_*, q=exp(Ω(n/ell²)) even if polynomially or exponentially many affine DEF gates were used and charged. This does NOT imply a large full-Rmix341 minimum: known Extended Resolution proofs exploit nonlinear extensions, and the unrestricted LOCAL-CONVERT circuit-wire grammar is not covered. B1, B2 and the weakest sufficient B3 remain unproved.

## Falsification-first and finite certificate checks
F1: a nonlinear output remains undetermined on some leaf; F2: 48 affine gates cause exponentially many branches; F3: guarded affine cuts are illegal. The symbolic construction settles F1-F3 in the grammar; a separately written independent checker verified their finite certificates. F4: downstream legal use of uncharged internal LOCAL-CONVERT wires violates the premises; OPEN for full Rmix341.

A deterministic Python producer and separately authored no-import JavaScript checker generated and replayed 24 source-authenticated certificates for the UNSAT control (x)&(y)&(~x|~y), with the SAT control obtained by deleting the third source clause. They checked 558 total Res(XOR) proof records, 85 affine-branch leaves, 26,828 independent assertions, and rejected 12 corrupted structures. With 48 affine gates and no nonlinear ones the branching is 1 leaf and 8 printed lines; adding AND gives 4 leaves and 26 lines; two independent nonlinear gates give 16 leaves and 98 lines. Some gates are not needed for the short source contradiction, so these tests certify the compiler's affine-branch/guard mechanism and proof validity, NOT shortest mixed proofs or a general executable mixed-proof compiler. n≤6 exhaustive semantic checks are finite, not asymptotics.

## Logical work, Grok/Claude, corpus audit and next gap
A compiler actually generating the translation must read the entire input proof and source, handle all source indices and gate payloads, perform GF(2) feasibility checks, materialize all branch proofs and output and check the completed proof. A conservative charged runtime is 4^{g_nl} 2^{O(k_*)} poly(L+N+q) for input proof payload bits L; no FLMV time-space domination or cheap proof search follows. Peak simultaneous memory must include every phase, with s'≤max{rho,eta,lambda,lambda*s}; temporary N-bit allocation gives rho≥1.

Reviewed the fixed 2026-11-02 12:04 refocus at verified blob 033b54b87b7cbe94912af5cf67daa52859143a07; GitHub issue #3; AGENTS.md, CODEX.md, pnp-research skill; Rmix341 original report 341, LSPV-2 346/369/370, LSPV-1 BRAUN-PAID-GATE-BUDGET370, LSPV-3 BOUNDED-INTERFACE367 and LSPV-5 REFEREE299. The LSPV-1 result already bounded all paid AND gates by 4^g; this work refines it by eliminating arbitrarily many affine gate definitions with no exponential factor, while retaining a broad two-input nonaffine basis. No claim of academic novelty is made beyond this specific scoped statement.

The actual Grok folder contains GROKPROOF/2026-11-03_2214_PROGRESS.md, blob 59fe73c20473bd6bc20500cf58d75e42519aee88. Its all-input fully charged ARC/FLMV contraction remains explicitly OPEN. The actual Claude folder contains research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex, blob b7150bb9ed964affd5fb90ecd24b0aa35d600bf9, and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67. Its portfolio barrier concerns a specified alternation-trading rule system, not B3. The prior Grok 1217 upper-to-lower per-query runtime inference remains invalid. Neither other-agent report supplies an unrestricted SAT separation.

Primary source: Braun, An exponential lower bound for the bit pigeonhole principle in resolution over parities, arXiv:2609.23015 (September 19, 2026). Other sources: Itsykson and Sokolov (2020), Cook (1976), Cook and Reckhow (1979), Gocht and Nordström (2022). Searches of repository prior work found LSPV-1 370 as a directly relevant predecessor; searches in github.com/openai showed unrelated uses of resolution. A complete repository checkout and preflight was unavailable due to DNS failure in the local runtime.

Next: authenticate the exact full LOCAL-CONVERT grammar, including access to named internal wires, then extend or falsify the gate-elimination compiler. Independently, establish a noncircular machine-correctness/reflection implication for the SAME fixed calculus B3. P versus NP remains OPEN.
