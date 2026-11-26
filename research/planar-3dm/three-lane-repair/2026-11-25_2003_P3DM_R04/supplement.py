from p3r04_audit import *
U=parse('000 002 010 011 021 022 100 101 111 201 202 221')
print('AGE_U',planar(3,U),oracle(3,U),solve(3,U))
for k in (3,4,8):
    T=[(b*k+i,b*k+(i+d)%k,2*i+d) for b in (0,1) for i in range(k) for d in (0,1)]
    print('concentric',k,planar(2*k,T),len(close(2*k,T) or []),solve(2*k,T)[:4])
