#!/usr/bin/env python3
"""LSPV-2 PRISM-PARITY-FRONTIER214. No external packages. Python 3.10+.
Finite independent controls of the elementary parity/Tseitin prism theorem.
The source is a canonical proper 3-CNF, with exact signed (4,4), NOT (2,2).
All integer counters in the generated raw JSON are explicit tests, not claimed TM steps.
"""
import itertools, io, json, random, sys
from collections import Counter

SEED=20261029
YES='p cnf 3 1\n1 2 3 0\n'
NO='p cnf 3 8\n'+''.join(' '.join(str(i if bit == 0 else -i) for i,bit in enumerate(bits,1))+' 0\n' for bits in itertools.product((0,1),repeat=3))

def graph(r):
    assert r>=3
    E=[]
    for i in range(r): E.append((i,(i+1)%r))
    for i in range(r): E.append((r+i,r+(i+1)%r))
    for i in range(r): E.append((i,r+i))
    assert len(E)==3*r and len(set(tuple(sorted(e)) for e in E))==3*r
    return E

def incident(r):
    E=graph(r); inc=[[] for _ in range(2*r)]
    for j,(u,v) in enumerate(E,1):
        inc[u].append(j);inc[v].append(j)
    inc=[tuple(sorted(x)) for x in inc]
    assert all(len(x)==3 for x in inc)
    return inc

def constant_space_incident_triple(r,v):
    """Compute three incident edge IDs with O(log r) numeric registers."""
    i=v%r
    t=0 if v<r else r
    return tuple(sorted((t+(i-1)%r+1,t+i+1,2*r+i+1)))

def indexed_charge_probe(text,r):
    """Promise-only bit-probe decoder. Never use it to recognize ordinary input.
    One indexed ASCII bit (bit 4 of first character of third literal) per group.
    Full address computation and fixed per-block lengths are explicitly charged.
    """
    source=text.encode('ascii')
    offset=len(f'p cnf {3*r} {8*r}\n')
    xor=0; addresses=[]; address_arithmetic=0
    for v in range(2*r):
        tr=constant_space_incident_triple(r,v)
        # The first lex forbidden assignment is 001 when charge=0, 000 when charge=1.
        # Its first two literal signs are always positive.  The third starts at:
        addr=offset+len(str(tr[0]))+1+len(str(tr[1]))+1
        one_bit=(source[addr]>>4)&1
        assert source[addr] in b'-0123456789'
        assert one_bit==(source[addr]!=ord('-'))
        xor^=one_bit
        addresses.append(addr)
        block0=encode_single_block(tr,0)
        block1=encode_single_block(tr,1)
        size0=sum(map(len,block0));size1=sum(map(len,block1))
        assert size0==size1
        offset+=size0
        address_arithmetic+=10+len(str(tr[0]))+len(str(tr[1]))+sum(map(len,block0))
    assert offset==len(source)
    assert len(set(addresses))==2*r
    return xor==0,{'bit_probes':len(addresses),'address_arithmetic_upper_proxy':address_arithmetic,
                    'max_address_bits':len(source).bit_length(),
                    'distinct_block_probes':len(set(addresses))}

def validate_stream_and_decide(text):
    """Streams input with constant line buffers and O(log N) integer counters.
    The Python immutable input string belongs to the read-only input model, not work.
    This is an algorithmic model, NOT a measured physical TM or Python heap cap.
    """
    stream=io.StringIO(text)
    h=stream.readline()
    parts=h.strip().split()
    if len(parts)!=4 or parts[:2]!=['p','cnf'] or any(not p.isdecimal() for p in parts[2:]):
        raise ValueError('invalid stream header')
    n,m=map(int,parts[2:])
    if n<9 or n%3 or m!=8*(n//3):raise ValueError('invalid stream size')
    r=n//3
    if h!=f'p cnf {3*r} {8*r}\n':raise ValueError('noncanonical stream header')
    scan_chars=len(h); answer=0; peak_line=len(h)
    for v in range(2*r):
        tr=constant_space_incident_triple(r,v)
        first=stream.readline()
        scan_chars+=len(first);peak_line=max(peak_line,len(first))
        seq0=encode_single_block(tr,0);seq1=encode_single_block(tr,1)
        if first==seq0[0]: charge=0;expected=seq0
        elif first==seq1[0]:charge=1;expected=seq1
        else:raise ValueError('invalid first clause')
        answer^=charge
        for row in expected[1:]:
            line=stream.readline();scan_chars+=len(line)
            peak_line=max(peak_line,len(line))
            if line!=row:raise ValueError('noncanonical parity block')
    extra=stream.read(1)
    if extra:raise ValueError('trailing data')
    # Exact input-cell coverage, with no source copies or occurrence tables.
    assert scan_chars==len(text)
    return (answer==0, {'input_characters_read':scan_chars,'max_line_characters':peak_line,
          'numeric_register_bits_bound':8*(n.bit_length()+1)})

def parity(x): return x.bit_count()&1

def encode(r,charges):
    assert len(charges)==2*r
    out=[f'p cnf {3*r} {8*r}']
    for v,edge_triple in enumerate(incident(r)):
        for bits in itertools.product((0,1),repeat=3):
            if (sum(bits)&1)==charges[v]: continue
            lits=[eid if bit==0 else -eid for eid,bit in zip(edge_triple,bits)]
            out.append(' '.join(map(str,lits))+' 0')
    assert len(out)==8*r+1
    return '\n'.join(out)+'\n'

def parse(text):
    """Pay for all exact bytes via canonical re-encoding; rejects malformed data."""
    if text==YES:return ('BASE',1)
    if text==NO:return ('BASE',0)
    lines=text.splitlines(keepends=True)
    if not lines or not lines[0].startswith('p cnf '): raise ValueError('invalid header')
    parts=lines[0].strip().split()
    if len(parts)!=4 or not all(x.isdecimal() for x in parts[2:]):raise ValueError('bad header fields')
    n,m=map(int,parts[2:]);
    if n%3 or n<9 or m!=8*(n//3):raise ValueError('nonprism size')
    r=n//3
    if len(lines)!=m+1:raise ValueError('incorrect number of lines')
    inc=incident(r); charges=[]
    for v,triple in enumerate(inc):
        block=lines[1+4*v:1+4*(v+1)]
        valid=[]
        for b in (0,1):
            cand=encode_single_block(triple,b)
            if block==cand:valid.append(b)
        if len(valid)!=1:raise ValueError('invalid parity clause block')
        charges.append(valid[0])
    if encode(r,charges)!=text:raise ValueError('noncanonical serialized bytes')
    return ('PRISM',r,charges)

def encode_single_block(triple,b):
    ans=[]
    for bits in itertools.product((0,1),repeat=3):
        if (sum(bits)&1)!=b:
            ans.append(' '.join(str(e if bit==0 else -e) for e,bit in zip(triple,bits))+' 0\n')
    return ans

def compile_one_child(text):
    got=parse(text)
    if got[0]=='BASE':return text
    return YES if validate_stream_and_decide(text)[0] else NO

def clauses_from_cnf(text):
    rows=text.splitlines()
    return [tuple(int(x) for x in row.split()[:-1]) for row in rows[1:]]

def eval_clause(lits,assignment):
    return any(((assignment>>(abs(lit)-1))&1) == (lit>0) for lit in lits)

def eval_cnf(lits,assignment):
    return all(eval_clause(cl,assignment) for cl in lits)

def check_vertex_constraints(r,charges,assignment):
    return all((sum((assignment>>(x-1))&1 for x in edges)&1)==charges[v] for v,edges in enumerate(incident(r)))

def column_masks(r):
    es=graph(r)
    return [(1<<u)|(1<<v) for u,v in es]

def gf2_rank(cols):
    pivots={}
    for x in cols:
        while x:
            p=x.bit_length()-1
            if p not in pivots:
                pivots[p]=x
                break
            x ^= pivots[p]
    return len(pivots)

def cut_rank(r,indices):
    cols=column_masks(r)
    ac=[cols[i] for i in indices]
    bc=[cols[i] for i in range(3*r) if i not in indices]
    return gf2_rank(ac)+gf2_rank(bc)-gf2_rank(cols)

def residual_vectors(r,charges):
    """At natural rung-first cut. Returns all distinct residual Boolean functions."""
    assert r<=6
    inc=incident(r); nA=1<<r; nB=1<<(2*r)
    signatures=set(); feasible=0; models=0
    for a in range(nA):
        sig=0
        for b in range(nB):
            mask=b | (a<<(2*r))
            # Independent vertex parity check, not CNF evaluation.
            if all((sum((mask>>(j-1))&1 for j in triple)&1)==charges[v] for v,triple in enumerate(inc)):
                sig |= (1<<b)
                models+=1
        feasible+= bool(sig)
        signatures.add(sig)
    return dict(distinct_residuals=len(signatures),feasible_rung_assignments=feasible,total_models=models,zero_residual=(0 in signatures))

def run():
    rng=random.Random(SEED)
    count=Counter(); examples=[]; sampled=[]
    for r in (3,4,5,6,8,12,24,48):
        inc=incident(r)
        for e in range(1,3*r+1):
            assert sum(e in group for group in inc)==2
            count['source_incidence_checks']+=1
        assert gf2_rank(column_masks(r))==2*r-1
        assert gf2_rank(column_masks(r)[2*r:])==r
        assert gf2_rank(column_masks(r)[:2*r])==2*r-2
        assert cut_rank(r,set(range(2*r,3*r)))==r-1
        count['rank_identity_checks']+=4
        charges0=[rng.randrange(2) for _ in range(2*r)]
        charges1=charges0[:]
        if sum(charges1)%2:charges1[0]^=1
        if not sum(charges0)%2:charges0[0]^=1
        # Now charges1 SAT (even), charges0 UNSAT (odd).
        assert (sum(charges1)%2)==0 and (sum(charges0)%2)==1
        for label,charges in (('SAT',charges1),('UNSAT',charges0)):
            text=encode(r,charges); got=parse(text)
            assert got==('PRISM',r,charges)
            child=compile_one_child(text)
            assert parse(child)==('BASE',1 if label=='SAT' else 0)
            streamed,stream_ledger=validate_stream_and_decide(text)
            assert streamed==(label=='SAT')
            assert stream_ledger['input_characters_read']==len(text)
            qans,query_ledger=indexed_charge_probe(text,r)
            assert qans==streamed and query_ledger['bit_probes']==2*r
            count['indexed_bit_query_controls']+=2*r
            count['source_stream_validations']+=1
            assert compile_one_child(child)==child
            clauses=clauses_from_cnf(text)
            assert len(clauses)==8*r
            assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in clauses)
            counts=Counter(lit for cl in clauses for lit in cl)
            assert all(counts[e]==4 and counts[-e]==4 for e in range(1,3*r+1))
            count['canonical_group_checks']+=2*r
            count['literal_degree_checks']+=3*r
            # Hostile mutation: reject a modified sign byte while preserving header and length.
            lines=text.splitlines(keepends=True)
            first=lines[1].split();first[0]=str(-int(first[0]));lines[1]=' '.join(first)+'\n'
            try:parse(''.join(lines));raise AssertionError('malformed accepted')
            except ValueError: count['hostile_rejections']+=1
            try:validate_stream_and_decide(''.join(lines));raise AssertionError('malformed streaming accepted')
            except ValueError: count['hostile_stream_rejections']+=1
            examples.append(dict(r=r,label=label,clauses=len(clauses),variables=3*r,parent_bits=len(text.encode())*8,
                child_bits=len(child.encode())*8,lambda075_bound=round((len(text.encode())*8)**.75,3),
                child_below_power=(len(child.encode())*8 <= (len(text.encode())*8)**.75)))
            if r<=6:
                z=residual_vectors(r,charges)
                expect=(1<<(r-1))+1 if label=='SAT' else 1
                assert z['distinct_residuals']==expect
                assert z['total_models']==(1<<(r+1) if label=='SAT' else 0)
                assert z['feasible_rung_assignments']==(1<<(r-1) if label=='SAT' else 0)
                count['residual_cut_checks']+=1
                sampled.append({'r':r,'label':label,**z})
            if r<=5:
                for mask in range(1<<(3*r)):
                    lhs=eval_cnf(clauses,mask)
                    rhs=check_vertex_constraints(r,charges,mask)
                    assert lhs==rhs
                    count['full_cnf_assignments']+=1
                # Independent correct outcome proof control: spanning-tree rank full.
            if r>=6:
                for _ in range(250):
                    mask=rng.randrange(1<<(3*r))
                    assert eval_cnf(clauses,mask)==check_vertex_constraints(r,charges,mask)
                    count['random_cnf_assignments']+=1
        # Exhaust all 2^(2r) charge vectors for only r=3, one scan for each parity label.
        if r==3:
            for integer in range(1<<(2*r)):
                charge=[(integer>>j)&1 for j in range(2*r)]
                c=compile_one_child(encode(r,charge))
                assert c==(YES if parity(integer)==0 else NO)
                assert validate_stream_and_decide(encode(r,charge))[0] == (parity(integer)==0)
                assert indexed_charge_probe(encode(r,charge),r)[0] == (parity(integer)==0)
                allclauses=clauses_from_cnf(encode(r,charge))
                count_models=sum(eval_cnf(allclauses,edge_word) for edge_word in range(1<<(3*r)))
                assert count_models==(16 if parity(integer)==0 else 0)
                count['all_charge_vector_full_source_assignments_r3']+=(1<<(3*r))
                count['all_charge_vectors_r3']+=1
    # Direct difference of two residuals for SAT fixed r=6, and no residual for UNSAT.
    result={'status':'PASS','seed':SEED,'family':'prism cubic-graph XOR/Tseitin 3CNF',
        'source_promise':'proper signed exact-(4,4), canonical labeled prism (NOT exact-(2,2))',
        'checks':dict(count),'runs':examples,'residuals':sampled,
        'symbolic_claims':{'SAT_even':'2^(r+1) assignments, 2^(r-1)+1 residual functions at rung cut',
          'UNSAT_odd':'0 assignments, exactly one constant-false residual function',
          'rank_at_cut':'r-1', 'minimum_clause_hitting_set':'r rung variables',
          'promise_bit_queries_each_side':'exactly 2r for deterministic decision trees, matched by indexed bit algorithm',
          'source_size':'Theta(r log r) bits',
          'child_size':'O(1) bits after full polynomial-time authentication and parity scan'},
        'limits':['Canonical restricted promise, not unrestricted SAT.','One tape and two tape machine bounds are conservative analytical upper bounds, not measured transitions.',
          'Exponential OBDD lower bound at rung-first fixed order, not all orders; circuit/parity access escapes.',
          'Finite exhaustive/model assertions are computational, mathematical statements require symbolic proofs.']}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':run()