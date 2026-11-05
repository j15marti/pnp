#!/usr/bin/env python3
"""LSPV-2/411 independently reconstructed semantic and corruption checker.
Python >=3.9; checks data produced by JS, no shared code import."""
import sys,json,copy
p=sys.argv[1] if len(sys.argv)>1 else "lspv2_411_raw.json"
raw=json.load(open(p,encoding="utf8"))
checks=0
def ck(value,reason):
    global checks
    if not value: raise AssertionError(reason)
    checks+=1
def verify(data):
    ck(data["schema"]=="LSPV2-411-def-quotient/v1","schema")
    ck(data["k"]==3 and data["original_variables"]==["x","y","z"],"original support")
    ck(data["source_clauses"]==[[1],[-2],[3],[1,2]],"source clauses")
    defs=data["paid_definitions"]
    ck(len(defs)==4,"four paid gates")
    ck([a["out"] for a in defs]==["a","b","c","d"],"fresh names")
    ck([a["gate"] for a in defs]==["XOR","XOR","AND","XOR"],"gate functions")
    ck([a["in"] for a in defs]==[["x","y"],["a","y"],["b","z"],["a","a"]],"ordered positional inputs")
    rows=[]
    ck(len(data["tables"])==8,"table size")
    for code in range(8):
        x=code&1; y=(code>>1)&1; z=(code>>2)&1
        a=(x+y)%2;b=(a+y)%2;c=b*z;d=(a+a)%2
        on=bool(x and not y and z)
        rec=dict(assignment=code,original=[x,y,z],a=a,b=b,c=c,d=d,source_sat=on)
        ck(rec==data["tables"][code],"forged table row")
        rows.append((rec,dict(x=x,y=y,z=z,a=a,b=b,c=c,d=d)))
    ck(data["source_models"]==1,"source SAT count")
    targets={"R1":("x",["b"],1,True),"R2":("x_and_z",["c"],1,True),
             "R3":("x",["a"],1,False),"R4":("x",["d"],0,False),
             "R5":("x",["a","x","y"],0,False)}
    ck(len(data["queries"])==5,"query length")
    for q in data["queries"]:
        kind,names,rhs,expected=targets[q["id"]]
        ck([q["factor"],q["terms"],q["rhs"],q["expected"]]==[kind,names,rhs,expected],"query fields")
        diff=[];src=[]
        for table,v in rows:
            f=v["x"] if kind=="x" else v["x"]*v["z"]
            row=int(sum(v[name] for name in names)%2==rhs)
            if f!=row:
                diff.append(table["assignment"])
                if table["source_sat"]:src.append(table["assignment"])
        ck(q["disagreement_original_assignments"]==diff,"global disagreement set")
        ck(q["disagreement_source_models"]==src,"source-only disagreement set")
        ck(q["definition_consistent_all_original_equal"]==(len(diff)==0)==expected,"exact semantic result")
    ids=data["semantic_identities"]
    ck(len(ids)==3,"identity count")
    for rec in ids:ck(rec["true_on_definition_consistent"]==8,"definition consistency")
    ck(ids[0]["row"]==["a","x","y"] and ids[0]["true_on_unconstrained_wire_triples"]==4,"3 wires")
    ck(ids[1]["row"]==["b","x"] and ids[1]["true_on_unconstrained_wire_pairs"]==2,"2 wires")
    ck(ids[2]["row"]==["d"] and ids[2]["true_on_unconstrained_wire_pair_values"]==1,"one wire")
    ck(data["logical_paid_nodes_in_candidate"]["DEF"]==4,"paid defs")
    return True
verify(raw)
corrupt=[]
def altered(fn):
    d=copy.deepcopy(raw);fn(d);corrupt.append(d)
altered(lambda d:d["paid_definitions"][3]["in"].__setitem__(1,"x"))
altered(lambda d:d["paid_definitions"][2].__setitem__("gate","XOR"))
altered(lambda d:d["tables"][3].__setitem__("b",1-d["tables"][3]["b"]))
altered(lambda d:d["queries"][2].__setitem__("definition_consistent_all_original_equal",True))
altered(lambda d:d["queries"][1]["disagreement_original_assignments"].append(0))
altered(lambda d:d["source_clauses"].append([-1]))
for i,d in enumerate(corrupt):
    caught=False
    try:verify(d)
    except (AssertionError,KeyError,ValueError,TypeError,IndexError):caught=True
    ck(caught,"accepted corruption %d"%i)
print(json.dumps({"status":"PASS","independent_assertions":checks,
                  "corruptions_rejected":len(corrupt),
                  "scope":"explicit 3-original-input definition quotient; not native row export"}))
