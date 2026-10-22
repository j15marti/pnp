# Independent arithmetic check of VIRTUAL-CHILD-COMPOSITION61 Corollary 61B (runs <1s).
from fractions import Fraction as F
def step(t, s): return max(F(11,10), F(3,5)+t/2), max(F(1,2), s/2)
t, s = F(1203,1000), F(505,1000)
for k in range(1, 9):
    t, s = step(t, s)
    print(k, float(t), float(s), "gap_to_1.2 =", float(t-F(6,5)))
# gap halves each step: t_k - 1.2 = (t_0 - 1.2)/2^k  (exact while t>1.2)
assert step(F(1203,1000),F(505,1000)) == (F(12015,10000), F(1,2))
