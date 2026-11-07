# LSPV-4/471: Quantified counted-WORK INDEX barrier
**2026-11-07 08:11 PST | Route A | PROVED/RESTRICTED, COMPUTATIONAL | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** The simultaneously live INDEX-payload obstruction in LSPV-4/470 can be turned into a same-decider conditional counterexample to *both* required Route A exponents, but only for the particular faithful counted-WORK canonical-radix simulator, not for all algorithms.

**Predeclared falsifiers.** (F1) The INDEX-pattern generator actually requires guest counted WORK space comparable to payload length; (F2) canonical sharing yields fewer than $2^r-1$ simultaneously live distinct height-$\log_2r$ nodes; (F3) the wrapper fails SAT/UNSAT/malformed correctness or fixed uniformity; (F4) the argument inadvertently excludes the legal native uncharged INDEX tape, static code reduction or smaller-guest alternatives.

**Current corpus.** Both complete root trackers read; exact nodes [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-B1], [P2-B2]. LSPV-2/469 (report SHA `32f118a3a6999f414e0371a83bc8c413898d861b`) and /470 (`b1567c0427155e68fe82ffa8fb45a6fcfb94fe8b`), LSPV-4/469 and /470 (`12a09e9a9fe85c241a412d36240ad8a11ab9ea5a`) were read. Also reviewed the November 2 five-role handoff (`c3889a3e514ddbd747150dcb68607013a3b2d154`), AGENTS.md, CODEX.md, pnp-research SKILL.md, latest issue #3, GROKPROOF/2026-11-07_1220_PROGRESS.md (`2c450bb3084c8a2065243305168d269442ace430`), and Claude world ledger (`79e4d4e7e0e3edff3aba8610852c45534bdde128`).

**Primary sources.** FLMV [1], §2.1, author PDF page 4 visually inspected: INDEX tape contents are *not* counted as non-index WORK space; native indexed jumps erase INDEX contents. Ben-Sasson/Wigderson [2] supplies ordinary Resolution controls, not an all-machine lower bound. Source files read with exact blob identifiers: konard/p-vs-np/proofs/complexity/README.md (`7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3`, different finite one-tape model); blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md (`b30515cced93d8911a6415555ee9ec1444502d93`, missing universal plan acquisition); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (`4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`); meelgroup/frat-xor/format.md (`986a21aa92b62f844ef1fce852193142c41b2b1f`); openai/math/README.md (`cc5b0a03bca6c742f045d683b6647a6f44ef2cae`); berkeley-abc/abc/README.md (`88a9d1a316dd9751acade746de315fd1e6e6c362`). Public web searches performed; a separately attributable Google-branded search was unavailable. None proves the missing transfer.

## Theorem 471.1 (conditional, restricted architecture)

**Assume**, without claiming, that a fixed uniform total correct indexed-machine SAT/UNSAT/malformed decider $A$ exists, with worst-case time $N^{t+o(1)}$ and measured non-index WORK high-water $N^{s+o(1)}$, for finite $t,s\ge0$. Choose a fixed power-of-two integer $d>\max(4,t,s)$. Define another fixed total decider $D_d$ on every binary input $x$ of length $N$: calculate $r(N)$, the largest power of two at most $d\lfloor\log_2N\rfloor$ (handle small $N$ by a constant convention). On a dedicated guest INDEX tape sequentially write every $r$-bit word, least-significant bit first, in increasing order. Do not make any indexed WORK jump on that tape pair. Retain the entire INDEX payload. Then execute $A(x)$ with disjoint tape pairs and return precisely its ternary classification.

A binary counter and block serializer on ordinary guest WORK use $O(r)$ high-water cells and at most $O(r^2 2^r)$ time. Full source length acquisition, parsing and eventual $A$ execution are charged. Thus
$$
T_{D_d}(N)=O(N^d\operatorname{polylog}N+T_A(N)),\qquad
S_{D_d}(N)=O(N^{s+o(1)}+\log N).
$$
On infinitely many lengths $N_j=2^{2^j}$, with $d$ a power of two, $r=d\log_2N_j$ exactly. The live INDEX payload length is $L=r2^r=rN_j^d$, and the guest must perform at least $L$ sequential writes. Consequently the worst-case time exponent of $D_d$ is exactly $d$ up to $o(1)$; the guest's counted WORK exponent is at most $s$. The prologue changes no SAT, UNSAT or malformed answer.

Now restrict the purported transformation to one architecture: faithfully execute the full $D_d$ prologue and represent the entire live INDEX payload as canonical binary radix-DAG nodes, with *one physical record per distinct nonzero node* held on a fixed finite number of **counted host WORK tapes**. This is LSPV-4/469's literal counted-WORK representation, not LSPV-2/469's native shifted-INDEX alternative.

Because $r=2^a$, the $2^r$ aligned $r$-bit blocks form all words. Each nonzero block is a different canonical node at height $a$; at least $2^r-1$ nodes remain **simultaneously live** under the payload root. Reference counting and physical free-list recycling cannot remove live nodes. Fixed-alphabet record allocation on finitely many host WORK tapes therefore forces maximum counted address $\Omega(2^r)$ and at least that many record-construction writes.

At $N_j$, this gives
$$
S_{\mathrm{host}}(N_j)=\Omega(N_j^d),\quad
T_{\mathrm{host}}(N_j)=\Omega(N_j^d).
$$
The intended Route A bounds for the SAME guest $D_d$ demand
$$
s'\le\max(1/2,s/2)<d,\qquad
t'\le\max(11/10,3/5+d/2)=3/5+d/2<d.
$$
Hence this **specified faithful counted-WORK radix architecture** violates both targets under the conditional premise that $A$ exists. It is NOT a counterexample to an unrestricted effective transformation and NOT a P-versus-NP proof. Native uncharged INDEX storage (LSPV-2/469), code-aware removal of the useless prologue, smaller children, direct SAT tactics and other online/replay representations remain available.

**Increment beyond LSPV-4/470:** the original live-node result is reused, not rediscovered. Here it is placed into one uniform correct conditional SAT-decider family with arbitrary unknown exponent $s$ and a simultaneous, strict numerical violation of both Route A exponents. LSPV-2/470's delayed-trace counterexample is a separate, complementary trace-first architecture control.

## Verification and full-cost audit

Standalone Python and independently authored JavaScript finite checkers agree on the six $(N,d)$ parameter cases $(4,2),(8,2),(16,2),(4,4),(8,4),(16,4)$. Python explicitly hash-conses the radix subtree nodes for $r\le8$; JavaScript independently enumerates $r$-bit block strings. At $r=16$, only the exact combinatorial count is checked rather than materializing a million-bit DAG. Python **25** checks and JavaScript **21** checks passed, zero failures. Original signed K4 Tseitin strict 3-CNF control: 6 edge variables, 16 ternary clauses, even charges 8 models, odd charges 0; malformed repeated-variable control rejected. These finite results do **not** certify asymptotic hardness or native FLMV instruction costs.

**Resource ledger:** Original read-only input length/heads and index operations: $O(N\operatorname{polylog}N)$; guest prologue writes $L=r2^r$ uncharged-INDEX bits in $O(r^2 2^r)$ time with $O(r)$ counted WORK counter; eventual guest $A$ time/space charged; source label and output charged; restricted host canonical representation needs $\Omega(2^r)$ *simultaneous* physical WORK records, their IDs and pointers, $\Omega(2^r)$ construction writes, plus dynamic retention/GC. The witness does not run SAT-child decomposition, failed policy search or proof checking; any real full compiler still must charge those phases, child materialization and $s'\le\max(\rho,\eta,\lambda,\lambda s)$. No free algebraic oracle, snapshot, or impossible time-to-space transfer assumed.

**Hard-family ledger:** For an odd-charge connected cubic expander on $H$ vertices, the direct signed Tseitin 3-CNF has $3H/2$ variables, $4H$ original proper ternary clauses, bit length $\Theta(H\log H)$ under binary IDs; UNSAT by odd charge; exponential **ordinary shared-DAG Resolution** proof size for suitable expanders [2]. GF(2) Gaussian elimination is a polynomial computational shortcut; there is no asserted $R_{\rm mix341}$ or all-algorithm lower bound. Haken PHP and Cook extended Resolution remain separate mandatory controls. The INDEX witness is solely an implementation architecture falsifier, not a new hard SAT family.

**Tracker decision:** Material restricted quantified evidence for [P2-A4] only; [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-B1], [P2-B2] OPEN. Historical $R_{\rm mix341}$ grammar and weights, five identities/schedules and 2A/3B allocation unchanged. No root main.tex edit absent complete verified contents.

**Actual advance:** Quantified dual-resource obstruction for one counted-WORK simulator architecture. **Verification:** restricted symbolic proof plus independent finite checks. **Remaining gap:** fully charged native-index or code-aware recursively iterable ALL-INPUT SAT contraction. **P versus NP OPEN.**

### References
[1] Fortnow L, Lipton RJ, van Melkebeek D, Viglas A. *Time-Space Lower Bounds for Satisfiability.* JACM 52(6), 2005, §2.1. https://lance.fortnow.com/papers/files/tst.pdf
[2] Ben-Sasson E, Wigderson A. *Short Proofs Are Narrow: Resolution Made Simple.* JACM 48(2), 2001. DOI 10.1145/375827.375835.
