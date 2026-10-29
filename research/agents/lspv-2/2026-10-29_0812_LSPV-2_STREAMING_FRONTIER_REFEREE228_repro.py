#!/usr/bin/env python3
"""Independent finite audit of source-authenticated cyclic-scope signed 3CNF.

A sequential read-only input head is explicitly charged for every symbol
scanned and every physical rewind. The Python implementation is a model
simulator, NOT a native one- or two-tape TM timing measurement.
No stored clause list, per-variable sign-count table, or position index is used
by the streaming decision routine; its live logical state has constant many
O(log n)-bit integers plus an at-most-16-bit relation mask.
"""
from __future__ import annotations
import json
import random
from collections import Counter
from itertools import product

class ReadOnlyTape:
    def __init__(self, text):
        self.source = text  # read-only input does not count as writable work space
        self.pos = 0
        self.moves = 0
        self.reads = 0
        self.rewinds = 0
        self.peak_index = 0
    def reset(self):
        if self.pos:
            self.moves += self.pos  # physically move the input head to the left end
            self.pos = 0
            self.rewinds += 1
    def token_stream(self):
        self.reset()
        value = 0
        sign = 1
        active = False
        has_digit = False
        while self.pos < len(self.source):
            c = self.source[self.pos]
            self.pos += 1
            self.moves += 1
            self.reads += 1
            self.peak_index = max(self.peak_index,self.pos)
            if c == '-' and not active:
                sign, active = -1, True
            elif '0' <= c <= '9':
                value = value * 10 + ord(c) - ord('0')
                if value > len(self.source):
                    raise ValueError('oversized numeric token')
                active = True
                has_digit = True
            elif c in ' \n\t\r':
                if active:
                    if not has_digit:
                        raise ValueError('a sign without digits')
                    yield sign * value
                    value, sign, active, has_digit = 0, 1, False, False
            else:
                raise ValueError('invalid character')
        if active:
            if not has_digit:
                raise ValueError('trailing sign')
            yield sign * value
    def rows(self):
        tokens = self.token_stream()
        try:
            n = next(tokens)
        except StopIteration:
            raise ValueError('no variable count')
        if n < 3 or n % 3:
            raise ValueError('bad variable count')
        ci = 0
        row = []
        for v in tokens:
            if v == 0:
                if len(row) != 3:
                    raise ValueError('not a proper ternary clause')
                yield n,ci,tuple(row)
                ci += 1
                row=[]
            else:
                if abs(v)>n:
                    raise ValueError('out of range')
                row.append(v)
                if len(row)>3:
                    raise ValueError('clause too long')
        if row or ci != n+n//3:
            raise ValueError('incorrect clause count')

def cycle_scopes(n):
    return [tuple((i+j)%n for j in range(3)) for i in range(n)] + [tuple(range(i,i+3)) for i in range(0,n,3)]

def canonical_encoding(cs,n):
    return str(n)+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs)

def checked_rows(tape,n,check_balance=False):
    count=0
    for observed,ci,row in tape.rows():
        if observed!=n:
            raise ValueError('inconsistent source variable count')
        if ci<n:
            scope = ((ci%n)+1,((ci+1)%n)+1,((ci+2)%n)+1)
        else:
            j=(ci-n)*3
            scope = (j+1,j+2,j+3)
        if tuple(abs(x) for x in row)!=scope:
            raise ValueError('source is not the canonical cyclic-scope class')
        count+=1
        if check_balance:
            yield ci,row
    if count != n+n//3:
        raise ValueError('bad clause count')

def following_indices(n,j):
    """Precomputed from the public family grammar, never a free source table."""
    if j==n-1:
        return ()
    return tuple(sorted(set(range(min(j,1)+1)) | set(v for v in (j-1,j) if 0<=v<=j)))

def decide_cyclic_stream(source,require_balanced=True):
    tape=ReadOnlyTape(source)
    tokens=tape.token_stream()
    try:n=next(tokens)
    except StopIteration:raise ValueError('empty source')
    if n<3 or n%3:raise ValueError('source has invalid n')
    # Full grammar authentication without storing clause lists.
    sum(1 for _ in checked_rows(tape,n))
    if require_balanced:
        # For every name, use a separate paid scan: no uncharged O(n) occurrence table.
        for v in range(1,n+1):
            positive=negative=0
            for ci,row in checked_rows(tape,n,check_balance=True):
                positive+=sum(l==v for l in row)
                negative+=sum(l==-v for l in row)
            if (positive,negative)!=(2,2):
                raise ValueError('not exact-(2,2)')
    old=()
    mask=1
    stages=0
    candidates=0
    peak_live_count=1
    peak_frontier=0
    max_closed_clauses=0
    for j in range(n):
        # Read source again and retain at most 4 just-closing clauses.
        close=[]
        for ci,row in checked_rows(tape,n,check_balance=True):
            if max(abs(l)-1 for l in row)==j:
                close.append(row)
        assert len(close)<=4
        max_closed_clauses=max(max_closed_clauses,len(close))
        nxt=following_indices(n,j)
        assert len(nxt)<=4
        newmask=0
        for k in range(1<<len(old)):
            if not ((mask>>k)&1):continue
            for bit in (0,1):
                candidates+=1
                # Constant-size map, since |old|<=4, not an N-element truth table.
                a={v:(k>>i)&1 for i,v in enumerate(old)}
                a[j]=bit
                if all(any(a[abs(l)-1]==(l>0) for l in row) for row in close):
                    index=sum(a[v]<<i for i,v in enumerate(nxt))
                    newmask|=1<<index
        old=nxt
        mask=newmask
        stages+=1
        peak_frontier=max(peak_frontier,len(nxt))
        peak_live_count=max(peak_live_count,mask.bit_count())
    assert old==()
    return bool(mask),{
        'n':n, 'source_bytes':len(source.encode('ascii')),
        'input_read_symbols':tape.reads,'input_head_moves':tape.moves,
        'input_rewinds':tape.rewinds,'max_input_head_index':tape.peak_index,
        'stages':stages,'candidates':candidates,'max_frontier':peak_frontier,
        'max_feasible_states':peak_live_count,'max_closed_clauses':max_closed_clauses,
        'logical_writable_bits_upper_bound':'O(log n) with at most 16-bit relation and 4 ternary rows',
        'model':'instrumented input-head simulator, not native TM runtime'
    }

def sign_variant(n,rng):
    scopes=cycle_scopes(n)
    locs=[[] for _ in range(n)]
    for ci,scope in enumerate(scopes):
        for j,v in enumerate(scope):locs[v].append((ci,j))
    cs=[[v+1 for v in scope] for scope in scopes]
    for v,places in enumerate(locs):
        assert len(places)==4
        neg=set(rng.sample(range(4),2))
        for k,(ci,j) in enumerate(places):
            if k in neg:cs[ci][j]*=-1
    return tuple(tuple(c) for c in cs)

def brute(cs,n):
    for k in range(1<<n):
        if all(any(bool(k>>(abs(l)-1)&1)==(l>0) for l in row) for row in cs):
            return True
    return False

def W1_control():
    s='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
    unsat=tuple(tuple(map(int,row.split())) for row in s.split(';'))
    sat=[list(r) for r in unsat]
    sat[0][0]*=-1
    sat[7][0]*=-1
    sat=tuple(map(tuple,sat))
    for cs in [unsat,sat]:
        counts=Counter(l for row in cs for l in row)
        assert all(counts[i]==counts[-i]==2 for i in range(1,16))
        assert len(cs)==20 and all(len({abs(l) for l in row})==3 for row in cs)
    assert not brute(unsat,15) and brute(sat,15)
    assert [tuple(abs(l) for l in row) for row in unsat] == [tuple(abs(l) for l in row) for row in sat]
    return {'unsigned_scopes_identical':True,'all_names_2P_2N':True,
            'unsat_label':False,'sat_label':True,
            'flipped_sign_positions':[(0,0),(7,0)]}

def run():
    rng=random.Random(20261029)
    cases=[]; checks=0
    for n,reps in [(3,15),(6,15),(9,15),(12,15),(15,5)]:
        for j in range(reps):
            cs=sign_variant(n,rng)
            sat,stats=decide_cyclic_stream(canonical_encoding(cs,n))
            if n<=15:assert sat==brute(cs,n)
            assert stats['input_head_moves']<8*(n+1)*stats['source_bytes']
            assert stats['max_frontier']<=4 and stats['max_feasible_states']<=16
            assert stats['max_closed_clauses']<=4 and stats['candidates']<=32*n
            checks+=1
            if j==0:cases.append(stats|{'sat':sat})
    faults=0
    cs=sign_variant(6,rng)
    src=canonical_encoding(cs,6)
    lines=src.splitlines(keepends=True)
    bad_identifier=lines[:]
    bad_identifier[1]='99'+lines[1][lines[1].find(' '):]
    bad_quota=lines[:]
    tok=lines[1].split()
    tok[0]=str(-int(tok[0]))
    bad_quota[1]=' '.join(tok)+'\n'
    malformed=[src.replace(' 0\n',' 0 0\n',1),
               ''.join(bad_identifier),''.join(bad_quota)]
    for src in malformed:
        try:decide_cyclic_stream(src)
        except (ValueError, AssertionError,KeyError):faults+=1
    assert faults==len(malformed)
    return {'status':'PASS','cases_checked':checks,'malformed_controls':faults,
            'sample_cases':cases,'W1_same_scope_balanced_labels':W1_control(),
            'notes':['Every source scan and rewind charged in symbol-head moves.',
                     'Python runtime and heap are not native TM step/space counts.',
                     'The source class is restricted to cyclic-scope proper strict exact-(2,2)-3CNF.',
                     'No all-input SAT shrinker or P-vs-NP resolution.']}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
