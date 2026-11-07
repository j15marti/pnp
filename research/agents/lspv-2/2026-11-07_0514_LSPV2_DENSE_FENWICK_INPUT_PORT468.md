# LSPV-2/468: dense WORK-indexed INPUT-port macros and amortized resizing
**2026-11-07 05:14 PST | Route A | PROVED/RESTRICTED component at charged macro level; COMPUTATIONAL host checks; OPEN native integrated simulator, all-input contraction, P versus NP.**

## IDEA -> SEARCH -> ITERATE
Initial hypothesis: the two-arena ordered-set INPUT-port transducer of LSPV-4/466 can use direct indexed-WORK arrays, Fenwick counts and an intrusive list of live one-bits, eliminating its abstract AVL dictionary assumption while retaining O(S polylog T) physical workspace for sequential guest INDEX-head high-water S.

**Falsifiers:** (F1) repeated jumps require Omega(qS) clearing; (F2) sparse high INDEX j entails host space much larger than S polylog T; (F3) unknown S and T cause cumulative dynamic-resizing cost above T polylog T; (F4) high-index jump + LEFT/RIGHT displacement yields false in-range reads or wrong zero clamp.

Search found that LSPV-4/466 already solved abstract dual-arena amortization; this is a narrower concrete implementation of its missing dictionary step, not a new general decomposition. Compared LSPV-2/467's repaired INDEX-space accounting, LSPV-4/460 source alias, FLMV [R1] Sec. 2.1 and Fenwick [R2]. Read both current trackers [P1-01],[P1-03],[P1-04],[P1-S3],[P2-A2],[P2-A4],[P2-A5],[P2-D1],[P2-B1],[P2-B2], governance handoffs and issue #3, Grok/Claude actual files, konard complexity model and blkph0x method index; searched relevant general literature. No Google-branded separate service authenticated.

## Theorem 468.1: qualified component bound
In a fixed FLMV-type random-access Turing machine, simulate ONE guest INPUT tape and its sequential writable INDEX tape, with T guest transitions, maximum visited INDEX-head coordinate S, finite virtual-input length B and an indexed original-source bit provider. Maintain two physically writable WORK arenas, LIVE and FROZEN. Each direct-address slot j stores the bit flag, its doubly linked live-one neighbors, and Fenwick partial count; the latter admits point updates and maximum-one-position queries in O(log P) cell probes at power-of-two arena capacity P. Host WORK indexed jumps charge sequential construction of their O(log(S+T+2))-bit target INDEX addresses and erasure, O(log(S+T+2)) time per cell probe, rather than free RAM reads.

On guest indexed INPUT jump, retire old FROZEN by following only its nonzero linked list; swap arena identities without copying LIVE, and set signed displacement delta=0. Each retired deletion is charged to a distinct past guest 0-to-1 INDEX write, so total retirement clears <= U <= T. The guest INPUT head is symbolically a+delta, where a is the frozen binary address. Let L=bit_length(B+|delta|+2). If the highest frozen one-bit index m>=L then a+delta>B, so reads are blank and LEFT cannot hit zero. Otherwise reconstruct only <=L low bits, test the exact position, and query a real authenticated source bit when in range. Clamp LEFT at zero. No exponential-length address is materialized.

Grow P by powers of two when the guest's *sequential* INDEX head reaches capacity. Rebuild complete Fenwick arrays and the charged physical record layout at each doubling; summing geometric capacities costs O((S+1) polylog(T+2)) native macro operations. For unknown time exponent, grow field width at time-count powers of two, re-encoding current work records with total O((T+1) polylog(T+2)) amortized native steps, because S<=T+O(1). Including physical INDEX writes, simultaneous dual arenas, source pointer restoration and controller registers gives, with SOURCE-bit service separately charged,

$$
T_{\mathrm{port}}=O((T+1)\operatorname{polylog}(B+T+N+2))+T_{\mathrm{source}},
$$

$$
S_{\mathrm{port}}=O((S+1)\operatorname{polylog}(B+T+2)+\log N).
$$

**Scope:** an explicit indexed-WORK macro construction for the isolated INPUT port, not a compiled native FLMV instruction trace or complete guest interpreter. Source-bit service, arbitrary guest work/output tapes, source authentication, malformed all-input processing, full peak across wrapper stages, and recursive decomposition remain OPEN. Any physical field layout and indexed-work jump must be charged, not silently treated as RAM. The same historical R_mix341 is unchanged.

## FINITE CONTROLS
Python Fenwick + independent BigInt model: 150 seeded traces, 70,200 guest actions, 185,029 indexed-array probes, 107,100 rebuild-cell charges, 6,561 insertions, 5,020 retirement deletions, 3,391 far source reads, max INDEX coordinate 67. All exact stepwise checks passed. Three malformed-header tests rejected. Independently written JavaScript segment-tree + BigInt model, exact published executable: 120 traces, 51,112 guest actions, **28,256 assertions PASS**, 10,127 jumps, 3,482 insertions, 3,108 retirements, 2,131 far reads; no native FLMV run. Both validate signed K4 cubic Tseitin proper 3CNF for 16 charges, 8 SAT/8 UNSAT. These are finite controls, NOT asymptotic certificates.

**Hard-family ledger:** odd-charge cubic expander Tseitin direct strict 3-CNF, H vertices, 3H/2 edge variables, 4H proper clauses, N=Theta(H log H). Exponential ordinary shared-DAG Resolution size on suitable expanders under published expansion/width assumptions. GF(2) elimination is an efficient algorithmic control; no all-machine or mixed R_mix341 lower bound follows. Haken PHP and Cook ER are separate mandatory controls.

**Tracker decision:** restricted component evidence affects [P2-A4] only, while [P2-A2],[P2-A5],[P1-01],[P1-03],[P1-04],[P2-D1],[P2-B1],[P2-B2] remain OPEN. Five existing agents, 2 Route A / 3 Route B roles and schedules, and native R_mix341 grammar/weights preserved. Root main.tex not to be overwritten without fully readable original bytes.

**Actual advance:** replaces the peer's AVL/dictionary abstraction with explicit dense WORK slot and Fenwick/list mechanism with paid dynamic growth. **Next gap:** fixed-finite-alphabet FLMV instruction compilation for all guest tapes and authenticated virtual input, then universal all-input recursive contraction.

[R1] Fortnow, Lipton, van Melkebeek, Viglas. Time-Space Lower Bounds for Satisfiability. JACM (2005), Section 2.1 and Theorem 3.1. https://lance.fortnow.com/papers/files/tst.pdf

[R2] Fenwick. A New Data Structure for Cumulative Frequency Tables. Software: Practice and Experience 24 (1994), 327-336. https://doi.org/10.1002/spe.4380240306

[R3] j15marti/pnp research/agents/lspv-4/2026-11-07_0436_LSPV4_DUAL_ARENA_INPUT_PORT466.md (blob 1f87ebe48c6a2995e974c2d1eee89586091f4fe8).