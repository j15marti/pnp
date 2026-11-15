# TMR-3/038: Authenticated parity macro and the physical input-ingress tariff

**2026-11-14 23:27 PST | MACROINGRESS067 | PNP Time-Space Tradeoffs**  
**Scientific status: PROVED/RESTRICTED (symbolic argument), independent mathematical and physical-machine review OPEN.** Finite V8 tests COMPUTATIONAL. **P versus NP OPEN.**

## Candidate and falsifiers fixed before prior-source review

**Candidate.** The binary named-record output floor of TMR-3/037 is a genuine lower bound for **that record grammar**, but is not an intrinsic cost of establishing an authenticated parity contradiction. Construct a sound one-symbol macro certificate with a fully charged, polynomial-time syntactic verifier for the same growing cubic Tseitin sources. Prove a separate native input-ingress bound for the *macro-language recognizer* using indistinguishable last-symbol pairs. Preserve a complete input/output/time/space/interface ledger.

Falsifiers preselected: (F1) an incomplete four-clause block is accepted as parity; (F2) a variable identifier of huge numerical magnitude triggers proportional storage; (F3) two sources with the same prefix but different final signs are treated as identical by the recognizer; (F4) the one-symbol macro is silently treated as a legal Q-XOR3 SOURCE/ADD/HALT record or as a universal SAT-machine lower-bound transfer.

## Models and exact source grammar

The source is an 8-bit ASCII string consisting of **proper three-distinct-variable clauses** separated by semicolons, each clause `id+ , id- , id+` without spaces, with positive canonical decimal variable identifiers and polarity suffixes `+` or `-`. Four consecutive clauses are one authenticated parity block. Each of its clauses must contain the same three distinct variable IDs, and their four falsifying Boolean triples must be exactly the four triples of one parity. Equivalently this block is the complete width-three CNF encoding of an equation `x XOR y XOR z = b`. Mixed triples, duplicate forbidden triples, incomplete groups, invalid IDs and all malformed syntax reject the certificate.

The verifier `V_MAC(F,1)` recognizes only the one-character proof token `1`. It accepts iff (i) all blocks authenticate, (ii) every variable ID occurs in an **even number of blocks** (not literal occurrences), and (iii) the XOR of the block charges is one. These are raw-source predicates. No source oracle, advice, Gaussian-elimination oracle or free derived-row transcript is given. Connectedness and exactly-two incidence are NOT needed for soundness. The verifier is not complete for all UNSAT formulas and is not a complete Cook-Reckhow proof system on all CNFs. It is a **source-bound sound certificate verifier**.

The explicit growing source family uses the prism graph `C_m square K_2`, m>=3, with H=2m vertices, 3m edge variables, H blocks / 4H clauses, one odd-charged vertex and all others even. Dense edge names give encoded source bits L_m=Theta(H log H). Every edge variable occurs in two blocks. No expander property is used or claimed.

Q-XOR3 from TMR-1/037 and its *mandatory named SOURCE/ADD/HALT record language* from TMR-3/037 remain untouched and distinct. The prior exact named binary-record length is
```
B_H = H(2+ceil(log2(H+1)))
    +(H-1)(2+2ceil(log2(2H+1)))
    +(2+ceil(log2(2H+1))).
```
It is Theta(H log H) **bits in its own mandatory output grammar**. The new macro has one ASCII certificate symbol, 8 bits, **in a different verifier and grammar**. Thus the output-evidence ratio is Theta(H log H); this is a genuine alternative representation, not a refutation of the qualified Q-XOR3 bitstream theorem.

## Theorem MACROINGRESS067-A: source soundness and compact evidence

For **every** source F in the specified raw syntax, `V_MAC(F,1)=accept` implies F is UNSAT. On each prism source F_m, the same accepted certificate is the single token `1`.

**Proof.** An authenticated four-clause block is logically equivalent to its unique parity equation. XOR all such equations. Every variable appears an even number of times, so the left side cancels to zero. The right side is one, yielding 0=1. Thus no assignment satisfies all the original clauses. In each charged odd prism every edge occurs twice and the vertex-charge sum is one, so the verifier accepts. Nothing in the proof assumes graph connectivity or a specific Resolution refutation. QED.

The verifier can be compiled to **one fixed finite-control finite-alphabet deterministic multitape machine** with a left-initialized read-only input head and initially blank ordinary work tapes. A conservative resource bound is `O((L+1)^6)` transitions, `O((L+1)^2)` writable cells, and one constant certificate token. A concrete implementation is: copy/validate the byte source by local head scans; make at most O(L) variable-ID occurrence records, each a bit string of length at most L; authenticate four-pattern groups by repeated pairwise bitstring comparisons; for each occurrence rescan all occurrence records to compute the parity of matching variable names; XOR the block charges and decide. There are O(L^2) record comparisons, and each comparison and repositioning needs at most O(L^2) finite-alphabet head moves using the O(L^2)-cell copy. All navigation, memory, dense reindexing and source authentication are charged. The bound is deliberately coarse. The published JS uses native Maps for semantic validation; **it is not a physical-TM execution trace or a compilation certificate**. The physical upper bound rests on the explicit repeated-scan construction, not on Map constant-time access.

## Theorem MACROINGRESS067-B: authentic input-ingress floor (restricted language)

Let M be any fixed, correct, deterministic, locally moving **single-read-only-input-head macro-language recognizer** which accepts all strings accepted by V_MAC and rejects the strings it rejects, with input head starting at byte index zero. On each F_m above, M must read its final polarity byte, hence needs at least `|F_m|_bytes` input-reading/transport transitions (up to the initial indexing convention).

**Proof.** Flip only the very last polarity suffix `+` to `-`, or conversely. The altered string F'_m has identical preceding bytes, is still a syntactically proper 3-CNF, but its final parity block no longer contains all four distinct falsifying patterns of one parity. Therefore V_MAC accepts F_m and rejects F'_m. Until the first actual read of the last byte, deterministic executions have identical configurations and answers on this pair. Correctness on both requires such a read. A head initially at the first byte and moving at most one cell per transition needs Omega(|F_m|_bytes) transitions. This is a restricted recognizer-language bound, **not** a pair of SAT/UNSAT formulas, and does not transfer to arbitrary SAT deciders. QED.

Let r(C) be the largest input-byte index actually read on the run, initially -1, and B=|F_m|_bytes. Define `p_ing(C)=max(0,B-1-r(C))`. Every authentic physical transition has `Delta p_ing <=1`, every accepted correct macro-recognizer path has terminal `p_ing=0`, and initially `p_ing=B`. Hence the exact one-component tariff certificate `lambda_ing=1` gives `W>=B=Theta(L)`. This is **dynamic**, one-head, same-execution, and length-aware. The certified time scale is only linear.

## Transition-cost, fusion and output ledger

The seven standard columns in order are `(p_CNF,p_aff,p_sep,p_fus,p_Gamma,p_interface,p_machine)`. In this **physical input-ingress slice** set all but `p_interface=p_ing` to zero. An actual transition reading a new rightmost source byte has discharge at most one and costs one. A reread, left motion, cache update, internal reduction, label write, branch, buffer operation or other legal transition has discharge zero unless that same transition also reads the next previously unread input byte. Every physical transition costs one; there is no authentic zero-cost physical transition and the zero SCC quotient is identity. The singleton vector `lambda=(0,0,0,0,0,1,0)` passes every physical transition in this qualification. If a different candidate combines unfinished output and terminal flags, physically legal fused READ/WRITE/HALT instructions mean independent unit weights cannot be imported without its **full** joint-row analysis. Other abstract component charges are zero/MAY, not secretly assumed illegal.

| Operation | Work/elapsed/space/evidence | Max source-ingress discharge | Status |
| :-- | :-- | --: | :-- |
| READ_NEXT new high-water byte | one actual transition; no forced extra work tape allocation | 1 | PROVED/RESTRICTED |
| READ_AGAIN, LEFT, BUFFER, XOR, compare | one actual transition; retention, head motion and recompute counted | 0 | PROVED/RESTRICTED |
| WRITE_OUTPUT, HALT, or their fused execution | one transition, possibly one first output cell and final halt simultaneously | 0 | PROVED/RESTRICTED |
| READ_NEXT simultaneously with output/write/control update | one transition, cannot independently charge per action | 1 | PROVED/RESTRICTED |
| Arbitrary new non-affine SAT abstraction operation | no claimed separate charge | MAY | OPEN |

The LP/matrix constraints are `lambda_interface <=1` on the original seven-column slice, with all other weights zero. This is a bona fide same-machine one-component lower bound on the **macro verifier recognition task**, not a nontrivial all-seven-component SAT potential. Output-certificate length is 8 bits; named-record evidence bits are B_H. Work is O(L^6) upper / Omega(L) ingress lower; sequential elapsed time equals work for this sequential machine; parallel span and multi-machine port simulations have not been constructed; peak writable space O(L^2). Proof sharing and cached row identities require no per-use payments. Giant IDs are treated as strings, never as exponentially large array indices. There is no compulsory production of the Q-XOR3 record stream in Q-MACRO.

## Tests and hostile controls

The exactly executed native V8 function was captured in `experiments/tmr/tmr3_macro_ingress067.js`. It produced **348 assertions, zero failures**, 33 last-byte distinguishing pairs, 4 small full truth-assignment SAT checks, 33 valid odd prism sources and 73 negative control classes. Controls include even-charge satisfiable prisms, incomplete and duplicate parity blocks, a changed last sign, wrong block triples, repeated variables, canonical-ID parsing, huge sparse variable-ID bitstrings, two contradictory parity rows, disconnected components, Horn-like/all-positive and non-four-clause grammar rejects. The computed finite samples are in the raw JSON. Tests are semantic JS-level, not physical finite-state replays. No randomness used.

**New relative to prior project work:** TMR-3/037 already warned that compact macros change grammar and invalidate any transfer of the mandatory record output length. Here we supply an exact all-input **sound macro source verifier**, full raw-input parsing checks, a polynomial charged finite-alphabet compilation argument, and a separate last-byte physical ingress potential with a syntactic single-byte adversary. TMR-1/037 already supplied Q-XOR3 price 2H; TMR-5/034 supplied a generalized 2s formula. Neither is replaced or strengthened. TMR-4/038 supplied source ancestry tariffs for those **separate** inference-priced systems. This report adds an explicit *legal alternate verifier* and the physical input-access floor, not a generalized SAT lower bound.

## Provenance, primary literature and dependency ledger

Governing refocus SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; Nov 13 replacement SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Both trackers, authentic full proof2 Git blob and full root main.tex Git blob, AGENTS.md, CODEX.md, repository skill, all five current handoffs and issue #3 inspected before publication. Original TMR-1/037, TMR-3/037, TMR-4/038, TMR-2/038, LEAD-0029 original reports inspected; earlier /341 **FAIL** as a full logical checker and /386 **RESTRICTED** preserved.

Primary literature (scope only; present macro lemmas are independently proved here):
[1] Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1), 1979, pp.36-50, https://doi.org/10.2307/2273702 . Proof systems require sound polynomial verification; our incomplete source-bound macro is not a complete all-CNF proof system.
[2] Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 2001, pp.149-169, https://doi.org/10.1145/375827.375835 . Exponential lower bounds concern ordinary Resolution, not macros with parity authentication.
[3] Laitinen, Junttila and Niemela, *Conflict-Driven XOR-Clause Learning*, SAT 2012 and arXiv:1407.6571 (extended version), https://arxiv.org/abs/1407.6571 . XOR/GF(2) processing is an established compact alternative.

**Dependency status:** Q-XOR3 2H price PASS/RESTRICTED; compulsory named output B_H PASS/RESTRICTED; alternative macro one-token soundness PROVED/RESTRICTED, peer OPEN; macro-language ingress floor PROVED/RESTRICTED, peer OPEN; ordinary SAT decider transfer OPEN; superpolynomial fusion-safe initial potential OPEN; historical /341 FAIL, /386 RESTRICTED. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root main.tex change, schedules untouched. P versus NP OPEN.

**Peer requests:** TMR-1 audit exact source parser and whether macro authority should be qualified as an incomplete source-bound checker; TMR-2 audit the last-byte witness and high-ID nonuniformity traps; TMR-4 import the one-column physical ingress row and distinguish Q-MACRO from Q-XOR3 closure; TMR-5 independently search for a shorter *actual* accepted source with no syntactic 4-block cost or a flaw in universal soundness. **Next TMR-3 target:** physically compile a head-positioned source verifier into explicit transition-level costs, then test whether any non-affine multiscale component retains a positive weight alongside this length-linear ingress tariff.
