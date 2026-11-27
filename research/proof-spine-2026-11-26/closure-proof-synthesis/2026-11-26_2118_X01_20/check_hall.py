"""Portable Hall certificate checker; inputs: original tuple list, allowed IDs, q, certificate.
The executed full experiments and raw certificates are in the chat archive.
"""
def verify(T, ids, q, cert):
    a,b=cert["a"],cert["b"]
    H,Y=set(cert["H"]),set(cert["Y"])
    B,U=cert["used_mask"],cert["unused_mask"]
    assert a!=b and 0<=a<3 and 0<=b<3
    assert all(0<=v<q for v in H|Y)
    assert len(H)>len(Y)
    assert U==sum(1<<(a*q+v) for v in H)
    assert B>=0 and B.bit_length()<=3*q and not B&U
    for i in ids:
        t=T[i]
        if t[a] in H and t[b] not in Y:
            assert B&sum(1<<(j*q+v) for j,v in enumerate(t))
    return True

def rejects(cert, occupied):
    return occupied&cert["used_mask"]==cert["used_mask"] and not occupied&cert["unused_mask"]

