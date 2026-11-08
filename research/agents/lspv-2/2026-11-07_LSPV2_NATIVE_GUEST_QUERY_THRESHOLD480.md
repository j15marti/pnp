# LSPV-2/480: Native guest-call length barrier (restricted)

**November 7, 2026 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Nodes:** [P2-A4] evidence; [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged. R_mix341 grammar and weights unchanged.

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** The child length exponent `lambda=1/2` is a necessary barrier for a Route A compiler that *actually invokes the original unmodified native solver* on each child when that solver can be an arbitrarily polynomially padded correct decider. This is different from LSPV-2/470's full-parent trace-first time barrier and LSPV-4/416's upper-envelope calculation.

**Falsifiers stated first:** (F1) native WORK space would not count visited/read WORK positions; (F2) polynomial padding changes SAT/UNSAT/malformed labels or totality; (F3) one child above sqrt(N) still meets the target space exponent; (F4) the argument might illegitimately rule out code-aware padding removal or shared virtualized computation. FLMV Sec. 2.1 defeats F1; fixed padding and delegation defeat F2; exponent comparison defeats F3; F4 explicitly limits the theorem.

**Source review:** Read complete `proof1.txt` (initial blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), `proof2.txt` (initial blob 038cb0deb8ef1cb1666865e21c5e4115ffdd05b6), issue #3 through recent LSPV-5/420 and LSPV-1/491, governing November 2 handoff, AGENTS.md, CODEX.md, research skill, LSPV-2/470 and /479, LSPV-4/416 and /477, GROKPROOF/2026-11-06_2316_PROGRESS.md (a20fb8b3640d7574faf238a4a83a021bb0984808), and Claude WORLD-LEDGER-0001 (79e4d4e7e0e3edff3aba8610852c45534bdde128). Examined FLMV author PDF Sec. 2.1 and Cor. 5.8 with page images, https://lance.fortnow.com/papers/files/tst.pdf . General web search available; no Google-branded direct search.

**External pinned files:** konard/p-vs-np `README.md` (0e0ec77f83ad6eec1719a96066108b96ac1c2a95), `TOOLS_AND_METHODOLOGIES.md` (b3f5ceb025a75360d1956f4bb0ab6ae702761283); blkph0x/p-vs-np-proof-research `METHOD_INDEX.md` (18d693ea71dfa433370eb7afbebc3106e32f03e5), `INDEPENDENT_AUDIT.md` (b30515cced93d8911a6415555ee9ec1444502d93); meelgroup/frat-xor `format.md` (986a21aa92b62f844ef1fce852193142c41b2b1f); MassimoLauria/cnfgen `cnfgen/families/tseitin.py` (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); berkeley-abc/abc `README.md` (88a9d1a316dd9751acade746de315fd1e6e6c362); openai/math `lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` (1ced21f44ad49370d1b812e862c03c3a91d7f836). None proves an all-input A -> Phi(A).

## Theorem 480.1: native direct guest padding moment (PROVED/RESTRICTED)

Let L be any language with a fixed total correct polynomial-time decider A0 on the original indexed-random-access machine, including designated malformed encodings. For any fixed integer k exceeding the time and space exponents of A0 by >1, create a uniform total correct decider A_k that, on *every* guest input y of length m, sequentially visits, **writes and reads** (m+1)^k distinct WORK cells before running A0(y), then returns exactly A0(y)'s answer.

The padded solver remains a fixed polynomial-time decider, with tight exponents `t=k, s=k` up to polylog factors. FLMV Sec. 2.1 counts the largest WORK position visited/read even if later erased. An outer transformation that actually performs q distinct, sequential *unmodified native executions* of A_k on guests of lengths m_i must satisfy

$$
T_{\Phi(A_k)}(N) \ge \Omega\left(\sum_{i=1}^{q}(m_i+1)^k\right),
\qquad
S_{\Phi(A_k)}(N) \ge \Omega\left(\max_{1\le i\le q}(m_i+1)^k\right).
$$

This charges actual call work and peak, not the ideal logical minimum, and assumes no optimized emulation, omission, early cancellation or sharing of mandatory padding. A single actually executed guest of size `m >= N^{alpha-o(1)}`, with fixed `alpha>1/2` on infinitely many N, yields `s' >= alpha*k > max(1/2,k/2)`, violating the Route A space recurrence for that A_k. If `q >= N^{gamma-o(1)}` actual calls each have at least that guest length, then `t' >= gamma+alpha*k`, which must be compared against

$$
t'\le \max\left(\frac{11}{10},\frac35+\frac{k}{2}\right).
$$

At `alpha=1/2, gamma=3/5`, the *native padding workload* saturates `3/5+k/2`. At any `alpha>1/2, gamma=3/5`, it exceeds this envelope by `k(alpha-1/2)`. For one `N^{5/8}`-bit guest and k=8, the excess is 1 in space exponent and 2/5 in time exponent. This is **not** a tight lower bound on SAT computation, only on the explicitly mandatory native workload.

**Proof:** Fixed-k repeated WORK writes/reads are a total, polynomial, semantically irrelevant prefix; one terminal read and the sequential sweep force the guest's WORK high-water mark and real transition count to Theta(m^k), up to logarithmic counting overhead. Delegating afterward to A0 preserves both SAT labels and malformed classification. Each distinct actually executed native call pays its prefix. Adding sequential work and maximizing the simultaneous high-water mark gives the inequalities; exponent comparison gives the claimed obstruction.

**Crucial limitation:** The theorem does NOT rule out a code-aware A -> Phi(A) that proves the padding irrelevant and deletes it, runs A0 by a justified compiler, uses smaller children, shares computation, or implements a different same-machine virtual solver. It is **not** a no-go for every solver-dependent transformation. The full universal iterability, certificate, parser, malformed path and resource upper bound remain OPEN.

## Established hard-family / shortcut control

For a connected cubic graph G_H, signed Tseitin parity at each degree-three vertex becomes four proper 3-CNF clauses. The native source contains exactly 4H clauses, 3H/2 edge variables, and N=Theta(H log H) binary encoded bits. Odd total charge certifies UNSAT; on connected graphs even charge is SAT. On cubic expander families ordinary DAG Resolution has 2^{Omega(H)} refutation-size lower bounds (Urquhart; Ben-Sasson/Wigderson, exact expansion assumptions required). GF(2) elimination is a polynomial shortcut; Extended Resolution and the original mixed R_mix341 cannot inherit ordinary Resolution hardness. The finite K4 graph below is a regression control, NOT an asymptotically certified hard instance.

## Computation and resource ledger

Published Python standard-library independent producer: 16 original strict signed K4 formulas (8 SAT, 8 UNSAT), 8 malformed packets rejected, 24 literal finite WORK-cell sweeps, 92 rational exponent cases, 296 assertion groups PASS. Independently written no-import Node.js verifier: same 8 SAT/8 UNSAT, 8 malformed rejects, 15 distinct-cell sweeps, 92 integer-scaled exponent cases, 305 checks PASS. These tests do not execute a native FLMV machine nor prove the hypothetical correct A0 exists. They support only finite implementation/arithmetic. Python raw SHA256 of local full ledger: `b294175fb50ba89f8ace9d094c5a05083d987c9739c80a3bfcf47056d074b6fc`; the repository compact raw summary is distinct.

**Work:** all guest calls, prefix writes and reads, counters, parsing, indexed source/head reads, construction, search/failures, transformations, verification and output must be charged. The theorem only lower-bounds the mandatory direct calls and treats all remaining costs as nonnegative. **Space:** visiting the highest WORK position is charged even if later released. Indexed virtual input, caches, head resets and retention/recomputation require independent accounted upper bounds, not supplied here. **Proof bits:** no R_mix341 certificate is generated or verified. Local direct-call lower cost is not a bound on minimum branching shared-DAG inference cost. Native complete simulation, recursive application, both-label general source correctness remain OPEN.

**Publication:** report, independent executable, compact raw results, handoff in role-owned paths; root main.tex not modified. Node [P2-A4] may be updated with restricted evidence only. All five tasks, Route A/B allocation, schedules and historical inference grammar/weights preserved. **P versus NP OPEN.**
