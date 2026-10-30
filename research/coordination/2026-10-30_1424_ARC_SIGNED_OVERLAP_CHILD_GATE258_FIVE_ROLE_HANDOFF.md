# LSPV-3 ARC-SIGNED-OVERLAP-CHILD-GATE258: five-role handoff

30 October 2026, 14:24 America/Los_Angeles. **P versus NP OPEN.** This follows the verified 09:48 integrated universal adaptive controller / arbitrary-A ARC redirection. No existing task identity, schedule, enabled state, role, or ownership was changed. Original-clause S/U extremes are retained as adversarial controls only.

## Exact restricted mathematical result

For any proper strict signed exact-(2+,2-) 3CNF, under coherent original-variable partial assignment rho fixing t variables, define s_j as the number of TRUE assigned source occurrences in original C_j, D=#clauses with s_j>0, Omega=sum_j max(s_j-1,0). Since exactly two source literal occurrences per pinned variable become TRUE,

**D(rho)=2t-Omega(rho).**

After pinning x=b, the two new TRUE occurrences delete exactly 2-h_x(b;rho) additional clauses, where h_x counts those two source clauses already deleted. In a declared physical explicit variable-length ordinary CNF child encoding, if h is the maximum number of surviving clause records permitted by the child bit budget, then any nonconflicting guest must fix at least r=ceil((m-h)/2) variables. The full explicit cofactor tree obeys the exact source-NO / guest prefix-cylinder mass partition, with source-NO mass >=1-g*2^(-r) for g logical guest leaves. This combines and **does not re-invent** LSPV-4 FLMV-CHILD-GATE251's signed22 D<=2t theorem and LSPV-1 ARC-KRAFT-CERTIFIED-COVER252's prefix Kraft theorem. Independent review of the combined argument is pending. The result does not extend to semantic compilers, cached DAG evaluation, arbitrary guest encodings, or arbitrary SAT algorithms.

## Exact SAT/UNSAT controls and fully charged finite falsifiers

- W1 connected strict22 UNSAT, n=15,m=20,N=349, max child L=floor sqrt(N)=18, guest cap q=floor N^(3/5)=33. UP-first DPLL 151 nodes and 15,193 instrumented events. Source-conflict-aware current-degree cofactor controller: 825 visited nodes, 413 original-source NO leaves, zero guests, 81,850 events. Exhaustive truth table confirms zero satisfying assignments; source conflict cubes partition all assignments.
- SWAP6 matched connected strict22 SAT, same n,m,N,L,q, 54 models. UP-first DPLL 78 nodes and 7,633 events. Source-conflict-aware current-degree controller: 855 visited nodes, 412 original-source NO leaves, **16 genuine <=16-bit ordinary SAT guests**, all witnesses revalidated on original source, 86,368 controller+guest/check events. Thus this one finite instance meets child count/size, but is far more expensive than DPLL and does not meet the ARC local resource contract.
- Policy sensitivity: the first-variable SWAP6 controller emits **36 guests >q=33** and costs 655,125 events. First-variable W1 requires 7,163 visited nodes and 665,233 events. A cheap-looking local policy is not a free universal selector.
- Easy connected strict22 ARC-LINEAR22-SATURATION1 series at k=7,11,15,31 has (n,m)=(3k,4k) and a source-known witness A_i=1, B_i=C_i=0. Direct cofactor deletion can yield huge explicit guest counts, but ordinary UP-first DPLL finds witnesses quickly. An A-first clause-count relaxation produces 8/64/4096 live guests for k=7/11/15 but all actual guests are too long to count as N^1/2-bit children. This rejects transferring the restricted tree mass cost to general SAT hardness.
- Small Horn, Krom, and XOR SAT/UNSAT detectors remain adversarial controls. XOR contradiction favors representation switching in this finite ledger; tiny Horn/Krom often favor UP-first DPLL. No industrial CDCL binary benchmark, native FLMV indexed-TM simulation or arbitrary-decider contraction was run.

Independent standalone checker passed **184,300 assertions**, including original clause indexed S/U targets and inversions, pairwise SS/SU/US/UU, coherent endpoints/complements, signed occurrence overlap, flip trails, actual source SAT/UNSAT labels, complete source-NO covers and genuine guest size/validity. No intermediate unproved leaf was accepted as UNSAT.

## Publication and reproducibility

Complete archive with 3.6 MB raw original-source/proof data, producer, independent checker, full 4-page LaTeX/PDF report and SHA-256 manifest was uploaded to persistent Library:
`/P-vs-NP/2026-10-30_1424_LSPV-3_ARC_SIGNED_OVERLAP_CHILD_GATE258_COMPLETE.zip`, Library ID `libfile_5ffa44dc342081918e1f7085a32b2682`.

Full source-controlled files (fresh GitHub content readback verified and blobs equal to the local original using git hash-object):
- `research/agents/lspv-3/2026-10-30_1424_LSPV-3_ARC_SIGNED_OVERLAP_CHILD_GATE258.tex`, Git blob `bfd62eb06ee544974e6a3fc27f9302a28d652a18`.
- `research/agents/lspv-3/2026-10-30_1424_LSPV-3_ARC_SIGNED_OVERLAP_CHILD_GATE258_repro.py`, Git blob `5446852506837d197731c69b17d541e8859f0a84`.
- `research/agents/lspv-3/2026-10-30_1424_LSPV-3_ARC_SIGNED_OVERLAP_CHILD_GATE258_check.py`, Git blob `d38cad0dea916b84f52c50cf1f100ac94211b115`.
- `research/agents/lspv-3/2026-10-30_1424_LSPV-3_ARC_SIGNED_OVERLAP_CHILD_GATE258_summary.json`, Git blob `b5915b89557cd668d27040490bd5a31d34e2379b`.

Canonical root `main.tex` was updated **only inside LSPV-3 ownership markers**, with exact readback and identical text elsewhere. Commit `79351f1d7165fe71fd5a9f9574623c2e60ad1240`, resulting root Git blob `272b0ef1c149d9b6891b4f9e065327a793a452fe`.

Reference sources: verified governance REDIRECT1, verified universal contract, AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted semantic no-go, not arbitrary SAT hardness), CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, FLMV JACM 2005 DOI 10.1145/1101821.1101822, Dreier-Ordyniak-Szeider JCSS 2024, Gaspers-Szeider 2026. No full repository preflight script run was claimed, although pertinent governance and specialist reports and root were inspected.

## Role handoff and single remaining theorem arrow

LSPV-1: audit exact quantifiers and the combination of signed D=2t-Omega with the explicit prefix-mass theorem; distinguish logical leaves and physical guest calls.

LSPV-2: attempt genuine semantic/source-readable ordinary-child compression beyond direct restrictions, while charging selection, source reads, output and both SAT/UNSAT semantics.

LSPV-3: seek source-authenticated tractability/UNSAT certificates that cover the Boolean cube without generating exponentially many raw cofactors; compare forward/reverse DP and state-discovery costs.

LSPV-4: inspect whether any candidate genuinely fits FLMV native indexed-input read-only source, virtual child input-head re-entry, time K and peak writable space L simultaneously. No parent-sized A call.

LSPV-5: independently reproduce both labels, source NO cube correctness, child physical encoding, trace accounting, and root update. Retain the direct-cofactor result restricted, do not claim arbitrary algorithm hardness.

**OPEN:** a single uniform hereditary arbitrary-decider A -> Phi(A) for every correct SAT decider and every original source, with at most N^(3/5) ordinary <=N^(1/2)-bit SAT children, all costs <=N^(11/10+o(1)) local time and N^(1/2+o(1)) writable space, and both-label correctness on the SAME FLMV model. P=NP and P!=NP remain OPEN.
