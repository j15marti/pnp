# RP-BLOCK-SPECTRAL-HEAVY-PATH42

**Timestamp:** 2026-10-21 14:48 Asia/Seoul  
**Scope:** P-vs-NP two-route synthesis plus a separate P-vs-RP proof DAG.  
**Status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Recovered state and preregistered mechanisms

This run directly reread the portfolio governance, continuity protocol,
COMPACT-HISTORY20 addendum, root `main4.tex` and `main5.tex`, the latest
accessible complete :12 report RP-REPLAY-STATE6 and its 149-record ledger,
the earlier complete :36 report RP-TRACE-FOURIER4, the 13:48 synthesis, and
the new :36 RP-BLOCK-SPECTRAL7 five-line handoff plus its 156-record cumulative
ledger. The shared fallback Google Doc was also read; its newest visible entry
remained the 2026-10-20 ARC-HEREDITARY-SCOPED10 handoff. These are targeted
reads, not a claim that all historical project bytes were reviewed.

Before the new primary-source search, four mechanisms were fixed:

1. prove a heavy accepting-path lemma with transition density
   `>1/(O(ell*w))`;
2. combine it with the Fourier small-bias error `epsilon*B`;
3. test the singleton-edge obstruction showing why low Fourier L1 alone does
   not imply hitting; and
4. keep the resulting restricted RP theorem firewalled from both open PNP
   arrows.

The first two succeed exactly in the stated block model. The third gives the
sharp scope guard. The fourth remains enforced.

## 2. Exact restricted theorem

Fix an input `x` of length `n`. An RP verifier's random tape is partitioned
into `ell=ell(n)` independent consecutive blocks. At every block boundary the
verifier is in one of at most `w=w(n)` explicitly enumerable states. For
layer `i`, state `q`, and block `r`, a total deterministic transition

`T_i(x,q,r)=q'`

is uniformly computable in polynomial time. Put

`f_{i,q,q'}(r) = 1[T_i(x,q,r)=q']`.

Assume that every such indicator has normalized Boolean Fourier spectral L1
at most a known `B=B(n)`, and that `ell,w,B` and all block lengths are
polynomially bounded.

**Theorem (ESTABLISHED, restricted).** Such an RP verifier has a uniform
deterministic polynomial-time decider. Moreover, on every YES input the
decider can reconstruct an accepting random tape.

### Proof

For an edge `(i,q,q')`, let

`p_i(q,q') = Pr_r[T_i(x,q,r)=q']`.

Set `delta=1/(4*ell*w)` and call the edge rare when `p_i(q,q')<=delta`.
At a fixed layer, conditioned on the current state `q`, the total probability
of taking a rare edge is at most `w*delta`, because there are at most `w`
destinations. Averaging over `q` preserves that upper bound. A union bound over
the `ell` layers gives

`Pr[a random execution traverses any rare edge] <= ell*w*delta = 1/4`.

On a YES input, RP acceptance has probability at least `1/2`. Therefore

`Pr[accept and traverse no rare edge] >= 1/2-1/4 > 0`.

So there exists an accepting state path every one of whose edges has density
strictly greater than `delta`.

Choose an explicit epsilon-biased set `S` for each block length with
`epsilon < delta/(2B)`. For a transition indicator `f`, normalized Fourier
expansion gives

`|E_S[f]-E_U[f]| <= epsilon * sum_{A != empty}|fhat(A)| <= epsilon*B`.

Hence every edge of density greater than `delta` is hit by `S`. Layered
reachability that enumerates `S` from every currently reachable boundary
state follows the heavy accepting path and reaches an accepting state.
For a NO input no random tape accepts, so enumeration introduces no false
positive. Storing one predecessor block per reached state reconstructs a
tape. Naor--Naor's explicit epsilon-biased construction has seed length
`O(log b + log(1/epsilon))`; with polynomial `ell,w,B,b`, the set and the
layered search are polynomial. QED.

This proof repairs the density step omitted from the short BLOCK-SPECTRAL7
handoff. It does not normalize an arbitrary RP verifier into the promised
model.

## 3. Sharp firewall: spectral L1 alone does not hit nonempty edges

For `a in {0,1}^b`, the singleton indicator `1[r=a]` has `2^b` normalized
Fourier coefficients, each of magnitude `2^-b`, and therefore Fourier L1
exactly one. Its density is only `2^-b`. Any small-bias set of size below
`2^b` can be translated so that it omits `a`; translation preserves all
parity-bias magnitudes. Thus polynomial Fourier L1 by itself does not make
every nonempty edge visible to a polynomial small-bias set.

The theorem survives because global RP mass at least `1/2`, together with only
`ell*w` opportunities to enter a rare edge, forces one accepting path whose
edges all have inverse-polynomial density. Removing the RP mass condition,
the polynomial boundary-state bound, or the known polynomial `B` invalidates
the argument.

## 4. Reproducible audit

`rp_block_spectral_heavy_path42_audit.py` uses exact rational arithmetic.
It exhausts all 13,104 binary-block layered transition systems with two states
and one to three layers (including 10,424 RP-mass cases); checks the rare-edge
union bound and heavy-path conclusion; exhausts 65,532 Boolean-function and
sample-set Fourier inequalities for dimensions one through three; checks
15,823 edge-hitting implications; and checks singleton L1 exactly through
dimension eight. Result: **104,891 assertions, zero failures**.

These computations validate finite instances of the displayed identities;
they are not the asymptotic proof and do not decide P versus RP.

## 5. Primary-source and model audit

- Naor--Naor, *Small-Bias Probability Spaces* (SIAM J. Comput. 1993), gives
  explicit epsilon-biased spaces with `O(log b+log(1/epsilon))` generating
  bits: <https://doi.org/10.1137/0222053>.
- Gill's probabilistic-machine paper is the primary one-sided-randomness
  foundation; the current theorem uses the standard zero-error-on-NO,
  at-least-one-half-on-YES RP convention:
  <https://doi.org/10.1137/0206049>.
- Impagliazzo--Wigderson is hardness-based BPP derandomization, not an
  unconditional P=RP theorem: <https://doi.org/10.1145/258533.258590>.
- CHMY STACS 2021 concerns one-way read-only input plus one work tape for
  MCSP and does not supply the missing deterministic SAT-to-ordinary-MKTP
  map: <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
- McKay--Murray--Williams gives a one-pass **search-MCSP** streaming algorithm
  using a Sigma3-SAT oracle, with target and query-length parameters that
  cannot be silently identified with this RP block theorem:
  <https://doi.org/10.1145/3313276.3316396>.
- Oliveira--Pich--Santhanam uses nonuniform circuit lower bounds for a gap
  minimization problem, not a uniform RP or ARC conversion:
  <https://doi.org/10.4086/toc.2021.v017a011>.
- Ilango's SAT reduction is relative to a uniformly random oracle (uniform
  only with access to that oracle); it is not the needed deterministic
  standard-model totalizer: <https://doi.org/10.1137/24M1652568>.
- FLMV JACM 2005 supplies the matched SAT time-space forbidden region only
  after an all-input, model-correct SAT algorithm exists:
  <https://doi.org/10.1145/1101821.1101822>.

## 6. Two independent proof DAGs

### P versus NP

1. **ESTABLISHED:** published CHMY/MMW/OPS/FLMV theorems in their own models.
2. **OPEN:** deterministic, total, both-label SAT to ordinary MKTP/MCSP with
   met threshold, source acquisition, output, and same-machine charges.
3. **OPEN:** all-input hereditary solver-dependent ARC contractor with every
   child byte, replay and peak-work-space charge.
4. **CONDITIONAL:** either completed arrow can feed its matched magnification
   or FLMV endpoint.
5. **OPEN:** P versus NP.

COMPACT-HISTORY20 remains supporting diagnostics: the compact-witness premise
is OPEN, while oracle-iteration and truth-table-history lower bounds do not
transfer to explicit succinct transitions.

### P versus RP

1. **ESTABLISHED:** RP is one-sided error; `P subseteq RP subseteq NP`.
2. **ESTABLISHED (restricted):** REPLAY-STATE6, TRACE-FOURIER4, and the present
   BLOCK-SPECTRAL heavy-path theorem derandomize their stated promised models.
3. **OPEN:** transform every RP machine uniformly into polynomially many
   explicit block states with known polynomial local Fourier L1. Quadratic
   phase and the two-axis verifier controls already prevent a syntax-only
   assertion of this step.
4. **OPEN:** uniform deterministic simulation of every RP language (`P=RP`).
5. **OPEN:** an explicit RP language outside every deterministic polynomial
   machine (`P!=RP`). SAT in RP would give `NP=RP`, not `P=RP`.

## 7. Allocation and next falsifiers

- **:00 MKTP/MCSP:** test one deterministic total both-label generator against
  the exact ordinary-KT threshold and the affine/source-conjugacy fast-forward
  controls; reject it on the first opposite-label threshold collision.
- **:12 RP separation:** present an actual language candidate and diagonal
  quantifiers over every deterministic polynomial machine; reject any claim
  that depends only on a selected verifier's trace syntax.
- **:24 ARC/FLMV:** serialize one high-width mixed child on an
  expander-incidence source and verify parent semantics plus source reads,
  replay and simultaneous peak workspace before recurrence algebra.
- **:36 RP derandomization:** attempt an arbitrary-verifier block normal form;
  the first experiment is a block-size tradeoff curve for the quadratic-phase
  verifier, measuring boundary-state count times local Fourier L1.
- **:48 synthesis:** promote BLOCK-SPECTRAL only as a restricted theorem until
  that normal form is proved; keep both PNP arrows OPEN.

No automation, role, schedule, or root `main.tex` was changed.

