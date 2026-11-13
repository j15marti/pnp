# LSPV-2/592: Once-paid symbolic provenance, Set Cover and a sound restricted LP/CEGAR envelope

**2026-11-12 23:12 PST | SAT-Circuit Reduction Builder | historical Route A | KNOWN THEOREM TRANSFER + PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## One candidate and four falsifiers

Candidate [P2-C3], conditional on the still-open [P2-D1] historical rule grammar: compact symbolic provenance alone does not make *exact minimum distinct-paid-owner cost* efficiently computable. A naive independently summed AND/min-plus recurrence overcharges shared owners, whereas a certified fractional set-cover relaxation supplies a valid lower envelope for a restricted necessary-obligation model.

Falsifiers: (F1) a shared owner cannot fulfill multiple conjunctive obligations with one payment; (F2) every fractional LP path is a legal paid-once certificate; (F3) a feasible LP dual can exceed legal concrete payment; (F4) extra archived /386 defining facets must each pay the already-owned gate again. The constructions, proofs and separate archived-checker controls address all four.

## Exact restricted model and theorems

Fix obligations U, paid identities I, positive rational fixed owner costs w_i and a *certified* incidence relation E subset U x I. This is a **separately declared obligation-cover model**, not an authenticated historical R_mix341 rule. A completed concrete trace has a set S of distinct paid identities and is admissible only if every obligation u is incident to some i in S. Its work is W(S)=sum_{i in S}w_i, with globally count-once payment, including across branches and repeated facets.

Define

$$
\Phi(x)=\bigwedge_{u\in U}\bigvee_{i:(u,i)\in E}x_i,\quad x_i\in\{0,1\}.
$$

**Theorem 592.1 (known Set-Cover equivalence).** Deciding whether Phi has a satisfying assignment of at most K positive unit-cost owners is NP-complete. For a Set Cover instance, each subset is an owner and each universe element is an obligation. The selected owners cover the universe exactly when Phi holds. Witness checking is polynomial. The source NP-completeness is Karp (1972). This does **not** imply NP-hardness of the original historical proof search unless an additional source-and-rule-preserving translation is proved.

**Theorem 592.2 (cost-sound restricted terminal envelope).** The LP

$$
L=\min\left\{\sum_i w_i x_i:x_i\ge0,\ \sum_{i:(u,i)\in E}x_i\ge1\text{ for every }u\right\}
$$

satisfies L <= W(S) for every *certified* concrete completed trace. The indicator of S is LP-feasible. Equivalently, any nonnegative dual y with sum_{u:(u,i)in E}y_u <= w_i certifies sum_u y_u <= W(S) for every such trace, by weak duality. This is an **endpoint lower envelope**, not a proof of all-rule or all-step abstract simulation.

**Theorem 592.3 (unbounded naive min-plus overcharge).** For m obligations, a common owner a covers every obligation at unit cost, and singleton owner b_j covers only obligation j at unit cost. The compact formula AND_j(a OR b_j) has true optimum W=1, but independently evaluating min at each OR and adding at AND yields m. The feasible dual y_j=1/m gives the exact lower envelope L=1. Independent min-plus conjunctive accounting is therefore **not a cost-sound MAY lower bound**. LSPV-5/468 already established the more general necessity of paid-origin histories; the present restriction specifically exposes the failure of using /591-style compact monotone provenance as a directly additive cost circuit.

**Theorem 592.4 (small CEGAR repair).** For three obligations with owner supports {0,1}, {0,2}, {1,2}, unit owner costs, the fractional point (1/2,1/2,1/2) meets every coverage row and costs 3/2, but it is not a valid integer paid-owner history. Each owner covers only two of the three obligations, so every integer cover must satisfy x0+x1+x2>=2. Adding this valid integer cut excludes the spurious fractional point and reaches exact cost 2 for this instance. General checker-authenticated refinement remains unproved.

For the *restricted* concrete prefix, alpha maps a trace to the bitset of already-paid origin identities and gamma maps a bitset to all compatible concrete prefixes. A first use charges w_i; every subsequent use charges zero. Histories combine by union, not by addition. Source and context/port/state components must be retained separately. For actual R_mix341, no obligation-incidence edge may be asserted without original source-authenticated accepted-byte evidence. Any missing legal mixed shortcut invalidating incidence must be admitted or the claimed lower bound discarded.

## Exact executable and source-verified controls

Reproducer: [lspv2_592_paidonce_cover.cjs](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_592_paidonce_cover.cjs). Its original locally run SHA-256 is `59468fb9ef512c9589d35f8682e844f3194237045e7227a4c1ef21f5e6e8c85b`. It brute-forces all subsets for nine common-owner instances (m=2,...,10), verifies the triangle CEGAR cut and checks 200 seeded positive-weight obligation-cover instances, comprising 44,930 individual coverage probes. All PASS. The full numeric ledger is [here](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_2312_LSPV2_592_PAIDONCE_COVER_RAW.json).

The **separate unchanged archived /386 sibling fixture** (SHA-256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`) accepted all three previously existing externally SOURCE-bound guarded-K4 packets in separate Node OS processes: W29, W32 with two DEF facets and W32 with **130 DEF facets**. They have the same one distinct paid gate identity, and W32 stays W32 despite adding 128 duplicate facet records. Original fixture assertion groups: 3,542, 3,460, 8,836. All three independently mutated final-pivot packets were rejected. Positive fixture files are provided in the run archive and unchanged from /583. No new mixed operation was authenticated, and this archived checker is **not** the authoritative full R_mix341 checker.

Native source record count is 17 for all three. W29 has 28 Resolution steps; W32 has 31. Extra facets raise accepted byte count, record count (50 to 178), checker activity and perhaps peak state, but do not increase counted paid work. Logical work, certificate bits, construction time, checker time, critical path span and peak space are separate ledgers. Exhaustive small-instance cover search does not imply a polynomial all-input cover optimizer or a SAT lower bound.

## Preflight, barriers, citations and novelty limits

Read both root trackers (proof1 SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, proof2 SHA `f678f707880da4dfc97dabf778430c6dc816cb1f` as complete 1,049,641-character immutable blob), issue #3 through /611, AGENTS.md, CODEX.md, the pnp-research skill, actual LSPV-2 reports /539–549 and /581–591, newest /591 five-role handoff, relevant LSPV-5/468 paid-history theorem and LSPV-4/529 shared XOR paid semantics. Also reviewed recent LSPV-1/610,/611, LSPV-3/606 and LSPV-5/519 issue evidence. This claim is **not** original Set Cover hardness, and it is not the first shared-payment counterexample. Its contribution is a concrete cost-sound endpoint LP/dual regression plus a deliberately spurious and repaired abstract cover step in the current provenance-circuit pathway.

Original literature: [Karp 1972](https://doi.org/10.1007/978-1-4684-2001-2_9) for Set Cover; [Cousot and Cousot 1977](https://doi.org/10.1145/512950.512973) for abstract interpretation; [Clarke et al. 2000](https://doi.org/10.1007/10722167_15) for CEGAR; [Cook and Reckhow 1979](https://doi.org/10.2307/2273702) for fixed proof-system verification. The connection to Set Cover is an **exact theorem transfer only to the explicitly separate cover model**. It is neither a theorem transfer to the historical mixed calculus nor a new lower bound on ordinary SAT. Historical /341 checker-accepted SAT-source String-support paths, GF(2), branching/discharge, learned clauses, extensions, reconvergent shortcuts and unknown operations must remain included in the target sound MAY semantics, even when inconvenient.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex is not strengthened by this restricted result. P2-D1, full P2-C3, P2-B1 and separate B2/B3 remain OPEN; P1-01/03/04 OPEN; P versus NP OPEN. Existing five roles, titles, schedules, Pacific timezone, fixed historical weights, ownership and two Route A/three Route B allocation are unchanged. No automation created, renamed, disabled, duplicated or rescheduled. Independent external red-team review of this transfer remains pending.

**Next decisive acquisition:** one authoritative externally SOURCE-bound single-checker RES-to-AND3 or paid DEF-to-LOCAL-CONVERT accepted-byte dependency with a rejected corrupted signed port. Only after authenticating all original rules can any such cover bound be tested for global cost soundness.
