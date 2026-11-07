# LSPV-2/457: OR-folded moving-frontier SAT compiler
**2026-11-06 18:14 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Precise proposed repair, falsifiers, and iteration
**Initial hypothesis.** LSPV-2/456 enumerated every incoming/outgoing boundary pair $(a,b)$, costing $h2^{2w}$ SAT calls. It should be possible to encode the ENTIRE prior frontier truth table as ordinary CNF clauses and ask the unchanged guest SAT decider one question per outgoing $b$, costing only $h2^w$ calls, without a free semantic operation.

Falsifiers checked: (F1) a single forbidden-assignment clause accidentally excludes the *wrong* predecessor; (F2) an outgoing-$b$ SAT query fails to implement the existential OR over predecessors; (F3) the appended table clauses, encoding bits or guest work exceed child or peak-space budgets; (F4) incompatible branch assumptions or a malformed suffix produce false acceptance. Finite independent controls refuted F1/F2; direct bit-cost accounting refutes F3 under the stated promise; F4 requires complete source validation and proper context-scoped message keys. Early semantic answers never authorize skipping validation of a remaining source suffix.

**Evidence changed the approach.** In LSPV-4/454, Gray-code pin gadgets reduce materialization cost for pair enumeration, but still require up to $2^{2w}$ guest calls. The revised construction inserts a CNF representation of the whole valid predecessor set into ONE guest per outgoing $b$. It exploits the guest SAT existential quantifier and changes no historical inference rules.

## Exact restricted theorem, including original-source grammar
Let a fully authenticated signed proper-width-three source be encoded as
$$
F=\bigwedge_{i=1}^h F_i(X_i,Z_{i-1},Z_i),\qquad Z_0=Z_h=\varnothing.
$$
All private $X_i$ and interface sets $Z_j$ are pairwise disjoint. Clauses appear contiguously in blocks, every clause has exactly three distinct signed variable occurrences, and a leading, self-delimiting authenticated header gives canonical disjoint identifier ranges, lengths and expected block positions. A grammar verifier can stream-check every literal, ID, delimiter and end marker with $N^{1+o(1)}$ time and $N^{o(1)}$ scratch. This is an explicit restricted *sublanguage*. Any ordinary valid CNF outside this structural promise is NOT thereby malformed.

Assume
$$
h\le N^{1/2+o(1)},\quad L_i\le N^{1/2+o(1)},\quad
w=\max_i|Z_i|\le\frac1{10}\log_2N+o(\log N),
$$
where $L_i$ includes all paid block fields and $N$ is the total encoded binary input size.

Let $A$ be ANY fixed uniform total correct polynomial-time **general binary-encoded CNF-SAT** decider with indexed random-access same-machine time $L^{t+o(1)}$ and writable space $L^{s+o(1)}$, including its malformed-input parser. There is an explicitly constructed wrapper deciding both SAT and UNSAT on the above special source grammar with
$$
\boxed{t'\le\max\left(\frac{11}{10},\frac35+\frac t2\right),\qquad
s'\le\max\left(\frac12,\frac s2\right).}
$$
This theorem is *restricted*, not the universal all-input, recursively applicable transformation [P2-A2].

## Construction and proof
Maintain the exact prefix-extension truth table $M_{i-1}:\{0,1\}^{Z_{i-1}}\to\{0,1\}$. For any assignment $a$ of incoming variables, define the blocking clause
$$
D_a=\bigvee_{j=1}^{|Z_{i-1}|}
\begin{cases}z_j,&a_j=0,\\ \neg z_j,&a_j=1.\end{cases}
$$
It is false EXACTLY on $a$. (When $Z_{i-1}=\varnothing$ and its only message bit is false, $D_\varnothing$ is the empty clause, valid in general CNF.)

For each outgoing assignment $b$, physically materialize and pay for the ordinary CNF
$$
G_{i,b}:=F_i\ \land\ \bigwedge_{a:M_{i-1}(a)=0}D_a
\ \land\ \bigwedge_{z_j\in Z_i}(z_j=b_j).
$$
Invoke the unchanged guest $A$ once to set $M_i(b):=\operatorname{SAT}(G_{i,b})$. The fixed outgoing unit clauses are ordinary CNF, not a new R_mix341 pin/discharge rule. If strict-three guest syntax is desired, use a separately charged equisatisfiable chain/gadget encoding and prove its size; the theorem as stated uses the GENERAL CNF guest.

For every complete assignment $a$, the blocker conjunction holds iff $M_{i-1}(a)=1$. Therefore
$$
\operatorname{SAT}(G_{i,b})\iff
\exists a\,[M_{i-1}(a)\land\operatorname{SAT}(F_i|_{a,b})].
$$
By induction, $M_i(b)$ means the first $i$ source blocks have a single compatible satisfying extension with outgoing boundary $b$. This encodes OR over predecessor alternatives and AND with the current block. It does not claim an UNSAT branch has been discharged through historical R_mix341. The final $M_h(\varnothing)$ is exactly SAT($F$). All source bytes, including any unprocessed suffix, must be authenticated before classification.

## Full asymptotic resource ledger (restricted grammar)
At most
$$
q=\sum_i 2^{|Z_i|}\le h2^w\le N^{3/5+o(1)}
$$
real guest invocations occur; old LSPV-2/456 costed up to $h2^{2w}$ calls and therefore permitted only $w\le(\log_2N)/20$. The revised wrapper permits $w\le(\log_2N)/10$, doubling the coefficient.

For each child, at most $2^w$ blocking clauses, each of width $w$ and signed identifiers of $O(\log N)$ bits, plus $w$ outgoing units, give an *explicit evidence/guest-input* bound
$$
|G_{i,b}|\le L_i+O(2^w w\log N+\operatorname{polylog}N)
\le N^{1/2+o(1)}.
$$
Full source authentication/reading/indexing takes $N^{1+o(1)}$ time. Reconstructing and encoding all guests takes
$$
O\left(h2^w\left(L_{\max}+2^ww\log N\right)\operatorname{polylog}N\right)
\le N^{11/10+o(1)}.
$$
All guest work is bounded by $q\cdot(N^{1/2+o(1)})^t=N^{3/5+t/2+o(1)}$ steps. The loop explicitly resets or overwrites guest scratch, pays index/head/return/serialization costs and stores only the current/next message vectors, one input block, one materialized child, the guest's simultaneous work/index tapes, and counters. Hence high-water writable space is
$$
N^{\max(1/2,s/2)+o(1)}.
$$
The local phase exponent $\rho\le 1/2$ includes allocating and freeing the child and table. In the envelope $s'\le\max(\rho,\eta,\lambda,\lambda s)$ we have $\lambda=1/2$, $\eta\le1/2$, $\rho\le1/2$. No source-scale array or uncharged virtual port is allowed. All actual construction, failed-query and guest time counts remain physical machine work. Distinct native R_mix341 refutation nodes and certificates: *not applicable*, because this is a SAT decision construction rather than a proof certificate. Weighted logical proof work, critical-path span and realizable machine runtime must not be conflated.

## Published-hard-family and shortcut control ledger
**Family:** odd-charge Tseitin on simple connected cubic expander $G_H$. Exact original proper 3-CNF consists of $4H$ clauses on $3H/2$ edge variables. For incident edges $a<b<c$, charge $\chi_v$ and $\ell_0(x)=x$, $\ell_1(x)=\neg x$, its four original signed clauses are
$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)
\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),
\quad p,q\in\{0,1\}.
$$
Explicit binary source size is $N=\Theta(H\log H)$. Odd total charge certifies UNSAT. Ben-Sasson and Wigderson (JACM 2001, Definition 4.1, Theorem 4.4, Corollary 4.5, building on Urquhart 1987) give $2^{\Omega(H)}$ **ordinary shared-DAG Resolution** size for suitable connected cubic expanders, not full R_mix341 or machine time. The known direct GF(2) sum of all vertex charges efficiently decides the same instances, and can yield short semantic mixed derivations. A source-packet path ordering with small original blocks has frontier $\Omega(H)$; the new logarithmic-width promise still fails on expander packet layouts. No lower-bound-preserving general R simulation follows. Related published controls: Haken ordinary Resolution PHP, Cook Extended Resolution, and Braun Res(XOR) wide bit-PHP, with their respective encoding/transfer cautions as in [P2-F1]–[P2-F4].

## Independently executed finite controls (COMPUTATIONAL only)
The Python producer and separate JavaScript bit-mask verifier both constructed original signed proper 3-CNF path instances, checked old pairwise joins vs new single-call-per-outgoing OR folding, and compared with complete parent brute force. Python: **40 sources** (20 SAT/20 UNSAT), **543 assertions**, **296 folded calls** vs **704 available pairwise calls**. JavaScript: **20 sources** (10 SAT/10 UNSAT), **273 assertions**, **148 folded calls** vs **352 available pairwise calls**. Adversarial blocker-sign test and exhaustive blocker truth tables pass. An additional proper signed K4 even/odd-charge Tseitin test passes. At first the JavaScript test found a genuine empty-boundary indexing error in the *test harness* (key '' vs '0'); it was repaired and the final published code was independently executed with PASS. This is an engineering regression, not a counterexample to the theorem. Git blob SHA for exactly executed published JS: `87c1d59280f2d585089c336ca043e54a33f4c86c`. The host tests use brute force and source arrays, not FLMV native-machine timing or general 3-CNF lower-bound certificates.

## IDEA -> SEARCH -> ITERATE record / external trust
Read both root trackers before work: `proof1.txt` SHA `0c24df268207e9436d51519ec168a984ab10ae3e`; `proof2.txt` SHA `191187a85b168561d681a2326dfb58bbc20522e6`. Relevant IDs: **[P2-A2], [P2-A4], [P2-F2], [P1-S3], [P1-01], [P1-03], [P1-04]**. Read current issue #3; governing Nov 2 handoff; AGENTS.md, CODEX.md, project skill; LSPV-2/456, LSPV-4/453 and /454, LSPV-3/462, Grok REWIRE and 2026-11-06 progress, Claude ONETAPE and WORLD ledger. The exact historical mixed R_mix341 remains untouched.

Primary research: E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow—Resolution Made Simple*, JACM 48(2), 2001, original PDF https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf, actual Definitions 4.1–4.3, Theorem 4.4 and Corollary 4.5 inspected (page image inspected); FLMV, JACM 52(6), 2005, DOI 10.1145/1101821.1101822, random-access machine assumptions required. Source-oriented GitHub files actually read: `konard/p-vs-np/proofs/complexity/README.md` blob `7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3` (one-tape model, no FLMV transfer); `blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md` blob `4aba9d94405402c4dc122c7ebe2ef3665da17f5a` (bounded-visible-variable projection, different classification); `meelgroup/frat-xor/README.md` blob `38a137bca4d4ab6443703d4c31fba5783021c581` (authenticated external checker pipeline, not native R_mix341); `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` (raw research, not a SAT theorem). Queries included “SAT dynamic programming path decomposition”, “existential projection boundary SAT”, “Tseitin Resolution theorem 4.4” and “FLMV same-machine time space”; web search used, direct Google-branded search not available. No independent external builds or native FLMV trace execution claimed.

## Tracker status, collaboration, and exact remaining gap
Material **restricted-evidence** improvement only: [P2-A4] and [P1-S3] should record the new $w\le (\log_2N)/10$ OR-folded source-grammar construction. [P2-A2] and [P1-01] remain OPEN. Preserve two Route A (LSPV-2, LSPV-4) and three Route B (LSPV-1, LSPV-3, LSPV-5) role ownership. No task, R_mix341 inference grammar/weights, or root main.tex changes.

**Actual advance:** a formally justified, fully materialized and resource-charged restricted compiler doubles the permitted frontier-width coefficient by moving predecessor OR into a single SAT child per successor context. **Verification:** finite two-language independent checks passed, not native complexity verification. **Publication:** report, executed independent JS and results/handoff to be verified by full readback. **Remaining gap:** effective solver-dependent interface acquisition for arbitrary SAT inputs, malformed-aware all-input recursive iteration on the FLMV machine, and the Route B fixed-system B3 and mixed-work lower bound. **P versus NP OPEN.**
