# LSPV-2 SIGNED-PUNCTURE-PROFILE218 | Additive LSPV-1/LSPV-4 handoff
Date: 2026-10-29 07:19 UTC. Status: PROVED/EXACT for restricted transfer theorem, COMPUTATIONAL for explicit finite controls, independent review pending; all-input reduction and P vs NP OPEN.

## What changed and how to use it

For disjoint CNF modules `A_i AND (l_i OR D_i)` whose designated literal occurrences `l_i` all have the same sign, define exact puncture states `(a_i,d_i)` realized by some assignment satisfying `A_i`, where `a_i=truth(l_i)` and `d_i=truth(D_i)`. Replace in each selected clause the literal `l_i` by the predecessor's `l_(i-1)` in a cycle. All positive/negative occurrence quotas remain unchanged. The resulting formula is satisfiable iff the Boolean trace of the product of 2-by-2 transition matrices `T_i(u,v)=OR_{d:(v,d) in P_i}(u OR d)` is true. Computing these matrices from unknown arbitrary SAT-hard source modules is not free. This is the exact missing acquisition obligation.

Old LSPV-3 CONNECTED-SPLICE-LOCAL-CORE133 proved that cyclic swapping among minimally UNSAT modules stays UNSAT. Its hypothesis requires *every* source module minimally UNSAT. Such a module has puncture profile exactly `{(0,0)}`. The new control has a SAT affine shell R_p with all four puncture states; exchanging a negative literal with UNSAT W11 reverses answer from UNSAT to SAT. This is a counterexample to arbitrary degree-preserving answer transport, not to Role-3's sound theorem.

For every odd p>=5 and k>=3, a cycle consisting of affine shell R_p and k-1 W1 modes gives connected proper signed exact-(2pos,2neg) ordinary 3CNF. Matched modes (W11,W00,...) yield SAT, modes (W11,W11,W00,...) yield UNSAT, while unsigned scopes, every signed degree, n,m and DIMACS byte lengths agree. Exactly four signed occurrences differ. A single fixed program recognizing and parsing the entire canonical cycle can compute 2-bit W profile from <=2^15 assignments per fixed W module and then multiply the constant-sized matrices, writing a 226-byte YES or NO base formula. For source bit length >=32768, child length 1808 bits obeys Nchild<=Nparent^(3/4). This is a RESTRICTED one-child decision compiler, not arbitrary SAT.

Finite audit: W modes 772/272/272/0 complete solutions; 131072 profile assignment checks; all 256 abstract profile-pair combinations; 6 matched growing pairs (p,k)=(5,3),(5,4),(7,3),(11,6),(31,7),(101,12); all 16 W mode pairs at p5,k3 agree with separately implemented DPLL, 11319 aggregate calls; direct witnesses and malformed-source controls. Python reexecution raw SHA256: fb549f2f8cf8275aefe37c29a6778ff71b7396c6982e5a7f8f3f78cf38bc86a3. No random seed.

Resources: indexed source can be parsed on fixed-k read-only-input multitape machine in conservative O(N^3) native time/O(logN) work bits with constant child output, and via ordinary one-tape simulation O(N^4) time/O(N) footprint including input. These are upper bounds on canonical grammar, not general-SAT lower bounds. RAM access and malformed-input scanning charged. No claims about FLMV transport or a hypothetical K without the missing all-input map.

## Requests for peer review

LSPV-1: Audit the cyclic trace proof and check any generalization to a growing interface. In particular do not treat computed W profiles as free for arbitrary attached NP-complete core.

LSPV-4: Audit the same-machine fixed-k/one-tape resource ledgers and fixed-base physical output bytes. Avoid conflating the profile lower boundary with SAT decision lower bounds.

Next LSPV-2 bottleneck: Find a *constructively discoverable* exact relation summary on arbitrary hard modules under a fixed, polynomially charged preprocessing and ordinary-SAT reentry cost. Try a growing-interface two-level closure with both answer sides. No change to five agents, schedules or original responsibilities.