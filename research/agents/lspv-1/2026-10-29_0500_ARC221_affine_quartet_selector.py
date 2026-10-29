#!/usr/bin/env python3
"""ARC221: source-authenticated XOR3 quartet recognition and affine certificate.

One deterministic polynomial-time algorithm recognizes an exactly specified
subclass of 3CNF. It produces either a verified SAT witness or a verified
GF(2) inconsistency combination; outside the recognized subclass it returns
UNKNOWN. It does not solve arbitrary SAT. Python bitset operations are a
reference implementation, not native TM step measurements.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
import json, math, random, time, zipfile, importlib.util

SEED = 22120261029
ROOT = Path(__file__).resolve().parent


def canonical_clause(clause):
    c=tuple(sorted(clause,key=lambda x:(abs(x),x<0)))
    if not c or any(abs(v)==abs(u) for i,v in enumerate(c) for u in c[:i]):
        raise ValueError('empty/duplicate-variable clause unsupported')
    return c


def serialize(n,clauses):
    lines=[f'p cnf {n} {len(clauses)}\n']
    for c in clauses:
        lines.append(' '.join(map(str,canonical_clause(c)))+' 0\n')
    return ''.join(lines).encode('ascii')


def parse(data):
    try: lines=data.decode('ascii').splitlines(keepends=True)
    except (UnicodeError,AttributeError) as e: raise ValueError('not ascii input') from e
    if not lines or not all(s.endswith('\n') for s in lines):
        raise ValueError('unterminated line')
    header=lines[0].split()
    if len(header)!=4 or header[:2]!=['p','cnf']:
        raise ValueError('bad header')
    n,m=map(int,header[2:])
    if n<1 or n>len(data)+1 or m<0 or m>len(data) or len(lines)!=m+1:
        raise ValueError('bad size')
    source=[];offsets=[]; offset=len(lines[0])
    for line in lines[1:]:
        words=list(map(int,line.split()))
        if not words or words[-1]!=0 or 0 in words[:-1]:
            raise ValueError('invalid terminator')
        c=canonical_clause(words[:-1])
        if any(abs(v)>n for v in c): raise ValueError('literal out of range')
        source.append(c)
        offsets.append(offset);offset+=len(line)
    return n,source,offsets


def parity(x):
    return x.bit_count()&1


def xor3_clauses(scope,rhs):
    """Four 3-clauses falsified exactly by the opposite-parity assignments."""
    assert len(scope)==3 and len(set(scope))==3 and rhs in (0,1)
    ans=[]
    for mask in range(8):
        if parity(mask)==rhs: continue
        c=tuple(-v if (mask>>i)&1 else v for i,v in enumerate(scope))
        ans.append(canonical_clause(c))
    assert len(ans)==4
    return ans


def extract(source):
    """Accept precisely a disjoint union of exact four-clause XOR3 quartets.

    A pair (scope, rhs, source-index quartet) authenticates each extracted row.
    This is an exact syntax check: no semantic equivalence solver is assumed.
    """
    groups=defaultdict(list)
    for i,c in enumerate(source):
        if len(c)!=3: return None
        scope=tuple(sorted(abs(v) for v in c))
        groups[scope].append(i)
    rows=[]
    for scope,idxs in sorted(groups.items()):
        if len(idxs)!=4: return None
        signed=set(source[i] for i in idxs)
        if len(signed)!=4: return None
        if signed==set(xor3_clauses(scope,0)):
            rhs=0
        elif signed==set(xor3_clauses(scope,1)):
            rhs=1
        else: return None
        rows.append({'scope':scope,'rhs':rhs,'sources':tuple(idxs)})
    return rows


def verify_rows(source,rows):
    found=set()
    for row in rows:
        scope,rhs,idxs=row['scope'],row['rhs'],row['sources']
        if len(scope)!=3 or not all(0<=i<len(source) for i in idxs):return False
        if len(set(idxs))!=4 or any(i in found for i in idxs):return False
        if set(source[i] for i in idxs)!=set(xor3_clauses(scope,rhs)):return False
        found.update(idxs)
    return found==set(range(len(source)))


def equation_masks(rows):
    return [(sum(1<<(v-1) for v in r['scope']),r['rhs']) for r in rows]


def gaussian(n,rows):
    """Square-free bit-mask GF(2) elimination, storing complete row provenance.

    Every basis row is (variable mask, rhs, mask over original equation ids).
    Output certificate is either n-bit assignment or equation-id combination.
    """
    basis={}; reduction_xors=0; peak_basis=0
    for rid,(mask,rhs) in enumerate(equation_masks(rows)):
        combo=1<<rid
        while mask:
            low=(mask&-mask).bit_length()-1
            if low not in basis:
                basis[low]=(mask,rhs,combo)
                peak_basis=max(peak_basis,len(basis));break
            oldmask,oldrhs,oldcombo=basis[low]
            mask^=oldmask;rhs^=oldrhs;combo^=oldcombo;reduction_xors+=1
        else:
            if rhs:
                proof=[j for j in range(len(rows)) if combo>>j&1]
                return {'status':'NO','equations':proof,'reduction_xors':reduction_xors,
                        'peak_basis':peak_basis,'max_indexed_row_bits':n+len(rows)+1}
    assignment=0
    for low in sorted(basis,reverse=True):
        mask,rhs,_=basis[low]
        higher=mask & ~(1<<low)
        value=rhs^parity(higher&assignment)
        assignment|=(value<<low)
    assert all(parity(mask&assignment)==rhs for mask,rhs in equation_masks(rows))
    return {'status':'YES','witness_mask':assignment,'reduction_xors':reduction_xors,
            'peak_basis':peak_basis,'max_indexed_row_bits':n+len(rows)+1}


def verify_certificate(n,source,rows,result):
    if not verify_rows(source,rows):return False
    if result['status']=='YES':
        w=result['witness_mask']
        if w<0 or w>=1<<n:return False
        return all(any(((w>>(abs(l)-1))&1)==int(l>0) for l in c) for c in source)
    if result['status']=='NO':
        indexes=result['equations']
        if not indexes or len(set(indexes))!=len(indexes):return False
        mask,rhs=0,0
        for i in indexes:
            if not 0<=i<len(rows):return False
            rm,rb=equation_masks(rows)[i]
            mask^=rm;rhs^=rb
        return mask==0 and rhs==1
    return False

YES_BASE=b'p cnf 3 1\n1 2 3 0\n'
NO_BASE=b'p cnf 1 2\n1 0\n-1 0\n'


def decide(data):
    try:n,source,offs=parse(data)
    except (ValueError,TypeError,OverflowError):
        return {'status':'INVALID','route':'parser'}
    rows=extract(source)
    if rows is None: return {'status':'UNKNOWN','route':'not-pure-quartets','child':data}
    result=gaussian(n,rows)
    assert verify_certificate(n,source,rows,result)
    result['route']='authenticated-affine'
    result['rows']=rows
    result['child']=YES_BASE if result['status']=='YES' else NO_BASE
    result['input_bytes']=len(data)
    result['child_bytes']=len(result['child'])
    result['certificate_bytes']=len(json.dumps({
        'status':result['status'], 'equation_combination':result.get('equations'),
        'witness_mask':result.get('witness_mask'),
        'source_groups':[r['sources'] for r in rows]}))
    return result


def grid_quartets(L,flip=False):
    assert L>=3
    def idx(r,c):return r*L+c+1
    scopes=[]
    for r in range(L):
        for c in range(L-2):scopes.append((idx(r,c),idx(r,c+1),idx(r,c+2)))
    for r in range(L-2):
        for c in range(L):scopes.append((idx(r,c),idx(r+1,c),idx(r+2,c)))
    clauses=[]
    for i,scope in enumerate(scopes):
        clauses.extend(xor3_clauses(scope,int(flip and i==0)))
    return serialize(L*L,clauses),scopes



def cubic_toroidal_tseitin(L,flip=False):
    """Cubic graph from four-cycle vertex gadgets of an LxL toroidal grid.

    Vertices: (r,c,port) with port 0=N,1=E,2=S,3=W. Each has two
    intragadget neighbors and one external neighbor, giving degree exactly 3.
    Edges of this graph are Boolean variables. Each vertex imposes one
    XOR3 equation on its three incident edge variables. Only dependency
    among the GF(2) rows is the XOR of all vertex equations.
    """
    assert L>=3
    verts=[(r,c,p) for r in range(L) for c in range(L) for p in range(4)]
    edges=set()
    def add(u,v):
        assert u!=v
        e=tuple(sorted((u,v))); assert e not in edges;edges.add(e)
    for r in range(L):
        for c in range(L):
            for p in range(4):add((r,c,p),(r,c,(p+1)%4))
            add((r,c,1),(r,(c+1)%L,3))
            add((r,c,2),((r+1)%L,c,0))
    ordered=sorted(edges);edgeno={e:j+1 for j,e in enumerate(ordered)}
    incident=defaultdict(list)
    for e,num in edgeno.items():
        u,v=e;incident[u].append(num);incident[v].append(num)
    assert len(verts)==4*L*L and len(edges)==6*L*L
    assert all(len(incident[v])==3 for v in verts)
    clauses=[];first=verts[0]
    for v in verts:
        clauses.extend(xor3_clauses(tuple(sorted(incident[v])),int(flip and v==first)))
    return serialize(len(edges),clauses),{'vertices':len(verts),'edges':len(edges),
       'equations':len(verts),'clauses':len(clauses),'grid_L':L}


def brute(source,n):
    for mask in range(1<<n):
        if all(any(((mask>>(abs(l)-1))&1)==int(l>0) for l in c) for c in source):return True
    return False


def independent_grid_inconsistency(L):
    data,scopes=grid_quartets(L,True)
    rows=extract(parse(data)[1]); assert rows
    index={r['scope']:i for i,r in enumerate(rows)}
    def idx(r,c):return r*L+c+1
    block=[tuple(idx(r,c) for c in range(3)) for r in range(3)] + [tuple(idx(r,c) for r in range(3)) for c in range(3)]
    ids=[index[s] for s in block]
    mask,rhs=0,0
    for i in ids:
        rm,rb=equation_masks(rows)[i];mask^=rm;rhs^=rb
    assert mask==0 and rhs==1
    return ids


def load_arc220():
    p=ROOT/'ARC220_adaptive_dual_parameter_repro.py'
    if not p.exists():return None
    spec=importlib.util.spec_from_file_location('arc220_prev',p)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod



def tri_portfolio(data):
    """One deterministic program: authenticated affine -> ARC220 width/backdoor.

    The ARC220 file is bundled source, not a remote oracle or hidden advice.
    The recognized child is always one of two physically serialized bases.
    A non-recognized input returns UNKNOWN, never a guessed answer.
    """
    if data==YES_BASE:
        return {'phase':'terminal','status':'YES','child':None,'route':'base'}
    if data==NO_BASE:
        return {'phase':'terminal','status':'NO','child':None,'route':'base'}
    a=decide(data)
    if a['status'] in ('YES','NO'):
        return {'phase':'successor','status':a['status'],'child':a['child'],
                'route':'affine','proof':a}
    if a['status']=='INVALID':
        return {'phase':'invalid','status':'INVALID','child':None,'route':'parser'}
    mod=load_arc220()
    if mod is None:return {'phase':'unresolved','status':'UNKNOWN','child':data,'route':'missing-fixed-code'}
    result=mod.portfolio(data)
    if result['status'] in ('YES','NO'):
        return {'phase':'successor','status':result['status'],
                'child':YES_BASE if result['status']=='YES' else NO_BASE,
                'route':result['route'],'proof':result['proof']}
    return {'phase':'unresolved','status':'UNKNOWN','child':data,'route':'identity'}


def test():
    rng=random.Random(SEED)
    stats=defaultdict(int); controls={};start=time.monotonic()
    for n in range(3,9):
        scopes=list(combinations(range(1,n+1),3))
        for trial in range(85):
            k=rng.randint(0,min(8,len(scopes)))
            chosen=rng.sample(scopes,k)
            clauses=[]
            for s in chosen:clauses.extend(xor3_clauses(s,rng.randrange(2)))
            rng.shuffle(clauses)
            data=serialize(n,clauses)
            result=decide(data)
            assert result['status'] in ('YES','NO')
            assert result['status']=='YES' if brute(clauses,n) else result['status']=='NO'
            assert verify_certificate(n,clauses,result['rows'],result)
            assert len(result['child'])<100
            stats['random_cases']+=1
            stats['sat' if result['status']=='YES' else 'unsat']+=1
    # Every subset of the eight 3-clauses on a single 3-variable scope.
    universe=[canonical_clause(tuple(-v if mask>>i&1 else v for i,v in enumerate((1,2,3)))) for mask in range(8)]
    recognized=0
    for selection in range(256):
        clauses=[universe[i] for i in range(8) if selection>>i&1]
        result=decide(serialize(3,clauses))
        if result['status'] in ('YES','NO'):
            recognized+=1
            assert result['status']=='YES'
        else:assert result['status']=='UNKNOWN'
        stats['subset_controls']+=1
    assert recognized==3  # empty, even-falsifier quartet, odd-falsifier quartet
    controls['recognized_subsets']=recognized
    for L in [3,4]:
        for flip in (False,True):
            data,_=grid_quartets(L,flip)
            n,source,_=parse(data);result=decide(data)
            assert result['status']==('NO' if flip else 'YES')
            assert result['status']=='YES' if brute(source,n) else result['status']=='NO'
            assert verify_certificate(n,source,result['rows'],result)
            stats['brute_grid_controls']+=1
    for L in [8,16,24]:
        for flip in (False,True):
            data,scopes=grid_quartets(L,flip)
            n,source,_=parse(data)
            result=decide(data)
            assert result['status']==('NO' if flip else 'YES')
            assert verify_certificate(n,source,result['rows'],result)
            # In induced primal graph, an LxL grid is a subgraph: tw>=L-1.
            # Disjoint horizontal triples: one in every row, block columns in triples.
            # At least L*floor(L/3) variables in a hitting backdoor.
            h=int(math.log2(len(data)))
            backdoor_lb=L*(L//3)
            grid_tw_lb=L-1
            controls[f'L{L}_{"UNSAT" if flip else "SAT"}']={
                'N_bytes':len(data),'n':n,'clauses':len(source),
                'equations':len(result['rows']), 'minfill_width_lb':grid_tw_lb,
                'backdoor_lb':backdoor_lb,'ARC220_threshold':h,
                'evades_both_for_this_N':grid_tw_lb>h and backdoor_lb>h,
                'status':result['status'],'proof_equations':len(result.get('equations',[])),
                'cert_bytes':result['certificate_bytes'],'child_bytes':result['child_bytes'],
                'reduction_xors':result['reduction_xors'],
                'peak_basis':result['peak_basis']}
            if L==24:assert controls[f'L{L}_{"UNSAT" if flip else "SAT"}']['evades_both_for_this_N']
            if flip:
                six=independent_grid_inconsistency(L)
                assert len(six)==6
                stats['independent_six_equation_controls']+=1
            stats['large_grid_controls']+=1
    # A stronger hostile control: cubic Tseitin graph. Every SAT/UNSAT instance
    # has the same connected scopes. The only equation-dependency is all rows,
    # so the UNSAT parity-combination proof uses *every* equation.
    for L in [3,6,12,24]:
        for flip in (False,True):
            data,info=cubic_toroidal_tseitin(L,flip)
            n,source,_=parse(data)
            result=decide(data)
            assert result['status']==('NO' if flip else 'YES')
            assert verify_certificate(n,source,result['rows'],result)
            count=defaultdict(lambda:[0,0])
            for clause in source:
                for lit in clause:count[abs(lit)][0 if lit>0 else 1]+=1
            assert len(count)==n and all(x==[4,4] for x in count.values())
            if flip:assert len(result['equations'])==info['equations']
            h=int(math.log2(len(data)))
            # Contract each vertex four-cycle gadget to recover toroidal grid.
            # Any strong-2CNF syntactic backdoor must hit every source quartet,
            # and each Boolean variable occurs in exactly two scopes.
            # Hence backdoor size >= |V|/2 = 2L^2.
            tw_lb=L-1;backdoor_lb=2*L*L
            tag=f'CUBIC_L{L}_{"UNSAT" if flip else "SAT"}'
            controls[tag]={**info,'N_bytes':len(data),'status':result['status'],
                'source_exact_positive_negative':[4,4],
                'proven_affine_min_refutation_equations':info['equations'] if flip else None,
                'certificate_equations':len(result.get('equations',[])),
                'certificate_bytes':result['certificate_bytes'],
                'peak_basis':result['peak_basis'],
                'backdoor_lb':backdoor_lb,'treewidth_lb':tw_lb,
                'ARC220_threshold':h,
                'evades_both_for_this_N':tw_lb>h and backdoor_lb>h}
            if L==24:assert tw_lb>h and backdoor_lb>h
            stats['cubic_tseitin_controls']+=1
    # Mixed 2CNF + XOR gadget demonstrates non-universality.
    mixed=list(xor3_clauses((4,5,6),0))+[(1,4),(2,5),(3,6)]
    mixed_result=decide(serialize(6,mixed))
    assert mixed_result['status']=='UNKNOWN'
    stats['mixed_rejected']+=1
    # Unified portfolio: pure affine branch and non-affine width/backdoor
    # branch both produce true terminal children under one fixed program.
    da,_=cubic_toroidal_tseitin(3,True)
    route=tri_portfolio(da)
    assert route['route']=='affine' and route['status']=='NO'
    assert tri_portfolio(route['child'])['phase']=='terminal'
    for clauses in [[(1,2,3)],[(1,2,3),(-1,-2,-3)],[(1,),(-1,)]]:
        data=serialize(3,clauses)
        route=tri_portfolio(data)
        assert route['status'] in ('YES','NO')
        assert route['status']==('YES' if brute(clauses,3) else 'NO')
        if route['phase']!='terminal':
            assert tri_portfolio(route['child'])['phase']=='terminal'
        stats['tri_portfolio_non_affine_controls']+=1
    stats['tri_portfolio_affine_two_level_controls']+=1
    # Syntactic corruption of a quartet is not accepted as affine.
    c=list(xor3_clauses((1,2,3),0));assert decide(serialize(3,c[:-1]))['status']=='UNKNOWN'
    stats['incomplete_quartet_rejected']+=1
    c[0]=(1,2,3)
    assert decide(serialize(3,c))['status']=='UNKNOWN'
    stats['corrupted_quartet_rejected']+=1
    # Forge UNSAT evidence: empty subset cannot certify a contradiction.
    data,_=grid_quartets(3,True);n,source,_=parse(data);r=decide(data)
    fake=dict(r);fake['equations']=[]
    assert not verify_certificate(n,source,r['rows'],fake)
    stats['forged_certificate_rejected']+=1
    # ARC220 exact heuristic for L=24 SAT case; skip expensive failed backdoor branching.
    mod=load_arc220()
    if mod is not None:
        data,_=grid_quartets(24,False);n,source,_=parse(data)
        started=time.monotonic();order,peak=mod.minfill(source,n)
        controls['ARC220_minfill_L24']={'width':peak,'threshold':int(math.log2(len(data))),
          'ordering_variables':len(order),'wall_seconds':round(time.monotonic()-started,3)}
        assert peak>int(math.log2(len(data)))
        stats['arc220_minfill_hostile_tests']+=1
    stats['elapsed_seconds']=round(time.monotonic()-start,3)
    stats['source']='ARC221 full implementation and independently checked grid-six-row equation certificate'
    out={'status':'PASS','seed':SEED,'stats':dict(stats),'controls':controls}
    (ROOT/'ARC221_affine_quartet_raw.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':test()
