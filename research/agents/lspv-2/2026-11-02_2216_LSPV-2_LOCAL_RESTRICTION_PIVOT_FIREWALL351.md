# LOCAL-RESTRICTION-PIVOT-FIREWALL351

**PNP SAT-Circuit Reduction Builder / LSPV-2. November 2, 2026, 22:16 PST.**

**PROVED/EXACT** primitive restriction identities and growing-width assigned-RES-pivot counterfamily. **COMPUTATIONAL** independent exhaustive 3-variable check. **CONDITIONAL** nondegenerate typed-DAG specialization. **OPEN** full mixed restriction, the source compiler, B1/B2/B3, superpolynomial worst-case minimum, and P versus NP.

## Fixed model and exact target

Keep the preselected source-independent-VARDEF unit-cost binary-premise system Rmix341 unchanged: original named CNF clauses are free; RES, exact AND3 (combined support at most three original variables), GF(2) binary row addition, charged LOCAL-CONVERT and charged conservative local two-input VARDEF are the available derived operations. Shared DAG nodes cost once. This report **does not add weakening, constant-input DEF, zero-cost type aliases, or a semantic oracle**. Let $q(\pi)$ be the number of distinct paid inference nodes in a legal source-authenticated refutation DAG. Free hindsight-optimal selection is separate from proof-search machine work.

For a Boolean function $f$ and a partial assignment $\rho$, $f|_\rho$ is its substituted truth function. A GF(2) equation is represented by coefficient mask $a$ and right-hand side $b$.

## Theorem A: operator-level restriction closure, all variable counts

For every Boolean $f,g$, every partial assignment $\rho$, and every local sound implication $f\Rightarrow g$:

$$
(f\land g)|_\rho=(f|_\rho)\land(g|_\rho),\qquad
\operatorname{supp}(f|_\rho)\subseteq\operatorname{supp}(f)\setminus\operatorname{dom}\rho,
$$

$$
f\Rightarrow g\quad\Longrightarrow\quad f|_\rho\Rightarrow g|_\rho.
$$

Thus AND3 preserves its combined-support-at-most-three admissibility after substitution; constant-support implication checks remain sound; exact local affine annotations remain affine.

For the affine equation $E(a,b)=[\bigoplus_i a_i x_i=b]$, when $\rho$ fixes the set $D$ to values $s_i$, let $a'$ be $a$ with coordinates in $D$ cleared and $b'=b\oplus\bigoplus_{i\in D}a_i s_i$. Then

$$
E(a,b)|_\rho=E(a',b')
$$

and **GF(2) equation addition** commutes with restriction:

$$
(E(a,b)\oplus E(c,d))|_\rho
=(E(a,b)|_\rho)\oplus(E(c,d)|_\rho).
$$

The XOR shown here is addition of **equations**, not pointwise XOR of their satisfying predicates.

**Proof.** Evaluate either Boolean expression on any total extension of $\rho$; conjunction and implication commute with evaluation, and a formerly inessential coordinate cannot become essential after fixing coordinates. The equation substitution changes its RHS by exactly the parity of fixed nonzero-coefficient inputs. XORing substituted masks and RHS values agrees with substituting their XOR. All checks are local and explicit. These are operator identities, not a theorem that all typed proof DAGs are closed under restriction.

## Theorem B: exact resolution pivot firewall

For a valid RES step $(p\vee A),(\neg p\vee B)\Rightarrow A\vee B$, fixing variables **other than** $p$ reproduces exactly the same RES pivot when the restricted resolvent is nontrivial. However if $p$ itself is pinned, the conclusion need not be a legal same-step derivation.

For **every** $r\ge3$, take fresh distinct $z,a,b_1,\ldots,b_r$:

$$
(z\vee a),\quad(\neg z\vee b_1\vee\cdots\vee b_r)
\quad\overset{\operatorname{RES}(z)}\Longrightarrow\quad
(a\vee b_1\vee\cdots\vee b_r).
$$

At the restriction $z=0$, the parents become $a$ and $\top$, whereas the derived conclusion remains $a\vee b_1\vee\cdots\vee b_r$. It is a strict *weakening* of $a$ (set $a=0,b_1=1$ to distinguish them). Its support $r+1>3$ rules out a direct constant-three-variable LOCAL-CONVERT justification under the specified local checker. The complementarily signed $z$ pivot no longer occurs in two active parents, so copying the original RES step is illegal.

**Scope:** This refutes the **naive direct-line/zero-cost-alias transport**, not the standard subsumption-aware restriction theorem for pure Resolution; it does **not** disprove existence of an alternative mixed-DAG translation, a worst-case lower bound or B3. To use a stronger surviving premise later under GF(2), CONVERT, AND3 or DEF requires a separately verified typed rederivation, not a free weakening.

## Lemma C: 16-gate, 9-restriction semantic table

Across all 16 total two-input Boolean functions and all nine partial input-fixing patterns, there are 144 gate/pattern pairs: 16 unpinned binary cases, 32 pinned nonconstant unary cases, and **96 pinned constant cases**. This is a complete exact count: for each of four one-pin choices, eight of the sixteen gates restrict to a constant and eight to nonconstant unary; all four two-pin choices yield a constant. **Semantic closure does not imply syntactic admissibility** of a constant gate, repeated input, unary slot or zero-argument definition under unchanged Rmix341. The VARDEF checker must explicitly settle such cases, with every retained gate still charged.

## Conditional proof-DAG corollary, not full RT

If after a particular restriction (i) every retained RES node has an unassigned pivot and a legal, nontrivial typed conclusion, (ii) all local Boolean, affine and conversion nodes retain permitted type and parent relations, without an uncharged alias, (iii) every retained source is authenticated from the specialized source CNF, and (iv) all active DEF slots remain legal conservative charged gates under the **same** rule grammar, then copying the retained nodes in topological order gives a valid DAG with at most $q(\pi)$ paid nodes. These are explicit restrictions on the proof and substitution, not a universal statement over all mixed proofs. Full RT in LSPV-1's universal-soundness construction is still OPEN, as is separate authenticated source compilation SC.

## Falsifiers

1. Support grows or GF(2) addition fails after pinning: **FALSIFIED/RETIRED**, by symbolic proof and exhaustive three-variable audit.
2. Every assigned-pivot RES step can be directly copied or made a free exact alias: **FALSIFIED/RETIRED**, by the unbounded $r$ counterfamily.
3. Gate restrictions never require constant outputs: **FALSIFIED/RETIRED**, 96/144 gate cases.
4. Primitive identities establish B3 or a machine execution lower bound: **FALSIFIED AS AN INFERENCE**; there is no universal mixed proof retyping, source compiler or arbitrary-decider correctness reflection.

## Independent finite replay and resource scope

A Python producer and separately written no-import Node verifier exhaustively check **1,769,472** three-variable AND commutations (256-by-256 input pairs, 27 partial assignments), **177,147** local implication restrictions, **6,912** essential-support monotonicity cases, **6,912** affine row-pair restrictions, and **144** complete gate restrictions. Python raw record SHA-256: 0a474615736fa93164303b76335abc67f6b92ea6ff0450f2d5a499c849cafd13. Node independent assertions **1,967,383 PASS**; odd/even K4 parity controls 0/8 models, an UNSAT unit contradiction and SAT binary control, six malformed DIMACS sources, and two illegal RES pivot controls all passed. Python runtime 0.37s/approximately 94MiB host RSS, Node 0.07s/approximately 33MiB RSS. These are executable measurements, not a machine-work lower bound. Full local files are included in the reproducibility archive. The **only exhaustive universe** is three-variable operators, not all mixed derivations or growing family minima. No result on $\overline W_R(N)$ beyond inherited finite cases is asserted.

## Current project state and source audit

Read the November 2, 12:04 PST five-role refocus at verified commit/blob 4e29ed7/033b54b; issue #3 through LSPV-5 REFEREE304 at 21:48 PST; AGENTS.md, CODEX.md, pnp-research skill; original Rmix341 rule definition; LSPV-2 GUARD-RES349 and GUARD-EXCESS-CAP350; LSPV-4 G342 SPLIT350; LSPV-1 UNIVERSAL-REFLECTION353, and LSPV-5 REFEREE304. The latest peer reports **exact finite** $W_{Rmix341}(\mathrm{rsmu\_5\_7\_1})=9$, replacing historical interval $[8,9]$. Peer verification used two SAT engines and a no-import auditor; checked independent LRAT/DRAT traces would be a further strengthening, not a new claimed proof here.

Primary literature: Cook and Reckhow (1979) on proof systems, Peitl and Szeider (2021) on shortest Resolution formulas, Szeider (2003/04) on bounded-deficiency tractability. Search on github.com/openai for Resolution proof-checker implementations returned generic logic material and irrelevant uses of "resolution"; no external proof checker adopted. The elementary Boolean/GF(2) identities are standard; the new project increment is the quantified typed-rule audit and concrete exposed guard-pivot obstruction, not a claimed academic originality for those identities. This is compatible with existing source-guard upper transports; it does not prove reverse hardness transport.

**Access/publication fallback:** The partial local workspace lacks the repository preflight executable. GitHub returned **zero bytes** for root main.tex while reporting a nonempty blob SHA (b85d881ba62eaad245c9c25a8138408bc31a2b65). No partial or empty root content was overwritten. Role-owned append-only report, code, raw record and five-role handoff are the documented fallback. Reconciling root main.tex within LSPV-2 markers must await full current blob readback, with all bytes outside markers preserved. No task identity, schedule or enabled state changed.

**NEXT:** construct and verify subsumption-aware **assigned-pivot** RES translations that preserve the types of downstream AND3/XOR/LOCAL-CONVERT/charged VARDEF nodes; separately prove RT, SC and weakest sufficient B3. P versus NP is OPEN.

## References

[1] S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, DOI 10.2307/2273702.
[2] T. Peitl and S. Szeider, *Finding the Hardest Formulas for Resolution*, JAIR 72 (2021), 69–97, DOI 10.1613/jair.1.12589.
[3] S. Szeider, *Minimal Unsatisfiable Formulas with Bounded Clause-Variable Difference Are Fixed-Parameter Tractable*, COCOON (2003), 548–558.


## Final root reconciliation (subsequent verified recovery)

The initial plain-content root main.tex read returned zero bytes with a nonempty SHA. **An authenticated Git-blob fetch by current blob SHA subsequently returned the complete 1,355,231-character root.** This enabled a safe ownership-only insertion. Final complete root readback matched **every byte** of the intended 1,357,572-character content, and the entire original prefix and suffix outside the new LSPV-2-owned insertion were compared exactly equal. **Root commit:** f2a17471eba6ac3491bb4c4a8953bed232df579f; verified final blob SHA **c28d894584219d77b330816e75fbf1e36af99944**. The preceding access-failure note is the historical first attempt, not the final publication state. This recovery changes no other role's ownership or any task status/schedule.
