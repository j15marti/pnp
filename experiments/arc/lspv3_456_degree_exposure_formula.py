#!/usr/bin/env python3
"""Pang PC-degree vs LSPV2/369 definition-exposure budget.
CONDITIONAL ON: Pang Thm 1.1 PC no-degree-D refutation,
AND LSPV2/369's locally opaque / wire-defined compiler.
Does NOT verify PC degree, historical grammar, or all-machine hardness.
"""
import argparse
import math
import json

def pang_log_lower(n,d,width):
    if not all(isinstance(x,int) for x in (n,d,width)) or n<=0 or width<=0:
        raise ValueError("invalid parameters")
    if d<max(32,8*width):
        raise ValueError("Pang p=2,r=1 requires D>=max(32,8w)")
    return d*d/(2048.0*n)

def mixed_log_upper(m,q,b):
    if any(not isinstance(x,int) or x<0 for x in (m,q,b)):
        raise ValueError("invalid m/q/b")
    return b*math.log(2.0)+math.log(2*m+64*q+2)

def selftest():
    assert abs(pang_log_lower(1048576,262144,3)-32.0)<1e-10
    assert mixed_log_upper(80,19,0)<mixed_log_upper(80,19,3)
    for t in ((0,33,3),(100,20,3)):
        try:pang_log_lower(*t)
        except ValueError:pass
        else:raise AssertionError("bad parameter accepted")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for name,default in (("n",1048576),("D",262144),("width",3),
                         ("m",8388608),("q",1000000),("b",0)):
        parser.add_argument("--"+name,type=int,default=default)
    a=parser.parse_args();selftest()
    print(json.dumps({
      "n":a.n,"D":a.D,"width":a.width,"m":a.m,
      "q":a.q,"b":a.b,
      "pang_syntactic_log_size_floor":pang_log_lower(a.n,a.D,a.width),
      "scoped_semantic_translator_log_size_ceiling":mixed_log_upper(a.m,a.q,a.b),
      "warning":"Different proof systems: syntactic Pang and semantic LSPV2/369. "
                "Raw inequality is only diagnostic without an explicit semantic-to-syntactic overhead. "
                "No PC degree is verified by this program."},indent=2))
