#!/usr/bin/env python3
"""Decision-only short-circuit companion to exact complete-cover experiment.
Uses source-unit propagation and source-authenticated original-cube pruning.
"""
import pathlib,importlib.util,json,collections
here=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('arc261',here/'arc261_experiment.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cases={'W1_UNSAT':m.W1,'SWAP6_SAT':m.SWAP6,'W1_RENAMED_UNSAT':m.rename(m.W1,81),'SWAP6_RENAMED_SAT':m.rename(m.SWAP6,81),'XOR_K4_UNSAT':m.xor_k4(True),'XOR_K4_SAT':m.xor_k4(False)}

def run(F,n,limit,policy):
 C=collections.Counter();answers=[]
 def recursion(a):
  C['nodes']+=1
  rem,unit,conf=m.clause_scan(F,a,C)
  if conf is not None:
   assert all(abs(l) in a and a[abs(l)]!=int(l>0) for l in F[conf]);C['source_conflict_certificate']+=len(F[conf]);return False
  if unit is not None:
   j,l=unit;v=abs(l);b=int(l>0)
   assert v not in a
   wrong=dict(a);wrong[v]=1-b
   assert all(abs(z) in wrong and wrong[abs(z)]!=int(z>0) for z in F[j])
   C['unit_certificate']+=len(F[j]);C['units']+=1
   aa=dict(a);aa[v]=b;return recursion(aa)
  if not rem:
   aa={v:a.get(v,0) for v in range(1,n+1)}
   assert all(any(aa[abs(l)]==int(l>0) for l in c) for c in F)
   C['source_witness_literal_tests']+=sum(len(c) for c in F)
   answers.append(aa);return True
  if len(rem)<=limit:
   C['child_emission_reads']+=sum(len(c) for c in F)+len(F)
   R=m.residual(F,a);C['child_bits_written']+=m.enc_bits(R,n);C['child_calls']+=1
   yes,res=m.dpll(R,n)
   C['guest_events']+=res['total_events'];C['guest_nodes']+=res['nodes']
   if yes:
    aa=dict(res['witness']);aa.update(a)
    assert all(any(aa[abs(l)]==int(l>0) for l in c) for c in F)
    C['source_witness_literal_tests']+=sum(len(c) for c in F)
    answers.append(aa)
   else:C['child_unsat_refutations']+=1
   return yes
  v=m.choose(F,rem,a,policy,C)
  for b in (0,1):
   C['branches']+=1
   aa=dict(a);aa[v]=b
   if recursion(aa):return True
  return False
 yes=recursion({});return {'answer':'SAT' if yes else 'UNSAT','events':sum(C.values()),'stats':dict(C),'witness':answers[0] if answers else None}

def main():
 result={}
 for name,F in cases.items():
  n=max(abs(l) for c in F for l in c);truth=m.models(F,n)[0]
  result[name]={'models':truth,'strategies':{}}
  for cutoff in (4,8,12):
   for policy in ('first','max','min'):
    ans=run(F,n,cutoff,policy)
    assert (ans['answer']=='SAT')==(truth>0)
    result[name]['strategies'][str(cutoff)+':'+policy]=ans
 (here/'decision.json').write_text(json.dumps(result,indent=2,sort_keys=True))
 for case,v in result.items():
  for pol in ('first','max','min'):
   a=v['strategies']['8:'+pol]
   print(case,pol,a['answer'],'work',a['events'],'nodes',a['stats'].get('nodes'),'child_calls',a['stats'].get('child_calls',0))
if __name__=='__main__':main()
