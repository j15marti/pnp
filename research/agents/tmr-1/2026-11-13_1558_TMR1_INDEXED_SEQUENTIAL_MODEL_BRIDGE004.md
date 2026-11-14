# TMR-1/004: charged indexed-to-sequential machine bridge and the weak transferred crossing bound

**Date:** 2026-11-13 15:58 PST (America/Los_Angeles). **Role:** TMR-1 Machine Model Lead.  
**Status:** Simulation and quantitative transfer CANDIDATE, awaiting independent TMR-5 review; finite source tests COMPUTATIONAL; TMR-3/002 crossing bound PROVED/RESTRICTED as previously independently reviewed. Unrestricted P versus NP remains OPEN.

## 1. Exact research target, model and antecedents

The full separation target is

$$
\forall A\in\mathrm{Dec}_{3SAT}\;\forall k\in\mathbb N_{\ge1}\;\forall C>0\;\forall L_0\;
\exists F\text{ valid 3-CNF}:
|F|\ge L_0\land T_A(F)>C(|F|+1)^k.
$$

One fixed finite total deterministic decider A must serve ALL binary lengths, correctly decide SAT and UNSAT on valid sources, and terminate with a defined response on malformed strings. Count all physical transitions, heads, temporary buffers, INDEX registers, stacks, input rereads, preprocessing, fallback and final output. Writable space means all physically visited writable cells on the SAME computation. The encoded original bit length L, not variables or clauses, is the measured input size. Hard inputs may depend on A,k,C,L0.

TMR-3/002 proved a two-way physically SEQUENTIAL-input-head crossing-product bound for a special recognizable strict proper-3CNF equality family. Historical LSPV-4/487 and TMR-3/002 already showed native INDEXED-input fast-path escapes. The new, narrow mathematical increment is to quantify a full machine simulator and derive exactly what weak lower product still transfers to a specified indexed model. The polynomial-equivalence idea is standard; no claimed new general complexity-theory technique.

## 2. Explicit machine interfaces

SEQ: one freely reversing read-only original-input head, one-cell movement per concrete transition, left/right endmarkers, fixed finite alphabet and fixed finitely many ordinary sequential writable work tapes. It cannot jump to an original input bit by address. A native transition, including a source-head move or writable tape operation, costs one.

IDX(w): same finite multitape program, except a fixed number of original-input INDEX ports may return original bit x_j or an out-of-range marker from an address j stored in a paid binary w(L)=ceil(log2(L+2))-bit register. An indexed read itself costs a transition; writing/revising/clearing the INDEX registers, their heads, and every other work tape costs transitions and space. The model may be given L as a read-only length parameter. This is a specified bounded-address indexed model, NOT an unbounded-word RAM, a free oracle, or unrestricted indexed writable random memory. Other random-access models require separate translation.

## 3. New scoped lemma TMR1-IB4 (symbolic, CANDIDATE)

For every fixed total correct IDX(w) decider A, there exists ONE fixed total correct SEQ decider B=Sim(A), and a constant d_A>0, such that for EVERY binary input x of length L>=2:

$$
T_B(x)\le d_A(L+2)\log_2(L+2)(T_A(x)+1), \tag{IB4-T}
$$

$$
S_B(x)+1\le d_A(S_A(x)+\log_2(L+2)+1). \tag{IB4-S}
$$

**Construction.** The fixed B first discovers actual input length by physically walking from left to right endmarker and rewinding, using a charged O(log L)-cell binary counter. Conservative time is O(L log L) and space O(log L). B then simulates the exact fixed controller and the fixed ordinary work tapes of A, storing each simulated tape symbol and head position on sequential physical work tapes. This does not hide workspace or provide free table lookup.

For each virtual INDEX source read, B copies the at-most-w-bit address to a separate charged binary cursor, resets the real source head to the left, and physically seeks forward to the requested bit or endmarker. Each physical head movement costs a real transition. Updating/decrementing a small binary cursor costs at most O(log(L+2)) sequential work-tape transitions per source-head move using conservative grade-school arithmetic. Hence each virtual INDEX query costs O((L+2)log(L+2)) transitions and O(log(L+2)) extra writable cells. Address values beyond L are resolved by the endmarker; the simulator pays to discover that result. Any required virtual INDEX erasure is also simulated. A fixed number of simultaneous read ports changes only d_A. Non-INDEX virtual transitions, the complete parser, both terminal labels, and malformed-input behavior are preserved with finite charged overhead.

Critically, B never copies the whole L-bit original source to a writable tape. The physical transport appears in TIME, not as an unexplained extra L work cells. All bounds concern the very same input x and the same simulated execution, not separate worst-case witnesses. The compiled simulator B has one fixed finite program for ALL L. A correct total A gives a correct total B.

**All-exponent implication.** A genuine universal superpolynomial SEQ time lower bound against every polynomial exponent would also rule out fixed polynomial-time IDX(w) SAT deciders: any t_A(L)=O(L^k) would produce t_B(L)=O(L^{k+1}log L) for all binary inputs. This valid polynomial model-transfer implication does not preserve particular lower exponents or raw time-space product inequalities.

## 4. New same-witness quantitative transfer, and its ceiling

TMR-2's proper 3-CNF family E_n(a,b) has N=5n variables, M=8n clauses, w_n=max(1,ceil(log2(5n))), and bit length

$$
L_n=13n+2+24n(1+w_n)=\Theta(n\log(n+1)).
$$

It is satisfiable exactly when a=b. Independently reviewed TMR-3/002 states that for every correct fixed SEQ B, every sufficiently large n admits one SAT diagonal F_n=E_n(a_n,a_n) on which

$$
T_B(F_n)(S_B(F_n)+1)\ge c_B L_n n. \tag{TW2}
$$

Apply TW2 to the particular B=Sim(A) for any fixed correct total IDX(w) A and substitute IB4-T and IB4-S on THAT SAME F_n. There is c'_A>0 such that for every sufficiently large n, SOME SAT diagonal satisfies

$$
\boxed{
(T_A(F_n)+1)(S_A(F_n)+\log_2(L_n+2)+1)
\ge c'_A\,\frac{n}{\log_2(L_n+2)}.
} \tag{IB4-X}
$$

This is a valid but very WEAK model transfer, conditional on precisely the scoped TW2 result and the new simulator proof. Physical source transport L log L is lost during translation. IB4-X gives at most polynomial-strength restrictions, allows arbitrary polynomial workspace, and proves no superpolynomial SAT time lower bound. It is weaker on this easy equality family than existing elementary input-observation controls.

**Hostile indexed countermodel (already known, not new).** One fixed complete SAT decider can authenticate canonical E_n clauses using INDEX accesses and regenerated binary addresses in O(L_n log^2 L_n) transitions and O(log L_n) writable cells, compare the n first-bank and second-bank signs without retaining n bits, and use a fully charged exhaustive correct fallback for every other valid source. Thus on every authenticated member,

$$
T_A(F)(S_A(F)+1)=O(L_n\log^3 L_n)=o(L_n n).
$$

Therefore a direct, overhead-free transfer of the original TMR-3/002 product to IDX is FALSIFIED/RESTRICTED. IB4-X survives. No fixed-program uniformity or source-length issue is hidden: the same indexed program works across n and handles both labels.

## 5. Fresh finite controls, not a native machine measurement

A new self-contained JavaScript program independently implements the exact indexed E_n source grammar: unary N/M headers, all signed original three-variable clauses, each canonical four-row unit-forcing gadget, every auxiliary variable identifier, and indexed first/second bank sign comparisons. It counts actual indexed source queries and cumulative hypothetical physical seek distances along that same query sequence. It uses conservative arithmetic proxies for index writing and sequential binary seeking. It does NOT simulate a native TM controller or prove the asymptotic inequalities by testing.

**Actually executed in V8:** 1,364 exhaustive n=1..5 pairs plus 108 deterministic seeded n=6,8,16,32,64,96 controls. Of 1,472 exact source classifications, 98 SAT and 1,374 UNSAT passed. Forty malformed and clause-shape corruptions were rejected as family nonmembers. The tests processed 1,960,384 encoded input bits, 1,973,696 indexed queries and 74,710,528 charged source-head seek-distance units. Zero failures. Exact source lengths, query-count bounds, seek-distance ceilings, and same-trace simulation proxy bounds were checked. Algebraic log-cubed/n sample ratios at n=2^8 through 2^32 decreased from 16.711 to 0.000016976; only the symbolic limit proves the asymptotic relationship.

Published executable: experiments/tmr/tmr1_indexed_sequential_bridge004.cjs, blob f46597879543da76d1cc382af4680c385fd47ae0.  
Immutable raw JSON: results/raw/tmr/2026-11-13_1558_TMR1_INDEXED_SEQUENTIAL_BRIDGE004_RAW.json, blob 2e52ec5498f695d7a2248750deda053d4feb69c3.

The exact published code was freshly fetched and re-executed in a new V8 tool isolate, and its semantic output exactly matched the committed raw JSON. No native OS Node CLI, exact physical TM interpreter, LaTeX compilation, repository-wide preflight or report-validator was run. The finite outcome remains COMPUTATIONAL. The general finite machine construction and same-witness algebra remain CANDIDATE pending TMR-5 review.

## 6. Dependency DAG, falsifiers, scope and next target

$$
\text{fixed machine+parser}
\longrightarrow \text{IB4 charged SEQ simulation (CANDIDATE)}
\quad+\quad\text{TW2 (PROVED/RESTRICTED)}
\longrightarrow \text{IB4-X (CANDIDATE/RESTRICTED)}
\not\Longrightarrow \text{unrestricted SAT time separation (OPEN)}.
$$

A valid universal proof still must cover arbitrary compact algebra, Horn, 2-SAT, XOR/Tseitin, bounded width, products, sharing, padding, renaming, auxiliary variables, caching and paid recomputation. High treewidth, exponential assignments, abstract state capacity, a streaming communication transcript or a restricted proof calculus does not alone prove unavoidable transitions. ETH/SETH, cryptographic assumptions and nonuniform advice are not assumed. An all-input polynomial SAT algorithm remains an admissible endpoint.

Team tests: TMR-2 should challenge any information lemma against indexed first reads and small affine summaries; TMR-3 should audit the simultaneous workspace and the precise lost L log L factor; TMR-4 must retain genuine cheap indexed and sequential traces in its all-transition cost domain; TMR-5 should independently test the binary-seek simulation, INDEX semantics and same-diagonal quantifiers.

**Primary literature inspected:** [1] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), original ACM publisher page https://doi.org/10.1145/1101821.1101822 (restricted random-access theorem, NOT all-polynomial separation). [2] Hennie, *One-Tape, Off-Line Turing Machine Computations*, Information and Control 8:553-578 (1965), NASA original bibliographic record https://ntrs.nasa.gov/citations/19660041785 (crossing methods depend on input interface). [3] Original restricted indexed resource audit, LSPV-4/487: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-11-07_2236_LSPV4_INDEXED_EQUALITY_ESCAPE487.md . Related original TMR-3/002: https://github.com/j15marti/pnp/blob/main/research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md . TMR-3/003 and original Claude ONETAPE-0001 were also read. No priority claim for standard machine simulations.

**Corpus and publication safeguards:** First read 2026-11-13 12:49 PST superseding directive on main and rechecked its SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 before report publication. Read complete root proof1.txt (28,714 chars; SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and complete genuine proof2.txt via blob (1,051,196 chars; SHA 930c5eeddafce656717f28055a7a9a755f44737c), full root main.tex via blob (2,490,254 chars; SHA 3886f0e574849e69140f5bec3286cb6666724657), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, newest five TMR handoffs, original claims/code and latest issue #3 comments through TMR-4/004. Blank contents fetch was not interpreted as an empty tracker. Historical scientific results preserved; superseded old LSPV ownership and Route allocations not revived.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt/proof2.txt: no P1 or P2 central obligation changed. TMR-1 authorized main.tex region exists but was left untouched pending independent review, to avoid prematurely promoting a candidate. No tasks or schedules modified.

**ONE NEXT TARGET:** TMR-5 independently validate every physical seek/scratch-memory step in IB4 and same-witness inequality IB4-X; then replace source-transport products with a cost-sound global-consistency charge that survives INDEX, arbitrary polynomial space, shortcuts and recomputation.

END_OF_REPORT::TMR1::IB4::2026-11-13_1558_PST
