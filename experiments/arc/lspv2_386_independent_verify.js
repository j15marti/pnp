'use strict';
// Independently written strict-Resolution / conservative-AND2 checker.
// Usage: node independent_verify.js <k4_certificate.json> [others...]
const fs=require('fs'),crypto=require('crypto'),assert=require('assert');
let tests=0;function check(b,msg){tests++;if(!b)throw new Error(msg||('check '+tests))}
function key(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function clean(c){if(!Array.isArray(c)||c.some(x=>!Number.isSafeInteger(x)||x===0))return false;let q=new Set(c);return !c.some(x=>q.has(-x))&&JSON.stringify(c)===JSON.stringify(key(c))}
function forbidden(xs,bits){return key(xs.map((x,i)=>bits[i]?-x:x))}
function ground_source(h,edges,charges,guard){
 let occ=Array.from({length:h},()=>[]);edges.forEach(([u,v],i)=>{occ[u].push(i+1);occ[v].push(i+1)});
 let rows=new Map();for(let v=0;v<h;v++){
  check(occ[v].length===3,'not cubic');let keys=[];
  for(let x=0;x<8;x++){
   let bits=[x&1,(x>>1)&1,(x>>2)&1];
   if(bits.reduce((a,b)=>a+b,0)%2 !== charges[v])keys.push(JSON.stringify(key([...forbidden(occ[v],bits),-guard])));
  }
  rows.set(v,new Set(keys));
 }
 return rows;
}
function views(z,a,b){return [[-z,a],[-z,b],[z,-a,-b]].map(key).filter(c=>!c.some(x=>c.includes(-x)))}
function checkProof(dat,{control=true}={}){
 check(dat&&dat.spec&&dat.records&&dat.gate_defs&&dat.summary,'missing fields');
 const {h,edges,charge,guard}=dat.spec;check(Number.isInteger(h)&&h>=4&&h%2===0,'bad h');
 check(Array.isArray(edges)&&edges.length===3*h/2,'edges');
 check(Array.isArray(charge)&&charge.length===h&&charge.every(x=>x===0||x===1),'charge');
 check(charge.reduce((a,b)=>a^b,0)===1,'not odd');
 const es=new Set();edges.forEach(([u,v],i)=>{check(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v<h&&u<v,'edge');check(!es.has(u+':'+v),'duplicate edge');es.add(u+':'+v)});
 check(Number.isInteger(guard)&&guard>edges.length,'bad guard');
 const expected=ground_source(h,edges,charge,guard);
 const defs=new Map();const gids=new Map();
 for(const tuple of dat.gate_defs){
  check(Array.isArray(tuple)&&tuple.length===4,'gate spec');const [id,z,a,b]=tuple;
  check([id,z,a,b].every(Number.isSafeInteger),'gate integer');
  check(id>=0&&z>edges.length&&z!==guard&&!defs.has(z)&&!gids.has(id),'gate fresh');
  for(let x of [a,b]){check(x!==0&&Math.abs(x)!==guard,'gate guard');check(Math.abs(x)<=edges.length||defs.has(Math.abs(x)),'gate used before declared')}
  defs.set(z,{id,z,a,b,cs:new Set(views(z,a,b).map(JSON.stringify))});gids.set(id,z);
 }
 const known=[];let nsrc=0,nres=0,ndefviews=0;const seenSources=new Set();
 for(let i=0;i<dat.records.length;i++){
  let r=dat.records[i];check(r&&['SOURCE','DEF','RES'].includes(r.kind)&&clean(r.c),'record kind or clause at '+i);
  check(Array.isArray(r.parents)&&r.parents.every(j=>Number.isInteger(j)&&j>=0&&j<i),'bad parents '+i);
  const clause=JSON.stringify(r.c);
  if(r.kind==='SOURCE'){
   nsrc++;check(r.parents.length===0,'source parent');
   if(r.source===-1)check(clause===JSON.stringify([guard]),'guard source');
   else check(expected.has(r.source)&&expected.get(r.source).has(clause),'wrong source '+i);
   const srcKey=String(r.source)+':'+clause;check(!seenSources.has(srcKey),'duplicate source');seenSources.add(srcKey);
  }else if(r.kind==='DEF'){
   ndefviews++;check(r.parents.length===0,'DEF view parent');
   check(gids.has(r.gate),'undefined gate');
   const gd=defs.get(gids.get(r.gate));check(gd.cs.has(clause),'not true gate view '+i);
  }else{
   nres++;check(r.parents.length===2,'RES arity');let [A,B]=r.parents.map(j=>known[j]);const p=r.pivot;
   check(Number.isInteger(p)&&p!==0,'bad pivot');check(A.includes(p)&&B.includes(-p),'bad pivot signs '+i);
   const resolvent=key([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
   check(clean(resolvent),'taut resolvent '+i);check(JSON.stringify(resolvent)===clause,'wrong resolvent '+i);
  }
  for(const x of r.c){check(Math.abs(x)<=edges.length||Math.abs(x)===guard||defs.has(Math.abs(x)),'undefined auxiliary literal '+i)}
  known.push(r.c);
 }
 check(known.length>0&&known[known.length-1].length===0,'not refutation');
 check(dat.summary.source===nsrc,'source count');check(dat.summary.def_views===ndefviews,'gate clause count');
 check(dat.summary.resolution===nres,'RES count');check(dat.summary.paid_gates===defs.size,'gate paid count');
 check(dat.summary.paid_total===nres+defs.size,'paid cost');
 check(dat.summary.live_records===known.length,'record count');
 check(nsrc===4*h+1,'missing original clauses');
 for(const [v,cs] of expected)for(const c of cs)check(seenSources.has(v+':'+c),'missing source clause '+v);
 check(seenSources.has('-1:'+JSON.stringify([guard])),'missing guard unit');
 if(control){
  let visited=0,odd=0,even=0,guardSat=0;
  if(edges.length<=12){
   for(let m=0;m<2**edges.length;m++){
    let xor=Array(h).fill(0);edges.forEach(([u,v],i)=>{let bit=(m>>i)&1;xor[u]^=bit;xor[v]^=bit});
    let oddok=xor.every((z,i)=>z===charge[i]);
    let evenCharge=[0,...charge.slice(1)];
    let evenok=xor.every((z,i)=>z===evenCharge[i]);
    odd+=Number(oddok);even+=Number(evenok);guardSat++;visited++;
   }
   check(odd===0,'odd SAT');check(even===2**(edges.length-h+1),'even mismatch');
  }
  return {paid:nres+defs.size,def:defs.size,res:nres,records:known.length,sources:nsrc,sourceBits:edges.length,oddModels:odd,evenModels:even,guardFalseModels:guardSat};
 }
 return {paid:nres+defs.size};
}
function corrupt(d,mutator){let cp=structuredClone(d);mutator(cp);try{checkProof(cp,{control:false});return false}catch(e){return true}}
for(const f of process.argv.slice(2)){
 let content=fs.readFileSync(f);let d=JSON.parse(content);
 const outcome=checkProof(d), mutations=[
  o=>{o.records.at(-1).pivot=999999},
  o=>{o.records.at(-1).c=[123456]},
  o=>{o.records[0].c=[-o.spec.guard]},
  o=>{o.gate_defs.shift()},
  o=>{o.records.at(-1).parents[0]=o.records.length+1},
  o=>{o.summary.paid_total--},
  o=>{o.spec.charge[0]^=1},
  o=>{o.records.at(-1).kind='SOURCE'},
  o=>{o.spec.edges[0]=o.spec.edges[1].slice()},
  o=>{o.records[0].c=[0]},
  o=>{o.spec.guard=o.spec.edges.length}
 ];
 for(const change of mutations)check(corrupt(d,change),'accepted a corrupted proof');
 console.log(JSON.stringify({file:f,sha256:crypto.createHash('sha256').update(content).digest('hex'),...outcome,negativeTests:mutations.length,assertions:tests}));
}
