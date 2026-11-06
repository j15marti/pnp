# LSPV-1/436 five-role handoff, November 5 2026 22:26 PST

**Governance unchanged:** exactly TWO Route A LSPV-2/LSPV-4, THREE Route B LSPV-1/LSPV-3/LSPV-5. Fixed historical R_mix341 native weights, schedules, roles and previous requirements preserved. P versus NP OPEN.

## What is new, what is reused

LSPV-1/435 at 22:08 PST ALREADY proved signed-literal substitution for shared strict Resolution, private clause splitting, and a 3m-clause proper width-three padding. That result is reused, not counted again as a new theorem. LSPV-1/436 introduces a smaller fully strict proper-3-CNF UNSAT guard $K(F)$ with **$2m+4$ clauses** and $n+m+3$ variables:

$$
K(F)=\bigwedge_i [(g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)]
\wedge \bigwedge_{\epsilon,\delta\in\{0,1\}}(\neg g\vee u^\epsilon\vee v^\delta).
$$

Original-source substitution $g=u=v=0,\ y_i=\neg a_i$ makes all first/guard sources tautological and every second clause exactly $C_i$. Thus **PROVED/RESTRICTED ordinary shared-DAG Resolution** minimum $L(F)\le L(K(F))\le L(F)+2m+3$, and ideal minimum depth $D(F)\le D(K(F))\le D(F)+3$. Lower-bound preservation has a genuine proofwise simulation direction; it is not merely equisatisfiability.

If the original F is clause-minimally UNSAT, K(F) is too, with an explicit satisfying assignment after deletion of each of its **$2m+4$ source clauses**. For ANY sound source-bound calculus with charged node weights at least 1 and at most binary premise fan-in, this forces **$W_R(K(F))\ge2m+3$**, even allowing optimal sharing, auxiliary conservative definitions and legal shortcuts.

## Established published hard family and mixed upper control

Odd cubic-expander Tseitin F_h: proper signed width-three source, 4h clauses, 3h/2 variables, $\Theta(h\log h)$ indexed bits, published $2^{\Omega(h)}$ ordinary DAG Resolution lower bound (Urquhart 1987; Ben-Sasson/Wigderson 2001). New K(F_h) has **8h+4** proper 3-clauses and **11h/2+3** variables, and is also exponentially Resolution-hard by proofwise substitution. Earlier /435 strict padded encoding had **12h** clauses.

Known LSPV-2/341 specified-semantic mixed GF(2)/AND3 refutations of F_h cost 4h-1 nodes. Recover original clauses from K in 8h+3 strict Resolution steps, then replay the algebraic shortcut. Thus, CONDITIONAL on historical native checker acceptance of the declared semantic interfaces:

$$
8h+3\le W_{R_{\mathrm{mix341}}}(K(F_h))\le12h+2.
$$

This gives a **linear full-rule lower floor**, not a superpolynomial mixed or all-machine lower bound. Private/exported wires, LOCAL-CONVERT and defining facets still demand historical grammar authentication.

## Executed evidence

Finite K4/K33/Cube: F 16/24/32 clauses, K 36/52/68 clauses, K strict-Resolution proof witnesses 51/103/219 paid nodes, projected F proof witnesses 31/75/183, 36/52/68 distinct deletion-model witnesses. Python 3,728 checks and independent Node K4 2,551 checks, five corruptions rejected. K4 strict CNF SHA256 bc669b8665a3ab0dcb132fbae71fdf5396b9dd3522cb616f0f669f1982ec2755. Full local ZIP preserves Python producer, independent Node, original and derived CNF, original-source certificates, raw results, hashes. These are witness checks, not exact finite global minima or authoritative historical /341 checker runs. Host runtime/RSS not a TM proof.

## Role-specific next checks

**LSPV-1 Route B:** authenticate exact native DEF and LOCAL port/facet permissions; look for all-mixed superpolynomial invariants and noncircular SAME R B3 SAT in P => Wbar_R polynomial.

**LSPV-3 Route B:** independently replay exact strict source substitution, K source-deletion certificates, shared-DAG inference and correct pivot orientation. Check whether 8h+3 RES preprocessing followed by historical /341 Tseitin GF(2)/AND3 proof has a native accepted certificate.

**LSPV-5 Route B:** attack the source-indispensability binary-fan-in lemma under conservative DEF, multi-premise edge semantics and source ancestry. Do not infer a native split/discharge rule or overpromote restricted Resolution hardness.

**LSPV-2 and LSPV-4 Route A:** use this hard-vs-shortcut pair only as a stress test. Universal, all-input, recursively iterable, both-label malformed-aware same-machine FLMV contraction is still unproved. Charge ALL construction/lookup/restarts/retention/output and peak-space phases.

Review included governing Nov 2 handoff, current issue #3 including prior /435, AGENTS/CODEX/skill, historical /341, peers /438-/439 and REFEREE377, actual Grok and Claude files, two mandatory outside repositories and FRAT-XOR/CakeLPR/OpenAI; exact references and scope are in the full report. Root main.tex still returns SHA but zero readable bytes and was not changed.

**P versus NP OPEN; B1/B2/B3 OPEN.**
