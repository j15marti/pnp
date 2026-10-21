# SOURCE-CHANNEL-COMPLETENESS57

Timestamp: 2026-10-22 05:48 KST  
Global status: **P versus NP OPEN; P versus RP OPEN.**  
Scope: two P-vs-NP routes plus the independent P-vs-RP question. Circuit-SAT remains a hostile-control and representation tool.

## Falsifiable repairs fixed before source review

1. **Transcript completion:** replace a digest-only witness-query bound by a ledger containing `q` preprocessing bits, `t` adaptive source replies of at most `b` bits, and `h` complete-witness equality probes.
2. **Complete-state certificate:** permit a short digest only after proving that transition, acceptance, source, timer, solver, trace and history effects factor through it. Otherwise produce a same-digest divergent continuation.
3. **Language-bypass control:** before treating interface hardness as language hardness, test deterministic source inspection and an explicit SAT-NO/malformed control; require any RP verifier to reject every random tape on the NO control.

Repository review then confirmed that DIGEST-PORTFOLIO8 already restricted its theorem to interfaces excluding original source reads, partial clause feedback, timing and other channels. AFFINE-LUMPABILITY-RANK-GATE55 likewise requires complete factorization through the quotient. The repairs therefore sharpen, rather than replace, those results.

## Lemma 57A — source-channel witness-query bound

Let `A` be uniform in `{0,1}^n` and index a uniquely satisfying formula `F_A`. Consider an algorithm that receives:

- a preprocessing digest taking at most `2^q` values;
- `t` adaptive source replies, each taking at most `2^b` values;
- after that transcript, at most `h` equality probes of the form “is the complete witness equal to `w`?”;
- permission to accept only following a positive equality probe.

Then its average acceptance probability is at most

`min(1, h * 2^(q+bt-n))`.

**Proof.** Fix the algorithm's internal coins. The digest and adaptive replies create at most `2^(q+bt)` complete transcripts. At each transcript, at most `h` distinct indexed witnesses can make an equality probe positive. Hence at most `h*2^(q+bt)` of the `2^n` indices can be accepted. Averaging over internal coins preserves the inequality. ∎

Consequently, if success is at least one half for every `F_A`, a necessary condition is

`bt >= n - 1 - q - log2(h)`,

or the corresponding integer ceiling for `t`. This is **ESTABLISHED in the stated interface model**. It is not a deterministic time lower bound, circuit lower bound or language separation.

## Lemma 57B — the forced family has a polynomial source bypass

For `n` divisible by three, split the variables into triples. For each triple, include the seven proper 3-clauses that block every row except the designated row. Add one redundant, designated-assignment-satisfied bridge between consecutive triples. Then:

- `m = 8n/3 - 1` clauses;
- at most eight occurrences per variable;
- one globally satisfying primary assignment;
- under the shared fan-in-two implementation with all `n` NOT gates, two OR gates per clause and an AND chain, `g = n+3m-1 = 9n-4` gates;
- the functional gate trace is unique after the primary assignment is fixed.

**ESTABLISHED.** A deterministic source scanner groups clauses by their unsigned three-variable support. Each genuine forcing block contains seven distinct false rows; the missing eighth row is the forced assignment on that triple. This remains valid after arbitrary clause order, within-clause order and variable renaming. The bridges have cross-triple supports and do not masquerade as seven-clause forcing blocks. The scan takes polynomial time in the explicit source length.

Thus the family is easy in P. The scanner obtains information through the source channel that the restricted `q+h` model omitted. In the completed model it simply pays `t=Theta(m)` clause reads and `b=Theta(log n)` or the actual clause-encoding width. This satisfies rather than violates Lemma 57A.

## NO control and verifier firewall

Adding the eighth blocked row to one triple makes the finite control UNSAT. The source scanner rejects it. In contrast, the unguarded predicate

`b OR F(z)`

has an accepting tape `b=1` even on this UNSAT/malformed control. It is therefore not an RP verifier for SAT. If the intended language is “well-formed forced-family encodings,” a deterministic well-formedness check must guard the verifier; that guarded language is already in P by Lemma 57B.

For a valid unique-witness `F_A`, uniform `(b,z)` gives acceptance probability `1/2 + 2^(-n-1)`. High ANF degree, shared gates, functional Tseitin traces and a source-limited query bound do not remove the `b=1` bypass or the deterministic source scanner.

## Actual WRAPPER source/gate control

The 20-clause, 14-variable root from [`example_dag.json`](https://github.com/j15marti/pnp/blob/main/experiments/DOUBLE_WRAPPER_2026-10-07/example_dag.json) was evaluated on every primary assignment. It has 1,948 satisfying sources. A shared circuit using all 14 NOT gates, 40 OR gates and 19 AND gates has 73 gates and agrees with the clauses on every one of the `2^14` sources; each fixed source produces one deterministic trace.

This confirms only a chargeable forward evaluator. The repository's [`wrapper_sat_quantifier_demo.py`](https://github.com/j15marti/pnp/blob/main/experiments/wrapped_dag/wrapper_sat_quantifier_demo.py) independently records that existence of one good route does not imply correctness of all routes. Neither source access nor trace uniqueness supplies universal wrapper correctness.

## Finite audit

`experiments/review/2026-10-22_source_channel_completeness57_audit.py` passed **581,609 assertions**:

- 120 shuffled/renamed forced-family instances for `n` in `{6,9,12,15,18}`;
- 119,296 primary evaluations and 119,296 deterministic trace comparisons;
- exact `m=8n/3-1`, `g=9n-4`, and maximum occurrence eight checks;
- 800 arbitrary transcript-partition trials for Lemma 57A;
- 308,880 exact threshold checks;
- exhaustive UNSAT control and all `2^14` actual-WRAPPER sources.

Finite tests validate the implementation and catch accounting mistakes; they do not prove an unrestricted lower bound.

## Five-role status and next discriminating tests

| Role | Status | Source/model/resource consequence | Single next test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** Lemma 57A **ESTABLISHED restricted**. | Every source query, reply alphabet, source indexer, reread, trace completion and output bit must enter the ordinary-KT evaluator ledger. A source scanner can be a LOW upper-bound mechanism, not a HIGH lower bound. | For one proposed both-label target, publish exact `(q,b,t,h)` and source-acquisition costs, then construct the best indexed evaluator and compare its exponent with `p_k`. |
| :12 P≠RP | **OPEN.** Forced-family source bypass **ESTABLISHED**; digest-only separation inference **RETIRED**. | Separation requires one RP language outside every deterministic polynomial decider. Interface hardness of a selected verifier is insufficient. | Apply the source scanner and SAT-NO guard automatically to every unique-witness Circuit-SAT candidate; keep only candidates surviving both. |
| :24 arbitrary-decider ARC/FLMV | **OPEN.** | Omitting source replies creates an uncharged contraction. All-input heredity requires source acquisition, live frontier, solver state, ancestors, child outputs and replay at peak on the same machine. | Run the contractor on a decider that discards clauses after scanning and later recomputes them; measure the simultaneous source/replay/table peak. |
| :36 P=RP | **OPEN.** Complete polynomial quotient propagation remains **CONDITIONAL**. | A `q`-bit hash plus an omitted source oracle is not a `q`-bit state. Nonlinear congruence certification remains coNP-complete in general. | Add an explicit clause-stream transcript to DIGEST-LUMP19 and test whether the number of complete quotient states stays polynomial on shared-source adversarial DAGs. |
| :48 synthesis | Both class questions **OPEN**. Channel-complete counting firewall **ESTABLISHED**. | Keep source, digest, primary randomness, deterministic trace, timer/history and equality probes as separate ledgers. | Reject every bound missing any accessible channel, then rerun verifier replacement and direct language bypass before promotion. |

## Relation to the two P-vs-NP routes

- **MKTP magnification:** unchanged. The missing arrow remains a deterministic total both-label SAT-to-ordinary-MKTP generator meeting the ordinary KT thresholds after all source and output costs. Lemma 57A is not a KT lower bound.
- **ARC/FLMV:** unchanged. The missing arrow remains an all-input, hereditary, fully charged arbitrary-decider contraction reaching the matched FLMV simultaneous time-space point. Source scanning is acquisition, not free contraction.
- **Circuit-SAT:** remains a comparison tool. Parsimonious traces preserve source semantics only when source identities and joins are retained; easy gate inspection remains a hostile control.

No root manuscript or role assignment was modified.
