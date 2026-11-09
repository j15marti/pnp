# LSPV-1/524: source-authenticated strict-3 one-hot inverse-cancellation packet

**November 8, 2026, 21:00 PST | Route B lead | PROVED/RESTRICTED in a separately declared signed-AND2, owner-addressable-facet ER2 calculus; COMPUTATIONAL independent packet replay. Historical R_mix341, B3, all-rule lower bound and P versus NP OPEN.**

**Affected proof-chain IDs:** new [P2-L1-524]; narrows the constant-size source-to-cancellation interface gaps in [P2-L1-518], [P2-L1-520], [P2-L1-522], [P2-L5-448], [P2-L5-449], [P2-L5-450], [P2-C3] and [P2-F6]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. [P1-X1] unaffected.

## IDEA, precise falsifiers, and quantifiers

**Hypothesis.** For every triple of original Boolean edge-indicator variables $(x_0,x_1,x_2)$ with the strict-three source asserting exactly one true indicator, and every padding bit $z$, there is **one fixed, context-free, original-source-authenticated** signed-AND2/Resolution DAG deriving an independently named one-hot encoding of $-x$ over $\mathbb F_3$ and the three unit conclusions that their mod-three sum is zero. The derivation must charge all paid definitions, respect distinct absolute input IDs, and use no branch discharge, weakening, native GF(3) oracle or free defining facets labelled as original sources.

Four falsifiers: (F1) original strict 3-CNF cannot yield the required pairwise at-most-one clauses by ordinary Resolution; (F2) making three globally fresh inverse ports requires an illegal repeated-ID gate or an uncharged constant; (F3) the zero-sum **units** cannot be derived with properly oriented, source/facet-owner-addressed Resolution; (F4) the result is claimed as accepted in historical R_mix341 despite its unverified byte grammar. F1-F3 have exact positive packets below. F4 remains an unresolved *historical transfer*, not a mathematical falsifier of this expressly different calculus.

## SEARCH: current sources, precedence, and literature

Read both COMPLETE root trackers: proof1.txt blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** and proof2.txt prepublication blob **e5e3084ec9e5a3a31165000d187bf2f824dc658a**. The November 2 five-role governing handoff, current issue #3 including LSPV-5/451 and LSPV-4/510R, AGENTS.md (**19656af10260**), CODEX.md (**754999f50d**), and .codex/skills/pnp-research/SKILL.md (**b8df83a7b0**) were inspected. Root main.tex returned its blob SHA **fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba** but **zero text bytes**, so no safe manuscript mutation was attempted.

Reused, rather than relabelled as novelty: historical calculus declaration in research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob **c87acd11d32c**); /518 strict3 padded opposite-characteristic source; /520 global balanced cancellation schema; /522 exact 18-node vertex Resolution interface; LSPV-5/448 distinct-port repair (research/main/2026-11-08_1752_MAIN_PEER520_ZERO_FACTORY_REFEREE448.md); LSPV-5/449 one-hot adder packet and LSPV-5/450 correction that defining facets are not free SOURCE axioms; LSPV-5/451 articulation correction to /523 (exact indispensable forbidden count $3^{3-c_v}$, not universally nine per vertex). This run supplies the previously missing **local strict-original-source inverse+cancel exact UNIT packet**, not a complete expander refutation or historical checker.

Actual independent Grok review: GROKPROOF/2026-11-08_1130_PROGRESS.md, blob **6942a99f176e**. Actual Claude review: research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex, blob **79e4d4e7e0e3**; the directory was inventoried, not guessed.

Required GitHub corpus inspected by exact file: konard/p-vs-np README.md (blob **0e0ec77f83ad**), proofs/p_not_equal_np/README.md (blob **3a0304116e71**); blkph0x/p-vs-np-proof-research README.md (**f397a7747eac**), METHOD_INDEX.md (**18d693ea71df**); meelgroup/frat-xor README.md (**38a137bca4d4**); openai/math README.md (**cc5b0a03bca6**); anthropics/formal-math eth/README.md (**0b3dcf4a858f**). FRAT-XOR/XLRUP is a different checker language, not R_mix341. The two P-vs-NP repositories disclaim unrestricted resolution. External indexed search read the primary arXiv record and explicit formula for Pang, Cook-Reckhow's 1979 journal article, and established ER literature. A standalone Google-branded portal was unavailable; no Google-branded search or authoritative historical checker execution is claimed.

Primary sources:
1. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, October 24, 2026, Thm 7.2(b), Cor. 7.3, https://arxiv.org/html/2610.00837v2.
2. Stephen A. Cook and Robert Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), pp. 36-50, https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf.
3. Stephen A. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976.
4. Historical frozen R_mix341 prose: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex. Its full accepted-byte grammar and owning facet-selectors remain unspecified.

## ITERATE: exact source, rules, and proof

Let $x_0,x_1,x_2$ be three original indicator variables, and $z$ a global padding bit. The complete local **proper signed strict 3-CNF** source is the seven clauses

$$
(x_0\vee x_1\vee x_2),\quad
(\neg x_i\vee\neg x_j\vee z),\quad
(\neg x_i\vee\neg x_j\vee\neg z)\quad(0\le i<j\le2).
$$

Three ordinary Resolution inferences on $z$ recover the three binary at-most-one clauses. They are not free input clauses. There are six original models, exactly the three one-hot values at both possible $z$ values.

**Separate fixed calculus (ER2-OWNER/524):** A paid definition $q\leftrightarrow(\ell\wedge k)$ has a globally fresh output and two previously known, distinct absolute input IDs. The three owned defining-facet views are $(\neg q\vee\ell)$, $(\neg q\vee k)$, and $(q\vee\neg\ell\vee\neg k)$; they are NOT source axioms, and each definition owner costs one fixed unit. An ordinary binary Resolution inference with correct oriented pivot costs one. Facet views are addressable by owner+selector without an additional cost in this *declared* calculus; whether the historical system provides the same interface or charges applications remains OPEN.

Use the **source-forced zero** definition $t\leftrightarrow(x_0\wedge x_1)$. Two RES steps combining its owned facets with the recovered $(\neg x_0\vee\neg x_1)$ derive $\neg t$. Now introduce three **fresh, different** inverse-port definitions

$$
q_0\leftrightarrow(x_0\wedge\neg t),\quad
q_1\leftrightarrow(x_2\wedge\neg t),\quad
q_2\leftrightarrow(x_1\wedge\neg t).
$$

Each $q_j$ has a distinct absolute ID from its other gate input. Three RES steps derive $(q_j\vee\neg x_{-j})$ from $\neg t$, while the owned forward facets supply $(\neg q_j\vee x_{-j})$. Another three RES steps derive $q_0\vee q_1\vee q_2$ from the original positive source, and six derive all three q-at-most-one clauses. Therefore $q$ is an independently named exact one-hot negative of $x$, not an aliased/illegally duplicated port.

Introduce nine paid term gates $T_{ij}\leftrightarrow(x_i\wedge q_j)$ and, for each $k\in\mathbb F_3$, two paid AND gates implementing the negation of the OR of $T_{ij}$ with $i+j=k$. Total paid definitions: $1+3+9+6=19$.

For $k=0$, each $x_i$ implies its matching term $T_{i,-i}$ (three RES), the original positive ALO implies the disjunction of those terms (three RES), and the defined OR gates provide two local lifting clauses plus three resolutions deriving the exact **unit** that the zero output is true. For each $k=1,2$, the three corresponding off-diagonal terms are false by at-most-one and clone equivalence (three RES per term), and four RES steps per k derive the exact negative nonzero output unit.

**Theorem 524.1 (PROVED/RESTRICTED).** In ER2-OWNER/524, the seven original strict-three clauses have an acyclic shared proof DAG deriving the seven listed interface goals ($q$ one-hot four clauses, three sum-zero units) with

$$
\boxed{19\text{ paid definitions}+54\text{ paid RES}=73\text{ paid distinct nodes}.}
$$

There are exactly 7 original source records, 57 owner-qualified facet views and 54 RES records: 118 explicit clause records in the machine-readable packet. Exact unit targets are $-19$, $21$, and $23$ in its fixed auxiliary-ID allocation. No case splitting, free weakening, hidden raw binary AMOs, assumed source equivalence, or illicit shared-zero tuple occurs. The result gives a legal candidate local macro when **its precise declared** DEF and facet addressing is available; it does not authenticate those features for historical R_mix341.

## Independent replay and hostile controls

The executable deterministic producer and separate independently authored verifier were both executed against **freshly fetched GitHub files**. They agree on the entire 118-line, 19-owner certificate. The independently built verifier performed **160 record/goal/source checks**, replayed 54 correctly oriented RES nodes, reconstructed all 57 facets from their 19 owners, evaluated all 16 original Boolean assignments (6 source models, 10 nonmodels), checked inverse and zero-sum semantics, rejected **five corrupt packets** (pivot, facet, original-source clause, repeated port, altered goal) and **three malformed DIMACS texts** (header, terminator, extra clause). The producer completed its own 129 consistency checks. No authoritative historical checker was run.

**Resource separation.** Logical work 73 (19 DEF, 54 RES), maximal RES-only depth 11; when definition owners are charged and owner dependencies are included, the maximal target critical path is also 11 unit layers in a parallel model with free source availability and zero facet-application cost. This is **not** a claim about realizable machine runtime. The full pretty-printed raw packet occupies exactly 25,770 ASCII bytes, or **206,160 serialized bits**; compact canonical proof formatting could use fewer. The generator performs finite deterministic clause construction and verification; there is no proof search/restarts in the generator. Source/index retrieval, prompt/repository audits, publication, actual serialized output, verifier parsing, object allocation, cache storage and readback are real work not counted in the ideal $W_R$. No native indexed-TM time or all-phase simultaneous peak RSS was measured, so neither is invented. Replicating independently once per edge of a fixed cubic graph has $O(h)$ paid local nodes and $O(h\log h)$ explicit identifier bits, but **does not yet compose the global Tseitin UNSAT refutation**.

## Family/theorem/encoding/known-method/remaining-transfer ledger

| Family and exact source | Known scoped hardness | Legal shortcut tested | Unproved transfer |
|---|---|---|---|
| Pang opposite-characteristic cubic expander $\mathbb F_3$ Tseitin, one-hot: canonical $9h/2$ variables, $24h$ clauses, padded to $9h/2+1$ variables and $57h/2$ proper signed 3-clauses, $N=\Theta(h\log h)$ | Pang Thm 7.2(b), exponential shared-DAG size in fixed-$r$ syntactic $\mathrm{Res}(\mathrm{PC}_r/\mathbb F_2)$, assuming its expander/degree hypotheses, preprint scope | /522 source vertex packet, /449 ownerized adder, THIS /524 strict-original inverse+zero packet, /448 legal zero factories, /520 balanced global cancellation plan, Cook ER, $\mathbb F_3$ algebra | Full LCA propagation/congruence under exact paid semantics; historical R_mix341 owner/facet grammar; all-rule mixed minimum, B3. |
| Odd-charge cubic $\mathbb F_2$ Tseitin, four proper signed 3-clauses per vertex, $3h/2$ edge variables | Exponential ordinary shared-DAG Resolution for certified expander graphs | Historical /341 declared AND3+GF(2) has linear-size derivations in the specified local model | Resolution-only hardness does NOT transfer to mixed R_mix341 or algorithms. |
| Cook PHP | Haken exponential ordinary Resolution in standard encodings | Extended Resolution can refute PHP polynomially | Native rule simulation or all-algorithm separation not supplied. |

**Status / corrective interpretation:** Existing /520 $O(h\log h)$ is a separately declared ER2 **schema** with remaining LCA and parser obligations, not a fully published native R_mix341 certificate. /524 fills one exact bounded-support packet without upgrading /520 to historical acceptance. Existing /523 was narrowed by /451 at articulation vertices, so the nine-per-vertex necessity count is not universally valid. Neither source-essentiality nor local upper proofs imply superpolynomial mixed minimum.

**Remaining precise gaps:** [P2-D1] authoritative frozen byte syntax and owner-qualified DEF facet selectors; [P2-C3] complete paid LCA/group-congruence and authentic historical translation; [P2-B1] superpolynomial $\overline W_{R_{\rm mix341}}$ surviving every native rule; [P2-B2] genuinely noncircular same-fixed-calculus B3. [P1-X1] and Route A remain unchanged. **P versus NP OPEN.**

## Reproducibility artifacts

- experiments/arc/lspv1_524_strict3_inverse_cancellation.js, blob 3fa42e25e02d05b9a915458a7f780e59fd828c12
- experiments/arc/verify_lspv1_524_strict3_inverse_cancellation.js, blob 33d8cba410a784e8a26f38efc7c91b07d06c35ce
- results/raw/arc/2026-11-08_2100_LSPV1_524_STRICT3_INVERSE_CANCEL_RAW.json, blob 5bb75d0e50ed139a0349abe4d2a48569cd91f6f1
- For Node.js replay: node experiments/arc/lspv1_524_strict3_inverse_cancellation.js; node experiments/arc/verify_lspv1_524_strict3_inverse_cancellation.js results/raw/arc/2026-11-08_2100_LSPV1_524_STRICT3_INVERSE_CANCEL_RAW.json.
- Root main.tex not edited because full current bytes were unavailable through the connector; safe ownership-region replacement was impossible.
