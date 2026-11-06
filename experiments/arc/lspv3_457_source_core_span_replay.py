#!/usr/bin/env python3
"""LSPV-3/457. Source-authenticated all-rule work/span control and random-family union audit.
Native semantic AND3/XOR on the published cubic Tseitin encoding; NOT a historical byte checker.
"""
import hashlib,json,math,itertools,time,resource
from pathlib import Path
start=time.perf_counter()
O=Path(__file__).resolve().parent
edges=list(itertools.combinations(range(4),2))
assert len(edges)==6
inc={v:tuple(i+1 for i,e in enumerate(edges) if v in e) for v in range(4)}
charge=[1,0,0,0]
clauses=[]; groups={}
for v in range(4):
    ids=[]
    for bits in itertools.product((0,1),repeat=3):
        if sum(bits)%2 == charge[v]: continue
        clause=[(-var if bit else var) for var,bit in zip(inc[v],bits)]
        ids.append(len(clauses));clauses.append(clause)
    groups[v]=ids
assert all(len(ids)==4 for ids in groups.values())
source='p cnf 6 16\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
source_hash=hashlib.sha256(source.encode()).hexdigest()
nodes=[]
for i,c in enumerate(clauses):
    nodes.append({'id':i,'type':'source','source_index':i,'clause':c,'depth':0})
for v in range(4):
    triple=inc[v]
    def vals_for_clause(c):
        return [int(any((x>0 and bits[triple.index(abs(x))]==1) or (x<0 and bits[triple.index(abs(x))]==0) for x in c)) for bits in itertools.product((0,1),repeat=3)]
    def add_pair(pa,pb):
        ta=vals_for_clause(clauses[pa]) if pa<16 else nodes[pa]['table']
        tb=vals_for_clause(clauses[pb]) if pb<16 else nodes[pb]['table']
        obj={'id':len(nodes),'type':'and3','parents':[pa,pb],'support':list(triple),'table':[a&b for a,b in zip(ta,tb)],'depth':max(nodes[pa]['depth'],nodes[pb]['depth'])+1}
        nodes.append(obj);return obj['id']
    p0=add_pair(*groups[v][:2]);p1=add_pair(*groups[v][2:]);p2=add_pair(p0,p1)
    assert nodes[p2]['table']==[int(sum(bits)%2==charge[v]) for bits in itertools.product((0,1),repeat=3)]
    nodes[p2]['affine_annotation']={'mask':sum(1<<(x-1) for x in triple),'rhs':charge[v]}
    groups[v]=p2
def add_xor(a,b):
    A=nodes[a]['affine_annotation'] if 'affine_annotation' in nodes[a] else nodes[a]['row']
    B=nodes[b]['affine_annotation'] if 'affine_annotation' in nodes[b] else nodes[b]['row']
    obj={'id':len(nodes),'type':'xor','parents':[a,b], 'row':{'mask':A['mask']^B['mask'],'rhs':A['rhs']^B['rhs']}, 'depth':max(nodes[a]['depth'],nodes[b]['depth'])+1}
    nodes.append(obj);return obj['id']
a=add_xor(groups[0],groups[1]);b=add_xor(groups[2],groups[3]);root=add_xor(a,b)
assert nodes[root]['row']=={'mask':0,'rhs':1}
q=sum(z['type']!='source' for z in nodes)
span=nodes[root]['depth']
assert (q,span)==(15,4)
models=[];deletion_witness=[]
for bits in itertools.product((0,1),repeat=6):
    violations=[i for i,c in enumerate(clauses) if not any((x>0 and bits[abs(x)-1]) or (x<0 and not bits[abs(x)-1]) for x in c)]
    if not violations: models.append(bits)
    if len(violations)==1: deletion_witness.append((violations[0],bits))
assert not models
wits={i:list(b) for i,b in deletion_witness}
assert set(wits)==set(range(16))
anc=set();todo=[root]
while todo:
    i=todo.pop()
    if i in anc:continue
    anc.add(i);todo.extend(nodes[i].get('parents',[]))
assert anc==set(range(31))
assert len(anc&set(range(16)))==16
assert q==16-1 and span==math.ceil(math.log2(16))
theta=8*math.e**2/60
assert theta<1
limit_abs=math.exp(-24)
H=lambda x: -(x*math.log(x)+(1-x)*math.log1p(-x))
rate=lambda x:H(x)+8*H(x/8)+3*x*math.log(x)
lo,hi=.015,.020
for _ in range(100):
    mid=(lo+hi)/2
    if rate(mid)>0:hi=mid
    else:lo=mid
root_rate=(lo+hi)/2
packet={'type':'semantic_R_mix341_native_AND3_XOR_control','status':'KNOWN/PROVED-RESTRICTED','source_sha256':source_hash,'original_variable_bound':6,'source_clause_count':16,'nodes':nodes,'root':root,'deleted_source_sat_witnesses':wits}
summary={'source_sha256':source_hash,'source_ascii_bytes':len(source.encode()),'source_clause_count':16,'source_var_count':6,'mu_F':16,'paid_nodes':q,'weighted_span':span,'sources_in_root_ancestry':16,'theta_1_over_60':theta,'log_union_sufficient':theta<1,'entropy_rate_root_diagnostic':root_rate,'entropy_rate_at_1_over_60':rate(1/60),'ambient_missing_variable_limit':limit_abs,'large_n_missing_var_fraction_nonzero':limit_abs>0,'producer_wall_s':time.perf_counter()-start,'producer_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
print(json.dumps({'original_dimacs':source,'certificate':packet,'summary':summary},indent=2))
