# LSPV-1/453: Bit pigeonhole, explicit strict-3-CNF ER shortcut and forbidden lower-bound backtranslation

**2026-11-06 10:11 PST | Route B | PROVED/RESTRICTED in separate ER-FACET; COMPUTATIONAL local checks; historical R_mix341 and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

Hypothesis: Braun's certified unrestricted-DAG Res(XOR)-hard bit pigeonhole family can be reduced to unary PHP through polynomial-work **paid conservative AND definitions plus strict RES**, even after source conversion to proper 3-CNF. Hence any polynomial backtranslation of **all** these stronger ER proofs to the original Res(XOR) system is impossible.

Falsifiers: (F1) source-to-strict3 existential projection fails; (F2) a non-complementary pivot, spoofed defining facet or source sign enters the construction; (F3) a purported shared gate has no paid definition owner; (F4) a polynomial lower-bound-preserving backtranslation survives the published exponential Res(XOR) bound. F1-F3 were addressed by symbolic argument and independent finite controls; F4 contradicts Braun's published theorem when composed with the existing ER PHP upper bound.

Primary review: Braun arXiv:2609.23015v2, revised November 3, 2026; Cook-Reckhow (1979) and Cook (1976) Extended Resolution PHP; Buss (1987) Frege PHP; Grosof-Zhang-Heule (2022) DRAT PHP; Pich-Santhanam (2026) proof-to-circuit limits. Read current issue #3, project governing handoff, LSPV-2/341, LSPV-1/452, LSPV-3/455, LSPV-5/REFEREE389, actual Grok and Claude files, AGENTS/CODEX/research skill. Inspected konard/p-vs-np proofs/complexity/README.md (blob 7ee9a11), scripts/proof_status.json (93b77ed); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693e); meelgroup/frat-xor format.md (986a21a); tanyongkiam/cake_lpr README.md (e94f45e), openai/math README.md (cc5b0a0). The external checker formats are not native R_mix341. Google-branded direct search, original Lean replay, full local repository preflight and authoritative R_mix341 checker were not used.

**Duplicate audit:** LSPV-3/455 already has an independently checked complete ell=2 UNSAT FACET-A refutation with 495 paid nodes, and an ell=3 partial proof with 2,979 paid nodes. Those counts and the broad polynomial ER shortcut are not claimed novel. This run adds a self-contained uniform signed 3-CNF compiler and *exact general local-work formula*, a new independent implementation, both-label controls, and the explicit impossible backtranslation corollary.

## Certified hard family and exact source transformation

Set n=2^ell, ell>=2, and m=n+1 pigeons. Braun's bit-PHP uses bit variables x_(i,t), 0<=i<m, 0<=t<ell, with each pair i<j constrained by the Res(XOR) clause

$$
B_{ij}=\bigvee_{t=0}^{\ell-1}(x_{i,t}\oplus x_{j,t}=1).
$$

For ell>=32, Braun's 2026 theorem proves every unrestricted shared-DAG Res(XOR) refutation has more than

$$
\exp\left(\frac{n}{32768\ell^2}\right)
$$

clauses. No arbitrary SAT algorithm or extension-variable lower bound is claimed.

For address h in {0,1}^ell let L_(i,t,h) be x_(i,t) when its address bit is 1 and neg x_(i,t) otherwise. For every i<j and h define the ordinary width-2ell clause

$$
C_{ijh}=\bigvee_t\neg L_{i,t,h}\ \vee\ \bigvee_t\neg L_{j,t,h}.
$$

It forbids exactly the event that both pigeons have address h. Thus the conjunction over all h is *equivalent* to B_(ij). There are A=n*binom(m,2) wide clauses. Replace each k=2ell clause by its private signed strict3 chain (k-2 clauses, k-3 fresh original-coordinate wires). Resolving each chain yields the wide clause with exactly k-3 strict RES inferences; its existential projection is precisely that clause. The resulting source Phi_(n,3) has

$$
S=A(2\ell-2)\quad\text{original strict-three clauses},\qquad
V_{\mathrm{orig}}=m\ell+A(2\ell-3).
$$

Hence Phi is UNSAT for m=n+1 and has SAT controls for m<=n. This translation and recovery are **upper simulation/equisatisfiability only**. Lower-bound preservation would need a polynomial translation of every *target proof back to source Res(XOR)*, not the reverse.

## Exact paid shared-prefix compiler to unary PHP

Use a separate, explicitly specified ER-FACET calculus: strict RES plus a paid globally fresh signed two-input AND gate u=(a AND b), with three typed owner facets (neg u OR a), (neg u OR b), (u OR neg a OR neg b). These facets are not free source axioms, and whether the historical native R_mix341 permits their export is OPEN. Reuse all owner nodes for matching address prefixes. Per pigeon, create gates for 2^d prefixes of length d=2,...,ell. Thus the number of paid conservative gates is

$$
D=m\sum_{d=2}^\ell 2^d=m(2n-4).
$$

The full-address gate p_(i,h) means x_i=h. Strict RES from its definition facets derives (neg p_(i,h) OR L_(i,t,h)), and the reverse (p_(i,h) OR bigvee_t neg L_(i,t,h)). Shannon resolution on the n reverse clauses yields the unary-PHP axiom bigvee_h p_(i,h), in exactly n-1 RES inferences per pigeon. Resolving the recovered wide clause C_(ijh) with the 2ell justified forward clauses yields (neg p_(i,h) OR neg p_(j,h)), in 2ell RES inferences per pair and hole. No split, discharge or weakening rule is added.

For this explicit (not minimum) compiler the exact paid RES count is

$$
R=A(4\ell-3)+m(n-1)+mn\frac{(\ell-2)(\ell+3)}2.
$$

The total **local** paid logical work is D+R; sources and all three gate facets remain explicitly represented and charged in bit/verification costs. Cook-Reckhow's known polynomial Extended Resolution proof of ordinary PHP can then be appended, yielding a polynomial-size ER proof of the complete strict3 Phi family. This run did not produce that final appended refutation or run an authoritative historical mixed checker.

## No-polynomial-backtranslation corollary

**PROVED/RESTRICTED corollary, conditional only on the cited published source theorem and known ER PHP upper bound.** There does not exist any polynomial p and family-uniform transformation taking **every** ER-FACET refutation pi of Phi_(n,3) to a Res(XOR) refutation of Braun's original B_n with length at most p(n+|pi|) for every n=2^ell, ell>=32.

Proof: above construction plus polynomial-size unary-PHP ER refutations yields an ER-FACET pi_n with |pi_n|=n^O(1), including complete evidence bits. Such a translator would produce a Res(XOR) proof of polynomial size n^O(1), eventually smaller than exp(n/(32768 ell^2)); contradiction. This rules out the precise ER-to-Res(XOR) transfer, **not** any established R_mix341 proof. ER may be strictly stronger.

## Finite replay and resource limits

Independent standard-library Python producer and separate Node.js checker reconstruct signed source clauses, paid globally fresh AND owners, all facets, dependency DAG and oriented RES pivots. Five malformed DIMACS strings and six mutated proof/source/facet records were rejected.

| Input | Original strict3 clauses | Source vars | Paid DEF | Paid RES | Local paid total | JS assertion groups |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ell=2, 5 pigeons/4 holes UNSAT | 80 | 50 | 20 | 215 | 235 | 3,979 |
| ell=2, 4 pigeons/4 holes SAT | 48 | 32 | 16 | 132 | 148 | 2,220 |
| ell=3, 9 pigeons/8 holes UNSAT | 1,152 | 891 | 108 | 2,871 | 2,979 | 35,163 |

For 4 pigeons/4 holes the verifier constructed a satisfying assignment to every signed original strict3 clause and counted exactly 24 distinct bit-address models. For 5 pigeons/4 holes there were zero models among all 1,024 bit-address assignments. The ell=3 UNSAT assertion uses pigeonhole counting, not enumeration over 2^27 assignments. These are **local unary-PHP reduction certificates**, not completed refutations or global proof minima. The ell=3 paid totals independently reproduce prior LSPV-3/455.

Raw original source is 868 bytes at ell=2 UNSAT and 15,423 bytes at ell=3 UNSAT; raw full local trace JSON 24,386/322,748 bytes. Final locally executed producer wall 0.79 seconds / 99,484 KiB peak RSS; independent verifier 0.06 seconds / 36,704 KiB. These physical figures do not include literature, repository I/O, final Cook proof, source searches, restarts and other phases. The full charge ledger is in the downloadable local archive; no FLMV machine contraction or all-rule hardness follows.

**Family ledger:** Braun bit-PHP lower bound is unrestricted-DAG Res(XOR) only; Cook ER supplies a polynomial shortcut in a stronger calculus. Odd-expander Tseitin is ordinary Resolution hard but has the declared semantic R_mix341 4h-1 mixed GF(2) shortcut. Unary PHP has Haken Resolution hardness but Cook ER/Buss Frege polynomial proofs. No certified source hard family yet supplies an all-legal-rules superpolynomial R_mix341 bound.

**OPEN:** Historical DEF-facet/LOCAL/owner accepted-byte grammar; all-mixed branching/shared Wbar superpolynomial lower bound; noncircular fixed-system B3 SAT in P => Wbar_R poly; B1/B2 and P versus NP. Root main.tex returned SHA f41d1cd but 0 readable bytes, and was left unchanged. Exactly five tasks, 2 Route A and 3 Route B, identities, schedules and native weights retained.

## References

1. Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2, revised November 3, 2026: https://arxiv.org/abs/2609.23015
2. Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, J. Symb. Logic 44 (1979), 36-50.
3. Buss, *Polynomial Size Proofs of the Propositional Pigeonhole Principle*, J. Symb. Logic 52 (1987), 916-927.
4. Grosof, Zhang, Heule, *Towards the shortest DRAT proof of the Pigeonhole Principle*, arXiv:2207.11284.
5. Cook, *A short proof of the pigeon hole principle using extended resolution*, SIGACT News 8(4) (1976), 28-32.
