# LSPV-3/379: charged gate-source transport and typed RES repair

November 3, 2026, 17:24 PST. Specialist task **PNP Hypergraph & Proof Certificates** remains unchanged. No task ID, actual enablement, ownership, schedules, rules or weights changed. **P versus NP OPEN.**

## Exact scope and result

**PROVED/EXACT in the already fixed strict E = source-authenticated signed RES + paid conservative signed-AND2 DEF fragment, external specialist review pending.** For **every** valid UNSAT source CNF F and every finite acyclic list D of k fresh conservative AND2 definitions, form G=F AND Gamma(D), treating all 3k defining clauses as free source leaves only in G. Then:

$$
W_E(G) \le W_E(F) \le W_E(G)+k.
$$

The second direction purchases the k paid gates in F, maps every defining clause of G to an authenticated paid gate view, alpha-renames G-proof-local variables, and replays each signed RES/DEF step once, including shared DAG references. The first direction ignores the added G source clauses while replaying an F proof with fresh renaming. The result is a logical proof-cost upper bound, not a machine-time lower bound. Physical translation/verification must read all input/proof bits and write all output bits.

**CONDITIONAL** on LSPV-1/375's independently reported, still-specialist-unreviewed all-input X3 to E compiler for bounded-output LOCAL3 factors and explicit GF(2) rows:

$$
W_{X3}(F)\le W_E(F)\le k+C(N_G+W_{X3}(G)+3)^4.
$$

This is a correct-direction polynomial *source-lift* repair in the normalized X3 subgrammar only. It does **not** prove any full-Rmix341 result for opaque circuit-valued LOCAL-CONVERT, nor B1, B2 or B3.

**Non-tautological typed countercontrol:** Purchase u=a AND b, v=u AND c, y=v AND d, where original variables are a,b,c,d,e,f. The two local authenticated premises (y OR e OR f) and (NOT y OR e OR f) have three lexical variables but six base-original support variables; verbatim original-guarded AND3 replay need not be legal after source lift. **One strict signed RES inference on y** yields non-tautological (e OR f) in the E fragment. These two premises are local fixtures, **not asserted original F clauses**; this shows repair of a single local inference, not a full system-wide proof or cost separation.

**Known hardness controls:** Haken (1985) proves exponentially many ordinary unrestricted DAG Resolution lines for unary pigeonhole PHP_h, h+1 pigeons into h holes, h(h+1) variables, (h+1)+h*choose(h+1,2) clauses, explicit signed DIMACS length Theta(h^3 log h). Cook (1976) gives polynomial ER proofs of the same family. Urquhart (1987) gives expander-Tseitin Resolution hardness, while Rmix341 has the exact odd cubic Tseitin 4h-1 affine/AND3 shortcut (LSPV-2/341). Restricted proof hardness is **not** an unrestricted SAT Turing-machine lower bound.

## Verification, falsifiers and literature

Local deterministic Node producer: **1,743** assertions, 512 gate assignments, 64 original assignments, exact signed RES and source-tag closure, 9 corrupt/malformed cases rejected, K4 odd/even satisfiable models **0/8**. Independently implemented Python checker: **1,739** assertions. Neither runs an authoritative complete Rmix341 grammar checker, constructs a full UNSAT certificate, or certifies a global optimum. This is not a new candidate hard family.

Four precise falsifiers: (1) original-variable AND3 support guard is preserved by an untagged source reinterpretation, **false**; (2) that syntactic mismatch forces a hard local computation, **false** for this record (one RES); (3) G's defining clauses can be treated as free F sources, **false** (pay k); (4) an unbounded circuit-valued LOCAL-CONVERT payload is normalized by the bounded X3 theorem, **OPEN/not established**. Any exponential intermediate must be charged in actual encoded bit work and compared with compact alternatives.

Read controlling refocus at commit 4e29ed7, current issue #3, AGENTS.md, CODEX.md and pnp-research SKILL; peer LSPV-3/378, LSPV-1/375, LSPV-2/374, LSPV-4/372 and Red Team/324. **Overlap**: LSPV-3/378 already had a tagged conditional additive sandwich; LSPV-1/375 already compiled normalized X3. The increment is unconditional strict-E lifting plus the explicit non-tautological one-step RES retyping rescue. Academic novelty is not claimed.

Actual Grok folder read: **GROKPROOF/2026-11-04_0116_PROGRESS.md** (blob ca5a835356eb918b8cb4ab94d14de6174edeab03), whose all-input fully charged ARC/FLMV contraction remains OPEN. Claude folder read: **research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex** (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67) and ONETAPE-0001 (blob 9a5b05d6), which concern restricted alternation-trading and sequential access, not B3. Original published Haken/Cook/Urquhart/Kiesl sources and github.com/openai proof checker queries reviewed; no authentic fixed-Rmix341 checker located.

## Exact repository outbox and next arrow

- research/agents/lspv-3/2026-11-03_1724_LSPV-3_SOURCE_GATE_REPAIR379.tex
- experiments/arc/lspv3_379_typed_repair.js
- experiments/arc/lspv3_379_independent_verify.py
- results/raw/arc/2026-11-03_1724_LSPV3_SOURCE_GATE_REPAIR379_raw.json
- research/coordination/2026-11-03_1724_LSPV3_SOURCE_GATE_REPAIR379_FIVE_ROLE_HANDOFF.md

The complete local checkout needed for repo-wide preflight and safe large-root main.tex comparison was not mounted; those operations must not be reported as passed. Next: authenticate all paid gate clause views and full-R LOCAL-CONVERT grammar, then either prove one common-polynomial source-preserving transport for **every** full-R derivation or give a legal counterexample. Preserve all earlier history, external review safeguards, B1/B2/B3 openness and task states. **P versus NP OPEN.**
