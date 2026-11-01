#!/usr/bin/env python3
"""No-import verifier for REFEREE271's symbolic word/matrix theorem."""
import collections,itertools,json,sys

M={"2":((0,2),(0,0)),"8":((0,0),(0,10)),"B":((3,9),(0,3)),"C":((0,0),(8,18))}
S=("2","8","B","8","C","B");U=("2","8","C","B","8","B")

def mm(A,B):return tuple(tuple(sum(A[i][h]*B[h][j] for h in (0,1)) for j in (0,1)) for i in (0,1))
def prod(w):
 A=((1,0),(0,1))
 for x in w:A=mm(A,M[x])
 return A
def inflate(w,L):return tuple(y for x in w for y in (("B",)*L+(x,)))
def deck(w,k):return collections.Counter(tuple(w[(i+j)%len(w)] for j in range(k)) for i in range(len(w)))

def main(path):
 d=json.load(open(path));checks=0
 assert d["P_vs_NP"]=="OPEN";checks+=1
 assert d["base_words"]["SAT"]==list(S) and d["base_words"]["UNSAT"]==list(U);checks+=2
 # Independent exhaustive symbolic checks extend beyond producer's k=64.
 for k in range(1,97):
  L=max(0,k-2);a=inflate(S,L);b=inflate(U,L)
  assert collections.Counter(a)==collections.Counter(b);checks+=1
  for j in range(1,k+1):assert deck(a,j)==deck(b,j);checks+=1
  A,B=prod(a),prod(b)
  assert A[0][0]+A[1][1]>0 and B[0][0]+B[1][1]==0;checks+=2
 # The base cyclic 1- and 2-decks are equal but words are not rotations.
 assert deck(S,1)==deck(U,1) and deck(S,2)==deck(U,2);checks+=2
 assert all(tuple(S[i:]+S[:i])!=U for i in range(len(S)));checks+=1
 # Independent exact A/B disjoint-region hitting-set check through t=9.
 for t in range(1,10):
  R=[{2*i,2*i+1} for i in range(t)]
  assert not any(all(set(c)&r for r in R) for q in range(t) for c in itertools.combinations(range(2*t),q));checks+=1
  assert all({2*i for i in range(t)}&r for r in R);checks+=1
 assert d["controls"]["Y6_models"]==20 and d["controls"]["F9_models"]==70;checks+=2
 assert d["controls"]["F9_A_models"]==1 and d["controls"]["F9_B_models"]==0;checks+=2
 assert d["controls"]["F15_SAT_models"]==2 and d["controls"]["F15_UNSAT_models"]==0;checks+=2
 print(json.dumps({"status":"PASS","checks":checks,"max_k":96,"P_vs_NP":"OPEN"},indent=2))

if __name__=="__main__":main(sys.argv[1])
