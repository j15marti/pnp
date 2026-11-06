#!/usr/bin/env node
// LSPV-4/438: independent finite exact audit; input is full expander_deletion_raw.json.
// Requires Node.js, no NPM dependencies. This does NOT simulate an FLMV TM.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const file = process.argv[2] || 'expander_deletion_raw.json';
const data = JSON.parse(readFileSync(file,'utf8'));
let assertions=0;
const check=(b,m)=>{assertions++;if(!b)throw new Error(m)};
function forest(n,edges,deleted){
 let groups=Array.from({length:n},(_,i)=>[i]);
 for(let t=0;t<edges.length;t++){
  if(deleted.has(t))continue;
  let [u,v]=edges[t], gu=groups.findIndex(x=>x.includes(u)), gv=groups.findIndex(x=>x.includes(v));
  if(gu!==gv){groups[gu].push(...groups[gv]);groups.splice(gv,1);}
 }
 return groups;
}
function orig(n,edges,charge){
 let arr=[];
 for(let v=0;v<n;v++){
  let refs=[];
  edges.forEach(([a,b],i)=>{if(a===v||b===v)refs.push(i+1)});
  refs.sort((a,b)=>a-b);
  check(refs.length===3,'not cubic');
  for(let p=0;p<2;p++)for(let r=0;r<2;r++){
   let z=p^r^1^charge[v];
   arr.push([p?-refs[0]:refs[0],r?-refs[1]:refs[1],z?-refs[2]:refs[2]]);
  }
 }
 return arr;
}
function minExpansion(n,edges){
 let num=999,den=1;
 for(let mask=1;mask<(1<<n);mask++){
  let size=0;
  for(let i=0;i<n;i++)size+=(mask>>>i)&1;
  if(size>n/2)continue;
  let boundary=edges.reduce((s,[a,b])=>s+((((mask>>>a)&1)!==((mask>>>b)&1))?1:0),0);
  if(boundary*den<num*size){num=boundary;den=size}
 }
 return [num,den];
}
for(const r of data.records){
 const n=r.H,edges=r.edges,m=edges.length;
 check(m*2===3*n,'wrong edge count');
 const w=Math.floor(Math.log2(m)+1);
 check(r.encoded_bits===8+(n+1)+(m+1)+n+3*n*w+12*n*(w+1),'encoded size');
 const [hNum,hDen]=minExpansion(n,edges);
 check(hNum*r.expansion_den===r.expansion_num*hDen,'expansion mismatch');
 const sources=[];
 for(let z=0;z<2;z++){
  let c=Array(n).fill(0);c[0]=z;
  let arr=orig(n,edges,c);
  let sig=createHash('sha256').update(JSON.stringify(arr)).digest('hex');
  check(sig===r.charges[z].sha256,'source hash mismatch');
  sources.push(arr);
 }
 for(const row of r.by_k){
  let k=row.k;
  let totals={deletion_sets:0,branch_assignments:0,graph_parity_checks:0,giant_claim_checks:0,
   unchanged_original_clauses:0,empty_clauses:0,units:0,binaries:0,ternaries:0,
   minimum_largest_component:n,maximum_outside_largest:0};
  let recurse=(start,chosen)=>{
   if(chosen.length<k){
    for(let i=start;i<=m-(k-chosen.length);i++)recurse(i+1,[...chosen,i]);
    return;
   }
   const D=new Set(chosen), cc=forest(n,edges,D), largest=Math.max(...cc.map(x=>x.length));
   totals.deletion_sets++;
   totals.minimum_largest_component=Math.min(totals.minimum_largest_component,largest);
   totals.maximum_outside_largest=Math.max(totals.maximum_outside_largest,n-largest);
   if(3*k*hDen<hNum*n){
    check(largest*2>n,'unique giant absent');
    check((n-largest)*hNum<=k*hDen,'giant expansion inequality false');
    totals.giant_claim_checks++;
   }
   for(let mask=0;mask<2**k;mask++){
    let assigned=new Map(chosen.map((e,j)=>[e,(mask>>>j)&1]));
    let degree=Array(n).fill(0);
    for(let e of chosen){degree[edges[e][0]]++;degree[edges[e][1]]++}
    for(let z=0;z<2;z++){
     let counts=[0,0,0,0],empty=0;
     for(let cl of sources[z]){
      let sat=false,free=0;
      for(let lit of cl){
       let ei=Math.abs(lit)-1;
       if(!assigned.has(ei))free++;
       else{
        let val=assigned.get(ei);
        if((val===1&&lit>0)||(val===0&&lit<0))sat=true;
       }
      }
      if(!sat){if(free===0)empty++;else counts[free]++}
     }
     check(counts[3]===4*degree.filter(x=>x===0).length,'ternary count');
     check(counts[2]===2*degree.filter(x=>x===1).length,'binary count');
     check(counts[1]===degree.filter(x=>x===2).length,'unit count');
     check(empty<=degree.filter(x=>x===3).length,'empty count');
     let residual=Array(n).fill(0);residual[0]=z;
     for(let [ei,val] of assigned){
      residual[edges[ei][0]]^=val;
      residual[edges[ei][1]]^=val;
     }
     let parity=cc.map(comp=>comp.reduce((a,v)=>a^residual[v],0));
     check(parity.reduce((a,v)=>a^v,0)===z,'parity conservation');
     if(z===1)check(parity.includes(1),'odd UNSAT contradiction lost');
     if(empty)check(parity.includes(1),'empty row but no parity obstruction');
     totals.branch_assignments++;
     totals.graph_parity_checks+=cc.length;
     totals.unchanged_original_clauses+=counts[3];
     totals.empty_clauses+=empty;
     totals.units+=counts[1];
     totals.binaries+=counts[2];
     totals.ternaries+=counts[3];
    }
   }
  };
  recurse(0,[]);
  for(let key of Object.keys(totals))check(totals[key]===row[key],r.graph+' k='+k+' field='+key);
 }
}
let test=orig(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],[1,0,0,0]);
let a=createHash('sha256').update(JSON.stringify(test)).digest('hex');
test[0][0]*=-1;
let b=createHash('sha256').update(JSON.stringify(test)).digest('hex');
check(a!==b,'source sign mutation not detected');
console.log(JSON.stringify({status:'PASS',graphs:data.records.length,assertions,
 branches:data.records.reduce((n,r)=>n+r.by_k.reduce((s,k)=>s+k.branch_assignments,0),0)}));
