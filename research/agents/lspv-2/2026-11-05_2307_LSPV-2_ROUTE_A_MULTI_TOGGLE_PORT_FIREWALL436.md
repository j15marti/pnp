# LSPV-2/436 | Exact multi-toggle Tseitin child-port firewall
**November 5, 2026, 23:07 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL. Universal FLMV contraction and P vs NP OPEN.**

## Hypothesis, falsifiers, correction
The earlier LSPV-4/432 *one-toggle* source-authenticated Tseitin child port does not automatically extend to arbitrary-length **unsorted** vertex-toggle streams with polylogarithmic bit access. Four falsifiers: (1) repeated toggles may fail to cancel across the four signed clauses; (2) an unqueried update word may not affect a requested child bit; (3) sorted-list binary search may be used without paying to authenticate sortedness; (4) a child-bit query lower bound might be confused with SAT decision hardness. (1) and (2) fail for the exact stipulated source, (3) requires an explicit charged scan, (4) prohibits universal-hardness conclusions.

## Published-hard family and exact strict 3-CNF encoding
For a connected cubic graph $G=(V,E)$ with $H$ vertices, $M=3H/2$ edges, and sorted incident edge IDs $a_v<b_v<c_v$, take the **standard Tseitin parity clauses**:
$$
C_{v,p,q}(chi)=ell_p(x_{a_v})lorell_q(x_{b_v})lorell_{poplus qoplus1opluschi_v}(x_{c_v}),
quad(p,q)in{0,1}^2,qquad ell_0(x)=x, ell_1(x)=
eg x.
$$
There are $4H$ proper signed three-clauses, $M$ variables, and $N_0=Theta(Hlog H)$ encoded bits. The historical LSPV-2/435 serialization (8-bit magic, unary $H,M$, $2Mw$ endpoint bits, $12H(w+1)$ signed-literal bits, terminal 00) gives
$$
N_0=8+(H+1)+(M+1)+2Mw+12H(w+1)+2.
$$
Odd charge is UNSAT by XOR of vertex equations. On *suitable growing cubic expander graphs* with odd charge, Urquhart (1987) and Ben-Sasson/Wigderson (2001) establish $2^{Omega(H)}$ **ordinary shared-DAG Resolution** refutation-size lower bounds. This is not hardness for arbitrary algorithms, extended Resolution, GF(2) or all legal $R_{mathrm{mix341}}$ proofs. The earlier $4H-1$-node mixed GF(2)/AND3 derivation is a mandatory short-proof control. K4, cube and Petersen below are finite controls, not a certified expanding sequence.

## Theorem 436.1: exact virtual source, with repeats
Take authenticated base charge $bin{0,1}^H$ and arbitrary valid vertex-ID edits $u_1,ldots,u_r$ (repeated IDs legal). Define $chi_v=b_voplusigoplus_{j=1}^r[u_j=v]$. **Every bit** of the generated child 3-CNF agrees with its original base bit except the third-literal sign in the four rows at vertex $v$, which flips by that edit-incidence parity. Proof: the charge appears in exactly that signed position of each canonical row, as an XOR summand. Repeated flips cancel. This is an exact-original-source identity, not only equisatisfiability.

## Theorem 436.2: unsorted edit-bit access is expensive, though decision label is cheap
Let $H=2^wge4$ so every $w$-bit edit word is valid, let $v$ be a fixed vertex, and request one of its four charge-sensitive literal-sign bits. For a read-only **unsorted** $r$-word edit stream, any deterministic correct exact-bit port *without a prepaid index or summary* must read at least one source bit in **every** update word on the stream $u_j=z
e v$. If word $j$ is never sampled, replace its ID by $v$: the queried bits remain equal, the required child source sign flips, and deterministic identical execution would produce a contradiction. Thus worst-case **source-bit query complexity** is at least $r$ for this port. A scan uses $O(r,mathrm{polylog}N)$ native bit time in the indexed model.

Yet, for a connected $G$ the SAT status of that generated child is
$$
operatorname{SAT}(F_{G,chi})iff
left(igoplus_v b_vight)oplus(rmod2)=0.
$$
After base and grammar authentication, the label depends only on $r$, not on edit IDs. Therefore exact virtual-child input access can be asymptotically harder than deciding this promised child's label. This is **not** a lower bound against any general SAT decider or all-input FLMV transformation.

## Theorem 436.3: sorted, authenticated repair
For a validated nondecreasing list of IDs, child-bit sign parity is $(mathrm{upper_bound}(v)-mathrm{lower_bound}(v))mod2$. Two binary searches use $O(log(r+1))$ indexed ID reads, with $O(log N)$ densely addressed physical work/index space and $O(log(r+1)mathrm{polylog}N)$ native bit time. An untrusted list must first be validated at $Omega(r)$ update-word probes and charged source/index-head costs. Sorting is not silently assumed. A fully charged precomputed index is another legal option.

For $q$ *explicitly recorded* edit lists of lengths $r_j$, the original-source length includes $sum_j r_jlog H$ bits. A once-only sorted-list validation scans those source bits; $Q$ subsequent exact-port reads then cost $O(Qlog(r_{max}+1)mathrm{polylog}N)$ under a **separately established** polylog-local graph/template generator. Guest A executions, their own read requests, failed policies, output, cache retention and physical work-tape high-water are additional. The $qH$ lower bound of LSPV-4/432 concerned **independent fully supplied original children**; it cannot be applied to authenticated correlated virtual descendants.

## Verification and original-source controls
The Python producer passed **483,910 assertions** on 421 K4, 665 cube and 1,191 Petersen edit streams, including duplicates and lists through length 17. Every generated child literal was checked against an independently regenerated exact three-CNF. The separately implemented Node.js verifier passed **212,595 assertions**, with independent exact literal checks and exhaustive K4 SAT/UNSAT charge controls. Five malformed/invalid-ID or invalid-sorting controls were rejected; corrupt records are not relabeled UNSAT. Host tests do **not** measure FLMV native machine time or peak space. The complete executed originals, full 11-KB mathematical report, raw JSON and SHA-256 manifest are preserved in the run's reproducibility archive.

## Corpus, literature, duplication
Authenticated reads: five-role handoff November 2 at commit `4e29ed7`, issue #3 through LSPV-5/379, LSPV-2/435 blob `0366a09d`, LSPV-4/432 blob `208e9bd3`, actual Grok `GROKPROOF/2026-11-06_0515_PROGRESS.md` and Claude world ledger. Cross-track `research/agents/cross-track/2026-10-17_0553_CROSS-TRACK_GAUGEORBIT35_SHORT.md` had already established charge orbits and ordinary Resolution gauge invariance; none is claimed novel. New work specifically separates an unsorted multi-edit **bit port** from the much easier charge-parity **label** and proves the sorted repair including its authentication bill.

External actual files: `konard/p-vs-np/proofs/complexity/README.md` (`7ee9a11e`), `scripts/proof_status.json` (`93b77ed3`) (distinct finite one-tape model); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (`18d693ea`) and `CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md` (`b37da20a`) (sound but incomplete certified mergers); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` (`4bb5fd19`); `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` (`1ced21f4`, a special costed program, not universal compiler). General web searches reviewed FLMV, Tseitin Resolution, and Reingold; direct Google-branded search was not available. **Original FLMV PDF §2.1 page 4 visually inspected:** an indexed jump clears the index tape and work space is the largest visited work-tape coordinate. These physical obligations are retained, not replaced by host memory measurements.

Proof branching DAG OR/AND, contextual assumptions, fixed mixed rules/weights, B1/B2/B3 and the two Route A/three Route B allocation are preserved. No R_mix341 checker was run. Root `main.tex` blob `fb95952d` returned zero readable bytes; it was not overwritten.

**OPEN:** Construct a uniform all-input recursively iterable same-FLMV-machine transformation $AmapstoPhi(A)$ for every polynomial SAT decider, satisfying $t'lemax{11/10,3/5+t/2}$ and $s'lemax{1/2,s/2}$, with effective source-authenticated child generation, join, same-machine time and physical peak. Same-R B3 and P vs NP OPEN.

### Primary references
1. Urquhart, *Hard examples for resolution*, JACM 34 (1987), 209–219, DOI 10.1145/7531.8928.
2. Ben-Sasson and Wigderson, *Short proofs are narrow*, JACM 48 (2001), 149–169, DOI 10.1145/375827.375835.
3. Fortnow, Lipton, van Melkebeek and Viglas, *Time-space lower bounds for satisfiability*, JACM 52 (2005), 835–865, DOI 10.1145/1101821.1101822.
