#!/usr/bin/env python3
"""Strict auxiliary JSON-source grammar controls for LSPV-4 338.
This tests declared JSON serialization, NOT the project's separate fixed-width
indexed input encoding; its native-machine parsing charges remain outstanding.
"""
import json
from verify338_compact import source, canonical, F9P, F9N

def parse_source(text):
    if not isinstance(text,str):
        raise ValueError("source must be text")
    obj=json.loads(text)
    if type(obj) is not dict or list(obj)!=["n","clauses"]:
        raise ValueError("header or key order")
    if text!=json.dumps(obj,separators=(",",":"),ensure_ascii=False):
        raise ValueError("noncanonical serialization")
    n=obj["n"];F=obj["clauses"]
    if not canonical(F,n):
        raise ValueError("invalid proper duplicate-free monotone 3-SAT-(2,2) original")
    return n,F

def main():
    F=source(F9P,F9N)
    valid=json.dumps({"n":9,"clauses":F},separators=(",",":"))
    assert parse_source(valid)[0]==9
    invalid=[
        "", "{", valid+"garbage", valid.replace('"n":','"n" :',1),
        valid.replace('"n":','"n":0,"n":',1),
        valid.replace('"n":9','"n":"9"',1),
        valid.replace('"clauses":','"other":[],"clauses":',1),
        valid.replace('"clauses":','"clauses":[],"clauses":',1)
    ]
    for s in invalid:
        try: parse_source(s)
        except (ValueError,TypeError,KeyError):continue
        raise AssertionError("malformed string accepted")
    print({"valid_source_accepted":1,"malformed_strings_rejected":len(invalid),
           "encoding":"strict canonical compact JSON, auxiliary only"})

if __name__=="__main__":main()
