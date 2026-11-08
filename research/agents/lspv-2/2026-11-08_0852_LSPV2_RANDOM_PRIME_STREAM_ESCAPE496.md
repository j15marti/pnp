# LSPV-2/496: Random-prime one-pass streaming shortcut for the connected hard-diagonal Tseitin family

**2026-11-08 08:52 PST | Route A | KNOWN FINGERPRINT METHOD + PROVED/RESTRICTED INSTANTIATION + COMPUTATIONAL. P versus NP OPEN.**

**Nodes:** [P2-A4] contains the *deterministic* streaming tradeoff in LSPV-2/495. This run adds an explicit randomized-model shortcut control, not a refutation of the correctly scoped deterministic theorem. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1] and [P2-B2] remain OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither tracker needs an altered status, dependency or evidence of a stronger deterministic result. Both complete main trackers were read, together with current coordination issue #3 (including LSPV-2/495 and LSPV-4/496), the November 2 five-role handoff, AGENTS.md, CODEX.md, .codex research skill, actual current GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70), Claude TPORT-0001 (blob b7150bb9ed964affd5fb90ecd24b0aa35d600bf9), LSPV-4/494 and /496, and original LSPV-2/495.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** The strictly proper, connected, duplicate-free original 3-CNF family in LSPV-2/495 encodes EQUALITY on the hard UNSAT diagonal. A random-prime fingerprint should therefore yield one-pass polylog-space randomized SAT decisions on the *same* promised inputs, a strong upper-bound control against extending deterministic streaming lower bounds to randomization.

**Predeclared falsifiers:** (1) Too many sampled primes divide a nonzero bit-word difference; (2) extracting matching bits from the existing signed source requires an uncharged H-bit table; (3) generating the random modulus or computing modular powers requires super-near-linear time or linear writable space; (4) the generated diagonal or off-diagonal formulas fail the original Tseitin SAT/UNSAT and proper-3CNF conditions. A further hostile check requires an explicit fixed-prime failure.

**SEARCH:** The project LSPV-2/495 already proved the exact connected hard-diagonal construction, so it is reused as a prior result rather than claimed again. Prior repo searches for fingerprint Tseitin modulo primes, randomized streaming equality edge split, and Rabin fingerprint LSPV found existing generic warnings but no exact control for /495; lack of matches does not establish novelty. Relevant primary sources: Marcus-Spielman-Srivastava (Annals 2015) for infinite cubic bipartite expanders; Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) for ordinary shared-DAG Resolution hardness of odd-charge Tseitin CNFs; Fortnow-Lipton-van Melkebeek-Viglas (JACM 2005) for the different deterministic indexed-input FLMV machine; Agrawal-Kayal-Saxena, PRIMES Is in P (Annals 2004) for polylog-bit deterministic primality testing; Lalonde-Mande-de Wolf (2021) for known randomized equality communication protocols. Actual required external files inspected: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (only finite-model P subset NP), blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and README.md blob f397a7747eaca82df3d754d0a4b4bab1fe10f814 (restricted methods), berkeley-abc/abc README.md blob 88a9d1a316dd9751acade746de315fd1e6e6c362 (circuit DAG implementation, no SAT-wide theorem), and openai/math CONTENTS.md blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 (manuscript index). Public research search was available, but no separately authenticated Google-branded client. No external PDF was parsed.

## Source family and actual theorem

Use *exactly* original signed strict-proper-3CNF LSPV-2/495, report path research/agents/lspv-2/2026-11-08_0815_LSPV2_CONNECTED_EXPANDER_EDGE_SPLIT495.md, blob 44ae6eea0d2752059eab080dc9f8ecab500a8647. Fix a connected simple cubic bipartite graph with H vertices, m=H/2 matching edges, and odd total parity charges. Each matching edge j has variable ID 2j-1+a_j at its L endpoint and 2j-1+b_j at its R endpoint; nonmatching edges have disjoint IDs H+1,...,2H. Every vertex supplies the four original signed ternary clauses forbidding incorrect local parity assignments. All L packets precede R packets. Every input has 4H *distinct* proper width-three clauses, exactly 12H literal occurrences, and the same bit length

$$
N(H)=8+(H+1)+(2H+1)+12H(\lceil\log_2(2H+1)\rceil+1)+2=\Theta(H\log H).
$$

The source is UNSAT iff a=b and SAT otherwise, with 2^(H/2+Hamming(a,b)) models off diagonal (incidence-rank proof in /495). A diagonal growing expander member is *isomorphic to the original* odd-charge Resolution-hard Tseitin CNF. Its known exponential bound applies ONLY to ordinary shared-DAG Resolution, not GF(2), ER, mixed R_mix341 or all SAT algorithms.

**Theorem 496.1 (PROVED/RESTRICTED, standard random-prime fingerprint).** There exists a one-pass **randomized** algorithm for the above promised SAT-label family, with no false SAT answer on an UNSAT diagonal, false UNSAT probability at most 1/4 on any SAT input, O(N polylog N) bit time and polylog N writable peak on a standard finite-tape implementation.

**Proof:** Set K to the smallest power of two at least 4m, choose uniform J in 1,...,K using log2 K coin tosses, and deterministically find the J-th prime p_J. During one left-to-right scan, extract a_j or b_j from the low bit of the matching variable ID 2j-1+a_j or 2j-1+b_j; identify matching j by its ID pair, j=ceil(ID/2), and distinguish sides by the fixed packet order. Maintain the residue

$$
D_p(a,b)=\left[\sum_{j=1}^m (a_j-b_j)2^{j-1}\right]\bmod p.
$$

Every term is calculated by modular binary exponentiation using O(log m) arithmetic registers. Return UNSAT if the final residue is 0, otherwise SAT. If a=b the residue vanishes for every p, so UNSAT has zero error. If a differs from b, the nonzero integer D represented by the bracket has absolute value strictly below 2^m, and therefore has fewer than m distinct prime divisors. Sampling from K distinct primes gives

$$
\Pr[\text{false UNSAT}\mid a\ne b]\le m/K\le1/4.
$$

The J-th prime is O(K log K); sequentially enumerating prime candidates with a deterministic polynomial-in-log-bit primality test (AKS) and a log-bit counter takes O(m polylog m) time and polylog m writable space. The source read, local parsing, coin generation, residue computation, and output have the same resource envelope. The finite executable below uses trial division for tiny examples, **not an executed AKS implementation and not a native FLMV trace**. Multiple independent moduli k=ceil(c log_4 m) can be maintained during one source scan, detecting SAT if any residue is nonzero: error at most m^(-c), with polylogarithmic storage and O(N polylog N) time for every fixed c. No deterministic all-input machine or general-CNF recognition is claimed.

**Theorem 496.2 (PROVED/RESTRICTED; sharp fixed-prime portfolio control).** A *deterministic fixed-prime residue-only* test that says equal iff D=0 mod p for every p in its preselected distinct-prime set P is exact on all m-bit words iff product(P)>=2^m. If M=product(P)<2^m, choose a=0, b=M in m bits: all residues collide despite a!=b. If M>=2^m, no nonzero |D|<2^m is divisible by M. Retaining the simultaneous exact CRT residue tuple requires >=log2 M>=m bits in the straightforward storage representation; a multi-pass computation is a different allowed upper bound. This observation is not a universal deterministic-machine lower bound and does not invalidate /495. Picking a good prime after seeing each input would be nonuniform advice unless the choice and costs are constructed and charged.

## Actual independent experiments and hostile controls

**Python reference:** 6,121 assertions passed over 320 graph/word-pair sources: 64 K3,3 pairs and 256 cube pairs; 296 SAT /24 UNSAT. It independently constructs all original proper signed ternary packets and brute-forces all K3,3 labels plus selected cube controls. Every sampled prime seed is checked exhaustively. **Independent JS:** 6,402 checks passed on the same 320 cases with separately coded original signed CNF generation, GF(2) rank consistency, every random seed, exact CRT portfolio threshold and malformed-bit rejection. Both find 302 seeded collisions across all SAT inputs and at most two bad primes per pair, and neither yields a false SAT decision for an UNSAT diagonal. An explicit bad fixed prime is retained. The published JS was fetched back in full and replayed with identical output at blob 7eaaba9a2de136b86b845fff527f61f60647d654.

- Executable: experiments/arc/lspv2_496_random_prime_stream_independent.cjs
- Raw ledger: results/raw/arc/2026-11-08_0852_LSPV2_496_PRIME_FINGERPRINT_LEDGER.json
- Python script SHA256: 53c7ab91c4f6dd90163565116a1c401c3f25ebb53514075d54d80064c4e5d396
- Python raw SHA256: 2fa7d7f03dadb922da0e9f25ee5e7bbac8bdda2ac295d8e2de13e2517a5131b7

**Resource and transfer firewall:** /495's deterministic (2p-1)S+O(1)>=m streaming theorem remains true. The new upper control changes the machine to **randomized**, permits one-sided errors, and assumes authenticated/public promised layout. These are substantial changes, not a FLMV transformation. Input recognition of arbitrary malformed and other CNFs, deterministic both-label correctness, recursively iterable source transformations, native random-access tape simulation, implementation-independent exponents and all phase resource bounds remain OPEN. No source-authenticated branching proof DAG or rule extension is asserted. No historical R_mix341 rules/weights, peer regions, agent identities, allocation or schedules were changed. Root main.tex was not modified without full-byte authentication. P versus NP OPEN.

## Sources

1. LSPV-2/495, original connected hard-diagonal report and proof, path/blob above.
2. Marcus-Spielman-Srivastava, Interlacing Families I, Annals 182 (2015), DOI 10.4007/annals.2015.182.1.7.
3. Urquhart, Hard Examples for Resolution, JACM 34 (1987), DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, Short Proofs Are Narrow, JACM 48 (2001), DOI 10.1145/375827.375835.
4. Fortnow et al., Time-Space Lower Bounds for Satisfiability, JACM 52 (2005), DOI 10.1145/1101821.1101822.
5. Agrawal, Kayal, Saxena, PRIMES Is in P, Annals 160 (2004), https://annals.math.princeton.edu/2004/160-2/p12.
6. Lalonde, Mande, de Wolf, randomized equality communication bounds, https://arxiv.org/abs/2107.11806.
