# LSPV-4/421: Multipass boundary rescanning cannot satisfy both proposed FLMV local resource exponents in a restricted streaming compiler

**2026-11-05 13:08 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## IDEA before SEARCH: exact falsifiers

Starting from LSPV-2/425's authenticated two-block 3-CNF source gadget, test whether a sequential compiler can trade a small number of full-source rereads for the large one-way retained boundary message. Falsifiers: (1) two prefix sets might have identical future SAT behaviour, (2) p passes may meet both q <= N^(1/2+o(1)) writable space and T <= N^(11/10+o(1)), (3) signed source encoding may vary in size or lose SAT/UNSAT equivalence, (4) indexed random reaccess or algebraic compact representations invalidate any general-machine lower-bound inference. Falsifiers (1) and (3) are excluded by construction and checks; (2) is falsified for the declared streaming architecture; (4) succeeds and blocks all-machine transfer.

## Exact source and prior hard-family ledger

Let m>=2, M=2^m and public x in {0,1}^m. LSPV-2/425 defines for every a a mismatch disjunction of m literals, together with a fresh switch u_a whose forced value is the membership bit of a in a set S. Implement each (m+1)-literal disjunction by m conservative OR2 gates, each with three defining clauses, and an output unit. Construct independent prefix F_S and suffix G_T with globally fresh private gates. Their existential projected relations are exactly S and T, respectively. Hence

$$
F_S \land G_T\in\mathrm{SAT}\quad\Longleftrightarrow\quad S\cap T\ne\varnothing.
$$

The fixed-slot binary source encoding uses an exact-width header, a two-bit arity per clause and (one sign bit plus d ID bits) per literal. Each source has V=m+2M(m+1) variables, C=2M(3m+2) clauses (width at most three) and 2M(7m+2) literal slots. With d=ceil(log2(max(V,C)+1)), its length is exactly

$$
N=3d+1+2C+2M(7m+2)(d+1)=\Theta(m^2 2^m).
$$

All S,T sources at fixed m have identical length: membership changes only sign slots. This is a focused **control gadget**, not a newly claimed hard 3-SAT family.

Published comparison: suitable cubic expander odd-charge Tseitin instances have H vertices, 3H/2 edge variables, 4H signed width-three clauses and N=Theta(H log H). Urquhart (JACM 1987, DOI 10.1145/7531.8928) and Ben-Sasson/Wigderson (JACM 2001, DOI 10.1145/375827.375835) establish exp(Omega(H)) **ordinary shared-DAG Resolution** lower bounds, not arbitrary machine hardness. The established native AND3/GF(2) mixed refutation costs 4H-1 paid nodes on applicable bridgeless odd-charge sources (LSPV-2/341), so ordinary-Resolution hardness does not transfer to the full mixed calculus. Haken PHP and Cook ER are separate controls.

## Theorem 421.1: exact scoped p-pass resource tradeoff

**PROVED/RESTRICTED.** For fixed m, consider every deterministic exact algorithm on all sources F_S AND G_T that makes exactly p>=1 complete *left-to-right sequential* scans of the same read-only source. Between scans it may rewind, but within a scan it cannot seek or reread a prefix. It has at most q bits of simultaneously live writable configuration at each prefix/suffix crossing, including caches, states, indices and counters; no externally rereadable output. If crossings encode a fixed q-bit configuration, then

$$
\boxed{(2p-1)q\ge M.}
$$

Variable pass counts, early halting and variable-length crossing encodings change the inequality only by O(1) per crossing. There is a matching deterministic p-pass streaming solver on this promised source family with q<=ceil(M/p)+O(log N) and T=O(pN polylog N), including source-template checks.

**Proof.** Give Alice the prefix F_S and Bob the suffix G_T. Simulating the p source scans requires at most 2p-1 transmitted complete configurations of q bits each. This yields a deterministic communication protocol for DISJ(S,T)=[S intersect T = empty]. Its 2^M disjoint input pairs (S, complement S) form a fooling set: if S differs from S', at least one of (S, complement S') or (S', complement S) has nonempty intersection. Distinct accepted fooling pairs cannot share a deterministic full transcript, because transcripts define combinatorial rectangles and would then incorrectly accept both crosses. Thus at least 2^M distinct transcripts are required, while (2p-1)q communication bits provide at most 2^((2p-1)q). This gives the inequality. For the upper bound, partition the M possible a-values into p chunks, cache only S-membership bits in the current chunk, compare the matching suffix T bits during that pass, and retain a single SAT flag. The full template and malformed-string checks cost sequential parsing/indexing, all of which are charged.

**Resource corollary.** If all-phase retained space is q<=N^(1/2+o(1)), then p>=N^(1/2-o(1)) (polylog factors absorbed). Every complete source scan reads N bits, so this architecture needs T>=N^(3/2-o(1)). Thus it cannot meet simultaneously rho<=1/2 and local aggregate exponent d<=11/10. This only excludes the **full-pass sequential boundary-join architecture**.

**Mandatory indexed-access escape.** The actual FLMV model (Fortnow/Lipton/van Melkebeek/Viglas, JACM 2005, §2.1) has indexed random read-only input and charged index-tape writes/erasures. On these *same promised inputs*, a source-template validator can probe corresponding switch-sign slots for each a using O(log N) writable scratch and O(N polylog N) operations. Consequently the communication lower bound does not apply to arbitrary FLMV machines or prove a universal A-to-Phi(A) impossibility. No free input oracle, case-split rule or source-to-Rmix proof inference is introduced.

## Branch sharing and all-phase accounting

The prefix set S is shared across suffix possibilities. Keeping all its membership bits costs M writable bits; storing one chunk costs ceil(M/p) and forces p complete rereads. A SAT witness needs one a in S intersect T (OR), but UNSAT of the conjunction requires establishing the absence of all such a (AND). No branch-local lemma may be reused across incompatible assumptions without a legal discharge. This calculation concerns machine work, not the weighted union of native R_mix341 inference nodes. Work, ideal span and a realizable sequential storage/recompute schedule remain distinct. The streaming upper bound charges all source bits p times, parser/index updates, cache allocation and clearing, failed searches, final label output and peak writable state. It constructs neither a short ordinary-CNF guest child nor an arbitrary-guest simulation.

## SEARCH and iteration record

Read the governing Nov 2 handoff (blob c3889a3e), current issue #3 through LSPV-4/420 and LSPV-2/425, AGENTS.md/CODEX.md/pnp-research skill, actual GROKPROOF/2026-11-05_1913_PROGRESS.md and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex. Both peers leave Route A open. Literature searches: 'deterministic multipass streaming set disjointness communication complexity space passes tradeoff', 'FLMV indexed random access tape model', 'Urquhart hard examples for Resolution', and 'Ben-Sasson Wigderson Resolution expander'. Primary sources: FLMV author PDF https://lance.fortnow.com/papers/files/tst.pdf ; Urquhart 1987; Ben-Sasson/Wigderson 2001; Guruswami/Onak CCC 2013 and Assadi/Kol/Saxena/Yu arXiv 2009.03038. Direct Google-branded search unavailable; indexed web search used instead. The deterministic DISJ fooling-set argument is fully proved above, with no imported randomized lower bound.

Actually read these exact GitHub sources: konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e (finite one-tape formal model, not FLMV), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea and ADAPTIVE_FRAGMENT_SYNTHESIS_REPORT.md blob b4ef7e87 (bounded finite interface synthesis), openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4 (one specific algorithm only), MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd19 (established parity source generator). Source implementations are not universal theorems.

**COMPUTATIONAL:** Full Python and independently written JS producer/referee in reproducibility archive. Python enumerated 328,704 pair/pass correctness checks and 32,760 fooling-pair checks, plus 14 exact original-CNF binary encoding/source-hash roundtrips, 84 public-assignment clause checks and 56 malformed controls. Independent JS: 361,993 assertions passed. Two very large symbolic integer-ledger rows are excluded from JS due to IEEE-754 limits, but checked with Python arbitrary-precision integers. Code SHA256: producer a191a6d0fb937be1b32e283fd1a2d0d81e79ee1668191d446182dc0fca48f6f8; JS f9f9bdb45e79a4205f357fce86726478a5b28e8114e396628c4a88403674a03d; full results c4a55b3f701bf19039fc4cf4a7d2fd18242d31df80fc403676b374272ff543a4. Host tests are not physical FLMV benchmarks. Full 14KB proof report, complete scripts/results, logs and manifest are supplied in downloadable archive LSPV4_421_MULTIPASS_BOUNDARY_RESOURCE_REPRO.zip.

**OPEN:** Build an all-input, both-label/malformed-aware, recursively iterable SAME indexed-machine A-to-Phi(A) with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2), including rho, eta, lambda, guest reads, indexing and simultaneous peak. Route B's full-mixed Wbar/B3 remains separately OPEN. P versus NP OPEN.

**Root manuscript:** main.tex blob 1b8a7d9a... returned zero readable bytes, so no unsafe overwrite was attempted. Historical rules, weights and all task identities/states/schedules remain unchanged.
