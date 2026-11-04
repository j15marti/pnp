# LSPV-2/377: Uniform length-preserving proof-cost noninvariance

**November 3, 2026, 19:09 PST.** Role: PNP SAT-Circuit Reduction Builder. Status: **PROVED/EXACT** for the declared syntactic involution and ordinary-Resolution separation, independent specialist review pending; **COMPUTATIONAL** finite controls; Haken/Cook **KNOWN THEOREM**; full mixed proof-hardness, B1/B2/B3 and P versus NP **OPEN**.

## Published hard-family anchor and exact model

Let $P_h=\mathrm{PHP}_{h+1}^{h}$ be the canonical unary pigeonhole CNF: $v_h=h(h+1)$ variables $x_{i,j}$, $h+1$ occupancy clauses $\bigvee_{j=1}^h x_{i,j}$ and $h\binom{h+1}{2}$ collision clauses $\neg x_{i,j}\vee\neg x_{k,j}$. Set $m_h=(h+1)+h\binom{h+1}{2}$. Signed source clauses are encoded explicitly in ASCII DIMACS, with legal comment lines; size is $\Theta(h^3\log(h+2))$ bytes.

**Haken (1985):** There are constants $c>0,h_0$ such that, for **every** $h\ge h_0$, **every** unrestricted shared-DAG ordinary Resolution refutation of $P_h$ has at least $2^{ch}$ total lines. Original clauses are free sources in our unit-paid derived-resolvent convention, yielding $W_{\mathrm{Res}}(P_h)\ge2^{ch}-m_h=2^{\Omega(h)}$. The theorem is *not* for Extended Resolution, Res($\oplus$), the fixed full mixed $R_{\mathrm{mix341}}$, or unrestricted uniform SAT machines. Cook (1976) gave polynomial Extended Resolution PHP proofs. The mandatory odd cubic Tseitin countercontrol has an independently certified $4h-1$ mixed GF(2) proof despite exponential ordinary Resolution hardness.

The preselected **Rmix341 remains unchanged**: authenticated source clauses and unit-paid RES, AND3, GF(2), locally checked LOCAL-CONVERT and conservative binary DEF with shared DAGs. This run proves a representation-invariance obstruction for **ordinary Resolution**, not a lower bound on the full Rmix341.

## Four falsifiers

1. A uniform, invertible, length-preserving, label-preserving efficient recoding must preserve ordinary-Resolution proof cost up to polynomial factors: **FALSIFIED**.
2. It can preserve source-clause count, declared-variable count, source distinctness and bit length simultaneously: **PROVED**.
3. The recoding is a freely justified same-source proof step, or establishes B3: **FALSIFIED as an inference**. New clauses require authenticated, charged construction.
4. This refutes *every* physically charged, source-rooted algorithm-invariant: **NOT ESTABLISHED**.

## New theorem

There is **one fixed**, total, uniform polynomial-time involution $E:\{0,1\}^*\to\{0,1\}^*$, preserving encoded bit length and SAT/UNSAT/malformed status, and pairs of valid UNSAT CNFs $X_h,Y_h$ for every $h\ge1$ such that $E(X_h)=Y_h$, $E(Y_h)=X_h$ and both have exactly $v_h$ declared variables, $m_h$ proper pairwise-distinct source clauses, and equal explicit encoded length $N_h=\Theta(h^3\log(h+2))$. But for sufficiently large $h$,

$$
W_{\mathrm{Res}}(X_h)=2^{\Omega(h)},\qquad W_{\mathrm{Res}}(Y_h)=1.
$$

**Proof.** Take $X_h$ to be canonical unary PHP in a deterministic clause ordering. Construct $Y_h$ from the contradictory source units $(x_1)$, $(\neg x_1)$ and the first $m_h-2$ distinct positive binary clauses $(x_a\vee x_b)$ for $1\le a<b\le v_h$ in lexicographic order. There are enough because $\binom{v_h}{2}\ge m_h-2$ for every $h\ge1$. All clauses are nonempty, non-tautological and pairwise different. Both formulas are UNSAT; $Y_h$ has an exact one-RES-node refutation using its two opposing units.

Serialize unpadded clause lists as ASCII DIMACS strings $x_h,y_h$, with the *same* header specifying $v_h,m_h$. Choose $N_h=|x_h|+|y_h|+8$ bytes. Prepend one standard DIMACS comment line starting with c X to $x_h$, and a line starting with c Y to $y_h$, padding each with filler characters to exactly $N_h$ bytes. Such comments do not change semantics or Resolution inference counts. The $N_h$ are strictly increasing and have the stated asymptotic size.

On arbitrary binary input $z$, enumerate the lengths $N_h$ until they reach or exceed $|z|$. If one matches, regenerate $X_h,Y_h$ and exchange them only when the input matches one exactly; otherwise return $z$. On non-byte-aligned bitstrings take the identity. This is **one fixed all-input program**, not different advice per $h$; it uses only byte comparisons and construction of known clauses, not an UNSAT oracle. Both swapped inputs are UNSAT, so SAT and malformed inputs remain unchanged. The map is a total label-preserving involution. At most $O(N)$ candidates, each of at most $O(N)$ bytes, are examined, giving conservative $O(N^2)$ bit-time and $O(N)$ peak space. Materializing any changed output itself requires $\Omega(N)$ bit writes. Haken's bound applies unchanged to $X_h$ because comments have no proof significance; $Y_h$ has exact paid cost one. QED.

**Invariant corollary.** If $I(F)\ge0$ is invariant under *all* such uniform efficient length-preserving label-preserving bijections, and satisfies $I(F)\le W_{\mathrm{Res}}(F)$ on all UNSAT source presentations, then

$$
I(X_h)=I(Y_h)\le W_{\mathrm{Res}}(Y_h)=1.
$$

It therefore cannot encode the published exponential ordinary-Resolution lower bound. This does not rule out a source-authenticated invariant that *charges* the transformation and is proved to reflect actual uniform-machine work.

## Independent executable checks and scope

The full local Node producer checked $h=1..5$, exact headers/lengths, proper distinct clauses, the involution, unrelated valid SAT/UNSAT and malformed-string identity, and exhaustive SAT/UNSAT and all original occurrence-sign flip SAT controls for $h=1..3$: **151 assertions**, including **70** SAT sign flips. A separately authored Python implementation independently parsed the generated strings, validated source structures and the involution for $h=1..8$, checked both labels and all sign-flip neighbors for $h\le3$, and passed **6,572 assertions**. Larger $h$ were not exhaustively enumerated. The public, compact JS reproducer independently replayed after GitHub readback, **111 assertions PASS**. None of these finite checks re-proves Haken or certifies a full-R shortest derivation. The complete producer, full independent verifier and raw results are separately preserved in the accompanying reproducibility archive.

Work ledger: actual CNF bytes, construction, comparison, output, source reading, checking and peak space are charged. $O(N^2)$ work and $O(N)$ live bytes are **upper** estimates for this explicit recoding, not SAT decision lower bounds. Exponential intermediate states are legal but unnecessary here; compact representation alternatives are included. The all-phase space guard $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$ is not altered.

**Classification:** family/representation-transfer failure for ordinary Resolution, **not** a B2 or B3 failure. The recoding changes authenticated source clauses and is not a free Rmix341 inference. A uniform special-case PHP recognizer with complete exponential fallback is consistent with Haken and with worst-case general-SAT hardness. No unrestricted all-algorithm lower bound follows.

## Reconciliation, actual Grok/Claude paths, and next gap

Read the Nov 2 12:04 five-role refocus, issue #3, AGENTS.md, CODEX.md, repository pnp-research skill, original LSPV-2/341, /375 and /376, LSPV-1 root semantic handoff376, LSPV-4 PHP sign-probe373, LSPV-5 semantic quotient REFEREE323 and minimax REFEREE326. Earlier LSPV-2/375 established a non-bijective, source-preserving prefix compressor; LSPV-5/323 already established pure semantic quotient collapse. The increment here is a fully **involutive**, equal-length, equal-$n$, equal-$m$, duplicate-free syntactic collapse anchored in Haken's existing hard family, not a new hardness theorem.

The **actual Grok path** reviewed is GROKPROOF/2026-11-04_0116_PROGRESS.md (blob ca5a835356eb918b8cb4ab94d14de6174edeab03). Its universal, all-input, fully charged ARC contraction remains OPEN. The **actual Claude path** reviewed is research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67). Its portfolio/alternation-trading conclusions apply to declared proof rules, not fixed-R B3. GitHub/OpenAI code search did not surface an authoritative fixed-R verifier; no novelty is inferred from absent results.

Root main.tex fetch returned **zero content** with nonempty SHA 3be075c8659e174afd239b8432e90a40c9eba230; no unsafe overwrite was attempted. Full checkout preflight unavailable in this runtime. All tasks, enabled states, titles, five roles, calendars and original weights remain unchanged.

**Next exact task:** define a *source-rooted*, representation-conversion-charged invariant for the fixed full calculus, test compact circuit/affine/DEF/LOCAL-CONVERT counterexamples, then independently prove or refute the weakest sufficient B3 implication:

$$
\mathrm{SAT}\in P\implies \overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$

B1/B2/B3, superpolynomial full-R minima, and P versus NP remain **OPEN**.

## References

[1] Haken A. The Intractability of Resolution. Theoretical Computer Science. 1985;39:297-308. DOI 10.1016/0304-3975(85)90144-6.

[2] Cook SA. A Short Proof of the Pigeon Hole Principle Using Extended Resolution. SIGACT News. 1976;8(4):28-32.

[3] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. J Symbolic Logic. 1979;44:36-50.

[4] Urquhart A. Hard Examples for Resolution. JACM. 1987;34:209-219.
