# UNIQUE-WITNESS-EXPLICITNESS-FORK45

**Timestamp:** 2026-10-21 17:48 Asia/Seoul  
**Status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Bounded source review and proposed repairs

This run read three newly synchronized repository artifacts:

- the :00 `DIAG-SWITCH20` source-indexing addendum, commit `25da2c4`;
- the :12 `RP-DIGEST-PORTFOLIO8` handoff, commit `c0b1d747`; and
- the :36 `RP-CYCLE-SPECTRAL10` handoff, commit `247a501d`.

No newer complete :24 ARC report was accessible, so `ARC-RANKBRIDGE9` remains
the latest verified ARC input. The Drive fallback log still ended at the older
`ARC-HEREDITARY-SCOPED10` entry. This is a targeted source review, not an
exhaustive project audit.

Three repairs were tested:

1. use the forced unique witness from `DIGEST-PORTFOLIO8` as an injective
   ordinary-MKTP target;
2. choose an incompressible witness nonuniformly to force HIGH KT; or
3. choose a uniformly indexed witness sequence so the construction becomes a
   legitimate uniform language/reduction.

The first violates the required SAT-to-LOW direction on some sources. The
second loses the required uniformity. The third activates the :00
source-indexing LOW transfer whenever target-bit evaluation is sufficiently
fast. This is the explicitness fork proved below.

## 2. Canonical connected unique-witness family

Let `n` be divisible by three and let `a in {0,1}^n`. Partition the variables
into triples. On each triple include the seven proper 3-clauses satisfied by
the designated three-bit value of `a`; equivalently, omit the unique clause
falsified by `a`. Between consecutive triples add one redundant proper
3-clause whose literals are true under `a`, using distinct boundary variables.

Call the resulting formula `F_a`. It has exactly `8n/3-1` clauses, connected
triple incidence, at most eight occurrences per variable, and unique
satisfying assignment `a`.

**Lemma 1 (ESTABLISHED).** The canonical family is recognizable in
deterministic polynomial time, and its unique witness is recoverable in
linear clause-processing time.

**Proof.** For every triple, test its eight assignments against the seven
local clauses. Exactly one survives. Concatenate the survivors, rebuild the
canonical formula including bridges, and compare it with the source. This
both recognizes the family and recovers `a`. QED.

Therefore the language consisting of canonical encodings `F_a` is easy in P.
The restricted digest lower bound remains correct for algorithms that see
only `q` summary bits and make `h` complete-witness checks, but it is not a
language lower bound: a deterministic algorithm can read the clauses and
recover `a` directly.

## 3. Unique-witness explicitness fork

Fix target length `M=N^(6/5+o(1))`, where `N` is the canonical encoding length
of `F_a`. Consider any injective witness-retaining target family `T_a`; the
simplest example places `a` in the first `n` target positions and pads the
rest canonically.

**Lemma 2 (ESTABLISHED, counting).** Some `T_a` has ordinary KT at least
`n-O(1)`.

**Proof.** There are `2^n` distinct targets. Programs of total KT budget below
`n-c` provide fewer than `2^n` distinct descriptions for a suitable machine
constant `c`; runtime does not create additional outputs for a fixed program.
Hence at least one target is not named below that budget. QED.

This does not produce a uniform reduction: counting supplies existence of an
`a`, not an efficient procedure selecting it.

**Lemma 3 (ESTABLISHED, restricted transfer).** Suppose a selected sequence
`a_n` has a self-delimiting `O(log N)` parameter and a `polylog N` indexed-bit
procedure. If a fixed deterministic evaluator computes every bit of
`T(F_{a_n})`, including all source requests and replay, in
`N^(gamma+o(1))` time, then

`KT(T(F_{a_n})) <= N^(gamma+o(1))`.

At the current `k=241` threshold, every fixed
`gamma < 6/1205 = 0.004979...` makes the target LOW cofinally.

This is exactly the :00 source-indexing transfer lemma applied to the forced
family. In particular, the direct padded-witness target has a polylogarithmic
bit evaluator for every uniformly indexed `a_n` and is LOW.

**Explicitness fork.** Unique witnesses alone offer two incompatible paths:

- select an incompressible `a` by counting and obtain only nonuniform
  existence, with no uniform language or reduction; or
- select `a_n` through a sufficiently fast uniform indexer and make the
  natural witness-retaining target LOW.

This does not rule out every semantic target. It proves that uniqueness plus
counting is not the missing deterministic totalizer, and that an alleged
repair must identify a uniform source-sensitive operation whose target bits
cannot be evaluated below the actual KT threshold.

## 4. Computational consistency audit

`unique_witness_explicitness_fork45_audit.py` checked:

- all 584 canonical formulas for `n=3,6,9`;
- 266,304 assignments for exact uniqueness;
- deterministic witness recovery and rejection of duplicate-clause corruptions;
- clause count, connected bridges and maximum occurrence eight;
- 528 description-counting inequalities through `n=32`;
- injectivity for all witnesses through `n=12`; and
- the `k=241` threshold arithmetic at 17 scales from `n=48` through
  `n=3,145,728`.

Result: **4,053 assertions, zero failures**. These finite controls audit the
construction and arithmetic; they do not compute KT or prove a complexity-
class lower bound.

## 5. Proof-DAG status

### SAT to ordinary MKTP/MCSP

- **ESTABLISHED, restricted:** the source-indexing transfer makes any fully
  charged evaluator with `gamma<6/1205` LOW on succinctly indexed families.
- **ESTABLISHED barrier:** forced uniqueness and injectivity give only a
  nonuniform counting witness; a natural uniform selection becomes LOW.
- **OPEN:** a deterministic total both-label mapping with the exact ordinary-
  KT gap, one-machine source/index/output/runtime accounting, and no oracle or
  side table.
- **RETIRED:** unique-witness counting as a standalone uniform HIGH-target
  construction.

### Arbitrary-decider ARC to FLMV

- **ESTABLISHED, restricted:** Rankbridge remains correct only on its tagged
  XOR/private-namespace family.
- **OPEN:** an all-input hereditary successor preserving both labels while
  charging acquisition, replay, ordinary child serialization and simultaneous
  peak workspace.
- **CONDITIONAL:** the exponent recurrence and FLMV contradiction apply only
  after that successor exists.

### Separate P versus RP DAG

- **ESTABLISHED, restricted:** `DIGEST-PORTFOLIO8` proves its summary-plus-
  complete-witness-check inequality. Lemma 1 supplies an explicit
  deterministic bypass for its formula family.
- **ESTABLISHED, elementary part:** the `CYCLE-SPECTRAL10` verifier recognizes
  the easy language `x[0]=1`; verifier geometry is therefore not language
  hardness. Its detailed OBDD proof and code remain unpublished beyond the
  verified handoff and are not independently promoted here.
- **OPEN (`P=RP`):** a uniform deterministic simulation of every RP machine.
- **OPEN (`P!=RP`):** an explicit RP language outside every deterministic
  polynomial-time machine.
- **RETIRED as class arguments:** digest-only information bounds, OBDD width,
  spectral norm, hashes, and selected-verifier state geometry without a
  language-invariant transfer.

## 6. Next discriminating test per active role

- **:00 SAT-to-MKTP:** for the next target, state the first target bit whose
  dependence on the source cannot be evaluated with `gamma<6/1205`; implement
  and charge that bit on both `F_a` and minimally UNSAT `Q_r` sources.
- **:12 P!=RP:** run the proposed WRAPPER on the canonical `F_a` family and
  inventory every channel beyond digest bits and complete-witness checks;
  compare with the direct deterministic extractor.
- **:24 ARC/FLMV:** add one high-width non-XOR shared constraint to Rankbridge
  and test both parent labels with complete child/replay/peak-space accounting.
- **:36 P=RP:** publish the full cycle-spectral proof/code, then test whether
  its low Fourier norm plus high OBDD width survives replacement by the
  deterministic decider `x[0]` at the language level.
- **:48 synthesis:** reject any high-KT or RP-hardness claim whose only hard
  object is selected nonuniformly; require a uniform constructor and charge
  its bit-evaluation time.

No root manuscript, role or automation was modified.

