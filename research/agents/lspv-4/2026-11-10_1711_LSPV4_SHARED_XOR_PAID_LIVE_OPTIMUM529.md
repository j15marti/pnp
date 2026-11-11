# LSPV-4/529: Exact peak retention for a shared GF(2) proof DAG

**2026-11-10 17:11 PST | Time-Space Resource Auditor | historical Route A retained | PROVED/EXACT in explicitly restricted scheduling model + COMPUTATIONAL | P versus NP OPEN**

**New material evidence [P2-L4-529].** Refines [P2-L4-523], [P2-L4-525], [P2-L4-528] and [P2-L5-464]. Unclosed primary path: [P2-D1] -> [P2-C3] -> [P2-B1], separate [P2-B2]/B3.

## IDEA -> falsifiers -> SEARCH -> ITERATE

**Hypothesis:** A fixed original-source K4 odd-Tseitin SOURCE/AND3/XOR refutation with a reused paid affine anchor requires exactly four simultaneous *paid semantic result slots* under non-overwriting, no-recomputation execution, one more than the corresponding unshared proof. Yet this optimum is independent of the number of shared paid XOR detours.

**Falsifiers:** (F1) a legal k>=1 schedule achieves three paid live slots; (F2) growing k forces the minimum above four; (F3) the shared anchor must be paid again at each reference; (F4) reordered authentic-source proof fails the separately typed reference checker or a dangling premise is accepted. F1-F3 are disproved under the stated restricted model by symbolic proof and exact state-space search. F4 is false in the five tested cases; full historical rule authentication remains unavailable.

Read full root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 chars) and proof2.txt (startup blob 282c42f891b8528e2181a1f50de795e1d5b10e12, 948,636 chars), issue #3 through /528, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, /528 handoff, /341 historical rule report, original /341 producer and separate /539 source-bound checker, LSPV-4/523-528, LSPV-3/539/549/554-556, and LSPV-5/464. Peers' Grok/Claude references were checked through /528; this run does not claim independent inspection of additional original Grok/Claude documents.

**External exact files checked:** konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (scoped formal status); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped methods); meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2 (different external XOR proof grammar); tanyongkiam/cake_lpr README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c (different certified checker); MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (known Tseitin CNF generator). No external repository authenticates missing original mixed byte rules.

**Primary literature:** Nordstrom and Hastad, Towards an Optimal Separation of Space and Length in Resolution, Theory of Computing 9 (2013), DOI 10.4086/toc.2013.v009a014; Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979), DOI 10.2307/2273702; Cousot and Cousot, Abstract Interpretation, POPL 1977, DOI 10.1145/512950.512973. These provide context, not proof of this particular fixed DAG optimum.

## Authenticated finite source and exact DAG

The original signed proper K4 odd-Tseitin CNF has 6 variables, 16 ternary clauses and 163 ASCII DIMACS bytes. Independent complete enumeration finds 0/64 satisfying assignments, while even charges give 8/64 satisfying assignments. The source is not an asymptotically hard-family certificate.

The original /341 producer, blob 4081022e8a3841d79f751a3d3a7a10decbb026da, has 12 binary AND3 nodes d0..d11 (three per vertex), with vertex outputs f0=d2, f1=d5, f2=d8, f3=d11. The three binary XOR nodes are a=d12=XOR(f0,f1), b=d13=XOR(a,f2), z0=d14=XOR(b,f3)=0=1. For each i>=1 append fresh nodes u_i=d_(13+2i)=XOR(z_(i-1),a) and z_i=d_(14+2i)=XOR(u_i,a). These cancel a and preserve the contradiction, while forcing the same original paid anchor to remain available. Every node is separately paid once, and all dependencies are acyclic.

For k appended XOR pairs:

$$
W(k)=15+2k,\qquad R(k)=30+4k,\qquad D(k)=6+2k.
$$

W is distinct unit-paid creation work, R is explicit premise reference occurrences and D is dependency span (unit per paid step). R is NOT an extra historically authenticated tariff. The 15-node proof without detours remains a cheaper legal candidate, so no lower bound on the minimum W_R(F) follows.

## THEOREM 529.1: exact paid-live peak

**Model:** Original SOURCE nodes are on a read-only INPUT channel, and only *paid derived result values* count toward this narrowly defined slot measure. A paid inference writes a new value in a fresh paid-result slot while its paid parents remain live; finished parents may be released after their last use without an inference charge. Computations are topologically ordered; no recomputation or destructive in-place overwrite is permitted. This defines a hypothetical resource scheduler, NOT an additional historic proof rule or a bound on all physical WORK bytes.

For the exact fixed paid-occurrence DAG,

$$
\boxed{P_{\min}(k)=3\quad(k=0),\qquad P_{\min}(k)=4\quad(k\ge1).}
$$

**Proof, k=0:** Forming a from the two independent 3-step AND3 subchains f0 and f1 requires three live result slots: retain the first subchain's output while the other subchain needs two slots during a fresh write, or retain both outputs before writing a. The topological order 0,1,2,3,4,5,12,6,7,8,13,9,10,11,14 uses at most three slots, proving optimality.

**Proof, k>=1:** Since a is used after z0, it cannot be released when computing b and z0. If either f2 or f3 is completed before a, that independently retained value is still live when the fresh a computation needs the three slots from the k=0 subargument, giving at least four. Otherwise both are computed after a. To finish z0, the first completed of f2/f3 must remain as itself or its descendant b while the other independent three-step chain is computed. The pinned a plus this retained value plus two transient fresh-result slots imply a peak of at least four. Conversely the explicit order 0,1,2,3,4,5,12,6,7,8,9,10,11,13,14 followed by 15,16,...,14+2k never exceeds four. After z0, retaining a and current z costs two slots, computing next u and z costs at most one fresh extra slot at a time. Thus exactly four for every k>=1. QED.

This argument is restricted to the fixed dependency DAG and its specified fresh-write semantics. Deletion here means *forgetting a physical cached value*, not a zero-cost historical DELETE proof rule. In-place updates, alternative proof DAGs, different context rules, and recomputation may have other Pareto optima.

## Executable checks and resource ledger

The published exact order-ideal dynamic program enumerates all legally produced-node subsets and computes the minimum of maximum live-before-reclamation paid slots. Its recurrence considers every available next inference and charges one extra slot before releasing consumed parents. Induction on the number of produced nodes proves exhaustive coverage of this precise scheduling model.

| k | W | Exact peak | Explored produced-set states |
|---:|---:|---:|---:|
| 0 | 15 | 3 | 277 |
| 1 | 17 | 4 | 279 |
| 2 | 19 | 4 | 281 |
| 3 | 21 | 4 | 283 |
| 4 | 23 | 4 | 285 |
| 8 | 31 | 4 | 293 |
| 16 | 47 | 4 | 309 |

Independent Python DP yielded the same optima and state counts for k=0..3. Four adverse structural controls rejected missing and future premises, omitted nodes, and a false three-slot assertion.

Reordering the actual /341 original K4 proof with k=0..4 paid XOR pairs was separately checked in hosted V8 by the **distinct** strict source-bound /539 checker, blob fc91a6f33d0d010d6225365a3d9ce72a090af21f. All five source-authenticated typed packets ACCEPTED with W=15,17,19,21,23 and D=6,8,10,12,14 respectively. SHA-256 in the checker result was replaced by an explicitly disclosed V8 adapter stub; **no cryptographic digest is claimed**. The original fixture checker /341 has a hard-coded 4V-1 guard and is not the full accepted-byte R_mix341 language. No Node OS CLI run or machine RSS high-water measurement was performed.

**Fixed logical charges:** SOURCE 0; every fresh AND3 and XOR 1; historical semantic declaration also states one each for fresh RES, LOCAL-CONVERT and paid DEF. **Unverified historical bytes/cost details:** defining facets, exported/private/fresh wires, true branch/case, weakening, discharge, joins, deletion, and native reference/application charges. The exact source/authentication and all evidence bits, JSON tokens, identifier comparisons, masked integer processing, lookup, reconstruction, output, verifier reads, simultaneous ancestors/children and all-phase physical WORK peak must be added separately. A checker retaining the full JSON packet is NOT a four-slot physical implementation.

**Cost-sound abstraction rule:** Count each distinct paid occurrence exactly once, including shared a; do not sum component lower bounds unless the overlapping node charges are partitioned so their total never exceeds the one concrete payment. Context-compatible shared deductions and cheap GF(2) shortcuts remain legal candidates in a full calculus. The extant 15-node K4 proof prevents treating detour scheduling costs as minimum refutation cost.

**New contribution relative to prior work:** /523 optimized the no-sharing fixture to 3; /525 established shared XOR detours and count-once references; /528 exhibited semantic quotient cycles. This report proves the precise one-slot retention premium for shared a and the constant peak for arbitrarily many detours. It is neither new general pebbling theory nor a universal SAT lower bound.

## Publication and exact remaining gaps

Code: experiments/arc/lspv4_529_shared_xor_peak_exact.cjs (blob 7757f8f63a29e81b0af3ad14e7c3b37d47aef950).
Raw: results/raw/arc/2026-11-10_1711_LSPV4_529_SHARED_XOR_PEBBLE_RAW.json.
Handoff: research/coordination/2026-11-10_1711_LSPV4_SHARED_XOR_PEAK_FIVE_ROLE_HANDOFF529.md.

Root main.tex may be edited only after full-content retrieval and outside-owner byte preservation; the preceding run reported an empty payload despite a returned SHA. No existing schedule, ownership, historical grammar/weight, or 2 Route A/3 Route B allocation was changed.

**Still OPEN:** [P2-D1] complete historical accepted-byte source-bound grammar and semantic soundness; [P2-C3] full rule-by-rule cost-sound goal-preserving abstract simulation; [P2-B1] superpolynomial minimum over every legal historical mixed shared-DAG proof; independent same-calculus B3 [P2-B2]. P versus NP remains OPEN.
