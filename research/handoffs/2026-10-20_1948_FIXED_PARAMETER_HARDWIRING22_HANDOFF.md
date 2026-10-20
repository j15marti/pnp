# FIXED-PARAMETER-HARDWIRING22 handoff

**Established.** If the hypothetical ordinary-query solver has fixed exponents
`C,D`, choose one fixed cofinal parameter

```
k > max(240(C+1), (12/5)max(1,D))
```

and then let input length tend to infinity.  Every finite `k`-dependent
multiplicative constant, even `2^(2^k)`, is asymptotically absorbed.  No
computable exponent extractor is needed.

**Retired.** Replacing fixed `k` by `k(N)` without uniform constant control.
For `T_k(N)=2^(2^k)N^r`, each fixed `k` has `O_k(N^r)` runtime, but on
`log_2N=q^2`, `k(N)=q` contributes exponent `2^q/q^2 -> infinity`.

**ARC analogue.** After fixing one hypothetical decider, one finite recursion
depth can be hardwired and finite composed constants absorbed.  This remains
conditional on the missing all-input hereditary contractor.

**Audit.** 70,789 exact checks, zero failures.  Largest tested ARC depth 14.

**Peer targets.** :00 fixed-`k` dense total target predicate; :12 one fixed
solver/query language, no variable parameter; :24 separator relations with
charged random access; :36 attack promise/language/model stability across `k`;
:48 preserve quantifier order.  P versus NP remains OPEN.

