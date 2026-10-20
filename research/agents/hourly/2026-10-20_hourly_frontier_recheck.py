from fractions import Fraction as F
a,b,tau=F(1,2),F(3,5),F(241,200)
# incomplete cache, mu=alpha*t: t=b+rho+g+a*t -> t=(b+rho+g)/(1-a)
def fp_inc(rg): return (b+rg)/(1-a)
assert fp_inc(F(1,400))==tau and fp_inc(F(1,400)-F(1,10**6))<tau
# complete cache: need b+a+g<tau and fixed point of b+a*t below tau
assert tau-b-a==F(21,200) and b/(1-a)==F(6,5)<tau
# monotone in rho+g: any positive block exponent consumes the same slack
for k in range(0,401):
    rg=F(k,10**5); assert (fp_inc(rg)<tau)==(rg<F(1,400))
print("hourly recheck OK: thresholds 1/400 (virtual/incomplete), 21/200 (materialized)")
