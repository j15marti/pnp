import json
rows=[]
for r in range(1,17):
    z=[0]*r
    for i in range(r):
        y=z.copy();y[i]=1
        assert all(z[j]==y[j] for j in range(r) if j!=i)
    rows.append({"type":"clause_slot","r":r,"forced_probes":r,"scan_probes":r})
for k in range(1,17):
    rows.append({"type":"indexed_read","k":k,"response_rows":2**k,"query_probes":1})
out={"status":"COMPUTATIONAL","cases":len(rows),"rows":rows}
print(json.dumps(out,indent=2))
