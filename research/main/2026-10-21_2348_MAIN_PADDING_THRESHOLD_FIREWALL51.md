# PADDING-THRESHOLD-FIREWALL51

Timestamp: 2026-10-21 23:48 Asia/Seoul

## Outcome

This run establishes a scoped architectural firewall: semantic-preserving padding of a Circuit-SAT source can inflate an ordinary-MKTP threshold measured against padded source length without adding target information. Any proposed both-label reduction whose target commutes with canonical padding therefore fails on a sufficiently padded HIGH-label family. The statement is conditional on a target upper bound and padding equivariance; it is not a KT lower bound, a universal reduction impossibility, or a class separation.

P versus NP and P versus RP remain OPEN.

## Falsifiable repairs proposed before source review

1. **Padding-normalized source charge.** Track semantic-core length n, physical circuit length N, target length M, and one-tape acquisition cost separately. Reject exponent gains obtained only by replacing n with N = n^a.
2. **Padding-sensitive HIGH target.** Require a proposed UNSAT-to-HIGH map to inject genuinely new, uniformly addressable information from every padding block. Test it against canonical unpadding; if the target is recoverable from the core plus O(log a) advice, the HIGH claim fails once the MKTP threshold crosses the inherited upper bound.
3. **All-input heredity firewall.** An ARC speedup obtained by stripping deterministic padding applies only to a padded promise family. It cannot be substituted for an all-input SAT algorithm at the FLMV endpoint.

## Sources and newest role evidence

- :00 source report `research/agents/mktp/2026-10-21_FUTURE_EXPLICIT25.tex`, verified at GitHub commit `5a8fbfa3d51bff28f524044d8d5eaa5d44bcf704`: explicit future-query traffic is too large, while simple periodic targets remain low on both labels.
- Prior synthesis `research/main/2026-10-21_2248_MAIN_PROJECTED_DENSITY_GAUGE50.md`, verified at GitHub commit `1c589687bfaa24a5af6dae6fdad92fbff6c38fb7`: projected witness density is a diagnostic, not a derandomization theorem.
- The shared Google document was readable but contained no newer substantive role output than the verified repository evidence used here.

## Lemma: padding-threshold firewall

Fix k = 241. Let C_n be a circuit encoding of length Theta(n). Let P_a(C_n) append a canonical unique-extension copy chain and have physical length

N' = Theta(n^a).

Assume a proposed reduction R has the following property on this family: R(P_a(C_n)) is index-computable from R(C_n), a, and deterministic padding metadata with total ordinary-KT cost at most

KT(R(P_a(C_n))) <= n^(beta + o(1)).

The intended ordinary-MKTP threshold in the current parameter ledger is

p(N') = (N')^(6/(5k) + o(1)) = n^(6a/(5k) + o(1)).

For every fixed beta, choose any integer a > 5k beta / 6. Then 6a/(5k) > beta, so for sufficiently large n,

KT(R(P_a(C_n))) < p(N').

Thus the padded target is LOW. In particular, no padding-equivariant target satisfying this upper bound can map every member of an UNSAT family to HIGH at that threshold.

### Quantifiers and scope

The order is: for each fixed reduction-specific exponent beta, there exists a fixed padding power a, and then for all sufficiently large n the crossing occurs. This does not prove an upper bound for arbitrary targets. A padding-sensitive reduction that actually converts the padded source bits into irreducible indexed information is outside the lemma; constructing such a total deterministic both-label map remains OPEN.

## Circuit-SAT versus Tseitin/3-CNF

For a circuit with fixed input x, standard definitional Tseitin clauses give one forced variable value for every gate. Hence every satisfying input assignment has exactly one satisfying extension to gate variables. A copy chain preserves the computed Boolean function, number of satisfying input assignments, and unique-trace property. Gate sharing may reduce representation size compared with a tree formula, but a canonical copy chain remains visible to linear gate inspection and can be stripped with charged linear work.

Consequently:

- **Information source:** the copy chain contains no new semantic information beyond its predecessor gate.
- **Unique assignments:** Tseitin uniqueness preserves witnesses but supplies no hardness.
- **Digest portfolio:** hashes of deterministic copy-gate values are computable from the core; multiplying such digests does not create independent entropy.
- **Inspection attack:** simple copy/identity padding is RETIRED as a source of HIGH KT or RP hardness. Obfuscating gate names or topology merely moves the burden to a proved, chargeable source-hiding property.

## ARC/FLMV consistency check

If an algorithm first strips P_a(C_n) to its core and then spends n^c time, its running time expressed in padded length is (N')^(c/a). Taking large a makes c/a arbitrarily small on that padded family. This is not an all-input hereditary contraction: it says nothing about unpadded circuits or adversarial encodings, and therefore cannot reach the FLMV simultaneous time-space contradiction.

The same normalization applies to space and output. Peak storage for the physical padded input, streaming passes, and output materialization must be charged in the native machine model; source compression cannot be silently treated as free.

## Finite audit

`experiments/review/2026-10-21_padding_threshold_firewall51_audit.py` passed 963,379 assertions. It checked 980 padded random circuits, 948,944 assignment-level function/Tseitin equivalences, 56 indexed zero-extension controls, 25 ARC exponent cases, and exact rational threshold crossings for nine beta values. This validates only the implementation and algebraic examples, not unrestricted complexity claims.

## Status ledger

| Role / arrow | Status | Current boundary | Single next discriminating test |
|---|---|---|---|
| :00 SAT to ordinary MKTP | OPEN | Need a total deterministic both-label generator meeting ordinary-KT thresholds, same-machine costs, and resisting canonical unpadding without random-oracle leakage. | Specify one padding-sensitive candidate at the bit-index level and either prove its padded HIGH lower bound or exhibit an index program below threshold. |
| :12 P != RP | OPEN | Circuit width, ANF degree, digest diversity, and padded size do not identify a language outside every deterministic polynomial-time machine. | Normalize away deterministic gates, then test whether the residual language still defeats the explicit gate-inspection algorithm. |
| :24 ARC/FLMV | OPEN | Core stripping yields only promise-family exponents; heredity over every input length and every encoding is absent. | Write the contractor's recurrence on both canonical and adversarially padded inputs and charge acquisition, output, time, and peak space on the same machine. |
| :36 P = RP | OPEN | Deterministic padding does not provide a uniform hitting set for every RP machine; verifier acceptance must be preserved for all inputs. | Require a seed generator invariant under canonical padding and test it against a verifier whose accepting seeds are shifted by the unpadded core. |
| :48 padding firewall | ESTABLISHED under stated hypotheses | Threshold drift defeats padding-equivariant HIGH targets; finite audit passed. | Apply the lemma to the next concrete :00 target with an explicit beta and target-index algorithm. |

## Retired in this run

- RETIRED: treating deterministic Circuit-SAT copy padding as new semantic entropy.
- RETIRED: converting a padded-promise exponent c/a into an all-input ARC/FLMV bound.
- RETIRED: inferring P != RP or P != NP from circuit-family measurements, hashes, or the finite audit.

## Publication status

Repository publication and exact readback are recorded separately after upload. No root manuscript was modified.
