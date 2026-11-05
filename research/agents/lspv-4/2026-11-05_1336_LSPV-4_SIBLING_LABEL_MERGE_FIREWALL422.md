# LSPV-4/422: Guarded sibling-label merging is SAT-hard even on SAT parents

**2026-11-05 13:36 PST | Route A Resource Auditor | PROVED/RESTRICTED plus COMPUTATIONAL finite controls. P versus NP OPEN.**

## IDEA before SEARCH: falsifiable target

Hypothesis: a universal shared-branch compiler cannot use exact *SAT-decision-label equivalence* of sibling cofactors as a free or uniformly cheap predicate, even when the common parent is guaranteed SAT. Falsifiers: (1) guard at z=1 may fail; (2) guard at z=0 may not preserve F after existential private variables; (3) eager materialization could secretly cost linear writable space; (4) translating the test encoding to FLMV's exact SAT encoding might not be justified. (1)-(2) fail by the explicit proof; (3) is repaired with an indexed virtual-bit accessor; (4) remains an explicitly bounded encoding-model condition.

## PROVED/RESTRICTED theorem

For a proper original 3-CNF F=AND_i(a_i OR b_i OR c_i), introduce a globally fresh selector z and separate private y_i. Form the ordinary proper width-three CNF

$$
H_F=\bigwedge_{i=1}^{m}[(z\lor a_i\lor y_i)\land(\neg y_i\lor b_i\lor c_i)].
$$

For every assignment x to original variables, direct two-value enumeration of each private y_i gives

$$
\exists y\,H_F(0,x,y)\iff F(x),\qquad \exists y\,H_F(1,x,y)=\mathsf{TRUE}.
$$

Indeed if a_i is false, the first clause requires y_i=1, so the second requires b_i OR c_i. If a_i is true, y_i=0 satisfies both. At z=1 all y_i=0 satisfy H_F regardless of x. Hence H_F itself is always SAT.

Let E(H,z) return whether the two sibling cofactors H|z=0 and H|z=1 have the same **zero-boundary Boolean SAT/UNSAT decision labels**. Then

$$
\boxed{E(H_F,z)=1\iff F\in\mathrm{SAT}.}
$$

Thus even a perfect sibling-label merger promised only *always-SAT* parent formulas is SAT-hard. This is NOT equality of the projected relations on x, a native R_mix341 case-split rule, nor permission to reuse a lemma across incompatible assumptions.

## Exact indexed machine/resource translation

Use a stated fixed-slot signed binary 3-CNF representation: two Elias-gamma headers encode m+1 and v+1, followed by m records with exactly three signed literal identifiers of width b=max(1,floor(log2(v))+1). IDs are distinct and in [1,v], 1<=v<=3m, the byte/bit length must be exact. The parent H_F has 2m records, v'=v+m+1 and b'=O(log N), so its encoded length M=O(N log(N+2)); do not silently say O(N) when v is much smaller than m.

To access bit j of the virtual guarded input, use O(log N)-bit division/index arithmetic to locate its clause and literal slot; obtain its selector, private y_i, or one signed original-source literal by paid random-access probes. This takes log^{O(1)} N native steps and O(log N) scratch, with all input-index writes and jump erasures charged. A full source grammar validation can be done in N log^{O(1)} N time, O(log N) scratch. For any fixed solver E for these sibling equivalence predicates, virtual-input simulation on the same indexed read-only-input machine gives

$$
T_{3SAT}(N)=O((N+T_E(O(N\log N)))\log^c(N+2)),\quad
S_{3SAT}(N)=O(S_E(O(N\log N))+\log(N+2)).
$$

This counts parsing, source authentication, input reads/index tapes, guest steps, temporary scratch, output, and all-phase simultaneous peak. Eager materialization instead retains Omega(M) writable bits (rho>=1), even if freed before guest execution. The tested Python/Node implementations buffer strings and are not physical logspace-machine executions; the bit-local machine bound is a separate mathematical argument.

**Quantitative conditional corollary:** If E solved every guarded parent in time O(M^{11/10}) and space O(M^{1/2}), the displayed reduction would decide 3-SAT in time O(N^{6/5}), space O(N^{101/200}) after absorbing polylogarithmic factors. At c=6/5, beta(c)=((c+2)/c^2-c)/2=23/45>101/200. The FLMV theorem rules this out **provided** the standardized fixed-slot 3-CNF language has a proved quasi-linear locally-bit-addressable transfer from the paper's SAT encoding on the same machine. FLMV Theorem 3.1 and Corollary 3.2 provide the relevant transfer pattern, but the exact encoding identity cannot be assumed. No unconditional 3-SAT lower bound is claimed from the custom parser alone.

## Established-hard-family and shortcut ledger

Known odd-charge cubic-expander Tseitin 3-CNF: H vertices, 3H/2 original edge variables, exactly four forbidden-parity width-three clauses per vertex (4H source clauses), N=Theta(H log H) under standard sequential IDs, odd-charge UNSAT, even-charge SAT. Urquhart (1987) and Ben-Sasson/Wigderson (2001) show exp(Omega(H)) **ordinary shared-DAG Resolution** lower bounds on suitable expanders. This is not unrestricted machine hardness. The pre-existing original-source-authenticated R_mix341 AND3/GF(2) upper bound and exact binary-premise node minimum 4H-1 on bridgeless cubic odd-charge sources remain the countercontrol. Haken's ordinary Resolution PHP and Cook's ER PHP shortcut are additional separate proof-model controls. K4 and cube below are finite examples, NOT the asymptotically certified expander sequence.

## IDEA -> SEARCH -> ITERATE provenance

Read governing five-role handoff blob c3889a3e, current issue #3 through LSPV-3/430, AGENTS.md 19656af1, CODEX.md 754999f5, pnp-research skill b8df83a7, LSPV-2/426 c7e4563e, LSPV-4/420 e24528e3, LSPV-4/421 a3610cde, actual GROKPROOF/2026-11-05_1913_PROGRESS.md 8a004bf4, Claude TPORT-0002 1f9fc727. External full files: konard/p-vs-np proofs/complexity/README.md 7ee9a11e (finite one-tape model); blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea (scoped methods); openai/math Lean ExecCNFNodeSearchCosts.lean 1ced21f4 (fixed costed execution, no general oracle); FRAT-XOR README.md 38a137bc, CakeML LPR README.md e94f45e9, CNFgen tseitin.py 4bb5fd19. Web queries included 'FLMV theorem 5.7 indexed input', 'Urquhart expander Tseitin', 'Haken Resolution and Cook ER PHP', and 'black pebbling shared DAG'. Read original FLMV PDF pages 4, 6, 7 and Corollary 5.8. **Direct Google-branded search not available**; used indexed web search without claiming Google execution.

The initial materialized-guard implementation fails all-phase square-root space. Revised lazy input is O(log N) scratch and preserves source indices. Host-language producer **20,972 assertions**, independent no-import Node checker **16,771**, six sources (3 SAT, 3 UNSAT), 4,216 byte/bit-position parent checks and 9,420 instrumented original bit probes. K4 even/odd 206 -> 596 bits, cube even/odd 498 -> 1,368 bits; even models 8 and 32, odd 0. Malformed, zero-ID and source-size mutations rejected. Full executable producer, independent checker, source/guard records, raw results and SHA-256 manifest are in the same-run reproducibility archive, not all reproduced in the compact repository summary. Tests are finite, not unrestricted lower bounds.

## Status and next gap

**PROVED/RESTRICTED:** exact guarded-sibling reduction, physically explicit lazy accessor for a declared fixed grammar. **CONDITIONAL:** strict FLMV corollary requires checked standard-encoding transport. **OPEN:** an all-input, malformed-aware, recursively iterable, exponent-oblivious SAT-decider contraction with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2), including local rho, eta, guest access, caches and all phases. This result rejects cheap *general semantic* reconvergence, not selective legally proven reuse. Route B native R_mix341 and noncircular B3 remain OPEN. P versus NP OPEN.

Sources: FLMV JACM 2005 DOI 10.1145/1101821.1101822 (https://lance.fortnow.com/papers/files/tst.pdf); Urquhart JACM 1987 DOI 10.1145/7531.8928; Haken TCS 1985; Ben-Sasson/Wigderson JACM 2001.