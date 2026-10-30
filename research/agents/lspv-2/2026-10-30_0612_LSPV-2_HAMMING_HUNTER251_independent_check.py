#!/usr/bin/env python3
"""Independent finite checker for the Hamming-Hunter251 fixed source and certificate.
Does NOT call the report's binomial/counting/Hunter functions.
"""
import itertools,json,collections,sys

def sat(c,a):return any(bool(a&(1<<(abs(z)-1)))==(z>0) for z in c)
def false(c,a):return not sat(c,a)
def Fof(x):return [tuple(v['original_literals']) for v in x['local_targets']]
def check(path):
 raw=json.load(open(path));cases=raw['cases'];count=collections.Counter()
 for x in cases:
  F=Fof(x);n=x['n'];m=len(F)
  if x['strict22']:
   z=collections.Counter(v for c in F for v in c)
   assert all(z[i]==z[-i]==2 for i in range(1,n+1));assert len(set(tuple(sorted(c)) for c in F))==m
  # Clause-local S/U and inverted occurrence targets.
  for c,row in zip(F,x['local_targets']):
   for z,occ in zip(c,row['occurrences']):
    assert occ['literal']==z
    assert occ['S_local']==(z>0) and occ['U_local']==(z<0)
    assert occ['invert_S_is_U']==(z<0) and occ['invert_U_is_S']==(z>0)
    count['signed_occurrences']+=1
  # Pair-target compatibility is checked against entire coherent support universe.
  for e in x['pair_matrix']:
   c1=F[e['j']-1];c2=F[e['k']-1];V=sorted({abs(z) for z in c1+c2})
   modes=set()
   for bits in itertools.product((0,1),repeat=len(V)):
    a=dict(zip(V,bits));t1=sum(a[abs(z)]==(z>0) for z in c1);t2=sum(a[abs(z)]==(z>0) for z in c2)
    if t1 in (0,len(c1)) and t2 in (0,len(c2)):
     modes.add(('S' if t1 else 'U')+('S' if t2 else 'U'))
    count['extreme_pair_support_checks']+=1
   assert modes=={k for k,v in e['SS_SU_US_UU'].items() if v}
  # Actual global complement statuses.
  for st in x['flip_trail']+x['endpoints']:
   a=st['mask'];literal_t=[sum(bool(a&(1<<(abs(z)-1)))==(z>0) for z in c) for c in F]
   assert literal_t==st['t'] and [literal_t.count(t) for t in range(4)]==st['N']
   inv=a^((1<<n)-1)
   assert all(literal_t[j]+sum(bool(inv&(1<<(abs(z)-1)))==(z>0) for z in c)==len(c) for j,c in enumerate(F))
   count['coherent_full_states']+=1
  # Every source-parent resolvent refuted on falsifying cube; no SAT completion.
  for p in x['resolvent_proofs']:
   a,b=(F[j-1] for j in p['parents']);v=p['pivot'];assert v in a and -v in b
   R=set(a+b)-{v,-v};assert not any(-z in R for z in R)
   assert R==set(p['resolvent'])
   cube={int(v):int(val) for v,val in p['forbidden_cube'].items()}
   rem=[j for j in range(1,n+1) if j not in cube]
   for bits in itertools.product((0,1),repeat=len(rem)):
    state={**cube,**dict(zip(rem,bits))};full=sum(val<<(j-1) for j,val in state.items())
    assert false(a,full) or false(b,full)
    count['resolvent_cube_extensions']+=1
  actual=sum(all(sat(c,a) for c in F) for a in range(1<<n))
  assert actual==x['exhaustive_model_count'];count['all_assignment_checks']+=1<<n
 # Primary n9 strict22 Hamming-layer certificate.
 x=cases[0];F=Fof(x);n=x['n'];D=x['hunter_controller']['result']['bound'];r=x['hunter_controller']['result']['radius'];anchor=x['hunter_controller']['result']['anchor'];assert r==3 and anchor==0
 T=D['tree'];adj={i:[] for i in range(len(F))}
 for i,j,w in T:adj[i].append(j);adj[j].append(i)
 parent={0:None};stack=[0]
 while stack:
  i=stack.pop()
  for j in adj[i]:
   if j not in parent:parent[j]=i;stack.append(j)
 assert len(parent)==len(F)
 mask=lambda a:[not sat(c,a) for c in F]
 def tree_bad(a):
  e=mask(a)
  return int(e[0])+sum(int(e[j] and not e[p]) for j,p in parent.items() if p is not None)
 layer=[i for i in range(1<<n) if (i^anchor).bit_count()==r]
 assert len(layer)==84
 assert sum(sum(mask(a)) for a in layer)==126
 assert sum(tree_bad(a) for a in layer)==83
 assert all(tree_bad(a)>0 if any(mask(a)) else tree_bad(a)==0 for a in layer)
 assert sum(all(sat(c,a) for c in F) for a in layer)==10
 for i,j,w in T:assert sum(false(F[i],a) and false(F[j],a) for a in layer)==w
 count['layer_assignment_direct_checks']+=len(layer)
 trail=x['hunter_controller']['result']['conditional_steps'];pins={}
 for z in trail:
  pins[z['variable']]=z['chosen_flip']
  sub=[a for a in layer if all(((a>>(v-1))&1)==bit for v,bit in pins.items())]
  assert len(sub)==z['remaining_layer_size'] and sum(tree_bad(a) for a in sub)==z['weighted_hunter_numerator']
  count['conditional_expectation_direct_checks']+=len(sub)
 witness=x['hunter_controller']['result']['witness'];assert witness==265 and witness in layer and all(sat(c,witness) for c in F)
 # Robustness to a signed source-variable rename/polarity swap (a bijection on models and Hamming layers).
 perm={i:(n+1-i) for i in range(1,n+1)};toggle={2,5,7}
 Fp=[tuple((1 if z>0 else -1)*(-1 if abs(z) in toggle else 1)*perm[abs(z)] for z in c) for c in F]
 def transform(a):
  out=0
  for v in range(1,n+1):out|=(((a>>(v-1))&1)^(v in toggle))<<(perm[v]-1)
  return out
 anc=transform(anchor)
 for a in layer:
  b=transform(a)
  assert (b^anc).bit_count()==r and all(sat(c,a) for c in F)==all(sat(c,b) for c in Fp)
 count['signed_renaming_checks']=len(layer)
 print('INDEPENDENT PASS',dict(count),'Hunter=83/84, union=126/84, radius3_models=10, witness=265; P-vs-NP OPEN')
if __name__=='__main__':check(sys.argv[1] if len(sys.argv)>1 else '2026-10-30_0612_LSPV-2_HAMMING_HUNTER251_raw.json')