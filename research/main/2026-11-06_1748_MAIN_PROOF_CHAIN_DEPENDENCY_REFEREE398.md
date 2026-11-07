# LSPV-5 REFEREE398: live proof-chain dependency firewall and exact random-3-CNF baseline

**2026-11-06 17:48 PST, America/Los_Angeles. Route B red team.**

**Status:** **KNOWN THEOREM** for the Chvatal-Szemeredi ordinary-Resolution family; **PROVED/EXACT** for the ledger consistency theorem; **COMPUTATIONAL** for the executable audit and hostile controls; the historical $R_{\mathrm{mix341}}$ grammar, full-mixed superpolynomial minimum, noncircular B3, and P versus NP remain **OPEN**.

## IDEA and falsifiers

The initial repair hypothesis was that the new root proof1.txt and proof2.txt could be made into a shared dependency firewall: preserve restricted results, expose every load-bearing OPEN arrow, and reject a terminal $P=NP$ or $P\ne NP$ claim whenever any necessary premise remains unresolved.

Falsifiers were:

1. a terminal chain closes while depending on OPEN, CONDITIONAL, merely COMPUTATIONAL, or restricted evidence;
2. Route B omits either all-native-rule transfer or same-calculus B3;
3. a Resolution/Res(XOR) lower bound is presented as arbitrary-machine hardness, or Cook ER/Tseitin GF(2) shortcuts disappear;
4. concurrent tracker creation is overwritten rather than merged.

The current head changed before this run began: proof1.txt was added at commit ebba137e69525087d380feab5f6f58d86b5567b7, and proof2.txt at d33904385357f2cc73daef8b6f4f8bc08190a991. They were therefore audited as current peer work and preserved.

## SEARCH and corpus reconciliation

Read completely or through authenticated commit/file responses:

- proof1.txt blob db5c3a197f9588ab43c6191eaecff94231b0a891;
- proof2.txt blob 6eca309b568245187c5c7b7bc619ac6871eb9859;
- the full main.tex blob d48dd0fbc8d23d66d9f903e08194a14df78fee9f;
- AGENTS.md, CODEX.md, the complete project research skill and its red-team/protocol references;
- governing five-role handoff at historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8;
- current issue #3;
- LSPV-1/459 and /461, LSPV-2/456, LSPV-3/462, LSPV-4/454, REFEREE397;
- actual Grok progress blob a20fb8b3640d7574faf238a4a83a021bb0984808;
- actual Claude world-ledger report;
- required konard/p-vs-np and blkph0x/p-vs-np-proof-research heads and READMEs;
- FRAT-XOR/XLRUP, CakeLPR, short-proof, CNFgen, and OpenAI math artifacts recorded in the source log.

Primary theorem statements were checked from Chvatal-Szemeredi (1988), Haken (1985), Cook (1976), Cook-Reckhow (1979), Urquhart (1987), Ben-Sasson-Wigderson (2001), de Rezende-Nordstrom-Risse-Sokolov (2025), and Braun v2 (2026).

Direct Google-branded search was unavailable; general indexed web search was used. The workspace did not contain a repository checkout, so the mandated local preflight.py invocation could not run. Authenticated remote tree/blob/issue/commit reads supplied the preflight instead. The authoritative historical $R_{\mathrm{mix341}}$ byte checker was not found or executed.

## ITERATE I: a tracker status defect and its minimal repair

The first executable audit failed because node P1-S6 used the status FALSIFICATION CONTROL, absent from the tracker’s own allowed vocabulary. The underlying claim is the elementary quantifier fact that a fast algorithm on one family does not prove an all-input polynomial bound. The minimal repair is:

P1-S6 — KNOWN THEOREM / FALSIFICATION CONTROL.

No algorithmic node was promoted. In particular P1-01, P1-03, and P1-04 remain OPEN.

## ITERATE II: established native strict-3-CNF family

### Exact family

Fix $k=3$ and a positive integer $c$ satisfying $c2^{-3}\ge0.7$; $c=6$ is an explicit choice. Let $X=\{x_1,\ldots,x_n\}$. Draw $m=cn$ source clauses independently and uniformly from the

$$
\binom n3 2^3
$$

ordinary clauses of size three: three distinct variables, one polarity choice for each. The input is an indexed family, so repeated clauses are permitted. Every source clause is already proper 3-CNF; no width reduction is needed. With binary variable identifiers, explicit encoded size is $N=\Theta(n\log n)$ for fixed $c$.

### Published theorem and exact scope

Chvatal and Szemeredi, Section 2, prove that for every such fixed $c,k$ there is $\epsilon>0$ such that with probability tending to one as $n\to\infty$, the random family is UNSAT and its ordinary Resolution complexity is at least

$$
(1+\epsilon)^n.
$$

Their proof model is a shared-DAG sequence in which each clause is a source or a resolvent of two earlier clauses, ending with the empty clause. The lower bound counts generated clauses. This is published high-probability proof-size hardness in ordinary Resolution.

It is **not**:

- an UNSAT certificate for a particular sampled instance;
- an empirical solver-runtime claim;
- a lower bound for Extended Resolution, Res(XOR), historical $R_{\mathrm{mix341}}$, or arbitrary SAT algorithms;
- a lower-bound-preserving consequence of equisatisfiable encoding (none is needed here because $k=3$).

### Legal shortcut controls

The full minimum $W_R$ must still optimize over every legal historical mixed shortcut: preprocessing, branching, learned clauses, shared reconvergence, extension variables, compact circuits, AND3, GF(2), LOCAL-CONVERT, and source-authenticated lemma reuse. Cook’s short ER treatment of PHP shows why extension shortcuts cannot be ignored. Cubic Tseitin has a direct GF(2) shortcut despite exponential ordinary Resolution lower bounds. FRAT-XOR/XLRUP provides a concrete authenticated XOR-checking model, but it is not evidence that the same bytes or rules belong to historical $R_{\mathrm{mix341}}$.

Therefore the Chvatal-Szemeredi family is a better **starting family** than a bespoke candidate, but it does not close P2-B1. The missing theorem is still a lower-bound-preserving retraction/simulation covering every native mixed rule with correct source scope and encoded-size overhead.

## Ledger dependency theorem

The checker treats the two candidate $P\ne NP$ routes as OR alternatives and each route’s load-bearing premises as an AND set.

- $P=NP$ spine blockers: P1-01, P1-03, P1-04, and conditional P1-05.
- Route A blockers: P2-A2, conditional P2-A3, and P2-A5.
- Route B blockers: P2-D1, conditional P2-D2, P2-B1, P2-B2, P2-B5, P2-C1, and P2-C3.

Thus no terminal chain is closed. P2-B4 remains CONDITIONAL. A conditional implication is not itself a fulfilled premise.

The checker also requires unique node IDs, overall OPEN headers, same-$R$ B3 wording, branch-context scope, Haken/Cook/Tseitin/Res(XOR) controls, and the exact random-3-CNF distribution. Five hostile mutations were all rejected: deleting P2-F8, falsely closing the $P=NP$ header, duplicating P1-01, promoting conditional P2-B4, and erasing the exact random-clause distribution.

## Family/theorem/encoding/known-method/transfer ledger

| Family | Exact encoding and size | Established theorem/model | Strong known shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Chvatal-Szemeredi random 3-CNF | $n$ variables; $cn$ iid ordinary width-3 clauses; $N=\Theta(n\log n)$ | w.h.p. UNSAT and $(1+\epsilon)^n$ ordinary shared-DAG Resolution size | every legal mixed/extension/algebraic/branching proof remains available | all-native-rule $R_{\mathrm{mix341}}$ lower-bound preservation |
| Haken PHP | placement variables, long pigeon rows and binary collisions | exponential ordinary Resolution | Cook polynomial ER proof | precise lower-bound-preserving proper-3-CNF reduction plus full-mixed transfer |
| cubic expander Tseitin | $3h/2$ edge variables, $4h$ proper clauses | exponential ordinary Resolution | linear declared-semantic AND3/GF(2) proof | family fails as a current full-mixed witness; byte grammar still unauthenticated |
| Braun bit-PHP | $(n+1)\ell$ address bits, wide collision clauses, $n=2^\ell$ | $>\exp(n/(32768\ell^2))$ unrestricted DAG Res(XOR), $\ell\ge32$ | extension-variable/ER controls | wide-to-3CNF and Res(XOR)-to-historical-mixed preservation OPEN |
| sparse graph PHP | exact sparse-expander graph regimes | exponential ordinary Resolution | Hall-deficient kernel DP when a small deficient neighborhood exists | hard-regime graph conditions plus 3-CNF and all-mixed preservation |

## Resources

This run constructed no $R_{\mathrm{mix341}}$ refutation and therefore adds no logical inference-node upper or lower bound. The executable ledger audit checked 42 tracker nodes and five hostile controls.

- explicit tracker input: 26,952 bytes;
- raw audit output: 6,397 bytes;
- checker source: 5,186 bytes;
- wall time: 0.0043 s;
- peak RSS: 10,880 KiB;
- parsing/index work: complete scans of both trackers and regex indexing of every node ID;
- construction/search: remote source recovery and theorem authentication, not proof search;
- failed policy retained: first audit rejected the noncanonical P1-S6 status;
- verification: all safeguards true; all hostile mutations rejected;
- caches/retrieval: tool-session remote responses plus local immutable raw JSON;
- output/update costs: separately recorded by final publication/readback manifest;
- simultaneous peak: checker RSS above; remote connector memory is not observable and is not claimed.

No proof-search discovery cost is inserted into $W_R$. Conversely, no machine upper bound is inferred from this ideal ledger audit.

## Revised claim and exact remaining gap

**Actual advance:** the requested live root trackers now have an executable dependency firewall; one status inconsistency was repaired; and proof2.txt now starts from an exact, published, native proper-3-CNF ordinary-Resolution hard family instead of relying only on wider encodings. This narrows the next Route B question to the transfer:

> Does every legal historical $R_{\mathrm{mix341}}$ refutation of the Chvatal-Szemeredi proper-3-CNF family admit a polynomially related ordinary-Resolution object, or is there a legal mixed shortcut?

No such transfer is proved. Historical grammar authentication, P2-B1, P2-B2, and B1/B2/B3 remain OPEN. P versus NP remains OPEN.

