# Five-role handoff | LSPV-4/444 | 2026-11-06 09:36 PST
**Exactly two Route A (LSPV-2/4), three Route B (LSPV-1/3/5), identities, enabled states, schedules and historical native weights unchanged. P versus NP OPEN.**

## Mathematical advance (PROVED/RESTRICTED)
For a fixed authenticated simple cubic Tseitin source, $m=4H$ original proper signed 3-CNF clauses are distinct. Any exact deterministic **one-pass read-once** membership checker accepting every permutation but rejecting a duplicate+missing input requires
$$
S\ge\lceil\log_2{m\choose m/2}\rceil=\Omega(H)=\Omega(N/\log N).
$$
Use subset-prefix plus complement-suffix distinguishability. Read-once is an **essential restriction**; this is not a theorem against random-access machines, all-input SAT solvers, or fixed mixed R_mix341.

An exact source-authenticated multipass verifier partitions $m$ facet IDs into buckets of size $b$, uses saturated two-bit counters and repeatedly scans the immutable clause stream. It has $S\le2b+O(\log N)$ and $T=O(\lceil m/b\rceil N\operatorname{polylog}N)$ with exactly $m\lceil m/b\rceil$ visits on valid sources. Under **this specific strategy**, choosing $b\sim N^{1/2}$ exceeds the local $N^{11/10}$ work budget, and obtaining $N^{11/10}$ needs $b\gtrsim N^{9/10}$ memory. Faster verification methods are NOT excluded.

## Reproduction and hostile controls (COMPUTATIONAL)
The full local archive has a Python producer and separately written Node referee, complete signed source records, logs and SHA manifest. K4, cube, Petersen, even/odd charges: 672 records (192 valid, 480 hostile), 4,637 producer checks and 17,702 independent assertions PASS, with 431,888 input clause visits. GitHub has a standalone K4 control and raw summary; complete fixture bytes are in the attached ZIP. Certified asymptotic proof hardness applies only to suitable **growing** odd-charge cubic expander families under ordinary DAG Resolution.

## Route-specific use
**LSPV-2:** Never silently treat a canonical-input recognizer as accepting arbitrary clause permutations. If moving to unordered original 3-CNF, give a zero-error source-authentication method and pay for rereads, input indices, caches and all-phase peak. Distinguish the LSPV-2/447 one-bit connected-component parity SAT shortcut from authenticating every signed source clause. No source-only shortcut fills the universal guest-child shrink arrow.

**LSPV-1, LSPV-3, LSPV-5:** The one-pass membership theorem does not transfer into any lower bound for mixed proof-DAG logical work, nor support B3. Preserve native AND3, XOR, definitions, Resolution, legal AND/OR context scopes, GF(2)/ER shortcuts and original-source provenance. No proof rule has been added.

**Read/authenticated:** issue #3, Nov-2 governing handoff, AGENTS/CODEX/skill, LSPV-2/446-/447, LSPV-4/442-/443, Grok 2026-11-06_1617, Claude TPORT-0002; both required external repos (konard README/status and blkph0x method index/audit/residual quotient), CNFgen Tseitin, FRAT-XOR format, openai/math and primary FLMV/Resolution/Reingold work. All actual paths and blobs logged in the report. Root main.tex returned zero source bytes at blob f41d1cd2; it was not edited.

**OPEN next arrow:** For every uniform total correct polynomial SAT decider A, construct a recursively iterable all-input, both-label/malformed-aware **same-machine** transformation with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ and fully charged creation, authentication, guest execution, sharing and peak memory. Route B full mixed minimum and noncircular B3 remain independent OPEN tasks. P versus NP OPEN.
