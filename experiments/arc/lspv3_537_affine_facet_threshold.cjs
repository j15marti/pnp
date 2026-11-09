'use strict';
// LSPV-3/537 independent parity-facet affine threshold replay.
// Declared source-labelled AND3 fragment only; NOT historical native checker.
const assert=require('assert');
const bits=x=>{let n=0;while(x){n+=x&1;x>>>=1}return n};
const parity=x=>bits(x)&1;
function dim(vs){if(!vs.length)return -1;const bs=new Map();for(let x of vs){x^=vs[0];while(x){const p=31-Math.clz32(x);if(!bs.has(p)){bs.set(p,x);break}x^=bs.get(p)}}return bs.size}
const facet=(v,k)=>Array.from({length:k},(_,i)=>v&(1<<i)?-(i+1):i+1);
const sat=(C,x)=>C.some(l=>Boolean(x&(1<<(Math.abs(l)-1)))===(l>0));
let checks=0;const ck=(v,m)=>{assert.ok(v,m);checks++};let stats={};let cases=0;
for(let k=2;k<=5;k++){
 let count=0,full=0;
 for(let charge of [0,1]){
  const forbidden=Array.from({length:1<<k},(_,i)=>i).filter(i=>parity(i)!==charge);
  const clauses=forbidden.map(v=>facet(v,k));
  for(let i=0;i<forbidden.length;i++)for(let x=0;x<(1<<k);x++)ck(sat(clauses[i],x)===(x!==forbidden[i]),'facet truth');
  for(let mask=0;mask<(2**forbidden.length);mask++){
   const models=[];
   for(let x=0;x<(1<<k);x++)if(clauses.every((C,i)=>!(mask&(1<<i))||sat(C,x)))models.push(x);
   const isFull=mask===(2**forbidden.length)-1;
   ck(dim(models)===(isFull?k-1:k),'affine hull threshold');
   count++;if(isFull)full++;
  }
 }
 stats[k]={facet_count:1<<(k-1),cases:count,full_affine_exception_cases:full,proper_subset_cases:count-full};cases+=count;
}
let certificates=[],rejected=0;
for(let charge of [0,1]){
 const forbidden=Array.from({length:8},(_,i)=>i).filter(x=>parity(x)!==charge);
 const src=new Map(forbidden.map(v=>['S'+v,facet(v,3)]));
 const truth=new Map([...src].map(([id,C])=>[id,Array.from({length:8},(_,a)=>sat(C,a))]));
 const derived=new Map();
 function add(id,p,q,annotation){
  if(src.has(id)||derived.has(id)||(!truth.has(p)&&!derived.has(p))||(!truth.has(q)&&!derived.has(q)))throw Error('invalid identifier/parent');
  const u=truth.get(p)||derived.get(p).truth,v=truth.get(q)||derived.get(q).truth;
  const t=u.map((b,i)=>b&&v[i]);
  if(annotation!==undefined&&t.some((b,i)=>b!==(parity(i)===annotation)))throw Error('bad affine annotation');
  const support=[...(src.has(p)?[p]:derived.get(p).support),...(src.has(q)?[q]:derived.get(q).support)];
  derived.set(id,{truth:t,support:[...new Set(support)].sort()});
 }
 const ids=[...src.keys()];add('a',ids[0],ids[1]);add('b',ids[2],ids[3]);add('c','a','b',charge);
 ck(derived.get('c').support.length===4,'full source ancestry');
 ck(derived.get('c').truth.filter(Boolean).length===4,'parity valuation count');
 for(let omit of ids){const present=ids.filter(x=>x!==omit);const models=Array.from({length:8},(_,i)=>i).filter(x=>present.every(id=>sat(src.get(id),x)));ck(dim(models)===3,'missing facet affine hull')}
 for(let bad of [()=>add('c',ids[0],ids[1]),()=>add('v','NONEXISTENT',ids[1]),()=>add('v',ids[0],ids[1],1-charge)]){
  try{bad();throw Error('accepted invalid packet')}catch(e){if(e.message==='accepted invalid packet')throw e;rejected++}
 }
 certificates.push({charge,paid_and3_nodes:3,source_clauses:4});
}
const result={status:'PROVED/RESTRICTED symbolic + COMPUTATIONAL replay',method:'full subset enumeration and declared three-input AND3 semantics',k_range:[2,5],by_width:stats,subset_configuration_checks:cases,source_three_factor_certificates:certificates,negative_controls_rejected:rejected,total_assertion_events:checks,seed:'none',environment:{node:process.version}};
console.log(JSON.stringify(result,null,2));