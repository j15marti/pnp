# LSPV-3/427 | Native Resolution lifting of two complementary branches
**November 5, 2026, 10:30 PST | Route B / Hypergraph & Proof Certificates.**
**Status: KNOWN/PROVED-RESTRICTED classical syntactic lifting, independently replayed COMPUTATIONAL controls. R_mix341 global normalization, B3, superpolynomial mixed Wbar and P vs NP OPEN.**

## IDEA before SEARCH, and falsifiers
**Hypothesis.** Given ordinary-Resolution refutations of both restrictions F|x=1 and F|x=0, compile them into an exact ORIGINAL-source proof using only the pre-existing binary RES rule of fixed R_mix341, without paying for a nonexistent native split/assumption/weakening/discharge rule. Deduplicate fully unconditional shared clauses across branches.

Falsifiers: (1) original-source restoration makes a Resolution pivot disappear or introduces a tautology; (2) a satisfied restricted source is used as an axiom; (3) a missing branch or a context-local lemma leaks into unconditional inference; (4) published Resolution-hard Tseitin expanders admit two polynomially short restricted Resolution branches.

## SEARCH: governing sources and established families
Read current issue #3, governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (blob `c3889a3e514ddbd747150dcb68607013a3b2d154`), original fixed calculus `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`), AGENTS.md, CODEX.md, research skill, LSPV-3/426, and LSPV-5/366. Grok `GROKPROOF/2026-11-05_0315_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` do not supply native split discharge or B3.

**Family ledger.** Odd Tseitin on cubic graphs: one variable for each edge, each vertex forbids exactly four incorrect parity triples by four distinct width-3 clauses. At h vertices: 3h/2 variables, 4h clauses, O(h log h) DIMACS bytes; odd total charge is UNSAT. For suitable constant-degree expanders, Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001; ECCC TR99-022) give exponential **ordinary DAG Resolution** proof-size lower bounds, from expansion/width. This is not hardness for the mixed calculus. Existing LSPV-2/341 exhibits 4h-1 mixed AND3/GF(2) inferences, and proves exact optimality for simple bridgeless cubic graphs. Haken (TCS 1985) gives exponential Resolution PHP hardness, whereas Cook (SIGACT News 1976) has polynomial Extended Resolution PHP proofs; classical PHP has width-n pigeon clauses, so its transfer to 3-CNF requires an independently validated lower-bound-preserving reduction. Braun's bit-PHP theorem (arXiv:2609.23015, revised 2026-10-22) gives >exp(n/(32768 ell^2)) DAG Res(XOR) proof lines for n=2^ell, ell>=32, but its CNF clauses have width 2ell and its system has no paid conservative extensions. Do not transfer this restricted lower bound into R_mix341 without a legal compiler and size accounting.

External repos actually reviewed: `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`; `blkph0x/p-vs-np-proof-research/README.md` blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814` plus Resolution/PHP width repository search; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`. Distinct clause/XOR typed IDs are useful precedent, not native /341 authorization. Github.com/openai search for Resolution proof checker found no applicable /341 compiler. Direct Google-branded search was unavailable; indexed web and authenticated GitHub searches were performed.

## ITERATE: exact source-retreating syntactic lift (restricted known principle)
Let F_a=F|x=a remove each source satisfied by literal ell_a and delete falsified -ell_a from other sources while retaining its original clause index. Suppose P_a is an **ordinary exact binary RES** refutation of F_a with q_a paid nodes, no weakening or semantic/oracle steps. Map every indexed restricted source C_i|x=a to its *original full source C_i*, which is the restricted clause possibly plus -ell_a.

For each RES on pivot p != x, apply the same oriented pivot to its two lifted parent clauses. By induction both parents are their restricted clauses optionally augmented by -ell_a, which cannot remove p nor introduce +ell_a. Consequently the new exact resolvent is its restricted counterpart optionally augmented by -ell_a and is not a tautology. The branch's final empty restricted clause lifts to either empty or unconditional singleton -ell_a. Do this separately for a=0,1: either branch already proves empty, or two opposite source consequences x and -x are resolved by **one ordinary native RES**. All derived nodes have complete original-source proof provenance and no paid/implicit assumption node.

Hence, in the preselected native R_mix341 (containing ordinary RES), for any such supplied branch proofs:
$$
W_{R_{\mathrm{mix341}}}(F)\le W_{\mathrm{RES}}(F)\le q_0+q_1+1.
$$
This upper bound charges each legal inference once. When identical derived clauses from the two lifted **unconditional** proofs coincide, redirect a later reference to the earlier derivation; it remains justified by F and saves nodes. Identical *branch-local* clauses that have not been source-retracted cannot be shared unconditionally.

**Corollary:** If an established 3-CNF family requires S(F) paid ordinary-RES inferences, then every pair of opposite-branch ordinary-RES refutations satisfies q0+q1+1>=S(F). Thus a single split cannot bypass ordinary-RES Tseitin exponential hardness. This corollary does NOT address arbitrary nested/context-shared mixed proof DAGs or any R_mix341 GF(2), AND3, LOCAL-CONVERT, DEF shortcut.

## Independent computational controls and full cost separation
Exact original odd cubic Tseitin DIMACS inputs were instantiated for K4, K3,3 and the cube. Python producer generated variable-elimination branch proofs and compiled them into unconditional native oriented RES records. Independent JavaScript verifier reconstructed source clauses, branch restrictions and every pivot/inference from scratch, checked exact original clause refs, verified same-graph even-charge SAT models, rejected malformed/corrupted certificates and both-branch omission. **5,651 assertions evaluated, seven deliberately corrupted controls rejected**. These runs are finite certificates, not global minima.

| Graph | ASCII DIMACS bytes | Paid branch RES nodes, total | Native original-source RES nodes | Cross-branch paid-node savings | Prior mixed AND3+XOR upper |
|---|---:|---:|---:|---:|---:|
| K4 | 163 | 30 | 31 | 0 | 15 |
| K3,3 | 239 | 78 | 79 | 0 | 23 |
| Cube Q3 | 340 | 142 | 135 | 8 | 31 |

On Cube the compiler reuses eight precisely matching original-source-entailed clauses derived in the first branch while compiling the second. The 135-node certificate is not asserted minimal. Ordinary RES is a strict subsystem of /341; the mixed 31-node proof on Cube is an available shortcut, not an anomaly to exclude.

Native proof weights charge distinct inference nodes once. Independent evidence bit length, parsing, search/failed candidates, indexing/reads, constructing and writing proofs, verifying refs and clauses, DAG retrieval/recomputation, and live workspace require additional costs. Fully materialized topological proof storage is bounded by O(qN+q log(q+2)) bits for q nodes and N input-size upper bound on clause width. No arbitrary machine lower bound, native FLMV resource bound, or B3 transfer is inferred.

## Remaining obligations
Historical native LOCAL-CONVERT private/exported-wire/AND3/paid DEF/facet and affine typing are not completely serialized; the proposed CANON completions cannot replace /341 silently. Extend source retraction to mixed branch steps and arbitrary reconvergent contextual DAG sharing only after defining and checking exact native legality. Prove or refute same-R B3 independently, and find a true superpolynomial mixed Wbar family or invalidate the candidate. P versus NP OPEN.

**Readback/reproducibility note.** Full Python generator, independent Node verifier, explicit original-source proof DAGs and signed source bytes, raw JSON, SHA256 manifest, report and handoff are in the self-contained local bundle `lspv3_427_repro.zip`. It has not been asserted that the historical native checker executed these RES-only proofs; the independently written verifier checked exactly the unequivocal RES fragment.