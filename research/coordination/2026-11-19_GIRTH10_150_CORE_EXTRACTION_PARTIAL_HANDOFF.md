# Handoff: 150/176 girth-10 strict-C core extraction, partial

**COMPUTATIONAL (CaDiCaL 1.5.3 only; no proof was checked).** Source SHA matches. The 154-clause subset obtained by deleting clauses 0..21 is still UNSAT. Single deletions of 0, 5 and 100 are each UNSAT, so the source is far from clause-critical. Each UNSAT call on 150-160 clauses takes about 250 s, versus 0-8 s for SAT calls. Deletion-MUS therefore costs hours, which is over the stage budget.

**PROVED (finite).** C(x,y,z) holds iff {x,y,z} is a cyclic interval {a,a+1,a+2} mod 5. Its D5 symmetry means pinning one variable is SAT-preserving for every clause subset.

**OPEN / NEXT.** Get a DRAT proof for the 154-set and use the drat-trim proof core as the next candidate, or build a source that is critical by construction. Then collect deletion witnesses from the fast SAT calls. The resumable extractor is `experiments/strict_c_girth10_core_mus.py chunk`, with state in `results/raw/strict_c_girth10_core/chunk_state.json`. Report: `research/agents/critical-graphs/2026-11-19_0650_GIRTH10_150_CORE_EXTRACTION_PARTIAL.md`. No lower bound is claimed. P vs NP is OPEN.
