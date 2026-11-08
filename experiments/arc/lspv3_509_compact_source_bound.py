#!/usr/bin/env python3
"""Source-bound, trace-only Tseitin SOURCE/AND3/XOR control; NOT historical R_mix341 bytes."""
import hashlib,itertools,json,math

def family(name):
    if name=='K4':h=4;E=[(a,b) for a in range(4) for b in range(a+1,4)]
    elif name=='K33':h=6;E=[(a,b) for a in range(3) for b in range(3,6)]
    elif name=='cube':h=8;E=[(a,b) for a in range(8) for b in range(a+1,8) if (a^b).bit_count()==1]
    else:
        r=int(name.replace('prism',''));h=2*r
        E=sorted({tuple(sorted((u,v))) for i in range(r) for u,v in ((i,(i+1)%r),(i+r,(i+1)%r+r),(i,i+r))})
    assert len(E)*2==3*h
    C=[];groups=[]
    for v in range(h):
        xs=[i+1 for i,e in enumerate(E) if v in e];assert len(xs)==3
        g=[]
        for b in itertools.product((0,1),repeat=3):
            if sum(b)%2!=(v==0):
                g.append(len(C));C.append(tuple(-x if t else x for x,t in zip(xs,b)))
        groups.append(g)
    src=('p cnf %s %s\n'%(len(E),len(C))+''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode()
    P=[['S',j] for j in range(len(C))];current=[]
    for a,b,c,d in groups:
        u=len(P);P.append(['A',a,b]);v=len(P);P.append(['A',c,d]);z=len(P);P.append(['A',u,v]);current.append(z)
    while len(current)>1:
        nextrow=[]
        for i in range(0,len(current),2):
            if i+1==len(current):nextrow.append(current[i]);continue
            j=len(P);P.append(['X',current[i],current[i+1]]);nextrow.append(j)
        current=nextrow
    cert={'nodes':P,'root':current[0],'source_sha256':hashlib.sha256(src).hexdigest()}
    packet=json.dumps(cert,sort_keys=True,separators=(',',':')).encode()
    return src,packet

def verify(src,packet):
    if not isinstance(src,bytes) or not src.endswith(b'\n'):raise ValueError('source bytes')
    lines=src.decode('ascii').splitlines();H=lines[0].split(' ')
    if len(H)!=4 or H[:2]!=['p','cnf'] or not all(t.isdigit() and t[0]!='0' for t in H[2:]):raise ValueError('header')
    n,m=map(int,H[2:]);C=[]
    if len(lines)!=m+1:raise ValueError('source count')
    for line in lines[1:]:
        t=line.split(' ')
        if t[-1]!='0' or len(t)!=4 or any(not x.lstrip('-').isdigit() or x in ('0','-0') for x in t[:-1]):raise ValueError('clause')
        c=tuple(map(int,t[:-1]))
        if len({abs(x) for x in c})!=3 or not all(1<=abs(x)<=n for x in c):raise ValueError('literals')
        C.append(c)
    def strict(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ValueError('duplicate key')
            d[k]=v
        return d
    o=json.loads(packet.decode('ascii'),object_pairs_hook=strict)
    if json.dumps(o,sort_keys=True,separators=(',',':')).encode()!=packet:raise ValueError('noncanonical packet')
    P=o['nodes'];root=o['root']
    if type(root)!=int or root!=len(P)-1 or o['source_sha256']!=hashlib.sha256(src).hexdigest():raise ValueError('source binding')
    if P[:m]!=[['S',j] for j in range(m)]:raise ValueError('source positions')
    slot=[];depth=[]
    for i,row in enumerate(P):
        if not isinstance(row,list) or len(row) not in (2,3) or row[0] not in ('S','A','X'):raise ValueError('node')
        op=row[0];pa=row[1:]
        if any(type(x)!=int or x<0 for x in pa):raise ValueError('bad index type')
        if op=='S':
            if i>=m or row!=['S',i]:raise ValueError('source reference')
            support=tuple(sorted(map(abs,C[i])));tab=0
            for j in range(8):
                bits={x:(j>>k)&1 for k,x in enumerate(support)}
                if any(bits[abs(l)]==(l>0) for l in C[i]):tab|=1<<j
            slot.append(('f',support,tab));depth.append(0);continue
        if len(pa)!=2 or any(x>=i for x in pa):raise ValueError('DAG order')
        a,b=[slot[j] for j in pa];depth.append(1+max(depth[j] for j in pa))
        if op=='A':
            if a[0]!='f' or b[0]!='f':raise ValueError('factor type')
            support=tuple(sorted(set(a[1])|set(b[1])))
            if len(support)>3 or any(v>n for v in support):raise ValueError('AND support')
            def ev(f,bits):
                j=sum(bits[x]<<k for k,x in enumerate(f[1]));return (f[2]>>j)&1
            tab=0
            for j in range(1<<len(support)):
                bits={x:(j>>k)&1 for k,x in enumerate(support)}
                if ev(a,bits) and ev(b,bits):tab|=1<<j
            affine=None
            if len(support)==3:
                for rhs in (0,1):
                    if tab==sum(1<<j for j in range(8) if j.bit_count()%2==rhs):affine=('r',sum(1<<(x-1) for x in support),rhs)
            slot.append(affine or ('f',support,tab))
        elif op=='X':
            if a[0]!='r' or b[0]!='r':raise ValueError('XOR type')
            slot.append(('r',a[1]^b[1],a[2]^b[2]))
        else:raise ValueError('rule')
    if slot[root]!=('r',0,1):raise ValueError('not UNSAT')
    return {'source_bytes':len(src),'trace_bytes':len(packet),'paid':len(P)-m,'depth':depth[root]}

if __name__=='__main__':
    for name in ['K4','K33','cube','prism8','prism16','prism32','prism64']:
        src,pkt=family(name);r=verify(src,pkt)
        try:verify(src+b'\n',pkt);raise AssertionError('bad source accepted')
        except ValueError:pass
        print(name, r)
