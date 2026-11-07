#!/usr/bin/env python3
"""Independent LSPV-5 audit of the LSPV-1/459 5/4 Hall-kernel control."""
from __future__ import annotations
import hashlib, json, resource, time

NEIGH = ((0,1,2),(0,1,3),(0,2,3),(1,2,3),(0,1,2))

def canon(xs):
    s=set(xs)
    if any(-x in s for x in s): return None
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def build_source():
    edge={}; nxt=1
    for i in range(5):
        for h in NEIGH[i]: edge[i,h]=nxt; nxt+=1
    clauses=[canon(edge[i,h] for h in NEIGH[i]) for i in range(5)]
    pairs=[]
    for h in range(4):
        members=[i for i in range(5) if h in NEIGH[i]]
        for ai in range(len(members)):
            for bi in range(ai+1,len(members)):
                i,k=members[ai],members[bi]; z=nxt; nxt+=1
                a,b=-edge[i,h],-edge[k,h]
                first=len(clauses)
                clauses += [canon((a,b,z)),canon((a,b,-z))]
                pairs.append({'hole':h,'pigeons':[i,k],'edge_vars':[edge[i,h],edge[k,h]],'z':z,'source_ids':[first,first+1]})
    assert len(clauses)==47 and nxt-1==36 and len(pairs)==21
    return edge,clauses,pairs

def eval_clause(c,bits):
    return any(((bits>>(abs(x)-1))&1)==(1 if x>0 else 0) for x in c)

def deletion_witnesses(clauses,pairs):
    out={}; scans=0; clause_tests=0
    pair_of_source={sid:(j,which) for j,p in enumerate(pairs) for which,sid in enumerate(p['source_ids'])}
    for deleted in range(len(clauses)):
        found=None
        for edge_bits in range(1<<15):
            scans+=1
            bits=edge_bits
            bad=False
            for r in range(5):
                if r==deleted: continue
                clause_tests+=1
                if not eval_clause(clauses[r],bits): bad=True; break
            if bad: continue
            okay=True
            for j,p in enumerate(pairs):
                x,y=p['edge_vars']
                collision=((bits>>(x-1))&1) and ((bits>>(y-1))&1)
                ids=p['source_ids']
                if collision and deleted not in ids: okay=False; break
                if collision:
                    # Make the surviving pad clause true and the deleted one false.
                    which=pair_of_source[deleted][1]
                    ztrue=(which==1) # deleting +z means z=false; deleting -z means z=true
                    if ztrue: bits |= 1<<(p['z']-1)
                # With no collision, z=false is sufficient because a negative edge literal is true.
            if not okay: continue
            valid=True
            for i,c in enumerate(clauses):
                if i==deleted: continue
                clause_tests+=1
                if not eval_clause(c,bits): valid=False; break
            clause_tests+=1
            if valid and not eval_clause(clauses[deleted],bits):
                found=bits; break
        assert found is not None, deleted
        out[str(deleted)]=found
    return out,scans,clause_tests

def resolution(c,d,p):
    assert p in c and -p in d
    return canon(tuple(x for x in c if x!=p)+tuple(x for x in d if x!=-p))

def proof(clauses,pairs):
    # IDs are strings S0..S46 and R0..; this differs from the peer's numeric serialization.
    db={'S%d'%i:c for i,c in enumerate(clauses)}; nodes=[]; active={clauses[i]:'S%d'%i for i in range(5)}
    def add(a,b,p,stage):
        out=resolution(db[a],db[b],p); rid='R%d'%len(nodes)
        db[rid]=out; nodes.append({'id':rid,'left':a,'right':b,'pivot':p,'stage':stage,'clause':list(out)})
        return rid
    for p in pairs:
        s0,s1=p['source_ids']; rid=add('S%d'%s0,'S%d'%s1,p['z'],'pad')
        active[db[rid]]=rid
    for pivot in range(1,16):
        vals=list(active.values()); pos=[r for r in vals if pivot in db[r]]; neg=[r for r in vals if -pivot in db[r]]
        nxt={db[r]:r for r in vals if pivot not in db[r] and -pivot not in db[r]}
        for a in pos:
            for b in neg:
                c=resolution(db[a],db[b],pivot)
                if c is None or c in nxt: continue
                rid=add(a,b,pivot,'dp'); nxt[c]=rid
        active=nxt
        if () in active: break
    root=active[()]
    by={n['id']:n for n in nodes}; needed=set(); stack=[root]
    while stack:
        x=stack.pop()
        if x.startswith('R') and x not in needed:
            needed.add(x); stack += [by[x]['left'],by[x]['right']]
    kept=[n for n in nodes if n['id'] in needed]
    sources=set(); depth={'S%d'%i:0 for i in range(47)}
    for n in kept:
        depth[n['id']]=1+max(depth[n['left']],depth[n['right']])
    stack=[root]; seen=set()
    while stack:
        x=stack.pop()
        if x in seen: continue
        seen.add(x)
        if x.startswith('S'): sources.add(int(x[1:]))
        else: stack += [by[x]['left'],by[x]['right']]
    return kept,root,len(nodes),len(active),max(depth.values()),sources

def main():
    start=time.monotonic(); edge,clauses,pairs=build_source()
    witnesses,witness_scans,witness_clause_tests=deletion_witnesses(clauses,pairs)
    nodes,root,candidates,active_final,span,sources=proof(clauses,pairs)
    source_text='p cnf 36 47\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
    result={
      'run':'LSPV-5/REFEREE397 Hall-kernel independent audit','status':'COMPUTATIONAL_EXACT_FINITE',
      'source_model':'degree-three graph-PHP with private pad variable per collision pair',
      'neighborhoods':[''.join(map(str,x)) for x in NEIGH],
      'variables':36,'source_clauses':47,'collision_pairs':21,'source_dimacs':source_text,
      'source_sha256':hashlib.sha256(source_text.encode()).hexdigest(),
      'clauses':[list(c) for c in clauses],'pairs':pairs,'deletion_witnesses':witnesses,
      'witness_search_edge_assignments':witness_scans,'witness_search_clause_tests':witness_clause_tests,
      'proof_nodes':nodes,'root':root,'candidate_inferences_before_prune':candidates,
      'retained_inferences':len(nodes),'pad_inferences':sum(n['stage']=='pad' for n in nodes),
      'dp_inferences':sum(n['stage']=='dp' for n in nodes),'source_ancestors':sorted(sources),'span':span,
      'minimum_interval':[46,len(nodes)],
      'host':{'seconds':round(time.monotonic()-start,6),'ru_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
      'scope':'native strict RES semantic trace; not historical accepted-byte R_mix341 replay; not a mixed lower bound; B3 OPEN'
    }
    assert len(nodes)==92 and sum(n['stage']=='pad' for n in nodes)==21 and span==12 and len(sources)==47
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
