# LSPV-1/378: Clause-deletion witness fibres under conservative extensions

**November 3, 2026, 19:55 PST.** Specialist: General SAT Lower-Bound Lead. **PROVED/EXACT** under explicit source-transparent binary-DAG assumptions, pending external specialist review. **COMPUTATIONAL** finite exhaustive + independent verification. **OPEN:** B1, B2, B3, superpolynomial full mixed-calculus worst-case minimum, unrestricted SAT computational hardness and P versus NP. No fixed calculus, task, or schedule was changed.

## 1. Prior history and precise increment

LSPV-1/358 (research/agents/lspv-1/2026-11-03_0100_LSPV-1_ER2_SOURCE_PADDING_TYPE_FIREWALL358.tex, blob ca6dd1f7) proved a paid binary-definition padding sandwich in strict ER2 and a special full mixed-calculus padded Horn-chain floor. LSPV-3/379 (research/agents/lspv-3/2026-11-03_1724_LSPV-3_SOURCE_GATE_REPAIR379.tex, blob f37a00cd) reproduced that source-padding result. LSPV-1/373 showed that mere satisfiability equivalence permits adding an externally recognized contradictory unit pair, destroying ordinary Resolution proof hardness. The **increment here** is a necessary-and-sufficient clause-deletion-witness condition for *arbitrary* appended relations D, not merely total functional definitions or Horn chains, and the corresponding precise charged binary-DAG floor. This is elementary proof accounting, not a new asymptotic hard family.

## 2. Fixed model and quantifiers

Preserve the same preselected Rmix341 with authenticated original CNF source clauses as free leaves and unit-paid distinct binary RES, bounded-original-variable AND3, GF(2) row additions, justified LOCAL-CONVERT and conservative two-input DEF steps, with shared DAG nodes counted once. For the lemma, explicitly require every inference to be sound **from its named at-most-two antecedents alone**, and any source-dependent side condition that affects logical validity must be included in the declared ancestor relation. Arbitrary uncharged source-set/oracle side conditions are excluded. This source-transparency requirement is an audit obligation where full LOCAL-CONVERT syntax remains ambiguous; it does not silently modify Rmix341.

Take **every** clause-minimally UNSAT signed CNF F(X)=C1 AND ... AND Cm and **every** valid CNF D(X,Y), where Y is fresh. Set G=F AND D and define

$$
I_D(F)=\{i\in[m]:\exists a\in\{0,1\}^{X}\exists b\in\{0,1\}^{Y},
(F\setminus\{C_i\})(a)=1\land D(a,b)=1\},\quad r_D(F)=|I_D(F)|.
$$

This tests satisfiable *counterfactual clause deletions* of the original UNSAT source. Unlike existential equivalence of UNSAT F and G alone, it cannot be vacuously satisfied by a disconnected contradictory clause pair.

### Theorem 378A: exact survivor criterion

**PROVED/EXACT.** For every F,D,i as above,

$$
i\in I_D(F)\quad\Longleftrightarrow\quad G\setminus\{C_i\}\in SAT.
$$

Proof: deleting Ci from G leaves exactly (F without Ci) AND D, so its satisfiability is precisely the displayed existential statement. In particular, all m original clauses remain indispensable in G iff r_D(F)=m. The sufficient fibrewise-totality condition

$$
\forall a\in\{0,1\}^{X}\;\exists b\in\{0,1\}^{Y}:D(a,b)=1
$$

implies r_D(F)=m, since every minimal-UNSAT clause-deletion assignment extends through D. Acyclic conservative signed AND2, XOR, and circuit definitions are total by recursive evaluation. Totality is not necessary: it suffices that one deletion witness survives per original clause.

### Theorem 378B: exact necessary source-accounting floor

**PROVED/EXACT under source transparency and at-most-binary rule arity; specialist review pending.** For *every* sound, conservative, locally source-transparent proof DAG system S with positively weighted unit-cost internal nodes and at most two declared premises per internal node, and *every* F,D above,

$$
\boxed{W_S(G)\ge\max\{0,r_D(F)-1\}.}
$$

Proof. Suppose a refutation DAG omits from the ancestor subgraph a source Ci whose deletion has a satisfying assignment (a,b). Every included source clause is then satisfied under (a,b). Since every paid extension is conservative, its new variables can be assigned their defined values in topological order; every other internal inference is semantically justified from its explicit parents, so the root cannot be false. Contradiction. Thus all r indispensable original clauses occur in the root ancestor graph. Let q count distinct internal nodes and l the source leaves in that graph, l>=r. The underlying graph is connected to the root, so it has at least q+l-1 edges; the internal nodes have at most two incoming edges each, so at most 2q edges. Therefore q>=l-1>=r-1. If r=0 the nonnegative-cost floor is zero. Sharing and temporary enlargement are already covered by the connected-DAG count. Minimize over all valid refutations.

The theorem is applicable to any admitted Rmix341 fragment with these exact source-locality properties. An opaque rule with extra unnamed source assumptions is **not certified** by this argument until those assumptions are charged into provenance. This is not a polynomial backtranslation from ordinary Resolution, and does not establish full-R superpolynomial hardness.

## 3. Tight countercontrols and full mixed optimum

Take the minimally UNSAT signed source

$$
F=(x\lor y)\land(\neg x)\land(\neg y).
$$

Its three unique clause-deletion witnesses are 00,10,01 respectively. A strict two-RES-node proof attains the universal binary floor W=2; it is consequently also the full Rmix341 optimum under the declared binary source-transparent rules. Appending fresh signed AND2 definition z=(x AND y) or the four clauses defining z=(x XOR y) extends **each** original assignment uniquely, preserves all three witnesses and leaves exact mixed optimum 2. Appending just (NOT x OR NOT y) is not total (it forbids 11) but preserves 00,10,01, so r=3 and exact mixed optimum 2. Appending (x) destroys two original deletion witnesses (r=1) and immediately permits a one-node RES refutation with (NOT x). The transformed formula remains UNSAT, demonstrating why mere label preservation is an insufficient transfer condition.

## 4. Established hard theorem, exact unavailable computational transfer

**KNOWN THEOREM:** Haken (1985) proved there are c>0,h0 such that for every h>=h0 and every unrestricted shared-DAG **ordinary Resolution** refutation pi of the canonical unary PHP(h+1,h) signed CNF, lines(pi)>=2^(c h). It has h(h+1) variables, (h+1)+h*binom(h+1,2) clauses and explicit signed decimal DIMACS bit length N_h=Theta(h^3 log(h+2)). In our convention source axioms are free, thus W_Res>=2^(c h)-m_h. This is not an Extended Resolution, Res(XOR), Rmix341 or unrestricted uniform-machine lower bound. Cook (1976) gave polynomial Extended Resolution PHP refutations, and Buss (1987) polynomial Frege proofs. Odd expander Tseitin has a different ordinary-Resolution lower bound, but the certified cubic odd source has exact 4h-1 mixed GF(2) refutations. **No exponential lower bound transfers from these families through Theorem 378B**: its source count m-1 is polynomial. No new formulas were manufactured to imitate a published hard family.

## 5. Falsifiers and exact computational controls

F1 (FALSIFIED): retaining the UNSAT truth value alone retains all indispensable clauses; append (x) or contradictory fresh units.

F2 (FALSIFIED): preserving every clause-deletion witness requires total D; append (NOT x OR NOT y), which excludes 11 but preserves all three witnesses.

F3 (PROVED in typed binary local grammar): a sound proof DAG can omit a deletion-surviving source Ci without using it as an explicit premise; ruled out by the satisfiable counterfactual model.

F4 (FALSIFIED as an inference): an m-1 source floor implies Haken's 2^Omega(h) Resolution cost in the combined calculus; Cook's ER shortcut already defeats that transfer.

**COMPUTATIONAL:** Deterministic exhaustive producer considers all 256 subsets of eight proper non-tautological signed clauses on x,y, computes each source survivor count by four exhaustive assignments, and certifies exact unrestricted Resolution cost by BFS over at most 2^9 possible clause-database states (eight nonempty clauses plus false). Independent checker uses the three known deletion witnesses and the closed-form one-step criterion: q=1 iff two available source unit clauses are contradictory; otherwise q=2 since the original two-step proof always works. They agree in all 256 cases:

| r | q=1 | q=2 |
|---|---:|---:|
| 0 | 160 | 18 |
| 1 | 32 | 30 |
| 2 | 0 | 14 |
| 3 | 0 | 2 |

Producer: **797 assertions**; independent: **1051 assertions**, performed from exact GitHub-readback JavaScript source. AND/XOR unique-auxiliary extension controls, source-sign-flip SAT sibling, odd/even K4 Tseitin (0/8 satisfying edge assignments), nine malformed producer cases, six independent malformed cases and a forged zero-step output are checked. This is a finite exact optimum certification, not a claim of exponential machine lower bound. Deterministic, no random seed.

**Costs:** logical W counts shared inference nodes once; the BFS optimizer is separately charged and is exponentially exhaustive in the number of possible clauses, though bounded for these two-variable tests. Proof output encoding, source and index/head reads, intermediate construction, random-access/lazy representation, proof verification, output and all simultaneous peak space are separate machine resources. No FLMV contradiction follows. Preserve the all-phase rho envelope s'<=max{rho,eta,lambda,lambda*s}. An exponentially long explicit intermediate is allowed but physically expensive; compact alternatives are legal where justified.

## 6. Reconciliation and primary literature

Actual corpus reads: full 2026-11-02_1204 refocus file (blob c3889a3e514ddbd747150dcb68607013a3b2d154), issue #3 and recent LSPV peers, AGENTS.md (19656af1), CODEX.md (754999f5), pnp research SKILL (b8df83a7), LSPV-1/357 Gödel reflection, /358 padding, /375 ER2 affine simulation, LSPV-2/377 invertible encoding (a198a87c), and LSPV-3/379 (f37a00cd). Searched for prior fibrewise totality and clause-deletion witness extensions; none supplied the present all-appended-D exact characterization. Duplicate ideas from /357 (unprovable correctness), /358 (conservative definition sandwich), and LSPV-2/376 (native signed XOR gate) were **not republished**.

Grok source actually read: GROKPROOF/2026-11-04_0116_PROGRESS.md (blob ca5a835356eb918b8cb4ab94d14de6174edeab03). Its fully charged all-input SAT resource contraction remains OPEN. Claude reports actually read: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727d3e2b009cba7afec2a93beb62959dd67) and 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6ec0d5580fffe4687b82b4e3dd227de4). These are restricted alternation-trading and one-tape results, not the general Rmix341/B3 bridge. No assessment is treated as authority over an explicit soundness check. Current peer LSPV-3/381 and Red Team REFEREE327 in issue #3 reinforce shared-DAG and fixed-uniform-program constraints.

External primary-literature queries: Haken Resolution PHP, Cook 1976 ER PHP, Buss 1987 Frege PHP, Cook-Reckhow proof systems, Braun 2026 bit PHP Res(XOR), and GitHub/OpenAI resolution SAT checker search. No compatible OpenAI-owned strict Rmix341 verifier found. The container/Python environment produced transient execution errors; both standalone JavaScript programs executed successfully using V8, directly from **GitHub-readback** contents. The full local repository preflight could not be run; no local preflight success is claimed.

**Next gap:** identify a substantially stronger source-deletion potential that survives native GF(2), circuit conversion and paid extensions but is not limited by m-1. In parallel audit opaque LOCAL-CONVERT source-dependencies and resolve whether it fulfills the source-transparent premise used here. Do not infer B3 from this restricted lemma. P versus NP remains OPEN.

## Paths and references

Formal report: research/agents/lspv-1/2026-11-03_1955_LSPV-1_CLAUSE_DELETION_FIBRE378.md

Producer: experiments/arc/lspv1_378_clause_deletion_fibre.js

Independent: experiments/arc/lspv1_378_independent_verify.js

Raw: results/raw/arc/2026-11-03_1955_LSPV1_CLAUSE_DELETION_FIBRE378.json

Handoff: research/coordination/2026-11-03_1955_LSPV1_CLAUSE_DELETION_FIBRE378_FIVE_ROLE_HANDOFF.md

References: [1] A. Haken, The Intractability of Resolution, Theoretical Computer Science 39 (1985), 297-308. [2] S. A. Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4) (1976), 28-32. [3] S. R. Buss, Polynomial Size Proofs of the Propositional Pigeonhole Principle, JSL 52(4) (1987), 916-927. [4] S. Cook and R. Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44(1) (1979), 36-50. [5] K. Braun, An exponential lower bound for the bit pigeonhole principle in resolution over parities, arXiv:2609.23015 (2026), no full-mixed transfer claimed.
