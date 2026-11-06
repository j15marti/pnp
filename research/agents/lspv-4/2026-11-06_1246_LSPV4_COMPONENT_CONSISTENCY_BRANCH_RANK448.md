# LSPV-4/448: Exact cofactor SAT/UP rank on original cubic Tseitin 3-CNF

**2026-11-06 12:46 PST | Route A primary | KNOWN graph algebra + PROVED/RESTRICTED new project corollary + COMPUTATIONAL controls | P versus NP OPEN**

## IDEA, prespecified falsifiers, review

**Hypothesis:** UP-open cofactor branches in the /447 cubic Tseitin edge-deletion model do not necessarily remain satisfiable; the gap is governed by the number of cyclic residual components. Falsifiers: (1) tree-row rank fails with a cyclic component; (2) all-component rank is not $c-1$ because of internal selected edges; (3) an even-charge parent has no UP-open-but-UNSAT branches; (4) actual signed source-clause UP differs from graph parity. Falsifier (3) is **TRUE**, as demonstrated below; (1)-(2) are disproved mathematically, and (4) rejected by independent original-clause tests. This builds on project LSPV-2/422, /450 and LSPV-4/447 rather than claiming novelty for GF(2) incidence rank.

## Family/theorem/encoding/known-method ledger

Let $G=(V,E)$ be any connected simple cubic graph, $H=|V|$, $M=3H/2$ original edge variables. For charge $\chi_v$, and incident ordered edge IDs $a<b<c$, the original four proper signed ternary clauses at vertex $v$ are
$$
C_{v,p,q}=\ell_p(x_a)\lor\ell_q(x_b)\lor\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),
\quad p,q\in\{0,1\},\quad \ell_0(x)=x,\ \ell_1(x)=\neg x.
$$
They encode $x_a\oplus x_b\oplus x_c=\chi_v$, use $4H$ clauses and $12H$ literal occurrences, and have $N=\Theta(H\log H)$ fixed-width original-ID bits. Global SAT iff $\bigoplus_v\chi_v=0$.

**KNOWN hardness, restricted model only:** for growing constant-expansion cubic graphs with odd charges, Urquhart 1987 (DOI 10.1145/7531.8928) establishes exponential **ordinary shared-DAG Resolution** length; Ben-Sasson/Wigderson 2001 (DOI 10.1145/375827.375835) provides the width-to-size route. These are not arbitrary-algorithm, ER, Res(XOR), or full historical $R_{\mathrm{mix341}}$ hardness statements. A source-authenticated global GF(2) parity check is a valid efficient shortcut. The finite bridged control below is not an expander-hard sequence. No conversion from non-3-CNF is involved.

## Theorem 448.1 (PROVED/RESTRICTED)

Fix any $S\subseteq E$ of $k\le H/2$ original edge variables and all $2^k$ assignments $\alpha$. Suppose $G-S$ has $r$ tree components and $b$ cyclic components; $b\ge1$. Let $c=r+b$. Then
$$
\#\{\alpha:\operatorname{UPopen}(F|_\alpha)\}=2^{k-r},
$$
where UP is **ordinary original signed-clause unit propagation**. The number of genuinely SAT cofactors is
$$
\boxed{\#\{\alpha:\operatorname{SAT}(F|_\alpha)\}=
\begin{cases}2^{k-r-b+1}, & \bigoplus_v\chi_v=0,\\
0, & \bigoplus_v\chi_v=1.
\end{cases}}
$$
For even charge, precisely fraction $2^{1-b}$ of UP-open branches are truly SAT; for odd charge *all* UP-open branches are UNSAT. For even charge, open-UNSAT count is $2^{k-r}-2^{k-r-b+1}$. A satisfiable branch has exactly $2^{M-k-H+c}$ full extensions, reproducing global total $2^{M-H+1}$.

**Proof.** The residual graph has $M-k\ge H$ unassigned edges, hence at least one cyclic component. Summing vertex equations within any residual component $C$ gives one boundary parity condition:
$$
\bigoplus_{e\in S\cap\delta_G(C)}\alpha_e=\bigoplus_{v\in C}\chi_v.\tag{448A}
$$
Every remaining tree edge is uniquely assigned by leaf elimination and UP detects contradiction exactly when its component's (448A) fails; a cyclic component retains a nonempty 2-core without a unit or empty parity clause. The $r$ tree-component equations are linearly independent because at least one cyclic component exists, yielding $2^{k-r}$ UP-open branches (the earlier /447 theorem). For full SAT all $c$ component equations must hold. Contract residual components. Every selected edge crossing components gives a binary incidence column, and every selected edge internal to a component gives a zero column. The contracted graph is connected, and its incidence matrix has rank $c-1$, with the single all-row XOR dependence. The RHS overall XOR equals $\bigoplus_v\chi_v$. Therefore odd charge is inconsistent and even charge gives $2^{k-(c-1)}$ solutions. QED.

## Hostile exact witness

Subdivide one edge in each of two disjoint K4 copies and join their new subdivision vertices by a single bridge. This connected simple cubic graph has $H=10$, $M=15$. Select only the bridge ($k=1$). Deleting it leaves $r=0$ tree and $b=2$ cyclic components. Both assignments are UP-open. With all charges zero, exactly one is SAT and one remains UP-open but UNSAT. With one odd charge, both remain UP-open and both UNSAT. This example deliberately tests the scope; it is **not** a certified growing Resolution-hard expander.

## Exact independent computation

Full source and raw reproducibility archive: \`LSPV4_448_COMPONENT_COFAC_SAT_UP_REPRO.zip\` (separate attached artifact). Python directly generates 4 signed ternary clauses at each vertex, applies literal-wise CNF UP, and independently evaluates component parity. Node.js independently reconstructs clauses by **forbidden local truth triples**, executes original-CNF UP, and performs GF(2) elimination of the entire remaining incidence matrix. The two independently implemented programs agree on **41,216 cofactor evaluations** for all $S$ with $k\le\min(3,H/2)$ over K4, cube, Petersen and bridged K4-pair, four source charge patterns per graph. Python additionally performs **476** direct complete-assignment SAT checks and records **159,080** logical assertions. Exact generated-source multiset controls: **32** accepted canonical/permuted packets; **48** rejected sign-corrupt/duplicate/out-of-range packets. All tests PASS. Initial attempted $k=3$ on K4 failed the declared $k\le H/2$ guard and was corrected before final results. The tests do not measure FLMV indexed-machine time/space and are not asymptotic hardness certificates.

## Resource and transfer ledger

**Input/acquisition:** source graph and charges are supplied in controls, not inferred from arbitrary unannotated CNF. **Parsing/authentication:** host multiset checks use large memory and are not asserted to meet $N^{1/2}$ space; malformed general CNF remains outside the constructed port. **Search/policy:** all small edge sets enumerated in validation, not charged as a proposed universal compiler. **Bit evidence and source reads:** raw source clauses and runtime are in archive, not converted into FLMV TM traces. **Children:** no guest A executed, no universal smaller ordinary CNF produced; full serialization and virtual port cannot be interchanged for free. **Sharing:** the exact $c$-component boundary syndrome is information necessary for this graphical join, but computing, storing, verifying and rereading it are chargeable. **All-phase peak:** program adjacency/clauses/maps are resident in Python/Node; no FLMV work/space claim. **Proof DAG:** no native $R_{\mathrm{mix341}}$ rules or weights changed; all AND cases and contexts remain required. The minimum over legal shared DAGs may freely select this source-authenticated shortcut when simulated legally in the historical rules.

The FLMV conditional profile arithmetic is unchanged: $\beta(6/5)=23/45$ and strict gap $\beta(6/5)-1/2=1/90$. The **OPEN** missing transformation still requires, for **every** total correct polynomial-time SAT decider on all binary CNF/malformed inputs, same indexed-machine, recursively iterable, two-label correctness and all cost phases:
$$
t'\le\max(11/10,3/5+t/2),\qquad s'\le\max(1/2,s/2).
$$
Also retain $s'\le\max(\rho,\eta,\lambda,\lambda s)$ for materialized children with $\rho$ including all allocate-then-free local phases.

## Audited sources and continuity

Project: issue #3; \`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md\` SHA c3889a3e; \`AGENTS.md\`, \`CODEX.md\` SHA 754999f5 and \`.codex/skills/pnp-research/SKILL.md\` SHA b8df83a7; LSPV-4/447 SHA 0a5189b6; LSPV-2/450 SHA cb51b0a8, /451 SHA 88c54d1f; Grok \`GROKPROOF/2026-11-06_1617_PROGRESS.md\` SHA b931933c; Claude \`research/agents/claude/tport/README.md\` SHA d1290822 and \`onetape/README.md\` SHA 6255025f. New required repository texts actually inspected: \`konard/p-vs-np/scripts/proof_status.json\` SHA 93b77ed3 and \`P_NOT_EQUAL_NP_SOLUTION_STRATEGIES.md\` SHA 345c1743; \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` SHA 18d693ea and \`INDEPENDENT_AUDIT.md\` SHA b30515cc. Also inspected FRAT-XOR and CNFgen repository sources and original Urquhart, Ben-Sasson/Wigderson, FLMV and de Colnet/Mengel regular-Resolution literature. No separate Google-branded search, no native FLMV TM execution, no third-party writes, no claimed P versus NP proof.

**Advance:** Exact SAT-versus-UP-open cofactor counts and focused adversarial witness. **Verification:** Independent finite host implementations PASS, mathematical proof restricted to fixed source model. **OPEN:** Full all-input SAT transformation, arbitrary-rule mixed-calculus lower bound, noncircular B3. **P versus NP OPEN.**