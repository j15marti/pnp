'use strict';
// LSPV-4/381: no dependencies, no free SAT oracle or new proof rules.
// Source clauses are arrays of signed nonzero integers, each width at most two.
// Run with node experiments/arc/lspv4_381_compact_source_path.js
function ok(b,m){if(!b)throw Error(m||'assertion failed')}
function norm(xs){return [...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function srccheck(f){
  if(!Array.isArray(f))throw Error('source missing');
  for(const c of f){
    if(!Array.isArray(c)||c.length>2||c.some(x=>!Number.isSafeInteger(x)||x===0))
      throw Error('malformed signed <=2 CNF');
  }
}
function calc(f,proof){
  srccheck(f);const d=new Map(f.map((c,i)=>['S'+i,norm(c)]));
  for(let i=0;i<proof.length;i++){
    const t=proof[i],a=d.get(t.left),b=d.get(t.right),p=t.pivot;
    if(!a||!b||!Number.isInteger(p)||!p||!a.includes(p)||!b.includes(-p))
       throw Error('forged proof dependency/pivot');
    const out=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
    if(JSON.stringify(out)!==JSON.stringify(t.clause))throw Error('invalid resolvent');
    d.set('D'+i,out);
  }
  return proof.length?d.get('D'+(proof.length-1)).length===0:f.some(c=>c.length===0);
}
function solve(f){
  srccheck(f);
  const ids=[...new Set(f.flat().map(Math.abs))].sort((a,b)=>a-b),v=ids.length;
  if(f.some(c=>!c.length))return {status:'UNSAT',proof:[],v};
  const g=new Map();
  for(const a of ids){g.set(a,[]);g.set(-a,[]);}
  for(let i=0;i<f.length;i++){
    const c=norm(f[i]);if(c.length===1){g.get(-c[0]).push([c[0],i]);continue}
    if(c.length===2&&c[0]!==-c[1]){
      g.get(-c[0]).push([c[1],i]);g.get(-c[1]).push([c[0],i]);
    }
  }
  function path(s,t){
    const seen=new Set([s]),parent=new Map(),queue=[s];
    for(let k=0;k<queue.length;k++){
      const u=queue[k];if(u===t)break;
      for(const [w,j] of g.get(u)){if(!seen.has(w)){
        seen.add(w);parent.set(w,[u,j]);queue.push(w);
      }}
    }
    if(!seen.has(t))return null;
    const result=[];let w=t;
    while(w!==s){const [u,j]=parent.get(w);result.push([u,w,j]);w=u;}
    return result.reverse();
  }
  let witness=null;
  for(const x of ids){const a=path(x,-x),b=path(-x,x);if(a&&b){witness=[x,a,b];break;}}
  if(!witness)return {status:'SAT',v,proof:null};
  const [x,p1,p2]=witness,proof=[];
  function derive(edges,start){
    let ref='S'+edges[0][2];
    for(const [u,w,j] of edges.slice(1)){
      let z=ref[0]==='S'?norm(f[Number(ref.slice(1))]):proof[Number(ref.slice(1))].clause;
      if(z.length===1&&z[0]===-start)break; // early-unit repair
      const a=norm(f[j]);ok(z.includes(u)&&a.includes(-u),'illegal pivot');
      const next=norm([...z.filter(t=>t!==u),...a.filter(t=>t!==-u)]);
      proof.push({left:ref,right:'S'+j,pivot:u,clause:next});
      ref='D'+(proof.length-1);
    }
    const final=ref[0]==='S'?norm(f[Number(ref.slice(1))]):proof[Number(ref.slice(1))].clause;
    ok(JSON.stringify(final)===JSON.stringify([-start]),'unit result');
    return ref;
  }
  const neg=derive(p1,x),pos=derive(p2,-x);
  proof.push({left:pos,right:neg,pivot:x,clause:[]});
  ok(calc(f,proof),'certificate rejected');
  ok(proof.length<=4*v-3,'bound exceeded');
  return {status:'UNSAT',v,proof,paths:[p1.length,p2.length]};
}
function model(f){
  const ids=[...new Set(f.flat().map(Math.abs))],n=ids.length;
  if(n>18)throw Error('finite oracle only');
  for(let z=0;z<(1<<n);z++){
    const a=new Map(ids.map((x,j)=>[x,!!(z&(1<<j))]));
    if(f.every(c=>c.some(l=>a.get(Math.abs(l))===(l>0))))return a;
  }
  return null;
}
function run(){
 let count=0,sat=0,unsat=0,checks=0;
 function test(f){const t=solve(f),m=model(f);
   ok((m!==null)===(t.status==='SAT'),'label error');checks++;
   if(t.status==='UNSAT'){ok(calc(f,t.proof),'unsound');checks++;unsat++}
   else sat++;
   count++;return t;
 }
 for(let n=1;n<=2;n++){
  const ls=Array.from({length:n},(_,i)=>[i+1,-(i+1)]).flat(),base=ls.map(x=>[x]);
  for(let i=0;i<ls.length;i++)for(let j=i+1;j<ls.length;j++)
    if(Math.abs(ls[i])!==Math.abs(ls[j]))base.push([ls[i],ls[j]]);
  for(let mask=0;mask<2**base.length;mask++)test(base.filter((_,i)=>(mask&(1<<i))!==0));
 }
 for(let m=2;m<=12;m++){
   const h=[[1]];for(let i=1;i<m-1;i++)h.push([-i,i+1]);
   h.push([-(m-1)]);const t=test(h);
   ok(t.proof.length===m-1,'Horn exact upper');checks++;
   for(let j=0;j<h.length;j++){ok(model(h.filter((_,k)=>k!==j))!==null,'source essentiality');checks++}
 }
 for(const bad of [null,{},[[0]],[[1,2,3]],[[0,1]],[['x']],[[1.5]],[[Infinity]]]){
   let rejected=false;try{srccheck(bad)}catch(e){rejected=true}
   ok(rejected,'malformed accepted');checks++;
 }
 const sparse=solve([[1],[-1]]);ok(sparse.v===1&&sparse.proof.length===1,'sparse ID');
 const empty=solve([[]]);ok(empty.proof.length===0,'empty source');
 const t=solve([[1],[-1]]);
 for(const key of ['pivot','left']){
   const f=JSON.parse(JSON.stringify(t.proof));f[0][key]=key==='pivot'?100:'S99999';
   let rejected=false;try{calc([[1],[-1]],f)}catch(e){rejected=true}
   ok(rejected,'forgery accepted');checks++;
 }
 return {status:'PASS',cases:count,SAT:sat,UNSAT:unsat,assertions:checks,
        horn_exact_through:12,corrupted_rejected:2,malformed_rejected:8};
}
const result=run();
if(typeof console!=='undefined')console.log(JSON.stringify(result));
