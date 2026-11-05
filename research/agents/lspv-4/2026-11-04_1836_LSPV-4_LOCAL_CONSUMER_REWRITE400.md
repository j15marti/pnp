# LSPV-4/400: LOCAL-CONVERT conclusion normalization requires downstream proof repair
**2026-11-04 18:36 PST | IDEA -> SEARCH -> ITERATE | Fixed native R_mix341 unchanged**

**Status:** PROVED/EXACT for an explicitly legal AND3, LOCAL-CONVERT, RES fragment of original R_mix341 (not a full derivation translator); COMPUTATIONAL finite controls. Full native exported-wire grammar, B1/B2/B3, superpolynomial mixed lower bound, P versus NP OPEN.

## IDEA / falsifiable prediction
Hypothesis: replacing an explicitly implied LOCAL-CONVERT output by a stronger logically entailed root without rebuilding consumers need not preserve a syntactically legal proof DAG, even if source authentication, original-variable support and every individual rule are otherwise sound. Prediction: a valid downstream RES pivot can disappear, or a resolvent change, under a locally sound normalization. Falsifiers: (1) replacement preserves all pivots; (2) original fragment is not legal under the actual /341 rules; (3) replacement creates genuine unsoundness rather than only an invalid proof syntax; (4) some legal output weakenings are wrongly rejected.

## SEARCH / authenticated corpus / primary literature
First read governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` and issue #3 (through 18:24 PST LSPV-3/407), authoritative `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob c87acd11), REFEREE349/350, LSPV-2/405, LSPV-3/406/407, LSPV-4/389/399, AGENTS.md, CODEX.md, pnp-research skill. Actual Grok: `GROKPROOF/2026-11-04_2315_PROGRESS.md` blob f5b8ef62; actual Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, `...1521_CLAUDE_ONETAPE-0001.tex`. Neither supplies B3. OpenAI authenticated search `ExecCNF` found `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean`, blob e60f4d9; full content reviewed: executable clause normalization, not a compiler for paid native mixed proofs. General web queries: `Cook Reckhow 1979 proof systems polynomially bounded iff NP coNP extended Frege proof system`, `Krajicek 2022 information in propositional proofs and algorithmic proof search`, `Haken 1985 exponential resolution pigeonhole Cook extended resolution polynomial`, `Soltys Cook extended Frege gaussian elimination`; read Stanford Encyclopedia computational complexity, Krajicek (JSL 2022), Soltys-Cook LICS 2002 abstract and Soltys's Extended Frege/Gaussian Elimination text. Direct Google-branded search unavailable; do not claim it searched. Prior REF349 already gives internal-wire safety and REF350 conditionally p-equates a *different root-only completed grammar* to ER. This report is narrower: even on unambiguous native operations, local conclusion substitutions alone do not give a complete proof translation.

## ITERATE / exact legal witness
Let the **satisfiable original source**, with 3 original variables, be the signed CNF
\[
F=(x)\wedge(x\vee z)\wedge(\neg y).
\]
It has exactly two satisfying assignments, x=1,y=0,z arbitrary. The following full native-rule *fragment* has 3 paid nodes:
1. AND3 with original source clauses (x) and (x OR z) obtains exact 2-original-support factor x, truth table [0,0,1,1] on ordered (x,z).
2. LOCAL-CONVERT obtains clause (x OR y). All assignments satisfying factor x satisfy this clause, verified on all 8 original-variable assignments.
3. RES on y between (x OR y) and original (NOT y) derives (x), pivot y.

All three rules belong to original /341; no exported internal wires, uncharged gates, newly invented rules or SAT oracle are used.

**PROVED/EXACT failure of an overstrong converter claim:** Replace the LOCAL conclusion by the stronger, still source-entailed clause (x) without changing its node ID and consumer. The original pivot y is absent: the RES consumer is now illegal. Alternatively replace the LOCAL conclusion by valid weakening (x OR y OR z); the correct RES output is (x OR z), so retaining the old (x) output also violates the exact Resolution rule. These are counterexamples to *edge-preserving independent per-node normalization*, not to the existence of a more sophisticated polynomial global normalization and not to soundness of R_mix341.

An explicit downstream-rewriting repair exists on this 3-node example: change the RES resolvent when weakening, or omit/redirect the RES step when strengthening. This repair depends on consumer-edge inspection and is not an all-rule, all-size normalization theorem.

## RESOURCE AUDIT
N is exact original CNF encoded length, q is distinct paid inference-node count, E is **supplied proof and circuit payload bits**, and M=N+E. The finite example has q=3. Any faithful parser must charge source input acquisition, clause signs and indices, factor truth tables, LOCAL implication checks, resolution pivots and resulting clauses, reference rewrites, all reads and output. A buffered graph-based normalization has at least O(M) stored bytes in its straightforward implementation, plus object overhead. A read-only-input, append-only-output strategy can re-scan the full proof to enumerate all consumers of a changed node with O(log M) address memory and O(M^2) time for one global pass, but **this does not construct legal rewritten inference steps** without an additional all-rule rewrite theorem. Repeated cascading revisions may require more work; no uniform polynomial total or FLMV sublinear-space bound is asserted. q alone is not runtime; an E-bit untrusted circuit payload cannot be assumed free. Actual machine head/index operations, compilation, verification and temporary allocations count in all-phase peak rho. The example's 3-node logical lower bound is not a minimum W_R theorem.

## COMPUTATIONAL controls
A standalone no-dependency JS checker independently evaluates each AND3 table, checks each LOCAL implication, validates literal-exact Resolution pivots/resolvents, confirms 2 SAT models for original F, accepts the corrected weakening path and rejects the unchanged-edge strengthening and invalid negative LOCAL. Odd/even K4 Tseitin controls have 0/8 models. Finite controls do not certify a generalized native compiler.

## Haken / Cook / B3 firewall
Haken 1985: for each large h, **every** ordinary shared DAG Resolution refutation of explicitly encoded unary PHP_(h+1)^h has 2^{Omega(h)} lines; with signed literal indices source size N_h=Theta(h^3 log h). The quantifiers are all large h/every ordinary Resolution refutation; no auxiliary DEF, XOR, LOCAL, ER or arbitrary decider. Cook 1976 provides polynomial Extended Resolution PHP proofs; Tseitin admits short GF(2) proofs. REF350's root-parser p-equivalence is explicitly conditional on a parser completion. No restricted proof lower bound transfers without proof.

B3 for the **same fixed native R** remains SAT in P => Wbar_R polynomial. This witness proves neither B3 nor its negation; it eliminates only a tempting edge-preserving normalizer. Correctness of a hypothetical SAT decider and short same-R reflection proofs remain separate missing obligations. Cook-Reckhow yields *some* p-bounded proof system under NP=coNP, not the preselected R.

## CORPUS / duplication / root
This is a new explicit native-fragment counterexample to edge-preserving normalization, unlike previous private-wire export/semantic-alias failures. Prior root-only proof and local private-wire reports are adopted with their conditional labels. The latest peer LSPV-3/407 studies coNP-hard equivalence of paid exported wires; it is not duplicated. Root `main.tex` remains OPEN; do not modify without complete current byte retrieval and ownership-marker-safe SHA update. Next: formally specify native PUBLIC vs PRIVATE port grammar, then construct a consumer-aware source-preserving compiler with a polynomial full-payload E time/space ledger, or a truly legal obstruction. No task/schedule/weight changes.
