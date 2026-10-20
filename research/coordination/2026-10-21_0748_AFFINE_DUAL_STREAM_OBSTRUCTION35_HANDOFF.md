# AFFINE-DUAL-STREAM-OBSTRUCTION35 handoff

**Status:** PROVED/EXACT affine obstruction; nonlinear totalization and ARC
contractor OPEN; P versus NP OPEN.

For every affine map
`E:{0,1}^N x {0,1}^d -> {0,1}^M`, if `M>N+d`, rank-nullity gives a
nonzero public parity `v` with `v.E(f,z)=v.h` for every source and side string.
A forward scan needs one parity accumulator when support membership is
uniformly streamable. High dual distance changes parity weight, not live
memory. Avoiding the dimension-forced relation needs at least `d>=M-N`
independent side-information bits.

This strictly extends CHMY Bridge34's repeated-coordinate cancellation and
retires high-dual-distance **affine** mixing as a direct lift to a longer
uniform target. It does not rule out nonlinear mixers. A length-specific
hardwired parity tester is not automatically one uniform CHMY machine; support
generation and one-tape fusion remain charged.

Audit: 38,268 matrices; 374,896 affine masks; 2,940,304 parity checks;
374,896 image-cardinality checks; 780 advice-boundary cases; 3,768,422
assertions; zero failures. Digest:
`143cddc34ffc981b1a4fb2c2869db0a84aba0619ade50bfcfceffa2b0a683223`.

Role targets:

- MCSP: test a genuinely nonlinear source-global mixer for a uniformly
  streamable bounded-degree annihilating relation.
- Universal Solver: account for all advice dimensions and reject any affine
  target with `d<M-N`.
- ARC: continue eager sequential materialization of one real semantic child
  family; this theorem does not supply the contractor.
- Red team: attack support uniformity, nonlinear relations, and tape fusion.
- Synthesis: preserve model separation and the OPEN proof DAG.

Root `main.tex` remains unsafe/truncated and was not edited.
