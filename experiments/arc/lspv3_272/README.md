# INTERFACE-SOURCE-SELECTOR-GATE272 reproducibility package

Status: restricted exact proof and finite computational tests; external mathematical review pending; universal arbitrary-A ARC and P vs NP remain OPEN.

The producer and checker require Python 3.10+ standard library and complete local `fixtures271.json` from the prior LSPV-3 control archive. To avoid time-limited jobs, execute these steps separately in this directory:

```
python run272.py --out raw272.json
python verify272.py raw272.json > check272.json
pdflatex -interaction=nonstopmode -halt-on-error 2026-10-31_0324_LSPV-3_INTERFACE_SOURCE_SELECTOR_GATE272.tex
```

The checker is independent of the producer's solver, predictor, signature data, and proof implementation. It validates every source by fresh DPLL, verifies SAT witnesses and original-source resolution for UNSAT PIN sources, enumerates SS/SU/US/UU modes for every source clause pair (distinct variables per proper clause), checks complement and Gray traces, and independently validates four deliberately corrupted records are rejected. On b<=2 it additionally enumerates every global Boolean assignment.

Source experiments: 25 original CNFs, 13 SAT and 12 UNSAT. The `source_kind` field distinguishes recognized proper ternary PIN grammars from adverse Krom, Horn, affine and strict22 sources. All experiments preserve original indexed clause literals; signed renamings are genuine bijections, not independent occurrences. Native FLMV random-access indexed-TM time and space are not measured. Python event counters are a finite policy stress test, not a machine lower bound.

The JSON `raw272.json` contains all original clauses, local S/U occurrence targets and inverses, indexed four-way pair compatibility, globally coherent zero/one assignments, per-clause 0/1/2/3 true-literal status, Gray/complement trails, source-certified forbidden cubes, resolution steps, witnessed assignments, exact DPLL/DP operation counters, stage allocation high-water mark, physical DIMACS bit lengths and retained certificate JSON bits.

The theorem is an elementary exact membership-oracle restriction: when one interface relation is U={0,1}^b, distinguishing an empty relation from an unknown singleton using only individual Boolean membership probes requires 2^b deterministic probes on the empty instance; with worst-case error <=epsilon, expected probes on the empty instance are >=(1-2epsilon)*2^b. This theorem does not transfer to a general SAT machine that reads source clauses. A validated PIN grammar supplies an explicit countercontrol, including a full original-source UNSAT resolution proof, while unrecognized formulas use charged DPLL fallback.

`manifest272.json` contains SHA-256 hashes for source artifacts. `summary272.json` is a compact comparison. PDF was created by compiling the report TeX and visually inspected by rendering. No universal ordinary-SAT ARC child compiler was built.
