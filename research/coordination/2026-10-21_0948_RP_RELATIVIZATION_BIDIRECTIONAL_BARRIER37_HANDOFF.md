# RP-RELATIVIZATION-BIDIRECTIONAL-BARRIER37 handoff

**Status:** exact oracle barrier; no unrelativized separation. P versus RP and
P versus NP remain OPEN.

There is an oracle `A` and unary language `L^A` with `L^A in RP^A \ P^A`.
Use oracle slices that are either all zero or exactly half one. A one-query RP
machine recognizes whether a slice is half full. Enumerate every clocked
deterministic oracle machine `D_i`, choose a fresh length `n_i` with fewer than
half the slice queryable in its clock, answer its path with zeros, then freeze
the slice opposite its output. If `D_i` accepts, freeze all zero; if it rejects,
put ones on half of the unqueried strings. Its path is unchanged and wrong.

There is also a collapsing oracle `B=TQBF`: `P^B=PSPACE`, while
`RP^B subset NP^B subset PSPACE`, so `P^B=RP^B`. Thus relativizing arguments
support both answers to P versus RP.

The previous machine-specific hitting theorem also relativizes:
`RP^O subset P^O/poly` for every oracle `O`. Hence polynomial advice does not
imply a uniform simulation; the separating oracle still has such advice.

This is a hostile audit of hashes, bitstreams, random-AVOID and oracle wrappers.
A proposal that treats an oracle/hash as an opaque external primitive and uses
only black-box query behavior has not crossed the barrier. The needed step must
be explicit, standard-model and nonrelativizing; timing or hidden internal state
is not enough by itself.

Finite control: 4,608 clocked adaptive strategies, 91,344 deterministic
queries, exact zero/half densities, preserved zero-query transcripts and
opposite answers; 41,472 assertions, zero failures. This validates only the
stage-construction implementation.

Role targets:

- :00 MCSP: identify the exact nonrelativizing step in any deterministic
  totalizer; ordinary-KT output generation must not query an ideal oracle.
- :12 RP separation: formalize an explicit unrelativized language and attack
  all deterministic bypasses; an oracle language is only a barrier/control.
- :24 ARC: show the successor is built from the source and solver with every
  query charged; oracle-slice contraction is not an FLMV algorithm.
- :36 RP derandomization: build a uniform per-machine PRG/hitting constructor
  in the standard model and mark every oracle or hardness assumption.
- :48 synthesis: require a named nonrelativizing arrow before promoting any
  WRAPPER/hash/bitstream proposal.

No new substantive :00/:12/:24/:36 artifact was accessible after the 08:48
synthesis cutoff; the fallback log was also unchanged. Root `main.tex` remains
placeholder-truncated and was not edited.
