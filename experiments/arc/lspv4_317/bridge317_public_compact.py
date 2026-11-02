#!/usr/bin/env python3
"""LSPV4-317: promised signed balanced (2,3)-CNF -> signed balanced 3-CNF.
Reads authenticated U198 source from the j15marti/pnp repository checkout.
A separate independent verifier establishes U198 UNSAT, source D witness and both labels.
This is NOT the unrestricted SAT first leg or an FLMV indexed-TM simulation.
"""
import ast
from pathlib import Path
from collections import Counter
from itertools import product

ROOT = Path(__file__).resolve().parents[3]
U_FILE = ROOT / 'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
F9 = [[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]]
Y6 = [[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
H = [[1,2],[5,3],[6,8]] + F9[2:]
D_WITNESS = '010100010101000010000001110010101101010101010000100000001100111001011001010101001000000111001011000001000100001110101011000001111100100001000011101010000100001111000100001111000100010000111010100011000110001000'

def check(F,n,widths,monotone=False):
    if {abs(x) for c in F for x in c} != set(range(1,n+1)): return False
    if any(len(c) not in widths or len(set(map(abs,c))) != len(c) for c in F): return False
    if len({tuple(sorted(c)) for c in F}) != len(F):return False
    if monotone and any(any(x>0 for x in c) and any(x<0 for x in c) for c in F):return False
    count=Counter((abs(x),x>0) for c in F for x in c)
    return all(count[v,s]==2 for v in range(1,n+1) for s in (False,True))

def sat(F,bits):
    return all(any((bits[abs(x)-1]=='1')==(x>0) for x in c) for c in F)

def ren(c,o):
    return [(1 if x>0 else -1)*(abs(x)+o) for x in c]

def main():
    source=U_FILE.read_text()
    U=ast.literal_eval('\n'.join(x for x in source.splitlines() if not x.startswith('#')))
    assert check(U,198,(3,),True) and len(U)==264 and U[1]==[194,196,197]
    D=U[:1]+U[2:]
    assert sat(D,D_WITNESS) and all(D_WITNESS[x-1]=='0' for x in U[1])
    assert check(H,9,(2,3)) and check(F9,9,(3,),True) and check(Y6,6,(3,),True)
    count=sum(sat(H,''.join(str((q>>j)&1) for j in range(9))) for q in range(512))
    assert count==37
    FW=next(''.join(str((q>>j)&1) for j in range(9)) for q in range(512) if sat(F9,''.join(str((q>>j)&1) for j in range(9))))
    HW=next(''.join(str((q>>j)&1) for j in range(9)) for q in range(512) if sat(H,''.join(str((q>>j)&1) for j in range(9))))
    assert sat(Y6,'111000') and sat(F9,FW)
    out=[];bits=list(HW*12); nextv=12*9
    for c in H:
        begin=len(out)
        if len(c)==2:
            for g in range(4):
                for copy,port in enumerate((194,196,197)):
                    out.append(ren(c,(3*g+copy)*9)+[nextv+port])
                out += [ren(d,nextv) for d in D]
                bits.extend(D_WITNESS)
                nextv+=198
        else:
            for copy in range(12):out.append(ren(c,copy*9))
            for _ in range(130):
                out += [ren(d,nextv) for d in Y6]
                bits.extend('111000')
                nextv+=6
            out += [ren(d,nextv) for d in F9]
            bits.extend(FW)
            nextv+=9
        assert len(out)-begin==1064
    assert len(out)==13832 and nextv==10374 and len(bits)==nextv
    assert check(out,nextv,(3,)) and sat(out,''.join(bits))
    assert 3*1064-2*12==4*792 and 3*1064-3*12==4*789
    print({'status':'PASS','H_models':count,'output_vars':nextv,'output_clauses':len(out),
           'U198_UNSAT':'REQUIRES_INDEPENDENT_SOURCE_PROOF','P_vs_NP':'OPEN'})
if __name__=='__main__':main()
