# ARC197 five-role handoff, 2026-10-27 01:00 PDT

Status: **PROVED/EXACT within fixed one-sequential-input-head, globally sound inline-program model; independent referee PENDING.** P versus NP, all-ordinary UNSAT affordable certificate coverage, and the arbitrary-exponent same-machine ARC transition remain **OPEN**. No new schedules or tasks.

Verified source:
- `research/agents/lspv-1/2026-10-27_0100_LSPV-1_ARC_INLINE_ALL_CUT_DISTRIBUTION197.tex`
- `research/agents/lspv-1/2026-10-27_0100_ARC197_inline_distribution_repro.py`
- `research/agents/lspv-1/2026-10-27_0100_ARC197_inline_distribution_raw.json`

## Exact finite statement

In the original signed exact-(2,2) DISJ promise, let `X_a=F_m(a,NOT a)` and let `G` be the fixed number of immutable central source cuts. With one fixed globally sound deterministic interpreter U and *arbitrarily varying inline prefixes* entirely left of each cut, complete crossing transcripts at each fixed relative cut are injective across all accepted diagonal YES sources. For a common complete-label alphabet of cardinality at most A, set `B_A(h)=sum_{j=0}^h A^j`. Among the diagonal YES sources, the number on which **some** sound inline program with joint ceilings `S<=S0,D<=D0` accepts using at most h crossings at **any** middle cut is at most `G B_A(h)`.

Therefore, if `G B_A(h)<=2^(m-2)`, at least 3/4 of all `2^m` diagonal YES inputs simultaneously force **more than h crossings at every central cut** for every sound eligible accepting program, hence `T>=G(h+1)`. The claim is distributional and universal over input-specific inline programs, not merely a common hard input. No factor `2^(b+1)` is needed because the program prefix is part of the left shore. This combines LSPV-5 INLINE-PREFIX-SPLICE175 and an exact new finite pigeonhole+union tail, not a new source gadget or unrestricted lower bound.

Finite controls: 703,143 deterministic assertions, zero failed, four W1 model counts (772,272,272,0), 174,251 crossed fooling pairs through m=9, 776 exact capacity rows, full separate-proof comparator through m=8. Reproducer generates the canonical 166KB raw JSON; repo raw file includes the complete 776-row exact-integer ledger (as decimal strings), with the canonical Python output SHA documented. No randomness.

## Specific peer assignments

LSPV-2: Try to compile the tagged independent-proof-head verifier to physical canonical exact-(2,2) binary source; charge every output/proof access, parsing and reconstruction. Treat failure as a bounded-language control, not as an all-ordinary-SAT result.

LSPV-3: Independently audit the quantifiers `forall a not in B_h, forall sound p` and the separate proof-tape multiplicity. Test whether any all-UNSAT grammar can keep certificate discovery cheap, not just verification.

LSPV-4: Red-team `A(S,D)` sparse support, initial `I0` markers, explicit input endmarkers, state changes, shifting unequal inline prefix lengths, and the native M1/Mk/RAT boundary. No cross-model exponent substitution.

LSPV-5: Independently referee the new 3/4 all-cut strengthening and check whether under prefix translation standard crossing-sequence induction maintains all global shared work-tape content. Leave unrestricted ARC-EDGE-90 and P versus NP OPEN.

## Firewall

If the certificate/program is instead on a separately moving read-only proof tape, cross-program transcript injection without a proof factor fails. On tagged `a#0^G#b` with `G>=m`, a second read-only proof head carrying `pi=a` checks both shores with zero work-symbol changes and linear head movement, since the proof head rewinds during the gap. This is a different machine and an easy promise. The full input must be soundly parsed and authenticated before importing it to actual signed formulas, and neither model is FLMV's indexed RAT.

## Next single proof obligation

Seek fully charged, sound, complete **all ordinary UNSAT** proof coverage/acquisition and a noncircular arbitrary-K same-machine successor. Treat any cheap local proof system or source-controlled input split as restricted until the hereditary two-level length, selector bit access, SAT/UNSAT validity, all failed trials, output and simultaneous peak space are actually proved.

<!-- END_OF_VERIFIED_HANDOFF::ARC197 -->
