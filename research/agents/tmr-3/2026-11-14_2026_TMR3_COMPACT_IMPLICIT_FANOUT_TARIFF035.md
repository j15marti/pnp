# TMR-3/035: Fixed source-only machine, implicit fanout, and complete fusion tariff slice

**2026-11-14 20:26 PST** | **COMPACTFAN056** | TMR-3 Time-Space Tradeoffs.
Status: **PROVED/RESTRICTED** all-length mathematical row theorem for a specified fixed multitape regular-language decider; independent TMR-4/TMR-5 peer review OPEN. Finite experiments COMPUTATIONAL. **P versus NP OPEN.**

## Candidate and four hostile falsifiers

Candidate fixed before original source review: a single fixed deterministic machine with standard blank work tapes, one read-only input, and one terminal step that fills a shared cache while consuming a real physical message can resolve exponentially many **implicit alias views** without paying an exponential number of transitions.

Four falsifiers: (1) constructing aliases actually writes 2^n separate cells; (2) the final source read, cache write, message erase or terminal selection cannot occur in a single physical multitape transition; (3) a proposed weight violates a legal reachable tariff row or a malformed-input/terminal row; (4) the construction depends on an external command stream, nonuniform advice, or a free SAT/UNSAT oracle. Tests (1), (2), (4) do not apply in the qualified source-only model. Falsifier (3) succeeds for every positive constant fusion-view weight and for independently adding correlated obligations.

**Novelty relative to TMR-3/034 and TMR-5/031:** previous shared fanout event models required physical subscriber setup or an additional charged command input. This new countercontrol has NO command input, starts with blank work tapes, is one fixed total deterministic program for all n, and has 2^n semantic subscriber aliases described by n bits. The alias views are deliberately NOT independent physical computation obligations. The new result is an exact seven-column all-n tariff cone for a *real fixed program*, not a SAT separation.

## Fully qualified machine and growing source family

One fixed finite-state deterministic machine M has a single read-only binary source tape with blank end, and two blank writable tapes: one stationary one-cell cache head (blank, ?, 0, 1), one stationary one-cell message head (blank, M). The source head starts at position 0, moves right at most one cell per transition, and the control has START, SCAN, BIT, YES, NO and BAD states. Its complete physical reachable-state rule inventory is:

| Concrete step, exact guard | Operation within ONE paid transition | Source reads | Work writes | Input moves |
| --- | --- | ---: | ---: | ---: |
| INSTALL: START, input 1, blank work | write cache ?, message M; input head R; SCAN | 1 | 2 | 1 |
| SCAN_ONE: SCAN, input 1 | source head R | 1 | 0 | 1 |
| DELIMITER: SCAN, input 0 | source head R; BIT | 1 | 0 | 1 |
| FINISH: BIT, b in {0,1}, cache ?, message M | read b, write b to cache, erase M, halt YES iff b=1 else NO | 1 | 2 | 0 |
| BAD_PREFIX: START, first symbol 0/blank | halt BAD | 1 | 0 | 0 |
| BAD_DELIMITER: SCAN, blank before delimiter | halt BAD | 1 | 0 | 0 |
| BAD_BIT: BIT, blank after delimiter | halt BAD | 1 | 0 | 0 |

Every actual step costs w=1, including source read, all simultaneous tape writes, head movements and terminal control. No physical zero-cost edge exists, so authentic cl0 and zero-cost SCCs are identities. A mathematical relabeling of shared subscribers is not a zero-price machine transition.

The fixed machine decides the regular language of strings beginning with one or more 1 symbols, then 0, then 1, with arbitrary ignored suffix. Other inputs are rejected; both terminal labels are correct and all inputs halt. The canonical family is

$$
F_{n,b}=1^n0b,\quad n\ge1,\quad b\in\{0,1\},\qquad L=n+2.
$$

After n+1 paid header scans/initialization steps, FINISH is one real transition. Exact total time and peak writable-space consumption are

$$
T_M(F_{n,b})=n+2=L,\qquad S_M(F_{n,b})=2.
$$

Both writable heads visit only one work cell each. There are n+2 source read events, n+1 input-head moves, two work writes at INSTALL and two at FINISH. The program is constant size and uses no nonuniform lookup or preloaded subscriber/message tape.

Define one virtual subscriber label u for each u in {0,1}^n; all 2^n labels request the **same exact value b**. They are implicit shared semantic views with no physical subscriber cells, independent messages, or required physical per-view output. One cached bit b makes ALL views evaluable. This is the cheap-representation hostile control. If a changed task required 2^n separate physical outputs, those writes would need to be charged.

## Complete seven-column tariff matrix

For canonical input and any reachable nonterminal state, let z=1 when cache remains blank/? and z=0 when cache holds b. Let m=1 when the physical message tape contains M, and m=0 otherwise. Define:

$$
p(C)=(p_{\rm CNF},p_{\oplus},p_{\rm sep},p_{\rm fus},p_\Gamma,p_{\rm int},p_{\rm mach})
=(0,0,0,2^nz,z,m,z).
$$

All coordinates are zero on noncanonical sources and ALL completed terminal states. The fusion coordinate intentionally counts raw *aliases* rather than distinct canonical obligations and is tested as a known questionable candidate. It cannot be silently relabeled as a sound fusion invariant. Gamma, interface, and machine coordinates are correlated. Their joint discharge must be charged once.

The full rule-by-component delta vector, using Delta=p(before)-p(after), is:

| Rule | Price | Delta CNF | Delta XOR | Delta separator | Delta fusion | Delta Gamma | Delta interface | Delta machine |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| INSTALL | 1 | 0 | 0 | 0 | 0 | 0 | -1 | 0 |
| SCAN_ONE | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DELIMITER | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FINISH | 1 | 0 | 0 | 0 | 2^n | 1 | 1 | 1 |
| all three BAD guards | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

INSTALL creates the physical message, so its interface delta is negative. SCAN and DELIMITER have zero semantic discharge but still consume genuine steps. Every listed physical transition is included. The seven-coordinate machine-readable original is in results/raw/tmr/2026-11-14_2026_TMR3_COMPACTFAN056_TARIFF_MATRIX.json.

## Exact dual cone and proof

For any fixed nonnegative length-independent lambda, the FINISH row on every canonical n requires

$$
2^n\lambda_{\rm fus}+\lambda_{\Gamma}+
\lambda_{\rm int}+\lambda_{\rm mach}\le1\qquad(\forall n\ge1).
$$

Because lambda_fus is nonnegative and n unbounded, this is equivalent to

$$
\boxed{\lambda_{\rm fus}=0,\qquad
\lambda_{\Gamma}+\lambda_{\rm int}+\lambda_{\rm mach}\le1.}
$$

This condition is also **sufficient** for every other authentic row: INSTALL has discharge -lambda_int<=1, scans and malformed guards discharge zero, and FINISH is then at most one. The CNF, affine and separator weights are unrestricted nonnegative since those components vanish identically. This proves the exact **all-length** feasible tariff cone, not a finite-extrapolated conjecture.

An exact nonzero rational certificate is

$$
\boxed{\lambda=(0,0,0,0,1/4,1/2,1/4)}.
$$

Just before FINISH, Phi=1; at either terminal goal Phi=0, exactly matching the final cost one. At the standard blank-tape initial state, Phi=1/2; telescoping yields only a weak constant lower bound against the actual L transitions.

Concrete falsifiers are lambda_Gamma=lambda_interface=lambda_machine=1/2, yielding 3/2>1 at every FINISH, and lambda_fus=1/1024 with other weights zero, yielding cost claim 2 at n=11 on a real cost-one FINISH. A naive multiscale potential with one remaining flag at each of n scales and uniform per-scale weight 1/2 charges n/2 at the same final edge, already failing for n=3. Summable scale weights are not ruled out, but do not automatically provide a large initial gap.

## Authentic resource partition and transfer limitations

**Logical work** is a single cached source bit plus one message marker, not 2^n distinct operations. **Sequential elapsed time** and **physical total transition work** are both n+2; **parallel span** is n+2 because this is a single sequential machine, not 2^n processors. **Source traffic** counts every n+2 source read and n+1 input move; the final read of b is charged. **Peak writable space** is two physically visited cells and constant finite control. **Retention** is one cache cell; **retrieval/recomputation** of b is unnecessary, though the input remains readable. **Interfaces** have exactly one physical message M, installed then erased in paid transitions. **Evidence/output** is one decisive bit b, one cached output symbol and the YES/NO state. **Shared identity** appears as 2^n nonmaterialized views of one and the same source bit. There is no AND-branch, separate discharged proof obligation or paid derived-line identity per alias.

Hostile checks include b=0/1, malformed and prematurely ended strings, standard blank-work initialization, small and large n, exponential alias count, cache/message simultaneous write, nonnegative correlated weights and all terminal goals. This is compatible with TMR-2/035's public-affine quotient: all equal views would collapse to one distinct coordinate query. The present construction is not an adversarial SAT family; arbitrary SAT algorithms may also use Gaussian elimination, Horn/Krom, bounded-treewidth DP, autarkies, extensions, learning, preprocessing, rereading and alternate encodings. These remain unrestricted MAY behaviors outside this regular-language machine.

**Primary model reference:** Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, Section 2.1, original https://lance.fortnow.com/papers/files/tst.pdf (printed p.4 and visual screenshot inspected). FLMV chooses a distinct random-access/index-tape model; its SAT lower bound is not being imported. Original project safeguards from LEAD-0029, TMR-1/035, TMR-2/035, TMR-4/035, TMR-5/031 were reviewed. /341 remains FAIL as full logical authority, /386 remains RESTRICTED.

## Execution provenance, peer review and status

Exactly executed native CPython: experiments/tmr/tmr3_compact_fusion_native_audit056.py, Git blob **5cb6ff7c930488bca28be240d9fbd629cfef60ed**, independently read back and matching the local git hash-object. Exact raw stdout: results/raw/tmr/2026-11-14_2026_TMR3_COMPACTFAN056_NATIVE_RAW.json, Git blob **a558b692404553bdc21b3b3ea54460ae324600ee**, matching local output bytes. **33,234 assertion groups, 8,060 transitions, 671 tested inputs, zero failures**, including canonical n=1..80 and exhaustive binary strings up to length 8. Finite evidence is COMPUTATIONAL.

The additional self-contained interpreter experiments/tmr/tmr3_compact_fusion_tm056.py is **published but not natively executed**; no execution-identity claim is made for it. Mathematical all-n status rests on the fully enumerated fixed rule schema and the exact symbolic final inequality.

**Peer requests:** TMR-4 import the symbolic n-family into its exact LP and verify the negative INSTALL row, all goals and all-unbounded-n constraint; TMR-5 independently audit an actual fixed machine rather than the earlier command stream; TMR-2 quotient identical aliases and investigate genuinely distinct fusion/affine obstructions; TMR-1 qualify the regular-language model separately from SAT Q-TM/Q-RES-H.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, full proof2 blob 930c5eeddafce656717f28055a7a9a755f44737c, full canonical main.tex blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 were read, unchanged. Governing fusion directive rechecked, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. Five existing schedules unchanged. The fusion-safe superpolynomial initial gap, all-machine transition coverage and same-system SAT transfer remain OPEN. **P versus NP OPEN.**

END_OF_REPORT::TMR3::035::COMPACTFAN056::2026-11-14_2026_PST
