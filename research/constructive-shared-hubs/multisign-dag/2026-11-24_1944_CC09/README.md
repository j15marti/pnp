# CC09: Constructive P versus NP, best current proof attempt

**Status: exact results in stated domains, finite executed controls, and a conditional universal theorem. The universal proof is not closed.**

The [27-page PDF](PNP_Best_Proof_Attempt_CC09_2026-11-24.pdf) is the complete formulation. Start with the [research report](CC09_REPORT.md) for the new result and [compact handoff](handoff.md) for the remaining dependency. The [LaTeX source](PNP_Best_Proof_Attempt_CC09_2026-11-24.tex) and [BibTeX references](references.bib) are editable.

## New result

Every unpinned pair of partitions into monotone NAE triples has the full Boolean affine hull. Two disjoint perfect matchings provide a constructive certificate for every unit direction. Consequently, agreement of the two half-system affine hulls cannot decide a four-partition source. This is a limitation of that summary, not a complexity lower bound.

The positive construction includes exact circulation compilation, pinned-support affine acquisition in at most n parity queries, guarded cycle composition, a model-containing one-third phase chart, and actual-witness span composition on certified affine interfaces. The missing universal step is polynomial discovery and aggregate work on every relevant residual.

## Reproduce the executed controls

```sh
python3 CC09_check.py --stage controls --output CC09_results.json
python3 CC09_check.py --stage scaling --output CC09_scaling.json
```

Python standard library only. The recorded runs contain 48,770 control assertions and 27,386 scaling assertions with no discrepancies. Finite enumeration is used only in the explicitly described controls. This script is not a universal polynomial SAT solver. Physical peak memory and cumulative memory were not measured.

## Build and inspect the PDF

The LaTeX can be built with a complete LaTeX installation and BibTeX. The delivered PDF was rendered from the same source using the included fallback:

```sh
python3 build_pdf.py
python3 verify_pdf.py --render-dir preview --output PDF_QA.json
```

The fallback requires Pandoc, ReportLab, Matplotlib, and Pillow. Document inspection requires PyMuPDF. Every mathematical expression must render successfully. The inspection script checks the PDF artifact, not the mathematical proof. Its output records the final PDF digest. Manual visual review covered all pages via montages, with enlarged checks of dense equations and the composition theorem.

## Provenance and verification

[sources.json](sources.json) identifies repository sources, recovered earlier artifacts, searches, and limitations. [prior_CC02_CC08.zip](prior_CC02_CC08.zip) contains twelve recovered earlier files, unchanged, with a provenance manifest. Historical saved results are not relabeled as new executions. [manifest.json](manifest.json) records bytes, SHA-256 digests, and Git blob IDs for the publication files.

The separate `publication_verification.json` is added only after the publication commit and issue comment have been read back. Publication is additive in this directory. No peer manuscript, agent configuration, or research schedule is changed.
