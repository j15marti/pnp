# LSPV-4/566: same-realization work, reference-scan, transient peak and retention frontier

**November 12, 2026, 10:31 PST | PNP Time-Space Resource Auditor | Historical Route A | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

## Candidate theorem and four falsifiers

For the single signed fixed-DAG proof in LSPV-4/560, simultaneously minimize paid work W, parent scan payload B, transient derived-clause peak P and cumulative derived-clause retention A, rather than joining independent resource minima.

F1. A legal four-register cap-45 trace has retention below 748. Exhaustive area-first Dijkstra rejects this within the stated configuration grammar.

F2. A 35-RES trace (W38 including three once-paid owners) achieves retention 748. Work-first exhaustive search instead proves a **minimum 958** at 35 executions and 45 peak.

F3. The new 36-RES/748 trace contains an uncharged repeated step, invalid RES pivot, unavailable paid parent, expanding overwrite or mismatched original signed source. Direct trace replay, strict signed-resolution validation and hosted execution of the unchanged original /386 checker exclude these for the finite packet.

F4. A GF(2) shortcut, paid extension, shared lemma across branches, compact affine representation or alternate proof DAG destroys an all-proofs SAT lower-bound interpretation. These are explicitly **admitted** and outside this fixed-DAG theorem. A cheaper W29 archived proof is already known.

## Original corpus and precedence

The exact original /386 checker is [lspv2_386_independent_verify.js](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_386_independent_verify.js), Git blob **338305c0ce101704205e57543756b8127074a986**. The unchanged original signed W38 source proof is [LSPV-4/560 W38](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json), blob **6b72c961c2db19be87a0936361c467ef3445f4e2**. It has 17 original SOURCE records, six authentic zero-extra-paid defining facets, three globally paid conservative AND2 owners and 35 original strict signed RES identities. All 35 are ancestors of the final empty clause.

Read current root proof1.txt (blob **06f7ebc8c2283304a0f5200b518c6e48fa41e343**) and proof2.txt (blob **ba4d1c0faf9acbce836ffc5e16740b197e4c7bbe**), issue #3, AGENTS.md, CODEX.md, project research skill, current handoffs, LSPV-4/539, /544, /549, /560-565, LSPV-2/579 and LSPV-3/592. Surveyed the recovered /341 and /386 sources, peer artifacts and the present tracker status. Both original /341 and /386 checkers are restricted siblings, not the unauthenticated original combined R_mix341 dispatcher.

Prior novelty boundary: /562 already found 748 retention **without a simultaneous peak cap**; /563 identified inconsistent checkpoint conventions; /564 gave the no-recomputation peak, and /565 showed a cap-41 recomputing execution. The new increment is a **joint cap-45 area optimum, exact per-use parent-input scan proxy, and two new complete checker-accepted certificates representing competing Pareto resource vectors**. It does not rediscover 748 in isolation.

Primary references: Jakob Nordström, Pebble Games, Proof Complexity, and Time-Space Trade-offs, LMCS 9(3:15), 2013, https://doi.org/10.2168/LMCS-9(3:15)2013; Nordström and Håstad, Towards an Optimal Separation of Space and Length in Resolution, Theory of Computing 9 (2013), pp. 471-557, https://doi.org/10.4086/toc.2013.v009a014. Pebbling is an exact formal analogy for this finite state graph, but neither paper transfers the numerical results to unrestricted SAT machine time or physical memory.

## One concrete schedule and the exact resource semantics

A post-step state is a mask of up to four resident **paid RES identities**. Every paid-parent identity must be resident at inference time. All original signed SOURCE/DEF premises are read-only and outside this four-register derived-result proxy. A paid node can be executed repeatedly if its prior result is discarded, paying **one per execution**. Arbitrary deletion is free in this abstract model. In-place overwrite is legal only after the parent has been read and only if the resulting signed clause's canonical JSON-array byte length is no greater than the overwritten parent clause. Fresh output temporarily coexists with all retained premises.

For one selected execution schedule pi, define

$$
\mathcal R(\pi)=
\bigl(W(\pi),B_{\mathrm{parent}}(\pi),
P_{\mathrm{derived}}(\pi),A_{\mathrm{derived}}(\pi)\bigr).
$$

Here W equals 3 globally paid owners plus the number of RES executions; B_parent equals the sum over **each individual executed RES** of the canonical JSON byte lengths of **both signed parent clause arrays**, charging repeated scans again; P_derived is maximum transient canonical derived-clause payload; and A_derived is cumulative post-inference resident canonical payload, counting the final empty clause. B_parent is a **proxy for input traversal work**, not measured physical memory traffic or CPU cycles. Every RES has two parent-reference applications. Shared clauses are paid as deductions once if merely reused, but their parent uses are counted per application. This is the same-realization cost partition.

## Theorem 566.1 (exact restricted fixed-DAG frontier)

Four derived-result registers, paid recomputation allowed, nonexpanding parent overwrite, arbitrary free deletion:

| Maximum transient derived payload | Optimization order | Paid W | Parent-scan proxy bytes | Retention byte-steps |
|---:|---|---:|---:|---:|
| 40 | any | impossible | impossible | impossible |
| **41** | work-first, scan-first or area-first | **39** | **809** | **793** |
| 44 | work-first or area-first | 39 | 809 | 760 |
| **45** | work-first / scan-first | **38** | **790** | **958** |
| **45** | **area-first** | **39** | **809** | **748** |

Both cap-45 witnesses attain **45 bytes of transient derived-clause payload**, with 87 versus 71 retained register slot-steps respectively. The two same-realization resource vectors are

$$
\boxed{(38,790,45,958)\qquad\text{and}\qquad(39,809,45,748).}
$$

The componentwise-looking vector **(38,790,45,748)** is not realizable in this model. Equally, declaring a universal cap-45 retention floor of 958 would overcharge the legal W39 execution with 748 area, violating cost-soundness.

**Proof.** Given a resident set S, enumerate every ready original RES identity j not currently resident, every subset of optional nonparent residents retained until execution, each legal fresh or nonexpanding parent-overwrite production, and every post-step retained subset. Deletion-only moves can be folded into the adjacent paid step because they create no premise and never increase peak or retention; thus enumeration is complete. Each edge represents a concrete legal abstract-storage execution, including a fresh payment for repeated j. Dijkstra with positive additive costs and lexicographic priorities (executions, scan, area), (scan, executions, area) or (area, executions, scan) computes the exact optimum in the complete reachable finite state graph. Cap40 visits 4,084 states with no terminal. Cap41 work-first visits 5,160 states. Cap45 work-first settles 10,477 states; cap45 area-first settles 10,112 states. Explicit witnesses independently replay as legal step sequences and produce the stated sums. The terminal identity has all 35 distinct original identities as ancestors. Therefore all included comparisons and impossibilities are exact for this **specified fixed incidence and storage grammar**.

## Two new complete original-checker-accepted certificates

Topological schedules were compiled using the original signed Resolution conclusions, original oriented pivots, unchanged 17 SOURCE and six facet records, and globally paid three-owner bank. Each paid dependency references an actual earlier chronological record, including a reexecuted RES identity 0 in the W39 schedule.

| Concrete certificate | Work W | Peak derived proxy | Retention proxy | Parent scan proxy | Exact serialized bytes | Original hosted checker |
|---|---:|---:|---:|---:|---:|---|
| [W38/P45/A958](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_1031_LSPV4_566_W38_P45_AREA958_NATIVE386_ACCEPTED.json) | 38 | 45 | 958 | 790 | **3,639** | ACCEPT, 3,915 assertions |
| [W39/P45/A748](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_1031_LSPV4_566_W39_P45_AREA748_NATIVE386_ACCEPTED.json) | 39 | 45 | 748 | 809 | **3,700** | ACCEPT, 3,981 assertions |

Both ran the **unchanged original archived-/386 checker body in hosted V8**, with only file-input and diagnostic-SHA adapters. In each case **all eleven original bundled negative controls rejected**. Original checker source blob was matched before execution. This is not an operating-system Node subprocess; the diagnostic SHA field was deliberately a placeholder. The two certificate blobs, independently read back, are respectively **28fc9f41ec151a741e70274637c06629fb9a224f** and **07a43d1a3edd9fc2e97a26e0fd0a4c769145ba4d**. Complete original Node OS replay is still needed.

## Resource and machine-realization firewall

| Original /386 operation | Paid charge | Evidence, references, verification and retention |
|---|---:|---|
| SOURCE | 0 logical | 17 signed original source occurrences, independently source-bound; nonzero parsing and source-check work |
| Conservative paid AND2 owner | 1 per distinct owner | exactly 3 globally, not 3 per dependent branch |
| True defining facet | 0 additional paid units | six actual facets; owner provenance, parsing and equality verification still needed |
| Signed binary RES | 1 **per execution** | 35 or 36 signed oriented pivot checks and 70 or 72 parent applications; repeated identity pays again |
| Complete original JSON packet | no independent logical tariff | 3,639 or 3,700 evidence bytes; the original readFileSync input Buffer alone is 29,112 or 29,600 bits, plus parsed objects and temporary arrays |
| Parallel logical ancestry depth | not additive W | 13 original fixed ancestry layers; does not include sequential I/O, verification or compiler work |
| Branches, contexts, GF(2), AND3, LOCAL-CONVERT, paid fresh extensions, wire capabilities, deletion and joins in **full R_mix341** | **UNAUTHENTICATED** | cannot invent tariff, parent grammar or a transfer from /386 |

The four-register and 45-byte results describe **derived-clause canonical payload only**, not the original verifier's physical peak RAM or a proof-discovery cost. In the original checker, the parsed full packet remains available, and Resolution materializes new arrays. The proof certificates and the ideal minimum W_R are different objects; no bound on worst-case deterministic SAT machine time follows. Neither alternative GF(2)/extension/branch/learned-lemma shortcuts nor different accepted source encodings have been excluded. The native /341 checker additionally admits known soundness and lexical defects, so checker ACCEPT cannot automatically be interpreted as mathematical UNSAT in that sibling.

## Publication and handoff

[Complete Python finite-graph reproducer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_566_joint_resource_frontier.py) (Git blob **cdd6c0a1b128a3e584f590161cb0b72a61a450ab**); [raw exact state counts, parent-scan weights, three full witness traces and hosted checker results](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_1031_LSPV4_566_JOINT_REFERENCE_FRONTIER_RAW.json). A separate local Python implementation of the same recurrence was executed in the current run; the published portable script was read back but has not yet been independently run in an OS after publication. Original new certificate OS-Node replay remains pending.

Next: OS replay both new certificates with the intact checker and exact SHA, then extend the **same schedule**, rather than independent minima, to temporary decoder buffers, reference retrieval charges and measured verifier data structures. Audit every original full R_mix341 native operation only once historically authenticated, and preserve all legal shortcuts.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof chains P1-01/03/04 and P2-D1/C3/B1/B2/B3 remain OPEN; the present restricted fixed-DAG theorem does not promote a load-bearing proof node. No agent titles, identities, Pacific schedules, historical Route A/B allocations or weights were altered. P versus NP remains **OPEN**.
