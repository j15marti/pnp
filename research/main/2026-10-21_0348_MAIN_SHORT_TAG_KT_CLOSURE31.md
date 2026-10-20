# SHORT-TAG-KT-CLOSURE31

**Timestamp:** 2026-10-21 03:48 Asia/Seoul  
**Scope:** exactly two active directions: MCSP/MKTP hardness magnification and arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 remains a diagnostic workload, not a third route.  
**Global status:** **P versus NP remains OPEN.**

## 1. Recovered state and publication safety

The proof-portfolio governance file, continuity protocol, user-specified
COMPACT-HISTORY20 addendum at commit
`c4e1f72f10976405fa2479c88499894d3d58633f`, current `main2.tex` through
`main5.tex`, recent commits, and the shared fallback Google Doc were read.
The maintained root blobs are unchanged:

- `main2.tex`: `56464cb3d6bf9fc0b853287d1917d03bcf329ce3`
- `main3.tex`: `d82342d236feb2dcaadd03c8ae4c47a02d639137`
- `main4.tex`: `0281dcfc8833a031f2c5967a05ab7fdd8423640f`
- `main5.tex`: `05d9adae357b2970437130c3673fa2cc27e155e0`

Root `main.tex` is now blob `1c7d58010fff2ff3da764da46bdcf5d72bb57794`
after another independent-review annotation. It was not modified. No newer
complete two-route specialist body was visible after
`CERTIFIED-PADDING-QUOTIENT30`; the shared Doc still ends with the blocked
`ARC-HEREDITARY-SCOPED10` handoff. Commit
`c00f6467a358db814f3b9d67c34a42956e2b4fb7` is retained only as a bounded-QBF/
compact-witness comparison, not as an active third route.

## 2. Falsifiable proposals made before literature search

1. **Short semantic tag.** Append a deterministic SAT/UNSAT tag to the
   canonical quotient. Falsifier: the target program can hardwire the tag, so
   both labels remain below the ordinary-MKTP threshold.
2. **Locally indexed code expansion.** Expand the tag by a repetition, parity,
   affine, or error-correcting encoder. Falsifier: an indexed target program
   hardwires the seed/tag and computes a requested code coordinate in
   polylogarithmic time.
3. **Source-checkable hash fiber.** Use a short hash that is constant on each
   semantic source fiber. Falsifier: even if discovering the correct hash is
   SAT-hard, target KT charges the hardwired digest, while the reduction must
   separately pay discovery.
4. **ARC descriptor analogue.** Replace a child by a short descriptor plus a
   local bit generator. Falsifier: exact simulation charges generator time and
   space at every access; absent a strict ordinary-length shrink and an
   all-input hereditary compiler, no FLMV recurrence follows.

This run proves a general obstruction covering proposals 1--3 and retains
proposal 4 only as the already-known access-composition ledger.

## 3. Primary-source model check

- MMW STOC 2019 defines ordinary indexed `MKTP` using description length plus
  output time (`c+t`), distinct from `MKtP` (`c+log t`). Its Theorem 4.2 assumes
  `p(N)>=log N` and gives `O(Np)` time, `O(p)` space, with `Sigma_3 SAT` queries
  of length `O(p)`: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- CHMY STACS 2021 proves lower bounds in the one-way read-only-input,
  one-read/write-work-tape model. These do not turn a general target-KT closure
  statement into an unrestricted SAT lower bound:
  <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
- OPS concerns promise Gap-MKtP/Gap-MCSP in nonuniform circuit models, not a
  standard-model SAT-to-ordinary-MKTP totalization:
  <https://doi.org/10.4086/toc.2021.v017a011>.
- FLMV JACM 2005 uses deterministic random-access Turing machines with
  read-only input and one-way write-only output excluded from work space.
  Corollary 5.8 has forbidden space exponent
  `d=((c+2)/c^2-c)/2=23/45` at `c=6/5`:
  <https://lance.fortnow.com/papers/files/tst.pdf>.
- The easy-witness theorem derives polynomial-size witnesses from a circuit
  upper bound; it does not prove the `tau(n)^o(1)` single-history witness
  required by COMPACT-HISTORY20:
  <https://people.csail.mit.edu/rrw/easy-witness-nqp.pdf>.
- Ilango's MCSP/SAT hardness evidence is a random-oracle result and does not
  supply the missing deterministic standard-model construction:
  <https://doi.org/10.1137/24M1652568>.
- Levin's universal sequential search theorem, Hutter's proof-certified
  fastest-program construction, and Blum's axiomatic complexity/speed-up
  results do not provide a uniform numerical bound on the unknown exponent of
  an arbitrary hypothetical P=NP SAT solver. Hutter competes only with
  programs carrying the required formal correctness/time proofs, with
  program-dependent additive terms. These frameworks therefore do not turn a
  one-bit semantic tag into a high-KT target:
  <https://www.mathnet.ru/eng/ppi914>,
  <https://arxiv.org/abs/cs/0206022>, and
  <https://doi.org/10.1145/321386.321395>.

## 4. Exact theorem: short tags and local expansions remain low-KT

### Theorem 31 (short-tag KT closure)

Fix the ordinary indexed-KT universal machine used for the target problem.
Let `x in {0,1}^M` have an indexed generator of description length `c` and
worst-case bit time `t`. Let `z in {0,1}^h` be arbitrary; it may encode a
semantic fact that is expensive to discover.

1. There is an indexed program for `y=x||z` with description
   `c+h+O(log(M+h))` and worst-case bit time
   `O(t+h+log(M+h))` on a sequential universal simulation. Thus

   `KT(y) <= c+t+O(h+log(M+h))`.

2. More generally, let `E_{M,h}(z)` have output length `ell`, and suppose one
   requested bit of `E(z)` is computable uniformly from `(M,h,z,j)` in time
   `R(M,h)`. Then `y=x||E(z)` has length `L=M+ell` and

   `KT(y) <= c+h+O(log L) + O(t+h+R(M,h)+log L)`.

3. Consequently, if `c,t,h,R` are all `polylog(L)`, then
   `KT(y)=polylog(L)`. For every fixed `k`, this is eventually below
   `p_k=L^(1/k+o(1))`. Any such tagged target is therefore on the low-KT
   (ordinary-MKTP YES) side, independently of the semantic meaning of `z`.

### Proof

Hardwire the old generator, `z`, and self-delimiting encodings of the lengths.
On requested index `j`, branch on whether `j<M`. In the first case invoke the
generator for `x`; in the second, either read the hardwired tag bit or invoke
the uniform indexed encoder for `E(z)`. Sequential access to the hardwired tag
costs at most `O(h)`; random-access implementations only improve the bound.
The stated description and time bounds follow. A fixed positive power of `L`
dominates every polylogarithm, proving item 3.

The theorem is an upper bound, so no computability of the map from a SAT
instance to the correct `z` is assumed. This is precisely the firewall: target
KT can hardwire a short semantic answer even when discovering that answer
would make the proposed reduction circular. Conversely, making `E` expensive
to index or making `z` long enough to escape the bound moves the burden back to
the charged reduction and same-machine materialization ledger.

### Corollary 31.1 (failure of compact label repair after quotienting)

Take either low-KT canonical family from `CERTIFIED-PADDING-QUOTIENT30`.
Appending any `polylog(M)`-bit SAT/UNSAT certificate, digest, selector, public
seed, checksum, or fixed-size hash, and then applying any polynomial-length
locally indexed expansion, leaves both label families at `polylog(L)` ordinary
KT. Therefore a compact label tag cannot repair the missing high side.

This retires the planned “certified low-side quotient followed by a
source-monochromatic high-side code” whenever the code is locally indexed from
a short tag. A surviving bridge must retain or create source-specific
information whose indexed description-time cost exceeds the threshold, while
still being produced by a deterministic, total, charged reduction.

## 5. Reproducible audit and adversarial challenge

`experiments/review/2026-10-21_short_tag_kt_closure31.py` exhaustively checked
all tags of lengths `0..9` for both canonical labels and four encoders:

- raw append;
- length-`M` repetition expansion;
- length-`M` two-query XOR expansion;
- length-`2M` quadratic-address expansion.

It checked 8,184 materialized targets, 1,736,628 indexed output bits, 8,184
length identities, and 4,092 opposite-label inequalities, with zero failures.
The audit verifies the explicit program composition, not minimum KT.

**Strongest falsifier.** A semantically perfect tag still fails if its length
and indexed expansion cost are polylogarithmic. The cost of finding it cannot
be counted as target KT; it belongs to reduction time/space. This simultaneously
blocks short hashes, proof-certified one-bit answers, and local error-correcting
amplification after a low-KT quotient.

**Boundary not covered.** A code coordinate requiring `M^Omega(1)` source work,
a tag of polynomial length, or an output retaining incompressible source
payload need not satisfy the low-KT bound. But these are exactly the cases in
which same-machine source reads, materialization, replay, and output costs must
be charged. No such deterministic SAT-monochromatic totalization is known.

## 6. COMPACT-HISTORY20 diagnostic

The theorem sharpens the quantifier warning. `forall i exists W_i` can place a
short answer or short local witness into each per-index program, but it does
not yield the required single circuit `exists W forall i`. Conversely, a
single short tag plus a uniform local expander is itself a compact indexed
generator and hence cannot certify a high-KT target. The exact `t`-query
black-box lower bound and the `Omega(t)` truth-table history circuit lower bound
still do not transfer to explicit succinct transitions; modular increment
remains the fast-forward control. The open premise is still one
`tau(n)^o(1)` witness circuit on every specified self-padded YES input.

## 7. Versioned two-route proof DAG

### Route I: MCSP/MKTP

- **ESTABLISHED:** MMW ordinary-MKTP streamer parameters; CHMY one-tape lower
  bounds; OPS promise/nonuniform magnification in their published models.
- **ESTABLISHED:** after fixing one hypothetical P=NP solver, cofinal fixed-`k`
  hardwiring can absorb its fixed polynomial exponent, provided a valid
  ordinary-MKTP reduction already exists.
- **PROVED:** short-tag and locally indexed expansion closure (Theorem 31).
- **RETIRED:** a compact semantic label, digest, certificate, checksum, or
  locally indexed code repairs the high side after low-KT quotienting.
- **OPEN, weakest arrow:** deterministic all-input SAT-to-ordinary-MKTP
  totalization with a proved both-label KT gap at `p=M^(1/k+o(1))`, no full
  side table, and charged same-machine generation.

### Route II: ARC/FLMV

- **ESTABLISHED:** conditional ARC recurrence reaches `(6/5,1/2)`; matched
  FLMV Corollary 5.8 forbids space `n^(23/45-o(1))` at time `n^(6/5)`.
- **PROVED, restricted:** scoped/sublog-width event streams admit an iterable
  contraction; the domain is directly easy and not all-input.
- **RETIRED:** a short descriptor alone counts as an ordinary shorter SAT
  child. Virtual access must be charged per generated bit, and output remains
  part of the matched machine ledger.
- **OPEN, weakest arrow:** all-input hereditary successor for every SAT input,
  with charged acquisition, at most `N^(3/5+o(1))` children of ordinary length
  at most `N^(1/2+o(1))`, and peak space `N^(1/2+o(1))`.

## 8. Narrow role handoff

- **:00 MCSP:** abandon all `polylog`-tag local encoders. Attempt a
  source-retaining target whose high-label KT lower bound survives an explicit
  hardwiring attack; state exactly which source bits force the lower bound.
- **:12 Universal Solver:** test whether a fastest-correct certified portfolio
  supplies one uniform indexed object or merely moves an unknown exponent and
  per-instance tag into advice. Report `exists W forall i` versus
  `forall i exists W_i` explicitly.
- **:24 ARC:** for one proposed descriptor/child, measure ordinary serialized
  length and per-access generator time/space. Reject it unless the fully
  composed exponents enter the finite FLMV margin on every recursive child.
- **:36 Red team:** attack Theorem 31 under MMW's exact universal-machine
  convention and quantify simulation overhead. Seek a code whose coordinate
  cost escapes the bound without making charged reduction/materialization
  exceed the route budget.
- **:48 Synthesis:** next test source-retaining, nonlocal high-side transforms;
  require a source-checkable lower bound on ordinary indexed KT before any
  further composition with MMW.

No schedule was changed and no task was created. P versus NP remains OPEN.
