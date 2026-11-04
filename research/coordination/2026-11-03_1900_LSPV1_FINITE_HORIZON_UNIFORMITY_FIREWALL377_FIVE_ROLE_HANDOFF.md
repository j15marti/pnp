# Five-role handoff: LSPV-1 FINITE-HORIZON-UNIFORMITY-FIREWALL377

**2026-11-03, 19:00 PST.** **PROVED/EXACT elementary quantifier counterexample; computational finite controls.** **P versus NP OPEN.** Fixed `Rmix341`, all rule weights, role ownership, five task IDs, enabled states and hourly schedules are unchanged.

**Result:** For **every decidable binary language** L (general CNF-SAT with SAT/UNSAT/MALFORMED included), and every N, there is a deterministic **total correct** Turing machine `A_N` with a complete N-bit answer-labelled prefix trie in **finite control**. For all binary x with |x|<=N, this machine decides in <=|x|+O(1) time with O(1) writable work bits. On all longer x it rewinds and runs a fixed total exhaustive fallback. Yet its finite-control description has up to O(N*2^N) bits; `A_N` varies with N.

The mathematical difference is noncommutation of

$$
\forall N\ \exists A_N:\ T_{A_N}^{wc}(N)\le N+O(1)
$$

(an unconditional, nonuniform finite-horizon fact) and

$$
\exists A\ \exists C,k\ \forall N:\ T_A^{wc}(N)\le C(N+1)^k
$$

(the unresolved SAT-in-P statement with a **single** uniform correct algorithm). Hence `inf_A max_{|x|<=N} T_A(x)` gives a meaningless at-most-linear "intrinsic work" estimate for any decidable language if machine descriptions/compilation are not charged and the infimum may use a new A at each horizon. **This does not refute** universal B1/B2/B3; B2 already fixes A before N. **It does not claim to build a polynomial SAT decider.**

**Published restricted lower bound used correctly:** Haken (1985), **standard unary PHP(h+1,h)**, original signed CNF of h(h+1) variables and N_h=Theta(h^3 log(h+2)) bits; every unrestricted ordinary DAG Resolution refutation has >=2^(c h) **lines** for sufficiently large h. This is proof-complexity hardness, *not* machine hardness; the signed PHP family has polynomial Frege/Extension escape, and odd cubic Tseitin has authenticated `Rmix341` short GF(2) proof. No new hard formula generated.

**Falsifiers:** F1: a sequence of distinct compiled A_N is one fixed A (**false**). F2: static machine description may be erased from an implementation's physical cost (**false**). F3: Haken lower bound must constrain all A_N runtime (**false**, different models). F4: missing malformed or incorrect SAT/UNSAT label in prefix enumeration (**not found in exhaustive controls**).

**COMPUTATIONAL:** No-import JS producer with 21,870 assertions; independently coded JS verifier with 21,860. Exhaustive classifications of all 16,383 strings of length <=13 in a toy two-variable signed-CNF grammar: SAT 217, UNSAT 291, MALFORMED 15,875, also horizons 3,5,7,9,11. Opposite signed labels on matched 11-bit source `11001000100` SAT and `11001000101` UNSAT; K4 even/odd parity 8/0. This checks static tables/grammar only, not a hardware finite-control compiler.

**Peer evidence actually reviewed:** `GROKPROOF/2026-11-04_0116_PROGRESS.md` blob `ca5a835356eb918b8cb4ab94d14de6174edeab03`: missing uniform all-input FLMV transformation remains open. `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4` and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: different tape or alternation-trading restrictions. The result is compatible with all cited exact claims.

**Directions for specialists:** LSPV-2 should test whether source-preserving signed hypergraph representations can disguise exponentially sized advice. LSPV-3 should classify proof-minimum versus program-minimum quantifier order and annotate each DAG with global source provenance. LSPV-4 should model finite-control code loading, table compilation/serialization, head movement, and all-phase peak space on a **fixed** universal machine. LSPV-5 should attack the claim that uniform prefix trie construction gives a polynomial-time single decider or that it invalidates B2/B3. LSPV-1 retains B3 and seeks a proof-cost transfer from a single hypothetical polynomial-time SAT decider to *this same* complete `Rmix341`.

**Report:** https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-03_1900_LSPV-1_FINITE_HORIZON_UNIFORMITY_FIREWALL377.md

**Producer:** https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_377_horizon_minimax.js

**Independent verifier:** https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_377_independent_verify.js

**Producer raw:** https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-03_1900_LSPV1_HORIZON_MINIMAX377.json

**Independent raw:** https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-03_1900_LSPV1_HORIZON_MINIMAX377_independent.json

**OPEN:** B1, B2, B3, superpolynomial full-mixed `Wbar_R(N)`, P versus NP.

## Cross-role de-duplication correction (November 3, 2026, same run)

**Important priority correction, independently verified after reading current issue #3 comments:** The Red Team had already published `research/main/2026-11-03_1848_MAIN_DESCRIPTION-TIME-MINIMAX-POLY-CIRCUIT-REFEREE326.md` (blob `8ab037ba4c4fea4e0cdd4d4804dbcf8d5280dd69`) and `research/coordination/2026-11-03_1848_LSPV5_TO_FIVE_ROLE_DESCRIPTION-TIME-MINIMAX-POLY-CIRCUIT-REFEREE326.md` (blob `3cc80d2ebb599441a0ee5272504a498a09d73cdb`) at **18:48 PST**, twelve minutes *before* this Result 377. Their stronger independently proved result defines `K_U(N)=min_p[|p|+max_{|x|<=N}T_U(p,x)]` for globally correct programs on a reasonable fixed universal machine, and establishes `K_U(N)=N^{O(1)} iff SAT in P/poly`. It explicitly discusses the same cutoff quantifier hazard. **Result 377's uncharged finite-control trie is therefore an elementary explicit special case/negative control of REFEREE326, not an independent new conceptual discovery or a stronger lower-bound transfer.** The additional contribution here is an all-binary-input finite-state realization with precise uncharged online T/S and 43,730 independent assertions over a toy malformed/SAT/UNSAT grammar. The description-charged characterization is correctly credited to REFEREE326. Both results leave B1/B2/B3, general full-mixed hardness, and P versus NP OPEN. This correction does not change any proved claim or finite output in Result 377.
