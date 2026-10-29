# LSPV-4: PAID-SELECTOR-GADGET-FIREWALL224

Date 2026-10-29, Los Angeles. Restricted theorem and independent computational audit. P versus NP OPEN.

## Reproduce

From this directory:

```bash
python3 LSPV4_PAID_SELECTOR_GADGET224_repro.py > rerun.json
cmp rerun.json LSPV4_PAID_SELECTOR_GADGET224_raw.json
```

To recheck the original Library audit, unpack `Connected_Interface_Audit.zip` (not included in this source-only bundle) and run its `audit.py`; compare stdout byte-for-byte with `results.json`. Source-preserving Library file ID `libfile_a2862f0165b4819195a88d9e896a42a7`. Original JSON SHA-256: `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`. In this run that check passed.

The code is deliberately dependency-free and uses exhaustive enumeration on finite control instances. It does not count native TM transitions. The mathematics is in the LaTeX source and formatted PDF. The `.bib` is supplied for portability; references are also embedded in the PDF source as an explicit bibliography, so BibTeX is not required.

Sources inspected through connected GitHub: `j15marti/pnp/research/agents/lspv-4/2026-10-29_0636_LSPV-4_ADAPTIVE_MIN_CLUSTER_PORTFOLIO223.tex` blob `04d9a94e070c93a37e29d079cbd0676d2eda1203`, `msoos/cryptominisat/src/gaussian.cpp` blob `7b9d200c1c1d8e344ce0c3109bfc92806a14359b`, `uds-psl/coq-library-complexity/theories/NP/TM/mTM_to_singleTapeTM.v` blob `a12c882a5aed008870e913dd292b6f2530432ecc`, and `openai/math/.../build/sections/01-introduction.tex` blob `5ad06c26238e2572e93f68b380f542b2ab1845fe`.

Limitations: The proper signed 3SAT-to-mixed XOR/2CNF transformation does not preserve exact-(2P,2N) occurrence balance and expands instead of shrinking. The exponent K=m and cover number k>=2m constrain one known algorithmic upper-bound expression. They are not lower bounds for all algorithms. No kernel verification performed.
