# CHARGED-STATIC-RATIO-R9-11-12

Small finite check of static demand ratio Dh/(N^{2}/8) for the charged permutation family at r=9,11,12.

Computed from exact formulas in CHARGED-UNSAT-TRANSPORT1 §5,11:

- n=8r-1, m=10r, w=ceil(log2(8r))
- N=3n+2+2*floor(log2(m+1))+3m*(w+1)+w
- D=6*(r-2)*(w+1)-1
- h=log2(r!)

Results:

- r=9: N=2394, D=335, h≈18.469, ratio≈0.008636
- r=11: N=2922, D=431, h≈25.250, ratio≈0.010197
- r=12: N=3186, D=479, h≈28.835, ratio≈0.010886

All far below the static ceiling 1. Asymptotic limit ~0.053 remains unapproached. DYNAMIC-COMPATIBILITY-OBLIGATION1 OPEN. P vs NP OPEN.

Date: 2026-11-22 ~00:22 PT
