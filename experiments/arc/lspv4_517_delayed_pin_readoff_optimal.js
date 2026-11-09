// LSPV-4/517: exact zero-path read scheduling on original K4 selector.
"use strict";
function verify517() {
 let checks=0, patterns=0;
 function mk(k,d) {
  const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const core=[];let n=6,clauses=[], gs=[];
  for(let v=0;v<4;v++) {
    const es=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
    for(let p=0;p<8;p++) {const b=[p&1,(p>>1)&1,(p>>2)&1];
      if((b[0]^b[1]^b[2])!==Number(v===0))
        core.push(es.map((x,i)=>b[i]?-x:x));}
  }
  for(let j=0;j<k;j++) {let g=++n,a=++n,b=++n; gs.push(g);
    let s=(d&(1<<j))?g:-g;
    clauses.push([s,a,b],[s,a,-b],[s,-a,b],[s,-a,-b]);}
  let g=gs[0];
  for(let j=1;j<k;j++) {let x=gs[j],z=++n,u=++n,v=++n;
    clauses.push([-g,z,u],[-g,z,-u],[-x,z,v],[-x,z,-v],[g,x,-z]);g=z;}
  for(let [a,b,c] of core) {let h=++n;clauses.push([g,a,h],[-h,b,c]);}
  if(n!==19+6*k || clauses.length!==27+9*k ||
      clauses.some(c=>new Set(c.map(Math.abs)).size!==3)) throw Error("source shape");
  let w=Math.floor(Math.log2(n))+1;
  let bits='10110110'+'1'.repeat(n)+'0';
  for(let c of clauses) for(let x of c)
    bits+=Math.abs(x).toString(2).padStart(w,'0')+(x<0?'1':'0');
  return bits+'01';
 }
 function optimum(k) {
   const memo=new Map();let states=0;
   function dp(c) {
     let key=c.join(',');
     if(memo.has(key))return memo.get(key);
     states++;
     if(c.every(x=>x===4)){memo.set(key,0);return 0;}
     const live=2**c.filter(x=>x===0).length;
     let best=Infinity;
     for(let j=0;j<k;j++)if(c[j]<4) {
       const n=c.slice();n[j]++;
       best=Math.min(best,live+dp(n));
     }
     memo.set(key,best);return best;
   }
   return {min:dp(Array(k).fill(0)),states};
 }
 function opt(tag) {
   const k=tag.length,obs=[];
   for(let j=0;j<k;j++){obs.push([j,0,tag[j][0]]);if(tag[j][0])return ['SAT',obs];}
   for(let j=0;j<k;j++)for(let t=1;t<4;t++){
      obs.push([j,t,tag[j][t]]);if(tag[j][t])return ['SAT',obs];}
   return ['UNSAT',obs];
 }
 function old(tag) {
   const obs=[];
   for(let j=0;j<tag.length;j++)for(let t=0;t<4;t++){
      obs.push([j,t,tag[j][t]]);
      if(tag[j][t])return ['SAT',obs];}
   return ['UNSAT',obs];
 }
 // Every originally proper ternary four-facet pin with arbitrary tag signs.
 for(let mask=0;mask<16;mask++)
 for(let g=0;g<2;g++) {
   let feasible=false;
   for(let a=0;a<2;a++)for(let b=0;b<2;b++){
      const facets=[a||b,a||!b,!a||b,!a||!b];
      if(facets.every((v,i)=>((((mask>>i)&1)?g:!g)||v)))feasible=true;
   }
   if(feasible!==(g?mask!==0:mask!==15))throw Error("pin semantic");
   checks++;
 }
 const rows=[];
 for(let k=1;k<=10;k++){
    const base=mk(k,0), positions=[];
    for(let j=0;j<k;j++){
      const b=mk(k,1<<j);
      const diff=[];for(let i=0;i<base.length;i++)if(base[i]!==b[i])diff.push(i);
      if(diff.length!==4)throw Error("tag fields");
      positions.push(diff);
    }
    if(new Set(positions.flat()).size!==4*k)throw Error("tag overlap");
    let count=0,prev=0, classes=new Set();
    for(let d=0;d<2**k;d++) {
      const b=mk(k,d);
      const tags=positions.map(group=>group.map(i=>b[i]==='0'?1:0));
      let [label,trace]=opt(tags),[label2,trace2]=old(tags);
      if(label!==(d===0?'UNSAT':'SAT')||label!==label2)throw Error("classification");
      count+=trace.length;prev+=trace2.length;classes.add(JSON.stringify([label,trace]));
      checks+=2;
    }
    let q=2**k;
    if(count!==2*q-2+3*k||prev!==5*q-5||classes.size!==k+1)throw Error("aggregate");
    rows.push({k,q,source_bits:base.length,improved_reads:count,prior_reads:prev,
      full_scan_reads:4*k*q,trace_classes:classes.size});
    checks+=4;
 }
 for(let k=1;k<=3;k++){
   for(let m=0;m<2**(4*k);m++){
     const tag=Array.from({length:k},(_,j)=>Array.from({length:4},(_,t)=>(m>>(4*j+t))&1));
     if(opt(tag)[0] !== (m?'SAT':'UNSAT'))throw Error("mixed-tag soundness");
     patterns++;checks++;
   }
 }
 const dp=[];
 for(let k=1;k<=6;k++){
   const x=optimum(k),q=2**k;
   if(x.min!==2*q-2+3*k)throw Error("DP optimum");
   dp.push({k,...x});checks++;
 }
 return {status:'PASS',checks,mixed_tag_patterns:patterns,rows,dp,
 proof_scope:'Exact optimal total tag-bit reads for all-input-sound OR classifier on signed-template inputs; source authentication and all FLMV resource costs additional'};
}
if(typeof module!=='undefined' && require.main===module) console.log(JSON.stringify(verify517(),null,2));
