#!/usr/bin/env node
// Standalone deterministic test: node <filename>. Reproduces corresponding raw JSON exactly.
const run = function audit() {
  "use strict";
  let assertions=0;
  const check=(p,msg)=>{if(!p)throw Error("Audit assertion failed: "+msg);assertions++};
  const gcd=(a,b)=>b?gcd(b,a%b):a;
  const frac=(n,d)=>{let a=BigInt(n),b=BigInt(d),g=gcd(a,b);return [(a/g).toString(),(b/g).toString()].join("/")};
  const gamma=z=>{if(z<1)throw Error("gamma requires positive integer");const b=z.toString(2);return "0".repeat(b.length-1)+b};
  const encode=F=>{
    const n=Math.max(0,...F.flat().map(x=>Math.abs(x)));
    return gamma(n+1)+gamma(F.length+1)+F.map(C=>gamma(C.length+1)+C.map(x=>(x>0?"1":"0")+gamma(Math.abs(x))).join("")).join("");
  };
  const SAT=F=>{
    const n=Math.max(0,...F.flat().map(x=>Math.abs(x)));
    check(n<=3,"toy SAT bound");
    for(let bits=0;bits<(1<<n);bits++)
      if(F.every(C=>C.some(x=>(Boolean(bits&(1<<(Math.abs(x)-1)))===(x>0)))))return true;
    return false;
  };
  // Full-parent decision call is deliberately charged and destroys contraction.
  const child=(F,level)=>{
    const label=SAT(F), C=label?[[1]]:[[1],[-1]];
    if(level===1)for(let i=0;i<10;i++)C.push([1,-1,2]);
    return C;
  };
  const cases={
    empty_true:[],unit_true:[[1]],unit_false:[[1],[-1]],
    horn_true:[[1],[-1,2]],horn_false:[[1],[-1,2],[-2]],
    xor_true:[[1,2],[-1,-2]],
    xor_false:[[1,2],[-1,-2],[1,-2],[-1,2]],
    twosat_true:[[1,2],[-1,2],[1,-2]],
    twosat_false:[[1,2],[-1,2],[1,-2],[-1,-2]],
    threevar_true:[[1,2,3],[-1,2],[-2,3]],
    threevar_false:[[1],[-1,2],[-2,3],[-3]]
  };
  const twoLevel=[];
  for(const [name,F] of Object.entries(cases))for(const pad of [32,64,128]){
    const source=F.concat(Array.from({length:pad},()=>[1,-1,2]));
    const A=child(source,1),B=child(A,2);
    const labels=[SAT(source),SAT(A),SAT(B)];
    const lengths=[encode(source).length,encode(A).length,encode(B).length];
    check(labels[0]===labels[1]&&labels[1]===labels[2],"both labels "+name);
    check(lengths[0]>lengths[1]&&lengths[1]>lengths[2],"two shortening levels "+name);
    twoLevel.push({case:name,pad,N_bits:lengths[0],child1_bits:lengths[1],child2_bits:lengths[2],SAT:labels[0],full_parent_solver_invocations:2});
  }
  function powBig(a,b){return BigInt(a)**BigInt(b);}
  const retention=[];
  for(const N of [64,128,256,512,1024,2048,4096]){
    let k=1;while(powBig(k,10)<powBig(N,9))k++;
    const workspace=Array(k).fill(0);
    for(let i=0;i<k;i++)workspace[i]=0; // unchanged work writes still cost steps
    check(powBig(k,10)>=powBig(N,9)&&powBig(k-1,10)<powBig(N,9),"exact 0.9 ceil");
    check(workspace.length===k,"peak cells");
    retention.push({N,peak_work_cells:k,unchanged_writes:k,highest_work_address:k-1,streaming_variant_peak_cells:2});
  }
  const volume=[];
  for(const d of [1,2,3,4])for(const lengths of [[1,1,1,1],[1,2,3,5],[2,2,3],[1,4,4,4,7]]){
    const V=lengths.reduce((a,b)=>a+b,0),M=Math.max(...lengths);
    const L=lengths.reduce((a,b)=>a+b**d,0),R=V*M**(d-1);
    check(L<=R,"sum power bound");
    volume.push({d,lengths,V,M,solver_work:L,volume_cap:R});
  }
  const exact22=[[1,2,3],[1,2,3],[1,2,3]];
  const p=exact22.flat().filter(x=>x===1).length,m=exact22.flat().filter(x=>x===-1).length;
  check(p===3&&m===0,"literal copied occurrences");
  // beta((241/200)) = 11642479 / 23232400, exact independent cross-multiply
  const cNum=241n,cDen=200n;
  const bnum=((cNum+2n*cDen)*cDen**2n-cNum**3n), bden=2n*cNum**2n*cDen;
  check(bnum*23232400n===11642479n*bden,"FLMV beta exact identity");
  const seedNum=901n,seedDen=500n;
  const cn=(2n*seedNum-seedDen)*seedDen,cd=seedNum*(seedNum-seedDen);
  check(cn*361301n===cd*651000n,"conditional companion rational");
  return {
    run_id:"ARC-CIRCUIT-VOLUME-AUDIT124",date_utc:"2026-10-26",kind:"finite symbolic/numerical audit, not physical FLMV TM trace",
    seed:null,assertions,failures:0,
    exact_thresholds:{time:"241/200",space:"11642479/23232400",
      beta_at_time:frac(bnum,bden),time_slack_above_6_5:frac(1n,200n),
      space_slack_above_half:frac(26279n,23232400n),
      conditional_d:"901/500",conditional_c:frac(cn,cd),
      conditional_d_minus_c:frac(32201n,180650500n)},
    two_level_decide_first:twoLevel,
    retained_peak_space_counterexample:retention,
    volume_inequality_controls:volume,
    literal_copy_counterexample:{clauses:exact22,positive_x:p,negative_x:m,desired_each_sign:2},
    disclaimer:"Logical operation-count checks only. Fixed source children are easy; parent SAT called before both levels; memory counterexample refutes an implementation ledger, not a lower bound for arbitrary algorithms."
  };
};
process.stdout.write(JSON.stringify(run(),null,2)+'\n');
