# LSPV-4/394: exact Haken-source acquisition calibration and missing mixed transfer

**November 4, 2026, 12:36 PST. PROVED/EXACT elementary restricted-source lemma; COMPUTATIONAL finite controls. B1/B2/B3 for unchanged R_mix341 and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

The hypothesis was that every literal sign of the *original, unguarded* standard unary pigeonhole CNF PHP(h+1,h) is label-pivotal while the same source is uniformly recognizable, defeating an inference from Resolution hardness to unrestricted computation. Four predeclared falsifiers: pigeon-clause flip stays UNSAT; collision-clause flip stays UNSAT; randomized deciders read fewer pivotal signs; false promotion from source acquisition and Haken to full mixed hardness.

SEARCH: read approved 2026-11-02 12:04 five-role handoff; issue #3; AGENTS/CODEX/project research skill; REFEREE336/343; LSPV-1/396, LSPV-3/390 and /400, LSPV-4/393; Grok `GROKPROOF/2026-11-04_1518_PROGRESS.md` (blob 4e2bb9d9), Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` and `2026-10-28_1452_CLAUDE_TPORT-0002.tex`. Project GitHub search and OpenAI GitHub search included `sat certificate`, and read `openai/math/lean/OAI/Algorithms/SubexponentialSAT/RuntimeAssembly.lean`, SHA 41df76f4 (its machine implementation obligations are openly pending). General web literature queries covered Haken 1985, Cook 1976, randomized query sensitivity. Branded Google UI unavailable, no claim of using it. Generic randomized sign sensitivity is ALREADY established in LSPV-3/390 and REFEREE329.

ITERATE: On standard explicit signed-index unary PHP, variables h(h+1), clauses (h+1)+h*C(h+1,2), literal signs **L=h(h+1)^2**, source bit length Theta(h^3 log h). Every one-sign flip makes SAT. For a pigeon clause, leave that pigeon unassigned and biject the other h pigeons to the holes. For a collision clause, put the two pigeons together at that hole and biject the others to the remaining holes. Any fixed uniform bounded-error SAT decider with per-input error epsilon<1/2 reads in expectation at least (1-2epsilon)L distinct sign positions on the original UNSAT source, using coupled random tapes. This is only a **linear** acquisition lower bound. All source/preprocessing/lazy/guest reads charged.

Haken's original theorem: forall h>=h0, forall ordinary shared-DAG Resolution refutations pi of explicit unary PHP, |pi|>=2^(c h). The theorem does NOT bind Extended Resolution, mixed R_mix341, GF(2), or arbitrary SAT algorithms. Cook Extended Resolution gives polynomial PHP proofs. A fixed total correct uniform recognizer that checks exact PHP and falls back to full exhaustive SAT is polynomial on this family but has exponential global worst-case. It is a previously known B1 Resolution counterexample, NOT B2/B3 mixed disproof.

## Checks and artifacts

The Python standard-library original producer and independent Node verifier ran **3,585** and **3,571** assertions respectively. All **1,740** original sign flips for h=1,...,8 had explicit witnesses. For h<=3 brute-force SAT/UNSAT was checked; nine malformed controls rejected; odd/even K4 parity model counts **0/8**. Full reproducibility ZIP is available in the originating conversation; GitHub:
- `research/agents/lspv-4/2026-11-04_1236_LSPV-4_HAKEN_SOURCE_SIGN_BRIDGE_CALIBRATION394.tex`
- `experiments/arc/lspv4_394_php_sign_controls.py`
- `results/raw/arc/2026-11-04_1236_LSPV4_394_PHP_SIGN_CALIBRATION.json`

All-phase physical accounting: parsing, source/access, discovery, intermediate representation, construction, verification, output, index tapes, ancestors/cache/guests and peak writable space. The old rho bug remains forbidden: s'<=max{rho,eta,lambda,lambda*s} with rho including preprocessing/materialization.

**Next:** authoritative full R_mix341 grammar for LOCAL-CONVERT/DEF, polynomial certificate bit balance, and a noncircular all-input B3 bridge. No schedule, title, agent count, rule, weight or verified mathematics changed. The repository preflight executable was unavailable (repository not locally checked out); authenticated connector retrieval/search used as partial fallback. 

**Predecessor readback note:** `research/agents/lspv-3/2026-11-04_1124_LSPV-3_QUADRATIC_SHADOW_PORT_CERTIFICATE400.tex` is nonblank and substantive, but the inspected text lacks the AGENTS.md final `END_OF_VERIFIED_REPORT::LSPV-3` sentinel. Ask LSPV-3 to verify/repair only its own report markers, without altering science.
