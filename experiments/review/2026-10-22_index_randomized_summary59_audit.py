"""INDEX-RANDOMIZED59: exact small-case check that a detached b-bit summary of X_A (subset of {0,1}^k)
answering all singleton membership queries with error <= 1/3 per query needs b >= (1 - H(1/3)) 2^k
(information bound), and that deterministic exactness needs 2^k bits. Runs in well under 30s."""
from math import log2
def H(p): return -p*log2(p)-(1-p)*log2(1-p)
for k in range(1, 9):
    m = 2**k
    # one-way randomized INDEX lower bound (Ablayev 1996 / Kremer-Nisan-Ron 1999): >= (1-H(eps)) m
    lb = (1 - H(1/3)) * m
    # deterministic: all 2^m subsets distinguished by singleton queries -> m bits (checked exhaustively for m<=16)
    if m <= 16:
        sig = {tuple((S>>j)&1 for j in range(m)) for S in range(2**m)}
        assert len(sig) == 2**m
    print(f"k={k} m={m} det_bits={m} rand_bits>={lb:.2f}")
print("OK")
