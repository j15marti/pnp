#!/usr/bin/env python3
"""Construct source-authenticated strict Resolution proof gluing over port assignments.
Deterministic, standard library only; no semantic proof steps, no new inference rules.
"""
import json, hashlib, random, itertools, pathlib, sys, time, resource

ROOT = pathlib.Path(__file__).resolve().parent

def norm(lits):
    t=set(lits)
    if any(-x in t for x in t):
        raise ValueError('tautology not permitted in canonical source')
    if any(x == 0 for x in t):
        raise ValueError('zero literal')
    return tuple(sorted(t,key=lambda x:(abs(x),x<0)))

def parse(text):
    if not isinstance(text,str) or not text.endswith('\n'): raise ValueError('missing newline')
    lines = [s.strip() for s in text.splitlines() if s.strip() and not s.lstrip().startswith('c')]
    if not lines or len(lines[0].split())!=4: raise ValueError('bad header')
    h=lines[0].split()
    if h[:2]!=['p','cnf']: raise ValueError('bad header magic')
    try: nv,nc=map(int,h[2:])
    except Exception: raise ValueError('bad counts')
    if nv<1 or nc<1 or nc>10000: raise ValueError('bad bounds')
    clauses=[]
    for s in lines[1:]:
        try: nums=list(map(int,s.split()))
        except Exception: raise ValueError('nonnumeric')
        if not nums or nums[-1]!=0 or 0 in nums[:-1]: raise ValueError('missing or embedded terminator')
        if any(abs(i)>nv for i in nums[:-1]): raise ValueError('out of range')
        if len(set(nums[:-1]))!=len(nums[:-1]): raise ValueError('duplicate literal')
        clauses.append(norm(nums[:-1]))
    if len(clauses)!=nc: raise ValueError('clause count')
    if any(i not in set(abs(x) for c in clauses for x in c) for i in range(1,nv+1)):
        raise ValueError('unused name')
    return nv,clauses

def dimacs(n,clauses):
    return f'p cnf {n} {len(clauses)}\n' + ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def restrict(c, env):
    if any((lit>0)==env[abs(lit)] for lit in c if abs(lit) in env): return None
    return tuple(lit for lit in c if abs(lit) not in env)

def resolve(a,b,v):
    if v not in a or -v not in b: raise ValueError('not a pivot')
    t=(set(a)-{v}) | (set(b)-{-v})
    if any(-x in t for x in t): raise ValueError('tautological resolvent')
    return norm(t)

def is_sat(n,clauses):
    for bits in itertools.product((False,True), repeat=n):
        if all(any((l>0)==bits[abs(l)-1] for l in c) for c in clauses): return [int(x) for x in bits]
    return None

def residual_proof(sources, env):
    """Full finite closure, then prune; all source indices authentic."""
    res=[]; bank={}; root=None; trials=0
    for j,c in enumerate(sources):
        rc=restrict(c,env)
        if rc is None: continue
        if rc not in bank:
            bank[rc]=len(res)
            res.append({'kind':'source','source':j,'clause':list(rc)})
        if not rc:
            root=bank[rc]; break
    if root is None:
        cursor=0
        while cursor<len(res) and root is None:
            # Saturate all legal strict binary RES pairs, breadth-first in node index.
            for j in range(cursor):
                a=tuple(res[j]['clause']); b=tuple(res[cursor]['clause'])
                for x in a:
                    if -x in b:
                        trials+=1
                        try: r=resolve(a,b,abs(x)) if x>0 else resolve(b,a,abs(x))
                        except ValueError: continue
                        if r in bank: continue
                        idx=len(res)
                        bank[r]=idx
                        if x>0: pa,pb=j,cursor
                        else: pa,pb=cursor,j
                        res.append({'kind':'res','p':pa,'q':pb,'pivot':abs(x),'clause':list(r)})
                        if not r: root=idx; break
                if root is not None: break
            cursor+=1
    if root is None: raise ValueError('SAT residual, unable to refute')
    seen=set()
    def back(i):
        if i in seen:return
        seen.add(i)
        if res[i]['kind']=='res': back(res[i]['p']); back(res[i]['q'])
    back(root)
    order=sorted(seen); trans={old:new for new,old in enumerate(order)}
    out=[]
    for i in order:
        d=dict(res[i])
        if d['kind']=='res': d['p']=trans[d['p']];d['q']=trans[d['q']]
        out.append(d)
    return out, trans[root], trials, len(res)

def derive(sources,ports):
    n=max(abs(x) for c in sources for x in c)
    assert len(set(ports))==len(ports) and all(1<=x<=n for x in ports)
    if is_sat(n,sources) is not None: raise ValueError('requires UNSAT')
    m=len(sources); global_nodes=[{'kind':'source','clause':list(c)} for c in sources]
    leaves={}; stats={'closure_trials':0,'total_closure_nodes':0,'retained_residual_paid':0,'replayed_paid':0,'merges':0,'bypassed_restricted_steps':0}
    for vals in itertools.product((0,1),repeat=len(ports)):
        env=dict(zip(ports, map(bool,vals)))
        steps,root,trials,nclosure=residual_proof(sources,env)
        stats['closure_trials']+=trials; stats['total_closure_nodes']+=nclosure
        B=set((x if not env[x] else -x) for x in ports)
        localglobal=[]; localres=[]
        for entry in steps:
            D=set(entry['clause'])
            if entry['kind']=='source':
                idx=entry['source']
            else:
                stats['retained_residual_paid']+=1
                p=localglobal[entry['p']];q=localglobal[entry['q']];v=entry['pivot']
                pc=set(global_nodes[p]['clause']);qc=set(global_nodes[q]['clause'])
                if v in pc and -v in qc:
                    clause=resolve(pc,qc,v)
                    idx=len(global_nodes)
                    global_nodes.append({'kind':'res','p':p,'q':q,'pivot':v,'clause':list(clause)})
                    stats['replayed_paid']+=1
                elif v not in pc:
                    idx=p;stats['bypassed_restricted_steps']+=1
                else:
                    assert -v not in qc
                    idx=q;stats['bypassed_restricted_steps']+=1
            assert set(global_nodes[idx]['clause']) <= D|B, (entry,global_nodes[idx])
            localglobal.append(idx)
            localres.append(entry)
        final=localglobal[root]
        assert set(global_nodes[final]['clause']) <= B
        leaves[''.join(map(str,vals))]={'partial':list(vals),'residual':localres,'root':root,'lifted_root':final,'closure_count':nclosure,'closure_tests':trials}
    def combine(prefix,depth):
        if depth==len(ports): return leaves[prefix]['lifted_root']
        x=ports[depth]
        a=combine(prefix+'0',depth+1)
        b=combine(prefix+'1',depth+1)
        A=set(global_nodes[a]['clause']);B=set(global_nodes[b]['clause'])
        if x not in A: return a
        if -x not in B: return b
        clause=resolve(A,B,x)
        idx=len(global_nodes);global_nodes.append({'kind':'res','p':a,'q':b,'pivot':x,'clause':list(clause)})
        stats['merges']+=1
        return idx
    result=combine('',0)
    assert global_nodes[result]['clause']==[]
    stats.update({'actual_paid':len(global_nodes)-m,'leaf_count':len(leaves),'limit':stats['retained_residual_paid'] + 2**len(ports)-1,'source_nodes':m})
    assert stats['actual_paid']<=stats['limit']
    return {'n':n,'ports':ports,'source':dimacs(n,sources),'nodes':global_nodes,'leaves':leaves,'root':result,'stats':stats}

def build_cases():
    cases=[]
    cases.append(('port_two_arms',3,[(1,2),(1,-2),(-1,3),(-1,-3)],[1]))
    cases.append(('all_2_port_blockers',2,[(1,2),(1,-2),(-1,2),(-1,-2)],[1,2]))
    cases.append(('two_ports_deep',4,[(1,3),(1,-3),(-1,4),(-1,-4),(2,3),(2,-3)],[1,2]))
    cases.append(('three_bit_all_blockers',3,list(itertools.product(*[(i,-i) for i in range(1,4)])),[1,2]))
    cases.append(('horn_chain_6',6,[(1,)]+[(-i,i+1) for i in range(1,6)]+[(-6,)],[1,3]))
    cases.append(('peitl_4_6',4,[(1,2),(3,4),(-1,-3),(-2,-4),(1,-2,-3,4),(-1,2,3,-4)],[1,2]))
    cases.append(('all_3_port_blockers',3,list(itertools.product(*[(i,-i) for i in range(1,4)])),[1,2,3]))
    return cases

def main():
    t0=time.perf_counter(); cases=[]; sat=[]; malformed=0
    for name,n,raw,ports in build_cases():
        cs=[norm(c) for c in raw]
        nv,parsed=parse(dimacs(n,cs)); assert (nv,parsed)==(n,cs)
        if name=='two_ports_deep':
            # ensure the padded duplicate side does not create a false SAT control
            pass
        p=derive(cs,ports); p['name']=name;cases.append(p)
        for j in (0,len(cs)//2,len(cs)-1):
            neighbor=cs[:j]+cs[j+1:]
            sat.append({'base':name,'remove':j,'witness':is_sat(n,neighbor)})
    for bad in ['p cnf 2 1\n1 0\n2 0\n','p cnf 2 1\n3 0\n','p cnf 2 1\na 0\n','p cNF 2 1\n1 0\n','p cnf 2 1\n1 2\n','p cnf 2 1\n1 1 0\n','p cnf 2 1\n1 -1 0\n','p cnf 2 1\n1 0']:
        try: parse(bad)
        except ValueError:malformed+=1
        else: raise AssertionError('accepted malformed: '+bad)
    # SAT positive controls known to be SAT
    for n,clauses in [(2,[(1,2),(-1,2)]),(3,[(1,),(2,3)]),(4,[(1,2),(3,4)]), (3,[(1,2),(-1,2),(-2,3)])]:
        cs=[norm(c) for c in clauses];assert is_sat(n,cs) is not None
        try:derive(cs,[1])
        except ValueError:pass
        else:raise AssertionError('SAT derivation accepted')
    raw={'claim':'PORT-SPLIT-GLUE357','status':'EXPLICIT RES UPPER CERTIFICATES; NOT GLOBAL MINIMA','cases':cases,'sat_deletion_controls':sat,'malformed_rejected':malformed,'sat_positive':4,'timestamp':'2026-11-03 02:43 PST'}
    payload=json.dumps(raw,sort_keys=True,separators=(',',':'))+'\n'
    (ROOT/'lspv2_357_port_split_proofs.json').write_text(payload)
    result={'case_count':len(cases),'total_paid':sum(x['stats']['actual_paid'] for x in cases),'total_limit':sum(x['stats']['limit'] for x in cases),'raw_sha256':hashlib.sha256(payload.encode()).hexdigest(),'per_case':[{ 'name':x['name'], 'ports':x['ports'], 'paid':x['stats']['actual_paid'], 'limit':x['stats']['limit'], 'leaf_cost':x['stats']['retained_residual_paid'], 'merges':x['stats']['merges'], 'trials':x['stats']['closure_trials']} for x in cases], 'malformed_rejected':malformed,'wall_seconds':round(time.perf_counter()-t0,5),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/'lspv2_357_summary.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if __name__=='__main__':main()