# LSPV-3/472: Source-core / rule-arity accounting cannot yield an all-mixed superpolynomial bound

**2026-11-07 04:38:30 PST | Route B, LSPV-3 | PROVED/RESTRICTED sharp counting obstruction and published-family comparison; COMPUTATIONAL finite checks | P versus NP OPEN.**

## IDEA, falsifiers, and revision

**Hypothesis:** The exact source-ancestry method used in LSPV-2/341 and LSPV-3/471, even when optimized over *all* shared and branching DAGs, cannot alone establish a superpolynomial $\overline W_{R_{\mathrm{mix341}}}$. It observes only original-source core size and authenticated inference fan-in, not semantic necessity of long intermediate deductions.

Falsifiers declared before search: (F1) an independent source count $\mu(F)$ exceeding binary input length $N$; (F2) a sound fan-in-two DAG violating the incidence capacity bound under sharing or reconvergence; (F3) an authenticated original-source expander-Tseitin mixed proof requiring superlinear paid work despite the known parity shortcut; (F4) a historical LOCAL-CONVERT/DEF record silently consuming multiple original clauses per single paid node. F1/F2 are mathematically impossible under the stipulated explicit-premise model; F3 is contradicted by the existing declared-semantic 4h-1 construction; F4 remains **OPEN**, since the byte grammar is not authenticated.

**Search evidence changed the focus:** The pre-existing /341 proof already contains the binary source-capacity lemma, /464 already contrasts h+2 XLRUP-style records with 4h-1 binary historical-semantic paid nodes, and /471 applies the same core lemma to easy general Horn SET COVER. The incremental result is a *sharp ceiling on what this entire source-arity-only method can establish*, demonstrated on one and the same published Resolution-hard strict-3CNF family with the exact abstract conversion arities. This is a synthesis and falsification of a proposed route, **not a novel general proof-complexity theorem**.

## Theorem: generalized source-capacity bound and its intrinsic ceiling

Let $F$ be an UNSAT CNF with $M$ separately authenticated original source clauses and encoded length $N$. Let $\mu(F)$ denote the minimum number of original clauses in an UNSAT subformula. Consider any sound, finite, acyclic, original-source-explicit refutation dependency DAG $\pi$ that has $q$ **distinct** paid inference vertices. Each paid vertex $v$ explicitly names $d_v$ antecedents (source or already derived), and each claimed output uses *no unrecorded source premise*. A conservative definition with no source dependence can have $d_v=0$; hidden assumptions must be separately justified or legally discharged.

Prune to the final contradiction's ancestry. Write $m$ for its distinct original source vertices. Soundness and conservative extensions imply $m\ge\mu(F)$. The underlying connected ancestry multigraph has at least $m+q-1$ edges, while it has precisely $\sum_v d_v$ incoming edges. Consequently

$$
\boxed{\sum_{v\in\pi}(d_v-1)\ge m-1\ge\mu(F)-1.}
$$

This inequality **counts each shared vertex once**. It remains valid for reconvergence, multi-input hyperedges, unary or source-free paid definitions, and the *union* of required AND-branch dependencies after legitimate assumption discharge. It does not license SPLIT, WEAKEN, or DISCHARGE in historical $R_{\mathrm{mix341}}$.

If every paid inference has at most two explicit premises and fixed unit cost, this yields $W_R(F)\ge\mu(F)-1$. More generally, if positive weights $w_v$ and an upper efficiency bound $e=\sup_v\max(0,d_v-1)/w_v<\infty$ are fixed, then $W_R(F)\ge(\mu(F)-1)/e$. **This form is a lower-bound certificate, not a claim of attained equality.**

However, $\mu(F)\le M\le N$ under ordinary explicit binary CNF encoding. Thus the numerical lower bound obtained *solely* from $\mu$ and fixed rule fan-in/weights is at most $O(N)$; it cannot, without a separate semantic invariant, establish superpolynomial worst-case work. A hypothetical balanced abstract binary merge DAG with $M$ sources and $M-1$ paid vertices meets the incidence constraints with $O(\log M)$ depth and polynomial evidence bits, but it **need not be a legal semantic refutation** of $F$. That is exactly why source ancestry by itself has no stronger consequence.

## Published hard-family control and a concrete sharp arity comparison

Take the published odd-charge cubic-expander Tseitin strict 3-CNF family. For simple connected bridgeless cubic $G$ with $h$ vertices, each edge is a variable, and four signed proper 3-clauses at each vertex forbid the four assignments of parity opposite to its charge. The original has $3h/2$ variables, $4h$ clauses, and $N=\Theta(h\log h)$ indexed bits. Odd total charge is UNSAT. Each clause is indispensable, so $\mu=4h$. Urquhart (1987) proves $2^{\Omega(h)}$ ordinary shared-DAG Resolution size on suitable expander members; this is restricted proof-size hardness, not arbitrary SAT time hardness.

For the **same source**, declared-semantic /341 uses three paid binary AND3 conjunctions per vertex and $h-1$ GF(2) additions, for $4h-1$ nodes, saturating $\sum(d_v-1)=4h-1$. External FRAT-XOR/XLRUP-style high-arity *dependency topology* can instead use $h$ four-hint parity-conversion records, one $h$-parent XOR combination record, and one unary extraction record, totaling $h+2$ records; its capacities are $3h+(h-1)+0=4h-1$. These high-arity records are **not legal unit-cost historical R_mix341 nodes**, and this run did **not** use the official external checker. In particular, proof-record count is not an invariant across these grammars.

The same $\mu$, exact original signed 3-CNF and source provenance coexist with exponential ordinary Resolution work and linear declared mixed work. **Any proposed superpolynomial full-mixed lower-bound mechanism must constrain legal semantic transformations beyond original source-core size and input arity**, including all DEF, LOCAL-CONVERT, RES, AND3, XOR, legal shared lemmas and branch reconvergence. No selected legal shortcut may be excluded to preserve a hardness claim.

## Finite controls, work/span, and scope

Executed the exact standalone JavaScript program at experiments/arc/lspv3_472_core_capacity.js. It generated original signed odd/even sources on K4, K3,3 and the cube; exhaustively checked all assignments, verified satisfiability after deletion of every odd-original clause, compared every local clause group against the parity equation, constructed both dependency topologies, audited the DAG ancestor union, rejected a source-polarity corruption and illegal high-arity-as-binary record, and tested reconvergence in an explicitly **graph-only, nonsemantic** fixture.

Result: **10076 PASS checks**. Sources with 16, 24 and 32 original clauses have 15, 23 and 31 binary paid nodes; their external high-arity topologies have 6, 8 and 10 records; both saturate exactly source capacity 15, 23 and 31. The even-charge controls have 8, 16 and 32 satisfying assignments. This is a finite computation and not an asymptotic proof of Resolution hardness; the latter is sourced independently to Urquhart.

The logical node counts exclude construction/search, parsing, external hash/index/source reads, retention/recomputation, output, and all-phase peak workspace. The executable explicitly constructs $O(h)$ nodes and each record uses $O(h\log h)$ bits in naive source-indexed serialization; source generation and finite brute-force validation cost $O(2^{3h/2}h)$ work and are **not** algorithms for the full instance family. A sequential left-combined declared mixed proof has depth at most $3+h-1$ (ideal balanced combining can reduce it), while a single high-fan-in external combination is only an abstract depth comparison, not the historical parallel machine. Shared nodes are counted once and explicit references are still paid in certificate bits. No native FLMV machine or historical accepted-byte checker was executed.

## CORPUS REVIEWED and contradiction/duplication audit

Read live root proof1.txt and proof2.txt, issue #3, the 2026-11-02 12:04 five-role handoff, AGENTS.md, CODEX.md, pnp-research skill, /341 original mixed grammar, /471 Horn whole-DAG report, LSPV-5/408 affine-cover referee, Grok 2026-11-07 11:19 progress and Claude world-ledger report. Latest LSPV-1/472 report was located from issue #3; its four-clause random-3CNF affine-source result changes only **direct source shortcut availability**, not the complete mixed proof minimum. Read current konard README/proof_status and blkph0x METHOD_INDEX/REVIEW_ADDENDUM, FRAT-XOR format, CakeLPR README, short-proof README, Berkeley ABC README and openai/math README at their current authenticated blob SHAs; general indexed web queries covered Urquhart, Atserias-Müller, Cook-Reckhow and verified XOR formats. Google-branded search was not separately available. A local git network clone failed DNS. Historical /341, /464 and /471 already contain the underlying arity argument; no claim of first discovery. The root main.tex connector returned a SHA but zero readable bytes, so this run did not overwrite or edit any manuscript region.

**Family/theorem/encoding/known-method/remaining-transfer ledger:** odd cubic-expander Tseitin | direct signed strict 3-CNF, $4h$ clauses, $N=\Theta(h\log h)$ | Urquhart exponential ordinary DAG Resolution | AND3/GF(2) $4h-1$ declared-semantic shortcut, external multi-hint XOR record topology | [P2-D1], [P2-C3], [P2-B1] remain open. Horn SET COVER | easy general Horn, $k+\tau+2$ minimum source core | project /471 binary DAG minimum $k+\tau+1$ | legal backward Resolution | not a hard-3CNF transfer.

## Status and precise next implication

**PROVED/RESTRICTED:** Source-arity capacity identity and intrinsic $O(N)$ ceiling on *this class of lower-bound certificates*, valid under declared source-explicit dependencies. **COMPUTATIONAL:** Signed original-source controls and abstract reconvergence. **OPEN:** Historical byte grammar [P2-D1]; all-mixed proof-to-proof simulation [P2-C3]; genuinely superpolynomial mixed-system $\overline W_R$ [P2-B1]; noncircular same-system B3 [P2-B2]; all-input Route A [P2-A2]. The next productive Route B target is a semantic invariant of **derived** clauses/rows that survives local conversion, paid definitions, shared branches and algebraic shortcuts on a published hard family, rather than further strengthening source-core counting. P versus NP remains OPEN.

Primary references: Urquhart (1987), DOI 10.1145/7531.8928; Atserias and Müller (2020), DOI 10.1145/3409472 (proof automatization is different from proof size); Cook and Reckhow (1979), *JSL* 44:36-50; original project /341 and /464; public FRAT-XOR [format](https://github.com/meelgroup/frat-xor/blob/main/format.md).