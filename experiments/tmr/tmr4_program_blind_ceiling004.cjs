#!/usr/bin/env node
"use strict";
// TMR-4/004. Finite semantic regression, NOT a physical Turing machine.
// Usage: node experiments/tmr/tmr4_program_blind_ceiling004.cjs
function audit() {
  let seed=20261113>>>0;
  const next=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed;};
  const count={on_target:0,off_target:0,may_edges:0,shortcut_failures:0,
    virtual_completions:0,suffix_checks:0,last_bit_pairs:0};
  function encode(n, clauses) {
    const w=Math.max(1,Math.ceil(Math.log2(n)));
    return "1".repeat(n)+"0"+"1".repeat(clauses.length)+"0"+
      clauses.flatMap(cl=>cl.map(([v,s])=>String(s)+v.toString(2).padStart(w,"0"))).join("");
  }
  function parse(x) {
    if(!/^[01]+$/.test(x))return null;
    const n=x.indexOf("0"); if(n<3)return null;
    let p=n+1,m=0;
    while(p<x.length&&x[p]==="1"){p++;m++;}
    if(m<1||x[p]!=="0")return null;
    p++;const w=Math.max(1,Math.ceil(Math.log2(n)));
    if(x.length!==p+3*m*(w+1))return null;
    const clauses=[];
    for(let j=0;j<m;j++){
      let cl=[];
      for(let k=0;k<3;k++){
        const s=+x[p],v=parseInt(x.slice(p+1,p+1+w),2);
        p+=w+1;if(v>=n)return null;
        cl.push([v,s]);
      }
      if(new Set(cl.map(z=>z[0])).size!==3)return null;
      clauses.push(cl);
    }
    return {n,m,clauses};
  }
  function label(x) {
    const r=parse(x);if(!r)return "MALFORMED";
    for(let a=0;a<2**r.n;a++){
      if(r.clauses.every(cl=>cl.some(([v,s])=>((a>>>v)&1)===s)))return "SAT";
    }
    return "UNSAT";
  }
  // B_x is represented by an input-specific finite-state chain (hardwired
  // expected bits), with a universal exhaustive fallback on any mismatch.
  function hardwired(target,answer,incoming){
    const match=target===incoming;
    return {result:match?answer:label(incoming),match,
      on_match_scans:match?target.length+1:null};
  }
  function graphCeiling(L){
    const phi=Array.from({length:L+2},(_,i)=>L+1-i);
    for(let i=0;i<=L+1;i++){
      if(!(phi[i]<=phi[i]))throw Error("zero stutter");
      count.may_edges++;
      if(i<L+1){if(!(phi[i]<=1+phi[i+1]))throw Error("read edge");count.may_edges++;}
    }
    if(!(phi[0]<=L+100+phi[L+1]))throw Error("costly edge");
    count.may_edges++;
    if(phi[0]<=phi[L+1])throw Error("bad zero shortcut accepted");
    count.shortcut_failures++;
    return phi[0];
  }
  function suffix(x){
    const r=parse(x);if(!r)throw Error("invalid source");
    const L=x.length;
    const m=Math.min(Math.floor(Math.log2(L)),L-(r.n+r.m+2)-1);
    if(m<1||2**m>L)throw Error("bad suffix length");
    const p=x.slice(0,-m),tbl=[];
    for(let k=0;k<2**m;k++){
      tbl.push(label(p+k.toString(2).padStart(m,"0")));
      count.virtual_completions++;
    }
    const prefix=m===1?0:parseInt(x.slice(-m,-1),2);
    const last=+x[x.length-1],two=[tbl[2*prefix],tbl[2*prefix+1]];
    if(two[last]!==label(x))throw Error("speculative lookup failed");
    count.suffix_checks++;
    return m;
  }
  const samples=[];
  for(const n of [3,4,5]){
    for(const m of [1,2,3,4,6]){
      for(let q=0;q<3;q++){
        const clauses=[];
        for(let j=0;j<m;j++){
          const vars=Array.from({length:n},(_,i)=>i);
          for(let i=n-1;i>0;i--){const k=next()%(i+1);[vars[i],vars[k]]=[vars[k],vars[i]];}
          clauses.push(vars.slice(0,3).map(v=>[v,next()&1]));
        }
        samples.push(encode(n,clauses));
      }
    }
  }
  const sourceLengths=new Set();
  for(const x of samples){
    const answer=label(x);if(answer==="MALFORMED")throw Error("source");
    const z=hardwired(x,answer,x);
    if(!z.match||z.result!==answer||z.on_match_scans!==x.length+1)throw Error("on-target");
    count.on_target++;sourceLengths.add(x.length);
    if(graphCeiling(x.length)!==x.length+1)throw Error("potential");
    suffix(x);
    for(const y of [x+"1",x.slice(0,-1),"0",x.slice(0,Math.floor(x.length/2))+"0"+x.slice(Math.floor(x.length/2)+1)]){
      const r=hardwired(x,answer,y);
      if(r.result!==label(y)||((y!==x)&&r.match))throw Error("fallback");
      count.off_target++;
    }
  }
  function force(v,b,p,q) {
    const cl=[];for(const a of [0,1])for(const c of [0,1])cl.push([[v,b],[p,a],[q,c]]);
    return cl;
  }
  const base=[...force(0,1,6,7),...force(1,0,8,9),...force(4,1,10,11),...force(5,0,12,13)];
  const yes=encode(14,[...base,[[0,0],[1,1],[4,1]]]);
  const no=encode(14,[...base,[[0,0],[1,1],[5,1]]]);
  if(yes.length!==no.length||yes.slice(0,-1)!==no.slice(0,-1)||label(yes)!=="SAT"||label(no)!=="UNSAT")throw Error("final-bit controls");
  suffix(yes);suffix(no);count.last_bit_pairs=2;
  return {status:"COMPUTATIONAL: finite semantic emulator; no TM instruction simulation",
    code:"tmr4_program_blind_ceiling004.cjs",seed:20261113,sample_sources:samples.length,
    source_lengths:[...sourceLengths].sort((a,b)=>a-b),counts:count,opposite_pair_length:yes.length,
    theorem:"For any valid x, every all-machine cost-sound common-start potential on a machine-blind MAY graph is <= |x|+1.",
    caveat:"The hardwired witness machine B_x depends on x; not one polynomial decider across all inputs."};
}
if(typeof module!=="undefined"){module.exports={audit};if(require.main===module)console.log(JSON.stringify(audit(),null,2));}
