# Construction of decision-sensitive twins with matching occurrence profiles

21 November 2026, 12:36 PST, America/Los_Angeles.
Recovered head 5c2dc0626809809105d541a4f61afad24a9f48c8.

**T5-BALANCED-POLARITY1 — PROVED/EXACT construction and count transformation, external independent review pending.** For every acyclic OR/NOT circuit H on p>=1 declared inputs, with any designated output O, the construction below produces two strict-C formulas B_acc(H),B_rej(H). They have equal n,m,N, equal multiplier M, maximum occurrence five, and identical full histograms of recovered occurrence-path lengths. Their counts are M z and M(2^p-z), where z=#CircuitSAT(H). Therefore H is SAT iff B_acc(H) is SAT. B_rej(H) is SAT iff H has a rejecting assignment. The same structural histogram can occur on opposite decision labels.

This is an explicit extension of the unit-fiber compiler and equality splitter in Construction16db13e. It advances a decision-sensitive test family for the WRAPPER's unresolved compulsory-core-work problem. Its general input class contains arbitrary shared Boolean circuits. A lower bound on that core remains OPEN. Counting and decision are separate tasks.

## Exact quantifiers, model and falsifiers

Let H have p input wires, o OR gates, t NOT gates, and b=p+o+t wires in topological order. Fanout, repeated OR inputs, dead gates and declared unused input bits are permitted. O may be any existing wire, including an input. Every gate has a fresh output. For every such H the explicit uniform reduction below is correct.

Separately fix one total deterministic correct decision solver A_dec, or counter A_cnt, on all valid strict-C encodings. Fix K>0,a>=1 independently of the input, with proposed T_A(N)<=K N^a on the handoff's sole physical tape/head, fixed-alphabet model. Charge input, control, head, work, output, real moves and addresses. The compiler and A have separate executions. No input-dependent solver or free semantic oracle is supplied.

C consists of the 30 permutations of 012,123,234,340,401 over Z5. Every clause has three distinct names and all names start with full domain. R is the distinct 40-tuple ordered relation with a distinguished first coordinate. The construction uses C only. The exact encoding is unary n plus terminator, gamma(m+1), and 3m one-based IDs of width ceil(log2(n+1)):
    N=n+2+2 floor(log2(m+1))+3m ceil(log2(n+1)).
No historical S/Q substitution or uncharged R conversion occurs.

Four falsifiers are a repeated-name clause caused by fanout, unequal auxiliary fibers, a mismatch in the two occurrence histograms, or confusing “H has a rejecting assignment” with “H is UNSAT.” A fifth claim is deliberately excluded from promotion by the proof: histogram equality does not imply indistinguishability under richer tests.

## Full clause generator

Number anchors a0,...,a4, then one variable per Boolean wire, followed by fresh helpers. All arithmetic on anchor subscripts is modulo5.

For a five-name sequence A, let frame(A) contain C(A_i,A_(i+1),A_(i+2)) for i=0,...,4. Emit frame(a0,...,a4).

For every Boolean wire X and k=2,3,4 allocate a fresh helper h_(X,k) and emit
    C(a_k,X,h_(X,k)), C(a_(k+2),a_(k+3),h_(X,k)).
These six clauses restrict X to {a0,a1}, with precisely one helper extension for each choice in a fixed anchor frame.

An original NOT gate X=NOT P emits C(a2,P,X).
An original OR gate X=P OR Q allocates fresh Y,Z and emits
    C(a1,a2,Y), C(a0,a1,Z), C(a4,P,Y), C(a3,Q,Z), C(X,Y,Z).
These determine Y,Z uniquely and enforce the gate on Boolean wires.

Before applying this compiler, append three fresh NOT gates
    q0=NOT O, q1=NOT q0, q2=NOT q1.
Use the same circuit and domain clauses for both variants. The accepting variant adds C(a0,a2,q1). The rejecting variant instead adds C(a0,a2,q0). q2 remains a real evaluated wire with its domain clauses. Its occurrence is what balances the local use counts of q0 and q1. The original O may have arbitrary fanout because both chosen pin targets are fresh.

Apply the original occurrence-path splitter to either clause list. Scan each clause and replace its three occurrences by three fresh occurrence copies, retaining the resulting core triple. For the ordered occurrences u1,...,ud of every source variable, and each consecutive pair u,v, allocate four fresh names r1,...,r4, set r0=u, and emit
    frame(r0,r1,r2,r3,r4), C(r4,v,r1).
This is the entire split generator. No variable has zero occurrences in the compiled source. The provided executable twins() implements the three-gate augmentation using the pinned compiler, and the test invokes the pinned split().

## Correctness and exact count proof

The five anchors receive distinct colors because every pair occurs together. Their allowed triple system is a 5-cycle triple system, so there are ten dihedral frames. In a fixed frame the exclusion pair above has one extension exactly when X differs from a_k. Conjoining k=2,3,4 gives the Boolean domain with one extension. The NOT clause enforces distinct Boolean colors. In the OR gadget, the first four clauses choose Y=a3 or a0 according to P=0 or1, and Z=a4 or a2 according to Q=0 or1; its last clause enforces X=P OR Q. The pin selects Boolean1.

For every original input assignment, all original wires, appended wires and helpers have a unique extension per frame. The three appended values are q0=1-H, q1=H, q2=1-H. Hence the two unsplit counts are exactly10z and10(2^p-z). Conversely any satisfying target assignment determines a frame, valid Boolean wires and an original assignment with the indicated output. These two directions prove both count identities and SAT(H) iff SAT(B_acc). For B_rej the equivalence is with SAT(NOT H), and UNSAT(B_rej) iff H is a tautology. When 0<z<2^p both twins are SAT.

For an equality packet, fixed u=v has exactly two private extensions, corresponding to the two orientations of its frame. Fixed unequal u,v has zero extensions. This follows from the same dihedral-frame characterization and the pin on the two nonadjacent frame colors. Distinct packets have disjoint private names. If E is the total number of links, every satisfying unsplit assignment therefore has exactly2^E split extensions, and every split assignment projects uniquely back to one unsplit assignment. Thus with M=10*2^E,
    Z(B_acc)=Mz, Z(B_rej)=M(2^p-z),
    Z(B_acc)+Z(B_rej)=M2^p.
M is known from the syntax ledger. The sum identity allows legitimate complement reuse once either count is known; obtaining that count remains a separate task.

## Why the full path histogram agrees

Before the final pin, q0 occurs in its domain three times, its producing NOT clause once and the consuming q1 NOT clause once. q1 likewise occurs three times in its domain, once in its producing clause and once in the q2 clause. Both therefore have degree5. Moving the pin swaps their degrees6 and5; every other name's occurrence degree is unchanged, including a0,a2 in the pin.

A variable of degree d becomes a copy path with exactly d vertices. Thus the complete multiset of path lengths agrees, not merely the number of three-vertex paths. The private equality packet inventory also agrees because E agrees. This yields matching split variable-degree histograms too. It does not certify equal clause incidences, isomorphism, or equal answers. Relabeling names, reordering clauses and permuting C-slots preserve the counts and path-length multiset. No uniform random-shuffle assumption is needed for this invariance.

Redteam's previous NOR/implication control matched histograms for two all-SAT instances. This construction matches them for complementary output pins of every circuit and includes opposite SAT/UNSAT labels. The older original transport matching family has a cycle-decomposition count formula and all instances SAT. The new accepting map retains the full original shared Boolean computation, including nonlinear OR dependencies. A proposed compulsory-progress theorem would have to identify source-dependent semantic work that remains after legal equality contraction, beyond degree/path statistics. It cannot charge each equality orientation as a fresh mandatory bit.

## Complete size and resource ledger

The augmented circuit has p inputs, b+3 wires, o OR gates and t+3 NOT gates. Substitution into the unit-fiber compiler gives, for either unsplit twin,
    n_J=17+4b+2o,
    m_J=27+6b+5o+t.

Each of the 3m_J occurrences becomes a copy, and every original variable occurs, so
    E=3m_J-n_J=64+14b+13o+3t.
Each link adds four private variables and six clauses. Consequently
    n_B=3m_J+4E=337+74b+67o+15t,
    m_B=m_J+6E=411+90b+83o+19t.
In particular3m_B-n_B=14E. Both N_J and N_B are obtained from their own n,m in the fixed formula above, and each is identical between twins. Never substitute b or N_J for N_B in A's cap.

Each core copy occurs once in a core clause, at most three times as the first port of an outgoing link, and at most once in an incoming pin. Its degree is at most5. Private packet degrees are3,3,4,4. All clauses have distinct names even when OR repeats its input, because those occurrences appear in different clauses. The original circuit DAG shares its wire identities; the reduction does not unfold a tree.

Let U include the source circuit's actual bit length and both constructed encodings. The compiler must validate topological wire indices, allocate names, generate every helper/packet, build occurrence lists, and serialize exact widths and headers. An indexed implementation uses polynomial work and O(U) bits of records on these sparse images. A conservative sole-tape implementation may repeatedly scan these records for each input/gadget occurrence, move O(log U)-bit keys by local shifts, and use an O(U^4) total time envelope with O(U) occupied bits. This includes all parse checks, real addresses, allocation counters, scans, writes, and the two outputs; it asserts an upper envelope, not a benchmark or an optimal exponent. With p unary and gate IDs fixed-width, N_J,N_B=O((p+o+t)log(p+o+t+2)); retaining the source's own length covers alternative input conventions.

Compiler physical CM is at most O(U^5) for that one implementation. Compiler descriptive CM obeys its separate input-charged replay bound. These are not lower demands on A. The target answer has O(n_B) bits, and multiplication/division by M and complement arithmetic cost actual bit operations. Discovery, failed recognizers and adaptive switching performed by A remain paid. Stored input, indices, certificates, caches, maps and output coexist in its storage account. Sharing counts once while retained; rereads and recomputation incur their actual cost. Recognition failure is UNKNOWN, never UNSAT.

For the fixed A,K,a on N_B the ceilings remain S=O(N_B^a), physical CM=O(N_B^(2a)), minimum-description CM=O(N_B^(a+1)), and count-map circuits O(N_B^a log N_B). At a=2 these are N_B²,N_B⁴,N_B³,N_B²logN_B. Nothing here exceeds them. No fixed exponent is excluded. A polynomial reduction supplies no same-exponent time-space transfer without its full overhead.

## Controls and finite evidence

The tautology H=x OR NOT x with p1,o1,t1 gives n_J31,m_J51,N_J808 and n_B641,m_B783,E122,N_B24151. The accepting count is20*2^122=106338239662793269832304564822427566080 and the rejecting count is0. Their entire path histograms agree. The contradiction NOT(x OR NOT x) reverses the labels, at n_B730,m_B892,E139,N_B27510. These are easy explicit controls. Their decision formulas are retained as counterexamples to histogram sufficiency and rejected as hard families.

The broad reduction accepts every shared OR/NOT source, including encoded affine systems and easy bounded-width, forced-domain, matching and private-leaf instances. Such recognizable subclasses remain legally solvable by Gaussian elimination, propagation, dynamic programming or compact evaluators. Complement is explicitly used and paid. Equality links are contractible. Input relocation and full-state entropy prevent charging imaginary residual services or independent witness orientations. The construction creates no obligation to print a witness. It does not make a single fixed hard input for all solvers.

DISJ is not applicable because no communication partition is claimed. Relativization and algebrization receive no new barrier bypass from a local reduction. Simultaneous DTISP accounts separate compiler and target runs. Deterministic configuration counts supply no lower demand. Natural Proofs and all unrestricted scalar-coverage questions remain OPEN.

COMPUTATIONAL evidence comprises28 original circuits/output selections and56 full-domain generic unsplit counts. The suite exhausts depth0/1 circuits at p1,2 with every designated output, then adds tautology, contradiction and shared-gate/unused-input controls. It checks the new identities, sizes, complete path histograms, split occurrence bounds and exact encoding roundtrips. Split counts use the equality theorem; no large expanded brute-force count is claimed. The raw evidence gives complete unsplit clauses for opposite-label examples and hashes for every split encoding. This tests the new three-gate augmentation rather than rerunning the previous98-case positive-offset suite.

Reproduce with Python3 from the published repository:
    python experiments/t5_construction_balanced_polarity_20261121.py > /tmp/t5-balanced.json
    cmp /tmp/t5-balanced.json results/raw/t5_construction_balanced_polarity_20261121.json
The script pins the existing generator by SHA2566cd122e55ab7150dff6c8a1a22099ec5b44b195395c9f83670965773417accdb. No source key or planted witness is supplied to the generic counter.

## Recovery, literature and search record

Current handoff/assignment/AGENTS/CODEX/research instructions were recovered from head5c2dc0626809809105d541a4f61afad24a9f48c8. The baseline blob a886f3387a8676b9cc86afbf3bebf22630109d49 matches the complete source recovered in the continuous preceding runs. Its hypotheses and external-review status remain inherited. Original Construction report, generator and raw evidence, Redteam orbit report, Synthesis quotient report, relevant handoffs and issue324 were recovered before choosing the augmentation. There is no complete checkout, so repository preflight and LaTeX were not run. No TMR manuscript ownership is acquired.

Primary source revision for unit-fiber clauses and splitter is Construction16db13effd093c0df7ce104b3c117ec570be7c7c. Redteam064577d8c8fab8b11d167928cb8ed93dde801b38 supplies the recovered-path statistic that this construction equalizes. Synthesis5c2dc0626809809105d541a4f61afad24a9f48c8 warns that deleting presentation changes side information; no reconstruction-kernel or pseudoentropy claim is made here. [Construction](https://github.com/j15marti/pnp/blob/16db13effd093c0df7ce104b3c117ec570be7c7c/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_113200_Positive_Offset_Pair.md), [Redteam](https://github.com/j15marti/pnp/blob/064577d8c8fab8b11d167928cb8ed93dde801b38/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_121200_Wrapper_Orbit_Test.md), [Synthesis](https://github.com/j15marti/pnp/blob/5c2dc0626809809105d541a4f61afad24a9f48c8/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_122200_Quotient_Side_Information.md).

Fresh primary literature search used “Valiant1979 enumeration reliability parsimonious satisfiability” and “Schaefer1978 satisfiability constraints original.” Read Valiant1979, section2 definitions and section3 Facts1–2. Fact2 uses uniquely determined new gate variables to preserve counts, consistent with the present fiber argument. Its general counting reductions are oracle reductions; neither they nor #P completeness supplies an unconditional lower bound. Schaefer's ACM endpoint failed with a redirect/server error; no five-domain theorem was imported from its Boolean dichotomy abstract. [Valiant original paper](https://www.math.cmu.edu/~af1p/Teaching/MCC17/Papers/enumerate.pdf), [Schaefer DOI](https://doi.org/10.1145/800133.804350).

Fresh connected official-owner search '"circuit" "negation" "SAT"' was run under anthropics,openai,xai-org,google,google-research,google-deepmind. Google429 was retried successfully. xAI and Google Research returned no hits. Host ownership uses the verified official owner identities and corporate links recovered in the preceding search logs, not product-name matches. Anthropic formal-math16a5ce41304fcdaea4e0be7c132e1c361dc26da5 returned CircuitLowerBoundStatement.lean, an oracle/circuit statement outside this reduction; its prior deep review was not repeated. DeepMind code-verification8c8d371f1962ac73435c8eb148678991f5c3470d returned ARM bitvector negation, irrelevant to strict-C fibers. Google OR-Tools4782dbd0aa85621c8115cf33de1574a2e6757004 returned reification comments in cp_model.proto, a modeling clue without a count-preserving theorem. OpenAI/math4eaee87548250b2682affda7d05d947c05554bae returned ExecClauseCost.lean, whose actual definitions were read. They explicitly charge list inspections/comparisons rather than primitive tape transitions, so no unit-cost bit-model transfer is imported. No external code or formal kernel was built. [Inspected OpenAI source](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/lean/OAI/Algorithms/SubexponentialSAT/ExecClauseCost.lean).

ONE next dependency, **T5-BALANCED-CORE-SERVICE1**, Accounting owner with Redteam adversarial review and Synthesis tracking. On a specified growing distribution of these balanced twins, exhibit an actual source-dependent decoding obligation after equality contraction and match its real event/reuse budget, or falsify that obligation with a legal shared/algebraic solver. A histogram-only service cannot even distinguish the opposite-label control above. Input-aware distinguishing and higher-order structural tests remain unrestricted.

P versus NP remains OPEN.

