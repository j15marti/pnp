# LSPV-4/489 | Fixed-record guarded source grammar closure versus semantic recursive failure

**2026-11-08 00:40 PST | Route A LSPV-4 resource auditor | PROVED/RESTRICTED syntax/semantic results plus COMPUTATIONAL tests | P versus NP OPEN.**

**Affected exact node:** [P2-A4] material evidence. [P2-A2] and [P2-A5] remain OPEN. [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] also OPEN. Historical R_mix341 rules and weights untouched.

## IDEA: one hypothesis and four precise falsifiers

Investigate whether the LSPV-2/487 fixed-eight normalizer and guarded projection, originally emitting a separately formatted 16m-clause guest source, can be encoded as an ACTUAL input accepted by its very same canonical source parser, with locally indexed output bits and complete physical charges. Determine whether this syntactic closure suffices to iterate the SAT decision signal.

F1: The old two-field guest already parses as a canonical source. F2: Adding a new self-delimiting width header necessarily requires a large source directory or nonlocal rank/select. F3: empty, repeated, tautological, large-ID, malformed, or odd/even original 3-CNF cases violate source agreement. F4: after repair the second guarded source's NEW outer z2=0 feasibility still equals SAT(F).

IDEA -> SEARCH -> ITERATE: F1 is refuted on all 136 test cases, since the prior guest deliberately omitted the parser's unary-width header. F2/F3 are refuted in the fixed-record grammar by a new bit-local header/record constructor and finite tests. F4 is refuted exactly: z2=0 is SAT for all F, including UNSAT F, because the first guarded J(F) is always SAT. This last phenomenon is an ALREADY KNOWN guard-saturation phenomenon in earlier project work. This run supplies a precise common-grammar source construction and verifies a two-level concrete witness, NOT a novel general guard theorem.

## Governing and source review

Read both complete root proof trackers, current issue #3 including peer comments, Nov 2 five-role handoff, AGENTS.md, CODEX.md, pnp-research SKILL.md and mode notes. Read actual LSPV-2/487 report plus source experiments/arc/lspv2_487_fixed8_guard.js blob 661cd7317719728af516969c081ea31ced1f0dfc; LSPV-2/462,/464,/486, LSPV-4/460,/488 and LSPV-1/498. Read GROKPROOF/2026-11-08_0320_PROGRESS.md blob 72edb3140d8ed798d0905a827f85d3428728e396 and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a. Earlier guard projection and saturation work includes LSPV-3/481 and LSPV-5/126; no rediscovery claim.

Primary source examined visually and textually: Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6), 2005, DOI 10.1145/1101821.1101822, https://lance.fortnow.com/papers/files/tst.pdf, Section 2.1 PDF page 4 and Corollary 5.8 PDF page 18. This specifies native INPUT/INDEX head jumps and erasures, write-only OUTPUT, and charged non-index work-tape high water. Search also inspected Pang, A Degree--Size Relation for Resolution over Polynomials, arXiv:2610.00837v2 (24 October 2026), whose restricted Res(PC) bound is NOT a machine bound.

Targeted repository files and exact Git blobs: konard/p-vs-np/scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite machine model); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 (promise/projection control); meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (different proof grammar); openai/math/README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae (research manuscript data, not authority). Public indexed web and GitHub connector were used; no separate Google-branded client, Lean proof replay, native FLMV interpreter or authoritative historical R_mix341 checker was executed.

## Fixed grammar and exact repair: Theorem 489.A (PROVED/RESTRICTED)

Let F contain m records of width 0..3, including empty, duplicate or tautological signed clauses. Declared variable ceiling is 0<=n<=3m+3. Set

$$
b(n,m)=\lceil\log_2(128(n+m+3))\rceil,\qquad N=3b+1+3m(b+2).
$$

The source string starts with unary 1^b0, then b-bit n and m, then m triple slots (present, sign, b-bit unsigned ID). Absent slots are zero, trailing only; a present ID is in [1,n]. The previous LSPV-2/487 guest format has two b-bit header fields only, with no initial 1^b0, and is not a member of this SAME self-describing grammar. This does NOT invalidate its claimed separate guest format.

Keep the EXACT LSPV-2/487 normalized source clauses and IDs: original x_v -> 4v; normalization private p_(j,k)=4(3j+1+k)+1; guarded clause-pair private a_r=4(r+1)+2; common guard z=3. Eight proper width-three clauses per input record, followed by two guarded clauses per normalized record, give precisely m'=16m clauses. Define

$$
n'=\begin{cases}3&m=0,\\32m+2&m\ge1,\end{cases}
\quad b'=b(n',16m),\quad
M=3b'+1+48m(b'+2).
$$

For m>=1, all introduced and old remapped IDs are <=32m+2 since n<=3m+3. Also 32m+2<=48m+3=3m'+3. For m=0, n'=3 and m'=0 are legal. Thus the repaired J(F) outputs exactly the SAME accepted unary-header, field, length and source-ID grammar as its input.

To recover an output bit i, compute b', m', n' in O(log N) counters; classify i into its unary prefix, header fields or 16m fixed-length records. Division by 16, 2 and the record stride identifies original clause index j, one of eight normalized rows r, and the guarded pair half. Only three original source slots need to be fetched by native indexed reads. Finite algebraic case logic generates each of the three new literals; out-of-range guest bits are blank. A conservative SYMBOLIC bound, including binary address formation, guest-to-parent INDEX refills, head restoration and long ID arithmetic, is O(log^3(N+2)) time and O(log(N+2)) live WORK+INDEX for one bit, provided the original fixed source grammar. Original parsing takes O(N polylog N) time and O(log N) space. A full M-bit guest retained on charged WORK would instead use Omega(M) peak; writing M bits on OUTPUT does not make them a new INPUT for free. No actual arbitrary-A native guest tape simulation is claimed.

The inherited local truth-table proof is exact:

$$
\exists p\, H(F)(x,p)\iff F(x),
$$

$$
\exists_{x,p,a}J(F)(z=0)\iff\operatorname{SAT}(F),
\qquad J(F)(z=1)\text{ is satisfiable}.
$$

This is a SAT-decision / existential equivalence, not a proof-size lower-bound-preserving reduction between Res, Res(XOR), Res(PC), R_mix341 and arbitrary algorithms.

## Iteration and physical obstruction: Theorem 489.B (PROVED/RESTRICTED)

A second application J(J(F)) is now SYNTACTICALLY valid under the same parser. But its new outer port satisfies

$$
\exists_{\mathrm{private}}J(J(F))(z_2=0)
\iff\operatorname{SAT}(J(F))=1
$$

for every original F. In particular the empty-clause contradiction F=(empty clause) becomes a guaranteed satisfiable z2=0 outer projection. The original SAT(F) information remains only at a PINNED INNER z1=0 port, which requires separate fully charged source operations to access. Thus the syntactic fix does NOT supply a recursively iterable SAT label reduction.

For m>=1, the clause count multiplies by 16 on each iteration and the encoded ratio M/N ->16 as m grows. The output is Theta(N), not N^(1/2). Neither [P2-A2] time-contraction nor [P2-A5] recursive closure follows. This is a restricted falsifier of naive iterate-J source construction only, not of every possible solver-intensional A -> Phi(A).

## Executed reproducibility and hard-family control

Published standalone independent V8/Node producer experiments/arc/lspv4_489_fixedrecord_selfclosure.cjs, Git blob 848ed3574e4b18e8225fcd6f91f0f7253cff85b8; raw results/raw/arc/2026-11-08_0040_LSPV4_489_FIXEDRECORD_SELF_CLOSURE_RAW.json, blob 5bc54da4ba22a84456e4074dcdac34970cc4fdf6. The exact fetched GitHub script was independently replayed, and its generated JSON matches the committed raw JSON.

Verified: 136 original width<=3 source variants and repaired grammar parses; 16 ORIGINAL signed K4 cubic-Tseitin 3-CNFs (8 SAT and 8 UNSAT from exhaustive 64-input model evaluation), 4,096 output K4 signed strict-three clauses, 345,809 exact per-bit indexed virtual comparisons, 408 malformed/corrupted-source rejections, and 512 individually checked original clause truths in explicit satisfying witnesses of the SECOND guard J(J(F)) for F SAT and F UNSAT. 693,575 V8 assertions passed; zero failures. The 136 legacy two-field formats were all rejected as canonical inputs. Native FLMV transition-by-transition instruction counts and guest A execution were NOT measured.

Known growing hard family: odd-charge cubic-expander Tseitin original source with H vertices, 3H/2 edge variables, 4H signed proper-three clauses and binary length Theta(H log H). Urquhart (1987) and Ben-Sasson/Wigderson (2001) give exponential ordinary shared-DAG Resolution size lower bounds on appropriate expanders. Affine GF(2) charge sum is an efficient decision shortcut. K4 tests above are finite original-source controls, NOT a certified asymptotically hard set. Pang 2026 random strict3 theorem is a separately restricted proof-system control. No transformation of a published proof lower bound into arbitrary SAT computation is asserted.

## All-phase resource ledger and status

Source/index/head reads: O(N polylog N) validation, O(log^3 N) per virtual output bit. Child description: arithmetic, no full guest materialization. Output: if streamed O(M) write minimum, if retained charged WORK Omega(M). Failed policy search and restarts: NOT IMPLEMENTED, cannot be counted as zero in a prospective solver. Guest A simulation, repeated calls, work-tape high-water, cache, reference/retrieval, join and recomputation: NOT IMPLEMENTED and hence NO generic complexity claim. Branch sharing: read-only original source is aliased rather than duplicated, but any shared computed lemma/branch result would require separately proved validity and charged storage. Logical proof DAG nodes, certificate bits and parallel critical path: NONE constructed; source bit generation is not an R_mix341 proof.

**Advance:** Exact same-grammar bit-local fixed-record guarded source repair and a concrete two-level saturation control, not a SAT speedup. **Verification:** symbolic proof, original K4 SAT/UNSAT and 693575 finite checks, exact published-code replay. **Publication:** role-owned report/code/raw/handoff; conflict-safe tracker/issue receipt follows. **Remaining gap:** all-input, same-FLMV-machine, solver-dependent, recursively iterable Phi(A) meeting t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2). Route B [P2-B1]/[P2-B2] also OPEN. **P versus NP OPEN.**
