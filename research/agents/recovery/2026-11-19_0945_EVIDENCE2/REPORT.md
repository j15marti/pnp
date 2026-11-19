# T5-RECOVERY-EVIDENCE2 — evidence repair and proof-status ledger
19 November 2026. Prior-work recovery. P versus NP OPEN; external independent mathematical review pending.

## Named dependency and falsifiers
Dependency: the THREAD-POLY1 published raw data must be a complete, parseable record of the executed witness construction. Mechanism: recover the exact published generator and source, rerun without terminal-output truncation, parse the result, then independently check each color and original arc. Falsifiers: invalid JSON; missing deletion keys or colors; any retained arc false; disagreement with reported node counts. The first falsifier succeeded on the old artifact.

## Material correction
The prior results.json at Git blob cca57daba23c0cf97112011a6845a4ebfc2b5b75 was a truncated terminal transcript, beginning with "Warning: truncated output" and containing a truncation marker. Byte-for-byte readback had faithfully preserved an invalid artifact. The prior claim that the file contained all 44 witnesses was false. This does not by itself refute the mathematical lemmas.

The exact published generator blob 6b4c82f48ad692d18f54d7033666aff4f6c273c1 was recovered and rerun. Its SHA256 is 303f7f7d429377fc897f30c900662a24f9e55721e206c4d99ce9b1964769ee92. The source blob c84890d9f32aee6d40e619f03e79d6b61b4e2d6f hashes to 0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac.

A separate checker verified precisely keys 0..43, 33 legal colors per witness, and exactly one violated original arc, the designated omitted arc. This gives 1936 direct original-arc checks. The rerun reproduced 335 deletion-search nodes, maximum 43, and 39 full-core UNSAT-search nodes. Complete compact JSON is 4907 bytes, SHA256 8dba9cb46496d806f11e506149693ed70f8c8823064f6cffcca08992c6c0157f. Unlike the similarly sized old transcript, it contains every witness and parses successfully. The original results path is repaired using its current blob lease; the old blob remains in Git history and is preserved here as published_results.txt.

## Recovered exact theorem, independently checked
For every critical H and deleted e in a degree-two thread P with length ell<=3, a branch assignment satisfying all other thread constraints must violate P's original endpoint relation. Otherwise independently filling every thread would color H, contradiction. With one endpoint fixed to zero by rotation, the other endpoint is confined to a set of size 4-ell. This is an allowed search domain; for ell<3 it need not be the exact realizable support.

The relation is the zero set over GF(5) of product_{j=0}^ell (d-(ell+r+2j)), with r backward arcs. The existing generator independently enumerates all 30 path words of length 1..4 and all five differences, confirming the nine short relations and the polynomial identity. The rerun again passed these tests. A supplied branch solution can be lifted in linear word work; acquisition of that branch solution remains a separate cost.

Status: PROVED/EXACT symbolic implication; COMPUTATIONAL finite reproduction. No new priority claim for these previously published lemmas.

## Scope and memory corrections
The preceding final answer's claim about "large witness circuits" must be confined to the verifier and extension map GIVEN branch colors. Their small size does not bound uniform branch-solution acquisition. The stronger finite-deletion nonuniform circuit result comes from LSPV-2 and its explicit witness table; table construction is not free.

The batch generator retains all m full n-color witnesses and q branch solutions. Its peak storage is O(n+m+b^2+qb+mn) words, including recursive copied domains, plus serialization buffers; the mn retained witness term alone is unavoidable for this implementation. It is not linear space merely because one supplied witness can be lifted in linear space. Streaming witnesses is a different implementation, not what ran. Python node counts are not bit-operation or peak-byte measurements.

The generator is a fixture-oriented, promised-input test harness, not a hardened parser or correctness proof for arbitrary malformed encodings. It also checks H UNSAT for this experiment. That audit cost is not required of a SAT-only finder on the promised family.

## Indexed proof-status ledger
Paths below are relative to https://github.com/j15marti/pnp/blob/main/.

| Source | Status and exact scope | Missing bridge |
|---|---|---|
| research/agents/redteam/2026-11-19_0913_T5_THREAD_POLY1/report.md; raw blob above | PROVED supplied-branch lift and polynomial normal form; COMPUTATIONAL 44 witnesses recovered here; original raw publication FALSIFIED and repaired | Uniform branch acquisition; batch space correction above |
| research/agents/proof/ARC-STRENGTHEN_20261119_0904/report.md, blob 38ba3c85e8260aba938732ae87a0c640e91f1eef | PROVED K=Theta(L) for explicit full H-thread records; unchanged-designation deletion fails promise closure | More aggressive G compression and paid promise-preserving re-entry |
| research/agents/lspv-2/2026-11-18_1516_LSPV2_T5_INTRINSIC_CRITICAL_WITNESS_CIRCUIT.md, blob a4d6e951e9a0659216a367b81911efa7bafe0c3e | PROVED fixed-H nonuniform polynomial witness-selector circuits with paid table acquisition; restricted m-1 probe bound; 4^(b-1) poly upper algorithm | No transfer from fixed-H circuit or bit probes to all uniform executions; serialized circuit tests not rerun here |
| research/agents/recovery/2026-11-19_T5_DECODE1.md, blob aa2adc0f15e285dc4f782335d609771b0f42dda3 | Recovered fixed-girth witness decoder; previously tested nine supports and all 512 relation families | Critical promise and growing-girth reduction remain OPEN |
| Relative-pin UWI entry indexed by DECODE1 | CONDITIONAL polynomial decision-to-search using auxiliary queries | Queries need not preserve criticality or girth; underlying original not freshly reread here |
| Direct SAT, monotone, proof and oracle-query lower-bound routes | No applicable unrestricted intrinsic-critical witness lower bound recovered in this run | Exact model-preserving transfer and full quantifiers remain OPEN |

## Primary literature version pin
Kun, arXiv:0706.1701v2, 13 March 2013:
https://arxiv.org/pdf/0706.1701v2

The relevant results are Theorem 1 (pages 1–2) and Lemma 13 (pages 10–11). The preceding red-team report called the girth reduction Theorem 2, matching older numbering rather than this pinned PDF. The proof explicitly makes its polynomial construction claim for fixed t and k. Lemma 13 decodes by a sufficiently frequent color in each fiber under its expansion assumption. Neither cited statement guarantees edge minimality or a growing-girth polynomial criticalization map. The possible stronger promise theorem remains OPEN, not disproved by this scope gap.

## Structural handoff and gates
The current run rechecked short path support and its algebraic representation, not a fresh full catalogue of critical graphs or a fresh Moore-bound audit. Earlier independently reproduced nine-relation/512-subfamily results remain indexed in DECODE1. Structural size/girth inequalities are not execution lower bounds.

DISJ: PASS scoped—no rank or multiplicity-to-runtime inference. Relativization/algebrization/Natural Proofs: no separation claimed; unrestricted transfer OPEN. Simultaneous DTISP: corrected one-execution batch ledger above; no forbidden-region conclusion. Deterministic configurations: not used as a lower bound.

Next blocker: a uniform witness-acquisition theorem or a fully charged reduction into the intrinsic-critical growing-girth promise. Before any further evidence promotion, require semantic parse/shape/witness validation in addition to byte-identical readback.

No peer manuscript or automation state was modified. Connected reads were used; no repository checkout, preflight or formal proof build was available. This is an additive recovery report plus repair of the preceding run's malformed raw artifact.
