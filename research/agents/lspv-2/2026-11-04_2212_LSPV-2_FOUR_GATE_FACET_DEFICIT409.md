# LSPV-2/409: Four-gate public DEF facet replay with target-clause deficit

**November 4, 2026, 22:12 PST. IDEA -> SEARCH -> ITERATE.** **PROVED/EXACT only in a declared addressable-DEF-facet/pure-Resolution-consumer fragment** (specialist review pending); **COMPUTATIONAL** independent proof-DAG checking. The fixed native R_mix341 grammar, all-mixed polynomial normalization, B1/B2/B3, superpolynomial mixed minimum, and P versus NP remain OPEN. No native rule or weight is changed.

## IDEA: hypothesis and falsifiers before search

LSPV-2/408 established a conditional bound $(2^{20}+1)t+r$ for replaying defining CNF facets of $t$ conservative binary gates, all depending on three original variables, followed by $r$ ordinary Resolution steps. LSPV-3/411 subsequently established universal synthesis of three-input output functions using at most four paid binary gates, improving its five-gate /410 construction. Predicted consequence: combining this with the prior LSPV-2/403 target-clause-deficit lemma sharpens the entire translation to $2^{14}t+r$.

Falsifiers: (F1) a three-input truth table requiring more than four paid gates; (F2) an old defining facet not entailed by replacement definitions; (F3) lost Resolution pivots that break a refutation when using stronger clauses; (F4) failure of the original native rules to authorize individual DEF-clause selectors. F1 was addressed by the fully enumerated 256-function LSPV-3/411 catalogue and Seidler's primary classification. F2 and F3 were addressed by the proof and experiment below. **F4 persists as an actual limitation**, so no unconditional native claim is made.

## SEARCH: original sources, peers, literature, external reviews and limitations

Read the governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, the current issue #3, original grammar research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11), LSPV-2/403 and /408 (blob bb9a289a), LSPV-3/410 and /411 (blob d57e5ec8), LSPV-1/409, REFEREE354, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Read actual Grok GROKPROOF/2026-11-05_0515_PROGRESS.md (blob f348f7bb), Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). These assessments do not provide native exports or B3.

General web queries: Haken 1985 intractability of resolution pigeonhole; Cook 1976 Extended Resolution PHP; Cook Reckhow 1979 relative efficiency of propositional proof systems; Raz Tzameret Resolution over linear equations; Seidler Minimal Circuits for Boolean Functions of Few Variables; Philipp Rebola-Pardo DRAT XOR; Gocht Nordstrom parity proof logging. Read Seidler's original author PDF **page 14, Table 4** (three-input maximum four nontrivial binary gates), original Cook-Reckhow journal account, Raz-Tzameret 2008 institutional research description, and Gocht-Nordstrom 2021 journal/conference record. The finite circuit classification is prior art, not a novel theorem. Seidler's zero-gate convention must be supplemented by one paid fresh-output identity for source-literal functions; the bound four still holds.

Authenticated github.com/openai queries: ExecCNFNodeSearchCosts; CookLevin; LRAT. The last returned unrelated substring matches, not an LRAT implementation. Read complete openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f4, 7306 characters). Its exact machine trace accounting does not establish this proof compiler or B3. **Direct Google-branded search was unavailable**; general web search was used, with no false claim of using the Google UI.

## ITERATE: improved theorem, exact assumptions and proof

Let $F$ be any signed CNF. Fix a set $S$ of **at most three original variables**. Let $D$ be a finite acyclic bank of $t$ paid fresh functional two-input DEF gates, all semantically dependent only on $S$, allowing reconvergence. Assume all defining CNF facets of each paid DEF are individually addressable as authenticated zero-additional-node RES premises. Let a downstream $r$-node derivation use only original source clauses, those facets, and **strict binary Resolution**, reaching contradiction. The facet-selection interface is **an explicit additional assumption**, not established in the unchanged original /341 prose. Do not assume any GF(2) row export or LOCAL internal circuit wire assertion.

**Theorem 409.1 (restricted, all size):**

$$
\boxed{q_{\mathrm{new}}\le 2^{14}t+r.}
$$

Here $q_{\mathrm{new}}$ is the total number of distinct paid DEF and RES nodes in a conservative, original-source-preserving and correctly typed replacement refutation. No minimum proof-search charge is included.

**Proof.** Replace **each of the $t$ old gate-output names**, not just externally listed ports, by a separately reconstructed three-original-input function. The complete 256-function classification provides a circuit with at most four separately paid two-input DEF gates per old name; if the function is an old input or constant, charge one identity/constant gate to retain a legally fresh named output. Use globally fresh private intermediates and old output names only as new final gate names, so no names clash. This uses at most $4t$ new paid gates. Every old gate output has the identical function of the original $S$ on every input, and all conservative extensions preserve original models.

For an original defining clause $C$, let $c\le3$ be its distinct variables. Its involved old gate names have replacement cones using at most $4c$ new variables in total. Including all three original inputs, the replacement facet CNF $\Gamma_C$ uses at most $k\le3+4c$ variables. It entails $C$ because the entire old named output vector is unchanged. Therefore $k-c\le3+3c\le12$. Apply the strict target-clause implicate construction from LSPV-2/403: falsify the literals of $C$, branch on the remaining $k-c$ variables, select a falsified defining facet at each full leaf, and combine/prune by strict binary Resolution. This derives a subclause $C'\subseteq C$ with at most $2^{k-c}-1\le4095$ paid RES inferences. No weakening or semantic oracle is used. There are at most four facets per old gate, so the total reconstruction charge is at most $4t(4095)$.

Replay the old downstream Resolution proof with these stronger antecedents. If both complementary pivots survive, one resolution yields a subclause of the old resolvent; if a pivot disappears, retain the parent lacking it, already a subclause of the old resolvent. An old empty conclusion remains empty. Sharing may reduce counts. In total,

$$
q_{\mathrm{new}}\le4t+4t(2^{12}-1)+r=\boxed{16384t+r}.
$$

This is an upper bound **in the declared fragment**, not a lower bound on the complete mixed calculus or arbitrary-machine work. QED.

## ITERATE: nested affine test, tests and correction

Original three paid gate network: $p_4=x_1\oplus x_2$, $p_5=p_4\oplus x_3$, $p_6=\neg(p_4\oplus p_5)$. Construct a replacement with four independently charged DEF gates: $p_4=x_1\oplus x_2$, $z_7=x_1\oplus x_2$, $p_5=z_7\oplus x_3$, $p_6=\neg x_3$ (the last is a valid two-input gate with both inputs $x_3$). Both compute the same vector $(p_4,p_5,p_6)$ on all eight original assignments, but the replacement has different internal wiring.

Replacement gates expose **14** non-tautological defining clauses; old gates have **12**. A constructive strict Resolution tree generated 56 paid RES nodes: 0 for each of four old $p_4$ facets already present, then exactly **7 each** for the other eight facets. Maximum branch-variable deficit was four, where the verified per-facet upper bound is 15. All intermediate pivots and parent IDs were independently replayed. Full detailed 16,141-byte JSON DAG SHA-256: 97caa363e6366c9933605fb0dc01177f5db1e49f41da309b982f9abd9911cf5c. The separately implemented Python verifier checked all clauses and rejected six different corrupted traces; original SAT $(x_1)\land(x_1\lor x_2)$ has four models on the three-variable universe and UNSAT $(x_1)\land(\neg x_1)$ has zero. This is **COMPUTATIONAL**, not a claim of optimality for 56 nodes.

The evidence refined the mechanism: semantic equality of the three exported gate values alone does **not** license copying downstream faceted RES steps. The repaired compiler explicitly rederives old facets. The test has XOR functions but makes no claim that native GF(2) rule can consume separately paid DEF equations. Exact native grammar remains unsettled.

## Full physical-cost and independent-hardness firewall

Paid-node cost is distinct from physical execution. A literal translation must acquire and parse the original $N$-bit CNF and the entire $E$-bit explicit proof, validate all original source references, gate function tables and globally fresh IDs; evaluate each old gate on eight source assignments, retrieve or compute fixed synthesis templates, materialize all replacement gates and strict RES clauses, check every parent/pivot and support, manage DAG storage/access/recomputation, serialize full output and check it. Physical time and peak memory are polynomial in **$N+E$** for the declared explicit fragment, but **not** bounded by paid node count alone if uncharged LOCAL payload bits are unbounded. One deliberately loose upper bound for full buffering and rescanning is bit time $O((N+E+q_{\mathrm{new}}+2)^4)$ and simultaneous writable space $O((N+E+q_{\mathrm{new}}+2)^3)$; no native TM or host-RSS measurement is asserted. The optimizer's discovery cost is separate. The all-phase FLMV $\rho$ restriction remains untouched.

Haken's 1985 published exponential lower bound quantifies over **all ordinary shared-DAG Resolution** proofs of the standard unary $\mathrm{PHP}_{h+1}^{h}$ with $h(h+1)$ variables, $(h+1)+h\binom{h+1}{2}$ clauses and $N=\Theta(h^3\log h)$ signed-index bits: proof size $2^{\Omega(h)}$. Cook's 1976 Extended Resolution polynomial PHP proofs and exact mixed /341 affine odd-cubic-Tseitin cost $4h-1$ prevent treating this as a lower bound on R_mix341 or on all uniform SAT algorithms. Raz-Tzameret's Res(lin) is a distinct line language. Efficient parity proof logging in Gocht-Nordstrom is a format/compiler result, not a hardness theorem.

The weakest same-preselected-R B3 transfer is still

$$
\mathrm{SAT}\in P\implies\exists C,k\ \forall N:\quad
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

A rejecting decider trace does not provide a source-authenticated proof of the decider's universal correctness. Cook-Reckhow supplies *some* polynomially bounded proof system when NP=coNP, not automatically this named R. Hence B1/B2/B3, full native polynomial normalization, superpolynomial mixed worst-case minimum and P versus NP remain **OPEN**.

## Reconciliation and next precise implication

The mathematical components are explicit improvements of LSPV-2/408 using prior LSPV-2/403 and LSPV-3/411, not rediscoveries. The full producer, independent verifier and detailed raw record are preserved as a reproducibility archive; the role-owned report and compact repo experiment/summary are separately published. Root main.tex currently returns a Git blob SHA but **zero decoded content** from authenticated reads; no blind overwrite was attempted.

Next: settle native byte-grammar selectors for defining facets, GF(2) DEF equation ports, AND3 annotations, and LOCAL public/private exports; extend this replay to *all* consumer kinds or exhibit a **legal** native counterexample. In parallel, attack same-R B3 by a noncircular proof compiler, not a semantic SAT-decider assertion.

### References

[1] Blair A. Seidler, Minimal Circuits for Boolean Functions of Few Variables (2022), https://sites.math.rutgers.edu/~bas312/Research/slp/SLP.pdf, p.14 Table 4.
[2] A. Haken, The Intractability of Resolution, TCS 39 (1985) 297-308.
[3] S. A. Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4) (1976) 28-32.
[4] S. A. Cook and R. A. Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979) 36-50, https://doi.org/10.2307/2273702.
[5] R. Raz and I. Tzameret, Resolution over Linear Equations and Multilinear Proofs, APAL 155 (2008) 194-224.
[6] S. Gocht and J. Nordstrom, Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs, AAAI 2021, https://doi.org/10.1609/aaai.v35i5.16494.
