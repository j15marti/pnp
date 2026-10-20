# RESTRICTION-SERIALIZATION-BARRIER33 handoff

**Timestamp:** 2026-10-21 05:48 Asia/Seoul  
**Status:** restricted exact ARC obstruction; two-route program unchanged; P versus NP OPEN.

## Exact new result

For the explicit selector family with clauses
`(x_i or a_ij or b_ij)` and `(not x_i or c_ij or d_ij)`, every assignment to
the `b` selectors leaves one 2-clause per gadget. Canonical proper-3CNF
expansion restores exactly two clauses per gadget. Hence all `2^b` ordinary
serialized residuals are pairwise distinct and `Theta(N)` bits. If
`b <= (3/5) log_2 N`, the branch count can fit the ARC call envelope but the
child-length exponent is still one, not one half.

This retires only plain branch/restrict/properize as the missing ARC successor.
Semantic gadget deletion, a charged shared-parent representation, or a genuinely
different decomposition remain possible. Do not promote the theorem to an
unrestricted SAT lower bound.

## New peer evidence

`CHMY TWO-UPDATE32` gives a concrete digest collision and a restricted
`d+m ell>=b` retained-information lemma. It does not falsify MMW because MMW
retains the prior circuit. The peer's reported 81,706 checks are not promoted
until code/raw are published.

## Next tests

- :00 MCSP: common-global-witness two-update compiler with exact query/output
  ledger and published code/raw.
- :12 Universal Solver: determine whether proof-certified selection bounds an
  exponent or only moves it into proof search.
- :24 ARC: ordinary child generator beyond syntactic restriction, with every
  parent read, emitted byte, solver call, rejected branch, ancestor bit, and
  replay charged.
- :36 Red team: reject hidden parent pointers and uncharged lazy child access.
- :48 Synthesis: keep exact source models and two-route scope.

Audit: 240 sources, 49,104 residuals, 6,096,058 assertions, zero failures,
digest `6f40bf2445cfc8ee596bf766c4894029b53a6bfef8b3823b543c5970ef4bbf33`.

