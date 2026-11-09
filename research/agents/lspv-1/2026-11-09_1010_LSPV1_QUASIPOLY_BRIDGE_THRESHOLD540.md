# LSPV-1/540: exact rate threshold for an abstract-proof lower bound paired with a fixed-r computational bridge

2026-11-09 10:10 PST | Route B | PROVED/RESTRICTED logical metatheorem; COMPUTATIONAL arithmetic controls. **P versus NP OPEN.**

**Affected proof-chain IDs:** proposed [P2-L1-540], refining the *required growth rate* at [P2-B1] and the candidate quasipolynomial substitute for [P2-B2], without closing [P2-D1], [P2-C3], [P2-B1] or [P2-B2]. Related [P1-X1] and [P1-05] remain unchanged.

## IDEA: falsifiable candidate and four falsifiers

**Candidate.** A fixed-exponent quasipolynomial same-R bridge can suffice for a separation when paired with a sufficiently strong **all-rule** abstract lower-bound certificate, but merely proving superpolynomial worst-case minimum refutation work is not enough for bridge exponent r>1. The precise threshold is growth faster than exp(O((log N)^r)).

F1: a fixed-r bridge with r>1 already implies polynomially bounded R refutations from SAT in P (FALSE, only quasipolynomial follows).
F2: a lower-bound family with exponential log-work and polynomially encoded length can coexist with the bridge and a polynomial SAT decider (FALSE, quantitative contradiction below).
F3: an abstract lower bound computed for ordinary Resolution alone can be substituted for full historical R_mix341 (FALSE: known local GF(2) and AND3 shortcut is an upper-bound control).
F4: superpolynomial work by itself contradicts a fixed-r bridge for r>1 (FALSE as a statement about growth rates; explicit countermodel below).

## SEARCH and continuity

Read the governing `research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md`, BOTH full root trackers at start (proof1 SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2 SHA 6f9d12992b157112934c3e76604d8483586b6e68), current issue #3 including LSPV-5/464, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-1/538-539, LSPV-3/536-537, LSPV-5/464, GROKPROOF/2026-11-09_1230_PROGRESS.md and actual Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`. These do not establish a full historical-calculus lower bound or a same-R computational bridge.

External change-aware exact files: `konard/p-vs-np/README.md` blob 0e0ec77f83ad6eec1719a96066108b96ac1a95 and `scripts/proof_status.json` blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-machine P subset NP only); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped claims); `meelgroup/frat-xor/format.md` blob 986a21aa92b62f844ef1fce852193142c41b2b1f (XLRUP theory syntax, not the historical R_mix341 grammar); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (standard source generator); `openai/math/README.md` blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (heterogeneous verification status).

Primary references consulted: Cook & Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44:36-50, https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf ; Urquhart (1987), *Hard Examples for Resolution*, JACM 34:209-219, DOI 10.1145/7531.8928 (expander-derived **ordinary Resolution** lower bounds); Atserias & Dalmau, JCSS 74(3):323-334 (2008), https://eccc.weizmann.ac.il/eccc-reports/2002/TR02-035/index.html (Resolution width/game, NOT full mixed rules); Cousot & Cousot POPL 1977 and Keller et al. IJCAI 2016 from governing handoff for sound overapproximation and admissible cost partitioning. Indexed public web queries were run; no separately authenticated Google-branded search interface. No external proof assistant replay.

## FORMAL SETTING

Fix one sound, complete, effective source-authenticated weighted calculus R before all inputs. W_R(F) is the minimum total native weight of *distinct* paid nodes in a valid shared branching refutation DAG; Wbar_R(N) is the maximum over UNSAT binary sources of length <=N, empty max zero. Free after-the-fact optimization, auxiliaries, valid branch reconvergence, source authentication and all legal rules are included.

For each single fixed uniform total correct decider A let T_A^wc(N) be its worst-case time over **all binary inputs of length <=N**, including malformed strings. Write Q_r(R), for one fixed real r>=1, for the **OPEN candidate bridge**

$$
\forall A\ \exists C_A>0,N_A\ \forall N\ge N_A:\quad
\overline W_R(N)\le
\exp\!\left(C_A[\log(N+T_A^{\rm wc}(N)+2)]^r\right).
$$

The quantifier over A is not restricted to a chosen solver class. The constants may depend on A; r is fixed independently of A and N. This is NOT a theorem about historical R_mix341.

A cost-sound abstract construction has W_R(F)>=H(F) only when the abstract may-transition system covers **every native rule**, charges no more than each concrete transition, preserves every completed refutation, and independently proves abstract budget nonreachability. With unidentified native rules it must overapproximate them conservatively. No such superpolynomial H is presently certified for full R_mix341.

## THEOREM 540.1 (PROVED/RESTRICTED logical rate calibration)

**(a)** If Q_1(R) holds then B2 and B3 hold for R: setting p_A(x)=(x+2)^ceil(C_A) gives a polynomial upper bound in N+T_A^wc(N) for all sufficiently large N (increase its coefficient to cover finite initial N). In contrast Q_r(R) for r>1 and a polynomial-time SAT A yields only Wbar_R(N)<=exp(O((log(N+2))^r)). This growth-rate implication alone does not imply B3.

**(b)** Suppose a family of encoded UNSAT sources F_h, with h unbounded, satisfies |F_h|=N_h<=K h^b(log(h+2))^a for constants K,b>0 and a>=0, and an all-rule certificate proves

$$
W_R(F_h)\ge\exp(c h^\delta)
$$

with constants c,delta>0. Then Q_r(R) implies, for **every** single total correct uniform SAT decider A, on all sufficiently large family lengths,

$$
T_A^{\rm wc}(N_h)\ge
\frac12\exp\!\left((c/C_A)^{1/r}h^{\delta/r}\right)
$$

after adjusting the positive constant if needed. In particular no polynomial-time SAT decider exists, and P!=NP **conditional on both premises**, neither of which is proved for full R_mix341.

**Proof.** Since Wbar_R(N_h)>=W_R(F_h), the two inequalities force
C_A[log(N_h+T_A^wc(N_h)+2)]^r>=c h^delta.
Thus N_h+T_A^wc(N_h)+2>=exp((c/C_A)^(1/r)h^(delta/r)). Since N_h is polynomial in h, subtracting N_h+2 leaves at least one half of that exponential for sufficiently large h. A fixed polynomial-time A contradicts this estimate. For (a), r=1 is a power of N+T and r>1 gives a quasipolynomial expression. QED.

**(c) SHARP GROWTH-RATE OBSTRUCTION.** Fix any r>1 and choose 1<q<=r. The numerical growth function

$$
g(N)=\exp((\log(N+e))^q)
$$

is superpolynomial, but is bounded above by exp(C(log(N+e))^r) for large N. Thus the lower-bound statement Wbar_R superpolynomial **alone** cannot contradict Q_r under a hypothetical polynomial-time A when r>1. This is a countermodel for the abstract rate inference, NOT a constructed proof calculus. To contradict Q_r via the rate comparison alone one needs log Wbar_R(N)/(log N)^r unbounded on sufficiently large N, for example exp(Omega(N^eps)) hardness.

## Exact published-family calibration and known shortcuts

Urquhart's exponential lower bound is for qualifying **expander-derived odd Tseitin** formulas in ordinary shared-DAG Resolution, not the full mixed calculus. For simple cubic graphs with h vertices, strict source has n=3h/2 edge variables, m=4h source clauses and N_h=Theta(h log h) fixed indexed bits. If a same-Resolution Q_2 bridge existed, Theorem 540.1 would give T_A^wc(N_h)>=exp(Omega(sqrt(h))) = exp(Omega(sqrt(N_h/log N_h))). This implication does not prove the bridge.

For the project's **declared binary-source historical semantic fragment**, LSPV-2/341 already gives a 3h AND3 plus h-1 GF(2) proof of the same odd-charge sources: paid cost 4h-1. Therefore its Resolution exponential hardness CANNOT be plugged into the all-mixed premise. This is an actual cheap certificate control, not a failure of the rate algebra. Haken PHP Resolution versus Cook Extended Resolution is the second mandatory warning. A hypothetical historical native full R_mix341 all-rule exp-hard family and Q_r would be new open proof obligations.

## ITERATE, validation and scope ledger

Symbolic checks: (a) exponent comparison (log N)^r vs log N, (b) monotonicity and inversion of Q_r, (c) explicit 1<q<=r growth-rate countermodel; no unproved theorem is invoked beyond the *conditional* inputs. Executed Python 3 standard-library numeric verifier: 25 recorded cases (r=2,3,4, q=(1+r)/2, logN=16..1024; and h=64..4096 encoding controls), all assertions passed. Executable SHA256 d0adc1e5181bd9c83d012fa6f2f8b16cc2af5795e6f6358207905c2d9eb93542; local complete raw SHA256 24f5a2b509f50b776c52134b9e5076b995f87e75a7514888c2cfa733d3c96189. Arithmetic tests do NOT establish Q_r, a mixed lower bound, proof-checker correctness or any SAT runtime fact.

**Three ledgers:** (i) a particular solver abstraction supplies no all-A result; (ii) full R_mix341 all-rule may abstraction and H remain OPEN under [P2-D1]/[P2-C3]/[P2-B1]; (iii) unrestricted machine lower bound and same-R Q_r/B3 remain OPEN [P2-B2]. W_R is logical distinct-node cost, not certificate-bit length, discovery, sequential time, weighted span or physical peak memory. Construction and verification costs of any actual algorithm remain separate; time alone does not imply polynomial space.

**Material new statement:** for r>1 the proposed Q_r bridge requires superquasipolynomial *relative to r* abstract hardness, not merely the currently targeted generic superpolynomial [P2-B1]. A concrete work-horizon for LSPV-3/5 is an all-rule cost-sound may certificate of exp(Omega(h^delta)) on an encoded certified-hard family, plus an independent noncircular Q_r simulation. This is a calibrated target, not an assertion that either exists.

**Remaining exact gap:** Authenticate all historical RES/AND3/GF(2)/LOCAL-CONVERT/DEF/facet/scope/side-read rules and charges; derive a genuinely strong all-rule abstract lower bound; prove Q_r or B3 for SAME preselected R without assuming certificates. No root main.tex edit without authenticated complete content. P versus NP OPEN.
