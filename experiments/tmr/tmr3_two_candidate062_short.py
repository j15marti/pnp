#!/usr/bin/env python3
"""TMR-3/062 exact finite test of two block graphs and FAIL selection.
Scope: source semantics and movement-word labels, not native TM microcode.
"""
import json,random,sys
SEED=202611152254
R=random.Random(SEED)
checks=0

def ok(v):
 global checks
 checks+=1
 assert v,checks

def source(gs):
 n=len(gs);out=['1'*n+'0']
 for j,(op,a,b) in enumerate(gs):
  A='0'*n if op<2 else ''.join(('1' if k==a else '0') for k in range(n))
  B='0'*n if op<2 else ''.join(('1' if k==b else '0') for k in range(n))
  out.append(format(op,'02b')+A+B)
 return ''.join(out)

def parse(s):
 if not s or set(s)-{'0','1'}:return None
 n=len(s)-len(s.lstrip('1'))
 if not n or len(s)!=2*n*n+3*n+1:return None
 out=[];k=n+1
 for j in range(n):
  op=int(s[k:k+2],2);A=s[k+2:k+2+n];B=s[k+2+n:k+2+2*n];k+=2+2*n
  if op<2:
   if '1' in A+B:return None
   out.append((op,-1,-1));continue
  a=[i for i,z in enumerate(A) if z=='1'];b=[i for i,z in enumerate(B) if z=='1']
  if len(a)!=1 or len(b)!=1 or a[0]>=j or b[0]>=j:return None
  out.append((op,a[0],b[0]))
 return out

def value(gs):
 v=[]
 for op,a,b in gs:v.append(op if op<2 else (v[a]&v[b] if op==2 else v[a]|v[b]))
 return v[-1]

def motion(N,c,h,i,p=7,C=4,d=64):
 # p-1 is MARK; i=1..B, movement at boundary after block i.
 b=N+d;B=C*b*b+4
 assert 1<=i<=B
 return (1+c if h==p-1 and i==B else 1,c if h==p-1 and i==B-1 else 0)

def verify(s,c):
 g=parse(s);f=value(g) if g is not None else 0
 N=len(s);B=4*(N+64)**2+4
 return f if motion(N,f,6,B-1)[1]==motion(N,c,6,B-1)[1] else 'FAIL'

valid=bad=0
for n in range(1,21):
 for z in range(45):
  g=[]
  for j in range(n):
   if j==0 or R.randrange(4)==0:g.append((R.randrange(2),-1,-1))
   else:g.append((R.choice((2,3)),R.randrange(j),R.randrange(j)))
  s=source(g);f=value(g);N=len(s);b=N+64;B=4*b*b+4;t=4*b**3+3*b+1
  ok(parse(s)==g);ok(len(s)==2*n*n+3*n+1)
  ok((verify(s,0),verify(s,1))==((0,'FAIL') if f==0 else ('FAIL',1)))
  ok((B-1)*b+1==t);ok(t<=2**b)
  for i in (1,2,B-1,B):
   for h in (0,6):
    a=motion(N,0,h,i);c=motion(N,1,h,i)
    ok(a==c or (h==6 and i>=B-1))
  ok(motion(N,f,6,B)[0]==1+f)
  for wrong in (s+'0',s[:-1]):
   ok(parse(wrong) is None);ok(verify(wrong,0)==0 and verify(wrong,1)=='FAIL');bad+=1
  valid+=1
 for f in (0,1):
  s=source([(f,-1,-1)]*n)
  ok(verify(s,f)==f and verify(s,1-f)=='FAIL')
for s in ('','0','1','10','110','11x0','1000000'):
 ok(parse(s) is None);bad+=1
raw={'revision':'tmr3-two-candidate062-short-v1','seed':SEED,'valid_sources':valid,'malformed_controls':bad,'assertions':checks,'failures':0,'candidate_count':2,'status':'COMPUTATIONAL','limits':'No native TM compiler, no Cook-Mertz evaluator, asymptotics symbolic.'}
with open(sys.argv[1],'w') as f:json.dump(raw,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps(raw,sort_keys=True))
