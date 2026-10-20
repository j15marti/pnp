# MCSP-SPARSE-TEMPLATE-KT-FIREWALL1
Date: 2026-10-20 17:00 Asia/Seoul. Route: MCSP/MKTP only. **P vs NP OPEN**.

## Proposals and falsifiers
1. Tag an easy indexed target by one SAT-dependent bit: falsified.
2. Hash-scatter a polylogarithmic number of edits into an easy target: falsified.
3. XOR a sparse exception dictionary into an affine/parity template: falsified.
4. Dense semantic transport with no short ordinary indexed description: OPEN; must prove both promises, totality, encoded length, input reads, replay, and matched costs.

## Exact restricted lemma
Fix an efficient universal indexed-bit machine U. Let B_{M,sigma} be a uniformly indexed template, where |sigma|<=b(M) and any B[i] is produced in poly(b(M),log M) time without source oracle. For any E subseteq [M], |E|<=h(M), define Y[i]=B[i] XOR 1_{i in E}. Then a source-free ordinary program containing M, sigma and the exception list computes every bit. Its length is O(b+(h+1)log M) and its per-index runtime is poly(b+h log M). Therefore KT_U(Y)<=P_U(b+(h+1)log M) for a fixed polynomial P_U.

If b,h=polylog(M), then KT_U(Y)=polylog(M) for EVERY source, independent of the cost of finding E. For each fixed k>=2 and p_k=floor(M^(1/k)), all outputs are MKTP YES for sufficiently large M. Hence a uniform total SAT-to-ordinary-MKTP reduction whose image lies in this sparse-template family cannot preserve the SAT/UNSAT high-KT promise (in either polarity). This is not a general SAT lower bound. Universal-machine constants mean finite crossover points are not established.

## Exact target and experimental falsifier
The source is explicitly serialized proper 3-CNF. A 4-clause unit gadget U(l;a,b) represents each unit. A payload family SAT instance forces z and attaches arbitrarily chosen (z OR a_j OR v_{b_j}) clauses; the UNSAT family forces z and not-z, with the same payload. A candidate uses the easy indexed template parity(i AND sigma) XOR bit_shift(i), and flips h SHA256-derived indices. Hash security is irrelevant. Every output admits ordinary program (M,sigma,shift,E); both source labels yield low KT asymptotically.

Finite standard-library Python checker: 124 labeled formula controls, 1984 target descriptor cases, 2698240 indexed-output consistency checks, 2702404 assertions, **0 failures**. Largest materialized target: 4096 bits. Toy-machine program/time proxies are explicitly NOT actual universal-machine KT.

## Resource ledger
Ordinary MKTP string Y has M bits; a many-one output must actually be encoded (M writes), not replaced by a pointer. A streaming source hash scans all N input bits; exceptions need O(h log M) stored bits. The finite Python checker stores inputs/outputs, so no matched memory claim is made. The existential ordinary KT program hardcodes only sigma and E, not source or hidden oracle; its acquisition may be arbitrarily hard. MMW Theorem 4.2 uses O(Mp) oracle-unit time, O(p) space, and ordinary Sigma_3 SAT queries of O(p) length **after** Y already exists; it does not construct Y.

## Primary literature and status
MMW (STOC 2019), Theorem 4.2: https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf
OPS (Theory of Computing 2021) analyzes Gap-MKtP (not ordinary KT) and Gap-MCSP under nonuniform models: https://theoryofcomputing.net/articles/v017a011/
CHMY (STACS 2021) uses a distinct one-way one-work-tape model: https://doi.org/10.4230/LIPIcs.STACS.2021.23
Ilango (SIAM J Comput 2026) proves random-oracle-relative hardness; fixed hash is only heuristic: https://eccc.weizmann.ac.il/report/2023/165/

**PROVED (restricted):** sparse-template ordinary-KT ceiling. **COMPUTATIONAL:** finite decoder/SAT controls. **FALSIFIED:** sparse semantic tag/hash/affine patch family. **OPEN:** deterministic uniform total SAT-to-MKTP R_k with both promises; ordinary source-free MMW query interface; P vs NP.

**Next falsifier:** For a dense or proof-of-work R_k candidate, attempt to extract a short ordinary index program or sparse exception dictionary; if that fails, demand a concrete target-bit predicate and exact source reads, query length, full output acquisition and same-realization space/time.