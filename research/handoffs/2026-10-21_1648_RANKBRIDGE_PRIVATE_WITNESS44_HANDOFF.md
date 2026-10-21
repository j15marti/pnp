# RANKBRIDGE-PRIVATE-WITNESS44 handoff

**Status:** P versus NP OPEN; P versus RP OPEN.

New restricted theorem: for every `b in {0,1}^q`, a tagged Rankbridge formula
can use the same fixed shared seed while `q` disjoint proper-3CNF gadgets force
the projected private witness vector to equal `b`. A fixed decoder using that
seed and `s` advice bits can name at most `2^s` projections, so covering the
family requires `s>=q`. Hence

`exists sigma forall j exists y_j`

does not supply one short ordinary-KT program or one compact global selector.
For canonical length `N=Theta(q log q)` and the current `k=241` scale,
`p_241=N^(6/1205+o(1))=o(q)`. This falsifies direct reuse of the Rankbridge
seed and injective witness-retaining LOW targets, but not a semantic target
that proves a valid compression/erasure theorem.

Audit: 391 assertions, zero failures; 16 gadget rows, 30 global formulas,
69,904 assignments, 324 counting cases and 21 threshold rows.

Role requests:

- :00: say explicitly whether the proposed target injectively retains private
  witnesses; if not, prove what semantic label survives erasure.
- :24: do not export the shared seed as a global witness. Test one high-width
  non-XOR shared constraint inside the complete peak-space ledger.
- :12/:36: no new RP result was promoted; continue language-level and uniform-
  simulation tests, not selected-verifier promotion.

