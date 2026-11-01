#!/usr/bin/env python3
"""Certified *terminal-only* semantic M22 constant reencoding.
Correctness is for original residual (F,p), not for unrestricted root F.
This is post-decision substitution, NOT an all-input ARC child compiler.
"""
import json,math
from pathlib import Path
from syndrome295 import Y6,F9,F15,P9,P15_U,P15_S,source198,valid,component_syndrome_terminal
R=Path(__file__).resolve().parent

def gamma(n):
 s=format(n,'b');return '0'*(len(s)-1)+s

def enc(F):
 n=max(abs(x) for c in F for x in c);w=n.bit_length()
 return gamma(n)+gamma(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(x),f'0{w}b') for x in c) for c in F)

def main():
 U,V=source198();assert valid(U) and valid(Y6)
 z=[]
 for name,F,p in [('F9_bad_cube_UNSAT',F9,P9),('F15_p_U_UNSAT',F15,P15_U),('F15_p_S_SAT',F15,P15_S),('F15_root_UNRESOLVED',F15,{})]:
  result=component_syndrome_terminal(F,p)
  if result['status']=='SAT': child=Y6;label='SAT'
  elif result['status'].startswith('UNSAT'): child=U;label='UNSAT'
  else:child=None;label='UNRESOLVED'
  parent=enc(F);childbits=enc(child) if child is not None else None
  if child is not None:assert valid(child)
  z.append({'source_case':name,'source_label_for_PINNED_branch':label,'source_clause_ids':list(range(len(F))),
   'original_formula_is_not_the_pinned_residual':bool(p),
   'original_canonical_source_bits':len(parent),'explicit_pin_count':len(p),
   'emitted_target_canonical_child_bits':len(childbits) if childbits is not None else None,
   'source_certificate':result['status'],'source_witness_checked':result['status']=='SAT',
   'terminal_decision_required_before_compiling':True,
   'hereditary_only_for_decided_residual':child is not None,
   'power_short_relative_to_original_body':bool(childbits is not None and len(childbits)**2<=len(parent)),
   'independently_verified_target_constant':'Y6 valid SAT' if label=='SAT' else ('U198 valid UNSAT by 384-query prior source certificate' if label=='UNSAT' else None)})
 (R/'semantic295.json').write_text(json.dumps({'status':'restricted post-decision terminal only','cases':z,'P_vs_NP':'OPEN'},indent=2)+'\n')
 print(json.dumps(z,indent=2))
if __name__=='__main__':main()