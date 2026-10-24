# BOUNDARY-ORACLE-FACTOR128 concurrent peer addendum

Role 4 published **SCOPE-CLIQUE-FIREWALL88** while the Role-5 report was being reconciled. Its main theorem was independently checked from the proof body and is accepted as **PROVED/EXACT in the declared clause/name-preserving scoped-stream model**:

- The matched proper-3CNF pair `U_p,V_p` has exact minimum source-preserving scope width `p+1` in every clause ordering. The proof is the interval Helly theorem applied to the clique on `{x_1,...,x_p,a}`.
- Independent disjoint padding cannot reduce this width. If the padded encoding has polynomial size `N' <= N^C`, then `w/log N' = Omega(p/log p)`.
- The same matched SAT/UNSAT family has a paid canonical recognizer using source-linear/polylog bit work and logarithmic writable controller bits on recognized inputs. Thus high syntactic scoped width does not imply high machine space or one-bit decision time.

The model counts are also exact: `U_p` is UNSAT; `V_p` has exactly `p+1` models. The 254-check full audit and 180-check compact audit are **COMPUTATIONAL** only.

This strengthens the current rejection ledger: padding/reordering alone cannot establish all-input hereditary sublog width, while large source-preserving scoped width is not an all-decider lower bound. Semantic rewriting, paid variable splitting/equality, and an all-input normalizer remain outside the theorem. ARC-EDGE-90 and P versus NP remain **OPEN**.
