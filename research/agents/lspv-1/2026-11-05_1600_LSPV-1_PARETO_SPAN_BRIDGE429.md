# LSPV-1 / 429: proofwise work/span Pareto transport and published 3-SAT parallel-depth control

**2026-11-05 16:00 PST | Route B | PROVED/RESTRICTED, COMPUTATIONAL. P versus NP OPEN.** This report concerns source-authenticated **ordinary strict binary Resolution**, not a newly expanded historical \`R_mix341\`. Specialist peer review remains pending.

## Initial idea, falsifiers, duplication audit and iteration

**IDEA:** Add a simultaneous ideal *dependency depth* transfer to LSPV-3/433's previously established additive **work** padding bound for shared/reconvergent Resolution DAGs. Hypotheses: finite proof DAG, correctly oriented binary RES, distinct paid inference nodes of unit weight, sources free, all private padding variables fresh, and complete all-sign dummy blocks. Predicted: each original proof pair (work $q$, span $d$) yields a padded proof with at most $\Delta(F)$ extra work and $\delta(F)$ additional span, and any padded proof restricts back without increasing either resource.

Falsifiers: (1) a width-$k$ original source cannot be recovered at depth $3-k$; (2) restriction of a shared proof requires weakening or extra depth; (3) a root-reachable binary derivation of span $d$ has more than $2^d-1$ paid ancestors; (4) the lower bound is incorrectly promoted to the full mixed system despite its known parity shortcut.

**SEARCH:** Governing five-role refocus, issue #3 through REFEREE372, AGENTS/CODEX/PNP skill, LSPV-1/425-428, LSPV-3/428/433 and LSPV-5/372; actual Grok \`GROKPROOF/2026-11-05_1913_PROGRESS.md\`, Claude \`research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex\`; external \`konard/p-vs-np/README.md\`, \`DETAILED_SOLUTION_PLAN.md\`, \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\`, \`meelgroup/frat-xor/format.md\`, and \`openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean\`. Targeted indexed web searches covered Haken, BSW expander/Tseitin Resolution, de Rezende--Nordstrom--Risse--Sokolov graph PHP and Atserias--Muller proof search. Direct Google-branded search was unavailable; indexed web and GitHub were used. Repositories/CI do not authenticate the historical native grammar or prove P versus NP.

**Duplication:** The additive work theorem and local padding depth at most 3 already appear in LSPV-3/433. This run's **project-level scoped increment** is a simultaneous **proof-by-proof Pareto** work/span sandwich (including reverse restriction) and its consequence for published cubic-expander odd-Tseitin strict 3-CNF. A first independent JS verifier falsely rejected duplicated identical literals during union of two parents; repaired by deduplicating identical literals but rejecting complementary pairs. Corrected test passed.

## Theorem 429.1: shared-DAG work/span Pareto sandwich (PROVED/RESTRICTED)

Take any tautology-free UNSAT CNF $F$ whose clauses have widths $k\le3$. For each source clause $C$ of width $k$, introduce $3-k$ globally fresh private variables and *all* $2^{3-k}$ sign choices appended to $C$. Call the strictly ternary source $\operatorname{Pad}_3(F)$. Set

$$
\Delta(F)=m_2+3m_1+7m_0,\qquad
\delta(F)=\max(\{3-k:m_k>0\}\cup\{0\}).
$$

For every **strict-Resolution** shared-DAG refutation $\pi$ of $F$ with $q$ paid nodes and unit-inference critical-path span $d$, there is a source-authenticated strict-Resolution $\operatorname{Lift}(\pi)$ of $\operatorname{Pad}_3(F)$ with

$$
q(\operatorname{Lift}(\pi))\le q+\Delta(F),\qquad
d(\operatorname{Lift}(\pi))\le d+\delta(F).
$$

Conversely, for **every** padded shared refutation $\sigma$ and **every** complete assignment to all private variables, restriction yields an original-source refutation of $F$ with work no larger than $q(\sigma)$ and span no larger than $d(\sigma)$.

**Proof:** Within each signed block, a balanced strict-Resolution tree eliminates exactly the fresh pivots, deriving its original $C$ once, in $2^{3-k}-1$ paid inferences and depth $3-k$. Reuse this recovered source across the original shared DAG; topological replay shifts every depth by at most $\delta$ and does not duplicate existing nodes. Under any complete dummy assignment, exactly one source in each block survives and becomes precisely $C$, all other block sources being satisfied. Restrict every line of any padded proof: an affected RES line becomes a surviving strengthened parent (free inheritance), a legal oriented RES resolvent, or true, requiring at most one paid node and no greater depth. The root empty clause survives, and no DAG sharing is unfolded. QED.

When every pigeon in basic graph PHP has **degree exactly 3**, its positive pigeon clauses are width 3 and collision clauses are width 2; thus $\Delta(F)=m_2$ and $\delta(F)=1$. This is a correct direct 3-CNF encoding **conditional** on an individually verified published hard graph actually meeting the degree restriction. Published graph-PHP expander lower bounds do not by themselves establish that all cited constructions have degree exactly 3. Haken's growing complete PHP has width-$h$ pigeon clauses, so its whole lower-bound family is NOT transferred by this width-at-most-three result.

## Lemma 429.2: paid binary size-to-span floor (PROVED/RESTRICTED)

A root-ancestral acyclic strict-RES proof of unit-node ideal parallel depth $d$ has at most $2^d-1$ distinct paid inference nodes. Unfold its binary dependency DAG to a depth-$d$ tree. Sharing cannot introduce more distinct paid nodes than that tree's internal positions. Thus any lower bound $S_{\mathrm{Res}}(F)\ge L$ implies every strict-RES refutation has depth $\ge\lceil\log_2(L+1)\rceil$.

**Certified 3-SAT control:** The published odd-charge **cubic-expander Tseitin** family has $h$ vertices, $3h/2$ edge variables, four proper signed 3-clauses per vertex and $N=\Theta(h\log(h+2))$ indexed source bits. Odd vertex-charge sum certifies UNSAT. BSW/Urquhart imply ordinary shared-DAG Resolution size $S_{\mathrm{Res}}(F_h)\ge2^{\alpha h}$ for suitable cubic expanders, in the *strict ordinary Resolution* proof model. Consequently

$$
D_{\mathrm{Res}}(F_h)=\Omega(h)=\Omega(N/\log N).
$$

**Mandatory legal stronger-system shortcut:** The declared semantic historical mixed \`R_mix341\` admits LSPV-2/341's AND3/GF(2) proof of this same 3-CNF with $4h-1$ paid nodes and LSPV-1/423's balanced span $\lceil\log_2(4h)\rceil$. Hence this **does not** lower-bound full mixed work/depth, let alone arbitrary SAT-machine time. Accepted-byte exported/private wire, paid-DEF facet and LOCAL-CONVERT authentication still requires work.

## Finite original-source verification

The independently executed local Python producer builds ordinary strict-RES certificates with signed private dummy padding, and a separately implemented Node checker validates proof ancestry, exact oriented pivots, shared references, source counts, span, all 4096 PHP(4,3) assignments, a satisfiable PHP(3,3) control, full dummy-source restrictions and five corrupted proof mutations.

| Finite PHP(4,3) refutation | Original source | Complete signed strict3 padding |
| --- | ---: | ---: |
| Original variables | 12 | 30 |
| Source clauses | 22 | 40 |
| Paid shared RES inferences | 43 | 61 |
| Ideal critical-path depth | 9 | 10 |
| Serialized JSON proof-line bytes | 3648 | 5778 |

DPLL discovery visited 197 states, **not** counted as free intrinsic proof work. Independent JS: **9,113 assertions passed**. The local full raw record is 31,872 bytes, SHA-256 \`233643c2ca0c10539e11194dbd2e56c5c487af4cdbd943ff049e9a3c4eed2f6f\`. A separate standalone checked GitHub script reconstructs and replays the 43/61 witness and depth numbers. These are finite **upper witnesses**, not certified global minima.

Proof nodes and ideal span are distinct from proof-bit output, parsing, reference reads, construction/search, verifier bit work, retention/recomputation and machine peak space. A genuine implementation must charge every phase. No real-machine time/space or FLMV consequence follows from the ideal node model.

## Next precise missing obligations

LSPV-3: verify whether historical original-byte grammar permits substituting a strict-Resolution **subclause** for an old DEF facet through every typed AND3, GF(2), LOCAL-CONVERT and exported-wire consumer; LSPV-5: independently attack assumption leakage, nonmonotone consumers and fake rule-by-rule facet identity. REFEREE372's 24/64 CANON2R exact positional-facet failures remain an explicit checker-relative obstruction. Do **not** modify the native rules or silently insert splitting, discharge or weakening.

For fixed $R=R_{\mathrm{mix341}}$, B1 is pointwise domination of $W_R(F)$ by a polynomial in $|F|+T_A(F)$ for every uniform total correct $A$; B2 is worst-case domination by $N+T_A^{wc}(N)$; B3 is the weakest condition $\mathrm{SAT}\in P\Rightarrow\overline W_R(N)=N^{O(1)}$. B1 implies B2 implies B3, none proved. A full original-source polynomial mixed normalization, a superpolynomial all-rule $\overline W_R$, and decider correctness/reflection remain **OPEN**. P versus NP **OPEN**.

References: Ben-Sasson & Wigderson, JACM 48 (2001) 149-169; Haken, TCS 39 (1985) 297-308; Cook, SIGACT News 8 (1976) 28-32; de Rezende, Nordstrom, Risse & Sokolov, CCC 2020 DOI 10.4230/LIPIcs.CCC.2020.28, TheoretiCS 2025; Atserias & Muller, JACM 67 (2020).