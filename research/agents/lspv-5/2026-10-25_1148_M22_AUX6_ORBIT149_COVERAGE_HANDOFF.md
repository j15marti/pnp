# M22-AUX6-ORBIT149 — Role-5 coverage and gap handoff

**Status:** COMPUTATIONAL finite exclusion; no formal infeasibility certificate. ARC-EDGE-90, DIRECT-POST, and P versus NP remain OPEN.

## Exact tested specification

- Three source ports, each with one already-used positive occurrence.
- Six private auxiliary variables.
- Proper unique all-positive/all-negative ternary gadget clauses.
- Gadget signed degrees `(1+,2-)` on each port and `(2+,2-)` on each auxiliary.
- Existential port projection required to equal exactly `{000,111}`.

The resulting block would contain exactly five positive and six negative clauses. The aggregate 180-binary-variable MILP is feasible for quotas alone and for quotas plus extension of both constants, but infeasible after imposing nonextension of all 384 auxiliary completions of the six nonconstant port words.

## Independent symmetry formulation

Fix witnesses `y0,y1 in {0,1}^6` for port words `000` and `111`. Simultaneous auxiliary renaming preserves feasibility, and the orbit is determined by the four counts `(n00,n01,n10,n11)`. There are `C(9,3)=84` weak compositions. All 84 fixed-witness 0/1 MILPs returned infeasible; none timed out or returned unknown.

This is exhaustive modulo the declared symmetry, but solver infeasibility is retained as COMPUTATIONAL rather than PROVED/EXACT because no independently checkable integer/Farkas certificate is published.

## Gap consequences

- **FALSIFIED/RETIRED computationally at this parameter:** `r=3,a=6`, uniform-sign, standalone private-auxiliary equality block.
- **OPEN:** `a>=9`; contextual/cross-variable balancing; shared clauses or auxiliaries; a different local semantic compiler.
- The failure does not imply compulsory SAT work. The 84-orbit search is an offline constant-size design audit and can be compiled into a finite lookup.
- A proposed potential counting unresolved template candidates has only constant initial range here and is representation-dependent; it cannot yield DIRECT-POST.

## Contraction/resource ledger

Had a fixed block existed, each source group would add six names and eleven ordinary clauses, hence linear encoded output. For `g` groups and index width `ell=ceil(log2(9g+2))`, it would write 33g variable-index fields plus clause/sign/header bits: `Theta(g ell)` output traffic. Validation, occurrence ranking, group/sign selection, address arithmetic, writes including unchanged bits, and source rereads remain charged. Streaming construction could use `O(log N)` local writable bits beyond the source accessor; materialization uses `Theta(g ell)` live bits. Neither version gives a power shrink. Because the block is infeasible before one semantic adapter level, no second recursive level exists and no ARC successor is claimed.

## Peer/source reconciliation

- Role 1 M22-NAE-PAIR149: exact local marginal law and sharp `1/3` correlation floor; no global SAT or decision-work implication.
- Role 2 ARC-STREAM-NORMALIZER150: exact source-order normalizer and a valid FLMV conditional firewall; the eager/replay tradeoff is not a favorable all-input edge.
- Role 5 AUX-PORT-CONGRUENCE148: exact necessary congruences; this run eliminates the first open congruence-allowed case.
- Döcker arXiv:1912.08032 remains the primary target-class source. Its NP-completeness theorem supplies no per-instance time lower bound.

## Next artifact

Either obtain a proof-producing SAT/MILP certificate for the `a=6` infeasibility, or formulate a cross-variable contextual block with public local output addresses and an explicit bit-cost ledger. Do not advance to `a=9` blind enumeration without symmetry or a structural lemma.

## Coverage status

Full text read this run: latest Role 1 and Role 2 substantive reports, predecessor AUX-PORT-CONGRUENCE148, `main13.tex`, and lead `FINAL-LINK-ARC`. Primary-source search: Döcker arXiv:1912.08032 and Darmann–Döcker arXiv:1908.04198 metadata/abstracts. Inherited 3,532-file keyword census was not rerun. Drive LOG/PROVED_EXACT/BOOL/SIL pagination and older historical revisions remain unread here; no absence claim is made.
