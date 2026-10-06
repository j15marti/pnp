#!/usr/bin/env python3
import math, json

gamma = 2*math.cos(math.pi/7)

def explicit(theta, eta, r=1.0, sigma=0.0):
    C=max(r, eta/(1-theta))
    rho=max(sigma, theta)
    return {"C":C,"rho":rho,"sum":C+rho,"hits":C+rho<gamma}

def macro_route_bits(N,theta,eta,base=16):
    x=float(N); bits=0.0; levels=0
    while x>base and levels<100:
        bits += eta*math.log2(x)
        x = x**theta
        levels += 1
    return levels,bits

def oblivious_cover(n,theta):
    live=math.ceil(n**theta)
    return {"n":n,"theta":theta,"live":live,"log2_min_children":n-live}

out={
  "gamma":gamma,
  "landing_examples":[],
  "macro_lineage":[],
  "oblivious_cover":[]
}

for theta,eta in [(0.5,0.5),(2/3,1/3),(0.75,0.2),(0.8,0.15),(0.82,0.0)]:
    row={"theta":theta,"eta":eta}
    row.update(explicit(theta,eta))
    out["landing_examples"].append(row)

for theta,eta in [(0.5,0.5),(2/3,1/3),(0.75,0.2),(0.8,0.15)]:
    levels,bits=macro_route_bits(2**80,theta,eta)
    out["macro_lineage"].append({
        "theta":theta,"eta":eta,"N":"2^80","levels":levels,
        "route_bits_upper_proxy":bits,
        "leaf_exponent":eta/(1-theta)
    })

for n in [128,512,1024]:
    for theta in [0.5,2/3,0.8]:
        out["oblivious_cover"].append(oblivious_cover(n,theta))

print(json.dumps(out,indent=2))
