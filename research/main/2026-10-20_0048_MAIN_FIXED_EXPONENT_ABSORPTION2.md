# FIXED-EXPONENT-ABSORPTION2

Date: 2026-10-20 00:48 Asia/Seoul. **P versus NP remains OPEN.**

## Outcome

The proof-certified “fastest correct” portfolio does **not** control the unknown MMW polynomial exponent. It preserves that exponent and adds program/proof-dependent constants, certification, simulation, replay, and space costs. The exponent does not need to be known or minimized if—and only if—the proposed SAT-to-KT/MKTP bridge is a single uniform all-\(k\) construction. A fixed unknown exponent can then be absorbed by choosing a fixed \(k\) after the exponent.

This is a quantifier and resource-composition lemma, not a construction of the missing bridge.

## Recovered current artifacts

- UNIVERSAL-CERTIFIED-RACE1 proves:
  - unrestricted per-instance “fastest algorithm” selection is circular because an \(O(N)\)-bit program can hardcode the chosen instance and its answer;
  - a sound proof-certified weighted dovetail is correct and near a fixed certified candidate in abstract guest-step accounting;
  - it does not prove fixed-theory completeness, one-way tape simulation, jointly bounded time/space, or exponent reduction.
- CHMY-FKBASEERASURE1 retires only the attempted injection of an arbitrary MCSP source into the base slot of the CHMY mask recurrence. It does not attack the original CHMY generator.
- The full MINFREE-SIGMA2-MERGE17 report/code/raw is now published and agrees with the MMW Stream-Merge spine.
- Exact-title FLMV-KT-BRIDGE1 and CHARGED-TOTALIZATION1 artifacts were not present in the verified repository tree or continuity log. Exact-keyword Drive searches returned older related documents, not current exact-title outputs. Their claimed arrows therefore remain unavailable rather than credited.

## Ideas proposed before literature

1. Absorb a single fixed exponent \(C\) through \(p_k=M^{1/k+o(1)}\), rather than trying to discover or minimize \(C\).
2. Use quantifier reversal as the falsifier: \(\forall k\,\exists A_k,C_k\) is inadequate when \(C_k/k\) need not vanish; one uniform all-\(k\) language and algorithm is required.
3. Treat certified universal search as a soundness device only. It cannot lower the exponent of the best certified member and may omit correct but unprovable algorithms.
4. Compose the complete call and storage ledger before invoking the FLMV endpoint.

## Theorem: fixed-exponent absorption with a charged ledger

Let \(M\) be target length. For every fixed integer \(k\), suppose a uniform bridge uses objects of length

\[
p_k(M)=M^{1/k+o_M(1)}.
\]

Assume one fixed deterministic subroutine \(A\), independent of \(k\), runs on every encoded bridge query in time \(p^C\) and space \(p^D\), for fixed finite \(C,D\). Suppose the bridge makes sequentially charged

\[
M^{q_k+o(1)}
\]

subroutine calls, has local time \(M^{\ell_k+o(1)}\), and local live space \(M^{r_k+o(1)}\). Then the composed leading exponents are

\[
t_k\le \max\{\ell_k,\ q_k+C/k\}+o(1),
\qquad
s_k\le \max\{r_k,\ D/k\}+o(1),
\]

provided query materialization, source access, replay, and answer serialization are already included in \(q_k,\ell_k,r_k\), and calls do not leave uncharged simultaneously live states.

### Proof

Each call costs

\[
p_k^C=M^{C/k+o(1)}
\]

time and \(M^{D/k+o(1)}\) space. Multiplying sequential call count by per-call time adds exponents, while sequentially reusable work space takes the maximum. Local work contributes the other maximum terms. All constants \(C,D,k\) are fixed before \(M\to\infty\).

Consequently, if \(q_k\le q_0\), \(\ell_k\le \ell_0\), and \(r_k\le r_0\) for arbitrarily large fixed \(k\), with

\[
\max\{q_0,\ell_0\}<T,\qquad r_0<S,
\]

then after the single fixed \(C,D\) are supplied by the assumption, choose a fixed \(k\) with

\[
\frac Ck<T-q_0,\qquad \frac Dk<S-r_0.
\]

The composed computation enters \((T,S)\) for sufficiently large \(M\).

For the project’s conservative time cap \(T=241/200\):

- from a one-full-scan baseline \(q_0=1\), it suffices at leading order to take
  \[
  k>\frac{200C}{41};
  \]
- from baseline \(q_0=6/5\), it suffices to take
  \[
  k>200C.
  \]

Thus a finite unknown \(C\) is absorbable. What is not absorbable is \(C=C_k\) with no bound on \(C_k/k\), a nonuniform family of languages/machines, or an uncharged number of calls/replays.

## Materialization floor

For every fixed \(k\),

\[
M^{1/k+o(1)}\ge \log M
\]

eventually. Indeed the exponent is eventually at least \(1/(2k)\), and \(M^{1/(2k)}/\log M\to\infty\). Therefore the required threshold floor \(p_k\ge\log M\) is compatible with fixed-\(k\) absorption. Allowing \(k=k(M)\) would require a new uniform asymptotic proof and is unnecessary here.

## Universal-solver decision

Hutter’s construction is near-fastest among algorithms with proofs of correctness and time bounds. If its best certified member runs in \(n^C\), the universal algorithm still has exponent \(C\); multiplicative constants and additive proof-search terms do not turn \(C\) into a universal small exponent. Levin search similarly addresses verifiable search/inversion with program-dependent overhead, not trustworthy arbitrary UNSAT answers. Blum speedup prevents a model-free “the fastest algorithm” principle for all computable functions.

Therefore UNIVERSAL-CERTIFIED-RACE1 is a useful firewall and possible implementation tool, but it does not close either active proof route. The correct use of the \(k\)-parameter is to absorb a fixed exponent after the existential \(P\)-algorithm is fixed.

## Primary-source model check

- MMW already constructs search-MCSP Stream-Merge using short \(\Sigma_3\mathrm{SAT}^A\) queries and derives its streaming magnification under \(P=NP\). Any use here must retain its one-pass output and update model.
- CHMY is randomized two-sided-error one-way-input/one-work-tape MCSP at a larger fixed threshold. The new base-slot erasure result removes one candidate descent only.
- OPS requires the prescribed Gap-MCSP circuit excess for every sufficiently small \(\beta\).
- Ilango’s SAT-to-MCSP result is in the random-oracle model (with a \(P/\mathrm{poly}\) reduction, uniform given oracle access). It is not a standard-model totalization.
- Conditional MKTP/McKTP theorems keep their conditional side information. A conversion to ordinary KT/MKTP without an \(M\)-bit table remains open.
- FLMV is a deterministic random-access time-space endpoint. One-tape streaming or proof-certified guest steps cannot be inserted without a charged same-machine simulation.

## Proof DAG

| Status | Arrow |
|---|---|
| ESTABLISHED | MMW Stream-Merge magnification; CHMY fixed-threshold one-tape lower bound; OPS every-small-\(\beta\) premise; FLMV random-access SAT endpoint; Hutter proof-certified near-fastest theorem; Ilango random-oracle reduction. |
| PROVED | Fixed-exponent absorption lemma and fixed-\(k\) materialization floor. |
| COMPUTATIONAL | 32,768 exact \((C,D,q)\) envelope cases, 98,304 exact inequality/minimality checks, zero failures. |
| CONDITIONAL | If one uniform all-\(k\) subroutine has fixed exponents and a fully charged bridge has suitable \(q_k,\ell_k,r_k\), choosing fixed \(k\) absorbs \(C,D\). |
| CANDIDATE | SAT \(\to R_k\) charged totalization \(\to\) ordinary KT/MKTP at \(p_k\) \(\to\) MMW \(\to\) matched SAT DTISP. |
| OPEN | Standard-model replacement for Ilango’s oracle; totalization without an \(M\)-bit side table; deterministic replay avoidance; SAT-monochromatic source-checkable fibers; uniform all-\(k\) encoding; same-machine ledger; complete ARC contractor. |
| RETIRED | Free fastest-instance chooser; claim that certified racing reduces the polynomial exponent; using \(\forall k\,\exists A_k,C_k\) as though \(C\) were uniform; base-slot CHMY injection. |

## Strongest falsifier

Produce a required bridge component whose algorithm or language depends on \(k\) so that only exponents \(C_k\) exist and \(C_k/k\not\to0\), or show that source materialization/replay creates \(q_k\ge241/200\) or \(r_k\ge1/2\). Either defeats absorption regardless of portfolio selection.

## Narrow assignments

- **:00 MCSP:** test later-\(D_i\) CHMY insertion only if both promises and the exact one-tape ledger survive; otherwise prioritize standard-model replacement for Ilango’s oracle.
- **:12 universal solver:** stop searching for a numerically fastest exponent. Prove or falsify one uniform all-\(k\) encoded language with a single \(C,D\), including proof discovery, input access, replay, interpreter, and peak space.
- **:24 ARC:** instantiate \(q_k,\ell_k,r_k\) for one complete charged \(R_k\) totalization; include table access and ordinary-KT conversion.
- **:36 red team:** force quantifiers into the order \(\exists A,C,D\,\forall k\,\forall M\); attack any hidden \(\forall k\exists A_k,C_k\), \(M\)-bit side table, random oracle, or parallel live-state cost.
- **:48 synthesis:** maintain only the two active routes and compare them by proved interfaces, not by finite experiments.

Root main.tex was not modified because it remains placeholder-truncated with unbalanced ownership markers.
