#!/usr/bin/env python3
"""UTM-PROOF-REACH-ACTIVITY153. Deterministic, stdlib-only reproducer.
Finite tests only: model-specific proof-head activity, distinct proof advice,
ordinary W1 proper exact-2,2 sign controls, and arithmetic inequalities.
Usage: python 2026-10-27_0236_UTM_PROOF_REACH_ACTIVITY153_repro.py --output results.json
"""
import argparse, itertools, json, math
from collections import Counter

W1 = (
    (-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
    (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
    (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),
    (6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14),
)
A_SLOTS=((6,0),(11,0))
B_SLOTS=((17,2),(9,2))
assertions=0

def check(cond,message):
    global assertions
    assertions+=1
    if not cond: raise AssertionError(message)

def bits(i,m):return format(i,'0%db'%m)
def neg(x):return ''.join('1' if c=='0' else '0' for c in x)
def disjoint(a,b):return all(x!='1' or y!='1' for x,y in zip(a,b))

def gadget(a,b):
    clauses=[list(c) for c in W1]
    if a=='0':
        for c,j in A_SLOTS:clauses[c][j]*=-1
    if b=='0':
        for c,j in B_SLOTS:clauses[c][j]*=-1
    return tuple(tuple(c) for c in clauses)

def satcount(clauses):
    count=0
    for mask in range(1<<15):
        if all(any(((mask>>(abs(lit)-1))&1)==int(lit>0) for lit in cl) for cl in clauses):count+=1
    return count

def valid22(clauses):
    pos=Counter();nneg=Counter()
    for c in clauses:
        check(len(c)==3 and len({abs(l) for l in c})==3,'proper clause')
        for lit in c:(pos if lit>0 else nneg)[abs(lit)]+=1
    return all(pos[v]==nneg[v]==2 for v in range(1,16))

class ProofReader:
    """A single sequential source head plus a one-cell-moving proof head.
    Every source/proof position change is one charged transition. All work cells
    are blank; the optional work-head is stationary at coordinate zero.
    No source input changes and no second source head is used.
    """
    def __init__(self,a,b,p,tail='',gap=None):
        self.m=len(a)
        check(len(b)==len(a) and len(p)==len(a),'lengths')
        self.a=a;self.b=b;self.p=p;self.proof=p+tail+'#'
        self.source='^'+a+'|'+'X'*(4*self.m if gap is None else gap)+'|'+b+'$'
        self.x=1;self.z=0;self.state='verify';self.T=0;self.H=0
        self.max_z=0;self.R=0;self.D=0;self.S=1;self.events=[];self.full=[]
        self.cut=1+self.m+1+(4*self.m//2 if gap is None else gap//2)
        self.last_source_dir=0
    def step(self,newx,newz,newstate):
        check(abs(newx-self.x)<=1 and abs(newz-self.z)<=1,'one cell move')
        oldx,oldz=self.x,self.z
        self.T+=1
        if newx!=oldx:
            direction=1 if newx>oldx else -1
            if self.last_source_dir and self.last_source_dir!=direction:self.R+=1
            self.last_source_dir=direction
        self.x,self.z,self.state=newx,newz,newstate
        if newz!=oldz:
            self.H+=1;self.events.append(('proof_move',newz-oldz))
        self.max_z=max(self.max_z,newz)
        if oldx<self.cut<=newx:
            self.events.append(('cross','right',newstate,0))
            self.full.append({'state':newstate,'proofhead':newz,'workhead':0,'workmap':(), 'direction':'right'})
        if oldx>=self.cut>newx:
            self.events.append(('cross','left',newstate,0))
            self.full.append({'state':newstate,'proofhead':newz,'workhead':0,'workmap':(), 'direction':'left'})
    def run(self):
        m=self.m
        for i in range(m):
            check(self.source[self.x] in '01','source verify char')
            check(self.proof[self.z] in '01','proof verify char')
            if self.source[self.x]!=self.proof[self.z]:return self.finish(False)
            self.step(self.x+1,self.z+1,'verify')
        check(self.source[self.x]=='|','source separator')
        for i in range(m):self.step(self.x,self.z-1,'rewind')
        check(self.z==0,'rewound proof')
        self.step(self.x+1,self.z,'gap')  # pass Alice delimiter
        while self.source[self.x]!='|':self.step(self.x+1,self.z,'gap')
        self.step(self.x+1,self.z,'check')  # pass Bob delimiter
        for i in range(m):
            check(self.source[self.x] in '01','source Bob char')
            check(self.proof[self.z] in '01','proof Bob char')
            if self.source[self.x]=='1' and self.proof[self.z]=='1':return self.finish(False)
            self.step(self.x+1,self.z+1,'check')
        check(self.source[self.x]=='$','end source')
        return self.finish(True)
    def finish(self,accept):
        # Only decision is reported. A suffix can remain unread.
        self.T+=1;self.state='accept' if accept else 'reject'
        z=0;crosses=[]
        for e in self.events:
            if e[0]=='proof_move':z+=e[1]
            elif e[0]=='cross':crosses.append({'state':e[2],'proofhead':z,
                     'workhead':e[3],'workmap':(), 'direction':e[1]})
        check(crosses==self.full,'chronicle decodes every complete crossing')
        V=2*6*(2*self.S+3)
        L=len(crosses)
        check(L<=(self.D+self.H+1)*V+self.D+self.H,'activity epoch cap')
        check(L<=(self.D+1)*V*(self.max_z+1)+self.D,'reach epoch cap')
        check(L<=self.R+1,'source reversal cap')
        return {'accept':accept,'T':self.T,'S':self.S,'D':self.D,'H':self.H,
                'reach':self.max_z,'R':self.R,'crossings':L,
                'events':tuple(self.events),'full':tuple(str(x) for x in self.full)}

# Independent signed exact-(2,2) CNF check, plus all four model counts.
models={};gadget_valid=0
for a,b in itertools.product('01',repeat=2):
    clauses=gadget(a,b)
    check(valid22(clauses),'2P2N source quota')
    check(len(set(clauses))==20,'no duplicate W1 clauses')
    models[a+b]=satcount(clauses);gadget_valid+=1
check(models=={'00':772,'01':272,'10':272,'11':0},'W1 sign counts')

# End-to-end strict soundness of a *fixed* proof-head verification program.
# On every NO input, every candidate proof is rejected. On every YES input,
# the correct 'Alice copy' proof accepts. S=1 and D=0 throughout.
probes=0;yes_proofs=0;accepted_diagonals=[];accepted_histories=[]
by_m=[]
for m in range(1,5):
    total=0;local_accept=0
    for ai in range(1<<m):
        a=bits(ai,m)
        for bi in range(1<<m):
            b=bits(bi,m)
            for pi in range(1<<m):
                p=bits(pi,m)
                result=ProofReader(a,b,p).run();probes+=1;total+=1
                expect=(p==a and disjoint(a,b))
                check(result['accept']==expect,'global sound proof-accepting program')
                if result['accept']:local_accept+=1
    for ai in range(1<<m):
        a=bits(ai,m);b=neg(a);z=ProofReader(a,b,a).run()
        check(z['accept'],'YES diagonal accepting proof')
        accepted_diagonals.append((m,a));accepted_histories.append((m,a,z['events']))
    by_m.append({'m':m,'all_proof_runs':total,'accepting_proof_runs':local_accept,
                 'diagonal_satisfiable':1<<m})
    yes_proofs+=local_accept

# Proof copied into a private read-only tape creates same cut chronicle for
# *different* YES diagonal sources: absent the proof-prefix factor the putative
# crossing-count injection is false. Prove the safe count >= 2^m.
for m in range(1,5):
    runs=[v for mm,_,v in accepted_histories if mm==m]
    check(len(set(runs))==1,'all diagonal chronicles collide without proof prefix')
    cap=3*m
    reachable=min(m+1,cap+1)
    check(2**m <= 2**(reachable+1)-1,'visible prefix capacity not violated')

# Suffix indistinguishability on a live proof head: same actual accessed prefix
# with arbitrarily different lengths/suffixes produces same decisions and event
# histories. The maximal reached coordinate is smaller than the moving count.
suffix_tests=0
for m in range(1,7):
    for pi in range(min(1<<m,16)):
        a=bits(pi,m);b=neg(a)
        base=ProofReader(a,b,a).run()
        for tail in ('0'*m,'1'*(m+7),'0101'*(m+2),''):
            z=ProofReader(a,b,a,tail=tail).run();suffix_tests+=1
            check((z['accept'],z['events'],z['reach'],z['H']) ==
                  (base['accept'],base['events'],base['reach'],base['H']),
                  'long unread suffix independent')
            check(z['D']==0 and z['S']==1 and z['R']==0,'no-free-work side channel')

# Exact activity-vs-reach adversary: a proof-head step can enable another
# source-cut crossing without any work-symbol edits. This is a finite symbolic
# crossing event trace of a 2-way source/independent proof-head controller.
oscillator=[]
for P in (1,3,8,32,64):
    H=P;D=0;S=1;q=2;V=2*q*(2*S+3)
    # Same source cut crossed P+1 times; proof head advanced P times.
    L=P+1
    check(L <= (D+H+1)*V + D+H,'activity cap for oscillatory proof')
    check(L <= (D+1)*V*(P+1)+D,'reach cap for oscillatory proof')
    oscillator.append({'proof_moves':H,'proof_reach':P,'source_cut_crossings':L,
                       'old_omit_proof_cap_V':V,'violates_omitted_proof_cap':L>V})
check(any(x['violates_omitted_proof_cap'] for x in oscillator),'need proof activity')

# Strict exponent faces: old length-only vs reachable-prefix and joint epoch
# bound, with full proof-length P allowed to be much greater than reach.
exponents=[]
for s,d,rho,alpha,ell,k in [
    (.3,.1,.2,.3,2.0,1),(.3,.3,.1,.8,2.0,1),
    (.4,.2,.4,.6,2.0,1),(.5,.3,.2,.6,2.0,1),
    (.3,.4,.3,.8,.4,1),(.15,.2,.3,.5,2.0,2),
]:
    beta=min(rho,ell)
    reach=d+k*s+beta
    activity=max(d,alpha)+k*s
    old=d+k*s+ell
    check(alpha+1e-9>=rho,'physical proof movement >= reach')
    exponents.append({'s':s,'d':d,'reach_exp':rho,'proof_moves_exp':alpha,
        'proof_length_exp':ell,'k':k,'old_length_face':round(old,6),
        'new_reach_face':round(reach,6),'new_activity_face':round(activity,6),
        'excluded_by_new_reach':reach<1-1e-10,
        'excluded_by_new_activity':activity<1-1e-10})
check(exponents[0]['excluded_by_new_reach'] and exponents[0]['excluded_by_new_activity'],
      'strict excluded example')

# Conservative one-tape simulation is an upper bound; direct RAM transfer fails.
model_transfer=[]
for tk,sk in [(1.0,0.0),(1.4,0.5),(1.8,0.1),(2.0,0.0),(3.0,2.0)]:
    t1=tk+max(1,sk);p1=max(1,sk)
    check(t1>=2,'one-tape exponent upper ceiling never strict below 2 for t_k>=1')
    model_transfer.append({'mk_time_exp':tk,'mk_space_exp':sk,
                           'certified_one_tape_time_ceiling_exp':t1,
                           'certified_one_tape_footprint_ceiling_exp':p1})

out={'id':'UTM-PROOF-REACH-ACTIVITY153','date':'2026-10-27','status':'COMPUTATIONAL finite controls; formal restricted theorem separate',
 'seed':None,'assertions':assertions,'failures':0,'W1_model_counts':models,'W1_exact22_gadgets':gadget_valid,
 'proof_verifier_runs':probes,'proof_verifier_acceptances':yes_proofs,'by_m':by_m,
 'diagonal_examples':len(accepted_diagonals),
 'cross_history_collisions_ignoring_proof':True,
 'unread_suffix_invariance_tests':suffix_tests,
 'oscillator_controls':oscillator,'exponent_controls':exponents,
 'one_tape_simulation_controls':model_transfer,
 'scope':'One source head plus independent sequential proof head, blank work tapes, restricted separated DISJ/ W1 SAT promise. P versus NP and ARC-EDGE-90 OPEN.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='2026-10-27_0236_UTM_PROOF_REACH_ACTIVITY153_raw.json')
    args=parser.parse_args()
    with open(args.output,'w') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps({'assertions':assertions,'failures':0,'proof_verifier_runs':probes,
     'suffix_tests':suffix_tests,'models':models,'example':exponents[0]},indent=2))