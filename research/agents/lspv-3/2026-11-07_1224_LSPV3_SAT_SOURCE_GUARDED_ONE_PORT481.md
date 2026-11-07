# LSPV-3/481 | Satisfiable strict-3CNF source: global one-port entailment barrier

**2026-11-07 12:24 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

Exact tracker IDs: previous [P2-L3-475], [P2-L3-477], [P2-L3-479], [P2-L3-480], [P2-F13]; current [P2-L3-481]. Open [P2-D1] grammar, [P2-C3] full mixed translation, [P2-D2] shared-DAG minimum, [P2-B1] all-rule lower bound, [P2-B2] B3. P=NP chain [P1-01], [P1-03], [P1-04] OPEN.

## IDEA / four falsifiers (specified before search)

Hypothesis: globally checking whether a one-bit output is entailed by an arbitrarily large source is coNP-complete even when that source is guaranteed SAT, properly encoded strict 3-CNF, with no hidden SAT oracle. The word LOCAL must describe the antecedent's semantic/input support, not just the output width.

F1: splitting a guarded clause fails existential projection for some x,z. F2: output clauses fail proper *exactly three distinct* variables. F3: a no-instance makes guarded source UNSAT (vacuity). F4: a claimed corollary silently treats the whole-source global entailment oracle as historical LOCAL-CONVERT. Mathematical proof discharges F1–F3. F4 is prohibited and historical accepted grammar remains OPEN.

## SEARCH / prior-state audit

Read complete root proof1.txt (initial blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 characters) and proof2.txt (initial blob d43c7731269a322efe73262c898c7190e4528060, 225,900 characters), active issue #3 and recent comments, Nov 2 five-role handoff, AGENTS.md, CODEX.md and pnp-research SKILL.md. Inspected LSPV-3/477, /479, /480 and LSPV-1/485; historical rule declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb) and source/AND3/XOR-only verifier experiments/arc/lspv2_341_independent_verify.js (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0). Actual Grok GROKPROOF/2026-11-07_1920_PROGRESS.md (blob 231561ce216699f286b705a0056584789ba9ee99) and Claude research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (blob b7150bb9ed964affd5fb90ecd24b0aa35d600bf9) read. No root main.tex edit: complete fetch gave zero characters (blob 68188a24badda635a5983fda1c381cdb694fd497).

Required targeted external review:
- konard/p-vs-np/scripts/proof_status.json, blob 93b77ed3d8fe456f81c690035f45f07910a247f2: finite-machine P subset NP, not NP subset P.
- blkph0x/p-vs-np-proof-research/METHOD_INDEX.md, blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md, blob 4aba9d94405402c4dc122c7ebe2ef3665da17f5a: analogous fixed-width projection complexity distinctions, no general proof.
- meelgroup/frat-xor/format.md, blob 986a21aa92b62f844ef1fce852193142c41b2b1f: external source-indexed FRAT-XOR/XLRUP format, not historical native R_mix341.
- tanyongkiam/cake_lpr/README.md, blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c: separate checker/producer; final planned release dated Nov 1.
- peitl/short-proof/README.md, blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab: restricted ordinary Resolution minimum controls.
- openai/math/README.md, blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae: unformalized manuscript caveat.

Primary controls: Chvátal–Szemerédi, Many Hard Examples for Resolution, JACM 35(4), 1988, DOI 10.1145/48014.48016; Cook–Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44(1), 1979, DOI 10.2307/2273702. No separate Google-branded search interface used. Earlier project /384 and /475 already noted coNP barriers for broader predicates/circuits; present scoped construction specializes the STANDARD clause-splitting reduction to always-SAT original sources and ONE distinguished output variable, without a claim of mathematical novelty.

## Theorem 481.1 (PROVED/RESTRICTED)

Let F be any signed proper strict-3CNF on n original variables with clauses C_j=(l_j1 OR l_j2 OR l_j3), j=1..m. Introduce a fresh global guard z and independent fresh a_j. Define a new ORIGINAL strict-3CNF source

$$
G(F,z,a)=\bigwedge_{j=1}^m
[(\ell_{j1}\vee\ell_{j2}\vee a_j)
\land(\neg a_j\vee\ell_{j3}\vee z)].
$$

Every new clause has exactly three distinct variables. G contains 2m clauses, n+m+1 variable labels and 6m literal occurrences. For each assignment to original x,z,

$$
\exists a\; G(F,z,a)\quad\Longleftrightarrow\quad z\vee F(x).
$$

Consequently G is SAT for EVERY F, and

$$
G(F,z,a)\models z\quad\Longleftrightarrow\quad F\ \mathrm{UNSAT}.
$$

The marked-unit entailment problem on this syntactically recognized, guaranteed-satisfiable guarded class is coNP-complete, via a polynomial-time many-one reduction from proper strict-3CNF UNSAT.

**Proof.** For each j, if the first two literals of C_j are both false, the first guarded clause forces a_j=1 and the second requires l_j3 OR z. Otherwise choose a_j=0 and both clauses hold. Hence existential elimination of a_j is exactly C_j OR z. Since all a_j are disjoint, eliminating the entire tuple gives ∧_j(C_j OR z)=F(x) OR z. With z=1 every x extends to a model of G, and with z=0 a model exists exactly if F is SAT. Therefore G entails z precisely when F is UNSAT. For coNP membership, failure of entailment has a polynomial witness: a complete assignment satisfying G and falsifying z. Construction and checking of the rigid guarded source grammar require polynomial time and bits. QED.

This is a complexity CLASSIFICATION, not an unconditional superpolynomial running-time lower bound. It does NOT claim that a generated guarded source inherits a published Resolution proof-size lower bound, since equisatisfiable splitting does not by itself establish the required reverse proof simulation.

## Family / theorem / encoding / known-method / transfer ledger

Published Chvátal–Szemerédi random proper strict-3CNF F(n,3,6n), n original variables, m=6n, N=Theta(n log n), ordinary shared-DAG Resolution exponential lower bound with high probability under the theorem's density assumptions. Guarded transform gives G with 12n strict clauses and 7n+1 variable labels, always SAT; its unit z is entailed for UNSAT F. Only semantic polynomial-time many-one preservation is proved here. No Resolution-size or mixed-system lower-bound preservation is asserted. For odd Tseitin 3CNF, known GF(2) shortcuts give polynomial alternative derivations. All admissible source-authenticated shortcuts remain available in the ideal all-DAG minimum. A single legal primitive LOCAL-CONVERT in the historical declaration checks implication from a *previously derived local at-most-three-original-support* antecedent in an eight-row table; this is efficiently checkable and NOT the source-global problem above. Treating G itself as one inferred factor would silently add a different rule.

## ITERATE / independent finite controls

An independent Python implementation exhaustively tested eleven original-source families: nine prefixes of all eight signed clauses on x1,x2,x3, and odd/even charge K4 cubic Tseitin strict 3CNF. It checked 400 original x,z assignments, 9,344 local split-witness trials and 8,176 full assignments on small G sources; four malformed-source controls rejected. Prefix source model counts 8,7,6,5,4,3,2,1,0. K4 odd source had 0 models and even had 8, but BOTH guarded sources were SAT: odd entailed z, even did not. Python ~0.278 s wall and 9,917 traced Python allocation bytes (not full process RSS).

A separately implemented local Node.js verifier passed 19,346 assertions and rejected four malformed controls, ~0.12 s wall and 36,728 KiB maximum RSS. The actual GitHub-published compact JS blob c58ed049410f8dd3c09a627f1c1d6fdfbb61ee32 was fetched and replayed in V8 with ONLY the Node assert import and stdout adapter substituted; it passed 19,331 checks and four negative controls, with matching model counts. The authoritative historical checker was NOT executed for any new mixed-rule proof.

Code: experiments/arc/lspv3_481_guarded_one_port.cjs. Raw: results/raw/arc/2026-11-07_1224_LSPV3_481_GUARDED_ONE_PORT_RAW.json. Separate Python and Node scripts plus full raw output are in the current conversation reproducibility archive.

Resource ledger: deterministic construction writes 2m clauses, m+1 names and O(N+m log(n+m+1)) bits; output construction and direct model verification are polynomial. Exhaustive finite truth-table checks are exponential in input variables at scale. The tests do NOT measure R_mix341 paid proof nodes or the full minimum. Distinguish proof discovery, construction, malformed classification, source/metadata/head reads, retrieval, check, serialization, failed policies, and all-phase simultaneous peak space. No same-machine FLMV inference is made.

**Scientific advance:** an exact strict-3CNF, always-SAT, one-port antecedent example proves why exposure width alone does not make an arbitrary source-global implication rule local. Native history [P2-D1] and full simulation [P2-C3] remain OPEN, as do [P2-B1] and [P2-B2]. All five roles, their two Route A/three Route B allocation, schedules, enabled states and fixed historical grammar/weights were unchanged. P versus NP OPEN.
