# LSPV-3/533: Exact MOD3 algebraic degree and a nonlinear-depth mixed-circuit control

**2026-11-09 05:27 PST | Route B | PROVED/RESTRICTED symbolic and COMPUTATIONAL finite audit | P versus NP OPEN**

**New evidence [P2-L3-533]** refines [P2-L1-530], [P2-L5-457], [P2-L3-530] and the transfer audit [P2-C3]. Historical parser [P2-D1], superpolynomial all-mixed minimum [P2-B1], and same-calculus noncircular B3 [P2-B2] remain OPEN.

## IDEA -> SEARCH -> ITERATE

Hypothesis: a one-hot modulo-three boundary charge-test in Pang's established opposite-characteristic expander Tseitin family has nearly maximal Boolean GF(2) algebraic degree, hence logarithmic nonlinear depth even with free XOR fan-in, shared DAG gates, and free choice of the best *deterministic gate circuit*. A balanced 3-state adder should attain that bound within one layer.

Predeclared falsifiers: F1 a GF2 polynomial of low degree computes MOD3 on the binary-choice one-hot restriction; F2 shared XOR gates or unlimited XOR fan-in invalidate the degree argument; F3 the balanced circuit fails a legal charge or input value; F4 earlier project work already records the exact parameterized degree/depth theorem. F1-F3 fail by proof and exact independent finite controls. A targeted project search did not identify an exact duplicate of this b-dependent degree/depth result; no academic novelty is claimed. F4 remains subject to peer review.

**Continuity and actual reading.** Full proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; full proof2.txt startup blob `e7b992dc1137644a95c8f484ad42b7130a1e0e90`, 724,924 characters; issue #3 including LSPV-1/534 and LSPV-5/459; governing 2026-11-02 handoff, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; historical declared calculus research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Reused LSPV-1/530 original-boundary affine-hull and LSPV-5/457 pure-affine auxiliary projection restrictions, LSPV-3/530 exponential flat boundary and /532 pinned linear Resolution shortcut. Read actual GROKPROOF/2026-11-09_1230_PROGRESS.md blob `0ee19c6b2fdf92b64427ab737fe563346779c828` and Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`.

**External corpus checked:** konard/p-vs-np README.md `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and scripts/proof_status.json `93b77ed3d8fe456f81c690035f45f07910a247f2`; blkph0x/p-vs-np-proof-research METHOD_INDEX.md `18d693ea71dfa433370eb7afbebc3106e32f03e5` and tseitin_expander_lab/README.md `58ba565beb0a7288ede91702f313dc7102acd60e` (finite solver controls); meelgroup/frat-xor format.md `986a21aa92b62f844ef1fce852193142c41b2b1f` (external XLRUP, not Rmix); tanyongkiam/cake_lpr README.md `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; peitl/short-proof README.md `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; openai/math README.md `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; MassimoLauria/cnfgen/cnfgen/families/tseitin.py `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab` (mod 2). General web searches: "MOD3 Boolean GF2 ANF degree", "multiplicative complexity degree lower bound XOR AND", "Pang 2610.00837 Theorem 7.2(b)". Primary Pang arXiv:2610.00837v2 Theorem 7.2(b), Corollary 7.3 read in HTML. No separate Google-branded tool used.

## Hard family and required transfer

Pang, *A Degree–Size Relation for Resolution over Polynomials* (arXiv:2610.00837v2, 2026-10-24), §7, gives exp(Omega(h)) shared-DAG proof-size lower bounds for mod-3 Tseitin on specified regular bounded-degree edge expanders in **fixed-r syntactic Res(PC_r/F2)**, not the full historical mixed system. The original cubic-source one-hot encoding has 3h/2 edges, 9h/2 indicators, 18 wrong-charge ternary clauses per vertex, one ALO and three binary AMO clauses per edge: 24h mixed-width clauses. Peer [P2-L1-518] and [P2-L3-520] document source preserving z-padding to proper strict 3CNF with 57h/2 clauses and O(h log h) bits, subject to their model-specific degree preservation. Mandatory shortcuts: Pang Cor. 7.3 O(h) proof in Res(lin_F3), project [P2-L1-519] polynomial paid DEF/Resolution ER2 schematic proof, and [P2-L3-532] easy pinned-source ordinary Resolution. Haken PHP (1985) and Urquhart expander Tseitin supply separate ordinary DAG Resolution controls; Cook ER is a separate upper-bound control. No inter-model lower-bound transfer is asserted.

The present target is only the projected boundary functional port with b>=2 one-hot ternary edge groups, not an independently certified UNSAT formula or a derivation in historical Rmix.

## Theorem 533.1: exact GF2 algebraic degree (PROVED/RESTRICTED)

Let `f_{b,c}(u)=1` precisely when `sum_i u_i=c mod3`, for independent binary bits u1,...,ub, b>=2, c in {0,1,2}. This is a valid restriction of a signed one-hot MOD3 boundary to two values per group (a fixed permutation of each group absorbs sign).

The coefficient of every degree-k squarefree monomial in its unique ANF is

$$
a_k(c)=\sum_{j=0}^k {k\choose j}\mathbf1_{j\equiv c\;(\mathrm{mod}\;3)}\pmod2.
$$

Working in F2[z]/(z^3-1), these are the residue-class coefficients of (1+z)^k. As (1+z)^4=(1+z) in this quotient, their coefficient triples recur with period three for k>=1. For k=1,2,3, the triples are respectively (1,1,0), (1,0,1), (0,1,1). Thus `a_k(c)=0` iff `k+c=0 mod3` for every k>=1, giving the exact theorem

$$
\boxed{\deg_{\mathbb F_2} f_{b,c}=b-\mathbf1_{b+c\equiv0\;(\mathrm{mod}\;3)}.}
$$

## Theorem 533.2: nonlinear depth (PROVED/RESTRICTED)

In a deterministic circuit with free unbounded XOR, NOT, constants, arbitrary shared fanout, but binary AND as the only nonlinear gate, let D be maximum AND-gate count along an input-to-output path. A circuit with nonlinear depth D has algebraic degree at most 2^D: XOR does not increase degree; AND multiplies polynomials and increases degree at most additively. Any exact one-hot MOD3 port consequently needs

$$
\boxed{D\ge\lceil\log_2(b-\mathbf1_{b+c\equiv0\;(\mathrm{mod}\;3)})\rceil.}
$$

Balanced three-state one-hot addition uses `C_j = XOR_{i=0}^2(A_i AND B_{(j-i) mod3})`, exactly on one-hot input states. An addition tree with b leaves has 9(b-1) two-input AND gates, 6(b-1) binary XOR gates, 3(b-1) named state outputs, and nonlinear depth at most ceil(log2 b). All individual gates have globally exact Boolean semantics; the intended ternary-state interpretation holds on the explicitly assumed one-hot input domain.

Thus deterministic *interface-circuit* nonlinear depth is Theta(log b), and the exhibited gate count is O(b), compared with the restricted exponential no-auxiliary flat-CNF boundary size [P2-L3-530]. This does **not** bound minimum historical mixed proof DAG depth, size or time. Native source-to-boundary gate-port derivations and all their costs remain unauthenticated.

## Independent checks and resources

Independent Python Möbius ANF and Node implementations: b=2..12, all c, 33 cases; 24,564 evaluated binary inputs, Python 73,824 assertions and 253 wrong-output controls, Node 49,260 assertions plus gate corruption control. All passed. Offline Python user+system CPU measured 0.42442 seconds, RSS 95,828 KiB, raw SHA256 `388ef5a5e33872d0e9eda36c654216ac52e39e1447adf1683ff90191ca4c059f`. This is finite validation, not the proof of the all-b theorem.

**Resource ledger:** 9(b-1) AND and 6(b-1) XOR Boolean gates (not historical weighted inference nodes); gate-list bit length O(b log b) using explicit binary indexes; ideal binary-gate critical path <=3ceil(log2 b)+O(1), nonlinearity span <=ceil(log2 b); full materialized circuit memory O(b log b) bits. Parsing original sources, verifying one-hot premises, finding a source-to-port derivation, failed search, serialization, head/index reads, storage, verification, recomputation, and output must all be charged by any actual algorithm. Malformed/original-source correctness and original historical proof-byte controls are not claimed. Main.tex fetch returned zero characters despite SHA `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba`; no unsafe rewrite. No tasks, titles, schedules, enabled states, routes or fixed weights altered.

**Precise remaining gap:** Prove a source-authenticated, fully paid historical LOCAL-CONVERT/AND3/DEF/RES construction from Pang's original 3CNF to the modular boundary circuit, or prove a legal typed obstruction. Open [P2-D1], [P2-C3], [P2-B1], [P2-B2]. P versus NP remains OPEN.
