# LSPV-4 ARC-TARGET-QUOTA-BATCH284
**October 31, 2026, 16:36 PDT.** **PROVED/EXACT only for a declared restricted source-validation architecture**, mathematical external referee pending. **COMPUTATIONAL** certified both-label controls. The fully charged hereditary ARC contractor, numerical FLMV transport, and **P versus NP remain OPEN**.

## Exact obstruction and falsifiers
The canonical NP-complete target is Döcker's **duplicate-free proper clausewise-monotone 3-SAT-(2,2)**. Three different names of the same sign occur in each clause, and every original variable occurs twice per sign. A total decider must reject malformed strings. The broader proper strict-2P2N source is comparison only, not the hardness target.

F1. Can a quota verifier that retains only a small block of per-variable counters and repeatedly scans every source clause meet ARC's N^(11/10) local time and N^(1/2) workspace? **No, for this restricted policy.**
F2. Do two positive/two negative occurrences per variable suffice to recognize the target grammar? **No:** duplicate clauses, mixed-sign clauses, and repeated variables can each preserve the quotas.
F3. Does cumulative physical **counter subtape** XOR increase with the number of source rescans? **No:** exact formula below, even when source reads vary by a factor of 198.
F4. Does the policy-specific scan lower bound imply unrestricted target-SAT hardness or FLMV transport? **No.** Other algorithms, random access, sorting, source-authenticated output emitters, and caching are not excluded.

## Two proved restricted theorems
For a valid target with n variables, m=4n/3 clauses, fixed-width w=floor(log2(n))+1 identifiers, a 1^w 0 bin_w(n) header and records of one sign plus three w-bit source IDs, payload P=m(1+3w), source length N=P+2w+1=Theta(n log n).

**Architecture B_b:** consecutively authenticate up to b variable names at a time. For every batch scan *every* original clause; maintain two saturating binary 2-bit counters per active variable; check both signed quotas exactly two; reset between batches, and retain no inter-batch cache or compressed source summary. Syntax/uniqueness validation is additional.

**Theorem 1.** On every valid original target, number of scans p=ceil(n/b), exactly R=P*p input payload-bit reads, m*p original-clause visits, 3*m*p original signed-literal inspections, 4*n counter increments, and a fixed 4*b-bit counter tape. Hence
R*S_counter = 4*P*b*ceil(n/b) >= 4*P*n = Theta(N^2/log N).
If S_counter <= N^(1/2+o(1)), then R >= N^(3/2-o(1)) for this model. **Proof:** the batches partition all n original variable names, every pass scans every source clause, and valid 2P2N gives four occurrences per variable. The inequality follows from b*ceil(n/b)>=n. Every index/head move, parse, selector or child-work cost is additional. This is NOT a general grammar-validation or SAT lower bound.

**Theorem 2, fixed physical counter tape.** Encode each of two signed counters per active variable in two fixed binary bits; initially all zero, split each changed bit into its own physical work-tape write, and clear only between batches. Let ell=n-(ceil(n/b)-1)b. Each signed counter runs 00 -> 01 -> 10, contributing 1+2=3 adjacent bit changes. The exact counter-tape XOR path is
D_counter=6*n+2*(n-ell), and the counter-tape endpoint Hamming distance is 2*ell.
The counter tape's adjacent XOR is always between 6n and 8n, although source reads vary from P through P*n. This counter **subtape** is not the entire native FLMV physical state; the input is immutable, and head movements, indexed tape creation/erasure, scratch, replay and policy work are separate. Full-state XOR is offline experimental measurement, not a free solver oracle.

**Malformed quota-correct counterexamples:** six-variable formulas with duplicate positive and negative triples; a paired sign flip making two Y6 clauses mixed-polarity; a positive-variable occurrence swap yielding a repeated name within one clause. Every counterexample has exact 2+/2- quota, but must be rejected by a valid total target decider.

## Same-source certified SAT and UNSAT
Y6: SAT, 6 variables/8 clauses, 20 exhaustively verified models; U198: UNSAT, 198/264, six independently refuted original-source private modules (179 DPLL nodes each) plus every one of 64 boundary assignments ruled out; V198: SAT, complete checked 198-bit witness after swapping the first positive literals in zero-based U198 clause indices 1 and 7. Do not confuse this V variant with the different 2/44 counterpart. Independent no-producer-import checker passed **73,928 checks**.

| b | Passes U/V | Source payload reads U/V | Fixed counter bits | Adjacent counter XOR U/V |
|---:|---:|---:|---:|---:|
| 1 | 198 | 1,306,800 | 4 | 1,582 |
| 8 | 25 | 165,000 | 32 | 1,572 |
| 32 | 7 | 46,200 | 128 | 1,572 |
| 64 | 4 | 26,400 | 256 | 1,572 |
| 198 | 1 | 6,600 | 792 | 1,188 |

Both U198 and V198 have original-clause pair compatibility: 351 same-sign (SS,SU,US,UU)=(1,0,0,1), 786 opposite-sign (0,1,1,0), 33,579 disjoint (1,1,1,1). Both coherent all-0/all-1 histograms are (132,0,0,132). Historical full original-clause occurrence S/U and inverted targets, all indexed pairs, and flip/complement trails were independently rechecked and retained in the full local reproducibility archive. Original-clause IDs touched by each batch are included in the run's expanded raw. Matched capped UP-DPLL: Y6 SAT in 4 nodes; U/V **UNKNOWN** at the same 1,200-node limit, NOT UNSAT proofs.

## FLMV and ARC boundary
FLMV Theorem 5.7: f_0=1, f_k=c*f_(k-1)/(1+f_(k-1)); d_k(c)=min((1/f_k-c)/k,c^(-k)). Exact rational arithmetic independently confirms d_*(6/5)=23/45 and d_*(241/200)=11642479/23232400; k=2 uniquely maximizes both, with the entire tail k>=4 excluded by d_k<=c^(-4)<d_2. These numerical constraints apply to the SAME deterministic indexed-input TM for ordinary SAT and do not transfer from NP-completeness alone. Proposed fixed point (6/5,1/2) is conditional: no uniform hereditary, malformed-rejecting, fully charged arbitrary-A to Phi(A) contractor producing shorter target-valid children has been proved, nor a quantitatively sufficient SAT-to-target reduction/direct bound. CONSTRUCTION-STRENGTHEN17 still lacks the strict22 bit-local emitter; CP22LIFT1 and AFFINE-SMALLBIAS-DESCENT-GATE2 are not replacements.

## Pre-proof literature, GitHub and duplication audit
Read project root main.tex, AGENTS.md, CODEX.md, the pnp-research skill, active issue #3, REDIRECT1, CONTRACT1, AFFINE-GATE2, CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, latest LSPV-1/2/3/4/5 reports, and prior SOURCE-SCAN-SCHEDULING69/CHILD-SCAN-AMORTIZATION272. Web queries: FLMV indexed model and Theorem 5.7; Döcker Monotone 3-SAT-(2,2) proper clause grammar; Munro--Paterson limited-storage sorting; Beame--Clifford--Machmouchi element-distinctness tradeoffs; Darmann--Döcker 2021. Primary sources: https://lance.fortnow.com/papers/files/tst.pdf ; https://arxiv.org/abs/1912.08032 ; https://wrap.warwick.ac.uk/id/eprint/46321/ ; https://arxiv.org/abs/1309.3690 ; https://doi.org/10.1016/j.dam.2020.12.010 .

Project GitHub queries: INDEX RESET; XOR INDEX; source scan per child; counter budget validation; payload sensitivity composition; clause count invariant. Search of github.com/openai for FLMV found irrelevant dependency lockfile hits; search tape xor state found https://github.com/openai/math/blob/main/lean/OAI/Computability/DepthThree/TapeXor.lean, a different tape model and not FLMV verification. Earlier LSPV-1 PAYLOAD-SENSITIVITY284 establishes accepted-target payload reading; LSPV-5 REFEREE251 already reduces logical flip XOR to activity. Neither is claimed new. Multipass storage tradeoffs are known from Munro--Paterson. The new restricted claim is the joint exact batch-quota product and fixed counter-subtape XOR identity, with independent same-target tests and malformed source counterexamples. External mathematical referee and native end-to-end FLMV benchmarks remain pending. Repository preflight unavailable locally because repo checkout is absent; GitHub connector reads/writes and readback serve as fallback.

**Single next arrow:** a uniform both-label-correct all-valid-target and malformed-rejecting source-authenticated hereditary arbitrary-A to Phi(A) contraction that charges ALL source, child, selector/switch, guest, work/index, output-bit accessor, failed route, replay and simultaneous retained writable state, plus quantitative FLMV transfer. **P versus NP OPEN.**