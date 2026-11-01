# LSPV-4 ARC-ZERO-CYCLE-CUBIC300

**November 1, 2026, 04:59 PST | Circuit Resource Auditor.** Status: **PROVED/EXACT, restricted implementation theorem; COMPUTATIONAL, independent controls; CONDITIONAL, FLMV transport. P versus NP OPEN.** Independent external review pending.

## Exact obstruction and original-source theorem

Adopt the verified SATURATED-CYCLE-AFFINE-TERMINAL1 restricted theorem from the 01:48 five-role handoff, with authenticated source M22 residuals and `delta=2f-u-eta-nu=0`. Its exact GF(2) terminal still has to **acquire** and validate the edge-disjoint odd-cycle family and pay native indexed-input operations. Its derived residuals are not necessarily valid canonical Döcker children.

Original canonical F9 has positive clauses (1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9), and negatives of (4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9). It has 9 variables, 12 unique proper monotone clauses, exact 2+/2- quotas, and 70 full SAT models.

Two coherent **partial assignments on this same original source** independently certify both answer labels:

| Fixed original-variable cube | Free f | Uncovered u | Spill eta | Cycles nu | delta | Binary edges E | Complete models | GF2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| SAT: x1=0,x2=0,x8=1,x9=1 | 5 | 6 | 4 | 0 | 0 | 6 | 2 | rank 4 |
| UNSAT: x3=0,x6=1,x7=1,x9=1 | 5 | 6 | 4 | 0 | 0 | 4 | 0 | refuted |

The UNSAT affine contradiction uses three authenticated original-clause rows (zero-based IDs 2,7,11), whose GF(2) coefficient XOR is zero and RHS XOR is one. No invalid occurrence-level assignment is used.

**Restricted implementation theorem.** For t disjoint variable-renamed F9 copies, with either corresponding product cube, the original F9^t remains canonical, the root has 70^t models, the SAT cube has 2^t extensions, and the UNSAT cube has zero. Both have delta=0 and nu=0, with E=6t or E=4t. The **published actual greedy producer** `experiments/review/saturated_cycle_affine_terminal_greedy.py` materializes its binary-source-edge list and executes `for select in combinations(edges,3)` eagerly, even if no triangle exists. It therefore checks exactly `C(6t,3)` or `C(4t,3)` candidates, Theta(t^3) loops, before its one affine system. In the declared fixed binary encoding `N=2H+36t(B+1)`, `B=ceil(log2(9t+1))`, `H=ceil(log2(12t+1))`, this is Omega((N/log N)^3) native transitions **for a faithful implementation of this algorithm**. A fixed-width explicitly retained list of source clause ID plus 2 variable IDs needs `E(H+2B)=Theta(N)` addressed writable cells on the declared layout.

At t=64: N=25,364 bits, SAT E=384, triple inspections=9,363,584 and explicit record payload=11,520 bits; UNSAT E=256, inspections=2,763,520 and payload=7,680 bits. This acquisition violates the proposed ARC local time N^(11/10) and half-power writable-space budgets **only for this specific loop and representation**. Low-space mutual-minimum triangle selection, early UP, source rescans and sparse GF(2) remain legal alternatives and must be charged. Thus no lower bound on unrestricted SAT or arbitrary A is asserted.

## Evidence and same-source adversarial controls

The full independent no-import verifier passed **7,586 assertions**. It checked all 512 F9 assignments and 70 global models; both original-source cubes and 2 versus 0 completions; original S/U targets and inversions; all **264 original-clause SS/SU/US/UU extreme compatibility modes**; complete 0^9/1^9 true-literal histograms; nine coherent flip trails with changed original-clause IDs and logical XOR; six malformed-target rejections; affine witness and the three-row source-derived UNSAT refutation. A separate UP-DPLL baseline solved the same SAT cube in **two** search nodes (51 original clause checks) and the UNSAT cube in **one** node (23 clause checks). This is a hostile easy-family control that prevents falsely inferring algorithm-independent hardness.

With an explicitly declared indexed-input one-full-scan microprotocol at t=64, counted native components are: 25,364 source-bit reads, 181,368 index one-bit writes, 710,192 index-head moves, 25,364 indexed jumps, and 25,364 read actions. Sum 942,288. Index tape max extent 15 bits, cumulative adjacent **physical index tape-content XOR** 362,736, endpoint XOR zero. The independent N=188 microtrace checked 188 jumps, 680 index one-writes, 2,632 head moves, and 1,360 cumulative physical XOR. FLMV index jumps erase index contents atomically, so no unrestricted one-bit-per-index-step XOR inequality applies. These figures **exclude** address calculation, clause parsing, policy discovery/switching, failure costs, Gaussian elimination, row proof production, guests, ancestor retention and complete peak work/index space. They are not native end-to-end SAT timings.

## Exact actual FLMV Theorem 5.7 test and local-bit transport

Use f0=1, fk=c*f(k-1)/(1+f(k-1)), dk(c)=min((1/fk-c)/k,c^(-k)). Exact rational arithmetic gives `d*(6/5)=23/45` and `d*(241/200)=11642479/23232400`; k=2 uniquely maximizes each and the entire k>=4 tail is strictly less by `dk<=c^-4<d2`. For a hypothetical same-machine, fully local-bit-addressable SAT-to-canonical-Döcker reduction with output expansion exponent b, setup exponent a, guest-step accessor penalty theta and combined retained/index-space rho, transfer of a hypothetical canonical target solver (K,L)=(6/5,1/2) to the strict FLMV box c=241/200 requires `max(a,6b/5+theta)<241/200` and `max(rho,b/2,other simultaneously live peaks)<11642479/23232400`. At zero power-scale overhead, **b<11642479/11616200 ≈1.00226227**. This is only an algebraic necessary accounting window. Döcker NP-completeness alone and the existing **nonmonotone** strict22 compiler do not give such a bit-addressable numerical transport. No actual near-unit local-bit reduction or fully charged arbitrary-A→Phi(A) construction exists in the verified project.

Four falsifiers: F1, zero selected triangles means cheap discovery by the existing greedy policy, **FALSIFIED**; F2, retained explicit binary edge IDs fit half-power space, **FALSIFIED** for declared layout; F3, the implementation bottleneck applies to all SAT algorithms, **FALSIFIED as an inference** by matched UP-DPLL and alternative policies; F4, NP-completeness suffices for the numerical FLMV transfer, **REJECTED** for missing same-machine local-bit proof.

**Corpus and literature search:** Read handoff first, 01:44 theorem and both verifiers, AGENTS/CODEX/pnp-research, root main.tex, REDIRECT1/CONTRACT1, role-4 297–299, newest role-5 synthesis, and coordination issue #3. Primary web queries: FLMV Theorem 5.7 indexed input/atomic index erase; Döcker monotone (2,2) reduction; near-linear local-bit SAT normalization. GitHub project queries: `triangle greedy`, `local bit`, `Gaussian matrix`; independent `openai/math` query: `SAT formal`, found formalization work on bounded-width SAT but no verified canonical local-bit reduction; generic `openai` query failed a repository-name validation requirement. Search absence is not novelty. Prior LSPV-4 298 dense global-mask memory obstruction and 299 low-space triangle policy are explicitly distinguished.

Reproducibility: the full source producer, independent no-import verifier, raw original-clause-indexed JSON, exact FLMV fractions, physical microtrace, LaTeX/PDF report and SHA-256 manifest are in the companion archive; compact executable and result summary are published separately. Local artifact SHA-256: producer `125769b2836d091223aab891d4ac04c00cc57b249ed1a23fb04cc9e316e43890`; independent verifier `1a8f9ca5cc55cc05bf685618720e052294d662b6bf1590c407b5c2290733af67`; full JSON `6368f760bf60a7495a5616da27451b1e0cc19f2515038d3ed961299400821e35`.

**Next:** Audit low-space paid triangle-absence policies and GF(2) proof acquisition on both labels, with full source/address/proof/guest/ancestor accounting. Separately seek a near-linear truly local-bit ordinary-SAT-to-Döcker compiler. Preserve exact five roles/status/schedules; no changes requested or made. **P versus NP OPEN.**

Primary sources: Fortnow et al., JACM 2005, https://lance.fortnow.com/papers/files/tst.pdf ; Döcker 2019, https://arxiv.org/abs/1912.08032 ; project theorem https://github.com/j15marti/pnp/blob/main/research/review/reports/wrapper/2026-11-01_0144_SATURATED_CYCLE_AFFINE_TERMINAL1.md .

END_OF_VERIFIED_REPORT::ARC_ZERO_CYCLE_CUBIC300::P_VS_NP_OPEN
