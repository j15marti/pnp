#!/usr/bin/env python3
"""Exact GF(4), oracle and finite streaming-controller controls. Native CPython.
Run: python tmr3_gf4_extension023.py --output raw.json
This is NOT an arbitrary SAT machine compiler.
"""
import argparse,hashlib,json
from pathlib import Path

def mul(x,y):
 a,b=x&1,(x>>1)&1;c,d=y&1,(y>>1)&1
 return (a*c^b*d)|((a*d^b*c^b*d)<<1)

def canonical_eval(fn,n,z):
 s=0
 for a in range(1<<n):
  if not fn(a):continue
  w=1
  for j,v in enumerate(z):w=mul(w,v if a>>j&1 else v^1)
  s^=w
 return s

def or_extension(z):
 p=1
 for v in z:p=mul(p,v^1)
 return p^1

def sat(f,a):
 return all(any(((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in f)

def run_machine(bits):
 # One local read-only input head, finite GF4/product control, charged output.
 tape='^'+bits+'$';head=0;steps=0
 assert tape[head]=='^';head+=1;steps+=1
 if head==len(tape)-1:return ('MALFORMED',None,steps+2,0)
 mode=tape[head];head+=1;steps+=1
 if mode not in '01':return ('MALFORMED',None,steps+1,0)
 acc=0 if mode=='0' else 1;pending=None
 while tape[head]!='$':
  bit=int(tape[head]);head+=1;steps+=1
  if mode=='0':acc|=bit
  elif pending is None:pending=bit
  else:
   acc=mul(acc,((pending<<1)|bit)^1);pending=None
 steps+=1
 if mode=='1' and pending is not None:return ('MALFORMED',None,steps+1,0)
 if mode=='0':out=str(acc)
 else:
  v=acc^1;out=f'{v>>1&1}{v&1}'
 steps+=len(out)+1
 return ('OK',out,steps,len(out))

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);o=p.parse_args()
 for x in range(4):
  assert mul(x,0)==0 and mul(x,1)==x
  for y in range(4):
   assert mul(x,y)==mul(y,x)
   for z in range(4):assert mul(mul(x,y),z)==mul(x,mul(y,z))
 oracle=0;tables=0;curve=[]
 for n in range(1,10):
  z=[2]*n;weights=[]
  for a in range(1<<n):
   w=canonical_eval(lambda b,aa=a:int(b==aa),n,z)
   assert w!=0
   weights.append(w);oracle+=1
  v=canonical_eval(lambda a:int(a!=0),n,z)
  assert v==or_extension(z)
  if n<=3:
   for truth in range(1<<(1<<n)):
    f=lambda a,k=truth:(k>>a)&1
    actual=canonical_eval(f,n,z);independent=0
    for a,w in enumerate(weights):
     if f(a):independent^=w
    assert actual==independent
    tables+=1
  curve.append({'n':n,'oracle_calls_necessary':1<<n,'OR_ANF_terms':(1<<n)-1,
                'factorized_multiplications':n,'extension_at_alpha':v})
 runs=ok=malformed=max_space=max_slack=0
 for L in range(14):
  for j in range(1<<L):
   bits=format(j,f'0{L}b') if L else ''
   label,value,t,s=run_machine(bits);runs+=1
   if label=='MALFORMED':
    assert L==0 or (bits[0]=='1' and (L-1)%2==1)
    malformed+=1
   else:
    ok+=1
    if bits[0]=='0':expected=str(int('1' in bits[1:]))
    else:
     values=[(int(bits[i])<<1)|int(bits[i+1]) for i in range(1,L,2)]
     v=or_extension(values);expected=f'{v>>1&1}{v&1}'
    assert value==expected
   assert t<=L+6 and s<=2
   max_space=max(max_space,s);max_slack=max(max_slack,t-L)
 controls=[
 ('Horn',3,[(1,),(-1,2),(-2,3)]),
 ('HornUNSAT',3,[(1,),(-1,)]),
 ('twoSAT',3,[(1,2),(-1,3),(-2,-3)]),
 ('XOR3',3,[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)]),
 ('duplicate',3,[(1,2,3)]*12),
 ('shared',3,[(1,2,3),(-1,2,3)]),
 ('product',6,[(1,2,3),(-1,-2,-3),(4,5,6),(-4,-5,-6)]),
 ('renamed',4,[(4,2,3),(-4,2,3)])]
 for r in (1,2,3,4):
  cube=[tuple(-j-1 if s>>j&1 else j+1 for j in range(3)) for s in range(8) for _ in range(r)]
  near=cube[:]
  for j in range(r):
   row=list(near[j]);row[0]*=-1;near[j]=tuple(row)
  controls.extend([(f'U_{r}',3,cube),(f'nearest_{r}',3,near)])
 records=[]
 for name,n,f in controls:
  truth=lambda a,formula=f:int(sat(formula,a))
  v=canonical_eval(truth,n,[2]*n)
  check=0;models=0
  for a in range(1<<n):
   if truth(a):
    models+=1;w=1
    for j in range(n):w=mul(w,2 if a>>j&1 else 3)
    check^=w
  assert v==check
  assert (models==0)==(name.startswith('U_') or name=='HornUNSAT')
  records.append({'name':name,'variables':n,'clauses':len(f),'models':models,'canonical_alpha':v})
 sharing=[{'depth':h,'naive_unfolded_occurrences':(1<<(h+1))-1,'unique_DAG_nodes':h+1}
          for h in range(21)]
 for item in sharing:assert item['naive_unfolded_occurrences']>=item['unique_DAG_nodes']
 raw={'status':'COMPUTATIONAL','native_python':True,'physical_TM_binary_compiler':False,
      'model':'restricted one-head local streaming controller, GF4, generic Boolean value oracle',
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'field_tables':'exhaustive GF4 triples',
      'oracle_spike_checks':oracle,'all_functions_n_le_3':tables,
      'curve':curve,'machine_runs':runs,'machine_ok':ok,'machine_malformed':malformed,
      'max_visited_output_cells':max_space,'max_T_minus_L':max_slack,
      'cnf_controls':records,'sharing_controls':sharing,'failed_assertions':0}
 Path(o.output).write_text(json.dumps(raw,sort_keys=True,indent=2)+'\n')
 print(json.dumps({k:raw[k] for k in ['oracle_spike_checks','all_functions_n_le_3','machine_runs',
                                      'machine_ok','machine_malformed','max_visited_output_cells',
                                      'max_T_minus_L','failed_assertions']},indent=2))
if __name__=='__main__':main()
