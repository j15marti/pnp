# COMPILERSIGNAL1

Date: 2026-10-05 00:22 PT
Status: COMPUTATIONAL
P versus NP: OPEN

## What was read

HEAD `0d735050` is RAZCAP1. The approximation-method count is capped by `24(M+1)`, and the pair span does not separate. The note names the missing arrow as a compiler from SAT, and not from the XOR slice, into a model whose per-gate error survives that cap.

Literature checked only for that arrow. ECCC TR26-213 (Beimel-Nir, 26 Sep 2026) shows that width-`w` multislices have slice-gate formulas of size at most `2^{n(w+1)}`. Cavalar-Goos-Riazanov-Sofronova-Sokolov (arXiv:2507.16105) improve matching via the approximation method plus a matching sunflower; that is not a slice SAT compiler. Neither paper supplies the missing arrow.

## Test

Grant exact Gaussian elimination on the parity shadow and exact 2-SAT on the width-2 projection. The resource that would still have to scale is a 3-unsat formula the shadow does not already reject.

The shadow is the project encoding: a proper 3-clause becomes the GF(2) equation on its three variables with right-hand side equal to the number of negative literals mod 2. A pure 3-CNF has no width-2 clause, so the 2-SAT oracle accepts every sample.

Uniform exact-layer samples at `q=12,t=11` and across `q in {6,7,8,10}` gave

    satU and xorS = 0

in every cell. Every observed 3-unsat formula was XOR-unsat. A `q=6` random walk of 84240 formulas and a 4000-attempt XOR-preserving killer at `q=5` also found none.

Separate method comparison, not a SAT bound: at `q=12` the Razborov counting cap is `42264`, while the already proved sparse-layer depth-2 DNF lower bound has `log2` size `428.90`. The log2 gap is `413.53`. The counting cap cannot reach that depth-2 bound. The cap is the method.

## Box

With GE and 2-SAT free, the sampled unsat mass sits inside the GE-easy shadow. There is no measured residual for the compiler to charge. That is not a theorem that the residual is empty, and it is not a monotone-circuit lower bound.

P versus NP remains OPEN.

Raw: `results/raw/monotone_slice/COMPILERSIGNAL1.txt`
