#!/usr/bin/env python3
from itertools import product
def y(row,mode):
 a,b,c,d=row
 return not (a or b) if mode=='P' else (c or d)
def cnf(modes,sign):
 base=[];pairs=[]
 for i,mode in enumerate(modes):
  if sign=='+':
   if mode=='P':pairs.append([[(i,0,False)],[(i,1,False)]])
   else:base.extend([(i,2,True),(i,3,True)])
  else:
   if mode=='S':pairs.append([[(i,2,False)],[(i,3,False)]])
   else:base.extend([(i,0,True),(i,1,True)])
 return [base+sum(x,[]) for x in product(*pairs)]
def check(t):
 n=0
 for modes in product('PS',repeat=t):
  clauses={sign:cnf(modes,sign) for sign in '+-'}
  assert len(clauses['+'])==2**modes.count('P')
  assert len(clauses['-'])==2**modes.count('S')
  for flat in product((False,True),repeat=4*t):
   rows=[flat[4*i:4*i+4] for i in range(t)]
   for row,mode in zip(rows,modes):
    a,b,c,d=row;v=y(row,mode)
    assert ((a or b or v) and ((not v) or c or d))==(a or b or c or d)
   for sign in '+-':
    expected=any(y(row,mode) if sign=='+' else not y(row,mode) for row,mode in zip(rows,modes))
    actual=all(any(row[i][j]==positive for i,j,positive in clause for row in [rows]) for clause in clauses[sign])
    assert expected==actual
    n+=1
 return n
if __name__=='__main__':
 for t in (1,2,3,4):
  print(t,check(t))
