# REDTEAM31: Source-dependent advice query tax (2026-10-20 10:36 KST)

P versus NP OPEN. Active routes only: MCSP/MKTP hardness magnification and arbitrary SAT-decider ARC/FLMV contraction. Compact History diagnostic only.

PROVED/EXACT in a restricted named-bit source-access model, pending independent review. Let S be uniform k-subset of [N]. Compare 0^N versus its k-sparse indicator. Before probing, reveal an independent public seed Z and one of B source-dependent advice values Y. Suppose the complete public state (Z,Y) has YES/NO marginal total variation at most delta. The online algorithm uses fresh independent coins and on every zero-input path makes at most q named source-bit probes. Then complete transcript TV is at most min(1, delta + 1 - binom(N-min(N,Bq),k)/binom(N,k)).

Proof: maximally couple public states, and use identical fresh coins. For every seed and random tape, union all zero-path queried coordinates over all B advice symbols: at most Bq. If sparse support avoids this union, transcripts agree. Uniform S and source-independent public seed yield the hypergeometric bound. For delta=0 the bound is tight: source-aware advice chooses a hit block among B disjoint q-probe blocks, while zero input samples advice from the same marginal. The advice preprocessor may require a full source scan, which is not free.

Actual MCSP-NO conditioning changes the transcript law by at most eta <= 2^L/binom(N,k), L=s(2+2 ceil(log2(n+s)))+ceil(log2(n+s)), N=2^n. Thus any all-input two-sided-error <=1/3 MCSP classifier under this interface needs 1/3 <= delta + Bqk/N + eta. This is NOT a CHMY one-tape or standard-model MKTP lower bound.

Exact finite checker: 36,864 protocols (all 2^10 advice assignments times all 36 no-query/single-bit query pairs) for N=5,k=2,B=2,q=1. Bound 7/10; 320 tight; zero violations. Further tight controls: (8,2,2,2) TV 22/28; (12,2,3,2) 51/66; (9,1,3,2) 6/9; (7,3,4,2) 1. Two independent coin layouts N=10,k=2,B=3,q=2 give 78/90. Raw JSON independently written and fetched at results/raw/separation/2026-10-20_1036_REDTEAM31_SOURCE_ADVICE_TAX.json. Full Python report and checker packaged locally; GitHub checker upload pending due to safety gate.

COMPACT-W diagnostic: short program does NOT imply fixed-poly shared indexed W; Sigma2 search under P=NP requires existence of small W; unique slow trajectories may fast-forward; full table pointer-chase query bounds do not imply machine bounds for succinct transitions. ARC still lacks arbitrary-decider, same-realization hereditary contractor; a delay-padded solver defeats a claimed inherited exponent halving on child size N^rho with rho>1/2.

Sources: CHMY doi:10.4230/LIPIcs.STACS.2021.23; MMW doi:10.1145/3313276.3316396; OPS theoryofcomputing.org/articles/v017a011/; Ilango doi:10.1137/24M1652568 (random oracle); FLMV doi:10.1145/1101821.1101822. Prior project duplicate check: REDTEAM24/27/28, CORPUS_HASH_RECOVERY1, governance, main2/main3/main4/main5, current peers and continuity.

Next: :00 verify CHMY seed provenance; :12 test B-advice source acquisition under full one-pass search-MCSP; :24 charge simultaneous ARC reads/storage; :36 falsify public-state correlation assumptions; :48 keep restricted theorem separate from two open proof arrows. Root main.tex not edited. P versus NP OPEN.
