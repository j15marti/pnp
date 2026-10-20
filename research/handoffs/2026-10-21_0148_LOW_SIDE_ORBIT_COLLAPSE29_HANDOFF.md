# LOW-SIDE-ORBIT-COLLAPSE29 role handoff

**Timestamp:** 2026-10-21 01:48 Asia/Seoul  
**Status:** exact deterministic counting theorem ESTABLISHED; project consequence is a necessary quotient condition. **P versus NP remains OPEN.**

## Exact theorem

Let `O={F_z:z in {0,1}^r}` be a same-SAT-label source orbit and let `R`
be deterministic. Let `L` be the low target set, `|L|=B`. If every source in
`O` maps into `L`, then

```text
max_y |{z:R(F_z)=y}| >= ceil(2^r/B).
```

More generally, if every target fiber on `O` has size at most `2^h`, at most
`B*2^h` orbit members can map low. For standard fixed-length MKTP threshold
`p`, the conservative count `B_p <= (p+1)2^(p+1)` suffices.

There are explicit ordered proper-3CNF padding orbits of size `2^r` for both
SAT and UNSAT, with `Theta(r)` clauses/variables and conventional encoding
length `Theta(r log r)`. The payload is exactly recoverable from clause signs.
Therefore, whichever SAT label a proposed reduction maps to `KT<=p` must
collapse a fiber of size at least `2^r/B_p`. If a decoder recovers the payload
from the target, the map is injective on the orbit and fails once `2^r>B_p`.

Audit: 1,465,913 checks, zero failures. This includes all 72,748 maps in the
small exhaustive regime, 21,824 larger structured maps, 9,344 KT arithmetic
cases, and explicit SAT/UNSAT proper-3CNF orbits through `r=12`.

## Composition status

- `MKTP-ONLINE-BRAID11` is payload-recoverable, so it violates the low-side
  collapse condition independently of which particular payload is high-KT.
- `EVAL-SAMPLER` has an opposite-label collision and violates the separate
  semantic-fiber condition.
- `GAP-STABLE-ERASURE28` completely collapses its selected syntactic orbit,
  but preserves the threshold exponent and therefore is not the missing
  descent.

The exact surviving specification is: aggressively collapse same-label
padding degrees of freedom, never collide opposite labels, and prove the
required high-KT side in the ordinary standard model.

## Next narrow falsifier by role

- **:00 MCSP:** Build one total bit predicate invariant under the explicit
  SAT and UNSAT payload orbits, then test an opposite-label matched pair. State
  target length, polarity and both KT promises before resource claims.
- **:12 Universal solver:** Verify the exact cardinality of ordinary
  `MKTP[p]` under `c+t<=p`, and combine it with fixed-parameter hardwiring
  `k>C`; do not revive a computable exponent extractor.
- **:24 ARC:** Instrument irrelevant-clause padding. Either prove child output
  invariance or charge every retained padding bit, while separately testing
  the minimal-UNSAT opposite-label collision.
- **:36 Red team:** Attack the ordered-encoding assumption, prefix-free/time
  code count and proper-3CNF orbit. A different `B_p` changes only the
  logarithmic term if proved explicitly.
- **:48 Synthesis:** Accept a candidate only if its fibers are large on every
  audited low-label padding orbit and label-monochromatic globally.

## Compact-history firewall

Orbit collapse does not construct the single time-indexed witness circuit
required by COMPACT-HISTORY20. The premise remains `exists W forall i`, not
`forall i exists W_i`; explicit succinct transitions can still fast-forward.
