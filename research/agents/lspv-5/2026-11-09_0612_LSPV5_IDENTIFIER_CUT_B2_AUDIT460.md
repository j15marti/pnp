# LSPV-5/460: independent arbitrary-identifier and worst-case-envelope audit of the conditional B2 countercontrol

**2026-11-09 06:12 PST | Route B independent red team | PROVED/RESTRICTED reduction audit + COMPUTATIONAL controls + CONDITIONAL external premise. P versus NP OPEN.**

**Affected evidence node: [P2-L5-460].** It independently refines peer **[P2-L1-534]** and the B1/B2 quantifier ledger **[P2-B3]**. Historical grammar **[P2-D1]**, complete mixed normalization **[P2-C3]**, all-rule mixed lower bound **[P2-B1]**, and same-calculus B3 **[P2-B2]** remain OPEN. Route-A **[P1-01]**, **[P1-03]**, and **[P1-04]** remain OPEN.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** An ordinary/regular-Resolution hard-family transfer into the full fixed $R_{mix341}$ minimum fails if the same exact source admits a polynomial GF(2) or extension-variable shortcut.

**Predeclared falsifiers.** (F1) the authenticated historical grammar plus a polynomial normalization retracts every legal mixed proof into the cited lower-bound system; (F2) the selected family has a lower bound in a system covering every relevant mixed, algebraic, extension, split and sharing rule; (F3) an explicit polynomial shortcut exists but the tracker already records the family failure at its exact scope; (F4) a peer supplies a source-bound rule-by-rule transfer, not equisatisfiability or empirical hardness.

**Search changed the target.** F3 fired for the newest MOD3 work: [P2-L3-533] explicitly gives a balanced nonlinear adder upper control and refuses promotion of its GF(2)-degree bound to mixed-proof hardness. Repeating that caveat would not be progress. The revised target was peer [P2-L1-534], whose substantive claim is different: conditional on one uniform $2^{o(n)}$ at-most-3SAT machine, an explicit-identifier decomposition yields an all-input general-CNF decider with cumulative worst-case time $2^{o(N/\log N)}$, which conditionally falsifies B2 for the **distinct** fixed system $Res(PC_1/\mathbb F_3)$ using Pang's established random proper 3-CNF lower bound.

## Exact continuity and search record

Both trackers were read completely. Initial `proof1.txt` blob: `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters). Initial `proof2.txt` blob: `8abfd93ba4f9accb3dde07bd8a2b806853ebb856` (731,025 characters), including [P2-L1-534], [P2-L3-533], and [P2-L4-520]. Read issue #3 through the current paginated comments, the historical five-role handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current LSPV-4/520 handoff blob `2e35b6de29fdd2be660928dd2cde0bb2285d64ff`, AGENTS.md blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`, CODEX.md blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, and the complete research instructions/protocol blobs `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`, `c211e9f545f94b636b119f1e721b475a31e925f9`, and `25b38dc02bc0b0331ed03b0a4c7ff1b1e2a4ed00`.

Actual assessment files: `GROKPROOF/2026-11-09_1230_PROGRESS.md` blob `0ee19c6b2fdf92b64427ab737fe563346779c828`; `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`. Neither supplies an historical mixed normalization or B3 bridge.

Change-aware repository heads were unchanged: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c` with actual `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` with `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc` with `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`; CNFgen `24e633bdbed0d0998493bee99c42faf480c7dc96`, actual Tseitin generator blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`; `anthropics/formal-math` `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. These repositories provide controls and claims, not an $R_{mix341}$ theorem.

Primary research was read at source. Pang, arXiv:2610.00837v2, defines $\mathcal F(n,w,\Delta n)$ as independent uniformly selected proper signed width-$w$ clauses with repetitions and Theorem 7.2(a) gives $\exp(\Omega(n))$ all-DAG node size in fixed $Res(PC_r/\mathbb F_p)$ for fixed $w\ge3$, $\Delta\ge2^w$, prime $p$, and $r\ge1$, asymptotically almost surely. Thus $w=3,\Delta=8,p=3,r=1$ is the exact restricted hard-family control. The paper defines proof size as DAG nodes, matching the distinct unit-node measure used by [P2-L1-534]. This is not historical mixed-system hardness.

Public indexed web search also read the October 25 OpenAI manuscript and the primary Impagliazzo-Paturi 2001 ETH definition. A separate Google-branded engine was unavailable and is not claimed.

## Audit theorem 460.1: arbitrary explicit identifiers

Assume the source grammar physically repeats each canonical nonempty binary identifier at every literal occurrence. For source length $N$ and

$$
L=\left\lfloor\log_2\left(\frac{N}{(\log_2N)^2}\right)\right\rfloor,
$$

there are fewer than $2^L$ possible identifiers of length below $L$. Branching on all occurring short identifiers therefore uses at most $2^{2^L}=2^{O(N/(\log N)^2)}$ branches. After simplification, every residual literal occurrence contains at least $L$ paid source bits, so the number $Q$ of residual occurrences satisfies $QL\le N$. Dense renaming plus the standard existential clause chain uses at most $Q$ original variables, at most $Q$ fresh chain variables, and $O(Q)$ clauses. Hence each guest has at most $2Q=O(N/\log N)$ variables and polynomially many encoded bits.

The published peer JavaScript uses `Number.isSafeInteger` and therefore tests only machine-sized identifiers. That does not falsify the symbolic theorem, but it left the arbitrary-bitstring evidence untested. The independent Python verifier here treats identifiers as canonical strings and never converts them to integers. It tested 41 exact sources, including identifiers up to 8,192 bits, a five-literal long-ID chain, 28 SAT and 13 UNSAT sources, 309 short-ID branches and ten malformed encodings. Every source label matched the union of the converted guest labels; every residual satisfied $QL\le N$ and every converted guest satisfied the $2Q$ variable bound.

## Audit theorem 460.2: cumulative worst-case envelope

[P2-L1-534] states a pointwise exact-length construction and concludes

$$
T_A^{wc}(N)=\max_{|x|\le N}T_A(x)=2^{o(N/\log N)}.
$$

The missing max-envelope justification is valid. Write the pointwise exponent at length $m$ as $h(m)=\varepsilon(m)m/\log m$, where $\varepsilon(m)\to0$, absorbing finitely many small lengths into a constant. Split $m\le N$ at $\sqrt N$.

For $m\le\sqrt N$, eventually $h(m)=O(m)$, so

$$
\frac{\max_{m\le\sqrt N}h(m)}{N/\log N}
=O\left(\frac{\log N}{\sqrt N}\right)=o(1).
$$

For $\sqrt N<m\le N$, $m/\log m\le N/\log N$ for large $N$, while

$$
\sup_{m>\sqrt N}\varepsilon(m)\longrightarrow0.
$$

Therefore $\max_{m\le N}h(m)=o(N/\log N)$. This repairs the quantified passage to the exact B2 definition; it adds no proof-system transfer.

## External premise and trust boundary

The OpenAI proof-bearing file `lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean` blob `a69635a2492e06a26f2e33d4251edd1e21ba3332` contains explicit theorem bodies for `compiled_exact_count_and_sat`, `exact_count_and_sat`, and `original_sat_main`; the separate comparator challenge blob `a8d5ff3a3e80323675b1f2d1ea611560b783e9ca` ends in `sorry`. Comparator metadata blob `d4cc9e7074e900c1aa6371151cfd234c121a0b82` permits only `propext`, `Quot.sound`, and `Classical.choice`. No GitHub workflow run or commit status was exposed for the pinned commit. This environment has neither Lean nor Lake, so no independent build or `#print axioms` replay occurred.

Anthropic's independent repository states the same type of subexponential result. Its `eth/Solution.lean` blob `176892178e49792ae41368c13bb4973bae035b29` supplies proof terms; comparator blob `85f16dc55e511335729e668917308b375f0f6036` permits the same three standard axioms and enables `nanoda`. This run inspected those files but did not build them. Accordingly, the algorithmic premise remains **CONDITIONAL EXTERNAL**, exactly as [P2-L1-534] labels it.

## Classification, resources and remaining gap

**PROVED/RESTRICTED:** the explicit-identifier decomposition and cumulative $T_A^{wc}$ envelope are correct under their stated grammar and uniform guest premise. Combining them with Pang's theorem conditionally falsifies B2 only for the distinct fixed calculus $Res(PC_1/\mathbb F_3)$. The hard family is already proper 3-CNF; no equisatisfiable reduction is used to transfer its lower bound.

**COMPUTATIONAL:** independent verifier SHA-256 `410fe93e9fc69f6d00031a56f88a8254b19e63dc9273ea9e846ce590d00bfaaf`; raw SHA-256 `d7a244b592c70637568d30f10a6bb0c5493a411cc01a6d0bb7b74931a6c96bf0`; 0.0245 hosted seconds and 9,088 KiB reported peak RSS. The verifier charges parsing, identifier storage/comparison, branching, simplification, dense renaming, chain construction and exhaustive finite guest checking. It does not execute the external algorithm, Pang's asymptotic lower bound, or the historical checker.

**OPEN:** this says nothing about [P2-B1] or [P2-B2] for historical $R_{mix341}$. GF(2), AND3, extension, LOCAL-CONVERT, branching and shared-DAG shortcuts remain legal candidates until [P2-D1]/[P2-C3] is completed. It is a B2 countercontrol for another calculus, not a B2 counterexample for the target calculus and not a P-versus-NP result.

Local preflight failed because the partial scratch checkout lacks root `main.tex`, AGENTS.md, CODEX.md and the local skill file; authoritative remote versions were read. Root `main.tex` again returned an empty body at blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` and was not edited.

Publication: code `experiments/review/lspv5_460_identifier_cut_b2_audit.py`; raw `results/raw/arc/2026-11-09_0612_LSPV5_460_IDENTIFIER_CUT_AUDIT_RAW.json`; handoff `research/coordination/2026-11-09_0612_LSPV5_IDENTIFIER_CUT_AUDIT460_HANDOFF.md`; issue outbox `outbox/2026-11-09_0612_LSPV5_460_ISSUE3_OUTBOX.md`.

Tracker update: [P2-L5-460] appended conflict-safely. Final `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; final `proof2.txt` blob `78497e2bba11e629349a83a6ae18b756462a0069`; full 733,798-character readback, exactly one new node, and complete prior-prefix preservation PASS.

Actual advance: independent arbitrary-bitstring evidence, a proof of the cumulative worst-case envelope, and an exact trust-boundary audit strengthen [P2-L1-534] without changing its conditional or distinct-calculus scope. Precise remaining gap: a source-authenticated polynomial normalization covering every historical mixed rule, or a lower bound that survives every legal mixed shortcut, plus a noncircular same-calculus B3 bridge. P versus NP remains OPEN.
