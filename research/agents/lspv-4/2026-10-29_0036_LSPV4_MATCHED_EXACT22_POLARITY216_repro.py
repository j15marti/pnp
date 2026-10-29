#!/usr/bin/env python3
"""LSPV-4 matched SAT/UNSAT monotone exact-(2,2)-3CNF control.
Primary source: J. Docker, Monotone 3-Sat-(2,2) is NP-complete,
arXiv:1912.08032 (2019), Appendices A-C.
Finite cores and the outer skeleton are checked exhaustively.
The 198-variable UNSAT result uses the explicit sound composition argument.
No general SAT lower bound is asserted.
"""
from collections import Counter
import hashlib
import json

M = [
 [1,2],[-2,-3],[-2,-4],[-3,-5,-6],[-4,-5,-6],
 [5,7,8],[6,7,8],[-7,-18,-19],[-7,-20,-21],
 [-8,-18,-19],[-8,-20,-21],[3,9,10],[3,11,12],
 [4,13,14],[4,15,16],[9,12,15],[10,13,17],
 [11,16,17],[-9,-13,-16],[-9,-14,-17],
 [-10,-11,-14],[-10,-12,-16],[-11,-13,-15],
 [-12,-15,-17],[2,24,32],[18,23,25],
 [18,28,29],[19,23,25],[19,28,29],
 [20,22,26],[20,30,31],[21,22,31],
 [21,26,27],[24,27,30],[-1,-22,-23],
 [-1,-24,-25],[-22,-25,-32],[-23,-24,-26],
 [-26,-28,-30],[-27,-28,-31],[-27,-29,-31],
 [-29,-30,-32]
]
Y = [
 [1,2],[3,4],[5,6],[7,8],[1,4,7],[2,5,9],[3,8,9],
 [-1,-5,-8],[-1,-6,-9],[-2,-3,-6],[-2,-4,-8],
 [-3,-5,-7],[-4,-7,-9]
]
Z = [
 [-1,-2],[-3,-4],[-5,-6],[-7,-8],[7,15],
 [1,6,8],[1,11,12],[2,6,8],[2,11,12],
 [3,5,9],[3,13,14],[4,5,14],[4,9,10],[7,10,13],
 [-5,-8,-15],[-6,-7,-9],[-9,-11,-13],
 [-10,-11,-14],[-10,-12,-14],[-12,-13,-15]
]
EXT = [
 [197,-194,-194],[196,-195,-198],[193,-195,-197],
 [-197,195,195],[-196,193,194],[-193,198,198]
]
OUTER = [[-193,-196,-198],[194,196,197]]

def satisfied(clause, mask):
    return any(((mask >> (abs(v)-1)) & 1)==(v>0) for v in clause)

def exhaustive_unsat(clauses, n):
    return all(not all(satisfied(c, bits) for c in clauses)
               for bits in range(1<<n))

def norm(c):
    return tuple(sorted(c))

def check_cores():
    assert len(M)==42 and len(Y)==13 and len(Z)==20
    assert exhaustive_unsat(Y,9) and exhaustive_unsat(Z,15)
    G = M[11:24]
    derivedY=[]
    for c in G:
        d=[v for v in c if v not in (3,4)]
        derivedY.append([abs(v)-8 if v>0 else -(abs(v)-8) for v in d])
    assert Counter(map(norm,derivedY))==Counter(map(norm,Y))
    W=M[6:11]+M[24:]
    derivedZ=[[-18,-19],[-20,-21],[-22,-23],[-24,-25],[24,32]]
    derivedZ += [c for c in W if all(abs(v)>=18 for v in c)]
    derivedZ=[[abs(v)-17 if v>0 else -(abs(v)-17) for v in c]
              for c in derivedZ]
    assert Counter(map(norm,derivedZ))==Counter(map(norm,Z))
    skeleton=OUTER+EXT
    outer6=[[abs(v)-192 if v>0 else -(abs(v)-192)
             for v in c] for c in skeleton]
    assert exhaustive_unsat(outer6,6)
    return 512+32768+64

def unsat_source():
    clauses=[c[:] for c in OUTER]
    for i in range(6):
        flip=-1 if i>=3 else 1
        for j, c in enumerate(M):
            d=[flip*(abs(v)+32*i)*(1 if v>0 else -1) for v in c]
            if j<3: d.append(EXT[i][j])
            clauses.append(d)
    for pos in [1,5,6,14,32]:
        clauses.append([pos,pos+32,pos+64])
        clauses.append([-(pos+96),-(pos+128),-(pos+160)])
    return clauses

def sat_source(r=66):
    assert r>=5
    clauses=[]
    for j in range(r):
        def idx(d,k):
            return 3*((j+d)%r)+k+1
        a,b,c=idx(0,0),idx(0,1),idx(0,2)
        clauses += [[a,b,c], [b,c,idx(1,0)],
                    [-a,-b,-idx(1,2)],
                    [-a,-idx(1,1),-idx(2,2)]]
    return clauses

def verify_structure(clauses, n=198, m=264):
    assert len(clauses)==m
    assert len({norm(c) for c in clauses})==m
    counts=Counter(v for c in clauses for v in c)
    adj=[set() for _ in range(n+1)]
    for c in clauses:
        assert len(c)==3 and len(set(map(abs,c)))==3
        assert all(v>0 for v in c) or all(v<0 for v in c)
        assert all(1<=abs(v)<=n for v in c)
        for a in map(abs,c):
            adj[a].update(abs(v) for v in c if abs(v)!=a)
    assert all(counts[v]==counts[-v]==2 for v in range(1,n+1))
    seen={1}
    frontier=[1]
    while frontier:
        u=frontier.pop()
        for v in adj[u]-seen:
            seen.add(v); frontier.append(v)
    assert len(seen)==n

def encoded_bits(clauses,n=198):
    w=n.bit_length()
    return (f"{n:032b}{len(clauses):032b}" +
            "".join(("1" if v<0 else "0")+f"{abs(v):0{w}b}"
                    for c in clauses for v in c))

def run():
    checked=check_cores()
    neg=unsat_source()
    pos=sat_source()
    verify_structure(neg)
    verify_structure(pos)
    mask=sum((1<<j) for j in range(198) if j%3!=2)
    assert all(satisfied(c,mask) for c in pos)
    a,b=encoded_bits(neg),encoded_bits(pos)
    assert len(a)==len(b)==7192
    return dict(status="PASS",variables=198,clauses=264,
                exact_22_connected_monotone_proper=True,
                verified_core_and_skeleton_assignments=checked,
                matched_canonical_bits_each=len(a),
                sat_witness="110"*66,
                unsat_encoding_sha256=hashlib.sha256(a.encode()).hexdigest(),
                sat_encoding_sha256=hashlib.sha256(b.encode()).hexdigest(),
                note="UNSAT of 198 source follows by six copies of M plus outer skeleton, not full enumeration")

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
