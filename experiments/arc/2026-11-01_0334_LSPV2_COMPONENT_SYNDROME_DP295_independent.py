#!/usr/bin/env python3
"""Independent source-clause and syndrome-table verification. No producer import.
Checks every projected row using original clause parity and row-XOR provenance,
all small source labels, all reported DP state counts, overlap exclusions,
global clause S/U coherence, and 2,187 restricted cube classifications.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
import json,math,ast,gzip,hashlib
R=Path(__file__).resolve().parent
D=json.loads((R/'results295.json').read_text())
checks=Counter()
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
POS15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
NEG15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=POS15+tuple(tuple(-v for v in c) for c in NEG15)
E5=((1,2),(2,3),(3,4),(4,5),(1,5))
C5=tuple(e for e in combinations(range(1,6),2) if e not in E5)
K5=tuple((u,v,6+i) for i,(u,v) in enumerate(E5))+tuple((-u,-v,-11-i) for i,(u,v) in enumerate(C5))+tuple((6+i,11+i,11+(i+1)%5) for i in range(5))+tuple((-(11+i),-(6+i),-(6+(i+1)%5)) for i in range(5))
P9={8:0,3:0,7:0,6:0,1:1,5:1}
PU={v:b for v,b in zip(range(7,16),(0,0,0,0,1,1,1,1,0))}
PS={v:b for v,b in zip(range(7,16),(1,0,0,0,1,1,1,1,0))}
P5={**{v:0 for v in range(6,11)},**{v:1 for v in range(11,16)},6:1,15:0}
U=tuple(map(tuple,ast.literal_eval(''.join(l for l in (R/'U198.txt').read_text().splitlines() if not l.startswith('#')))))
V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(map(tuple,V))

def ck(x,message):
 checks['assertions']+=1
 if not x:raise AssertionError(message)

def sat(F,a):return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def truth(F,a):return [sum(a[abs(l)]==int(l>0) for l in c) for c in F]

def models(F,p):
 n=max(abs(l) for c in F for l in c)
 free=[v for v in range(1,n+1) if v not in p]
 for bits in product((0,1),repeat=len(free)):
  a={**p,**dict(zip(free,bits))}
  if sat(F,a):yield a

def grammar(F):
 n=max(abs(x) for c in F for x in c);count=Counter(l for c in F for l in c)
 ck(3*len(F)==4*n,'source length mismatch')
 ck(len(set(tuple(sorted(c)) for c in F))==len(F),'duplicate')
 for c in F:ck(len(c)==3 and len(set(map(abs,c)))==3 and (all(l>0 for l in c) or all(l<0 for l in c)),'source grammar')
 for v in range(1,n+1):ck(count[v]==count[-v]==2,'occurrence degree')

def gate(F,p):
 f=[x for x in range(1,max(abs(l) for c in F for l in c)+1) if x not in p]
 covered=[];uncovered=[];edge={};occ=Counter()
 for j,c in enumerate(F):
  if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):
   covered.append(j)
   for l in c:
    if abs(l) not in p:occ[abs(l),l>0]+=1
  else:
   remaining=[l for l in c if abs(l) not in p]
   if not remaining:return {'status':'EMPTY'}
   uncovered.append(j)
   if len(remaining)==2:edge[j]=tuple(abs(l) for l in remaining)
 tri=[]
 for cyc in combinations(sorted(edge),3):
  deg=Counter(x for j in cyc for x in edge[j])
  if len(deg)==3 and all(x==2 for x in deg.values()):tri.append(cyc)
 used=set();cs=[]
 for cyc in tri:
  if not used.intersection(cyc):cs.append(cyc);used.update(cyc)
 eta=sum(min(occ[x,True],occ[x,False]) for x in f)
 pref={v:int(occ[v,False]>occ[v,True]) for v in f if occ[v,True]!=occ[v,False]}
 return {'status':'GATE','cycles':cs,'uncovered':uncovered,'free':f,'delta':2*len(f)-len(uncovered)-eta-len(cs),'pref':pref,'edge':edge}

def template(F,p,cycle,selected):
 verts=sorted(set(x for j in cycle for x in gate_edge(F,p,j)))
 candidates=[]
 for bits in product((0,1),repeat=len(verts)):
  a=dict(zip(verts,bits))
  hits={j:sum(a[abs(l)]==int(l>0) for l in F[j] if abs(l) not in p) for j in cycle}
  if hits[selected]==2 and all(hits[j]==1 for j in cycle if j!=selected):candidates.append(a)
 ck(len(candidates)==1,'unique odd cycle template')
 return candidates[0]

def gate_edge(F,p,j):return [abs(l) for l in F[j] if abs(l) not in p]

def group_check(F,p,case):
 g=gate(F,p)
 ck(case['delta']==g.get('delta'),'delta source authentication')
 ck(case['nu']==len(g.get('cycles',[])),'cycle count source authentication')
 if case['gate'] in ('UNRESOLVED','UNSAT_GAP','UNSAT_EMPTY'):
  return
 cmask=0
 for cycle in g['cycles']:
  for j in cycle:
   for v in g['edge'][j]:cmask|=1<<(v-1)
 wmask=sum(1<<(v-1) for v in g['free'])&~cmask
 cycleids={j for cycle in g['cycles'] for j in cycle}
 original={}
 for j in g['uncovered']:
  if j in cycleids:continue
  rest=[l for l in F[j] if abs(l) not in p]
  original[('source_parity',j)]=(sum(1<<(abs(l)-1) for l in rest),int(rest[0]>0) if rest[0]>0 else 1^(len(rest)&1))
 for v,b in g['pref'].items():original[('source_spill_preference',v)]=(1<<(v-1),b)
 projected=case.get('projected_rows',[])
 for row in projected:
  comb=0;rhs=0
  for item in row['source_row_xor']:
   src=tuple(item)
   ck(src in original,'provenance exists in source')
   m,b=original[src];comb^=m;rhs^=b
  ck(comb&wmask==0,'row-XOR eliminated all W coefficients')
  ck(comb&cmask==row['mask'] and rhs==row['rhs'],'row-XOR proof equality')
 eqs=[(r['mask'],r['rhs']) for r in projected]
 for group in case.get('groups',[]):
  cyc_idx=group['cycles'];rows=group['rows']
  target=sum(eqs[j][1]<<t for t,j in enumerate(rows))
  ck(target==group['target'],'target syndrome')
  if group['method']=='syndrome_dp':
   table={0:1};transitions=0
   for ci in cyc_idx:
    c=g['cycles'][ci];new=Counter()
    for chosen in c:
     z=template(F,p,c,chosen)
     ones=sum(1<<(v-1) for v,b in z.items() if b)
     sig=sum(((eqs[j][0]&ones).bit_count()%2)<<t for t,j in enumerate(rows))
     for syndrome,ways in table.items():new[syndrome^sig]+=ways;transitions+=1
    table=dict(new)
   ck({int(k):v for k,v in group['last_state_counts'].items()}==table,'independent DP table')
   ck(group['compatible_options']==table.get(target,0),'independent target count')
   ck(group['transitions']==transitions,'independent transition count')
  else:
   solutions=0;conflict=0;attempts=0
   for choice in product(*(g['cycles'][j] for j in cyc_idx)):
    attempts+=1;z={};bad=False
    for ci,selected in zip(cyc_idx,choice):
     for v,b in template(F,p,g['cycles'][ci],selected).items():
      if v in z and z[v]!=b:bad=True;break
      z[v]=b
     if bad:break
    if bad:conflict+=1;continue
    ones=sum(1<<(v-1) for v,b in z.items() if b)
    if all(((eqs[j][0]&ones).bit_count()%2)==eqs[j][1] for j in rows):solutions+=1
   ck(group['compatible_options']==solutions,'overlap-enumerated model count')
   ck(group['attempts']==attempts,'overlap attempts')
  checks['group_certificates']+=1

def verify_original_controls():
 summary=json.loads((R/'signed_controls_summary295.json').read_text())
 trace=R/'signed_controls295.json.gz'
 ck(hashlib.sha256(trace.read_bytes()).hexdigest()==summary['sha256'],'gzip integrity')
 source={'F9':F9,'Y6':Y6,'F15':F15,'U198':U,'V198':V}
 with gzip.open(trace,'rt') as z:
  for line in z:
   x=json.loads(line);F=source[x['source']];grammar(F)
   ck(len(x['clauses'])==len(F),'full clause extreme coverage')
   for j,c in enumerate(F):
    targets=x['clauses'][j]
    ck(targets['signed_literals']==list(c),'source signed literal IDs')
    for lit,pair in zip(c,targets['S_occurrence_targets']):
     ck(pair==[abs(lit),int(lit>0)],'S signed local target')
    ck(targets['inverted_S_equals_U']==targets['U_occurrence_targets'],'complement S')
   for j,k,ss,su,us,uu in x['pair_extreme']:
    same=any(l in F[k] for l in F[j]);opp=any(-l in F[k] for l in F[j])
    ck([ss,su,us,uu]==[int(not opp),int(not same),int(not same),int(not opp)],'SS/SU/US/UU')
   n=x['n'];a={v:0 for v in range(1,n+1)}
   t=truth(F,a)
   ck([t.count(v) for v in range(4)]==x['zero_hist'],'original 0 endpoint')
   for v in range(1,n+1):
    before=t[:];a[v]=1;t=truth(F,a)
    touched=[i for i,(u,w) in enumerate(zip(before,t)) if u!=w]
    ck(len(touched)==4,'source variable occurrence count')
    ck(all(abs(before[j]-t[j])==1 for j in touched),'coherent flip')
   ck([t.count(v) for v in range(4)]==x['one_hist'],'original 1 endpoint')
   ck(x['full_forward_gray_logic_xor_total']==5*n,'full Gray logical XOR, offline only')
   checks['original_pairs']+=len(x['pair_extreme'])

def main():
 verify_original_controls()
 cases=[('F9_UNSAT_CUBE',F9,P9),('Y6_ROOT',Y6,{}),('F15_UNSAT',F15,PU),('F15_SAT',F15,PS),('K5_SAT_OVERLAP',K5,P5),('U198_UNSAT_ROOT',U,{}),('V198_SAT_ROOT',V,{})]
 report={'status':'PASS','P_vs_NP':'OPEN','cases':{},'all_source_labels':{},'exhaustive':{}}
 for name,F,p in cases:
  grammar(F);raw=D['cases'][name]
  group_check(F,p,raw)
  actual=sum(1 for _ in models(F,p)) if len(F)<25 else None
  if actual is not None:
   ck(actual==raw['model_count'] if raw['gate']=='SAT' else (actual==0 if raw['gate'].startswith('UNSAT') else True),'original-source exact SAT decision/count')
   if raw['witness']:
    witness={i+1:b for i,b in enumerate(raw['witness'])}
    ck(all(witness[v]==b for v,b in p.items()) and sat(F,witness),'full source witness')
  report['cases'][name]={'gate':raw['gate'],'model_count':actual,'cycles':raw['nu']}
 for name,F,roots in [('Y6',Y6,[{}]),('F15',F15,[PU,PS])]:
  histogram=Counter();total=0
  for root in roots:
   free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in root]
   for states in product((-1,0,1),repeat=len(free)):
    pin={**root,**{v:b for v,b in zip(free,states) if b!=-1}}
    g=gate(F,pin);actual=list(models(F,pin))
    if g['status']=='EMPTY':histogram['UNSAT_EMPTY']+=1;ck(not actual,'empty contradiction')
    elif g['delta']<0:histogram['UNSAT_GAP']+=1;ck(not actual,'negative gap contradiction')
    elif g['delta']!=0:histogram['UNRESOLVED']+=1
    else:
     histogram['SAT' if actual else 'UNSAT_DELTA_ZERO']+=1
     for a in actual:
      for c in g['cycles']:
       over=[j for j in c if sum(a[abs(l)]==int(l>0) for l in F[j])==2]
       ck(len(over)==1,'unique original-source cycle overfull edge')
      for j in g['uncovered']:
       if all(j not in cyc for cyc in g['cycles']):
        ck(sum(a[abs(l)]==int(l>0) for l in F[j])==1,'outside original clause exact one')
     total+=len(actual)
  report['exhaustive'][name]={'cubes':sum(histogram.values()),'histogram':dict(histogram),'saturated_sat_extensions':total}
  raw=D['exhaustive'][name]
  ck(report['exhaustive'][name]['cubes']==(729 if name=='Y6' else 1458),'all source cubes')
  for key in ('SAT','UNSAT_GAP','UNSAT_EMPTY','UNRESOLVED'):
   ck(histogram[key]==raw.get(key,0),'source status histogram')
  ck(histogram['UNSAT_DELTA_ZERO']==raw.get('UNSAT_PROJECTION',0)+raw.get('UNSAT_SYNDROME_EXHAUSTED',0),'complete zero-budget refutations')
  ck(total==raw['sat_extensions'],'saturated total exact extension count')
 for item in D['product_controls']:
  ck(item['count']==2**item['copies'] and item['nu']==2*item['copies'],'disjoint factor counts')
 report['assertions']=checks['assertions'];report['group_certificates']=checks['group_certificates'];report['original_pair_checks']=checks['original_pairs']
 (R/'independent295.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()