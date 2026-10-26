#!/usr/bin/env python3
"""LSPV-3 VERTEX-CUT-CRITICALITY134. Python 3 stdlib, deterministic.
Source-authenticated cubic Tseitin minimality and degree-3 GF(2)-PC audits.
Finite tests support, but do not replace, the symbolic proofs in companion tex.
"""
import itertools, collections, json, hashlib, argparse, sys
from pathlib import Path

counts=collections.Counter()
def check(cond,name):
    counts[name]+=1
    if not cond: raise AssertionError(name)

def cubic_graph(n,edges,preserve_order=False):
    E=[tuple(sorted((int(u),int(v)))) for u,v in edges]
    check(len(set(E))==len(edges),'no_duplicate_graph_edge')
    if not preserve_order:E.sort()
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(E,1):
        check(u!=v and 0<=u<v<n,'simple_edge')
        adj[u].append((v,i));adj[v].append((u,i))
    check(all(len(a)==3 for a in adj),'cubic')
    return E,adj

def honeycomb(r):
    assert r>=3
    def vid(i,j,b): return 2*((i%r)*r+(j%r))+b
    E=[]
    for i in range(r):
        for j in range(r):
            v=vid(i,j,0)
            for u in (vid(i,j,1),vid(i-1,j,1),vid(i,j-1,1)):
                E.append((v,u))
    E,adj=cubic_graph(2*r*r,E,preserve_order=True)
    return E,adj

def bridged_k4():
    edges=[]
    for offset in (0,4):
        for a,b in itertools.combinations(range(4),2):
            if (a,b)!=(0,1):edges.append((a+offset,b+offset))
    edges += [(0,8),(1,8),(4,9),(5,9),(8,9)]
    return cubic_graph(10,edges)

def k4():return cubic_graph(4,list(itertools.combinations(range(4),2)))

def prism(r):
    e=[]
    for i in range(r):
        e.extend([(i,(i+1)%r),(r+i,r+(i+1)%r),(i,r+i)])
    return cubic_graph(2*r,e)

def comps_minus(adj,v):
    n=len(adj); unvisited=set(range(n))-{v};out=[]
    while unvisited:
        start=min(unvisited);unvisited.remove(start);todo=[start]; comp={start}
        while todo:
            u=todo.pop()
            for w,e in adj[u]:
                if w in unvisited:
                    unvisited.remove(w);comp.add(w);todo.append(w)
        out.append(comp)
    return out

def is_connected(adj):
    n=len(adj);todo=[0];reached={0}
    while todo:
        for w,e in adj[todo.pop()]:
            if w not in reached:reached.add(w);todo.append(w)
    return len(reached)==n

def parity_clauses(adj,charges):
    clauses=[];groups=[]
    for v,inc in enumerate(adj):
        ids=tuple(sorted(e for w,e in inc)); g=[]
        for word in itertools.product((0,1),repeat=3):
            if (sum(word)&1)==charges[v]:continue
            clause=tuple((-eid if bit else eid) for eid,bit in zip(ids,word))
            clauses.append(clause);g.append((tuple(word),clause))
        check(len(g)==4,'quartet_count')
        groups.append(g)
    return clauses,groups

def dimacs(clauses,variables):
    s=f'p cnf {variables} {len(clauses)}\n';off=[]
    for c in clauses:
        off.append(len(s));s+=' '.join(map(str,c))+' 0\n'
    return s,off

def clause_at(data,ptr):
    if not isinstance(ptr,int) or not (0<=ptr<len(data)) or (ptr>0 and data[ptr-1]!='\n'):
        return None
    q=data.find('\n',ptr)
    if q<0:return None
    try: a=tuple(map(int,data[ptr:q].split()))
    except (ValueError,TypeError):return None
    if len(a)!=4 or a[-1]!=0 or any(z==0 for z in a[:3]):return None
    return a[:3]

def authenticate_paired_source(data,adj,charges,offset_by_v,allow_extras=True):
    """Independently authenticate actual source offsets, literal identities and odd parity.
    This is a SOUND UNSAT terminal for ANY valid input (including extra clauses),
    but it covers only formulas containing the supplied complete odd Tseitin witness.
    """
    if len(charges)!=len(adj) or len(offset_by_v)!=len(adj):return False
    if any(x not in (0,1) for x in charges) or sum(charges)%2!=1:return False
    header=data.split('\n',1)[0].split()
    if len(header)!=4 or header[:2]!=['p','cnf']:return False
    try: n,m=int(header[2]),int(header[3])
    except ValueError:return False
    if n<3*len(adj)//2:return False
    lines=data.splitlines()
    if len(lines)!=m+1:return False
    for v,inc in enumerate(adj):
        if len(offset_by_v[v])!=4:return False
        actual=[clause_at(data,p) for p in offset_by_v[v]]
        if any(x is None for x in actual):return False
        ids=tuple(sorted(e for _,e in inc))
        expected=[]
        for w in itertools.product((0,1),repeat=3):
            if sum(w)%2 != charges[v]:expected.append(tuple(-eid if bit else eid for eid,bit in zip(ids,w)))
        if sorted(actual)!=sorted(expected):return False
    return True

def gf2_consistent(nvar,rows):
    piv={}
    for ids,rhs in rows:
        x=0
        for e in ids:x^=1<<(e-1)
        y=rhs&1
        while x:
            top=x.bit_length()-1
            if top not in piv:
                piv[top]=(x,y);break
            u,v=piv[top];x^=u;y^=v
        else:
            if y:return False
    return True

def deletion_witness_satisfiable(adj,charges,v,word):
    """Independent GF2 elimination of all other vertex parity constraints and fixed incident edges."""
    ids=tuple(sorted(e for _,e in adj[v])); fixed=dict(zip(ids,word)); rows=[]
    for u in range(len(adj)):
        if u==v:continue
        rows.append(([e for _,e in adj[u]],charges[u]))
    for e,w in fixed.items():rows.append(([e],w))
    return gf2_consistent(3*len(adj)//2,rows)

def predicted_clause_essential(adj,charges,v,word):
    fixed=dict(zip(sorted(e for _,e in adj[v]),word))
    for block in comps_minus(adj,v):
        rhs=sum(charges[u] for u in block)&1
        left=0
        for u in block:
            for z,e in adj[u]:
                if z==v:left^=fixed[e]
        if left!=rhs:return False
    return True

def brute_sat(clauses,n):
    for a in range(1<<n):
        if all(any(((a>>(abs(z)-1))&1)==int(z>0) for z in c) for c in clauses):return True
    return False

# Multilinear polynomial over GF(2), a frozenset of monomial tuples.
def p_add(a,b):return a.symmetric_difference(b)
def p_mul(a,b):
    out=set()
    for x in a:
        for y in b:
            z=tuple(sorted(set(x)|set(y)))
            if z in out:out.remove(z)
            else:out.add(z)
    return frozenset(out)
def p_clause(c):
    out=frozenset([()])
    for lit in c:
        if lit>0:part=frozenset([(),(lit,)])
        else:part=frozenset([(abs(lit),)])
        out=p_mul(out,part)
    return out

def expected_boundary_poly(adj,vertices,charges):
    coef=set();rhs=0
    for v in vertices:
        rhs^=charges[v]
        for _,e in adj[v]:
            if e in coef:coef.remove(e)
            else:coef.add(e)
    terms={(e,) for e in coef}
    if rhs:terms.add(())
    return frozenset(terms)

def pc_audit_honeycomb(r, adj, clauses, charges, source, offsets):
    q=len(adj);E=3*q//2
    # All derivation steps are axioms or binary ADD. We independently verify every local polynomial identity.
    groups={v:clauses[4*v:4*v+4] for v in range(q)}
    summaries=collections.Counter(); local={}
    def record(p,label):
        summaries['lines']+=1;summaries['polynomial_monomials']+=len(p)
        summaries['degree_peak']=max(summaries['degree_peak'],max((len(x) for x in p),default=0))
        summaries['single_line_peak_terms']=max(summaries['single_line_peak_terms'],len(p))
        summaries['symbolic_bits_estimate']+=max(1,len(p))*max(1,E.bit_length())+3*E.bit_length()
        summaries['kind_'+label]+=1
    for v in range(q):
        ids=tuple(sorted(e for _,e in adj[v]))
        acc=None
        for j,c in enumerate(groups[v]):
            p=p_clause(c);record(p,'axiom')
            check(clause_at(source,offsets[4*v+j])==c,'pc_axiom_exact_source_line')
            if acc is None:acc=p
            else:
                acc=p_add(acc,p);record(acc,'add')
        target=frozenset(set((e,) for e in ids)|({()} if charges[v] else set()))
        check(acc==target,'pc_local_parity_identity')
        local[v]=acc
    def cell(i,j):
        v=2*(i*r+j)
        out=p_add(local[v],local[v+1]);record(out,'add')
        check(out==expected_boundary_poly(adj,(v,v+1),charges),'pc_cell_boundary')
        return out
    def quad(i,j,width):
        if width==1:return cell(i,j)
        z=width//2
        # Entire subregions always contain both endpoints of each cell's matching edge.
        A=quad(i,j,z);B=quad(i,j+z,z);C=quad(i+z,j,z);D=quad(i+z,j+z,z)
        AB=p_add(A,B);record(AB,'add')
        CD=p_add(C,D);record(CD,'add')
        out=p_add(AB,CD);record(out,'add')
        verts=[2*(x*r+y)+b for x in range(i,i+width) for y in range(j,j+width) for b in (0,1)]
        check(out==expected_boundary_poly(adj,verts,charges),'pc_rectangle_boundary')
        return out
    check(r&(r-1)==0,'dyadic_r')
    final=quad(0,0,r)
    check(final==frozenset([()]),'pc_final_one_unsat')
    check(summaries['lines']==8*q-1,'pc_linear_line_count')
    # This count is an exact symbolic certificate record accounting, not a machine-space measurement.
    return dict(summaries)


def canonical_honeycomb_edge_ids(r,vertex):
    """Independent direct O(log N)-addressable edge naming e(i,j,t)=3*(i*r+j)+t+1."""
    cell,b=divmod(vertex,2);i,j=divmod(cell,r)
    e=lambda x,y,t:3*((x%r)*r+(y%r))+t+1
    if b==0:return tuple(sorted((e(i,j,0),e(i,j,1),e(i,j,2))))
    return tuple(sorted((e(i,j,0),e(i+1,j,1),e(i,j+1,2))))

def verify_odd_honeycomb_stream(source,r,records):
    """One-way record stream: no revisits to earlier guess bits.
    Each record contains one charged bit and 4 source byte offsets.
    Ordinary CNF arbitrary extras allowed. The certificate is checked
    by direct deterministic canonical variable IDs, not a supplied matching table.
    """
    if type(r)!=int or r<3 or 2*r*r>len(source):return False
    lines=source.splitlines()
    head=lines[0].split() if lines else []
    if len(head)!=4 or head[:2]!=['p','cnf']:return False
    try:n,m=map(int,head[2:])
    except ValueError:return False
    if n<3*r*r or len(lines)!=m+1 or m<8*r*r:return False
    it=iter(records);parity=0
    for v in range(2*r*r):
        try:charge,offsets=next(it)
        except (StopIteration,TypeError,ValueError):return False
        if charge not in (0,1) or not isinstance(offsets,(tuple,list)) or len(offsets)!=4:return False
        parity^=charge
        ids=canonical_honeycomb_edge_ids(r,v)
        expected=[]
        for w in itertools.product((0,1),repeat=3):
            if sum(w)%2!=charge:
                expected.append(tuple(-e if bit else e for e,bit in zip(ids,w)))
        observed=[clause_at(source,p) for p in offsets]
        if any(c is None for c in observed) or sorted(observed)!=sorted(expected):return False
    try:next(it);return False
    except StopIteration:return parity==1

def restrict_ordinary(clauses,assignment):
    out=[]
    for row in clauses:
        if any(abs(z) in assignment and int(z>0)==assignment[abs(z)] for z in row):continue
        child=tuple(z for z in row if abs(z) not in assignment)
        out.append(child)
    return out

def stream_and_descendant_checks(r,adj,charges,clauses,source,offsets):
    records=[(charges[v],tuple(offsets[4*v:4*v+4])) for v in range(2*r*r)]
    check(verify_odd_honeycomb_stream(source,r,iter(records)),'canonical_stream_accepts_odd')
    check(not verify_odd_honeycomb_stream(source,r,iter(records[:-1])),'canonical_stream_rejects_missing_leaf')
    altered=list(records);z,loc=altered[0];altered[0]=(1-z,loc)
    check(not verify_odd_honeycomb_stream(source,r,iter(altered)),'canonical_stream_rejects_wrong_charge')
    altered=list(records);z,loc=altered[0];altered[0]=(z,(loc[1],loc[0],loc[2],loc[3]))
    check(verify_odd_honeycomb_stream(source,r,iter(altered)),'canonical_stream_accepts_clause_permutation')
    altered=list(records);z,loc=altered[0];altered[0]=(z,(loc[0]+1,loc[1],loc[2],loc[3]))
    check(not verify_odd_honeycomb_stream(source,r,iter(altered)),'canonical_stream_rejects_bad_source_offset')
    extra=records+[(1,(0,0,0,0))]
    check(not verify_odd_honeycomb_stream(source,r,iter(extra)),'canonical_stream_rejects_overlong_guess')
    # Two actual ordinary encoded descendants from restrictions on original edge IDs.
    x=1;y=2
    child=restrict_ordinary(clauses,{x:0});grand=restrict_ordinary(child,{y:1})
    s1,o1=dimacs(child,3*r*r);s2,o2=dimacs(grand,3*r*r)
    check(len(child)>0 and len(grand)>0,'two_actual_descendants')
    check(all(tuple(int(z) for z in line.split()[:-1])==row for line,row in zip(s1.splitlines()[1:],child)),'child_body_matches')
    check(all(tuple(int(z) for z in line.split()[:-1])==row for line,row in zip(s2.splitlines()[1:],grand)),'grandchild_body_matches')
    check(gf2_consistent(3*r*r,[([e for _,e in adj[v]],charges[v]) for v in range(len(adj))]+[([x],0),([y],1)])==False,'two_descendants_unsat_by_independent_linear_solver')
    return {'root_bytes':len(source),'child_bytes':len(s1),'grandchild_bytes':len(s2),
            'root_clauses':len(clauses),'child_clauses':len(child),'grandchild_clauses':len(grand),
            'stream_records':len(records),'max_record_bits_bound':1+4*((len(source)+1).bit_length()),
            'symbolic_work_index_bits_bound':8*((len(source)+1).bit_length()+1)}

def w1_controls():
    txt='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
    W=[tuple(int(z) for z in row.split()) for row in txt.split(';')]
    check(len(W)==20 and len(set(W))==20,'w1_twenty_unique')
    for v in range(1,16):
        check(sum(v in c for c in W)==2 and sum(-v in c for c in W)==2,'w1_signed_2_2')
    check(not brute_sat(W,15),'w1_unsat')
    check(brute_sat(W[:1]+W[2:],15),'w1_one_clause_deleted_sat')
    # Same-named gluing of conflicting forced literals is UNSAT, fresh-name alias instead is SAT.
    def pin(l,a,b):return [(l,p*a,q*b) for p in (1,-1) for q in (1,-1)]
    check(not brute_sat(pin(1,2,3)+pin(-1,4,5),5),'named_boundary_conflict')
    check(brute_sat(pin(1,2,3)+pin(-6,4,5),6),'wrong_alias_sat')
    check(not brute_sat([(1,),(-1,)],1),'horn_unsat')
    check(brute_sat([(1,2),(-1,2)],2),'2sat_sat')
    return {'W1_vars':15,'W1_clauses':20,'W1_signed_2_2':True,'W1_UNSAT':True}

def run():
    datasets=[]
    choices=[('K4',k4()),('prism5',prism(5)),('bridge_K4x2',bridged_k4())]
    for r in (3,4,5,8,16):choices.append((f'honeycomb{r}',honeycomb(r)))
    for name,(edges,adj) in choices:
        n=len(adj);E=len(edges);charges=[int(i==0) for i in range(n)]
        check(is_connected(adj),'graph_connected')
        clauses,groups=parity_clauses(adj,charges)
        src,offsets=dimacs(clauses,E)
        check(len(set(clauses))==len(clauses),'all_clauses_distinct')
        check(authenticate_paired_source(src,adj,charges,[offsets[4*v:4*v+4] for v in range(n)]),'source_authenticated_odd')
        even=[0]*n
        check(not authenticate_paired_source(src,adj,even,[offsets[4*v:4*v+4] for v in range(n)]),'charge_mismatch_rejected')
        even_clauses,_=parity_clauses(adj,even)
        even_src,even_offsets=dimacs(even_clauses,E)
        check(not authenticate_paired_source(even_src,adj,even,[even_offsets[4*v:4*v+4] for v in range(n)]),'sat_even_rejected')
        if E<=10:
            check(not brute_sat(clauses,E),'brute_odd_unsat')
            check(brute_sat(even_clauses,E),'brute_even_sat')
        critical=0;noncritical=[];examples=[]
        for v in range(n):
            comps=comps_minus(adj,v);c=len(comps)
            check(1<=c<=3,'cubic_vertex_cut_components')
            pred=2**(3-c)
            actual=0
            for word,clause in groups[v]:
                P=predicted_clause_essential(adj,charges,v,word)
                G=deletion_witness_satisfiable(adj,charges,v,word)
                check(P==G,'independent_GF2_vs_component_criterion')
                if P:actual+=1
                else:noncritical.append((v,word))
            check(actual==pred,'exact_essential_clauses_at_vertex')
            critical+=actual
            if c>1:examples.append((v,c,pred))
        check((critical==4*n)==all(len(comps_minus(adj,v))==1 for v in range(n)),'minimal_iff_2vertexconn')
        # Bad original clause offset and bad source variable alias are not acceptable witnesses.
        byv=[offsets[4*v:4*v+4] for v in range(n)]
        modified=[list(g) for g in byv];modified[0][0]+=1
        check(not authenticate_paired_source(src,adj,charges,modified),'invalid_offset_rejected')
        tampered=src[:offsets[0]]+str(-clauses[0][0])+src[offsets[0]+len(str(clauses[0][0])):]
        check(not authenticate_paired_source(tampered,adj,charges,byv),'wrong_sign_rejected')
        entry={'graph':name,'vertices':n,'edge_variables':E,'clauses':len(clauses),'dimacs_bytes':len(src),
               'two_vertex_connected':all(len(comps_minus(adj,v))==1 for v in range(n)),
               'essential_source_clauses':critical,'nonessential_source_clauses':len(noncritical),
               'articulation_examples':examples,'min_incidence_var_occurrence':min(sum(e==ee for _,e in adj[v] for ee in (e,)) for v in range(n))}
        if name.startswith('honeycomb'):
            # Every edge participates in 4 positive and 4 negative clauses: NOT signed exact (2,2).
            occ=collections.Counter((abs(x),x>0) for c in clauses for x in c)
            check(all(occ[e,True]==4 and occ[e,False]==4 for e in range(1,E+1)),'tseitin_occurrence_4_4')
            if int(name.removeprefix('honeycomb')) in (3,4,5,8,16):
                entry['stream_and_descendants']=stream_and_descendant_checks(int(name.removeprefix('honeycomb')),adj,charges,clauses,src,offsets)
            if int(name.removeprefix('honeycomb')) in (4,8,16):
                entry['pc']=pc_audit_honeycomb(int(name.removeprefix('honeycomb')),adj,clauses,charges,src,offsets)
        datasets.append(entry)
    strict=w1_controls()
    result={'id':'LSPV-3_VERTEX_CUT_CRITICALITY134','time_label':'2026-10-26_0759_LA',
            'classification':'PROVED/EXACT restricted symbolic; COMPUTATIONAL controls; all-UNSAT bound OPEN',
            'cases':datasets,'strict_signed_controls':strict,'checks_total':sum(counts.values()),'checks_by_name':dict(sorted(counts.items())),
            'claim_limitations':['GF(2) PC and specific odd Tseitin sources only','No all-UNSAT uniform certificate size guarantee','No signed exact (2,2) transfer; each edge has (4,4) occurrences','No machine-verified FLMV time-space claim']}
    return result

if __name__=='__main__':
    args=argparse.ArgumentParser();args.add_argument('--out',default=None);a=args.parse_args()
    result=run();data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.out:Path(a.out).write_text(data)
    print(data)
