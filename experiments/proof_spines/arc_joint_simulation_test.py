#!/usr/bin/env python3
"""Exact charged two-stage model. No SAT closure theorem is asserted."""
from fractions import Fraction as F
from pathlib import Path
import json
import time
import math


def main():
    start=time.monotonic()
    checks=0
    def checked(condition):
        nonlocal checks
        assert condition
        checks+=1
        assert time.monotonic()-start < 25
    def joint(time_witness,space_witness,model_time,model_space):
        return time_witness==space_witness and model_time==model_space
    checked(not joint('original','simulator','RAM','MT'))
    checked(not joint('original','simulator','RAM','RAM'))
    checked(not joint('same','same','RAM','MT'))
    checked(joint('same','same','RAM','RAM'))
    # A proposed simulator yields joint (q*t, alpha*t), then a contractor
    # yields joint (a+b*q*t+c*alpha*t, d+alpha*t).
    # theta=b*q+c*alpha; fixed time a/(1-theta); sum=(1+alpha)*time+d.
    rows=[]
    gamma=2*math.cos(math.pi/7)
    for q in (F(1),F(3,2),F(2)):
        for alpha in (F(1,4),F(1,2)):
            for a in (F(1,4),F(1,2),F(1)):
                for b in (F(1,4),F(1,2),F(3,4)):
                    for c in (F(0),F(1,4)):
                        d=F(0)
                        theta=b*q+c*alpha
                        stable=theta<1
                        row={'q':str(q),'alpha':str(alpha),'a':str(a),'b':str(b),'c':str(c),'theta':str(theta),'stable':stable}
                        if stable:
                            tf=a/(1-theta)
                            sf=d+alpha*tf
                            row.update(fixed_time=str(tf),fixed_space=str(sf),endpoint_sum=str(tf+sf),margin=float(gamma-float(tf+sf)))
                            t=F(10)
                            for r in range(1,11):
                                previous=t
                                t=a+theta*t
                                s=d+alpha*previous
                                expected=tf+theta**r*(F(10)-tf)
                                checked(t==expected)
                                checked(s==d+alpha*(tf+theta**(r-1)*(F(10)-tf)))
                        rows.append(row)
                        checked(stable==(b*q+c*alpha<1))
    # Even fictional perfect-time square-root simulation alone has eigenvalue 1.
    t=F(10)
    for _ in range(50):
        t,s=t,t/2
        checked(t+s==15)
    out={'status':'EXACT ARITHMETIC MODEL; SIMULATOR AND CONTRACTOR ASSUMPTIONS OPEN','checks':checks,'elapsed_seconds':time.monotonic()-start,'parameter_cases':len(rows),'typed_guards':4,'simulation_only_time_eigenvalue':1,'rows':rows,'limits':'No general SAT algorithms are constructed. Bounds in each phase require one model-matched realization. Decimal endpoint margins are illustrations; exact rational fixed points are recorded.'}
    path=Path(__file__).with_name('arc_joint_simulation_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('checks','elapsed_seconds','parameter_cases')}))

if __name__=='__main__':
    main()
