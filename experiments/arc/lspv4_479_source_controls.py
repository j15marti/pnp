"""Original strict signed 3-CNF parity packet checks for LSPV-4/479.
Separate from the exact graph frontier optimizer; Python stdlib only.
"""
from itertools import combinations,product

def graph_edges(name):
    if name=='K4':return 4,list(combinations(range(4),2))
    if name=='K3,3':return 6,[(u,v) for u in range(3) for v in range(3,6)]
    if name=='cube Q3':return 8,[(u,v) for u in range(8) for v in range(u+1,8) if (u^v).bit_count()==1]
    raise ValueError(name)

def make_packets(H,edges,odd):
    inc=[[i+1 for i,(a,b) in enumerate(edges) if a==v or b==v] for v in range(H)]
    assert all(len(row)==3 for row in inc)
    groups=[]
    for v,row in enumerate(inc):
        q=int(odd and v==0)
        clauses=[]
        for bits in product((0,1),repeat=3):
            if bits[0]^bits[1]^bits[2] != q:
                clauses.append(tuple(x if b==0 else -x for x,b in zip(row,bits)))
        assert len(clauses)==4 and len(set(clauses))==4
        groups.append(clauses)
    return groups

def check_packet_auth(packets,H,edges):
    inc=[[i+1 for i,(a,b) in enumerate(edges) if a==v or b==v] for v in range(H)]
    for v,packet in enumerate(packets):
        if len(packet)!=4 or any(len(c)!=3 or [abs(x) for x in c]!=inc[v] for c in packet):return False
        if len(set(packet))!=4:return False
        seen=[]
        for clause in packet:
            forbidden=tuple(int(l<0) for l in clause)
            seen.append(forbidden[0]^forbidden[1]^forbidden[2])
        if len(set(seen))!=1:return False
        if len({tuple(int(l<0) for l in c) for c in packet})!=4:return False
    return True

def sat(packets,a):
    return all(any((((a>>(abs(l)-1))&1)==(l>0)) for l in clause) for packet in packets for clause in packet)

def main():
    rows=[]
    for name in ['K4','K3,3','cube Q3']:
        H,edges=graph_edges(name)
        for odd in (False,True):
            pkts=make_packets(H,edges,odd)
            assert check_packet_auth(pkts,H,edges)
            count=sum(sat(pkts,a) for a in range(1<<len(edges)))
            expected=0 if odd else (1<<(len(edges)-H+1))
            assert count==expected,(name,odd,count,expected)
            bad=[p[:] for p in pkts];bad[0]=pkts[0][:];bad[0][0]=tuple([-pkts[0][0][0]]+list(pkts[0][0][1:]))
            assert not check_packet_auth(bad,H,edges)
            bad2=[p[:] for p in pkts];bad2[0]=pkts[0][:];bad2[0][0]=(pkts[0][0][0],pkts[0][0][0],pkts[0][0][2])
            assert not check_packet_auth(bad2,H,edges)
            rows.append((name,'odd' if odd else 'even',len(edges),count))
    print('Original signed clause cases:',len(rows))
    for row in rows:print(*row)
    print('Exhaustive assignment evaluations:',sum(1<<m for _,_,m,_ in rows))
    print('Out-of-family packet controls rejected:',2*len(rows))
if __name__=='__main__':main()
