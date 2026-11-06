# LSPV-4/430: Read-only signed-autarky certificates and independent-port authentication cost

**November 5, 2026, 21:45 PST. Route A primary. PROVED/RESTRICTED + COMPUTATIONAL. Universal FLMV contraction OPEN. P versus NP OPEN.**

## Falsifiers, search, iteration
**Idea:** Extend existing LSPV-4/429 (positive private tail) and LSPV-2/434 (fixed signed witness) with an arbitrary **supplied read-only private witness**, then audit the cost of validating q separately supplied original children, rather than just comparing projected cores. Falsifiers: (F1) a purported pivotal sign flip does not change certificate validity; (F2) rejection of a corrupt certificate is misused as an UNSAT formula label; (F3) certificate lookup secretly stores a length-N map; (F4) a verified common-parent generator already authenticates the child bits, defeating the independent-source hypothesis.

Reviewed governing refocus, GitHub issue #3, actual Grok/Claude and LSPV-2/433-/434, primary FLMV machine definition, autarky literature, and both required external P-NP repositories. This work **reuses** the known autarky theorem, contributes an explicit certificate/source ledger and a restricted pivotal-query lemma, and does not assert a new universal hardness theorem.

## Exact experimental 3-CNF encoding
A separate certification grammar: 8-bit magic 11011010; positive unary counts 1^nX0 and 1^nY0; nY witness bits h in the immutable input; proper width-three core clauses tagged 10; proper width-three tails tagged 11; endmarker 00. Each literal is namespace X/Y, sign, and a fixed-width densely numbered ID (width max(1,bit_length(nNamespace))). Every core literal is X. Tail clauses may mix signed X and Y. Exactly three distinct variables are required per clause. Parser rejects malformed or duplicate names, invalid indices, misplaced tags, and trailing data.

A source authenticates a **private autarky witness** iff every tail clause has at least one Y-literal evaluating TRUE under that same h. Then, for every X-assignment a,

$$
F(a,h)=(G\wedge T)(a,h)=G(a),\qquad
\mathrm{SAT}(F)\iff\mathrm{SAT}(G).
$$

**PROVED/RESTRICTED:** This preserves both SAT and UNSAT. Rejection of a *certificate* must never be mistaken for an UNSAT answer about the underlying formula: flipping only h in an even-charge K4 source rejects the certificate but leaves the original CNF satisfiable.

**Physical resource argument:** A streaming deterministic validator keeps only counts, 3 indexed literal descriptors, input/head cursors and source-cut offsets, all O(log M) bits. A Y-literal's h bit is retrieved from the original read-only source by a paid input-index tape seek, followed by index erasure and restoration of the parsing position. All work/index fields occupy dense positions: worst all-phase FLMV physical high-water O(log M), verifier time O(M polylog M). The host-language producer itself stores full strings and is **not** a native FLMV implementation. A child encoding changes the header to nY=1, witness=0, copies the authenticated core body as a *virtual* interval and appends 00. Each child bit is locally computable with O(log M) indexed operations/scratch. A guest correct for this *typed grammar* has conditional time O(M polylog M + T_A(L)polylog M) and space O(log M+S_A(L)). A conversion to a different fixed SAT encoding requires its own proof and charges.

## Important qM versus qL distinction
For q **independent untrusted original child ports** of length at most M, with projected cores of length L, a full certificate validator and exact core comparator costs

$$
T_{\mathrm{local}}=O(qM\operatorname{polylog}M+qL\operatorname{polylog}M)
$$

before a single guest call. The earlier O(qL) shortcut applies only when originals themselves have size O(L), or authenticated shared provenance amortizes validation. At q=N^(3/5+o(1)) and M=N^(1+o(1)), direct validation has exponent 8/5, not the permitted 11/10. This proves the inadequacy of **this implementation**, not of every possible SAT compiler.

**PROVED/RESTRICTED pivotal-bit lemma:** With fixed cubic Tseitin core, fixed read-only h=1111, and k tails each containing one positive private literal and two core literals, flipping the private literal sign makes that certificate invalid. Every deterministic exact checker presented with q independent blocks, and no authenticated cross-block constraint, must inspect all qk pivotal bits on the all-valid input, or a single unseen flip yields an erroneous acceptance. For constant-width clause encodings, M=Theta(k), hence **Omega(qM)** original-bit probes. When children arise from one authenticated generator, these bits are *not independent*; the lemma does not apply. Also, an odd-charge core already proves UNSAT algebraically, so SAT algorithms need not validate these tails.

**KNOWN, not new computational hardness:** When h is not supplied and all tails are private clauses, existence of a globally satisfying private witness is exactly proper 3-CNF-SAT(T): attach an unrelated fixed satisfiable core G and copy arbitrary 3-CNF T as the private tails. This witness-discovery problem is NP-complete. It is not a superpolynomial algorithm lower bound and does not prohibit the fixed cheap witnesses of LSPV-2/434.

## Established published-hard-family ledger
Odd-charge Tseitin on connected cubic edge expanders with H vertices has 3H/2 edge variables, 4H proper 3-clauses, size Theta(H log H) with polynomial numbering, and is UNSAT by total-charge parity. Published exponential **ordinary shared-DAG Resolution** lower bounds (Urquhart 1987; Ben-Sasson and Wigderson 2001) require a suitable growing expander family and do **not** apply to unrestricted R_mix341 or arbitrary machines. Existing mixed AND3/GF(2) derivations attain the historical 4H-1 upper bound on eligible sources. The current K4/cube/Petersen instances are finite SAT/UNSAT functionality controls, not asymptotic hardness certification; our new typed sidecar grammar does not establish a Resolution-hardness-preserving encoding transfer. CNFgen's actual parity source is \`cnfgen/families/tseitin.py\` blob 4bb5fd198fc4.

## Reproducible checks
Executed Python producer 82,117 assertion units; independently implemented Node.js parser 83,702 assertions, including 14,296 projected-child bit checks and 1,312 individual pivotal-sign corruptions. 24 signed-tail families K4/cube/Petersen (odd UNSAT, even SAT), 304 certificate-erased finite private-tail cases (300 SAT, 4 explicit UNSAT), negative malformed/corrupt tests, and source/child SHA-256 output. Pivotal pairs (q,k)=(4,8),(8,32),(16,64), original lengths 434,842,1386 bits and qk=32,256,1024 independent critical bits. All results are finite host-language controls, not native FLMV timings. Expanded executed producer, independent referee, raw fixtures and SHA-256 manifest are in the attached LSPV4_430 reproducibility ZIP.

## Source authentication and remaining transfer
Read private \`j15marti/pnp\` historical handoff, current issue #3, LSPV-2/434 (cb86930e), /433 (fae636e6), current Grok 2026-11-06_0415 (2ba67d4), Claude TPORT-0002 (1f9fc727). External sources: \`konard/p-vs-np/scripts/proof_status.json\` (93b77ed), \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` (18d693e), \`meelgroup/frat-xor/README.md\` (38a137b), \`openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean\` (1ced21f), CNFgen cited above. FLMV author PDF Section 2.1 was read and visually checked (indexed tape erased on seek; physical work-tape maximum indexed position). Direct Google-branded search unavailable; indexed web search used. No full native R_mix341 proof checker was run in this Route A study. No schedule, agent identity or proof weight changed.

**OPEN:** a universally effective, original-source-authenticated, recursively iterable, both-label and malformed-aware transformation for *every* uniform polynomial SAT decider satisfying t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2). The full qM acquisition term cannot be discarded without a charged proof of shared provenance/deltas. Route B B3 and mixed minimum remain OPEN; P versus NP OPEN.

**References:** (1) Fortnow et al., JACM 52 (2005), 835-865, DOI 10.1145/1101821.1101822. (2) Urquhart, JACM 34 (1987), 209-219. (3) Ben-Sasson & Wigderson, JACM 48 (2001), 149-169. (4) Marek & Truszczynski, *Algorithmic Properties of Autarkies* (2006). (5) Kullmann, Fundamenta Informaticae 109 (2011), 27-81.
