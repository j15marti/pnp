# PADDING-SELF-REDUCTION-FIREWALL77

Timestamp: 2026-10-23 01:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis tests three proposed ways to turn the CONDITIONAL succinct two-label certificate interface of TWO-LABEL-CERTIFICATE-ENVELOPE76 into the all-input hereditary ARC transformer: ordinary SAT self-reduction, polynomial padding, and direct search for a small certificate circuit under `P=NP`. The first makes current-scale source-bearing queries; the second has essentially no FLMV slack; the third restates the OPEN compact-witness premise. No load-bearing arrow is closed.

## Repairs fixed before source review

1. **Prefix self-reduction:** use SAT prefix queries to reconstruct the correct label and a certificate-bit circuit.
2. **Polynomial padding:** pad source length `n` to `N=n^p` until a polynomial-size witness circuit becomes `N^beta`-small.
3. **Collapsed validity search:** under `P=NP`, search directly for `W` satisfying `exists W forall i not Bad(F,b,W,i)`.

Predeclared falsifiers: a query that must carry the full source is not a strict child; padding must be unpadded before applying FLMV; PH collapse supplies polynomial time but neither a fixed exponent nor a small witness.

## Repository sources reviewed after fixing the repairs

1. [TWO-LABEL-CERTIFICATE-ENVELOPE76](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-23_0048_MAIN_TWO_LABEL_CERTIFICATE_ENVELOPE76.md): a small certificate-bit circuit plus exact small source evaluator is CONDITIONAL; explicit histories and sampled digests are RETIRED generically.
2. [FLMV-PROBE-MARGIN71](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-22_1948_MAIN_FLMV_PROBE_MARGIN71.md): the audited random-access FLMV curve is
   `d_F(c)=((c+2)/c^2-c)/2`, with strict simultaneous-space entry required.
3. [Independent review 01:15 KST](https://github.com/j15marti/pnp/blob/main/comments/grok-4.7/2026-10-23/2026-10-23_0115_GROK_REVIEW.tex): no load-bearing implication is closed; exact all-input hereditary source-aware compression remains OPEN.

## Lemma 77A — ordinary prefix self-reduction is current-scale

Let `F` be an explicit SAT or Circuit-SAT source of encoded length `N`. A standard lexicographic witness search asks, for prefixes `a_1...a_j`,

`exists a_(j+1)...a_m : R(F,b,a_1...a_m)=1`.

Every standalone ordinary SAT/Circuit-SAT query must either:

1. contain an exact encoding of the source-dependent verifier, hence has length `Omega(N)` in the worst case; or
2. refer to `F` through a shared oracle/pointer, which is no longer an ordinary standalone child and must charge the source representation and every access.

Therefore standard self-reduction does not produce children of maximum length `N^beta` for fixed `beta<1`. Moreover, choosing the correct label `b` by first deciding `F` repeats parent-label circularity.

This is not an unrestricted lower bound: an independently proved exact source evaluator of size `N^beta` could evade it. That evaluator is precisely one of the OPEN interfaces.

**Status: ESTABLISHED representation/accounting lemma; ordinary explicit prefix-search repair RETIRED generically; compressed exact source evaluator OPEN.**

### Quantifier warning

Self-reduction may produce a different continuation for every prefix. It does not prove one circuit `W` satisfying `exists W forall i`. The invalid exchange

`forall i exists W_i  =>  exists W forall i`

remains forbidden.

## Lemma 77B — exact padding/FLMV transport

Pad an original length-`n` input to `N=n^p`, `p>=1`. If an algorithm measured at padded length uses time `N^(c+o(1))` and space `N^(s+o(1))`, then as an algorithm for the original input it uses

`n^(pc+o(1))` time and `n^(ps+o(1))` space.

The audited FLMV contradiction is available only when

`p s < d_F(p c)`, where `d_F(x)=((x+2)/x^2-x)/2`.

If an original witness circuit has size `n^(d+o(1))`, making it fit a padded child bound `N^(beta+o(1))` requires

`d <= p beta`.

Combining the inequalities gives the necessary condition

`d < beta p_max(c,s)`,

where `p_max` is the unique root above one of `p s=d_F(p c)`; uniqueness follows because the left side increases and `d_F` strictly decreases for positive arguments.

### Computed margins

| Envelope at padded size | `p_max` | Largest original witness exponent `beta p_max` |
|---|---:|---:|
| baseline `(c,s,beta)=(1.2,.5,.5)` | 1.003836695566892 | 0.501918347783446 |
| safe point `(1.205,.5,.5)` | 1.000390875057075 | 0.500195437528537 |
| retuned `(1.2021,.505,.505)` | 1.000657289925443 | 0.505331931412349 |

Thus polynomial padding cannot turn an arbitrary `n^d` certificate circuit into a legal child while preserving the matched FLMV endpoint. At the baseline it buys less than 0.002 in witness exponent.

**Status: ESTABLISHED exponent-transport firewall, conditional only on the already source-audited FLMV statement and same-model serialization. Generic arbitrary-polynomial padding repair RETIRED.**

### Physical versus virtual padding

- **Physical padding:** generating/reading the length-`N` input and then unpadding multiplies resource exponents as above.
- **Virtual padding:** passing `(F,1^{N-n})` succinctly leaves the native input description near length `n`; measuring witness size against `N` without proving a model-preserving transfer is invalid.
- Padding also changes ordinary MKTP instance length and threshold. It cannot be used merely as a denominator trick.

## Lemma 77C — collapsed validity search does not supply the missing object

For a proposed bit-circuit `W`, exact validity has the form

`exists W forall i : not Bad(F,b,W,i)`.

Under `P=NP`, the polynomial hierarchy collapses and this bounded explicit search predicate is decidable in polynomial time. But this fact gives neither:

1. existence of a `W` of size `N^beta` (or `tau(n)^o(1)`);
2. a fixed exponent compatible with the ARC/FLMV envelope;
3. strict-child queries, because each standard search query still contains or accesses the length-`N` source;
4. hereditary correctness and charged acquisition on every recursive child.

Consequently this is exactly the COMPACT-HISTORY20 conditional interface, not a construction.

**Status: CONDITIONAL logical search reduction; W-size premise, exact source compression and resource envelope OPEN.**

## Circuit-SAT and SOURCE-CHANNEL21 control

Functional Tseitin variables are uniquely determined after shared primary inputs are fixed, but this does not compress those inputs or permit occurrence-local witness splitting. Direct source clauses can expose an easy deterministic decoder, as in SOURCE-CHANNEL21. Any use of the inequality

`success <= h 2^(q+bt-n)`

must count all preprocessing bits, adaptive source replies, gate/source inspection and complete witness probes. A source-readable easy family is a control, not a lower bound.

## Ordinary MKTP/MCSP route

- **ESTABLISHED:** virtual or physical padding must be charged in source description, indexed runtime and target threshold.
- **RETIRED:** claiming HIGH ordinary KT from the padded length or from a long materialized history.
- **OPEN:** deterministic total both-label SAT-to-ordinary-MKTP generator with a true label-sensitive HIGH case, correct polynomial threshold, same-machine indexed evaluation and no random-oracle proof-of-work.
- A small `W` would naturally support a LOW description; it does not provide the missing HIGH label.

## ARC/FLMV route

- **ESTABLISHED:** ordinary prefix search has current-scale source-bearing queries.
- **ESTABLISHED:** padding must satisfy `ps<d_F(pc)`; the three audited envelopes tolerate only `p=1+o(1)` with the explicit constants above.
- **RETIRED:** standard self-reduction and arbitrary polynomial padding as generic repairs.
- **CONDITIONAL:** a pre-existing small exact source evaluator and uniformly acquired small `W` could still yield a violation-search child.
- **OPEN:** construct those objects for every input and every recursive descendant, with both labels, output, replay, acquisition and simultaneous peak space charged.

## Independent P-vs-RP audit

Dummy input padding or ignored dummy random coins do not create a uniform derandomizer. If a verifier ignores `r` new coins, its accepting density is unchanged although its tape space grows. A candidate simulator must either strip such padding uniformly or charge it; a hitting list proved only for one encoding or fixed gate budget does not establish `P=RP`.

- **OPEN P!=RP:** no explicit unrelativized RP language outside all deterministic polynomial-time machines.
- **OPEN P=RP:** no uniform deterministic simulator for every RP machine.
- **RETIRED:** padding, high degree, oracle query bounds, source-limited inequalities or finite experiments as class-separation evidence.

## Mathematical consistency audit

The accompanying JavaScript recomputes each root by 200 bisection steps and checks 100,001 grid points per envelope plus both sides of every boundary.

Result: **300,009 checks, zero failures.** This checks the exponent arithmetic only.

## Five-role next discriminating tests

| Role | Status | Single next experiment |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | For one padded target, report unpadded source-description length, per-bit time and both KT thresholds; reject any HIGH claim caused only by padding. |
| :12 P!=RP | restricted SOURCE-CHANNEL21 **ESTABLISHED**; separation **OPEN** | Apply the full `q,b,t,h` ledger to one real WRAPPER DAG and run source/gate-inspection bypass first. |
| :24 ARC/FLMV | Lemmas 77A–B **ESTABLISHED**; transformer **OPEN** | Attempt one exact source evaluator below `N^beta`; if it embeds the source, record the resulting maximum child length. |
| :36 P=RP | dummy-padding firewall **ESTABLISHED**; derandomization **OPEN** | Test whether a proposed hitting-set constructor is invariant under ignored dummy coins and equivalent verifier rewrites. |
| :48 synthesis | generic self-reduction/padding repairs **RETIRED** | Admit a compact-witness candidate only with one global `W`, exact source access and unpadded FLMV exponents. |

## Conclusion

Neither standard SAT self-reduction nor polynomial padding bridges the succinct-certificate gap. Self-reduction retains the current-scale source; padding consumes the same time-space exponents needed for the FLMV contradiction and buys less than 0.002 witness exponent at the baseline. Direct `Sigma_2` search under `P=NP` still assumes the missing small `W` and carries unknown polynomial costs. The only surviving form is the already explicit CONDITIONAL interface: a uniformly acquired small global certificate circuit plus a genuinely small exact source evaluator. P versus NP and P versus RP remain OPEN.

No root manuscript, automation or role assignment was modified.
