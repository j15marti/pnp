from fractions import Fraction as F
alpha=F(1,2)
beta=F(3,5)
tau=F(241,200)
d=((tau+2)/(tau*tau)-tau)/2
assert d==F(11642479,23232400)>F(1,2)
assert tau-beta-alpha==F(21,200)
assert (tau-F(6,5))/2==F(1,400)
def mat(t,s,g):
    return max(F(1), beta+alpha+g, beta+alpha*t),max(F(1,2),alpha*s)
def vir(t,s,g):
    return max(F(1), beta+g+alpha*t),max(F(1,2),alpha*s)
t=s=F(16)
for j in range(12):
    t,s=mat(t,s,F(1,10))
assert t==F(2465,2048) and s==F(1,2) and t<tau
t=s=F(16)
for j in range(100):
    t,s=vir(t,s,F(1,10))
assert t>=tau
print('ARC restricted exponent arithmetic passed; SAT semantic compiler still OPEN')
