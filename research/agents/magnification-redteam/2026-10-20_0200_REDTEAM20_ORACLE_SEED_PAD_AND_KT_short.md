# REDTEAM20 | Two-route audit, 2026-10-20 02:00 KST
Status: mathematical counterexamples and bounded controls. P versus NP OPEN. Two active routes only: MCSP/MKTP and ARC/FLMV. Compact Witness Bridge remains a diagnostic.

## Pre-source falsifiers
1. Per-input randomized oracle correctness need not admit one globally valid fixed seed.
2. A conditional KT witness may carry its source as free side information.
3. Explicit diagonal-history formula output may itself cost the entire simulated clock.
4. Proof-certified solver races, local witness selection and delayed SAT deciders need separate model and resource accounting.

## Exact results
**Oracle quantifiers:** For three inputs x_i and three uniformly sampled seeds z_j let success iff i != j. Every input succeeds with probability 2/3, but for every seed some input fails. Thus forall x Pr_z[success]>=2/3 does not imply exists z forall x success. This does NOT challenge Ilango's actual stronger almost-sure random-oracle theorem.

**Output materialization:** If producing a diagonal tableau explicitly writes L>=T bits for a T-step computation, it costs Omega(T) time before any purported shortcut. An implicit local-index generator evades this lower bound but must supply a genuinely shared compact W for all clause indices and charge construction/evaluation. For SAT input n, writing a full M=n^a source already costs Omega(n^a), exceeding the target n^(241/200) when a>=241/200.

**Conditional advice:** Choose incompressible x of length m and auxiliary input y=x. Plain K(x)>=m-O(1) while K(x|y)<=O(log m). Under RANDOM-ACCESS BITWISE conditional KT, y_i may be copied quickly, but an ordinary KT machine cannot silently retain this auxiliary y. This does not assert a gap for sequential full-output KT where outputting m bits is itself expensive.

**Witness:** The three separate constraints W(0)=0, W(1)=1-W(0), W(1)=0 are individually satisfiable yet no one W satisfies all. Thus forall i exists W_i cannot replace exists W forall i. This does not settle the actual diagonal compactness premise.

## Exact bounded audit
All 512 Boolean 3-by-3 seed/input correctness matrices enumerated; six have each input correct on at least two seeds but no global success seed. Four possible W values exhaustively checked. For affine f(v)=a*v+b mod m, 11,288 serial versus binary-power comparisons passed, showing short explicit transitions can fast-forward. Twelve positive instances are falsely rejected by a hypothetical premature UNSAT decision. Twenty length/time exponent controls passed. No assertions failed.

Raw JSON: results/raw/separation/2026-10-20_0200_REDTEAM20_ORACLE_SEED_PAD_AND_KT.json (readback required).
Code attempt: experiments/review/2026-10-20_0200_REDTEAM20_ORACLE_SEED_PAD_AND_KT.js (publication blocked unless subsequently verified).

## Peer handoffs
:00 distinguish Ilango almost-sure oracle statement from unjustified fixed-hash selection; preserve CHMY both promises, one-way input and one work tape.
:12 produce charged source-free ordinary-KT short queries, not conditional KT, and preserve unknown fixed polynomial exponent C.
:24 audit a delayed arbitrary correct SAT decider, every child/source read, replay, output and peak simultaneous space against FLMV.
:36 attack actual succinct diagonal witness W existence, not restricted full-table path counts.
:48 integrate only into MCSP and ARC DAG; retain OPEN for ordinary R_k and arbitrary-decider contractor.

References: Ilango, SIAM J Computing 2026 doi:10.1137/24M1652568; CHMY STACS 2021 doi:10.4230/LIPIcs.STACS.2021.23; OPS ToC 2021 v17a011; MMW STOC 2019; FLMV JACM 2005 doi:10.1145/1101821.1101822; Hutter 2002; Blum 1967.

END_OF_VERIFIED_REPORT::REDTEAM20::P_VS_NP_OPEN
