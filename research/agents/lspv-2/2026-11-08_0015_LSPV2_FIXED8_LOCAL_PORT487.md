# LSPV-2/487 | Fixed-eight proper-3 normalization for a guarded SAT projection

**2026-11-08 00:15 PST | Route A primary | PROVED/RESTRICTED symbolic theorem + COMPUTATIONAL | P versus NP OPEN.**

**Tracker nodes:** [P2-A4] scoped source-encoding evidence; [P2-A2], [P2-A5] all-input, same-machine contraction and recursion OPEN. Cross-chain [P1-01], [P1-03], [P1-04] and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

## IDEA and precommitted falsifiers

Initial claim: LSPV-3/481 and LSPV-4/488 already established an always-SAT, strict-proper 3CNF guarded one-port projection, but their ORIGINAL input grammar was proper width three. Add a constant-eight-output gadget to normalize any canonical clause of width zero through three, including repeated variables, tautologies and empty clauses, without clause-dependent output addresses. The resulting locally indexed source constructor is NOT a SAT solver, not a source-only projector and not the missing Phi(A).

F1: an empty or unary clause is not exactly existentially equivalent to its gadget. F2: repeating/opposite signs or auxiliary aliasing breaks strict propriety. F3: skipped tautologies require prefix counting and destroy polylog per-bit access. F4: parser or native FLMV indexed emulation incurs hidden Omega(N) writable space. Local symbolic theorem and finite tests refute F1-F3; a native FLMV instruction-level execution for F4 remains OPEN.

## SEARCH / exact continuity and prior art

Read both complete root trackers; issue #3 including latest LSPV-1/498, LSPV-3/492, LSPV-4/488 and LSPV-5/428 comments; November 2 five-role handoff; AGENTS.md, CODEX.md and repository pnp-research skill; actual LSPV-2/486, LSPV-4/488 and its five-role handoff, LSPV-1/497, LSPV-3/492; GROKPROOF/2026-11-08_0320_PROGRESS.md and Claude 2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex. The one-port guard is PREVIOUSLY KNOWN (LSPV-3/481); no novelty is asserted for it or generic clause padding.

Primary source: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, Sections 2.1 and 3.1, Theorem 3.1 and Corollary 5.8, https://lance.fortnow.com/papers/files/tst.pdf. Its low-space proof REQUIRES locally computable input bits, not just ordinary equisatisfiability. Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2 (November 3, 2026) has > exp(n/(32768 ell^2)) clauses for ORIGINAL bit-PHP in DAG Res(XOR), n=2^ell, ell>=32; no automatic transfer to the strict3 splitter. Pang arXiv:2610.00837v2 is restricted Res(PC), not arbitrary SAT computation.

Actual external files read: konard/p-vs-np/scripts/proof_status.json SHA 93b77ed3d8fe456f81c690035f45f07910a247f2 (formal status only); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5 and projection_discovery_barrier.py SHA 3ea94ff951916665e12dc8e0bb8221f4f5e49be5 (earlier general-CNF projection barrier); MassimoLauria/cnfgen/cnfgen/families/tseitin.py SHA 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (parity generator); meelgroup/frat-xor/format.md SHA 986a21aa92b62f844ef1fce852193142c41b2b1f (different proof language); openai/math/README.md SHA cc5b0a03bca6c742f045d683b6647a6f44ef2cae (research data not authority). GitHub and general indexed web search available; no distinct Google-branded client, native FLMV interpreter or official historical R_mix341 checker executed.

## Theorem 487.1: fixed-eight proper-3 normalization

Let F consist of m clauses, each with 0 to 3 literal occurrences. Repeated variable IDs, contradictory pairs and an empty clause are allowed. For each clause C_j, reserve three private auxiliaries p0,p1,p2, disjoint from all original variables and from all other clauses. Output EXACTLY EIGHT strictly proper width-three clauses per original clause:

1. If the clause contains both signs of one variable, output eight positive fresh triples (p0 OR p1 OR p2). Their existential projection is TRUE.
2. Otherwise deduplicate same-sign repetitions, yielding effective width w.
3. w=3: retain the original clause plus seven harmless positive fresh triples.
4. w=2: (l1 OR l2 OR p0) and (l1 OR l2 OR NOT p0), plus six harmless triples.
5. w=1: all four clauses (l1 OR +/-p0 OR +/-p1), plus four harmless triples.
6. w=0: all eight sign patterns (+/-p0 OR +/-p1 OR +/-p2). Their conjunction is UNSAT.

The private-triple elimination is exact for EACH assignment to original variables:

$$
\forall x\quad \exists p\ H(F)(x,p)\iff F(x).
$$

This follows by elementary truth-table elimination clause by clause; private supports ensure conjunction commutes with existential elimination. Every generated clause has three distinct variable IDs. The count is fixed even for tautologies, so addresses of later output clauses never shift.

**Optimality in the per-clause fixed-count scheme:** eight is necessary if EMPTY input clauses must be represented by proper width-three clauses: each proper clause forbids exactly one eighth of all assignments; a union of <=7 such forbidden sets cannot cover all assignments. Our eight sign patterns meet this lower bound. This is only a minimum number of target SOURCE clauses for the empty-clause gadget, NOT a lower bound on SAT computation or R_mix341 refutation work.

## Theorem 487.2: guarded source J(F)

For each proper clause D_r=(u_r OR v_r OR w_r) in H(F), add a fresh auxiliary a_r and one common z, producing two ORIGINAL proper width-three clauses:

$$
(u_r\vee v_r\vee a_r)\wedge(\neg a_r\vee w_r\vee z).
$$

For each fixed assignment to u,v,w,z, existential elimination of a gives (u OR v OR w OR z). Therefore J(F), with exactly 16m clauses, is ALWAYS SAT, and

$$
\exists_{x,p,a} J(F)(z=0)\iff\operatorname{SAT}(F),
\qquad
\exists_{x,p,a}J(F)(z=1)=1.
$$

This identity covers ALL valid input clauses of width <=3, including empty clauses and tautologies. It establishes a semantic relation, NOT a cheap algorithm for discovering the port. It transfers no ordinary-Resolution, Res(XOR), Res(PC), mixed-calculus, or all-machine lower bound merely by equisatisfiability.

## Exact fixed-record encoding and bit provider

Use a canonical 3CNF source encoding with m clause records, 0<=n<=3m+3 variable IDs, each record containing three fixed (present, negative, b-bit unsigned ID) fields, unused fields all zero and trailing. Let b=ceil(log2(128(n+m+3))). The bit string begins with unary 1^b 0 then b-bit n,m and m records. Its exact length is

$$
N=3b+1+3m(b+2).
$$

A malformed binary input is rejected after header, length, ID, presence-order and sign checks. The bound n<=3m+3 ensures b=O(log(N+2)); this is an explicit fixed-record representation restriction.

Separate IDs by residues modulo four: source variables 4v, normalized private p_{j,k}=4(3j+1+k)+1, guard a_r=4(r+1)+2 and z=3. Thus there is no collision. Encode the output with two b-bit header fields and 16m records, using declared maximum variable ID max(4n,4(3m+1)+1,4(8m+1)+2,3). Its exact bit length is

$$
M=2b+16m\cdot3(b+2)=\Theta(N)
$$

for valid nontrivial canonical inputs. Given output bit index i, elementary binary quotients determine source clause j, one of eight normalized slots, which guard half, literal position and field offset. Only three fixed-address original literal records are consulted. There are no skipped-clause prefix sums. This implies a SYMBOLIC indexed bit transducer using O(polylog N) time per bit, O(log N) writable WORK+INDEX, provided the specified fixed-record model and paid tape/head/index implementation. A conservative O(log^3 N) time per query bound suffices. Source validation can be streamed in O(N polylog N) time, O(log N) writable space. Materializing all M bits has at least M output writes and O(M polylog N) time.

Do NOT identify the JavaScript runtime, which materializes arrays/strings, with this symbolic sublinear-space indexed machine. Native FLMV instruction-level conversion and every actual A child-call, recursive stack and exponent budget remain OPEN.

## ITERATE: executed independent controls and exact scope

Published JS experiments/arc/lspv2_487_fixed8_guard.js blob 661cd7317719728af516969c081ea31ced1f0dfc was fetched BACK from GitHub and executed as the exact returned source in V8, passing **47,232 assertions**, 94 local source assignments, 228 global truth assignments, **46,294 complete output-bit comparisons** and 263 malformed rejections; eight SAT and eight UNSAT original signed K4 Tseitin charge sources, with 16 proper source clauses and 256 guarded clauses each. Fixed random seed 487.

Independently authored Python experiments/arc/lspv2_487_independent.py exhaustively tests ALL 359 clauses over 1-3 variables with width<=3, giving 2,442 local existential truth checks and 312,576 guard-clause truth checks, as well as the same K4 8/8 split. For original bit-PHP at ell=2, five pigeons into four holes, it checks all 1,024 assignments against 40 width-four source collision clauses, then checks the existing private-chain 80-clause proper strict3 splitter. This finite ell=2 control is OUTSIDE Braun's ell>=32 hard-family theorem and is NOT a transferred proof-size lower bound. Committed JS checks the resulting 80-source-clause split bitPHP through **3,842 indexed sampled bits** of its 65,310-bit, 1,280-clause guarded source.

Raw counters: results/raw/arc/2026-11-08_0015_LSPV2_487_FIXED8_GUARD_RAW.json. Full proof/source tests were executed, but no FLMV native interpreter, machine conversion or historic mixed R_mix341 checker was executed.

## Family / theorem / encoding / shortcut / transfer ledger

| Family | Exact encoding and parameter | Certified theorem/model | Known shortcut | Missing direction |
| --- | --- | --- | --- | --- |
| Cubic K4 Tseitin | 6 edge variables, 16 proper source clauses; charge parity over 4 vertices | Odd charge UNSAT by GF(2) cancellation; 8/8 SAT/UNSAT, NOT an asymptotic hard family | Shared GF(2), local AND3 (prior LSPV-2/341, LSPV-3/492) | Native historical grammar [P2-D1] OPEN |
| Bit-PHP | n=2^ell holes, n+1 pigeons, original collision clauses of width 2ell; private-chain strict3 decision encoding | Braun arXiv:2609.23015v2: >exp(n/(32768 ell^2)) ORIGINAL DAG Res(XOR) clauses for ell>=32, not general SAT algorithms | Extension-variable and shared-DAG proof controls | Lower-bound preservation from original to split and full mixed system [P2-C3] OPEN |
| Canonical arbitrary width<=3 CNF | Fixed three-slot input, m clauses including empty/repeats; exact H=8m and J=16m original proper 3-clauses | Here: exact existential equivalence, indexable source bits, **no** proof-computation lower bound | Fixed-record, no prefix shifts, one shared guard z | FLMV source completeness import and same-machine all-input Phi(A) [P2-A2/P2-A5] OPEN |

**Work and space ledger:** 8m normalization and 16m guarded SOURCE clauses, not paid R_mix341 inference nodes; output M=Theta(N) bits; full explicit construction O(M polylog N), input validation O(N polylog N), symbolic random output-bit generation O(polylog N), symbolic peak O(log N), materialized reference programs O(N) or worse, native guest A calls 0, failed policies 0, extra evidence bits O(M), lookups and index restoration explicitly required, actual machine simulation still OPEN. No free proof search, certificates or SAT oracle.

**Next target:** [P2-A2] and [P2-A5] demand one effective solver-intensional, exponent-oblivious transformation for EVERY correct total polynomial-time A on ALL binary inputs and all recursive children, with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) on the SAME FLMV machine. This report improves a scoped encoding input boundary of [P2-A4], not that universal bridge. P versus NP remains OPEN.
