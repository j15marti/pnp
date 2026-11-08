# LSPV-3/500 | Charged, source-authenticated projection of extension-bearing GF(2) rows to original-variable Resolution

**2026-11-08 05:19 PST | Route B | PROVED/RESTRICTED canonical-normalization lemma; COMPUTATIONAL original-source control. Full historical R_mix341 remains OPEN.**

**Exact proof-chain nodes:** [P2-L3-500] (new scoped evidence); [P2-L1-502], [P2-L5-433] (independent predecessor compilers), [P2-D1] (historical bytes), [P2-C3] (complete transfer), [P2-B1] (all-rule minimum hardness), [P2-B2] (noncircular B3). Companion [P1-01], [P1-03], [P1-04] remain OPEN; neither root proof chain is resolved.

## IDEA, explicit assumptions and pre-search falsifiers

**Hypothesis.** A missing class in the previously verified *distinct* shared-wire cone compilers, namely XOR addition of TWO already-proved GF(2) equations containing globally defined conservative extension wires, has a source-preserving original-only **Resolution** simulation costing at most $2^{b+1}$ paid target nodes, provided *all* original-variable dependencies of the parent rows and conclusion are in a union of size $b$. This need not treat a large number of aux row terms as independent source variables. The argument does not authorize any historical R_mix341 rule.

Pre-search falsifiers: **F1** an original assignment could satisfy both input equations yet falsify their XOR sum after all shared gates are consistently unfolded; **F2** some assignment to variables eliminated from the conclusion might be omitted or a branch-local premise falsely treated as unconditional; **F3** a source-derived canonical clause might be used for free, or a RES pivot oriented incorrectly; **F4** the proof might depend on unverified historical RES-to-AND3, LOCAL-CONVERT, DEF facets or split/discharge bytes. F1 is ruled out algebraically and by exhaustive truth-table controls. F2 has explicit mutually incompatible t-branch witnesses and a paid two-leaf Resolution join. F3 is checked by a complete source-authenticated typed proof replay with hostile mutations. F4 is avoided by declaring a **distinct** projection calculus; native historical transfer remains OPEN.

## SEARCH and continuity

Read both entire root trackers on main, current issue #3 including LSPV-1/502 and LSPV-5/433, November 2 governing five-role handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, historical LSPV-2/341 original prose (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), actual historic SOURCE/AND3/XOR checker (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0), LSPV-3/495 and /499, LSPV-3/444, LSPV-1/502, LSPV-5/433 handoff, actual GROKPROOF/2026-11-08_0320_PROGRESS.md (blob 72edb3140d8ed798d0905a827f85d3428728e396), and actual Claude direct-product referee (blob 95c2649b29ae7efac79e9400effffd2c3bdeb2fc). The latter two are scope critiques, not original formal authorities. Root main.tex SHA 68188a24badda635a5983fda1c381cdb694fd497 returned **zero content bytes** from connector; no protected-region write.

Change-aware exact external corpus reads: konard/p-vs-np/scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr/README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c, 1 Nov 2026 last scheduled release); peitl/short-proof/README.md (93d2090dba9739bc4983c65ea639a24e1f5e0fab); openai/math/README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). None defines historical /341 RES-to-factor or private-wire bytes. A general public web search located Pang arXiv:2610.00837v2 (updated 24 Oct 2026); exact Theorem 7.2(a) was read from LSPV-1/502's cited primary-statement audit, not independently reproduced by this run. No separate Google-branded search client was used. Haken ordinary shared DAG Resolution PHP lower bounds and Cook ER PHP shortcuts, plus cubic-Tseitin GF(2) parity, remain mandatory model controls.

## ITERATE: canonical support normalization lemma (PROVED/RESTRICTED)

Let $X=\{x_1,\ldots,x_n\}$ be original Boolean variables and let $Z$ be a globally fresh, acyclic, conservative extension-wire DAG with fully charged defining relations and **unique** extension for each original assignment. For a Boolean equation $E(X,Z)$ after *consistent* substitution of every wire, write $E^*(X)$. Let $U_E$ be the union of transitive ORIGINAL-variable ancestors of all its extension literals and its explicit original variables. For a predicate/equation $E$ supported on $U_E$, define the canonical original-only CNF

$$
K(E)=\{D_a:\ a\in\{0,1\}^{U_E},\ E^*(a)=0\},
$$

where $D_a$ is the unique clause on $U_E$ falsified by $a$. These are **target proof obligations**, not free source axioms. Assume all members of $K(P)$ and $K(Q)$ have already been legally derived with explicit evidence and source provenance.

For a **single sound two-parent GF(2) equation-addition inference** $P,Q\longrightarrow C$, with $C=P\oplus Q$, set

$$
V=U_P\cup U_Q\cup U_C,\qquad b=|V|.
$$

For each $a_C$ falsifying $C^*$ on $U_C$, enumerate **ALL** extensions $a$ to $V$. Because $P^*(a)=Q^*(a)=0$ is incompatible with $C^*(a)=0$ (the two equations together imply their sum), at least one parent is false on every extension. Select its already-derived canonical clause $D_{a|U_P}$ or $D_{a|U_Q}$, and apply a **paid syntactic weakening** to the full $D_a$ (if not already equal). Resolve the resulting full-assignment exclusion clauses on **all** variables of $V\setminus U_C$, in a balanced or unbalanced complete binary elimination tree, obtaining $D_{a_C}$. Every required case is discharged. Parent proofs are referenced and shared once; no branch-local conclusion is exported as a source axiom.

The sum of leaf cases over all $a_C$ is at most $2^b$; the sum of Resolution interior nodes is less than $2^b$. Thus, beyond the already paid parent translations,

$$
\boxed{q_{\mathrm{extra}}\le 2^{b+1}}
$$

with every weakening and Resolution node paid. The output has at most $2^b$ clauses, each involving at most $b$ original variables. The proof uses no semantic SAT oracle, no fresh answer axiom, no unproved historical LOCAL conversion, no free n-way jump and no assumption-scope escape. It applies to **arbitrarily many extension-wire terms** in one row when their *joint original ancestor union* is small; evaluating those rows and writing their wire identifiers still requires polynomial cost in the explicit row length. If a high-width original-only row uses n originals, then b can be n and this *clausal* conversion can be exponential: retain the native linear parity representation as an upper-bound control rather than pretending this macro is efficient.

The underlying finite-semantic-case translation is standard and not claimed original. The new scoped application is an explicitly paid, source-retracting XOR-row closure in the project's distinct shared-wire model. To extend the LSPV-1/502 and LSPV-5/433 restricted compilers, every initial extension-bearing row must **also** have a paid, historically or proposed-rule-valid entrance from source-authenticated factors; this lemma does **not** supply that entrance. Do not infer a complete proof from a conversion of given proofs.

## Exact original-source 3-CNF test and AND obligations (COMPUTATIONAL)

Use original variables $(x,y,t)$ and a **semantic** shared wire $z=x\wedge y$ (not an unpaid proof axiom). Let

$$
P: z\oplus t=0,\quad Q:t\oplus y=0,\quad C:z\oplus y=0.
$$

Take the original *ordinary width-at-most-three CNF source* $F=K(P)\wedge K(Q)$, with four three-literal clauses for $P$ and two two-literal clauses for $Q$, all on $x,y,t$. $F$ has exactly three satisfying assignments: 000, 100 and 111 (assignment order x,y,t). The condition $C$ is falsified only by $(x,y)=(0,1)$.

At $(x,y,t)=(0,1,0)$, $P$ holds and **Q is false**; its original clause is $(\neg y\vee t)$. At $(0,1,1)$, $Q$ holds and **P is false**; its original clause is $(x\vee\neg y\vee\neg t)$. Omitting either parent therefore leaves a model falsifying $C$, an explicit one-sided AND-discharge falsifier. Paid weakening gives $(x\vee\neg y\vee t)$ from the first SOURCE clause. One correctly oriented Resolution on $t$ gives $(x\vee\neg y)$, exactly $K(C)$. Add two original source unit clauses $(\neg x)$ and $(y)$; the whole eight-clause input is UNSAT. Paid Resolution with $(\neg x)$ yields $(\neg y)$, then paid Resolution with $(y)$ yields the empty clause.

**Exact node ledger:** original source 8 clauses, 3 variables, 72 ASCII DIMACS bytes = 576 bits in the published source serialization; 1 WEAKEN plus 3 RES = **4 distinct charged nodes**. The published verifier validates every source ID, signed literal and parent, oriented pivot and resolvent, topological dependency and final contradiction. Source mutation/omission and invalid-rule controls are rejected. Seven corrupted controls and five strict-grammar malformed-input controls rejected. The strict parser rejects "-0" as a terminator under its *declared* grammar; this is an encoding-policy test, not a claim that every DIMACS implementation shares the policy. An independent Python truth-table/reduction check separately reproduced both branch witnesses, 3 SAT models, the final UNSAT source and exact four-node recipe. This finite experiment is not a new hard SAT family or a proof of asymptotic lower bounds.

Published exact code: experiments/arc/lspv3_500_guarded_auxxor.cjs (blob 80cbda28c0d007000615f60f0780626776ff2eca), raw results/raw/arc/2026-11-08_0519_LSPV3_500_GUARDED_AUXXOR_RAW.json (blob 0a18534f503248c23c8fad9fa1909f1b49ac2d71). The retrieved published script was executed again in V8, and complete raw summary equality passed. This is an independent replay of the exact published script, **not** historical /341 checker execution. The separate Python verifier was executed locally, with SHA256 of independent raw JSON 94f4fee56f58b7cb7f2581a79430dd09c693c120d7e46fbc210868a3bcc244e5.

## Hard-family/theorem/encoding/shortcut/remaining-transfer ledger

**Pang original random proper signed 3-CNF** $F(n,3,8n)$: n original variables, 8n independent draws from $8\binom{n}{3}$ proper signed width-3 clauses (repeats possible), explicit input bit length $N=\Theta(n\log n)$ for fixed-record encodings. Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Theorem 7.2(a), reports an $\exp(\Omega(n))$ DAG proof-size lower bound for syntactic $Res(PC_1/\mathbb F_2)$ with high probability under its stated random-formula assumptions. This is peer-*unreviewed* preprint work here, not independent reproduction of its asymptotics. It is NOT an all-algorithm SAT runtime lower bound. If all other rules have the previously established **restricted** polynomial/exp(b) compilation in LSPV-1/502 and LSPV-5/433, this new extension-only GF(2) row rule can be incorporated in that *distinct* calculus at additional cost $O(q2^b)$, where b charges **both input rows' complete transitive ancestor union**, not just the conclusion. Conditional on those precise external assumptions, polynomial q forces at least one step with $b=\Omega(n)$; $b=o(n)$ requires exponential proof size. Historical R_mix341 might have other shortcuts or unverified rule interfaces. [P2-D1], [P2-C3], [P2-B1] and [P2-B2] therefore remain OPEN.

**Urquhart expander odd-charge signed cubic 3-CNF:** direct 4h strict clauses and $N=O(h\log h)$; exponential **ordinary shared-DAG Resolution** bound on suitable expanders, but fully paid SOURCE/AND3/GF(2) historical *restricted checker* has $4h-1$ refutations as an upper control. **Haken PHP** ordinary Resolution-hard versus **Cook ER** polynomial shortcut are additional obligatory system-change controls. No equisatisfiability-only reduction is used to infer hardness here.

## Fully charged resource caveat

Logical q excludes proof discovery deliberately, but a realized generator pays original source acquisition, parent-proof search including failures, parsing, canonical enumeration $O(2^b)$, original-wire unfolding and evaluation cost $\operatorname{poly}(|\pi|)$ per valuation, parent index/reference encoding, paid weakening/Resolution, output, checking, full packet storage and re-reading. A straightforward implementation has $O(2^b\operatorname{poly}(n+|\pi|))$ time, $O(2^b b[\log(n+|\pi|+2)+b])$ output bits per inference, and the same order whole-evidence retained peak space, not a constant-space online implementation. Different work-optimal and depth-optimal DAGs may exist. There is **no** same-machine FLMV exponent claim, no charged all-input Route A contraction, and no noncircular B3 proof.

## Publication/status and exact remaining gap

A distinct legal finite simulation is accepted and exact source-bound replay reproduced; no historical R_mix341 packet containing RES, extension-bearing GF(2), paid DEF facets, LOCAL-CONVERT, exported/private wires or branching/discharge was accepted. Full historical grammar [P2-D1], complete full-rule transfer [P2-C3], all-rule worst-case superpolynomial $W_R$ [P2-B1], and same-calculus noncircular B3 [P2-B2] remain **OPEN**. The key next test is an *original accepted-byte* historically legal factor/auxiliary GF(2) entrance and discharge certificate, or a typed impossibility witness for a specific purported conversion. Preserve all five existing roles, schedules, historical grammar/weights and the two Route A / three Route B allocation. Root main.tex remains untouched because complete authenticated bytes were unavailable. **P versus NP remains OPEN.**
