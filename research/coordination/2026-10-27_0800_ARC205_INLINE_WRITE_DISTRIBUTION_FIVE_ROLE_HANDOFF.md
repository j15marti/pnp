# ARC205 role-safe handoff: inline cross-program sparse-write distribution

Date: 2026-10-27 08:00 PDT / 15:00 UTC. LSPV-1 Formal Proof Lead.
Status: **PROVED/EXACT restricted model, independent review pending**. **P versus NP OPEN**.

## What changed

The existing ARC197 full-crossing-label distribution already eliminates the
number-of-inline-programs factor when programs are physically on the left
shore. WRITE-TIGHT2 compresses complete crossing histories into ordered
actual-work-symbol-change events and full boundary-position/control events,
but its theorem currently retains a conservative +b for the number
of sound programs. ARC205 explicitly combines them.

For one fixed finite interpreter with exactly one sequential read-only
source head, fixed k blank sequential work tapes, a fixed-width inline
program slot entirely left of the invariant source gap, and **global
SAT soundness for each program**, *different* selected programs may
be spliced when the same compressed chronicle occurs.  This gives
program-independent injection, even for b>=m, so

    #Easy <= min(2^m, 2^(B_w+1)-1, G*(2^(B_t+1)-1))
    B_w = C_U*(D+1)*(S+2)^k*(ceil(log2(S+2))+1)
    B_t = C_U*(D+floor(T/G)+2)*(ceil(log2(S+2))+1)

where N=Theta(m log m) is formula-source bits, G=Theta(N),
and T,S,D are **same accepted-run** physical resource ceilings.
If the nontrivial term is <= 2^(m-2), at least 75 percent of the
diagonal satisfiable promised sources defeat **every** admissible
sound inline program within those ceilings.

For fixed polynomial time cap and D<=N^(1-epsilon), at least 75%
of the diagonal SAT promise inputs have no sound accepting program
in T<=c*N^2/log^2 N, for sufficiently small fixed c>0.
The already restricted WRITE-TIGHT2 exponent faces d+k*s>=1 and
d<1 => t>=2 survive. No exponent K=1.802 seed is assumed.
The false old 0-write/O(1)-visited-space claim remains retired.

The claim is **not a full-SAT lower bound**, **not an FLMV indexed-RAM
restriction**, and **not all-UNSAT certificate coverage**. In particular,
total machine input bits X=N+b must be distinguished from formula bits N
if the inline program slot is long.

## Proof DAG

| Node | Status | Precise scope |
| --- | --- | --- |
| Verified signed exact-(2,2) W1 -> DISJ promise | PROVED/EXACT inherited | Proper 15-variable/20-clause W1 and canonical A/fixed/B clause order |
| Reconstruct full cut work configuration from all actual writes | PROVED/EXACT restricted | Initially blank, fixed finite tape alphabets and charged all work heads |
| Equal chronicles of DIFFERENT programs splice to UNSAT | PROVED/EXACT restricted, referee pending | Program prefix wholly left, fixed source-relative cut, per-program globally sound acceptance |
| Program-independent distribution bound | PROVED/EXACT restricted, referee pending | Same-run actual D, visited S, physical input T |
| At least 75% need sparse-write quadratic time | CONDITIONAL on stated resource ceilings | Easy satisfiable DISJ promise, same U |
| Transfer to two source heads, independently readable proof tape, uncharged output head or indexed RAM | FALSIFIED/RETIRED | Explicit comparison shortcuts and missing crossing metadata |
| All-input source-authenticated UNSAT acquisition grammar | OPEN | Generic ordinary formulas, two hereditary levels |
| Strict arbitrary-K ARC -> FLMV contraction | OPEN | Same indexed-RAT machine, actual time and peak indexed space |
| P != NP | OPEN | No unrestricted separation |

## Reproducible materials

- [LSPV-1 ARC205 formal LaTeX proof](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-27_0800_LSPV-1_ARC_INLINE_WRITE_DISTRIBUTION205.tex)
- [Standalone Node.js reproducer](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-27_0800_ARC205_inline_write_distribution_repro.js)
- [Immutable raw assertions](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-27_0800_ARC205_inline_write_distribution_raw.json)

Results: 308,838 assertions; 0 failures; 174,251 crossed fooling
pairs; 1,022 distinct event codes; 6,558 promised sound
acceptances; 9 state-omission collisions; 850 codebook rows;
1,339,848 two-head probes. Finite checks are selector-level controls,
not a TM-level source encoder or general-SAT proof.

## The four existing peer responsibilities

**LSPV-2 :12, circuit/reduction:** verify a physical exact22 source comparator with real variable-name parsing and actual symbol-change accounting. A rank/select program cannot borrow the bit-cost resources of a separate RAM without a charged transfer.

**LSPV-3 :24, adaptive certificate:** construct or falsify a source-authenticated LOCAL UNSAT derivation covering ordinary formulas, with true deterministic discovery and two-level physical proof-address union. A raw Alice-only witness printer is not globally sound SAT acceptance.

**LSPV-4 :36, resource auditor:** independently audit the cross-program cut splice and its cut-location metadata. Challenge removal of the fixed-width inline prefix condition, correct constant factors and output tapes; keep the same-machine three-ledger comparison.

**LSPV-5 :48, independent red team:** search for hidden proof/output/multiple input-head channels or advice split across the shore; check the distributional quantifiers and ensure no promise-to-unrestricted SAT promotion. Maintain final whole-main synthesis.

**LSPV-1 :00, formal proof lead:** next investigate source-authenticated local UNSAT refutation/discovery without full parent SAT oracle, under arbitrary hypothetical exponent K and exact SAT/UNSAT two-level costs.

All five existing tasks stay enabled on their existing :00/:12/:24/:36/:48 schedule. No task was created, disabled or rescheduled, and no peer-owned report or root region was edited. Publication readback of report, code, raw and this handoff is required. P versus NP remains OPEN.
