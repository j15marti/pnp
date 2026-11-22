CHARGED-STATIC-RATIO-TINY (2026-11-22 ~23:23 PT)

Small computational test of Theorem 2 static demand ceiling on the permutation family from CHARGED-UNSAT-TRANSPORT1.

For r=5,6,7:
n=8r-1, m=10r, w=ceil(log2(8r))
N = 3n+2+2*floor(log2(m+1))+3m(w+1)+w
D = 6*(r-2)*(w+1)-1
h = log2(r!)
ratio = Dh / (N^2/8)

Results:
r=5: N=1185, D=125, h=6.906891, ratio=0.00491865
r=6: N=1419, D=167, h=9.491853, ratio=0.00629786
r=7: N=1655, D=209, h=12.299208, ratio=0.00750788

Ratios increase slowly toward the asymptotic ~0.053 as expected; still far below ceiling. Confirms static method saturates only a constant fraction at small scale.

P vs NP OPEN. DYNAMIC-COMPATIBILITY-OBLIGATION1 OPEN.
