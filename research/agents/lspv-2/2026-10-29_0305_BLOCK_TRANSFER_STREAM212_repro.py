#!/usr/bin/env python3
"""LSPV-2 independently reproducible audit of connected-interface handoff.

Runs two distinct exact finite controls:
  (1) one-pass Boolean-transfer SAT decision on canonical block-major signed
      cyclic scopes, including sign-balance and structural verification;
  (2) a connected bounded-occurrence proper-3CNF equality family exhibiting
      exponential residual width for grouped fixed variable order and linear
      residual width for interleaved order.
No assertion of unrestricted SAT hardness is made.
"""
import itertools
import json
import random
from collections import defaultdict, Counter


def scopes_block_major(n):
    assert n >= 3 and n % 3 == 0
    groups=[]
    for j in range(n//3):
        t=3*j
        groups.append(((t,t+1,t+2), ((t+1)%n,(t+2)%n,(t+3)%n),
                       ((t+2)%n,(t+3)%n,(t+4)%n), (t,t+1,t+2)))
    return groups


def balanced_cycle(n,rng):
    scopes=scopes_block_major(n)
    positions=defaultdict(list)
    for bi,block in enumerate(scopes):
        for ci,clause in enumerate(block):
            for pi,v in enumerate(clause):
                positions[v].append((bi,ci,pi))
    assert all(len(v)==4 for v in positions.values())
    positive=set()
    for where in positions.values():
        positive.update(rng.sample(where,2))
    return [tuple(tuple((v+1 if (bi,ci,pi) in positive else -(v+1))
                        for pi,v in enumerate(clause))
                  for ci,clause in enumerate(block))
            for bi,block in enumerate(scopes)]


def arbitrary_cycle(n,rng):
    return [tuple(tuple((v+1 if rng.randrange(2) else -(v+1)) for v in clause)
                  for clause in block)
            for block in scopes_block_major(n)]


def encode(blocks,n):
    return (f'p cnf {n} {4*(n//3)}\n' + ''.join(
        ' '.join(map(str,clause))+' 0\n' for block in blocks for clause in block
    )).encode('ascii')


def signed_truth(lit,bits):
    return (bits[abs(lit)-1] == (lit>0))


def signed_clause_eval(clause,assignment):
    return any(assignment[abs(lit)-1] == (lit>0) for lit in clause)


def parse_fully(bytes_input,require_balanced=True):
    """Reference validator; the streaming validation theorem is explained in .tex.
    This executable uses O(n) Python counters for independent structural checking,
    not a claim that it has measured native TM log-space usage.
    """
    try:
        text=bytes_input.decode('ascii')
        lines=text.splitlines(keepends=True)
        if not lines or not lines[0].startswith('p cnf '): return None
        header=lines[0].strip().split()
        if len(header)!=4 or header[0:2]!=['p','cnf']: return None
        n,m=int(header[2]),int(header[3])
        if n<3 or n%3 or m!=4*(n//3) or len(lines)!=m+1: return None
        scopes=scopes_block_major(n)
        blocks=[]
        counts=Counter()
        k=1
        for block in scopes:
            group=[]
            for scope in block:
                line=lines[k].split();k+=1
                if len(line)!=4 or line[3]!=b'0'.decode(): return None
                clause=tuple(int(x) for x in line[:3])
                if any(x==0 for x in clause):return None
                if tuple(abs(x)-1 for x in clause)!=scope:return None
                if len(set(map(abs,clause)))!=3:return None
                group.append(clause)
                counts.update(clause)
            blocks.append(tuple(group))
        if require_balanced and any(counts[v]!=2 or counts[-v]!=2 for v in range(1,n+1)):
            return None
        return n,blocks
    except (ValueError,UnicodeError,IndexError):
        return None


def bit_from_triple(state,position):
    return (state>>position)&1


def clause_on_pair(clause,scope,left,right,block_idx,n):
    # Generic independent clause evaluation from physical original variable IDs.
    # left = values of variables in block idx, right = values in next block.
    next_idx=(block_idx+1)%(n//3)
    vals={3*block_idx+d:bool(bit_from_triple(left,d)) for d in range(3)}
    vals.update({3*next_idx+d:bool(bit_from_triple(right,d)) for d in range(3)})
    return all((abs(l)-1) in vals for l in clause) and any(vals[abs(l)-1]==(l>0) for l in clause)


def block_matrix(block,idx,n):
    t=3*idx
    scopes=((t,t+1,t+2),((t+1)%n,(t+2)%n,(t+3)%n),
            ((t+2)%n,(t+3)%n,(t+4)%n),(t,t+1,t+2))
    rows=[0]*8
    for a in range(8):
        for b in range(8):
            if all(clause_on_pair(c,s,a,b,idx,n) for c,s in zip(block,scopes)):
                rows[a]|=1<<b
    return rows


def boolean_compose(A,B):
    out=[0]*8
    for a in range(8):
        reachable=A[a]
        while reachable:
            least=reachable & -reachable
            j=least.bit_length()-1
            out[a]|=B[j]
            reachable^=least
    return out


def transfer(blocks,n):
    P=[1<<i for i in range(8)]
    ops=0
    for bi,block in enumerate(blocks):
        M=block_matrix(block,bi,n)
        P=boolean_compose(P,M)
        ops+=8*8*8  # conservative bit-test/candidate AND-OR upper budget
    return any(P[i]&(1<<i) for i in range(8)),ops


def guarded_transfer(blocks,n,guard):
    """Transfer with extra proper 3CNF clauses confined to first triple.

    This is an augmented ordinary-3CNF control, not strict signed exact22,
    and its extended guard bytes require separate source parsing.
    """
    P=[1<<i for i in range(8)]
    for bi,block in enumerate(blocks):
        M=block_matrix(block,bi,n)
        if bi==0:
            for state in range(8):
                small=tuple(bool(state&(1<<j)) for j in range(3))
                if not all(signed_clause_eval(c,small) for c in guard):
                    M[state]=0
        P=boolean_compose(P,M)
    return any(P[i]&(1<<i) for i in range(8))


def first_witness(blocks,n):
    clauses=[c for group in blocks for c in group]
    for word in range(1<<n):
        values=tuple(bool(word&(1<<p)) for p in range(n))
        if all(signed_clause_eval(c,values) for c in clauses):
            return values
    return None


def all_eight_ternary_signs():
    return [tuple((-1 if mask&(1<<j) else 1)*(j+1) for j in range(3))
            for mask in range(8)]

def independent_brute(blocks,n):
    clauses=[c for group in blocks for c in group]
    for word in range(1<<n):
        bits=tuple(bool(word&(1<<p)) for p in range(n))
        if all(signed_clause_eval(c,bits) for c in clauses):
            return True
    return False



class CanonicalByteReader:
    """Position-indexed *input-only* reference. No splitlines or input copy."""
    __slots__=('source','at','reads')
    def __init__(self,source):
        self.source=source;self.at=0;self.reads=0
    def get(self):
        if self.at>=len(self.source):return -1
        ch=self.source[self.at];self.at+=1;self.reads+=1
        return ch
    def expect(self,string):
        for ch in string:
            if self.get()!=ord(ch):raise ValueError('wrong fixed syntax')
    def unsigned(self,terminator,limit):
        c=self.get()
        if c<ord('0') or c>ord('9'):raise ValueError('expected integer')
        if c==48:
            if self.get()!=terminator:raise ValueError('leading zero')
            return 0
        value=c-48
        if value>limit:raise ValueError('integer exceeds physical input budget')
        while True:
            c=self.get()
            if c==terminator:return value
            if c<48 or c>57:raise ValueError('noncanonical integer')
            value=value*10+(c-48)
            if value>limit:raise ValueError('integer exceeds physical input budget')
    def literal(self,expected_variable):
        c=self.get()
        positive=True
        if c==45:
            positive=False
            c=self.get()
        if c<49 or c>57:raise ValueError('wrong literal integer')
        val=c-48
        if val>expected_variable:raise ValueError('oversize literal')
        while True:
            c=self.get()
            if c==32:break
            if c<48 or c>57:raise ValueError('bad literal suffix')
            val=val*10+(c-48)
            if val>expected_variable:raise ValueError('oversize literal')
        if val!=expected_variable:raise ValueError('wrong variable label')
        return positive


def streaming_decider(source,require_balanced=True):
    """One sequential read, O(log N) bit register schematic.

    Python's bytes buffer is the read-only input. The procedure only saves
    constant-sized matrices/signs and O(log N)-bit scalar counters.
    Returns ('SAT'|'UNSAT'|'INVALID', input_bytes_read, 512*r budget).
    Does not claim Python interpreter/native-TM instruction equivalence.
    """
    inp=CanonicalByteReader(source)
    try:
        inp.expect('p cnf ')
        N=len(source)  # indexed RAM input length, or tape length counted in a first pass
        n=inp.unsigned(32,N)
        m=inp.unsigned(10,N)
        if n<3 or n%3!=0 or m!=4*(n//3):raise ValueError('bad dimensions')
        r=n//3
        if not (len(source)>=12 and len(source)>=m*8):
            # Conservative minimal line size: 3 one-digit literals and 0.
            raise ValueError('undersized physical source')
        P=[1<<i for i in range(8)]
        carry=[0,0]
        saved_first=[0,0]
        for j in range(r):
            curr=[carry[0],carry[1],0] if j else [0,0,0]
            next_carry=[0,0]
            signs=[]
            scopes=(
                (3*j,3*j+1,3*j+2),
                ((3*j+1)%n,(3*j+2)%n,(3*j+3)%n),
                ((3*j+2)%n,(3*j+3)%n,(3*j+4)%n),
                (3*j,3*j+1,3*j+2)
            )
            for scope in scopes:
                signed=[]
                for v in scope:
                    positive=inp.literal(v+1)
                    if positive:
                        if v//3==j:curr[v%3]+=1
                        elif r==1:curr[v%3]+=1
                        elif (j==r-1 and v//3==0):saved_first[v%3]+=1
                        elif v//3==(j+1)%r:next_carry[v%3]+=1
                        else:raise ValueError('unknown nonlocal index')
                    signed.append(v+1 if positive else -(v+1))
                signs.append(tuple(signed))
                inp.expect('0\n')
            block=tuple(signs)
            M=block_matrix(block,j,n)
            P=boolean_compose(P,M)
            if require_balanced:
                if j==0 and r>1:
                    if curr[2]!=2:raise ValueError('bad sign balance at initial block')
                    saved_first[0]+=curr[0]
                    saved_first[1]+=curr[1]
                elif curr!=[2,2,2]:
                    raise ValueError('bad sign balance')
            carry=next_carry
        if require_balanced and r>1 and saved_first!=[2,2]:
            raise ValueError('wrapped sign imbalance')
        if inp.get()!=-1:raise ValueError('trailing bytes')
        return ('SAT' if any(P[i]&(1<<i) for i in range(8)) else 'UNSAT',inp.reads,512*r)
    except (ValueError,IndexError,OverflowError):
        return ('INVALID',inp.reads,0)

def equality_formula(k):
    """Exact connected proper-3CNF; projection onto a,b is equality."""
    assert k>=1
    def a(i):return 1+i
    def b(i):return k+1+i
    def u(i):return 2*k+1+i
    def t(i):return 3*k+1+i
    def p(i):return 4*k+i
    def q(i):return 5*k-1+i
    cs=[]
    for i in range(k):
        cs += [(-a(i),b(i),u(i)),(-a(i),b(i),-u(i)),
               (a(i),-b(i),u(i)),(a(i),-b(i),-u(i))]
    for i in range(k-1):
        cs += [(t(i),p(i),q(i)),(t(i),p(i),-q(i)),
               (t(i),-p(i),q(i)),(t(i),-p(i),-q(i)),
               (t(i),a(i),a(i+1))]
    n=6*k-3
    assert max(abs(l) for c in cs for l in c)==n
    assert len(cs)==9*k-5
    return n,cs


def connected_incidence(cs,n):
    graph=[set() for _ in range(n)]
    for c in cs:
        ix=[abs(l)-1 for l in c]
        for x in ix:
            graph[x].update(y for y in ix if y!=x)
    seen={0};pending=[0]
    while pending:
        v=pending.pop()
        for w in graph[v]-seen:
            seen.add(w);pending.append(w)
    return len(seen)==n


def dpll(cs,values=None):
    """Generic DPLL with unit propagation. Independent of E_k structure."""
    values=dict(values or {})
    def solve(values):
        while True:
            move=False
            for c in cs:
                any_true=False;empty=[]
                for lit in c:
                    v=abs(lit)
                    if v not in values: empty.append(lit)
                    elif values[v]==(lit>0): any_true=True;break
                if any_true: continue
                if not empty:return False
                if len(empty)==1:
                    lit=empty[0];v=abs(lit);bit=lit>0
                    if v in values and values[v]!=bit:return False
                    if v not in values: values[v]=bit;move=True
            if not move:break
        active=[c for c in cs if not any(abs(l) in values and values[abs(l)]==(l>0) for l in c)]
        if not active:return True
        unassigned=next(abs(l) for c in active for l in c if abs(l) not in values)
        for bit in (False,True):
            v=dict(values);v[unassigned]=bit
            if solve(v):return True
        return False
    return solve(values)


def projected_truth(k):
    n,cs=equality_formula(k)
    assert connected_incidence(cs,n)
    assert all(len(c)==3 and len(set(abs(l) for l in c))==3 for c in cs)
    occur=Counter(abs(l) for c in cs for l in c)
    assert max(occur.values())<=6
    checked=0
    for aval in range(1<<k):
        for bval in range(1<<k):
            assign={i+1:bool(aval>>i&1) for i in range(k)}
            assign.update({k+i+1:bool(bval>>i&1) for i in range(k)})
            assert dpll(cs,assign)==(aval==bval),(k,aval,bval)
            checked+=1
    return dict(k=k,variables=n,clauses=len(cs),max_degree=max(occur.values()),
                checked_projected_assignments=checked,encoded_bytes=len(cnf_text(n,cs)))


def cnf_text(n,cs):
    return ('p cnf %d %d\n'%(n,len(cs)) + ''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode()


def residual_fingerprints(k,order):
    """Count distinct suffix functions at every cut. Terminal false is included."""
    assert len(order)==2*k
    fingerprints=[]
    for cut in range(2*k+1):
        table={}
        for left in range(1<<cut):
            # Fingerprint is the full suffix truth-table of projected equality.
            signature=0
            for right in range(1<<(2*k-cut)):
                bits=left|(right<<cut)
                assign={v:bool(bits>>i&1) for i,v in enumerate(order)}
                sat=all(assign[i+1]==assign[k+i+1] for i in range(k))
                signature=(signature<<1)|int(sat)
            table[left]=signature
        fingerprints.append(len(set(table.values())))
    return fingerprints


def fully_projected_equality_3cnf_bytes(k):
    # Replace each binary equality clause by two proper 3clauses using u_i.
    clauses=[]
    for i in range(k):
        a=1+i;b=k+1+i;u=2*k+1+i
        clauses.extend([(-a,b,u),(-a,b,-u),(a,-b,u),(a,-b,-u)])
    return len(cnf_text(3*k,clauses)),len(clauses)


def run():
    rng=random.Random(21120261028)
    transfer_checks=0
    scaling=[]
    sat_counts=Counter()
    for n,reps in ((3,30),(6,30),(9,30),(12,30),(15,10)):
        for _ in range(reps):
            b=balanced_cycle(n,rng)
            raw=encode(b,n)
            parsed=parse_fully(raw)
            assert parsed is not None and parsed[1]==b
            streamed,reads,budget=streaming_decider(raw)
            assert streamed in ('SAT','UNSAT') and reads==len(raw) and budget==512*(n//3)
            ans,ops=transfer(b,n)
            assert (streamed=='SAT')==ans
            assert ans==independent_brute(b,n)
            sat_counts[str(ans)]+=1
            transfer_checks+=1
    # Arbitrary-sign controls, outside signed-(2,2) promise; no UNSAT guarantee.
    for n in (3,6):
        for _ in range(100):
            b=arbitrary_cycle(n,rng)
            raw=encode(b,n)
            assert parse_fully(raw,True) is None or all(Counter(l for group in b for c in group for l in c)[v]==2 and Counter(l for group in b for c in group for l in c)[-v]==2 for v in range(1,n+1))
            streamed,reads,budget=streaming_decider(raw,False)
            assert streamed in ('SAT','UNSAT') and reads==len(raw)
            assert (streamed=='SAT')==transfer(b,n)[0]==independent_brute(b,n)
            transfer_checks+=1
    for n in (3,6,12,30,120,300):
        b=balanced_cycle(n,rng)
        ans,ops=transfer(b,n)
        # Quoted parsing measurements are for concrete DIMACS bytes; this
        # reference parser uses O(n) arrays, not proved small-space code.
        data=encode(b,n)
        assert parse_fully(data) is not None
        assert streaming_decider(data)[0] in ('SAT','UNSAT')
        scaling.append(dict(n=n,N_bytes=len(data),M=4*(n//3),booleans_per_block=64,
                            worst_bit_attempt_budget=ops,answer=ans))
    # One-bit signed source mutation violates exact balance (except when the
    # changed sign is offset elsewhere); corrupted labels and framing reject.
    malformed_checks=0
    for n in (3,6,12,30):
        orig=encode(balanced_cycle(n,rng),n)
        bad=[]
        bad.append(orig+b'X')
        bad.append(orig.replace(b'p cnf ',b'p xnf ',1))
        bad.append(orig.replace(b' 0\n',b' 7\n',1))
        bad.append(orig.replace(b' 0\n',b' 0',1))
        bad.append(orig.replace(b' 1 ',b' 099 ',1))
        bad.append(orig[:-3])
        for sample in bad:
            assert streaming_decider(sample)[0]=='INVALID',(n,sample)
            malformed_checks+=1
    # Genuine two-polarity *ordinary proper 3CNF* controls, outside exact22:
    # append seven/eight source clauses on first triple, and test with a
    # fully independent exhaustive ordinary-CNF truth evaluator.
    augmented_checks=0
    augmented_labels=Counter()
    all_guards=all_eight_ternary_signs()
    for n in (3,6,9,12):
        for _ in range(10):
            b=balanced_cycle(n,rng)
            witness=first_witness(b,n)
            assert witness is not None
            # Exactly one of the eight clauses is false on the witness.
            false_clause=[g for g in all_guards if not signed_clause_eval(g,witness)]
            assert len(false_clause)==1
            yes_guard=[g for g in all_guards if g not in false_clause]
            for guard,want in ((yes_guard,True),(all_guards,False)):
                clauses=[c for group in b for c in group]+guard
                assert all(len(set(map(abs,c)))==3 for c in clauses)
                brute=any(all(signed_clause_eval(c,tuple(bool(word>>p&1) for p in range(n)))
                              for c in clauses) for word in range(1<<n))
                ans=guarded_transfer(b,n,guard)
                assert ans==brute==want,(n,ans,brute,want)
                augmented_checks+=1
                augmented_labels['SAT' if ans else 'UNSAT']+=1
    eq_tests=[]
    for k in range(1,7):
        r=projected_truth(k)
        r['proper_3cnf_projected_bytes'],r['projected_clauses']=fully_projected_equality_3cnf_bytes(k)
        eq_tests.append(r)
    obdd=[]
    for k in range(1,9):
        grouped=list(range(1,2*k+1))
        interleaved=[j for i in range(k) for j in (i+1,k+i+1)]
        wg=residual_fingerprints(k,grouped)
        wi=residual_fingerprints(k,interleaved)
        assert wg[k]==(1<<k)
        assert max(wi)<=3
        obdd.append(dict(k=k,grouped_cut_width=wg[k],interleaved_max_width=max(wi),
                         grouped_all_cuts=wg,interleaved_all_cuts=wi))
    return dict(status='PASS',test_seed=21120261028,
                exact22_transfer_vs_independent_bruteforce=130,
                additional_arbitrary_sign_transfer_bruteforce=200,
                total_transfer_truth_checks=transfer_checks, malformed_controls_rejected=malformed_checks,
                signed_exact22_sample_answers=dict(sat_counts),
                canonical_block_major_scaling=scaling,
                guarded_ordinary_3cnf_two_polarity_checks=augmented_checks,
                guarded_ordinary_3cnf_answer_counts=dict(augmented_labels),
                equality_dpll_controls=eq_tests,
                obdd_frontier_controls=obdd,
                limitations=['Unbounded claims depend on symbolic proof, not finite tests.',
                             'Python parser uses O(n) memory; small-space streaming validator is symbolic, not native-TM measured.',
                             'Equality family has max variable degree 6, NOT signed exact-(2,2).',
                             'OBDD lower bound is fixed variable order and exact residual-function preservation, NOT SAT decision.',
                             'Transfer method restricted to authenticated cyclic block-major clause scopes.'])


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
