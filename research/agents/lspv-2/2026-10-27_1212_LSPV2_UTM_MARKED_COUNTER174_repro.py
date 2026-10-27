#!/usr/bin/env python3
"""UTM-MARKED-COUNTER174. Python >=3.10, no external dependencies.
Exact 15-name signed (2,2) four-mode SAT gadget and finite-state one-marker
position counter on a specially tagged CANONICAL SAT promise. The Python
host is a trace harness, not a proposed unrestricted SAT algorithm.
"""
import json, itertools, collections, hashlib, argparse

W1 = (
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))
A = ((6,0),(11,0)); B = ((17,2),(9,2))
FIXED = tuple(i for i in range(20) if i not in {6,11,17,9})


def H(a,b):
    out=[list(c) for c in W1]
    if not a:
        for i,j in A: out[i][j]=-out[i][j]
    if not b:
        for i,j in B: out[i][j]=-out[i][j]
    return tuple(map(tuple,out))


def holds(formula,mask):
    return all(any(bool((mask>>(abs(l)-1))&1)==(l>0) for l in c)
               for c in formula)


def audit_gadget():
    counts={}; checks=0
    for a,b in itertools.product((0,1),repeat=2):
        f=H(a,b); pc=collections.Counter()
        for c in f:
            assert len(c)==3 and len(set(map(abs,c)))==3
            for l in c: pc[(abs(l),l>0)]+=1
        assert len(set(f))==20
        assert all(pc[(v,True)]==pc[(v,False)]==2 for v in range(1,16))
        ct=0
        for mask in range(1<<15):
            ct += holds(f,mask); checks+=1
        counts[f'{a}{b}']=ct
    assert counts=={'00':772,'01':272,'10':272,'11':0}
    assert holds(H(0,0),616) and holds(H(0,1),616)
    assert holds(H(1,0),4742) and not holds(H(1,1),4742)
    return {'counts':counts,'w0':616,'w1':4742,'model_membership_tests':checks,
            'A_switch_positions':A,'B_switch_positions':B}


def offs(lit,k):
    return (1 if lit>0 else -1)*(abs(lit)+15*k)


def format_clause(clause):
    return ','.join(('+' if l>0 else '-')+format(abs(l),'b') for l in clause)+';'


def enc(m,a,b):
    """One finite-alphabet canonical source layout L{two clauses} G{16} R{two}E.
    Fixed tags are syntax, not a standard DIMACS parser or arbitrary-SAT format.
    All source variable names are ordinary signed binary IDs; tags are constant.
    """
    L=[];F=[];R=[]
    for i in range(m):
        f=H(a[i],b[i]); mapped=lambda idx:format_clause(tuple(offs(l,i) for l in f[idx]))
        L.append('{'+mapped(6)+mapped(11)+'}')
        R.append('{'+mapped(17)+mapped(9)+'}')
        F.extend(mapped(j) for j in FIXED)
    return 'L'+''.join(L)+'G'+''.join(F)+'R'+''.join(R)+'E'


def parsed_formula(m,a,b):
    clauses=[]
    for i in range(m):
        f=H(a[i],b[i]);clauses.extend(tuple(offs(l,i) for l in c) for c in f)
    return tuple(clauses)


def exact_incidence(formula,m):
    cnt=collections.Counter(); seen=set()
    for c in formula:
        assert len(c)==3 and len({abs(l) for l in c})==3 and c not in seen
        seen.add(c)
        for l in c: cnt[(abs(l),l>0)]+=1
    assert len(formula)==20*m
    assert all(cnt[(v,True)]==cnt[(v,False)]==2 for v in range(1,15*m+1))


class MarkedCounterTM:
    """Single two-way READ-ONLY source head + one two-way READ/WRITE work head.

    Every work cell is BLANK except work cell zero, changed to '#' once.
    Actual decisions inspect only finite-state control, current input char,
    and current work symbol (# or blank). Host integers are TRACE METRICS ONLY.
    Source is a specially tagged, honest, syntactically fixed-layout promise.
    """
    def __init__(self,x):
        self.x=x;self.n=len(x);self.ip=0;self.wp=0
        self.state='INIT';self.abit=None;self.marker=False
        self.t=0;self.ih=0;self.wh=0;self.reversals=0;self.last_input_dir=0
        self.work_visited={0};self.input_read={};self.D=0;self.writes=0
        self.output=None;self.output_bits=0;self.transitions_by_state=collections.Counter()

    def probe(self):
        assert 0<=self.ip<self.n
        return self.x[self.ip], '#' if self.marker and self.wp==0 else '_'

    def transition(self):
        c,w=self.probe();s=self.state;d_i=0;d_w=0;new=s
        if s=='INIT':
            assert not self.marker and self.wp==0
            self.marker=True;self.D+=1;self.writes+=1;new='L_START'
        elif s=='L_START':
            assert c=='L';d_i=1;new='A_DECIDE'
        elif s=='A_DECIDE':
            if c=='G':
                if w=='#':self.output=True;new='HALT'
                else:self.output=False;new='HALT'
            elif c=='{':
                d_i=1;new='A_READ' if w=='#' else 'A_SKIP'
            else:raise AssertionError(('bad A grammar',s,c,self.ip))
        elif s=='A_SKIP':
            d_i=1
            if c=='}': d_w=-1;new='A_DECIDE'
        elif s=='A_READ':
            assert c in '+-';self.abit=(c=='+');d_i=-1;new='A_BACK_TARGET'
        elif s=='A_BACK_TARGET':
            assert c=='{';d_i=-1;new='A_BACK'
        elif s=='A_BACK':
            if c=='L':new='FIND_R'
            else:
                d_i=-1
                if c=='{':d_w=1
        elif s=='FIND_R':
            if c=='R':d_i=1;new='B_DECIDE'
            else:d_i=1
        elif s=='B_DECIDE':
            if c=='{':d_i=1;new='B_COMMA1' if w=='#' else 'B_SKIP'
            else:raise AssertionError(('bad B grammar',s,c,self.ip))
        elif s=='B_SKIP':
            d_i=1
            if c=='}':d_w=-1;new='B_DECIDE'
        elif s=='B_COMMA1':
            d_i=1
            if c==',':new='B_COMMA2'
        elif s=='B_COMMA2':
            d_i=1
            if c==',':new='B_READ'
        elif s=='B_READ':
            assert c in '+-'
            if self.abit and c=='+':self.output=False;new='HALT'
            else:d_i=-1;new='B_BACK_TARGET'
        elif s=='B_BACK_TARGET':
            if c=='{':d_i=-1;new='B_BACK'
            else:d_i=-1
        elif s=='B_BACK':
            if c=='R':d_i=-1;new='RETURN_L'
            else:
                d_i=-1
                if c=='{':d_w=1
        elif s=='RETURN_L':
            if c=='L':d_w=1;new='L_START'
            else:d_i=-1
        else:raise AssertionError(s)
        self.transitions_by_state[s]+=1;self.t+=1
        self.input_read[self.ip]=self.input_read.get(self.ip,0)+1
        assert self.t<=100*self.n*self.n, 'timeout'
        if d_i:
            if self.last_input_dir and d_i!=self.last_input_dir:self.reversals+=1
            self.last_input_dir=d_i;self.ih+=1
        self.ip+=d_i;self.wp+=d_w;self.wh+=abs(d_w)
        self.work_visited.add(self.wp)
        assert self.wp>=0 and self.ip>=0 and self.ip<self.n
        self.state=new
        if new=='HALT':
            self.output_bits=1;self.t+=1 # one write-only output transition
        return self.state

    def run(self):
        while self.state!='HALT':self.transition()
        assert self.D==1 and self.writes==1
        return {'decision':self.output,'T_multi':self.t,'S_work_visited':len(self.work_visited),
          'D_actual_work_symbol_changes':self.D,'work_write_attempts':self.writes,
          'H_input_moves':self.ih,'R_input_reversals':self.reversals,
          'H_work_moves':self.wh,'Q_all_input_plus_work_probes':2*(self.t-1),
          'head_boundary_crossings':self.ih+self.wh,
          'input_distinct_positions_read':len(self.input_read),'work_head_peak_offset':max(self.work_visited),
          'L_output_bits':self.output_bits,'states_visited':len(self.transitions_by_state)}


def elementary_model(m,a,b):
    return all(not(x and y) for x,y in zip(a,b))


def audit():
    raw={'status':'COMPUTATIONAL (finite) + separately stated general lemmas',
      'witness_gadget':audit_gadget(),
      'counter_model':'one sequential read-only input head; one two-way blank work tape, one changed origin mark',
      'declared_assumptions':['fixed canonical L/G/R/E grammar, binary signed clauses, two per variable module',
       'workhead positions are not free work bits: visited cells S includes blanks',
       'input head moves/reversals charged; no read/write of immutable input',
       'NOT an all-input ordinary SAT decision algorithm'],
      'cases':[],'malformed_controls':[]}
    worst_by_m=[];tots=collections.Counter();max_groups=0
    for m in range(1,6):
        cases=0;max_t=0;max_s=0;min_t=10**30;max_r=0;max_h=0
        for ai in range(1<<m):
            a=tuple((ai>>i)&1 for i in range(m))
            for bi in range(1<<m):
                b=tuple((bi>>i)&1 for i in range(m))
                f=parsed_formula(m,a,b)
                exact_incidence(f,m)
                text=enc(m,a,b)
                # Recompute actual clause list by splitting the three zones to
                # check that every binary-ID token corresponds to its signed literal.
                payload=text[1:].replace('{','').replace('}','').replace('G','').replace('R','').rstrip('E')
                expected=[t for t in payload.split(';') if t]
                assert len(expected)==20*m
                labels={tuple(int(s,2)*(1 if sign=='+' else -1)
                     for sign,s in ((lit[0],lit[1:]) for lit in item.split(',')))
                     for item in expected}
                assert len(labels)==20*m
                assert labels==set(f)
                t=MarkedCounterTM(text).run()
                assert t['decision']==elementary_model(m,a,b)
                assert t['D_actual_work_symbol_changes']==1
                assert t['S_work_visited']==m+1 if t['decision'] else t['S_work_visited']<=m+1
                cases+=1;min_t=min(min_t,t['T_multi']);max_t=max(max_t,t['T_multi'])
                max_s=max(max_s,t['S_work_visited']);max_r=max(max_r,t['R_input_reversals'])
                max_h=max(max_h,t['H_input_moves'])
                tots['simulated_transitions']+=t['T_multi']
                tots['literal_field_checks']+=60*m
                if cases==1:raw['cases'].append({'m':m,'a':a,'b':b,'T':t['T_multi'],
                    'source_bits':8*len(text),'source_chars':len(text),**t})
        worst_by_m.append({'m':m,'pairs_checked':cases,'max_time':max_t,
            'min_time':min_t,'max_work_cells':max_s,'max_reversals':max_r,
            'max_input_moves':max_h,'source_chars_example':len(enc(m,(0,)*m,(0,)*m))})
        max_groups+=cases
    raw['all_pair_controls']=worst_by_m
    raw['total_pairs']=max_groups
    raw['total_transitions']=tots['simulated_transitions']
    raw['all_boolean_promise_circuits']=[{'m':m,'G_boolean_gates':2*m,
        'gate_input_refs':4*m-1,'logical_input_wires':2*m,'logical_gate_output_wires':2*m,
        'output_bits':1} for m in range(1,6)]
    raw['canonical_false_positive_guard']={
      'meaning':'if the promise is violated, the counter can accept a noncanonical string',
      'example':enc(1,(0,),(0,)).replace('R{', 'R{!',1),
      'note':'the inserted exclamation mark is not a valid signed clause token; no general parser claimed'}
    raw['theorem_boundary']={
      'D_zero_two_way_uniform_blank':'FINITE-STATE ONLY; regular-language barrier',
      'D_one_single_origin_marker':'EXPLICIT upper; S<=m+1, T=O(mN), R=O(m)',
      'nonregularity':'fixed-gap Alice/Bob Myhill-Nerode prefixes 2^m for every m',
      'witness_only':'Alice-local 616/4742 witnesses can be printed without reading Bob; not sound acceptance',
      'RAM_vs_tape':'separate; no FLMV contraction','P_vs_NP':'OPEN'}
    return raw

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='2026-10-27_1212_LSPV2_UTM_MARKED_COUNTER174_raw.json');args=p.parse_args()
    raw=audit();out=json.dumps(raw,sort_keys=True,indent=2)+'\n'
    with open(args.output,'w') as f:f.write(out)
    print(json.dumps({'gadget_counts':raw['witness_gadget']['counts'],'pair_tests':raw['total_pairs'],
       'all_source_transitions':raw['total_transitions'],'worst':raw['all_pair_controls'],
       'raw_sha256':hashlib.sha256(out.encode()).hexdigest()},indent=2))


def full_single_tape_rescan(x):
    """Independent 4-sweep, multi-track ONE shared read/write tape control.

    One initial input-to-product alphabet formatting sweep plus return. Each
    source step uses read-forward, update/reverse, marker-forward and return.
    Marker propagation is purely local, with no arbitrary head relocation.
    The source delta table is the single declared verifier transition table;
    independent tape positions/symbols are checked at EVERY transition.
    """
    src=MarkedCounterTM(x); n=len(x)
    tape=[{'input':c,'work':'_','ih':j==0,'wh':j==0} for j,c in enumerate(x)]
    t1=2*n;h1=2*(n-1);probes=2*n;write_events=n
    checks=0;main_steps=0
    while src.state!='HALT':
        old_ip,old_wp=src.ip,src.wp
        assert sum(int(c['ih']) for c in tape)==1
        assert sum(int(c['wh']) for c in tape)==1
        got_input=None;got_work=None
        # First sweep to read both simulated heads' symbols.
        for j in range(n):
            probes+=1;write_events+=1;t1+=1
            if j:h1+=1
            c=tape[j]
            if c['ih']:got_input=c['input']
            if c['wh']:got_work=c['work']
        assert (got_input,got_work)==src.probe()
        # Mutate the INDEPENDENT source machine, then realize its legal
        # two head movements by physically local marker transfers.
        src.transition();main_steps+=1
        di=src.ip-old_ip;dw=src.wp-old_wp
        assert abs(di)<=1 and abs(dw)<=1
        need_i_left=False;need_w_left=False
        for j in range(n-1,-1,-1):
            probes+=1;write_events+=1;t1+=1
            if j<n-1:h1+=1
            c=tape[j];oldih=c['ih'];oldwh=c['wh']
            if j==old_wp:
                c['work']='#' if src.marker and old_wp==0 else '_'
            if need_i_left:
                assert not oldih;c['ih']=True;need_i_left=False
            if need_w_left:
                assert not oldwh;c['wh']=True;need_w_left=False
            if oldih and di==-1:
                assert j>0;c['ih']=False;need_i_left=True
            if oldwh and dw==-1:
                assert j>0;c['wh']=False;need_w_left=True
        assert not need_i_left and not need_w_left
        need_i_right=False;need_w_right=False
        for j in range(n):
            probes+=1;write_events+=1;t1+=1
            if j:h1+=1
            c=tape[j];oldih=c['ih'];oldwh=c['wh']
            if need_i_right:
                assert not oldih;c['ih']=True;need_i_right=False
            if need_w_right:
                assert not oldwh;c['wh']=True;need_w_right=False
            if oldih and di==1:
                assert j<n-1;c['ih']=False;need_i_right=True
            if oldwh and dw==1:
                assert j<n-1;c['wh']=False;need_w_right=True
        assert not need_i_right and not need_w_right
        for j in range(n-1,-1,-1):
            probes+=1;write_events+=1;t1+=1
            if j<n-1:h1+=1
        assert tape[src.ip]['ih'] and tape[src.wp]['wh']
        assert all(c['work']==('#' if src.marker and j==0 else '_')
                   for j,c in enumerate(tape))
        checks+=1
    # Append one output bit on tape to avoid a free write-only output channel.
    t1+=n+1;h1+=n;probes+=1;write_events+=1
    assert src.output_bits==1
    assert t1==4*n*main_steps+3*n+1
    assert t1<=4*(main_steps+1)*(n+len(src.work_visited)+(main_steps+2).bit_length())+1
    return {'decision':src.output,'Mk_transitions':src.t,
       'M1_transitions':t1,'M1_head_steps':h1,
       'M1_total_footprint_including_input':n+1,
       'M1_physical_probes':probes,'M1_write_events_including_unchanged':write_events,
       'M1_emitted_output_bits':1,'same_step_configuration_checks':checks}


if __name__=='__main__':
    # Independent, small full-machine regression. Append to same raw artifact.
    controls=[]
    for m,pairs in ((1,[(0,0),(0,1),(1,0),(1,1)]),
                    (2,[(0,0),(1,1),(1,3),(3,3)])):
        for ai,bi in pairs:
            a=tuple((ai>>i)&1 for i in range(m));b=tuple((bi>>i)&1 for i in range(m))
            out=full_single_tape_rescan(enc(m,a,b))
            assert out['decision']==elementary_model(m,a,b)
            controls.append({'m':m,'a':ai,'b':bi,**out})
    with open(args.output) as f:raw=json.load(f)
    raw['full_one_tape_simulation_controls']=controls
    raw['full_one_tape_same_step_checks']=sum(x['same_step_configuration_checks'] for x in controls)
    data=json.dumps(raw,sort_keys=True,indent=2)+'\n'
    with open(args.output,'w') as f:f.write(data)
    print(json.dumps({'M1_controls':len(controls),
       'M1_same_step_checks':raw['full_one_tape_same_step_checks'],
       'new_raw_sha256':hashlib.sha256(data.encode()).hexdigest()}))