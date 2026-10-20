# ADAPTIVE-TRANSCRIPT-KT-FIREWALL32

**Timestamp:** 2026-10-21 04:48 Asia/Seoul  
**Scope:** exactly two active directions: MCSP/MKTP hardness magnification and
arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint.
COMPACT-HISTORY20 remains diagnostic, not a third route.  
**Global status:** **P versus NP remains OPEN.**

## 1. Recovered state and publication safety

The proof-portfolio governance file, continuity protocol, user-specified
COMPACT-HISTORY20 addendum at commit
`c4e1f72f10976405fa2479c88499894d3d58633f`, current `main2.tex` through
`main5.tex`, recent GitHub commits, and the complete shared fallback Doc were
read. Maintained root blobs remain:

- `main2.tex`: `56464cb3d6bf9fc0b853287d1917d03bcf329ce3`
- `main3.tex`: `d82342d236feb2dcaadd03c8ae4c47a02d639137`
- `main4.tex`: `0281dcfc8833a031f2c5967a05ab7fdd8423640f`
- `main5.tex`: `05d9adae357b2970437130c3673fa2cc27e155e0`

Root `main.tex` is blob `ea1e2b3562ccd3bfb9f2c9696c7f09273462d8d1`
after another independent annotation/restoration attempt. Its own commit still
records truncation and requests full-body restoration, so it was not modified.

No new complete :00/:12/:24/:36 two-route body was visible after
`SHORT-TAG-KT-CLOSURE31`, and the fallback Doc still ends with
`ARC-HEREDITARY-SCOPED10`. The newer commit `10d9a7cb...` contains
`SUPERLOG-MARKOV1`, an exact finite-state/QBF comparison. It correctly notes
that a sufficiently small all-SAT source-only continuation compressor would
itself enter an existing FLMV forbidden region. Its code/raw are not published,
so the stated finite counts are not promoted here. It does not build the
required solver-dependent all-input ARC successor and is not a third route.

## 2. Falsifiable proposals made before literature search

1. **Source-description ceiling.** Any indexed target derived from a retained
   source has a source-hardwiring upper bound. This was found to duplicate
   `SOURCE-REFERENCE-FLOOR15` and was retired before construction.
2. **Adaptive-answer-as-advice theorem.** Hardwire the entire realized answer
   transcript of a solver-dependent compiler and replay every adaptive query.
   Falsifier: a deterministic compiler whose output cannot be reproduced from
   its base object and Boolean answer path.
3. **Quantitative high-side necessity.** If the base object and indexed replay
   cost are `o(p)`, a target with ordinary KT greater than `p` must carry
   `Omega(p)` answer/source-specific information. Falsifier: an `o(p)` answer
   path selecting a high-KT output through an `o(p)` replay algorithm.
4. **ARC transcript dichotomy.** A solver-dependent continuation quotient must
   charge query construction, answers, replay, and live state. Falsifier for a
   claimed contractor: it counts only the final short state while omitting the
   recursive SAT calls that selected it.

This run proves proposals 2 and 3. Proposal 4 is an accounting consequence,
not an ARC impossibility theorem.

## 3. Primary-source model check

- MMW STOC 2019 defines ordinary indexed `MKTP` using description length plus
  worst-case indexed output time (`c+t`). Its streaming construction begins
  with an already-present target and uses short `Sigma_3 SAT` merge queries:
  <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- CHMY STACS 2021 is a randomized one-way-read-only-input, one-work-tape result.
  It supplies no deterministic standard-model SAT-to-MKTP target constructor:
  <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
- OPS magnifies lower bounds for promise Gap-MKtP/Gap-MCSP in nonuniform
  circuit models; it is not an adaptive target totalizer:
  <https://doi.org/10.4086/toc.2021.v017a011>.
- Ilango's available SAT/MCSP hardness theorem is explicitly relative to a
  uniformly random oracle, including its uniform form with oracle access:
  <https://doi.org/10.1137/24M1652568>.
- Hutter's fastest-program theorem enumerates provably correct programs with
  proved time bounds. It neither computes a bound for every correct polynomial
  solver nor changes the KT accounting of a realized answer transcript:
  <https://arxiv.org/abs/cs/0206022>.
- FLMV JACM 2005 uses deterministic random-access machines and simultaneous
  time/space accounting. At time exponent `6/5`, Corollary 5.8 gives forbidden
  space exponent `23/45`, leaving gap `1/90` above `1/2`:
  <https://lance.fortnow.com/papers/files/tst.pdf>.
- Easy-witness results produce polynomial-size witnesses under circuit upper
  bounds; they do not establish the `tau(n)^o(1)` single-circuit premise of
  COMPACT-HISTORY20:
  <https://people.csail.mit.edu/rrw/easy-witness-nqp.pdf>.

## 4. Exact theorem: adaptive Boolean answers become target advice

### Theorem 32 (adaptive-transcript KT firewall)

Fix an efficient universal machine for ordinary indexed KT. Let a base string
`x` of length `M` have an indexed generator of description length `c_x` and
worst-case bit time `t_x`. Consider a deterministic compiler that interacts
adaptively with an arbitrary Boolean oracle for at most `h` rounds. Its query
at round `i` may depend on `x` and the preceding answers. Let
`a=a_1...a_h` be the realized answer transcript, and let the final target
`y` have length `L`.

Assume there is a uniform deterministic indexed replay procedure which, given
the generator for `x`, transcript `a`, and target index `j`, returns `y_j` in
time `R`, with no further oracle calls. Then

`KT(y) <= O(c_x+t_x+h+R+log L)`

on the fixed efficient universal machine. The hidden constant depends only on
that machine and the replay procedure, not on `x`, `a`, or `L`.

Moreover, for fixed `x` and fixed compiler/replay code, transcripts of length
at most `h` select at most `2^(h+1)-1` targets; for exactly `h` answers they
select at most `2^h` targets.

### Proof

Hardwire the base generator, the realized transcript, and self-delimiting
lengths. To output coordinate `j`, the program runs the replay procedure. When
the procedure reconstructs query `i`, all prior answers are already hardwired,
so adaptivity introduces no missing information. The program supplies the next
hardwired bit and continues. Description cost is `c_x+h+O(log L)` and the
indexed execution cost is bounded by the base and replay costs, proving the KT
upper bound. The cardinality claim follows because a deterministic replay map
has at most one output per transcript.

### Corollary 32.1 (p-scale answer/source necessity)

If `KT(y)>p` while `c_x+t_x+R+log L=o(p)`, then the hardwired transcript or
some additional non-replayed source-specific component must have
`Omega(p)` cost. In particular, an `o(p)` adaptive sequence of yes/no solver
answers cannot turn a low-KT canonical quotient into the high side of ordinary
`MKTP[p]` through an `o(p)` indexed replay procedure.

This conclusion is unaffected by how difficult it was to discover the answer
path. Discovery is charged to the reduction; target KT is allowed to hardwire
the realized path.

### Corollary 32.2 (certified universal solvers do not create target hardness)

A proof-certified fastest-correct portfolio may determine which answers are
used, but after the interaction those answers are still an advice string.
Unless the transcript/replay/source-specific component has `p`-scale cost, it
does not establish a high-KT target. This is separate from the already-settled
cofinal hardwiring fact: once a correct `R_k` exists, one unknown fixed solver
exponent can be absorbed by a sufficiently large fixed `k`.

## 5. ARC boundary and strongest challenge

The theorem does **not** rule out a solver-dependent ARC self-reduction.
An ARC compiler is allowed to query the hypothetical SAT decider on smaller
ordinary instances. The answers may select a small exact continuation state
without any need for that state to have high KT. What must be charged is:

1. serialized length and construction of every query;
2. the hypothetical solver's simultaneous time and workspace on every call;
3. retained answer transcript and ancestor state;
4. replay/access cost for the selected representation;
5. all output bytes and rejected attempts.

If a claimed ARC construction instead obtains a high-KT object from a short
transcript, Corollary 32.1 attacks it. If it only obtains a small semantic
state, the remaining test is the exact ARC recurrence and all-input hereditary
correctness, not KT.

**Strongest falsifier:** exhibit a total deterministic ordinary SAT-to-MKTP
compiler that starts from a low-KT quotient, makes `o(p)` Boolean solver calls,
has `o(p)` indexed replay, retains no other `p`-scale source component, yet
provably outputs `KT>p`. The theorem says these specifications are mutually
inconsistent.

## 6. Reproducible adversarial audit

`experiments/review/2026-10-21_adaptive_transcript_kt_firewall32.py`
exhaustively checked every answer transcript of lengths `0..10`, for two base
families and five transcript-dependent encoders. Queries at each round depended
on all prior answers.

- 2,047 transcripts;
- 36,868 adaptive-query replay checks;
- 20,470 materialized targets;
- 3,763,838 indexed-byte checks;
- 10,235 opposite-label target inequalities;
- 132 output-cardinality checks;
- zero failures.

The computation verifies the replay construction and finite cardinality bound.
It does not compute minimum KT or prove an oracle-query acquisition lower bound.

## 7. COMPACT-HISTORY20 diagnostic

Per-input or per-index answer paths instantiate `forall i exists W_i`, not the
required single `exists W forall i` circuit. A short shared transcript plus a
uniform local replay algorithm is itself a compact indexed generator, so it
cannot prove high KT. Conversely, an `Omega(p)` transcript is not automatically
a time lower bound: it may be generated from an explicit succinct transition,
as affine and modular fast-forward controls show. Exact `t` black-box queries
and `Omega(t)` truth-table history gates remain source-specific diagnostics.
The diagonal single-circuit size premise remains OPEN.

## 8. Versioned two-route proof DAG

### Route I: MCSP/MKTP

- **ESTABLISHED:** MMW ordinary-MKTP streamer and model; CHMY one-tape result;
  OPS nonuniform promise magnification; Ilango random-oracle reduction.
- **PROVED:** adaptive-transcript KT firewall and `p`-scale necessity.
- **RETIRED:** short solver-answer paths, certified one-bit decisions, or local
  replay as a source of high target KT after canonical quotienting.
- **CONDITIONAL:** once a valid cofinal `R_k` exists, one fixed unknown P=NP
  solver exponent is absorbed by a sufficiently large fixed `k`.
- **OPEN, weakest arrow:** deterministic all-input, both-label ordinary-MKTP
  totalization with an actual KT gap, charged source access/output, and no full
  side table.

### Route II: ARC/FLMV

- **ESTABLISHED:** conditional exponent recurrence and matched FLMV endpoint.
- **PROVED, restricted:** source-only exact finite-state compressors inside the
  forbidden region cannot exist; scoped sublog-width streams remain directly
  easy controls.
- **CONDITIONAL:** solver-dependent recursive queries may select continuation
  states only with complete query/answer/replay/live-space accounting.
- **OPEN, weakest arrow:** all-input hereditary successor with at most
  `N^(3/5+o(1))` ordinary children of length at most `N^(1/2+o(1))`, and
  `N^(1/2+o(1))` peak workspace.

## 9. Narrow role handoff

- **:00 MCSP:** every solver-assisted `R_k` must report answer-transcript
  length and indexed replay time. Attempt a high-side construction only if a
  source-specific component has a defensible `p`-scale KT lower bound.
- **:12 Universal Solver:** stop treating selected answers or a winner index as
  target hardness. Determine whether the certified portfolio yields a uniform
  replay bound and charge proof enumeration, cached input, and solver state.
- **:24 ARC:** build one solver-dependent ordinary child decomposition and
  publish every query length, count, answer bit, rejected branch, ancestor
  buffer, and recurrence exponent; high KT is not required for this route.
- **:36 Red team:** attack the replay assumption. Find any proposed compiler
  whose output cannot be reconstructed from base plus transcript without an
  omitted source pointer, random tape, or `p`-scale computation.
- **:48 Synthesis:** next prioritize a genuine source-specific high-side
  invariant for MCSP and a separately model-matched solver-dependent ARC child
  relation; do not conflate their requirements.

No schedule was changed and no task was created. P versus NP remains OPEN.
