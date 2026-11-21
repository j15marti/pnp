"""Exact zero-atom tests, not a count lower bound. Python 3, no dependencies."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib,json

def colorings(v,edges):
    return sum(all(a[u]!=a[w] for u,w in edges) for a in product(range(3),repeat=v))

def main():
    sat=[(u,w) for u in range(2) for w in range(2,5)]
    unsat=list(combinations(range(4),2))
    assert colorings(5,sat)==30 and colorings(5,unsat)==0
    rows=[]
    for r in range(8):
        v=5+r;e=6;k=v
        E=10+9*v+12*e;n=55+48*v+63*e;m=65+58*v+77*e
        N=n+2+2*((m+1).bit_length()-1)+3*m*n.bit_length()
        mul=10*(1<<E)
        fake=[mul*6*t for t in range(1<<k)]
        assert len(set(fake))==1<<k and all(0<=z<=5**n and z%mul==0 for z in fake)
        pzero=F(sum(z==0 for z in fake),len(fake))
        adv=F(1,2)-pzero
        assert adv==F(1,2)-F(1,1<<k)
        rows.append(dict(r=r,v=v,e=e,k=k,E=E,n=n,m=m,N=N,
                         true_counts=[mul*30*3**r,0],fake_support_size=len(fake),
                         fake_zero_probability=str(pzero),zero_advantage=str(adv),
                         zero_gate_budget=3*N,full_multiplier=mul))
    # Exhaustively check the universal guessing inequality for two input values,
    # three output symbols and conditional probabilities on the quarter grid.
    triples=[(a,b,4-a-b) for a in range(5) for b in range(5-a)]
    checks=0
    for p in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
        for a,b in product(triples,repeat=2):
            guess=p*F(max(a),4)+(1-p)*F(max(b),4)
            atom=p*F(a[0],4)+(1-p)*F(b[0],4)
            assert guess>=atom
            # p is also assigned as the true zero mass for this finite control.
            assert abs(p-atom)>=max(F(0),p-guess)
            checks+=1
    print(json.dumps(dict(lemma='T5-ZERO-ATOM-MINENTROPY1',
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        source_commit='c5d8802644abe2caef15ef67153fa76ab8da1152',
        mode='exact fractions; exhaustive stated supports; no randomness',
        base_graph_counts=[30,0],rows=rows,probability_table_checks=checks,
        status='COMPUTATIONAL PASS; no expanded T5 assignment enumeration'),separators=(',',':')))

if __name__=='__main__':main()
