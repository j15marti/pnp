#!/usr/bin/env python3
"""TWOTREEBRIDGE1. Exact shared-DAG cofactors and a two-tree 3-colouring bridge.
Python 3.10+, standard library only. All tests are deterministic. Each audit
invocation has a 25-second budget, separate from the production algorithms.
Examples:
  python two_tree_bridge_audit.py --batch local --out local.json
  python two_tree_bridge_audit.py --batch circuits --n 4 --out circuits4.json
  python two_tree_bridge_audit.py --batch reduction --n 4 --out reduction4.json
A finite test is not an unrestricted lower bound. New project theorems await
independent review. Colors 0,1,2 here label the three NONZERO F4 elements.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import itertools as it
import json
from pathlib import Path
import time

COLORS = (0, 1, 2)

class Audit:
    def __init__(self): self.start = time.monotonic(); self.counts = Counter()
    def check(self, ok, label):
        self.counts[label] += 1
        if not ok: raise AssertionError(label)
        if time.monotonic() - self.start > 25: raise TimeoutError('split audit into smaller batches')

def graph_ok(n, edges):
    if type(n) is not int or n < 1: raise ValueError('positive explicit vertex count required')
    if any(type(u) is not int or type(v) is not int or not 0 <= u < v < n for u,v in edges):
        raise ValueError('invalid canonical edge')
    if len(edges) != len(set(edges)): raise ValueError('duplicate edge')

def coloring(c, edges): return all(x in COLORS for x in c) and all(c[u] != c[v] for u,v in edges)

def components(vertices, edges):
    vs = set(vertices); adj = {v: [] for v in vs}
    for u,v in edges:
        if u not in vs or v not in vs: raise ValueError('edge outside vertex set')
        adj[u].append(v); adj[v].append(u)
    unseen = set(vs); result = []
    while unseen:
        r=min(unseen); unseen.remove(r); todo=[r]
        for v in todo:
            for u in adj[v]:
                if u in unseen: unseen.remove(u); todo.append(u)
        result.append(sorted(todo))
    return result

def tree_ok(vertices, edges):
    vs=set(vertices)
    return bool(vs) and len(edges)==len(vs)-1 and len(components(vs,edges))==1

class DAG:
    """Interned fan-in-two Boolean circuit; domain inputs test a color equality."""
    def __init__(self):
        self.nodes=[('const',0),('const',1)]; self.deps=[0,0]; self.cache={}
    def inp(self,v,c):
        key=('in',v,c)
        if key not in self.cache:
            self.cache[key]=len(self.nodes); self.nodes.append(key); self.deps.append(1<<v)
        return self.cache[key]
    def gate(self,op,a,b):
        if a==b: return a
        if op=='and':
            if a==0 or b==0:return 0
            if a==1:return b
            if b==1:return a
        elif op=='or':
            if a==1 or b==1:return 1
            if a==0:return b
            if b==0:return a
        else: raise ValueError('unknown gate')
        a,b=sorted((a,b)); key=(op,a,b)
        if key not in self.cache:
            self.cache[key]=len(self.nodes); self.nodes.append(key); self.deps.append(self.deps[a]|self.deps[b])
        return self.cache[key]
    def combine(self,op,roots):
        r=1 if op=='and' else 0
        for x in roots:r=self.gate(op,r,x)
        return r
    def reach(self,roots):
        seen=set(); todo=list(roots)
        while todo:
            x=todo.pop()
            if x in seen:continue
            seen.add(x); a=self.nodes[x]
            if a[0] in ('and','or'):todo.extend(a[1:])
        return sorted(seen)
    def size(self,roots):return sum(self.nodes[x][0] in ('and','or') for x in self.reach(roots))
    def evaluate(self,root,point):
        vals={}
        for j in self.reach([root]):
            node=self.nodes[j]
            if node[0]=='const':v=bool(node[1])
            elif node[0]=='in':v=point.get(node[1])==node[2]
            elif node[0]=='and':v=vals[node[1]] and vals[node[2]]
            else:v=vals[node[1]] or vals[node[2]]
            vals[j]=v
        return vals[root]
    def forget(self,root,var):
        """Exact three cofactors. Only var-dependent gates are copied.
        All created nodes remain in the pool; active and archived sizes differ.
        """
        reach=self.reach([root]); gates=[j for j in reach if self.nodes[j][0] in ('and','or')]
        dependent=sum(bool(self.deps[j]&(1<<var)) for j in gates)
        independent=len(gates)-dependent
        old_pool=len(self.nodes); out=[]
        for color in COLORS:
            remap={}
            for j in reach:
                node=self.nodes[j]
                if not self.deps[j]&(1<<var):remap[j]=j
                elif node[0]=='in':remap[j]=int(node[2]==color)
                elif node[0] in ('and','or'):remap[j]=self.gate(node[0],remap[node[1]],remap[node[2]])
                else:raise AssertionError('bad dependency annotation')
            out.append(remap[root])
        answer=self.combine('or',out)
        new_gates=sum(n[0] in ('and','or') for n in self.nodes[old_pool:])
        return answer,out,{'before_gates':len(gates),'independent_gates':independent,
                          'dependent_gates':dependent,'after_active_gates':self.size([answer]),
                          'after_support_gates':self.size(out+[answer]),'new_gates':new_gates,
                          'allocated_nodes':len(self.nodes)}

def graph_circuit(D,n,edges):
    return D.combine('and',[D.combine('or',[D.gate('and',D.inp(u,a),D.inp(v,b))
          for a in COLORS for b in COLORS if a!=b]) for u,v in edges])

def tree_summary(D,vertices,edges,boundary):
    if not tree_ok(vertices,edges):raise ValueError('tree required')
    adj={v:[] for v in vertices}
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    root=min(vertices); parent={root:None}; order=[root]
    for v in order:
        for u in adj[v]:
            if u!=parent[v]:parent[u]=v;order.append(u)
    feasible={v:[D.inp(v,c) if v in boundary else 1 for c in COLORS] for v in vertices}
    for v in reversed(order[1:]):
        p=parent[v]
        for c in COLORS:
            allowed=D.combine('or',[feasible[v][a] for a in COLORS if a!=c])
            feasible[p][c]=D.gate('and',feasible[p][c],allowed)
    return D.combine('or',feasible[root])

def tree_lift(vertices,edges,pins):
    if not tree_ok(vertices,edges):raise ValueError('tree required')
    if any(v not in vertices or c not in COLORS for v,c in pins.items()):raise ValueError('invalid pin')
    adj={v:[] for v in vertices}
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    root=min(vertices);parent={root:None};order=[root]
    for v in order:
        for u in adj[v]:
            if u!=parent[v]:parent[u]=v;order.append(u)
    feasible={v:({pins[v]} if v in pins else set(COLORS)) for v in vertices}
    for v in reversed(order[1:]):
        p=parent[v];feasible[p]={c for c in feasible[p] if feasible[v]-{c}}
    if not feasible[root]:return None
    col={root:min(feasible[root])}
    for v in order[1:]:col[v]=min(feasible[v]-{col[parent[v]]})
    return col

def reduce_two_trees(n,edges):
    """Occurrence splitting plus partitioned equality diamonds, then hub paths."""
    graph_ok(n,edges); incidence=[[] for _ in range(n)]; next_id=0
    for ei,(u,v) in enumerate(edges):incidence[u].append(ei);incidence[v].append(ei)
    occ=[];port={}
    for v in range(n):
        block=[]
        for ei in (incidence[v] or [-1]):
            block.append(next_id);port[(v,ei)]=next_id;next_id+=1
        occ.append(block)
    red=[];blue=[];diamonds=[]
    for block in occ:
        for x,y in zip(block,block[1:]):
            a,b=next_id,next_id+1;next_id+=2
            red.extend([(x,a),(a,b),(b,y)]);blue.extend([(x,b),(a,y)])
            diamonds.append((x,y,a,b))
    blue.extend((port[(u,i)],port[(v,i)]) for i,(u,v) in enumerate(edges))
    canon=lambda es:sorted(tuple(sorted(e)) for e in es)
    red,blue=canon(red),canon(blue);q=next_id;shared=list(range(q));trees=[]
    for forest in (red,blue):
        parts=components(shared,forest)
        if len(forest)!=q-len(parts):raise AssertionError('constructed forest has a cycle')
        hub=next_id;next_id+=1;joins=[];vs=shared+[hub];es=list(forest)
        for part in parts:
            mid=next_id;next_id+=1;endpoint=min(part);vs.append(mid)
            es.extend([(endpoint,mid),(mid,hub)]);joins.append((endpoint,mid,hub))
        trees.append({'vertices':vs,'edges':canon(es),'hub':hub,'joins':joins})
    return {'universe':next_id,'shared':shared,'occurrences':occ,'diamonds':diamonds,
            'red_forest':red,'blue_forest':blue,'trees':trees}

def lift_source(R,source):
    out={}
    for c,block in zip(source,R['occurrences']):
        for x in block:out[x]=c
    for x,y,a,b in R['diamonds']:
        other=[c for c in COLORS if c!=out[x]];out[a],out[b]=other
    for T in R['trees']:
        out[T['hub']]=0
        for endpoint,mid,hub in T['joins']:
            out[mid]=next(c for c in COLORS if c!=out[endpoint] and c!=out[hub])
    return out

def project_source(R,target):return tuple(target[block[0]] for block in R['occurrences'])

def valid_target(R,col):
    return set(col)==set(range(R['universe'])) and all(c in COLORS for c in col.values()) and all(
        col[u]!=col[v] for T in R['trees'] for u,v in T['edges'])

MAGIC='01010100'
def encode_pair(R):
    h=R['universe'];out=MAGIC+'1'*h+'0'
    for T in R['trees']:
        vs=set(T['vertices']);es=set(T['edges'])
        out+=''.join('1' if i in vs else '0' for i in range(h))
        out+=''.join('1' if (i,j) in es else '0' for i,j in it.combinations(range(h),2))
    return out

def decode_pair(bits):
    if type(bits) is not str or any(c not in '01' for c in bits) or not bits.startswith(MAGIC):
        raise ValueError('invalid binary header')
    stop=bits.find('0',len(MAGIC))
    if stop<0:raise ValueError('missing unary terminator')
    h=stop-len(MAGIC)
    if h<1 or len(bits)!=9+h*h+2*h:raise ValueError('wrong explicit length')
    offset=stop+1;trees=[]
    for _ in range(2):
        vs={i for i in range(h) if bits[offset+i]=='1'};offset+=h;es=[]
        for i,j in it.combinations(range(h),2):
            if bits[offset]=='1':es.append((i,j))
            offset+=1
        if any(i not in vs or j not in vs for i,j in es) or not tree_ok(vs,es):raise ValueError('invalid tree')
        trees.append({'vertices':sorted(vs),'edges':es})
    if set(trees[0]['vertices'])|set(trees[1]['vertices'])!=set(range(h)):raise ValueError('unused universe label')
    return {'universe':h,'trees':trees}

def solve_graph(n,edges):
    """Independent DSATUR backtracking oracle for finite tests, no reduction access."""
    graph_ok(n,edges);adj=[set() for _ in range(n)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    col=[-1]*n;nodes=0
    def visit(left):
        nonlocal nodes
        nodes+=1
        if not left:return tuple(col)
        v=max(left,key=lambda x:(len({col[u] for u in adj[x] if col[u]>=0}),len(adj[x]),-x))
        used={col[u] for u in adj[v]}
        for c in COLORS:
            if c not in used:
                col[v]=c;ans=visit(left-{v})
                if ans is not None:return ans
        col[v]=-1;return None
    return visit(set(range(n))),nodes

def local_batch(A):
    count=0
    for x,y in it.product(COLORS,repeat=2):
        ext=[(a,b) for a,b in it.product(COLORS,repeat=2)
             if x!=a and x!=b and a!=b and y!=a and y!=b]
        A.check(bool(ext)==(x==y),'diamond_exact_equality');count+=len(ext)
    for a,h in it.product(COLORS,repeat=2):A.check(any(m!=a and m!=h for m in COLORS),'length_two_join_is_total')
    # Three summaries on shared x and two other fixed boundary values.
    D=DAG();tree_parts=[([0,1],[(0,1)]),([0,2],[(0,2)]),([0,1,2],[(0,1),(1,2)])]
    roots=[tree_summary(D,vs,es,set(vs)) for vs,es in tree_parts]
    H=D.combine('and',roots);G,branches,met=D.forget(H,0)
    for a,b in it.product(COLORS,repeat=2):
        env={1:a,2:b};truth=[D.evaluate(H,env|{0:c}) for c in COLORS]
        A.check(D.evaluate(G,env)==any(truth),'three_summary_common_assignment')
        A.check([D.evaluate(r,env) for r in branches]==truth,'three_summary_support_roots')
        if any(truth):
            point=env|{0:truth.index(True)}
            for vs,es in tree_parts:
                w=tree_lift(vs,es,{v:point[v] for v in vs})
                A.check(w is not None and all(w[u]!=w[v] for u,v in es),'three_tree_internal_witness')
    A.check(met['after_support_gates']<=met['independent_gates']+3*met['dependent_gates']+2,'one_step_active_bound')
    A.check(met['new_gates']<=3*met['dependent_gates']+2,'one_step_allocation_bound')
    R=reduce_two_trees(2,[(0,1)]);s=encode_pair(R)
    A.check(decode_pair(s)['universe']==R['universe'],'total_bit_encoding_roundtrip')
    for bad in ('',s+'1',s[:-1],MAGIC+'0','x'+s,42):
        try:decode_pair(bad)
        except ValueError:A.check(True,'malformed_pair_rejected')
        else:A.check(False,'malformed_pair_rejected')
    return {'diamond_extensions':count,'one_shared_variable_metrics':met,'malformed_controls':6}

def circuits_batch(A,n):
    if not 1<=n<=5:raise ValueError('exhaustive circuit batch n<=5')
    pairs=list(it.combinations(range(n),2));rows=[]
    for mask in range(1<<len(pairs)):
        edges=[e for i,e in enumerate(pairs) if (mask>>i)&1]
        originals=[c for c in it.product(COLORS,repeat=n) if coloring(c,edges)]
        D=DAG();root=graph_circuit(D,n,edges);initial=D.size([root]);history=[];records=[]
        for v in range(n):
            root,branches,met=D.forget(root,v);history.append((v,branches));records.append(met)
            A.check(met['new_gates']<=3*met['dependent_gates']+2,'charged_created_gate_bound')
            A.check(met['after_support_gates']<=met['independent_gates']+3*met['dependent_gates']+2,'retained_support_size_bound')
            rem=list(range(v+1,n));project={tuple(c[x] for x in rem) for c in originals}
            for vals in it.product(COLORS,repeat=len(rem)):
                env=dict(zip(rem,vals));A.check(D.evaluate(root,env)==(vals in project),'all_prefix_exact_circuit_projection')
        sat=D.evaluate(root,{})
        A.check(sat==bool(originals),'circuit_complete_decision')
        witness=None
        if sat:
            env={}
            for v,bs in reversed(history):env[v]=next(c for c,b in enumerate(bs) if D.evaluate(b,env))
            witness=tuple(env[i] for i in range(n));A.check(witness in originals,'reverse_circuit_witness')
        rows.append({'edge_mask':mask,'models':len(originals),'initial_gates':initial,
                     'allocated_nodes':len(D.nodes),'steps':records,'witness':witness})
    return {'n':n,'graphs':len(rows),'rows':rows}

def reduction_batch(A,n,start=0,count=None):
    if not 1<=n<=5:raise ValueError('split reduction audit at n<=5')
    pairs=list(it.combinations(range(n),2));rows=[]
    stop=min(1<<len(pairs),start+count) if count is not None else 1<<len(pairs)
    if not 0<=start<stop:raise ValueError('invalid chunk')
    for mask in range(start,stop):
        edges=[e for i,e in enumerate(pairs) if (mask>>i)&1];R=reduce_two_trees(n,edges)
        s=sum(len(v) for v in R['occurrences']);t=len(R['diamonds']);q=len(R['shared'])
        A.check(t==s-n and q==s+2*t,'occurrence_gadget_size')
        A.check(len(components(R['shared'],R['red_forest']))==n,'red_path_components')
        A.check(len(components(R['shared'],R['blue_forest']))==s-len(edges),'blue_forest_components')
        for T in R['trees']:A.check(tree_ok(T['vertices'],T['edges']),'connected_tree_validity')
        A.check(set(R['trees'][0]['vertices'])&set(R['trees'][1]['vertices'])==set(R['shared']),'private_interiors_disjoint')
        code=encode_pair(R);parsed=decode_pair(code)
        A.check(parsed['universe']==R['universe'] and len(code)==9+R['universe']**2+2*R['universe'],'exact_bit_record')
        D=DAG();roots=[tree_summary(D,T['vertices'],T['edges'],set(R['shared'])) for T in R['trees']]
        H=D.combine('and',roots);source_models=0
        for c in it.product(COLORS,repeat=n):
            w=lift_source(R,c);yes=coloring(c,edges);source_models+=yes
            A.check(valid_target(R,w)==yes,'pointwise_constructed_target_equivalence')
            A.check(project_source(R,w)==c,'source_projection_identity')
            # Checking every original source assignment, but only its canonical gadget lift.
            shared={x:w[x] for x in R['shared']}
            A.check(D.evaluate(H,shared)==yes,'compiled_two_summary_equivalence')
        target_witness=None;nodes=None
        if n<=4 or mask in (0,(1<<len(pairs))-1):
            union=sorted(set(e for T in R['trees'] for e in T['edges']))
            target_witness,nodes=solve_graph(R['universe'],union)
            A.check((target_witness is not None)==bool(source_models),'independent_target_solver_decision')
            if target_witness is not None:
                back=project_source(R,dict(enumerate(target_witness)))
                A.check(coloring(back,edges),'independent_target_projection')
        rows.append({'edge_mask':mask,'source_models':source_models,'shared_variables':q,
                     'total_vertices':R['universe'],'tree_vertices':[len(T['vertices']) for T in R['trees']],
                     'summary_gates':[D.size([x]) for x in roots],'joint_gates':D.size([H]),
                     'target_solver_nodes':nodes,'target_solver_witness':target_witness})
    return {'n':n,'graphs':len(rows),'rows':rows,
            'limitation':'All source assignments are checked via one canonical lift; all target assignments are not exhaustively enumerated.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--batch',choices=['local','circuits','reduction'],required=True)
    p.add_argument('--n',type=int,default=4);p.add_argument('--out',type=Path,required=True);p.add_argument('--start',type=int,default=0);p.add_argument('--count',type=int);a=p.parse_args();A=Audit()
    result={'run_id':'TWOTREEBRIDGE1','status':'COMPUTATIONAL','batch':a.batch,'n':a.n,'start':a.start,'count':a.count,'randomness':'none',
            'timestamp_utc':datetime.now(timezone.utc).isoformat(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'failures':0}
    try:result['data']=local_batch(A) if a.batch=='local' else circuits_batch(A,a.n) if a.batch=='circuits' else reduction_batch(A,a.n,a.start,a.count)
    except Exception as exc:result['failures']=1;result['error']=repr(exc);raise
    finally:
        result.update(assertions=sum(A.counts.values()),counts=dict(A.counts),elapsed_seconds=time.monotonic()-A.start)
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('batch','n','assertions','failures','elapsed_seconds')}))
if __name__=='__main__':main()
