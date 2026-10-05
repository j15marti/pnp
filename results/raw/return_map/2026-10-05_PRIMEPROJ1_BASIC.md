# PRIMEPROJ1 basic dual-prime tests

Status: COMPUTATIONAL finite controls only. P versus NP remains OPEN.

Parameters:
- n = 5 Boolean variables
- true primes: 2, 5, 11, 17, 23
- false primes: 3, 7, 13, 19, 29
- 32 assignments
- 80 distinct width-3 clauses over distinct variables and both polarities

Results:
1. Exact DUALPRIME-SAT clause semantics passed every assignment/clause pair tested:
   assignment satisfies clause iff gcd(assignment prime product, clause satisfying-literal prime product) > 1.
2. Projection onto k retained variables produced exactly 2^k distinct projected prime codes, with preimage size 2^(5-k).
3. Contextual equivalence test: for a boundary of b variables, using all clauses of width at most 3 over that boundary, the number of distinct future-context satisfaction signatures was exactly 2^b for b=1,...,5. Thus this unrestricted local context family does not compress the boundary state below the ordinary assignment count.
4. Multiplication-only history fingerprints forget order. For length-4 histories over four event primes, 31 product values represented more than one ordered history; the largest collision class had 24 histories.

Interpretation:
- Unique true/false prime support is an exact Boolean namespace.
- GCD/divisibility evaluates clause satisfaction exactly without full factorization.
- Forgetting variables by deleting their factors gives exact semantic projection, but unrestricted clause contexts distinguish every remaining Boolean assignment in this finite test.
- Plain commutative multiplication is unsuitable for ordered provenance without extra positional/event labels.
- None of these finite tests imply an asymptotic SAT lower bound or a contractive ordinary-CNF return theorem.
