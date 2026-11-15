# TMR-3/042: synchronous physical I/O, terminal fusion, and an exact seven-column tariff

**2026-11-15 03:30 PST | SYNCIO089 | PNP Time-Space Tradeoffs.**
Governing priority: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md`, SHA `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`. **PROVED/RESTRICTED** for the explicitly qualified finite-alphabet physical I/O task, independent mathematical review **OPEN**. Native V8 checks are **COMPUTATIONAL**. There is **no unrestricted SAT lower bound** and **P versus NP remains OPEN**.

## 1. Candidate and precommitted falsifiers

**Candidate.** A genuine physical multitape transition can authenticate a new input cell, physically write the corresponding mandatory output cell, and terminate, all at unit price. The resulting *joint* fusion-Lipschitz tariff, not separate input/output/terminal charges, may be derived exactly for a complete class of local-head microsteps. It should certify the true minimum work of an explicit streaming copy task.

**Four falsifiers specified before primary literature and repository audit.** (F1) A physical transition may correct more than one cell on the one designated output tape; (F2) a machine may jump its read-only local head over multiple unobserved input positions in one transition; (F3) the final output correction and successful HALT may occur simultaneously, invalidating separate full prices; (F4) a compact representation, copied cache, reread, or other extra tape can bypass the requirement to physically fill the specified output cells. F1 and F2 are excluded by the *explicit finite-alphabet, single-head local-movement model*, F3 actually occurs and forces the joint price inequality, and F4 fails only for the **explicit full-output contract**. F4 remains a valid shortcut to any attempted transfer to a one-bit SAT decision service.

## 2. Sources and novelty boundary

The current directives, both root proof trackers, root `main.tex`, issue #3, `AGENTS.md`, `CODEX.md`, repository skill, and latest five TMR handoffs were recovered. The large root `proof2.txt` (SHA `930c5eeddafce656717f28055a7a9a755f44737c`, 1,051,196 chars) and `main.tex` (SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`, 2,545,859 chars) required Git blob fetch because ordinary contents reads returned empty bodies. The original TMR-3/037 proof-record serialization report, TMR-3/041 output-only tariff report/matrix, TMR-2/041 signed leaf quotient, TMR-4/042 canonical leaf-core tariff and TMR-1/042 connected width-two/rank countercontrol were examined. LEAD-0029 is the earlier failed raw-semantic-mass Lipschitz audit.

Historical machine-model context: Hartmanis and Stearns (1965), *On the Computational Complexity of Algorithms*, `https://doi.org/10.1090/S0002-9947-1965-0170805-7`; Hennie (1965), *One-tape, off-line Turing machine computations*, `https://doi.org/10.1016/S0019-9958(65)90399-2`. Neither is credited with this elementary copy-task theorem. The incremental finding relative to TMR-3/037 and /041 is the exact **joint ingress, output, and halt** charge on *actual simultaneous local-head physical steps*, rather than only output+halt or a postcomputation output phase.

## 3. Qualified physical state, all-step inventory, and goals

Fix an arbitrary finite binary string `x` of length `n>=0`. Its immutable read-only input tape has cells `0,...,n` containing `x#` with endmarker `#`; let `B=n+1`. A single designated output tape starts blank and has one finite-alphabet read/write head. Both heads start on cell zero and move at most one cell per transition. Each physical multitape transition reads the currently scanned source and output symbols, can rewrite **at most one designated output cell**, change finite control, move both heads locally, update arbitrary finitely many other work tapes through their own one-head-per-tape ports, and optionally halt. Every such transition costs **one**. Work-tape caching, extra scans, deletion, recomputation and head reversals are allowed with their usual transition price. A fixed program has a fixed finite number of tapes and states. The abstract envelope is **not** a new unit-cost RAM, an unbounded-parallel tape operation, or a free oracle.

A successful `COPY` goal is deliberately stronger than merely producing a YES/NO answer: (i) the source `#` at input index `n` was authentically read in the execution, (ii) all `B` physical designated output cells currently contain the **literal** stream `x#`, and (iii) the machine has successfully halted. A machine halting without these conditions has **not** completed this qualified task. No source-correctness hypothesis or family-specific certificate is precomputed for the machine.

The full ghost-instrumented concrete configuration retains the exact input, fixed program, all tape contents, all head coordinates, control state, paid transition ledger and the **historical largest actually read source position** `r` (initially `-1`). `r` is used by the analyst, not an uncharged oracle available to the machine. Set `c(C)` to the number of the `B` designated output cells whose **current** symbols equal the corresponding source symbols. Previously written but now corrupted cells do not count. Let `h(C)=1` before successful halt and `0` afterward.

**Zero-cost closure:** there is no physical zero-price transition. Thus all genuine zero-cost SCCs are singleton; `cl_0` is identity. Reversible metadata view aliases, if added, can be quotient-equivalent only where they preserve the complete physical configuration and every potential component. No zero-cost PEEL, source proof step or macro output is smuggled into this system.

## 4. Reduced-product potential and complete local tariff

In the shared canonical order (CNF, affine, separator, fusion, Gamma, interface, machine), define

$$
\mathbf p(C)=(0,0,0,0,0,\; B-1-r(C),\; B-c(C)+h(C)).
$$

The first nonzero component is the actual unvisited input frontier, not source Shannon entropy; the second counts currently incorrect literal output cells **plus** the unfinished successful-halt obligation. Both are nonnegative and both vanish at every completed goal.

Write `a=lambda_interface>=0`, `b=lambda_machine>=0`, setting the other five coefficients to zero. Any authentic paid step satisfies

$$
\Delta_{\rm int}\le1,\qquad
\Delta_{\rm machine}=c(C')-c(C)+h(C)-h(C')\le2.
$$

The first inequality follows from one input head with unit movement (a previous rightmost read can advance by at most one); input rereads may give zero discharge. The second follows because only one physical output cell can change its correctness and a transition can switch successful-halt status at most once. Corrupting a correct cell gives a **negative** discharge, which is kept rather than silently discarded. Each underlying physical step, including any simultaneous source read, output write, work-tape mutation, and control change, still costs exactly one.

A complete sufficient *all-transition* condition is therefore `a+2b<=1`. It is also **necessary**, since the final transition of the fixed copier below has the physically real discharge `(Delta_int,Delta_machine)=(1,2)` for price one. Consequently the exact uniform nonnegative cone on the two live coefficients is

$$
\boxed{a\ge0,\quad b\ge0,\quad a+2b\le1.}
$$

The physical bit-copying rows are `(1,1)` at all nonterminal positions and `(1,2)` at the endmarker. Additional legal MAY rows include input-only `(1,0)`, output-only `(0,1)`, revisit/cache work `(0,0)`, signed corruption `(0,-1)` and `(1,-1)`, halt-only `(0,1)`, write-last-and-halt `(0,2)`, and their nonpositive variants. These are all charged one even when the obstruction vector is unchanged. No source-algebra, clause elimination or output compression is granted for zero cost. The complete JSON matrix lists the physical preconditions and signed rows.

A stronger fine-grained view separates `q=(unread input, incorrect output cells, unfinished halt)`. The authentic final microstep simultaneously reduces all three by one, so its nonnegative uniform tariff must satisfy `lambda_read+lambda_write+lambda_halt<=1`. The displayed seven-column cone is its aggregation with equal weights on output and halt.

**Exact counterexample to additive pricing:** `a=b=1` charges the real endmarker-read+last-write+halt step by `1+2=3` although its physical price is `1`. It also charges each ordinary read+write by `2` instead of `1`. Any sum of input-parsing and explicit-output lower bounds that treats these as disjoint budgets without a serialization proof is unsound.

## 5. Fixed deterministic finite-alphabet machine, exact work and rational LP

Let one single **fixed** two-tape machine `M_sync` have nonhalting state `q` and accepting state `H`. Its complete behavior on every valid source `x#`, for output blank `_`, is:

- `(q,0,_)`: output `0`, move both heads right, remain in `q`.
- `(q,1,_)`: output `1`, move both heads right, remain in `q`.
- `(q,#,_)`: output `#`, keep heads in place, enter `H`.

Off this valid promise, a fixed total rejecting cleanup may be defined; it has no bearing on the successful copy language. This is an **actual** finite-state locally moving Turing machine, not a record macro. It visits the `B` source cells in order, writes all `B` designated output cells and halts on the final write, in exactly

$$
\boxed{T_{M_{sync}}(x\#)=B=n+1.}
$$

The initial seven-vector is `(0,0,0,0,0,B,B+1)`, the final vector is zero, and the tariff LP is

$$
\max_{a,b\ge0}\bigl[Ba+(B+1)b\bigr]\quad
\text{subject to }a+2b\le1.
$$

For every `B>=1`, its exact optimum is **B**, attained by `(a,b)=(1,0)`. The exact dual has one multiplier `y>=0`, requires `y>=B`, `2y>=B+1`, and is feasible at **y=B**. Thus both independently checked primal and dual equal the actual cost `B`. The fractional rational certificate `(a,b)=(1/2,1/4)` also satisfies every row, but is weaker. The potential telescopes along *any* successful completion in the qualified physical envelope and gives the exact bound `W_min(x#)=B`. Independently, one designated output head must physically correct/write at least B initially blank required output cells.

## 6. Joint time/space/evidence ledger

For `M_sync`, the source has `B` physically read symbols including its endmarker and the designated output has `B` physically written symbols. There is also one logical successful HALT event. These are `2B+1` **overlapping logical milestones**, not `2B+1` physical instructions. Elapsed sequential time and physical work are each `B`, and the machine's sequential dependence span is `B`. Explicit output evidence occupies `B` physical finite-alphabet cells. The peak visited writable storage is `B` output cells and **zero other work cells** for this machine. There are no messages, branch/AND obligations, authenticated proof line identities, or separate caches in the copier. The larger all-step envelope admits caching, rereading, recomputation, arbitrary work tape changes and overwrites; all remain charged per physical step and no such behavior permits writing two designated output cells in one step.

**Cost partition proved:** a single native multitape transition is the shared cost identity. Source-read, output-write, and control-halt events in that same transition are *not* three independent prices. This is precisely the fusion-safe ledger required before component tariffs can be added.

## 7. Executed checks and falsification controls

The exact published V8 `audit()` implementation checked **8,191 binary sources of lengths 0 through 12**, with **98,305 actual simulated copy transitions**, all outputs and goal conditions exact. It also enumerated **1,286,676** signed local-microstep templates through length four, including input rereads, one-cell rewrites, output corruption, correct-cell restoration, work-tape placeholders, and genuine terminal cases. **285,460** negative-discharge rewrite controls and **2,106** positive terminal-control rows were visited. The final executed tally was **4,758,942 assertions, zero failures**. Exact rational grid certificates were checked by scaled integer inequalities `di<=1`, `dm<=2`, `2di+dm<=4`, `6di+7dm<=20`, rather than approximate LP floats. These exhaustive finite tests are only **COMPUTATIONAL**; the all-length theorem above is the independent symbolic argument.

The code was executed directly in the hosted V8 runtime and the exact function body serialized to `experiments/tmr/tmr3_sync_io_tariff089.js`. The standalone Node wrapper is not separately tested, and no generalized SAT algorithm, compiled arbitrary TM simulator, exhaustive proof-calculus verifier or LaTeX build was executed.

**Artifacts:** code `experiments/tmr/tmr3_sync_io_tariff089.js`; raw `results/raw/tmr/2026-11-15_0330_TMR3_SYNCIO089_V8_RAW.json`; complete matrix `results/raw/tmr/2026-11-15_0330_TMR3_SYNCIO089_TARIFF_MATRIX.json`.

## 8. Exact status, transfer firewall and peer repair

**PASS / PROVED/RESTRICTED:** exact native `M_sync` copy trace; jointly costed source read + output write + halt; complete seven-column envelope tariff; nonnegative exact primal/dual optimum `B`; identity zero-cost quotient; full-output goal preservation. Independent mathematical peer review remains **OPEN**.

**FAIL:** assigning separate unit tariffs to authenticated ingress, literal output emission and HALT when a native transition can fuse these. Such a tariff overdischarges the actual final microstep by a factor of three.

**RESTRICTED:** `B` means required explicit copy-stream length, **not** ordinary SAT decision time; no machine is compelled to print `x#` or a proof. Source authentication is an express goal of this toy service and cannot be imposed on an arbitrary SAT algorithm without proof.

**OPEN:** a dynamic nonaffine SAT fusion component with a superpolynomial initial gap and a same-system, all-correct-algorithms transfer theorem. The exact copier gives only a linear bound and cannot be used as a candidate P-versus-NP separation. Historical `/341` remains **FAIL** as full logical UNSAT authority; `/386` remains **RESTRICTED** to its guarded tested fragment.

**Next peer repair:** TMR-4 should import the signed two-coordinate envelope into a full-state zero-cost/LP audit, explicitly retaining the actual `(1,2)` terminal row. TMR-2 should separate mandatory physical output from semantic/evaluation-matrix views. TMR-1/5 should reject transfer of `B` explicit-output work to one-bit SAT decision and independently replay the all-step bound. TMR-3's next physical target is a fully implemented *source-authenticating signed-NAE leaf recognizer* with end-to-end charged head movements, parser memory and witness verification.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root proof trackers and canonical `main.tex` are left unchanged; all five TMR agents and their hourly Pacific schedules are unchanged.
