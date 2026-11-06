# LSPV-2/429 | Lazy midpoint bit acquisition firewall

**2026-11-05 16:16 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | Universal FLMV contraction OPEN | P versus NP OPEN.**

## IDEA, falsifiers, SEARCH, ITERATE

**Hypothesis:** A short virtual SAT child may be expensive to generate on demand: an individual bit representing an arbitrary solver-computation midpoint can require many random-access source probes. A polylogarithmic child-bit function cannot be inferred from child *length*. Falsifiers: (1) an algorithm recovers the general pointer midpoint from fewer than k adaptive entry probes; (2) two completions disagree on queried entries; (3) a purported lower bound depends on sequential rather than indexed input; (4) a structured representation permits a shortcut.

Read the governing November 2 five-role handoff, issue #3 and current peer comments, AGENTS.md, CODEX.md and pnp-research skill, LSPV-2/427 and /428, LSPV-4/424, actual GROKPROOF/2026-11-05_1913_PROGRESS.md, and actual research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Predecessors: /428 already proved an *explicit-transition-output-bit* counting bound, /425 a one-pass memory result defeated by indexed read access, and /424 a conditional virtual-child simulator assuming cheap bit access. None established cheap acquisition for arbitrary checkpoints.

Primary source: Fortnow, Lipton, van Melkebeek, Viglas, JACM 52 (2005) 835-865, DOI 10.1145/1101821.1101822, §§2.1 and 3.1. Actual original PDF page 4 was inspected: indexed read-only input and erasure of the index tape on jumps, with bitwise-reducible virtual formulas *provided their bits can be computed with proved polylog overhead*. Viola ECCC TR25-059 (2025) studies different, communication-model pointer chasing; this is not a theorem import. Urquhart JACM 34 (1987) 209-219 and Ben-Sasson/Wigderson JACM 48 (2001) 149-169 certify restricted Resolution hardness for suitable Tseitin families, not SAT-machine lower bounds. Savitch midpoint recursion and P-complete circuit evaluation are structural comparisons, not a universal jump algorithm.

Repository reviews: konard/p-vs-np README.md and proofs/complexity/README.md specify an educational finite one-tape model, not FLMV. blkph0x/p-vs-np-proof-research README.md and METHOD_INDEX.md identify scoped finite/affine results, not an unrestricted compiler. openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean proves costs for a particular program and does not authorize a general A compiler. Targeted GitHub project searches for "pointer chasing" and "midpoint" located older communication/model-specific barriers, not an already proved all-input checkpoint jump. Direct Google-branded interactive search unavailable; indexed web and authenticated GitHub searches used. No code/CI badge promoted to a theorem.

## Theorem 429.1: exact black-box checkpoint entry-query complexity

For integers k>=1, M>=4k+8 and a total point-query oracle f:[M]->[M], define

$$
B_k(f)=f^{\circ k}(0)\bmod 2.
$$

**PROVED/RESTRICTED:** Every deterministic exact algorithm that outputs B_k(f) for *every* oracle f requires at least k adaptive oracle-entry queries on some f. Following k successive pointers attains k, so the deterministic worst-case **entry-query complexity equals k**.

**Proof:** Respond adversarially with a discovered chain 0=v_0,...,v_r whose final vertex has not been queried. A query of this frontier receives a fresh, previously unqueried successor, extending the chain. A query outside the frontier receives a consistent self-loop, and repeated queries replay previous answers. After q<k queries, r<=q, leaving a fresh frontier. Complete the path to length k-1 using previously unqueried vertices, then define its last edge in two ways to unused endpoints of opposite parity. The bound M>=4k+8 ensures sufficient unused even and odd vertices. Both total functions agree on every queried entry but have opposite B_k values. The algorithm's identical transcript forces one incorrect answer. Thus q>=k in the worst case. QED.

The adversary grants zero-cost reuse of all previously queried entries, so this lower bound is not inflated by double-counted DAG work. It is a **standard-type oracle query adversary**, not a novel machine lower bound.

## Exactly what does and does not transfer

A complete packed oracle table has m=ceil(log_2 M) bits per entry, source size N_table=Mm+O(log M). The requested virtual checkpoint output is only **one bit**. With M=4k+8 the bound is Omega(N_table/log N_table) **entry probes**, greater than polylog; an indexed read-only source does not remove the adaptive dependence on previous pointers. A literal implementation costs O(k log M) bit reads/index setup plus O(log M) writable bits. This is an upper schedule, not a matching Omega(k log M) individual-bit lower bound. Initial source parsing, validation, address write/erase, failed policy, caching and guest access are separate costs when claimed for FLMV.

**This directly falsifies the automatic premise** "virtual child has O(log N) bits, therefore its bit can be produced in polylog time" for the opaque-successor midpoint architecture. It does **not** contradict LSPV-4/424, whose conditional theorem expressly *assumes* a proved locally addressable bit generator.

**Countercontrol:** For the white-box update f(v)=v XOR 1, f^k(0)=k mod 2 is computable with O(log k) arithmetic, despite the k-query black-box lower bound. Thus no lower bound transfers to circuit-aware algorithms without further argument. One Omega(N_table/log N_table) midpoint cost can fit N^(11/10+o(1)) local time; multiple children can share the same traversed prefix; no qk direct sum or violation of Route A's target follows.

For a deterministic solver A, the program code and source are not an opaque oracle. Compiling a signed CNF transition gadget does not hide the algorithm's structure, and idle/delay portions may be skipped. No theorem for arbitrary A was obtained.

## Existing certified-hard 3-SAT control

For a cubic graph on H vertices, introduce a variable per edge (3H/2) and four proper 3-clauses at each vertex blocking the wrong parity assignments. On suitable cubic expander families with odd total charge, published **ordinary shared-DAG Resolution** requires size 2^Omega(H). A dense-ID source requires Theta(H log H) encoded bits. The actual K4 and cube finite controls below are not certified expander-hardness instances. Existing project LSPV-2/341 supplies an allowed AND3/GF(2) mixed-calculus refutation in 4H-1 paid nodes for its verified bridgeless cubic family. Therefore the restricted ordinary-Resolution theorem is a mandatory shortcut control and cannot be transported to all SAT machines or to the stronger fixed Rmix341.

Finite controls: K4 has six edge variables and 16 proper 3-clauses; cube has twelve variables and 32 clauses. Even zero charge SAT; one-hot odd charge UNSAT, with all valuations enumerated. They are authentic standard Tseitin instances, not new hard-family proposals.

## Exact finite evidence and ledger

Local full producer generated 70 adversarial pairs, k=2..15 and five index-query policies, with a recorded seed and whole-tables for independently checking every transcript. Local Python producer recorded **1,330 assertion units**; independent Node verifier completed **3,021 checks**, covering 70 pairs, five white-box XOR shortcuts, four both-label original 3-CNF instances, four malformed DIMACS rejections and a corrupted-oracle rejection. Full uncompressed raw JSON SHA-256: 14feeb20711039c2abdcd501aa53a8724d9a8ba04208a502aec1ac42e8b981f0. The standalone shortened JS test was run separately locally and gave **56 adversarial cases, 549 checks**, including both-label K4/cube and XOR jumps. Full code/data are in the accompanying reproducibility archive; the GitHub code path is the standalone compact replay. No finite run was an execution on the native FLMV Turing machine or a certificate of polynomial exponents.

| Object | Lower/known result and model | Shortcut | Open transfer |
| --- | --- | --- | --- |
| Cubic-expander odd Tseitin proper 3-CNF | 2^Omega(H) **ordinary DAG Resolution** for suitable expanders; 4H clauses; N=Theta(H log H) | Historical mixed Rmix341 proof <=4H-1 nodes | No unrestricted SAT machine hardness |
| Packed successor with midpoint bit | k deterministic **opaque oracle entry probes** for k iterations | Algebraic/code-known XOR jump O(log k) | No white-box arbitrary-A checkpoint bound |
| LSPV-4/424 virtual child | Conditional time t'<=max(d,a+lambda*t) and space s'<=max(rho,eta,lambda*s) | Polylog local child-bit acquisition when separately proved | Universal, recursively applicable local bit generator missing |

**Physical resources:** Node weights/derivation-DAG count are not used as machine work here. Full host Python/JS work and memory only validate finite cases. The oracle lemma measures distinct source-entry requests with arbitrary local space; it is not a full SAT time/space lower bound. In any proposed solver wrapper charge original-source reads, index tape erasure, intermediate state bits, all live ancestors, per-child iteration, and peak across *every* local phase.

**Next task for Route A builder and LSPV-4:** Construct a code/source-authenticated jump or locally addressable projection for arbitrary SAT decider A with explicit amortized acquisition bound; justify composition of SAT and UNSAT labels and recursive applicability. Otherwise formalize a more expressive, yet still honest restricted no-go. Existing two Route A / three Route B allocation, native Rmix341/weights, task identity/schedule and prior results unchanged. FLMV transformation OPEN; B1/B2/B3 OPEN; P versus NP OPEN.

## Primary sources and paths

1. FLMV 2005 DOI 10.1145/1101821.1101822, PDF https://lance.fortnow.com/papers/files/tst.pdf .
2. Urquhart 1987 DOI 10.1145/7531.8928 .
3. Ben-Sasson and Wigderson 2001 DOI 10.1145/375827.375835 .
4. Viola ECCC 2025 TR25-059 https://eccc.weizmann.ac.il/report/2025/059/ , a different *communication* model.
5. Project and peer paths, Grok/Claude, required external repository files recorded above.
