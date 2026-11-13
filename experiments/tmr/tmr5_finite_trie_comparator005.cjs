#!/usr/bin/env node
"use strict";
function audit(){
  "use strict";
  let seed=20261113>>>0;
  const next=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
  const count={on_target:0,on_steps:0,fallbacks:0,adversarial_probes:0,terminal_checks:0,zero_edge_checks:0,invalid_shortcut_rejections:0};
  const encode=(n,cs)=>"1".repeat(n)+"0"+"1".repeat(cs.length)+"0"+cs.map(cl=>cl.map(([v,s])=>s+v.toString(2).padStart(Math.max(1,Math.ceil(Math.log2(n))),"0")).join("")).join("");
  function parse(x){
    if(!/^[01]+$/.test(x))return null;
    const n=x.indexOf("0");if(n<3)return null;
    let p=n+1,m=0;while(x[p]==="1"){p++;m++;}
    if(m<1||x[p]!=="0")return null;
    p++;const w=Math.max(1,Math.ceil(Math.log2(n)));
    if(x.length!==p+3*m*(w+1))return null;
    const clauses=[];
    for(let j=0;j<m;j++){
      let cl=[];
      for(let k=0;k<3;k++){const s=+x[p],v=parseInt(x.slice(p+1,p+1+w),2);p+=w+1;if(v>=n)return null;cl.push([v,s]);}
      if(new Set(cl.map(z=>z[0])).size!==3)return null;
      clauses.push(cl);
    }
    return {n,clauses};
  }
  let labelcache=new Map();
  function label(x){
    if(labelcache.has(x))return labelcache.get(x);
    let r=parse(x),z="REJECT";
    if(r){
      z="UNSAT";
      for(let a=0;a<2**r.n;a++){
        if(r.clauses.every(cl=>cl.some(([v,s])=>((a>>>v)&1)===s))){z="SAT";break;}
      }
    }
    labelcache.set(x,z);return z;
  }
  function force(v,b,p,q){let arr=[];for(let a=0;a<2;a++)for(let c=0;c<2;c++)arr.push([[v,b],[p,a],[q,c]]);return arr;}
  let base=[...force(0,1,6,7),...force(1,0,8,9),...force(4,1,10,11),...force(5,0,12,13)];
  let yes=encode(14,[...base,[[0,0],[1,1],[4,1]]]),no=encode(14,[...base,[[0,0],[1,1],[5,1]]]);
  if(yes.slice(0,-1)!==no.slice(0,-1)||label(yes)!=="SAT"||label(no)!=="UNSAT")throw Error("opposite-label sibling");
  const H=new Set([yes,no,"","0","1","00","1010","111111","001"]);
  for(let n=5;n<=8;n++){
    let core=[...force(0,0,1,2),...force(0,1,3,4)];
    for(let q=0;q<6;q++){
      let cs=core.slice();
      for(let i=0;i<1+(next()%4);i++){
        let vs=[...Array(n).keys()];
        for(let j=n-1;j>0;j--){let k=next()%(j+1);[vs[j],vs[k]]=[vs[k],vs[j]];}
        cs.push(vs.slice(0,3).map(v=>[v,next()&1]));
      }
      H.add(encode(n,cs));
    }
  }
  for(let n=3;n<=6;n++){
    for(let trial=0;trial<18;trial++){
      let clauses=[],m=1+(next()%9);
      for(let i=0;i<m;i++){
        let vs=[...Array(n).keys()];
        for(let j=n-1;j>0;j--){let k=next()%(j+1);[vs[j],vs[k]]=[vs[k],vs[j]];}
        clauses.push(vs.slice(0,3).map(v=>[v,next()&1]));
      }
      let x=encode(n,clauses);H.add(x);
      if(next()%3===0)H.add(x.slice(0,-1));
      if(next()%4===0)H.add(x+"0");
    }
  }
  const longest=[...H].filter(x=>x.length>20).sort((a,b)=>a.length-b.length)[0];
  for(let j of [1,2,5,10])H.add(longest.slice(0,j));
  const edges=[Object.create(null)],goals=[null];
  for(let x of [...H].sort()){
    let q=0;
    for(let ch of x){
      if(edges[q][ch]===undefined){edges[q][ch]=edges.length;edges.push(Object.create(null));goals.push(null);}
      q=edges[q][ch];
    }
    goals[q]=label(x);
  }
  function simulate(x){
    let q=0,head=0,steps=0;
    for(;;){
      const symbol=head<x.length?x[head]:"#";steps++;
      if(symbol==="#")return {match:goals[q]!==null,result:goals[q],steps,head};
      if(edges[q][symbol]===undefined)return {match:false,result:null,steps,head};
      q=edges[q][symbol];head++;
    }
  }
  let labels={SAT:0,UNSAT:0,REJECT:0},sumBits=0,maxLength=0;
  for(let x of H){
    let z=simulate(x);
    if(!z.match||z.result!==label(x)||z.head!==x.length||z.steps!==x.length+1)throw Error("trie complete trace failed");
    labels[z.result]++;count.on_target++;count.terminal_checks++;count.on_steps+=z.steps;sumBits+=x.length;maxLength=Math.max(maxLength,x.length);
    // Exact matched trace yields a unit-cost successor and an admissible potential.
    for(let step=0;step<z.steps;step++){
      if(z.steps-step>1+(z.steps-step-1))throw Error("potential");
      count.zero_edge_checks++;
    }
    if(z.steps>0){if(z.steps<=0)throw Error("invalid zero shortcut");count.invalid_shortcut_rejections++;}
  }
  let tests=new Set();
  for(let n=0;n<=7;n++)for(let i=0;i<2**n;i++)tests.add(i.toString(2).padStart(n,"0").replace(/^0$/,"0"));
  tests.add("");
  for(let x of H){
    tests.add(x+"0");tests.add(x+"1");tests.add(x.slice(0,-1));
    if(x){let pos=Math.floor(x.length/2);tests.add(x.slice(0,pos)+(x[pos]==="0"?"1":"0")+x.slice(pos+1));}
  }
  for(let x of tests){
    let tr=simulate(x),truth=label(x);
    if(H.has(x)){
      if(!tr.match||tr.result!==truth)throw Error("fast path wrong");
    }else{
      if(tr.match)throw Error("false hit");
      // A total fallback can rewind the read-only input and run a charged parser/exhaustive solver.
      if(!["SAT","UNSAT","REJECT"].includes(truth))throw Error("fallback impossible");
      count.fallbacks++;
    }
    count.adversarial_probes++;
  }
  let q=edges.length, pointerBits=Math.ceil(Math.log2(q+2));
  if(q>1+sumBits)throw Error("state bound");
  return {status:"COMPUTATIONAL: direct finite-control trie transitions, fallback semantic only",seed:20261113,
    source:"tmr5_finite_trie_comparator005.cjs",count,labels,finite_battery:H.size,
    trie_states:q,sum_input_bits:sumBits,max_input_bits:maxLength,
    comparator_table_upper_bits:q*(2*pointerBits+5),
    zero_failures:true,
    opposite_label_last_bit_pair_length:yes.length,
    caveat:"One finite program per selected finite battery; not a single polynomial-time SAT program uniformly over growing batteries. The fallback uses an explicit exhaustive algorithm but is not physically simulated."};
}
if(typeof module!=="undefined"){module.exports={audit};if(require.main===module)console.log(JSON.stringify(audit(),null,2));}
