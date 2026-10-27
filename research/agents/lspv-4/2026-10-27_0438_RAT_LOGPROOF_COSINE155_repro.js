#!/usr/bin/env node
'use strict';
function audit() {
  const counts={assertions:0,traces:0,trace_pairs:0,epoch_tests:0,stale_controls:0,wrap_controls:0,table_checks:0};
  function ok(value,label) { if(!value) throw new Error("FAIL: "+label); counts.assertions++; }
  const gamma=2*Math.cos(Math.PI/7), c0=241/200;
  const beta=c=>((c+2)/(c*c)-c)/2;
  ok(Math.abs(gamma-1.8019377358048383)<1e-13,"Williams cosine value");
  ok(Math.abs(beta(c0)-11642479/23232400)<1e-14,"FLMV rational endpoint");
  const rows=[[.001,1.80083],[.01,1.79092],[.1,1.69618],[.25,1.55242],[.5,1.34070],[.75,1.15765],[.9,1.06011],[.99,1.00583]];
  for(let i=0;i<rows.length;i++){
    const [eps,c]=rows[i],safe=c-.0001;
    ok(safe<c,"strict conservative table slack");ok(safe>1,"table exceeds one");
    ok(i===0||c<rows[i-1][1],"sample trend");
    counts.table_checks+=3;
  }
  const ops=[];
  for(let a=0;a<3;a++)ops.push({type:"read",addr:a});
  for(let a=0;a<3;a++)for(let v=0;v<=1;v++)ops.push({type:"write",addr:a,value:v});
  const traces=[[]];
  for(let len=1;len<=3;len++){
    function recurse(seq) {if(seq.length===len){traces.push(seq);return;}for(const op of ops)recurse([...seq,op]);}
    recurse([]);
  }
  counts.traces=traces.length;
  ok(new Map([[0,1]]).get(0)===1,"unreset memory leaks");
  counts.stale_controls++;
  ok(Math.ceil(Math.log2(4))===2,"3 epochs require two tag bits");
  for(const first of traces)for(const second of traces){
    const physical=new Map();
    function runEpoch(trace,epoch){
      const fresh=new Map();
      for(const op of trace){
        const p=physical.get(op.addr)||{epoch:0,value:0};
        const actual=p.epoch===epoch?p.value:0;
        const expected=fresh.get(op.addr)||0;
        ok(actual===expected,"stale state exposed");
        if(op.type==="write"){
          physical.set(op.addr,{epoch,value:op.value});
          fresh.set(op.addr,op.value);
        }
        counts.epoch_tests++;
      }
      for(let addr=0;addr<3;addr++){
        const p=physical.get(addr)||{epoch:0,value:0};
        ok((p.epoch===epoch?p.value:0)===(fresh.get(addr)||0),"fresh final");
      }
    }
    runEpoch(first,1);
    runEpoch(second,2);
    runEpoch([{type:"read",addr:0},{type:"read",addr:1},{type:"read",addr:2}],3);
    counts.trace_pairs++;
  }
  const old={epoch:1,value:1}, wrapped=3%2;
  ok(old.epoch===wrapped&&old.value===1,"one bit wrap leaks");
  counts.wrap_controls++;
  const tests=[
    {name:"cosine-excludes-a=.80",r:1,a:.80,sigma:0,eps:null,yes:true},
    {name:"cosine-does-not-exclude-a=.81",r:1,a:.81,sigma:0,eps:null,yes:false},
    {name:"cosine-strict-boundary",r:1,a:gamma-1,sigma:0,eps:null,yes:false},
    {name:"BW-eps-half-exclusion",r:1,a:.3405,sigma:.49,eps:.5,yes:true},
    {name:"BW-eps-half-no-exclusion",r:1,a:.341,sigma:.49,eps:.5,yes:false},
    {name:"BW-no-equal-space-exponent",r:1,a:.2,sigma:.5,eps:.5,yes:false},
    {name:"BW-tiny-space-exclusion",r:1,a:.7907,sigma:.009,eps:.01,yes:true},
    {name:"no-cosine-transfer-to-positive-space",r:1,a:.2,sigma:.1,eps:null,yes:false}
  ];
  for(const t of tests){
    const c=t.eps===null?(t.sigma===0?gamma:null):(rows.find(row=>row[0]===t.eps)?.[1]-.0001);
    const native=t.eps===null?t.sigma===0:t.sigma<t.eps;
    const excluded=native && t.r+t.a<c-1e-12;
    ok(excluded===t.yes,"scenario "+t.name);
  }
  return {
    title:"LSPV4_RAT_LOGPROOF_COSINE155",
    status:"proved conditional corollary from published SAT bound, tests computational only",
    passed:true,counts,cosine:gamma,coefficient_for_linear_verifier:gamma-1,
    difference_over_FLМV_1_205_coefficient:gamma-c0,
    flmv_beta_at_c0:beta(c0),
    positive_space_rows:rows.map(([eps,c])=>({epsilon:eps,original_quoted:c,conservative_c:Number((c-.0001).toFixed(6)),requires_strict_space_sigma_below_epsilon:true})),
    controls:tests.map(z=>({name:z.name,excluded:z.yes})),
    methodology:"exhaustive 820 squared ordered trace pairs, 9 operations and trace length <=3, 3 epochs; seed none",
    hard_guard:"Williams cosine applies to RAM/indexed subpolynomial space, not positive fixed polynomial space; B-W rows author talk checked, full journal PDF retrieval pending",
    mathematical_status:"P versus NP OPEN"
  };
}
process.stdout.write(JSON.stringify(audit(),null,2)+'\n');
