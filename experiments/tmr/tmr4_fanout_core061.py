#!/usr/bin/env python3
"""TMR-4/061: authentic circuit DAG -> no-advice shared-core register/OBDD transfer.
Deterministic seed 20261115, exhaustive small input assignments; evidence is COMPUTATIONAL.
"""
import json, random, itertools, hashlib, sys
from collections import Counter, defaultdict

SEED=20261115
rng=random.Random(SEED)

def enc(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')

def validate(source):
    if not isinstance(source,(bytes,bytearray)) or not source.isascii():raise ValueError('ascii')
    obj=json.loads(source)
    if enc(obj)!=source:raise ValueError('noncanonical')
    if set(obj)!={'version','n','gates','root'} or type(obj['version']) is not int or obj['version']!=1:raise ValueError('shape')
    n=obj['n']; gl=obj['gates']; root=obj['root']
    if type(n) is not int or n<1 or not isinstance(gl,list) or not gl or n>2*len(gl):raise ValueError('preallocation arity bound')
    if not isinstance(root,str):raise ValueError('root')
    gates={}
    for e in gl:
        if not isinstance(e,dict) or set(e)!={'id','a','b','op'}:raise ValueError('gate fields')
        ident=e['id']
        if not isinstance(ident,str) or not ident.startswith('g') or not ident[1:].isdigit() or str(int(ident[1:]))!=ident[1:] or ident in gates:raise ValueError('gate id')
        if type(e['op']) is not int or e['op'] not in range(16):raise ValueError('opcode')
        if any(not isinstance(e[z],str) for z in ('a','b')):raise ValueError('ref')
        gates[ident]=e
    if len(gates)!=len(gl) or root not in gates:raise ValueError('root gate')
    def check_ref(s):
        if s.startswith('x') and s[1:].isdigit() and str(int(s[1:]))==s[1:] and int(s[1:])<n:return
        if s in gates:return
        raise ValueError('bad ref')
    for v in gates.values():check_ref(v['a']);check_ref(v['b'])
    colors={}; topo=[]; used_inputs=set()
    def dfs(v):
        if v.startswith('x'):
            used_inputs.add(v);return
        if colors.get(v)==1:raise ValueError('cycle')
        if colors.get(v)==2:return
        colors[v]=1
        e=gates[v]
        dfs(e['a']);dfs(e['b']);colors[v]=2;topo.append(v)
    dfs(root)
    if len(topo)!=len(gates) or len(used_inputs)!=n:raise ValueError('dead vertices/inputs')
    out=Counter()
    for e in gates.values():out[e['a']]+=1;out[e['b']]+=1
    out[root]+=1  # output consumer
    shared={v for v,d in out.items() if d>=2}
    # Source topological shared order, including shared input ancestors.
    done=set(); all_topo=[]
    def topo_full(v):
        if v in done:return
        if v in gates:
            topo_full(gates[v]['a']);topo_full(gates[v]['b'])
        done.add(v);all_topo.append(v)
    topo_full(root)
    return obj,gates,root,n,shared,all_topo

def compile_source(source):
    obj,gates,root,n,shared,full_topo=validate(source)
    shared_order=[v for v in full_topo if v in shared]
    shared_ids={v:i for i,v in enumerate(shared_order)}
    labels={}
    def label(v):
        if v in shared or v.startswith('x'):return 1
        if v in labels:return labels[v]
        a,b=gates[v]['a'],gates[v]['b']
        ra,rb=label(a),label(b)
        labels[v]=max(ra,rb)+(ra==rb)
        return labels[v]
    instr=[]; visited=set()
    def emit(v,as_target=False):
        if v in shared and not as_target:
            instr.append(('REF',shared_ids[v],v));return
        if v.startswith('x'):
            assert v not in visited
            visited.add(v)
            instr.append(('READ',int(v[1:]),v))
            if v in shared:instr.append(('STORE',shared_ids[v],v))
            return
        if v in visited:raise AssertionError('duplicate original gate execution')
        visited.add(v)
        e=gates[v]; a,b=e['a'],e['b']
        ra,rb=label(a),label(b)
        if rb>ra:
            emit(b);emit(a);instr.append(('GATE_REV',e['op'],v))
        else:
            emit(a);emit(b);instr.append(('GATE',e['op'],v))
        if v in shared:instr.append(('STORE',shared_ids[v],v))
    for v in shared_order:emit(v,as_target=True)
    emit(root,as_target=True)
    assert len(visited)==n+len(gates)
    assert sum(i[0]=='GATE' or i[0]=='GATE_REV' for i in instr)==len(gates)
    read_order=[i[1] for i in instr if i[0]=='READ']
    assert sorted(read_order)==list(range(n))
    # Refs always after the original signal has been computed.
    avail=set()
    for op,arg,ref in instr:
        if op=='REF':assert ref in avail
        if op=='STORE':avail.add(ref)
    def target_label(v):
        if v.startswith("x"):return 1
        e=gates[v];ra,rb=label(e["a"]),label(e["b"])
        return max(ra,rb)+(ra==rb)
    rbound=max([target_label(v) for v in shared_order+[root]] or [1])
    # Conservative bound from all leaf occurrences in source binary DAG.
    import math
    wbound=len(shared)+2+math.ceil(math.log2(n+2*len(gates)+2))
    return dict(n=n,g=len(gates),k=len(shared),shared=shared_order,order=read_order,instr=instr,wbound=wbound,rbound=rbound,source_sha256=hashlib.sha256(source).hexdigest())

def exec_comp(comp, bits, detailed=False):
    cache=[0]*comp['k']; stack=[]; maxstack=0; states=[]; cursor=0; original_gates=[]
    for op,arg,ref in comp['instr']:
        if op=='READ':
            states.append(tuple(cache+stack));stack.append(bits[arg]);cursor+=1
        elif op=='REF':stack.append(cache[arg])
        elif op=='STORE':cache[arg]=stack.pop()
        elif op in ('GATE','GATE_REV'):
            b=stack.pop();a=stack.pop()
            if op=='GATE_REV':a,b=b,a
            z=(arg>>((a<<1)|b))&1
            stack.append(z);original_gates.append((ref,a,b,z))
        else:raise AssertionError(op)
        maxstack=max(maxstack,len(stack))
        assert maxstack<=comp['rbound']
    assert len(states)==comp['n'] and len(stack)==1
    res=dict(out=stack[0],states=states,maxstack=maxstack)
    if detailed:res['gates']=original_gates
    return res

def direct(obj,bits):
    gs={e['id']:e for e in obj['gates']}
    memo={}
    def visit(v):
        if v.startswith('x'):return bits[int(v[1:])]
        if v in memo:return memo[v]
        e=gs[v];a,b=visit(e['a']),visit(e['b'])
        memo[v]=(e['op']>>((a<<1)|b))&1
        return memo[v]
    return visit(obj['root'])

def rank2(rows,cols,outs):
    vec=[]
    for p in range(1<<rows):
        bitset=0
        for s in range(1<<cols):
            bitset|=int(outs[(p<<cols)|s])<<s
        vec.append(bitset)
    basis={}
    for v in vec:
        while v:
            i=v.bit_length()-1
            if i not in basis:basis[i]=v;break
            v^=basis[i]
    return len(basis)

def stage_transition(c, layer, state, z):
    # Source-derived transition with no assignment oracle or truth table.
    reads=[i for i,v in enumerate(c['instr']) if v[0]=='READ']
    start=reads[layer]; stop=reads[layer+1] if layer+1<c['n'] else len(c['instr'])
    cache=list(state[:c['k']]);stack=list(state[c['k']:])
    assert c['instr'][start][0]=='READ'
    for i in range(start,stop):
        op,arg,ref=c['instr'][i]
        if op=='READ':
            assert i==start;stack.append(z)
        elif op=='REF':stack.append(cache[arg])
        elif op=='STORE':cache[arg]=stack.pop()
        elif op in ('GATE','GATE_REV'):
            b=stack.pop();a=stack.pop()
            if op=='GATE_REV':a,b=b,a
            stack.append((arg>>((a<<1)|b))&1)
        else:raise AssertionError(op)
    if layer+1<c['n']:return tuple(cache+stack)
    assert len(stack)==1
    return ('HALT',stack[0])

def build_obdd(c):
    # BFS on compiled states, two labelled arcs at every real input test.
    states=[{tuple([0]*c['k'])}]
    edges=[]
    for j in range(c['n']):
        emap={}; next_states=set()
        for st in sorted(states[-1]):
            for z in (0,1):
                dest=stage_transition(c,j,st,z)
                emap[(st,z)]=dest
                if j+1<c['n']:next_states.add(dest)
        edges.append(emap)
        if j+1<c['n']:states.append(next_states)
    paths={tuple([0]*c['k']):1}
    for emap in edges:
        nxt=defaultdict(int)
        for st,number in paths.items():
            for z in (0,1):nxt[emap[(st,z)]]+=number
        paths=nxt
    return states,edges,paths

def test(obj):
    source=enc(obj);c=compile_source(source);n=c['n'];assert n<=10
    states,edges,final=build_obdd(c)
    replay=[];assertions=0; maxstack=0
    for mask in range(1<<n):
        bits=tuple((mask>>i)&1 for i in range(n))
        e=exec_comp(c,bits);want=direct(obj,bits)
        assert e['out']==want and len(e['states'])==n
        assertions+=2
        replay.append((bits,e['out'],e['states']))
        maxstack=max(maxstack,e['maxstack'])
        for t,st in enumerate(e['states']):
            assert st in states[t]
            a=bits[c['order'][t]]
            target=e['states'][t+1] if t<n-1 else ('HALT',e['out'])
            assert edges[t][(st,a)]==target
            assertions+=2
    got=final.get(('HALT',1),0)
    exact=sum(v for _,v,_ in replay)
    assert got==exact and final.get(('HALT',0),0)+got==(1<<n)
    assertions+=2
    assert c['k']+maxstack<=c['wbound']
    assert all(len(s)<=2**c['wbound'] for s in states)
    assertions+=2
    # F2 rank from exact assignment matrix in the source-discovered prefix order.
    vals={}
    for bits,v,_ in replay:
        index=0
        for t in range(n):index=(index<<1)|bits[c['order'][t]]
        vals[index]=v
    maxrank=0
    for p in range(1,n):
        rank=rank2(p,n-p,vals)
        assert rank<=len(states[p])
        assertions+=1
        maxrank=max(maxrank,rank)
    return dict(n=n,g=c['g'],shared=c['k'],shared_ids=c['shared'],read_order=c['order'],maxstack=maxstack,frontier_bound=c['wbound'],labelled_obdd_nodes=sum(map(len,states)),obdd_generic_upper=n*2**c['wbound'],max_prefix_rank_f2=maxrank,accept=got,source_sha256=c['source_sha256'],assertions=assertions,paths=len(replay))

OPS={'AND':8,'OR':14,'XOR':6,'EQ':9,'NAND':7,'NOR':1,'A':12,'B':10}
def mk(n,kind,op=6):
    gates=[]
    def gate(a,b,opcode):
        ident=f'g{len(gates)}';gates.append(dict(id=ident,a=a,b=b,op=opcode));return ident
    def balanced(xs,opcode=14):
        while len(xs)>1:
            xs=[gate(xs[i],xs[i+1],opcode) if i+1<len(xs) else xs[i] for i in range(0,len(xs),2)]
        return xs[0]
    if kind=='fanout_hub':
        h=gate('x0','x1',op)
        leafs=[gate(h,f'x{i}',OPS['AND']) for i in range(2,n)]
        root=balanced(leafs)
    elif kind=='shared_input':
        leafs=[gate('x0',f'x{i}',op) for i in range(1,n)]
        root=balanced(leafs,OPS['AND'])
    elif kind=='long_edge':
        h=gate('x0','x1',op)
        root=gate(h,'x2',OPS['AND'])
        for i in range(3,n):root=gate(root,gate(h,f'x{i}',OPS['XOR']),OPS['OR'])
    elif kind=='two_hubs':
        h=gate('x0','x1',op);j=gate('x2','x3',OPS['OR'])
        leafs=[gate(j,gate(h,f'x{i}',OPS['XOR']),OPS['AND']) for i in range(4,n)]
        root=balanced(leafs)
    elif kind=='disj':
        assert n%2==0
        leafs=[gate(f'x{i}',f'x{i+n//2}',OPS['NAND']) for i in range(n//2)]
        root=balanced(leafs,OPS['AND'])
    else:raise ValueError(kind)
    rng.shuffle(gates)  # The source provides NO topological layout.
    return dict(version=1,n=n,gates=gates,root=root)

def main():
    results=[]; checked=0; paths=0
    for kind,ns in [('fanout_hub',range(4,11)),('shared_input',range(4,11)),('long_edge',range(4,11)),('two_hubs',range(6,11)),('disj',(4,6,8,10))]:
        for n in ns:
            for op in (6,8,14,9):
                obj=mk(n,kind,op)
                a=test(obj);a['family']=kind;a['op']=op
                results.append(a);checked+=a['assertions'];paths+=a['paths']
    invalid=[]
    src=enc(mk(6,'fanout_hub',6));obj=json.loads(src)
    cases=[]
    for edit in ('huge_n','bad_op','dead_gate','bad_ref','cycle','duplicate_id'):
        z=json.loads(src)
        if edit=='huge_n':z['n']=10**40
        if edit=='bad_op':z['gates'][0]['op']=16
        if edit=='dead_gate':z['gates'].append(dict(id='g99',a='x0',b='x1',op=8))
        if edit=='bad_ref':z['gates'][0]['a']='x999'
        if edit=='cycle':
            # Force root gate to reference itself.
            for e in z['gates']:
                if e['id']==z['root']:e['a']=z['root']
        if edit=='duplicate_id':z['gates'][0]['id']=z['gates'][1]['id']
        cases.append((edit,enc(z)))
    cases.append(('noncanonical',b'{"version": 1}'))
    for label,s in cases:
        try:compile_source(s);raise AssertionError('accepted '+label)
        except (ValueError,RecursionError):invalid.append(label);checked+=1
    assert len(invalid)==len(cases)
    record={'name':'tmr4_fanout_core061','revision':'release1','seed':SEED,'status':'COMPUTATIONAL','cases':len(results),'assignment_replays':paths,'assertions':checked,'failures':0,'malformed_rejected':invalid,'families':{k:sum(q['family']==k for q in results) for k in ['fanout_hub','shared_input','long_edge','two_hubs','disj']},'samples':[results[0],results[len(results)//2],results[-1]],'max_cache':max(x['shared'] for x in results),'max_nodes':max(x['labelled_obdd_nodes'] for x in results),'scope':'fully encoded valid acyclic binary gate DAGs with all vertices/input uses root-reachable, canonical ASCII JSON'}
    print(json.dumps(record,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
