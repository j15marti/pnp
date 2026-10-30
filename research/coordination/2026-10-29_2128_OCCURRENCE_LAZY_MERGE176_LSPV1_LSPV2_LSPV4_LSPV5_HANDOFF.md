# OCCURRENCE-LAZY-MERGE176: LSPV-3 issue #2 research handoff

Timestamp: 2026-10-29 21:28 America/Los_Angeles. Owner: LSPV-3, PNP Adaptive Certificate Theorems, currently acting on issue #2's resource-accounting package. Existing five-agent schedules and roles are unchanged. Both P=NP and P!=NP remain OPEN.

## Proved narrow theorem

For every proper width-k CNF F and partial source assignment p, let P=sum_x d_x^+ d_x^- be the number of ordered positive-vs-negative source-occurrence pairs. Unit propagation after adding **all first-generation** non-tautological resolvents is exactly reproducible with a lazy source-parent-authenticated policy that fully saturates source UP, then fires only unit **merge** resolvents and repeats. No derived resolvent table is stored. Indexed-RAM word-time O(N+(n+1)^2*m*k+(n+1)*P*k^2), peak O(N+(m*k+n*k)*log N) bits. Every failed scan, index rebuild, source check, assignment, and witness pointer is charged. This upper bound is per residual and does NOT imply polynomial full SAT branch-DAG work. Full proof: [LSPV-3 report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-29_2128_LSPV-3_OCCURRENCE_LAZY_MERGE176.tex), commit `1f80c367e575edac7e2541f5f68f4cb989936ff0`, blob `0bb351c866d105fb3d668f8fb15afe4c435ec78d`, exact content readback.

## New hostile family: distinct resolvents still overcount arbitrarily

For r,s >= 1 let G_(r,s) = AND_i (x OR a OR u_i) AND_j (NOT x OR a OR v_j). All r*s non-tautological opposite source resolvents a OR u_i OR v_j are **distinct** and merge. Their raw additive forbidden cube weight is r*s/8 but exact union density is (1/2)(1-2^-r)(1-2^-s) < 1/2, so the ratio diverges even after deduplication. Every positive source clause has exact Q_j=2^s; every negative one Q_j=2^r. Under all u_i=v_j=0 with x,a unset, source UP is stuck but one certified merge forces a=1. The entire grid is SAT by a=1, and is not strict22: it is an easy control, not hardness. Source-original forbidden FULL-assignment union is already saturated before sound learning, so it cannot amortize learned clauses.

This closes the specific distinct-versus-duplicate weakness of LSPV-2 MERGE-FILTER239's earlier **repeated** resolvent counterexample. The non-merge UP-redundancy fact is known from Babka et al. 2013 Lemma 3.3, DOI 10.1016/j.artint.2013.07.006, not claimed as new.

## Code, raw evidence and provenance

[Verified independent concise Python reproducer](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-29_2128_LSPV-3_OCCURRENCE_LAZY_MERGE176_spotcheck.py): 891 exhaustive partial-prefix checks for grid_2_2, XOR, 2SAT, Horn, UNSAT, six exact grid forbidden-union enumerations; locally independently run PASS; source SHA-256 `a084e5832254701c7c3cc4de02470e7bbe28645c2d25fe75e63187685b4eb565`; GitHub commit `fee30e21af7f4bf7cb4b8fef437cf052408057bf`, blob `7b610e62fd94445eff0a36e358201a30abd20516`; readback exact.

[Verified summary JSON](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-29_2128_LSPV-3_OCCURRENCE_LAZY_MERGE176_summary.json), commit `c04dab21eb6115b91879aaa5150d232c850db480`, blob `ba8ae8991bf0e940989854ba6fe6403a0d9224c4`; exact readback.

Full 12,550-byte Python implementation and 72,245-byte raw JSON were created and executed locally. SHA-256 of full source `ce299a88c7ee7f5509986a7dfc67dd39aa8b0f2038beec84f63e328c199eccbc`; full raw `12553df005d4fa10a059dd18c646f2d813d50641dc748b349d5d4c3f772fc3f3`. These exact full bytes are **PENDING GitHub upload** because Library upload returned `container_session_unavailable`; they are available as same-turn sandbox attachments but NOT presented as cross-run repository files. Do not treat the 891-prefix spotcheck as if it reproduced all 4063-prefix full-implementation checks.

Full implementation test: 4063 eager-vs-lazy UP partial-state comparisons, 720 exact complement identities, eight grid scaling instances, exact Q_j and small SAT labels (18 source CNFs), complete original-formula DPLL SAT witness checking and exhaustive UNSAT branches. Overall source/lazy/eager DPLL nodes: 81/77/77; selected work 3044/18267/29838. The Python proxy charges explicit scans and writes but not all interpreter operations; elapsed times and `tracemalloc` peaks recorded. For grid r=s=128, same-run selected work lazy/eager 4124/429569, simultaneous peak 56944/1195200 bytes. Those scaling prefixes are exceptionally easy, not universal bounds.

Root `main.tex` only LSPV-3 region was amended; verified commit `b54fed5df8e144b583ae9d04147e5ec8602fa44f`, blob `826ab6f63ae297db9d8daa7e1777e56d1421e783`. Exact readback confirmed all bytes outside region unchanged, balanced four role markers and explicit OPEN status.

## Directed handoffs

- **LSPV-1 formal semantics:** Treat full-assignment excluded-union potential as zero for every sound learned clause once source clauses are included. Seek a certified partial-prefix frontier potential with acquisition expense and overlap correction, not additive raw cube volume.
- **LSPV-2 adaptive policy:** Test a cost-capped lazy merge trigger against failed literal and XOR/2SAT/Horn early exits. Do not infer net benefit from lower branch counts. Need policy discovery charges and completed SAT/UNSAT proofs.
- **LSPV-4 red team:** Independently attack exact eager/lazy fixed-point equivalence on short conflicting prefixes, source index/sign handling, and grid Q_j=2^s/2^r. Try connected signed strict22 SAT/UNSAT lifts with genuine merge effects.
- **LSPV-5 circuit/reduction:** Preserve source parent pointers, exact sign and clause indices in streamed proof DAG; test compatibility with full-interface joins. Do not infer ordinary SAT lower bounds from P, interface width, or a restricted proof-system count.

**Next open lemma:** A recognizable, source-faithful connected strict signed exact-(2,2)-3CNF paired SAT/UNSAT class with a polynomial whole-search adaptive DAG ledger (including score discovery, failed branches, switches, memo and reconstruction). No general P versus NP resolution.
