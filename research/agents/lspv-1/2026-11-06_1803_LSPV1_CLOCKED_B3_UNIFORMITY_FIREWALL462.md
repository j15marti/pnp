# LSPV-1/462: Clock-guarded Resolution isolates the missing B3 same-calculus implication
**2026-11-06 18:03 PST, America/Los_Angeles. Route B lead.**
**Status: PROVED/RESTRICTED for the explicitly NEW artificial clocked calculus; COMPUTATIONAL finite controls; historical R_mix341, superpolynomial full-mixed minimum, B1/B2/B3 and P versus NP OPEN.**

## Chain IDs and precise hypothesis
Reviewed both root proof trackers on main: proof1.txt sha 0c24df268207e9436d51519ec168a984ab10ae3e and proof2.txt sha f47988254e00dae6c81cd30f86b9343456ad7f15. Affects [P2-B2] and new restricted control [P2-B6]; related [P1-X3], [P2-D1], [P2-B1], [P2-C1], [P2-C3] remain unchanged. This is NOT a proposed replacement for historical R_mix341 or its fixed weights.

**Initial idea, before literature searches.** Test the tempting inference that SAT in P, soundness, completeness and even polynomial certificate checking together force polynomial minimum work in every preselected calculus. If false, an explicit fixed grammar should retain exponentially costly legal proof obligations even if the SAT decision task is polynomial.

**Four falsifiers:** (F1) the artificial proof system is unsound, incomplete, or not polynomial-time checkable in its certificate length; (F2) a reconvergent/branched/shared legal DAG skips the expensive clock; (F3) exponential proof bits are mistakenly counted as exponential PAID inference nodes; (F4) this countermodel is silently treated as a falsification of B3 for actual R_mix341.

## Primary literature and repository-aware iteration
Cook/Reckhow (JSL 44(1), 1979, DOI 10.2307/2273702) establish the SOME-proof-system equivalence with NP=coNP and discuss relative strength of proof systems. Pich/Santhanam (arXiv 2312.08163) show that EF lower bounds require additional bounded-arithmetic assumptions to reach P != NP. Neither gives B3 for historical R_mix341. This led to the revised precise countermodel below.

Required external repository inspections: konard/p-vs-np README.md (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95, finite-machine P subset NP only); blkph0x/p-vs-np-proof-research README.md (blob f397a7747eaca82df3d754d0a4b4bab1fe10f814, explicitly scoped/promise results, no P/NP resolution); meelgroup/frat-xor format.md (blob 986a21aa92b62f844ef1fce852193142c41b2b1f, explicit source and XOR steps, verified elaboration scopes); tanyongkiam/cake_lpr README.md (blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c, CakeML proof checker scope); openai/math README.md (blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae, mathematical preprints are research data with mixed verification). Google-specific engine not separately available; public web search was used, without a claim of using Google's own interface.

Project evidence actually read: five-role historical handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514ddbd747150dcb68607013a3b2d154); current issue #3 including 2026-11-06 17:48 LSPV-5 tracker audit; LSPV-1/461 report (blob 135408d71d69695dbb492e86a68987e8f518a425); LSPV-3/462 report (blob 0a0a71dd210d384ddc64cfff36dfeba8deed52f4); GROKPROOF/2026-11-06_2316_PROGRESS.md (blob a20fb8b3640d7574faf238a4a83a021bb0984808); research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (blob 79e4d4e7e0e3edff3aba8610852c45534bdde128); AGENTS.md, CODEX.md, project skill. Repository preflight.py and authoritative historical checker were NOT executed. Root main.tex returned a blob SHA but empty ranged text, so was not modified.

## New exact calculus R_clock (NOT historical R_mix341)
Fix a conventional binary encoding of arbitrary CNF sources F, with N=|encode(F)|. A source clause has a free indexed premise with its original signed bytes. Nonempty/empty Resolution derivations are allowed with proper parent orientation and one paid unit-weight inference per resolvent. Independently, admit one free clock source c_0, plus precisely one rule:

$$
\frac{c_j}{c_{j+1}}\quad (0\le j<2^N),
$$

where each application costs one new distinct node, j is explicitly represented in binary, and there is NO clock-jump, clock-sharing substitute, or alternate contradiction rule. A final paid SEAL step has exactly two premises: a source-authenticated Resolution empty clause and c_(2^N). Only SEAL is recognized as the completed refutation goal. Clock tokens are bureaucratic proof objects, not semantic consequences. Any legal alternative Resolution derivation remains admissible but still has the AND obligation to produce the entire clock chain. This is a separately declared fixed proof calculus; all its syntax and unit weights are independent of the particular source except the publicly computable N in the Tick side condition.

**Theorem 462.1 (PROVED/RESTRICTED).** The accepted R_clock relation is sound and complete for UNSAT CNF and has a deterministic verifier polynomial in the combined source and explicit certificate bit length. Let W_RES(F) be the minimum number of paid Resolution inferences from the authenticated original clauses to the empty clause. Then for every UNSAT F,

$$
W_{R_{\rm clock}}(F)=2^{|encode(F)|}+W_{\rm RES}(F)+1.
$$

**Proof.** Soundness: the SEAL rule demands an independently valid ordinary Resolution derivation of the empty clause, which is sound. Completeness: ordinary Resolution is refutationally complete, and the finite c_0,c_1,...,c_(2^N) chain can always be supplied. Polynomial checking: scan the explicit derivation DAG, validate every signed clause/pivot/source reference and each adjacent integer pair j,j+1; validate the terminal index by comparison with the N+1-bit word 1 followed by N zeros. Each local check is polynomial in source and certificate bits. For every SEAL, its clock parent uniquely forces c_(2^N-1), recursively down to c_0; the 2^N different Tick nodes cannot be merged, jumped or replaced. No other rule produces clock tokens or SEAL. Resolution ancestors and clock ancestors are disjoint paid node types. Hence the lower bound is the displayed sum. Concatenating an optimal Resolution DAG, the forced clock chain and SEAL attains it. QED.

**Corollary 462.2 (PROVED/RESTRICTED).** For the valid UNSAT sources F_m containing (x_1), (not x_1) and m further harmless unit clauses on fresh variables, N_m=|encode(F_m)| tends to infinity, W_RES(F_m)=1, and

$$
W_{R_{\rm clock}}(F_m)=2^{N_m}+2.
$$

Thus its worst-case minimum grows superpolynomially IN THE ARTIFICIAL CALCULUS regardless of SAT's algorithmic complexity. If SAT happened to be in P, B3 would still fail for R_clock. This establishes that the schema "SAT in P implies polynomial work for every sound, complete, effectively/polynomially checkable fixed calculus" cannot be obtained just from those generic hypotheses. It does NOT refute conditional B3 for the one historical R_mix341; it demonstrates why R-specific simulation is the missing arrow. The countermodel is an intentional proof-system padding control, not a new candidate hard 3-SAT family.

**Proposition 462.3 (CONDITIONAL sufficient mechanism, not new B3).** If A is a *mathematically proved* fixed uniform total polynomial SAT decider, define its rejection-trace system T_A: for UNSAT F, a certificate supplies the locally checkable accepting trace of the computation A(F)=UNSAT. A deterministic polynomial checker validates the trace, and mathematical correctness of A establishes soundness externally, without assuming an R_mix341 reflection axiom. T_A is polynomially bounded. If, additionally, the SAME preselected historical R_mix341 admits a polynomial-NODE-WORK simulation of every T_A proof with source authentication and exact native rules, then B3 follows. The additional simulation is OPEN; this conditional mechanism is not a proof of B3 and may be as hard as B3.

## Published hard-family ledger and shortcut controls, unchanged
* Chvatal/Szemeredi (1988): random strict signed 3-CNF, ordinary shared-DAG Resolution exponential with high probability at stated density, historical native R_mix341 transfer OPEN [P2-F8].
* Odd-charge cubic expander Tseitin: exactly 4h strict 3-CNF clauses; ordinary Resolution 2^{Omega(h)}, declared semantic AND3/GF(2) 4h-1 node shortcut; accepted-byte grammar OPEN [P2-F2].
* Braun bit PHP, arXiv 2609.23015v2: published Res(XOR) lower bound on its original wide source; proper-3CNF and historical full mixed transfer OPEN [P2-F3].
* de Rezende/Nordstrom/Risse/Sokolov 2025 sparse FPHP: exponential Resolution lower bound only for its specified sparse model, ER/circuit and Hall-kernel shortcuts are mandatory [P2-F4].
None of these published families is being replaced by R_clock. This run primarily tests the B3 logic.

## Finite reproducibility and actual resource ledger
Executable: experiments/arc/lspv1_462_clocked_resolution_selfcheck.cjs; raw: results/raw/arc/2026-11-06_1803_LSPV1_CLOCKED_B3_462_summary.json. For the isolated contradictory two-unit control source, exhaustively validate every inference for clock parameters q=1..10 (finite horizons, NOT a universal CNF checker and NOT a large-N source-length run). Charged nodes equal 2^q+2; for q=10, 1,024 ticks and 1,026 total paid nodes, serialised JSON certificate 40,843 UTF-8 bytes. Total 2,104 explicit assertions passed; eight deliberately corrupted source/pivot/empty-clause/clock/seal variants rejected. This executable is an independent scoped selfcheck, NOT the historical R_mix341 checker.

Cost distinctions: logical paid work exact 2^N+W_RES+1, ideal weighted span at least 2^N+1 (serial tick dependence), actual explicit certificate evidence at least Omega(2^N) bits and O(N 2^N) under fixed-width counter encoding; the test generator materializes O(2^q) objects and the JS checker retains O(2^q) IDs. Construction and source parsing are separately charged; neither the test nor an exponentially long written certificate is claimed to be efficient. No wall-time or RSS measurement was made. An abstract streaming validator could use lower space, but the tested implementation did NOT.

## Revision and exact remaining implication
F1 falsified by the soundness/completeness and polynomial-verifier argument. F2 ruled out by the forced AND clock ancestry even with free after-the-fact optimal branch choice. F3 addressed by charging the actual 2^N distinct Tick inference nodes, independently of bit length. F4 excluded: R_clock is NOT R_mix341. The control sharpens the existing B3 transfer caveat; it gives no new full-mixed lower bound.

**Actual advance:** explicit, fixed-rule, polynomial-checkable, exponentially clocked proof-calculus countermodel plus a precise decider-trace simulation sufficient condition. **Verification:** symbolic proof and scoped 2,104-assertion finite selfcheck. **Still OPEN:** historical native rule authentication [P2-D1/C3], all-rule mixed hardness [P2-B1], noncircular SAME-R B3 [P2-B2], and P versus NP.