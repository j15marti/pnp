# LSPV-5 interactive continuation: native-core audit and completion-robust Tseitin exclusion

November 7, 2026, 22:19 PST request. **PROVED/RESTRICTED theorem application; COMPUTATIONAL new accepted-byte replay. P versus NP OPEN.**

Affected existing nodes: [P2-B12], [P2-D1], [P2-C3]. [P2-B1] and noncircular B3 [P2-B2] remain OPEN. No new agent, schedule, rule or weight is introduced.

## IDEA -> SEARCH -> ITERATE

Initial target: test a source-preserving polynomial-output normalization using the actual historical mixed rules. Falsifiers: unsupported rule composition, exponential backtranslation, and lost branch assumptions.

The source review changed the target. The missing full parser is not needed to exclude standard cubic odd-Tseitin: its short SOURCE/AND3/XOR proofs already avoid every disputed interface. Adding more legal derivations cannot increase the minimum. This is a family failure and a failure of specified normalization targets, not a P-versus-NP result.

Prior results are credited: /341 proves the linear optimum; /469 [P2-B12] proves exact ideal span; /496 corrects the one-hot source identity. The new contribution is native-checker validation of independently rebuilt balanced proofs and an independent syntactic audit of /496, not a claim of new asymptotic mathematics.

## Recovered historical bytes actually executed

The local producer and verifier matched Git blobs `4081022e8a3841d79f751a3d3a7a10decbb026da` and `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0` respectively. Execution reproduced the 197,514-byte original packet, blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`, and the 1,469-byte, 30,714-check original verification record, blob `42ba4cad6dc165aa9e96a29011df5602d33281b9`.

The new Python constructor balances each four-clause AND3 packet and then the binary XOR tree. Original source clauses, charges, graph, witnesses, rule tags, costs and total proof work remain unchanged. The **unmodified historical verifier** accepts every rebuilt fixture and reproduces its original stdout byte-for-byte. A separate Python semantic/source checker passes 56,528 assertions.

| Graph | Clauses | Paid nodes | Old ideal depth | Balanced ideal depth | Exact work optimum certified |
|---|---:|---:|---:|---:|---|
| K4 | 16 | 15 | 6 | 4 | Yes |
| K3,3 | 24 | 23 | 8 | 5 | Yes |
| Cube | 32 | 31 | 10 | 5 | Yes |
| Petersen | 40 | 39 | 12 | 6 | Yes |
| Prism6 | 48 | 47 | 14 | 6 | Yes |
| Prism16 | 128 | 127 | 34 | 7 | Yes |
| Bridged K4 pair | 40 | 39 | 12 | 6 | No, only 36 clauses indispensable |

Ten mutations were rejected by both implementations: wrong XOR, wrong factor table, source sign, absent parent, forward/cyclic parent, duplicate ID, RES tag, LOCAL-CONVERT tag, DEF tag, and even charge. SAT and source-deletion witnesses were independently checked. The small graphs are finite controls, not asymptotic hardness certifications.

Balanced packet SHA-256: `7904069986fa806338de0dfa05006c29cf61cfd6e53050e31a80fa0e789ed2db`.

## What can be concluded without the full parser

Let B_h be one-bit-per-edge odd-Tseitin on a connected simple bridgeless cubic graph with h vertices: 3h/2 variables and 4h proper signed 3-clauses. In every sound source-explicit, conservative, unit-paid, at-most-binary completion preserving the historical core rule schemas:

$$
W(B_h)=4h-1,\qquad D_{\mathrm{ideal}}(B_h)=\lceil\log_2(4h)\rceil.
$$

Proof: three AND3 nodes per vertex and h-1 XOR nodes give the upper bound. Every original clause is indispensable by the prior deletion-witness theorem. A connected ancestor DAG with m sources and q paid nodes has at least m+q-1 edges and at most 2q, so q>=m-1. Depth d covers at most 2^d original sources. The balanced construction attains both bounds. All shared nodes are counted once. The all-size claim assumes preservation of the rule schemas, not merely agreement on seven examples.

Suitable expander instances have exponential ordinary-Resolution proofs [1]. A universal same-source converter from these polynomial-bit mixed proofs to ordinary Resolution with polynomial output is therefore impossible. A full parser cannot repair that mathematical conflict. No algorithm-independent SAT lower bound follows.

## Correct one-hot transfer, independently checked

Pang's Section 7.1 uses a one-hot Tseitin source, not literally B_h. For q=2, T_h has two indicators per edge, exactly-one clauses, and four forbidden-value clauses per vertex: 3h variables and 7h clauses. Theorem 7.2(b) concerns fixed-degree opposite-characteristic target systems; it is a 2026 preprint [2].

Derive each bit clause from its one-hot clause by resolving every negative zero-indicator against the corresponding at-least-one clause. Across the four local clauses there are exactly six replacements per vertex. Each ordinary RES step expands into one polynomial linear-combination line and one false-constant deletion line, all degree one. This gives the correct direction

$$
S_{p,r}(T_h)\le S_{p,r}(B_h)+19h,\qquad r\ge1,
$$

including 7h source axioms and 12h derived lines. Under the cited expander theorem for characteristic three, the one-bit target remains exponentially hard. Thus the analogous polynomial-output normalization from the preserved mixed core into fixed-r Res(PC/F3) is also excluded, conditional on that preprint result.

The independent producer/checker emitted 21 literal-exact target certificates on seven graphs over primes 2,3,5. It passed 23,794 assertions and rejected four forged records. Local one-hot semantics were checked on all 64 assignments per vertex. These are separate target-system checks, not an implementation of missing R_mix341 rules or a numerical verification of an asymptotic theorem.

## Scope and costs

The recovered verifier implements AND3 and XOR, not RES, LOCAL-CONVERT or DEF. Rejection of a RES tag does not delete RES from the prose calculus. RES-to-AND3, branching/discharge and exported/private-wire semantics remain unauthenticated. No such step was used here.

Ideal span uses unit inference duration and unlimited processors; it is not machine time. Dense affine masks and deletion witnesses can require O(h^2) bits. Construction, parsing, hashing, verification, rejected policies and output are separately paid. One host balance audit took about 0.57 seconds; peak RSS was not measured. No FLMV resource exponent or same-machine contraction is claimed.

The existing /397 cofactor translation has exponential dependence on nonlinear definitions. It does not give a polynomial full-calculus normalization. The next lower-bound candidate must survive nonaffine extensions and conversions; a parity family cannot be rescued by suppressing its legal XOR shortcut. Haken PHP and Cook ER remain restricted-hardness/shortcut controls, not all-machine hardness. Published random 3-CNF target-system results remain only candidate starting points for full-mixed analysis.

## Continuity and publication limits

Pinned head read: `b5572117146a0aff7cfda988502e1c613a772d15`. Consulted both root tracker responses, the governing November2 handoff, AGENTS/CODEX/research skill, current issue3 page, /341, /397, /413, /469 and /496 evidence; actual Grok `GROKPROOF/2026-11-07_0819_PROGRESS.md` and Claude world-ledger README. Relevant search terms included extension-free Res, arity deficit, and Tseitin span/minimum. External checks included both required repositories' manifest/audit, FRAT-XOR format and OpenAI math README. These do not authenticate missing project rules. General web search was used; no Google-specific or local Lean execution is claimed. The entire corpus was not exhaustively reread; repository preflight was not executed in this partial workspace.

The large tracker response could not be safely reconstructed as a complete replacement locally, so root trackers are not overwritten. This report and issue3 record the proposed evidence attachment to [P2-B12]/[P2-D1]/[P2-C3]. `main.tex` returned empty content for nonempty blob `68188a24badda635a5983fda1c381cdb694fd497` and was left untouched. These are explicit publication limitations, not mathematical closures.

Code and recorded results: `experiments/review/2026-11-07_2219_native_core_audit/`. The directory contains pinned historical artifacts and both new scripts. Run the historical producer/verifier, then `python3 balance_and_audit.py` and `python3 onehot_transfer_audit.py`. Full newly generated packets, certificates, report and hashes are also supplied in the conversation's reproducibility archive.

## References

[1] A. Urquhart, Hard Examples for Resolution, JACM34(1),209-219,1987, DOI10.1145/7531.8928. Standard ordinary-Resolution theorem; full paper not independently replayed here.

[2] S. Pang, A Degree-Size Relation for Resolution over Polynomials, arXiv:2610.00837v2,2026-10-24, Section7.1 and Theorem7.2(b). https://arxiv.org/html/2610.00837v2

[3] LSPV-1/469: `research/agents/lspv-1/2026-11-07_LSPV1_TSEITIN_WORK_SPAN_RIGIDITY469.md`, [P2-B12].

[4] LSPV-1/496: `research/agents/lspv-1/2026-11-07_2200_LSPV1_ONEHOT_BIT_ENCODING_TRANSFER496.md`, blob `d6c56ef88750ea3733d496c97adaf499925d2a76`.
