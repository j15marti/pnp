# LSPV-2/514 | Paid affine read-coset cache: a restricted rank-cap transfer

**2026-11-08 22:52 PST, America/Los_Angeles | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proof-chain links:** [P2-A2], [P2-A4], [P2-A5] and companions [P1-01], [P1-03], [P1-04] are **OPEN**. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remains **OPEN**. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The historical R_mix341 grammar, weights, all five role IDs/schedules/enabled states, and TWO Route A / THREE Route B allocation were not altered.

## IDEA -> SEARCH -> ITERATE

**Initial idea:** If every completed guest computation on an authenticated affine virtual-child family has at most $b\log_2 N+o(\log N)$ independent input-bit read constraints, then caching *entire read-value trace equivalence classes*, rather than comparing against all previous full execution logs, can reduce actual guest executions from $N^a$ to at most $N^b$ while explicitly paying class-membership lookup and cache storage.

Four falsifiers: F1 an adaptive input-read trace has a non-affine matching-descriptor set; F2 two descriptor inputs pass the stored row-basis test but produce different guest outputs (including a write-only OUTPUT action); F3 full-rank guests or naive cache lookup exceed the conjectured simultaneous $T/S$ exponent caps; F4 any produced source is malformed, or core charge flips fail to switch UNSAT to SAT. F1/F2/F4 did not occur under stated assumptions; F3 is a genuine scope barrier when rank exceeds the cap.

**Continuity actually read:** BOTH *complete* main trackers \`proof1.txt\` and \`proof2.txt\` (initial Git blobs \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`, \`b68565137846a1737299ddbce69ae2a178da0e84\`), current coordination issue #3 and its recent peer updates, AGENTS.md (\`19656af102604d5f0a721d548cf2e4e72a063561\`), CODEX.md (\`754999f50de93cdb693ed37bc8110d31e9e698ef\`), .codex/skills/pnp-research/SKILL.md (\`b8df83a7b0b1428f349b0e02ce1387d979e8db7f\`), governing \`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md\` (\`c3889a3e514ddbd747150dcb68607013a3b2d154\`), own /513 (\`8b4c94ec1836e6c0cb159959e8614f9d85af1f5b\`), LSPV-4/511 and /512 (\`73126523a7d0a0a85ce5abad93557c923c83e58a\`, \`f9773f5bd34255dfc249221533c59fd00a5c26c4\`), actual \`GROKPROOF/2026-11-08_1130_PROGRESS.md\` (\`6942a99f176e996e9542f0386b7aa7fe2ce89e70\`) and \`research/agents/claude/world-ledger/README.md\` (\`de75a371ce3143a4495e6892df7fb04794a6b708\`). The 2026-11-08 22:03 LSPV-4/512 output-tape caution was explicitly incorporated.

**Literature and live source checks:** FLMV, *Time-space lower bounds for satisfiability*, JACM 52(6), 2005, DOI https://doi.org/10.1145/1101821.1101822 (random-access/INDEX/OUTPUT model, not an arbitrary RAM); Ben-Sasson and Wigderson, *Short proofs are narrow*, JACM 48(2), 2001 (ordinary Resolution width-size link); Urquhart on Tseitin/Resolution; Cook's extension rule is a shortcut control. GitHub **actual bytes**, not snippet authority: \`konard/p-vs-np/README.md\` blob \`0e0ec77f83ad6eec1719a96066108b96ac1c2a95\` and \`scripts/proof_status.json\` \`93b77ed3d8fe456f81c690035f45f07910a247f2\` (finite-machine formalization, no all-SAT transfer); \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` \`18d693ea71dfa433370eb7afbebc3106e32f03e5\` and \`INDEPENDENT_AUDIT.md\` \`b30515cced93d8911a6415555ee9ec1444502d93\` (restricted projection, explicitly missing uniform constructor); \`MassimoLauria/cnfgen/cnfgen/families/tseitin.py\` \`4bb5fd198fc4a698a5a207f67b36a9591b2a3bab\` (source-family generator); \`meelgroup/frat-xor/README.md\` \`38a137bca4d4ab6443703d4c31fba5783021c581\` (different checker); \`berkeley-abc/abc/README.md\` \`88a9d1a316dd9751acade746de315fd1e6e6c362\` (circuit rewrite, not an all-input contraction); \`openai/math/CONTENTS.md\` \`7e1ed90ac5a666f1bbecb22027387c4ad79e9d03\` (no directly applicable general SAT construction). Public web searches used; no Google-branded search or native FLMV emulator invoked.

**Prior-work/duplication control:** LSPV-2/513 already established affine rank-nullity for a *single* anchor. LSPV-4/511 already derived online row-basis compression, and /512 showed internal-config equivalence without OUTPUT observability is insufficient. LSPV-1/252 already discussed a Kraft-style trace-cylinder cover. These are reused, **not claimed as novel**. The present narrowly stated advance is a *paid portfolio of all read-value classes* with explicit time/space threshold and independent finite high-rank falsifier. No new universal lower bound is claimed.

## Lemma 1: exact affine read-value trace classes (PROVED/RESTRICTED, not new rank-nullity)

Fix one authenticated immutable read-only parent p, one deterministic guest machine with the same initial configuration, the same guest-visible transducer and output convention, and equal-length virtual child inputs

$$
y_i(d)=p_i\oplus c_i\oplus\langle v_i,d\rangle,\qquad d\in\mathbb F_2^k.
$$

Run the guest on anchor descriptor d0. Let R(d0) list the input positions *actually read*, **including** reads that may affect the write-only output tape; retain every observed symbol (the raw read-value transcript, not merely the internal configuration). Let V_R be its binary coefficient rows v_i. Then the class of descriptors with **the identical complete raw read-value transcript** is precisely

$$
C(d_0)=d_0+\ker(V_R)
$$

and has size

$$
|C(d_0)|=2^{k-\operatorname{rank}(V_R)}.
$$

*Proof:* Difference of observed input values is $\langle v_i,d\oplus d_0\rangle$ because p and c cancel. Vanishing on every recorded read produces identical deterministic transitions inductively, hence identical future read positions, all observable output actions and final SAT/UNSAT/MALFORMED labels. The converse is immediate from the definition of the **raw read-value** trace, even at transition-neutral reads. No unobserved branch-local context can be imported: the entire actual child encoding, including assumptions, must be authenticated. Distinct complete trace classes are disjoint and partition the descriptor domain. Thus if every class has read-rank at most r, each has at least $2^{k-r}$ descriptors and there are **at most** $2^r$ classes. This is a conservative guarantee: two different read-value transcripts might nevertheless have the same observable execution or final label. LSPV-4/512's output warning is avoided by comparing read values, not only internal states.

## Lemma 2: fully stated conditional cache threshold (PROVED/RESTRICTED symbolic upper bound)

Suppose an independently supplied, **sound and complete for its declared inputs**, uniform child constructor provides $q=2^k\le N^{a+o(1)}$ affine descriptors and virtual child size $m\le N^{\lambda+o(1)}$. Suppose every executed guest trace on these children has rank $\le b\log_2 N+o(\log N)$, and assume:
(1) an indexed virtual-input port computes each bit and coefficient row in $\operatorname{polylog} N$ *paid* time/workspace without materializing the child;
(2) each complete guest and its row-basis accumulation is faithfully simulated on the SAME declared machine with time $m^{t+o(1)}\operatorname{polylog}N$ and space $m^{s+o(1)}+N^{\eta+o(1)}$;
(3) original-source authentication, parent handling, descriptor enumeration, output aggregation, and ALL local phases cost at most $N^{\rho_T+o(1)}$ time and $N^{\rho_S+o(1)}$ simultaneously writable cells; no unaccounted historical WORK-tape high-water exists; and
(4) the supplied reduction's AND/OR semantics and all-input recursive applicability are established **separately**, not inferred from this cache.

The cache scans stored coset bases and executes a fresh guest only for a descriptor absent from previous classes. Each anchor's live coefficient rows are streamed into a $k\times k$ echelon basis. At most $K\le 2^r\le N^{b+o(1)}$ guest executions and cached classes occur. A linear scan of at most K entries per candidate takes $O(qKk^2)$ bit operations; storing anchor descriptors, basis and labels uses $O(Kk^2)$ bits. Therefore the **conditional** exponent envelope is

$$
t'\le\max\{\rho_T,\ a+b,\ b+\lambda t\},\qquad
s'\le\max\{\rho_S,\eta,\ b,\lambda s\}.
$$

At $(a,\lambda,b)=(3/5,1/2,1/2)$, assuming $\rho_T\le11/10$ and $\rho_S,\eta\le1/2$, the guest term improves from $3/5+t/2$ to $1/2+t/2$, while lookup consumes up to $N^{11/10+o(1)}$ and cache storage up to $N^{1/2+o(1)}$:

$$
t'\le\max(11/10,1/2+t/2),\qquad
s'\le\max(1/2,s/2).
$$

**This is NOT the missing Route A theorem.** Its low-rank hypothesis is unproved for arbitrary A and arbitrary children, and cannot be supplied by assuming the desired output behavior. High-rank computations may have $K=q$ and destroy the improvement. The naive scan crosses the local $11/10$ exponent if $b>1/2$, and an explicit per-class cache crosses the $1/2$ storage exponent if $b>1/2$. These are bounds for this specified implementation, not machine-independent lower bounds or exclusions of compressed/semantic shortcuts. Anchor acquisition, failed searches, source/index/head reads, writes, restarts, output and historical space must be charged; treating a proof DAG or an ideal oracle as a physical schedule is forbidden.

## Established 3-CNF family and shortcut control

For a connected cubic graph G with H vertices and 3H/2 edge variables, a vertex parity constraint $\bigoplus_{e\ni v}x_e=c_v$ has four width-three source clauses, one excluding each parity-incorrect assignment of its incident three edges. Thus the native signed strict 3-CNF has exactly $4H$ clauses, and with ordinary indexed binary variable IDs its bit length is $\Theta(H\log H)$. If $\bigoplus_v c_v=1$, summing constraints gives $0=1$, proving UNSAT. For suitable uniformly expanding cubic graph families, published **ordinary DAG Resolution** lower bounds are exponential in H under the source/proof model and the relevant width-expansion hypotheses. This is **not** an R_mix341 lower bound and certainly not hardness against all SAT algorithms. GF(2) addition is an explicit linear-size source-semantic shortcut when permitted and source-authenticated; ER/learned-DAG reasoning must be allowed as controls.

The finite K4 control ($H=4$, 6 edges) uses exactly 16 original signed proper ternary parity clauses plus seven independent proper 3-clauses on fresh variables, each individually satisfiable whatever the first literal's sign. Its fixed binary packet is eight magic bits, eight count bits, 23 times eighteen-bit literal records (5-bit ID plus sign), and 2-bit terminator, **432 bits**. Bit d0 toggles the K4 parity charge (UNSAT for d0=0, SAT for d0=1), while seven other descriptor bits toggle optional tail literal signs. These are original valid source clauses; no derived answer axiom is inserted. K4 is a **small SAT/UNSAT control**, not a certified asymptotically hard instance.

## Computational falsifiers and resource observations

Independent Python \`verify514.py\` (local SHA-256 \`d6e18770f36a829c908f979679a51d0989b319dbe732670d8ca63e7ce20b7bff\`) passed **4,748 assertion groups**. Independently written published JavaScript \`experiments/arc/lspv2_514_affine_coset_cache.js\` (blob \`f07d9c15500825b41734a9fa8735c92a8dbf6292\`) passed **774,001 assertions** in the V8 evaluation runtime. Both verify all 256 descriptors for each rank cap $r=1,\dots,8$; full bit-affine expansion; an independently brute-forced 0-versus-8 K4 core model count; and six or seven deliberate malformed packet corruptions. Exact observed cache-policy fresh guest counts are $2,4,8,16,32,64,128,256$, with corresponding safe reuses $254,252,248,240,224,192,128,0$. Linear-scan membership checks were $382,636,1144,2160,4192,8256,16384,32640$; cache anchor+basis+label bits were $34,100,264,656,1568,3648,8320,18688$. The independently executed full-guest **ground-truth** validations were **256 per rank**, not secretly counted as cache speedups.

The finite implementations explicitly materialized each 432-bit packet and retained authenticated ground-truth results. Both tests are **COMPUTATIONAL**, not physical same-FLMV-machine timing/space evidence; symbolic bit counts above are modeled upper bounds, not an instrumented native machine ledger. The Python fallback decides other valid packets by DPLL within the explicitly bounded 31-variable toy grammar; the independent JavaScript verifier marks valid non-family packets OUTSIDE_FAMILY rather than pretending to be a general CNF decider. The seven tail signs are optionally read solely as raw-transcript probes and may be observationally neutral. An alternative guest can avoid them, so **no optimal-derivation lower bound** follows from the rank-eight case.

**Artifacts:** independent V8 verifier \`experiments/arc/lspv2_514_affine_coset_cache.js\`; published full raw \`results/raw/arc/2026-11-08_2252_LSPV2_514_AFFINE_COSET_CACHE.json\`; local independent Python and raw archive; five-role handoff \`research/coordination/2026-11-08_2252_LSPV2_AFFINE_COSET_CACHE514_FIVE_ROLE_HANDOFF.md\`. New report and code are within LSPV-2 ownership; no root main.tex or tracker content was modified.

**Actual advance:** an explicit lookup, guest, rank and cache simultaneous-resource tradeoff under an independently stated low-rank premise, plus a concrete high-rank falsifier for the chosen cache. **Remaining gap:** establish the low-rank guarantee, construct the independently supplied all-input adaptive solver-dependent child reduction, prove recursive closure and SAME FLMV machine resource charges; [P2-A2], [P2-A4], [P2-A5] remain OPEN. Route B full R_mix341 and B3 remain OPEN. **P versus NP OPEN.**
