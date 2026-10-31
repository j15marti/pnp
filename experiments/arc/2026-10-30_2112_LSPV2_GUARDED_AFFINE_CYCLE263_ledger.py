#!/usr/bin/env python3
"""Explicit physical record/tape/child accounting, not a native FLMV simulation."""
import json,sys,math
raw=json.load(open(sys.argv[1]))
obj={'basis':'indexed signed-clause-word accounting; Python arrays kept; no native FLMV bound',
     'encoding':'w=max(2,ceil(log2(2n+2))); header 2 words; per clause 1 width word plus 1 signed literal word per occurrence',
     'arc_requirements':'lambda=1/2, sigma=1/2; generated append-only child fails size target, actual Python source copy fails workspace target',
     'cases':{}}
for name,case in raw['cases'].items():
    F=case['F'];n=case['meta']['n'];m=len(F);L=sum(map(len,F));w=max(2,(2*n+1).bit_length())
    N=(2+m+L)*w
    blocker=case['blocker'];outclause=blocker['clause'] if blocker else []
    Nchild=N+(1+len(outclause))*w if blocker else N
    rows=len(case['source_rows']);pairs=4*rows
    # A conservative record/ledger estimate for the *declared named arrays*.
    # This ignores runtime overhead and cannot serve as a tape upper bound.
    named_bytes=(13*rows+7*pairs+2*L)*w
    n_gf_rows=rows*(n+rows+2)
    live=named_bytes+n_gf_rows+len(outclause)*w
    ops=case['hybrid_ledger']
    record={'n':n,'m':m,'literal_occurrences':L,'signed_word_bits':w,
       'source_bit_length_N':N,'source_words':2+m+L,
       'literal_reads_discovery':case['discovery'].get('source_literal_reads',0),
       'other_recognition_trials':sum(case['discovery'].get(k,0) for k in ('candidate_split_checks','guard_template_trials','parity_template_trials')),
       'failed_policies':ops.get('failed_policy_trials',0),
       'policy_switches':ops.get('policy_switches',0),
       'gaussian_xor_pivots':ops.get('xor_pivots',0),
       'gaussian_xor_updates':ops.get('xor_row_updates',0),
       'proof_local_checks':ops.get('certificate_checks',0),
       'guest_A_queries':0,
       'guest_A_query_bits':0,
       'explicit_full_parent_copy_required_for_returned_F_and_blocker':bool(blocker),
       'append_only_child_bits':Nchild,
       'child_to_source_size_ratio':round(Nchild/N,5),
       'arc_power_half_target_bits':int(N**.5),
       'power_short_child_exists_in_this_run':False,
       'source_retained_in_python':True,
       'separately_named_array_bits_estimate_not_usable_as_machine_bound':live,
       'dpll_clause_scans':ops.get('clause_scans',0),
       'dpll_branch_clause_scans':ops.get('branch_clause_scans',0),
       'dpll_literal_tests':ops.get('literal_tests',0),
       'native_random_access_head_transitions':'NOT MEASURED',
       'max_simultaneously_live_FLVM_tape_bits':'NOT CERTIFIED'}
    obj['cases'][name]=record
obj['totals']={'initial_source_bits':sum(c['source_bit_length_N'] for c in obj['cases'].values()),
  'append_only_output_bits':sum(c['append_only_child_bits'] for c in obj['cases'].values()),
  'recognition_source_literal_reads':sum(c['literal_reads_discovery'] for c in obj['cases'].values()),
  'failed_policies':sum(c['failed_policies'] for c in obj['cases'].values()),
  'policy_switches':sum(c['policy_switches'] for c in obj['cases'].values()),
  'native_FLVM_model':'OPEN'}
with open(sys.argv[2],'w') as f:json.dump(obj,f,indent=2,sort_keys=True)
print(json.dumps(obj['totals'],indent=2))