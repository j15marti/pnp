#!/usr/bin/env python3
"""TMR-1/046: native CPython regression for the indexed family recognizer.
Finite checks are COMPUTATIONAL; the indexed-family ceiling is a symbolic theorem.
"""
import itertools
import json
from collections import deque

MAGIC = '00110101'


def gamma(n):
    b = format(n, 'b')
    return '0' * (len(b)-1) + b


def length(m):
    H, E = 4*m, 6*m
    w = E.bit_length()
    return len(MAGIC) + len(gamma(E)) + len(gamma(4*H)) + 12*H*(w+1)


def graph(m):
    t = 2*m
    edges = sorted({tuple(sorted((a,b))) for i in range(t)
                    for a,b in ((i,(i+1)%t),(t+i,t+(i+1)%t),(i,t+i))})
    inc = [[] for _ in range(2*t)]
    for j,(a,b) in enumerate(edges):
        inc[a].append(j)
        inc[b].append(j)
    return edges, [sorted(x) for x in inc]


def source(m):
    edges, inc = graph(m)
    H, E = len(inc), len(edges)
    clauses = []
    for v in range(H):
        charge = int(v == 0)
        forbidden = [s for s in itertools.product((0,1),repeat=3)
                     if (s[0]^s[1]^s[2]) != charge]
        tail = next(s for s in forbidden if s[2] == 0)
        for s in [q for q in forbidden if q != tail]+[tail]:
            clauses.append([(inc[v][j]+1,s[j]) for j in range(3)])
    body = ''.join(format(e, f'0{E.bit_length()}b')+str(s)
                   for clause in clauses for e,s in clause)
    original = MAGIC + gamma(E)+gamma(len(clauses))+body
    assert original[-1] == '0' and len(original) == length(m)
    return original, original[:-1]+'1'


def parse(bits):
    """Decode and validate our explicit proper signed 3-CNF grammar."""
    if not bits.startswith(MAGIC) or set(bits)-{'0','1'}:
        return None
    at = len(MAGIC)
    def get_gamma():
        nonlocal at
        z=0
        while at+z<len(bits) and bits[at+z]=='0':
            z+=1
        if at+2*z>=len(bits):
            raise ValueError('truncated gamma')
        ans=int(bits[at+z:at+2*z+1],2)
        at+=2*z+1
        return ans
    try:
        E,M=get_gamma(),get_gamma()
        if E<3 or M<1 or (len(bits)-at)!=3*M*(E.bit_length()+1):
            return None
        clauses=[]
        for _ in range(M):
            C=[]
            for _ in range(3):
                e=int(bits[at:at+E.bit_length()],2)
                at+=E.bit_length()
                sign=int(bits[at]);at+=1
                C.append((e,sign))
            if len({e for e,s in C})!=3 or not all(1<=e<=E for e,s in C):
                return None
            clauses.append(C)
        if len({tuple(C) for C in clauses})!=len(clauses):
            return None
        assert at==len(bits)
        return E,clauses
    except (ValueError,IndexError):
        return None


def recognize(bits):
    """Polynomial-time family match on the ENTIRE source, no SAT oracle."""
    N=len(bits)
    m=2
    while length(m)<=N:
        if length(m)==N:
            original,mutant=source(m)
            if bits==original:
                return False,m
            if bits==mutant:
                return True,m
        m+=1
    return None


def decide(bits):
    """One fixed total proper-3CNF SAT decider, exponential off family."""
    parsed=parse(bits)
    if parsed is None:
        return False
    found=recognize(bits)
    if found is not None:
        return found[0]
    E,clauses=parsed
    for assign in itertools.product((0,1),repeat=E):
        if all(any((assign[e-1]^s)==1 for e,s in C) for C in clauses):
            return True
    return False


def main():
    rows=[]
    assertions=0
    for m in range(2,41):
        f,g=source(m)
        assert len(f)==length(m)==len(g);assertions+=1
        assert sum(a!=b for a,b in zip(f,g))==1;assertions+=1
        assert parse(f) is not None and parse(g) is not None;assertions+=2
        assert recognize(f)==(False,m) and recognize(g)==(True,m);assertions+=2
        assert decide(f) is False and decide(g) is True;assertions+=2
        assert length(m+1)>length(m);assertions+=1
        rows.append(dict(m=m,N=length(m),tested_source_bits=12*4*m,
                         index_length_checks=m-1,known_labels=['UNSAT','SAT']))
    # A syntactically valid nonfamily formula must trigger the exact SAT fallback.
    E=3;w=E.bit_length()
    def encode(clauses):
        return MAGIC+gamma(E)+gamma(len(clauses))+''.join(
            format(e,f'0{w}b')+str(s) for C in clauses for e,s in C)
    sat=encode([[(1,0),(2,0),(3,0)]])
    unsat=encode([[(1,s[0]),(2,s[1]),(3,s[2])]
                  for s in itertools.product((0,1),repeat=3)])
    assert recognize(sat) is None and recognize(unsat) is None;assertions+=2
    assert decide(sat) is True and decide(unsat) is False;assertions+=2
    # Malformed-input guard: fixed finite decider rejects invalid bit strings.
    for bad in ('', '0', 'foobar', sat+'0'):
        assert decide(bad) is False;assertions+=1
    out={'case':'TMR1_EFFECTIVE_FAMILY046','status':'COMPUTATIONAL',
         'python':'CPython standard library','family':'circular-ladder odd Tseitin and one-bit SAT mutant',
         'm_min':2,'m_max':40,'family_members_checked':78,'index_upper_enumeration':40,
         'assertions':assertions,'failures':0,'rows':rows,
         'claim':'A fixed total decider recognizes these well-labeled instances in polynomial time; fallback is exhaustive.',
         'limitation':'Finite implementation tests do not prove asymptotic complexity or P versus NP.'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
