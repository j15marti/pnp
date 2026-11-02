#!/usr/bin/env python3
"""Independent declared canonical ASCII-original grammar checks.
This source-indexed format is deliberately explicit and is not the
unique repository wire format. Reject malformed text, never label UNSAT.
"""
from collections import Counter
import json,re
POS=[(1,2,4),(1,3,5),(2,4,6),(3,5,6)]
NEG=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
def encode(n,pos,neg):
    rows=['n='+str(n)]+['+'+','.join(map(str,c)) for c in pos]+['-'+','.join(map(str,c)) for c in neg]
    return ('\n'.join(rows)+'\n').encode('ascii')
def parse(raw):
    if type(raw) is not bytes:raise ValueError('bytes required')
    text=raw.decode('ascii','strict')
    if '\r' in text or not text.endswith('\n'):raise ValueError('LF required')
    rows=text[:-1].split('\n')
    if not re.fullmatch(r'n=[1-9][0-9]*',rows[0]):raise ValueError('bad n header')
    n=int(rows[0][2:])
    if n<3 or n%3 or len(rows)!=1+4*n//3:raise ValueError('wrong size')
    counts=Counter();seen=set()
    for row in rows[1:]:
        if not re.fullmatch(r'[+-][1-9][0-9]*(?:,[1-9][0-9]*){2}',row):raise ValueError('malformed clause')
        sign=row[0];c=tuple(map(int,row[1:].split(',')))
        if c!=tuple(sorted(c)) or len(set(c))!=3 or c[-1]>n:raise ValueError('source names')
        key=(sign,c)
        if key in seen:raise ValueError('duplicate signed clause')
        seen.add(key)
        for x in c:counts[(x,sign)]+=1
    if any(counts[(x,'+')]!=2 or counts[(x,'-')]!=2 for x in range(1,n+1)):raise ValueError('signed source quota')
    return n,seen
def main():
    source=encode(6,POS,NEG);parse(source);parse(encode(6,NEG,NEG))
    bad=[
      source+b'\xff',source[:-1],source.replace(b'n=6',b'n=7',1),
      source.replace(b'n=6',b'n=06',1),source.split(b'\n',1)[1],
      source.replace(b'+1,3,5',b'+1,2,4',1),
      source.replace(b'+1,3,5',b'-1,3,5',1),
      source.replace(b'+1,2,4',b'+1,1,4',1),
      source.replace(b'+1,2,4',b'+1,2,7',1),
      source.replace(b'+1,2,4',b'+1,2,-4',1),
      source.replace(b'+1,2,4',b'+2,1,4',1),
      source+b'+1,2,4\n',source.split(b'\n',3)[0]+b'\n',
      source.replace(b'+1,2,4',b'+1,2',1),
      source.replace(b'\n',b'\r\n'),source+b'junk\n',
      b'\xc3\xa4'+source,source.replace(b'-1,2,3',b'-1,2,4',1),
      source.replace(b'+1,2,4',b'+1,\x002,4',1),
      source.replace(b'+1,2,4',b'+0,2,4',1),
    ]
    for i,b in enumerate(bad):
        try:parse(b)
        except (ValueError,UnicodeError):continue
        raise AssertionError('bad source accepted '+str(i))
    print(json.dumps({'status':'PASS','valid_sources_checked':2,'malformed_declared_binary_strings_rejected':len(bad),'scope':'declared ASCII bytes, not native FLMV machine'}))
if __name__=='__main__':main()
