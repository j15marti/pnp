# LSPV-4/549 independent exact finite reachability checker.
# Fully self-contained dependency incidence transcribed from pinned /579 60-RES packet
# 807aaf7b7cf5e4a4feb29c2599f9e582ea140e30.
# Run: python3 experiments/arc/lspv4_549_independent_slot_lower.py
from collections import deque
import json
DEP=[[],[],[],[],[],[],[],[],[6],[3],[7],[5],[2],[1],[0],[4],[12,8],[9,14],[10,15],[13,11],[17],[19],[16],[18],[21,23],[20,22],[25],[24],[27,26],[],[],[],[],[],[],[],[],[29],[33],[31],[32],[30],[36],[35],[34],[43,39],[40,37],[42,38],[44,41],[47],[46],[48],[45],[50,52],[49,51],[54],[53],[56,55],[57,28],[58]]
WIDTH=[19,17,19,17,19,17,19,17,20,17,17,18,19,17,18,18,16,14,14,14,13,13,14,14,10,10,12,11,9,16,14,16,14,16,14,16,14,15,15,17,14,15,14,16,14,14,12,12,12,12,12,13,13,10,10,11,10,8,5,2]
ORDER=[0,1,2,3,5,9,12,13,14,17,11,4,15,19,7,10,18,6,20,21,23,24,8,16,22,25,26,27,28,29,30,31,32,37,40,46,39,35,43,45,33,38,50,52,53,36,42,47,41,34,44,48,49,51,54,55,56,57,58,59]
n=len(DEP)
assert n==len(WIDTH)==len(ORDER)==60 and set(ORDER)==set(range(60))
ALL=(1<<n)-1
P=[sum(1<<j for j in d) for d in DEP]
S=[0]*n
for i,deps in enumerate(DEP):
    for j in deps:
        assert 0<=j<i
        S[j]|=1<<i
def count_live(mask):
    un=ALL^mask
    return sum(bool(mask>>j&1 and S[j]&un) for j in range(n))
def reuse(mask,i,mode):
    un=ALL^mask
    return any((S[j]&un)==(1<<i) and (mode!='byte' or WIDTH[j]>=WIDTH[i]) for j in DEP[i])
def run_order(order):
    mask=0
    peaks={'fresh':0,'byte':0,'inplace':0}
    eligible=0
    for i in order:
        assert not mask>>i&1 and not P[i]&~mask
        live=count_live(mask)
        for mode in peaks:
            charge=1 if mode=='fresh' or not reuse(mask,i,mode) else 0
            peaks[mode]=max(peaks[mode],live+charge)
        eligible+=reuse(mask,i,'byte')
        mask|=1<<i
    assert mask==ALL
    return {'peaks':peaks,'byteSafeEligible':eligible}
def enumerate_cap(cap,mode):
    q=deque([0]);seen={0};edges=0;far=0
    while q:
        mask=q.popleft()
        far=max(far,mask.bit_count())
        if mask==ALL:
            return dict(cap=cap,mode=mode,complete=True,states=len(seen),transitions=edges,furthest=far)
        live=count_live(mask)
        un=ALL^mask
        for i in range(n):
            if mask>>i&1 or P[i]&un:
                continue
            c=live+(1 if mode=='fresh' or not reuse(mask,i,mode) else 0)
            if c>cap:
                continue
            edges+=1
            nm=mask|(1<<i)
            if nm not in seen:
                seen.add(nm)
                q.append(nm)
    return dict(cap=cap,mode=mode,complete=False,states=len(seen),transitions=edges,furthest=far)
if __name__=='__main__':
    f5=enumerate_cap(5,'fresh')
    i4=enumerate_cap(4,'inplace')
    s=run_order(ORDER)
    assert (f5['complete'],f5['states'],f5['transitions'],f5['furthest'])==(False,993927,2185554,52)
    assert (i4['complete'],i4['states'],i4['transitions'],i4['furthest'])==(False,181387,590930,51)
    assert s=={'peaks':{'fresh':6,'byte':5,'inplace':5},'byteSafeEligible':36}
    print(json.dumps({'freshCap5':f5,'inplaceCap4':i4,'schedule':s},indent=2))
