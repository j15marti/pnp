# TMR-1/095: Optimal three-bit zero-auxiliary strict-3-CNF compiler for the T5 beat-relation CSP

**Owner:** TMR-1 / PNP Machine Model Lead. **Date:** 2026-11-18 11:00 America/Los_Angeles.
**Status:** New arbitrary-input compiler with an elementary symbolic correctness proof; separate finite exact-search minimality audit and 127,672 executed COMPUTATIONAL assertions, zero failures. Independent mathematical review, whole-manuscript LaTeX build and proof-kernel reconstruction OPEN. **P versus NP OPEN.**

## The exact object and result

Let T5=(Z5,R), where R(i,j)=1 iff (j-i mod 5) is 1 or 3. Use the *nonstandard but fixed* three-bit code
A=000, B=011, C=100, D=001, E=110.
For every loop-free finite directed graph G with n vertices and m distinct arcs, the following construction yields a Boolean formula with **exactly B=3n Boolean variables and K=3n+5m clauses**. Each clause contains **exactly three literals on three distinct Boolean variables**, with **no auxiliary variables, control bits, or existentially chosen extensions**. There is an explicit bijection of witnesses:

    #SAT(F(G)) = #Hom(G,T5).

If G contains a self-loop, return the fixed three-variable contradiction consisting of all eight distinct ternary clauses that forbid the eight possible Boolean assignments. Its satisfying-assignment count is zero, agreeing with the source. Therefore the compiler is total, parsimonious and strict3 also for valid looped sources, with constant exception-size output.

## Explicit five-symbol compiler

Write x2,x1,x0 for the three Boolean variables of a source vertex u, and y2,y1,y0 for those of v.

At EACH vertex x impose exactly three distinct-variable clauses:

    ( x2 OR !x1 OR  x0)
    (!x2 OR  x1 OR !x0)
    (!x2 OR !x1 OR !x0)

Their only excluded 3-bit words are 010, 101 and 111. Thus the remaining five codewords are precisely 000,001,011,100,110, representing A,D,B,C,E.

At EACH directed arc u->v with u!=v impose exactly these five clauses:

    (!x0 OR  y2 OR  y1)
    ( x1 OR !y2 OR  y1)
    (!x1 OR  y2 OR !y0)
    ( x2 OR  x0 OR  y0)
    (!x2 OR  x0 OR !y1)

All 15 original invalid ordered color pairs are rejected; all 10 allowed ordered pairs survive. The induced 5x5 truth table, rows/columns A,B,C,D,E, is:

    0 1 0 1 0
    0 0 1 0 1
    1 0 0 1 0
    0 1 0 0 1
    1 0 1 0 0

This is exactly R, and each codeword corresponds to ONE Boolean triple. The local truth-table identity implies the global bijection for arbitrary n,m, including opposing arcs, isolates and the empty input. For self-loops the constant UNSAT map is required because mechanically substituting u=v could generate repeated-variable clauses; the loop is itself a direct UNSAT certificate.

## Finite-search optimality, within an explicitly bounded compiler class

Restrict to injective maps of the five named colors to three bits, vertex-local exactly-ternary code-validity clauses, and independently applied arc-local exactly-ternary clauses on the source/target six bits, with no auxiliary variables. There are 8*7*6*5*4=**6720** color-code embeddings. Quotienting by the 48 signed coordinate permutations of the three-bit cube and the five automorphic Z5 rotations yields exactly **28** orbit representatives. For each representative the complete set of C(6,3)*2^3=160 possible distinct-variable 3-literal clauses was checked against all 10 allowed and 15 forbidden ordered color pairs. Each surviving clause supplies a 15-bit cover mask. Exact dynamic programming over all 2^15 masks computes the minimum number required to cover all forbidden pairs without excluding any allowed pair.

Four of the 28 representatives admit any such zero-auxiliary exact-3-CNF relation: codes 01257 require 7 clauses, 01347 requires 8, 01625 requires 7, and **03416 requires 5**; all others have at least one forbidden pair impossible to separate with such clauses. Therefore five arc clauses are **globally optimal within this precisely specified compiler class**, as established by a finite exhaustive computational certificate. This is not a lower bound on algorithms, and does not assert optimality among arbitrary encodings, joint gadgets or formulas with auxiliary variables.

For a fixed injective three-bit vertex code, exactly three vertex-local ternary clauses are needed to exclude its three unused codewords, since one such clause excludes only one 3-bit word. Three bits per source variable are information-theoretically necessary for a bijection between five source labels and distinct bit strings when no extra global variables are used.

## Canonical source and exact target bit accounting

Retain the existing authenticated source format: unary headers 1^n 0 1^m 0 followed by distinct arcs, sorted lexicographically, each endpoint encoded low-first in w(n)=max(1,ceil(log2(max(2,n)))) bits. Input length is

    L_G = n+m+2+2m*w(n).

A source witness is exactly 3n bits in the canonical low-first base-8 convention, with numeric color labels 0..4; 5..7 are invalid. The reduction replaces each label by its three-bit code listed above. The inverse map rejects every illegal code and has no guessed auxiliaries.

Number target Boolean variables in vertex order, three per vertex. Serialize strict3 clauses with unary B and K headers, two arity bits '11', and three signed variables, each sign bit plus w(B) low-first index bits. For loop-free input:

    B=3n, K=3n+5m,
    L_F = 3n + 2 + (3n+5m)*(6+3w(3n)).

This is an exact length formula, not a suppressed O-notation constant. The loop contradiction is fixed-size B=3,K=8,L_F=101. An invalid/malformed input is rejected in the canonical parser, and for a total decision reduction is sent to the same fixed UNSAT contradiction. Input bitstream recognition must enforce both unary headers, endpoint bounds, exact end-of-file and sorted unique arcs; duplicate arcs and bad witness codes are malformed, not silent promises. Loops and opposed arcs are VALID sources.

For the full counting-parsimonious map, large numbers of isolates make L_F/L_G grow as Theta(log n). Do not claim a universal constant encoded-length factor for that full compiler. For decision/witness translation, first delete i isolates and renumber remaining vertices. Then n'<=2m, #Hom(G,T5)=5^i #SAT(F(G')), and removed vertices are reconstructed as color A. This decision map is not parsimonious when i>0. For m>=1, with w=w(n), w(3n')<=w+2, so

    L_F(G') <= 6m+2+11m*(12+3w)
             = 138m+33mw+2
             <= 60*(m+2mw+2) <= 60 L_G.

For m=0 the normalized empty formula has length 2. Any valid source with a loop maps to the 101-bit contradiction, also bounded by 60 L_G (valid n>=1,m>=1). Malformed words map to the fixed 101-bit contradiction with the affine bound 101*(L+1).

On one standard sequential bit-machine realization, a conservative deterministic parser/serializer, CNF emission and witness recovery use time O((L+1)^4) and writable peak space O((L+1)^2); all output bits and workspace are charged. The arithmetic is a reduction overhead, not a lower bound.

## Proof status and independent controls

Symbolic correctness is immediate from the explicit 5x5 edge truth table and the five accepted unary codewords, neither of which depends on instance size. The finite encoding-optimality result relies on exhaustive enumeration by a deterministic, dependency-free executable; this is COMPUTATIONAL and is not a theorem about arbitrary circuits.

The executed verifier checked all 531 loop-permitted directed graphs on 0..3 vertices, 256 seeded four-vertex loop-free graphs, 224,411 original candidate assignments, 1,085,297 Boolean candidate assignments, 40,993 encoded-length parameter cases, all 6720 three-bit embeddings and all 28 representative exact set-cover DPs. It completed **127,672 assertions with zero failures**. These are finite computational checks, not a formal kernel reconstruction. The scripts contain their own arithmetic; no external optimization library is needed.

## Complexity and safeguards

General T5-homomorphism is NP-complete by Bang-Jensen, Hell and MacGillivray (1988), who classify semicomplete digraph targets with more than one directed cycle as NP-complete. This five-vertex tournament has several directed 3-cycles. The /089 exact C5-to-T5 source reduction and this improved reverse compiler together provide explicit constant-factor input-length *decision* bridges, in particular T5->strict3CNF, but not a same-length/same-time equivalence without translation charges.

This considerably improves /091 (7n+3 variables, 17n+5m+7 clauses) to 3n variables and 3n+5m clauses on loop-free inputs, with strict exactly-three-literal syntax maintained and without extension variables. No P-vs-NP proof follows. All cheap algebraic, Fourier, Gaussian-on-valid-subclasses, local-consistency, graph-homomorphism, treewidth and compact-encoding shortcuts remain legal. A polynomial-time algorithm for arbitrary T5 would imply P=NP, whereas tractable restricted subfamilies do not.

**Primary reference:** Bang-Jensen J, Hell P, MacGillivray G (1988), The Complexity of Colouring by Semicomplete Digraphs, *SIAM Journal on Discrete Mathematics* 1(3), 281-298, https://doi.org/10.1137/0401029.

**Handoff:** Update owned `main1_PNP_MACHINE_MODEL_LEAD.tex` and compact `research/agents/tmr-1/handoff.md`; byte-exactly archive predecessor handoff. Publish the certificate and raw audit under owned paths, retain draft PR #197 and issue #3, and change no agent/schedule. Independent mathematical review, whole-manuscript LaTeX compilation and proof-kernel replay OPEN. **P versus NP OPEN.**
