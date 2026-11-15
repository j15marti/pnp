# TMR-4/038: Exact ancestry-connectivity tariff for source-authenticated XOR proofs, with fusion and zero-cost saturation falsifiers

**2026-11-14 22:49 PST | XORANCESTRY065 | PNP Cost-Sound Abstraction**  
**Status: PROVED/RESTRICTED for the precisely qualified inference-priced XOR authorities. Independent mathematical and machine-model review OPEN. Finite execution COMPUTATIONAL. P versus NP OPEN.**

## 1. Candidate and falsifiers fixed before source review

**Candidate:** On the Q-XOR3 source-bound shared-DAG proof calculus from TMR-1/037, distinguish (i) unacquired *authenticated source identities*, (ii) connected components of the *actual proof-ancestry fusion graph*, and (iii) the still-unperformed final HALT. The three quantities support a transition-by-transition nonnegative tariff, with an exact LP optimum equal to the authentic minimal inference-event work. The same structural potential must be recalibrated for either a one-price combined SOURCEADD operation or an authentic zero-price GF(2) span closure.

**Falsifiers:** (F1) a zero-price genuine GF(2) combination merges source ancestries and invalidates a raw positive fusion charge; (F2) a one-price SOURCEADD simultaneously discharges acquisition and connectivity; (F3) a false seven-clause source authentication or even-charge satisfiable source is wrongly accepted as a contradictory parity source; (F4) a native proof-event price is falsely promoted to physical Turing-machine time or to all-CNF SAT hardness. F1 and F2 produce legal witnesses *only in the explicitly augmented authorities*. F3 is rejected in the tested normalized grammar; F4 remains a fatal unrestricted-transfer restriction.

## 2. Controlling sources and provenance

The controlling fusion-Lipschitz refocus file was read FIRST: \`research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md\`, Git blob \`54c9177fc211dfca6c94d89d6ebbf3f3908809d6\`. Next: 2026-11-13 TMR replacement \`47459817e66dccf1f3079e6c724c0fd2643e7bc4\`; complete root \`proof1.txt\` SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`; complete \`proof2.txt\` authentic Git blob \`930c5eeddafce656717f28055a7a9a755f44737c\` (1,051,196 characters); complete canonical \`main.tex\` authentic Git blob \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\` (2,545,859 characters); \`AGENTS.md\`, \`CODEX.md\`, repository skill, all five current TMR handoffs, and issue #3 through TMR-3/037. The Contents API returned empty bodies for the two large files, so their authentic Git blobs were explicitly recovered. No shared root edits made.

Primary methodology [1] Cousot and Cousot, *Abstract Interpretation: A Unified Lattice Model*, POPL 1977, pp.238-252, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml ; [2] Hoffmann and Jost, *Two Decades of Automatic Amortized Resource Analysis*, Mathematical Structures in Computer Science (online 2022-03-16), https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/article/two-decades-of-automatic-amortized-resource-analysis/9A47A8663CD8A7147E2F17865C368094 ; [3] Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 2001, see original ECCC TR99-022 https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/index.html . [1,2] justify attention to abstraction and local costs but DO NOT supply the new XOR tariff theorem. [3] concerns **ordinary Resolution**, not XOR rules. All new assertions below are directly proved for their named authority.

Project originals: TMR-1/037 \`research/agents/tmr-1/2026-11-14_2156_TMR1_AUTHENTICATED_XOR_CALCULUS_QUALIFICATION037.md\` and its authentic rule inventory; TMR-3/037 \`research/agents/tmr-3/2026-11-14_2230_TMR3_XOR_BINARY_SERIALIZATION_TARIFF037.md\`; TMR-2/037 certificate envelope; TMR-5/033 fixed-source paid envelope; TMR-4/035 zero-cost SCC LP, /036 directed scalar closure, /037 paid Bellman envelope; LEAD-0029 historical Lipschitz audit. The native 2H price was **already proved by TMR-1/037** and independently checked by TMR-3/037. The new contribution is an **explicit shared-ancestry potential and complete exact cone**, plus rigorously compared zero-cost and one-price fusion variants. No claim of discovering the 2H number is made.

## 3. Qualified source, state, transition relation and model boundary

Fix a connected simple cubic graph \`G=(V,E)\` with \`H=|V|>=4\`, with exactly one locally authenticated four-clause proper-3CNF parity source group per vertex, and public vertex charges \`b_v\` of odd total parity. The original encoded CNF bit length is \`L_H=Theta(H log(H+2))\` under dense literal IDs, and is distinct from \`H\`, the inference-event count, and any MCSP truth-table length. Authentication must inspect the **actual four clauses**: a missing clause cannot be inferred for free.

For Q-XOR3, a complete concrete proof-prefix configuration includes immutable authenticated original formula, current source/derived row shared-DAG, each row's actual GF(2) coefficients and *full transitive source identity ancestry*, globally paid identity history, legal source group IDs, and a halted flag. Duplicate SOURCE or ADD nodes remain legal and charged; DAG reuse and reconvergence do not duplicate their earlier charge. Q-XOR3 permits only native \`SOURCE(i)\`, \`ADD(j,k)\`, \`HALT(j)\`, priced one each. HALT is legal only on an explicit derived \`0=1\` row. Its zero-cost closure is identity. Other SAT-machine instructions remain **unknown/MAY**; this is not a physical Turing-machine calculus.

Two **separate, explicitly augmented authorities** are qualified as hostile controls, not retroactively added to Q-XOR3:
- \`Q-XOR3-FUSE\` adds one-price \`SOURCEADD(i,j)\`: authenticate vertex source \`i\` and append its GF(2) sum with pre-existing line \`j\` as **one** charged primitive. An intermediate separate SOURCE line is not required. Other Q-XOR3 rules remain.
- \`Q-XOR3-GFREE\` adds authentic zero-price \`GFADD(j,k)\` and allows finite saturation by GF(2) linear combinations of already acquired rows. SOURCE and HALT remain price one. The canonical zero closure is the complete *span of acquired source vectors*, not a guessed unbounded oracle: canonical source-provenance masks form a finite \`2^H\` domain. Full physical Gaussian elimination is **not** free on an ordinary machine; free means this distinct proof-event model grants the operation zero price. Its zero-cost paths may add rows but never acquire an unauthenticated source.

The resolution-tagged \`Q-TOTAL-XOR-RES\` of TMR-1/037 remains a different complete all-proper-3CNF proof authority. The recovered \`/341\` stays FAIL on its full accepted language and \`/386\` RESTRICTED. Neither is modified.

## 4. New explicit reduced-product obstruction

For a proof prefix C, let \`S(C)\subseteq V\` be the **set** of actually acquired source identities, \`m=|S(C)|\` (duplicates count once). Define the undirected source-ancestry equivalence graph \`K(C)\` on **all H genuine vertex identities** as follows: each SOURCE leaf supplies a singleton; each ADD joins the previously internally connected ancestry of its two input rows by one union edge between representative leaves. Existing shared source identities are the same vertex in K, not copies. A source identity not yet acquired is an isolated vertex. Define \`c(C)\` as K's component count. One ADD merges at most two previously internally connected components, so reduces c by at most one, no matter how many leaves each input has.

Use the three nonzero subcomponents of the project's seven-column vector (CNF, XOR, separator, fusion, Gamma, interface, machine):

$$
p_{\Gamma}(C)=H-m,\qquad p_{\mathrm{fus}}(C)=c(C)-1,\qquad p_{\mathrm{machine}}(C)=\mathbf1_{\neg\mathrm{halted}}.
$$

All other four components are zero for this **source-bound inference-priced subproblem**, not claims that they vanish in actual SAT-machine execution. Initial vector is \`(H,H-1,1)\`. If a valid HALT occurs, its contradiction row has left-hand-side zero and right-hand-side one. The connected incidence kernel is \`{0,1_V}\`: each edge (u,v) forces equal coefficients of u and v, connectedness makes them identical, and odd total charge excludes zero provenance. Hence every authentic goal must have acquired all H sources and has one connected ancestry containing all H identities; after HALT its vector is \`(0,0,0)\`.

**Local row theorem (all legal Q-XOR3 DAG prefixes, including duplicates, cancellations and sharing):**

| Authentic step | Price | \`(Delta p_Gamma, Delta p_fus, Delta p_machine)\` |
| --- | ---: | --- |
| SOURCE with previously unseen ID | 1 | (1,0,0) |
| SOURCE repeated ID | 1 | (0,0,0) |
| ADD joining two previously disconnected ancestries | 1 | (0,1,0) |
| ADD joining already connected ancestries | 1 | (0,0,0) |
| successful HALT | 1 | (0,0,1) |
| identity | 0 | (0,0,0) |

The **exact nonnegative linear tariff cone** on these three components is

$$
0\le\lambda_\Gamma\le1,\quad
0\le\lambda_{\mathrm{fus}}\le1,\quad
0\le\lambda_{\mathrm{machine}}\le1.
$$

Sufficiency follows by checking the six complete row classes. Necessity comes from an initial unseen-source step, an ADD connecting two genuine SOURCE ancestries, and a final HALT. The exact rational LP maximizing initial potential has certificate \`(1,1,1)\`, value \`H+(H-1)+1=2H\`. Telescoping under each actual inference-event edge and completed goal proves native shared-DAG price at least 2H. SOURCE all H, ADD in an H-1 chain and HALT supplies a matching 2H proof. This is a fresh cost-sound dual presentation of TMR-1's already-established combinatorial result.

**All-step abstraction relation:** map each concrete prefix to its exact seen-source bitset, the partition K induced by the *actual shared DAG*, and the halted flag. Every SOURCE, ADD and HALT maps to precisely one corresponding abstract edge of **identical** native price and related successor; identity maps to a zero abstract path. The source equation and full authenticated original remain in the concrete state. Thus the simulation is cost-underestimating on **every** qualified native step. No formula-syntax, physical-interface, or arbitrary-machine transfer is claimed.

## 5. Genuine paid fusion collapses the optimum

A legal \`SOURCEADD(i,j)\` in Q-XOR3-FUSE can simultaneously acquire a new source and connect it to an existing ancestry component. With source 0 already acquired and line 0 available, source 1 fused into it gives an actual one-price transition

$$
(\Delta p_\Gamma,\Delta p_{\mathrm{fus}},\Delta p_{\mathrm{machine}})=(1,1,0).
$$

Old weights (1,1,1) charge **2 for a price-1 operation**, a concrete violation, not a spurious path. The complete cone for the augmented authority becomes

$$
\lambda_\Gamma+\lambda_{\mathrm{fus}}\le1,\qquad
0\le\lambda_{\mathrm{machine}}\le1,\qquad \lambda_\Gamma,\lambda_{\mathrm{fus}}\ge0.
$$

Its initial LP optimum is \`H+1\`, attained by (1,0,1), because H>H-1. It is tight: SOURCE one row, apply H-1 fused SOURCEADDs, and HALT. Repeated SOURCE or reuse cannot produce a cheaper contradiction by the source-identity kernel bound. This is a **different proof-authority price**, not an instruction that an actual finite-state machine can parse a full CNF source in one time step.

## 6. Authentic free span closure changes the abstraction, not the source truth

In Q-XOR3-GFREE, a free GFADD joining two independent acquired source rows decreases the **raw** fusion component by one at price zero. For H=4 and already acquired sources 0,1, the legal free sum has raw delta (0,1,0) and price 0, directly falsifying every unclosed positive fusion tariff.

Correct directed zero-cost saturation gives the closed fusion component

$$
p_{\mathrm{fus}}(\operatorname{cl}_0 C)=
\begin{cases}
H-1,&m=0,\\
H-m,&m\ge1.
\end{cases}
$$

Reason: free span can connect all m acquired source identities (using m-1 free additions), while each of H-m unacquired identities is isolated. Source identities and their authentication are unchanged. This closure is representable by a finite GF(2) basis / acquisition set without materializing all \`2^m\` combinations. All genuine zero-cost GFADD steps have **zero** delta *after* closure; no real cheap path is deleted.

A paid SOURCE after m>=1 now reduces both source deficit and *closed* fusion deficit, producing (1,1,0) at price one. Hence the exact closed-cone constraints coincide with the fused authority's \`lambda_Gamma+lambda_fus<=1\`, \`lambda_machine<=1\`. Their optimal initial potential is H+1, matching H paid SOURCE acquisitions and one HALT with free span. **It would be incorrect to conclude that free GFADD forces lambda_fus=0 after canonical zero closure; what it forces is a recalculated coupled SOURCE row.**

## 7. Machine-readable matrix, rational LP and executed hostile controls

Artifacts:
- exact published native V8 source: \`experiments/tmr/tmr4_xor_ancestry_tariff065.js\`;
- original native-run evidence: \`results/raw/tmr/2026-11-14_2246_TMR4_XORANCESTRY065_V8_RAW.json\`;
- seven-column rule inventory and tariff schema: \`results/raw/tmr/2026-11-14_2246_TMR4_XORANCESTRY065_MATRIX.json\`.

The ECMAScript source function was executed in native V8 and published using the same function serialization; final standalone startup/console wrapper was not independently re-executed byte-for-byte. The finite experiment completed **2,013,519 assertion checks with zero failures**, **75,324 charged/zero test edges**, including **16,971 free-GFADD edges** and **13,651 fused SOURCEADD edges**. It ran H=4 K4 and H=6,8 cubic prism graphs, tested charge-even satisfiable controls, duplicate source acquisitions, shared reuse, GF(2) provenance and ancestry connectedness, complete constructive proof certificates and malformed seven-clause group cardinality. The parity control is *not* a physical parser replay, and H=6,8 prisms are not claimed to be expanders.

A separate exact BigInt-rational three-variable LP enumerated all feasible vertices for H=4,6,8,100, with maxima base 2H and fused/free H+1. Finite checks validate code and detect counterexamples, not the all-H theorem (proved symbolically above).

The explicit row-by-row (not only average) cone and upper/lower matching proof are **PROVED/RESTRICTED**, awaiting peer review. \`Q-XOR3-FUSE\` and \`Q-XOR3-GFREE\` are deliberately stronger, distinct authorities. Other genuine shortcuts in a physical SAT machine remain **MAY**, including complete Gaussian elimination, preprocessing, compact parity circuits, learned clauses, autarkies, and source rereads.

## 8. Dependency ledger and next discriminating target

- **PASS/RESTRICTED:** TMR-1/037 authentic SOURCE grammar and connected-kernel theorem, under its declared source-bound XOR calculus; TMR-3/037 explicit binary output price remains a *separate* physical proof-serialization model.
- **NEW PASS/RESTRICTED:** exact three-coordinate shared-ancestry tariff cone for the original calculus, all-step cost simulation, closed-cone recalibration for two explicit cheap-mechanism variants.
- **FAIL:** old (1,1,1) tariff after authentic one-price SOURCEADD or after treating a free GFADD as chargeable; neither shortcut may be CEGAR-refined away.
- **OPEN:** full same-system arbitrary total deterministic SAT-machine transfer, arbitrary compact algorithm and proof authorities, nonaffine fusion obstruction, and a superpolynomial initial gap on one explicit growing family.
- **Growth ceiling:** all three authorities have exact upper price O(H) and encoded \`L_H=Theta(H log H)\`; no valid tariff on this family can be superpolynomial. Counted source identities are linear in authenticated input size.

**Next TMR-4 target:** instrument the source-authenticated Q-TOTAL-XOR-RES mode selection and actual published proof-record output grammar in one *typed*, exact paid/zero abstract product, then falsify attempts to combine a RES-only exponential component with a cheap XOR-derived goal. Request TMR-1 audit the source ancestry and completeness; TMR-2 audit the free GFSPAN saturation, any shortest-path/online quantifier confusion; TMR-3 audit the one-price fusion versus physical output serialization; TMR-5 independently reproduce the exact cones and seek a legal cheaper joined proof.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root proof1/proof2/main.tex write, no schedule modification. P versus NP remains OPEN.
