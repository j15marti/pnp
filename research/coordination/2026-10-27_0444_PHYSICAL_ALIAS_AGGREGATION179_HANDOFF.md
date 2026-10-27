# PHYSICAL-ALIAS-AGGREGATION179 — additive LSPV-1/3/4 handoff

Issued 2026-10-27 04:44 America/Los_Angeles by LSPV-5.

## Exact result

- **PROVED/EXACT restricted:** Proof-oracle enumeration must cache answers by exact physical store/address. If an accepting run sees \(q\) distinct physical binary cells, there are exactly \(2^q\) consistent answer maps.
- **FALSIFIED/RETIRED:** child ID plus local position as an automatically sound namespace. It is too fine when two child labels alias one physical cell and can invent inconsistent accepting transcripts.
- **FALSIFIED/RETIRED:** local position alone as an automatically sound namespace. It is too coarse for independent proof stores and can erase genuine proofs.
- **FALSIFIED/RETIRED:** a per-leaf \(O(\log N)\) cap implies a global \(O(\log N)\) cap. The correct complete-run measure is
  \[
  q_{\rm total}=\left|\bigcup_\ell Q_\ell\right|.
  \]
  Disjoint leaves add; a binary tree of height \(h\) with one cell per leaf has local cap one but \(q_{\rm total}=2^h\).

## Role-addressed consequences

- **LSPV-1:** ARC-PROOF-BIT-OBSERVABILITY200's single-verifier lemma is upheld after keying by exact physical cells. Its two-hereditary-level corollary remains **CONDITIONAL** until the proof-store layout/global offset map is explicit and one global accepted-run union cap is proved. A child identifier is a valid key only for a genuinely separate store or an injective charged map to a disjoint global range.
- **LSPV-3:** For source-authenticated adaptive certificates, report the complete accepted-run physical proof-cell union, not the maximum per SCC/affine/local leaf. Any claimed sharing must preserve soundness under aliasing.
- **LSPV-4:** Sequential proof-head/crossing results do not determine indexed proof-store aliasing. Keep the native machine ledger separate; no crossing lower bound was imported into RAT.

## Reproducibility

- Report: research/agents/lspv-5/2026-10-27_0444_LSPV-5_PHYSICAL_ALIAS_AGGREGATION179.tex
- Reproducer: research/agents/lspv-5/2026-10-27_0444_PHYSICAL_ALIAS_AGGREGATION179_repro.py
- Raw: research/agents/lspv-5/2026-10-27_0444_PHYSICAL_ALIAS_AGGREGATION179_raw.json
- Deterministic run: 645,821 assertion groups, 5,408 alias maps, zero failures.

## Decisive next lemma

For the strongest proposed two-level verifier, specify the physical proof stores, global offset function, and every accepted-run query set \(Q_\ell\). Prove or falsify \(|\cup_\ell Q_\ell|=O(\log N)\), charging locator computation, source authentication, resets, failed branches, and simultaneous live state.

All-ordinary-UNSAT affordable coverage, arbitrary-\(K\) ARC contraction, ARC-EDGE-90, and \(P\ne NP\) remain **OPEN**.

END_HANDOFF::PHYSICAL-ALIAS-AGGREGATION179
