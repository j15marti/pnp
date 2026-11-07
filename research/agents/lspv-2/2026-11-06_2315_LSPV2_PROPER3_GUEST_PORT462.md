# LSPV-2/462 | Proper signed 3-CNF guest port for the postorder OR-folded TREE compiler
**2026-11-06 23:15 PST. Route A. PROVED/RESTRICTED decision equivalence; CONDITIONAL same-machine resources; COMPUTATIONAL finite tests. P versus NP OPEN.**

## IDEA and precise falsifiers
Hypothesis: standard existential clause-splitting gadgets repair the ordinary-CNF-to-strict-proper-3CNF guest mismatch in LSPV-2/461 without changing its child length/call exponents. F1: a unit pin, binary blocker or empty child guard changes SAT; F2: helper names alias source/interface variables; F3: output indexing requires a nonpolylog directory or length exceeds the $N^{1/2+o(1)}$ limit; F4: proper ternary guest is mistakenly treated as a recursively eligible tagged postorder source.

## SEARCH and revisions
Historical project readback: proof1.txt SHA 9273776e5ac0c9a4940b8c3e404d98ed5b205202 and proof2.txt SHA 67fc915249a6f2667b7d85feaedc7853b884ec86; current issue #3; AGENTS.md, CODEX.md, project research skill; LSPV-2/457, /459, /460, /461; LSPV-4/456, /458, /459; peer Grok actual GROKPROOF/2026-11-06_2316_PROGRESS.md and Claude actual research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex. Repositories actually fetched: konard/p-vs-np README 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (only P subset NP in its model); blkph0x/p-vs-np-proof-research README f397a7747eaca82df3d754d0a4b4bab1fe10f814 (scoped promises); MassimoLauria/cnfgen cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (distinct external proof grammar). OpenAI math source remains prior-run evidence only, not fetched afresh. Google-branded search was not available; web search and primary paper PDF were examined. The clause gadgets were already known, see OpenDSA https://opendsa.org/OpenDSA/Books/CS4104/html/SAT_to_threeSAT.html. Do not claim their novelty.

## Theorem 462.A (PROVED/RESTRICTED): proper-ternary normalization
For any source clause $C=\ell_1\vee\cdots\vee\ell_k$ with distinct nonzero underlying variables, replace it with fresh-helper proper ternary clauses:
- $k=0$: all 8 signed patterns on three fresh variables, a contradiction;
- $k=1$: four $(\ell_1\vee \pm u\vee\pm v)$ clauses;
- $k=2$: $(\ell_1\vee\ell_2\vee u)$ and $(\ell_1\vee\ell_2\vee\neg u)$;
- $k=3$: original clause;
- $k\ge4$: $(\ell_1\vee\ell_2\vee y_1)$, then $(\neg y_{j-1}\vee\ell_{j+1}\vee y_j)$ for $2\le j\le k-3$, ending $(\neg y_{k-3}\vee\ell_{k-1}\vee\ell_k)$.

For every assignment $a$ of original variables, $C(a)=1$ iff there exists an assignment to the fresh helper variables satisfying its entire gadget. For $k=0,1,2$ this follows by exhausting helper signs; for $k\ge4$, eliminate each intermediate $y_j$ by existential resolution, recovering the original OR clause. Distinctness and fresh helpers keep every output clause strictly proper. Disjoint helper sets across clauses allow conjunction and yield exact SAT/UNSAT preservation, not exact model-by-model equivalence.

The output clause count per original clause is $g(0)=8,g(1)=4,g(2)=2,g(3)=1,g(k)=k-2$ for $k\ge4$.

## Theorem 462.B (CONDITIONAL machine composition)
An authenticated TT3-461 OR-fold guest consists of $m_v$ original 3-clauses, at most $w$ unit pins, and at most $2\cdot2^w$ child forbidden-assignment clauses of width at most $w$. Each gadget uses fresh signed IDs above a deterministic polynomial source-tag upper bound. Therefore its strict-proper-3CNF child $G'_{v,b}$ obeys
$$
\operatorname{SAT}(G'_{v,b})=\operatorname{SAT}(G_{v,b})=M_v(b),
$$
and has $O(m_v+w+2^w(w+1))$ ternary clauses and $O(\log N)$-bit literal IDs, so
$$
B'_v=O(L_{\max}+(w+2^w(w+1))\log N)\le N^{1/2+o(1)}.
$$
The number of calls remains $q\le(h-1)2^w+1\le N^{3/5+o(1)}$ for restricted $h,L_{\max}\le N^{1/2+o(1)}$, $w\le (\log_2 N)/10+o(\log N)$.

In an explicitly aligned fixed-record source, index the original ternary block directly; unit-pin gadget sections have constant four-clause length; each child blocker gadget has uniform width and known $g(w_c)$. A rank/select bitmap locates the j-th forbidden assignment without scanning it. Within a gadget each ternary output literal, including globally fresh helper index, is an arithmetic function of section, clause ordinal and relative offset. This *could* be exposed to a strictly-3SAT decider A with polylogarithmic guest-index transduction using the paid source/epoch assumptions in LSPV-4/456,/458. This is **not** independently established native FLMV bytecode. Fallback to physical materialization if it fails.

Conditional materialized bounds: $t'\le\max(11/10,3/5+t/2)$, $s'\le\max(1/2,s/2)$. Conditional indexed-virtual bounds: $t'\le\max(1,3/5+t/2)$, $s'\le\max(1/10,s/2)$. Charge parser, indexing, helper bits, guest access/reset, all failed calls, source rereads, storage and all-phase peak. No free general-CNF solver; no free machine change.

**Important limit:** Proper strict 3CNF syntax does not establish the *tagged balanced-tree postorder grammar* of TT3-461. The auxiliary variables and blocker interfaces have no certified small-interface re-decomposition, and arbitrary CNF/malformed inputs are uncovered. Recursive all-input $\Phi(A)$ remains OPEN [P2-A2]. This is SAT-decision equisatisfiability only, not any proof-size lower-bound-preserving reduction and not historical R_mix341 certificate normalization.

## Independent finite verification
Executed full Python: 8 gadget widths 0..7, 255 exhaustive original-assignment projection checks, 18 genuinely executed OR-fold SAT guest calls on two original signed strict-3CNF 3-node trees (one SAT, one UNSAT); 4 malformed literal rejections; odd-charge K4 Tseitin original 16-clause UNSAT and even-charge 16-clause SAT. Executed independently written JavaScript: 255 original-assignment checks, 18 OR-fold guests, 18 guests with subternary clauses before conversion, 3 corruption rejects. Public small Python selfcheck executed: 255 assignment checks and 3 corrupt-source rejects. All final checks PASS. A failed initial Python pilot used incorrect integer-key dictionary keyword unpacking; repaired before final verification. Full Python and JS producers, detailed raw results and hashes are in the downloadable run archive. Host experiments are not a native FLMV time/space measurement, historical mixed native checker, or asymptotic hard-family certification.

## Established-family, theorem, encoding and shortcut ledger
Cubic expander Tseitin: one Boolean edge variable, four original strict signed ternary clauses per cubic vertex excluding the wrong local parity, $H$ vertices, $3H/2$ edge variables, $4H$ clauses, binary length $\Theta(H\log H)$. Odd total charge mathematically certifies UNSAT. Published Urquhart 1987 bound $2^{\Omega(H)}$ applies to ordinary shared-DAG Resolution on suitable expander graphs, **not** to all legal mixed R_mix341 rules or arbitrary algorithms. The known GF(2) charge sum is a polynomial-time shortcut and must be permitted. LSPV-4/459 shows large adhesions for original-source clause-preserving tree layouts but no barrier to algebraic derived encodings. No lower-bound transfer to TT3 is claimed. FLMV theorem, Fortnow et al JACM 2005 DOI 10.1145/1101821.1101822 (Corollary 5.8) was inspected with page screenshot. Buss-Williams 2015 DOI 10.1007/s00037-015-0104-9 is a control, not a new claim.

## Proof-chain status
The material restricted evidence concerns [P2-A4] and source-language interface only. [P1-S3] reviewed. [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A5], [P2-B2], [P2-D1] remain OPEN. No alteration to native R_mix341 grammar or weights. No claim of P=NP or P!=NP.
