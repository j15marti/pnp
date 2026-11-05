# LSPV-3/431 | Path graph-PHP: exact minimal mixed proof and invalid lower-bound restriction transfer

**2026-11-05, America/Los_Angeles. Route B. PROVED/EXACT as an all-size restricted-model theorem, COMPUTATIONAL finite controls, P versus NP OPEN.**

## IDEA before SEARCH

Test whether a hard published complete pigeonhole CNF can be edge-restricted to a width-at-most-three graph-PHP formula while retaining a nontrivial Resolution lower bound, especially when every surviving source clause is individually indispensable and the Hall-deficient core requires every pigeon.

Falsifiers: (F1) restriction does not reproduce the claimed source clauses; (F2) any claimed essential clause has no satisfying deletion witness; (F3) the advertised linear refutation contains an illegal pivot, source or cycle; (F4) a hidden Resolution shortcut beats the advertised optimum; (F5) the result is incorrectly promoted from a nonexpanding path to published expander-hard graphs or unrestricted machines.

## Source model and exact encoding

Use the **standard basic** graph pigeonhole principle (no functionality or onto axioms). For each $h\ge1$, let pigeons be $p_0,\ldots,p_h$ and holes $0,\ldots,h-1$. Connect $p_j$ to hole $j$ and $p_{j+1}$ to hole $j$. Thus every hole has exactly two incident pigeons, every interior pigeon has two choices, and the two end pigeons have one choice.

Use original edge variables $a_j=x_{p_j,j}$ and $b_j=x_{p_{j+1},j}$, with DIMACS identifiers $a_j=2j+1$, $b_j=2j+2$. Clauses are

$$
P_0=(a_0),\qquad P_i=(b_{i-1}\lor a_i)\ (1\le i<h),\qquad P_h=(b_{h-1}),
$$

$$
H_j=(\neg a_j\lor\neg b_j)\quad(0\le j<h).
$$

Exactly $2h$ variables and $m=2h+1$ nonempty source clauses. Every clause has width at most two, hence this is directly a width-at-most-three CNF, not a claim that the instance is a proper width-exactly-three hardness instance. Signed ASCII DIMACS length $N_h=\Theta(h\log(h+2))$. The formula is UNSAT since $h+1$ pigeons cannot inject into $h$ holes.

**Important literature qualification:** de Rezende, Nordström, Risse, Sokolov (CCC 2020) prove exponential ordinary-Resolution lower bounds for specified sparse graph-PHP/FPHP expanders, but their representative weak-PHP degree parameters can exceed three; one must not call these particular hard inputs direct 3-CNF without a documented encoding and hardness-preserving translation. This path is a deliberately easy **countercontrol**, not one of their expander-hard graphs.

## Theorem: full indispensability and exact paid minimum

**PROVED/EXACT (all $h\ge1$).** Every one of the $2h+1$ source clauses is individually indispensable. For the historical fixed $R_{\mathrm{mix341}}$ with unit weights, conservative paid definitions, and at most two premises per paid node,

$$
\boxed{W_{R_{\mathrm{mix341}}}(F_h)=2h.}
$$

**Proof of essentiality.** On deletion of $P_i$, set exactly $a_j=1$ for $j<i$ and $b_j=1$ for $j\ge i$, all other variables zero. Every remaining pigeon row is satisfied, no hole is shared, and precisely $P_i$ is false. On deletion of $H_i$, set exactly $a_j=1$ for $j\le i$ and $b_j=1$ for $j\ge i$, all other variables zero. All pigeon rows are satisfied; only hole $i$ is shared and precisely $H_i$ is false. Thus every source clause is needed.

**Lower bound.** Any sound source-explicit refutation needs all $m=2h+1$ essential original clauses as ancestors of the empty conclusion, even allowing shared DAGs, conservative auxiliary definitions, and every other legal at-most-binary-premise rule. The connected ancestral dependency graph with $m$ source leaves and $q$ paid nodes has at least $m+q-1$ edges but at most $2q$ premise edges, giving $q\ge m-1=2h$. There is no requirement that the proof be a tree.

**Matching upper bound.** Starting at source $P_0=(a_0)$, resolve with $H_0$ on $a_0$ to obtain $(\neg b_0)$, then with $P_1$ on $b_0$ to obtain $(a_1)$. Repeat through hole $h-1$, and finally resolve with $P_h$ to reach the empty clause. Every step is ordinary unrestricted binary RES, a historical native rule. This gives exactly $2h$ paid nodes and proves the minimum without any finite-search cutoff. The exhibited sequential chain has depth $2h$, but no assertion is made that this depth is globally minimal.

**Maximal Hall-witness control.** For each deleted pigeon $P_i$, the preceding witness yields a matching of all other pigeons. Every proper subset of pigeons is contained in some such deletion, so every proper subset satisfies Hall's condition. The smallest Hall-deficient pigeon subset is therefore the entire set of $h+1$ pigeons. Thus maximal indispensable-source count AND maximal Hall-violating-subset size coexist with linear native proof cost. Neither can be promoted to superlinear generalized-work hardness.

## Theorem: one-way restriction does not transfer hardness

Let $\mathrm{PHP}_{h+1}^h$ be the **complete** basic PHP CNF with variable $x_{p,j}$ for every pigeon-hole pair, positive row clauses and negative collision clauses. Define the fixed missing-edge restriction $\rho_G(x_{p,j})=0$ whenever $(p,j)$ is absent from the path graph; keep the two path edges per hole free. Exact clause restriction deletes the missing positive row literals and satisfies every collision clause involving a missing edge. After the explicit variable renaming above,

$$
\boxed{\mathrm{PHP}_{h+1}^h\big|_{\rho_G}=F_h.}
$$

Haken's published $\exp(\Omega(h))$ ordinary-Resolution lower bound applies to the **complete** formula. Yet the restricted formula has an exact ordinary-Resolution and mixed-$R_{\mathrm{mix341}}$ refutation using $2h$ paid inferences. The closure of Resolution under restrictions, when used in the valid direction, offers $L_{\mathrm{Res}}(F|_\rho)\le L_{\mathrm{Res}}(F)$, not its converse. Therefore no lower bound for the complete formula transfers merely from this equisatisfiable, variable-fixing restriction. This is a concrete all-size failure of a proposed hardness-transport **inference**, not a counterexample to Haken's theorem or to the expander graph-PHP theorems. The complete source has clauses of width $h$, so it is **not directly 3-CNF for $h>3$**.

## Proofs, independent tests and resource ledger

The producer explicitly builds each source and ordered RES certificate. A separate, independently implemented bitmask checker reconstructs every oriented inference; both implementations check deletion-model source truth, and the full-PHP restriction formula is reconstructed independently. For $1\le h\le64$, **378,944 assertions** passed (set-based and BigInt-mask checkers, exact graph restriction); **21,844 full assignments** were checked for unsatisfiability at $h\le7$; **24 hostile mutations** were rejected, including wrong pivot, source, deletion witness, and omitted final AND obligation. Selected full certificates and witnesses are included in raw JSON. This is **COMPUTATIONAL** corroboration of the all-size written proof, not an authoritative complete-native checker replay beyond its unrestricted RES fragment.

Logical work minimum is exactly $2h$. The exhibited chain's weighted critical-path span is $2h$, while a different valid proof might have smaller span at greater paid-node work. Serialized proof bits are $O(h\log(h+2))$ for this linear chain with decimal IDs; generated deletion witnesses taken all together require $O(h^2\log h)$ bits. A streaming generator needs index/state counters of $O(\log h)$ bits besides the read-only original and append-only output under an explicitly indexed-access model, but this is not a measured FLMV machine-space bound. Parsing, source queries, verification, branch search, proof output, retrieval/recomputation and peak buffers are separate physical costs and are not charged to the ideal proof minimum. No uncharged split/discharge, weakening, ER or DRAT rules are added.

## Search ledger, duplicates, gaps

Source checked: original /341 at SHA c87acd11d32ccfc3b7acd3667ef11daeb60079cb; governing 2026-11-02 five-role handoff; issue #3; AGENTS.md, CODEX.md and the pnp-research skill; LSPV-3/430 graph-PHP individual-essentiality theorem and prior /384 Hall-to-PHP ER work; LSPV-1/426 reuse accounting; active Grok 2026-11-05_1218_PROGRESS.md and Claude TPORT-0002. This supplements /430 with a **sharp all-size source-minimal countercontrol**, not a discovery of a new graph family or a novel proof-complexity technique.

Both required external repositories checked: konard/p-vs-np README and formal proof-status manifest (its finite-machine P-subset-NP results do not supply B3); blkph0x/p-vs-np-proof-research README and RESOLUTION_STANDARD.md (its accepted results do not establish universal lower bounds). FRAT-XOR format/verified checker reviewed; its proof semantics cannot silently substitute for native Rmix. OpenAI math GitHub was searched for a direct proof-compiler connection without relevant hit. Primary sources: Haken 1985 as discussed in de Rezende et al. CCC 2020, and Cook 1976 polynomial-size ER PHP proof. Exact URLs: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2020.28 ; https://dblp.org/rec/journals/sigact/Cook76 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC7089731/ . The latter discusses modern short PHP proofs in stronger nonnative redundancy calculi. Direct Google-branded search was unavailable. No new published 3-CNF hardness theorem was verified for this nonexpanding path.

**OPEN:** the original Rmix341 LOCAL-CONVERT/private/exported-wire/DEF-facet serialization and polynomial source-retracting normalizer; a superpolynomial full mixed $\overline W_R(N)$; any noncircular fixed-$R$ B3 implication, any FLMV all-input contraction, and P versus NP. Natural next target is a published, explicitly parameterized expanding **width-three** hard family with certified theorem assumptions, followed by actual mixed legal ER/GF(2)/shared-DAG shortcut checks. No research automations, schedules, roles, rules, weights or root main.tex were changed.
