# PRIMEPROJ2 stronger contextual quotient tests

Status: COMPUTATIONAL finite controls. P versus NP remains OPEN.

The test treats a boundary assignment as equivalent to another exactly when every legal future completion in the tested context family gives the same SAT outcome.

## Test A: unrestricted future clauses
For boundary size b=1,...,8, all clauses of width at most 3 distinguish every one of the 2^b assignments. Results:
b: 1 2 3 4 5 6 7 8
classes: 2 4 8 16 32 64 128 256

## Test B: width exactly 3 only
To remove the trivial unit-clause explanation, for b=3,...,8 only exact width-3 future clauses were admitted. Again every assignment was distinguished:
b: 3 4 5 6 7 8
classes: 8 16 32 64 128 256

Thus unrestricted 3-clause contexts give no nontrivial semantic quotient of the dual-prime boundary support.

## Test C: fixed-source residual contexts
For random 3-CNFs on n variables, a boundary assignment on the first floor(n/2) variables was represented by the full truth table of the residual formula over all remaining variables. Twenty deterministic samples were tested per (n,m), seed 20261005.

n=6,b=3:
m=6 classes min/mean/max 3/5.30/8
m=12 3/5.25/8
m=18 2/3.70/7
m=24 1/2.75/4

n=7,b=3:
m=7 3/6.20/8
m=14 4/6.25/8
m=21 2/3.70/6
m=28 1/2.60/5

n=8,b=4:
m=8 5/8.50/15
m=16 5/7.80/12
m=24 2/4.95/8
m=32 1/2.80/6

Fixed-source contexts can therefore collapse many dual-prime boundary assignments. This is real semantic quotienting, but it is not evidence of hardness: dense formulas can collapse because many residuals are identically false.

## Test D: parity hostile control
For the even-parity function on n=4,...,8 with b=floor(n/2), the residual contextual quotient has exactly 2 classes for every tested n. Hence dramatic contextual collapse can occur for an easy affine/Tseitin-type function. Quotient collapse alone is not a SAT-hardness signal.

## Interpretation
1. Dual-prime support faithfully names boundary assignments.
2. All possible width-3 contexts retain the full 2^b contextual index.
3. A fixed source formula can induce a much smaller quotient.
4. Small quotient does not imply hardness or algorithmic contraction.
5. A useful theorem must additionally show that the quotient is computable/acquirable without solving the original SAT problem, has a compact model-matched representation, yields exact ordinary-CNF return semantics, and recursively contracts after all charges.
