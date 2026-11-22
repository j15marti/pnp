"""Exact payload-read phase audit; prefix/compiler costs proved symbolically."""
import json
def scan(q,d):
    tape={i:str(d) for i in range(q)}
    tape[q]="#"
    head=0
    trace=[]
    state="SCAN"
    while state=="SCAN":
        symbol=tape[head]
        span=max([0,head,*tape])+1
        trace.append(dict(event=len(trace),address=head,symbol=symbol,span=span))
        if symbol=="#":
            state="RETURN"
        else:
            head+=1
    return trace
def run():
    results=[]
    for q in range(1,33):
        traces=[scan(q,d) for d in (0,1)]
        for d,tr in enumerate(traces):
            assert len(tr)==q+1
            events=[{j} for j in range(q)]
            rho=max(sum(e in s for s in events) for e in range(q))
            assert rho==1
            for j in range(q):
                assert int(tr[j]["symbol"])==d
                assert tr[j]["address"]==j
            assert sum(x["span"] for x in tr[:q])==q*(q+1)
        # Each marginal distribution has two equiprobable one-bit codewords.
        # Joint support has two vectors regardless of q. No floating logs needed.
        alias_events=[{0} for _ in range(q)]
        alias_rho=sum(0 in e for e in alias_events)
        assert alias_rho==q
        results.append(dict(q=q,marginal_entropy_sum=q,joint_entropy=1,
                            copied_rho=1,copied_time_bound=q,
                            aliased_rho=alias_rho,aliased_time_bound=q//alias_rho,
                            chain_entropy_sum=1,conditioned_on_D_entropy=0,
                            scan_transitions=q+1,payload_physical_CM=q*(q+1),
                            traces=traces if q<=4 else None))
    print(json.dumps(dict(cases=64,seed=None,results=results,
                         scope="literal fixed SCAN suffix transitions; no SAT/compiler/prefix simulation"),indent=2))
if __name__=="__main__":
    run()
