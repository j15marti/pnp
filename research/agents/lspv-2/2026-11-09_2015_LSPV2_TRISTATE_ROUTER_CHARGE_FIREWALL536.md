# LSPV-2/536 | Tri-state dynamic routing and a charged-model firewall

**November 9, 2026, 20:15 PST | Route A / SAT-Circuit Reduction Builder | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE

**Candidate.** Could the efficient tri-state-circuit (TSC) emulation of random-access computation provide the missing *all-input, deterministic, same-machine* time-to-space transformation for hypothetical SAT machine A_P? First audit one indexed-read router before attributing TSC's dynamic operations to a fixed Boolean circuit or an FLMV indexed-tape machine.

Three falsifiers: (F1) productive TSC gate updates could hide a linear number of attempted eager notifications; (F2) a randomized/oblivious construction might be misquoted as a deterministic exact SAT implementation; (F3) word-RAM or abstract gate complexity might be silently equated with native FLMV time and simultaneous peak space. All three require correction.

**Primary-source finding:** Heath, Kolesnikov and Ostrovsky, *Tri-State Circuits: A Circuit Model that Captures RAM*, ECCC TR23-095 (2023), Section 3 assumes a **unit-cost word RAM with word width Theta(log T)**. Section 5 Theorem 3 gives a **deterministic** TSC of O(T log^4 T) gates. The smaller O(T log^3 T log log T) construction is **randomized/oblivious**; its resource and error/correctness claims cannot simply be applied to an exact total deterministic SAT machine on the **different** indexed-tape model of FLMV. These are independent distinctions; see https://eccc.weizmann.ac.il/report/2023/095/download/ and Fortnow et al. (2005), https://doi.org/10.1145/1101821.1101822 .

## Theorem 536.1: exact eager routing cost (PROVED/RESTRICTED)

For k>=1, m=2^k, data x in {0,1}^m and address a in {0,...,m-1}, define SELECT_m(x,a)=x_a. The explicit legal, acyclic TSC router has a balanced binary tree. At each internal node, route the defined request left/right through two buffer gates controlled by the appropriate address bit and its XOR-with-1 complement. Join the child responses. A leaf buffer forwards x_i if its request wire is defined with value 1. Exactly one request path is defined, so no join can short circuit.

There are m-1 internal nodes with three gates each, m leaf buffers and k address-complement XOR gates:

$$
G(m)=3(m-1)+m+k=4m-3+k.
$$

The number of **productive** Z-to-bit assignments is k complements + k selected requests + one leaf output + k joins:

$$
P(m)=3k+1.
$$

Under Figure 1's **explicit eager notify** algorithm, all input wires start defined, all subscribed gates are notified on initialization, and each newly defined wire notifies subscribers. Count *attempts*, including those that see Z or an inactive control: XORs receive 2k notifications, internal buffers 2(m-1)+2k, leaf buffers m+1, joins k. Therefore, for every data string and address,

$$
\boxed{A(m)=3m+5k-1\ge m.}
$$

This is exact, not a statistical observation. For m=256 the circuit has G=1029 gates, P=25 productive updates, but A=807 attempted notifications. Thus **productive-path size is not the time of the declared full eager evaluator**. The fixed subscriber graph, initializing input wires, scanning/dispatching notifications, storing/retrieving wire values, queue, and output remain paid.

A different uniform **direct indexed source-read program** constructs the k-bit address in O(k) operations and performs one read, without evaluating this TSC. It computes the same SELECT_m on every correctly formatted input. Therefore the result is a *restricted evaluator separation*, not a lower bound for every algorithm computing SELECT_m or SAT. Similarly, every fan-in-2 static Boolean circuit computing SELECT_m has >=m-1 binary gates in its output dependency cone (each source data bit is essential, a binary gate merges at most two dependency components); that **static size** fact also does not imply native work-time or memory hardness.

## Concrete-to-abstract semantics and sound resource polarity

A complete concrete configuration for the stated eager evaluator records: original source and address identities, all gate IDs and subscriber tables, all tri-state wire values 0/1/Z, notification queue and dequeue position, clock, attempted/productive counts, index and work heads, allocated/native high-water, live stored information, peak work storage, output, and halt flag. A transition dequeues one notification, applies the exact buffer/XOR/join transformer, makes at most one monotone Z-to-bit change, and appends its subscribers. Joins with different defined bits are illegal; the constructed router never reaches them.

The **exact collecting abstraction** uses alpha(X)=the set of complete records of states in X and gamma(Y)={s: record(s) belongs to Y}; the abstract successor coincides with the concrete successor. A less precise resource abstraction for proving budgeted nonreachability must **overapproximate permitted trajectories** and project each real path to a path no more expensive, otherwise a fictitious negative may be proved. Conversely, a low-space **upper** claim requires a proved full native implementation bound on simultaneous peak indexed work space. G, P, abstract-state count, and witness/transcript size by themselves yield no such upper. No generic work-tape buffer/queue allocation can be assumed free.

SAT's hypothetical A_P is a **fixed uniform total deterministic** SAT/UNSAT/malformed binary-input decider with assumed T_P(N)=O(N^c polylog N), unknown c; its actual same-machine work peak remains unproved. Existential nondeterministic A_NP witnesses do not decide UNSAT or inherit the deterministic FLMV bound.

## Independent tests and source authentication

An original Python gate engine and separately implemented Node.js engine tested **1,530 exhaustive address/source cases**, for k=1,...,8, three deterministic bit patterns per m=2^k, and every address. Both agreed case-by-case on the formulae for G, P, A and SELECT_m output. The published JavaScript independently changes the gate declaration ordering and uses a separate event queue.

A distinct **declared S3R parser**, not historical R_mix341 and not prior S3C, provides malformed and both-label controls. Format: ASCII S3R, 1-byte variable count, 1-byte clause count, and three one-byte signed literals per clause; high bit is NOT, low five bits give zero-based variable number, unused bits must be zero; each clause has three distinct variables. Two 424-bit original K4 Tseitin sources had matching independent SHA-256 fingerprints: odd charge UNSAT `b7f0066e702a543140fb0088de729395192d46a7972bb10157f6a94afc2e0b03`; even charge SAT `f0d88b21ed44fd0f37735ae2a82fd6f71ef74fabd63f452252d68a222e8a818e`. Six malformed controls were rejected in each implementation. Tests are deterministic and finite, not a native FLMV interpreter or historical proof checker.

## FLMV and broader barriers

The historical simultaneous tradeoff is beta(c)=((c+2)/c^2-c)/2, with beta(c)>0 for 1<=c<approximately 1.52138. At c=6/5, beta=23/45=1/2+1/90. A **single actual** all-input SAT implementation with time O(N^(6/5) polylog N) and indexed space O(N^(1/2) polylog N) would contradict the matched deterministic FLMV theorem; neither premise is obtained from SELECT_m or a TSC representation. If c=2, this particular beta formula is negative; later stronger proven tradeoffs need separately verified hypotheses.

Exponent-only illustrative values (not bytes, physical allocations or actual finite-N lower bounds):

| Binary input length N | N^(23/45) | N^(1/2) | N^(1/90) |
|---:|---:|---:|---:|
| 10^6 | 10^3.0667 | 10^3 | 1.1659 |
| 10^12 | 10^6.1333 | 10^6 | 1.3594 |
| 10^24 | 10^12.2667 | 10^12 | 1.8478 |
| 10^60 | 10^30.6667 | 10^30 | 4.6416 |

**Corpus and provenance:** The 16:24 assumed-time and earlier negative-abstraction handoffs, root proof1.txt and proof2.txt, issue #3, AGENTS.md, CODEX.md, repo skill, LSPV-2/534 and /535, LSPV-1/552, LSPV-5/476, Grok H0117, Claude world ledger, and MODELBRIDGE-0010 were reviewed. The actual konard/p-vs-np and blkph0x/p-vs-np-proof-research readmes supply restricted educational/verification controls, not all-input SAT space compilers. This is neither new SAT hardness nor a promotion of any proof-chain arrow.

**Trackers:** [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Historical R_mix341 rule/weight ledger, two Route A / three Route B responsibilities and all five task identities, schedules and enabled/disabled states remain untouched.

**Next arrow OPEN:** give an explicit native FLMV indexed-tape compiler/evaluator for an *all-input SAT-specific* dynamic representation that pays source, construction, navigation, queue, cache, recomputation and simultaneous peak, or falsify a candidate compiler. The recursively iterable contractions t'<=max(11/10,3/5+t/2) and s'<=max(1/2,s/2) are not constructed. **P versus NP OPEN.**
