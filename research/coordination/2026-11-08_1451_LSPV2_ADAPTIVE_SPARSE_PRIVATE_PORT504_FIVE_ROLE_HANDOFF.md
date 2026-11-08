# LSPV-2/504 five-role handoff | 2026-11-08 14:51 PST

**Route A primary | PROVED/RESTRICTED symbolic construction + COMPUTATIONAL finite control | P versus NP OPEN.**

**Exact chain IDs:** [P2-A2], [P2-A4], [P2-A5], companion [P1-01], [P1-03], [P1-04] unchanged OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

A syntactically bounded private indexed WORK-port macro with $r=\lceil\sqrt{n+1}\rceil$ and $L=k\lceil\log_2(n+2)\rceil$, fixed $k\ge2$, can have $O(r)$ dynamic accesses into a huge virtual range $[2^L,2^{L+1})$. Unlike the static /503 guest, addresses can depend on prior *private read values*, values may be modified by read-before-write, and indices may collide. Charge every INDEX-tape reconstruction/erasure and every source access. A native-tape unsorted exact-address table with last-write-wins and default-blank semantics preserves the complete private execution, including malformed original sources, and costs

$$
T_C(n)=O(T_B(n)+n+r^2L+rL^2)=O(T_B(n)+n\log^2(n+2)),
$$

$$
S_C(n)=O(S_B(n)+rL+L)=O(S_B(n)+\sqrt n\log(n+2)).
$$

Original virtual high-water is $\Omega(2^L)$; the compiled physical port high-water is $O(rL)$. This is an explicitly restricted application of the standard sparse-cell idea already present in FLMV (2005), not a new arbitrary-machine compiler. The guest $B$ still runs once at the full original parent length $n$. **No solver exponent contracts; no SAT child construction and no recursive transformation are obtained.** LSPV-4/503's stronger $O(\log n)$ source recomputation remains the proper control where immutable-source data suffice. The entire irrelevant macro could also be erased by an admissible compiler, so there is no minimization theorem.

**Tests actually executed:** Python 5,742 assertions on 638 original binary sources (47 SAT, 30 UNSAT, 561 MALFORMED), Node 5,296 on 662 sources (35 SAT, 27 UNSAT, 600 MALFORMED), preserving readback, final audit state and last-write-wins collisions. Both independently authenticate the odd-charge signed proper K4 Tseitin SHA256 `849823bdb972026841da0ac55e5bc84545e2f1ac63180563a40232703aab83ae`. Tests are symbolic finite emulators, NOT native FLMV runs or historical R_mix341 checker execution.

**GitHub verified files:** role report `research/agents/lspv-2/2026-11-08_1451_LSPV2_ADAPTIVE_SPARSE_PRIVATE_PORT504.md`, blob `c2fcbe1610c4938e3b84a44dcbad2a6ac8d74813`; executable `experiments/arc/lspv2_504_adaptive_sparse_private_ports.cjs`, blob `3562713aac3ad57b2de55ba091c97240e787becf`; raw `results/raw/arc/2026-11-08_1451_LSPV2_504_ADAPTIVE_SPARSE_RAW.json`, blob `194d6e16047fb39420466c31d60b93e971aa2e3e`. Full independent Python and expanded report available in run archive.

**Requests:** LSPV-4 audit the claimed same-FLMV key/data tape implementation and look for space-favorable replay when state-dependent values occur; LSPV-1/3/5 test whether our authenticated macro assumption is incorrectly generalized to unknown arbitrary deciders or charged derivation systems. Use known expander Tseitin/ordinary-Resolution hardness only as a restricted control, retaining all GF(2), ER, CDCL and shared-DAG shortcuts. Maintain the existing two Route A, three Route B team, historical R_mix341 rules/weights and user governance. P versus NP OPEN.
