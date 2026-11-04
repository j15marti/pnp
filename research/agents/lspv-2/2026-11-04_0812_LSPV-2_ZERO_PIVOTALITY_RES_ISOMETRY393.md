# LSPV-2/393: Duplicate-free pivotality erasure with exact Resolution-cost preservation

**2026-11-04 08:12 PST (America/Los_Angeles).** **PROVED/EXACT** elementary algebraic and ordinary-Resolution theorem (independent specialist referee pending); **COMPUTATIONAL** independent finite enumeration; **KNOWN THEOREM** Haken (1985), Cook (1976), standard Resolution restriction closure; **OPEN** all-rule mixed-cost transfer B1/B2/B3 and P versus NP.

## IDEA -> SEARCH -> ITERATE

**Original hypothesis before literature search.** Every source-clause indispensability argument in a binary-premise source-transparent proof system is capped by the encoded input's source count, $E(F)-1\le m-1\le N-1$. Prediction: even maximal indispensability cannot independently give a superpolynomial worst-case lower bound. The older LSPV-2/341, /389, /390 and LSPV-3/395 already establish this linear ceiling, so this observation is **DUPLICATE**, not a new result.

**Search-driven revision.** LSPV-3/393 already erases singleton pivotality by duplicated labels. LSPV-3/396 proves conservative definitional extensions can collapse ordinary Resolution proof cost. The missing sharper control is an explicit **duplicate-free**, **no-new-definition** representation preserving **exactly the minimum ordinary shared-DAG Resolution count**, while erasing *all* single-clause and single-literal sensitivities. Standard proof restriction closure (Ben-Sasson and Johannsen, IJCAI 2011, Proposition 2 for tree-like Resolution; general DAG case proved below) suggested a solution. Krajíček's *Implicit Proofs* warns that compressed representations constitute a potentially stronger proof system, not free machine execution. GitHub searches under github.com/openai for "resolution proof" found only unrelated mathematical/sheaf uses and UI code, no usable CNF proof checker. Direct Google search was not available; general web-engine searches and connected GitHub code search were used. This negative search result is not a novelty assertion.

## Fixed proof grammar and published hard anchor

Let $R_{\rm Res}$ be strict ordinary binary Resolution over a set of non-tautological explicitly signed CNF source clauses, with source leaves free and each distinct **derived** resolvent node unit-paid; DAG sharing is allowed, no weakening, arbitrary semantic shortcut, algebraic/ER rule, or new definition. This is a subcalculus of, **not a replacement for**, the fixed $R_{\rm mix341}$. For UNSAT $F$, $W_{\rm Res}(F)$ is its globally shortest paid shared-DAG refutation, with perfect free proof selection. Physical proof-byte length, construction and verification are separate.

Haken (1985) proves: for standard **unary** $\mathrm{PHP}_{h+1}^{h}$ with $h(h+1)$ named variables, $m_h=(h+1)+h\binom{h+1}{2}$ original signed clauses and $N_h=\Theta(h^3\log(h+2))$ explicit binary-index encoding bits, there are constants $c>0,h_0$ such that $\forall h\ge h_0$, **every** ordinary unrestricted shared-DAG Resolution refutation has $\ge 2^{ch}$ proof lines. Subtracting $m_h$ source leaves leaves $W_{\rm Res}(\mathrm{PHP}_h)=2^{\Omega(h)}$ paid nodes. This is **not** a lower bound for arbitrary SAT machines, Extended Resolution, Res($\oplus$), or $R_{\rm mix341}$. Cook (1976) constructs polynomial-size Extended Resolution proofs for this exact hard family.

## Theorem 393.1 (duplicate-free, no-gate isometry)

For **every** CNF $F=(C_1,\ldots,C_m)$ on old variables $x_1,\ldots,x_n$, with distinct non-tautological clauses and fresh $z$, define the explicit signed source CNF

$$
H_z(F)=\bigwedge_{i=1}^{m}\left[C_i\land(C_i\lor z)\land(C_i\lor\neg z)\right].
$$

There are no duplicate clauses or tautologies in $H_z(F)$; it contains no defining gate and no added empty clause or contradictory pair of unit clauses not already logically forced. For every old assignment $a$ and **both** $z\in\{0,1\}$,

$$
H_z(F)(a,z)=F(a).
$$

In fact this is a pointwise conservative extension, not merely SAT preservation. Its $3m$ clauses contain $3L+2m$ literal occurrences when $L$ is the number of original occurrences. It is produced uniformly in polynomial bit-time from an explicit signed encoding; $|{\rm enc}\ H_z(F)|=O((N+1)^2)$ is a safe bound including signed names/delimiters.

If $F$ is UNSAT then **no source clause of $H_z(F)$ is indispensable**: deleting any one clause leaves an UNSAT formula. In addition, reversing the polarity of **any one literal occurrence** in $H_z(F)$ also leaves it UNSAT. Thus $E(H_z(F))=L_{\rm sign}(H_z(F))=0$.

Most importantly,

$$
\boxed{\forall F\in{\rm UNSAT}:\quad W_{\rm Res}(H_z(F))=W_{\rm Res}(F).}
$$

**Proof.** The three-clause block is equivalent to $C_i$ for every $z$: the base $C_i$ entails both guarded clauses. Removing either guarded clause leaves $C_i$; removing $C_i$ leaves $(C_i\lor z)\land(C_i\lor\neg z)$, which entails $C_i$ by a single propositional case split. Hence every one-clause deletion preserves the full old formula. If a literal in a guarded clause is flipped, intact original $F$ remains and is UNSAT. If a literal in the base clause is flipped, the two untouched guards still imply its original $C_i$, so UNSAT persists. This proves both spectra vanish.

Since $F\subseteq H_z(F)$ as source clauses, any Resolution refutation of $F$ is valid verbatim for $H_z(F)$, giving $W_{\rm Res}(H_z(F))\le W_{\rm Res}(F)$. Conversely restrict an arbitrary strict Resolution DAG $\pi$ for $H_z(F)$ by $z=0$. Original $C_i$ and $C_i\lor z$ both restrict to $C_i$, while $C_i\lor\neg z$ disappears as satisfied. For a Resolution node, carry a clause subsuming the restricted original line. If its pivot survives in both retained parents, resolve them once; if fixed or absent from a retained parent, reuse the stronger parent. This is topologically valid with DAG sharing and no extra paid node. The terminal empty clause remains empty, giving a strict Resolution refutation of $F$ with at most $|\pi|$ paid derived nodes. Therefore $W_{\rm Res}(F)\le W_{\rm Res}(H_z(F))$ and equality follows. $\square$

**Corollary 393.2 (published hardness retained with zero singleton pivotality).** For Haken's explicit unary pigeonhole family $P_h$, $H_z(P_h)$ is a distinct fully explicit, duplicate-free, pointwise conservative CNF with
$$
E(H_z(P_h))=L_{\rm sign}(H_z(P_h))=0,\qquad
W_{\rm Res}(H_z(P_h))=W_{\rm Res}(P_h)=2^{\Omega(h)},
$$
and $|{\rm enc}\ H_z(P_h)|=h^{O(1)}$. This uses Haken's restriction-specific theorem and Theorem 393.1, **not** an independent new lower bound on arbitrary algorithms. It demonstrates that singleton semantic pivotality can vanish while an established restricted proof minimum remains exactly unchanged.

## Explicit five-inference control and independent checks

Take the inconsistent odd XOR triangle
$$
F_\triangle=(x\lor y)\land(\neg x\lor\neg y)\land(y\lor z)
\land(\neg y\lor\neg z)\land(x\lor z)\land(\neg x\lor\neg z).
$$
A five-step strict Resolution proof derives $(y\lor\neg z)$, $(\neg z)$, $(\neg y\lor z)$, $(z)$, and $\bot$. All six base clauses are indispensable, so the source-ancestry binary-premise lower bound is $6-1=5$; thus $W_{\rm Res}(F_\triangle)=5$. Theorem 393.1 gives $W_{\rm Res}(H_w(F_\triangle))=5$ with 18 distinct non-tautological clauses, zero indispensable clauses and zero single-sign-flip sensitivity. There are 12 original vs 48 padded literal occurrences.

The primary independent Python enumerator exhausted **all 256** subset CNFs over eight canonical two-variable non-tautological clauses (95 SAT, 161 UNSAT). It verified projection equivalence, distinct padded clauses, **3,072** one-source-deletion checks and **4,848** one-occurrence polarity-flip UNSAT checks; 127 UNSAT base formulas had at least one indispensable source. A separately implemented Node.js bitmask enumerator reproduced exactly the same 256/95/161 and 3,072/4,848 counts, zero discrepancies; the two implementations used different truth-evaluation representations. The finite controls are computational evidence, while the all-input result rests on the symbolic proof. No bounded optimizer result is mislabelled global: the triangle's minimum is proved using ancestry plus the explicit proof.

Falsifier F1: one guard alone erases source necessity. **FALSE**: when deleting $C$, $C\lor z$ alone permits setting $z=1$. F2: both guards create a shorter Resolution refutation. **FALSE for all inputs**, by the restriction-isometry proof. F3: the example merely introduces duplicated clauses. **FALSE**: each padded clause has a distinct signed literal set. F4: exact ordinary-Resolution hardness is also full-mixed or all-machine hardness. **FALSE INFERENCE**: ER/Cook, GF(2)/Tseitin and mixed rules are escape controls.

## Resources, representation, bridges

Producing explicit H costs output of $3L+2m$ literals and the name $n+1$; parsing, source indexing, representation conversion, proof materialization, restriction proof reconstruction, bit access, independent checking and output each contribute real time and possible peak space. A conservative upper bound for streaming generation with a buffered input is quadratic bit-time and quadratic total-bit storage, with output size polynomial; no claim of a *lower* machine cost follows. A Resolution proof of $K$ derived nodes can have statement/proof bit-size larger than $K$; all text reads, intermediate lengths and copies must be counted. Arbitrarily long implicit/lazy representations are not excluded; this particular theorem is for explicit signed sources and a *fixed* strict Resolution proof grammar. No exponential output backtranslation or polytime solver is conjured from the isometry.

The fixed project $R_{\rm mix341}$ additionally permits paid AND3, GF(2), conservative DEF and authenticated LOCAL-CONVERT. The restriction normalization has **not** been proved for every mixed rule; equality for $W_{R_{\rm mix341}}$ is **OPEN**, and one must not use Haken to deduce its mixed cost. Even a restricted exponential proof minimum is no machine-time lower bound. B1, B2 and B3 for the unchanged fixed $R_{\rm mix341}$, its superpolynomial $\overline W_R$, and P versus NP are **OPEN**.

## Exact search and review provenance

Initial project query terms: "clause indispensable", "clause replication", "source essentiality disappears", "redundant source padding", "restrict resolution"; project matches LSPV-2/390, /392, LSPV-3/393, /395, /396 and LSPV-1/367 were reviewed. External web queries: "Haken 1985 intractability resolution pigeonhole principle"; "extended resolution polynomial simulations pigeonhole Cook 1976"; "resolution refutations restriction under partial assignment size no increase"; "Krajicek implicit proofs exponentially long polynomial circuits". Sources: Haken, *The Intractability of Resolution*, TCS 39 (1985) 297--308; Cook, *A Short Proof ... Using Extended Resolution*, SIGACT News 8(4) (1976) 28--32; Ben-Sasson and Johannsen, IJCAI 2011, Proposition 2; Krajíček, *Implicit Proofs*, ECCC TR03-055 / JSL 69 (2004) 387--397. Source links: https://cir.nii.ac.jp/crid/1570291225682575744 ; https://dblp.org/rec/journals/sigact/Cook76 ; https://ijcai.org/proceedings/2011/428 ; https://eccc.weizmann.ac.il/eccc-reports/2003/TR03-055/index.html .

Repository file versions actually read: November-2 refocus latest blob (via connector); AGENTS.md \`19656af1\`; CODEX.md \`754999f5\`; pnp-research skill \`b8df83a7\`; LSPV-2/392 \`bbdfe936\`; LSPV-3/393 handoff \`954f78d0\`; LSPV-3/396 \`43d6e5fd\`; LSPV-1/367 \`64f4e87a\`; Grok \`GROKPROOF/2026-11-04_0615_PROGRESS.md\` blob \`6603e613\`; Claude \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\` blob \`1f9fc727\` and \`2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\` blob \`9a5b05d6\`; issue #3 newest comments and current role handoffs. Their restrictions are respected; none supplies B3. Other-agent assessments are not authority for promoting an unproved transfer.

## Next exact obligation

Test whether a **source-block** hitting-set invariant has a representation-stable polynomial-cost normalization under *every* legal paid GF(2)/LOCAL-CONVERT/DEF transition in the **same** Rmix341; require a proved translation and prohibit free input recoding. If not, publish a specific legal counterexample. The one-step criticality and singleton pivotality metrics are retired as candidate intrinsic machine-hardness measures. **P versus NP remains OPEN.**