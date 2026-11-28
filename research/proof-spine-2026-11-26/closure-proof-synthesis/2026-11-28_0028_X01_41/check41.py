"""Independent prefix certificate check; audit39.project reconstructs exact native chart from authenticated original bytes."""
import audit39 as source
import json
from pathlib import Path

def check(c,F,meta):
    assert c['instance_id']=='STRICT-EB4-v1:sha256:'+meta['input_hash']
    assert c['original_N_bits']==meta['N']
    for k in ('guard_id','residual_id','chart_hash','map_hash'):assert c[k]==meta[k]
    assert c['source_rows']==len(F)
    db=list(F);vis=0
    # independent scalar UP implementation; no graph-derived reason trusted for RUP
    for row in c['proof_prefix']:
        A=set(-l for l in row)
        conflict=False
        while not conflict:
            changed=False
            for clause in db:
                vis+=len(clause)+1
                if any(l in A for l in clause):continue
                remaining=[l for l in clause if -l not in A]
                if not remaining:conflict=True;break
                if len(remaining)==1:A.add(remaining[0]);changed=True
            if not changed and not conflict:raise AssertionError('RUP failed')
        db.append(row)
    def path(P):
        assert P
        start=P[0][0];prev=start
        for u,v,i in P:
            assert u==prev and 0<=i<len(db)
            row=db[i]
            assert (len(row)==1 and row[0]==v and u==-v) or (len(row)==2 and sorted(row)==sorted([-u,v]))
            prev=v
        return start,prev
    u,v=path(c['path_forward']);w,z=path(c['path_backward'])
    assert u==-v and w==v and z==u
    return vis
if __name__=='__main__':
    P=Path(__file__).parent
    out={}
    for n in ('joint','random'):
        F,C,mp,m=source.project(n)
        c=json.loads((P/(n+'41.scc.cert.json')).read_bytes())
        vis=check(c,F,m)
        import copy
        corrupt=copy.deepcopy(c);corrupt['path_forward'][0][2]=-1
        try:check(corrupt,F,m)
        except AssertionError:pass
        else:raise AssertionError('corrupt certificate accepted')
        out[n]={'verified':True,'rup_literal_plus_row_visits':vis,'path_edges':len(c['path_forward'])+len(c['path_backward']),'corrupt_rejected':True}
    (P/'check41.json').write_bytes(source.enc(out));print(out)
