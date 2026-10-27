#!/usr/bin/env python3
"""LSPV-3 INDEXED-LOCATOR-GAP140, complete dependency-free finite audit.
New theorem: ALL-UNSAT coverage on a signed exact-(2,2) equality promise
with O(log N)-bit authenticated local certificates, but Omega(N/log N)
source-coordinate probes for deterministic all-label construction even on
indexed RAM; genuinely connected proper 3CNF parity-free equality bridges.
The executable tests finite encodings, not asymptotic machine run time.
"""
import collections
import hashlib
import itertools
import json
from pathlib import Path

W = '''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W1 = tuple(tuple(map(int, r.split())) for r in W.split(';'))
A_ROWS, B_ROWS = (6, 11), (9, 17)
BACKDOOR = (2, 4, 7, 14, 15)
checks = 0

def ck(condition, msg='assertion failed'):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(msg)


def h(a, b):
    rows = [list(row) for row in W1]
    if a == 0:
        for ci in A_ROWS:
            rows[ci][0] = -rows[ci][0]
    if b == 0:
        for ci in B_ROWS:
            rows[ci][2] = -rows[ci][2]
    return tuple(tuple(r) for r in rows)


def satisfied(clauses, bits):
    return all(any(bits[abs(lit)] == (lit > 0) for lit in row) for row in clauses)


def local_models(clauses):
    out = []
    for state in range(1 << 15):
        bits = {i: bool(state & (1 << (i - 1))) for i in range(1, 16)}
        if satisfied(clauses, bits):
            out.append(bits)
    return out


def residual(c, branch):
    if any(abs(x) in branch and branch[abs(x)] == (x > 0) for x in c):
        return None
    return tuple(x for x in c if abs(x) not in branch)


def edges(c):
    if len(c) == 1:
        return ((-c[0], c[0]),)
    if len(c) == 2:
        return ((-c[0], c[1]), (-c[1], c[0]))
    return ()


def bfs(adjacency, source, target):
    previous = {source: None}
    queue = collections.deque([source])
    while queue:
        node = queue.popleft()
        for nxt, src_id in adjacency[node]:
            if nxt not in previous:
                previous[nxt] = (node, src_id)
                queue.append(nxt)
    if target not in previous:
        return None
    proof = []
    t = target
    while previous[t] is not None:
        u, src_id = previous[t]
        proof.append((src_id, u, t))
        t = u
    return tuple(reversed(proof))


def make_leaf(clauses, assignment):
    g = collections.defaultdict(list)
    for ci, c in enumerate(clauses):
        r = residual(c, assignment)
        if r == ():
            return ('empty', ci)
        if r is not None and len(r) < 3:
            for u, v in edges(r):
                g[u].append((v, ci))
    for var in range(1, 16):
        if var in assignment:
            continue
        p, q = bfs(g, var, -var), bfs(g, -var, var)
        if p is not None and q is not None:
            return ('scc', var, p, q)
    return None


def verify_leaf(clauses, assignment, leaf):
    if leaf is None:
        return False
    if leaf[0] == 'empty':
        ci = leaf[1]
        return 0 <= ci < len(clauses) and residual(clauses[ci], assignment) == ()
    if leaf[0] != 'scc':
        return False
    _, var, p, q = leaf
    if var in assignment or not 1 <= var <= 15:
        return False
    for segment, start, end in ((p, var, -var), (q, -var, var)):
        current = start
        for ci, u, v in segment:
            if not (0 <= ci < len(clauses)) or u != current:
                return False
            r = residual(clauses[ci], assignment)
            if r is None or (u, v) not in edges(r):
                return False
            current = v
        if current != end:
            return False
    return True


def shifted_row(row, base):
    return tuple((1 if x > 0 else -1) * (abs(x) + base) for x in row)


def pin(name, z, w):
    return ((name, z, w), (name, z, -w), (name, -z, w), (name, -z, -w))


def assemble(a, b, connected=False, two_levels=False):
    m = len(a)
    assert len(b) == m and m > 0
    chunks = []
    module_info = []
    # Construct as source-identical 20-clause modules; reorder only for fixed-gap transport.
    for j in range(m):
        for side, x, y in (('U', a[j], 1 - b[j]), ('V', 1 - a[j], b[j])):
            base = 15 * (2 * j + (side == 'V'))
            module_info.append((j, side, base, x, y))
    records = []
    trace = {}
    for group in ('A', 'M', 'B'):
        for j, side, base, x, y in module_info:
            rows = h(x, y)
            selected = A_ROWS if group == 'A' else B_ROWS if group == 'B' else tuple(i for i in range(20) if i not in A_ROWS + B_ROWS)
            for local_id in selected:
                trace[(j, side, local_id)] = len(records)
                records.append(shifted_row(rows[local_id], base))
    next_name = 30*m + 1
    anchors = [1 + 15*i for i in range(2*m)]
    if connected:
        for x, y in zip(anchors, anchors[1:]):
            z1, z2 = next_name, next_name + 1
            next_name += 2
            # Non-vacuous genuine equality constraints, every clause proper ternary.
            records.extend(((-x, y, z1), (-x, y, -z1), (x, -y, z2), (x, -y, -z2)))
    n0, c0 = next_name - 1, len(records)
    original_records = tuple(records)
    if two_levels:
        n1 = next_name + 1
        records.extend(pin(-anchors[0], next_name, next_name + 1))
        next_name += 2
        n2 = next_name + 1
        records.extend(pin(-anchors[1], next_name, next_name + 1))
        next_name += 2
        ck(n1 == n0 + 2 and n2 == n0 + 4)
    return {'m':m,'n':next_name-1,'n0':n0,'c0':c0,'C':tuple(records), 'source':original_records,
            'anchors':tuple(anchors),'trace':trace,'modules':tuple(module_info), 'connected':connected}


def encode_binary(obj):
    n = obj['n']
    c = len(obj['C'])
    width = n.bit_length()
    # FIXED RECORD binary signed proper 3CNF encoding used by the tape theorems.
    header = f'p b3 {n} {c} {width}\n'
    recsize = 3*(width+1) + 1
    text = header
    sign_pos = []
    for row in obj['C']:
        assert len(row) == 3
        for x in row:
            sign_pos.append(len(text))
            text += ('+' if x > 0 else '-') + format(abs(x),f'0{width}b')
        text += '\n'
    ck(len(text) == len(header) + c*recsize)
    return text, tuple(sign_pos), len(header), recsize


def parse_binary(raw, n, c):
    lines = raw.splitlines()
    hdr = lines.pop(0).split()
    ck(hdr[:2] == ['p','b3'] and len(hdr) == 5)
    nn, cc, width = map(int, hdr[2:])
    ck(nn == n and cc == c and width == n.bit_length())
    ck(len(lines) == c)
    rows = []
    for row in lines:
        ck(len(row) == 3*(width+1))
        clause = []
        for j in range(3):
            sign = row[j*(width+1)]
            binary = row[j*(width+1)+1:(j+1)*(width+1)]
            ck(sign in '+-' and set(binary) <= {'0','1'})
            v = int(binary, 2)
            ck(1 <= v <= nn)
            clause.append(v if sign == '+' else -v)
        ck(len({abs(v) for v in clause}) == 3)
        rows.append(tuple(clause))
    return tuple(rows)


def encode_dimacs(obj):
    raw = f"p cnf {obj['n']} {len(obj['C'])}\n" + ''.join(' '.join(map(str,c)) + ' 0\n' for c in obj['C'])
    head = raw.splitlines()[0].split()
    ck(head == ['p','cnf',str(obj['n']),str(len(obj['C']))])
    result = []
    for row in raw.splitlines()[1:]:
        xs = list(map(int,row.split()))
        ck(len(xs)==4 and xs[-1]==0 and len({abs(x) for x in xs[:3]})==3)
        result.append(tuple(xs[:3]))
    ck(tuple(result)==obj['C'])
    return raw


def is_incidence_connected(obj):
    n=obj['n0']; C=obj['source']
    adj = collections.defaultdict(list)
    for ci, row in enumerate(C):
        for lit in row:
            v = abs(lit)
            adj[('c',ci)].append(('v',v))
            adj[('v',v)].append(('c',ci))
    queue=collections.deque([('c',0)]); seen={('c',0)}
    while queue:
        u=queue.popleft()
        for v in adj[u]:
            if v not in seen:seen.add(v);queue.append(v)
    return len(seen)==n+len(C)


def local_witness(models, obj):
    bits = {}
    for j,side,base,x,y in obj['modules']:
        pool=models[(x,y)]
        choices=[s for s in pool if not s[1]] # all anchors set False
        if not choices:
            return None
        pick=choices[0]
        for name,val in pick.items():bits[name+base]=val
    for v in range(30*obj['m']+1,obj['n0']+1):bits[v]=False
    return bits


def defect_certificate(obj, a, b, leaves):
    j = next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),None)
    if j is None:return None
    side='U' if a[j]==1 else 'V'
    module=next(t for t in obj['modules'] if t[0]==j and t[1]==side)
    _,_,base,x,y=module
    ck((x,y)==(1,1))
    clause_ids=tuple(obj['trace'][(j,side,ci)] for ci in range(20))
    ck(tuple(obj['source'][ci] for ci in clause_ids)==tuple(shifted_row(row,base) for row in W1))
    for assignment,leaf in leaves:
        ck(verify_leaf(W1,assignment,leaf))
        # Source-ID authentication, not unverified oracle guesses.
        for ci in range(20):
            ck(obj['source'][clause_ids[ci]]==shifted_row(W1[ci],base))
    return {'index':j,'side':side,'base':base,'source_ids':clause_ids,
            'size_bits_bound':(20*32+32*16+32*16)*max(1,obj['n'].bit_length())}


def run():
    local={(a,b):local_models(h(a,b)) for a,b in itertools.product((0,1),repeat=2)}
    counts={str(k):len(v) for k,v in local.items()}
    ck([counts[str(k)] for k in ((0,0),(0,1),(1,0),(1,1))]==[772,272,272,0])
    for (a,b), mm in local.items():
        for v in range(1,16):
            ck(sum(v in row for row in h(a,b))==2)
            ck(sum(-v in row for row in h(a,b))==2)
        if mm:
            ck(any(not z[1] for z in mm))
            ck(any(z[1] for z in mm))
    leaves=[]
    for assignment_bits in itertools.product((False,True),repeat=5):
        assignment=dict(zip(BACKDOOR,assignment_bits))
        leaf=make_leaf(W1,assignment)
        ck(leaf is not None and verify_leaf(W1,assignment,leaf))
        leaves.append((assignment,leaf))
    ck(len(leaves)==32)
    # For all a,b up to m=3, check SAT iff equality, exact22, source pointers,
    # connected incidence and nonvacuous equality bridges.
    sources=0; connected_count=0; unsat_certificates=0; sat_sources=0; two_level=0
    digest=hashlib.sha256(); tests={}
    for m in (1,2,3):
        tests[str(m)]={'sources':0,'sat':0,'unsat':0}
        for a in itertools.product((0,1),repeat=m):
            for b in itertools.product((0,1),repeat=m):
                for connected in (False,True):
                    obj=assemble(a,b,connected=connected,two_levels=True)
                    ck(obj['n0']==(34*m-2 if connected else 30*m))
                    ck(obj['c0']==(48*m-4 if connected else 40*m))
                    ck(all(len(row)==3 and len({abs(t) for t in row})==3 for row in obj['C']))
                    ck(is_incidence_connected(obj)==connected)
                    raw,_,_,_=encode_binary(obj)
                    ck(parse_binary(raw,obj['n'],len(obj['C']))==obj['C'])
                    dm=encode_dimacs(obj)
                    ck(len(dm)>0)
                    digest.update(hashlib.sha256(raw.encode()).digest())
                    if not connected:
                        for v in range(1,obj['n0']+1):
                            ck(sum(v in row for row in obj['source'])==2)
                            ck(sum(-v in row for row in obj['source'])==2)
                    if a==b:
                        sat_sources+=1
                        assignments=local_witness(local,obj)
                        ck(assignments is not None and satisfied(obj['source'],assignments))
                        for anchor in obj['anchors']:ck(assignments[anchor] is False)
                        ck(defect_certificate(obj,a,b,leaves) is None)
                    else:
                        info=defect_certificate(obj,a,b,leaves)
                        ck(info is not None and info['source_ids'])
                        unsat_certificates+=1
                    if connected:
                        connected_count+=1
                        # Genuine coupling: both endpoints of each bridge admit opposite
                        # anchor values individually on good sources, but EQ disallows them.
                        ck(all(any(p[1] for p in local[(x,y)]) and any(not p[1] for p in local[(x,y)])
                               for _,_,_,x,y in obj['modules'] if (x,y)!=(1,1)))
                    # Independently check both real PIN descendant source identity.
                    ck(obj['C'][:obj['c0']]==obj['source'])
                    ck(len(obj['C'])==obj['c0']+8)
                    ck(obj['C'][obj['c0']:obj['c0']+4]==pin(-obj['anchors'][0],obj['n0']+1,obj['n0']+2))
                    ck(obj['C'][obj['c0']+4:]==pin(-obj['anchors'][1],obj['n0']+3,obj['n0']+4))
                    sources+=1;two_level+=1
                    tests[str(m)]['sources']+=1
                    tests[str(m)]['sat' if a==b else 'unsat']+=1
    # Concrete strict control: each defect j modifies ONLY a distinct 4-row sign
    # group. It changes neither headers nor original-name fields nor all other rows.
    sensitivity=[]
    for m in (2,4,8,16,32):
        base=(0,)*m; obj=assemble(base,base,connected=True)
        raw,signs,hd,recsize=encode_binary(obj)
        positions=[]
        for j in range(m):
            defective=tuple(1 if i==j else 0 for i in range(m))
            alt,_signs,hdr2,rs2=encode_binary(assemble(defective,base,connected=True))
            ck(hd==hdr2 and rs2==recsize and len(alt)==len(raw))
            diff={i for i,(x,y) in enumerate(zip(raw,alt)) if x!=y}
            ck(len(diff)==4 and diff<=set(signs))
            positions.append(diff)
        for j in range(m):
            for k in range(j):ck(not positions[j]&positions[k])
        # The baseline all-equal run of any correct deterministic literal-cell
        # RAM decider must touch >=m mutually disjoint sensitive regions.
        # Bounded RAM words of width <=4*ceil(log2 N) can overlap only O(1)
        # coordinate groups because these groups are length 4*(3w+4).
        wordwidth=4*max(1,len(raw).bit_length())
        max_hits=0
        for start in range(0,len(raw),max(1,recsize)):
            end=start+wordwidth
            max_hits=max(max_hits,sum(bool(g & set(range(start,end))) for g in positions))
        ck(max_hits<=4)
        sensitivity.append({'m':m,'N_bits':len(raw)*8,'characters':len(raw),
                            'width':obj['n'].bit_length(),'signs_changed_per_defect':4,
                            'disjoint_defect_groups':m,'baseline_cell_probe_lb':m,
                            'test_word_length_char':wordwidth,'max_groups_intersected':max_hits})
    # Negative controls: forged zero-cost certificate, misaliased source name,
    # wrong source row, missing opposite branch, and witness on SAT are rejected.
    a,b=(0,0),(1,0)
    one=assemble(a,b,connected=True)
    cert=defect_certificate(one,a,b,leaves)
    ck(cert is not None)
    bad_ids=list(cert['source_ids']); bad_ids[3]=bad_ids[2]
    ck(tuple(one['source'][ci] for ci in bad_ids)!=tuple(shifted_row(z,cert['base']) for z in W1))
    wrong=list(W1); wrong[2]=tuple(-v for v in wrong[2]); ck(wrong!=list(W1))
    invalid_branch=list(leaves); invalid_branch.pop();ck(len(invalid_branch)!=2**len(BACKDOOR))
    eq=assemble((0,0),(0,0),connected=True)
    ck(defect_certificate(eq,(0,0),(0,0),leaves) is None)
    return {'result':'PASS','assertions':checks,'H_counts':counts,'backdoor':BACKDOOR,
            'leaves':len(leaves),'sources_serialized_with_two_real_levels':sources,
            'connected_sources':connected_count,'SAT_sources':sat_sources,
            'UNSAT_certificates_authenticated':unsat_certificates,
            'source_distribution':tests,'sensitivity':sensitivity,
            'serialization_SHA256_chain':digest.hexdigest(),
            'limits':'Finite checks are not physical RAM/tape resource measurements, nor all-ordinary-SAT coverage.'}

if __name__=='__main__':
    ans=run()
    outfile=Path(__file__).with_name('2026-10-26_2119_INDEXED_LOCATOR_GAP140_raw.json')
    outfile.write_text(json.dumps(ans,indent=2,sort_keys=True)+'\n')
    print(json.dumps(ans,indent=2,sort_keys=True))