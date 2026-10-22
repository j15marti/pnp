# DENSE-COVER-ORACLE38 | 2026-10-22 KST

Global status: unrelativized P!=RP OPEN, P=RP OPEN, P versus NP OPEN.

## Three falsifiable constructions set before source review
1. Black-box zero-versus-half-dense query promise: exact deterministic 2^(m-1)+1 versus RP one uniform oracle query.
2. Explicit bounded-fan-in Circuit-SAT forbidden-row C_H=AND_(h in H) OR_i(r_i != h_i): evade any fixed polynomial-size tape list H; check gate-readable shortcut, ANF degree and faithful Tseitin.
3. Recursive clocked oracle diagonalization specialized to dense-or-zero slices: prove P^A != RP^A RELATIVE to one recursive oracle, not unrelativized.

## Results
ESTABLISHED restricted: zero-or-at-least-half-dense Boolean evaluation oracle requires exactly 2^(m-1)+1 deterministic value queries; an RP oracle algorithm uses m independent random bits and one query with no false positive.

ESTABLISHED explicit hostile control: C_H has 2^m-|H| models. Source-shared bounded-fan-in circuit has g=m+m|H|-1 gates for nonempty H. For odd |H|, its ORIGINAL random-tape ANF has maximum degree m. For m=8, H={0,e_1,...,e_8}, g=79, acceptance 247/256, ANF degree 8. Functional 3CNF has 90 variables, 237 clauses and precisely 247 full satisfying assignments by unique gate trace. Reading gate opcodes and signed source wires reconstructs H and gives an accepting tape (00000011) in polynomial time. A q-bit digest and h full-witness-only probes do not bound these gate-source reads.

ESTABLISHED recursive RELATIVE theorem: enumerate clocked deterministic oracle machines; at a fresh n_i answer their at most p_i(n_i)<2^(n_i-1) oracle probes consistently as zero. If M_i accepts, fill the fresh A(1^n_i0z) slice with zeros; if it rejects, fill its unqueried slice cells with ones. Freeze all answers and increase the cutoff. Every P^A machine is diagonalized, but a uniform RP^A machine samples n unbiased bits and queries one slice address with one-sided success >=1/2. Construction of A itself is recursive but unbounded time, and A is an external oracle not an explicit polynomial-size circuit input. This is a standard-form relativizing diagonal construction, not a new class separation. Baker-Gill-Solovay's recursive P^B=NP^B oracle yields P^B=RP^B in an opposite oracle world.

CONDITIONAL: A uniform polynomial-time density booster from arbitrary Circuit-SAT to zero-or-half-dense explicit circuits would give SAT in RP and hence NP=RP, not P=RP.

Audit: stdlib Python, 17,927 assertions, zero failures; 7 explicit Circuit-SAT cases, 164 promised three-bit oracle tables, six finite diagonal strategy tests. Complete 3CNF assignment enumeration was limited to at most 14 total variables. Higher examples used mathematical unique-extension proof plus full PRIMARY assignments and deliberate wrong-trace checks.

## Direct three-source budget
1. 2026-10-22_RP_TRACE_COEFFICIENT37_REPORT.md (local accessible original predecessor, revisited).
2. research/main/2026-10-22_2248_MAIN_FULL_COVER_CHILD_FIREWALL74.md (GitHub SHA 83373a91ede6be409386b3dbdd60174a0bb24281, new direct read): all-row cover gives UNSAT endpoint, our partial cover gives density continuum.
3. research/agents/rp-derandomization/2026-10-22_0836_RP_AFFINE_BASIS25_HANDOFF.md (GitHub SHA e5adbe6d9c1918ee5aeae0db6c77fbd418613c42, revisited): its certified source-affine factor independence does NOT hold for full-source-shared C_H.

Literature checked: Gill 1977, Baker-Gill-Solovay 1975, Bennett-Gill 1981, Cook 1971. Still unseen here: complete growing SHA/timer WRAPPER, most Drive Living Logs, newer :36 results, uninspected archive, independent feedback. Next: test three growing real WRAPPER acceptance circuits, original independent coin density and zero-error promise; adversarial H list versus gate-readable bypass; charge all source reads, gate inspections, traces, digests, advice and simulation.
## Important nonuniform bounded-size qualification
For any *fixed* m-input circuit gate budget s, the number of bounded-fan-in circuits is at most 2^O(s log(m+s)); a union bound gives a nonuniform list of O(s log(m+s)) random tapes hitting ALL half-dense circuits of size <=s. This may be polynomial advice, not a uniform polynomial-time hitter (cf. Adleman 1978, RP subseteq P/poly, DOI 10.1109/SFCS.1978.37). The hostile C_H requires Theta(m|H|) gates, potentially beyond this fixed budget. Therefore it only excludes a single fixed polynomial-size oblivious hitting-list family against the UNION of all polynomial-size circuit families with no shared degree bound. It does not contradict fixed-s nonuniform hitting sets or AFFINE-BASIS25.
