# LSPV-3/449 | Native binary XOR proofwise branch discharge

**2026-11-06 06:24 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL.** Historical accepted-byte `R_mix341` grammar, all-mixed normalization, B3, and P versus NP remain **OPEN**.

## Hypothesis and falsifiers, stated before search

Given a source-authenticated, shared, **GF(2)-XOR-only** refutation from already legally derived affine equations $E$ plus one *marked* assumption equation $a$, delete the assumption syntactically while retaining source provenance and at most the original number of paid XOR inferences. Falsifiers: (1) a projected step requires an unlicensed free zero-row axiom; (2) a branch-local line leaks into the other case; (3) the original CNF cannot legally supply the required affine rows at the stated cost; (4) shared nodes are charged twice or an obligatory branch is omitted.

## Theorem: assumption-coefficient projection

Let $\pi$ be an acyclic shared-DAG, native binary XOR-of-rows derivation of $0=1$ from $E\cup\{a\}$, with $r$ distinct paid XOR inferences in its root ancestry; all equations in $E$ have their own independently authenticated source derivations. Then a source-preserving DAG over $E$ alone derives either $0=1$ or the **complement of $a$**, using at most $r$ additional paid native XOR nodes.

For each original line $L$, track one bit $t(L)$ and the row

$$
P(L)=L\oplus t(L)a.
$$

For $e\in E$, take $t(e)=0$, $P(e)=e$; the assumption has $t(a)=1$, $P(a)=0=0$ represented only as a **virtual zero marker**. At each original XOR inference, XOR the two tags and the two projected rows. If both parents have materialized rows, emit one ordinary paid XOR. If one projection is virtual zero, copy the other existing reference, adding no inference; if both vanish, keep virtual zero. Induction gives $L=P(L)\oplus t(L)a$ and preserves topology. At the contradictory root, $P(0=1)$ is either $0=1$ or $\neg a$, never a virtual zero. QED. This is a familiar linear-algebra deduction principle specialized to paid source-authenticated proof DAGs, **not a new general theorem about P versus NP**.

Two contextual proofs $E,x=0\vdash0=1$ and $E,x=1\vdash0=1$ (both **AND** obligations) yield either an unconditional contradiction or opposing unconditional equations $x=0,x=1$, joined by **one paid native XOR**. Given input branch costs $r_0,r_1$ and union of common pre-derived source rows costing $B$, the exhibited upper-bound witness satisfies

$$
W_{\mathrm{exhibited}}\le B+r_0+r_1+1.
$$

Shared nodes cost once. The ideal global minimum can choose a different, shorter derivation. No native SPLIT, DISCHARGE, weakening or semantic oracle is introduced. The theorem does **not** cover conditional RES/AND3/LOCAL/DEF operations.

## Exact published-family and upper-shortcut ledger

| Family | Encoding and certified lower-bound model | Known shortcut / missing transfer |
|---|---|---|
| **Urquhart odd cubic Tseitin expanders** | $h$ vertices, $3h/2$ edge variables; four wrong-parity signed ternary source clauses per vertex, $4h$ clauses, $\Theta(h\log h)$ indexed encoding bits. Urquhart 1987 establishes exponential **ordinary shared Resolution** size for suitable expander instances (DOI 10.1145/7531.8928). | Historical *declared semantic* /341 AND3 + XOR refutation uses exactly $4h-1$ nodes on bridgeless graphs. Therefore ordinary Resolution hardness **does not transfer** to full mixed rules by analogy. |
| **Haken unary PHP** | Ordinary CNF including wide clauses; exponential ordinary Resolution lower bound (Haken 1985, DOI 10.1016/0304-3975(85)90144-6). | Cook ER / Frege polynomial refutations are controls; any strict-3 conversion needs an explicit lower-bound-preserving simulation. |
| **Two-triangle bridge Tseitin control** | Connected two triangles with bridge $(2,3)$, 7 edge variables, odd charge $(1,0,0,0,0,0)$, **16 original 2- and 3-literal clauses**, max-width-three CNF. This is a *validation control*, not a certified published hard expander. | Ten native semantic AND3 operations extract all six vertex rows; four XOR derive opposite bridge units; one XOR joins. **15 paid nodes**, span **6**, no global minimum claim. |

## Independent test: exact original-source authentication

The source has **205 exact ASCII DIMACS bytes**, SHA-256 `a0df281786bdde3acd0d819c6814ef55597bf54c51a6fe946d184617747ec76e`. Generator emits 16 source lines, 10 paid AND3 and a contextual three-XOR refutation for *each* complementary bridge assignment. Syntactic projection produces two paid XOR per branch and an XOR join: 15 paid nodes in unconditional final goal ancestry. Every source clause participates. Source is UNSAT on all $2^7=128$ assignments. The even-charge all-zero edge assignment is a SAT semantic control.

Independently written Node.js verifier reconstructs exact DIMACS bytes, clause indices, local truth-table AND3 implications, parity annotations, all XOR operations, separate assumption scopes, copy-vs-XOR compiler decisions, final root ancestry, and paid work. **228 assertions passed; 15/15 deliberate corruptions rejected**. Separate 19-variable, up-to-eight-variable-width pure affine source-equation control checked $2^{19}=524,288$ assignments and opposite-unit discharge with one shared source row; that control is **not** a 3-CNF proof.

Resource measurements (Linux host, complete local processes): Python producer **0.95 s / 96,268 KiB RSS**, Node verifier **0.04 s / 27,508 KiB RSS**. Verbose proof trace **10,620 bytes**, compact JSON **4,970 bytes**, original source **205 bytes**. For arbitrary input affine proof data $B$, $r$ paid XOR nodes, $n$ variables, and ID range $L$, explicit row-bitmap proof records occupy $O(B+r(n+\log L))$ bits. This is not a same-machine FLMV space contraction. Discovery, failed searches, all source/index reads, storage/retrieval, conversions, checking, output, simultaneous live state and publication accesses must be charged for a real algorithm; the ideal derivation minimum excludes discovery cost intentionally.

## Source and cross-review authentication

Read governing November 2 handoff, issue #3 through comment 6687084469, AGENTS.md/CODEX.md/pnp skill, original `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11`), earlier LSPV-3/448 (pure RES branch), LSPV-1/431 (semantic affine branch hull), LSPV-1/449 (paid-gate ANF blowup), LSPV-5/REFEREE385, actual Grok REWIRE and Claude TPORT. Both requested external repositories were inspected: `konard/p-vs-np` finite-machine model and proof manifest; `blkph0x/p-vs-np-proof-research` METHOD_INDEX and affine-compression audit. Actual `meelgroup/frat-xor/format.md` and `cake_xlrup/README.md` define **different** typed CNF/XOR proof formats, not an accepted historical R_mix341 byte grammar. Also checked cake_lpr, short-proof and openai/math READMEs. Primary literature: Urquhart 1987; Haken 1985; Raz–Tzameret 2008 `ECCC TR07-078`. Indexed web search performed; branded Google interactive search unavailable. No independent replay with an authenticated historical R_mix341 checker is claimed.

**Remaining transfer:** Source-authenticate the original LOCAL-CONVERT/DEF owner/private/exported port byte grammar and prove mixed-rule, scope-safe normalization or a LEGAL typed counterexample across *all* allowed rules. No superpolynomial full-mixed $\overline W_R$, noncircular B3, or all-machine lower bound has been proved. Root `main.tex` was not modified without complete owned-region readback. All five existing agents, two Route A and three Route B, schedules, weights, and ownership remain unchanged. **P versus NP OPEN.**

**Reproducibility:** Full local producer, independent verifier, 15 hostile mutations, complete original source/typed proof, high-width control, resource logs and SHA manifest in `LSPV3_449_XOR_BRANCH_DISCHARGE_REPRO.zip` conversation archive. A compact GitHub regression and raw summary are published separately.