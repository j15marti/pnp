# RESIDUAL-STATE-FIREWALL84 — enumeration is an upper bound; the universal charged bridge is open

**Role:** :48 synthesis  
**Timestamp:** 2026-10-23 08:48 KST  
**Global status:** P versus NP OPEN.

## Advance repairs

1. Define residual dimension from a charged normalization: source variables \(n\), eliminated variables \(k\), and \(r=n-k\). Use \(v=n/r\) only as a multiplicative compression ratio. Never infer \(r\) from observed runtime.
2. Separate three charged resources: acquisition/source access \(Q_A\), symbolic compression and compatibility \(C_A\), and residual continuation \(E_A\). Total time is at least their sum, plus ordinary parsing/output costs.
3. Test any claimed \(2^r\) necessity against a source-aware structured family and a decide-first normalizer before treating it as an unrestricted theorem.

## Sources reviewed

- Project original: research/agents/lspv-3/2026-10-16_1535_SOURCEPROBE19_HANDOFF.md.
- Project controls: research/main/2026-10-23_0648_MAIN_EXPANDER_RESIDUAL_SIZE82.md and research/main/2026-10-23_0748_MAIN_TSEITIN_EXPANDER_PAIR83.md.
- Shared original: ES-ATLAS-0025, Google Doc 1xUMt-pnPu2OMCVHIUGg3hPcEborWG7AMA4eJMh3qbzY.
- Primary literature: Impagliazzo–Paturi, “On the Complexity of k-SAT,” JCSS 62 (2001), DOI 10.1006/jcss.2000.1727; Impagliazzo–Paturi–Zane, “Which Problems Have Strongly Exponential Complexity?”, JCSS 63 (2001), DOI 10.1006/jcss.2001.1774.

The primary papers explicitly formulate exponential k-SAT time as ETH/SETH-style hypotheses and give sparsification/SERF reductions. They do not prove that every SAT algorithm must enumerate all residual assignments.

## Model and claim ledger

Let \(F\) be a fixed explicit 3-CNF encoding of bit length \(N\), with \(n\) named source variables. A declared normalization protocol \(\Pi\) may eliminate \(k\) variables and expose \(r=n-k\) residual variables. If \(r>0\), define \(v=n/r\). Thus:

- additive elimination: \(r=n-k\);
- multiplicative compression: \(r=n/v\);
- \(2^r\) is the number of total residual assignments;
- SAT asks whether at least one assignment works, not how many work.

The exhaustive algorithm evaluates all assignments in \(2^r\operatorname{poly}(N)\) time. This is an **ESTABLISHED enumeration upper bound**, not a lower bound.

## Lemma 84A — exact restricted point-query lower bound

Consider a black-box predicate \(O:\{0,1\}^r\to\{0,1\}\) promised to be either EMPTY or a SINGLETON. Every deterministic point-query algorithm deciding which case holds requires \(2^r\) queries in the worst case.

**Proof.** If it stops after fewer than \(2^r\) all-zero replies, choose an unqueried point \(z\). The empty oracle and the singleton oracle \(O_z(x)=[x=z]\) have identical transcripts, so the algorithm gives the same answer on two opposite labels. □

**Status: ESTABLISHED, restricted black-box lower bound.**

SOURCEPROBE19 is a compatible success-set version. Its own fatal lift issue remains: an explicit circuit for \(O_z\) reveals \(z\), so unrestricted source-aware computation can bypass the query bound.

## Lemma 84B — decide-first normalization firewall

Let \(L\) be any language in P. If the phrase “after all reductions” permits arbitrary polynomial-time semantic preprocessing, then there is a legal normalizer that decides \(x\in L\) first and outputs one fixed TRUE residual or one fixed FALSE residual. Its continuation has \(r=0\).

**Proof.** Run the assumed polynomial-time decider and branch to the corresponding constant instance. Acquisition includes the whole decision computation. □

**Status: ESTABLISHED logical firewall.**

Consequently, residual dimension cannot be defined after unrestricted semantic preprocessing and then used to prove that the preprocessing was slow. A useful residual theorem needs an independently specified operation/representation class and must charge discovery, source reads, failed attempts, representation construction, compatibility checks, DAG reuse, output, and peak space.

## Lemma 84C — structured source-aware falsifier

TSEITIN-EXPANDER-PAIR83 has \(r=\Theta(N/\log N)\) edge variables and hence \(2^r\) possible assignments. Nevertheless, parsing one charge bit per vertex and XORing all charges decides its SAT label in \(O(N)\) time and logarithmic auxiliary space.

The finite audit independently reconstructed connected cubic prism systems and confirmed by brute force that SAT is equivalent to even total charge parity on 72 instances.

**Status: ESTABLISHED restricted falsifier.**

Therefore the blanket statement “all \(2^r\) remaining states must be checked” is **RETIRED** for explicit source-aware algorithms. Large syntactic residual, large treewidth, many assignments, rare witnesses, and full-source cores do not repair it.

## The exact conditional theorem

Fix one NP-complete language \(L\), one machine model, and one charged normalization protocol \(\Pi\). For every deterministic decider \(A\), let

\[
T_A(F)=Q_A(F)+C_A(F)+E_A(F)+T_{\mathrm{parse}}(F)+T_{\mathrm{out}}(F),
\]

with the corresponding peak-space maximum charged separately.

Assume constants \(a>0\) and \(b\ge0\) such that for every correct deterministic \(A\), there are infinitely many inputs \(F\) on which:

1. \(r_A(F)\) is defined by \(\Pi\), independently of observed runtime;
2. \(T_A(F)\ge 2^{a r_A(F)}/N^b\);
3. \(r_A(F)/\log_2 N\) is unbounded.

Then \(L\notin P\), hence \(P\ne NP\).

**Proof.** If \(A\) ran in \(O(N^d)\), choose one of the promised inputs with \(a r_A/\log_2N-b>d+1\) and \(N\) larger than the hidden polynomial constant. Then

\[
T_A(F)\ge N^{a r_A/\log_2N-b}>N^{d+1},
\]

contradicting the time bound. □

**Status: CONDITIONAL theorem.** The arithmetic implication is complete. Premises 1–3 for every algorithm are the unresolved content, not consequences of residual cardinality.

Constant \(v=n/r\) would force \(r=\Theta(n)\) and an exponential target, which is stronger than needed. The conditional theorem only needs \(r/\log N\) unbounded along hard inputs.

## Charged acquisition/continuation trichotomy

For a candidate \(A\) under a declared protocol:

1. **Pointwise continuation:** if it learns the residual only through point queries, Lemma 84A gives \(2^r\) worst-case queries.
2. **Symbolic compression:** if it groups residual assignments, charge the compressor’s construction, size, interface, collision soundness, source provenance, and compatibility verification.
3. **Semantic/direct decision:** if it computes a global invariant or the final label, charge that computation to acquisition.

This is an exhaustive accounting trichotomy but not a lower bound. The missing theorem is that, on one explicit NP-complete language, every algorithm pays superpolynomially in at least one branch.

ES-ATLAS-0025 reaches the same boundary: quotient width lower-bounds OBDD-like representations with cut-distinguishability, while arbitrary machines may use global invariants. Its compression-or-distinguish target remains OPEN.

## Exact requested chain

1. **Defined obstruction — ESTABLISHED only in restricted models:** an \(r\)-bit EMPTY-vs-SINGLETON point oracle has \(2^r\) deterministic query complexity.
2. **Charged acquisition/continuation dichotomy — accounting ESTABLISHED, hardness OPEN:** pointwise continuation is expensive; symbolic/global escapes must be fully charged.
3. **All-algorithm coverage — OPEN:** no theorem covers every uniform deterministic polynomial-time SAT decider and every source-aware representation.
4. **Superpolynomial contradiction — CONDITIONAL and proved:** the stated \(2^{a r}/N^b\) bound plus unbounded \(r/\log N\) rules out polynomial time.

The broken arrow is 2→3. It is exactly where source inspection, affine elimination, SCC methods, Horn propagation, component decomposition, caching, and arbitrary representation changes enter.

## Resource and quantifier ledger

- **Language:** one fixed explicit 3-CNF SAT encoding; not a moving oracle family.
- **Algorithm quantifier needed:** for every uniform deterministic polynomial-time decider \(A\).
- **Input quantifier needed:** infinitely many source inputs \(F\) chosen after \(A\).
- **Source access:** every bit/word read and preprocessing pass charged.
- **Representation:** basis, gates, wires, switches, equality joins, and DAG reuse stated when used.
- **Normalization:** \(r\) source-defined through \(\Pi\), never reverse-engineered from runtime.
- **Time:** acquisition + compression/compatibility + continuation + parsing/output.
- **Space:** peak simultaneous live state, not summed certificate lengths.
- **Experiments:** finite falsifiers/implementation checks only.

## Audit

The executable audit performed:

- 100,000 additive/multiplicative parameter checks;
- 100,000 EMPTY-vs-SINGLETON transcript adversaries;
- 100,000 conditional exponent checks;
- 72 cubic-prism Tseitin instances, with 799,392 brute-force edge assignments.

Total: **3,115,037 assertions, zero failures**. This validates the finite implementations and exact arithmetic only.

## Status table

- **ESTABLISHED:** \(r=n-k\), \(v=n/r\) convention; exhaustive \(2^r\) upper bound; black-box singleton query lower bound; decide-first firewall; structured parity bypass; conditional exponent implication.
- **COMPUTATIONAL:** 3,115,037 finite assertions with zero failures.
- **CONDITIONAL:** the universal charged theorem above.
- **OPEN:** any all-algorithm acquisition/compression/continuation lower bound for explicit SAT.
- **RETIRED:** “remaining assignments must all be checked” as an unrestricted SAT claim; residual size alone; defining effective dimension from runtime.

## Highest-value next missing lemma

Prove one **representation-independent charged compression-or-distinguish lemma** for a fixed explicit 3-CNF family:

> For every deterministic random-access machine \(A\), either a model-matched extraction exposes \(2^{\Omega(r)}\) distinguishable residual obligations, or \(A\) constructs a sound compression/global invariant whose acquisition, representation, compatibility verification, or continuation cost is \(2^{\Omega(r)}/N^{O(1)}\).

The lemma must survive the Tseitin parity, 2-SAT SCC, Horn propagation, bounded-treewidth DP, caching, component, source-replay, and decide-first controls. No reviewed source proves it.

## Bottom line

The residual proposal now has an exact valid core and an exact missing arrow. \(2^r\) is a universal enumeration upper bound and a lower bound for a detached point-query model. It is not a lower bound for explicit SAT. The conditional exponent theorem would imply \(P\ne NP\), but its universal charged coverage premise remains OPEN. P versus NP remains OPEN.
