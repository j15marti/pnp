#!/usr/bin/env python3
"""Finite audit for REFEREE342 paid source-bit materialization and mux repair."""
import hashlib, json
from itertools import product
from pathlib import Path

def canon(clause):
    vals=set(int(x) for x in clause)
    if 0 in vals or any(-x in vals for x in vals): raise ValueError("invalid clause")
    return tuple(sorted(vals,key=lambda x:(abs(x),x<0)))

def resolve(c1,c2,pivot):
    a,b=set(c1),set(c2)
    if pivot in a and -pivot in b: x,y=pivot,-pivot
    elif -pivot in a and pivot in b: x,y=-pivot,pivot
    else: raise ValueError("missing complementary pivot")
    return canon((a-{x})|(b-{y}))

def slots(op,out,a,b):
    if op=="AND": return [canon((-out,a)),canon((-out,b)),canon((out,-a,-b))]
    if op=="OR": return [canon((-a,out)),canon((-b,out)),canon((a,b,-out))]
    raise ValueError("bad gate")

class Proof:
    def __init__(self,next_var=3): self.next_var=next_var; self.env={}; self.defs=[]; self.res=[]
    def gate(self,op,a,b):
        out,self.next_var=self.next_var,self.next_var+1; did=f"D{len(self.defs)}"; ss=[]
        for i,clause in enumerate(slots(op,out,a,b)):
            rid=f"{did}:s{i}"; self.env[rid]=clause; ss.append({"id":rid,"clause":list(clause)})
        self.defs.append({"id":did,"op":op,"out":out,"inputs":[a,b],"slots":ss})
        return out,[s["id"] for s in ss]
    def step(self,left,right,pivot):
        rid=f"R{len(self.res)}"; clause=resolve(self.env[left],self.env[right],abs(pivot))
        self.env[rid]=clause; self.res.append({"id":rid,"left":left,"right":right,"pivot":abs(pivot),"clause":list(clause)})
        return rid
    def record(self): return {"defs":self.defs,"res":self.res,"paid":len(self.defs)+len(self.res)}

def constant_bank(bits):
    if any(type(x) is not int or x not in (0,1) for x in bits): raise ValueError("bits must be integers 0/1")
    p=Proof(); u,us=p.gate("AND",1,2); v,vs=p.gate("AND",-1,-2); z,zs=p.gate("AND",u,v)
    r0=p.step(us[0],vs[0],1); r1=p.step(r0,zs[0],u); rz=p.step(r1,zs[1],v); assert p.env[rz]==(-z,)
    false_refs=[]
    for lit in (1,-1,2,-2):
        f,fs=p.gate("AND",z,lit); rf=p.step(rz,fs[0],z); assert p.env[rf]==(-f,); false_refs.append((f,rf))
    true_refs=[]
    for j in (0,2):
        f1,rf1=false_refs[j]; f2,rf2=false_refs[j+1]; t,ts=p.gate("AND",-f1,-f2)
        r=p.step(ts[2],rf1,f1); r=p.step(r,rf2,f2); assert p.env[r]==(t,); true_refs.append((t,r))
    (t1,rt1),(t2,rt2)=true_refs; units=[]
    for bit in bits:
        if bit==0:
            q,qs=p.gate("AND",z,t1); rq=p.step(rz,qs[0],z); assert p.env[rq]==(-q,)
        else:
            q,qs=p.gate("AND",t1,t2); rq=p.step(qs[2],rt1,t1); rq=p.step(rq,rt2,t2); assert p.env[rq]==(q,)
        units.append({"bit":bit,"var":q,"ref":rq,"unit":list(p.env[rq])})
    rec=p.record(); rec.update({"bits":bits,"units":units,"base_paid":20,"expected_paid":20+2*bits.count(0)+3*bits.count(1)})
    assert rec["paid"]==rec["expected_paid"]; return rec

def mux_repair(select_left,xlit,ylit):
    p=Proof(); p.env["C0"]=(-99,); c=99
    if select_left:
        a,ass=p.gate("AND",-c,xlit); b,bss=p.gate("AND",c,ylit); selected,active,dead=xlit,ass,bss[0]
    else:
        a,ass=p.gate("AND",c,xlit); b,bss=p.gate("AND",-c,ylit); selected,active,dead=ylit,bss,ass[0]
    q,qss=p.gate("OR",a,b); ractive=p.step("C0",active[2],c); rdead=p.step("C0",dead,c)
    if select_left:
        rp=p.step(qss[0],ractive,a); mid=p.step(qss[2],rdead,b); rn=p.step(mid,ass[1],a)
    else:
        rp=p.step(qss[1],ractive,b); mid=p.step(qss[2],rdead,a); rn=p.step(mid,bss[1],b)
    assert p.env[rp]==canon((-selected,q)) and p.env[rn]==canon((selected,-q))
    rec=p.record(); rec.update({"select_left":select_left,"x":xlit,"y":ylit,"q":q,"selected":selected,"alias_refs":[rp,rn],"expected_paid_excluding_false_unit":8})
    assert rec["paid"]==8; return rec

def sat(clauses,n):
    return any(all(any(a[abs(l)-1]==(l>0) for l in c) for c in clauses) for a in product((False,True),repeat=n))

def main():
    banks=[constant_bank(list(bits)) for w in range(9) for bits in product((0,1),repeat=w)]; assert len(banks)==511
    muxes=[mux_repair(side,sx,sy) for side in (False,True) for sx in (1,-1) for sy in (2,-2)]; assert len(muxes)==8
    unsat=[[1,2],[1,-2],[-1,2],[-1,-2]]; sat_sibling=[[1,2],[-1,2]]
    assert not sat(unsat,2) and sat(sat_sibling,2)
    rejected=0
    for bad in ([2],["0"],[None],[True],[0,-1]):
        try: constant_bank(bad)
        except (TypeError,ValueError): rejected+=1
    assert rejected==5
    compact=[{"bits":r["bits"],"paid":r["paid"]} for r in banks]
    payload={"claim":"SOURCE-BIT-MATERIALIZATION-REFEREE342","status":"PROVED_RESTRICTED_FINITE_CHECK","constant_bank_records":len(banks),"constant_bank_formula":"20 + 2*b0 + 3*b1","mux_records":muxes,"mux_paid_excluding_authenticated_false_unit":8,"unsat_control":{"clauses":unsat,"label":"UNSAT"},"sat_control":{"clauses":sat_sibling,"label":"SAT"},"malformed_rejected":rejected,"compact_digest":hashlib.sha256(json.dumps(compact,sort_keys=True).encode()).hexdigest()}
    out=Path("results/raw/arc/lspv5_342/source_bit_materialization_referee342.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"constant_banks":len(banks),"muxes":len(muxes),"malformed_rejected":rejected,"raw_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"status":"PASS"},sort_keys=True))
if __name__=="__main__": main()
