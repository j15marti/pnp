# LSPV-2/492: Positive-sensitivity lower bound blocks pointwise-OR shrinking of easy strict 3-CNF
**2026-11-08 05:12 PST | Route A | PROVED/RESTRICTED (elementary witness-injection lemma) + COMPUTATIONAL; P versus NP OPEN**

**Exact proof-chain nodes:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04]; cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2]. All load-bearing universal nodes remain OPEN. No historical R_mix341 grammar, weights, task identities or schedules are altered.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** Earlier /490 and /491 required syntactic read-once branching programs to transfer component-width complexity through a pointwise OR of existential projections. Perhaps a much simpler local invariant already precludes an **all-input, pointwise-function-preserving** OR decomposition into uniformly shorter proper-CNF children, even without any restriction on the child solver. Four predeclared falsifiers: (F1) an OR disjunct can accept a falsifying input while the full OR equals the target; (F2) one satisfied child clause can become false under two distinct individual pivotal input-bit flips; (F3) existential private variables bypass the fixed-private-witness single-flip argument; (F4) this would erroneously exclude a legitimate SAT-only algorithm that ignores the whole original-variable Boolean function. F1-F3 fail under the explicit pointwise-OR hypothesis; F4 is a genuine escape and limits the result.

**Literature search and iteration:** Project LSPV-2/491 had a component-width lower bound only for syntactic 1-NBPs; the present argument drops every branching-program condition. Nisan's sensitivity/block-sensitivity decision-tree literature (SIAM J. Comput. 20, 1991, DOI 10.1137/0220062) is standard background, not claimed to be the first source for the elementary lemma. FLMV (JACM 52, 2005, Section 2.1 and Corollary 5.8) supplies the target machine and bounds; no transfer from Boolean-function representation to time is used. Dell--van Melkebeek (JACM 2014, DOI 10.1145/2629620) supplies a DISTINCT conditional sparsification/communication comparator, not the proof of this theorem. Public web search was used, but a separate Google-branded interface was not available.

## Lemma 492.1: unconditional pointwise-OR witness-sensitivity lower bound

Let f:{0,1}^n -> {0,1} and suppose an exact identity holds at **every** original assignment:

$$
f(x)=\bigvee_{j=1}^{q}\exists y_j\;G_j(x,y_j),
$$

where every G_j is a finite CNF with arbitrary auxiliary variables, literal repetitions, and clause widths. A child may use different private variables, a shared source-compiled circuit, and arbitrary legal SAT-solving algorithms; only the *explicit CNF clause representation* is counted. At a positive input a with f(a)=1, define its one-bit positive sensitivity:

$$
s_1(f,a)=|\{i\in[n]:f(a\oplus e_i)=0\}|.
$$

**Claim:** At least one satisfiable disjunct G_j has **at least s_1(f,a) distinct clauses**. In fact every G_j admitting a witness G_j(a,y_j)=1 must have that many clauses.

**Proof.** Fix such a child and a satisfying private assignment y_j. For each sensitive original coordinate i, f(a xor e_i)=0. Exact pointwise equality and OR positivity imply G_j(a xor e_i,y_j)=0. Choose one child clause C_i falsified by the single flip. C_i was true under (a,y_j), so its ONLY true literals there must be occurrences of the changing variable x_i; otherwise an unchanged true literal would keep the clause true. No single clause can be assigned to two distinct sensitive coordinates: it cannot have all its true literals supported both exclusively on x_i and exclusively on x_k, i != k. Thus i -> C_i is an injection into the child's clause records. This charges distinct clauses and does not assume read-once, unshared branches, a particular proof calculus, or an execution-time lower bound. QED.

## Strict proper 3-CNF all-input counterexample to the pointwise shrinking architecture

For any m>=1, use original variables x_i,y_i,z_i for i=1,...,m and the exactly 4m distinct original strictly proper ternary clauses

$$
F_m=\bigwedge_{i=1}^{m}\ \bigwedge_{\sigma,\tau\in\{+1,-1\}}
(x_i\lor \sigma y_i\lor\tau z_i).
$$

Here +1 denotes an unnegated literal and -1 a negated literal. There are 3m variables; every clause has three distinct original variables; exactly four sign patterns occur on each unsigned triple. Elementary propositional simplification gives the **pointwise** identity

$$
F_m(x,y,z)\equiv\bigwedge_{i=1}^m x_i.
$$

At any assignment with every x_i=1, F_m is true independently of y,z. Flipping any one x_i falsifies F_m. Thus s_1(F_m,a)=m and **every satisfiable disjunct covering such an a must contain at least m clauses**, irrespective of q and all existential child auxiliaries. The bound is sharp for general width<=3 child CNF, witnessed by the m unit clauses x_i. For strict proper ternary children, F_m itself witnesses the same order with 4m clauses.

For the existing project three-slot fixed-width canonical binary encoding, use a header width b=ceil(log2(128(n+c+3))), n declared variables and c clauses, and N=3b+1+3c(b+2) bits. The source has n=3m,c=4m, hence N=Theta(m log m). A child retaining all m original distinguished variables and at least m clause records has at least Omega(m log m)=Omega(N) bits with that same parser, so for all sufficiently large m it CANNOT fit in N^(1/2+o(1)) bits. More generally in any explicit reasonable literal-indexed grammar it needs Omega(m) bits, already larger than N^(1/2+o(1)). This is a **representation lower bound for pointwise exact OR-of-existential-CNF children**, not a lower bound for SAT-equivalent transformations.

The restriction is decisive: SAT(F_m) is trivial, always YES. A SAT-only algorithm may detect this family and answer directly, or a correct unrestricted SAT decider may output one constant SAT child without preserving f(x,y,z) pointwise. Neither is excluded. No generic solver-dependent A -> Phi(A), recursively applicable all-input FLMV contraction or arbitrary-SAT time lower bound follows. The original hard family priority is respected by using F_m ONLY as the required focused *counterexample control* against an architecture, not claiming it is hard.

## Established-hardness family and legal shortcuts ledger

- **Original cubic-expander odd-charge Tseitin strict 3-CNF:** H graph vertices, 3H/2 original edge variables, four original signed ternary clauses per vertex, N=Theta(H log H), UNSAT by odd total charge. Published size 2^Omega(H) ordinary shared-DAG Resolution lower bound on suitable expanding cubic graphs: Urquhart (1987), Ben-Sasson and Wigderson (2001). **Model:** ordinary Resolution only; no lower-bound transfer to full mixed R_mix341 or arbitrary machines. No 3CNF reduction needed. GF(2) parity elimination is an essential **upper-bound shortcut**, not to be excluded. Satisfiable even-charge versions have large *syntactic read-once NBP representation* by Itsykson, Riazanov, Sagunov, Smirnov (Computational Complexity 2021) and admit compact read-twice evaluation: both are different from SAT decision work.
- **Forcing F_m:** exact strict3 source above, SAT and trivial; 4m clauses, n=3m, sensitivity m. This is a targeted counterexample to **pointwise projection shrinkage**, not a claimed certified hard family. Legal SAT-only constant-child compression invalidates extrapolation.

## Finite verification, failure controls and costs

Independent Python reference (locally archived) executed 15,642 assertions; independently written Node verifier (locally archived) executed 13,473 assertions. The **published exact standalone JS verifier**, re-fetched and re-executed in an isolated JS evaluator, passed **8,795** assertions on 4,680 original assignments, including 1,252 unique pivotal-clauses checks, five malformed-clause controls and four missing-variable negative controls. Original F_m source was exhaustive for m=1,2,3,4, matching 4, 16, 64, 256 positive assignments. The executable's raw-results JSON was refetched and exactly matched the replay object. Encoded-size arithmetic for m up to 1,000,000 verified the restriction. No native FLMV machine or original R_mix341 checker was executed.

**Cost ledger:** logical source clauses 4m; minimum satisfiable pointwise child clauses m; explicit child evidence bits Omega(m log m) under fixed parser; no proof inference DAG or R_mix341 node-count claim. Python finite enumeration time O(sum_{m<=4}2^(3m) m^2), plus private witness tests; JS similarly O(sum_{m<=4}2^(3m)m^2); source-bit encoding O(log m) arithmetic per test case. The Python and JS hosts fully materialized input clauses, assignments and test results. Their physical time/space do NOT satisfy or measure FLMV's same-machine requirement, since they are finite verification controls. For any hypothetical compiled algorithm, parsing, output materialization, guest calls, source/index/head reads, sharing, paid references, failed search, cache, retained/recomputed states, epoch reset, and total writable peak remain unbounded by this lemma; all are required for [P2-A4]/[P2-A5]. In particular no free original source access from a smaller guest is assumed.

## Project/external continuity and scientific safeguards

Read both complete root trackers at initial blobs proof1 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2 9094495c3fdf031a3d6a44738cc97bfdd6fd9595; current issue #3 and recent comments, November 2 governing handoff, AGENTS.md/CODEX.md/pnp-research SKILL, LSPV-2/470,/472,/473,/478,/490,/491, peer LSPV-4/491,/492,/493, Grok GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70), Claude research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (blob b7150bb9ed964affd5fb90ecd24b0aa35d600bf9). Root main.tex returned blob 68188a24badda635a5983fda1c381cdb694fd497 but ZERO readable bytes, so no root edit is safe.

External exact file checks: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-machine proof status, no SAT separation); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md blob b30515cced93d8911a6415555ee9ec1444502d93 (restricted methods, no general all-input theorem); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (distinct proof format, not R_mix341). No third-party repository claims are treated as proof.

**Actual advance:** symbolic pointwise-OR **clause sensitivity injection** that removes the read-once/branching-program restriction for a universal pointwise-preservation architecture. This changes no unrestricted complexity result. [P2-A2] and [P2-A5] remain OPEN; [P2-A4] acquires a scoped architecture obstruction, not a theorem closing the resource transfer. The missing target remains a solver-dependent, exponent-oblivious, recursively iterable, all-input SAT-decider transformation meeting both fully charged FLMV time and space inequalities on the original machine. **P versus NP remains OPEN.**

References: Nisan (SIAM J Comput 1991, DOI 10.1137/0220062); Fortnow--Lipton--van Melkebeek--Viglas (JACM 2005, DOI 10.1145/1101821.1101822); Urquhart (JACM 1987, DOI 10.1145/7531.8928); Ben-Sasson--Wigderson (JACM 2001, DOI 10.1145/375827.375835); Itsykson et al. (Computational Complexity 2021, DOI 10.1007/s00037-021-00213-2); Dell--van Melkebeek (JACM 2014, DOI 10.1145/2629620).

## Publication reconciliation (exact verified main, 2026-11-08 05 PST)

Material scoped evidence added to [P2-A4] in complete root proof2.txt with current old blob `3fd90ed88dc48c19976af2c0b0c376a1752553a8`, SHA-guarded new blob `48962803e62f3939e8c51f5a19548a4016d75de4`, and complete content readback equality. Exact prewrite outbox at research/agents/lspv-2/outbox/2026-11-08_0512_LSPV2_492_PROOF2_PREWRITE_EXACT.txt has blob equal to the old complete tracker. proof1.txt unchanged at `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`. Coordination issue #3 comment 6722054943, https://github.com/j15marti/pnp/issues/3#issuecomment-6722054943, passed exact independent comment readback. Code blob `5cd16325002f13dac63b206a910a316971293434`, raw blob `01590e8168e29ca00b1c8b8de4fdd2c53fdddca8`, handoff blob `004af228aa0ea470769899c3f5641f87324945e5`; every artifact passed full-content readback. The change records a restricted *pointwise preservation* firewall only; [P2-A2], [P2-A4] universal resource obligations and [P2-A5] remain OPEN. No agents or schedules changed.
