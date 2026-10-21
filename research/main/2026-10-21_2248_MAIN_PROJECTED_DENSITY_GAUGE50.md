# PROJECTED-DENSITY-GAUGE50

Date: 2026-10-21, Asia/Seoul. Scope: bounded synthesis across the fixed five roles. Circuit-SAT is used only as a comparison representation inside the existing P-vs-NP and P-vs-RP proof DAGs. Global status: **P versus NP OPEN; P versus RP OPEN**.

## 1. Repairs proposed before source inspection

1. **Projected-density ledger.** Every Circuit-SAT/RP claim must state whether randomness ranges over primary circuit inputs or over all Tseitin variables. These probabilities differ by an exactly chargeable trace factor.
2. **Deterministic-extension quotient.** Before treating low satisfying density, large width, or many gate variables as hardness, quotient out uniquely determined trace variables and deterministic copy chains. Otherwise arbitrary padding manufactures the claimed obstruction.
3. **Role-map and completion charge.** Projection-aware sampling is valid only with a uniformly recoverable primary-input map and a charged forward trace computation. A hidden or incompressible map removes the algorithm but does not establish hardness.

Each repair is falsifiable: count extensions for every primary input; add copy gates and see whether the claimed quantity changes; then test a selector bit or direct gate inspection for a deterministic bypass.

## 2. Repository evidence checked

Two current repository sources were used.

- “RP_DENSE_BYPASS14_HANDOFF.md,” commit 6834b3eb66d862e2a581cc349a1baa727dacb008, constructs a uniform fanin-two verifier whose reduced ANF has degree \(n+1\), whose gate graph has treewidth at least \(n-1\), and whose random inputs are all relevant, yet a selector bit gives an immediate accepting seed and the recognized language is \(x_1=1\in P\).
- “PARSIMONIOUS-CIRCUIT-3CNF47,” commit 587604b39b11bc83de6bf6c7bb621540fd0eeb27, gives a linear Circuit-SAT to proper-3CNF conversion with exactly one auxiliary extension for each legal gate row and hence exactly one complete trace for every accepting circuit input.

The Drive continuity log was read. Its latest substantive fallback remains “ARC-HEREDITARY-SCOPED10” from 2026-10-20; no newer unpublished role result was present.

## 3. Exact projection-density theorem

Let \(C:\{0,1\}^m\to\{0,1\}\). Let \(E_C(r,w)\) be any Boolean formula over primary variables \(r\in\{0,1\}^m\) and \(q\) auxiliary variables \(w\in\{0,1\}^q\) satisfying the parsimonious deterministic-extension condition

\[
\forall r\qquad
\sum_{w\in\{0,1\}^q} E_C(r,w)=C(r).
\]

Equivalently, each accepting \(r\) has exactly one valid trace \(w(r)\), and each rejecting \(r\) has none. If
\[
A=\{r:C(r)=1\},
\]
then
\[
\#SAT(E_C)=|A|,
\]
\[
\Pr_{r,w}[E_C(r,w)=1]
=\frac{|A|}{2^{m+q}}
=2^{-q}\Pr_r[C(r)=1].
\]

In contrast, the projection-aware experiment “sample \(r\), deterministically compute \(w(r)\), then check the output” accepts with probability exactly
\[
\Pr_r[C(r)=1].
\]

This is an equality, not an asymptotic estimate.

## 4. Deterministic padding gauge

Adjoin \(d\) new variables that are uniquely determined functions of the previous variables—for example a chain
\[
y_1=o,\qquad y_{j+1}=y_j,
\]
and force the final copy as output. The represented circuit function and accepting primary set \(A\) do not change. Parsimony remains true, so the number of formula models remains \(|A|\). Yet uniform full-assignment density becomes
\[
2^{-(q+d)}\Pr_r[C(r)=1],
\]
an additional factor \(2^{-d}\).

Therefore full Tseitin-assignment density is a representation gauge. It can be made exponentially small by deterministic copy padding while:

- preserving the circuit language;
- preserving projected RP acceptance probability;
- preserving a unique trace for every primary input;
- adding no hard witness choice;
- admitting linear-time forward completion.

The same applies to duplicated deterministic subcircuits. Gate sharing decreases the number of trace variables and increases full-assignment density; unsharing does the reverse. Neither operation changes the projected accepting input set.

## 5. Tseitin, proper 3-CNF, uniqueness and scrambling

The theorem applies directly to standard biconditional Tseitin clauses of width at most three. It also applies to the canonical proper-3CNF gadget from “PARSIMONIOUS-CIRCUIT-3CNF47”: its additional gadget variables are uniquely determined for legal rows, so they enter \(q\) and contribute another exact power-of-two density factor.

This separates four claims that must not be conflated:

| Claim | Exact status |
|---|---|
| One gate trace per fixed primary input | **ESTABLISHED** for biconditional/canonical parsimonious encoding |
| One complete satisfying assignment | Equivalent to one accepting primary input plus unique trace; not a hardness result |
| Low density over every formula variable | Representation-dependent; arbitrarily reducible by deterministic padding |
| Low density over primary inputs | Semantic for the specified circuit representation, but still not a deterministic lower bound |

Clause and variable permutations preserve full model count by assignment bijection. If a primary-role map is explicit or short-seeded, invert it and charge its description/time. If it is hidden, a projection-aware sampler is unspecified; hiding the map does not increase projected acceptance density or prove hardness.

## 6. DENSE-BYPASS14 integration

For the :12 verifier
\[
C_n(b,z)=b\lor H_n(z),
\]
setting \(b=1\) accepts for every \(z\), so projected acceptance probability is at least \(1/2\). The report independently proves high ANF degree, a \(K_n\) gate-graph minor, and relevance of every random bit.

After a parsimonious Tseitin conversion with \(q\) trace variables, uniform full-formula sampling succeeds with probability only
\[
2^{-q}\Pr[C_n=1].
\]
Appending \(d\) copy gates makes this \(2^{-(q+d)}\Pr[C_n=1]\), although the same fixed selector seed remains available and the language is still the linear-time language \(x_1=1\).

Thus none of high degree, high gate width, input relevance, unique trace, or exponentially small full-CNF density excludes an easy deterministic seed or an alternative language decider.

## 7. Digest portfolios, MKTP and ARC

### Digest portfolios

The “DIGEST-PORTFOLIO8” bound concerns how many **primary witnesses** a digest and a portfolio of complete-witness tests can cover. Randomly guessing gate/auxiliary variables would multiply success by a trace factor, but that loss is artificial because the trace can be completed deterministically. It cannot strengthen the primary-witness lower bound.

### SAT to ordinary MKTP

Appending deterministic gate traces or copy chains increases target length but creates no new entropy. If the circuit and role map have a short indexed description, target bits inherit a charged indexed evaluator and may be LOW. If the full circuit source is placed in the program, its description length is charged. Failure of full-assignment sampling is not an ordinary-KT HIGH proof.

The current weakest arrow remains a deterministic, total, both-label map producing the required ordinary-KT gap without random-oracle, hidden-source, side-table or replay leakage.

### ARC/FLMV

Gate traces can be streamed when the topological order and inputs are available, but a high-width shared circuit may require a large live frontier. Deterministic copy padding can inflate formula size or apparent width without adding semantic difficulty. Any ARC contractor must quotient such padding and still charge boundary state, source reads, serialized children, failed calls, ancestors and peak workspace on all inputs.

## 8. RP proof DAG

- **P=RP remains OPEN.** Projection-aware sampling is a valid simulation only for a supplied circuit representation with known primary variables and charged trace evaluation. It is not a uniform deterministic simulation of every RP machine.
- **P!=RP remains OPEN.** A sparse Tseitin formula, difficult role recovery, large circuit width, or high ANF degree is a verifier property. Separation needs a language in RP outside every deterministic polynomial-time machine.
- **RETIRED:** full-Tseitin-assignment density as a language hardness measure; deterministic trace-variable padding as an amplification; gate unsharing as evidence of a harder RP language.

## 9. Executable consistency check

The standard-library audit passed **769,806 assertions** with zero failures:

- 635,040 exhaustive full-assignment versus unique-trace equivalence checks;
- 1,080 copy-chain instances verifying invariant model count and exact \(2^{-d}\) density loss;
- 360 clause/variable scrambling controls;
- 254 point circuits with exactly one primary witness and one complete model;
- 14 exact “DENSE-BYPASS14” count and selector controls;
- 180 random fanin-two circuits.

These finite tests verify the theorem’s bookkeeping and encodings. They do not compute arbitrary KT or prove either class separation.

## 10. Status and next discriminating tests

| Role | Status | Weakest arrow | Single next test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN** | Both-label ordinary-KT gap after all indexed trace/source costs | Apply the target generator to a circuit plus \(d\) copy gates and prove its label and KT classification are padding invariant. |
| :12 P!=RP | **OPEN**; “DENSE-BYPASS14” **ESTABLISHED counterexample** | Actual language outside every deterministic polynomial-time machine | Quotient the proposed Circuit-SAT family by deterministic trace/padding, then test the residual primary function for a selector or direct decider. |
| :24 ARC/FLMV | **OPEN** | All-input hereditary contractor with true semantic frontier | Remove copy/trace-only gates before partitioning, then charge the remaining high-width frontier on an erasing decider. |
| :36 P=RP | **OPEN** | Uniform simulation of arbitrary RP machines | State and recover the primary-randomness projection for an arbitrary verifier without solving semantic dead-variable analysis. |
| :48 synthesis | Projection-density theorem **ESTABLISHED** | Promotion only from representation-invariant quantities | Require both projected and full density, extension multiplicity, role-map access and completion cost in every circuit claim. |

P versus NP and P versus RP remain **OPEN**.
