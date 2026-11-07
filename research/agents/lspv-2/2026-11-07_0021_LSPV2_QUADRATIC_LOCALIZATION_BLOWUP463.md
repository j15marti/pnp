# LSPV-2/463: Quadratic size inflation required by occurrence-local equality-copy tree recompilation

**2026-11-07 00:21 PST (America/Los_Angeles) | Route A | PROVED/RESTRICTED derived quantitative corollary; COMPUTATIONAL finite controls. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE: hypothesis and falsifiers

**Initial hypothesis.** The existing restricted TT3 postorder, OR-fold and proper-3CNF guest compiler cannot gain *recursive eligibility* by simply splitting original edge-variable occurrences and connecting their copies with local equality gadgets, unless the new encoding incurs near-quadratic size inflation. Scope is fixed source-clause preservation, disjoint connected equality-copy networks, and native small-adhesion tree blocks. This is **not** a conjecture about all source transformations.

Four precommitted falsifiers: F1 original cubic-expander Tseitin's variable-primal line graph might fail to be a linear-treewidth expander; F2 connected equality-copy gadgets might fail to preserve that primal as a graph minor; F3 a bounded-adhesion tree might retain many transit variables at a node not charged to bags; F4 polynomial padding might allow the near-half-exponent block budget to absorb the treewidth despite small interfaces. F1-F3 are addressed in the proof, and F4 is exactly why the result is a **size-inflation tradeoff**, not an outright ban on all padded encodings.

## SOURCE AUTHENTICATION, PRIOR WORK, AND SEARCH

Both live proof chains read in full before work: `proof1.txt` (initial blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; nodes [P1-01], [P1-03], [P1-04], [P1-S3], [P1-X2]) and `proof2.txt` (initial blob 6ce90617b5f40356f51081a341ccfde139b7418b; nodes [P2-A2], [P2-A3], [P2-A4], [P2-A5], [P2-D1], [P2-B2]). Issue #3, AGENTS.md, CODEX.md, research skill and the latest five-role handoff were read. Current peer LSPV-4/459 and /461 and LSPV-3/467 were read. Actual Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md` (a20fb8b3640d7574faf238a4a83a021bb0984808) and Claude `research/agents/claude/world-ledger/README.md` (de75a371ce3143a4495e6892df7fb04794a6b708) were inspected.

**Important priority/precedence correction:** `research/coordination/2026-10-22_1348_EQUALITY_LOCALIZATION_MINOR_BARRIER65_HANDOFF.md` (7fa410c7bb058e6c8d9d0f1098d0ef5591b41adc) ALREADY proves the equality-copy incidence-minor obstruction for logarithmic recursive separators. LSPV-4/459 (9795607976944dd924dd76ecae5867f8ed2e69a5) independently proves an original-variable clause-split expander adhesion obstruction. The present work combines these known mechanisms with the **specific TT3 first-level size exponent** to derive a quantitative minimum *encoded-length inflation*. It does not claim priority for graph minor monotonicity, expander treewidth or Tseitin hardness.

Targeted external actual-file inspection: `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; adds parity constraints with default odd charge); `konard/p-vs-np/README.md` (0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and `proofs/complexity/README.md` (7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3: separate finite one-tape model); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (18d693ea71dfa433370eb7afbebc3106e32f03e5: restricted scope) and its README (f397a7747eaca82df3d754d0a4b4bab1fe10f814); `meelgroup/frat-xor/format.md` (986a21aa92b62f844ef1fce852193142c41b2b1f: distinct mixed-proof system); `berkeley-abc/abc/README.md` (88a9d1a316dd9751acade746de315fd1e6e6c362: circuit optimization, not a transfer); `openai/math/README.md` (cc5b0a03bca6c742f045d683b6647a6f44ef2cae: mixed research statuses). Primary academic controls: Fortnow et al. JACM 2005 DOI 10.1145/1101821.1101822 (random-access SAT time-space); Urquhart JACM 1987 and Ben-Sasson/Wigderson JACM 2001 (ordinary resolution on suitable Tseitin expanders); Itsykson/Riazanov/Smirnov SAT 2022 DOI 10.4230/LIPIcs.SAT.2022.6 (REGULAR resolution/OBDD result, not unrestricted Resolution). General search-engine and repository searches performed; **no Google-branded search service, native FLMV execution, or external theorem checker used.**

## Exact established 3-CNF family, proof model and shortcut

Fix a family of connected simple cubic graphs $G_H$ on $H$ vertices with edge expansion $|\delta_G(U)|\ge\epsilon|U|$ for all $|U|\le H/2$, with constant $\epsilon>0$. Associate $x_e$ with each of the $3H/2$ edges. Fix charges $\chi_v\in\{0,1\}$ with $\bigoplus_v\chi_v=1$. At each vertex with edges $e_1,e_2,e_3$, place the FOUR distinct proper signed three-literal clauses that falsify precisely the edge assignments with parity different from $\chi_v$:

$$
C_{v,a}=\bigvee_{i=1}^{3}\begin{cases}x_{e_i},&a_i=0,\\\neg x_{e_i},&a_i=1,\end{cases}
\qquad \bigoplus_i a_i\ne\chi_v.
$$

This is already strict 3-CNF: $4H$ clauses, $3H/2$ variables and original binary encoded length $M=\Theta(H\log H)$ with dense integer IDs. Summing parity equations gives $0=1$, an exact UNSAT certificate at the *semantic* GF(2) level. Urquhart and Ben-Sasson/Wigderson furnish exponential $2^{\Omega(H)}$ refutation-size hardness on suitable growing expander families for ordinary shared-DAG Resolution, NOT for all legal $R_{\mathrm{mix341}}$ rules or every SAT algorithm. The polynomial GF(2) charge-sum shortcut is an obligatory upper-bound control. Local equality-copy encoding is SAT-equivalent; no proof-complexity lower-bound preservation into an arbitrary calculus is inferred.

## Theorem 463.A: line-primal expansion (PROVED/RESTRICTED)

The variable-primal graph of the original signed formula is the line graph $L(G_H)$: its vertices correspond to original edge variables, and two are adjacent exactly when they co-occur at a cubic vertex. It is a bounded-degree edge expander and has treewidth $\Omega(H)$.

**Explicit proof.** For $S\subseteq E(G)$ with $0<|S|\le|E|/2$, let $V_3$ be vertices with all three incident edges in $S$, and $B$ vertices with one or two such edges. Then $|V_3|\le 2|S|/3\le H/2$, and every edge leaving $V_3$ reaches $B$. Thus $\epsilon|V_3|\le3|B|$. Moreover $2|S|\le3|V_3|+2|B|$. Therefore

$$
|\delta_{L(G)}(S)|=2|B|\ge\frac{4\epsilon}{9+2\epsilon}|S|.
$$

A graph of bounded maximum degree with constant positive edge expansion has no sublinear balanced vertex separator: removing a small separator leaves a component-union with between one-fourth and one-half of all vertices and no edges to the remaining components, contradicting expansion. Standard balanced-separator/treewidth duality therefore gives $\mathrm{tw}(L(G))\ge cH$ for a constant $c>0$ depending only on $\epsilon$.

## Theorem 463.B: quantitative quadratic re-encoding barrier (PROVED/RESTRICTED)

Consider ANY proper-ternary formula $F'_H$ obtained by (i) replacing each ORIGINAL literal occurrence by a variable copy while retaining a corresponding ternary source clause, (ii) connecting all copies of each original variable by a connected network of actual equality constraints, and (iii) using only gadget-private auxiliary variables for each variable's equality network, disjoint across different original variables. Further extra clauses/variables are allowed provided the original clause triple and these connected, disjoint branch sets survive. Let $M'=|\mathrm{encode}(F'_H)|$.

Contracting each connected equality-copy branch set in the PRIMAL graph of $F'_H$ creates the original primal graph $L(G_H)$ as a minor: each original ternary clause still supplies every original pairwise edge. Therefore $\mathrm{tw}(\mathrm{primal}(F'_H))\ge cH$.

Suppose $F'_H$ admits a max-degree-three tree of clause blocks with: at most $B(M')$ encoded source bits per node; every variable's clause-occurrence bags connected through their tree paths; at most $w(M')$ distinct variable IDs on any tree-edge adhesion. Add to each tree bag its local clause variables and transit variables on incident adhesions. Each bag then contains at most $3B+3w$ variables, so it is a legitimate primal-graph tree decomposition and

$$
cH\le\mathrm{tw}(\mathrm{primal}(F'_H))+1\le3B(M')+3w(M').
$$

Under TT3 target $B(M')\le (M')^{1/2+o(1)}$ and $w(M')=O(\log M')$, this implies

$$
\boxed{M'\ge H^{2-o(1)}=M^{2-o(1)}.}
$$

Proof of the last implication: if $M'\ge H^2$, it is immediate; otherwise $\log M'=O(\log H)=o(H)$, so $B=\Omega(H)$ and $B\le(M')^{1/2+o(1)}$ forces $M'\ge H^{2-o(1)}$.

**Scope firewall.** The theorem is about explicit ORIGINAL clause-preserving, disjoint connected equality-copy networks and a bounded-degree, bounded-adhesion tree grammar. It does NOT constrain nonlocal semantic compilers, GF(2) elimination, source-clause deletion/substitution, arbitrary extension rewrites that destroy the graph minor, general uniform SAT algorithms, or $R_{\mathrm{mix341}}$ proof minima. Its main content is a source-size/adhesion tradeoff; a quadratic-size padded encoding can evade the *incompatible bounds* by being too large for useful contraction.

## Finite implementations and negative controls

Independently written Python and JavaScript programs constructed the ORIGINAL signed strict 3-CNF for K4, cube, Petersen, charge parity 0 and 1 each, copied every literal occurrence, connected copies by real equality gadgets $(\neg a\vee b)\land(a\vee\neg b)$, and converted every binary facet into two proper ternary clauses with fresh helpers. For all original assignments, evaluate the full canonical equal-copy lift, which satisfies all equality gadgets and agrees with source satisfaction. Conversely each equality gadget enforces $a=b$, so every satisfying expanded assignment projects to a true original assignment (symbolic proof, not exponential enumeration of all expanded assignments).

Python: six original sources; all minor connectivity and cross-branch primal edges verified; K4/cube/Petersen balanced two-thirds primal separator sizes 2/4/4; original-source SAT and UNSAT controls; exact original graph and line-graph finite expansion enumerated; 73,856 exhaustive original-model projection checks. Independent JS: 73,856 such checks, 132 verified original-primal cross-branch edges, 84 supporting assertions, six deliberately corrupted authenticated-source controls. All PASS. These small graphs are **NOT** asymptotically certified Resolution-hard instances. Local Python/JS execution is **NOT** a native FLMV machine benchmark or all-input contraction.

Published code: `experiments/arc/lspv2_463_public_selfcheck.cjs`; raw: `results/raw/arc/2026-11-07_0021_LSPV2_463_COPY_MINOR.json`. The expanded complete Python producer and independent JS test are also preserved in the local reproducibility archive supplied with this run.

## Charged resource ledger and outstanding transfer

This theorem lower-bounds encoded $M'$ for a restricted re-encoding architecture, **not** physical algorithm time or space. Finite producer used host RAM to hold full graphs, clauses and exhaustive assignments; no low-space FLMV claim. Actual candidate wrapper must charge source reads/authentication, parsing and variable names, gadget generation, source/guest input indexing, every work-index operation, guest resets and failed search, auxiliary bits, validation and all-phase simultaneous peak. A near-quadratic $M'$ is fatal to this particular attempt to obtain recursively smaller TT3 guests, but cannot rule out a solver-dependent NON-minor-preserving compiler. Restricted proof length does not translate to machine hardness.

**Tracker disposition:** material new quantitative evidence for [P2-A4] and the open [P2-A5] recursive-closure obstruction; [P1-S3] reviewed without any claim of an all-input algorithm. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-B2], [P2-D1] stay OPEN. Fixed historical $R_{\mathrm{mix341}}$ and five-role allocations untouched.

## Next exact missing implication

Find an effective, original-source-authenticated, SAME-MACHINE transformation of **an arbitrary SAT decider's OWN computation** into smaller SAT instances that does NOT preserve this copy-connected minor and that remains self-applicable after one iteration. Only then try to prove the all-input, both-label, malformed-aware $t',s'$ recurrence with full acquisition/space charges. P versus NP remains OPEN.
