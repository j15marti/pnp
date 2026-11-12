#!/usr/bin/env python3
"""LSPV-2/577. Original-/386 accepted-byte, LIVE rank-descent falsifier.

Requires the unchanged pinned archived /386 checker, /576 accepted W29
packet and finite potential under their published repository paths.
Usage: python3 experiments/arc/lspv2_577_live_rank_cegar.py . /tmp/lspv2_577
The reference search/transformer here is NOT an authoritative checker.
"""
import collections, copy, hashlib, json, pathlib, subprocess, sys, tempfile
ROOT=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
OUT=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else '/tmp/lspv2_577').resolve();OUT.mkdir(parents=True,exist_ok=True)
checker=ROOT/'experiments/arc/lspv2_386_independent_verify.js'
source=ROOT/'results/raw/arc/574_k01_SIGNED_SOURCE.cnf'
basefile=ROOT/'results/raw/arc/2026-11-12_0712_LSPV2_576_ACCEPTED_TREE_RES_W29.json'
if not basefile.exists():
 basefile=ROOT/'results/raw/arc/576_accepted_tree_min_W29.json'
potentialfile=ROOT/'results/raw/arc/2026-11-12_0712_LSPV2_576_POTENTIAL_2187.json'
if not potentialfile.exists():
 potentialfile=ROOT/'results/raw/arc/576_potential_2187.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
gitblob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert gitblob(checker.read_bytes())=='338305c0ce101704205e57543756b8127074a986','wrong original checker'
assert sha(source.read_bytes())=='3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c'
base=json.loads(basefile.read_bytes());h=json.loads(potentialfile.read_bytes());assert len(h)==2187 and h[0]==28
canon=lambda c:tuple(sorted(set(c),key=lambda x:(abs(x),x)))
def rank(c):
 s=set(c);idx=sum(3**(v-1)*(1 if v in s else 2 if -v in s else 0) for v in range(1,8))
 return h[idx]
def resolve(a,b,p):
 if p not in a or -p not in b:return None
 c=canon([x for x in a if x!=p]+[x for x in b if x!=-p]);return None if any(-x in c for x in c) else c
src=base['records'][:17];cnf=source.read_text().strip().splitlines()
assert cnf[0]=='p cnf 7 17'
assert [list(map(int,s.split()[:-1])) for s in cnf[1:]]==[r['c'] for r in src]
old=copy.deepcopy(base['records'][:-1]);assert len(old)==44 and base['records'][-1]['c']==[]
assert all(r['kind']=='SOURCE' for r in src)
# Search ALL signed RES pairs in this fixed original 44-record legal prefix,
# then restrict to rank-descending steps. This is discovery, not a rule guard.
candidates=[]
for j in range(44):
 for i in range(j):
  a=old[i]['c'];b=old[j]['c']
  for p in a:
   c=resolve(a,b,p)
   if c is None:continue
   gap=max(rank(a),rank(b))-rank(c)
   if gap>0:candidates.append((gap,i,j,p,c))
candidates.sort(key=lambda z:(-z[0],z[1],z[2],z[3],z[4]))
assert candidates
# Find a positive-length continuation that uses the descended result and
# reaches the original terminal predecessor [-7] via already authenticated
# available clauses. Avoid introducing invented source/gate/AND3 syntax.
known=[canon(r['c']) for r in old]
def continuation(start,target=(-7,)):
 seen={start:None};todo=collections.deque([start])
 while todo:
  a=todo.popleft()
  if a==target:
   seq=[]
   while seen[a] is not None:
    prev,k,p=seen[a];seq.append((prev,k,p,a));a=prev
   return seq[::-1]
  for k,b in enumerate(known):
   for p in a:
    c=resolve(a,b,p)
    if c is None or c in seen:continue
    seen[c]=(a,k,p);todo.append(c)
    if len(seen)>2187:raise AssertionError('exceeded exact clause universe')
 return None
selection=None
for gap,i,j,p,c in candidates:
 path=continuation(c)
 if path and len(path)>0:
  selection=(gap,i,j,p,c,path);break
assert selection is not None
gap,i,j,p,c,path=selection
assert gap>=1
full=copy.deepcopy(old);full.append({'kind':'RES','c':list(c),'parents':[i,j],'pivot':p})
prev_idx=len(full)-1;prev_clause=c
for a,k,pivot,out in path:
 assert a==prev_clause
 full.append({'kind':'RES','c':list(out),'parents':[prev_idx,k],'pivot':pivot})
 prev_idx=len(full)-1;prev_clause=out
assert prev_clause==(-7,)
full.append({'kind':'RES','c':[],'parents':[16,prev_idx],'pivot':7})
assert any(rank(full[x]['c'])<max(*(rank(full[q]['c']) for q in full[x]['parents'])) for x in range(44,len(full)-1))
# Terminal dependency closure: all 17 externally-bound SOURCE records are
# mandatory even when not in the proof's ancestor cone. The paid gate remains.
used=set();todo=[len(full)-1]
while todo:
 k=todo.pop()
 if k in used:continue
 used.add(k);todo.extend(full[k]['parents'])
keep=list(range(17))+sorted(k for k in used if k>=17)
assert 44 in keep, 'rank-descent must be live in pruned packet'
def packet(inds):
 mp={old_i:new_i for new_i,old_i in enumerate(inds)};records=[]
 for old_i in inds:
  r=copy.deepcopy(full[old_i]);r['parents']=[mp[q] for q in r['parents']];records.append(r)
 d=copy.deepcopy(base);d['records']=records
 R=sum(r['kind']=='RES' for r in records);D=len(d['gate_defs'])
 d['summary']={'source':17,'def_views':0,'resolution':R,'paid_gates':D,'paid_total':R+D,'live_records':len(records)}
 return d
packets={'baseline_W29':base,'live_descent_full':packet(list(range(len(full)))),'live_descent_pruned':packet(keep)}
checks=[]
def run(name,obj,accept):
 data=(json.dumps(obj,separators=(',',':'))+'\n').encode();dest=OUT/(name+'.json');dest.write_bytes(data)
 r=subprocess.run(['node',str(checker),str(dest)],capture_output=True,text=True,timeout=20)
 verdict=r.returncode==0
 assert verdict==accept,(name,verdict,r.stderr[:300],r.stdout[:300])
 parsed=json.loads(r.stdout) if verdict else None
 checks.append({'id':name,'expected':'ACCEPT' if accept else 'REJECT',
                'actual':'ACCEPT' if verdict else 'REJECT','sha256':sha(data),
                'bytes':len(data),'paid_total':obj.get('summary',{}).get('paid_total'),
                'assertions':parsed['assertions'] if parsed else None,
                'error_tail':r.stderr[-200:].strip() if not verdict else None})
for name,d in packets.items():run(name,d,True)
mutations=[
 ('bad_source',lambda d:d['records'][0]['c'].__setitem__(0,-1)),
 ('underpay',lambda d:d['summary'].__setitem__('paid_total',d['summary']['paid_total']-1)),
 ('forward_parent',lambda d:d['records'][-1]['parents'].__setitem__(0,len(d['records'])+1)),
 ('bad_descent_pivot',lambda d:next(r for r in d['records'] if r['kind']=='RES' and tuple(r['c'])==c).__setitem__('pivot',999)),
 ('unknown_AND3',lambda d:d['records'][-1].__setitem__('kind','AND3')),
 ('bad_gate_fresh',lambda d:d['gate_defs'][0].__setitem__(1,d['spec']['guard'])),
]
for name,mut in mutations:
 d=copy.deepcopy(packets['live_descent_pruned']);mut(d);run(name,d,False)
pruned=packets['live_descent_pruned'];rankdesc=[];fanout=collections.Counter()
for idx,r in enumerate(pruned['records']):
 for par in r['parents']:fanout[par]+=1
 if r['kind']!='RES':continue
 ranks=[rank(pruned['records'][p]['c']) for p in r['parents']]
 if rank(r['c'])<max(ranks):rankdesc.append({'index':idx,'parent_indices':r['parents'],'parent_ranks':ranks,'conclusion_rank':rank(r['c']),'conclusion':r['c']})
assert rankdesc and max(fanout[k] for k in range(17,len(pruned['records'])-1))>=2
raw={'experiment':'LSPV-2/577 native386 live rank descent / cost-sound abstraction falsifier',
 'scope':'exact externally signed guarded K4 SOURCE; only native /386 SOURCE/DEF/RES; NOT full R_mix341',
 'source_sha256':sha(source.read_bytes()),'checker_git_blob':gitblob(checker.read_bytes()),
 'original_tree_potential_sha256':sha(potentialfile.read_bytes()),
 'source_clause_count':17,'candidate_descending_inferences':len(candidates),
 'first_candidate':{'parent_indices':[i,j],'pivot':p,'conclusion':list(c),'parent_ranks':[rank(old[i]['c']),rank(old[j]['c'])], 'conclusion_rank':rank(c),'rank_drop':gap},
 'continuation_steps':len(path),'pruned_rank_descents':rankdesc,
 'pruned_paid_resolution':pruned['summary']['resolution'],
 'pruned_paid_work':pruned['summary']['paid_total'],
 'pruned_derived_shared_fanout_max':max(fanout[k] for k in range(17,len(pruned['records'])-1)),
 'tests':checks,'number_accepted':sum(k['actual']=='ACCEPT' for k in checks),
 'number_rejected':sum(k['actual']=='REJECT' for k in checks),
 'claim':'Rank-monotone RES abstraction omits a genuine LIVE accepted transition; cannot be a complete MAY abstraction without independent cost-safe normalization proof. Not a lower bound.'}
(OUT/'577_native386_live_rank_cegar_results.json').write_text(json.dumps(raw,indent=2)+'\n')
print(json.dumps(raw,indent=2))
