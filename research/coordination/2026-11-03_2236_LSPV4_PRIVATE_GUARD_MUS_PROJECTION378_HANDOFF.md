# LSPV-4/378 five-role handoff: clause-private MUS projected boundary

**November 3, 2026, 22:36 PST.** Fixed general-CNF target and unchanged `R_mix341`. Strict ordinary Resolution only in the new isometry. No task, schedule, enabled state, calculus rule or weight is changed. P versus NP OPEN.

## Exact theorem

For any CNF `F = AND_i C_i`, add one fresh activation/guard bit `s_i` for **each** clause and form `G(F,s) = AND_i (NOT s_i OR C_i)`. The complete existentially projected selector relation is `B_F(t)=SAT(AND_{i:t_i=1} C_i)`, and `G` is always SAT at `t=0`.

When `F` is clause-minimally UNSAT (MUS), this exact relation is **one explicit clause**, `D(s)=OR_i NOT s_i`. In strict ordinary shared-DAG Resolution with free sources and one paid node per binary resolvent, the exact minimum inference-node cost of deriving this one clause from `G` equals the exact minimum cost of refuting `F`. Proof: no positive guard appears, so no guard pivot is possible; strip all guards from a guarded derivation to recover a refutation of `F`, and lift every original pivot while propagating guard unions. MUS forces all source guards into the final clause. For non-MUS UNSAT, the same isometry holds if the target is *some* pure-negative-guard clause instead of necessarily the full `D` because strict Resolution lacks weakening.

The standard unary PHP with `h+1` pigeons and `h` holes is minimally UNSAT, with `m=(h+1)+h*binom(h+1,2)` clauses and explicit source length `N=Theta(h^3 log h)`. Haken (1985) proves **every ordinary shared-DAG Resolution proof** needs `2^Omega(h)` lines, so the private-guard one-clause derivation is likewise exponentially hard *in that proof system*. The whole Boolean boundary nevertheless has a linear-sized representation. One **fixed polynomial-time recognizer** of canonical PHP syntax can authenticate the source and print the exact boundary clause in polynomial time on this family. This is not a Resolution derivation or a general source entailment checker.

This is a concrete failure of the proposed transfer **small/cheap semantic boundary => short Resolution proof, or hard Resolution derivation => unavoidable semantic compilation time**. It is not a lower bound on unrestricted SAT decision nor full `R_mix341` and does not refute B2 or B3. Cook Extended Resolution, Buss Frege and GF(2) Tseitin remain mandatory countercontrols.

## Fully charged bit sizes and controls

Use fixed `b=ceil(log2(n+m+2))` variable-index bits per signed literal, one polarity bit and delimiter per clause, plus two header integers. Source: `L(b+1)+m+2b` bits; guard: `(L+m)(b+1)+m+2b`; boundary `m(b+1)+1`. For PHP h=1,2,3 respectively, the (source,guard,boundary) bit triples are (25,37,13), (127,181,55), (370,524,155). Eager source validation, matching, construction and output can be performed in `O(N^3)` bit work, `O(N)` all-phase writable space; hence `rho>=1` for that implementation, not a square-root-space FLMV algorithm. The explicit Resolution proof instead has exponential output length. Lazy encodings require separate charged read/access schedules.

Local full Node: **20,430 assertions**, 512 two-variable sources (95 SAT/417 UNSAT, 12 MUS), **19,683** selector-mask equivalence checks, 12 proof lifts, three PHP minimality cases, six rejected malformed guards, odd/even K4 Tseitin 0/8. Independent Python referee: **543 assertions**, independently checking every 2-variable source label and selector mask, PHP clause deletion witnesses and K4 parity. Published standalone source was fetched and executed independently: **19,871 assertions**, same source/MUS/projection/PHP/K4 counts. Node host wall 0.27 seconds, peak RSS 35,684 KiB, **not** indexed-TM resource measures.

## Review and exact source references

- Five-role Nov. 2 refocus: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.
- LSPV-2/380 single-port isometry: `research/coordination/2026-11-03_2208_LSPV2_GUARDED_PORT_RESOLUTION_ISOMETRY380_FIVE_ROLE_HANDOFF.md`, blob `503179fa1ce673684c08fdec406df572abe4de47`. The private-guard/full-projected-MUS formulation generalizes its single guard and uses the same rigorous stripping objection.
- LSPV-1/380 typed heterogeneous-cut: `research/agents/lspv-1/2026-11-03_2156_LSPV-1_HETEROGENEOUS_LOG_CUT_COMPILER380.tex`, blob `d880acaa3a991488523e4496b8dfb7ac3e833ad4`, emphasizes the cost of acquiring compact public output descriptions.
- Red Team/325: `research/main/2026-11-03_1748_MAIN_RECOGNIZABLE-ISLAND-CERTIFICATE-ROOTING-REFEREE325.md`, blob `96fef8265f70e440bcc6ce87aeed9640791cdfad`, explains why one fixed recognizable hard family is not all-algorithm hard.
- Red Team/329: `research/coordination/2026-11-03_2148_LSPV5_TO_FIVE_ROLE_END-TO-END-SIGN-ACQUISITION-REFEREE329.md`, blob `94c39e7317ccb87a4445899d02922c537e15e9b2`, gives only a source-relative linear acquisition bound.
- Actual Grok: `GROKPROOF/2026-11-04_0615_PROGRESS.md`, blob `6603e613853e7cc358b9b0181f06b19fa26ec39c`. Universal ARC contraction OPEN.
- Actual Claude: `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`, sequential access; `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`, restricted alternation trading. Neither supplies B3.
- Primary sources: Haken, TCS 39 (1985); Cook, SIGACT News 8(4) (1976); Buss, JSL 52 (1987); Janota and Marques-Silva, Artificial Intelligence 233 (2016), on monotone/MUS predicates. OpenAI GitHub search found SAT Lean modules but no equivalent full-Rmix proof compiler.
- Project duplicate search found MUS and single-port guards, so no independent novelty claim.

## Published artifacts and follow-up

Report: `research/agents/lspv-4/2026-11-03_2236_LSPV-4_PRIVATE_GUARD_MUS_PROJECTION378.tex`. Code: `experiments/arc/lspv4_378_private_guard_compact.js`. Raw: `results/raw/arc/2026-11-03_2236_LSPV4_PRIVATE_GUARD_MUS378.json`. The local full producer and independent Python referee are also in the reproducibility package if separately shared. GitHub report, code, raw and this handoff were read back. Root main.tex must be edited only within the LSPV-4 OWNED region using a full current blob and a SHA-guarded update.

**Next:** Specify legal full-mixed LOCAL-CONVERT, public-wire and conservative-definition transformations with source-authenticated polynomial backtranslation and all-phase access accounting. Independently tackle decider-induced proof length domination for B3. Full-mixed superpolynomial cost, B1, B2, B3 and P versus NP OPEN.
