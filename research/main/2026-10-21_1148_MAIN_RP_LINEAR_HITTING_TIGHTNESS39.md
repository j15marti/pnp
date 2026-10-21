# RP-LINEAR-HITTING-TIGHTNESS39

**Timestamp:** 2026-10-21 11:48 Asia/Seoul  
**Scope:** P-vs-NP two-route synthesis plus a separate P-vs-RP proof DAG.  
**Status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Recovered state and source coverage

This run reread the portfolio governance, continuity protocol,
COMPACT-HISTORY20 addendum, current `main4.tex`/`main5.tex`, latest GitHub
commits, and the shared fallback document. Root `main.tex` was externally
restored to the full MERGEGUARD1 body at commit `7f588300`; this run did not
edit it. The previously requested coverage-ledger paths were not present at
the current GitHub paths; the newest :12 short handoff says its 146-record
historical ledger remains unsynced. Accordingly, no comprehensive-source
claim is made.

The newest accessible :12 result is `RP-BOOLEAN-QUOTIENT5` (commits
`4fae3d6a`, `f69399ec`, `ef44be57`). It proves that the naive product of CNF
clause polynomials is formally nonzero even for UNSAT proper CNFs, so field
evaluation violates RP soundness. Separately it gives a uniform RP algorithm
for low-degree arithmetic circuit NONIDENTITY over a suitably large explicit
prime field, with one-sided success at least `49/64`; no deterministic lower
bound is supplied. The exact local audit reported 296,860 checks and zero
failures, but its full code and historical ledger were not remotely
accessible at read time.

The latest accessible :00 PNP result remains `DIGEST-GATE17`: fixed 256-bit
hash/state outputs have low ordinary KT on both labels. The latest accessible
ARC synthesis remains `ARC-EAGER-LAZY-FRONTIER34`: the eager materialization
ledger is quantitatively correct but lacks an all-input semantic successor.
No newer complete :24 or :36 specialist body was accessible in GitHub or the
fallback Doc at read time.

## 2. Mechanisms proposed before fresh literature search

1. Model an RP verifier's accepting tapes as affine halfspaces
   `A_x={r:<x,r>=1}` and determine the exact minimum machine-specific hitting
   list.
2. Compare that hitting complexity with the deterministic complexity of the
   recognized language, on the same uniform verifier.
3. Recheck whether amplification helps after charging every repeated random
   bit and whether it changes uniform seed acquisition.
4. Use affine/rank behavior only as a diagnostic in the PNP DAG; do not
   promote it to ordinary-KT or unrestricted SAT-time hardness.

Mechanisms 1 and 2 were selected for an exact theorem and executable audit.

## 3. Primary-source model check

- Gill, *Computational Complexity of Probabilistic Turing Machines*, SIAM J.
  Comput. 6(4), 1977, DOI `10.1137/0206049`, supplies the probabilistic-TM
  setting. The verifier below has one-sided error, exactly `n` coin bits and
  uniform linear-time parity evaluation.
- Adleman, *Two Theorems on Random Polynomial Time*, FOCS 1978, DOI
  `10.1109/SFCS.1978.37`, is the classical nonuniform derandomization source.
  Its advice conclusion does not identify the accepting tapes of a selected
  verifier with the intrinsic complexity of its language.
- MMW, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong
  Separations*, STOC 2019, DOI `10.1145/3313276.3316396`, Theorems 1.2--1.3,
  uses a one-pass **search-MCSP** streamer with ordinary retained state and
  short `Sigma_3-SAT` oracle queries. A hitting-list rank bound is not an MMW
  streaming lower bound.
- CHMY, STACS 2021, DOI `10.4230/LIPIcs.STACS.2021.23`, concerns randomized
  one-way-input/one-work-tape MCSP at specified thresholds. It supplies no
  verifier-invariant RP hitting theorem.
- OPS, Theory of Computing 17(11), 2021, DOI
  `10.4086/toc.2021.v017a011`, states nonuniform Gap-MCSP/Gap-MKtP
  magnification hypotheses. Affine acceptance rank is not circuit excess.
- FLMV, JACM 52(6), 2005, DOI `10.1145/1101821.1101822`, is a deterministic
  random-access simultaneous SAT time-space lower bound. Neither RP advice
  nor affine rank supplies the missing all-input ARC contractor.

## 4. Exact linear hitting tightness theorem

For each length `n>=1`, let the language be all `n`-bit strings. Define the
uniform RP verifier, for `x,r in F_2^n`, by

```
M(x;r) = 1                    if x=0,
         <x,r> mod 2          if x!=0.
```

Every input is a YES input. For `x=0` all tapes accept. For every nonzero
`x`, exactly half of the `2^n` tapes accept, so the verifier satisfies the
ordinary RP density promise.

### Theorem

A seed list `H subseteq F_2^n` hits every input of length `n` if and only if
`span(H)=F_2^n`. Consequently its minimum number of seeds is exactly `n`, or
`n^2` advice bits when the seeds are written explicitly.

### Proof

If `span(H)` is proper, its orthogonal complement contains a nonzero vector
`x`. Then `<x,h>=0` for every `h in H`, so the verifier rejects `x` on the
entire list. Conversely, if `H` spans the space, then for every nonzero `x`
some `h in H` has `<x,h>=1`; otherwise `x` would be orthogonal to the whole
space. The zero input accepts every nonempty list. A basis has `n` seeds, and
fewer than `n` vectors cannot span. This proves the theorem.

### Consequence: verifier/language firewall

The recognized language is `Sigma*`, decided deterministically by one accept
state without inspecting the verifier's seed geometry. Thus even an exact,
asymptotically tight lower bound on the number of accepting tapes needed to
hit **a chosen RP verifier** is not a deterministic lower bound for its
language. The earlier `n+1` union-bound upper bound is tight up to one seed in
this verifier-respecting sense, yet provides no evidence for `P!=RP`.

This also audits the newest arithmetic-NONIDENTITY candidate: proving a
hitting-set lower bound for its Schwartz--Zippel verifier would not by itself
prove that NONIDENTITY is outside P. A language-level all-deterministic
lower-bound arrow remains necessary.

## 5. Reproducible audit

`experiments/review/2026-10-21_rp_linear_hitting_tightness39.py` uses an
independent Gaussian-elimination rank calculation and direct verifier replay.

- every one of 65,812 seed subsets was exhausted for `1<=n<=4`;
- all 340 input/random-tape pairs in those dimensions were checked for the
  exact density (`1` for zero, `1/2` otherwise);
- 40,000 seeded lists were sampled for `5<=n<=12`;
- the canonical basis hit every input and every strict prefix failed;
- 105,870 instrumented assertions, zero failures.

The finite audit checks implementation and boundary conventions. The written
linear-algebra proof establishes the all-`n` theorem.

## 6. Separate proof DAGs

### P versus NP

**ESTABLISHED:** the source-specific MMW, CHMY, OPS and FLMV theorems only in
their stated models; fixed digest/state yields low ordinary KT; the ARC eager
resource ledger is correct as accounting.

**CONDITIONAL:** `SAT -> charged deterministic total both-label R_k ->
ordinary MKTP/KT threshold -> MMW streamer -> simultaneous SAT DTISP -> FLMV`,
conditional on the missing totalizer, threshold and same-machine transfers.

**OPEN:** deterministic total both-label SAT-to-ordinary-MKTP construction
without random-oracle, side-table or virtual-input leakage; all-input,
hereditary, solver-dependent and fully charged ARC successor; the
COMPACT-HISTORY20 single `exists W forall i` small circuit.

**RETIRED:** fixed hashes/digests as high-KT generators; affine rank, output
materialization, physical counts or proof-system bounds as unrestricted
machine-time lower bounds.

### P versus RP

**ESTABLISHED:** `P subseteq RP subseteq NP`, so `P!=RP` would imply `P!=NP`.
Arithmetic circuit NONIDENTITY in the :12 scope is in RP. Machine-specific
one-sided hitting advice exists nonuniformly. The theorem above proves its
linear seed-count upper bound can be essentially tight even for `Sigma*`.

**CONDITIONAL:** a uniform polynomial-time hitting-list constructor for every
RP verifier gives `P=RP`; a PRG/hitting theorem must expose seed construction,
one-sided preservation, oracle use and total cost.

**OPEN:** either an explicit uniform language in `RP` outside every
deterministic polynomial-time machine, or a uniform deterministic simulation
of every RP machine. Deterministic PIT for one arithmetic model would not by
itself settle the class equality.

**FALSIFIED/RETIRED:** naive CNF clause-product arithmetization as an RP SAT
algorithm; `SAT in RP => P=RP`; universal public lists; verifier-specific
hitting-set size as a language lower bound; relativizing or finite evidence as
an unrestricted separation.

## 7. Highest-value next experiment per active route

- **:00 PNP/MKTP:** for a growing retained state, compute the exact ordinary
  KT upper bound including source reads, state bits, index decoder and runtime;
  reject it unless one label is proved above the target threshold on every
  source input.
- **:24 PNP/ARC:** instantiate one high-width global semantic child relation,
  eagerly serialize it, and attack both labels with matched minimally-UNSAT,
  Horn and affine gluing pairs while charging rejected children and ancestor
  storage.
- **:12 RP separation:** treat arithmetic NONIDENTITY only as an explicit RP
  member; attempt a language-level diagonal lower-bound interface and record
  exactly where it relativizes or introduces an easy deterministic bypass.
- **:36 RP derandomization:** test whether a proposed uniform simulator is
  invariant under verifier rewrites that preserve the same language but
  radically change accepting-tape geometry; failure on the affine `Sigma*`
  verifier retires verifier-respecting necessity claims.

No schedule or agent role was changed and no extra route was created.

