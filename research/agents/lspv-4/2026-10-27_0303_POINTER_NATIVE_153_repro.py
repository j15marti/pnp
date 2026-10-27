#!/usr/bin/env python3
"""Deterministic exact source/proof construction and native pointer-itinerary audit.
Proof is two-level BRANCH(z), BRANCH(w), then PATH(x, gamma+, gamma-).
The input is canonical proper 3CNF in plain DIMACS and all pointers are byte offsets.
No external dependencies; ordinary SAT / coNTIME conclusions deliberately absent.
"""
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_FILE = ROOT / '2026-10-27_0303_POINTER_NATIVE_153_raw.json'
CHECKS = 0

def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)

def lit_neg(x):
    return -x

def prepare(r):
    check(r >= 2, 'r >= 2')
    z,w,x, a,b = 1,2,3,4,5
    ident = 6
    paths = {}
    entries = []
    for bit in (0,1):
        guard = z if bit==0 else -z
        for direction in (0,1):
            inn = x if direction==0 else -x
            out = -x if direction==0 else x
            intermediate = list(range(ident,ident+r-1))
            ident += r-1
            nodes = [inn]+intermediate+[out]
            paths[(bit,direction)] = []
            for step in range(r):
                src,dst = nodes[step],nodes[step+1]
                clause = (guard,-src,dst)
                check(len(set(map(abs,clause)))==3, 'proper 3CNF clause')
                entries.append({'bit':bit,'dir':direction,'step':step,'src':src,'dst':dst,'clause':clause})
    # All even-numbered chain edges occupy the left half; all odd-numbered edges the right half.
    # Within each half, order by the program-independent (bit, direction, step) tuple.
    even = sorted((e for e in entries if e['step']%2==0),key=lambda e:(e['bit'],e['dir'],e['step']))
    odd  = sorted((e for e in entries if e['step']%2==1),key=lambda e:(e['bit'],e['dir'],e['step']))
    filler = [{'bit':None,'dir':None,'step':None,'src':None,'dst':None,'clause':(w,a,b)},
              {'bit':None,'dir':None,'step':None,'src':None,'dst':None,'clause':(-w,a,b)}]
    ordered = even+filler+odd
    head = f'p cnf {ident-1} {len(ordered)}\n'.encode('ascii')
    output = bytearray(head)
    for e in ordered:
        e['offset'] = len(output)
        data = (' '.join(str(q) for q in e['clause'])+' 0\n').encode('ascii')
        output.extend(data)
        e['end'] = len(output)
        e['bytes'] = len(data)
    for e in entries:
        paths[(e['bit'],e['dir'])].append([e['offset'],e['src'],e['dst']])
    for key in paths:
        check(len(paths[key])==r,'path edges')
        check(paths[key][0][1]==(x if key[1]==0 else -x), 'starting literal')
        check(paths[key][-1][2]==(-x if key[1]==0 else x), 'ending literal')
        for i in range(r-1):
            check(paths[key][i][2]==paths[key][i+1][1], 'continuous path')
    cert = {'tag':'BRANCH','var':z,'children':[]}
    for bit in (0,1):
        c = {'tag':'BRANCH','var':w,'children':[]}
        for bit2 in (0,1):
            c['children'].append({'tag':'PATH','pivot':x,'plus':paths[(bit,0)],'minus':paths[(bit,1)]})
        cert['children'].append(c)
    return bytes(output),cert,ordered,entries

def read_and_authenticate_source(source,offset,assignment):
    check(0<=offset<len(source), 'pointer range')
    check(offset>0 and source[offset-1:offset]==b'\n', 'clause starts after newline')
    j=source.find(b'\n',offset)
    check(j!=-1, 'line is newline terminated')
    line = source[offset:j+1]
    values=list(map(int,line.split()))
    check(len(values)==4 and values[-1]==0,'three signed literals and final zero')
    check(all(v!=0 for v in values[:3]),'zero is terminator only')
    check(len({abs(v) for v in values[:3]})==3,'proper clause authenticated')
    residual=[]
    for v in values[:3]:
        if abs(v) in assignment:
            if assignment[abs(v)]==(v>0):
                return None,len(line) # satisfied clauses do NOT authorize binary implication edges
            continue
        residual.append(v)
    return residual,len(line)

def verify_proof(source,cert):
    header,sep=source.split(b'\n',1)
    check(header.startswith(b'p cnf '),'canonical header')
    _,_,nstr,mstr=header.decode('ascii').split(' ')
    n,m=int(nstr),int(mstr)
    check(n>=5 and m>=2,'header n m')
    rawlines=sep.splitlines(keepends=True)
    check(len(rawlines)==m and all(x.endswith(b'\n') for x in rawlines),'exact clause count')
    for line in rawlines:
        vals=list(map(int,line.split()))
        check(len(vals)==4 and vals[-1]==0, 'source signed ternary')
        check(all(0<abs(v)<=n for v in vals[:3]),'literal name in header range')
        check(len(set(map(abs,vals[:3])))==3,'three distinct names')
    lookup=[]
    def rec(node,assignment):
        if node['tag']=='BRANCH':
            v=node['var'];check(v not in assignment, 'new variable branch')
            check(len(node['children'])==2,'both branches')
            for bit,child in enumerate(node['children']):
                rec(child,{**assignment,v:bool(bit)})
        elif node['tag']=='PATH':
            pivot=node['pivot']
            check(pivot not in assignment,'pivot free')
            for name,initial,target in [('plus',pivot,-pivot),('minus',-pivot,pivot)]:
                prev=initial
                for off,src,dst in node[name]:
                    check(src==prev,'edge path continuity')
                    residual,byte_count=read_and_authenticate_source(source,off,assignment)
                    check(residual is not None and len(residual) in (1,2),'edge residual width')
                    if len(residual)==2:
                        a,b=residual
                        check((src==-a and dst==b) or (src==-b and dst==a),'authentic implication edge')
                    else:
                        check(src==-residual[0] and dst==residual[0], 'unit implication')
                    lookup.append((off,byte_count))
                    prev=dst
                check(prev==target,'path reaches contradiction')
        else:raise AssertionError('unknown node kind')
    rec(cert,{})
    return lookup

def sat_2cnf(clauses,variables):
    # DFS SCC check on binary residual clauses; pure Python no solver dependency.
    adj=defaultdict(list); rev=defaultdict(list)
    for c in clauses:
        check(len(c)<=2,'post-restriction width <=2')
        if not c:return False
        if len(c)==1:pairs=[(-c[0],c[0])]
        else:
            a,b=c;pairs=[(-a,b),(-b,a)]
        for u,v in pairs:adj[u].append(v);rev[v].append(u)
    seen=set();order=[]
    def visit(u):
        stack=[(u,False)]
        while stack:
            v,done=stack.pop()
            if done:order.append(v);continue
            if v in seen:continue
            seen.add(v);stack.append((v,True))
            for w in adj[v]:
                if w not in seen:stack.append((w,False))
    verts=[u for x in variables for u in (x,-x)]
    for v in verts:
        if v not in seen:visit(v)
    comp={};cid=0
    for v in reversed(order):
        if v in comp:continue
        queue=[v];comp[v]=cid
        while queue:
            u=queue.pop()
            for a in rev[u]:
                if a not in comp:comp[a]=cid;queue.append(a)
        cid+=1
    return all(comp[v]!=comp[-v] for v in variables)

def clause_residual(clause,assignment):
    res=[]
    for l in clause:
        if abs(l) in assignment:
            if assignment[abs(l)]==(l>0):return None
        else:res.append(l)
    return res

def restrict_cnf_size(ordered,n,assignment):
    """Canonical serialized ordinary CNF child, with original variable IDs preserved."""
    residuals=[clause_residual(e['clause'],assignment) for e in ordered]
    residuals=[row for row in residuals if row is not None]
    data=f'p cnf {n} {len(residuals)}\n'
    data+=''.join(' '.join(str(v) for v in row)+' 0\n' for row in residuals)
    return len(data.encode('ascii')),len(residuals)

def itinerary(lookup,source_size,left_right_seam):
    # The input head scans entire source once for syntax validation, as the proposed grammar does.
    single=source_size
    single_pos=source_size
    two=source_size+left_right_seam # head 0 scans all; head 1 seeks right-half seam.
    heads=[source_size,left_right_seam]
    motions=[]
    for off,width in lookup:
        # One-head verifier authenticates each next pointer IN RECORD ORDER, then leaves head after record.
        move=abs(single_pos-off)+max(0,width-1)
        single+=move
        single_pos=off+width-1
        # Two independent read-only heads assigned to disjoint left/right clause blocks.
        lane=int(off>=left_right_seam)
        move2=abs(heads[lane]-off)+max(0,width-1)
        two+=move2
        heads[lane]=off+width-1
        motions.append((off,width,lane,move,move2))
    return single,two,motions

def audit(r):
    source,proof,ordered,entries=prepare(r)
    lookup=verify_proof(source,proof)
    nvar=5+4*(r-1);mclauses=4*r+2
    check(source.startswith(f'p cnf {nvar} {mclauses}\n'.encode()),'header exact names and clauses')
    check(len(lookup)==8*r,'four leaves each 2r edges')
    check(sum(e['bytes'] for e in ordered)+len(source.split(b'\n',1)[0])+1==len(source),'physical line accounting')
    seam=next(e['offset'] for e in ordered if e['step'] is not None and e['step']%2==1)
    check(all(e['offset']<seam for e in ordered if e['step'] is not None and e['step']%2==0),'even clauses left of seam')
    check(all(e['offset']>=seam for e in ordered if e['step'] is not None and e['step']%2==1),'odd clauses right of seam')
    # Independent semantic check: every one of the four complete branch assignments is UNSAT.
    for zbit in (0,1):
        for wbit in (0,1):
            restrict={1:bool(zbit),2:bool(wbit)}
            residuals=[clause_residual(e['clause'],restrict) for e in ordered]
            residuals=[r for r in residuals if r is not None]
            vars2={abs(v) for c in residuals for v in c}
            check(not sat_2cnf(residuals,vars2),'independent 2SAT contradiction')
    # Removing any one source guarded clause on z=0 makes branch z=0 SAT.
    first=next(e for e in entries if e['bit']==0 and e['dir']==0 and e['step']==0)
    residuals=[clause_residual(e['clause'],{1:False,2:False}) for e in ordered if e is not first]
    residuals=[v for v in residuals if v is not None]
    names={abs(v) for c in residuals for v in c}
    check(sat_2cnf(residuals,names),'deleted edge makes one branch satisfiable')
    # Exactly one pointer forgery and one truncation must be rejected.
    bad=json.loads(json.dumps(proof));bad['children'][0]['children'][0]['plus'][0][0]+=1
    try:verify_proof(source,bad)
    except AssertionError:pass
    else:raise AssertionError('accepted bad pointer')
    bad=json.loads(json.dumps(proof));bad['children'][1]['children'][1]['minus']=bad['children'][1]['children'][1]['minus'][:-1]
    try:verify_proof(source,bad)
    except AssertionError:pass
    else:raise AssertionError('accepted truncated path')
    bad=json.loads(json.dumps(proof));bad['children'][0]['children']=bad['children'][0]['children'][:1]
    try:verify_proof(source,bad)
    except AssertionError:pass
    else:raise AssertionError('accepted incomplete branch')
    # Proof may not authenticate a tampered source clause, even if its offset still exists.
    bad_source=bytearray(source)
    flipped=next(e for e in ordered if e['step'] is not None and e['bit']==0 and e['dir']==0)
    p=flipped['offset']
    if bad_source[p]==ord('-'):
        bad_source[p]=ord('+') # noncanonical but safely rejected
    else:
        bad_source[p]=ord('-')
    try:verify_proof(bytes(bad_source),proof)
    except (AssertionError,ValueError):pass
    else:raise AssertionError('accepted forged source clause bytes')
    P=len(json.dumps(proof,separators=(',',':'),sort_keys=True).encode())
    spectra={}
    for bit in (0,1):
        first,mc1=restrict_cnf_size(ordered,nvar,{1:bool(bit)})
        second=[]
        for bit2 in (0,1):
            width,mc2=restrict_cnf_size(ordered,nvar,{1:bool(bit),2:bool(bit2)})
            second.append({'w':bit2,'bytes':width,'clauses':mc2})
        spectra[str(bit)]={'z_child_bytes':first,'z_child_clauses':mc1,'w_children':second}
    one,two,motions=itinerary(lookup,len(source),seam)
    check(one>=two,'one head no cheaper than two for tested layout')
    if r>=8:
        check(one>r*len(source)/4,'quadratic physical head movement witnessed')
        check(two<64*len(source),'two-head linear movement control')
    alternations=sum(motions[i][2]!=motions[i-1][2] for i in range(1,len(motions)))
    indexed_bit= 8*len(source)+sum(int(math.ceil(math.log2(len(source)+1)))+8*width for _,width in lookup)
    if r>=8:
        check(indexed_bit < one,'indexed bit-circuit upper below source-head itinerary for growing instances')
    return {
        'r':r,'N_bytes':len(source),'source_bits':8*len(source),'variables':nvar,'clauses':mclauses,
        'B':3,'L':4,'E':len(lookup),'h':2,'proof_bytes_json':P,
        'max_clause_bytes':max(e['bytes'] for e in ordered),
        'pointer_bits':(len(source)+1).bit_length(),'one_head_moves_after_parse':one-len(source),
        'real_ordinary_CNFs_two_level_child_spectrum':spectra,
        'one_head_moves_with_parse':one,'two_head_moves_with_parse':two,
        'indexed_address_and_source_bit_charges':indexed_bit,
        'proof_offsets_switch_halves':alternations,'proof_clause_offsets':len(lookup),
        'min_alternating_jump_bytes':min(abs(motions[i+1][0]-(motions[i][0]+motions[i][1]-1)) for i in range(len(motions)-1) if motions[i+1][2]!=motions[i][2]),
        'source_sha256':hashlib.sha256(source).hexdigest(),
        'proof_sha256':hashlib.sha256(json.dumps(proof,sort_keys=True).encode()).hexdigest(),
        'independent_unsat_check':'2SAT SCC on all four (z,w) leaves',
        'hostile_controls':['delete one z=0 guarded clause yields SAT leaf','forged offset rejected','truncated path rejected','missing branch rejected']
    }

def output_only_exception():
    # Transducer, NOT SAT decider: on N input bits write N*N bytes (one constant
    # byte per output action), using two O(log N) counters and one work tape.
    # A ONE-SHARED-TAPE machine required to retain the exact contiguous output
    # has visited footprint at least N*N, even when it overwrites the input.
    arr=[]
    for n in (4,8,16,32,64,128,256):
        kspace=2*math.ceil(math.log2(n+1))+3
        time=n*n+n
        output=n*n
        claimed=n+kspace+math.ceil(math.log2(time+2))
        check(output>claimed if n>=16 else output>0, 'output-only transducer distinct model')
        arr.append({'input_bytes':n,'output_bytes':output,'native_multitape_work_cells_upper':kspace,
                    'native_multitape_time_steps_upper':time,
                    'one_shared_tape_min_visited_cells':output,
                    'decision_only_space_expression_without_output':claimed})
    return arr

def main():
    rows=[audit(r) for r in (2,3,4,8,16,32,64,128,256)]
    printer_controls=output_only_exception()
    obj={
        'project':'LSPV-4 POINTER-NATIVE-153',
        'status':'COMPUTATIONAL finite checks plus separate symbolic restricted theorem',
        'implementation':'Python 3 standard library deterministic',
        'seed':None,
        'checks':CHECKS,
        'transducer_output_only_exception_controls':printer_controls,
        'machine_scope':'prescribed-order immediate-authentication verifier (one or two physical read-only input heads); indexed bit-cost control',
        'limitations':'head-movement lower bound is for THIS immediate-checker interface, not an arbitrary optimal offline verifier or general SAT solver',
        'rows':rows,
    }
    SOURCE_FILE.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':CHECKS,'runs':len(rows),'zero_failures':True,'file':str(SOURCE_FILE),'largest':rows[-1]},sort_keys=True))

if __name__=='__main__':main()