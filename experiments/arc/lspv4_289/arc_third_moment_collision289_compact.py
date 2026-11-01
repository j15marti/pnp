#!/usr/bin/env python3
"""ARC289: exact opposite-label third-moment collision on Döcker target.
Run from j15marti/pnp root. This is a restricted falsifier, not an ARC solver.
Uses existing ARC288 audited source / cumulant code to avoid copying U198.
"""
from pathlib import Path
import runpy,itertools
from fractions import Fraction
Q=Fraction
r=runpy.run_path("experiments/arc/lspv4_288/arc_connected_cumulant288_compact.py")
src,third,valid=r["src"],r["third"],r["valid"]
U=src()
V=[c[:] for c in U]
V[1][0],V[7][0]=V[7][0],V[1][0]
LO=[[1,6,7],[3,4,7],[1,2,3],[4,5,8],[5,6,9],[2,8,9],
    [-3,-4,-9],[-2,-3,-7],[-5,-6,-8],[-2,-4,-9],[-1,-5,-7],[-1,-6,-8]]
HI=[[2,3,6],[7,8,9],[4,7,9],[3,5,6],[1,4,8],[1,2,5],
    [-1,-2,-5],[-6,-7,-8],[-3,-4,-7],[-3,-4,-9],[-1,-6,-9],[-2,-5,-8]]
VW="010110111001100010001111000101011110010101001111010001001011010000110010000100001001010111010000111010101010001101001010010010110001100011111001010101011011001110000100000001110110111000101100100001"
def shift(F,z):return [[(1 if v>0 else -1)*(abs(v)+z) for v in C] for C in F]
def sat(F,a):return all(any((int(a[abs(v)-1])==1)==(v>0) for v in C) for C in F)
A=U+shift(LO,198)
B=V+shift(HI,198)
def check(name,F,n):
    assert valid(F,n),(name,"invalid")
    t=third(F)
    return {k:t[k] for k in ("k2","k3","raw_third")}
assert len(VW)==198 and sat(V,VW)
glo=[a for a in itertools.product((0,1),repeat=9) if sat(LO,a)]
ghi=[a for a in itertools.product((0,1),repeat=9) if sat(HI,a)]
assert len(glo)==72 and len(ghi)==66
assert sat(B,VW+"".join(map(str,ghi[0])))
values={name:check(name,F,n) for name,F,n in
   [("U198",U,198),("V198",V,198),("G_low",LO,9),("G_high",HI,9),
    ("UNSAT207",A,207),("SAT207",B,207)]}
assert values["U198"]["k3"]=="3189/256"
assert values["V198"]["k3"]=="1581/128"
assert values["G_low"]["k3"]=="27/32"
assert values["G_high"]["k3"]=="243/256"
assert values["G_low"]["k2"]==values["G_high"]["k2"]=="17/16"
assert all(values["UNSAT207"][x]==values["SAT207"][x] for x in ("k2","k3","raw_third"))
assert values["SAT207"]["k3"]=="3405/256"
assert values["SAT207"]["k2"]=="613/32"
assert values["SAT207"]["raw_third"]=="11023257/256"
# U198 is UNSAT by the separately source-derived 64-boundary refutation,
# replayed by the independent full verifier in the downloadable archive.
# No timeout is treated as an UNSAT certificate.
print(values)
print("EXACT third-moment collision. Unrestricted ARC/P vs NP OPEN.")
