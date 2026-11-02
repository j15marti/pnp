# LSPV-1 SOURCE-DISJOINT-BATCH-PROJECTION321
**2026-11-01 23:03 PST | Formal Proof Lead | PROVED/EXACT elementary one-phase canonical-source theorem | COMPUTATIONAL independent finite controls | P versus NP OPEN.**

## Exact obstruction and prior-work distinction
Same original F is modeled as canonical Monotone 3-SAT-(2,2) CNF and as a fan-in-two forward evaluator C_F on the ORIGINAL variables. F's evaluation circuit has 3m-1 source-private gates, but its SAT label is the existential disjunction over all original assignments. Forward circuit size, best OBDD size, or after-answer constant 0/1 do not lower-bound arbitrary SAT decision work. LSPV-5 REFEREE281 already proved a local existential source projector, and REFEREE282 proved the one-pivot four-resolvent quota; the present independently proved *increment* is a uniformly discovered **linear-size simultaneous safe pivot batch** with an all-input exponential work bound. Classical Davis-Putnam variable elimination and bounded-degree graph independence underlie the theorem; no novelty beyond this source-specific synthesis is claimed.

## Exact all-input theorem 321A
For EVERY valid proper duplicate-free Döcker monotone 3-SAT-(2,2) original F with n original variables, m=4n/3 proper width-three same-sign original clauses and binary length N, ONE fixed deterministic source-indexed compiler computes a set I of original variables and a provenance-labelled, possibly noncanonical residual G such that

|I| >= ceil(n/9);
G(z) = OR_{b in {0,1}^I} F(z,b) for EVERY assignment z to V(F)\I;
clauses(G) <= m, total_literal_records(G) <= 3m+4|I|;
max_clause_width(G) <= 4; number_of_candidate_resolvent_pairs = 4|I|.

The G relation remains exact under EVERY compatible future pin on surviving original variables; it does NOT promise correctness after new pins to deleted variables without source re-acquisition.

**Proof:** Build the primal graph joining source variables that co-occur in a clause. Each variable appears in four width-three clauses and has degree at most eight. Lexicographic greedy maximal independent-set selection removes at most nine still-unselected variables per chosen vertex and therefore constructs |I|>=ceil(n/9), with all discovery, index and source reads paid. Distinct selected variables never co-occur in a source clause. For each chosen x, its two positive and two negative original source clauses have exactly four positive-negative resolution pairs; remove those four source clauses, retain up to four non-tautological four-literal resolvents, and keep untouched source clauses. A resolvent cannot contain any other selected pivot, so all such eliminations commute, even in a different selected-pivot order. Davis-Putnam existential elimination yields exact pointwise G(z)=exists_I F(z,I). The removed source-clause sets are disjoint, yielding at most m-4|I| untouched clauses plus 4|I| resolvents, and at most 3(m-4|I|)+16|I|=3m+4|I| literal records. Tautology/duplicate deletion only reduces these counts. Every surviving derived clause retains a pair of original clause-ID parents and its pivot. QED.

## Consequence 321B, correct uniform but exponential decision algorithm
Validate all target-grammar/source bits, reject malformed strings, compute I and G, and enumerate every one of the 2^(n-|I|) surviving assignments. Output SAT on a satisfying G assignment; output UNSAT after exhaustive refutation. Thus ONE uniform deterministic exact all-input controller has total work

T_D(N,n) <= poly(N) * 2^(n-|I|) <= poly(N)*2^(8n/9).

The upper bound is EXPONENTIAL, not a polynomial-total-work construction, not a novel SAT algorithm record, and not an arbitrary-decider lower bound. Source-proof reconstruction is available but unnecessary for a one-bit answer: reconstruct a SAT witness by trying each deleted variable under surviving z and verify all original clauses; reconstruct a complete UNSAT certificate from resolution provenance and a full false-clause assignment cover. Both stronger outputs have their actual work and space charged.

## Exact forward/reverse circuit semantics
Under a declared clause-private fan-in-two AND/OR construction with free signed input negation, the original evaluator C_F uses 2m clause-OR plus m-1 final AND gates, i.e. 3m-1 gates. The projected noncanonical G with L surviving literal records can be explicitly compiled as a clause-private fan-in-two circuit with exactly L-1 binary gates, assuming a nonempty conjunction of nonempty clauses. This is a CONSTRUCTION count, not an unrestricted minimum. For every pivot x, F=(not x AND F|x=0) OR (x AND F|x=1) and exists_x F=(F|x=0) OR (F|x=1). No source-input assignment value need be retained or reconstructed by the decider. Circuit-SAT of the projected circuit remains an existential decision, not forward evaluation.

## Four falsifiers
F1: a computable Ω(n) source-disjoint batch exists, PROVED. F2: all original four-resolvent quotas commute across that batch, PROVED. F3: this single-phase n-shrink implies all-input polynomial total work, FALSIFIED as inference by remaining 2^(8n/9) search and noncanonical G. F4: compact forward C_F, a chosen OBDD or after-answer constant circuit forces all-decider hardness, INVALID.

## Same-original evidence, independent verification
A producer and separately implemented no-producer-import verifier exhaustively checked four ORIGINAL canonical sources, every selected-pivot order and every remaining assignment. **74,837 independent assertion groups PASS.**

| Source | Original n,m | #SAT original | Lexicographic greedy I | #SAT projected (different quotient) | projected clauses, literal records | forward gates original -> projected |
|---|---|---|---|---|---|---|
| Y6 | 6,8 | 20 | 1 | 16 | 5,16 | 23 -> 15 |
| F9 | 9,12 | 70 | 1,4 | 48 | 9,32 | 35 -> 31 |
| F15 | 15,20 | 1032 | 1,4,14 | 571 | 15,52 | 59 -> 51 |
| H15=F9 disjoint-union Y6 | 15,20 | 1400 | 1,4,10 | 768 | 14,48 | 59 -> 47 |

H15 is not the project's distinct F15 fixture. The checker independently rebuilt source clauses, authenticated quotas and original clause IDs, checked all 8,352 surviving assignment rows, 15 selected-pivot permutations, 264 F9 S/U/SS/SU/US/UU modes, all complete-assignment complement identities and five malformed source constructions. Coherent SAME-F9 original pins (x3,x5,x6,x7,x8)=(0,1,0,0,0), x1=0 have two SAT completions; flipping just x1 to 1 gives UNSAT with zero completions. An independent UP-DPLL comparison took one node on each branch, 48 vs 46 original-clause literal inspections. This batch method is NOT faster on these cases after charging prepass. U198/V198 controls are inherited from independently authenticated reports, NOT freshly rerun here. No native FLMV timing or industrial CDCL comparison was conducted.

**Countermodel to hereditary reuse:** F9 after projecting {x1,x4} has a width-four clause and x2 has 2 positive/3 negative residual occurrences. The four-pair rule and n/9 guarantee therefore CANNOT be applied recursively without new proof/reencoding. A variable-count contraction alone does not produce a power-short canonical child.

## Full work and peak-space ledger
Every source grammar, signed-occurrence, input/source/index/head read, graph link, deterministic greedy choice, four candidate resolvents per pivot (including deleted tautologies), normalization/deduplication, proof provenance, circuit/child/output-bit write, cache/replay, rejected policy, selection switch and guest DELAY/COPY/RECOMP invocation is charged. For a general adaptive controller,

W_D(z)=C_grammar+source/index/head+discover+select/failed/switch+resolution/GE/proof+cache/replay+child/output/bit+guest+SUM_{actually executed children y}W_D(y).

Simultaneous peak space is the maximum physically co-live index/head/adjacency/clause/proof/cache/ancestor/output/guest staging state, not an offline logical XOR difference. A conservative indexed read-only-input multitape implementation of the single phase takes O(N^3) preprocessing steps and O(N^2) writable bits; fallback contributes poly(N)*2^(n-|I|) time and polynomial peak space. These are **upper bounds in a declared implementation**, not an instruction-level FLMV measurement. They do not establish either strict (1.2,0.5) numerical FLMV transfer or a uniform arbitrary correct A -> Phi(A) power-short contraction. The latter still requires correct descendants and all unknown K,L/DELAY/COPY/RECOMP costs, plus separate SAT-to-Döcker near-linear local-bit transfer. P versus NP OPEN.

## Literature and project/source audit
Primary sources checked: Davis and Putnam (1960) JACM DOI 10.1145/321033.321034; Eén and Biere (SAT 2005) DOI 10.1007/11499107_5; Bryant and Heule (2021) arXiv:2105.00885 on proof-carrying existential BDD quantification; Döcker (2019) arXiv:1912.08032; FLMV JACM 2005 DOI 10.1145/1101821.1101822. Search queries included independent simultaneous Davis-Putnam elimination, bounded occurrence, OBDD quantification, and indexed-input FLMV. Repository prior work read FIRST: the 19:50 same-original five-role handoff, LSPV-1 MITER319/DOMINANCE320, LSPV-5 REFEREE281/282, LSPV-4 BACKDOOR324, LSPV-2 MATCH326, LSPV-3 GATE319/320/321, TRACE46, PARSIMONIOUS47; separate github.com/openai searches found no applicable exact original-source SAT implementation. Search absence implies no novelty claim.

## Reproducibility and publication
Full independently executed producer, no-import verifier, DPLL benchmark, detailed clause-ID projection records, raw JSON and SHA256 manifest are in the run's reproducibility ZIP. Repository compact verifier/code/raw and five-role directive are additional checked artifacts. Root main.tex must ONLY be changed inside the LSPV-1 marker after nonempty authenticated full-blob readback; otherwise no unsafe overwrite.

**Next decisive gate:** Find a fully charged effective source-authenticated reencoder that maps each noncanonical post-batch residual to a **strictly smaller valid original**, rather than expanding it. Test the existing LSPV-4 mixed gadget/rank-tax hostile controls. Alternatively acquire a uniform controller bounding the SUM of all executed SAT/UNSAT decision-work children polynomially, with no best-policy/semantic oracle. The present guaranteed n/9 variable reduction alone proves NEITHER route.

END_OF_VERIFIED_REPORT::LSPV-1::SOURCE-DISJOINT-BATCH-PROJECTION321::P_VS_NP_OPEN