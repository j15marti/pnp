# LSPV-2/408: Three-input paid-DEF facet recovery

**2026-11-04 21:12 PST.** PROVED/EXACT only in an explicitly declared readable-DEF-clause and pure-RES-consumer fragment; COMPUTATIONAL independent finite certificates. Actual native R_mix341 exported-wire, DEF-to-GF(2), and LOCAL-CONVERT grammar; B1/B2/B3; superpolynomial full mixed minima; and P versus NP all remain OPEN. Original rules, weights, tasks, ownership and schedules unchanged.

## IDEA before search

Falsifiable hypothesis: LSPV-3/410's five-paid-gate reconstruction of a public Boolean output can be strengthened to preserve every old defining clause as an authenticated strict-Resolution *subclause*, enabling downstream RES consumers to be repaired. Challenges: output equivalence could fail, facets could cease to be entailed, lost RES pivots could break refutation, or native defining-facet selectors might be undefined. The last limitation persists.

## SEARCH / prior work

Read governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, issue #3, AGENTS.md, CODEX.md, repository skill, original R_mix341 research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11), original LOCAL addendum (bbcdad9a), LSPV-2/366 and /407, LSPV-3/408-410, LSPV-4/402, and REFEREE353. Actual Grok review GROKPROOF/2026-11-05_0515_PROGRESS.md (f348f7bb), and Claude TPORT-0002 (1f9fc727) and ONETAPE-0001 (9a5b05d6) were read. None supplies the native grammar or B3.

Web queries: "resolution proof subsumption strengthening pruning"; "Cook Reckhow relative efficiency propositional proof systems 1979"; "Haken intractability resolution pigeonhole principle 1985"; "Cook short proof pigeonhole extended resolution 1976"; "Raz Tzameret resolution over linear equations"; "Davis Putnam variable elimination resolution". Primary Cook-Reckhow journal description, Cook bibliography and Raz-Tzameret institute abstract were read. ECCC PDF URL returned metadata only. **Direct Google-branded search was unavailable; general search was used.** Authenticated github.com/openai searches "ExecCNFNodeSearchCosts", "CookLevin", "resolution proof checker", "LRAT", and "subsumption resolution" were executed. Full openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean was read (blob 1ced21f4); it is not a native proof compiler. Project /366 had already proved subclause erasure and /410 had already proved the five-gate public-output normal form; these constituent facts are reused, not claimed novel.

## ITERATE: exact restricted theorem

Fix any source CNF F, SAT or UNSAT, and an acyclic bank of t paid fresh binary Boolean DEF gates *all ultimately depending on the same three original variables* x1,x2,x3. **Explicit extra assumption:** every separately paid DEF exposes its at-most-four exact truth-table CNF facets as individually selectable RES premises with charged byte validation. The downstream r-node proof uses only original source clauses, such facets, and strict binary RES.

Each named original gate output p has a three-input function f. Evaluate it on all 8 inputs and use the five-paid-gate Shannon construction

$$
a=f(0,x_2,x_3),\quad b=f(1,x_2,x_3),\quad
d=a\oplus b,\quad e=x_1\land d,\quad p=a\oplus e.
$$

Do this for *every original output*, not just an exposed subset. The replacement is conservative and preserves every old named output under every source valuation. Each original defining clause C mentions at most three old/public names and is entailed by the defining CNFs for at most three replacement 5-gate cones. Together they involve at most 18 variables. Falsifying C and branching over the remaining variables produces a strict RES subclause D subseteq C from the new gate facets, with at most 2^18-1 paid RES steps, no weakening. Every old gate has at most four such facets. The already verified strict subclause-erasure compiler (LSPV-2/366) repairs each downstream RES node using at most one RES, inheriting a stronger parent if a pivot vanishes. An old empty-clause conclusion stays empty.

**Proved bound, conditional on the stated facet interface and consumer restriction:**

$$
q_{\rm new}\le 5t+4t(2^{18}-1)+r=(2^{20}+1)t+r.
$$

The construction is fully source-authenticated within this declared fragment, permits DAG sharing and arbitrary reconvergence, and is polynomial in explicit source plus proof-evidence bits. Gate count and bit time are distinct: parsing, pointer/index access, eight-row evaluation, branch construction, validation, output and peak memory all incur physical cost. Short consistent auxiliary alpha-renaming bounds output bit length by a polynomial in source and original explicit proof size; no universal N+q bound for arbitrary opaque payloads is asserted.

**Scope firewall:** Original /341 does NOT fix exact DEF-clause selectors or whether XOR-DEF exposes a GF(2) row or LOCAL exports internal wires. This result does not authorize those operations. RES subclauses are not necessarily valid typed inputs to GF(2), AND3 or LOCAL-CONVERT, so this does NOT prove a whole-native normalization or B3.

## Reproducibility and correction

For original p4=x1 XOR x2, p5=p4 XOR x3, replaced two gates by ten paid gates with 40 defining clauses. Independently derived all eight original gate facets by strict RES with node counts **[17,17,17,17,19,19,19,19]**. The displayed detailed facet proof has **40 existing paid-definition facet records plus 19 paid RES nodes**, with all eight original input assignments checked. SAT source (x1) has 4 models; UNSAT source (x1) AND (NOT x1) has none, both unchanged under conservative definitions. A nonentailed altered facet, malformed gates, forged defining facet and bad pivot were rejected. Python producer: **885 assertions**; independent Node.js verifier: **930 assertions**; detailed raw JSON: **13,650 bytes**. No random sampling.

A first negative-control clause (p4 OR x3 OR NOT p5) was accidentally a *valid* XOR facet. This mistake was detected; the corrected nonentailed clause (p4 OR x3 OR p5) was rejected. These are conditional finite tests, not evidence of asymptotic hardness.

## Hard-family controls and B3

Haken 1985: standard explicit unary PHP_(h+1,h) has h(h+1) variables, h+1+h*binom(h+1,2) clauses, length Theta(h^3 log h), and requires 2^{Omega(h)} lines for **every ordinary shared-DAG Resolution** refutation. It does not bound mixed R or arbitrary SAT algorithms. Cook 1976 gives polynomial Extended Resolution PHP proofs. Native R_mix341 has 4h-1 paid mixed proofs for odd bridgeless cubic Tseitin through AND3+GF(2). Raz-Tzameret 2008 is a different Res(lin) grammar. No restricted hardness is transferred to unrestricted computation. SAT in P does not by itself yield short R_mix341 proofs from a rejecting machine trace. B1, B2, B3 and P versus NP remain OPEN.

**Reconciliation:** root main.tex fetch returned a content SHA e1f21ec8 but zero bytes, so no unsafe replacement was attempted. Full LaTeX manuscript, executable producer, independently written verifier and complete proof-DAG raw record are preserved in the run's local reproducibility archive. This GitHub report is the role-owned substantive publication; the complete local files remain available separately until exact source-byte publication is possible.
