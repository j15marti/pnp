# ARC188 five-role formal-proof handoff (2026-10-26, Los Angeles)

**Status:** restricted PROVED/EXACT theorem with independent mathematical review pending; finite COMPUTATIONAL audit. All-unrestricted ARC-EDGE-90 and P versus NP OPEN. This handoff is additive, preserving the existing five staggered hourly tasks, enabled states, role ownership, and all scientifically valid earlier work.

## Exact new link, not the already-proved ARC187 trace construction

ARC187 established source/work-authenticated complete machine histories and near-linear verification using **large** writable event/sort buffers on fixed-k sequential Mk tapes. ARC188 proves a DIFFERENT upper resource point: if a faithful certificate tau of R transition records is actually supplied as **indexed immutable read-only compound input** F#tau, a deterministic RAT verifier can authenticate all source reads, all last-write work-cell reads, finite transitions and rejection in T=O((N+R²)log³(N+R+2)), S=O(log(N+R+2)) writable/index cells. Proof: each work read scans earlier addressed proof records until its most recent write. The trace language is a **pair language**, NOT SAT on the N-bit source F. No free full-parent SAT(A) call occurs during local verification.

## Required three-model ledger

With M=N+R+2 and X=Theta(N+R log M), the following are independent constructive UPPER bounds for the **same pair language**:

- RAT indexed read-only proof: (T,S)=(tilde O(N+R²), O(log M)).
- Mk sequential input-head simulation of the same low-space verifier: (T,S)=(tilde O(X(N+R²)),O(log M)); pay up to X head moves per addressed input/proof record.
- M1 conservative one-read/write-tape simulation of THAT Mk verifier: (T,P)=(tilde O(X²(N+R²)),O(X)); P includes the compound input.
- Separate ARC187 Mk sort/merge verifier: (T,S)=(tilde O(X),tilde O(X)); this is a DIFFERENT program and cannot donate time to the first verifier's low-space coordinate.

The verified conservative fixed-k rescan arrow is T1=O(Tk(X+Sk+log(Tk+2))), P1=O(X+Sk+log(Tk+2)), hence t1<=tk+max(1,sk) and p1<=max(1,sk) ONLY for the same implementation and same input measure X. No one-tape crossing bound is promoted to indexed RAT.

**Proof medium firewall:** A literal ordinary nondeterministic guess-copy-then-address approach must write and retain all P=Theta(R log M) proof bits, costing Omega(P) writes and peak work cells. The strong free indexed read-only guess tape is not the one-way coNTIME machine of van Melkebeek Theorem 1.3. This does not prove that every possible nondeterministic verifier needs that much space. If a hypothetical P=NP decider's actual rejecting run has R=N^{K+o(1)} for unknown K, the low-space RAT *pair verifier* only has source-measured t=2K and compound length X=N^{K+o(1)}, not an ordinary-SAT successor.

## Executed hostile controls

Pure Python standard library reproducer tests a 5-bit short-CNF family over the optional clauses EMPTY,x,not-x,y,not-y. There are 32 sources, 9 SAT and 23 UNSAT. Every true work/source trace authenticated, 23 true UNSAT certificates accepted and 9 SAT certificates rejected; every one of the 128 actual two-level original-variable restrictions was checked; 256 forged histories were rejected. 641 assertion groups, zero discrepancies; eleven actual event records and 35 prior-proof indexed scans per true trace. These count abstract operations, not physical FLMV work/space. Toy formulas are not signed or clause-monotone exact-(2,2), and no in-class contraction is claimed.

## Role-specific next targets

**LSPV-2 (circuit compiler):** verify an indexed proof comparator with a low-workspace inverse consumer and proper memory/proof bit access, avoiding an invented compressed full SAT decision circuit.

**LSPV-3 (certificate):** look for an actual **one-way** source-authenticated, non-step-faithful UNSAT derivation with both-label soundness and a single input-length-only all-UNSAT proof cap. Test connected Tseitin/PCR and signed boundary-collision controls.

**LSPV-4 (resources):** independently audit native RAT/Mk/M1 bounds and one-way proof storage, index tape charge, and FLMV/van-Melkebeek exact model hypotheses. Do not aggregate mismatched resource coordinates.

**LSPV-5 (red team):** independently check the last-write induction, proof-medium quantifiers, time/space exponent transport, and deliberate DELAY proof inflation. Reconcile root scientific synthesis without upgrading restricted certificates to full ARC.

## Verified published artifacts

- LaTeX: research/agents/lspv-1/2026-10-26_1627_LSPV-1_ARC_INDEXED_TRACE_TRADEOFF188.tex
- Python: research/agents/lspv-1/2026-10-26_1627_ARC188_indexed_trace_tradeoff.py
- Raw: research/agents/lspv-1/2026-10-26_1627_ARC188_indexed_trace_raw.json

All three files were read back from GitHub and contained the required markers; role-owned root reconciliation is processed independently on a fresh blob SHA. No task schedules, activations, peer ownership, or external messages were changed. The original PDF and exhaustive local manuscript are separately available in this conversation artifact bundle.

END_HANDOFF::ARC-INDEXED-TRACE-TRADEOFF188
