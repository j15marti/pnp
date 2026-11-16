#!/usr/bin/env python3
"""TMR-4/057: exact, no-advice read-once-formula-to-OBDD compiler audit.

Python 3.10+, standard library only. Deterministic seed 20261115.
Source: root binary tree, each leaf exactly once x0..x(n-1), internal gate
one of sixteen two-input Boolean truth tables, all nodes unique.
"""
import json
import random
from functools import lru_cache
from collections import defaultdict

SEED = 20261115
rng = random.Random(SEED)
res = dict(revision="tmr4-ershov057.v1", seed=SEED, cases=0,
           assignments=0, stage_steps=0, target_edges=0,
           count_checks=0, rank_checks=0, optimum_checks=0,
           malformed_rejections=0, assertions=0, examples=[])


def check(cond, reason):
    res['assertions'] += 1
    if not cond:
        raise AssertionError(reason)


def gate(code, a, b):
    return (code >> (2 * a + b)) & 1


def make_tree(n, mode):
    """Construct tree gate records, with root and leaf names, no layout advice."""
    parts = [f'x{i}' for i in range(n)]
    gates = {}
    while len(parts) > 1:
        if mode == 'chain':
            i, j = 0, 1
        elif mode == 'balanced':
            i, j = 0, 1
        else:
            i = rng.randrange(len(parts)); j = rng.randrange(len(parts) - 1)
            if j >= i:
                j += 1
        a, b = parts[i], parts[j]
        for p in sorted([i,j], reverse=True):
            parts.pop(p)
        name = f'g{len(gates)}'
        gates[name] = dict(a=a, b=b, op=rng.randrange(16))
        if mode == 'balanced':
            parts.append(name)
        elif mode == 'chain':
            parts.insert(0, name)
        else:
            parts.insert(rng.randrange(len(parts) + 1), name)
    return dict(n=n, gates=gates, root=parts[0])


def validate(source):
    n = source.get('n'); gs = source.get('gates'); root = source.get('root')
    if type(n) is not int or n < 1 or not isinstance(gs, dict) or len(gs) != n - 1:
        raise ValueError('size/encoding')
    if set(gs) != {f'g{i}' for i in range(n-1)}:
        raise ValueError('gate identifiers')
    use = defaultdict(int)
    for gid, g in gs.items():
        if not isinstance(g, dict) or set(g) != {'a','b','op'} or type(g['op']) is not int or not 0 <= g['op'] < 16:
            raise ValueError('gate encoding')
        for child in [g['a'],g['b']]:
            if child not in gs and child not in {f'x{i}' for i in range(n)}:
                raise ValueError('missing reference')
            use[child] += 1
    if root not in gs and root not in {f'x{i}' for i in range(n)}:
        raise ValueError('missing output')
    use[root] += 1  # pseudo output consumer
    ids = set(gs) | {f'x{i}' for i in range(n)}
    if any(use[k] != 1 for k in ids):
        raise ValueError('sharing/repeated-variable/dead/invalid tree')
    marks = set(); active = set()
    def visit(v):
        if v in active:
            raise ValueError('cycle')
        if v in marks:
            return
        active.add(v)
        if v in gs:
            visit(gs[v]['a']); visit(gs[v]['b'])
        active.remove(v); marks.add(v)
    visit(root)
    if marks != ids:
        raise ValueError('disconnected or cyclic')


def schedule(source):
    """Sethi-Ullman / Ershov labeling and fully computed topological order."""
    gs = source['gates']; label = {}
    def number(v):
        if v not in gs:
            label[v] = 1
        else:
            a,b = gs[v]['a'],gs[v]['b']; p,q = number(a),number(b)
            label[v] = p + 1 if p == q else max(p,q)
        return label[v]
    width = number(source['root'])
    order = []
    def emit(v):
        if v in gs:
            a,b = gs[v]['a'],gs[v]['b']
            if label[a] >= label[b]:
                emit(a); emit(b)
            else:
                emit(b); emit(a)
        order.append(v)
    emit(source['root'])
    check(len(order) == 2 * source['n'] - 1, 'every original node once')
    return order, width, label


def frontier(source, order):
    gs = source['gates']; last = {v:-1 for v in order}
    for p, v in enumerate(order):
        if v in gs:
            last[gs[v]['a']] = max(last[gs[v]['a']],p)
            last[gs[v]['b']] = max(last[gs[v]['b']],p)
    last[source['root']] = len(order)
    live = [tuple(v for v in order[:p+1] if last[v] > p) for p in range(len(order))]
    return live


def simulate(source, order, live, x):
    value = {}; gs = source['gates']
    for p, v in enumerate(order):
        if v in gs:
            a,b,op = gs[v]['a'],gs[v]['b'],gs[v]['op']
            value[v] = gate(op, value[a], value[b]); res['stage_steps'] += 1
        else:
            value[v] = x[int(v[1:])]
        for u in live[p]:
            check(u in value, 'source retained value exists')
    return value[source['root']]


def stages(source, order, live):
    gs = source['gates']; ends = [p for p in range(len(order)) if p == len(order)-1 or order[p+1].startswith('x')]
    stage_list = []; begin = 0; prior = ()
    for end in ends:
        seq = order[begin:end+1]
        check(seq[0].startswith('x'), 'stage starts original read')
        check(all(u.startswith('g') for u in seq[1:]), 'all stage gates follow input')
        s = dict(input=int(seq[0][1:]), before=prior, after=live[end], gates=seq[1:])
        stage_list.append(s)
        prior = s['after']; begin=end+1
    check(len(stage_list)==source['n'] and begin==len(order), 'full coverage')
    return stage_list


def step(source, s, values, bit):
    gs = source['gates']; vals = dict(zip(s['before'],values))
    vals[f'x{s["input"]}'] = bit
    for v in s['gates']:
        g=gs[v]
        check(g['a'] in vals and g['b'] in vals,'real predecessor availability')
        vals[v] = gate(g['op'], vals[g['a']], vals[g['b']])
        res['stage_steps']+=1
    return tuple(vals[v] for v in s['after'])


def compile_bp(source, s_list, width):
    nodes=0; current={():1}; table=[]
    for s in s_list:
        nxt=defaultdict(int); transitions={}
        for state, multiplicity in current.items():
            nodes+=1
            for b in (0,1):
                target=step(source,s,state,b)
                nxt[target]+=multiplicity
                transitions[state,b]=target
                res['target_edges']+=1
        table.append((transitions,dict(nxt)))
        current=dict(nxt)
    check(nodes<=source['n']*2**width,'OBDD size')
    final_index=s_list[-1]['after'].index(source['root'])
    total=sum(q for state,q in current.items() if state[final_index]==1)
    return table,nodes,total


def direct_count(source):
    """Independent exact tree formula counting, each left/right input set disjoint."""
    gs=source['gates']
    def tally(v):
        if v not in gs:
            return (1,1)
        g=gs[v]; a=tally(g['a']); b=tally(g['b']); out=[0,0]
        for i in (0,1):
            for j in (0,1):
                out[gate(g['op'],i,j)] += a[i]*b[j]
        return tuple(out)
    return tally(source['root'])[1]


def optimum_by_ideal_dp(source):
    """Independent exhaustive over ALL topological orders via ideal subset DP."""
    n=source['n']; gs=source['gates']; vertices=[f'x{i}' for i in range(n)]+list(gs)
    ix={v:i for i,v in enumerate(vertices)}
    dep=[0]*len(vertices); consumers=[0]*len(vertices)
    for v,g in gs.items():
        for x in [g['a'],g['b']]:
            dep[ix[v]] |= 1<<ix[x]
            consumers[ix[x]] |= 1<<ix[v]
    consumers[ix[source['root']]] |= 1<<len(vertices) # virtual output
    full=(1<<len(vertices))-1
    @lru_cache(None)
    def dp(mask):
        if mask==full:
            return 0
        best=len(vertices)+1
        for i,v in enumerate(vertices):
            bit=1<<i
            if mask&bit or dep[i]&mask !=dep[i]:
                continue
            m2=mask|bit
            width=sum(1 for j in range(len(vertices)) if m2&(1<<j) and (consumers[j]&~m2))
            best=min(best,max(width,dp(m2)))
        return best
    return dp(0)


def source_eval(source,x):
    gs=source['gates']
    def ev(v):
        if v not in gs:
            return x[int(v[1:])]
        g=gs[v]
        return gate(g['op'],ev(g['a']),ev(g['b']))
    return ev(source['root'])


def rank_mod(mat,p):
    m=[row[:] for row in mat]; rows=len(m); cols=len(m[0]); h=0
    for c in range(cols):
        piv=next((j for j in range(h,rows) if m[j][c]%p),None)
        if piv is None: continue
        m[h],m[piv]=m[piv],m[h]
        inv=pow(m[h][c],-1,p)
        for k in range(c,cols): m[h][k]=m[h][k]*inv%p
        for j in range(rows):
            if j==h: continue
            z=m[j][c]
            if z:
                for k in range(c,cols): m[j][k]=(m[j][k]-z*m[h][k])%p
        h+=1
        if h==rows: break
    return h


def inspect(src,kind,check_optimum=False):
    validate(src)
    order,r,labels=schedule(src)
    live=frontier(src,order)
    w=max(map(len,live))
    check(w==r,'SU width equality')
    check(r<=1+(src['n'].bit_length()-1),'log leaf bound')
    s=stages(src,order,live)
    bp,nodes,count=compile_bp(src,s,r)
    check(count==direct_count(src),'exact weighted acceptance')
    res['count_checks']+=1
    if check_optimum:
        opt=optimum_by_ideal_dp(src)
        check(opt==r,'all-topological-order optimum')
        res['optimum_checks']+=1
    if src['n']<=8:
        actual=0
        for mask in range(1<<src['n']):
            x=tuple((mask>>i)&1 for i in range(src['n']))
            expected=source_eval(src,x)
            check(expected==simulate(src,order,live,x),'original gate semantics')
            state=()
            for stage_index,ss in enumerate(s):
                nxt=bp[stage_index][0][state,x[ss['input']]]
                check(nxt==step(src,ss,state,x[ss['input']]),'read-once stage transition')
                state=nxt
            check(state[s[-1]['after'].index(src['root'])]==expected,'terminal target')
            actual+=expected;res['assignments']+=1
        check(actual==count,'brute count')
        order_inputs=[ss['input'] for ss in s]
        for t in range(src['n']+1):
            A=order_inputs[:t]; B=order_inputs[t:]; mat=[]
            for u in range(1<<len(A)):
                row=[]
                for v in range(1<<len(B)):
                    bits=[0]*src['n']
                    for j,i in enumerate(A):bits[i]=(u>>j)&1
                    for j,i in enumerate(B):bits[i]=(v>>j)&1
                    row.append(source_eval(src,bits))
                mat.append(row)
            measured=len(s[t-1]['after']) if t else 0
            for p in (2,101):
                check(rank_mod(mat,p)<=1<<measured,'field rank vs actual boundary width')
                res['rank_checks']+=1
    res['cases']+=1
    if len(res['examples'])<18:
        res['examples'].append(dict(kind=kind,n=src['n'],structural_r=r,actual_width=w,
                                    internal_nodes=nodes,exact_count=count,order=order[:25]))


for n in range(1,9):
    for mode in ('chain','balanced'):
        inspect(make_tree(n,mode),mode,True)
    for t in range(18):
        inspect(make_tree(n,'random'),'random', n<=7 and t<8)
for n in (9,10,12,16,24,32,48,64):
    for mode in ('chain','balanced','random'):
        inspect(make_tree(n,mode),mode,False)
for change in ('bad_ref','duplicated_variable','shared_gate','cycle','bad_opcode','wrong_count','dead_gate'):
    s=make_tree(4,'balanced')
    if change=='bad_ref': s['gates']['g0']['a']='x99'
    if change=='duplicated_variable': s['gates']['g0']['a']=s['gates']['g0']['b']
    if change=='shared_gate':
        s['gates']['g2']['a']=s['gates']['g1']['a']
    if change=='cycle': s['gates']['g0']['a']='g0'
    if change=='bad_opcode': s['gates']['g0']['op']=16
    if change=='wrong_count': s['n']=5
    if change=='dead_gate': s['root']='x0'
    try: validate(s)
    except ValueError: res['malformed_rejections']+=1
    else: raise AssertionError('accepted malformed '+change)
# A known high structural width, cheap semantic shortcut: balanced AND tree.
def and_tree(n):
    gs={}; frontier=[f'x{i}' for i in range(n)]
    while len(frontier)>1:
        nxt=[]
        for j in range(0,len(frontier),2):
            if j+1==len(frontier): nxt.append(frontier[j]);continue
            gid=f'g{len(gs)}';gs[gid]=dict(a=frontier[j],b=frontier[j+1],op=8);nxt.append(gid)
        frontier=nxt
    return dict(n=n,gates=gs,root=frontier[0])
for n in (8,16,32,64,128):
    tree=and_tree(n)
    validate(tree)
    order,r,_=schedule(tree)
    check(r==n.bit_length(),'balanced AND tree structural width')
    check(direct_count(tree)==1,'one satisfying assignment AND')
    if len(res['examples'])<22:
        res['examples'].append(dict(kind='AND cheap semantic stream',n=n,structural_r=r,
                                    count=1,alternative='scan every bit, maintain running AND'))
res['failures']=0
print(json.dumps(res,sort_keys=True,separators=(',',':')))
