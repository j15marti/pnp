# REFEREE376: strict-3-CNF reflection wrapper and the existential-B3 quantifier firewall

**November 5, 2026, 19:58 PST. LSPV-5 Independent Proof Red Team, Route B.**

**Status.** **PROVED/EXACT, under the stated standard arithmetization hypotheses:** a fixed sufficiently strong, consistent, feasibly axiomatized theory cannot prove even one-sided rejection soundness for every externally correct polynomial-time SAT decider. **COMPUTATIONAL:** an independently replayed finite strict-3-CNF illustration. **DUPLICATION CORRECTION:** the initial diagonal idea was already present in LSPV-1/357; it is not new. This run's scoped increment is an explicit original-byte strict-3-CNF Tseitin instantiation, a full runtime/malformed-input audit, and an exact proof that this diagonal does **not** refute the weakest existential B3 implication. Historical `R_mix341` selector bytes, all-rule normalization, superpolynomial full-mixed $\overline W_R$, B1/B2/B3, and P versus NP remain **OPEN**.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

Hypothesis: a B3 bridge requiring one fixed arithmetic theory $T$ to prove correctness of **every** correct polynomial SAT decider fails by a proof-triggered wrapper. Falsifiers were:

1. the proof check or special-source recognition costs superpolynomial time;
2. no polynomially recognizable family of valid strict 3-CNFs supplies a uniform, theory-provable SAT witness;
3. correctness of the wrapped machine does not imply $\operatorname{Con}(T)$ inside $T$;
4. weakest B3 actually quantifies over every decider code, so one unprovable correct wrapper would refute it.

### Search and duplication discovery

Read the governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3 through LSPV-3/437 and LSPV-1/432, native source `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, REFEREE375, actual `GROKPROOF/2026-11-06_0215_PROGRESS.md` blob `eae7e6c9ce0d6d82b8da0e21db30aaa5fcf0c5f9`, and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`.

Project search found the decisive prior art: `research/coordination/2026-11-03_0032_LSPV1_GODEL_REFLECTION_B3_FIREWALL357_FIVE_ROLE_HANDOFF.md`. LSPV-1/357 already constructs a correct polynomial decider whose rejection soundness is unprovable in a fixed consistent $T$, and already states the existential escape: B3 could use one specially selected, provably sound decider. The initial theorem is therefore **duplicated**, not a new result.

Primary literature actually read or inspected:

- Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), especially the distinction between a polynomially bounded proof system and an arbitrary fixed system;
- Krajicek--Pudlak, *Propositional Proof Systems, the Consistency of First Order Theories and the Complexity of Computations*, JSL 54 (1989), author-hosted scan `scan10.pdf`, relating finite consistency statements and proof-system optimality;
- Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), exponential Resolution length on Tseitin expander formulas;
- Ben-Sasson--Wigderson, *Short Proofs Are Narrow—Resolution Made Simple*, JACM 48 (2001), Definition 4.1 and Lemma 4.2 for Tseitin CNFs and width-to-size transfer.

Actual indexed queries included `Gödel second incompleteness theory proves correctness every polynomial time SAT algorithm reflection proof complexity`, `Cook Reckhow proof systems feasible reflection Krajicek Pudlak primary paper PDF`, `Urquhart 1987 hard examples resolution Tseitin graph exponential lower bound JACM PDF`, and `Ben-Sasson Wigderson short proofs narrow resolution Tseitin expander primary paper PDF`. A direct Google-branded interface was unavailable; indexed web search was used and no claim of direct Google access is made.

Change-aware GitHub review found unchanged heads: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`, and `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`. Files inspected included `konard/p-vs-np/proofs/complexity/README.md`, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md`, `meelgroup/frat-xor/format.md`, and `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`. They provide useful verifier, certificate, and charged-execution precedents but no same-`R_mix341` B3 theorem.

### Revised target

The revised target is narrower and falsifiable: independently instantiate the LSPV-1/357 firewall with exact proper strict-3-CNF sources taken from the established Tseitin encoding, bind all claims to actual source bytes, and prove the **quantifier nonconsequence** that the construction blocks universal per-program reflection but leaves existential B3 untouched.

## Exact strict-3-CNF code family

Let $K_4$ have edge variables in the order

$$
(x_{01},x_{02},x_{03},x_{12},x_{13},x_{23}).
$$

At each vertex impose even parity on its three incident edges. Encode a three-variable parity row by the four width-three clauses falsified exactly by the four assignments of the opposite parity. Thus one even-charge block has six variables and sixteen proper width-three clauses, and the all-zero assignment satisfies it.

For each nonempty bit string $p=p_1\ldots p_k$, form $S_p$ from $k$ disjoint even-charge $K_4$ blocks using fresh consecutive variables. In block $i$, retain canonical clause order when $p_i=0$ and swap the first two distinct clauses when $p_i=1$. Clause order is part of the authenticated DIMACS byte source but does not change the CNF semantics. Consequently:

- $S_p$ has exactly $6k$ variables and $16k$ proper strict-3 clauses;
- its binary/ASCII encoded length is $\Theta(k\log(k+2))$;
- it is recognized and $p$ is recovered in time linear in its source length;
- the all-zero assignment is a uniform satisfying witness provable by a very weak arithmetic theory;
- distinct $p$ give distinct source bytes without changing satisfiability.

This is a validation/control family derived from the established Tseitin encoding. It is **not** a new hard family.

## The scoped reflection theorem

### Assumptions

Let $T$ be a consistent arithmetical theory satisfying the usual derivability conditions for Godel's second incompleteness theorem. Assume:

1. $T$ has a deterministic proof predicate $V_T(p)$ for proofs of $0=1$ decidable in time polynomial in $|p|$ (a feasibly axiomatized theory);
2. $T$ formalizes the elementary DIMACS parser, the $S_p$ generator, the all-zero witness check, and the finite computation of the machine below;
3. $D$ is any externally total correct polynomial-time decider for binary-encoded CNF-SAT with a distinct `MALFORMED` response.

The polynomial proof-predicate assumption is essential to the polynomial wrapper. For a merely recursively axiomatized theory the same computability diagonal can be written, but the claimed polynomial runtime need not follow.

### Construction

Define $D_T$ on binary input $x$:

1. parse $x$; malformed inputs are handled exactly as by $D$;
2. if $x$ is exactly $S_p$ for some nonempty $p$, run $V_T(p)$ and return `UNSAT` if it accepts, otherwise return `SAT`;
3. on every other well-formed source, return $D(x)$.

Recognition costs $O(|x|)$ and $|p|=O(|x|)$. Hence if $V_T$ and $D$ are polynomial-time, so is $D_T$. No semantic oracle, optimizer, proof search, or `R_mix341` inference is used.

### Theorem 376.1 (strict-3 reflection firewall; scoped instantiation of LSPV-1/357)

Under the assumptions above:

1. externally, if $T$ is consistent, $D_T$ is total, polynomial-time, correct on SAT/UNSAT/malformed encodings, and extensionally equal to $D$;
2. within $T$, one-sided rejection soundness of $D_T$ implies $\operatorname{Con}(T)$;
3. therefore, if $T$ is consistent, $T$ does not prove one-sided rejection soundness of $D_T$, and a fortiori does not prove its full correctness.

**Proof.** If $T$ is consistent, no string $p$ is accepted by $V_T$. Every special input $S_p$ is therefore labelled `SAT`, which is correct by the explicit all-zero witness; all other inputs follow $D$. Runtime and malformed handling were established above.

Let `RejectSound($D_T$)` state that for every well-formed source $F$ and assignment $a$, if $a$ satisfies $F$, then $D_T(F)$ does not return `UNSAT`. The generator and machine computation are elementary enough for $T$ to prove, uniformly in $p$,

$$
V_T(p)=1\quad\Longrightarrow\quad
\bigl(0^{6|p|}\models S_p\ \wedge\ D_T(S_p)=\texttt{UNSAT}\bigr).
$$

Thus $T$ proves

$$
\operatorname{RejectSound}(D_T)\ \Longrightarrow\
\forall p\,V_T(p)\ne1,
$$

and the right side is the standard consistency statement $\operatorname{Con}(T)$. By Godel's second incompleteness theorem, a consistent $T$ satisfying the stated hypotheses does not prove $\operatorname{Con}(T)$; hence it cannot prove `RejectSound($D_T$)`. Full correctness implies rejection soundness, so it is unprovable as well. QED.

This proof discharges falsifiers 1--3 under explicit hypotheses. It does not smuggle the correctness of $D$ into the internal argument: the implication to consistency uses only the special $S_p$ branch and its fixed witness.

## The exact B3 quantifier audit

The result above does **not** refute B1, B2, or B3 and does not exhibit a formula with a long `R_mix341` proof.

The weakest target is

$$
\mathrm{SAT}\in\mathrm P\quad\Longrightarrow\quad
\exists C,k\ \forall N:\ \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

Its antecedent says that **some** correct polynomial decider exists. The conclusion mentions only the fixed calculus and source formulas; it does not quantify over decider programs or require $T$ to prove their correctness. If $D$ witnesses SAT in P, the externally equal $D_T$ is another witness, but the unprovability of `RejectSound($D_T$)` does not rule out:

- a different correct polynomial decider $D_0$ whose needed soundness is provable in $T$;
- a direct rule-specific proof of polynomial `R_mix341` refutations that uses no formalized decider correctness;
- a proof in a different sound theory;
- a semantic argument later compiled by an independently authenticated native translation.

Therefore the construction falsifies only the bridge schema

> “For one fixed $T$, every externally correct polynomial SAT decider has $T$-provable rejection soundness, and this proof is then compiled into `R_mix341`."

It does **not** falsify the weaker schema “if SAT is in P, select one suitable decider and establish a rule-specific native simulation.” The latter still bears the noncircular obligations identified by LSPV-1/357: existence of a suitably provable decider, bounded-arithmetic reflection, and an authenticated polynomial EF/ER-to-historical-`R_mix341` compiler.

This also answers falsifier 4: B3 is existential at the machine level, not universal over program codes. Promoting the firewall into a B3 refutation would be a quantifier error.

## Established family / theorem / model / shortcut ledger

| Family | Exact encoding and size | Established theorem and exact model | Known legal shortcut/control | Remaining transfer |
| --- | --- | --- | --- | --- |
| Cubic-expander odd Tseitin | One variable per edge; four proper signed width-three blockers per degree-three vertex. For $h$ vertices: $3h/2$ variables, $4h$ clauses, encoded length $\Theta(h\log(h+2))$. | Urquhart 1987 and Ben-Sasson--Wigderson 2001: $2^{\Omega(h)}$ length for ordinary unrestricted shared-DAG Resolution on suitable expander sequences. This is proof size in Resolution, not arbitrary SAT-machine time. | Historical `/341` declares a $4h-1$ AND3/GF(2) refutation and binary-premise source-capacity lower bound for connected bridgeless cubic instances. | Ordinary Resolution hardness fails to transfer to the full mixed calculus; this family supplies a linear mixed upper bound, not a superpolynomial $\overline W_R$. |
| Disjoint even-charge $K_4$ blocks $S_p$ | $6|p|$ variables, $16|p|$ proper width-three clauses; actual source order carries $p$; all-zero witness. | Elementary SAT control, not an asymptotic hardness theorem. | Direct witness; no branching or algebra needed. | Used only to expose the reflection quantifier. It proves nothing about `R_mix341` minimum cost. |
| Odd-charge $K_4$ | Six variables, sixteen proper width-three clauses. | Exact finite UNSAT by XOR of the four vertex equations; finite exhaustive control here. | The `/341` mixed proof uses 15 paid nodes; no asymptotic inference. | Finite correctness control only. |

Haken's PHP ordinary Resolution lower bound and Cook's Extended Resolution shortcut remain mandatory controls, but PHP is not natively proper strict 3-CNF. Equisatisfiable width reduction alone does not preserve a lower bound in the required direction, so no PHP-to-strict3 mixed-system transfer is claimed.

## Branching/shared-DAG scope and historical grammar

Native `/341` contains RES, AND3, XOR, LOCAL-CONVERT, and paid conservative two-input DEF. It does not declare a free case-split/discharge rule. This run adds none. A branching proof under assumptions requires both children for an UNSAT split and may share only nodes whose contexts are justified; compiling such a proof into Resolution is a separate theorem. The reflection wrapper is a machine program, not a branching proof DAG and not an accepted native certificate.

The historical source leaves exact exported/private wire selectors and some byte grammar unspecified. Nothing here repairs or assumes those selectors. LSPV-3/437's one-wire global entailment is correctly rejected as an illegal LOCAL step; REFEREE375's selector isometry and scoped DEF repair remain conditional on declared views. No accepted trace bytes are claimed in this run.

## Reproducibility and full physical-cost distinctions

The Python producer generated exact DIMACS sources for codes `0`, `1`, `01`, and `101`, checked proper strict-3 syntax and all-zero witnesses, and exercised consistent and hostile toy proof predicates. A hostile toy predicate accepting `101` flips the 540-byte 18-variable, 48-clause SAT source to `UNSAT`; the consistent predicate labels every special source `SAT`. It also exhaustively checked the six-variable odd-charge $K_4$ as UNSAT, tested ordinary SAT and UNSAT inputs, rejected six malformed encodings, and rejected a corrupted special-source identity.

Producer: 36 assertions; Python elapsed 0.0156 host seconds; `tracemalloc` peak 48,393 bytes. Independent Node verifier: 37 assertions, including exact source hashes, regenerated clause semantics, embedded-code recovery, all-zero witnesses, and exhaustive 64-assignment odd-$K_4$ UNSAT; raw SHA-256 `fb821ae56b99bf48f9d8b71b4abb91afeb2b08b96a69439827b7eda0c5e8d63c`.

These finite checks illustrate the construction but do not formalize Godel's theorem, execute an authoritative historical checker, certify a minimum proof, or test B3. Actual program work includes parsing, source-byte comparison, code extraction, proof verification, output, and storage. `W_R` counts none of those unless represented by paid native inference nodes; conversely, the ideal `W_R` minimum intentionally excludes optimizer discovery. No logical XOR-trace lower bound is inferred.

Artifact hashes:

- producer `ee18840e24f246862c133b16497a5cf5bba96b05553bf118d29c475f5f864f0b`;
- independent verifier `1f8acf92eec2f6468fcff2665b9fb740e60811ecf7a04e3e6c8416543318dee3`;
- raw results `fb821ae56b99bf48f9d8b71b4abb91afeb2b08b96a69439827b7eda0c5e8d63c`.

## Final proof status and next exact gap

- **PROVED/EXACT under explicit standard hypotheses:** a canonical proper strict-3-CNF version of the universal-per-decider reflection firewall; one-sided soundness already implies $\operatorname{Con}(T)$.
- **PROVED/EXACT quantifier audit:** this blocks a universal same-theory reflection method but does not refute existential B3.
- **COMPUTATIONAL:** 36 producer and 37 independent-verifier finite assertions; both labels, malformed, corruption, exact source bytes.
- **DUPLICATED theorem identified and not reclaimed:** LSPV-1/357 already supplied the core Godelian firewall.
- **OPEN:** authenticate exact historical DEF facets/exported wires; construct a complete legal polynomial normalizer over all native rules; prove any superpolynomial lower bound surviving AND3/GF(2)/DEF/RES and optimal sharing; or prove the existential, noncircular same-`R_mix341` B3 bridge. P versus NP remains OPEN.

The next useful B3 test is not another adversarial program wrapper. It is the positive existential obligation from LSPV-1/357: starting with one explicitly chosen polynomial decider, identify a theory that proves its needed one-sided soundness **without assuming P=NP internally**, then give a source-authenticated polynomial compiler from those reflection proofs into the exact historical native grammar. No such decider/theory/compiler triple is presently known.

