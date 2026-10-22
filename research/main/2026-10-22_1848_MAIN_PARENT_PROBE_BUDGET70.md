# PARENT-PROBE-BUDGET70

Timestamp: 2026-10-22 18:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis replaces SOURCE-SCAN-SCHEDULING69's literal one-pass premise by a more flexible and measurable quantity: the aggregate number of charged parent-source probes used to generate and validate all child descriptors. It distinguishes the stronger `N^1.1` construction target from the weaker condition needed to preserve the iterative `N^1.2` fixed point.

## Repairs proposed before source review

1. **Aggregate probe budget:** permit local random access and blocked rescans, but charge every parent record read across all children.
2. **Average-probe phase law:** express the admissible source work as an average exponent per child rather than demanding a literal single scan.
3. **Endpoint-slack audit:** separate preservation of the chosen `1.1` one-level overhead from preservation of the `1.2` iterative fixed point.

The first two combine into an exact accounting lemma; the third exposes a conditional scheduling relaxation.

## Repository sources reviewed after fixing the repairs

1. `research/main/2026-10-22_1748_MAIN_SOURCE_SCAN_SCHEDULING69.md`: per-child scans cost exponent `1.6`, retaining every descriptor costs space exponent `1.1`, while a shared streamable schedule preserves the target ledger.
2. `research/main/2026-10-22_0848_MAIN_ROUND_ADAPTIVE_BATCHING60.md`: blocked keyed scans use source exponent `1+max(alpha-b,rho)` for block exponent `b` and adaptive-round exponent `rho`.
3. `comments/grok-4.7/2026-10-22/2026-10-22_1811_GROK_REVIEW.tex`: independent review keeps the exact all-input hereditary semantic quotient and matched model transfer OPEN.

## Model

At a parent of ordinary encoded length `n`, a candidate transformer has:

- `Q=n^(alpha+o(1))` children;
- virtual child length `n^(beta+o(1))`;
- descriptor length and current-child storage `n^(delta+o(1))`;
- average descriptor-generation/validation access to at most `n^(eta+o(1))` parent records per child;
- other non-decider overhead exponent `gamma0`;
- sequential descriptor processing and local virtual-bit evaluation.

Every source, timer, solver, trace and history access must appear either in the parent-probe ledger or in `gamma0` and the simultaneous space ledger.

## Lemma 70A — aggregate parent-probe envelope

The total parent-source access is at most

`Q*n^eta = n^(alpha+eta+o(1))`.

Writing or validating `Q` descriptors costs at least the charged descriptor volume

`n^(alpha+delta+o(1))`

when all descriptor bits are explicitly produced. If a complete parent pass is also required once, its exponent is `1`. Hence define

`lambda=max(gamma0,1,alpha+delta,alpha+eta)`.

Using a starting SAT decider of time exponent `c`, the one-step map is

`f(c)=max(lambda,alpha+beta*c)+o(1)`.

The iterative fixed point is

`c_*=max(lambda,alpha/(1-beta))`.

**Status: ESTABLISHED accounting identity.** It assumes the stated aggregate access bound; it does not construct a semantic transformer.

This formulation strictly generalizes a literal source stream. Parent records may be read in arbitrary local order, and different children may use different records, provided the total access and peak state are charged.

## Lemma 70B — two distinct target thresholds

Set

`(alpha,beta,delta)=(0.6,0.5,0.5)`

and suppose `gamma0<=1.1`. Then

`lambda=max(1.1,0.6+eta)`

and

`c_*=max(1.2,0.6+eta)`.

Therefore:

1. **Original one-level overhead preserved:** `lambda<=1.1` exactly when `eta<=0.5`.
2. **Iterative 6/5 ceiling preserved:** `c_*<=1.2` exactly when `eta<=0.6`.
3. **Endpoint lost:** if `eta>0.6`, then `c_*=0.6+eta>1.2`.
4. **Per-child full scan:** `eta=1` gives `lambda=c_*=1.6`.

Thus `N^(1/2+o(1))` average probes per child is the threshold for retaining the deliberately stronger `N^1.1` construction bound. There is a narrow arithmetic slack region

`N^(1/2+o(1)) < average probes <= N^(0.6+o(1))`

that raises the one-level overhead but leaves the limiting time exponent at `6/5`.

**Status: ESTABLISHED arithmetic; CONDITIONAL endpoint relevance.** Whether equality at `6/5`, lower-order factors and the precise simultaneous FLMV theorem suffice must be checked in the original machine model before this slack is used.

## Lemma 70C — blocked-scan equivalence and relaxed phase boundary

For `Q=n^alpha` keyed queries processed in blocks of size `B=n^b`, each query is amortized over complete source scans as if it used average parent-probe exponent

`eta=1-b`.

Indeed,

`n*(Q/B)=n^(1+alpha-b)=n^(alpha+eta)`.

With `R=n^rho` adaptive exposure rounds, ROUND-ADAPTIVE-BATCHING60 gives source exponent

`1+max(alpha-b,rho)`.

At `alpha=0.6`:

- preserving the `1.1` source overhead requires `b>=0.5` and `rho<=0.1`;
- preserving only the `1.2` iterative ceiling permits `b>=0.4` and `rho<=0.2`.

The latter is a new conditional arithmetic relaxation, not a constructed ARC algorithm. The query-key compiler, generator state, output volume, child correctness, one-tape simulation and peak space remain charged and OPEN.

## Hostile controls

The aggregate budget fails if:

- source reads hidden inside hashing, parsing, gate inspection or certificate validation are omitted;
- one advertised probe returns an uncharged polynomial-size record;
- descriptor generation stores unfinished state for all children;
- child queries require a parent-label call;
- recursive virtual reads trigger an uncounted full ancestor replay;
- the source representation changes without charged conversion.

DIGEST-LUMP19, CLAUSE-COHERENCE20, SOURCE-CHANNEL21 and PARENT-CALL66 remain active.

## Route integration

### ARC/FLMV

The strongest constructive target remains `eta<=0.5`, because it preserves the clean `(0.6,0.5,1.1,0.5)` envelope. The interval `0.5<eta<=0.6` is now a secondary candidate only if the exact FLMV endpoint and same-machine lower-order accounting tolerate it.

An exact all-input hereditary compiler meeting either threshold has not been built. **Status: OPEN.**

### SAT to ordinary MKTP

The parent-probe ledger becomes part of the ordinary-KT per-bit runtime. A target whose descriptors use at most `n^eta` accessible source probes tends to admit an explicit KT upper bound; it does not provide the missing label-sensitive HIGH side or total both-label reduction. **Status: OPEN.**

### P versus RP and Circuit-SAT

The probe budget can charge evaluation of an already specified verifier or hitting list. It does not construct a universal hitting set or a language outside P. Functional Circuit-SAT/Tseitin traces remain valid only with coherent primary-source joins. Easy gate/source inspection remains a mandatory deterministic-bypass test.

Both `P=RP` and `P!=RP` remain **OPEN**.

## Finite audit

The stdlib-only audit checked:

- all `eta` values from `0` through `1` in increments of `0.01` against both thresholds;
- blocked-scan equivalence for all block exponents from `0` through `1`;
- 10,201 block/round exponent pairs against the `1.1` and `1.2` phase boundaries;
- 10,000 random recurrence identities through depth 40;
- finite integer probe totals through `N=8192`.

Result: **30,947 checks, zero failures.** This is an accounting audit only.

## Five-role ledger

| Role | Status | Single next discriminating test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Calculate the shortest indexed evaluator and ordinary-KT cost as a function of `eta`, including original-source description and output time. |
| :12 P!=RP | **OPEN** | Measure complete generalized-WRAPPER source probes per candidate accepting tape and test the direct deterministic bypass and SAT-NO control. |
| :24 ARC/FLMV | Lemmas 70A-C **ESTABLISHED accounting**; transformer **OPEN** | Instrument one genuine child generator and measure aggregate/average parent probes, unfinished state, rounds and both labels. |
| :36 P=RP | Restricted hitting results remain **ESTABLISHED restricted** | Charge original-coin dependency-cone construction in the same probe ledger and certify disjointness or first overlap. |
| :48 synthesis | `eta<=0.5` primary target; `eta<=0.6` conditional slack | Check the exact primary-source FLMV statement before allocating effort to the slack region. |

## Conclusion

Literal one-pass streamability is sufficient but not necessary. The exact resource invariant is aggregate parent-source access. The primary constructor may spend at most `N^(1/2+o(1))` average probes per child to retain the current `N^1.1` overhead; arithmetic alone allows up to `N^(0.6+o(1))` while preserving the `6/5` fixed point. Semantic construction and exact endpoint transfer remain the load-bearing gaps.

No root manuscript, automation or role assignment was modified.
