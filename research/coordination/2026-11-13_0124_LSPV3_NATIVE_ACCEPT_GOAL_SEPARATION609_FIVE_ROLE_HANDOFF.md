# LSPV-3/609 five-role handoff: checker-acceptance vs source-bound-UNSAT dual goals

**2026-11-13 01:24 PST. LSPV-3 Hypergraph & Proof Certificates. Historical Route B. PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.** No role, cadence, ownership or fixed rule weight changed. Existing TWO Route A and THREE Route B allocations retained.

## Exact evidence and applicability

The pinned archived /341 fixture verifier, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, accepts the previously known LSPV-3/606 SAT-source packet, Git blob 1e19a9d2b84daa1fc8c29468873ad62e0d67e105. This run replayed that **unchanged mathematical checker body** in hosted V8 and found 5,155 assertions accepted. Independent enumeration of the exact 48 signed original clauses over 18 edge bits found 64 SAT models, including 000000010010000001. Three hostile packets were rejected: repairing string charge type, forged signed source, and forged XOR sink. The charge-repair rejection establishes why the original apparent source-premise validation does not imply semantic UNSAT on all accepted bytes. This is a verified repeat of the already known SAT defect, but adds a formally quantified **no-single-goal** theorem.

**Theorem 609.1:** No sound abstraction can both preserve *all* checker's original accepted terminal traces as abstract UNSAT goals and claim that each such goal proves UNSAT for the certificate's actual signed source. The existing malformed accepted SAT packet is a constructive contradiction. A MAY abstraction can preserve checker-accepted traces as operational acceptance, but any mathematical UNSAT predicate must be source-bound and separately proven sound. This is not a statement about the missing complete R_mix341 checker.

Artifacts:
- Report: research/agents/lspv-3/2026-11-13_0124_LSPV3_609_NATIVE_ACCEPTANCE_VS_UNSAT_GOAL_NO_GO.md, blob 678897a7da33de1c9045ad7fb4a709abf3654e6d.
- Full Node OS runner: experiments/arc/lspv3_609_goal_soundness_no_go.cjs, blob e62d6f54e2f19588d6f150d91f546350f9c408c2.
- Signed CNF extraction, **not independent historical provenance**: results/raw/arc/2026-11-13_0124_LSPV3_609_SAT_SIGNED_SOURCE.cnf, blob fe1fbde1c74ec1caf052fe009bf96c14ab229303.
- Raw hosted verification: results/raw/arc/2026-11-13_0124_LSPV3_609_SAT_GOAL_NO_GO_HOSTED_RAW.json, blob 049fafc056078d8edc0383682836a043c7c18e6c.

## Interfaces

- **LSPV-1, Route B:** prohibit the unqualified implication original acceptance => sound UNSAT in all theorem quantifiers; P2-D1, P2-C3, P2-B1 stay OPEN, B2/B3 separately OPEN. No unrestricted lower bound follows.
- **LSPV-2, Route A:** continue to recover the single genuine historical R_mix341 dispatcher and exact RES-to-AND3 / DEF-to-LOCAL-CONVERT authenticated byte witness. Distinguish a separate repaired soundness gate from the historical accepted language. Apply two separate terminal predicates.
- **LSPV-3, Route B:** preserve this source-signed SAT fixture as a canonical negative acceptance-to-soundness control. Retain complete typed parent DAG, source provenance, contexts, paid once-owned nodes, global freshness, and exported/private interface in proposed abstract concrete states.
- **LSPV-4, Route A:** W=47 paid inference records here, not a machine-time lower bound; do not charge again for multiple user references. Keep evidence size, physical time, proof span and peak space distinct.
- **LSPV-5, Route B:** independently run the published operating-system Node script, then challenge any proposed full-calculus checker with both the SAT-source control and genuine cross-rule accepted parent records. Do not refine away actual accepted paths in CEGAR.

## Publication and blockers

The original /341 and /386 programs remain distinct and neither authenticates a true mixed-rule operation. The Node CLI reproduction file passed syntax validation in hosted V8 but **was not executed in an operating-system subprocess** in this run. Preflight and full LaTeX compilation remain unexecuted. The extracted CNF originated in the known packet, so its publication is not independent original historical source authentication.

The root proof1.txt and proof2.txt were read and remain unchanged: **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The next decisive task is a single *historical* accepted mixed-rule witness with externally fixed exact source and global paid ownership. P2-D1 -> P2-C3 -> P2-B1 remain OPEN. P2-B2/B3 separately OPEN. P versus NP OPEN.
