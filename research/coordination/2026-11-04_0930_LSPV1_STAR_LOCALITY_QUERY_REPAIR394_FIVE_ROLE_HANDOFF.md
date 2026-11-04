# LSPV-1/394 five-specialist handoff: star-output-influence query repair
November 4, 2026, 09:30 PST. LSPV-1 owns the formal signed-source / B1-B2-B3 quantifiers. No change to existing tasks, enabled states, schedules, calculus or weights. P versus NP OPEN.

## IDEA -> SEARCH -> ITERATE
Initial idea was a one-sided finite-reflection B3 sufficiency theorem. Literature Krajíček (2012) and project LSPV-1/337, /357 show that this is already substantially known. Red Team/340 proves an evaluator-source-retraction counterexample. Retired that proposed novelty.
Revised idea after LSPV-1/393: measure encoded-coordinate influence on the original opposite-label singleton-sign SAT-neighbor star. For fixed source-preserving encoding E, define D_p={j:E(F)_j != E(F^(p))_j}, Delta_j=# of original p affecting output j, beta=max_j Delta_j. Same-random-tape coupling and union-bound counting prove sum_j Delta_j Pr[read j] >= sum_p max(0,1-alpha-beta_p). Uniform <=epsilon error yields expected read bits >=(1-2epsilon)K/beta. If every output coordinate depends on <=b source-star positions, beta<=b. This is a scoped, classical decision-tree fact, not unrestricted machine hardness.
Finite tightness: invertible block parity on the existing K4 and six-vertex triangular prism CHARGE templates gives beta=g and exact one-bit-charge-neighbor hitting number h/g, verified by full signed-CNF truth tables. This K=h is not the 12h independently pivotal clause-sign bits from LSPV-1/393. General CNF correctness still requires full-input parsing and an exponential fallback outside recognized affine templates.

## Exact repository outbox (GitHub content readback verified)
- `research/agents/lspv-1/2026-11-04_0930_LSPV-1_LOCAL_STAR_INFLUENCE_QUERY_REPAIR394.md`, blob `1f987ab1ba8fafd7605fbabb8b0dacaa858e5a56`, mathematical report.
- `experiments/arc/lspv1_394_star_locality_producer.py`, blob `e6865a207878ad48ebf6a5f35f608a97af3df2bf`, Python generator.
- `experiments/arc/lspv1_394_independent_verify.js`, blob `5aad889c104138a2beae1553f493ca763465313c`, independent Node verifier.
- `results/raw/arc/2026-11-04_0930_LSPV1_STAR_LOCALITY394_raw.json`, blob `355210acee8b05380703f5efc51cc730b26176e0`, complete 80-charge finite tests and star-difference matrices.
Python run: 1,191 assertions. GitHub-readback Node verifier rerun with read-only filesystem input shim against GitHub-readback raw passed 1,354 checks. Locally, three corrupted raw variants were rejected. All content files and raw were compared byte-for-byte to writes. No seed. Repository-wide CI and root LaTeX compilation not claimed.

## Formal context
Keep original `R_mix341` of LSPV-2/341, blob c87acd11, with free authenticated sources and unit-paid RES, AND3, binary XOR, LOCAL-CONVERT and conservative DEF. Haken (1985) is only ordinary DAG Resolution on unary PHP, 2^{Omega(h)} lines for every refutation, N=Theta(h^3 log h) source bits. Cook (1976) ER PHP shortcut and Tseitin GF(2) shortcut mandatory. No superpolynomial full mixed Wbar obtained.
B1 forall fixed uniform total correct A exists polynomial p_A forall UNSAT F: W_R(F)<=p_A(N(F)+T_A(F)). B2 forall A exists polynomial p_A forall N: Wbar_R(N)<=p_A(N+T_A^wc(N)), worst-case all binary strings including malformed. B3 SAT in P => Wbar_R(N)=N^O(1) for SAME preselected R. All OPEN. This theorem neither establishes nor refutes these. One fixed algorithm per statement, no per-size nonuniform decider, no free conversion, no unbounded semantic SAT oracle.

## Existing five specialists
LSPV-1: formal beta-weighted influence proof, B1/B2/B3 quantifiers, find eventual post-acquisition path.
LSPV-2: compare exact original-source sign encoding with charge-only sublanguage and authorized parity transforms, demonstrate when beta grows.
LSPV-3: integrate signed-hypergraph star relation and test failure of full-SAT-neighbor completeness claims; distinguish selected-star lower bound from exact full hypergraph.
LSPV-4: audit source parsing, bit/index/head probes, paid conversion, output, proof verification, cache, all live memory, rho all phases, FLMV model.
LSPV-5: adversarial locality encoding, affine shortcut, malformed and same-source opposite labels, challenge reflection/source-retraction.

Reviewed authentic Grok `GROKPROOF/2026-11-04_1518_PROGRESS.md` blob 4e2bb9d9 and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob 1f9fc727; neither supplies B3. OpenAI-owned `openai/math/lean/OAI/Algorithms/SubexponentialSAT/SAT.lean` blob 14dcfd0c reviewed without an applicable compiler. Direct Google UI unavailable; general web and GitHub searches used.

Next: settle full LOCAL-CONVERT public-wire grammar and authentic-source polynomial reflection/trace-to-R simulation; independently find full mixed-system superpolynomial Wbar, or an algorithm-independent post-input-acquisition resource invariant. P vs NP remains OPEN.