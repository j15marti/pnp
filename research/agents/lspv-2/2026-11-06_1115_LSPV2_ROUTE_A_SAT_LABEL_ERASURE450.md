# LSPV-2/450: Proper-block SAT labels erase Tseitin contradiction (Route A)

**2026-11-06 11:15 PST, America/Los_Angeles.** **PROVED/RESTRICTED**, elementary corollary of project LSPV-2/422 (NOT a new boundary-projection theorem); **COMPUTATIONAL** independent original-source tests. Universal FLMV contraction, Route B B3 and P versus NP remain **OPEN**.

## IDEA -> SEARCH -> ITERATE and falsifiers

Hypothesis: Any vertex-bundle partition of an authenticated connected cubic Tseitin 3-CNF into at least two nonempty proper children makes every local child SAT, even when the parent is UNSAT. Child SAT labels alone cannot implement the required original SAT/UNSAT join. Three falsifiers: (F1) a proper original-clause bundle might itself be UNSAT; (F2) some even/odd charges give different child SAT vectors; (F3) the bundles might not preserve the signed proper 3-CNF source. All were falsified in the declared model. (F4) A source-aware algebraic join can recover the parent despite erased local SAT labels. **Affirmed:** this is an essential shortcut and forbids universal-machine hardness claims.

Search disclosed that LSPV-2/422 already proves the stronger exact affine boundary-projection equation. LSPV-2/295 also uses syndrome trellises; LSPV-4/438 proves a distinct expander giant-core obstruction under edge restriction; LSPV-3/453 gives a known treewidth upper bound and explicitly corrects duplicate /361 work. This run's contribution is the explicit **label-only-join no-go corollary**, a constructive witness algorithm, and independent exact tests. Do not claim novelty for the algebra.

## Exact published-family ledger

For an established cubic expander-based Tseitin family choose a connected simple cubic graph $G=(V,E)$, $H=|V|$, $M=3H/2$ edge variables and charges $\chi_v\in\mathbb F_2$. For each vertex with ordered incident edges $a<b<c$, use the **original** four proper three-literal signed clauses

$$
C_{v,p,q}=\ell_p(x_a)\lor\ell_q(x_b)\lor\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),\quad p,q\in\{0,1\},\qquad \ell_0(x)=x,\quad\ell_1(x)=\neg x.
$$

This enforces $x_a\oplus x_b\oplus x_c=\chi_v$. There are $4H$ original clauses, $12H$ original occurrences, $M$ variables and ordinary binary-ID size $N=\Theta(H\log H)$. On connected $G$, the original formula is SAT exactly when $\bigoplus_v\chi_v=0$. No translation to 3-CNF is needed. Odd charge is a certified algebraic UNSAT witness.

**Published hardness:** Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), DOI 10.1145/7531.8928, establishes exponential **ordinary unrestricted shared-DAG Resolution** size for suitable expander-based Tseitin contradictions. Ben-Sasson/Wigderson, JACM 48 (2001), DOI 10.1145/375827.375835, supplies width/size tools. Itsykson/Riazanov/Smirnov, *Tight Bounds for Tseitin Formulas*, SAT 2022, DOI 10.4230/LIPIcs.SAT.2022.6, addresses **regular Resolution and OBDD**, separately. None is a lower bound for arbitrary SAT algorithms, Extended Resolution, historical $R_{\mathrm{mix341}}$, or algebraic joins. Previous project LSPV-2/341 and LSPV-1/452 exhibit paid mixed GF(2)/AND3 shortcuts within their declared native-rule scope. Finite K4, cube and Petersen inputs are authenticity/semantic controls, not growing certified-hard proof-size instances.

## Theorem 450.1: every proper block SAT, regardless of parent label

**Model:** Fix any connected cubic $G$ and *any* public partition $V=V_1\sqcup\cdots\sqcup V_q$, $q\ge2$, into nonempty proper blocks. Define $F_i$ by retaining exactly the original four source clauses per vertex $v\in V_i$. Every crossing-edge variable occurs freely in the relevant child, and distinct children may refer to the *same* original variable, not separate copies.

For every charge vector,

$$
\boxed{\forall i\quad\operatorname{SAT}(F_i)=1,\qquad
\operatorname{SAT}\left(\bigwedge_iF_i\right)=1\iff\bigoplus_{v\in V}\chi_v=0.}
$$

**Proof:** Every connected component $C$ of the induced graph $G[V_i]$ has at least one edge leaving $V_i$: otherwise $G$ would be disconnected. In the local vertex-by-edge incidence matrix over $\mathbb F_2$, the columns from edges internal to $C$ span the even-parity row vectors (rank $|C|-1$); one incident boundary edge contributes a unit column, raising rank to $|C|$. Thus each local system is solvable for *every* local charge assignment. The original four-clauses encode those equations exactly. The global incidence system for connected $G$ has rank $H-1$, with one dependence obtained by summing all vertex rows, giving the second claim. Choose two charge patterns of opposite global parity. Their ordered local SAT label vectors are both $(1,\ldots,1)$, but their parent labels differ. Therefore **no join function supplied only the local SAT labels and a public charge-independent partition is correct on both inputs**. QED.

**Constructive local witness:** In each induced connected component, select an exiting boundary edge at an anchor, set other boundary and non-tree internal variables to zero, then solve the internal spanning-tree edges leaf-to-root. Finally set the chosen boundary edge to satisfy the anchor. This constructs a model of every local proper block. Its boundary values need not agree with the other block's models.

**Critical scope:** This does not rule out a join that reads the parent source, extracts original charges, chooses charge-dependent partitions and uses that transcript, or processes full contextual boundary relations. Nor does it prohibit a source-dependent solver from deciding the parent directly.

## Exact existing repair, from LSPV-2/422

The **source-authenticated existential boundary relation**, not the local SAT label, is

$$
\exists x_{E(S)}F_S\equiv
\bigwedge_{C\in\operatorname{Comp}(G[S])}
\left(\bigoplus_{e\in\delta(C)}x_e=\bigoplus_{v\in C}\chi_v\right).
$$

For a connected induced block, this has one boundary parity condition. All independent blocks are SAT, while their exact boundary constraints may disagree. On K4, splitting vertices into $\{0,1\}$ and $\{2,3\}$ yields two SAT children. With original odd charges $(1,0,0,0)$, their boundary parities disagree and the parent is UNSAT; with even charges $(0,0,0,0)$ they agree and the parent is SAT. All source clauses are proper width three.

## Quantified small-child test and resource firewall

For $b=\lceil\sqrt H\rceil$, consecutive vertex blocks give $q=\lceil H/b\rceil=O(\sqrt H)\le N^{3/5+o(1)}$ children. Each has at most $4b$ signed clauses and $O(b\log H)=N^{1/2+o(1)}$ literal bits. Literal bodies of all children sum to $\Theta(N)$; shared edge variables retain their original IDs. These bounds are about child *representation*, not a successful all-input decision transformation. Boolean guest replies give exactly $q$ ones and no information about global parity.

**Resource ledger:** source parse/authentication not executed in the compact test (must be charged); initial source reads $\Theta(N)$ in a complete scan; clause splitting $4H$ distinct original clause records; children materialized once total $\Theta(N)$ literal bits plus headers (or virtual indexed ports with charged per-read costs); local formula satisfiability requires no guest calls for the recognized family but constructive witnesses need graph processing; a correct join must acquire/verify parity profiles or directly XOR charges. Exact all-phase peak on *general unannotated CNF* is not established. Failed discovery, malformed handling, external source/index/caches, retained versus recomputed parent state, output, arbitrary guest execution, iterative reapplication and same-machine Turing-tape accounting are OPEN. There are no native $R_{\mathrm{mix341}}$ deductions in this experiment. For any proof DAG, context-sensitive AND obligations must be discharged, and shared nodes paid only once at historical weights; no split/discharge rule is silently introduced.

## Tests and negative controls

Locally executed Python producer (full source in fallback archive) reconstructed every signed vertex clause and exhausted **1,296** charge patterns on K4 (16), cube (256), Petersen (1,024), with **648 SAT / 648 UNSAT parents**, **22,368** proper-block SAT checks, **8,064** boundary-relation assignment comparisons and **3,872** all-label collision partition cases. Nine valid-but-noncanonical sign mutations and nine malformed repeated-variable controls were rejected by the appropriate exact source/syntax checks. An independently implemented Node verifier constructed and checked **22,368 actual local satisfying witnesses** and **648 full even-charge satisfying witnesses** with no failures. Independently executable compact V8 verifier published as `experiments/arc/lspv2_450_compact_partition_interface.mjs`: 1,296 original instances, 22,368 local full-rank controls, 512 exhaustive K4 boundary comparisons. Its exact published bytes were read back and matched the executed string.

## Actual corpus and scientific safeguards

Read: governing 2026-11-02 five-role refocus, latest issue #3 page, AGENTS.md, CODEX.md and the PNP research skill; project LSPV-2/422,/295,/449; LSPV-4/438,/445; LSPV-1/452; LSPV-3/453; Grok `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex`; Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`. The required repositories `konard/p-vs-np` README and `blkph0x/p-vs-np-proof-research` README, METHOD_INDEX and `affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md` were inspected. This latter theorem addresses **fixed-width affine projection recognition** under its own BH hierarchy model, not a universal SAT compressor. Inspected `meelgroup/frat-xor` README and format, and `openai/math` metadata; no external format is substituted for historical R_mix341. Primary sources Urquhart, Ben-Sasson/Wigderson, Itsykson/Riazanov/Smirnov and FLMV (JACM 2005, DOI 10.1145/1101821.1101822) checked in indexed web sources. No claim of separately executing Google-branded search. Complete root main.tex was not safely available for outside-byte-preserving update, hence unchanged.

**OPEN:** an effective, all-input, malformed-aware, same-machine, recursively iterable, solver-dependent $A\mapsto\Phi(A)$ for EVERY total correct uniform polynomial SAT decider with

$$
t'\le\max\{11/10,3/5+t/2\},\qquad
s'\le\max\{1/2,s/2\},
$$

including the exact joining, construction, source access and peak-space phases. Noncircular Route B B3 and an all-rule mixed lower bound remain OPEN. P versus NP OPEN.
