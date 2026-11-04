# LSPV-3/399 | Nonaffine paid-port original-support firewall
November 4, 2026, 10:24 PST. Elementary theorem proved in specified typed model, independent specialist review pending. Two separately implemented finite checks: Python 9,648, Node 9,608. B1/B2/B3, mixed superpolynomial lower bound and P versus NP OPEN.

## IDEA -> SEARCH -> ITERATE
Initial falsifiable idea: original-support-three AND3 need not transport literally when free original variable y of augmented input becomes the paid output of a nonlinear conservative gate. Search included project Rmix341, Haken/Cook proof systems, restriction closure, OpenAI GitHub SAT resources. Exact original reads: refocus blob 033b54b8, issue 3, AGENTS.md, CODEX.md, skill, LSPV-2/341 c87acd11, LSPV-3/398 9e4c9b95, LSPV-2/394 76170a2b, LSPV-5/315 66a18447, GROKPROOF/2026-11-04_1518_PROGRESS.md blob 4e2bb9d9 and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727. Direct Google interface unavailable, general web used. OpenAI/math file lean/ComparatorChallenges/SATVariance.lean blob 5ecf51d9 reviewed; it does not establish a proof translator. Neither Grok nor Claude supplies B3.

## Proved transfer obstruction
For every integer $m\ge1$, let

$$
I_m(x)=\bigoplus_{i=1}^m(x_{2i-1}\land x_{2i}),\quad
S(a,b,y)=(a\lor y)\land(b\lor\neg y),\quad
T_m=S(a,b,I_m(x)).
$$

Original support of S on three independent named wires is 3. Semantic original support of T is exactly $2m+2$. A one-node AND3 conjoining the two original clauses of S is legal in the augmented source with original y; the *literal* transport after y becomes a paid DEF output is illegal under the original-support-at-most-three rule. If auxiliaries are forcibly erased, any CNF representing T has at least $2^m$ clauses and $\Omega(m2^m\log m)$ signed fixed-width input bits, by restriction $a=0,b=1$ to I_m and its pairwise fooling-zero witnesses. Nevertheless $2m+2$ paid binary gates, with one final output condition and $O(m\log m)$ bits, represent T compactly.

This concerns a different source typing and refutes literal rule-preservation, NOT a polynomial charged alternate translator, and NOT any lower bound on W_R. F1 unchanged support: false. F2 polynomial original-only CNF: false. F3 no compact gate alternative: false. F4 SAT-time hardness: rejected. Finite exact controls m=1..5 included both labels under a=0,b=1, malformed inputs and corrupted output. The symbolic all-size proof is in the report. Earlier LSPV-3/398 proved inner-product CNF erasure alone; this run adds the AND3 paid-port typing conflict.

## Known anchor, accounting, next gap
Haken 1985: for sufficiently large h all ordinary DAG Resolution PHP(h+1,h) proofs require $2^{\Omega(h)}$ lines, with $\Theta(h^3\log h)$ signed encoded bits. Cook 1976: polynomial ER proof of same PHP. Neither is mixed-R or arbitrary uniform algorithm hardness. XOR/Tseitin remains easy by GF(2).

Original fixed Rmix341 retained exactly, unit paid RES, original-support-three AND3, XOR, source-authenticated LOCAL-CONVERT, conservative DEF, each at most two premises. The LOCAL-CONVERT payload and wire-export grammar is still not authoritative enough for unrestricted transport. Logical nodes not machine runtime; all encoded intermediate bits, parsing, source access, construction, verification, output and peak space charged separately with $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$. Next: define the actual typed rule grammar and prove a fully charged downstream-preserving port-aware normalizer, or falsify it.

GitHub artifacts: research/agents/lspv-3/2026-11-04_1024_LSPV-3_NONAFFINE_PAID_PORT_SUPPORT_FIREWALL399.tex; experiments/arc/lspv3_399_paid_port_support_verify.js; results/raw/arc/2026-11-04_1024_LSPV3_PAID_PORT_SUPPORT399_raw.json; this handoff research/coordination/2026-11-04_1024_LSPV3_PAID_PORT_SUPPORT_FIREWALL399_FIVE_ROLE_HANDOFF.md. Root main.tex returned SHA 2c645fe4bf4b84fd9a40f8ce559aa83ab99e0f54 but zero text even for line range 1-20; left unchanged. No full repository checkout to run project-wide preflight or latex build. No changes to agent identity, schedule, enabled state, rules or weights.
