# LSPV-4/502 | An indexed high-water spike is not an invariant under a charged same-machine sparse repair

**2026-11-08 13:36 PST, America/Los_Angeles | Route A | PROVED/RESTRICTED symbolic typed-program construction + COMPUTATIONAL hosted controls | P versus NP OPEN.**

**Exact proof chain:** [P2-A2], [P2-A4], [P2-A5]; prior [P2-L4-496], [P2-L4-501], peer LSPV-2/502; companion [P1-01], [P1-03], [P1-04]. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged OPEN. New scoped resource-control evidence [P2-L4-502]. No mutation of historical R_mix341 grammar or weights.

## IDEA, exact hypothesis, and four predeclared falsifiers

Hypothesis: The dramatic gap between a virtual indexed WORK address and the one actually touched data bit can be neutralized for a precisely typed, bounded-index-port SAT-guest wrapper by a *same-machine*, side-effect-respecting virtual-cell implementation. A large raw FLMV high-water measure therefore does not, by itself, lower-bound the work space of every *equivalent* compiled program. Conversely, unchanged execution of the guest must still pay its original high-water. This is a narrower, constructive follow-up to the finite 2^25 high-water control of LSPV-4/496, not a generic sparse compiler for arbitrary machines.

F1: On the original FLMV machine, one indexed access to a high-address private WORK cell fails to increase the native high-water bound (would contradict Section 2.1).

F2: The repair silently assumes a free virtual-to-physical address jump, hides an input-length scan, or accesses a physical cell of address comparable to the large virtual address.

F3: The repair changes the actual read-back value or SAT/UNSAT/MALFORMED decision on any input, or leaks the private tape into the subsequent guest B.

F4: The result is falsely promoted to an all-input solver transformation, an arbitrary-guest exact-state simulation, a lower bound against white-box compilers, or proof that the Route A recursion is now closed.

## SEARCH: primary source, project, peers, external repositories

Read both COMPLETE living trackers: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt blob 33077f2c02d2b168cfb1f951eacb6852d281bcf0 at preflight; current issue #3 (1378 comments, latest LSPV-2/502); governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e514ddbd747150dcb68607013a3b2d154, AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef, .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f. Read LSPV-2/502 report blob 072818e4a4e23b4f3795454148bd7564204e0aa6 and handoff blob 2430aee7b7e5294805b4036eb58d79e0c7b86348; LSPV-4/501 blob 6091af9a81f1aaa8cec8f7db1b90236fd2b1e452; LSPV-2/433 certified inert-scan erasure blob fae636e637135ea46d7bf39bd9da2959e2760562 and LSPV-2/479 exponent-promise firewall blob 8b4c8b549ae7445aecb21cbac4f799a. Reused their precise scope and avoided treating this repair as an exponent extractor or universal dead-code eliminator. Inspected actual GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70, CLAUDE research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67 and ONETAPE-0001 blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a.

PRIMARY: Fortnow-Lipton-van Melkebeek-Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822; author manuscript https://lance.fortnow.com/papers/files/tst.pdf, actual PDF page 4 (zero-index page 3) screenshot read. §2.1 defines erased INDEX tape after an indexed head movement and WORK space by largest accessed address. **It explicitly observes that space may be exponential in runtime, while sparse accessed-cell data structures can cap space by time with polylog time overhead.** Thus a broad originality claim about sparse normalization would be false.

Required external repository actual files: konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3 (a distinct one-tape finite-machine model); konard/p-vs-np/proofs/p_not_equal_np/README.md blob 3a0304116e719948122302849ccae38d3890e410; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped methods, no universal SAT bridge); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (actual charged parity clauses); meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (separate certificate syntax, not R_mix341); openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f44ad49370d1b812e862c03c3a91d7f836 (concrete costed program, not arbitrary-callback theorem). Read original Urquhart 1987 ordinary Resolution hardness and Ben-Sasson/Wigderson 2001 proof-size/width source; neither provides an all-algorithm lower bound. Public web indexed queries searched exact FLMV model, sparse address normalizations, published Tseitin lower bounds and both new repositories. An independently branded Google search interface was not used.

## ITERATE: Theorem 502.1, one-cell indexed WORK virtualization (PROVED/RESTRICTED, known-method instantiation)

Conditionally suppose B is any fixed uniform total correct polynomial SAT/UNSAT/MALFORMED decider, with time T_B(n) and native-work space S_B(n), running on a fixed finite set of tapes. For every fixed positive integer k, define one program G_k(B) on *every binary input x*, n=|x|:

1. With a read-only input scan, compute n and b=(first input bit) XOR (last input bit), with b=0 on empty x. This takes O(n+1) native moves, O(log(n+2)) auxiliary WORK/INDEX bits; account for this local phase.
2. Put a 1 followed by L=k ceil(log2(n+1)) zeroes on the dedicated private WORK INDEX tape; the indexed jump goes to virtual WORK position A=2^L, erasing that INDEX tape. Write b at A. This costs O(k log(n+2)) INDEX construction time plus constant indexed operations.
3. Reconstruct the same INDEX word, jump again, read b from A, and use the read bit to select one of two identical, fresh B invocation entries. Both entries run B(x) without any prior private WORK tape exposed.
4. Return exactly B(x)'s SAT, UNSAT, or MALFORMED label. The private spike tape is not a B work tape.

The original G_k(B) remains uniform, total and correct on **all binary x**. It has T_{G_k}(n)=O(T_B(n)+n+k log(n+2)) and S_{G_k}(n)=Theta(max{S_B(n), (n+1)^k}) up to fixed-k constants under FLMV's largest-address metric. The reason is one real indexed WORK access to 2^L, with L=Theta(k log n), even though that cell stores only one bit. The INDEX-tape erasure and two address constructions are paid, and the input scan is read-only and excluded from space only as FLMV prescribes.

**Compiler C_one (typed one-port repair).** Recognize the *explicitly marked*, private one-cell WORK macro above. Replace its two high-address accesses by a physical private cell at a fixed low address (e.g. cell 1), keep the original read-back value and branch on that value, then invoke B fresh. The virtual address may be retained as a binary descriptor of L+1 bits for trace authentication, but it is NOT used as a physical WORK address. Original program and compiled program have identical read-back values, branch choices, and final outputs for every binary x. The private cell and descriptor are cleared before the call to B, paying O(k log(n+2)) native steps. Therefore:

$$
T_{C_{\mathrm{one}}(G_k(B))}(n)=O(T_B(n)+n+k\log(n+2)),
$$

$$
S_{C_{\mathrm{one}}(G_k(B))}(n)=O(\max\{S_B(n),\,k\log(n+2)\}).
$$

These are charged *same-machine* bounds for the restricted typed macro: the physical WORK never jumps to A, computing the descriptor takes logarithmic WORK, each INDEX move uses the actual index tape, and there is no free "oracle" or result cache. No general numerical-address dictionary, general pointer-aliased state, or arbitrary-guest simulation is claimed. This is a constructive instance of the sparse-access observation **already stated by FLMV §2.1**, not a novel universal theorem. Since the native unchanged guest and the compiled program differ, [P2-A4] must track the *same realization* as the claimed space lower/upper bound.

## Family / theorem / encoding / known shortcut / missing transfer ledger

Control family: original 3-CNF Tseitin on connected cubic expander G_h. Edge x_e per edge, charge c_v per vertex, and exactly four original proper 3-clauses per vertex forbidding assignments violating XOR_{e incident v} x_e = c_v. For h vertices, 3h/2 original variables, 4h original clauses and encoded length Theta(h log h) under explicit dense identifiers. Odd total charge gives UNSAT; Urquhart (1987) and Ben-Sasson/Wigderson (2001) give exp(Ω(h)) ordinary shared-DAG Resolution lower bounds for appropriate expanding families, not R_mix341 or arbitrary-machine SAT hardness. Complete GF(2) elimination is a legal algorithmic upper-bound shortcut and must not be excluded. Current finite controls use *only K4*, with h=4, 6 variables, 16 strict clauses, the exact 208-bit signed source grammar of peer LSPV-2/502 (8-bit magic, 8-bit count, 4 bits per signed literal), NOT an asymptotic expander instance. The high-water wrapper changes NO original clauses; it acts on the parser input program, not as a 3-CNF encoding reduction. Any 3-CNF conversion invoked elsewhere requires its own lower-bound preservation proof.

Missing transfer: no semantic all-input q<=N^(3/5), length<=N^(1/2) correct decomposition, no generic arbitrary-B code-aware reducer, no charged recursive FLMV contraction, and no B1/B2/B3 inference.

## Work, span, bit evidence, peak workspace and hostile controls

For G_k(B): source/input-length scan O(n); INDEX construction twice O(k log n); indexed read/write O(1) operations; B execution T_B; output B's original; parsed source read by B charged through T_B; private descriptor O(k log n); physical peak Θ(max{(n+1)^k,S_B}). For repaired C_one: low-slot write/read O(1); clearing O(k log n); guest invocation once, no caching, restart, failed policy or shared proof DAG; native all-phase peak O(max{log n,S_B}); one fixed-code compiler parse of the marked macro O(|B|+k) (program compilation cost separately, not a per-input free transformation). For both: logical proof nodes=none; source-authenticated SAT proof-certificate bits=none; elapsed sequential work and single-path span coincide up to constants. This construction does not model multiple simultaneous child buffers; those remain charged under [P2-A5].

F1 refuted: FLMV §2.1 says high-water is charged. F2 refuted for this typed macro by explicit low-cell implementation; the host test's numeric cell bound 16+4*(L+1+bit_length(n)) is an **illustrative slot ledger**, not a bit-exact transition-table peak. F3 refuted symbolically by deterministic read-back equality and original unmodified B invocation, and finitely by independent implementations. F4 explicitly retained as an open limitation. Unchanged-guest exact trace replay *still* incurs the high-water; white-box compilation may avoid it, and generic source-dependent child construction remains OPEN.

## Reproducibility

Independent hosted Python and JavaScript/V8 implementations each passed 644 checks over 26 inputs and 130 runs (16 signed K4 original controls: 8 SAT, 8 UNSAT; 7 malformed mutations and 3 short/empty controls; k in {1,2,3,4,6}). All sixteen original-source SHA-256 digests and large-case outputs matched across languages. For the valid 208-bit K4 source and k=6, the original virtual indexed WORK high-water is 2^48 = 281474976710656, whereas the hosted illustrative low-slot ledger reports 244 bits; **244 is not a verified native FLMV workspace bound**. No actual native FLMV transition-table interpreter nor authoritative R_mix341 checker ran. The experiments validate finite arithmetic and semantics only; the symbolic restricted compiler supplies the theorem.

GitHub report / verifier / raw / handoff committed separately with postwrite readbacks; independent Python reproduction attached in run artifacts. The intended material tracker update is new [P2-L4-502], refining [P2-A4] only; [P2-A2] and [P2-A5] remain OPEN. Source SHA must be refetched before mutating proof2.txt. No change to proof1.txt anticipated.

**Actual advance:** A paid, explicitly typed same-machine *positive* virtualization control complementing the prior negative unchanged-guest high-water test, while preserving every source and both-label/malformed output. **Precise remaining gap:** a universally correct, recursively iterable, code-aware FLMV contraction with full resource ledgers. P versus NP OPEN.
