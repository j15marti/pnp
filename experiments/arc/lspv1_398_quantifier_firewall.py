#!/usr/bin/env python3
"""LSPV-1/398: finite logic/source metadata control, not Haken/Cook proof."""
import json
def imp(p,q):
    return not p or q
def source(h):
    if type(h) is not int or h<1:
        raise ValueError("malformed source parameter")
    v=h*(h+1);m=h+1+h*h*(h+1)//2;L=h*(h+1)**2
    return {"h":h,"variables":v,"clauses":m,"literals":L,
            "id_width":v.bit_length(),
            "signed_field_bits":L*(v.bit_length()+1)}
def main():
    checks=0;rows=[]
    for P in [False,True]:
        for Q in [False,True]:
            B=imp(P,Q)
            assert B == (not P or Q);checks+=1
            if not Q:
                assert B == (not P);checks+=1
            rows.append({"SAT_in_P":P,"Resolution_p_bounded":Q,"B3_Resolution":B})
    assert imp(False,False) and not imp(True,False);checks+=2
    bad=[-10,-1,0,"3",None];rejected=0
    for z in bad:
        try: source(z)
        except ValueError: rejected+=1
    assert rejected==5;checks+=rejected
    src=[source(z) for z in [1,2,3,4,8,16,32,64]]
    for r in src:
        h=r["h"]
        assert r["clauses"]==h+1+h*h*(h+1)//2;checks+=1
        assert r["literals"]==h*(h+1)**2;checks+=1
        assert r["signed_field_bits"]>=r["literals"];checks+=1
    for a,b in [(10,100),(100,10000),(1,12345)]:
        assert a<b;checks+=1
    assert checks==40
    return {"research_id":"LSPV-1/398","assertion_groups":checks,
      "truth_table":rows,"php_source_metadata":src,
      "malformed_rejected":rejected,
      "status":"COMPUTATIONAL metadata and logic control only",
      "Haken_Cook_reproved":False,"B1_Rmix341":"OPEN",
      "B2_Rmix341":"OPEN","B3_Rmix341":"OPEN","P_versus_NP":"OPEN"}
if __name__=="__main__":
    print(json.dumps(main(),indent=2,sort_keys=True))
