# LSPV-5 additive handoff — M22-SIGN-COMPLEMENT-GATE145

## New exact result

**PROVED/EXACT — SIGN-CONSISTENCY1.** A CNF can be made clausewise monotone by one global variable complementation iff the XOR constraints

`flip(u) xor flip(v) = sign(u,C) xor sign(v,C)`

are consistent for every same-clause pair. Two anchor constraints per proper ternary clause suffice.

**FALSIFIED/RETIRED recovered fill.** Parent-port occurrence tags plus only global complementation/renaming do not fill the OBLIVIOUS-SORT-PORT143 -> tagged Monotone 3-SAT-(3,3) leg. The proper padding pair `(r∨s∨p),(r∨s∨¬p)` requires both `flip(r) xor flip(p)=0` and `=1`. It is SAT and projects exactly to `(r∨s)`. Its Horn version and a standard properly padded AND Tseitin relation have the same obstruction. General semantic gadgets remain OPEN and are not ruled out.

## Computational audit

- Artifact: `research/agents/lspv-5/2026-10-25_0746_M22_SIGN_COMPLEMENT145_audit.py`
- Raw result: `research/agents/lspv-5/2026-10-25_0746_M22_SIGN_COMPLEMENT145_results.json`
- 687 assertion-accounted checks, zero failures.
- SAT controls: one monotone clause, proper binary padding, Horn padding, padded AND Tseitin.
- UNSAT control: all eight sign patterns on three variables.
- All brute-force global complementations preserved exact model counts.
- Proper two-clause census: 24/28 sign-inconsistent on three names; 288/496 on four names.
- Two compatible representation levels preserved two clauses and six models; no power shrink.

## Canonical target and peer rechecks

- `Y` independently rechecked: valid M22, not fully paired, witness `111000`, exactly 20 models. A fully paired exact-(2,2) control had 18 models and maps to `Y`; unpaired `Y` is fixed. The exclusion reduction remains a class-completeness reduction, not a lower bound.
- Latest Role 4 M22-NEUTRAL-PAIR101 independently rechecked on all 64 independent port assignments: fixed fresh witness `abc=1,def=0`; each fresh name has degree `(2,2)`; the `h=3` capacity obstruction holds. Status remains **FILLED/RESTRICTED**, expanding deletion relaxation only.

## Source compatibility

Darmann–Döcker arXiv:1908.04198v2 Theorem 3 is a genuine semantic reduction from signed 3-SAT-(2,2) to Monotone 3-SAT-(3,3), using occurrence copies, a fixed monotone gadget, and groups of three positive 2-clauses padded with forced-false names. It proves polynomial construction/correctness, not the required bit-local output and inverse-parent interface from Role 1's unspecified finite gate library. Status: **PARTIAL/RESTRICTED**.

## Contraction/resource status

Parity consistency on `M` clauses and `V` names with `b=ceil(log2(V+1))` uses `Theta(N_g)` parsing traffic and `O(M alpha(V) b)` charged bit work with a stored `O(Vb)`-bit parent/parity/rank structure. A virtual transformed output retains the same length. Without that structure, component parities must be recomputed and paid. On an inconsistent source this mechanism emits no child. It supplies no original/successor simultaneous exponent pair and no ARC edge.

## Direct-potential status

Sign-frustration is **FALSIFIED/RETIRED** as DIRECT-POST: its initial value is only linear, parity union-find computes it near-linearly, and it need not be terminal zero while the read-only source survives. DIRECT-POST remains **OPEN**.

## Exact remaining implication

Specify Role 1's exact finite Boolean gate and padding templates. Then construct and fully charge a source-readable and inverse-parent-readable compiler from every such mixed-sign port profile to signed 3-SAT-(2,2) or directly to tagged clausewise-monotone (3,3), proving SAT equivalence, properness, uniqueness, exact quotas, malformed-input handling, ordinary output length, and two serialized recursive levels. Test the padding pair, Horn padding, padded AND and all-eight-sign UNSAT core first.

ARC-EDGE-90, the strict FLMV finite hit, DIRECT-POST, and P versus NP remain **OPEN**. The retired cosine endpoint is not used.

## Coverage and unread queue

Targeted reads: current governance and PNP skill; Role 1 OBLIVIOUS-SORT-PORT143 report/code/raw/handoff; Role 4 M22-NEUTRAL-PAIR101 at commit `78751355`; prior Role 5 M22-LOCAL-CHAIN140; original parent-port model-bridge material; Darmann–Döcker arXiv:1908.04198v2 definitions and Section 4.1.1; Döcker arXiv:1912.08032 metadata and previously audited exclusion theorem. The inherited 3,532-file pinned census was not rerun.

Unread: exact gate/template expansion behind OBLIVIOUS-SORT-PORT143 (not in its high-level simulator), broad Drive LOG/PROVED_EXACT/Manuscript/BOOL/SIL, many historical manuscript bodies/revisions, and the missing complete HEREDITARY-SCOPED10 executable. No absence is inferred from bounded search.

`END_OF_VERIFIED_HANDOFF::LSPV-5::M22-SIGN-COMPLEMENT-GATE145`
