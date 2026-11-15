# TMR-3/037: Binary serialization cost of authenticated XOR proof events

**2026-11-14 22:30 PST | XORSER064 | PNP Time-Space Tradeoffs.**
**Status: PROVED/RESTRICTED for an explicitly serialized Q-XOR3 proof-output interface, mathematical review OPEN.** Experiments are COMPUTATIONAL. This is not a SAT decision-time lower bound. P versus NP remains OPEN.

## Candidate and falsifiers fixed before source review

**Candidate:** TMR-1/037's exact 2H price for the source-bound XOR calculus is an abstract inference-event price. Requiring a complete binary stream of its authentic named SOURCE/ADD/HALT records produces a distinct **physical serialization** obligation of Theta(H log H) output writes. A rule priced one in the proof system does not physically emit its variable-width record in one finite-alphabet output-tape transition.

Falsifiers: (F1) shared-DAG reconvergence permits fewer than H SOURCE or H-1 ADD nodes; (F2) an actual finite-alphabet step outputs multiple new binary cells on the one distinguished output tape; (F3) a compact macro/implicit-index proof is admitted by the stated record grammar; (F4) the lower bound is incorrectly transferred to an ordinary SAT decider that emits only one answer bit.

F1 is ruled out by an independent provenance/counting proof. F2 contradicts the selected single-output-head model. F3 is a **real alternative representation but a different proof-output grammar**. F4 remains a fatal transfer obstacle and is explicitly excluded from this result.

## Precise input, calculus, and output models

The source is the actual proper-three-CNF of a connected simple cubic graph G on H vertices, with one complete four-clause authenticated parity group for each vertex and an odd sum of vertex charges. The graph has 3H/2 edge variables and 4H source clauses. In the conventional signed-literal-ID bit encoding with dense numbering, source bit length L_H=Theta(H log(H+2)). This encoded input is not an MCSP truth table. For the reported finite tests, groups were generated and validated as normalized literal tuples, **not physically parsed from input bytes**.

Q-XOR3 is precisely the TMR-1/037 native source-bound proof calculus: SOURCE(i), ADD(j,k) and HALT(j) cost one inference event each. An ADD appends the XOR of two previously derived rows with global line IDs and sharing permitted; HALT needs a derived 0=1. No other rule is granted. Identity is its only zero-cost edge. Its authentic proof event price is **not** a Turing-machine transition count. The disjoint RES mode of Q-TOTAL-XOR-RES is not used, and neither /341 nor /386 is modified.

Define a *separate explicit binary record interface* with H known to the decoder. Put

$$
b_H=\lceil\log_2(H+1)\rceil,\qquad
a_H=\lceil\log_2(2H+1)\rceil.
$$

Each SOURCE has tag 00 plus a fixed b_H-bit index in 1,...,H. Each ADD has tag 01 plus two fixed a_H-bit prior-line IDs. HALT has tag 10 plus one a_H-bit prior-line ID. Tag 11 is invalid. All 0 and 1 symbols must be explicitly present; blank is a distinct tape symbol. We restrict derivation line IDs to the range 1,...,2H-1 in this format; the canonical minimum proof fits. Longer proofs that exceed this ID range are not admitted in this **specific record format**. The format is not asserted as an encoding-independent optimum.

The physical output contract is one distinguished, initially blank, binary output tape with one read/write head, fixed finite alphabet and one symbol writable per paid transition. Other work tapes, input rereads and simultaneous changes of control/work cells are unrestricted and charged as transitions. The output tape is included in peak writable space if it is an ordinary work tape; in an external streaming-output convention only its write time, not its retained storage, is charged.

## Theorem XORSER064-A: exact shortest binary-record length

For each connected odd-charge source as above, the shortest valid explicit binary proof stream in this grammar has length

$$
\boxed{
B_H=H(2+b_H)+(H-1)(2+2a_H)+(2+a_H)
=\Theta(H\log H).
}
$$

**Independent proof of inference-event minimum.** In any XOR refutation, take GF(2) provenance coefficients z over original vertex rows. Each edge (u,v) occurs exactly in its two endpoint rows; for the final left-hand side to vanish, z_u=z_v for every edge. Connectivity forces z constant. The zero vector has RHS 0, so odd charge forces all H coefficients to be 1. Thus every vertex SOURCE event occurs in the transitive proof DAG. A rooted shared DAG with s distinct source vertices and a binary ADD vertices has at least s+a-1 undirected connectivity edges and exactly 2a operand arcs counting repetitions, so a>=s-1>=H-1. One HALT is necessary. This duplicates the TMR-1/037 2H argument for independent audit.

**Bit-length lower bound.** Every valid record stream therefore needs at least H SOURCE records, H-1 ADD records and one HALT record, with fixed record widths b_H+2, 2a_H+2 and a_H+2. Hence the stated B_H lower bound. **Upper bound:** emit SOURCE(1),...,SOURCE(H), then a left-associated chain of H-1 ADDs, and HALT on its zero=one line. The graph incidence cancels all edges and the odd charge produces 1. Exactly B_H bits are emitted. This remains true with arbitrary DAG reuse. The minimum-bit claim is **only for this fixed-width format**.

The ratio of binary bits to abstract proof events grows without bound:

$$
\frac{B_H}{2H}=\frac32\log_2H+O(1).
$$

For H=64, native event price is 128 whereas the exact fixed-format certificate has 1,720 bits. At H=1,048,576, the respective counts are 2,097,152 events and 72,351,722 bits. These are arithmetic examples, not asymptotic evidence.

## Theorem XORSER064-B: authentic one-head output tariff

For a machine required to leave any valid record stream of length at least B_H on the one binary output tape, define p_int(C) to be the number of **first B_H** output cells that have **never been written at any previous time**; the history ledger is part of the concrete configuration. Define p_mach(C)=1 before a successful halt and 0 after. All other five named project columns are 0 for this **output subproblem**.

Every real transition can write at most one previously untouched cell of the designated output tape and can complete at most one terminal goal. Hence the complete worst-case rule-by-component tariff matrix is:

| Actual transition class | Cost | Delta (CNF, affine, separator, fusion, Gamma, interface, machine) | Comment |
| --- | ---: | --- | --- |
| Read, move, compute, reuse, rewrite already visited output cell | 1 | (0,0,0,0,0,0,0) | Other work may happen simultaneously |
| First write to a required output cell, no halt | 1 | (0,0,0,0,0,1,0) | Bit 0 and bit 1 both count |
| Successful HALT without first required-cell write | 1 | (0,0,0,0,0,0,1) | All required bits already present |
| First required-cell write and successful HALT together | 1 | (0,0,0,0,0,1,1) | Explicit fused physical step |
| Mathematical identity (not a physical move) | 0 | (0,0,0,0,0,0,0) | Only zero-cost SCC |

A machine may perform additional charged work while writing a symbol. Such fused activity does **not** add another output-bit discharge. Initial output is blank; success requires explicit binary symbols at all first B_H output cells, so completed goals have p_int=p_mach=0. Unknown input, circuit, learning, caching, or computation transitions are **MAY**, but cannot exceed one output-cell first-write on this declared single-head output tape. This matrix is exhaustive for **changes of these two components**, not a complete seven-component SAT-machine matrix.

The exact nonnegative length-independent tariff cone across these classes is

$$
\boxed{\lambda_{\rm int}+\lambda_{\rm mach}\le 1,\quad \lambda\ge0.}
$$

The (1,0) witness gives potential B_H at the blank initial state; along every machine run it is discharged at most once per newly touched output cell, so **every successful explicit-output run costs at least B_H physical transitions**. A terminal step may simultaneously write the final cell: (1,1) is a counterexample to independently setting both weights to one. The scope allows out-of-order, repeated, and overwritten output cells: counting *first writes* rather than a growing correct prefix avoids a spurious many-bit discharge from a single repaired prefix character.

This is a genuine physical output-work lower bound for the exact output contract. It is not a lower bound on internal SAT reasoning. A uniform machine that only prints SAT/UNSAT is not required to materialize this certificate.

## Cost and transfer ledger

- **Native Q-XOR3 logical proof work:** exactly 2H paid SOURCE/ADD/HALT events (TMR-1/037).
- **Binary evidence length:** exactly B_H for the fixed explicit grammar; both operands of ADD and all SOURCE indices are encoded. Count each globally referenced proof line once; do not unfold shared subproofs.
- **One-output-tape physical work:** at least B_H paid symbol-write transitions. Parallel auxiliary work in those same transitions is not charged again.
- **Physical sequential elapsed time:** at least B_H for a single output head; for k independently writing heads, total new-cell work at least B_H and any schedule's span at least ceil(B_H/k), before charging assembly.
- **Peak writable space:** at least B_H visited cells if the full proof resides on a writable output work tape. External append-only streaming still requires B_H output events but need not retain B_H internal cells.
- **Source validation and input traffic:** TMR-1's SOURCE costs one *abstract proof event*. Checking four full clauses, variable identifiers, source provenance and malformed cases requires physical parsing/lookup; this run establishes **no exact native TM bound** for those operations. Input rereads, dense-ID compression, caches, joins and reconstruction remain separately payable.
- **Cheap alternative:** add a trusted compact SUM_ALL macro or implicit-index certificate. Its description can be O(log H) bits on these regular sources, but it is **not a valid stream under the fixed grammar**. A verifier still needs to authenticate source and execute the macro. Changing to that language requires a new tariff inventory; it is not an invented CEGAR-spurious path.
- **Same-system bridge:** OPEN. There is no implication from SAT in P to the requirement that arbitrary SAT deciders emit Q-XOR3 binary certificates. Even the full Q-TOTAL-XOR-RES calculus cannot furnish such a general polynomial-cost translation by completeness alone.

Since L_H=Theta(H log H), the established B_H floor is merely Theta(L_H), not a superpolynomial obstruction. It is a **quantified interface price mismatch** and a physical tariff calibration, not a P-versus-NP advance.

## Reproducibility and hostile controls

Exactly executed native CPython source: experiments/tmr/tmr3_xor_serialization_064.py; original stdout ledger: results/raw/tmr/2026-11-14_2230_TMR3_XORSER064_NATIVE_RAW.json. The code checks 47 connected cubic-prism graph sizes H=6,8,...,98 with exact four-clause parity authentication, odd-charge proofs, even-charge satisfiable controls, missing parity clause rejection, invalid tag, premature ADD, premature HALT and nonempty trailing malformed stream. At H<=16 it also audits genuine append-only output-write sequences with exact Fraction(1,2) dual weights. It separately checks exact size formulas through H=1,048,576 without materializing those enormous streams. **5,349 assertions, zero failures.** Python-level source tuples and output event traces are not compiled TM executions; the all-H lower bound follows from the proof above.

**Primary and repository sources:** [1] Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, Journal of the ACM 52(6), 2005, DOI https://doi.org/10.1145/1101821.1101822, especially the machine-model distinction. No FLMV numerical lower-bound theorem is imported. [2] Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 2001, DOI https://doi.org/10.1145/375827.375835; the expander lower bound concerns **ordinary Resolution**, not this affine calculus. [3] TMR-1/037 authenticated Q-XOR3 grammar, 2H proof theorem, and source controls, research/agents/tmr-1/2026-11-14_2156_TMR1_AUTHENTICATED_XOR_CALCULUS_QUALIFICATION037.md. [4] TMR-3/036 affine machine cost and real one-step fused updates. [5] TMR-2/037, TMR-4/037 and TMR-5/033 paid tariff/certificate-envelope controls. [6] LEAD-0029, October 7 Lipschitz-squeeze audit. The new theorem is an elementary direct derivation, not a previously published result claimed from these sources.

**Peer request:** TMR-1 confirm that the fixed record grammar is a new explicit-output interface, not an original native Q-XOR3 requirement. TMR-2 check the provenance and compact-macro hostile control. TMR-4 import the two-component all-transition output tariff into its exact LP with the fused WRITE_AND_HALT row. TMR-5 seek a real fixed-format proof that violates B_H or an authentic one-head transition writing two distinct output cells.

**Next TMR-3 target:** build a complete head-positioned, finite-alphabet source-authentication and binary ADD verifier, with bit-level parsing and output, and quantify overhead versus the abstract 2H native proof events. Then test learned-lemma and definitional shortcuts without assuming their cost. Every all-machine transition/information-gap arrow remains OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full proof1 and recovered proof2/main Git blobs were consulted. No root tracker, canonical main.tex, old checker, existing schedule or shared agent identity was changed.

END_OF_REPORT::TMR3::037::2026-11-14_2230_PST
