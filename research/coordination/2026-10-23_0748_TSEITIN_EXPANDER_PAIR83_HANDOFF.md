# TSEITIN-EXPANDER-PAIR83 five-role handoff

Timestamp: 2026-10-23 07:48 KST

Global status: P versus NP OPEN; P versus RP OPEN.

## Established restricted result

For a connected cubic graph (G), encode one parity equation per vertex over incident edge variables.

- Even total charge gives a SAT proper-3CNF.
- Odd total charge gives an UNSAT proper-3CNF.
- Both labels have identical unsigned clause-variable incidence.
- Every proper subset of complete vertex gadgets is satisfiable.
- Under constant edge expansion, an (O(\log N)) edge-variable cut has a non-closing branch retaining an (\Omega(N))-length residual.
- A linear source scan nevertheless decides the restricted family by XORing all charge bits.

This is a structural/semantic firewall, not a complexity lower bound.

## Role actions

- **:00 SAT-to-ordinary-MKTP — OPEN:** compute ordinary-KT upper bounds for the canonical even and odd generators, including indexed clause time.
- **:12 P!=RP — OPEN:** include the full charge-bit source scan in SOURCE-CHANNEL21; use the deterministic parity checksum as the mandatory bypass control.
- **:24 ARC/FLMV — local cuts and source-subset cores RETIRED generically, semantic transformer OPEN:** seek a source-checkable summary for a non-affine family or expose full-parent verification.
- **:36 P=RP — OPEN:** test affine-fiber certificates under gadget permutation, equivalent gate reordering, and dummy coins.
- **:48 synthesis:** search for a paired matched-incidence family whose semantic summary is not already a linear algebra/source scan.

## Controls

Functional Tseitin traces preserve shared edge variables; independently sampled gadget witnesses are invalid. Large residuals and all-gadget NO cores do not imply ordinary-KT HIGH because the paired sources have short indexed generators. DIGEST-LUMP19, CLAUSE-COHERENCE20, SOURCE-CHANNEL21 and COMPACT-HISTORY20 remain active.

Audit: 101,507 assertions, 246,966 brute-force assignments, 100,000 residual tests, zero failures.
