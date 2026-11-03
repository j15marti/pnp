#!/usr/bin/env node
/* LSPV2-369 independently authored Res(+) checker.
 * Finite exhaustive semantics on <=12 original variables only.
 * This does NOT verify Braun's asymptotic theorem.
 */
'use strict';
const fs=require('fs');
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'certificates.json','utf8'));
let checks=0;function ok(v,m){checks++;if(!v)throw Error(m)}
function eq(e,n){
 ok(Array.isArray(e)&&e.length===2&&e.every(Number.isInteger),'eq syntax');
 ok(e[0]>=0&&e[0]<(1<<n)&&(e[1]===0||e[1]===1),'eq range');
 return e;
}
function clause(c,n){ok(Array.isArray(c)&&c.length<=20,'clause');return c.map(e=>eq(e,n))}
function key(e){return e[0]+':'+e[1]}
function sig(c){return [...new Set(c.map(key))].sort().join('|')}
function eTrue(e,a){let x=e[0]&a,p=0;while(x){p^=1;x&=x-1}return p===e[1]}
function cTrue(c,a){return c.some(e=>eTrue(e,a))}
function implies(a,b,n){for(let v=0;v<(1<<n);v++)if(cTrue(a,v)&&!cTrue(b,v))return false;return true}
function resolve(a,b,p){
 let i=a.findIndex(e=>key(e)===key(p));
 let j=b.findIndex(e=>key(e)===key([p[0],1-p[1]]));
 if(i<0||j<0)throw Error('cut missing pivot');
 return a.filter((_,k)=>k!==i).concat(b.filter((_,k)=>k!==j));
}
function graph(name){
 ok(name==='K4'||name==='K33','graph');
 let h=name==='K4'?4:6,edges=[];
 if(h===4)for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
 else for(let i=0;i<3;i++)for(let j=3;j<6;j++)edges.push([i,j]);
 return {h,edges};
}
function sources(c,charge){
 const {h,edges}=graph(c.name),inc=Array.from({length:h},()=>[]);
 ok(c.nvars===edges.length&&c.vertices===h,'dimension');
 ok(JSON.stringify(c.edges)===JSON.stringify(edges),'edge list');
 edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});
 let cs=[];
 for(let v=0;v<h;v++){
  ok(inc[v].length===3,'cubic');
  for(let z=0;z<8;z++){
   const bs=[(z>>2)&1,(z>>1)&1,z&1];
   if((bs[0]^bs[1]^bs[2])!==charge[v])
    cs.push(bs.map((b,j)=>[1<<inc[v][j],1-b]));
  }
 }
 return cs;
}
function modelCount(cs,n){
 let count=0;for(let a=0;a<(1<<n);a++)if(cs.every(c=>cTrue(c,a)))count++;
 return count;
}
function check(c){
 const n=c.nvars;ok(n>0&&n<=12,'bounded independent verifier');
 ok(JSON.stringify(c.charge)===JSON.stringify([1,...Array(c.vertices-1).fill(0)]),'odd charge');
 const expected=sources(c,c.charge),auth=new Set(expected.map(sig));
 ok(c.source_clauses.length===expected.length,'source list length');
 let seen=new Set(),lines=[],paid=0;
 c.proof.forEach((rec,i)=>{
  const out=clause(rec.clause,n);
  if(rec.op==='src'){
   ok(auth.has(sig(out))&&!seen.has(sig(out)),'bad or duplicate source');
   seen.add(sig(out));
  } else if(rec.op==='weak'){
   ok(Number.isInteger(rec.parent)&&rec.parent>=0&&rec.parent<i,'bad weak parent');
   ok(implies(lines[rec.parent],out,n),'unsound semantic weakening');paid++;
  } else if(rec.op==='cut'){
   ok(Array.isArray(rec.parents)&&rec.parents.length===2&&
      rec.parents.every(p=>Number.isInteger(p)&&p>=0&&p<i),'bad cut parents');
   const p=eq(rec.pivot,n);
   ok(sig(resolve(lines[rec.parents[0]],lines[rec.parents[1]],p))===sig(out),'bad affine resolution');
   paid++;
  } else throw Error('invalid operation');
  lines.push(out);
 });
 ok(seen.size===auth.size,'missing originals');
 ok(paid===c.nodes&&expected.length===c.source_count,'node/axiom counts');
 ok(lines.length>0&&lines.at(-1).length===0,'missing contradiction');
 ok(modelCount(expected,n)===0,'odd label');
 const even=sources(c,Array(c.vertices).fill(0));
 const models=modelCount(even,n);ok(models>0,'even label');
 return {name:c.name,source_count:expected.length,paid_nodes:paid,even_models:models};
}
function checkBPHP(h){
 const ell=Math.ceil(Math.log2(h)),p=h+1,cs=[];
 for(let i=0;i<p;i++)for(let j=i+1;j<p;j++)for(let a=0;a<h;a++){
  let c=[];for(let t=0;t<ell;t++)c.push([1<<(i*ell+t),1-((a>>t)&1)]);
  for(let t=0;t<ell;t++)c.push([1<<(j*ell+t),1-((a>>t)&1)]);
  cs.push(c);
 }
 ok(modelCount(cs,p*ell)===0,'bit PHP UNSAT');
 return {holes:h,variables:p*ell,sources:cs.length,models:0};
}
function corrupt(c){
 for(let choice=0;choice<3;choice++){
  let z=JSON.parse(JSON.stringify(c));
  if(choice===0)z.proof.find(s=>s.op==='weak'&&s.clause.length>1).clause=[];
  if(choice===1)z.proof.find(s=>s.op==='cut').pivot=[9999,1];
  if(choice===2)z.proof[0].clause=[[0,0]];
  let rejected=false;try{check(z)}catch(_){rejected=true}
  ok(rejected,'corruption accepted');
 }
}
const results=raw.cases.map(check);
raw.cases.forEach(corrupt);
const controls=[checkBPHP(2),checkBPHP(4)];
ok(raw.cases.every(c=>c.nodes===15*c.vertices+2*(c.vertices-1)+1),'construction paid count');
console.log(JSON.stringify({status:'PASS',checks,results,controls,corrupted_rejected:raw.cases.length*3,
  scope:'finite exact line check, NOT Braun theorem nor a full mixed proof checker'},null,2));
