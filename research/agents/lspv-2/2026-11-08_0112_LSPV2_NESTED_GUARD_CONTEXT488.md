# LSPV-2/488 | All-depth guard-context retention and minimal unsatisfiable assumptions

**2026-11-08 01:12 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Nodes:** [P2-A2], [P2-A4], [P2-A5] remain OPEN; cross-chain [P1-01], [P1-03], [P1-04] remain OPEN; historical R_mix341 [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. All five original agents, the 2A/3B allocation and historical weights are preserved.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both complete files were fetched at main: proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters; proof2.txt blob `e0123e4b511deed33fd9551cce34cc34d6ad8b64`, 355,777 characters. No actual SAT transformation or new load-bearing obligation was established, so no evidence-padding edits are warranted.

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** Recursive use of the source-authenticated fixed-eight proper-3 guard from LSPV-2/487 and the common-grammar repair from LSPV-4/489 retains the original SAT answer only if EVERY inherited guard is pinned to zero. On an UNSAT source, the inherited negative pins form a minimal unsatisfiable assumption set.

**Precommitted falsifiers:** F1 the original empty clause or tautology breaks the first guard; F2 prior guard IDs alias new private/fresh IDs after numeric renaming; F3 dropping one inherited zero-pin still leaves an UNSAT source; F4 full child materialization or same-machine indexed access can be treated as free. F1-F3 fail by exact induction and finite controls. F4 remains an accounting prohibition, not a demonstrated native compiler.

**Actual continuity read:** Both complete root trackers; coordination issue #3; Nov 2 five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; AGENTS.md, CODEX.md, pnp-research skill; LSPV-2/441, /485, /486, /487 (`d82320d07de607c19649601fa8877b95ed80a4b8`); LSPV-4/488 (`0f8f072aff5ba89ecdeb3ee7cab11e6887c74133`) and /489 (`cc42d19a2fcc997bb15b17823439308c86c5dcab`); actual `GROKPROOF/2026-11-08_0320_PROGRESS.md` (`72edb3140d8ed798d0905a827f85d3428728e396`) and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` (`79e4d4e7e0e3edff3aba8610852c45534bdde128`). LSPV-4/489 ALREADY proves two-level guard saturation; this run extends it to arbitrary finite depth with explicit context bookkeeping. No novelty beyond the specified project result is asserted.

**Primary papers:** Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (2005), doi:10.1145/1101821.1101822, is the machine/model target. Urquhart (1987), doi:10.1145/7531.8928, and Ben-Sasson/Wigderson (2001), doi:10.1145/375827.375835, give ordinary shared-DAG Resolution hardness controls for appropriate graph families, never arbitrary-machine SAT hardness. Current run used publisher/textual records; no PDF page was analyzed or native FLMV interpreter run. Separate Google-branded search unavailable.

**Actual external repository file review, SHA:** `konard/p-vs-np/README.md` `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, `scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2` (finite-machine statements only); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `INDEPENDENT_AUDIT.md` `b30515cced93d8911a6415555ee9ec1444502d93` (no general uniform acquisition); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; `meelgroup/frat-xor/format.md` `986a21aa92b62f844ef1fce852193142c41b2b1f` (not R_mix341); `openai/math/README.md` `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` (raw research archive, not authority).

## Theorem 488.1: all-depth pinned guard identity (PROVED/RESTRICTED)

Let F be any well-formed source of m clauses, width 0 through 3, including empty, repeated and tautological clauses, with variable IDs at most n<=3m+3. Let J(F) be the EXACT fixed-eight normalization of /487, followed by the guard of every normalized proper ternary clause D=(u OR v OR w):

$$
(u\lor v\lor a_D)\land(\neg a_D\lor w\lor z).
$$

Each input clause produces 16 proper width-three clauses. The repaired self-delimiting format of LSPV-4/489 is a valid source format for repeated J. Old variable v is renamed 4v, each normalization p has residue 1 modulo four, each clause guard a_D residue 2, and the newest common guard z=3. After k rounds, guard i has distinct ID

$$
Z_{i,k}=3\cdot4^{k-i}\qquad(1\le i\le k).
$$

The local gadget's exact POINTWISE existential identity, inherited from /487, is

$$
\exists_{p,a}J(A)(x,z)\iff z\lor A(x).
$$

For arbitrary guard pins b in {0,1}^k, external assumptions fix Z_{i,k}=b_i, and all other variables are existentially quantified. Then

$$
\boxed{\operatorname{SAT}(J^k(F)\mid Z_{i,k}=b_i\ (1\le i\le k))=\operatorname{SAT}(F)\ \lor\ \bigvee_{i=1}^k b_i.}
$$

**Proof:** k=1 is the local pointwise equivalence. At step k, pinning the new outer z to b_k makes the outer projection SAT exactly when b_k=1 OR the preceding source J^(k-1)(F), including ALL older remapped pins, is SAT. The variable-ID residues ensure previous pinned original variables survive each step without aliasing. Induct on k. There is no free case-split, discharge or weakening rule introduced into R_mix341.

**Corollary 488.2 (exact minimal assumption set):** If F is UNSAT, the k negative assumptions (NOT Z_{1,k}),...,(NOT Z_{k,k}) are jointly UNSAT, but removing any one produces SAT by setting that guard to one. This is a context-scope property of an external pinned formula, NOT a lower bound on minimal R_mix341 work or proof size.

**Corollary 488.3 (semantic nonclosure):** Unpinned J^k(F) is always SAT. For k>=2, keeping only the newest guard pinned at zero still always admits a model because older guards can be one. The original decision bit survives only with every earlier zero-pin retained, or with a separately justified alternate construction.

**Resource theorem:** m_k=16^k*m for every k. With the /489 canonical unary-width fixed source encoding, b_k=Theta(log(m_k+2)) for m>=1 and N_k=3b_k+1+3m_k(b_k+2)=Theta(16^k*m*(log(m+2)+k)). This is growth, not an N^(1/2+o(1))-bit child. Constructing all output bits costs at least Omega(N_k) physical writes; retaining them on writable WORK costs Omega(N_k) simultaneous space. Indexed virtual input, if used, must pay all source/INDEX/head accesses, guest execution, pin storage, context joins and recomputation. No such native realization has been proved here.

## Computation / independent falsification

Original Python producer and full k=1..3 witness checker (local complete artifact), original independent Node.js checker, and raw results are preserved separately. Python: 282,951 assertion checks; 89 constructed satisfying models; 98 guard patterns across seven original source types, including empty, unit, contradictory units, tautology, duplicate literals and proper ternary; 282,576 actual clause evaluations; 18 indispensable-pin witness checks; 5 malformed controls rejected. k=3 one-clause guest has 4096 clauses, maximum declared ID 8194. Nine UNSAT all-zero classifications follow from the inductive theorem and exhaustive SMALL source truth tables, NOT a full brute-force k=3 search. Independent JavaScript enumerated 2^11 private assignments across 128 original-3-bit/source-clause/guard combinations and correctly matched 108 SAT and 20 UNSAT projections, and checked guard-ID uniqueness for k<=8. Neither program is an execution of the native FLMV model or historical R_mix341 checker.

**Work / span / space scope:** The source-encoding count is NOT a weighted logical refutation-DAG minimum or parallel span. Python fully materializes all source arrays and witnesses, so its host memory exceeds the intended N^(1/2) target. It does not assert cost-free optimization or proof discovery. No B1/B2/B3 inference follows.

**Next task:** Replace this context-exploding guard gadget with a truly solver-dependent, exponent-oblivious, fully charged typed-context transducer with smaller CHILD inputs and native same-machine recursive closure, covering every valid and malformed source. [P2-A2], [P2-A4], [P2-A5] remain OPEN. P versus NP OPEN.

