# TMR-3/040: EARLYNEG078, asymmetric negative-prefix and positive-endmarker machine tariff

**2026-11-15 01:27 PST | PNP Time-Space Tradeoffs | America/Los_Angeles**

**Scientific status:** PROVED/RESTRICTED symbolic theorem for the exact encoding and local-head machine model, independent mathematical and physical compilation review OPEN; finite V8 execution COMPUTATIONAL. This is a genuine legal negative-source shortcut and a linear/sublinear physical access result, not a superpolynomial SAT lower bound. P versus NP remains OPEN.

## 1. Claim and preselected falsifiers

**Candidate:** Test whether TMR-4/040's strict endmarker lower bound can be extended from accepted SAT inputs to rejected UNSAT inputs. Construct an opposite-label pair with the distinguishing bit *early* in a long valid source. Establish an exact first-inspection tariff, a fixed total SAT decider with an early negative exit, and an explicit positive-input endmarker contrast.

Preselected falsifiers: F1, the alleged first eight proper clauses are not collectively contradictory or the mutated source is not SAT; F2, early rejection would be unsound on an invalid or adversarial suffix; F3, the source encoding requires an uncharged random-access or an unbounded-word arithmetic operation; F4, the endmarker/terminal obligations are independently charged despite legal read-and-halt fusion. All four are addressed below. Tractable controls include affine, Horn, Krom/2-SAT, autarky, sharing, renaming, numeric-ID width, clause reordering, malformed strings, padding and exhaustive fallback.

## 2. Exact source, grammar and family

Use precisely the general proper 3-CNF grammar in TMR-3/039 and TMR-4/040: unary bit-width header 1^b0, unary clause-count header 1^M0, then exactly M ordered three-literal clauses; each literal is a nonzero b-bit identifier followed by one sign bit, and all three identifiers in a clause are distinct. No trailing bits are legal. Malformed strings have total-decider output NO. One fixed finite-alphabet deterministic machine has one left-initialized locally moving read-only input head, finitely many blank work tapes and ordinary unit-cost transitions. A physical transition scans before each head moves at most one position. There is no word-RAM, advice, random access or source-length oracle.

For every integer t>=9 take b=M=t. Three distinct binary identifiers are

$$
a_t=2^{t-1},\quad b_t=2^{t-1}+1,\quad c_t=2^{t-1}+2.
$$

These are representable by exactly t bits and have their most significant bit set. The numeric values are *never* used as array indices by the constructed program. A clause with sign mask s in {0,...,7} forbids exactly the assignment (x_a,x_b,x_c)=s. Form G_t^- with the first eight clauses having masks

$$
1,2,3,4,5,6,7,0
$$

on the same three IDs, followed by t-8 repetitions of mask 7 (all three literals negative). Form G_t^+ by changing only the final sign bit of the eighth clause from 0 to 1, replacing its mask 0 by the already-present mask 1. Both formulas are valid proper 3-CNF.

All eight assignments are forbidden in G_t^-, hence UNSAT. In G_t^+, assignment (0,0,0) satisfies every clause: mask 0 is absent and mask 7 in the suffix excludes only (1,1,1). All earlier source bits agree. The critical polarity bit is at index P_t-1 (zero based), with

$$
N_t=(t+1)+(t+1)+3t(t+1)=3t^2+5t+2,
\qquad P_t=2(t+1)+24(t+1)=26(t+1).
$$

Thus G_t^- and G_t^+ have identical prefixes of length P_t-1 but distinct SAT labels. P_t=Theta(sqrt(N_t)) while N_t=Theta(t^2). Unlike LASTSAT073, the single distinguishing bit is *not* at the end of the source.

## 3. New theorem: asymmetry of physical ingress

**EARLYNEG078-A (PROVED/RESTRICTED).** For every correct total deterministic local-head 3-SAT decider A on the declared strict grammar, for every t>=9,

$$
T_A(G_t^-)\ge P_t,\qquad T_A(G_t^+)\ge N_t+1.
$$

The first inequality holds because the two legal, opposite-label source tapes have identical first P_t-1 scanned cells. A's control, work and heads must remain identical until some head first reads cell P_t-1. With all input heads left-initialized and locally moving, the first possible inspection is transition P_t. The second inequality is TMR-4/040's *positive-only* strict-extension argument: G_t^+0 is invalid and has label NO, so every correct accepting computation must inspect the right endmarker at cell N_t, no earlier than transition N_t+1. All arbitrary work tapes, caching, recomputation and input rereads remain legal. These are two separate exact input sensitivity arguments, not a combined time-space lower bound.

**EARLYNEG078-B (new constructive shortcut, PROVED/RESTRICTED).** One fixed finite total correct SAT decider D, independent of t, rejects G_t^- after scanning only the initial P_t input bits, using

$$
T_D(G_t^-)=O(t\log(t+2))=O(\sqrt{N_t}\log(N_t+2)),
\qquad S_D(G_t^-)=O(\log(t+2)).
$$

D first scans the unary width b into a binary counter on its single writable work tape, scans the unary M header while recording only whether M>=8, and checks the next eight complete literal records against the fixed eight sign patterns on the three canonical b-bit IDs 1 followed by zeros, 1 followed by zeros then 1, and 1 followed by zeros then 10. It uses a binary b-bit-position countdown plus finite control for eight clause indices and three literal positions, not a b-bit integer register nor an array indexed by a_t. A work-head scan and return across O(log b) counter cells suffices for each input-bit counter increment/decrement, giving at most O(log(b+2)) charged work transitions per scanned input bit. The input head does not jump. The entire prefix length is b+M+2+24(b+1). One can halt in a rejecting state on the transition that reads the eighth clause's final sign. The machine has one fixed finite control program for all t and all binary source inputs.

If all eight clause records have been authenticated, **every valid completion is UNSAT**, because those original eight source clauses alone forbid all assignments to the three variables. Every malformed completion also has total-language label NO. It is therefore sound to halt without reading any remaining clauses or right endmarker. On all other prefixes D rewinds and runs a complete conventional parser, tests the all-zero assignment on valid formulas, and if necessary exhaustively searches all assignments. Malformed inputs are rejected. This is one fixed, correct, total SAT decider, not a per-t algorithm or a promise solver. On G_t^+ the prefix test correctly fails, and the full all-zero pass accepts after full-source/endmarker authentication in polynomial time. No polynomial upper bound is asserted for D on arbitrary formulas.

Asymptotically the negative shortcut is strictly sublinear in the *actual encoded input length*. The large IDs have their top bit set so the chosen bit width is not a redundant leading-zero field. Nevertheless, three sparse numeric identifiers can be renamed densely and the clause ordering is favorable. Those are real simplicity controls, not sources of hardness. G_t^- is trivial for SAT via its constant-size contradictory core. No superpolynomial claim follows.

## 4. Authentic seven-column tariff and negative-goal counterexample

A concrete state includes the exact immutable input, fixed program, finite control, all scanned tape symbols, head positions, live writable cells, paid transition history, result flag and a noninterfering observer r(C), the greatest original input index actually inspected, initially -1. Let tau(G_t^-)=P_t-1 and tau(G_t^+)=N_t. Outside these two source families let the interface coordinate be zero. Define

$$
p_{\rm int}(C)=\max(0,\tau(F)-r(C))
$$

on the family, with other four semantic coordinates and Gamma zero, and p_machine(C)=1 for nonhalt, 0 on halt. Under any genuine step, r'<=r+1; there is no zero-price physical step, hence cl0 is identity. Completed *correct* goals on G_t^- have read the pivotal bit by EARLYNEG078-A; goals on G_t^+ have inspected the endmarker. All seven obstruction coordinates therefore vanish on their respective goals.

In directive order (CNF, affine, separator, fusion, Gamma, interface, machine), the exact sound witness is

$$
\lambda=(0,0,0,0,0,1,0).
$$

Every physical transition has w=1 and interface discharge at most one; cache updates, head reversals, shared-message operations, definitions, clause parsing, paid work-tape moves, input rereads, computation, output and halting cannot add new *independent* tolls. A terminal transition can simultaneously first-read the pivotal bit and reject, or first-read the endmarker and accept. The conservative two-column tariff matrix has Delta (interface,machine) in {(0,0),(1,0),(0,1),(1,1)}, and the exact nonnegative rational cone for these rows is lambda_int+lambda_machine<=1. Example (1/2,1/2) is feasible; (1,1) is refuted by an actual fused read-and-halt operation. The optimal one-coordinate initial potential matches P_t on G_t^- and N_t+1 on G_t^+.

**CRITICAL FALSIFIER:** the seemingly uniform potential max(0,N_t-r) applied also to the negative family is *not* terminal-zero: D halts on G_t^- after inspecting cell P_t-1, with

$$
p_{\rm end}(C_{\rm reject})=N_t-P_t>0.
$$

Thus one cannot extend the positive-only ENDMARKER074 bound to all negative SAT outputs without first proving a corresponding source-specific indistinguishability obligation. This preserves, rather than contradicts, TMR-4/040's valid positive-input theorem.

**Physical resource ledger:** actual sequential time counts every transition; parallel span of one deterministic execution is its elapsed steps, but abstract proof span and shared-DAG events are different notions. Work S is the peak number of visited writable cells on this same run and is O(log t) for the early-reject branch; one read-only source bit may affect arbitrary implicit semantic views, so no separate per-view time charge. The proof produces no explicit multi-bit certificate. A header count, input record, counter index, work-head return, signed literal, record verification, halting and decision output all consume physical transitions as performed. Source authentication of the *entire input* is deliberately unnecessary for sound negative rejection once the first eight source clauses are authenticated; it is essential before positive acceptance.

The matrix JSON separately publishes all six representative transition templates, explicit source-sensitive tau, paid ledger and rational weights. The finite audit covers both sources at eleven t values, their single changed bit, exact formula length and pivot position, eight three-variable truth assignments, strict-extension malformed controls and more than the reported number of representative paid edge inequalities. These are finite **COMPUTATIONAL** controls. No compiled physical TM was run; the time/space asymptotic construction is a separate symbolic proof requiring independent machine-level review.

## 5. Hostile controls and prior-work reconciliation

| Hostile mechanism | Result / limitation |
|---|---|
| Arbitrary source padding | Unsupported as a hardness argument; the family uses large but needed binary identifiers, and is easy |
| Renaming to dense IDs | Can drastically reduce source length and improve recognition; not invariant |
| Clause reordering and learned cores | The prefix-specific fast path may disappear, but a general source-indexed detector can still reject after a polynomial scan |
| Gaussian, affine and Tseitin | The complete eight-clause local contradiction is easier than global Gaussian elimination |
| Horn/dual-Horn/Krom/2-SAT | No inference of general hardness from non-Horn width-three source |
| Autarky/extension/circuit sharing | Free to use, with work charged; a compact UNSAT core already suffices |
| Zero-cost preprocessing | Not assumed; finite-alphabet input scan/counter operations are paid |
| Malformed extensions | Early NO remains sound, whereas positive acceptance requires right endmarker |
| Alternate machine model | Random access and pre-positioned heads need a separately charged simulation |

**Prior primary/project material inspected:** fusion-Lipschitz directive blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; November 13 TMR replacement; root proof1.txt complete SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt complete authentic blob 930c5eeddafce656717f28055a7a9a755f44737c; main.tex complete blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34; AGENTS.md, CODEX.md, research skill, latest issue #3, all five current TMR handoffs, October LEAD-0029 and original peer reports/code/matrices TMR-3/039, TMR-4/040, TMR-5/036, TMR-2/040. Historical /341 remains FAIL as full logical UNSAT authority; /386 remains RESTRICTED to tested guarded fragment. No prior source claimed the positive-only endmarker lemma applies to NO instances. The classical fixed-tape/local-head model is standard and the present time/space counting claims are directly proved, not imported as a numerical historical theorem. Hartmanis and Stearns, "Computational Complexity of Recursive Sequences," SWCT 1964, 82-90, DOI 10.1109/SWCT.1964.6, is background on machine-level complexity only; no paper theorem is invoked.

**What is new:** This is not another LASTSAT073 last-bit family. The new G_t^- is an authentically early-refutable, long valid UNSAT input and shares its initial prefix with an authentic SAT formula having exactly one changed bit at position Theta(sqrt(N)). It shows the endmarker obligation is intrinsically acceptance-specific on the exact same strict source grammar, with an explicit O(sqrt(N) log N)-time, O(log N)-work-space correct total rejecting machine and a complete corresponding source-aware ingress tariff. Earlier TMR-1/035 presented a recognizable contradictory prefix without an exact sublinear physical asymptotic in this grammar.

## 6. Status, transfer and next target

PROVED/RESTRICTED symbolic: source labels, prefix position and source length, both input-access inequalities, single-work-tape fast negative algorithm, exact local tariff. COMPUTATIONAL: finite JS tests and edge-template enumeration. Independent physical-machine compilation review OPEN. Superpolynomial fusion-safe machine potential OPEN; all-machine same-system transfer for a nonlinear SAT obstruction OPEN. P versus NP OPEN.

**Peer request:** TMR-4 independently verify that the goal-conditioned source-aware tau is a ghost observer and not a free machine oracle, and replay the fused terminal tariff and negative-goal counterexample. TMR-5 inspect malformed trailing strings and the binary-counter tape accounting. TMR-1 audit sparse binary identifiers and strict grammar. TMR-2 seek a nonaffine dynamic obstruction that survives this genuine early rejection and ordinary compact computations.

**NEXT:** Audit a fixed complete source-authenticating nonaffine SAT front end at actual finite-alphabet tape level; distinguish unavoidable information acquisition from the mere existence of a long suffix. A superpolynomial transition potential is still absent.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root proof trackers and canonical main.tex remain unchanged; no schedules changed. P versus NP OPEN.
