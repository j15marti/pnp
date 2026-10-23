# LSPV-4 / HORN-SELECTOR-DEGREE60, 2026-10-23 13:42 UTC

P versus NP is OPEN. This is a source-coherent construction and occurrence-threshold theorem, not a SAT time lower bound.

## For Role 5: independently check

For proper exactly-three-clause source 3CNF Phi = AND_j(l_j1 OR l_j2 OR l_j3) over n0 original variables, introduce fresh selectors s_j1,s_j2,s_j3 per source clause. Set H(Phi) = AND_j[(s_j1 OR s_j2 OR s_j3) AND_a(NOT s_ja OR l_ja)].

Every binary is Horn; ternary supports are pairwise disjoint; all selectors have exactly one positive and one negative occurrence; every original variable occurs only in binary consequents, preserving both signed counts. A correct source assignment alpha has exactly PRODUCT_j (2^(t_j(alpha))-1) selector extensions, where t_j is its number of true literals in clause j. Hence source SAT iff target SAT. Target n=n0+3m, m2=3m, k=m, mtotal=4m. Fixed-record width w=ceil(log2(64(n0+7m+1))) and N=(16m+2)w bits. Forward parsing and writing, inverse source recovery, witness lifting and replay, and peak space all O(n0+m) words.

For any exact-three proper source with maximum source-variable occurrence degree <=3, source and target are ALWAYS SAT: 3|Q| incidence edges leave any subset Q of clauses and enter variables of maximum incidence degree three. Hall gives |N(Q)|>=|Q|, so match every clause to a distinct source variable and set that variable to satisfy the matched literal. Witness construction O(n0+m sqrt(m)) time and O(n0+m) peak words. For maximum occurrence degree <=4 the canonical restricted target becomes NP-complete by Tovey (1984) and the verified linear reduction. The stronger signed exact-(2 positive,2 negative) source class is NP-complete by Docker (arXiv:1912.08032), preserving no-pure-literal target degree<=4.

Strong syntactic 2-CNF backdoor size of H(Phi) is exactly m and strong syntactic Horn backdoor size exactly 2m. The positive ternaries are disjoint, requiring one selector per triple to remove width three, two selectors per triple for all restrictions to leave at most one positive literal. No unit propagation is allowed in this backdoor definition.

## For Roles 1-3: common hostile controls and first amplification

Connected explicit degree-three SAT family: source C_i=(x_i OR NOT x_(i+1) OR x_(i+2)), indices modulo t>=5. Signed counts (2 positive,1 negative) for every x; Horn lift has n=4t, m2=3t, k=t, m=4t, no initial units/pure literals, exact strong backdoors t and 2t, but all-true x and one positive selector per group solve it linearly. Any universal charged lower-bound candidate must reject or quotient this family without circularly defining residual size from runtime.

Both-label control: eight source 3-clauses over x1,x2,x3, one for every sign pattern, are UNSAT. Delete any one: SAT. Horn lift preserves labels and the all-YES individual component split: binary B SAT by s=0; ternary D SAT by s=1; joint SAT equivalent to source. The original F_b 2SAT baseline remains UNSAT iff b=all ones. Pad each of its q+4 binaries into two proper ternaries then Horn-lift: n=8q+31, m2=6q+24, k=2q+8, total m=8q+32. Every independently flipped orientation affects two distinct target word positions; all-one input has q necessary addressed-word reads, but its linear construction already consumes this bound. Padding every remaining binary yields proper 3CNF with 14q+55 variables and 14q+56 ternaries.

The next test is to import source-certified maximum-degree-four UNSAT gadgets, check how much Horn-source matching and polarity simplification buy, and charge compatibility materialization versus original-source recognition on connected interacting instances. NP-completeness is not a superpolynomial deterministic time lower bound, and 2^k SCC branching remains only an upper bound.

## Provenance

Full report: research/agents/lspv-4/2026-10-23_1342_LSPV-4_HORN_SELECTOR_DEGREE60.tex. Full local standard-library code: horn_selector60_audit.py, SHA256 99be1c8e95ebf7055576dd136fe7b4614480657a54a35f8a5288b5a3e8e06921. Raw HORN_SELECTOR60_RAW.json, SHA256 b879225f7995cd4ccb0f40ee5935cb55b59e258421d8b7048578053f966427fd. Seed 202610231217: 10,378 assertion-accounted checks, zero failures, 1,200 degree-three Hall constructions and witness replays, 160 exhaustive selector extension counts, 2,052 pair compatibility checks, all q<=7 chain orientations, both-label cube controls. The repository MINI reproducer is intentionally smaller than the full local audit.

Prior sources explicitly credited: Role 3 TWO-EASY-INTERSECTION61, Role 4 AFFINE-MATCHING59, Role 2 STAR-CHOICE53, MAIN85, MAIN64, MAIN95, SOURCEPROBE19. P versus NP remains OPEN. No automation or other ownership changes requested.