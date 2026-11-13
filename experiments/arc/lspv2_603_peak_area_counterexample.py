#!/usr/bin/env python3
"""LSPV-2/603. Original archived /386 OS checker replayer, not the R_mix341 checker.
usage: python lspv2_603_peak_area_counterexample.py <W249.json> <checker386.js> <outdir> <SOURCE.cnf>
"""
import sys,json,itertools,copy,hashlib,subprocess,pathlib,collections
src,checker,out,source_cnf=map(pathlib.Path,sys.argv[1:5]);out.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
expected='22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113'
assert sha(checker.read_bytes())==expected
base=json.loads(src.read_bytes())
source_bytes=source_cnf.read_bytes()
assert sha(source_bytes)=='3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c'
tokens=source_bytes.decode('ascii').split()
assert tokens[:4]==['p','cnf','7','17']
cnf=[];row=[]
for t in tokens[4:]:
 v=int(t)
 if v==0:cnf.append(tuple(row));row=[]
 else:row.append(v)
assert len(cnf)==17 and not row
assert collections.Counter(cnf)==collections.Counter(tuple(x['c']) for x in base['records'] if x['kind']=='SOURCE')
r=base['records'];defs=[i for i,x in enumerate(r) if x['kind']=='DEF'];assert len(defs)==2
users={j:[i for i,x in enumerate(r) if x['kind']=='RES' and j in x['parents']] for j in defs}
assert all(len(x)==8 for x in users.values());names={j:('A' if k==0 else 'B') for k,j in enumerate(defs)}
terminal=[i for i,x in enumerate(r) if x['kind']=='RES' and not x['c']];assert len(terminal)==8
use_idxs=set(sum(users.values(),[]));special=use_idxs|set(terminal)|set(defs)
prep=[i for i,x in enumerate(r) if x['kind']=='SOURCE' or (x['kind']=='RES' and i not in special)]
assert sum(r[i]['kind']=='SOURCE' for i in prep)==17
# All prep nodes should be closed under parents, enabling legal global rescheduling.
assert all(all(p in prep for p in r[i]['parents']) for i in prep)
assert all(all((p in prep) or(p in defs) for p in r[i]['parents']) for i in use_idxs)
assert all(all(p in use_idxs for p in r[i]['parents']) for i in terminal)
# all 16 DEF-consuming RES nodes reordered into AABB AABB AABB AABB, 8 monochrome runs.
order_labels='AABBAABBAABBAABB';uses_by_kind={'A':users[defs[0]],'B':users[defs[1]]}
by_name={k:iter(v) for k,v in uses_by_kind.items()}
consumer_order=[next(by_name[x]) for x in order_labels]
# Inserting 35 explicitly paid redundant RES steps within two A-runs creates a
# memory peak versus live-slot-area tradeoff at 8 facet views.
pads={0:35,4:35}
rowidx={};new=[]; first_res=None
for i in prep:
 x=copy.deepcopy(r[i]);x['parents']=[rowidx[p] for p in x['parents']]
 rowidx[i]=len(new);new.append(x)
 if x['kind']=='RES' and first_res is None:first_res=copy.deepcopy(x)
assert first_res and not first_res['parents']==[]
# DEF views are created JIT, based on the selected cuts, not original position.
def emit(cuts):
 rows=copy.deepcopy(new);oldmap=rowidx.copy();copies={j:{} for j in defs};used={j:0 for j in defs};
 consumers=[];paid_step=sum(x['kind']=='RES' for x in rows)
 for rank,i in enumerate(consumer_order):
  x=copy.deepcopy(r[i]);j=next(j for j in defs if j in x['parents']);k=used[j];used[j]+=1
  # cut indices are indices *after* the corresponding use in that facet class.
  g=0
  for pos in range(k):g+=(j,pos) in cuts
  if g not in copies[j]:
   copies[j][g]=len(rows);rows.append(copy.deepcopy(r[j]))
  x['parents']=[copies[j][g] if p==j else oldmap[p] for p in x['parents']]
  oldmap[i]=len(rows);rows.append(x);paid_step+=1
  consumers.append({'label':names[j],'step':paid_step,'old':i,'copy_id':copies[j][g]})
  for _ in range(pads.get(rank,0)):
   rows.append(copy.deepcopy(first_res));paid_step+=1
 for i in terminal:
  x=copy.deepcopy(r[i]);x['parents']=[oldmap[p] for p in x['parents']];oldmap[i]=len(rows);rows.append(x)
 outpkt=copy.deepcopy(base);outpkt['records']=rows
 def_view=sum(x['kind']=='DEF' for x in rows)
 nres=sum(x['kind']=='RES' for x in rows)
 outpkt['summary']=dict(source=sum(x['kind']=='SOURCE' for x in rows),def_views=def_view,
   resolution=nres,paid_gates=len(outpkt['gate_defs']),paid_total=nres+len(outpkt['gate_defs']),live_records=len(rows))
 return outpkt,consumers
# The event chronology is independent of cuts. Compute exact instance for two facets.
seed,trace=emit(set()); seq={f:[z['step'] for z in trace if z['label']==f] for f in ['A','B']}
gaps=[];F={'A':defs[0],'B':defs[1]}
for f,ts in seq.items():
 for i,(a,b) in enumerate(zip(ts,ts[1:])):
  others=[x for g,aa in seq.items() if g!=f for x in aa if a<x<b]
  gaps.append({'facet':f,'facet_id':F[f],'after_use':i,'unused_paid_steps':b-a-1,'cross_other':bool(others)})
assert len(gaps)==14
mandatory={(g['facet_id'],g['after_use']) for g in gaps if g['cross_other']}
assert len(mandatory)==6
cut_top={(g['facet_id'],g['after_use']) for g in sorted(gaps,key=lambda z:(-z['unused_paid_steps'],z['facet'],z['after_use']))[:6]}
assert len(cut_top)==6
assert cut_top!=mandatory

def resource(pkt):
 times={};paid=0
 for i,x in enumerate(pkt['records']):
  if x['kind']=='DEF':times[i]=[]
  if x['kind']=='RES':
   paid+=1
   for p in x['parents']:
    if p in times:times[p].append(paid)
 assert len(times)==8 and all(x for x in times.values())
 intervals=[(min(t),max(t)) for t in times.values()]
 area=sum(b-a+1 for a,b in intervals)
 peak=max(sum(a<=j<=b for a,b in intervals) for j in range(1,paid+1))
 return {'area':area,'peak':peak,'DEF_views':len(times),'RES':paid,'paid':paid+len(pkt['gate_defs'])}

def check(name,pkt,expect):
 raw=(json.dumps(pkt,separators=(',',':'),ensure_ascii=False)+'\n').encode();p=out/(name+'.json');p.write_bytes(raw)
 child=subprocess.run(['node',str(checker),str(p)],capture_output=True,text=True,timeout=30)
 ok=child.returncode==0
 assert ok==expect,(name,child.stderr[:700]);info=json.loads(child.stdout) if ok else {'error':child.stderr.split('Error:')[-1].split('\n')[0]}
 return {'name':name,'sha256':sha(raw),'bytes':len(raw),'verdict':'ACCEPT' if ok else 'REJECT',
   'original_assertions':info.get('assertions',0),'checker_output':info,'model':resource(pkt) if ok else None}

area_best,atrace=emit(cut_top);peak_best,ptrace=emit(mandatory)
ares=resource(area_best);pres=resource(peak_best)
assert ares['peak']==2 and pres['peak']==1 and ares['area']<pres['area'],(ares,pres)
# Exhaust over the full 14 choose 6 possible contiguous 8-view allocations; exact, not random.
min_area=10**9;min_peak=10**9;peak1_best=10**9;witness_count=0;count=0
for combination in itertools.combinations(gaps,6):
 cs={(g['facet_id'],g['after_use']) for g in combination}
 # Exact combinatorial intervals, no full checker call for each cut set.
 intervals=[]
 for f,ts in seq.items():
  j=F[f];start=0
  for t in range(len(ts)):
   if t==len(ts)-1 or (j,t) in cs:
    intervals.append((ts[start],ts[t]));start=t+1
 area=sum(b-a+1 for a,b in intervals)
 event=set(v for ab in intervals for v in ab)
 peak=max(sum(a<=v<=b for a,b in intervals) for v in event)
 min_area=min(min_area,area);min_peak=min(min_peak,peak)
 if peak==1:peak1_best=min(peak1_best,area);witness_count+=1
 count+=1
assert count==3003 and ares['area']==min_area and pres['area']==peak1_best and witness_count==1
cases=[]
cases.append(check('native_area_optimal_peak2',area_best,True))
cases.append(check('native_peak_optimal_area_larger',peak_best,True))
# Both packets match in source clauses, signed RES multiset, paid owners and records count.
assert area_best['gate_defs']==peak_best['gate_defs']
assert collections.Counter(tuple(x['c']) for x in area_best['records'] if x['kind']=='SOURCE')==collections.Counter(tuple(x['c']) for x in peak_best['records'] if x['kind']=='SOURCE')
assert collections.Counter((tuple(x['c']),x.get('pivot')) for x in area_best['records'] if x['kind']=='RES')==collections.Counter((tuple(x['c']),x.get('pivot')) for x in peak_best['records'] if x['kind']=='RES')
assert ares['paid']==pres['paid'] and ares['DEF_views']==pres['DEF_views']==8
for name,fn in [
 ('bad_signed_SOURCE',lambda x:x['records'].__setitem__(0,{**x['records'][0],'c':[-x['spec']['guard']]})),
 ('bad_DEF_clause',lambda x:next(t for t in x['records'] if t['kind']=='DEF').__setitem__('c',[99999])),
 ('bad_RES_pivot',lambda x:x['records'][-1].__setitem__('pivot',0)),
 ('underpaid',lambda x:x['summary'].__setitem__('paid_total',x['summary']['paid_total']-1)),
 ('unsupported_AND3',lambda x:next(t for t in x['records'] if t['kind']=='DEF').__setitem__('kind','AND3')),
 ]:
 bad=copy.deepcopy(peak_best);fn(bad);cases.append(check(name,bad,False))
manifest={'schema':'LSPV2-603-NATIVE386-PEAK-AREA-FRONTIER/v1','status':'PROVED/RESTRICTED and COMPUTATIONAL; full R_mix341 OPEN',
 'scope':'Fixed reordered Resolution chronology; 8 true DEF views; last-use facet slot model, NOT actual RAM or universal lower bound',
 'original_checker_sha256':sha(checker.read_bytes()),'input_sha256':sha(src.read_bytes()),'external_signed_SOURCE_sha256':sha(source_bytes),
 'event_sequence':order_labels,'paid_padding_after_consumer_position':pads,'facet_use_times':seq,
 'gaps':gaps,'required_cuts_for_peak1':sorted(list(mandatory)),
 'top_six_area_cuts':sorted(list(cut_top)),
 'combinatorial_exhaustive_14_choose_6':count,'number_peak1_choices':witness_count,
 'min_area_any_peak':min_area,'min_area_if_peak1':peak1_best,'min_peak':min_peak,
 'original_checker_cases':cases,'totals':{'accepted':2,'rejected':5,'original_assertions':sum(c['original_assertions'] for c in cases)}}
(out/'LSPV2_603_PEAK_AREA_FRONTIER_RAW.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'PASS':True,'area_optimal':ares,'peak_optimal':pres,'exhaustive_assignments':count,'peak1_assignments':witness_count,'original_checker':manifest['totals']},indent=2))