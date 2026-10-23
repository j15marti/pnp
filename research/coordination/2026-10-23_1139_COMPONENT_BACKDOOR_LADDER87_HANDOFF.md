# COMPONENT-BACKDOOR-LADDER87: 3+2 collaboration handoff
Timestamp: 2026-10-23T02:39:31Z (11:39 KST)
P versus NP remains OPEN. No roles, schedules, or automations were changed.

## Exact results, with scope
For a supplied source-complete separator S of size s, components V_j, and local hitting sets H_j meeting every ternary clause not touching S, h_j=|H_j|, exact SAT solving needs at most 2^s sum_j 2^h_j SCC calls. Word time is O(A_S+n+ell+2^s[ell_0+sum_j 2^h_j(n_j+ell_j)]), with O(N) bits of reusable workspace plus acquisition workspace. This is an upper bound. Shared variables cannot be independently assigned.

Extend the fixed-width q-orientation chain by s <-> z_floor(q/2) and k private blocks:
(x_j OR y_j OR u_j), (NOT x_j OR NOT y_j), (NOT x_j OR NOT u_j), (NOT y_j OR NOT u_j), (s OR NOT x_j).
The formula is connected, with n=q+2+3k, m=q+4+5k, ell=2q+6+11k. It is UNSAT iff all q orientation bits are one. Every ternary is irredundant on SAT members. The minimum syntactic restriction-only 2-CNF backdoor is exactly k, yet one shared selector yields at most 4k+2 SCC calls and O(q+k) word time. Generic storage is O(N) bits. Canonical template recognition gives O(log N) auxiliary bits, with all validation reads charged.

The q sensitive orientation words retain the exact q-probe lower bound. For k=Theta(q), this gives Omega(N/log N) word time, not exponential time. Word width is ceil(log2(64(n+m+1))), sufficient for source/workspace addresses, and N=(2+4m)w. The final report corrects the narrower draft field-width convention; all encoding counts were rerun.

## Exact NP-complete comparison
One exactly-one-of-three gadget per graph vertex gives k ternary clauses and 3k binary local clauses. Each graph edge adds three binary different-color clauses. SAT assignments correspond bijectively to 3-colorings. Counts: n=3k, m=4k+3|E|, ell=9k+6|E|. Construction is O(k+|E|) word time with streamed output and charged output length. Paths/cycles admit constant-boundary-state dynamic programs. Arbitrary graph coupling is NP-complete, not proved superpolynomial.

## Audit and publication
Executed 5,170 assertions, zero failures; 406,072 Boolean assignments; all 1,099 labeled graphs through five vertices, with 254,253 color assignments. Finite results are COMPUTATIONAL, not asymptotic evidence. Independent peer rerun is pending.
Report: research/main/2026-10-23_1139_MAIN_COMPONENT_BACKDOOR_LADDER87.tex
Code: experiments/review/2026-10-23_component_backdoor_ladder87_audit.py
Raw: results/raw/ladder/2026-10-23_1139_COMPONENT_BACKDOOR_LADDER87.json
Executed code SHA-256: c22e8187e30bf96e38c189a98f96e8a13b5336b0230a86498156446ad14d6a08
Code Git blob: df6cd5e68d5a91493d4f2ce1a58fbfccd6c40caa; remote readback matched the executed file exactly.
Final report commit: b5d0ddafc883e5156fe2a32cc556e1f5dec526bb.

## Role integration and first missing lemma
Role 4: independently verify the connected construction, both-label orientation flips, and graph-coloring endpoint; preserve the positive-remainder transport inequality.
Roles 1-3: any proposed residual/compression lower bound must survive this linear-time family despite k essential ternaries, connectivity and syntactic backdoor k. Do not infer all-context compilation or mandatory Cartesian-product enumeration.
Role 5: hold local ternary blocks fixed while adding binary inter-block constraints; charge separator discovery, failed branches, SCC work and peak live storage.
First missing theorem: superpolynomial post-acquisition compatibility work for every total uniform deterministic decider on one fixed NP-complete language, surviving SCC, affine solving, source inspection, learned constraints, decomposition and decide-first normalization.

## Coverage
Actually read root main.tex, AGENTS.md, CODEX.md, repository skill, INPUT-QUERY-CEILING86 and SMALL-INTERFACE64. Searched the Role 4 directory and implication-chain corpus; no current Role 4 ladder artifact was recovered by those queries. Full corpus coverage and repository preflight execution are not claimed. Primary sources: Aspvall-Plass-Tarjan 1979; Dreier-Ordyniak-Szeider 2024; Garey-Johnson-Stockmeyer 1976. General backdoor-depth phenomenon is prior literature, not a newly claimed result.
