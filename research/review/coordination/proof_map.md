# PROOF_MAP synthesis — PROOFMAP-0002 — 2026-10-10

**P versus NP remains OPEN.** The first scheduled builder cycle produced useful scoped theorems but no all-input SAT successor, arbitrary-algorithm lower bound, or bounded-list PFCERT verifier.

## Ranked routes

| Rank | Route | Established | Exact missing implication |
|---|---|---|---|
| 1 | Strict successor / charged wrapper | Fixed-depth and recursive composition are valid under one uniform charged all-input contract. | Construct a solver-independent ordinary-CNF successor for every input and every descendant with strict shrink, near-linear time, sublinear space, and physical access. |
| 2 | Bounded-list PFCERT | Counting plus time-bounded Kolmogorov immunity gives a conditional separation endpoint; a matched common-oracle barrier is proved. | Construct the globally bounded accepted-output verifier in a viable time window and separate existential witnesses from executable acquisition. |
| 3 | LSPV Boolean separator | Representation and scoped source-probe obstructions are exact. | Prove arbitrary-SAT source extraction/reconstruction with an ordinary-machine cost lower bound and a genuine nonrelativizing hinge. |
| 4 | ARC15 / finite portfolios | Useful COMPUTATIONAL coverage and positive witness validation. | Close UNSAT/fallback and prove all-input, successor-closed, same-machine resources. |

## Cycle-one verdicts

- MODEL_BRIDGE has no newer completed scheduled delta. MB1–MB3 remain correct CONDITIONAL interfaces; the all-input bridge remains OPEN.
- LOWER_BOUND LB-0002 proves a tight linear source-probe floor for deterministic self-contained, source-free exact transporters on its switch family. It relativizes and is not an arbitrary SAT lower bound.
- The LOWER_BOUND relativized immunity/list-cover theorem is accepted under its declared common oracle and plain-universal-machine conventions. Verifier existence remains OPEN.
- COST_CERTIFICATES CC-0002 correctly counts `2^(w+1)-1` candidates, proves its scoped bounded-list diagonal, and proves the finite semantic hash-factorization criterion and collision identity.
- CC-0002's claim that its *displayed* acquisition bound has exponent `v+kappa` is FALSIFIED/RETIRED as written when `v<1`. With `|p|=O(N)`, that displayed bound has exponent `kappa+max(v,1)`. The smallest repair is either to require `N+|p|+w=O(q)`, or to prove a separate shared-read-only-input random-access acquirer and charge all verifier probes in `q`.
- The newest complete REDTEAM artifact predates LB-0002 and CC-0002. Independent review of those deltas is therefore still pending.

## Exact source versions

Synthesis started from branch head `24bd52d21346824b72199d24b893998041ab1e23`. Relevant blobs: `main.tex` `a5e57493...`; `model_bridge.tex` `30d42a3...`; LB-0002 report `ee395cc...`; lower-bound spine `bae73aa...`; CC-0002 report `b6ce32c...`; cost spine `5b2dcab...`; prior proof-map spine `8106580...`; prior red-team report `a190765...`.

## Corpus and literature reconciliation

Reviewed current protocol, root synthesis, AGENTS, CODEX, repository research skill, STATUS, all five review spines, main4/main5/main9/main10, tasks, current builder reports/checkpoints, and the peer test code/results. Seven additional full Drive artifacts were read: LANG2-0070, PVG-3-0001, PVG-4-0001, PVG-5-0001, REDTEAM-0008, SIM-2-0005, and SIM-2-0007. They show that existence-versus-acquisition, bounded-image PFCERT, switch-family query floors, acquisition dominance, and dynamic witness tax already existed; the current reports refine them rather than originating them.

Primary sources checked: Hirahara Theorem 3.9 for P-immunity; Hirahara–Kabanets–Lu–Oliveira for the limited exact search-to-decision regimes; Fortnow–Lipton–van Melkebeek–Viglas Theorem 3.1 for model-explicit local access; and Carter–Wegman for probabilistic hashing. The first three are directly relevant at their stated scopes. Universal hashing is a failed transfer to exact semantic binding.

## Test and hostile controls

Peer tests reproduced: LB-0002 passed 65 semantic checks, 55 omitted-slot controls, and a 100,000-clause scan; CC-0002 passed 65,811 finite hash maps and 4,083 bounded-list counts. The new exact-integer acquisition test passed eleven hostile and eleven positive-control sizes. At `q=1`, `w=(log_2 N)/2`, the displayed CC bound is at least `N^(3/2)`, not the claimed `N^(1/2)`; when `q=N`, both ledgers have exponent `3/2` up to logarithmic factors. This finite harness supports an exact algebraic correction, not a lower bound on every acquirer.

## Builder assignments

- MODEL_BRIDGE: attack one solver-independent all-input ordinary-CNF successor with descendant closure.
- LOWER_BOUND: extend the switch-probe floor to arbitrary SAT-decider acquisition, or give a matched collapsing-oracle countermodel showing why it cannot extend.
- COST_CERTIFICATES: prove one shared-read-only-input random-access enumeration ledger, including initialization, input probes, output, replay, and peak workspace, then recompute the witness window.
- REDTEAM: independently audit that repair before any executive promotion.

Single next target: resolve whether the shared-input acquirer has time `O(2^w(q+w+log N))` and workspace `O(s+w+log N)` in exactly the endpoint machine conventions. This does not replace the OPEN SAT successor.
