# LOW-SIDE-ORBIT-COLLAPSE29: a quantitative same-label quotient obligation for SAT-to-MKTP

**Timestamp:** 2026-10-21 01:48 Asia/Seoul  
**Scope:** the two active directions only: MCSP/MKTP hardness magnification and arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 remains a diagnostic sublemma.  
**Global status:** **P versus NP remains OPEN.**

## Executive result

This run converts the newest online-braid and sampled-assignment failures into
one exact, representation-independent necessary condition.

Let

```text
O = {F_z : z in {0,1}^r}
```

be a family of source instances with the same SAT label, and let `R` be a
deterministic target generator. If every member of `O` must land in a low
target set `L` of cardinality `B`, then some target has at least

```text
ceil(2^r/B)
```

preimages in the orbit. Equivalently, if every fiber on `O` has size at most
`2^h`, at most `B*2^h` members of `O` can land low.

For ordinary fixed-length `MKTP[p]`, where a description of length `c` prints
an indexed output bit within `t` steps and `c+t<=p`, a conservative count is

```text
B_p <= (p+1) 2^(p+1).
```

Thus whichever SAT label is mapped to `KT<=p` must contain fibers of size at
least `2^r/B_p` on every `2^r` padding orbit of that label. If the payload is
recoverable from the target, the map is injective on that orbit and necessarily
maps some same-label source above threshold once `2^r>B_p`.

The complementary reduction obligation is exact: opposite SAT labels may
never collide, because a deterministic target decision cannot assign two
answers to one target. Therefore a valid SAT-to-MKTP reduction must be
simultaneously:

1. highly many-to-one on large low-label padding orbits; and
2. perfectly label-monochromatic across every target fiber.

This is a quantitative quotient specification, not an impossibility theorem.
A padding canonicalizer can satisfy the first condition. No construction is
known that also satisfies the second, proves the high-KT side, gives strict
threshold descent, and meets the required machine ledger.

## Recovered live state

The governing proof-portfolio file, continuity protocol, COMPACT-HISTORY20
addendum at the specified commit, current `main2.tex` through `main5.tex`, the
newest GitHub commits, and the shared fallback Google Doc were read. The
maintained root blobs remain:

| file | Git blob |
|---|---|
| `main2.tex` | `56464cb3d6bf9fc0b853287d1917d03bcf329ce3` |
| `main3.tex` | `d82342d236feb2dcaadd03c8ae4c47a02d639137` |
| `main4.tex` | `0281dcfc8833a031f2c5967a05ab7fdd8423640f` |
| `main5.tex` | `05d9adae357b2970437130c3673fa2cc27e155e0` |

The newest substantive specialist file is `MKTP-ONLINE-BRAID11`, Git commit
`29d0c543b51a0e259c75c3f22fb9088dad2ae198`. It records two falsified
candidates:

- **ONLINE-BRAID:** a complete one-way source scan expands to
  `M=N^(6/5+o(1))`, but the target retains each source bit at a known index.
  Both labels have explicit easy families, while either label also has
  independent payload orbits whose targets are recoverable and therefore
  mostly high-KT by counting.
- **EVAL-SAMPLER:** actual evaluation on `q=N^(1/5)` assignments charges
  `(q+1)N` source reads and `q` rewinds, but equal-size SAT and UNSAT sources
  can have identical all-zero sample traces and identical targets.

The specialist status reports 7,312 and 1,880 assertions respectively with
zero failures, but its executable and raw ledger were not included in the
commit. Those numerical claims were not independently rerun here. No newer
complete :12, :24 or :36 scientific body was visible in GitHub or the fallback
log. The subsequent repository changes are independent review annotations;
root `main.tex` remains placeholder-bearing and was not modified.

## Falsifiable variants proposed before literature

1. **Low-side orbit collapse:** quantify how much any correct low-side target
   must collapse an arbitrary same-label padding orbit.
2. **Recoverability firewall:** prove that decoding the payload from the target
   already falsifies an all-input low-KT promise, without needing an explicit
   incompressible payload.
3. **Certified canonicalization:** quotient only syntactically certified
   padding and challenge the result on an opposite-label matched pair; charge
   any semantic normalization separately.
4. **ARC analogue:** require invariance under irrelevant source padding or
   charge the retained payload in children, without treating this necessary
   representation condition as an all-input contraction theorem.

The first two are proved below. The third remains a construction target. The
fourth is retained only as a falsifier for ARC proposals.

## Primary-source alignment

- McKay--Murray--Williams defines `MKTP[p]` using indexed bit production with
  `c+t<=p`, requires `p>=log N`, and Theorem 4.2 supplies an
  `O(Np)`-time, `O(p)`-space streamer using ordinary `Sigma_3-SAT` queries of
  length `O(p)`. It starts with an already present target string; it does not
  construct `R_k` or canonicalize source padding.
  <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>
- Oliveira--Pich--Santhanam explicitly studies promise
  `Gap-MKtP[s_1,s_2]` and `Gap-MCSP[s_1,s_2]` in specified nonuniform models.
  The orbit theorem is not one of the required lower bounds.
  <https://theoryofcomputing.org/articles/v017a011/>
- Cheraghchi--Hirahara--Myrisiotis--Yoshida uses a one-way read-only input and
  one two-way work tape. A full source scan is permitted, but target
  recoverability and semantic correctness remain separate obligations.
  <https://doi.org/10.4230/LIPIcs.STACS.2021.23>
- Ilango's 2026 theorem gives the reduction relative to a uniformly random
  oracle, with heuristic hash instantiations offered as candidates. It does
  not establish the deterministic standard-model quotient needed here.
  <https://doi.org/10.1137/24M1652568>
- Hutter's fastest-program guarantee enumerates proofs of correctness and time
  bounds; it deliberately excludes unproved correct programs. It neither
  canonicalizes SAT padding nor extracts the exponent of every hypothetical
  polynomial decider. <https://arxiv.org/abs/cs/0206022>
- Easy-witness results derive compact witnesses from circuit-upper-bound
  hypotheses. They do not supply COMPACT-HISTORY20's source-specific
  `exists W forall i` premise for free.
  <https://eccc.weizmann.ac.il/report/2017/188/>
- FLMV remains a simultaneous time-space theorem for deterministic
  random-access SAT computation; a quotient condition alone does not enter
  its forbidden region. <https://doi.org/10.1145/1101821.1101822>

## Formal theorem

### Theorem 29A — low-side orbit-collapse bound

Let `O` be a finite set of size `2^r`, let `R:O->Y` be deterministic, and let
`L subseteq Y` have size `B`. If `R(O) subseteq L`, then

```text
max_{y in L} |R^{-1}(y) intersect O| >= ceil(2^r/B).
```

More generally, if every fiber of `R` on `O` has size at most `2^h`, then

```text
|{x in O:R(x) in L}| <= B 2^h.
```

**Proof.** The sets `R^{-1}(y) intersect O`, for `y in L`, partition the
low-mapped part of `O`. Summing at most `B` fibers each of size at most `2^h`
gives the second inequality. If all `2^r` sources map into `L`, averaging over
at most `B` nonempty fibers gives the first. QED.

### Corollary 29B — indexed-MKTP instantiation

Fix target length `M` and threshold `p`. For each program-description length
`c<=p`, there are fewer than `2^(c+1)` binary descriptions and at most `p+1`
admissible integer time charges. Hence the number `B_p` of length-`M` targets
with indexed KT cost at most `p` obeys the deliberately generous bound

```text
B_p <= (p+1) 2^(p+1).
```

Applying Theorem 29A, an entire `2^r` low-label source orbit requires a fiber
of size at least

```text
ceil(2^r / ((p+1)2^(p+1))).
```

If a decoder recovers `z` from `R(F_z)`, the restriction of `R` to the orbit
is injective. Therefore at most `B_p` orbit members can map into `MKTP[p]`,
and all-input low-side correctness fails whenever `2^r>B_p`.

### Theorem 29C — explicit proper-3CNF orbits on both labels

For every `r>=0`, there are ordered proper-3CNF families

```text
{S_z:z in {0,1}^r} subset SAT,
{U_z:z in {0,1}^r} subset UNSAT
```

with `8+r` clauses and `3+3r` variables, and with `z` recoverable from clause
signs.

**Construction.** On variables `x,y,z`, the conjunction of all eight sign
patterns is UNSAT: each assignment falsifies one of the clauses. Removing one
pattern and duplicating another leaves eight proper clauses with a satisfying
assignment. For payload bit `i`, use fresh variables `a_i,b_i,c_i` and select

```text
(a_i OR b_i OR c_i)       if z_i=0,
(a_i OR b_i OR NOT c_i)   if z_i=1.
```

Setting every `a_i=1` satisfies all payload clauses, so they preserve the SAT
core's witness; they cannot repair the complete UNSAT core. The sign of
`c_i` recovers `z_i`. Conventional ordered encodings use `Theta(r log r)`
bits. QED.

Whichever source label a many-one reduction maps to the low-MKTP side can be
paired with the corresponding orbit in Theorem 29C.

## Composite consequence and challenge

The result places the three newest constructions on one exact spectrum:

| construction | same-label collapse | opposite-label separation | descent |
|---|---|---|---|
| ONLINE-BRAID | fails: payload recoverable | not established | proposed, but semantically invalid |
| EVAL-SAMPLER | may collapse samples | fails: identical opposite-label target | none |
| fixed-coordinate erasure | exact on chosen syntactic orbit | only with additive gap | exponent preserved |

The surviving object is a **label-respecting quotient**: it must discard
arbitrarily large irrelevant degrees of freedom on the low label while
retaining enough source semantics that no opposite-label pair collides. It
must additionally produce a genuinely high-KT target on the other label.

This theorem does not rule that object out. Syntactically marked padding can
be stripped cheaply. No inference is made that semantic canonicalization is
hard for every algorithm; proving such an all-algorithm cost would itself be
a major missing lemma.

Randomized reductions are also outside the deterministic fiber statement:
per-input success does not provide one seed correct on all orbit members.
Advice containing orbit-specific payload information must be stated and
charged separately.

## Reproducible audit

`experiments/review/2026-10-21_low_side_orbit_collapse29.py` completed
**1,465,913 checks with zero failures**:

- every one of 72,748 maps in the exhaustive small regime;
- every low-target subset in that regime;
- 21,824 larger affine/folded/nonlinear deterministic maps;
- 9,344 exact integer KT-cardinality and ceiling cases;
- explicit SAT and UNSAT proper-3CNF payload orbits through `r=12`, including
  properness, witnesses, complete UNSAT cores, exact recovery, and `2^r`
  distinct encodings.

The program checks finite controls. The general result is the counting proof.

## Two-route proof DAG

### Route 1 — MCSP/MKTP magnification

- **ESTABLISHED:** low-side orbit-collapse theorem; recoverability firewall;
  explicit same-label SAT and UNSAT padding orbits.
- **ESTABLISHED downstream:** MMW Theorem 4.2 has `O(p)` queries and
  `O(Np)` time/`O(p)` space before replacing its PH oracle. A cofinal family
  can hardwire one fixed `k>C` after fixing a hypothetical solver; no exponent
  extractor is needed.
- **FALSIFIED/RETIRED:** payload-recoverable ONLINE-BRAID; sampled-assignment
  semantics; fixed-coordinate erasure as strict descent; proof-certified
  fastest solver as a way to cover every correct polynomial decider.
- **OPEN weakest arrow:** a deterministic standard-model, total, both-label
  ordinary SAT-to-indexed-MKTP quotient `R_k` that is padding-invariant on the
  low side, opposite-label separating, high-KT on the other side, in-order,
  and fully charged without an `M`-bit side table.

### Route 2 — ARC into FLMV

- **ESTABLISHED:** status-only strict-subformula projections collide on matched
  minimal-UNSAT controls; selector materialization and cache/replay costs have
  explicit scoped firewalls.
- **COMPUTATIONAL:** scoped fixed-depth event-stream recursion remains exact
  only on an already easy promise class.
- **CANDIDATE diagnostic:** require ARC children to be invariant under
  irrelevant source padding or charge the retained payload. This does not
  transfer Theorem 29A into a machine lower bound.
- **OPEN weakest arrow:** from an arbitrary polynomial SAT decider to one
  hereditary, all-input successor with acquisition, construction, selection,
  replay, output and peak live bits jointly charged in the FLMV model.

### COMPACT-HISTORY20 supporting diagnostic

- **CONDITIONAL:** the diagonal implication assumes one circuit `W` of size
  `tau(n)^o(1)` satisfying all indexed clauses on the specified self-padded
  YES sources.
- **OPEN:** existence of that circuit with quantifiers `exists W forall i`.
- **ESTABLISHED non-implication:** per-index witnesses, value-oracle iteration
  bounds, full-table counting and same-label quotienting do not prove that
  compactness; succinct modular increment remains a fast-forward control.

## Allocation

- **:00 MCSP:** implement one target bit predicate invariant under the explicit
  SAT/UNSAT payload orbits, then attack it with an opposite-label matched pair.
  Give both KT promises before the machine ledger.
- **:12 Universal Solver:** prove the exact low-target count for the selected
  universal-machine convention and compose it with fixed-`k` hardwiring. Do
  not attempt a total exponent extractor.
- **:24 ARC:** add irrelevant-clause padding to the next candidate successor;
  measure whether output children collapse it or retain it, then separately
  test the minimal-UNSAT pair.
- **:36 Red team:** challenge ordered encoding, duplicates, the program/time
  code count and polarity. Seek a canonicalizer that meets both quotient
  obligations, since that would falsify the barrier's practical reach without
  contradicting the theorem.
- **:48 Synthesis:** require every new `R_k` to report orbit fiber size,
  opposite-label collision tests, target length, `p>=log M`, source/output
  traffic and peak workspace before invoking MMW or OPS.

No all-algorithm separation follows. **P versus NP remains OPEN.**
