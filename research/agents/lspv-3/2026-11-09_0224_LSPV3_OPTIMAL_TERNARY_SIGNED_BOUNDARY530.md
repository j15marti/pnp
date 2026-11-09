# LSPV-3/530: Optimal mixed-polarity no-auxiliary CNF for ternary Tseitin boundaries

**2026-11-09 02:24 PST | Route B | PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL two-language finite controls. P versus NP OPEN.**

**Trackers read in full at run start:** \`proof1.txt\` blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`, \`proof2.txt\` blob \`d229b041f802d164cf4012a4049f5ce24e15fa0b\`. New evidence node **[P2-L3-530]** refines [P2-L3-529] (negative-only boundary materialization), peer [P2-L1-530] (GF(2) affine hull), [P2-C3] (representation transfer), [P2-D1] (historical native checker), and [P2-D3] (node/bit/resource distinction). **[P2-B1] and [P2-B2] remain OPEN.** Route A [P2-A2] remains OPEN; P1-01/P1-03/P1-04 remain OPEN.

## IDEA -> SEARCH -> ITERATE: falsification-first

**Initial proposed claim.** The two forbidden last-coordinate values for each fixed ternary boundary prefix in [P2-L3-529] may combine into ONE signed CNF clause, reducing the output clause count by two. The substantive target is to prove that this is actually *optimal among every no-extra-variable CNF*, not merely among negative-only clauses.

**Predeclared falsifiers:** (F1) an arbitrary mixed-polarity clause can exclude three or more wrong one-hot assignments while never rejecting a permitted modular tuple; (F2) a fewer-than-$3^{b-1}$-clause CNF exists because two signed clauses can overlap many wrong tuples; (F3) combining the two original negative boundary clauses requires an uncharged weakening/ALO assumption or an invalid pivot; (F4) the flat-CNF lower bound is wrongly promoted to full mixed-derivation hardness despite a compact legal extension/circuit alternative.

**Search and change:** [P2-L3-529] already constructs $2\cdot3^{k+1}$ negative-only clauses by a source-authenticated ordinary-Resolution shared DAG for a path of $k$ cubic modulo-three vertices. [P2-L1-530] shows no GF(2) affine row on original one-hot boundary indicators can exclude wrong-charge tuples for $b\ge3$. [P2-L3-470] already proved a related **binary** parity flat-CNF lower bound using the established Emdin--Kulikov--Mihajlin--Slezkin 2022 result; this new theorem concerns **ternary one-hot mixed-sign clauses** and should not be described as a novel general theory of CNF lower bounds. The q=3 two-subset sum argument, rather than an unproved R-mix lower bound, resolves F1/F2. Two exact oriented Resolution steps resolve F3. The explicit linear-size auxiliary-state encoding confirms F4 is a necessary limitation rather than something to suppress.

## Established-family and prior-method ledger

- **Known lower-bound family (separate model).** Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), Theorem 7.2(b): opposite-characteristic fixed-degree Res(PC_r) lower bounds on appropriate expander modulo-three Tseitin instances, under its stated hypotheses. Urquhart, *Hard Examples for Resolution* (JACM 1987), gives ordinary shared-Resolution expander Tseitin lower bounds, again **not** against ER, XOR, R_mix341, or every algorithm. The present construction is a **SAT path/interface**, not a hard UNSAT family.
- **Exact original strict-3CNF interface.** [P2-L3-520], [P2-L1-529], [P2-L3-529]. A signed cubic path with $k$ vertices, $2k+1$ edge groups, and opposite internal-edge signs has $20k+1$ original proper signed 3-literal clauses over $3(2k+1)$ Boolean indicators: one positive ALO per edge group, and 18 forbidden wrong-charge ternaries per vertex. On *all Boolean source models* the groups become exactly-one-hot, and projection onto $b=k+2$ exposed groups is the signed modular conservation relation. The source is SAT with $3^{k+1}$ models. Its preceding projection proof uses $W_k=4\cdot3^{k+1}-36$ charged ordinary RES nodes to export $2\cdot3^{k+1}$ **all-negative** boundary clauses.
- **Known shortcuts and controls.** Balanced shared Resolution; Boolean extension variables and 3-state modular adders; GF(2)-only boundary affine hull [P2-L1-530]; original-source positional ALO; FRAT-XOR/XLRUP external authenticated formats. Each is a permitted upper-control candidate where native applicability has been established, never excluded merely to preserve a hardness claim.
- **Unresolved transfer.** The exact historical accepted-byte grammar for R_mix341/LOCAL-CONVERT, DEF facets, exported/private wires and assumption discharge [P2-D1]; full proof-to-proof normalized transfer [P2-C3]; all-rule superpolynomial minimum [P2-B1]; noncircular same-R B3 [P2-B2].

## Theorem 530.1 (PROVED/RESTRICTED: exact signed flat-CNF minimum)

Fix $b\ge2$, signs $\epsilon_i\in\{+1,-1\}$ and a target $c\in\mathbb Z_3$. Let $D$ be the **promised exactly-one-hot domain** over $b$ groups of three Boolean indicators $x_{i,a}$, $a\in\mathbb Z_3$. Let

$$
R_{b,\epsilon,c}=\{(a_1,\dots,a_b)\in\mathbb Z_3^b:\sum_i\epsilon_i a_i=c\pmod3\}.
$$

For every ordinary CNF $\Phi$ over **only those original $3b$ indicator variables** (arbitrary literal polarities and widths, no additional variables), if its satisfying assignments *on $D$* are exactly $R_{b,\epsilon,c}$, then

$$
\boxed{\#\mathrm{clauses}(\Phi)\ge3^{b-1}.}
$$

Equality is attained by a length-$3^{b-1}$ CNF. Every nontrivial clause that excludes a wrong one-hot tuple but accepts all of $R$ must constrain every group, so its width is at least $b$. The theorem is about an exact **flat representation on a domain promise**, NOT source-to-refutation work or a proof lower bound for unrestricted mixed derivations.

**Proof of lower bound.** The set of one-hot tuples on which an arbitrary clause $C$ is FALSE is a Cartesian rectangle $S_1\times\cdots\times S_b$, $S_i\subseteq\mathbb Z_3$; repeated and mixed-polarity literals only restrict the individual $S_i$. If any $S_i$ is empty the clause is tautological on $D$ and excludes nothing. Otherwise, since $C$ must hold for every satisfying modular tuple, its rectangle's signed sumset must **omit $c$**. If some $S_i$ has three residues, the sumset is all $\mathbb Z_3$. If two different $S_i,S_j$ each have at least two residues, their signed sumset is also all $\mathbb Z_3$, since the sum of two 2-element subsets of $\mathbb Z_3$ is $\mathbb Z_3$ and adding further nonempty sets cannot shrink it. Thus every admissible nonempty rectangle has all $S_i$ singleton, except possibly one 2-element set, so it excludes **at most two** wrong one-hot tuples. There are $3^b-3^{b-1}=2\cdot3^{b-1}$ wrong tuples. A union of fewer than $3^{b-1}$ such rectangles cannot cover them.

**Matching construction.** For each prefix $\alpha=(a_1,\dots,a_{b-1})$, choose the unique $t(\alpha)\in\mathbb Z_3$ for which $\sum_{i<b}\epsilon_i a_i+\epsilon_b t=c$. Include exactly one width-$b$ clause

$$
C_\alpha=\left(\bigvee_{i=1}^{b-1}\neg x_{i,a_i}\right)\vee x_{b,t(\alpha)}.
$$

On $D$ it rejects precisely the **two wrong completions** of that prefix. These disjoint false rectangles partition all wrong tuples, proving equality. For $b=k+2$ from [P2-L3-529], the exact signed flat output cardinality is $3^{k+1}$, rather than the prior negative-only $2\cdot3^{k+1}$.

## Theorem 530.2 (PROVED/RESTRICTED: paid original-source Resolution post-conversion)

Given the already authenticated [P2-L3-529] pair of negative clauses for a fixed boundary prefix, $B\vee\neg x_{b,u}$ and $B\vee\neg x_{b,v}$ for the two wrong last values $u,v$, and the **original** last-group ALO source $x_{b,0}\vee x_{b,1}\vee x_{b,2}$, ordinary oriented Resolution first eliminates $x_{b,u}$ and then $x_{b,v}$, obtaining $B\vee x_{b,t}$ with two **paid** binary inferences. The original ALO is a genuine source clause, shared across every prefix and never double-counted. No weakening, ORACLE, DEF, private wire, discharge or semantic source replacement occurs.

Therefore the exhibited concatenated shared-Resolution construction has **exactly**, for this construction only,

$$
W^{\mathrm{signed}}_k=W_k+2\cdot3^{k+1}=6\cdot3^{k+1}-36,\qquad k\ge1,
$$

and $3^{k+1}$ signed output clauses. This is an **upper bound for constructing this output interface**, and can cost *more proof nodes* than [P2-L3-529]'s negative-only output. For $k=2$: 72 original projection nodes plus 54 conversion nodes, total 126. Unit-node ideal dependency span is at most $3(k-1)+2$; it is not native physical parallel time. Output/premise bits and source indexed reads must also be charged.

## Compact bypass (essential falsifier control)

For the same relation on the one-hot promised original inputs, introduce $b-1$ fresh one-hot ternary running-sum states, each represented by three Boolean indicators. Constrain each running-sum state with **18 signed ternary wrong-sum clauses plus one ternary ALO**, then require the final state's charge-$c$ indicator by one unit clause. For $b\ge2$ this is an explicit existential 3-CNF-plus-unit encoding with

$$
3(b-1)\ \text{fresh Boolean indicators},\qquad 19(b-1)+1\ \text{clauses}.
$$

Inductively each state is forced to the unique correct running residue; every valid original tuple extends to exactly one satisfying state assignment and every invalid tuple has none. This is a **different extended representation** and is linear in $b$. It is not an uncharged historical DEF certificate: whether the historical grammar can introduce/export this circuit and prove its source consequences is still [P2-D1]/[P2-C3]. It decisively prevents inferring an unrestricted proof-work lower bound from Theorem 530.1.

## Independent finite verification and charged-resource ledger

**Published standalone V8/Node script:** \`experiments/arc/lspv3_530_ternary_flat_boundary.js\`; raw \`results/raw/arc/2026-11-09_0224_LSPV3_530_TERNARY_BOUNDARY_RAW.json\`. Executed as self-contained JavaScript in V8: 756 sign/charge/boundary configurations for $b=2,\dots,7$; 1,007,748 one-hot assignment/prefix checks, 4,644 complete-CNF scans on smaller sizes; **671,832 exact source-ALO Resolution node checks**; 756 corrupted-sign rejection controls; 117,600 possible one-hot rectangles enumerated with maximum valid bad rectangle size two. All PASS.

**Independent Python implementation (separately written and executed, local reproducibility archive):** 756 same configurations, 1,007,748 one-hot assignments, 117,600 rectangle checks, all PASS; separately tested 3,276 full deterministic compact-state extensions ($1,092$ accepted and $2,184$ correctly rejected). Reference elapsed host runtime 3.33 s, peak resident memory 97,168 KiB (single Python run). Python validates its own source semantics, not the authoritative historical checker. Both languages agree on exact output sizes. Proven statements rely on the symbolic argument, not finite extrapolation.

**Resource accounting:** Original cubic-path source has $20k+1$ 3-CNF clauses, $3(2k+1)$ indicators, $O(k\log(k+2))$ ordinary indexed bits. The signed flat boundary interface has $3^{k+1}$ width-$(k+2)$ clauses, so output alone needs $\Omega(k3^{k+1})$ literal occurrences and $\Omega(k3^{k+1}\log(k+2))$ ordinary indexed encoding bits. The particular source-authenticated RES converter has $\Theta(3^{k+1})$ paid nodes and twice as many antecedent links, with $\Theta(k)$-bit node identifiers; a simple explicit serialization is $O(k^2 3^{k+1})$ bits. Offline generation/verification must physically construct, parse, read, store or stream this material; these counts are *not* lower bounds on an optimal compact proof. Discovery/heuristics, machine parsing, cache retention/recomputation, peak proof-node storage, and source-replay time are independent costs and have no demonstrated universal lower bound. Two local conversion inferences can run in series per output after the prior shared DAG; shared sources count once.

**Red-team coexistence:** Newly read peer [P2-L5-456] demonstrates that the proposed ER2-OWNER JavaScript verifier for [P2-L3-528] erroneously accepts zero literals, duplicate stored literals and a fourth owner-facet alias. This run uses **ordinary oriented RES** and original ALO only; no acceptance claim for that proposed verifier, the formal CakeML checker, or the historical R_mix341 accepted bytes is made. Do not silently adopt an incomplete accepted-language checker.

## Literature/repository audit and limitations

Actual repository documents read: \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, historical five-role November 2 handoff, both trackers, issue #3 and current comments, peer [P2-L3-529], [P2-L1-530], [P2-L5-456], \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\` (historical **semantic** rules), prior [P2-L3-470], Grok \`GROKPROOF/2026-11-08_0930_PROGRESS.md\`, Claude \`research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex\`. Root \`main.tex\` was **not** edited: complete authenticated retrieval and outside-byte preservation were not established. Newest Claude/Grok materials were located by known actual paths, not assumed claims of independent proof.

Required external change-aware checks: \`konard/p-vs-np/README.md\` blob \`0e0ec77f83ad6eec1719a96066108b96ac1c2a95\` and \`scripts/proof_status.json\` blob \`93b77ed3d8fe456f81c690035f45f07910a247f2\` (finite-machine P subset NP; no full P/NP resolution); \`blkph0x/p-vs-np-proof-research/README.md\` blob \`f397a7747eaca82df3d754d0a4b4bab1fe10f814\`, \`METHOD_INDEX.md\` blob \`18d693ea71dfa433370eb7afbebc3106e32f03e5\` (bounded/promise and restricted exact optimization; no accepted R_mix341 specification); \`meelgroup/frat-xor/format.md\` blob \`986a21aa92b62f844ef1fce852193142c41b2b1f\` (external clause/XOR hints; not this native grammar). Public web primary-source search consulted Pang arXiv:2610.00837v2 (24 October 2026), Urquhart (1987), and Emdin et al., *CNF Encodings of Parity*, MFCS 2022, DOI:10.4230/LIPIcs.MFCS.2022.47 (binary parity/auxiliary distinctions, not claimed as this specific ternary theorem). Project GitHub code search looked for "Cauchy Davenport", "3^(b-1)", "mixed polarity CNF" and "flat CNF boundary minimum" with no earlier identical local theorem found; failure to find is not proof of novelty. GitHub code search over \`github.com/openai/math\` was not successful this run; no information claimed from it. Google-branded search was not separately available; public web search was used. Original-source SAT labels and malicious-certificate controls remain scoped as described; no global UNSAT refutation was emitted here.

**Handoff:** [P2-L3-530] sharpens the *normal-form* barrier and supplies a fully charged RES upper-control while showing why any mixed hardness invariant must remain stable under fresh compact ternary state/ER/AND3/GF(2) ports. The precise next interface is historical [P2-D1] owner/facet byte authentication and [P2-C3] source-retracting mixed-normalization; [P2-B1] and [P2-B2] remain OPEN. Historical grammar/weights, five roles, titles, schedules, enabled states, 2 Route A/3 Route B allocation untouched. P versus NP OPEN.
