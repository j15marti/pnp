# LSPV-4/510 | Growing Resolution-hard Tseitin trace cylinder and trailing-length guard

**2026-11-08 20:36 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Nodes:** new [P2-L4-510] (restricted evidence toward [P2-A4]); [P2-A2], [P2-A4] full, [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-B1], [P2-B2] remain OPEN. Historical R_mix341 unchanged.

## IDEA -> SEARCH -> ITERATE; falsifiers

**Initial hypothesis:** LSPV-2/512's 4096 child same-trace fixed-K4 control can be generalized to *growing* original strict 3-CNF odd-charge cubic Tseitin sources with fresh, independently signed tail clauses, retaining precise source authentication and a small indexed WORK footprint. F1: truncation at an unread last sign yields false acceptance; F2: tail flips cause SAT/malformed sources; F3: wrong incidence/parity passes; F4: hidden full-source storage, trace storage or a claimed all-input decomposition invalidates the resource bound.

**Revision:** The final sign in a raw packet cannot be skipped while establishing exact source length if no independent length primitive is available. Define a separate, explicit **two-bit trailing marker** after all clauses and query marker+following blank. Thus every tail polarity bit may remain unobserved, and truncated/overlong inputs are rejected without an uncharged length oracle. This modifies a NEW source grammar, never the historical R_mix341 proof grammar.

Read both complete root trackers before work: proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters); proof2.txt blob `9aa65c584f324e5ba277d5d5ce53b348a5f0002b` (603,081 characters). Reviewed current issue #3 through LSPV-2/512, governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, LSPV-2/512 (`research/agents/lspv-2/2026-11-08_2012_LSPV2_SAME_PARENT_VIRTUAL_XOR_PORT512.md`, blob `20928dbaf238ffe0364823b232fb61d19d8d952e`), LSPV-4/509 (`research/agents/lspv-4/2026-11-08_1939_LSPV4_VIRTUAL_ALIAS_FIREWALL509.md`, blob `7ba87628d5eec733e11ec851a4c82418e6fc1e36`), Grok `GROKPROOF/2026-11-08_0930_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`. No novelty claimed for prior Tseitin, padding or trace reuse.

Outside repositories actually read (path, Git blob): `konard/p-vs-np/README.md` `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, `scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/README.md` `f397a7747eaca82df3d754d0a4b4bab1fe10f814`, `METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `INDEPENDENT_AUDIT.md` `b30515cced93d8911a6415555ee9ec1444502d93`; `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; `meelgroup/frat-xor/README.md` `38a137bca4d4ab6443703d4c31fba5783021c581`; `berkeley-abc/abc/README.md` `88a9d1a316dd9751acade746de315fd1e6e6c362`; `openai/math/CONTENTS.md` `7e1ed90ac5a666f1bbecb22027387c4ad79e9d03`. These prove neither all-input acquisition nor a native FLMV contractor. Targeted review only. A Google-specific search interface was not available, but public web and exact GitHub reads were used.

Primary papers inspected: Ben-Sasson/Wigderson, *Short Proofs Are Narrow*, JACM (2001) Definition 4.1, Theorem 4.4, Corollary 4.5, https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf (page 156 screenshot checked). Fortnow/Lipton/van Melkebeek/Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM (2005), Section 2.1, https://lance.fortnow.com/papers/files/tst.pdf (page 4 screenshot checked). Urquhart (1987), *Hard Examples for Resolution*. Restricted system evidence is not arbitrary-machine hardness.

## Exact family, encoding and transfer theorem

Let `G_H` be any connected simple cubic graph, `H` even vertices, `m=3H/2` edge variables. Each vertex has charge `b_0=1` and `b_v=0` otherwise. The **four original width-three clauses** at vertex `v` forbid precisely the four 3-bit edge assignments whose XOR differs from `b_v`. The core `Gamma_H` has `4H` proper strict 3-CNF clauses, `m` variables and `12H` original literal occurrences. Summing parity equations gives `0=1`: UNSAT.

Choose `k=max(2,ceil((2/5)log2 H))`. Add `k` ternary clauses on distinct fresh variable triples `(m+3j+1,m+3j+2,m+3j+3)`; independently select their `3k` polarity bits `z`. Each result `F_(H,z)` is original-variable duplicate-free proper strict 3-CNF and UNSAT. On any growing connected cubic edge expander family with `e(G)=Omega(H)`, the established **ordinary shared-DAG Resolution** bound is `S_Res(Gamma_H)=2^Omega(H)`. Restrict any putative Resolution refutation of `F_(H,z)` by an assignment satisfying all fresh-variable clauses. Restriction deletes the tails and does not increase Resolution inference count, hence `S_Res(F_(H,z)) >= S_Res(Gamma_H)`. Conversely ignore all tails. Therefore

$$
S_{\mathrm{Res}}(F_{H,z})=S_{\mathrm{Res}}(\Gamma_H)=2^{\Omega(H)}
$$

for that expander subfamily. **This is restricted Resolution proof-size preservation only**, not all-machine SAT hardness or an R_mix341 lower bound. GF(2) summation is a fast legal semantic shortcut control.

NEW binary grammar: 8-bit magic `10100101`, prefix-free Elias-gamma(H), gamma(m), gamma(k), `4H+k` ordered clauses of 3 records `(w-bit ID, sign)`, `w=ceil(log2(m+3k+1))`, then terminal `01` and the following INPUT cell blank. Every original variable identifier and core sign is authenticated. Tail IDs must be the stated fresh triples; tail signs remain unchecked since all 0/1 polarities are syntactically legal. Size is unbounded:

$$
M=8+\ell(H)+\ell(m)+\ell(k)+3(4H+k)(w+1)+2=\Theta(H\log H),
\quad \ell(n)=2\lfloor\log_2n\rfloor+1.
$$

The odd core need not be recognized as an expander: check its four parity clauses per vertex and that every edge ID appears in exactly two distinct vertex blocks. Then even disconnected graphs with exactly one odd-charged vertex give an UNSAT component. Expander *hardness* still requires the separately published expansion premise.

## Restricted same-machine indexed guard and physical ledger

A deterministic guard reads gamma-header, checks trailing `01` and blank, then verifies every four-clause parity block, and for each original edge ID `e=1..m`, rescans the `H` vertex blocks to count exactly two endpoints. Checks all tail *ID fields*; does **not query any of the 3k tail sign positions**. No full input/graph is stored; only counters, 4 local clauses, positions and INDEX-tape words of `O(log M)` bits. Every indexed INPUT read programs and clears an INDEX tape; INPUT positions themselves do not charge non-index WORK-space high-water in FLMV §2.1. The guard performs `O(H^2 log H)` bit reads and `O(H^2(log H)^2)=O(M^2)` physical steps with conservative index programming, `O(log M)` extra WORK/index high-water.

A program `G_B` that runs this guard, returns UNSAT on acceptance, and otherwise resets scratch and invokes any total correct binary-CNF classifier `B` is (conditionally on B) correct on SAT/UNSAT/malformed inputs. Worst-case guest complexity includes `T_B(M)+O(M^2)` and `max(S_B(M),O(log M))`; on the accepted hard family B is not invoked. This is an effective *special-case recognizer*, NOT a new all-input speedup. The hosted scripts are **not** native FLMV instruction-level interpreters.

All `q=2^(3k)=Theta(H^(6/5))` tail-sign variants of one immutable parent share the genuine deterministic completed guard trace because none of the varying bits is observed; their initial state, read values, effects and UNSAT label agree. Descriptor enumeration and checks can stream in `O(qk log M)` time and `O(log M)` extra WORK. The executable implementation may retain one accepted flag and a trusted syntactic-invariance argument; **it does not store an uncharged O(M²)-step dynamic trace.** Literal replay of a retained arbitrary trace remains separately unimplemented. Set **only a formal workload parameter** `N=M²`, without claiming an actual all-input parent reduction:

$$
T_{\rm restricted}=O(M^2+qk\log M)=N^{1+o(1)},\quad
S_{\rm extra}=O(\log M),\quad q=N^{3/5-o(1)}.
$$

If all children must be explicitly serialized, output alone costs `Theta(qM)=N^(11/10-o(1))` bit writes, with output and materialization counted. Sequential temporary CHILD occupancy `O(M)` fits `N^1/2` but simultaneous storage `qM` does not. No general reducer or recursively iterable all-input contraction has been built.

**Charge ledger:** source parser/scans O(M²) time, O(log M) WORK; INDEX generation/erasure included; tail grammar and boundary validated; policy search none for this **fixed** guard, NOT free in general; output q or qM paid bits; descriptors O(qk logM) time and O(logM) WORK; failures/malformed cases fall back to full B with its time/space; guest source reads and WORK high-water charged; retained dynamic trace not stored; branch reconvergence and reference/application costs beyond this pure decision wrapper are not free; proof evidence bits and fixed R_mix341 inference-node counts are *not generated or inferred*. All-phase peak includes the guard and eventual fallback, not only final-state memory.

## Independent computation

Independently written Python and Node finite scripts generated **identical original-packet SHA-256s** on K4, K3,3, Q3 and Heawood (`H=4,6,8,14`). Each instance uses k=2, six unread signs, and all 64 tail-sign variants; **256** virtual children in each script, all strict3/UNSAT with identical authenticated guest read sets and values. Packets are respectively **293,415,639,1073** bits; distinct observed INPUT positions **288,410,634,1068**, including the one terminal blank probe. Worst-case symbolic per-anchor input read counts **579,1061,2077,5481** under repeated incidence rescans. Negative checks reject missing/incorrect trailer, truncation, appended bits, core-sign mutation, incorrect tail ID and an even-charge SAT control. Python additionally brute-force classifies K4 and K3,3 original strict-3CNF sources; Heawood is **finite only**, not an asymptotic Resolution-hardness certificate. No historical R_mix341 checker or native FLMV machine executed.

Published verifier: `experiments/arc/lspv4_510_independent_node.mjs`. Raw JSON: `results/raw/arc/2026-11-08_2036_LSPV4_510_GROWING_CYLINDER_RAW.json`. Independent Python and full report available in the linked reproducibility archive.

**Actual advance:** Explicit unrestricted-size family grammar and rigorously scoped fresh-padding Resolution preservation, plus a trailing-length-authenticated no-tail-read guard with costed low-workspace rescans and a growing `N^(3/5-o(1))` replay-compatible portfolio. This is a *restricted upper-bound/control*, not universal compression. **OPEN:** [P2-A2], full [P2-A4], [P2-A5], [P2-D1], [P2-B1], [P2-B2]; all of P versus NP. No schedule, agent, role, enabling, historical calculus/weight or other role manuscript edits. Root `main.tex` not changed because a complete authenticated ownership-region readback was not acquired.
