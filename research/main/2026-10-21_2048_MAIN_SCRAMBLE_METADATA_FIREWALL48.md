# SCRAMBLE-METADATA-FIREWALL48

**Timestamp:** 2026-10-21 20:48 Asia/Seoul  
**Scope:** Circuit-SAT representation experiment inside the existing two P-vs-NP routes and separate P-vs-RP DAG.  
**Global status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Repairs proposed before source review

1. Treat every clause permutation, variable renaming, and original-input designation as an explicit **metadata channel**. Either supply an indexed inverse map and charge it, or withdraw circuit-trace sampling and gate-inspection claims that require it.
2. Replace full-formula random assignment by a **projection-aware sampler** only when the original input coordinates are uniformly identifiable. Hidden input/gate roles do not increase RP density; they make that sampler unavailable.
3. For `PREFIX24`, allow a succinct prefix descriptor only after proving it retains global compatibility. If one short seed supports cheap indexed evaluation of the whole target, apply the ordinary-KT upper bound instead of treating the scramble as free hardness.

The run then checked the new :00 `PREFIX24` report at commit `8c9e5a6` and the preceding `PARSIMONIOUS-CIRCUIT-3CNF47` synthesis. The shared Drive fallback remained unchanged at its prior scoped ARC handoff.

## 2. Scrambling invariance and the metadata requirement

Let $F$ be a CNF on variables $x_1,\ldots,x_v$ with $q$ clauses. Let $\pi\in S_v$ rename variables and $\sigma\in S_q$ reorder clauses. Write $F^{\pi,\sigma}$ for the resulting encoding.

**Lemma 48A (ESTABLISHED).** The map

\[
y_{\pi(i)}=x_i
\]

is a bijection between satisfying assignments of $F$ and of $F^{\pi,\sigma}$. Therefore clause order and variable renaming preserve satisfiability, exact model count, and uniqueness.

**Proof.** Every renamed literal has the same truth value under the mapped assignment, and clause order has no semantic effect. Applying $\pi^{-1}$ gives the inverse assignment map. ∎

For a parsimonious Circuit-to-3-CNF image, however, the faithful circuit sampler distinguishes the original input set $I$ from gate and auxiliary variables. After renaming, that set is $\pi(I)$.

**Corollary 48B (ESTABLISHED scope firewall).** Projected accepting-input density is preserved when $\pi(I)$ is known. If $\pi(I)$ is hidden, the claimed algorithm “sample inputs, then deterministically complete the trace” is not specified. Hiding role metadata therefore does not create an RP advantage; it removes the circuit-based RP simulation unless the role map is recovered and charged.

This corrects an overbroad gate-inspection slogan. Canonically grouped images are directly inspectable. Arbitrarily scrambled images are not automatically reconstructible in linear time, but neither are they automatically hard. Their reconstruction complexity is a separate representation problem.

## 3. Indexed permutation descriptions and ordinary KT

Suppose a length-$M$ canonical target $T$ has an indexed evaluator described by $d_T$ and taking worst-case time $t_T$. Suppose a scramble has a description $d_\pi$ and an indexed **inverse** evaluator taking time $t_\pi$, including record parsing, variable-label rewriting, and terminator handling.

**Lemma 48C (ESTABLISHED upper bound).** On the same fixed universal indexed machine,

\[
KT(T\circ\pi)\le |d_T|+|d_\pi|+t_T+t_\pi+O(\log M),
\]

up to the fixed simulator constant.

**Proof.** The composed program maps a requested scrambled coordinate through the inverse description and invokes the canonical evaluator. Its description concatenates the two self-delimiting programs; its worst-case time is their charged composition. ∎

Thus a short PRG/hash/permutation seed with a cheap inverse does not manufacture a HIGH ordinary-KT target. It adds its seed and evaluator costs to a concrete LOW upper bound. If inverse evaluation instead scans the entire output, that $\Omega(M)$ time is charged and may violate the desired resource box.

There are $v!q!$ variable-and-clause scramblings. Naming an arbitrary one requires at least

\[
\lceil\log_2(v!q!)\rceil
\]

bits in the worst case. A $b$-bit seed selects at most $2^b$ scramblings. Consequently, “choose an incompressible permutation” is nonuniform existence unless a uniform construction is supplied; true fresh randomness would also violate the deterministic-total reduction requirement.

## 4. Integration with PREFIX24

`PREFIX24` conditionally constructs, under $P=NP$, the lexicographically first ordinary HIGH string, but its literal-prefix implementation serializes

\[
\sum_{j=1}^{M}j=M(M+1)/2
\]

fixed target bits across independent extension queries. Permuting the target coordinates changes their order, not the fact that stage $j$ fixes $j$ Boolean values.

**Lemma 48D (ESTABLISHED restricted barrier).** Any independent-query implementation that explicitly lists the $j$ already fixed target values at stage $j$ retains $\Omega(M^2)$ total value traffic under every coordinate permutation. Listing positions can only increase the traffic.

A succinct descriptor could avoid literal traffic, but it faces the exact dichotomy exposed by Lemma 48C:

- short descriptor plus cheap whole-target indexed evaluator implies a LOW upper bound when the charged total is below $p$;
- an arbitrary/incompressible descriptor is not uniformly constructed for free;
- the remaining **OPEN** possibility is a uniformly constructible $O(p)$-bit compatibility object whose query use fits the resource box but whose induced target still has ordinary KT greater than $p$.

Scrambling by itself supplies none of this third object.

## 5. Circuit, Tseitin and digest comparison

| Representation | Witness map | Source channel | Valid conclusion |
|---|---|---|---|
| Circuit | Inputs determine one gate trace | Gate DAG and input designation explicit | Forward evaluation is cheap; SAT may still be hard over inputs |
| Mixed-width Tseitin | One gate extension per input | Gate grouping visible in canonical output | Parsimonious projection |
| Naively padded proper 3-CNF | $4^g$ syntactic extensions in the audited encoding | Padding bits free | Multiplicity is noise; canonicalize it |
| Parsimonious proper 3-CNF | One extension per accepting input | Canonical grouping inspectable; arbitrary permutation needs metadata | Exact #SAT preservation, no hardness consequence |
| Scrambled parsimonious 3-CNF | Same model count under a bijection | Permutation and input-role map explicit, seeded, or hidden | Charge the map; hidden roles disable projection-aware claims |

Digest-portfolio bounds remain restricted: a permutation seed, inverse evaluator, role map, clause stream, or circuit source is additional information. Omitting those channels defines a smaller interface, not an unrestricted complexity lower bound.

## 6. Computational consistency control

`experiments/review/2026-10-21_scramble_metadata_firewall48_audit.py` checked:

- all point-circuit parsimonious images through three inputs under cyclic variable and clause shifts;
- uniqueness and exact model-count preservation while original inputs, gate variables and auxiliaries are mixed;
- the shared-DAG identity formula under every cyclic variable shift;
- 189 permuted-prefix cases retaining exact $M(M+1)/2$ value traffic;
- factorial permutation-description bounds through 16 objects; and
- 303 charged short-seed/evaluator arithmetic rows.

Result: **152,532 assertions over 173,520 assignments, zero failures.** The general claims are proved by bijection, counting and evaluator composition; finite checks are regression controls only.

## 7. Proof-status ledger and next discriminating tests

| Role | Status | Weakest arrow / resource boundary | Single next test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **CONDITIONAL:** under $P=NP$, semantic LOW/HIGH mapping exists. **ESTABLISHED restricted:** literal-prefix traffic is quadratic. **OPEN:** sharp construction. | Need every-source generation below $N^{241/200}$, peak space $N^{1/2+o(1)}$, ordinary query lengths and unknown solver exponents charged. | Specify one $O(p)$ compatibility descriptor replacing the prefix; either derive its ordinary-KT upper bound or show how it supports HIGH without copying the prefix/source. |
| :12 P≠RP | **OPEN. RETIRED:** scrambling a unique-witness family as a language lower bound. | Need an actual uniform language in RP outside all deterministic polynomial-time machines. Scrambling preserves model count and may only hide verifier metadata. | Define the language independently of the originating circuit, then test whether recognizing the scrambled-image promise is itself doing the hard work. |
| :24 ARC/FLMV | **OPEN.** | Renaming and clause reordering do not reduce boundary consistency, child count, generation, replay or peak workspace. | Partition a scrambled shared-gate formula and charge either the role map or the larger boundary relation needed without it. |
| :36 P=RP | **OPEN.** | Projection-aware RP density needs a uniform input-role map; full-formula density remains exponentially diluted. | On the high-ANF verifier family, scramble all trace variables and compare full-assignment density with mapped-input density, charging inverse-map evaluation. |
| :48 synthesis | **ESTABLISHED:** Lemmas 48A–D. **OPEN:** both global questions. | Representation obfuscation is neither a language lower bound nor a free resource. | Search for the missing middle object: a uniform short compatibility descriptor that avoids $M^2$ traffic without becoming a cheap indexed program for the entire target. |

## 8. Source and publication audit

- New :00 report: [`PREFIX24`](https://github.com/j15marti/pnp/blob/8c9e5a670494faa3dd487ffbb284adba7150222f/research/agents/mktp/2026-10-21_2012_PREFIX24.md).
- Circuit predecessor: [`PARSIMONIOUS-CIRCUIT-3CNF47`](https://github.com/j15marti/pnp/blob/587604b39b11bc83de6bf6c7bb621540fd0eeb27/research/main/2026-10-21_1948_MAIN_PARSIMONIOUS_CIRCUIT_3CNF47.md).
- Shared Drive fallback was readable and unchanged; no newer role handoff was present.

No scrambling, unique witness, circuit, hash, random seed, selected solver, finite computation, or conditional recurrence is promoted to a class separation. Root manuscripts and role assignments were untouched.
