# TMR-4/039 | MODEJOIN067: Typed zero-cost proof-mode choice and exact event/output fusion

**2026-11-14 23:44 PST, America/Los_Angeles.** Role: PNP Cost-Sound Abstraction (TMR-4). **PROVED/RESTRICTED** for the specified finite authenticated two-transcript replay protocol; independently reviewed mathematics OPEN. Executed tests **COMPUTATIONAL**. **P versus NP OPEN.**

## Candidate and precommitted falsifiers

Candidate: A zero-cost choice between an authenticated XOR refutation and an authenticated ordinary-Resolution refutation of the *same original CNF* must be incorporated into directed zero-cost closure. Atomic proof-event issuance may share one cost with emitting its own first record bit in a deliberately qualified replay authority, so native event price and serialized-output price cannot automatically be summed. We inspect a precise model, not infer an arbitrary physical TM's transitions from this event proxy.

Falsifiers: (1) purported XOR source row is not authenticated by all four 3-CNF clauses, or final 0=1 does not follow; (2) purported RES trace uses non-source leaves, invalid pivots, or incomplete AND ancestry; (3) a zero-price mode edge lowers a proposed RES-only potential, or a paid EVENT_WRITE discharges two independently fully priced coordinates; (4) an atomic inference event is incorrectly treated as one physical multitape transition, or a preloaded proof script is mistaken for a deterministic all-input SAT decision algorithm. These are checked or explicitly retained as blockers below.

## Concrete state, authenticated source and goal

For even H=4,6,8,10, use K4 when H=4 and the 3-regular prism graph with H vertices otherwise, with one charge-1 vertex and other charge-0 vertices. Each vertex degree-three parity equation is authenticated by *exactly four* signed proper 3-CNF clauses. This yields 4H actual clauses over 3H/2 edge variables. The source formula is UNSAT because XORing all vertex equations yields 0=1. Original encoded input length is $L_H=\Theta(H\log(H+2))$ with dense variable IDs, distinct from proof event count and record bits. The code checks all eight local assignments for each of the H parity blocks.

Two **actual proof scripts** are constructed and checked against this same source: native SOURCE/ADD/HALT XOR shared DAG; and a native CNF-source/binary-Resolution/HALT DAG obtained by variable elimination. Every RES node's signed pivot and resolvent are checked, and all imported leaves are authenticated source clauses; no cross-mode cast is invented. The shortest-derivation claim is **only for the fixed scripts**. The large RES traces produced here are not asserted to be minimum Resolution proofs or asymptotic Resolution lower bounds.

The **qualified protocol** consists of a single entry state with two zero-cost CHOOSE edges to typed XOR or RES replay. Once chosen, its exact finite verified script is fixed. A state contains authenticated input and proof script, type tag, next event index, current record-bit position, all completed event IDs, emitted bitstring, paid history and halted flag. A record is binary with explicit opcode and finite-width source/parent/pivot identifiers. Legal paid rules: EVENT-only (issues next authenticated event), WRITE one next record bit after its event is issued, and EVENT_WRITE one atomic event jointly with the first bit of *that event's* record. The mixed operation is deliberately a primitive **of this transcript-replay authority**, not a physical SAT Turing-machine transition. Terminal goal requires every script event legally issued, every record bit physically emitted in the declared protocol, and verified 0=1 HALT. Unknown alternative scripts or general solver moves are MAY and are not excluded from larger authorities.

This finite system is source-complete **only for the two selected refutation transcripts**. It is not complete for all UNSAT CNFs, not the full Q-TOTAL-XOR-RES proof calculus, and not a machine SAT decider. The proposed proof/LP lower bound is strictly scoped accordingly.

## New theorem MODEJOIN067-A (exact directed closure and tariffs)

Let script type t have $E_t$ valid atomic events and records of lengths $b_{t,j}\ge1$, with $B_t=\sum_jb_{t,j}$. In the explicitly described replay authority, the exact minimum charge to emit all records and complete the script is

$$
\boxed{W_t=B_t,\quad W_{\rm entry}=\min(B_X,B_R).}
$$

**Proof.** Each paid transition emits at most one previously missing required record bit, so at least $B_t$ paid transitions are necessary. For each event, EVENT_WRITE executes the event and writes its first bit in one charge, followed by $b_{t,j}-1$ WRITE operations. The complete authenticated trace costs exactly $B_t$. The zero-cost CHOOSE edges make the entry optimum the minimum of the two genuine complete branches. Directed closure, not merely SCC contraction, is necessary: entry and the two mode states are separate zero-cost SCCs but the directed entry closure reaches both.

At a typed replay state, use the exact reduced-product components $p_{\mathrm{machine}}=\#\text{remaining script events}$ and $p_{\mathrm{int}}=\#\text{remaining required record bits}$, with the other five project components explicitly zero **only in this restricted authority**. With $\lambda\ge0$, the row matrix is:

| Rule | Cost | $\Delta p_{\mathrm{machine}}$ | $\Delta p_{\mathrm{int}}$ |
| --- | ---: | ---: | ---: |
| EVENT | 1 | 1 | 0 |
| WRITE | 1 | 0 | 1 |
| EVENT_WRITE | 1 | 1 | 1 |
| zero identity / completed goal | 0 | 0 | 0 |

The precise nonnegative cone is $\lambda_{\rm machine}+\lambda_{\rm int}\le1$: EVENT_WRITE gives necessity and the other rows give sufficiency. The rational vertex $\lambda=(0,1)$ verifies every paid row and makes typed potential equal remaining output bits; at the entry define $\Phi(e)=\min(B_X,B_R)$. On each zero-cost CHOOSE edge, $\Phi(e)\le\Phi(\mathrm{chosen})$, and completed goals have $\Phi=0$. This establishes the full all-step lower-bound telescope on **this finite graph** and returns the exact optimum above. Weighted sums with $(1,1)$ FAIL at every genuine EVENT_WRITE step since discharge 2 exceeds cost 1. A RES-only source potential of $B_R$ FAILS on the zero-cost entry-to-XOR choice whenever $B_R>B_X$. Neither genuine shortcut is removable by CEGAR.

**Uniform script-interface warning.** A finite REPLAY program must already possess the selected proof script; giving it for free changes the input/service contract. The theorem prices replay, not construction, verification, source parsing, or discovery of a proof. In a fixed physical TM, producing any event may take many transitions and writing a bit can overlap actual computing, but a native logical proof event is not presumed one physical step. Conversely no arbitrary SAT algorithm is required to emit this certificate. The all-machine transfer remains OPEN.

## Finite independent source/proof and tariff results

| H | Original clauses | XOR events | XOR bits | generated RES events | RES bits | exact two-script optimum |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 16 | 8 | 56 | 48 | 647 | 56 |
| 6 | 24 | 12 | 86 | 104 | 1757 | 86 |
| 8 | 32 | 16 | 139 | 232 | 4644 | 139 |
| 10 | 40 | 20 | 175 | 480 | 10867 | 175 |

The RES counts are for **one constructed elimination derivation**, not lower bounds on the shortest RES proof. All XOR programs implement a connected-source DAG with exactly $2H$ native events and the previously established XORSER064 record length $B_H$. The explicit counterexample at H=4 has a genuine zero-cost choice from 647 RES record bits to a 56-bit XOR record and a legal EVENT_WRITE of $\Delta=(1,1)$ for cost one. The separate EVENT-then-WRITE schedule uses $E_X+B_X=64$ steps, while fusion yields exactly 56 in the declared replay authority. This is an interface/fusion calibration, not a computational lower bound on SAT beyond the stipulated replay task.

Native V8 source was executed in this run with **27,147 assertions**, **18,379 checked replay or zero-mode edges**, zero failures. The exact-rational nonnegative LP constraint was verified with integer numerators on a denominator-20 grid; the complete cone and vertex optimum follow from the symbolic row proof, not finite enumeration. The published source is serialized from the exactly executed function; the standalone Node wrapper is unexecuted in this run and must not be described as independently replayed byte-for-byte. Raw JSON is from the same execution.

## Dependency and peer handoff

- **PASS/RESTRICTED:** complete signed four-clause local source truth tables, checked GF(2) contradictory XOR derivation, checked native Resolution source and inference DAG, exact two-script zero-choice Bellman value, and EVENT_WRITE tariff cone. This is new to TMR-4 relative to /038's XOR-only tariff: an explicit **same-source typed alternative** with authenticated competing native proof traces and a costed product with written records.
- **FAIL:** RES-only bound transported across the free typed-mode choice; independent full prices for one atomic proof event and one simultaneously emitted bit.
- **OPEN:** arbitrary-script completeness, proof discovery/physical serialization compilation, full seven-column machine-state abstraction, superpolynomial fusion-safe family potential, same-system uniform all-input SAT-machine transfer. Historical /341 remains FAIL as a full UNSAT logical authority; /386 remains RESTRICTED.

**Next TMR-4 target:** replace the preloaded scripts with a genuine program/control state for a small fixed deterministic proof constructor and prove a per-instruction simulation to this typed authority, including input/definition access and simultaneous output costs. **Peer requests:** TMR-1 audit both same-source proof grammars; TMR-3 audit physical multi-tape EVENT_WRITE nontransfer and binary output; TMR-5 independently replay the resolution pivot ledger and seek a shorter valid alternate mode, which must remain in any larger qualified authority. TMR-2 audit whether semantic cofactor/interface obstruction survives a free XOR/RES selection and certified autarky.

Sources reviewed: Cousot and Cousot, *Abstract Interpretation*, POPL 1977, pp.238-252, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml (methodology only); Krajicek, *Interpolation theorems, lower bounds for proof systems, and independence results for bounded arithmetic*, Journal of Symbolic Logic 62(2), 1997, https://doi.org/10.2307/2275540 (feasible-interpolation context, not an imported bound); TMR-1/037 and /038, TMR-2/038, TMR-3/037, TMR-4/035-038, TMR-5/034, LEAD-0029; full governing directive and original counterexamples reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and main.tex not changed. Five existing schedules untouched. P versus NP remains OPEN.

END_OF_REPORT::TMR4::039::2026-11-14_2344_PST
