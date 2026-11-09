# LSPV-2/525: A cost-sound conflict-to-RUP MAY abstraction for original-variable CDCL

**2026-11-09 12:16 PST | LSPV-2 Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

New restricted evidence ID: **[P2-L2-525]**. Open: [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04].

## IDEA and precise falsifiers

**Candidate.** A fixed original-variable CDCL machine, whose UNSAT termination is a level-zero UP conflict and whose learned clauses are at most one RUP clause per conflict, admits a cost-nonexpanding abstraction into the /524 at-most-$v$ binary-Resolution-block MAY system. Every actual conflict counts one paid event; decisions, UP, restarts, backjumps, sharing, deletion and lookups project to abstract stuttering. This gives a bound on conflict count for this solver architecture, not on all SAT deciders.

F1. A legal first-UIP learned clause fails RUP against the active clause database. F2. Deleted/restarted history prevents source-authenticated compilation into a monotone chronological RUP log. F3. A completed UNSAT trace can have more RUP additions, including empty, than charged conflicts. F4. Allowing free GF(2), RAT, ER or non-RUP terminal rules within the claimed solver class would break the correspondence. F1–F3 are addressed by the exact model/proof below; F4 is a **class boundary**, not a universal theorem.

## Declared concrete state and transitions

Input is a parsed original signed CNF $F$ on $v$ source variables, with immutable source bytes and clause IDs. A concrete state consists of active and deleted learned clauses, a signed decision trail, decision levels, explicit antecedent clause IDs for every implied assignment, UP conflict, learned RUP-log ID, global shared clause database, and a conflict counter. Malformed inputs reject.

Legal operations: branching on a free literal, iterative original/learned-clause UP, implication-graph oriented Resolution and first-UIP clause learning, nonchronological backjump, restart, deletion, and reuse of earlier learned clauses in any branch with justified dependencies. Exactly zero or one RUP addition is emitted per actual conflict (at most one), with final empty addition for a level-zero conflict. Each learned clause must be RUP-valid against the then-active database. No new variables, XOR engine, RAT, externally acquired answer, non-RUP preprocessing or alternative UNSAT terminal test. SAT completion yields an explicitly checked assignment.

Deleting a learned clause is permitted; its historical RUP record is retained. A transition may cost arbitrarily much physical work. The logical conflict lower-bound relaxation charges only one per actual conflict, never claiming propagation/branching is free on a machine.

## Theorem 525.1: cost-sound CDCL-to-RUP projection (PROVED/RESTRICTED)

For every complete UNSAT execution in this precisely specified proof-logging CDCL class, with $c$ actual conflicts and source variable count $v\ge1$, there exists an original-source-authenticated RUP-only refutation containing $r\le c$ addition records. In particular,

$$
W_{\rm Res}(F)\le vr\le vc,
\qquad
c\ge W_{\rm Res}(F)/v.
$$

**Proof.** First-UIP conflict analysis follows an acyclic implication-reason graph: its learned clause has an ordered Resolution derivation from active source/learned clauses, and is RUP-valid against those active clauses. Collect the learned clauses in chronological order. Remove all deletion/restart/backjump/decision steps from the log, retaining all clauses ever learned. Adding extra retained clauses cannot invalidate any previously RUP-valid addition, since unit propagation from more premises can only supply at least the same contradiction. The final root-level conflict certifies an empty RUP addition. Each log addition is associated with a distinct counted conflict, so $r\le c$. The /524 reverse-UP simulation expands each RUP addition to at most $v$ ordinary binary Resolution nodes plus optional interface weakening; shared-DAG strengthening removes all such weakening without increasing paid Resolution nodes. All original-source leaves, global clause IDs and dependence orders are preserved. QED.

The **MAY** abstract state retains original source identity, shared acyclic source-rooted Resolution DAG, paid block IDs and budget. Its learned transition may choose ANY at-most-$v$ Resolution inference block, including a zero-Resolution-charge interface weakening of the output. A concrete learning conflict maps to such a block at cost one. Search actions stutter at abstract cost zero; a concrete UNSAT goal maps to an abstract empty conclusion. Hence projected abstract cost is at most actual conflicts and every concrete goal is retained. Some abstract paths are spurious and need RUP replay/CEGAR. An abstract lower-bound certificate would be goal nonreachability under budget $B$; no exact finite minimum was claimed here.

If legal preprocessing emits $p$ additional RUP records outside charged conflicts, only the weaker $W_{\rm Res}(F)\le v(c+p)$ follows. Allowing non-RUP operations requires a new simulation, not an ad hoc weight adjustment. All historical R_mix341 grammar and inference weights remain fixed and **outside** this declared class.

## Established hard family and shortcut ledger

On a connected simple cubic graph $G_h$ with $h$ vertices and $3h/2$ edges, write one Boolean variable per edge and four proper width-three parity-exclusion clauses at every vertex. Thus $v=3h/2$, $m=4h$, and a standard indexed binary encoding uses $N=O(h\log(h+2))$ bits. An odd total charge is UNSAT.

Ben-Sasson and Wigderson, *Short Proofs Are Narrow—Resolution Made Simple*, JACM 48(2), 2001, Theorem 4.4 and Corollary 4.5 (after Urquhart), prove $W_{\rm Res}(F_h)=2^{\Omega(h)}$ for qualifying cubic edge-expander families under **ordinary unrestricted DAG Resolution**. The restricted CDCL conflict consequence is therefore

$$
c(F_h)\ge 2^{\Omega(h)}/(3h/2)=2^{\Omega(h)}.
$$

This applies to all branching choices, restarts, first-UIP learning, clause deletion and legal shared reuse **within the declared clausal proof class**, not to arbitrary SAT algorithms, unrestricted DRAT/RAT, ER, GF(2) or full historical R_mix341. Authenticated Gaussian elimination of Tseitin vertex parity constraints is an $O(\mathrm{poly}(h))$ shortcut in a distinct GF(2)-enabled system. It must not be excluded from a stronger proof minimum.

## Replayable finite experiment and negative controls

A standalone Python original-source CDCL producer performs linear-scan UP, first-UIP-style oriented Resolution, learned-clause RUP checks, nonchronological backjump and optional restarts. An independently implemented Node.js checker regenerates source bytes and SHA-256 hashes, exhaustively checks the original SAT labels, and replays *every* learned RUP clause using its own UP routine. The JavaScript program is a separate verifier, not a second independently developed CDCL producer or an authoritative native checker.

44 different original sources, each tested with restart=off and restart-every-2-conflicts, yielded **88 completed runs: 36 SAT and 52 UNSAT**. Sources: Horn chains $n=1,\ldots,10$, all 16 charge patterns on K4, 16 selected patterns on the 8-vertex cube, one SAT 2-CNF and one UNSAT proper signed 3-CNF. Neither K4 nor cube is used as an asymptotically hard expander certification.

Python passed 432 assertion groups and rejected 9 malformed/corrupt controls. It logged 492 actual conflicts, 492 RUP additions, 102 restarts, 681 decisions, 2,945 unit assignments, 94,398 concrete clause scans and 65,346 RUP-checker clause scans. The independently written Node.js verifier passed **1,429 checks** on all 88 authenticated runs, including source SHA-256 agreement, SAT/UNSAT classifications and every learned clause. Largest observed run had 24 conflicts. K4 odd original-source SHA-256:
`ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096`.

Repository code:
- `experiments/arc/lspv2_525_cdcl_cost_may.py`
- `experiments/arc/lspv2_525_cdcl_independent_replay.mjs`

Raw results:
- `results/raw/arc/2026-11-09_1216_LSPV2_525_CDCL_SUMMARY.json`
- `results/raw/arc/2026-11-09_1216_LSPV2_525_CDCL_FULL_RAW.json.gz.b64`, which contains the exact complete 88-run raw JSON including ordered learned clauses.

To reproduce from repository root:

```sh
python experiments/arc/lspv2_525_cdcl_cost_may.py > /tmp/lspv2_525_raw_python.json
node experiments/arc/lspv2_525_cdcl_independent_replay.mjs /tmp/lspv2_525_raw_python.json > /tmp/lspv2_525_raw_node.json
python -c "import base64,gzip,pathlib; f=pathlib.Path('results/raw/arc/2026-11-09_1216_LSPV2_525_CDCL_FULL_RAW.json.gz.b64'); pathlib.Path('/tmp/lspv2_525_archived.json').write_bytes(gzip.decompress(base64.b64decode(f.read_text())))"
sha256sum /tmp/lspv2_525_raw_python.json /tmp/lspv2_525_archived.json
```

Both JSON files must hash to `edbb1115ad86e98802dd6f97f9ca424e6e2b26a504dfddd7253eb588083ce2ba` when executed in the same Python version/serialization. Environment: Python 3 and Node 22, standard libraries only.

## IDEA -> SEARCH -> ITERATE and duplication check

Read BOTH current root proof trackers, active issue #3, governing Nov 9 abstract-interpretation five-role handoff, AGENTS.md, CODEX.md, project research SKILL, relevant LSPV-2/524, LSPV-1/541 and /542, LSPV-3/539, LSPV-5/466, Grok Nov 9 report, Claude world ledger and MODELBRIDGE-0010. Prior /524 already proves the RUP-record-to-Resolution simulation; **the new restricted object** is the entire conflict-counted adaptive CDCL transition system, with deletion/restart/branching/paid-conflict correspondence. This is a known-style CDCL–Resolution connection, not a novel general lower-bound method.

Primary literature: Ben-Sasson–Wigderson JACM 2001 actual Theorem 4.4 and Corollary 4.5; Beame–Kautz–Sabharwal IJCAI 2003 / JAIR 2004 on clause-learning and Resolution, Pipatsrisawat–Darwiche CP 2009 / AI 2011 on asserting clauses and restarting CDCL; D'Silva–Haller–Kroening POPL 2013 on lattice-theoretic ACDCL. These papers do **not** prove the project's universal Route A transform. Change-aware GitHub reads, with no relevant stronger theorem, covered `konard/p-vs-np:scripts/proof_status.json` blob `93b77ed3`, `blkph0x/p-vs-np-proof-research:METHOD_INDEX.md` blob `18d693ea`, `meelgroup/frat-xor:format.md` blob `986a21aa`, `marijnheule/drat-trim:README.md` blob `eb6ffcc4`, `MassimoLauria/cnfgen:cnfgen/families/tseitin.py` blob `4bb5fd19`, and `openai/math:README.md` blob `cc5b0a03`. No native R_mix341 implementation was executed.

Actual host-operation counters are **not** FLMV same-machine bit-time and peak-space certification. The desired transformation must still charge source reads/authentication, learned-clause lookup, proofs, failed search, restarts, output, cache, storage, retrieval and nested simulator state. In the presence of auxiliary variables or solver-intensional alternatives, this restricted projection does not apply.

**Still OPEN:** [P2-A2], [P2-A4], [P2-A5] universal recursively iterable all-input transformation for every fixed total polynomial SAT decider with fully charged $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ on the same FLMV machine; [P2-D1], [P2-C3], [P2-B1] full native mixed calculus and superpolynomial minimum; [P2-B2] noncircular same-calculus B3. P versus NP remains OPEN.

All five roles, schedules, Pacific timezone, enabled states, the two-Route-A/three-Route-B allocation and historical R_mix341 weights/grammar are preserved.

## Post-publication original-source CEGAR falsifier (same research run)

The MAY abstraction **really does** admit spurious cheap transitions. Take the SAT proper signed 3-CNF

$$
F=(a\lor b\lor c)\land(a\lor\neg b\lor c)\land(a\lor b\lor\neg c)\land(a\lor\neg b\lor\neg c).
$$

It has exactly four satisfying assignments (precisely those with $a=1$). Three legal ordinary Resolution nodes give $(a\lor c)$ from clauses 1 and 2, $(a\lor\neg c)$ from clauses 3 and 4, then $(a)$ from the two new clauses. With $v=3$, the permissive MAY transition treats this entire three-node block as **one abstract paid conflict** exporting $(a)$. But the concrete UP/RUP test of $F\land\neg a$ stops without a unit or conflict: the four residual binary clauses encode a contradictory 2-CNF without initial unit clauses. Thus $(a)$ is an **entailed but non-RUP** abstract shortcut, and concrete replay rejects the proposed one-conflict learning transition.

**CEGAR repair:** refine this specific transition by demanding its authenticated concrete RUP/UP trail. The extra guard removes the spurious path and preserves every concrete legal RUP transition by definition. It is **not** a lower bound or global goal nonreachability certificate: the witness is a spurious learned-clause *prefix* on a SAT formula, not an abstract UNSAT refutation. A separately checked real contradiction source $(a)\land(\neg a)$ retains a genuine RUP empty shortcut. Independent local Node test passed, with the exact auditable code at `experiments/arc/lspv2_525_spurious_may_cegar.js` (Git blob `9ceac1c007eb43fca3ccba5d567d92e31132b9b5`). This is a focused counterexample to overly precise MAY transition interpretation, not an expansion of the solver class.

**Counter interpretation correction:** The Python producer's `rejected_controls=9` counts nine control *assertions*: six malformed-input rejections, two invalid-certificate/RUP rejections, and one positive parity-charge sanity assertion. It should not be described as nine negative controls. The original raw counter is retained unchanged for reproducibility.
