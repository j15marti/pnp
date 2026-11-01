# Five-role handoff: COMPONENT-AMORTIZATION-FIREWALL-REFEREE259

Status: **PROVED/EXACT** for the certificate-carrying composition and additive threshold; **OPEN** for all-input power shrink, arbitrary-A→Phi(A), FLMV, and P versus NP.

For every valid canonical disjoint union `F = G ⊔ P`, pivot `x` in `G`, branch `b`, and checked SAT witness for every component of `P`:

`SAT(F|x=b) iff SAT(G|x=b) iff SAT(R(G,x=b))`.

If `P` has `h` variables, then it has `4h/3` clauses and the REF258 child has

`(n',m') = (n-h+201, m-4h/3+268)`.

Strict structural shrink begins exactly at `h=204`. Power shrink `n' <= n^lambda` requires

`h >= n+201-n^lambda`,

so the retained answer-bearing core must already have at most `n^lambda-201` variables. On UNSAT sources the retained core must contain an UNSAT component and every peeled component needs a SAT certificate; neither discovery nor selection is free.

Same-source controls:

- `U198/V198 + 33 Y6`: source 396/528, child 399/532, `+112` encoded bits.
- `U198/V198 + 34 Y6`: source 402/536, child 399/532, `-112` encoded bits.
- Independent replay passed 575,026 checks.
- Logical XOR is offline only; `d_phys` was not measured. DELAY/read-only loops remain countercontrols.

Next common target: connected-instance semantic contraction or a strictly smaller critical gadget. Easy disconnected padding is now classified as an exact amortizer, not an ARC proof.

Artifacts are in `experiments/arc/lspv5_259/`, `results/raw/arc/2026-10-31_2348_*REFEREE259*`, and `research/main/2026-10-31_2348_MAIN_COMPONENT-AMORTIZATION-FIREWALL-REFEREE259.tex`.
