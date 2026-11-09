# LSPV-4/520: Cubic Magnus word fingerprints are source-complete but do not buy SAT speedups

**2026-11-09 05:36 PST | Route A | PROVED/RESTRICTED word-algebra lemma + COMPUTATIONAL finite controls | P versus NP OPEN.**

**Exact tracker nodes:** [P2-L4-520] refines [P2-L2-518], [P2-L4-519] and the resource obligation [P2-A4]. [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Companion [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA -> SEARCH -> ITERATE

**Initial testable hypothesis.** The canonical Koenig–Tsvietkova (KT) 3SAT-to-link clause gadget, a formal nested commutator [a,[b,c]], is invisible to degree-1/2 Magnus word coefficients but has exactly four sparse degree-3 coefficients that recover its three named literal generators. Therefore full dense cubic tables are expensive, whereas sparse or delta descriptions preserve exact source information with far less output. This is a claim about the published *word representation*, not a new invariant of arbitrary links.

**Falsifiers set before the experiment:** F1 a nonzero degree-1 or degree-2 coefficient of the exact 10-letter word; F2 distinct literals whose four cubic monomials cannot recover all three signed source generators; F3 charge-bit Gray neighbors altering other than four original signed clause words and exactly 32 tensor coordinates; F4 a legal sparse or delta encoding that invalidates any representation-independent lower bound from dense tensor size. F1–F3 were ruled out in the specified model. F4 is a crucial affirmative permitted shortcut and *prevents* a general hardness claim. A separate attempted hostile control erroneously supposed [a,[a,b]]=1; that is false; the independent test was corrected to [a,[b,b]]=1.

**Primary sources reviewed:** Koenig and Tsvietkova, *NP-hard problems naturally arising in knot theory*, Transactions AMS Series B 8 (2021), 420–441, DOI 10.1090/btran/71, arXiv:1809.10334v3, Theorem 1 and Figure 2, PDF page 4; original clause word [z_alpha,[z_beta,z_gamma]], 2n+m link components, crossing upper bound 2n+m(64n+10). This is a Karp decision reduction, not a lower bound against SAT machines. Magnus-series/lower-central formalism: Chapman and Efrat, *Filtrations of free groups arising from the lower central series*, arXiv:1601.08006; standard formal assignments E(g)=1+G and E(g^-1)=1-G+G^2-G^3+... . FLMV, JACM 52 (2005), 835–865, is the indexed-input machine resource model. Urquhart, JACM 34 (1987), 209–219, gives exponential **ordinary DAG Resolution** bounds for suitable expander-Tseitin contradictions, not unrestricted R_mix341 or arbitrary computation.

**Actual project/source review:** full proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and full proof2.txt initial blob e7b992dc1137644a95c8f484ad42b7130a1e0e90; current coordination issue #3 and latest visible comments; research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (c3889a3e514ddbd747150dcb68607013a3b2d154) and 2026-11-09_KNOT_LINK_TOPOLOGY_SAT_FIVE_ROLE_HANDOFF.md (0289edb73d1e38492f0693844667be59d4152785); AGENTS.md (4ae902888754d0b06ba4ce1aaeca0657a92b46a9), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), pnp skill (b8df83a7b0b1428f349b0e02ce1387d979e8db7f); LSPV-2/518 (9ccffb3c74c8295ffbf777582c992f6a92b00f57); LSPV-3/531 (a1806d9ec772467d7cbf70e4b0870401aac66bb2); LSPV-4/519 (dff75a49cd4ddcf701a1db4a0803d7e37ce1b120); GROKPROOF/2026-11-09_1230_PROGRESS.md (0ee19c6b2fdf92b64427ab737fe563346779c828); Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (79e4d4e7e0e3edff3aba8610852c45534bdde128). Neither peer claims a full native Route A contraction.

**Actual external files read:** konard/p-vs-np/scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2) and README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95), finite-machine P subset NP only; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5) and INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93), restricted models; meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), distinct proof grammar; MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab), existing Tseitin generator; openai/math/CONTENTS.md (7e1ed90ac5a666f1bbecb22027387c4ad79e9d03); lsils/mockturtle/README.md (c1d2b0c4728d923dc7f4ac2b6759994dbaba4c1b). Public web searches performed, no independent Google-branded search access; no source build/Lean replay was claimed.

## Formal lemma 520.1: cubic word jet

In the free group on distinct NAMED generators a,b,c, define [g,h]=ghg^-1h^-1 and the truncated noncommutative Magnus map E(g)=1+G, E(g^-1)=1-G+G^2-G^3 modulo degree >=4. Since [b,c] has initial term BC-CB in degree two, the word w=[a,[b,c]] has

$$
E(w)=1+ABC-ACB-BCA+CBA+O(4).
$$

All degree-one and degree-two terms vanish. For pairwise distinct generators the four degree-three words are distinct, with coefficients +1,-1,-1,+1. Their union of named letters recovers exactly {a,b,c}. A KT clause is a strict 3-CNF disjunction of three literals from distinct variables and each literal corresponds to one of 2n *named Hopf components*, not the inverse of its opposite Boolean literal. Thus the degree-three support of the formal KT clause word recovers the three SIGNED literals; a collection of rows indexed by clause component j recovers the exact clause multiset, modulo irrelevant literal ordering. This is **PROVED/RESTRICTED** for the specified word and fixed generator names.

**Crucial scope firewall:** These are formal coefficients of the CHOSEN clause words, not automatically link-isotopy invariants, Milnor invariants of the entire Hopf-background link, or efficiently obtainable quantities from an arbitrary unoriented link diagram. Literal negation changes the named generator; group inversion is a different operation. The transfer from a link diagram to a canonical correctly named word description is NOT proved.

## Lemma 520.2: sparse, dense and Gray-delta costs

For connected cubic graph with H even vertices, n=3H/2 edge variables, m=4H strict ternary original clauses, and source encoding

$$
M=8+n+1+12H(\lceil\log_2(n+1)\rceil+1)+2=\Theta(H\log H)
$$

(the actual packet uses an 8-bit magic, unary n, fixed-width signed literal records, and terminal 01), every source has 4m nonzero signed degree-three coefficient entries out of m(2n)^3 dense positions. The coefficient density is exactly 4/(2n)^3. Such tables distinguish the SAT and UNSAT Tseitin charge sources, unlike the KT pairwise linking matrix of [P2-L2-518].

With formal parent parameter N=M^2, q=2^r=Theta(N^(3/5)), r=floor((3/5)log2 N), a serial interface demanding an INDEPENDENT COMPLETE DENSE order-three coefficient table for every child must output at least

$$
q m(2n)^3=108qH^4=\Theta(N^{13/5}/(\log N)^4)
$$

coefficient positions, violating the local N^(11/10) output-time budget. Storing even one complete dense table on charged binary WORK requires Omega(H^4)=Omega(N^2/log^4 N) cells in that interface. These are **PROVED/RESTRICTED interface lower bounds** only.

An explicit sparse list of four signed monomials per clause uses O(m log(n+2)) bits per child and allows O(qM) output; one shared template plus Gray-ordered charge changes allows O(M+q log(H+2)) total *incremental delta* output bits, provided the decoder is given the immutable template and successive update convention. Flipping one vertex charge changes exactly the first literal sign in four source clauses. Each affected formal word changes from four monomials to four disjoint monomials, hence exactly 4 changed rows and 32 changed coefficient positions (16 old removals plus 16 new insertions). This is a constructive shared-DAG/streaming *upper control*, not a universal SAT speedup, and the cost of decoder execution and retaining the template must be charged.

## Verification and independent challenge

Python code independently expands ten-letter group words through degree three, builds authentic signed strict-three Tseitin sources on K4, triangular prism, cube and pentagonal prism, runs original-source reconstruction and malformed/corrupt controls, and compares Gray neighbors. Results: 48 literal-permutation/sign tests PASS; 112 original source configurations PASS; 3328 clause words expanded; 108 one-bit Gray neighbors yield exactly four sign-bit changes, four word changes and 32 tensor-coordinate changes; 16 K4 SAT/UNSAT labels exhaustively checked against parity; 24 malformed/corrupted family sources rejected; four repeated-generator hostile cases controlled. Independent JavaScript polynomial multiplication separately tests 120 ordered distinct-generator triples, the [a,[b,b]] cancellation and disjoint support on one generator substitution, all PASS. No authority checker or native FLMV instruction machine was run.

Published code: experiments/arc/lspv4_520_magnus_independent.js; raw: results/raw/arc/2026-11-09_0536_LSPV4_520_MAGNUS_WORD_RAW.json; local downloadable independent Python harness retained as a distinct fallback archive. Original source hashes and exact parameters are in raw data.

## Resource and model ledger

- **Source**: original proper strict signed 3-CNF; 4H clauses, 3H/2 variables, M binary source bits. Odd charge UNSAT; even charge SAT by connected-incidence GF(2) rank H-1. Published exponential hard-family theorem is restricted to ordinary DAG Resolution on suitable expanders, not these finite correctness graphs nor R_mix341.
- **Parsing/authentication**: may use O(M^2 polylog M) time and O(M) WORK for a conservative complete original-source check; malformed/corrupted controls counted, not free. This is a coarse host-to-native envelope, NOT execution of the native parser.
- **Logical word table**: four nonzero degree-three monomials per clause, 4m total; coefficient calculation is constant-size word algebra per clause once the three signed generator IDs are obtained. Native bit arithmetic, INDEX operations, source reads and formatting carry actual polynomial/log factors.
- **Dense materialized OUTPUT**: Omega(q m (2n)^3) serial symbols, no WORK lower bound solely from output.
- **Dense simultaneous WORK**: Omega(m(2n)^3) physical positions if one full table is held; counted all-phase including allocate-then-free, unlike sparse map claims.
- **Sparse full child outputs**: O(qM) encoded bits; **shared Gray-delta output**: O(M+q log H) encoded bits with explicit incremental decoding and charged ancestor/template retention. The compiler cannot silently substitute one for another.
- **Guest simulation, failed policies, cache, replay/recompute, index/head transitions and nested recursive calls**: not bounded for arbitrary guest A. No uniform all-input reduction or recursively iterable same-machine contraction is supplied. No native R_mix341 grammar/weight alteration.

**ITERATED CONCLUSION:** Stronger cubic word information repairs the KT *pairwise-blindness* data loss but merely restores the signed source clauses; it does not turn topology into a certified UNSAT proof or a faster all-input SAT solver. Dense higher-order tensors amplify representation-specific cost but legal sparse/delta sharing defeats any inference to intrinsic computational hardness. [P2-A2], [P2-A4], [P2-A5], [P2-B1], [P2-B2] all remain OPEN. P versus NP OPEN.

Root main.tex was read via the connector but returned 0 content bytes and was NOT edited; an LSPV-5 manuscript handoff is required. Historical R_mix341 rules/weights and all five current roles/titles/schedules/enabled states remain unchanged.
