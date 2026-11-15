# TMR-4/052: Switch-count-aware multicut rank transfer for ordered branching programs

**2026-11-15 12:35 PST | TMR-4, PNP Cost-Sound Abstraction | Tracks A/C**  
**PROVED/EXACT (restricted algebraic lemma, independent mathematical review OPEN); COMPUTATIONAL for finite tests; unrestricted circuit/SAT-machine transfer OPEN. P versus NP OPEN.**

## 1. Candidate and falsifiers, fixed before source and project comparison

**Candidate MCFR052.** For EVERY Boolean function f on n bits, EVERY fixed variable order pi, EVERY deterministic shared ordered read-once BDD B that follows pi (skipped tests and early terminals allowed), EVERY nontrivial partition P=(X,Y) of its ORIGINAL variables, and EVERY field K, relate the rank of the assignment evaluation matrix M_P(f) to the ordered frontiers crossed when pi switches between X and Y. Count shared graph nodes once.

**Four falsifiers:** (F1) DISJ_k has rank 2^k at the grouped X:Y cut but an O(k)-node interleaved BDD and O(k)-gate circuit. (F2) IP_k has GF(2) rank k but rational rank 2^k-1. (F3) expander Horn / equality and unique-witness CNF can exhibit high restricted representation width despite cheap circuits and decisions. (F4) an alleged #SAT speedup may hide live gate, wire, Tseitin auxiliary-variable, interpolation or coefficient charges. All legal shortcuts remain legal.

This is the **assignment-evaluation function of one fixed formula**, not the SAT language on binary encodings.

## 2. Exact lemma and proof

For pi=(pi_1,...,pi_n), let Q_i be the set of distinct Boolean residual functions after assigning the first i variables, with BOTH constant terminals retained when reachable, and let q_i=|Q_i|. For the actual shared BDD, each cofactor is represented by at least one reachable frontier node, so q_i<=|F_i(B)|<=V(B)+2, V being distinct internal nodes.

For partition P=(X,Y), put D_pi(P)={i: 1<=i<n and pi_i,pi_(i+1) belong to opposite sides}; let b=|D_pi(P)|>=1.

**Theorem MCFR052-A (PROVED/EXACT restricted).** For EVERY field K:

    rank_K(M_P(f)) <= PRODUCT_{i in D_pi(P)} q_i
                      <= PRODUCT_{i in D_pi(P)} |F_i(B)|
                      <= (V(B)+2)^b.

In particular V(B)>=rank_K(M_P)^(1/b)-2. For a fully leveled oblivious branching program the actual layer widths w_i replace the F_i.

**Proof.** Distinct residual functions form a deterministic complete leveled automaton. Its layer-i transition matrices A_i(0),A_i(1) have exactly one 1 per row and map Q_(i-1) to Q_i. There exist fixed initial row alpha and accepting column omega with f(z)=alpha A_1(z_pi1)...A_n(z_pin) omega. Split this ordered product into maximal consecutive X-only and Y-only blocks. Insert identity sums over Q_i at EVERY boundary i in D_pi(P). Each choice of one boundary state per switch contributes the product of X-only scalar factors F_t(x) and Y-only scalar factors G_t(y). Thus M_P is a sum of at most PRODUCT q_i matrices F_t G_t^T, each of rank at most one. This proves the first bound in ANY characteristic. Since every cofactor has a reachable BDD frontier node, q_i<=|F_i|<=V+2. QED.

**Restricted all-step undercharging.** Map each reachable BDD state to its Boolean residual function. A paid test maps to its correct residual transition; skipped tests are identity/pass-through zero-cost transitions and early terminals absorb with matching truth labels. Every actual BDD test path is matched by a finite quotient path with no more paid Boolean tests. This does NOT account for arbitrary TM input seeking, addressing, storage, basis discovery or order switching and is NOT a general SAT-machine simulation. Generating Q_i explicitly can take exponential memory: this is a semantic proof object, not an online algorithm.

The product of frontier sizes is NOT a time tariff. A single shared gate can support many cuts; multiplying or summing ranks across cuts and billing them as independent work is not justified.

## 3. Authentic falsifiers and field sanity

DISJ_k(x,y)=PRODUCT_i(1-x_i*y_i) has x:y matrix the k-fold tensor power of [[1,1],[1,0]], hence rank 2^k over every field. With grouped order (x_1,...,x_k,y_1,...,y_k), b=1, so the rank requires an exponential frontier. With interleaved order (x_1,y_1,...,x_k,y_k), b=2k-1, a deterministic read-once diagram has exactly 2k internal nodes (TMR-4/051) and a synchronized frontier peak at most three: active, remembered x_i bit, dead. The general circuit has O(k) gates/wires and the all-zero assignment satisfies DISJ. Consequently the proposed FALSE inequality rank(M_P)<=max_i|F_i| for an ARBITRARY partition fails at k=3 with 8>3. The switch-product bound survives. This is a genuine legal cheaper ordering, not a CEGAR spurious path.

For IP_k(x,y)=XOR_i(x_i AND y_i), the GF(2) matrix is a sum of k outer products and its one-hot k-by-k minor is I_k, giving rank k. Over Q write M_IP=(J-H)/2, where H_(x,y)=(-1)^(x dot y) is invertible. H e_0=1 implies ker(J-H)=span(e_0), hence rank 2^k-1. Thus the algebraic transfer must specify the field: TMR-2/051 already established this exact model-scoped result. Walsh-Hadamard is NOT invertible over GF(2). Invertible separate-side basis changes preserve rank over their own fields.

Additional tested finite controls: equality, cycle Horn 2-CNF, singleton indicator (rank 1 on every cut). Easy affine/Gaussian, bounded-treewidth, autarky, product, padding, XOR/isolation, auxiliary-variable and compact-circuit controls remain legitimate. A unique satisfying assignment gives a rank-one full assignment tensor; Valiant-Vazirani randomness/promises are not silently made deterministic.

## 4. Exact computational evidence

Executed hosted V8/JavaScript revision multicut-frontier-052.v1, no seed. Enumerated ALL 720 orders and ALL 62 nonempty proper bipartitions of six variables for each of five functions: DISJ3, IP3, EQ3, HORN_C6 and SINGLETON6, totaling 223,200 matrix comparisons. Independently constructed all prefix residual truth tables, exact GF(2) BigInt matrix ranks, switch products, and DISJ's independent tensor-rank formula. **267,852 assertions, zero failures.** The switch bound is tight in 3,168 DISJ cases and 2,016 IP cases; the FALSE global single-frontier claim fails for 4,608 DISJ and 4,608 equality cases.

Concrete witnesses: DISJ3 grouped rank 8; grouped frontier sizes [1,2,4,8,5,3,2], interleaved [1,2,2,3,2,3,2] with peak 3. IP3 grouped rank 3 in GF(2), rank 7 modulo the odd prime 65521; interleaved frontier [1,2,2,4,2,4,2]. JS modular products are below 2^53. A separate container Python/SymPy exact rational audit found DISJ ranks [2,4,8,16,32] and IP ranks [1,3,7,15,31] for k=1..5. This finite evidence is COMPUTATIONAL; the proof above supplies the general quantifiers.

**Source revision and blob:** experiments/tmr/tmr4_multicut_frontier052.js, 82d5fc5feafb7ffd6dcede2272d1b21e6017e5b5.  
**Raw immutable result:** results/raw/tmr/2026-11-15_1235_TMR4_MULTICUT_FRONTIER052_V8_RAW.json, 94b7dbb183a69952e083f9f43e34091947f58498.  
Standalone OS Node, full repository preflight, project test suite and LaTeX builds were not run; hosted V8 executed the exact published source before commit.

## 5. Same-realization resource ledger and Track C connection

| Object | What is actually charged | Status |
| --- | --- | --- |
| Shared pi-ordered BDD | V distinct internal nodes once, despite fan-out; F_i actual reached states and two terminals; <=n Boolean tests per input | Restricted representation theorem only |
| Real tape-based evaluation | Input read/access, address arithmetic, graph traversal, tape movement, storage and output must be charged to ONE machine | General TM translation OPEN |
| Order/basis/partition discovery | Every order tried, failed strategies, switching, cofactor generation, local basis and representation storage must be paid | No free adaptive search |
| Circuit-to-CNF, fixed live DAG | n input variables plus l distinct LIVE fan-in-2 gates => V_CNF=n+l, m_CNF<=3l+n+1, O((n+l)log(n+l)) encoded bits (TMR-1/050, TMR-5/047) | Functional, parsimonious gate compiler, sharing preserved |
| Anthropic October 2026 source formula | For 3-CNF, E=min(3m/sqrt(log_2 m),9V log_2 log_2 V/sqrt(log_2 V)), constant factor C source-defined; no polynomial-space bound | CONDITIONAL on cited pinned proof, not reproduced here |
| Original n versus live l | If l=Theta(n^2) and m=Theta(l), this compiler's displayed bound does NOT certify exponent o(n), even though it is o(V); l=o(n sqrt(log n)) gives source-envelope o(n) under fixed polynomial raw circuit size (TMR-5/047) | An UPPER-bound limitation, never a runtime lower bound |
| Same-run DTISP | No uniform machine both inside strict time and space FLMV forbidden rectangle | OPEN |
| Deterministic configurations | T<=2^{O(s+log N)}, or 2^{O(s)} if s>=log N, for a halting total deterministic read-only-input machine | Upper bound only |

The source definition was read at https://github.com/anthropics/formal-math/blob/main/eth/MainResults.lean ; TMR-5 pins revision 16a5ce41304fcdaea4e0be7c132e1c361dc26da5. The Lean theorem proof, paper-to-statement correspondence and full counting runtime were NOT independently rebuilt. Williams algorithm-to-lower-bound results concern their stated NEXP and related target classes, not an automatic NP separation. No claim from rank forces arbitrary circuit size.

## 6. Mandatory four-gate table

| Gate | Verdict and reason |
| --- | --- |
| DISJ | **PASS restricted** for switch product. **FAIL** for unrestricted/static-rank or arbitrary-partition single-frontier transfer, since DISJ3 grouped rank 8 but interleaved width 3 and linear-size circuit. |
| Relativization | **PASS RESTRICTED** finite algebraic identity. **OPEN** load-bearing unrestricted step: no nonrelativizing construction; Baker-Gill-Solovay prevents a fully relativizing separation. Future universal invariant requires algebrization and Natural Proofs audit. |
| Simultaneous DTISP | **NOT APPLICABLE WITH REASON** to graph-size rank. **OPEN** to any FLMV/machine lower bound, because no one same realization satisfies both strict time and space bounds with all overheads. Networks require sequential total work and aggregate space. |
| Configuration counting | **PASS as upper-bound guard ONLY** for fixed deterministic total read-only-input machine. Does not infer a necessary-work lower bound; randomized/quantum models are separate. |

## 7. Corpus reconciliation and next lemma

Read first directive research/coordination/2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md SHA 7b8804dc7587abc5134055b5b0d16a143055ca5a. Root proof1.txt SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 was read; proof2.txt SHA 930c5eeddafce656717f28055a7a9a755f44737c and main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 returned EMPTY bodies due size, so their complete current content was NOT recovered. AGENTS.md, CODEX.md, repository pnp-research skill, all current TMR handoffs, issue #3, original TMR-1/051, TMR-2/051, TMR-4/051, TMR-5/047 reports, Bryant 1986 and Nisan 1991 original research entry points, and pinned Anthropic Lean statement were consulted. No duplicate in repo search; the previous TMR-4/051 theorem is precisely the b=1 prefix-cut case. Historical /341 FAIL full UNSAT authority and /386 RESTRICTED remain unchanged.

No verified unrestricted proof chain changed. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** No agent identities, schedules, tasks or ownership altered.

**ONE NEXT LEMMA:** For adaptive read-once branching programs whose variable-order decisions depend on earlier input values, either prove a path-respecting switch/interface factorization with genuine charges for state-dependent ordering, or produce the smallest shared adaptive counterexample. Do not apply the present oblivious-order theorem without those new hypotheses. General SAT-machine and circuit transfer OPEN; P versus NP OPEN.

**References:** [1] Bryant, IEEE Trans. Comput. 1986, https://doi.org/10.1109/TC.1986.1676819 . [2] Nisan, STOC 1991, https://doi.org/10.1145/103418.103462 . [3] Baker, Gill and Solovay, 1975, https://doi.org/10.1137/0204037 . [4] Anthropic pinned MainResults.lean, linked above. [5] Project TMR-2/051, TMR-4/051, TMR-5/047 and TMR-1/051 verified reports.

END_OF_VERIFIED_REPORT::TMR-4::052
