# TMR-5/015: physical-head replay, source-read ledger falsifier and tight scoped fetch bound

**Pacific timestamp:** November 14, 2026, 03:53 PST (America/Los_Angeles). **Role:** TMR-5 independent redteam and synthesis. **Status:** PROVED/RESTRICTED for a corrected physically charged symbol-fetch construction at the stated interface; CANDIDATE/RESTRICTED pending independent TMR-1/TMR-3 review of new tightness and full generic compiler; finite evidence COMPUTATIONAL. Unrestricted P versus NP OPEN.

## Exact peer claim and independently identified defect

Audited ORIGINAL TMR-3/016 report, executable and raw data:

- [Peer report](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-3/2026-11-14_0334_TMR3_AMORTIZED_POPCOUNT_ONEHEAD_BRIDGE016.md)
- [Peer JavaScript](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr3_amortized_countdown_bridge016.cjs)
- [Peer raw evidence](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0333_TMR3_AMORTIZED_COUNTDOWN016_RAW.json)

Peer AP16 claims a fixed charged single-read-only-input-head simulator for every fixed finite total uniform $h$-input-head multitape machine $A$, all lengths and both SAT/UNSAT plus malformed labels, with

$$
T_{B_A}(x)\le c_A(L+2)(T_A(x)+1),\qquad
S_{B_A}(x)\le S_A(x)+c_A\lceil\log_2(L+2)\rceil.
$$

**The peer program is not a physical current-cell source-read trace as described.** In its published lookup, the statement charging the input head's return to zero comes BEFORE the expression obtaining source[x,p] by direct array indexing. The variable head remains at its old numeric p and is never decremented when the return is charged. Therefore 49,833 successful lookups verify arithmetic and returned symbols, not an actual local input-head read after the return. Smallest hostile witness: length-one source x=1, target p=1. After the charged physical return the read-only head is at the LEFT marker (cell zero), which must return LEFT, while the peer indexed expression returns 1. This is an off-head-read flaw in the executed certificate, not a falsification of the correctly ordered abstract construction in the report.

**Minimal repair:** When the physical head reaches p, first execute a legal read of the CURRENT cell into finite control, THEN move the input head p times left while charging the return. The finite symbol alphabet makes caching that one symbol a constant-control operation. This preserves $O(L)$ fetch time, $O(\log L)$ additional visited work cells and both terminal-label possibilities. Neither the peer raw arithmetic evidence nor real shortcut executions are deleted; only its physical-read interpretation is downgraded.

## Independent charged construction and proof

Let L be the number of immutable encoded input bits, with endmarkers at 0 and q=L+1, input head initially at 0, an explicit binary target 0<=p<=q in $w=\max(1,\lceil\log_2(L+2)\rceil)$ work cells, and no prior cached source data. Use a charged little-endian countdown and a separate ordinary unary work-tape head at position equal to its population count. Initialize both with $O(w)$ local tape work. For a positive countdown j with t trailing zero bits, decrement by flipping t zeros and the first one, returning the binary head to its low cell, and moving the unary head t places right then one left. Every step is a local movement/write; the unary head is then at popcount(j-1). A left-marker test on that head detects zero in constant time.

Advance the physical input head one cell each decrement. After exactly p decrements it stands at source cell p. **Read and cache source[p] now**, then return to the left marker in p charged physical moves. The elementary identity

$$
\sum_{j=1}^p \nu_2(j)=\sum_{r\ge1}\lfloor p/2^r\rfloor\le p
$$

bounds all binary and unary work-head movements in the countdown by O(p), including head restoration and zero tests. Total fetch time is $O(p+w)$, additional writable footprint $O(w)$. This does not grant direct random access: all bit reads are from the actual current input-head location. Fixed $h$ original virtual source heads can be stored as $h$ binary addresses; every source fetch of each source symbol, virtual address update, original work-tape transition and preliminary length measure is charged. A compatible physical generic compiler then gives the peer $O_A((L+2)(T_A+1))$ bound. The generic arbitrary-$A$ instruction-table compiler was NOT executed, so its comprehensive status remains CANDIDATE.

### New independently proved interface lower bound (restricted)

For any correct deterministic source-bit fetch procedure starting with ONE locally moving input head at position zero, identical control and work storage for all equal-length inputs, and demanded to return x[p] for arbitrary data cell 1<=p<=L, take x=0^L and y differing only at p. Both complete computations are identical until they read position p, since every earlier observed cell matches. Different correct outputs require that read. Therefore there must be at least p charged rightward input-head moves; if the interface also requires restoring the left-marker position, at least 2p physical input-head moves. This remains true even with arbitrary writable workspace, provided the initial work state does not already contain input-dependent information. Hence the repaired O(L) fetch is asymptotically tight for p=Theta(L) on the stated **uncached reset-port** interface. This is NOT an SAT time lower bound: a semantic solver can cache bits, scan differently, abandon the emulated port or use algebraic processing.

## Independent native execution and precise limitations

The separately authored [native CPython source](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr5_physical_fetch_audit015.py) was run directly on the operating-system Python interpreter. This is neither an import-wrapper for peer JavaScript nor a synthetic proof claim. Physical input, binary countdown and unary population-count head positions are stored independently. All input-head moves, work-tape movements, binary reads/writes and zero tests increment the paid ledger. Source data are read ONLY through a method using the current physical input-head location, and always before paid head restoration.

| Native COMPUTATIONAL measurement | Value |
|---|---:|
| Complete source lookups | 49,392 |
| Charged local micro-operations | 3,711,877 |
| Genuine source-head displacements | 590,406 |
| Charged binary bit flips | 509,009 |
| Opposite-source adversary pairs | 24 |
| Assertion failures | 0 |

Inputs: EVERY binary string of length 0..11 with every valid position; independent seeded long controls at lengths 15, 24, 25, 31, 32, 63, 64, 127, 128, 255, 256, 511, 512, 1023 and 1024; endmarkers and late cells. Opposite-label-bit controls at nine lengths. This is **NOT** execution of a complete arbitrary 3-SAT machine. Peer JS was read and audited, not rerun natively. The native raw JSON was published at [TMR5 raw](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0351_TMR5_PHYSICAL_FETCH_AUDIT015_RAW.json); source SHA-256 d92826741ba3eba15c3e5808d3bfe14707a8ad17a58886b7d1a4f6b4a4cd6fd5; raw SHA-256 5eb0b6d0af032b4509b4cb5dfe9fd8f1be9e66edacdeaf4a51a36a0fd15277d6.

**Hostile controls and implications:** Genuine SAT/UNSAT sign streams, Horn, 2-SAT, GF(2)/Gaussian elimination, Tseitin, bounded-treewidth dynamic programming, products, sharing, auxiliary variables, padding, renaming and cache/recompute all remain legal alternate algorithms. The proved source-port interface does not mandate their solver use. TMR-2/017 disjoint block certificates remain restricted read necessities; TMR-1/017 control congruence and TMR-4/018 work-symbol congruence are sufficient local cost-exact abstractions, not source-decider cost lower bounds. New TMR-4/018 is still pending independent role review. Historical LSPV-5/523 accepted literal-order aliases are genuine physical-checker behaviors and cannot be erased as spurious.

## Integrated dependency and proof status

The strongest surviving scoped dependency is a physically correct current-cell input fetch with $O(p+\log L)$ time and $O(\log L)$ scratch, plus an independently established $\Omega(p)$ bound for uncached locally moving reset-port queries. This supports a model translation **upper bound** but cannot prove a universal compulsory post-read SAT computational bottleneck. For TMR-4, all-step abstract cost simulation and a Bellman-valid potential give a conditional lower bound, but no independently derived superpolynomial potential at the initial states of arbitrary correct uniform SAT machines. The required all-exponent implication remains OPEN:

$$
\forall A\ \forall k\ge1\ \forall C>0\ \forall L_0\
\exists F:\ |F|\ge L_0,\quad T_A(F)>C(|F|+1)^k.
$$

Neither P=NP nor P!=NP is proved. All mathematical status changes are limited to the restricted physical fetch audit; no tracker proof-chain node is promoted.

**Corpus:** the user-superseding 2026-11-13 12:49 PST TMR replacement directive first and rechecked (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4); complete proof1.txt 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; complete proof2.txt 1,051,196 chars recovered via authenticated Git blob 930c5eeddafce656717f28055a7a9a755f44737c despite blank contents API; complete main.tex 2,528,412 chars recovered via authenticated Git blob 31f68fe0fc5dcfb4f7947fb2dacd7d285074e2f5; issue #3, AGENTS.md, CODEX.md, repository research skill, all newest role handoffs, original TMR-3/016 code/raw, TMR-1/017, TMR-2/017, TMR-4/017 and /018, historical LSPV-5/523. No local full repository preflight or LaTeX build was executed. TRACKERS REVIEWED; NO MATERIAL CHANGE; canonical main.tex is the only authorized shared manuscript. No scheduled tasks were changed.

**Primary literature, exact scope checked:** [1] Fortnow, Lipton, van Melkebeek, Viglas (2005), JACM 52(6):835-865, https://doi.org/10.1145/1101821.1101822 . Their time-space exclusion applies to stated random-access SAT time exponents with correspondingly small space, not arbitrary polynomial workspace. [2] Paige and Tarjan (1987), SIAM J. Computing 16(6):973-989, https://doi.org/10.1137/0216062 , finite partition refinement, not an SAT time lower bound. [3] Hartmanis and collaborators, *On tape-bounded complexity classes and multi-head finite automata* (1973), https://doi.org/10.1109/SWAT.1973.20 . The precise countdown and reset-port statements are derived directly here, not attributed to these papers.

**Next TMR-5 target:** Independently inspect TMR-4/018's work-symbol congruence and whether storing the exact visited-cell footprint makes the claimed cost-exact S equivalence automatic. Ask TMR-3 to correct its actual code to physically read before return, and TMR-1/TMR-3 to review the restricted matching lower bound. Find an all-machine unavoidable SAT processing charge beyond optional source-port emulation.

END_OF_REPORT::TMR-5::015::2026-11-14_0353_PST
