# LSPV-3 EXACT22-PARITY-RING160 | 2026-10-29 12:55 UTC

**Scope: RESTRICTED computer-assisted finite-seed theorem, externally unrefereed. P versus NP OPEN.** Full LaTeX, executable reproducer, raw JSON and manifest are GitHub published in this directory with verified exact matching Git blob hashes; the PDF and complete source ZIP are deposited in Library folder `/P vs NP/LSPV-3_EXACT22_PARITY_RING160` and linked in the conversation. This explanatory record supplements the full reproducibility package. Original source gadget and isolated splice identities are credited to LSPV-2 EXACT22-PORT-WIRES221, not new findings.

## Exact connected two-polarity ring theorem

For every integer r>=1 and arbitrary mode string t in {0,1}^r, construct F_(r,t) from 2r disjoint 15-variable/20-clause W1 signed exact-(2 positive, 2 negative) source copies G. For each j, splice modules 2j and 2j+1 through signed clause slots C2-C2 if t_j=0 (equal signal), or balanced cross-polarity C2-C15 and C15-C2 if t_j=1 (opposite signal). Join each odd module 2j+1 to the next even module modulo 2r by the disjoint C3-C3 signed swap. Each source signal is x4. These occurrence swaps do not change clause or variable counts, preserve proper three-distinct-variable clauses, exactly two positive and two negative appearances of each variable, and connect the 2r-module cycle. Therefore n=30r, m=40r and canonical binary input size is Theta(r log(r+2)).

For the finite module G, the source-authenticated two- and three-puncture truth tables (obtained by exhausting all 2^15 assignments) yield a four-state interface s=(p,f3) ordered 00,01,10,11, and exact pairwise Boolean-semiring transfer matrices

    A0 = [1100;0000;0101;0101]
    A1 = [0101;0000;1100;1100].

Every whole-ring assignment is equivalent to a closed walk in the transfer automaton. The matrices satisfy A0*A0=A0, A0*A1=A1*A0=A1, A1*A1=A0; A0 has nonzero Boolean diagonal whereas A1 has none. Thus, with all products and traces over the Boolean semiring,

**F_(r,t) is SAT if and only if the XOR of its r mode bits equals 0.**

This establishes a connected proper strict signed exact-(2,2)-3CNF family with both SAT and UNSAT instances, and polynomial deterministic acquisition and authentication of source-identified exact four-state semantic certificates on both sides. SAT certificates reconstruct and check a full assignment; UNSAT certificates provide a source-bound r-step Boolean-matrix product with zero diagonal. This is a new relational proof grammar, **not** an original-clause 2CNF-SCC adaptive tree, a Resolution refutation, or a kernel-verified LRAT proof. Universal UNSAT coverage is not claimed.

## Reproducibility ledger

The stand-alone Python audit checked 55 full ring instances, including all mode strings for r<=4 and r through 64; tested parsing, connectedness, signed degree, source provenance, assignment reconstruction, sound UNSAT matrix traces, and corrupted-source/certificate rejection. Eight small-ring controls were independently checked by SciPy HiGHS full-formula MILP. Two runs reproduced the raw JSON byte-for-byte (SHA256 e3fcdb7ea106c4d13a28d03af1ead27e890b82e0e31a523a0dd8b8eec9d9ab59). At r=64: 1920 variables, 2560 clauses, 343584 encoded DIMACS bits, representative JSON UNSAT certificate 32744 bits. These finite computations corroborate, but do not substitute for, the all-r Boolean-matrix induction. There has been no kernel-certified formal verification.

The original Library Connected_Interface_Audit.zip was independently rerun, matching its results.json byte-for-byte (SHA256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca), 4680 boundary subsets, 7191 local discovery tests, 139 SAT comparisons. The bound k<=4b and n<=3b+12bq applies solely to the stated static syntactic modular hypothesis, not to unrestricted SAT time.

## GitHub source inspection

- j15marti/pnp: research/agents/lspv-2/2026-10-29_1025_LSPV-2_EXACT22_PORT_WIRES221.tex, file blob f9317c23d778703090b6cdd1adbbccadf7ef847f, exact finite wire source and hypotheses.
- lammich/lrat_isa: thys/LRAT_Checker_Impl.thy, blob e50d75e5cd759761399a979766f0acb6af3e1769, source-checked LRUP verification is not deterministic discovery.
- arminbiere/cadical: src/elim.cpp, blob c401152c7a733803d0b407d98e8a295ab44f7e99, bounded elimination heuristics do not establish universal contraction.
- openai/math: preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/06-recursion.tex, blob 65bf0450f460311b13a11a136db6ada4520cb6f0, one recursive quantum synthesis use with target-dependent oracle/slot data; no polynomial deterministic classical SAT oracle follows.

## Machine and negative-case resource accounting

On this restricted family, source validation, formula regeneration, finite-table construction, all r matrix multiplications, failed source checks, certificate construction/verification and SAT reconstruction fit conservatively within O(N^3) steps and O(N) bits work space for a fixed multitape machine with read-only input; O(N^6) head steps and O(N^3) physical footprint including input for a one-tape implementation; a fixed efficiently universal simulator incurs only polynomial overhead. These upper bounds are conservative and **not** RAM or TM hardness claims. A restricted one-byte answer-class child exists after deciding this family, but the class does not contain arbitrary SAT, so it is not a P=NP proof.

## Exact remaining gaps

A degree-preserving **branching** signed exact-(2,2) interface with at least three independently composable ports, rigorous source-identity transfer and genuinely interacting semantics; comparison against affine/Horn/BDD/2SAT/Resolution/PC/CP portfolios; polynomial uniform acquisition on **all** SAT and UNSAT instances; and one-child N^lambda size contraction on an arbitrary-SAT-containing closed class all remain OPEN.

**Publication status, updated after transient upload recovery:** Full `.tex`, `_repro.py`, `_raw.json`, and `_manifest.json` have all been committed to GitHub and read back with their exact local Git blob hashes (see manifest). Full PDF, reproducibility ZIP, handoff, manifest, raw, source and executable have been uploaded successfully to Library folder `/P vs NP/LSPV-3_EXACT22_PARITY_RING160`. The original complete coordination handoff is committed with matching blob `f3aea22a1ce07479faf1439eb523a24932fd7ba0`. There was a transient `container_session_unavailable` that cleared upon retry. Root main.tex and all agent schedules/state remain untouched.
