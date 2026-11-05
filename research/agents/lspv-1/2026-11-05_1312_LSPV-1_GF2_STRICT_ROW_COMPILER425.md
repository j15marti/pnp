# LSPV-1 / 425: strict GF(2)-row-to-Resolution compiler with 2b rather than 3b exponent

**2026-11-05 13:12 PST | Route B. PROVED/RESTRICTED (external specialist review pending), COMPUTATIONAL finite controls. Full native R_mix341, B1/B2/B3, a superpolynomial full-mixed minimum, and P versus NP remain OPEN.**

## IDEA -> SEARCH -> ITERATE

Original testable hypothesis: the previous /424 $2^{3b}$ strict Resolution backtranslation of a binary GF(2) row sum can be reduced to $2^{2b}$ by exploiting the intersection of the two supports. Four falsifiers: (F1) an output-falsifying assignment violates both parent equations; (F2) strengthened predecessor subclauses require weakening, introduce a tautology, or break provenance; (F3) zero-variable TRUE/FALSE rows defeat the bound; (F4) the improvement is incorrectly transferred to unauthenticated private/exported-wire grammar.

After searching prior LSPV-1/424 and /371, the authentic LSPV-2/341 semantic rules, peer /429 and REFEREE369, primary Resolution papers, repository implementations and independent Grok/Claude critiques, an exhaustive original-source backtranslation was constructed. **A first chained test actually falsified a checker premise**: a representative subclause derived from earlier sources need not be entailed by the *abstract intermediate row alone*. The repaired check verifies the complete original-source ancestry. This correction is important when sharing lemmas or lifting derivations.

## Exact established 3-CNF family, fixed rule scope

Let $G_h$ be a 3-regular expanding graph with $h$ vertices. Each vertex parity equation on its three edge variables is encoded by its four signed width-three blocking clauses. Odd total charge is UNSAT. There are $n=3h/2$ edge variables, $m=4h$ clauses and $N=\Theta(h\log(h+2))$ explicit DIMACS bits. Urquhart (1987) and Ben-Sasson--Wigderson (2001) give, for appropriate expanding graphs, an ordinary unrestricted shared-DAG Resolution lower bound $L_{\mathrm{Res}}(F_h)\ge2^{\alpha h}$ for a fixed $\alpha>0$. This is proof-system hardness, not arbitrary-machine time hardness.

The historical R_mix341, originally specified by LSPV-2/341 (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), charges each distinct inference/definition node once with unit weight and admits strict RES, local AND3 truth-table conjunction, binary GF(2) XOR, constant-support LOCAL-CONVERT, and conservative globally fresh paid two-input definitions, each with at most two dependencies. No ASSUME/MERGE/weakening rule is silently added. The historical exported-wire/facet/selector byte conventions remain incompletely authenticated.

**This report is restricted to the previously declared normalized X(K) usage fragment from /424**, with K-bounded extensional exposed local conditions, explicit named-variable GF(2) rows of width at most b and d globally fresh paid signed-AND2 definitions, excluding unratified hidden consumers. The native proof-system weights and grammar are not revised. The already verified legal AND3/GF(2) Tseitin shortcut with exactly $4h-1$ paid nodes remains admitted and defeats full-mixed superpolynomial hardness for this family.

## Lemma 425.1: parity-intersection Resolution compiler

Let the affine equations be $A:\bigoplus_{i\in S}x_i=a$ and $B:\bigoplus_{i\in T}x_i=b_0$. Their binary GF(2) sum is $C$ on $D=S\triangle T$, RHS $a\oplus b_0$. Write $I=S\cap T$, $t=|I|$, $r=|D|$. Represent each equation by its canonical blocker CNF: one signed clause per falsifying assignment; $0=0$ has no clauses and $0=1$ has the empty clause.

For each canonical blocker of $C$, there is a source-authenticated strict-Resolution derivation of a **subclause** using at most $2^t-1$ genuine binary inferences, assuming nonconstant inputs. Across all output blockers:

$$
R(A,B)\le
\begin{cases}
2^{r-1}(2^t-1),&r\ge1,\\
2^t-1,&r=0,\ C=(0=1),\\
0,&C=(0=0).
\end{cases}
\ \le 2^{|S\cup T|}\le2^{2b}.
$$

**Proof.** Fix output-falsifying assignment $\tau$ to $D$. For every assignment $u$ to the intersection $I$, exactly one of $A,B$ is violated at $(\tau,u)$: the XOR of their violation bits is the violation of $C$, which is one. Choose that parent's actual canonical blocking clause as a leaf. Eliminate the $t$ intersection bits using a balanced binary decision tree. At each sibling pair, if opposite pivot literals remain, genuinely resolve; if one previously strengthened representative lacks the pivot, inherit that subclause. Both children retain only literals falsified by the same fixed assignment on all other named variables, so no nonpivot complementary literals occur. The output is a subclause of the desired blocker and at most $2^t-1$ paid strict RES nodes were used. For $r>0$ there are $2^{r-1}$ output blockers, for contradictory zero-variable output just one. A TRUE input is the identity, while a FALSE input already supplies an authenticated empty clause. If any strengthened predecessor supplies an empty clause, stop immediately. Apply the procedure once per actual proof-DAG node, retaining upstream shared references and original-source ancestry; no exponential branch unfolding is charged as one node. QED.

The scope is a compiler from **explicit source plus paid-definition canonical CNFs**, not a new native GF(2) syntax or free inference rule. Earlier representatives may be stronger than an abstract row; they are justified by the *complete original source*, not by the abstract row in isolation.

## Theorem 425.2: improved restricted DEF/row-width escape bound

Using the previously scoped LSPV-1/371 signed-AND2 gate-elimination theorem $64^d$ (blob 816da1ebabc8ae78a03be80ed5fb18eecae18209; external specialist review still pending), every valid normalized X(K) proof of the above $F_h$, with q paid mixed nodes, d globally fresh signed-AND2 owners and maximum GF(2) input/output width b, satisfies

$$
L_{\mathrm{Res}}(F_h)\le64^d\left(4h+4C_K(q+1)2^{2b}+1\right).
$$

Therefore the published ordinary-Resolution lower bound gives

$$
\boxed{6d+2b+\log_2(4h+q+2)\ge\alpha h-O_K(1).}
$$

The improvement over /424 is the coefficient **2b instead of 3b**. This is not a lower bound on q alone. Native parity proofs legitimately use wide intermediate GF(2) rows; the best mixed proof remains linear for odd cubic Tseitin. The theorem is not established for unratified historical private/exported wires or general LOCAL-CONVERT consumers.

## Actual tests, source controls and physical costs

The full standalone Python producer exhaustively checked all 1,024 ordered pairs of signed GF(2) equations on four variables, including TRUE and FALSE rows, giving 2,592 output blockers and 2,210 genuine strict Resolution inferences. A separate independently written no-import JavaScript checker confirmed the same counts with **25,562 assertions** and rejected four corrupt pivot traces and three malformed row encodings. The Python test additionally checked 180 deterministic wider pairs (seed 4252026), chained strengthened-subclause provenance, and an exact 16-clause/6-variable original odd $K_4$ Tseitin 3-CNF; its three XOR sums compiled to 31 strict RES inferences, with an even-charge SAT control and five corrupted/malformed DIMACS inputs rejected. The K4 source SHA256 is 14b5c0f63ee211e3543af3007033df8ca6cef5376e4cc23fa1d0279e72804af2. None of this is an execution of the authoritative historical native proof checker.

Logical mixed work q, translated Resolution nodes, witness bits, actual construction/verifier time, reading/retaining original source clauses, lookups, sharing references, failed search, output, simultaneous live peak space and ideal parallel span are different resources. The compiler is **exponential in b and d**, with correspondingly charged output/work, and is not an arbitrary SAT machine lower bound or FLMV same-machine transfer. Free ideal optimal-proof selection intentionally excludes proof search; physical upper bounds do not.

## Search and review ledger

Read governing November 2 handoff, current issue #3 through REFEREE369, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, native /341, /371, /423, /424, peer /429 and REFEREE369, Grok GROKPROOF/2026-11-05_1913_PROGRESS.md (blob 8a004bf4), and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727). Both required new repositories were actually inspected: konard/p-vs-np README blob 0e0ec77f and DETAILED_SOLUTION_PLAN.md blob 19450e38; blkph0x/p-vs-np-proof-research README blob f397a774 and proof_producing_cdcl_lab/PUBLIC_SAT_BASELINE.md blob 9e09b19a. Also read meelgroup/frat-xor/format.md blob 986a21aa and openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFCodeTransport.lean blob 5d1a1946. These concern formats/algorithms/limited proof models, not a full-native transfer. Actual web searches addressed GF(2) Resolution backtranslation, Ben-Sasson/Wigderson, Braun 2026 Res(XOR), Cook Extended Resolution and parity proofs. Direct Google-branded interactive search was unavailable; indexed web and GitHub were used, without claiming Google execution. No academic novelty is inferred from negative search results.

## Exact unresolved bridges

For every fixed uniform total correct CNF decider A (both labels and malformed inputs), B1 asks for $W_R(F)\le p_A(|F|+T_A(F))$ pointwise; B2 bounds $\overline W_R(N)$ by a polynomial in $N+T_A^{wc}(N)$; B3 asks whether $\mathrm{SAT}\in P$ implies $\overline W_{R_{\mathrm{mix341}}}(N)=(N+1)^{O(1)}$ **for that same fixed calculus**. B1 implies B2 implies B3; all remain OPEN. A rejecting machine trace still requires independently justified correctness/reflection. The next exact work is historical exported/private-wire and definition-facet byte authentication plus testing whether every native consumer admits this normalization or a legal counterexample; LSPV-3 and LSPV-5 are asked to challenge the strengthened-representative and gate-elimination argument.

## References

[1] Urquhart, A. *Hard Examples for Resolution*. JACM 34 (1987), 209-219, DOI 10.1145/7531.8928.

[2] Ben-Sasson, E. and Wigderson, A. *Short Proofs Are Narrow: Resolution Made Simple*. JACM 48 (2001), 149-169, DOI 10.1145/375827.375835.

[3] Haken, A. *The Intractability of Resolution*. TCS 39 (1985), 297-308. Unary PHP is not the 3-CNF family in this report.

[4] Cook, S. *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*. SIGACT News 8 (1976), 28-32.

[5] Braun, K. *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015 (2026), separately qualified preprint.