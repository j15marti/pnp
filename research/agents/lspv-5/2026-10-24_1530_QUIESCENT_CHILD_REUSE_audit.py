#!/usr/bin/env python3
"""Exact finite audit of ordinary-child buffer reuse for scoped CNF joins.
No external dependencies. Counters are abstract events, not RAM instructions.
Run: python audit.py --quick (bounded suite; optional full suite is larger). The JSON includes this script's SHA-256.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse, hashlib, json, math, random, time

CHECKS=Counter()
def check(test:bool, name:str)->None:
    CHECKS[name]+=1
    if not test: raise AssertionError(name)

def sat(cnf, assignment):
    return all(any(assignment.get(abs(l),False)==(l>0) for l in c) for c in cnf)

def brute(cnf, pins=None):
    pins={} if pins is None else pins
    ids=sorted({abs(l) for c in cnf for l in c}|set(pins))
    free=[x for x in ids if x not in pins]
    return any(
        sat(cnf,dict(pins)|dict(zip(free,vals))) for vals in product((False,True),repeat=len(free)))

def dpll(cnf, stats:Counter)->bool:
    stats['solver_nodes']+=1
    clauses=[tuple(c) for c in cnf]
    while True:
        if any(len(c)==0 for c in clauses): return False
        if not clauses: return True
        units=[c[0] for c in clauses if len(c)==1]
        if not units: break
        l=units[0]
        nxt=[]
        for c in clauses:
            stats['solver_literal_visits']+=len(c)
            if l in c: continue
            nxt.append(tuple(a for a in c if a!=-l))
        clauses=nxt
    v=min(abs(l) for c in clauses for l in c)
    return dpll(clauses+[(v,)],stats) or dpll(clauses+[(-v,)],stats)

def properize(cnf):
    n=max((abs(l) for c in cnf for l in c),default=0)
    out=[]
    for c in cnf:
        if len(c)==3: out.append(tuple(c))
        elif len(c)==2:
            n+=1; out.extend((tuple(c)+(n,),tuple(c)+(-n,)))
        elif len(c)==1:
            a,b=n+1,n+2;n+=2
            out.extend((c[0],sa*a,sb*b) for sa in (1,-1) for sb in (1,-1))
        else: raise ValueError('Only nonempty clauses of width <= 3')
    return tuple(out)

def event_input(cnf):
    """Benchmark preparation, NOT a charged arbitrary-input low-width compiler."""
    first={};last={}
    for i,c in enumerate(cnf):
        for l in c:
            first.setdefault(abs(l),i);last[abs(l)]=i
    names={v:i+1 for i,v in enumerate(sorted(first,key=lambda v:(first[v],v)))}
    events=[]; renamed=[]
    for i,c in enumerate(cnf):
        for v in sorted((v for v in first if first[v]==i),key=names.get):events.append(('O',(names[v],)))
        row=tuple((1 if l>0 else -1)*names[abs(l)] for l in c)
        renamed.append(row);events.append(('C',row))
        for v in sorted((v for v in last if last[v]==i),key=names.get):events.append(('X',(names[v],)))
    return tuple(events),tuple(renamed)

class Source:
    def __init__(self,events,stats):self.events=events;self.stats=stats
    def read(self,i):
        self.stats['source_record_reads']+=1
        self.stats['source_word_reads']+=4 # fixed event record, including padding
        return self.events[i]
    def __len__(self):return len(self.events)

def validate(src):
    live=set();last=0;width=0
    for i in range(len(src)):
        kind,args=src.read(i)
        if kind=='O':
            if len(args)!=1 or args[0]!=last+1:raise ValueError('nonconsecutive OPEN')
            last=args[0];live.add(last)
        elif kind=='X':
            if len(args)!=1 or args[0] not in live:raise ValueError('invalid CLOSE')
            live.remove(args[0])
        elif kind=='C':
            if len(args)!=3 or len(set(map(abs,args)))!=3 or not all(abs(l) in live for l in args):
                raise ValueError('invalid CLAUSE')
        else:raise ValueError('invalid event')
        width=max(width,len(live))
    if live:raise ValueError('unclosed variables')
    return width

def blocks(src,B):
    live=set()
    for start in range(0,len(src),B):
        left=tuple(sorted(live));cnf=[]
        for i in range(start,min(start+B,len(src))):
            kind,args=src.read(i)
            if kind=='O':live.add(args[0])
            elif kind=='X':live.remove(args[0])
            else:cnf.append(args)
        yield left,tuple(sorted(live)),tuple(cnf)

class Child:
    """One genuine ordinary proper-3CNF buffer, immutable during each call."""
    def __init__(self,cnf,boundary,stats):
        self.stats=stats;self.locked=False;self.version=0
        ids=sorted({abs(l) for c in cnf for l in c}|set(boundary))
        self.ids=ids;self.local={x:i+1 for i,x in enumerate(ids)}
        self.boundary=tuple(boundary);self.pin_offsets=[]
        body=[tuple((1 if l>0 else -1)*self.local[abs(l)] for l in c) for c in cnf]
        n=len(ids)+2*len(boundary);m=len(body)+4*len(boundary)
        self.words=[n,m]+[l for c in body for l in c]
        stats['body_header_writes']+=len(self.words)
        for i,x in enumerate(boundary):
            a,b=len(ids)+2*i+1,len(ids)+2*i+2
            offsets=[]
            for sa in (1,-1):
                for sb in (1,-1):
                    offsets.append(len(self.words))
                    self.words.extend((-self.local[x],sa*a,sb*b))
                    stats['pin_initialization_writes']+=3
            self.pin_offsets.append(tuple(offsets))
        self.mask=0
        stats['max_child_words']=max(stats['max_child_words'],len(self.words))
        stats['max_local_map_words']=max(stats['max_local_map_words'],2*len(ids)+4*len(boundary))
    def change(self,i):
        if self.locked:raise RuntimeError('cannot mutate a live child input')
        self.mask^=1<<i
        val=self.local[self.boundary[i]]*(1 if self.mask>>i&1 else -1)
        for offset in self.pin_offsets[i]:
            self.words[offset]=val;self.stats['pin_patch_writes']+=1
        self.version+=1
    def read(self,i):
        self.stats['child_word_reads']+=1
        return self.words[i]
    def call(self,delay_passes=0):
        if self.locked:raise RuntimeError('recursive borrow')
        self.locked=True;ver=self.version;self.stats['solver_calls']+=1
        self.stats['eager_rebuild_words']+=len(self.words)
        try:
            for _ in range(delay_passes):
                # Explicit extra source probes; no sleeping or uncharged delay.
                for i in range(len(self.words)):self.read(i)
            n,m=self.read(0),self.read(1)
            rows=[tuple(self.read(2+3*j+r) for r in range(3)) for j in range(m)]
            if any(len(set(map(abs,c)))!=3 or not all(1<=abs(l)<=n for l in c) for c in rows):
                raise ValueError('invalid ordinary child')
            self.stats['max_solver_parsed_words']=max(self.stats['max_solver_parsed_words'],3*m+n)
            ans=dpll(rows,self.stats)
            if self.version!=ver:raise RuntimeError('child changed during exact call')
            return ans
        finally:self.locked=False

def project(mask,boundary,target):
    pos={v:i for i,v in enumerate(boundary)}
    return sum(((mask>>pos[v])&1)<<i for i,v in enumerate(target))

def joined(events,B,delay=0,local_check=False,width_budget=None):
    stats=Counter();src=Source(events,stats)
    width=validate(src);stats['observed_width']=width
    if width_budget is not None and width>width_budget:
        # Charged full-source fallback, not part of the small-space theorem.
        cnf=[]
        for i in range(len(src)):
            kind, row=src.read(i)
            if kind=='C': cnf.append(row)
        stats['fallback']=1
        return dpll(cnf,stats),stats,[]
    reach={0};trace=[]
    for j,(left,right,cnf) in enumerate(blocks(src,B)):
        boundary=tuple(sorted(set(left)|set(right)));p=len(boundary)
        child=Child(cnf,boundary,stats);out=set();prev=0
        stats['candidate_states']+=1<<p
        stats['max_frontier_bits']=max(stats['max_frontier_bits'],(1<<len(left))+(1<<len(right)))
        stats['max_union_boundary']=max(stats['max_union_boundary'],p)
        before=stats.copy();called=0
        for z in range(1<<p):
            mask=z^(z>>1)
            if z:
                delta=prev^mask
                if delta&(delta-1):raise AssertionError('not Gray')
                child.change(delta.bit_length()-1)
            prev=mask
            li=project(mask,boundary,left);ri=project(mask,boundary,right)
            stats['projection_bit_visits']+=len(left)+len(right)
            if li not in reach:continue
            ans=child.call(delay);called+=1
            if local_check:
                pins={v:bool(mask>>i&1) for i,v in enumerate(boundary)}
                check(ans==brute(cnf,pins),'pinned_child_exactness')
                fresh=Child(cnf,boundary,Counter())
                for i in range(p):
                    if mask>>i&1:fresh.change(i)
                check(child.words==fresh.words,'buffer_equals_fresh_serialization')
            if ans:out.add(ri)
        trace.append({'block':j,'clauses':len(cnf),'left':len(left),'right':len(right),'union':p,
                      'candidates':1<<p,'calls':called,'reachable_before':len(reach),'reachable_after':len(out),
                      'child_words':len(child.words),'patch_writes':stats['pin_patch_writes']-before['pin_patch_writes']})
        check(trace[-1]['patch_writes']==4*((1<<p)-1),'gray_four_field_updates')
        reach=out
        if not reach:break
    stats['reuse_generation_writes']=stats['body_header_writes']+stats['pin_initialization_writes']+stats['pin_patch_writes']
    stats['blocks_processed']=len(trace)
    return bool(reach),stats,trace

def chain(q,bits):
    # Variable 1 is z_0.
    return [(1,),(-(q+1),)]+[(-i, (i+1) if b else -(i+1)) for i,b in enumerate(bits,1)]

def parity_cycle(q,odd=False):
    cnf=[]
    for i in range(q):
        a,b=i+1,(i+1)%q+1
        if odd and i==0:cnf.extend(((a,b),(-a,-b)))
        else:cnf.extend(((-a,b),(a,-b)))
    return properize(cnf)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');args=parser.parse_args()
    rng=random.Random(20261024); cases=[];scaling=[];counts=Counter();t0=time.monotonic()
    def run(name,cnf,B,expected=None,local=False,delay=0,cap=None):
        events,renamed=event_input(cnf)
        ans,st,tr=joined(events,B,delay,local,cap)
        ref=brute(renamed) if expected is None else expected
        check(ans==ref,'parent_answer')
        counts['SAT' if ans else 'UNSAT']+=1
        record={'name':name,'records':len(events),'block_records':B,'answer':ans,'counters':dict(st),'trace':tr}
        cases.append(record);return record
    # The exact chain baseline, including both labels and equal-length flips.
    for q in range(1,7):
        for bits in product((0,1),repeat=q):
            f=chain(q,bits)
            check(brute(f)==(not all(bits)),'chain_baseline')
            if q<=4:
                run(f'chain-{q}-{bits}',properize(f),5,not all(bits),local=True)
    # All subsets of the three-variable cube; unconstrained duplicate-free proper clauses.
    cube=list(product((1,-1),(2,-2),(3,-3)))
    for mask in range(1,256):
        cnf=[cube[i] for i in range(8) if mask>>i&1]
        run(f'cube-{mask}',cnf,4,local=True)
    # Seeded general signed instances and shuffled clauses.
    for i in range(100 if args.quick else 240):
        n=rng.randrange(3,8);m=rng.randrange(1,15)
        cnf=[tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),3)) for _ in range(m)]
        run(f'random-{i}',cnf,rng.randrange(3,9),local=i<40,delay=2 if i<12 else 0)
    for q in (4,8,16,32,64) if args.quick else (4,8,16,32,64,128):
        for odd in (False,True):
            cnf=parity_cycle(q,odd);events,_=event_input(cnf)
            rec=run(f'parity-{q}-{odd}',cnf,max(4,math.isqrt(len(events))),not odd,delay=1)
            scaling.append({k:v for k,v in rec.items() if k!='trace'})
    # Boundary consistency must not be replaced by isolated SAT bits.
    blocks_small=[((1,2,3),),((-1,4,5),)]
    # Force x in one block and not x in another, with fresh private auxiliaries.
    contradiction=properize([(1,),(-1,)])
    check(all(brute(contradiction[i:i+4]) for i in (0,4)),'local_satisfiable_parts')
    run('incompatible-local-witnesses',contradiction,6,False,local=True)
    # Label-blind fallback switch with both SAT and UNSAT controls.
    for name,cnf,ans in [('horn-SAT',properize([(1,),(-1,2)]),True),
                          ('horn-UNSAT',properize([(1,),(-1,2),(-2,)]),False),
                          ('highwidth-SAT',cube[:-1],True),('highwidth-UNSAT',cube,False)]:
        rec=run(name,cnf,5,ans,cap=1)
        check(rec['counters'].get('fallback')==1,'charged_fallback_selection')
    # Invalid scope and immutable-live-input guards.
    for bad in [(('O',(1,)),('X',(1,)),('C',(1,2,3))),
                (('O',(1,)),('X',(1,)),('O',(1,))),
                (('O',(1,)),('O',(3,)))]:
        try:validate(Source(bad,Counter()));ok=False
        except ValueError:ok=True
        check(ok,'invalid_scope_rejected')
    c=Child(((1,2,3),),(1,),Counter());c.locked=True
    try:c.change(0);ok=False
    except RuntimeError:ok=True
    check(ok,'mutation_during_call_rejected')
    # Exact recurrence endpoint, no inference from scoped promise to all-input SAT.
    c0=Fraction(241,200);beta=((c0+2)/c0**2-c0)/2
    check(beta-Fraction(1,2)==Fraction(26279,23232400),'exact_endpoint_margin')
    a,lam,t=Fraction(3,5),Fraction(1,2),Fraction(6,5)
    check(max(Fraction(1),a+lam*t)==Fraction(6,5),'scoped_resource_exponent')
    result={'name':'QUIESCENT_CHILD_REUSE','status':'COMPUTATIONAL; scoped theorem only; P vs NP OPEN',
            'seed':20261024,'checks':dict(CHECKS),'total_checks':sum(CHECKS.values()),'failures':0,
            'labels':dict(counts),'instances':len(cases),'scaling':scaling,
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'elapsed_seconds_not_a_complexity_bound':time.monotonic()-t0,
            'limitations':['Benchmark event_input uses full metadata; it is not the missing ordinary-SAT normalizer.',
                            'Python sets implement frontier bitsets for testing; theorem packs bitsets explicitly.',
                            'Counters are abstract source/word/literal events, not RAM instructions or process RSS.',
                            'Solver DPLL workspace/cost is separate from construction; no polynomial solver claim.',
                            'No assumption that incoming solver retains state across changed children.'],
            'cases':cases}
    Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('name','instances','labels','total_checks','failures','elapsed_seconds_not_a_complexity_bound')},indent=2))
    for r in scaling:
        s=r['counters']; print(r['name'],'calls',s.get('solver_calls'), 'eager',s.get('eager_rebuild_words'),
                              'reuse',s.get('reuse_generation_writes'),'source',s.get('source_word_reads'),
                              'buffer',s.get('max_child_words'),'frontier',s.get('max_frontier_bits'))
if __name__=='__main__':main()
