# PROOF-0009 — Williams product endpoint and recursive space closure

**Agent:** PROOF  
**Global status:** P versus NP remains OPEN.

## Status

- **WILLIAMS-PRODUCT-ENDPOINT1:** literature theorem, exact in its stated SAT time-space model.
- **CSE-WILLIAMS-PRODUCT-ENDPOINT1:** **CONDITIONAL** on a valid uniform model-matched SAT compiler.
- **CSE-SPACE-CLOSE1:** **PROVED/EXACT** as a recurrence/accounting theorem in the stated sequential depth-first recursion model.

## 1. Strengthening the previous FLMV endpoint

Fortnow–Lipton–van Melkebeek–Viglas (JACM 2005) give the older golden-ratio deterministic SAT time-space lower bound. Ryan Williams subsequently strengthened the endpoint relevant to the present compiler architecture. STACS 2010, Theorem 3.9 states that for polynomially bounded time (t(n)) and space (s(n)), every SAT algorithm satisfies, for every (arepsilon>0),
[
t(n)s(n)=Omega!left(n^{gamma-arepsilon}ight),
qquad
gamma=2cos(pi/7)=1.8019377358ldots.
]

This is stronger for the current CSE architecture than requiring subpolynomial space plus a time exponent below the golden ratio.

## 2. CSE-WILLIAMS-PRODUCT-ENDPOINT1

Assume a valid uniform model-matched compiler transforms a hypothetical exact polynomial-time SAT decider into an exact SAT algorithm (A') on the machine model covered by Williams, with
[
T_{A'}(N)le N^{C+o(1)},qquad
S_{A'}(N)le N^{sigma+o(1)}
]
for fixed (C,sigmage0).

If
[
oxed{C+sigma<gamma,}
]
then the compiled algorithm contradicts Williams' SAT time-space product lower bound.

### Proof

Choose (delta>0) such that
[
C+sigma+2delta<gamma.
]
For sufficiently large (N),
[
T_{A'}(N)S_{A'}(N)
le
N^{C+sigma+delta}
<
N^{gamma-delta}.
]
Williams' theorem with (arepsilon=delta) requires
[
T_{A'}(N)S_{A'}(N)
=
Omega(N^{gamma-delta}),
]
a contradiction for sufficiently large (N).

The compiler hypothesis is not established.

## 3. CSE-SPACE-CLOSE1

Consider sequential depth-first recursive execution on source size (N). Assume:

1. each child source has size at most (N^{	heta+o(1)}) for fixed (0le	heta<1);
2. children are processed sequentially, so sibling workspaces are not simultaneously live;
3. parent-local live workspace, excluding the active child recursion, is at most (N^{sigma+o(1)});
4. recursion metadata per level is polylogarithmic and charged.

Then
[
S(N)
le
N^{sigma+o(1)}
+
S(N^{	heta+o(1)})
+
operatorname{polylog}N.
]

For (sigma>0),
[
oxed{S(N)=N^{sigma+o(1)}.}
]

If the local workspace is (N^{o(1)}), then
[
oxed{S(N)=N^{o(1)}.}
]

### Proof

At depth (j), the active source size is at most (N^{	heta^j+o(1)}). For fixed (sigma>0), the local workspace contribution is at most (N^{sigma	heta^j+o(1)}). The (O(loglog N)) nontrivial recursion levels are dominated by the root contribution up to an (N^{o(1)}) factor. For (sigma=0), each level contributes (N^{o(1)}), and multiplying by (O(loglog N)) remains (N^{o(1)}). Sequential child processing is essential.

## 4. Combined calibration

If RECURCLOSE1 yields
[
C=maxleft{r,rac{eta}{1-	heta}ight}
]
and CSE-SPACE-CLOSE1 yields workspace exponent (sigma), then a sufficient conditional landing condition is
[
oxed{
maxleft{r,rac{eta}{1-	heta}ight}
+sigma
<
2cos(pi/7).
}
]

For local (N^{o(1)}) workspace this reduces to
[
maxleft{r,rac{eta}{1-	heta}ight}
<
2cos(pi/7),
]
strictly improving the previous golden-ratio calibration.

## 5. Scope

This does **not** prove CSE, arbitrary-algorithm extraction, wrapper-covariant source projection, FSC, or a nonrelativizing/nonalgebrizing compiler. It does not show that a hypothetical polynomial SAT algorithm can be transformed into the forbidden region. It gives a sharper unconditional endpoint only after a valid compiler lands there.

## 6. Barrier audit

The Williams endpoint is an unconditional SAT lower bound in its stated time-space model. The present composition theorem does not supply the missing barrier-breaking extraction. If the SAT-to-CSE compiler relativizes, the overall P-vs-NP route remains blocked. A separate algebrization audit remains necessary.

## 7. Hostile controls

- Unknown starting exponent (k): unresolved by one-level shrink; genuine recursive fractional contraction is required.
- Parallel recursion: may increase space and must be charged.
- Memoization: may reduce time but increase retained space.
- Recomputation: may reduce space but increase time.
- Padding: exponents must be measured in the final SAT input length.
- Model conversion: must be explicit before applying the Williams endpoint.

## 8. Handoffs

**LEAD:** replace the phi-only endpoint with the Williams product frontier (gamma=2cos(pi/7)), retaining FLMV as historical/structural background.

**RED:** attack proposed CSE recurrences by optimizing time and space jointly, including memoization, parallel child retention, recomputation, padding, and model-conversion overhead.

**RESEARCH:** verify whether any later uniform deterministic SAT product lower bound improves (gamma) in the same broad random-access setting; do not infer this from restricted-machine results.

**WRITE:** integrate the product frontier and CSE-SPACE-CLOSE1 into main2.tex and main3.tex and keep the compiler landing CONDITIONAL.

## References

1. Ryan Williams, *Alternation-Trading Proofs, Linear Programming, and Lower Bounds*, STACS 2010, Theorem 3.9; ACM TOCT 5(2), 2013.
2. Lance Fortnow, Richard Lipton, Dieter van Melkebeek, Anastasios Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005.
