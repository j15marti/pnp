# LSPV-2/438 | Five-role handoff | November 6, 2026, 01:12 PST

**Route A primary. PROVED/RESTRICTED, not universal SAT hardness.** On a public connected cubic graph $G_H$, serialize the **original signed Tseitin proper 3-CNF** with the two $p=0$ clauses at every vertex first, then the two $p=1$ clauses. First-block charges $a$ and second-block charges $b$ yield a valid single-charge-vector source **iff $a=b$**. Exact deterministic $p$-pass left-to-right family recognition with $S$ bits of retained configuration satisfies $(2p-1)S\ge H$, so $TS=\Omega(N^2/\log N)$ for *that streaming architecture*. This is a special case of the earlier LSPV-2/425 and LSPV-4/421 communication method, not an unrestricted machine lower bound.

**Indexed escape:** When public graph neighbor/edge IDs are logspace and polylog-time computable, the actual FLMV indexed read-only input allows literal-by-literal source authentication in $O(N\operatorname{polylog}N)$ bit time and $O(\log N)$ writable high-water, including input index writes and erasures. A generic valid but non-template 3-CNF returns OUT_OF_FAMILY, **not MALFORMED**; it still needs a correct total SAT fallback. This shortcut never proves universal recursively shrinking children.

**COMPUTATIONAL:** Python 4,207 checks across 4,096 first-half/second-half charge pairs on K4, cube and Petersen; independent Node checker 500 assertions; standalone compact Node script 65,794 exhaustive K4/cube checks. Eight corrupt/invalid controls rejected. Full local archive contains Python producer, independent JS, all fixture hashes/records, report, and SHA256 manifest. Host memory and time are not native FLMV measures. Finite test graphs are not a certified asymptotically hard expander sequence.

**LSPV-4:** audit indexed source-address construction and the conditional public graph oracle. **LSPV-1/3/5:** do not add branch/discharge rules to historical $R_{\mathrm{mix341}}$, nor transfer Resolution hardness through the known GF(2) shortcut. Keep assumption-qualified shared AND/OR proof-DAG semantics, paid distinct-node weights, and noncircular B3 open.

**Unchanged governance:** exactly two Route A agents (LSPV-2/4) and three Route B agents (LSPV-1/3/5); no tasks, schedules, identities, enabled states, inference rules or weights modified.

**OPEN:** every fixed uniform total correct polynomial SAT decider $A$, all SAT/UNSAT/malformed encoded inputs, recursively iterable same-machine $A\mapsto\Phi(A)$ with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$; same-R B3; P versus NP.
