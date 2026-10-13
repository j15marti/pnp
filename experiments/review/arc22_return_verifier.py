#!/usr/bin/env python3
"""Independent bounded arithmetic check for ARC22RETURN1, not a lower-bound proof.
Requires the pinned universal22.py and image22_decoder_audit.py in this directory.
The larger phase/profiling runner and full raw outputs accompany the report ZIP.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time
import universal22 as u
import image22_decoder_audit as d

START = time.monotonic()
COUNTS = Counter()


def check(condition, name):
    if time.monotonic() - START > 25:
        raise TimeoutError('25-second cooperative deadline')
    COUNTS[name] += 1
    if not condition:
        raise AssertionError(name)


def git_blob(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def encoded_bytes(v):
    return 5 * (4*v//3) + 2*v + 4*sum(len(str(i)) for i in range(1,v+1)) + 1


def is22(F):
    counts = Counter(l for c in F for l in c)
    return all(counts[x] == counts[-x] == 2 for x in range(1,u.check_proper(F)+1))


def main():
    check(git_blob(u.__file__) == 'f985a13f237f2322f988ec82af132625acf3912c','compiler_pin')
    check(git_blob(d.__file__) == 'd5a551a1ee0082566d6a370e32df9e5fbdab70e0','decoder_pin')
    cube = [tuple((i+1)*(1 if b[i] else -1) for i in range(3))
            for b in itertools.product((0,1),repeat=3)]
    for mask in range(1,256):
        F = [cube[j] for j in range(8) if mask >> j & 1]
        compiled = u.compile22(F)
        y = d.encode(compiled.clauses)
        B = d.decode_image(y).balanced
        m = len(B)
        counts = Counter(l for c in B for l in c)
        for x in sorted({1,u.check_proper(B)}):
            r = counts[x]
            for b in (0,1):
                R = [tuple(l for l in c if abs(l)!=x) for c in B if (x if b else -x) not in c]
                variables = sorted({abs(l) for c in R for l in c})
                relabel = {v:i+1 for i,v in enumerate(variables)}
                R = [tuple(relabel[abs(l)]*(1 if l>0 else -1) for l in c) for c in R]
                P,_ = u.properize23(R)
                child = u.compile22(P)
                check(len(R)==m-r,'native_count')
                check(len(P)==m,'proper_count')
                check(2*r <= child.padding_gadgets <= 6*r,'padding_interval')
                check(len(child.clauses)==12*(m+7*child.padding_gadgets),'return_count')
                check(len(d.encode(child.clauses))==encoded_bytes(child.n),'exact_bytes')
                check(len(d.encode(child.clauses))>len(y),'strict_expansion')
    nested = u.W1
    rows = []
    for depth in range(4):
        if depth:
            nested = u.compile22(nested).clauses
        y = d.encode(nested)
        original_bytes = len(y)
        steps = 0
        while True:
            D = d.decode_image(y)
            if D is None or not is22(D.balanced):
                break
            z = d.encode(D.balanced)
            check(12*len(z)<len(y),'typed_contraction')
            y=z
            steps+=1
        check(y==d.encode(u.W1) and steps==depth,'exact_uniform_depadding')
        rows.append({'depth':depth,'input_bytes':original_bytes,'output_bytes':len(y)})
    print(json.dumps({'run_id':'ARC22RETURN1','status':'COMPUTATIONAL',
          'assertions':sum(COUNTS.values()),'checks':dict(COUNTS),'failures':0,
          'elapsed_seconds':time.monotonic()-START,'seed':None,'depadding':rows,
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
