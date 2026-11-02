#!/usr/bin/env python3
"""Independent instrumented original-clause UP/DPLL baseline for LSPV-1 318."""
import json
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))

def solve(pins):
    cost={'nodes':0,'literal_inspections':0,'clause_visits':0,'unit_assignments':0,
          'conflicts':0,'branch_edges':0,'complete_original_witness_checks':0}
    def node(pin):
        cost['nodes']+=1
        while True:
            changed=False
            done=True
            for c in F:
                cost['clause_visits']+=1
                free=[];sat=False
                for v in c:
                    cost['literal_inspections']+=1
                    z=pin.get(abs(v))
                    if z is None:free.append(v)
                    elif z==int(v>0):sat=True;break
                if sat:continue
                done=False
                if not free:
                    cost['conflicts']+=1
                    return None
                if len(free)==1:
                    v=free[0];i=abs(v);b=int(v>0)
                    if i in pin and pin[i]!=b:
                        cost['conflicts']+=1;return None
                    if i not in pin:
                        pin[i]=b
                        cost['unit_assignments']+=1
                        changed=True
                        break
            if changed:continue
            if done:
                witness={x:pin.get(x,0) for x in range(1,10)}
                cost['complete_original_witness_checks']+=1
                assert all(any(witness[abs(v)]==int(v>0) for v in c) for c in F)
                return ''.join(str(witness[i]) for i in range(1,10))
            break
        unassigned={abs(v) for c in F if not any(abs(w) in pin and pin[abs(w)]==int(w>0) for w in c)
                    for v in c if abs(v) not in pin}
        if not unassigned:
            cost['conflicts']+=1;return None
        v=min(unassigned)
        for b in (0,1):
            cost['branch_edges']+=1
            result=node({**pin,v:b})
            if result is not None:return result
        return None
    witness=node(dict(pins))
    return ('SAT' if witness is not None else 'UNSAT'),witness,cost

def main():
    base={2:0,3:0,6:1}
    result={}
    for name,p in [('parent',base),('SAT',{**base,7:1}),('UNSAT',{**base,7:0})]:
        label,witness,cost=solve(p)
        assert label==('UNSAT' if name=='UNSAT' else 'SAT')
        result[name]={'label':label,'witness':witness,'cost':cost}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
