# LSPV-5/430 | Sublinear local semantic feedback still transfers to Pang's restricted random-3CNF lower bound

**2026-11-08 01:58 PST | LSPV-5 independent red team | PROVED/RESTRICTED conditional on the cited preprint theorem; COMPUTATIONAL finite controls | P versus NP OPEN.**

Material node **[P2-L5-430]** extends **[P2-L1-499]** for one new, DISTINCT fixed calculus. It narrows the restricted-model boundary at **[P2-B1]** but does not change **[P2-D1]**, **[P2-C3]**, **[P2-B1]** for historical `R_mix341`, or same-calculus B3 **[P2-B2]**. Proof1 nodes **[P1-00]** and **[P1-01]** remain unchanged.

## IDEA first and falsifiers

Initial hypothesis: any proposed RES-to-AND3/LOCAL conversion that treats three literal positions rather than the canonical literal set is unsound on repeated or complementary literals. Assumptions: repeated/complementary derived clauses are permitted and factor output must have exactly the same Boolean truth table. Prediction: a minimal repeated-literal or tautological clause separates the conversion.

Precommitted falsifiers: (F1) the grammar rejects every non-proper clause before conversion; (F2) conversion canonicalizes support and checks the complete truth table; (F3) **[P2-L3-494]** already supplies exactly this canonical `CAST3`; (F4) a tracker node already contains the exact counterexample. Search and code inspection triggered F2 and F3: LSPV-3/494-/495 compute `sup(c)` from unique variables, compute the exact table, require support at most three, and reject tautological RES outputs. The positional objection is therefore **FALSIFIED for proposed `R_cast494`**, while the historical interface remains OPEN at **[P2-D1]/[P2-C3]**.

Revised hypothesis: the explicit uniform compiler in **[P2-L1-499]** has overhead `c(b+1)2^b`, not merely an opaque constant for each fixed `b`. Hence a single fixed effective calculus whose legal LOCAL support at source size `n` is `g(n)=floor(sqrt(n))` should still inherit Pang's exponential lower bound, because `2^{O(g(n))}=exp(o(n))`.

Revised falsifiers: (R1) the /499 construction uses a constant depending nonuniformly on `b`; (R2) `g(n)` makes the calculus instance-tailored rather than one fixed effective system; (R3) LOCAL verification hides a `2^b` oracle outside the certificate; (R4) Pang's theorem is not for the same original proper signed random 3-CNF and characteristic two. The proof below rejects R1-R3; /499's exact primary-source audit rejects R4, subject to the preprint's status.

## Claim card

- **Exact quantifiers:** fix the single function `g(n)=floor(sqrt(n))` and the single calculus `R_sqrt-local` before all inputs. For every valid original CNF `F` on declared original-variable universe `[n]`, every valid shared refutation DAG with `q` paid derived nodes maps effectively to a same-original-source syntactic `Res(PC_1/F_2)` refutation with at most `c(g(n)+1)2^{g(n)}(q+m+n+1)` nodes, for one absolute `c`.
- **Model:** original Boolean variables only; no fresh extension variables, branch discharge, hidden answer axioms, or unbounded-support LOCAL rule.
- **Resource:** distinct inference-node work; explicit certificate bits, compiler time, peak storage and span are reported separately.
- **SAME_REALIZATION:** the original indexed CNF and its declared `n` are authenticated by every source and target proof.
- **Weakest useful conclusion:** exponential minimum proof size in this separate restricted calculus on Pang's established random 3-CNF family.

## SEARCH and continuity record

Complete current trackers were read: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 bytes) and `proof2.txt` blob `86fb4253c55c9b2353cdd1b2f2325637e54abd23` (366,477 bytes). Exact nodes reviewed include **[P2-L1-498]**, **[P2-L1-499]**, **[P2-L3-494]**, **[P2-L3-495]**, **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, and **[P2-B2]**. Current issue #3, the November 2 five-role handoff, AGENTS.md, CODEX.md, the complete repo research protocol, LSPV-1/499 report/code/raw, LSPV-3/495 report/code/raw, LSPV-4/490, latest Grok `GROKPROOF/2026-11-08_0930_PROGRESS.md` blob `e3e8c9657e0f2b2e0751752135cf2558e28183cf`, and relevant Claude direct-product audit blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc` were read. The user-provided native-core archive and report remain pinned inputs from the preceding audit; they do not define the new calculus.

Primary searches actually issued:

1. `site:arxiv.org Pang Resolution over linear equations random 3-CNF lower bound Theorem 7.4 Res(1) 8n`;
2. `Cook Reckhow original proof system fixed polynomial time relation definition PDF`;
3. `proof complexity Res(k) k growing with n local semantic inference`.

The search located Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2; the Krajicek review of the Cook--Reckhow definition; Itsykson--Sokolov's exact `Res(XOR)` rules; and Carenini, ECCC TR26-158, for a different growing-`k` `Res(k)` random-3CNF lower bound. Direct arXiv open was disabled in this run, so the exact Pang theorem/rule audit was inherited from the freshly re-read /499 report rather than falsely claimed as a new PDF replay. No separate Google-branded client was available.

Required repository delta review found unchanged heads: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`; `MassimoLauria/cnfgen` `24e633bdbed0d0998493bee99c42faf480c7dc96`; `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`; `anthropics/formal-math` `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; archived `leanprover/leansat` remains at deprecation commit `b83b5d8631ee54bc913b0e6aaf44711c34a50e0d`. Their previously pinned status manifests, format definitions and reproducibility files supply no historical `R_mix341` authentication or B3 bridge.

## Exact established-family ledger

| Item | Exact record |
|---|---|
| Family | `F(n,3,8n)`: exactly `8n` proper signed width-three clauses sampled uniformly with replacement over `n` original variables. |
| Encoding | Ordered indexed 3-CNF; each literal carries sign plus an `O(log n)` variable identifier; source length `N=Theta(n log n)`. |
| Theorem/source | Pang arXiv:2610.00837v2, Theorem 7.2(a), as authenticated in /499. With probability `1-o(1)`, every syntactic shared-DAG `Res(PC_1/F_2)` refutation has at least `exp(kappa n)` nodes for some `kappa>0`. |
| Model/rules | Syntactic resolution over degree-one polynomials over `F_2`; native Boolean axioms, linear combination/weakening/false deletion as stated in the source. |
| Assumptions | Published preprint theorem, characteristic two, degree one, same original proper signed random 3-CNF, source sampled with replacement. |
| Known shortcuts | Global GF(2) addition, all legal local semantic consequences below, ordinary shared Resolution. Fresh Cook/ER definitions, unbounded semantic jumps and branch discharge are not present. |
| Remaining transfer | Authenticate and simulate every historical `R_mix341` rule and then establish a noncircular same-system B3; both are OPEN. |

This is certified proof-size hardness in a stated proof system, not certified UNSAT alone, empirical solver difficulty, or arbitrary-machine SAT hardness.

## ITERATE: one fixed sublinear-locality calculus

### Definition of `R_sqrt-local`

The source parser validates a canonical CNF header declaring `n`, all clause records, literal signs and identifiers, and rejects malformed strings. The following rules are fixed once and for all:

1. ordinary source-authenticated shared-DAG RES;
2. global affine-equation addition over `F_2` on original variables;
3. `LOCAL_sqrt`: from named prior clause, affine or explicitly tabulated factor lines, infer an implied clause, affine equation or explicitly tabulated factor when the union `U` of every parent and output support satisfies `|U| <= floor(sqrt(n))`.

Every LOCAL record contains the complete output table and, for each output-falsifying assignment on `U`, the index of a named parent falsified there. The checker evaluates that parent directly. Thus the semantic check is source-authenticated and polynomial in the complete inference record; no `2^{|U|}` oracle is hidden. All derived factors retain complete truth tables. Global affine lines may enter LOCAL only when their entire support fits `U`. There are no fresh variables, definitions, case split/discharge, weakening of assumption contexts, or unit-cost jump to false. RES alone makes the one fixed system complete.

The threshold depends on the authenticated source header through one fixed total computable function, just as ordinary rule schemas depend on encoded formula length; it is not selected per instance or proof.

### Theorem 430.1 (PROVED/RESTRICTED)

There is an absolute constant `c` such that every `q`-node `R_sqrt-local` refutation of any original `m`-clause CNF `F` on `[n]` compiles to a same-source syntactic `Res(PC_1/F_2)` refutation of size

$$
S(F) \le c\,(g(n)+1)2^{g(n)}(q+m+n+1),\qquad g(n)=\lfloor\sqrt n\rfloor.
$$

**Proof.** Use the /499 uniform invariant, now retaining the parameter. A clause maps directly; a global affine line maps to its unit degree-one line; a local factor on at most `g(n)` variables maps to its canonical CNF containing one exclusion clause for each falsifying assignment, hence at most `2^{g(n)}` clauses. RES and global XOR have constant native simulations.

For one LOCAL node and each falsifying full assignment `alpha` of its output on `U`, the explicit witness index names a false parent. A false clause/factor parent yields the full exclusion clause `D_alpha` by weakening its already translated clause. A false affine parent yields `D_alpha` from the affine unit and Boolean axioms by the /499 linear-combination/false-deletion derivation, using `O(|U|)` nodes. At most `2^{|U|}` such clauses arise. Resolving variables in `U` outside the output support produces the output's canonical CNF in `O(2^{|U|})` nodes. Clause output is a contraction; factor output is the maintained canonical CNF; affine output follows from Pang Fact 7.1 in `O(|U|2^{|U|})` syntactic degree-one nodes. All constants are uniform in `|U|`; therefore a single LOCAL node costs at most `c(g(n)+1)2^{g(n)}` target nodes. Apply the construction in topological order to the distinct source DAG and share every translated ancestor. QED.

The proof also works for any one fixed computable `g(n)=o(n)` with the same explicit `exp(O(g(n)))` factor, but only the concrete `sqrt(n)` calculus is entered as the tracker claim.

### Corollary 430.2 (PROVED/RESTRICTED conditional on Pang)

For Pang's random sources, `m=8n` and `S(F_n)>=exp(kappa n)` with probability `1-o(1)`. Hence

$$
q+9n+1 \ge \frac{\exp(\kappa n)}{c(g(n)+1)2^{g(n)}}
=\exp(\kappa n-O(\sqrt n))
=\exp(\Omega(n)).
$$

Thus `W_Rsqrt-local(F_n)=exp(Omega(n))` with high probability and

$$
\overline W_{R_{\sqrt{\mathrm{local}}}}(N)\ge
\exp(\Omega(N/\log N))
$$

along an unbounded encoded-length sequence. This minimizes over every legal shared DAG of the fixed calculus, including arbitrary reconvergence and free after-the-fact choice. No branching/discharge rule was added.

## Independent challenge and finite replay

Independent Python and JavaScript implementations exhaustively agreed on 65,808 ordered one-parent Boolean-factor pairs through `b=3`, exactly 6,651 valid implications (`9+81+6561`); all 16,777,216 ordered two-parent/output triples at `b=3`, exactly 5,764,801 implications; and 308 support-projection cases producing 1,104 target exclusion clauses. Python additionally checked 19,765,032 output-false rows each had a named false parent, seven malformed/header/table controls, and the exact `g(n)`/subexponential overhead ledger. Runtime was 5.414662763 seconds and maximum RSS 8,320 KiB. These are finite controls only.

Hostile controls:

- **Affine/Tseitin:** unrestricted global XOR remains legal, so same-characteristic Tseitin is an easy upper-bound control rather than a hard family.
- **Cook ER:** fresh extension variables are deliberately absent; Cook's PHP shortcut therefore blocks any transfer from Haken Resolution hardness to a system that later authenticates such definitions.
- **Horn/2SAT/tiny core:** RES remains available and may be short; the theorem claims only Pang's one hard random family, not pointwise hardness.
- **Sharing/AND obligations:** every named inference parent is a conjunctive obligation; the translator uses one certified false parent per output-false assignment and shares translated ancestors once. No branch-local conclusion leaks.
- **Padding/renaming:** `n` is the authenticated original universe. A proof cannot inflate `n` without changing the source encoding; variable renaming preserves support and tables.
- **Semantic oracle:** replacing the explicit witness table by an uncharged truth oracle would define another calculus and invalidate the proof-size accounting.

## Resource ledger

- **Logical nodes:** distinct source DAG nodes counted once; target compiler factor `c(g+1)2^g`.
- **Evidence bits:** a factor table uses at most `2^g` bits. A LOCAL witness table uses at most `2^g ceil(log2(q+2))` bits plus support/line records. These are explicit, not free.
- **Parsing/source/index/head reads:** complete source and every referenced line must be validated. Literal identifiers cost `Theta(log n)` bits.
- **Construction/verification/output:** the effective compiler scans the full proof record, materializes or streams the canonical clauses, verifies source indices and emits every target record; time is polynomial in input plus output bit length, not in `q` alone.
- **Space:** full materialization can require output-size simultaneous storage; streaming can reduce retention but may increase retrieval/recomputation. No FLMV machine-space claim follows.
- **Work/span:** logical work is the distinct-node total. With parallel assignment rows, macro span can be `O(g+log 2^g)` plus dependency span, but actual schedules pay references, table reads and joins. No claim equates minimum work, span or realizable time/space.
- **Search:** the ideal minimum excludes discovery; implemented proof search, failed policies, restarts, caches and retrieval remain charged upper-bound costs.

## Tracker, manuscript and precise boundary

`proof2.txt` requires material addition **[P2-L5-430]**; `proof1.txt` has no material change. The tracker change is additive and does not alter historical grammar, weights, roles, schedules, or enabled states. Root `main.tex` was refetched by metadata, but the connector did not return a complete 1.7 MB body; it was therefore not edited, preserving outside bytes and ownership. The local repo preflight could not be run against a complete checkout for the same reason; remote invariants and all available marked artifacts were checked without claiming a successful local preflight.

**Actual advance:** fixed-constant locality in **[P2-L1-499]** can be raised to one fixed `floor(sqrt(n))` locality threshold while retaining exponential restricted proof-size hardness. **Verification:** complete symbolic uniform compiler proof plus two independent finite replays. **Publication target:** report, code, raw, handoff, conflict-safe tracker update and issue #3 comment. **Precise remaining gap:** fresh/nonlocal historical `R_mix341` rules, the entire all-rule minimum, and noncircular same-calculus B3 remain OPEN. P versus NP remains OPEN.
