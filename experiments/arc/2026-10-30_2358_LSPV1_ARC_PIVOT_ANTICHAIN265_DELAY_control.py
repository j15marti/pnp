#!/usr/bin/env python3
"""Exact rational DELAY/COPY tariff sanity test: known restricted LSPV-5 theorem."""
from fractions import Fraction as Q
import json
alpha,gamma,lam=Q(11,10),Q(3,5),Q(1,2)
rows=[]
for K in (4,8,16,32):
    advertised=max(alpha,gamma+lam*K)
    parent=Q(K)
    childtax=gamma+lam*K+Q(1,20)
    assert parent>advertised and childtax>advertised
    rows.append({'K':K,'advertised':str(advertised),'mandatory_parent':str(parent),'saturated_child_with_N^1/20_tax':str(childtax)})
print(json.dumps({'scope':'KNOWN LSPV-5 black-box mandatory completed-call tariff; universal compiler OPEN','rows':rows},indent=2))
