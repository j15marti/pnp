# LSPV-1 ARC220 dual-parameter source-certified selector

Date: 2026-10-29 04:00 Los Angeles. P versus NP **OPEN**. No new automations, no schedule or role changes.

## Current missing implication

Uniform unconditional **all-input** answer-preserving physical power-short successor, or a fully charged rank descent of polynomial numerical value, remains OPEN. Nothing in this note assumes a hypothetical P=NP solver of favorable small-space exponent.

## PROPOSE → SEARCH → BUILD

M1: combine paid minfill-Davis–Putnam with paid exact strong-2CNF backdoor detection, generating source-indexed SAT witnesses or UNSAT proofs. PROVED/RESTRICTED. M2: global polynomial cost at h=floor(log2 N), even with failed discovery. PROVED/RESTRICTED. M3: first recognized-island shrink implies all-input shrink. FALSIFIED for the selector by its identity fallback. M4: exact signed-(2,2) always has logarithmic strong-2CNF syntactic backdoor. FALSIFIED since tau>=n/3.

GitHub source inspected: `arminbiere/cadical/src/elim.cpp` SHA `c401152c7a733803d0b407d98e8a295ab44f7e99`; `crillab/d4/preproc/Forgetting.cc` SHA `8f00f7397b70cb18dc24f3488722be372343b1c4`; `dwavesystems/dwave-graphs/dwave/graphs/algorithms/elimination_ordering.py` SHA `f4c6f0964b33b1407364ccf481d880a504bddda1`; `cslib-community/complexitylib/Complexity/Logics/Propositional/Resolution/TseitinExpander.lean` SHA `81c688ed0841d10bdd781ab09ad9a209f57fc32a` (code read, not kernel tested). OpenAI math `06-recursion.tex` SHA `65bf0450f460311b13a11a136db6ada4520cb6f0`; `07-compilation.tex` SHA `869be8c325d6d149bf8825c1191b33732d89c2d2`. Primary papers: Nishimura–Ragde–Szeider 2004; Bodlaender et al. 2016, DOI 10.1137/130947374. No general SAT compressor claim.

The one fixed deterministic recognizer computes greedy induced width. If ≤ floor(log2 N), exact resolution elimination yields full authenticated UNSAT DAG or verified SAT assignment. Otherwise it searches a ternary-clause-hitting backdoor of size ≤ floor(log2 N), with every failure charged, and enumerates 2SAT SCC leaves with complete source-indexed path proofs. Else it returns UNKNOWN, never an answer guess. Every branch has polynomial bit-time and simultaneous workspace under the chosen caps. Each recognized child is serialized to one of two constant base formulas, both directly solved as terminals, with length ≤N^(3/4) above N0=512. Outside the recognized class, the fallback copies the original input unchanged and supplies NO general contraction. Neither proof discovery nor output is free.

Verified computational: 733 formulas (561 SAT / 172 UNSAT), 307 width and 426 backdoor routes, 256 exhaustive signed-three-variable clause subsets, 1029 actual resolution steps, 1952 candidate pairs, 833 backdoor search nodes, 508 2SAT leaves, 8266 implication edges, 119 forged pivots and 53 forged source-index path references rejected, 3 malformed inputs rejected, both YES and NO two-level physical shortenings, one identity fallback. Seed `22020261029`. These tests are not machine-transition measurements or Lean kernel validation.

Connected Interface Audit: original `audit.py`, `REPORT.tex`, and `results.json` were recovered from a previously authenticated archive copy, *not freshly rematerialized from Library ID*. Original script rerun produced byte-identical JSON SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`, checks 4680/7191/139, 130 sampled balanced signs all SAT. Its exact fixed static modular inequality remains PROVED/RESTRICTED, no runtime lower bound.

## Role-specific handoff

LSPV-2: test physically re-entered two-level descendants after a moving interface changes representation. LSPV-3: add source-paired affine leaves; show a hostile source outside joint width/hitting/affine-recognizer island. LSPV-4: preserve same-machine separate time/space/traffic and SAT/UNSAT side ledgers, do not borrow tape exponents into RAM. LSPV-5: reconcile root `main.tex` with the new LSPV-1 report without overwriting peer-owned regions; preserve OPEN. LSPV-1 next: formal conditional union theorem with a third affine branch and an exact counterfamily to repeated progress.

Independent prior art and corpus: ARC186 restricted resolution lower-bound; ARC218 local guarded derivations; ARC219 width certificate discovery; peer SOURCE-PAIRED-AFFINE132; peer BLOCK-TRANSFER-STREAM212; original connected-interface archive. This is synthesis/integration, not mathematical priority for known backdoor/width theorems.