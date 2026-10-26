# LSPV-2 to Lead and Resource Auditor: CIRCUIT-QPORT-SWAP162

2026-10-26 05:40 UTC / 2026-10-25 22:40 Los Angeles. P vs NP OPEN. No full SAT circuit compression or fast coNTIME companion obtained. Five schedules and stagger unchanged. No external messages.

## Recovered evidence and missing original
Read 14-page Library PDF sat_resource_extension.pdf (October 26). The separate PNP_Circuit_Certificate_Continuation.pdf filename and source ZIP were not recovered; claimed Q348 source and RUP proofs, and mixed M_j data cannot be verified here.
Read actual historical Q15 in LSPV-4 PCRETRACT1 Appendix A; earlier report has a 69-node width-three port-resolution proof. New independent exhaustive checker validates all 2^15 assignments to 20-clause W1, all 20 deletions, Q15's 244 models and forced-zero ports {1,7,13}, all-zero model and exact sign profiles. J seven-clause gadget has five auxiliaries with 2P,2N and 5/9 extensions for its port literal false/true.

## New exact construction
The October 26 PDF's signed regularizer uses a Q solely through forced-false zero-extensible three ports (1 positive + 2 negative occurrences) and all other variables exactly 2 positive +2 negative. Replace its unobserved 348-variable 463-clause Q with verified historical 15-variable 19-clause Q; preserve SAT iff, all-source clauses, two-level eligibility and proper exact-(2,2) profile.
The original coefficients v348=366m+381n, m348=488m+508n become v15=33m+48n, m15=44m+64n, with 3m15=4v15. The separately claimed 131-fold monotone adapter would change its output counts from (47946m+49911n, 63928m+66548n) to (4323m+6288n, 5764m+8384n). 131=3+16*8; independently checked H's 8 clauses, 6 vars, 18 models and all 512 port assignments of already-monotone arm. Mixed M_j data remains unverified.
Both Q pairs have incidence deficit 4q-3m=3. Difference (333,444)=111*(3,4) is only numerical, NOT a proof that Q348 contains 111 filler components.

## Executed recursive checks
Full standard-library local program physically built:
SAT 3-variable/2-clause -> (210 vars,280 clauses) -> (19320 vars,25760 clauses), witness checked both levels.
UNSAT 3-var/8-clause -> (408,544) -> (37536,50048); UNSAT from proven model projection/forced port, not from enumerating 2^37536 assignments.
7-of-8 SAT, Horn and affine SAT controls; all generated clauses proper, unique and exactly (2P,2N).
Four 2-bit controlled fixed-incidence sources: at second level 77,280 signed slots are 77,272 constants and 8 literal-source-bit copies, zero nonlocal signatures.

## Exact limitation on access and full decision circuits
This proves literal/constant COORDINATE DEPENDENCE when incidence positions fixed, but not polylog(N) computing of the input position j for arbitrary output index i: inverse occurrence offsets must be constructed, not postulated. A comparator actually sorting one-bit keys computes AND/OR (nonlocal), but the PDF instead ENCODES the fixed comparator circuit as SAT, so that observation does not refute it.
Full C_{A,N} must decide all N-bit SAT strings; a single-instance gate trace after fixed input gives only a constant. An eight-clause presence mask family has 255 SAT of 256 masks (function NAND8) and one UNSAT; equal-length ordinary 3CNFs have opposite labels. q=1.29 instance-specific projected relations do not constitute full C_{A,N}.
The PDF's d=1.802 subpoly-space seed is an additional hypothesis, NOT implied by P=NP. Pippenger-Fischer O(T log T) circuitization is model-qualified to one-dimensional tape machines; do not silently give indexed read-only RAM the same bound. C(d)=651000/361301=1.801821749732...; gadget constants alone do not cross exponent d to C(d). Outputting original Theta(N^d) gate records before compression costs Omega(N^d) bit writes. Source-aware direct small-circuit generation remains OPEN. Log gate IDs, input bit reads, ancestor retention, repeated virtual bit accesses and peak space.

## Artifacts
LaTeX: research/agents/lspv-2/2026-10-26_0540_LSPV-2_CIRCUIT_QPORT_SWAP162.tex
Reproducer: research/agents/lspv-2/2026-10-26_0540_CIRCUIT_QPORT_SWAP162_repro.py
Raw: research/agents/lspv-2/2026-10-26_0540_CIRCUIT_QPORT_SWAP162_raw.json
Predecessor: research/agents/lspv-4/2026-10-13_0849_LSPV-4_PCRETRACT1.tex

FILLED/RESTRICTED: Q15 3-port model, substitution, explicit counts, two real regularizer levels and fixed-incidence sign locality.
CONDITIONAL: local indexing of every output bit, mixed M_j adapter after replay, indexed RAM-to-circuit compiler, one-machine resource bounds.
OPEN: Q348 source/RUP, full M_j 169 RUP tests, end-to-end virtual Cook fixed-verifier accessor, full C_{A,N} compression, universal UNSAT certificate coverage.
FALSIFIED/RETIRED: source-bit locality of executed comparator; treating a fixed-instance trace as full decision circuit; exponent reduction from gadget constants.

Next decisive lemma: implement an end-to-end map source input bit -> fixed Cook verifier pin -> occurrence clone -> Q15 -> M_j adapter output bit with polylog primitive bit arithmetic/O(log N) index space, including invalid encodings. Audit with Lead and Resource Auditor. P != NP OPEN.
