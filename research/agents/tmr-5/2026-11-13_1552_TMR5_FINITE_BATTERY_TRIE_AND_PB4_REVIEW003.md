# TMR-5/003: independent PB4 review and finite-battery trie no-go

**Research date:** November 13, 2026, 15:52 PST (America/Los_Angeles). **Role:** TMR-5, new machine-bottleneck red team and whole-document synthesis. **Primary peer under audit:** TMR-4/004, PROGRAM-BLIND-POTENTIAL-CEILING. **Statuses:** TMR4-PB4 **PROVED/RESTRICTED after independent TMR-5 symbolic review**; new TMR5-FT3 **CANDIDATE pending TMR-1/TMR-4 separate review**; finite executions **COMPUTATIONAL**; unrestricted 3-SAT superpolynomial lower bound **OPEN**.

## 1. Exact model, quantifiers, and audited peer source

The target is one fixed finite correct total deterministic multitape 3-SAT decider A serving ALL lengths, with one two-way physically sequential read-only original input, finite control and alphabet, fixed finitely many writable tapes, and unit-cost physical steps. All rewinds, input accesses, buffers, temporary programs, working space, parser steps, recomputation and outputs are charged. The language on malformed binary sources rejects. Encoded source length L is not the clause or variable count.

The separation obligation remains

$$
\forall A\in\mathrm{Dec}_{3SAT}\;\forall k\ge1\;\forall C>0\;\forall L_0\;
\exists x\in\mathrm{VALID3CNF}:\;
|x|\ge L_0\ \land\ T_A(x)>C(|x|+1)^k.
$$

The decisive ORIGINAL source audited was [TMR-4/004](../../tmr-4/2026-11-13_1540_TMR4_PROGRAM_BLIND_POTENTIAL_CEILING004.md), blob 3cf5828901e0aa2b051c23fe901c9830447680e4, with original executable blob 0fad5f8df5ef596ca36665a55b88430c4792cba8 and immutable raw blob 796d17c507c1bdb14399253f933ccf438d2a0f4f. Its direct finite comparator was implemented as a host-language equality predicate, not a physical step-by-step input scan. The present audit constructs and executes an independent finite-control trie successor relation and proves a simultaneous extension.

## 2. Peer verdict: TMR4-PB4

Fix a valid input x of length L and a single cost-labelled MAY graph G_x whose initial abstract state s_x and admissible potential Phi_x do not depend on the chosen correct decider A. Require that every concrete initial A,x is related to s_x, every legal concrete step from every related state is represented by a finite abstract path of cost at most its physical increment, every correctly labeled SAT/UNSAT terminal maps to the matching abstract terminal with Phi_x(goal)<=0, and EVERY graph edge (including zero-cost edges) obeys

$$
\Phi_x(u)\le c(u,v)+\Phi_x(v).
$$

For the particular fixed x, build B_x, a different but individually fixed finite correct total machine whose finite control compares the L input symbols against x, checks the right endmarker, and emits the hardwired true label. On mismatch, extra data or truncation it rewinds the physically readable source and runs a paid correct exhaustive 3-SAT solver. On x the transition trace costs L+1 (under the terminal-output-on-endmarker transition convention). By the asserted all-machine cost simulation, a matching abstract path of no greater cost exists. Telescoping the EVERY-edge inequalities, including zero-cost ones, gives

$$
\Phi_x(s_x)\le T_{B_x}(x)\le L+1.
$$

Both labels, malformed inputs and one fixed total program over all lengths are respected. This is a genuine physical fast path, not a spurious abstract shortcut. The program B_x depends on x; therefore the theorem DOES NOT constrain any initial abstract state tagged with A, and DOES NOT imply a polynomial-time general SAT decider. No hidden statement \`forall x exists B_x => exists B forall x\` is used.

**Independent verdict:** TMR4-PB4 is **PROVED/RESTRICTED** under its explicitly strong, machine-blind common-start hypothesis. The original "one comparator" idea is older per-length-hardcoding/finite-control theory, correctly credited to TMR-1/001; the all-edge graph ceiling is the incremental scoped formulation.

## 3. New TMR5-FT3: ONE uniform finite-battery fast path

**Theorem, new symbolic extension, CANDIDATE pending another role's review.** Let D be any total decidable binary language with a fixed correct total fallback A_0, and H any nonempty FINITE set of binary inputs. Write

$$
R(H)=\sum_{x\in H}|x|,\qquad Q(H)\le1+R(H).
$$

There exists ONE fixed total deterministic multitape decider B_H for D serving all lengths, with at most Q(H) prefix-comparator control states plus O(1) fallback states, such that simultaneously

$$
\forall x\in H,\qquad T_{B_H}(x)\le |x|+1.
$$

A conventional explicit binary transition-table encoding uses O((R(H)+1)log(R(H)+2)) program bits, allowing the fixed fallback's constant description.

**Proof.** Build a deterministic prefix trie of ALL words in H, with one root, one state for each distinct nonempty input prefix, and two binary outgoing transitions per state. Store the true answer D(x) as an endmarker-guarded terminal output at the state for each x. On each source symbol, the finite controller follows the corresponding trie edge, moving the read-only source head right once per step; on a right endmarker it halts with the labeled output ONLY if the current prefix is a complete word of H. Every nonexistent edge or missing terminal output transfers to a fixed fallback routine; it first rewinds the source head with paid unit moves and invokes A_0, which is correct and total on every binary string. Thus every input not in H is decided correctly, including sources that share a strict prefix with a member of H and malformed sources. Every x in H makes exactly |x| source-symbol transitions and one endmarker/terminal transition. The trie is finite because H is finite. It is compiled into ONE machine B_H, not a different machine for each x within H. There are at most 1+sum |x| trie states. Each constant-outdegree state needs O(log(Q+2)) bits per target pointer and O(1) label/type bits, giving the stated description bound. The offline finite labels can be computed via A_0 when constructing B_H, or specified as finitely many constants; they are NOT runtime oracle access or a uniform polynomial procedure for growing H. QED at this exact scope.

**Corollary FT3-ABSTRACTION.** Under the machine-blind MAY-graph contracts of Section 2 for every x in H, use the SAME concrete decider B_H for all x. Thus, simultaneously,

$$
\forall x\in H,\qquad \Phi_x(s_x)\le |x|+1.
$$

Consequently NO fixed finite suite H can be a universal superlinear worst-case hard-test battery for all correct finite deciders, even if it contains both SAT and UNSAT, malformed controls, formulas differing in only one decisive encoded bit, or high-width affine controls. The compiler cost and growing program description are outside each selected B_H runtime, so this is intentionally a **finite-battery nonuniformity obstruction**, NOT an attack on the actual quantifier order, which holds ONE fixed A while varying arbitrarily large x.

**Sharp caveat:** The candidate potential can be program-dependent and escape this result. Any genuine asymptotic hardness statement must also account for a fixed program-description budget independent of the arbitrarily large test length; the conclusion that such a potential actually grows superpolynomially remains OPEN. This elementary extension is not claimed to be a novel field-wide complexity theorem.

## 4. Hostile checks and executed verification

New exact, readback-verified V8 executable:
\`experiments/tmr/tmr5_finite_trie_comparator005.cjs\`, blob b6b43f86cd68b9e504a2734516a336ef5f5fc03e.

Immutable raw:
\`results/raw/tmr/2026-11-13_1552_TMR5_FINITE_TRIE005_RAW.json\`, blob 09402432a963b317909732c07247e252c45c43a4.

The executable builds one explicit prefix-trie transition table from a deterministic finite battery, then scans each input one physical source-symbol/endmarker state transition at a time. It checks 147 on-battery traces, 11,868 exact on-battery transitions, 147 endmarker guards, and 147 checks that an illegal zero-cost shortcut cannot support the same positive potential. Inputs include 73 SAT, 25 UNSAT and 49 malformed strings. A valid strict-proper 14-variable/17-clause SAT/UNSAT sibling pair has length 288 and differs only at the LAST bit. The trie has 5,909 states, below its proved 11,722 upper bound, with a conservative 183,179-bit transition-table bound. It also checks 798 adversarial source probes, of which 718 take the off-battery fallback. Zero assertions failed. Explicit fallback labels use exhaustive assignment enumeration in the source emulator; a complete physical fallback TM was proved constructible but NOT instruction-simulated.

Separately, a local-only independent Python implementation was actually executed with seed 20261113: 141 finite-battery inputs, 11,340 on-battery source transitions, 775 probes, 703 off-battery fallbacks, 6,936 trie states, 73 SAT/25 UNSAT/43 malformed on-battery inputs, zero failures. Local files \`/mnt/data/tmr5/tmr5_finite_trie_no_go005.py\` and its raw JSON were NOT published and are not presented as shared evidence. The published V8 source is the independently executed and readback-verified reproducible artifact. Neither runner simulates every concrete instruction of the fallback multitape TM, and neither verifies the all-machine MAY graph: that premise is symbolic. No Node OS CLI, full repo preflight, LaTeX compile or unrestricted SAT run was executed.

Hostile cases: both decision labels; strict last-bit-sensitive pair; input prefixes, suffixes, truncation, overlong strings, malformed syntax; repeated prefixes/structural sharing; and off-battery recomputation by an exhaustive fallback. The general theorem does not assume any solver enumerates assignments on its fast path; genuine Horn, 2-SAT, GF(2)/Tseitin, bounded-treewidth, padding and reencoding algorithms all remain legal in the machine class. TMR-2/004 supplies an affine/high-primal-width cheap-invariant control; no separate performance benchmark for each class was run in this audit.

## 5. Integrated dependency synthesis and source discipline

**Surviving, correctly scoped arrows:** TMR-4/001 observation-only hitting-set soundness and linear ceiling, TMR-5/001 optimality of THAT graph (independently checked by TMR-1), TMR-3/002 physical sequential-head equality-family crossing lower bound (independently checked by TMR-5), TMR-4/003 and TMR5-SF2 speculative final-bit/suffix constructions (reviewed by TMR-5 and TMR-4 respectively), TMR-1/003 polynomial recognizable fast-path island (independent symbolic proof follows directly by composition), and now TMR4-PB4 under machine-blind common-start. TMR-3/003 batching, TMR-2/004 affine clique minor, and new FT3 require their remaining independent reviews. Every such construction fails to establish an all-program superpolynomial total-time lower bound.

**OPEN load-bearing arrow:** Produce for EACH fixed correct uniform A a program-aware, input/source-bound, all-transition cost-sound resource potential whose initial value beats every polynomial on some arbitrarily long valid x, without tautologically defining it as the unknown T_A(x). Machine-blind common-start potentials cannot satisfy that arrow because of genuine hardwired comparison machines. Any claimed finite set of universally difficult formulas can be compiled into one finite fast-path machine and is equally insufficient. A general polynomial-time SAT algorithm remains an allowed alternative endpoint.

**Historical provenance:** The exact original LSPV-5/510 Infinity/null parse/reserialize collision and LSPV-5/511 \`AND3.support\` string-duck-typing accepted witnesses were checked in original archived coordination reports. They illustrate why real accepted checker paths cannot be deleted as "spurious" when refining an abstract checker, but are not a mandatory bridge to arbitrary-machine SAT. No checker evidence was edited. Original TMR-4/001 and /004, TMR-1/003, TMR-2/004 and TMR-3/003 reports, their relevant code/raw, all newest five TMR handoffs and issue #3 were examined. The replacement directive was read first and rechecked before writing. Root proof1.txt (28,714 chars, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), root proof2.txt (1,051,196 chars, authentic blob 930c5eeddafce656717f28055a7a9a755f44737c), and root main.tex (2,490,254 chars at blob 3886f0e574849e69140f5bec3286cb6666724657 before this synthesis) were recovered. No tracker status promotion is warranted: **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

**Primary literature and precise use:** [1] Hartmanis and Stearns, "On the Computational Complexity of Algorithms," *Trans. AMS* 117:285-306 (1965), https://doi.org/10.1090/S0002-9947-1965-0170805-7 (classical fixed-program machine complexity framework). [2] Blum, "A Machine-Independent Theory of the Complexity of Recursive Functions," *J. ACM* 14(2):322-336 (1967), https://doi.org/10.1145/321386.321395 (program-choice and model dependence in general complexity, **not** claimed to prove FT3). [3] Cousot and Cousot, "Abstract Interpretation," POPL 1977:238-252, https://doi.org/10.1145/512950.512973 (abstract simulation background, **not** source of PB4/FT3). [4] Lynch, "On Reducibility to Complex or Sparse Sets," *J. ACM* 22(3):341-345 (1975), https://groups.csail.mit.edu/tds/papers/Lynch/jacm75.pdf (complexity cores, with separate precise hypotheses; no claim that her theorem implies the present finite fast path). Titles, dates and model scope were checked against independent bibliographic/author/publisher records.

## 6. One next target

**TMR-1 or TMR-4 independently challenge FT3**, including trie-prefix and endmarker handling, finite-control description bound, per-battery vs per-length program quantifiers, and initial/terminal abstract bindings. **TMR-3** should test whether any restricted time-space cost survives replacing the equality-family source with this fixed finite trie compiler when program length is charged separately. **TMR-2** should seek a same-machine distinction measure beyond this program-dependent finite shortcut. **TMR-5 next** should audit TMR-3/003's claimed work-head and parser operation upper bound and TMR-2/004's original-source primal K_m minor; the current universal superpolynomial arrow remains OPEN.

END_OF_REPORT::TMR5-FT3::2026-11-13_1552_PST
