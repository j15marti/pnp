from fractions import Fraction as F
d=lambda c:F(1,2)*((c+2)/c**2-c)
tau=F(241,200)
print("d(tau)=",d(tau),float(d(tau)), d(tau)==F(11642479,23232400), d(tau)>F(1,2))
# threshold on c where d(c)=1/2 : bisect
lo,hi=F(1),F(2)
for _ in range(60):
    m=(lo+hi)/2
    (lo,hi)=(m,hi) if d(m)>F(1,2) else (lo,m)
print("d(c)=1/2 at c~",float(lo))
print("monotone decreasing on [1,1.3]:",all(d(F(100+i,100))>d(F(101+i,100)) for i in range(30)))
u,v,b=F(3,5),F(1,2),F(11,10)
for g in [F(0),F(1,500),F(1,401),F(1,400),F(1,399)]:
    t=F(5)
    for _ in range(80): t=max(b,u+g+v*t)
    print("g=",g,"t_fixed(80 it)=",float(t),"closed",float(max(b,6*F(1,5)+2*g)),"strict<tau:",max(b,F(6,5)+2*g)<tau)
