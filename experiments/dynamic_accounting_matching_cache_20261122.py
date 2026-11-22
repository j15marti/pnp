"""Exact suffix-event audit for conjunctions of paid prism matching results."""
from itertools import product
from fractions import Fraction
from collections import defaultdict
import json

def trace(bits):
    tape = {i:str(b) for i,b in enumerate(bits)}
    tape[len(bits)] = "#"
    events=[]
    for address in range(len(bits)):
        bit=int(tape[address])
        events.append({"event":len(events),"address":address,"payload":bit})
        if bit==0:
            break
    return events

def run():
    results=[]
    for k in range(1,13):
        total_reads=0
        fibers=[defaultdict(list) for _ in range(k)]
        small=[]
        for bits in product((0,1),repeat=k):
            events=trace(bits)
            reached={e["address"]:e for e in events}
            total_reads+=len(events)
            assert all(bits)==all(e["payload"] for e in events)
            for j in range(k):
                active=all(bits[:j])
                value=bits[j] if active else 0
                record=str(bits[j]) if active else ""
                assert (j in reached)==active
                assert record==("" if j not in reached else str(reached[j]["payload"]))
                assert value==(int(record) if active else 0)
                fibers[j][bits[:j]].append((value,record))
            assert len({e["event"] for e in events})==len(events)
            if k<=3:small.append({"bits":bits,"events":events})
        entropy_sum=Fraction(0)
        for j in range(k):
            for prefix, items in fibers[j].items():
                codebook={r for _,r in items}
                if all(prefix):
                    assert codebook=={"0","1"}
                    assert sum(v for v,_ in items)*2==len(items)
                    entropy_sum+=Fraction(len(items),2**k)
                else:
                    assert codebook=={""} and all(v==0 for v,_ in items)
        expected=Fraction(total_reads,2**k)
        assert expected==entropy_sum==2-Fraction(1,2**(k-1))
        results.append({"k":k,"inputs":2**k,"total_reads":total_reads,
                        "expected_reads":str(expected),"entropy_sum":str(entropy_sum),
                        "rho":1,"max_reads":k,"expected_payload_span_sum":str((k+1)*expected),
                        "small_traces":small})
    return {"cases":sum(x["inputs"] for x in results),"results":results,
            "scope":"suffix only; full matching prefix remains symbolic",
            "seed":None}

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
