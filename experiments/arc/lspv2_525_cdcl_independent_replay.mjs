#!/usr/bin/env node
/* Independent Node.js verifier for LSPV-2/525.
 * Regenerates source bytes, independently classifies all finite formulas by exhaustive truth tables,
 * validates every logged RUP addition using a separate UP algorithm, and checks source hashes.
 * This is NOT an authoritative R_mix341 checker or an FLMV bit-machine benchmark.
 */
import fs from 'node:fs';
import crypto from 'node:crypto';

function assert(flag,msg){if(!flag)throw new Error(msg)}
function edges(n){let out=[];for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)if(n===4||(n===8&&[1,2,4].includes(a^b)))out.push([a,b]);return out}
function makeSource(name){
 let n=0,clauses=[];
 if(name.startsWith('horn-')){
  n=+name.slice(5);clauses=[[1]];for(let i=1;i<n;i++)clauses.push([-i,i+1]);clauses.push([-n]);
 }else if(name.startsWith('K4-charge-')||name.startsWith('Cube-charge-')){
   let h=name.startsWith('K4-')?4:8,ed=edges(h),adj=Array.from({length:h},()=>[]);
   ed.forEach(([a,b],i)=>{adj[a].push(i+1);adj[b].push(i+1)});
   n=ed.length;
   for(let vertex=0;vertex<h;vertex++){
     let arr=adj[vertex].sort((a,b)=>a-b); assert(arr.length===3,'3 regular');
     let mask=+name.split('-').at(-1);let charge=(mask>>vertex)&1;
     for(let b0=0;b0<2;b0++)for(let b1=0;b1<2;b1++)for(let b2=0;b2<2;b2++){
       let bs=[b0,b1,b2];if((b0+b1+b2)%2!==charge)clauses.push(arr.map((x,i)=>bs[i]?-x:x));
     }
   }
 }else if(name==='sat-2cnf'){n=3;clauses=[[1,2],[-1,3]]}
 else if(name==='unsat-3cnf'){
   n=3; for(let mask=0;mask<8;mask++){clauses.push([1,2,3].map((v,i)=>mask&(1<<i)?-v:v))}
 }else throw new Error('unknown original source '+name);
 return {n,clauses};
}
function encode(n,clauses){return `p cnf ${n} ${clauses.length}\n`+clauses.map(c=>c.join(' ')+' 0\n').join('')}
function satExhaust(n,clauses){
 for(let a=0;a<2**n;a++){
   if(clauses.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===1)===(l>0))))return true;
 }return false;
}
function rup(n,source,added){
 const values=Array(n+1).fill(0);
 for(const lit of added){if(!Number.isInteger(lit)||Math.abs(lit)>n||lit===0)return {ok:false,scans:0};
   const v=Math.abs(lit),sgn=lit>0?-1:1;
   if(values[v]!==0&&values[v]!==sgn)return {ok:true,scans:0};values[v]=sgn;
 }
 let scans=0;
 while(true){
   let changed=false;
   for(const clause of source){
     scans++;
     let satisfied=false,unit=0,count=0;
     for(const lit of clause){const v=values[Math.abs(lit)];if(v!==0&&v===(lit>0?1:-1)){satisfied=true;break}
       if(v===0){unit=lit;count++}}
     if(satisfied)continue;
     if(count===0)return {ok:true,scans};
     if(count===1){values[Math.abs(unit)]=unit>0?1:-1;changed=true;break}
   }
   if(!changed)return {ok:false,scans};
 }
}
function verify(raw){let checks=0,results=[];
  assert(raw.scope.includes('CDCL'), 'scope');checks++;
  let nSat=0,nUnsat=0,nontrivial=0;
  for(const r of raw.results){
    const {n,clauses}=makeSource(r.case);
    assert(n===r.variables&&clauses.length===r.clauses,'shape '+r.case);checks++;
    const text=encode(n,clauses);
    assert(crypto.createHash('sha256').update(text).digest('hex')===r.sha256,'sha '+r.case);checks++;
    const sat=satExhaust(n,clauses);assert((r.label==='SAT')===sat,'sat disagreement '+r.case);checks++;
    nSat+=+sat;nUnsat+=+(!sat);let database=clauses.map(c=>[...c]);
    for(let step=0;step<r.learned_log.length;step++){
      const c=r.learned_log[step];
      assert(new Set(c.map(x=>Math.abs(x))).size===c.length,'duplicate literal');checks++;
      const ok=rup(n,database,c);
      assert(ok.ok,'false RUP step '+r.case+'/'+step);checks++;
      database.push([...c]);
    }
    assert(r.additions===r.learned_log.length&&r.conflicts>=r.additions,'cost correspondence');checks++;
    if(!sat){assert(JSON.stringify(r.learned_log.at(-1))==='[]','no final empty');checks++;}
    else {assert(!r.learned_log.some(x=>x.length===0),'SAT learned empty');checks++;}
    if(r.additions>1)nontrivial++;
    results.push({case:r.case,policy:r.restart_every,sat,clauses:clauses.length,steps:r.additions});
  }
  // corruption controls: malicious proofs, malformed source and tampered RUP step
  const validSource=[[1,2]],n=2;
  assert(!rup(n,validSource,[]).ok,'bad empty cert');checks++;
  assert(!rup(n,validSource,[-1]).ok,'bad false unit');checks++;
  assert(rup(2,[[1],[-1]],[]).ok,'true conflict');checks++;
  assert(nUnsat>0&&nSat>0&&nontrivial>0,'coverage');checks++;
  return {checks,nSat,nUnsat,nontrivial,runs:raw.results.length,results};
}
if(import.meta.url===`file://${process.argv[1]}`){
 const input=process.argv[2];const raw=JSON.parse(fs.readFileSync(input,'utf8'));
 const result=verify(raw);console.log(JSON.stringify(result,null,2));
}
export {verify};
