# LSPV-4/434: Nested epoch-tagged Tseitin ports and snapshot lifetime

**November 6, 2026, 00:36 PST. Route A primary. PROVED/RESTRICTED plus COMPUTATIONAL. Universal FLMV transformation, same-R B3, and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE: hypothesis, four falsifiers

Hypothesis: LSPV-2/437's epoch-tag array handles sequential sibling children but **not nested, simultaneously active parent-child source ports** if their epochs overwrite the same tag cells. A charged per-depth bank repairs this for depth-first nested charge edits on an authenticated common graph, without preserving arbitrary previously completed siblings.

F1: could one shared epoch bank still restore a live parent after a child overwrites its tag? **No; explicit K4 witness below.** F2: do independent depth banks leak stale epochs or repeated updates? **No; exact induction.** F3: can the repair silently escape the physical indexed-work-tape space ledger? **No in the declared fixed-tape contiguous layout; whole bank capacity and index construction/erasure are charged.** F4: does this yield an all-input shrinking SAT compiler? **No; fixed-graph descendants do not shrink and no general join/selection algorithm is given.**

## Exact established family/theorem/encoding/method ledger

For connected simple cubic G=(V,E), H vertices, M=3H/2 edges, and sorted incident edge IDs a_v<b_v<c_v, use canonical proper strict 3-CNF:

$$
C_{v,p,r}(\chi)=\ell_p(x_{a_v})\lor\ell_r(x_{b_v})\lor\ell_{p\oplus r\oplus1\oplus\chi_v}(x_{c_v}),\quad p,r\in\{0,1\},\quad\ell_0(x)=x,\ \ell_1(x)=\neg x.
$$

There are 4H proper three-clauses and M edge variables. Under LSPV-2/435's fixed-field binary format, with w=max(1,bitlength M), eight-bit magic, unary H and M, endpoint and signed literal fields and terminal 00:

$$
N_H=8+(H+1)+(M+1)+2Mw+12H(w+1)+2=\Theta(H\log H).
$$

Connectedness gives SAT iff XOR_v chi_v=0. Odd charge is mathematically UNSAT, which is **not** by itself proof-size hardness. Urquhart (1987) and Ben-Sasson/Wigderson (2001) give exponential **ordinary shared-DAG Resolution** lower bounds on suitable growing cubic expander families, not mixed R_mix341, ER, arbitrary SAT machines, or finite K4/cube/Petersen controls. A short GF(2)/AND3 algebraic refutation is an essential legal upper control, subject to native mixed-rule authentication.

## Theorem 434.1: concrete nested lifetime counterexample (PROVED/RESTRICTED)

Use K4, base all-zero charge b (SAT). Parent epoch 1 toggles vertex 0, so its exact charge parity becomes odd (UNSAT). A child of that parent, epoch 2, toggles vertex 0 again, making its exact charge parity even (SAT). The naive **single** epoch-tag array now has tag[0]=2. Returning to parent epoch 1, its stipulated read returns zero for tag mismatch; the actual parent charge remains one. Thus the port returns the wrong original-source sign at vertex 0, even falsely classifying the parent as SAT. The counterexample falsifies only this ephemeral-bank reuse, not general persistent data structures or LSPV-2/437's correct sequential-sibling result.

## Theorem 434.2: depth-banked repair and full port ledger (PROVED/RESTRICTED)

Fix an authenticated shared graph and base charge b. Along a depth-first active recursion path of depth <=D, each level i contributes unsorted, repeated, valid edit IDs U_i. Reserve distinct H-entry epoch-tag/parity banks for *live levels*. With q an authenticated upper bound on epoch starts per bank, tag width B=ceil(log2(q+1)), distinct positive nonwrapping epochs, and a packed contiguous layout on **one fixed indexed work tape**, each bank reports

$$
\delta_i(v)=\bigoplus_{u\in U_i}[u=v].
$$

The active source charge is

$$
\chi^{(d)}_v=b_v\oplus\bigoplus_{i=1}^d\delta_i(v).
$$

Induction over edits handles repeated toggles and stale tags within each bank. Since deeper banks occupy separate work-tape addresses, no descendant invalidates an ancestor; after a descendant returns, the parent can be queried exactly. Substitution into the original canonical clause expression proves **literal-bit** equality, not just equisatisfiability. The construction is *stack-persistent only*: revisiting an already finished sibling requires paid replay, retention, or a different persistent representation.

With R total edits, Q requested charge-sensitive source bits, q epoch starts, fixed depth D, and authenticated source and bank addresses, the physical **port-only** cost is

$$
T_{\rm port}=O((q+R+DQ)\operatorname{polylog}(N+q+H+R+Q)),
\qquad
S_{\rm port}\le DH(B+1)+O(D\log(N+q+H+R+Q)).
$$

These are charged **FLMV §2.1 indexed-machine upper bounds**, not measured native traces: each tagged lookup constructs a binary work-tape address, jumps, and erases the index; work-space counts the highest position visited, not nonblank cells. Use one work tape for all dynamic-depth banks, not an input-dependent number of tapes. For D=O(loglog N), polynomial q and H<=N^{1/2+o(1)}, port space is N^{1/2+o(1)}. This conditional exponent does **not** establish the strict complete s' target without charging source/template authentication, policy acquisition and failed policies, guest stacks, simultaneous caches/ancestor buffers, output, conversion, replay, and join work.

An actual wrapper must instead budget at least

$$
T_{\rm wrapper}\le V(N)+T_{\rm policy}+T_{\rm join}+T_{\rm output}
+O((q+R+D\sum_j T_A(L_j))\operatorname{polylog}N)
$$

only **if** uniform source-authenticated children, correct AND/OR composition and guest input-bit simulation have been separately proved. The fixed-graph descendants here have essentially the same encoded length, so they are **not recursively contracting**. No native R_mix341 rule, branch discharge, proof weight or semantic oracle is added.

## Computational checks and prior-work reconciliation

Python producer seed 202611060036: three graphs (K4, cube, Petersen), depth-three nested tests, 237 snapshot comparisons, 6,952 exact clause comparisons, 237 charge-parity controls, 48 K4/cube brute-force SAT controls, 904 edit macros, 4,534 tag-access/index-write/index-erase macro triples. Conservative physical bank-capacity bounds: 180/360/450 bits. Invalid graph, out-of-range edit, epoch overflow and corrupted-sign controls rejected. Independent Node.js referee: **2,127 assertions**, 507 cumulative visits, 11,337 conceptual indexed reads, 3,152 writes, 14,872 clause comparisons. Host operation proxies are **not physical FLMV instruction measurements**. A separately published executable compact checker reproduces the lifetime failure and banked source equality.

LSPV-4/427 already established the difference between live memory and physical high-water; /433 corrected mismatched parent/portfolio input baselines; LSPV-2/437 supplied sequential epoch tags; classic initializable arrays (Hagerup/Kammer 2017) and persistent data structures (Driscoll/Sarnak/Sleator/Tarjan 1989) precede this approach. No novel general data structure or unconditional complexity lower bound is claimed.

## Actual source and research audit

Governing handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3; live issue #3 through LSPV-1/438 and LSPV-2/437; LSPV-2/437 blob 2033e9d and LSPV-4/433 blob 94a8d72. Actual GROKPROOF/2026-11-06_0515_PROGRESS.md blob 93f9202 and research/agents/claude/world-ledger/README.md blob de75a37 read. konard/p-vs-np/proofs/complexity/README.md at head ecedd2b specifies a **different one-tape** machine, without an FLMV conversion; blkph0x/p-vs-np-proof-research/CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md at head 7dedc73 explicitly gives a sound incomplete semantic merge. CNFgen's actual tseitin.py at master 24e633b, FRAT-XOR README, peitl/short-proof README and openai/math ExecCNFNodeSearchCosts.lean at 4eaee87 were checked as source/proof/cost controls, not universal theorems. Original FLMV author PDF §2.1 **visually inspected** for work-tape indexing and erasure. Direct Google-branded search unavailable; indexed web and authenticated GitHub searches used.

Root main.tex blob d5ba222 yielded zero readable bytes from fetch_file and raw fallback failed, so no safe root-owner edit was possible. All five existing task titles, schedules and enabled states retained, with LSPV-2/4 Route A and LSPV-1/3/5 Route B. Shared branching AND/OR DAG, context scope, paid union and original fixed R_mix341 grammar/weights remain intact.

**Advance:** naive single-bank nested lifetime falsified; per-depth paid stack repair proved for authenticated common-graph Tseitin edits. **OPEN:** fully charged recursively iterable all-input same-machine SAT transformation at t'<=max(11/10,3/5+t/2) and s'<=max(1/2,s/2), plus separate same-R B3. P versus NP OPEN.

### Primary references

1. Fortnow, Lipton, van Melkebeek, Viglas. *Time-Space Lower Bounds for Satisfiability*. JACM 52(6), 2005, 835–865, doi:10.1145/1101821.1101822.
2. Urquhart. *Hard Examples for Resolution*. JACM 34(1), 1987, 209–219.
3. Ben-Sasson, Wigderson. *Short Proofs Are Narrow*. JACM 48(2), 2001, 149–169.
4. Hagerup, Kammer. *On-the-Fly Array Initialization in Less Space*. ISAAC 2017.
5. Driscoll, Sarnak, Sleator, Tarjan. *Making Data Structures Persistent*. JCSS 38(1), 1989, 86–124.
