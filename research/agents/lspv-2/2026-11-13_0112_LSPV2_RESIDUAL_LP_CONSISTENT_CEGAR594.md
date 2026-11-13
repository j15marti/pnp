% LSPV-2 REPORT::594::2026-11-13_0112_PST
# LSPV-2/594: Reoptimized residual-cover LP as a transition-consistent paid-once potential

**2026-11-13 01:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and four falsifiers

The candidate advances LSPV-2/592 (one terminal LP lower envelope) and /593 (a fixed feasible dual's step consistency). Recompute the **optimal residual fractional cover** at each globally paid-owner history D. F1: a newly acquired owner makes the lower bound fall by more than its marginal once-paid price. F2: reoptimization is weaker than a previously feasible fixed dual. F3: a genuine free shortcut is omitted, leaving an invalid positive lower bound or invalid CEGAR cut. F4: sharing across AND goals is charged twice or a valid integer proof choice is excluded.

## Theorem 594.1, PROVED/RESTRICTED

Fix a **complete certified necessary-obligation cover system**, with finite obligations U and paid identities I. Each owner i has a fixed weight w_i >= 0 and certified coverage C_i. Define Cov(D) as the union of coverage of already-paid owners, and R_D = U minus Cov(D). Assume every obligation can be covered, all needed obligations and possible covering actions have been authenticated, existing coverage is monotone, and a paid identity is never charged twice.

Define h(D) as the optimum of the residual fractional set-cover LP:

$$
h(D)=\min\left\{\sum_{i\notin D} w_i x_i:
x_i\ge 0,\quad
\sum_{i\notin D:\ u\in C_i}x_i\ge1\ (u\in R_D)\right\}.
$$

For every acquisition A, with D' = D union A,

$$
\boxed{0\le h(D)\le\sum_{i\in A\setminus D}w_i+h(D').}
$$

Further, for any globally feasible fixed cover dual y from /593,

$$
\sum_{u\in R_D}y_u\le h(D)\le W_{\mathrm{integer}}(D).
$$

**Proof.** Take an optimum fractional cover x' for the residual obligations after D'. Set x_i = 1 for each newly paid i in A minus D, and retain x' on the other unpaid owners. This covers every obligation residual to D, because any obligation newly covered by D' lies in at least one newly paid owner's C_i. This constructed feasible solution costs no more than the marginal acquired cost plus h(D'). The other inequalities follow from LP weak duality and restriction of a previously feasible dual to still-uncovered obligations. h=0 at every covered terminal. Telescoping along any legal acquisition history proves h(empty) <= the exact globally paid owner cost. This proof does not assume adjacent residual LP dual optima coincide.

**Limit:** These hypotheses are not authenticated for the complete historical R_mix341 grammar. In particular, an unmodeled LOCAL-CONVERT, GF(2), free branch-discharge or other shortcut can make coverage incomplete. Applying the theorem to that calculus before source/rule closure would be UNSOUND.

## Concrete CEGAR and shortcut controls

For three obligations, let the three unit-cost owners cover {0,1}, {1,2}, and {0,2}. Fractional optimum is 1.5 at x=(1/2,1/2,1/2), while the exact integer optimum is 2. The instance-specific cut x0+x1+x2 >= 2 rejects the spurious fractional candidate and preserves all four feasible integer combinations. After paying owner 0, residual reoptimization yields h({0})=1 versus the old fixed-dual value 0.5, demonstrating strict state-dependent improvement. Add a hypothetical, truly admissible owner of cost 0 covering all three obligations: the correct h(empty) becomes zero and the old cut is no longer valid. Thus cuts must be revalidated whenever an originally omitted rule is admitted.

A separate sharing control covers four AND goals via one globally paid owner at cost 1; private owners cost 4. The correct once-paid value remains 1.

## Executed source and finite tests

Self-contained local Node.js implementation enumerated residual dual basic feasible vertices, checked independent integer cover minima, and tested all paid masks and all acquisition masks on 56 seeded cases (seed 0x5945a7): **768 paid states, 12,176 acquisition transitions, 18,689 assertions PASS**. It separately tested the three-cycle CEGAR cut, zero-cost-shortcut invalidation and shared-owner reuse.

The exact **unchanged original /386 checker** (Git blob `338305c0ce101704205e57543756b8127074a986`) was executed in fresh Node OS processes: authentic W29, W32-two-facet, W32-130-facet packets 3 ACCEPT; actual corrupted signed terminal pivots 3 REJECT. The three positives executed 15,838 original-checker assertion groups, including 33 original internal corruption controls. This checker dispatches SOURCE/DEF/RES, not a unified R_mix341. The separate historical /341 checker (blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`) dispatches only AND3/XOR.

Raw local results SHA-256: `ced12fb26d9a79cb918b7ce66ff1d699ec04cebf3b3b5dd090bcc219a1d08590`. Executed local code SHA-256: `2d455d2aec451bca3f34a84b0426a7ab7281ddc84340726fb25e151bb5d739b1`. Separately published compact repository ledger includes all key counts and packet hashes. Reproduction evidence also delivered as an archive in the run response.

## Corpus, provenance, and scope

Read proof1.txt blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, proof2.txt via GitHub REST contents (fetch_file truncation; metadata SHA `f678f707880da4dfc97dabf778430c6dc816cb1f`), issue #3, AGENTS.md, CODEX.md, repository skill, latest five-role /593 handoff, original /341 source and verifier, /386 original checker, material LSPV-2 /539-549 and later /547, /583-593, LSPV-1/589 and /600, LSPV-3/567, LSPV-5/467. Reviewed external `konard/p-vs-np`, `blkph0x/p-vs-np-proof-research`, `meelgroup/frat-xor`, and `tanyongkiam/cake_lpr`. The last two specify DIFFERENT proof systems, not historical R_mix341.

Primary sources: Cousot and Cousot, POPL 1977 (DOI 10.1145/512950.512973); Clarke et al., CAV 2000 (DOI 10.1007/10722167_15); Keller et al., IJCAI 2016 (https://ijcai.org/proceedings/2016/448); Cook and Reckhow, JSL 1979 (DOI 10.2307/2273702). LP duality and state-dependent admissible cost partitioning are standard; the claimed contribution is only the exact model-specific residual consistency transformer and shortcut-sensitive CEGAR control, not a new universal complexity theorem.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, full P2-C3, P2-B1, separate P2-B2/B3 and P versus NP remain OPEN. Preserve all five original roles, titles, schedules, timezone, ownership regions, weights and the historical TWO Route A / THREE Route B labels. No automation was changed.

**Next decisive evidence:** an authoritative unified source-bound checker accepting RES-to-AND3 or paid DEF-to-LOCAL-CONVERT with a rejected corrupted signed-port control.

% END_OF_VERIFIED_REPORT::LSPV-2::594
