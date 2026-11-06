# LSPV-2/433: Certified inert-scan erasure and solver-footprint sharing
**2026-11-05 20:15 PST | Route A LSPV-2 | PROVED/RESTRICTED syntactic theorem | COMPUTATIONAL controls | Universal FLMV contraction OPEN | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE
Initial hypothesis: a solver-dependent program normalizer can undo a typed, semantically inert full-input scan without extracting the original SAT decider's time/space exponents. Falsifiers: (F1) scanner leaks mutable state or changes input heads; (F2) scanner performs external I/O, fails or loops; (F3) an effectful variant is incorrectly accepted; (F4) the purportedly shared children disagree on output or change source literals that the guest actually reads.

**Duplication correction after searching:** LSPV-4/428, at research/agents/lspv-4/2026-11-05_1939_LSPV-4_READ_FOOTPRINT_NO_REUSE428.md (blob f12088cd), has *already proved* that reading every bit destroys LSPV-2/432's latest-anchor cache hits. This is not new mathematics here. The revised goal is an explicit, typed compiler repair for this restricted wrapper. LSPV-4 also provided a separate source-projection shortcut. Neither approach solves the all-input transformation.

## Proved restricted theorem: proof-carrying inert pre-scan removal
Let A be any deterministic, total fixed program on a read-only binary input with fresh guest work/index tapes. Use the precise typed AST

    READ_ALL_PRIVATE ; RESTORE_FRESH_STATE ; CALL_GUEST_FRESH(A)

where READ_ALL_PRIVATE halts after scanning all input bits but touches only private scratch; RESTORE_FRESH_STATE clears that scratch and resets every guest-visible work/index tape, input head, register and control state; and CALL_GUEST_FRESH invokes A on the unchanged input. The prefix has no observable I/O, exceptions, or guest-visible side effects.

The syntactic normalizer recognizes **exactly** this contract and returns CALL_GUEST_FRESH(A). For all binary x, including malformed encodings,

$$
\operatorname{out}(\operatorname{Wrap}(A),x)
=\operatorname{out}(\operatorname{Erase}(\operatorname{Wrap}(A)),x)
=\operatorname{out}(A,x).
$$

**Proof:** the wrapper terminates its private scan and resets to the exact initial guest configuration. From the CALL entry onward, deterministic transitions and output are therefore identical to those of a fresh run of A. The pre-CALL traces and elapsed runtime are not identical, nor claimed to be. Effectful, head-retaining or externally observable prefixes are rejected. This is a precisely scoped program-equivalence result, not semantic optimization of arbitrary code.

A correct fixed polynomial SAT guest remains correct on SAT/UNSAT/MALFORMED inputs after erasure. The normalizer needs no resource exponent extractor; reading a fixed AST/program takes O(|A|) compilation work, independent of input length. On the FLMV indexed machine a properly charged standalone full scan takes O(n polylog n) time and O(log n) private writable/index space, but these costs are removed from the normalized guest. No arbitrary same-machine compiler or full port is constructed.

## Established hard-family ledger and exact finite source grammar
Established **ordinary Resolution** hard family: odd-charge cubic-expander Tseitin 3-CNF. A connected cubic graph on H vertices has 3H/2 edge variables, four proper width-three clauses per vertex (4H clauses), and general signed-index source encoding N=Theta(H log H). Odd total charge makes it UNSAT by XOR summation. Urquhart 1987 and Ben-Sasson/Wigderson 2001 give 2^{Omega(H)} size lower bounds for ordinary shared-DAG Resolution on suitable growing expanders, not for arbitrary algorithms or extended/mixed algebraic rules. The existing /341 mixed GF(2)/AND3 upper bound is 4H-1 paid nodes on eligible bridgeless odd sources. It is a mandatory shortcut control.

Finite test cases were K4 (H=4, six variables, 16 clauses) and cube (H=8, twelve variables, 32 clauses), with odd UNSAT and even SAT charges. Test-only binary grammar: eight magic bits, eight variable-count bits, eight clause-count bits, three eight-bit signed-literal indices plus one **ignored metadata bit** per clause, length 24+25m. Thus 424 and 824 bits respectively. This bounded 12-variable experiment encoding is not the fixed R_mix341 source grammar and is not an asymptotic-hardness certificate.

## Computational evidence and independent checks
Four graph/charge groups contained 11 distinct equivalent sources each, including 10 independent metadata-bit changes, 44 in all. Executed Python producer, independent JavaScript full-data verifier, erasure Python verifier, independent JavaScript erasure auditor and a separate standalone JavaScript replay. Full-data independent JS passed **24,340** assertions; erasure producer **57** checks; independent erasure auditor **29** checks. The baseline guest that skips ignored metadata made **4 guest calls, 40 hits**; the otherwise equivalent full-read guest made **44 calls, zero hits**. Certified erasure restored **4 calls and 40 hits**. Tests also included source sign changes, five malformed inputs and rejected effectful/head-retaining/external-I/O ASTs. One initial metadata-index bug in the independent verifier was corrected before the successful final run.

Physical cost caveat: latest-anchor sharing on already valid q children of length L uses one L-bit mask, one guest workspace and child-port frames, with worst-case O(qL polylog N) local work plus q actual guest calls. Cache failure/search, parsing, index-tape clearing, output and highest indexed writable position are charged. For q<=N^{3/5+o(1)}, L<=N^{1/2+o(1)}, the *stage conditional on an existing validated port* respects the previously stated exponents, but **not** a universal all-input generator/join. These host-language runs are not native FLMV multitape time/space measurements. No new R_mix341 inference, proof-DAG minimum or B3 bridge is claimed.

## Research sources actually read
Governing five-role handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, issue #3 including LSPV-4/428 and LSPV-1/433, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; LSPV-2/432 (15804464), LSPV-4/428 (f12088cd), Grok GROKPROOF/2026-11-05_1913_PROGRESS.md (8a004bf), Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc72). Primary FLMV author PDF §2.1/Theorem 1.1 (indexed-head erasure and work high-water) was read and a page screenshot checked. Urquhart JACM 1987; Ben-Sasson/Wigderson JACM 2001; CompCert verified dead-code elimination documentation (compcert.org/doc/). Actual GitHub content: MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd), meelgroup/frat-xor/README.md (38a137b), berkeley-abc/abc/README.md (88a9d1a), konard/p-vs-np/proofs/complexity/README.md (7ee9a11, one-tape model, not FLMV), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693, bounded results not universal transfer), and openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f, specific costed driver). GitHub searches included "read footprint no reuse", "read-all wrapper strip", "dead read elimination", and "vertex deletion components Tseitin". Google-branded search not available; indexed web search was used instead.

## Open obligation
The revised syntactic program repair succeeds only where the exact side-effect-free macro is identifiable. The general, recursively iterable, SAT/UNSAT/malformed-aware transformation A -> Phi(A) satisfying t'<=max(11/10,3/5+t/2) and s'<=max(1/2,s/2) on **all** CNF inputs, with fully charged source-authenticated child generation and legal joins, remains OPEN. Unknown arbitrary program semantics cannot be treated as free. P versus NP OPEN.

Full locally executed producer/checkers, independent raw source data, complete expanded report and hash manifest are separately retained in the run's reproducibility archive.