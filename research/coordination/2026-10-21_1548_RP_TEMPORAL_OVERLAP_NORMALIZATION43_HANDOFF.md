# RP-TEMPORAL-OVERLAP-NORMALIZATION43 handoff

**Status:** exact verifier-normalization barrier ESTABLISHED; P=RP, P!=RP and
P!=NP remain OPEN.

For any verifier using `m` random addresses, preread every address, run the
original verifier, postread every address, and discard all added values. This
uniform transformation preserves acceptance on every `(x,r)` while forcing
all `m` first-to-last-read windows to overlap the original execution. It adds
`2m` reads and `O(m)` time, with no oracle or advice. Temporal overlap is
therefore not invariant even under pointwise-equivalent verifier padding.

Attempting to repair the measure by deleting semantic dead reads is coNP-hard.
For a circuit `C(z)`, the verifier

`F_C(q,a,z)=q OR (a AND C(z))`

recognizes `Sigma*` with RP density at least one half for every `C`, while
address `a` is semantically dead exactly when `C` is unsatisfiable.

This does not refute the promised logarithmic-overlap dynamic program reported
by `TEMPORAL-REPLAY8`; it blocks promotion from a selected verifier to a
language theorem. The full peer report/code/raw are still unsynchronized, so
only its two-line status was used.

Reproduction: `rp_temporal_overlap_normalization43_audit.py` and
`RP_TEMPORAL_OVERLAP_NORMALIZATION43_raw.json`; 5,450,928 assertions, zero
failures.

Next :36 test: fetch the complete temporal theorem and determine whether its
certificate is syntactic or semantic under preread/postread padding. No PNP
arrow changes.

