# SUPERLOG-MARKOV1: Long histories versus exact continuation states

Date: 2026-10-21
Status: model-specific theorem + exact finite audits; P versus NP OPEN.

## New theorem (fully charged finite-state alternating game)
For an r-round alternating game with M exactly continuation-sufficient states and at most B universal and A existential moves per stage, the winner is computed by backward DP:

W_r(s)=terminal(s)
W_i(s)=AND_y OR_z W_(i+1)(delta_i(s,y,z))   [universal-first round].

For existential-first reverse the operators. With preprocessing time D/space E and transition access t time/w workspace, fully charged bounds are O(D+r*M*A*B*(t+polylog N)) time and O(E+M+w+log(N+rMAB)) simultaneous writable bits (in a bit-cost RAM model). State must preserve every future consequence, not merely share a hash value.

## Constructed quantified 3-SAT family, q=Theta(N/log N)
Use initial existential a followed by r rounds forall y_i exists z_i, with constraints z_1=a XOR y_1 and z_i=z_(i-1) XOR y_i. Each XOR is four proper 3-clauses. Source has 2r+1 variables, 4r clauses and 2^r adversarial histories, with unique adaptive response at each y-history for fixed a. Full Skolem table has 2^(r+1)-2 response bits, but a single parity state plus invalid sink suffices; the DP examines exactly 12r transitions. Standard encoded bit length is Theta(r log r).

Prior project's quantifier-preserving 7-clause+clone-cycle+Q-port compiler yields exactly 36r variables and 48r proper clauses, every variable twice positive and twice negative. For r=32: 1,152 variables, 1,536 clauses, 4,608 literal incidences, and 2^32 universal histories. A straightforward matrix evaluation circuit has 5,759 gates including shared negations, plus 10,366 declared connections; these are achieved evaluator costs, not minimal quantified decision circuit size.

Hash collision warning: digest h(u,v)=u XOR v maps 00 and 11 to the same value, but terminal test [u=1] separates them. Hash label equality does not certify equivalent future continuations.

## Existing unconditional SAT time-space lower bound rules out an all-input source-only compressor

Fortnow, Lipton, van Melkebeek, Viglas (JACM 2005, Cor. 5.8 and Cor. 3.2) show a sufficient forbidden region for simultaneous SAT time N^c and space N^d: d < beta(c) = ((c+2)/c^2 -c)/2, with strict margins. beta(11/10)=1769/2420>1/10.

If an all-SAT, uniform *source-only* correct compiler produced exact continuation-state games with prep N^(1.1+o(1)) time, N^(.1+o(1)) writable space, r<=N^(1+o(1)) rounds, M<=N^(.1+o(1)) states, constant actions, N^o(1) charged transition access, and <=N^(.1+o(1)) live transition workspace, the DP would violate that known theorem. Therefore at least one of these joint requirements cannot hold. This is a model-specific corollary, NOT a proof of P != NP.

The previous iterated-contract target (6/5,1/2) still falls strictly inside the known forbidden region: beta(6/5)=23/45 and gap=1/90. The missing item is an *assumption-dependent, globally correct, fully charged, iterable* transformation of every polynomial SAT solver, not an ordinary source-only layout.

## Experiment
- 1,574 independent brute-recursion/game-DP matches on random finite games.
- 17 parity-game round counts, to 128 rounds.
- 9 quantified exact-(2,2) compiles, through 1,152 variables and 1,536 clauses.
- 10,492 checked source witnesses.
- 56 positive and negative full-assignment fibers checked independently via SciPy/HiGHS MILP, all pass.
- Six generated QDIMACS files independently parsed; occurrence counts pass.
- Standalone three-page TeX/PDF formal proof and Python reproducibility bundle verified locally.

## Next proof target
Explore a *solver-dependent* recursive representation that retains an exact continuation quotient and reaches the simultaneous SAT forbidden resource region, charging generation, access, every live buffer, witness consistency and iteration closure. Do not treat exponential history counts, short hashes or high proof-system complexity as unconditional SAT time lower bounds.

Primary literature: https://doi.org/10.1145/1101821.1101822
Previous spine: research/review/spines/2026-10-21_SHORTCHALLENGE1.md
