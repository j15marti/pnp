d=lambda c:((c+2)/c**2-c)/2
def bis(f,lo,hi):
    for _ in range(200):
        m=(lo+hi)/2
        if f(lo)*f(m)<=0: hi=m
        else: lo=m
    return (lo+hi)/2
cb=lambda b:bis(lambda c:d(c)-b,1.0001,1.6)
c5=cb(.5);print("c_1/2",c5,c5**3+c5**2-c5-2)
print("d(1.205)",d(241/200))
sig=.1
bc=bis(lambda b:(cb(b)-1)*(1-b)-sig,.4,.6);print("beta_cap",bc)
for b in [.5,.506]:
    c=cb(b);print(b,c,"sigma<",(c-1)*(1-b),"eta<",c-(1-b+sig))
