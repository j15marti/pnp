#!/usr/bin/env python3
"""No-producer-import verifier for REFEREE270 machine-readable output."""
import itertools,json,sys
o=json.load(open(sys.argv[1]));checks=0
def ck(x,m):
 global checks;checks+=1
 if not x:raise AssertionError(m)
ck(o['run']=='DECISION_SUPPORT_TRANSFER_REFEREE270','run')
ck(o['P_vs_NP']=='OPEN','status')
ck(o['local_syntactic_states']==84,'84 states')
ck(1<=o['distinct_boolean_relations']<=16,'relations')
ck(o['distinct_integer_matrices']>=o['distinct_boolean_relations'],'matrix collapse')
ck(sum(o['relation_multiplicities'].values())==84,'multiplicities')
ck(len(o['six_explicit_pair_cover_witnesses'])==6,'pair cover witnesses')
for row in o['family_distribution']:
 ck(int(row['syntactic_states'])==84**row['t'],'family total')
 ck(int(row['SAT_states'])+int(row['UNSAT_states'])==int(row['syntactic_states']),'partition')
 ck(row['reachable_product_relations']<=16,'bounded state')
for row in o['AB_promise']:
 ck(row['minimum_SAT_input_pin_queries']==row['matching_scan_queries']==row['t'],'tight queries')
 ck(row['SAT_certificate_bits']==row['t'] and row['UNSAT_certificate_bits']==1,'certificate asymmetry')
ck(o['WA']==[[1,1],[0,0]] and o['WB']==[[0,0],[0,0]],'A/B matrices')
ck(o['controls']=={'F15_SAT_models':2,'F15_UNSAT_models':0,'F9_A_models':1,'F9_B_models':0,
                    'F9_SU_pair_modes':264,'F9_root_models':70,'Y6_models':20,'malformed_rejected':6},'controls')
ck(o['equivalence_firewall']['CUBEKEY_current_decision_classes']==1,'CUBEKEY decision class')
ck(o['equivalence_firewall']['AB_current_decision_classes']==2,'A/B decision classes')
ck(o['equivalence_firewall']['local_continuation_relation_universe']==16,'continuation universe')
ck(o['wrappers']['DELAY_logical_delta']==0,'delay')
ck('no all-input polynomial controller' in o['limitations'],'scope')
# Independently recheck the load-bearing six-row pair-cover certificate.
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
E=(2,3,4,6,7,8,9)
def sat(a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
C=[]
for row in o['six_explicit_pair_cover_witnesses']:
 ck(len(row)==9 and set(row)<={'0','1'},'witness syntax')
 a={i+1:int(b) for i,b in enumerate(row)};ck(a[5]==0 and sat(a),'witness source check');C.append(a)
for u,v in itertools.combinations(E,2):
 for x,y in itertools.product((0,1),repeat=2):ck(any(a[u]==x and a[v]==y for a in C),'pair cover')
# Independently rederive the A/B matrices without producer code.
def matrix(p):
 M=[[0,0],[0,0]]
 for left,right in itertools.product((0,1),repeat=2):
  free=[v for v in range(1,10) if v not in p and v!=5]
  for z in itertools.product((0,1),repeat=len(free)):
   a=dict(p);a.update(zip(free,z));a[5]=left
   good=True
   for j,c in enumerate(F):
    if not any((right if j==0 and q==5 else a[abs(q)])==int(q>0) for q in c):good=False;break
   M[left][right]+=good
 return M
ck(matrix({1:1,2:0,3:1,4:0,8:0})==o['WA'],'independent WA')
ck(matrix({1:1,2:1,3:0,4:0,8:0})==o['WB'],'independent WB')
print(json.dumps({'status':'PASS','checks':checks,'P_vs_NP':'OPEN'},indent=2))
