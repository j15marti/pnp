CHARGED-STATIC-RATIO-MED (2026-11-22 ~22:19 PT)

Small computational test of the static separated-input ceiling from CHARGED-UNSAT-TRANSPORT1 Theorem 2 on the permutation family at r=20,30,40.

For each r:
n=8r-1, m=10r, w=ceil(log2(8r))
N=3n+2+2*floor(log2(m+1))+3m*(w+1)+w
D=6*(r-2)*(w+1)-1
h=log2(r!)

Ratios:
r=20: N=5901 D=971 h=61.0774 Dh/(N^2/8)=0.013625 Dh2/(N^3/27)=0.000476
r=30: N=8843 D=1511 h=107.7091 Dh/(N^2/8)=0.016650 Dh2/(N^3/27)=0.000684
r=40: N=12984 D=2279 h=159.1590 Dh/(N^2/8)=0.017213 Dh2/(N^3/27)=0.000712

Still far below the asymptotic limit ~0.05333 of the static method. Confirms static distinguishability alone cannot force superpolynomial demand. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN.

P vs NP OPEN.
