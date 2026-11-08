# LSPV-3/499 | Composed external-source authentication for balanced historical /341 core, with affine-mask firewall

**2026-11-08 04:24 PST | Route B | PROVED/RESTRICTED composition lemma + COMPUTATIONAL direct replay | full historical R_mix341 OPEN.**

**Exact tracker dependencies:** [P2-L3-499] (this evidence), [P2-L3-490] (external binding), [P2-L3-491] (historical balanced packets), [P2-L5-414] (phantom affine-mask issue), [P2-D1], [P2-D3], [P2-C3], [P2-B1], [P2-B2]. Companion [P1-01], [P1-03], [P1-04] unchanged. P versus NP OPEN.

## IDEA, assumptions and pre-search falsifiers

**Hypothesis:** The recovered original historical SOURCE/AND3/XOR checker and /490's external CNF-multiset adapter can be composed on the exact /491 balanced proof packet, but a third, explicit source-variable-universe check is required because the recovered checker permits cancelling out-of-range affine-mask bits. The combined three-part certificate check proves source-authenticated UNSAT for the external formula for the verified core, without adding a logical rule.

Pre-committed falsifiers: (F1) any /491 balanced packet fails exact recovered native verifier or external input binding; (F2) a same-length satisfiable one-clause mutation of an original source passes the combined binding; (F3) the purported mask firewall fails to reject an out-of-universe bit pair that cancels in a later XOR; (F4) any conclusion relies on a RES, DEF, LOCAL-CONVERT or assumption-discharge byte that the recovered checker does not accept.

**Outcome:** F1/F2/F3 rejected by direct checks; F4 avoided by limiting the conclusion to the accepted historical SOURCE/AND3/XOR subgrammar. Native acceptance of the phantom-pair mutation *was* observed, consistent with earlier /414, so the extra firewall has nonredundant value.

## SEARCH and corpus reconciliation

Both complete root trackers and exact current blob identifiers were read (proof1 SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2 SHA 8fade227c5a44a393ab2e27bf6c771b27be8ff03 at review). Read current coordination issue #3 including latest peer [P2-L1-502], November 2 five-role governing handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-3/490,/491,/497,/498, LSPV-1/502 handoff, actual GROKPROOF/2026-11-08_0320_PROGRESS.md and actual research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex. The root main.tex remains unsafe for protected-region edits because full bytes are not available through authenticated connector reads.

Outside research files actually checked: konard/p-vs-np/scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), openai/math/README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). These contain no authority for historical /341 RES-to-AND3 or private-wire bytes. General web search was used; a distinct Google-branded search client was not available. Original published hardness controls were reviewed: Haken (1985) ordinary shared Resolution PHP lower bound, Cook (1976) polynomial Extended Resolution PHP shortcut, Urquhart (1987) expander Tseitin Resolution lower bounds, and Pang arXiv:2610.00837v2 syntactic Res(PC_r/F_p) theorem. These are **different proof models**; no asymptotic lower bound is imported into the current finite native-core test. Historical /341 producer and checker blobs, and /490 and /491 exact packets, were fetched and executed, not replaced with a convenient new grammar.

## ITERATE: restricted original-source composition theorem

Let V(P) be a sound verifier for the self-contained source-clause multiset C(P), with a certified proof and no free external facts. Let B(F,P) test exact signed clause-multiset equality and original-variable header bounds. Let A(P) reject every affine row mask with a bit at position >= n_original or a negative/ill-formed encoding, while independently retaining V's truth-table and XOR verification. Define

$$
\operatorname{Accept}(F,P)=V(P)\land B(F,P)\land A(P).
$$

**Theorem 499.1 (PROVED/RESTRICTED).** If Accept(F,P), then F is UNSAT, provided V is sound on its specified SOURCE/AND3/XOR grammar. Proof: V(P) implies C(P) is UNSAT, B preserves *exactly* its original clause multiset (up to order), and A only rejects. Thus F and C(P) have identical models. Source binding adds no unproved logical inference or SAT oracle. The claim is conditional on V's proved/replayed accepted-core soundness, not a claim that V authenticates undeclared RES/DEF/LOCAL-CONVERT/branch rules.

For original odd-charge signed Tseitin 3-CNF on a connected simple bridgeless cubic graph with h vertices, the 4h source clauses each exclude one locally incorrect parity assignment, and their conjunction is UNSAT by summing vertex parities. Deleting any original clause restores satisfiability (edge-graph cycle-space repair), with exact deletion witnesses checked in V. All 4h original source clauses must be used in any sound proof where each inference has at most two antecedents. For an acyclic connected dependency DAG of q binary-premise nodes and m indispensable source leaves, the underlying dependency edge count satisfies m+q-1 <= 2q, hence q>=m-1. Similarly depth >= ceil(log2 m). The balanced historical /491 construction attains both:

$$
W_{\mathrm{SOURCE/AND3/XOR}}(F)=4h-1,\qquad
D_{\mathrm{SOURCE/AND3/XOR}}(F)=\lceil\log_2(4h)\rceil.
$$

This is exact only in the FIXED recovered binary-premise subgrammar and unit-paid-node convention. Branching, definitions, Resolution, LOCAL-CONVERT and all other historical mixed rules have **not** been authenticated; the full R_mix341 minimum could be smaller. The theorem concerns certified UNSAT and minimum restricted proof work, not machine SAT time or a full 3SAT worst-case lower bound.

**Necessary mask guard:** In V's /341 AND3 check, affine mask compatibility is tested only for bit positions 0,...,E-1, and XOR addition checks masks arithmetically. Add bit 2^E to both row annotations entering a shared XOR: this bit cancels, and the original V still accepts the altered packet. The added A checks 0<=mask<2^E for every row and rejects the altered packet. This is a reproducible accepted-byte discrepancy, **not** an exhibited SAT formula falsely certified UNSAT, and does not alone prove the original checker unsound.

## Verification (COMPUTATIONAL)

Directly evaluated the unchanged GitHub-fetched original checker logic (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0) on the original balanced /491 packet (blob 481423a2f5271ab600bbc2f9a526fe62523239a9), yielding exactly **30,714 assertions**, seven original malformed controls and five original corrupted controls PASS. Evaluated the unchanged /490 source binder (blob b113119b7b87dac7510603804d91918e80f301b0), yielding **1,320 checks, 337 rejected negatives, 324 source-clause SAT mutations**. Replayed the exact GitHub-published /499 wrapper (blob bcd0933cbadd97889df9959bb54c20669d15f240) in a V8 isolation with these two exact components: **all seven original sources accepted**, all **324** same-length satisfiable mutations rejected on externally bound matching, and **one deliberately phantom-high-bit accepted by V but rejected by A**. The six bridgeless fixtures have (h,m,q,depth) (4,16,15,4), (6,24,23,5), (8,32,31,5), (10,40,39,6), (12,48,47,6), (32,128,127,7). The bridged control has m=40,q=39, only 36 essential clauses and no minimum-work certification. Strict external input syntax is the /490 DIMACS subset, not all DIMACS comment conventions.

Executable wrapper: experiments/arc/lspv3_499_native_source_bound_replay.cjs (exports firewall and validate; Node CLI also runs pinned native checker and binder). **Node CLI was not executed** in this V8 run. V8 executed the fetched original checker algorithm directly after removing only its Node CLI file-read/console wrapper; it was not an independent reimplementation. Published code was refetched and evaluated from actual main.

Raw results: results/raw/arc/2026-11-08_0424_LSPV3_499_COMPOSED_EXTERNAL_AUTH.json.

## Family, theorem, encoding, methods and remaining transfer ledger

**Family:** exact signed odd-charge Tseitin 3-CNF on connected simple cubic graphs. Parameter h even, E=3h/2 original Boolean edge variables, four strict ternary clauses per vertex, m=4h clauses; explicit signed-index input length N=Theta(h log(h+2)) for standard variable-indexed text and binary encodings with explicit indices. **UNSAT** follows from odd total vertex charge; on bridgeless connected cubic graphs, all 4h clauses are indispensable. **Hardness reference:** Urquhart's expander version is exponential for ordinary shared-DAG Resolution, not for GF(2) systems. **Known shortcut:** original SOURCE/AND3/XOR proof has 4h-1 paid nodes and balanced depth. **Outstanding transfer:** authenticate *all* historical R_mix341 rule bytes and exact accepted provenance, then seek a noncircular all-rule lower bound and B3; none follows from the current finite core.

**Logical resources:** q distinct unit-paid nodes; every shared node counted once, no invented branch/discharge, no discovery charge in ideal W. **Explicit bits:** external source Theta(h log h), proof q references at least O(q log q) bits and local table/row masks up to O(qh) bits in this dense packet representation; the packet stored on GitHub is 197,431 text characters. **Verifier/work resources:** external parser and clause-multiset sort O(N+ m log m*log h) elementary operations; mask bounds scanning O(sum encoded mask lengths); source/graph/head reads, full packet and source retention, array allocations, original graph/witness checking, output serialization and V8 host execution must be charged. Peak storage for whole-packet checking is O(packet bits+external source bits+index bits), not just q. A realized generator charges source acquisition, search/failed policies, balancing, certificate construction and all-phase memory. No actual time/space exponent on a fixed universal machine or FLMV contraction has been shown. Weighted span here assumes unlimited parallelism and unit binary-premise weights only within this subgrammar.

## Publication status and exact remaining gap

Role-owned report, executable, raw result and five-role handoff are published in main and SHA-readback checked. No root main.tex edit without full safe bytes. Tracker update, if any, must change only [P2-L3-499] evidence and dependent [P2-D1]/[P2-D3] scope, not the OPEN status of historical [P2-C3], all-rule minimum [P2-B1], or noncircular B3 [P2-B2]. Source-authentication composition is a verified finite-core improvement, not a P-vs-NP theorem. **P versus NP OPEN.**
