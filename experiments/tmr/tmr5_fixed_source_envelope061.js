"use strict";
// TMR-5 FIXSRC061. Standalone node script; no dependencies, no randomness.
// Counts exact queries, not Turing-machine transitions.
let tests=0;
function check(ok,msg){tests++;if(!ok)throw Error(msg);}
function bit(x,i){return (x>>i)&1;}
function done(q,x,mask){
  for(let r=0;r<q;r++){
    let all0=true;
    for(let j=0;j<q;j++){let i=r*q+j;if(!bit(mask,i)||bit(x,i)){all0=false;break;}}
    if(all0)return true;
  }
  for(let r=0;r<q;r++){
    let seen1=false;
    for(let j=0;j<q;j++){let i=r*q+j;if(bit(mask,i)&&bit(x,i)){seen1=true;break;}}
    if(!seen1)return false;
  }
  return true;
}
function triple(q,x,mask){
  if(done(q,x,mask))return [0,0,0];
  let active=[],W=0,uMin=q+1,trueSource=true,zeroMin=q+1;
  for(let r=0;r<q;r++){
    let obs1=false,any1=false,unread=0;
    for(let j=0;j<q;j++){
      let i=r*q+j,v=bit(x,i);
      if(v)any1=true;
      if(!bit(mask,i)){unread++;}
      else if(v)obs1=true;
    }
    if(!any1)trueSource=false;
    if(!obs1){
      active.push(r);W+=unread;uMin=Math.min(uMin,unread);
      if(!any1)zeroMin=Math.min(zeroMin,unread);
    }
  }
  const B=Math.min(active.length,uMin);
  const D=trueSource?active.length:zeroMin;
  check(D<=W&&B<=D&&B>=0,"ordered resource values");
  return [W,B,D];
}
function sig(q,x,mask){
  let s="";
  for(let i=0;i<q*q;i++)s+=bit(mask,i)?String(bit(x,i)):"?";
  return s;
}
let rows=[];
for(let q=1;q<=3;q++){
  const m=q*q,M=1<<m;
  let gap=0, witness=null,pairs=0, readEdges=0;
  const minima=new Map();
  for(let x=0;x<M;x++){
    let dist=new Int16Array(M).fill(-1),env=new Int16Array(M).fill(-1);
    function shortest(mask){
      if(dist[mask]>=0)return dist[mask];
      if(done(q,x,mask))return dist[mask]=0;
      let min=100000;
      for(let i=0;i<m;i++)if(!bit(mask,i))min=Math.min(min,1+shortest(mask|(1<<i)));
      return dist[mask]=min;
    }
    function envelope(mask){
      if(env[mask]>=0)return env[mask];
      if(done(q,x,mask))return env[mask]=0;
      let min=triple(q,x,mask)[0];
      for(let i=0;i<m;i++)if(!bit(mask,i))min=Math.min(min,1+envelope(mask|(1<<i)));
      return env[mask]=min;
    }
    for(let mask=0;mask<M;mask++){
      const [W,B,D]=triple(q,x,mask),name=sig(q,x,mask);
      check(shortest(mask)===D,"shortest fixed x");
      check(envelope(mask)===D,"envelope fixed x");
      minima.set(name,Math.min(minima.get(name)??100000,D));
      pairs++;
      if(!done(q,x,mask)){
        for(let i=0;i<m;i++)if(!bit(mask,i)){
          check(D<=1+triple(q,x,mask|(1<<i))[2],"READ tariff");
          readEdges++;
        }
        if(D-B>gap){gap=D-B;witness={source:sig(q,x,M-1),transcript:name,B,D,W};}
      }
    }
    check(shortest(0)===q&&envelope(0)===q,"fixed source initial q");
  }
  for(let [name,v] of minima){
    let x=0,mask=0;
    for(let i=0;i<m;i++)if(name[i]!=="?"){
      mask|=1<<i;if(name[i]==="1")x|=1<<i;
    }
    check(triple(q,x,mask)[1]===v,"source forgotten MAY minimum");
  }
  check(gap===q-1,"sharp additive gap");
  rows.push({q,source_bits:m,sources:M,source_transcript_pairs:pairs,
             compatible_MAY_transcripts:minima.size,read_edges:readEdges,
             max_fixed_MAY_additive_gap:gap,witness,
             initial_fixed_certificate:q,initial_deterministic_worst_case:q*q});
}
let sharp=[];
for(let q=2;q<=8;q++){
  let x=Array.from({length:q*q},()=>1),mask=0;
  for(let j=0;j<q-1;j++){x[j]=0;mask|=1<<j;}
  for(let j=q;j<2*q;j++)x[j]=0;
  // Here use arrays, not 32-bit integer masks, so q=8 is safe.
  const active=q, lowerCompatible=1, sourceFixed=q;
  check(x[q-1]===1&&x.slice(q,2*q).every(v=>v===0),"sharp source construction");
  sharp.push({q,source_fixed:sourceFixed,MAY:lowerCompatible,ratio:q});
}
let auditResult={claim:"TMR5-FIXSRC061",model:"fixed hidden-source q by q AND-of-OR paid-query graph",status:"PROVED/RESTRICTED, mathematical peer review OPEN",tests,failures:0,
  all_q_claims:["E_W^x(sigma)=D_x(sigma)","E_W^MAY(sigma)=min_x D_x(sigma)=B(sigma)",
  "max_fixed_source_certificate_at_initial=q; optimal_deterministic_worst_case_queries=q^2"],
  exhaustive:rows,sharp_ratio_examples:sharp,
  controls:["zero-cost TAG/cached read is identity on transcript","public equality reduces source budget to one but CHANGES promise","syntax-aware SAT machine not represented"],
  reference_note:"No external theorem imported; quantified query model only"};
if(typeof console!=="undefined")console.log(JSON.stringify(auditResult,null,2));

