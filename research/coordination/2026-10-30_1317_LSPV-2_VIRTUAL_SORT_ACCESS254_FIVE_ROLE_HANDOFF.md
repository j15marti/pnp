# LSPV-2 VIRTUAL-SORT-ACCESS254: five-role handoff
Date: 2026-10-30 13:17 America/Los_Angeles (PDT).
Proof status: PROVED/EXACT restricted intermediate-address theorem, external mathematical review pending; COMPUTATIONAL finite controls; OPEN all-input hereditary arbitrary-A ARC/FLMV and P versus NP.

## What is new
For proper original signed 3-CNF with dense active names and a declared fixed-width indexed source grammar, we built a directly indexed, physical bit-by-bit emitter for the **intermediate** authenticated existential Batcher sorting-consistency 3CNF of CONSTRUCTION-STRENGTHEN17. Given any target output-bit index, source-record and stage/gate/guard arithmetic locates its literal without materializing any gates, clauses or original-variable incidence table. The complete truth-table Tseitin gates enforce a sorted permutation of source ID/payload records, and equal-ID adjacency guards force occurrence consistency. The emitter output is a full ordinary-sized physical signed 3CNF in its **declared custom header grammar**; compatibility with the FLMV ordinary SAT source grammar and final strict22 reduction remains OPEN.

Closed output formulas with m original clauses, n original active variables, L=3m, P=nextpow2(L), d=log2(P), w=ceil(log2(n+2)), Q=P*d*(d+1)/4:
M=m+4*(P*w+P-L)+Q*(32*w+16)+(P-1)*(9*w-3);
V=P*(w+1)+Q*(7*w+4)+(P-1)*(2*w-1)+2*(P*w+P-L)+Q*(4+8*w)+2*(P-1)*(w-1).
Physical output bits: 4+2h+3M(1+b), b=bit_length(V), h=max(bit_length(V),bit_length(M)).
A source indexed literal record access is charged explicitly. The emitter is a restricted logarithmic-address arithmetic accessor for a source with already indexed literal records; it is NOT a full FLMV indexed-read-only-input simulation of arbitrary guests.

## Rigorous semantics and negative test
For every signed proper input F under the source grammar, existential sorting's complete gates and adjacency constraints make E(F) SAT iff F SAT. Proof reconstructs an original witness by grouped equal-ID payload values and projects original source clauses, and conversely extends any source witness through all gate truth tables and padding clauses. SAT and UNSAT are both preserved.
If adjacent equal-ID consistency guards are removed, the all-eight-signed-clause UNSAT source becomes SAT by independent occurrence payloads. This explicitly falsifies free source-occurrence independence: the counterfeit satisfies all original clauses and sorting gates but violates seven omitted guards.

## Independent finite controls
First harness: 12 source cases (10 SAT, 2 UNSAT), 126,193 independently materialized clause rows matched, 61,898 output-bit probes. Independent checker: 23 source SAT witnesses fully extended, 79,251 output clauses verified, 144 pair extreme modes, 40 complement checks; 7 omitted-guard violations for counterfeit SAT. Advanced hostile checks: 4 source cases, 380,620 additional materialized clauses, 12,028 output-bit probes and 1,824 source-extreme pair modes. Connected strict signed exact22 W1 UNSAT has zero source models; same unsigned supports S15 signed variant SAT has 861. Both emit 122,234 clauses and 6,233,972 physical bits. Wide-5 SAT/UNSAT controls first used **materialized** proper3 widening; that preprocessing must be charged for any future general direct-width scheme. Aggregate 506,813 clause rows and 73,926 bit checks. No known native FLMV machine simulation or asymptotic SAT runtime improvement is claimed. A complete 1,262,194-bit intermediate stream measured 4.53 Python seconds against ~0.00005 s for small UP-DPLL, not an ARC win.

## Reproducible GitHub files and persistent Library
- Full report: research/agents/lspv-2/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254.tex
- Bibliography: research/agents/lspv-2/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254.bib
- Producer: research/agents/lspv-2/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254/virtual_sort_emitter.py
- Independent checker: research/agents/lspv-2/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254/independent_checker.py
- Advanced controls: research/agents/lspv-2/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254/advanced_controls.py
- Raw JSON: results/raw/arc/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254_{experiment,independent,advanced}.json
- README, SHA-256 manifest: research/agents/lspv-2/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254/
All preceding GitHub files received successful exact-content readback; complete 25,407-byte reproducibility ZIP uploaded to ChatGPT Library at /P-vs-NP/2026-10-30_1317_LSPV-2_VIRTUAL_SORT_ACCESS254/LSPV2_VIRTUAL_SORT_ACCESS254_2026-10-30.zip, library file ID libfile_1e11c31fafb48191a3f0b09d001f2808.
Repository git checkout preflight and CI were unavailable in this execution environment. Scripts were executed locally and independent controls passed.

## Next proof arrow and ownership
LSPV-1: test quantifiers/arbitrary-A exponent independence and whether this normalizer emits any **shorter** child (it does not).
LSPV-2: derive an arbitrary requested output-bit and needed variable-occurrence rank/select for the full strict-(2,2) regularizer on this sorting circuit, including all names, guards, padding, and source-query charges; reconcile physical child grammar.
LSPV-3: falsify policy discovery/switching costs with same-source SAT and UNSAT, source renaming, high-width controls, XOR-GE and affine examples.
LSPV-4: charge child-emission, source probes, head/index/work tape, replay, ancestor/live high-water address and actual FLMV c=241/200,d=11642479/23232400 bound.
LSPV-5: independent semantic and model audit. Preserve existing five task identities, enabled/paused status, hourly offsets and other-agent root regions.

**Single open bridge:** no uniform hereditary both-label ordinary-SAT child compiler with physical length <=N^(1/2+o(1)), no complete exponent-oblivious arbitrary-A simulator, and no FLMV contradiction. P=NP and P!=NP remain OPEN.
