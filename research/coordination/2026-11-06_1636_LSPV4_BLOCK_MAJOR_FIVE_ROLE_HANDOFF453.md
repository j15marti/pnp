# LSPV-4/453 five-role handoff | November 6, 2026 16:36 PST
**Allocation unchanged:** LSPV-2 and LSPV-4 Route A; LSPV-1, LSPV-3 and LSPV-5 Route B. No changes to schedules, identities, fixed R_mix341 grammar/weights, or historical source. P versus NP OPEN.

**PROVED/RESTRICTED:** The LSPV-2/455 special block-structured SAT compiler can authenticate/read the original input only **once**, instead of up to $2^k$ full input scans. Buffer one source block and iterate the $2^k$ separator assignments, preserving a distinct alive[a] status for each assumption context. Execute the unchanged SAT guest A only for live assignments, explicitly materialize each child, and AND its response into alive[a]. At the end take the OR. Even after all assignments fail, parse the remaining source before distinguishing UNSAT from malformed input.

**Fully charged conditional special-language resources:**
$$
T(N)\le N^{\max(11/10,3/5+t/2)+o(1)},\quad
S(N)\le N^{\max(1/2,s/2)+o(1)}
$$
for source blocks of $N^{1/2+o(1)}$ bits, at most $N^{1/2+o(1)}$ blocks, and common separator $k\le0.1\log_2N+o(\log N)$. Child generation remains $O(2^kN)$, and guest calls $\le h2^k$; this improves source read work but not the worst-case exponent. One block buffer, one paid child, guest work/index tapes, status array and all intermediate buffers coexist in charged peak space.

**COMPUTATIONAL:** Complete original strict-3CNF fixtures: 48 (40 SAT, 8 UNSAT), 484 guest calls; independent Python 294 PASS, JavaScript 298 PASS. Published self-contained Node checker: 4 contrasting cases and 1 malformed control, 13 PASS. Illustrative fixed-width source bit total 14,007 versus full reread upper count 53,396. Host code is not native FLMV benchmarking.

**Transfer remains OPEN:** On established cubic-expander odd-charge original Tseitin 3CNF, source-packet separator needs $\Omega(H)$ variables per LSPV-2/455, while this wrapper requires $O(\log N)$. Fast GF(2) parity remains a legal easy shortcut, and ordinary shared-DAG Resolution lower bounds do not transfer automatically to the full mixed calculus or general computation. General all-input, same-machine, recursively iterable $\Phi(A)$ and Route B B3 remain OPEN.

Report: research/agents/lspv-4/2026-11-06_1636_LSPV4_BLOCK_MAJOR_JOIN_RESOURCE453.md
Code: experiments/arc/lspv4_453_block_major_public_selfcheck.js
Summary: results/raw/arc/2026-11-06_1636_LSPV4_453_BLOCK_MAJOR_SUMMARY.json
Full 48-source producer and independent verifier are provided in the separate local reproducibility archive; cannot publish its binary ZIP via text-only GitHub connector.
Root main.tex content not readable via authenticated fetch (blob d8514a8f), left untouched.
