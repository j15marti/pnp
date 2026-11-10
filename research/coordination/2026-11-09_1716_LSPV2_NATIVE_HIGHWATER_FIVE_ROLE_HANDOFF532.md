# LSPV-2/532 five-role handoff: exact FLMV native high-water and sparse-work difference

**November 9, 2026 17:16 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Verified result and ownership

LSPV-2's fully source-backed result is in [research report](../agents/lspv-2/2026-11-09_1716_LSPV2_NATIVE_HIGHWATER_ABSTRACTION532.md); independent JavaScript verifier is at ../../experiments/arc/lspv2_532_native_highwater_independent.cjs, and raw summary at ../../results/raw/arc/2026-11-09_1716_LSPV2_532_NATIVE_HIGHWATER_RAW.json.

The *literal* FLMV random-access Turing machine counts the farthest indexed work-tape position, which may be exponentially larger than time. For any total deterministic binary-language decider A, a fresh-tape prelude writes 1 followed by N zeros, indexes and reads work address 2^N, then runs A unchanged. Cost is N+3 extra native basic steps; same native machine's work-space high-water is at least 2^N, while the no-op prelude's actual distinct touched/index bits are O(N). All binary inputs including SAT/UNSAT/malformed preserve their original answer. This is a program-resource counterexample, **not inherent SAT space complexity**. Charged sparse-address simulation can eliminate the high-water at added lookup/conversion cost; no low-space SAT decider is constructed. The finding is consistent with FLMV 2005 Section 2.1, which explicitly notes exponential native space and sparse simulation. This is narrower than the user's universal contraction target.

Corrected independent replay charges *binary* source length, N=8 times each input's byte count. For a 53-byte K4 input, N=424 bits, prelude overhead is 427 steps, high-water 2^424, and sparse prelude bound 851 bits. Python and independent Node agreed on 133 finite original signed source controls: 3 SAT, 2 UNSAT, 128 malformed; N+3 index operations, exact 2^N high-water, and 13 original-source SHA-256 hashes. Published Node readback passed. Full report and raw summary verified by Git blob readback, and root main.tex LSPV-2-only section reconciled with all other bytes unchanged.

## Cross-role work suggested without changing primary allocation

**LSPV-1 lead (Route B):** carry the literal high-water/sparse-encoding distinction into the c-dependent FLMV feasibility envelope. A native S lower bound cannot be turned into an S upper.

**LSPV-2 builder (Route A):** attempt an actual all-input decoder-intensional bit/byte-access compiler that maps native far-head semantics to a charged compact representation and quantify the *complete* time plus simultaneous peak space, including guest cycles and hereditary recursion. Test circuit compactness and recomputation separately from workspace.

**LSPV-3 certificates (Route B):** retain exact machine state and branch source identity; proof DAG and machine memory differ. Resist existential witness-to-deterministic UNSAT transfer.

**LSPV-4 auditor (Route A, existing task disabled):** if resumed by separate authorization, inspect the indexed-tape high-water definition and sparse-machine overhead; **do not reactivate its schedule**.

**LSPV-5 red team (Route B):** challenge every compression under same-machine requirements, including model switching, abandoned high-space phases, huge c, unbounded index length, malformed source and hidden oracle.

Historical two Route A/three Route B scientific labels, five task IDs/titles/schedules/enabled states and R_mix341 weights remain unchanged.

## Tracker and remaining arrow

Material evidence node **[P2-L2-532]** added to proof2.txt, preceding bytes preserved, verified new Git blob **e3bbab3287d38fb872acfb29c064f32908d53996**. Proof1.txt reviewed without modification (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b). Root main.tex verified after authorized-only insertion at blob 39c5bdad6e821af08e656d5f40a904c77e3401ca.

The exact FLMV exponent-only k=2 bound stays $\beta(6/5)=23/45=1/2+1/90$, without an available upper $S\le N^{1/2+o(1)}$. Neither a hypothetical $A_P$ time bound nor $A_{NP}$'s nondeterministic verifier supplies this upper bound. **[P1-01], [P1-03], [P1-04], [P2-A2], [P2-D1], [P2-C3], [P2-B1], [P2-B2] are OPEN.** No P-versus-NP resolution follows.

**Readback correction:** The earliest finite result had treated bytes as N. Published verifier, raw ledger, report, and tracker node have been updated and re-read in full; symbolic binary-input theorem unchanged. The blob printed above is the corrected tracker blob.
