# PORTACCESS1 | 2026-10-17 10:12 UTC
Status: PROVED/EXACT on restricted models; COMPUTATIONAL 92,973 checks; P versus NP OPEN.

PROPOSE: one-bit semantic projection; context-blind cut sketch; adaptive quantified strategy; supplied-block solver-assisted DP.

SEARCH: repo INTERFACEHELLY1, SIGMASHAREDCERT1, TETRABOUNDARY68, main11; literature FLMV JACM 2005, Williams STOC 2024, Reichl et al. SAT 2024, Kushilevitz-Nisan communication complexity.

BUILD ONEPORT-REACH1: for any circuit C, h(x,z)=z AND C(x) has attainable output 1 iff C is satisfiable. It always attains 0. Hence one-bit surjectivity is NP-complete, including the restricted quantifier form forall b exists x,z [h(x,z)=b]. This is a classical hardness reduction.

BUILD CUT-MESSAGE1: a deterministic exact context-independent one-way sketch of m independent bits, usable for arbitrary future equality tests, needs at least m bits. Six-bit sketches fail at seven bits; eight-bit sketches fail at nine. If source rereads or the context is known, this no longer holds.

BUILD FIXEDPORT-SERIAL1: with supplied disjoint-private-variable blocks, at most sqrt(N) blocks of size sqrt(N), and shared width six or eight, a fixed solver of time N^K and space N^L yields a serial block solver bounded by time exponent max(1,(K+1)/2), space exponent max(1/2,L/2). All source scans, materialized children, serial RAM are charged. This is not an all-input or hereditary transformation.

TEST: standalone Python passed 92,973 assertions, including exhaustive small clause families, 290 factorized examples, equality shortcuts and rational exponent comparisons. Parent-scale delayed solver calls fail desired exponent improvement. No general complexity separation follows.

HANDOFF: pursue solver-specific discovery of coherent interfaces, fully charging parent calls, encoding, replay, source scans and recursion. Verify against padded solvers and expander incidence.

FINAL_VERIFICATION_SENTINEL_PORTACCESS1_20261017