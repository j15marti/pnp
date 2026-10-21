# RP-DENSITY-HITTING-TRADEOFF38

**Timestamp:** 2026-10-21 10:48 Asia/Seoul  
**Scope:** P-vs-NP two-route synthesis plus an independent P-vs-RP proof DAG.  
**Status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Recovered state and source coverage

The governance portfolio, continuity protocol, COMPACT-HISTORY20 addendum,
`main4.tex`, `main5.tex`, newest GitHub commits, current coverage ledgers, and
the shared fallback document were read. Root `main.tex` still contains an
omitted-body placeholder; this run did not edit it.

The newest :00 artifact, `DIGEST-GATE17`, falsifies a fixed 256-bit digest
generator: the digest and indexed decoder give every target polylogarithmic
ordinary KT, even if a perfect SAT label or witness tag is placed before the
hash. The latest accessible ARC synthesis remains
`ARC-EAGER-LAZY-FRONTIER34`: eager one-child materialization has a correct
resource ledger but no all-input semantic successor. The newest accessible RP
specialist artifact is `RP-SEED-CLOCK1`; it proves a public-list diagonalizer
for an easy language and exact enumeration for logarithmic coins, while
explicitly marking historical source recovery partial. The repository's
coverage JSONL files are historical and do not establish comprehensive RP
coverage; the Drive inventory is explicitly cumulative and non-exhaustive. No
new complete :12 or :36 RP body was accessible in GitHub or the fallback Doc
at read time.

## 2. Mechanisms proposed before fresh literature search

1. Generalize machine-specific RP hitting advice from acceptance probability
   `1/2` to an arbitrary one-sided density `alpha(n)`, with an exact seed-count
   bound.
2. Locate the uniformization barrier: validity of a fixed list is coNP, while
   asking whether a prefix extends to some valid list has an existential-list,
   universal-counterexample (`Sigma_2`) shape.
3. Re-test universal public lists against a verifier that rejects exactly the
   proposed list, but separately test whether the language has a deterministic
   bypass.
4. Transfer the description-length firewall to PNP: a generator retaining
   only a short digest/key cannot put its output on the high-KT side.

Mechanism 1 was selected for an exact theorem and exhaustive finite audit.

## 3. Primary-source model check

- Gill's probabilistic-machine paper (SIAM J. Comput. 1977,
  DOI `10.1137/0206049`) defines probabilistic Turing-machine resources and
  compares polynomial probabilistic classes with NP. The result below uses the
  modern one-sided RP promise: NO inputs accept on no tape; every YES input has
  accepting-tape density at least `alpha(n)`.
- Adleman's *Two Theorems on Random Polynomial Time* (FOCS 1978,
  DOI `10.1109/SFCS.1978.37`) is the classical nonuniform derandomization
  source. The theorem below is the elementary one-sided density-sensitive
  specialization; it does not provide uniform seed construction.
- MMW STOC 2019 (DOI `10.1145/3313276.3316396`) solves a specified search
  compression problem by retaining an ordinary circuit/state and using small
  `Sigma_3` queries. It does not justify replacing that state by a fixed digest.
- CHMY STACS 2021 (DOI `10.4230/LIPIcs.STACS.2021.23`) is a randomized
  one-way-input, one-work-tape MCSP lower bound at a larger threshold, not an
  RP derandomizer or small-beta transfer.
- OPS Theory of Computing 2021 (DOI `10.4086/toc.2021.v017a011`) assumes
  nonuniform Gap-MCSP/Gap-MKtP lower bounds for every sufficiently small
  parameter in the stated models.
- FLMV JACM 2005 (DOI `10.1145/1101821.1101822`) is a deterministic
  random-access simultaneous SAT time-space lower bound. An RP seed list does
  not instantiate an ARC successor.

## 4. Exact density-sensitive hitting theorem

### Theorem (machine-specific one-sided hitting advice)

Fix an input length `n` and a probabilistic verifier `M` using `r(n)` random
bits. Let `X_n` be its YES inputs of length `n`, with `m=|X_n|`. Suppose each
`x in X_n` has an accepting-tape set `A_x subseteq {0,1}^{r(n)}` of density at
least `alpha=a/q`. If

```
m (1-alpha)^t < 1,
```

then there exists a list of `t` random tapes hitting every `A_x`. Equivalently
for rational density `a/q`, the exact integer certificate is

```
m (q-a)^t < q^t.
```

The list depends on `(M,n)`. With it as advice, running `M` on every listed
tape and OR-ing the answers decides the length-`n` slice exactly, in time
`t*T_M(n)` and advice length `t*r(n)`.

### Proof

Choose `t` tapes independently and uniformly. A fixed YES input is missed with
probability at most `(1-alpha)^t`. The union bound makes the probability that
some one of the `m` YES inputs is missed strictly below one, so a good list
exists. Equivalently, at any greedy step the average tape hits at least an
`alpha` fraction of the remaining accepting sets, so some tape does; after
`t` steps fewer than one set remains. NO inputs never accept by the one-sided
promise, hence OR replay is exact. This proves the theorem.

### Corollaries and firewall

- Since `m<=2^n`, ordinary RP density `1/2` has the strict certificate `t=n+1`.
- If `alpha(n)>=1/poly(n)` and `r,T_M` are polynomial, the resulting advice is
  polynomial: this gives the scoped containment in `P/poly`.
- If `alpha=2^{-n}`, the certificate has order `n*2^n`, not polynomial. Thus a
  single random assignment on a unique-witness SAT formula is not an RP
  algorithm and cannot be imported into the RP DAG.
- Existence of the machine-specific list is nonuniform. It proves neither a
  polynomial-time constructor nor `P=RP`.

## 5. Uniformization quantifiers

For fixed polynomial-size `(M,n,H)`, a list `H` is invalid iff there exist an
input `x` and a random tape `rho` such that `M(x,rho)=1` but `M(x,h)=0` for
every `h in H`. This is an NP certificate; list validity is therefore in
coNP. Asking whether a chosen prefix extends to some valid full list adds an
existential list quantifier over a coNP predicate, giving a `Sigma_2`-type
search interface. This classification is an upper bound, not a hardness
proof. A polynomial-time uniform constructor for every RP machine would imply
`P=RP`; the converse need not produce hitting sets for each chosen verifier,
because a deterministic algorithm may bypass that verifier entirely.

Under the separate hypothesis `P=NP`, PH search collapses and RP is already
equal to P because `RP subseteq NP`; this does not resolve the unconditional
P-vs-RP question.

## 6. Reproducible adversarial audit

`experiments/review/2026-10-21_rp_density_hitting_tradeoff38.py` uses only
integer arithmetic for every certificate.

- all 34,845 nonempty families of density-constrained accepting subsets of a
  four-tape universe (`alpha=1/4,1/2,3/4`) were exhausted;
- 25,000 seeded families over an eight-tape universe were sampled at five
  densities;
- 40 exact half-density endpoint checks gave `t=n+1`;
- nine exponentially rare-density controls reached 7,095 certified tapes at
  `n=10`;
- 154,584 instrumented assertions, zero failures.

Finite checks audit the executable and boundary conventions; the analytic
proof establishes the theorem.

## 7. Separate proof DAGs

### P versus NP

**ESTABLISHED:** exact source theorems only in their MMW, CHMY, OPS, and FLMV
models; eager/lazy ARC accounting; fixed short digest implies low ordinary KT.

**CONDITIONAL:** `SAT -> charged total both-label R_k -> ordinary MKTP/KT ->
MMW -> simultaneous SAT DTISP -> FLMV`, conditional on the missing totalizer
and matched machine/resource transfer.

**OPEN:** deterministic total both-label SAT-to-ordinary-MKTP generator with
the correct threshold and no random-oracle/side-table escape; all-input,
hereditary, solver-dependent, fully charged ARC successor; COMPACT-HISTORY20's
single small `exists W forall i` circuit.

**RETIRED:** fixed digest/key generators as high-KT outputs; uncharged lazy
parent pointers; physical/output/proof-system counts as unrestricted time
bounds.

### P versus RP

**ESTABLISHED:** `P subseteq RP subseteq NP`; hence `P != RP` would imply
`P != NP`. The density-sensitive machine-specific advice theorem above and
logarithmic-coin enumeration are exact. Relativized equality and separation
worlds block purely relativizing conclusions.

**CONDITIONAL:** a uniform polynomial-time seed-list constructor for every RP
machine yields `P=RP`. A PRG/hitting-set theorem must state uniformity, seed
length, one-sided preservation, oracle access, and construction cost.

**OPEN:** an actual uniform language in `RP` outside every deterministic
polynomial-time machine, or a uniform deterministic simulation of every RP
machine.

**FALSIFIED/RETIRED:** “SAT in RP implies P=RP” (it gives `NP=RP`, not P=RP);
machine-independent public seed lists; treating exponentially rare witnesses
as RP; interpreting `RP subseteq P/poly` as uniform derandomization.

## 8. Single highest-value next experiment per active route

- **:00 PNP/MKTP:** replace the fixed digest by a growing retained state and
  compute an exact ordinary-KT upper bound including state bits, decoder,
  index, and runtime; reject the candidate unless one source label can still
  be proved above the target threshold on all inputs.
- **:24 PNP/ARC:** implement one proposed semantic child family by eager
  sequential materialization and attack it with the matched minimally-UNSAT
  and Horn/affine gluing pairs while recording source reads, rejected children,
  replay, ancestor bytes, and both labels.
- **:12 RP separation:** attempt a uniform diagonal RP language whose YES
  witness density is inverse-polynomial and whose membership definition does
  not contain an easy deterministic bypass; explicitly test uniformity and
  nonrelativizing dependence.
- **:36 RP derandomization:** implement lexicographic seed-list construction
  through the exact validity predicate and record which oracle level each
  prefix-extension query requires; a true repair must eliminate that oracle
  uniformly rather than hide it in advice.

No schedule was changed and no extra route was created.

