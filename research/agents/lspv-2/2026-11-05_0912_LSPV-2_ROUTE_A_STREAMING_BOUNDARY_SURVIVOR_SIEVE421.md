# LSPV-2/421: Route A authenticated streaming boundary-survivor sieve

**2026-11-05 09:12 PST, America/Los_Angeles.** Status: **PROVED/RESTRICTED** exact separator identity and conditional indexed-machine resource implementation for a precisely declared *tagged* sublanguage; **COMPUTATIONAL** finite controls; **OPEN** uniform recursively iterable full-language solver-dependent FLMV contraction and P versus NP. Five-role allocation: LSPV-2 and LSPV-4 Route A, LSPV-1/3/5 Route B; no task changes.

## IDEA: falsifiable predictions made before searches

Hypothesis: one can remove the source-rescan and cross-component SAT-bit join errors of an explicitly authenticated syntactic separator by maintaining a 2^b-bit boundary survivor mask and streaming each contiguous component once. F1: any authentication requires an N-bit writable directory or Nq parent scans. F2: independently SAT component labels may falsely imply parent SAT without a common boundary assignment. F3: actual serialized children or total calls exceed sqrt(N) and N^(3/5). F4: malformed tags, forged cofactors, or guest indexed reads are treated as free. This is an attempted **promised-family** construction, not an assumption of a general source-only splitter.

## SEARCH: exact project, primary and external sources

Read governing five-role November 2 handoff at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514d); current issue #3 through LSPV-4/416, LSPV-5 REFEREE365, LSPV-2/420; AGENTS.md (19656af1), CODEX.md (754999f5), and .codex/skills/pnp-research/SKILL.md (b8df83a7). Read LSPV-4/416 (research/agents/lspv-4/2026-11-05_0836_LSPV-4_GUEST_ACCESS_TAX416.md, 5b9b5365), LSPV-2/ARC252, ARC262 and historic PADDED-GUEST157 (50ae1b1c), and FALLBACK-PADDING118 (e5e2bb77). The latter already proves a different restricted black-box padding obstruction: no novelty claimed for unchanged-parent guest fallback.

Actual external assessments read: GROKPROOF/2026-11-05_1218_PROGRESS.md (d3183283), research/agents/grok/2026-10-12_1859_GROK_FL2.tex (f2a90a8b), research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727). They do not provide an arbitrary-A constructor. New external repositories reviewed: konard/p-vs-np README.md (0e0ec77f), proofs/complexity/README.md (7ee9a11e), finite one-tape P subset NP, not an FLMV reduction; blkph0x/p-vs-np-proof-research README.md (f397a774), METHOD_INDEX.md (18d693ea), RESOLUTION_STANDARD.md (729a9164), scoped finite audits; openai/math Lean OAI/Algorithms/SubexponentialSAT/ExecCNF.lean (e60f4d98), ExecCNFNodeSearchCosts.lean (1ced21f4), costed executable list operations but no all-input ARC. Primary source: Fortnow–Lipton–van Melkebeek–Viglas, "Time-Space Lower Bounds for Satisfiability", JACM 52(6), 835–865 (2005), https://lance.fortnow.com/papers/files/tst.pdf, inspected machine-model printed p.4 and theorem statement. Queries included "FLMV indexed random access input heads", "SAT virtual child access overhead", and component decomposition/backdoor SAT. Direct Google-branded search unavailable, indexed web and authenticated GitHub reads used. No code title or CI result treated as mathematical proof.

## ITERATE: theorem, charged construction and scope

Declare an ASCII tagged DIMACS **subclass**, not all original binary CNF encodings: header, one "c cut b" and ordered "c block lo hi" comments. Variables in first b positions are the common boundary B. Other variables are divided into strictly increasing, pairwise disjoint contiguous private-ID intervals X_i. Every clause is in exactly one group G_i and refers solely to B union X_i. Every input byte, header, comment, literal sign, positive ID, clause count, interval order, disjointness and variable bounds must be authenticated before using any early UNSAT inference; promise additionally requires the decimal IDs to be canonical and the header n to satisfy 1<=n<=N. Nonpromise source must fall back to the original guest or another correct full-language procedure.

**PROVED/RESTRICTED identity** for any total exact SAT decider A:

$$
\operatorname{SAT}(F)\ \Longleftrightarrow\
\bigvee_{\beta\in\{0,1\}^{b}}\ \bigwedge_{i=1}^{h}
\operatorname{SAT}(G_i\!\upharpoonright_{\beta}),
\qquad F=\bigwedge_iG_i(B,X_i).
$$

A global witness induces a single beta shared across all groups; conversely all private witnesses for the same beta coexist because private support sets are disjoint. Maintain a 2^b-bit mask of surviving beta, initially all ones. After a complete validation pass, stream one block into a buffer and, for each still-surviving beta, serialize an *ordinary CNF* cofactor and invoke the same guest A. Clear the beta bit on a NO. Accept iff a bit survives. This calls A on both SAT and UNSAT children and does not assume a semantic oracle; verification of any guest answer relies exactly on fixed A's global correctness premise.

For the **explicit syntactic promise**

$$
2^b \le N^{1/2},\quad h2^b\le N^{3/5},\quad
\max_i \{|\operatorname{encode}(G_i)|,
\max_\beta|\operatorname{encode}(G_i\!\upharpoonright_\beta)|\}
\le N^{1/2},
$$

including all original-ID digits, child headers, endmarkers and group-boundary metadata, two full linear-time source scans plus child construction perform local N^(11/10+o(1)) bit work; counters/indexing and source validation have polylogarithmic bit cost per token. The mask, group, materialized child, counters, input-index tapes and guest working/index tapes require simultaneous writable peak at most N^max(1/2,s/2)+o(1). *No virtual child is free.* In the actual FLMV indexed-tape model the child must be filled on a separate indexed work tape, with all input-index writes and erasures counted. The fixed controller can map the guest's read-only indexed input head operations to this writable indexed tape without allowing guest input writes, paying constant steps per indexed guest operation plus actual child filling, and reserve separate guest work tapes; the original N-bit source remains read-only.

For guest A of worst-case time m^(t+o(1)), space m^(s+o(1)) the resulting **PROMISE-ONLY** bound is

$$
t_{\rm promise}'\le\max\{11/10,\ 3/5+t/2\},\qquad
s_{\rm promise}'\le\max\{1/2,\ s/2\}.
$$

This is a mathematical implementation argument under the declared tape simulation and tag grammar, NOT a proof-assistant formalization or measured FLMV machine run. The executable Python and Node implementations keep an N-bit original source in process heap, so their actual peak memory is not the asserted native-tape bound. Discovery of the separator is not free; this construction merely *checks* a tagged separator. Distinct recursive children are ordinary CNFs and need not have tags, so hereditary closure is also not proved.

An explicit unbounded easy promise family does satisfy the above ratios: b=1, h disjoint private blocks, each with guard clauses (x OR z_i), (x OR NOT z_i), plus f(h)=max(1,floor[h/(100 log_2(h+2)^2)]) unit private filler clauses, all fresh. On the NO control only the last block's guard has both x polarities negated. All YES guards force x=1; last NO guard forces x=0. Its N=Theta(h^2/log h), max group and fully serialized child O(h/log h)=o(sqrt N), and possible calls 2h=o(N^(3/5)). This is ordinary bounded-interface decomposition and is not a new SAT worst-case hardness family or general ARC.

## Verified finite counters, falsifiers and physical ledger

Python full producer (available in attached local reproducibility archive): **40 assertions**. Separately written Node referee using no Python code: **1,721 checks** of eight SAT and UNSAT originals, source SHA-256, exact cofactor semantics, accepted/rejected shared-beta joins, original clause indices and serialized child bits. The standalone Node replay in repository regenerates and checks all eight cases. In the 700-block SAT case, N=181592 bits, max child=168 bits, 1400 possible calls and 701 actual. In the 700-block UNSAT case, N=181608, max child=200, same possible and actual calls. Both obey floor(sqrt N)=426 and floor(N^.6)=1430; small groups 2, 7, 100 **do not** obey the finite child-size cap. A source with huge cut tag is routed to original-source fallback before any exponential mask allocation. Four malformed/corrupt tags, forged x=0 cofactor and invalid independent joining are negative controls. The NO parent (x OR z) AND (x OR NOT z) AND (NOT x OR w) AND (NOT x OR NOT w) has SAT groups but no shared satisfying x; independent-AND is UNSOUND.

Physical model charges parsing, 2 source passes, source/head/index writes, every failed survivor policy, child construction/output, repeated guest input reads, A's work/indices, guest reset/answer, all-phase live mask/group/child and temporal peak. The finite programs measure serialized evidence and operation counts, NOT calibrated native-machine runtime or heap peak. There is no optimized arbitrary-set proof search being disguised as free. No old fixed R_mix341 rule/weight is changed.

## Unresolved transfer and preservation

On a general valid or malformed input, the declared full-language wrapper first detects invalid syntax, uses the certified sieve only when tags/promises validate, otherwise invokes A on the **unchanged full N-bit source**. This is correct on all labels but its unchanged-parent fallback does **not** imply the desired global time/space contraction, especially for a syntactically padded correct decider A. The family of recursive outputs also fails to carry the tag promise. Thus the universal same-machine, all-input and recursively iterable A -> Phi(A) edge, and therefore P versus NP, remain **OPEN**. Cross-role Route B results are untouched.

**Publication safeguards:** root main.tex returned blob 1b8a7d9a but empty body; it is not overwritten. Locally tested detailed producer/checker and original hashes are in the associated reproducibility ZIP.
