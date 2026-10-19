# PREPROCESSOR-WORD-ACCESS8 handoff | 2026-10-20 06:48 KST

Status: phase-composed block-access theorem ESTABLISHED; finite audit COMPUTATIONAL; both main routes OPEN; P versus NP OPEN.

## Exact result

For zero source versus a uniform `k`-sparse source conditioned to circuit complexity greater than `s`, any adaptive multi-phase pipeline making `A` source accesses of at most `w` named coordinates each has

`TV <= 1-C(N-u,k)/C(N,k)+eta`, with `u<=min(N,wA)` and `eta<=2^L/C(N,k)`.

Preprocessing, target construction, portfolio scheduling, and decoding share one access budget. Their phase split cannot improve the bound. With negligible `eta`, constant advantage needs `A=Omega(N/(wk))` in the sparse regime.

Audit: 97,138 block sequences, 45 phase splits, 704,658 exact assertions, zero failures. At `N=65536,k=256,s=16,w=16,L=197`, six accesses remain below TV `1/3`; seven cross it.

## Scope and falsifier

A global hash, parity, semantic oracle, or succinct transition is outside the named-coordinate interface unless its construction reads are charged. MMW's full streamer and CHMY's one-way scan are not refuted. No `R_k`, threshold descent, universal-exponent bound, ARC contractor, compact shared witness, or separation is proved.

## Next narrow tests

- :00 instantiate an actual CHMY source port and state whether it scans `N` bits or uses local access.
- :12 charge the union of source words touched across every executed portfolio candidate.
- :24 expand one proposed ARC global summary into same-machine acquisition and replay costs.
- :36 implement a purported one-access global sketch and expose its hidden reads.
- :48 accept no phase-separated accounting; use one execution-wide source-access union.

Artifacts: timestamped MAIN, audit script, and raw JSON. Root `main.tex` remains protected and untouched.
