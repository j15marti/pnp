# LSPV-1/529: original-source two-vertex modulo-three boundary Resolution port and exponential explicit-interface barrier

**2026-11-09, America/Los_Angeles (PST). Route B. PROVED/RESTRICTED symbolic lemma + COMPUTATIONAL reproducible packet. P versus NP OPEN.**

**Relevant proof-chain IDs:** proposed new evidence [P2-L1-529], building on [P2-L1-522], [P2-L1-524], [P2-L1-526], [P2-L3-527], [P2-L3-528], refining the *remaining transfer* [P2-C3]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] all remain OPEN. [P1-01], [P1-03], [P1-04] unchanged.

## IDEA -> falsifiers -> SEARCH -> ITERATE

**Hypothesis.** Rather than presupposing a conservative extension gate, combine two adjacent modulo-three Tseitin vertices entirely by historically declared *ordinary binary Resolution* from their exact original one-hot strict-three clauses. The interface is a four-edge congruence with 54 forbidden boundary assignments; all 54 corresponding signed clauses should have an explicitly shared source-authenticated DAG of 72 binary RES steps and no branch-scope assumptions.

**Four precommitted falsifiers:**
1. One of the 54 exported clauses fails on an original-source model or its derivation uses a non-source input/fabricated AMO axiom.
2. Any signed RES pivot, antecedent, conclusion or acyclic reference is wrong, or source records cannot be matched to the original proper three-CNF.
3. A repeated-intermediate accounting mistake makes 72 distinct paid steps insufficient, or an omitted boundary tuple invalidates the exact interface.
4. The asserted exponential boundary-materialization burden accidentally treats extension variables, compact affine rows, GF(2), learned DAG lemmas or alternative proof strategies as prohibited, or promotes a restricted normal-form size to all-rule minimum hardness.

**Search and provenance.** Read both complete root trackers at initial main blobs `proof1.txt` 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and `proof2.txt` b2c5dad9ee0bb0b7293e004fb993ddf932a824aa; current coordination issue #3 and its 2026-11-09 00:55 PST LSPV-3/528 comment; historical five-role November 2 handoff blob 033b54b87b7cbe94912af5cf67daa52859143a07, AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef and repository skill. Authenticated frozen *historical prose*, NOT bytes, at `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Reviewed LSPV-3/528 source-sharing report blob 2c5f7ab4b46ce856ec17c62ba608b084c464a504; LSPV-5/454 audit blob a217958485de06a8aa324d4822f4e23b020810eb; previous LSPV-1/528 spectral report blob bd28f451704486a42bc8d2e88cb2867a9d41ceb8; actual GROKPROOF/2026-11-06_2316_PROGRESS.md blob a20fb8b3640d7574faf238a4a83a021bb0984808 and Claude world-ledger README blob de75a371ce3143a4495e6892df7fb04794a6b708.

Targeted project code searches: `two vertex boundary modulo-three resolution elimination`, `boundary normal form q^(b-1) one hot Tseitin`, `54 clauses 72 Resolution Tseitin`, `frontier elimination mod 3 Tseitin`. Exact result not located in inspected repository, **not** a claim of scholarly novelty. Inspected external `konard/p-vs-np` README blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and its `proofs/p_not_equal_np/README.md` blob 3a0304116e719948122302849ccae38d3890e410: finite machine model, no general P/NP result. `blkph0x/p-vs-np-proof-research` README blob f397a7747eaca82df3d754d0a4b4bab1fe10f814: restricted/promise and Reed–Muller marginal programs, not a general lower bound. Inspected `meelgroup/frat-xor/format.md` blob 986a21aa92b62f844ef1fce852193142c41b2b1f and `tanyongkiam/cake_lpr/README.md` blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; these are distinct proof grammars, not historical R_mix341 checkers. Inspected `peitl/short-proof/README.md` blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab (shortest-Resolution SAT search). OpenAI math at `lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean` blob 1e23a159afcf8cf383c276720a878ad833940502 addresses polynomial-time tableau encoding, not this proof grammar.

Primary literature review: Pang (2026), arXiv:2610.00837v2, Theorem 7.2(b), bounded-degree algebraic-Resolution size lower bound with opposite prime characteristic; Ben-Sasson/Wigderson (JACM 48, 2001), width/size tradeoff for ordinary Resolution; source link https://eccc.weizmann.ac.il/report/1999/022/. Neither supplies an authenticated history-specific ER2/CANON/R_mix341 translation. An external web search for variable-elimination/expander-frontier blowup found existing width/space tradeoff literature, so the present result is a precise *restricted explicit-interface* calculation, not an unconditional complexity discovery.

## Exact original-source two-vertex construction

Let each edge be encoded by three Boolean indicators, one positive ALO clause, and the original forbidden signed triple clauses at vertices. Let the five one-hot edge groups be $U,V,E,W,T$. Orient the common edge $E$ oppositely, with vertex charges $c_A,c_B\in\mathbb Z_3$:

$$
U+V+E=c_A,\qquad W+T-E=c_B.
$$

Original strict-three source = five ALO clauses + 18 inconsistent triple clauses for each vertex = **41 proper signed clauses, 15 Boolean variables**. No AMO or private axiom is supplied. The constraints themselves enforce exactly-one, since the ALO clauses make every group nonempty, while two true values in a group would require two different values of the same neighbor group to be simultaneously consistent with a fixed charge.

For each $(a,b)\in\mathbb Z_3^2$ let $e=c_A-a-b$. From the original E-ALO clause and exactly the two original vertex-A clauses excluding the other two E values, derive by two exact, correctly oriented binary Resolution steps

$$
\neg U_a\lor\neg V_b\lor E_e.
$$

This produces nine shared port clauses in **18 paid RES nodes**. For each $(a,b,w,t)$ failing the combined boundary equation

$$
a+b+w+t\equiv c_A+c_B\pmod3,
$$

the original vertex-B forbidden triple $\neg W_w\lor\neg T_t\lor\neg E_e$ resolves against the shared port clause to derive

$$
\boxed{\neg U_a\lor\neg V_b\lor\neg W_w\lor\neg T_t}.
$$

Exactly $3^4-3^3=54$ boundary tuples fail. Each output costs one further Resolution step, yielding an explicit **72-distinct-RES-node shared DAG**, 144 paid premise-reference edges, and weighted critical path 3 under unlimited parallelism. The 113 serialized records are 41 authentic source clauses plus 72 Resolution steps. Only 37 of the 41 source records lie in output ancestry; the four outer-group ALO clauses are retained for complete original-source fidelity. No definition, case split, weakening, LOCAL-CONVERT, GF(2) shortcut or foreign clause is used.

**Generic fixed-$q$ lemma (PROVED/RESTRICTED):** The same construction over alphabet $q\ge2$, using one $q$-literal common-edge ALO clause, $q-1$ forbidden triples per boundary input pair and signed binary Resolution, derives all $(q-1)q^3$ boundary-forbidder clauses in at most

$$
q^2(q-1)+q^3(q-1)=q^2(q^2-1)
$$

paid RES steps, with shared intermediate ports. For $q=3$, every original clause is proper strict-three; for $q>3$ the ALO has width $q$ and is **not** a strict-three statement without a separately proved encoding.

## Larger connected clusters: exact representation barrier, not proof hardness

For a nonempty connected vertex set $S$ in a graph with oriented modulo-$q$ edge flows, eliminate internal edge values existentially. The interface on the $b=|\delta(S)|$ boundary edges is **exactly** the single charge-balance equation

$$
\sum_{e\in\delta(S)}\epsilon_e x_e\equiv\sum_{v\in S}c_v\pmod q.
$$

Necessity follows by summing vertex equations. Sufficiency follows by setting non-tree internal edges arbitrarily and solving leaf-to-root on an internal spanning tree; the last row is consistent precisely by the total balance. This holds for connected $S$ with any $b\ge1$ and any $q\ge2$ (tree coefficients $\pm1$ are units).

Among **explicit full-boundary negative one-hot assignment-forbidder clauses only**, the exact unique set of clauses needed to express this interface is

$$
\boxed{(q-1)q^{b-1}}.
$$

Reason: exactly $q^{b-1}$ of the $q^b$ boundary assignments obey balance; each full-forbidder clause is false on *exactly one* one-hot assignment. A negative tuple clause that mentions fewer than $b$ distinct boundary groups is not entailed by balance: one omitted boundary value always completes it. Thus every wrong complete tuple must be forbidden explicitly, and this full-tuple normal form is irredundant.

For a cubic family with edge-expansion $|\delta(S)|\ge\alpha\min\{|S|,h-|S|\}$ and connected $S$ of size $\lfloor h/2\rfloor$, $b\ge\alpha\lfloor h/2\rfloor$. Hence materializing *all* full boundary forbidders demands at least $(q-1)q^{\alpha\lfloor h/2\rfloor-1}$ clauses, and at least that many output records/bits, even though the one-row affine interface itself has $O(b\log q)$ semantic bits. This barrier concerns a **specific explicit normal form**, not all CNF with auxiliaries, all proof DAGs, or all historical R_mix341 inference schedules. Definitional circuits, GF(2), extensions, symbolic linear algebra and reconvergence are legitimate upper-bound candidates, never excluded to protect hardness. It cannot prove [P2-B1] or B3.

## ITERATE: independent finite evidence and resource accounting

Executable proof generator and independent replay:
- `experiments/arc/lspv1_529_twovertex_boundary_port.cjs` (published blob afb8752619355f49ffd377a2f41f0e79ecc9b24d), complete 5,252-byte code.
- `results/raw/arc/2026-11-09_0109_LSPV1_529_BOUNDARY_PORT_RAW.json` (published blob 855d0bf3b85470dae013fb30ec0497bfe356c87a), full 20,434-byte, 113-record certificate.
- Separate independently written Python generator/verifier `lspv1_529_boundary_elimination.py` and full raw `lspv1_529_boundary_elimination_raw.json` were executed in local run storage. The Python compact canonical pre-hash fixture was 8,432 bytes, SHA-256 c8460584ea48b4813dffafb55017b65725e12cd193a8f43af01b00484f1d906d; it is an independently implemented check, not an official historical checker.

The JS reconstructed all clauses and exact signed parents, checked 32,768 original Boolean assignments with exactly 27 source models, and rejected three corrupted-pivot controls. The Python check independently reconstructed the same 72-node derivation, checked all 32,768 Boolean assignments and all 81 boundary tuples with exactly 27 valid and 54 impossible, and rejected two invalid-pivot controls. No solver oracle was used in construction, only finite brute force for *external verification*.

**Work vs span vs realizable resource scope:** ideal distinct work 72 RES, 144 premise references, unlimited-processor span 3. A serial executor must at least emit/verify all 113 records (41 source+72 RES), including 54 boundary output clauses and 15-variable source parsing. The raw published packet is 20,434 bytes; JS program 5,252 bytes. Actual construction/verification host time, retrieval, source reads, repository updates, certificate serialization, parsing, failed search and peak RSS are not measured as native-machine complexity and must not be silently included in the 72; they are distinct additional phases. No claim of FLMV same-machine $ho,\eta,\lambda$ budgets. For the explicit full-boundary expansion, the output size alone grows as $\Omega(q^{b-1})$ and cannot be treated as constant-cost.

## Family / theorem / encoding / known-method / missing-transfer ledger

| Selected source | Encoding and size parameter | Established theorem and model | Legal upper controls | Missing transfer |
|---|---|---|---|---|
| Odd-charge binary cubic expander Tseitin | Four proper 3-clauses per vertex, $4h$ source clauses, $N=\Theta(h\log h)$ | Exponential DAG ordinary-Resolution hardness for expanders, model-specific (Urquhart; Ben-Sasson/Wigderson) | Historical $R_{\mathrm{mix341}}$ AND3+GF(2) direct $4h-1$ exact optimum in /341 | No general lower bound survives mixed rules; no B3 |
| Opposite-characteristic modulo-three Tseitin | One-hot edge-group encoding, strict proper 3-CNF with original ALO and forbidden triples, $\Theta(h)$ variables/clauses and $O(h\log h)$ bits | Pang arXiv:2610.00837v2, Theorem 7.2(b): $\exp(\Omega_r(h))$ for fixed $r$ in $\mathrm{Res}(\mathrm{PC}_r/\mathbb F_2)$ with stated expander assumptions | Modulo-three algebra; paid ER2 modules /524-/528; present native signed RES two-vertex 72-node interface | No polynomial-full-R_mix341 translation of compact interface, no all-rule lower bound, no noncircular B3 |

**Precise next step:** compose these *actual* 54 ordinary RES clauses into a three-or-more-vertex shared boundary packet without claiming efficient full interface expansion, and separately test whether existing paid DEF facet/LOCAL-CONVERT rules admit polynomially compact, source-authenticated affine-interface certificates in the unchanged historical grammar. Native accepted-byte authentication [P2-D1] remains unavailable, and the stronger mixed transfer [P2-C3], unrestricted superpolynomial [P2-B1] and same-calculus B3 [P2-B2] remain OPEN. No rule or weight revised. P versus NP OPEN.
