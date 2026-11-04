#!/usr/bin/env node
'use strict';
/* Independently reconstructs signed source CNFs, replayed RES DAGs, witnesses. */
const fs=require('fs'), assert=require('assert');
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0;
function ok(p,msg){assert.ok(p,msg);checks++;}
function clauses(h,type) {
 if(type==='chain')return [[1],...Array.from({length:h},(_,j)=>[-(j+1),j+2]),[-h-1]];
 if(type==='cycle')return [[h+1],...Array.from({length:h},(_,j)=>[-(j+1),((j+1)%h)+1]),[-h-1]];
 throw Error('bad type');
}
function sat(c,a){return c.every(row=>row.some(l=>(l>0?a[l-1]:1-a[-l-1])===1));}
function res(a,b,p){
 if(!a.includes(p)||!b.includes(-p))throw Error('bad pivot');
 const s=new Set([...a.filter(v=>v!==p),...b.filter(v=>v!==-p)]);
 for(const x of s)if(s.has(-x))throw Error('tautology');
 return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?1:-1));
}
function validate(h,type,ns){
 const src=clauses(h,type),values=[];
 for(let j=0;j<ns.length;j++){
  const n=ns[j];
  function parent(ref){
   if(!Array.isArray(ref)||ref.length!==2)throw Error('bad ref');
   const [t,i]=ref;
   if(!Number.isInteger(i)||i<0)throw Error('bad index');
   if(t==='s'&&i<src.length)return src[i];
   if(t==='d'&&i<j)return values[i];
   throw Error('missing/forward ref');
  }
  const got=res(parent(n.parent1),parent(n.parent2),n.pivot);
  if(JSON.stringify(got)!==JSON.stringify(n.clause))throw Error('wrong resolvent');
  values.push(got);checks++;
 }
 if(JSON.stringify(values.at(-1))!=='[]')throw Error('nonempty root');
}
function assignments(n){
 return Array.from({length:1<<n},(_,mask)=>Array.from({length:n},(_,j)=>(mask>>j)&1));
}
let deletions=0,flips=0;
for(const c of data.cases){
 const h=c.h,src=clauses(h,'chain'),easy=clauses(h,'cycle');
 ok(c.vars===h+1&&c.clauses===h+2&&c.occurrences===2*h+2,'counts');
 for(let j=1;j<=h+1;j++)for(const cs of [src,easy]){
  ok(cs.flat().filter(v=>v===j).length===1,'positive count');
  ok(cs.flat().filter(v=>v===-j).length===1,'negative count');
 }
 function dimacs(cs){
  return 'p cnf '+(h+1)+' '+cs.length+'\n'+cs.map(r=>r.join(' ')+' 0\n').join('');
 }
 ok(dimacs(src).length===dimacs(easy).length&&8*dimacs(src).length===c.dimacs_bits,'bytes');
 ok(c.minima.chain===h+1&&c.minima.cycle===1,'minima statement');
 ok(c.proof_nodes.chain.length===h+1&&c.proof_nodes.cycle.length===1,'proof nodes');
 validate(h,'chain',c.proof_nodes.chain);validate(h,'cycle',c.proof_nodes.cycle);
 for(let j=0;j<src.length;j++){
  const rec=c.deleted_source_witnesses[j],a=rec.assignment;
  ok(rec.clause_index===j,'deletion ID');
  ok(!sat(src,a)&&sat(src.filter((_,i)=>i!==j),a),'deleted witness');deletions++;
  for(let k=0;k<src[j].length;k++){
   const flipped=c.flipped_sign_witnesses.find(w=>w.clause_index===j&&w.literal_index===k);
   ok(!!flipped,'flip record');
   const mod=src.map(row=>row.slice());mod[j][k]=-mod[j][k];
   ok(sat(mod,flipped.assignment),'flipped witness');flips++;
  }
 }
 for(const cs of [src,easy]){
  ok(sat(cs.slice(0,-1),Array(h+1).fill(1)),'left feasible');
  ok(!sat(cs,Array(h+1).fill(1)),'full contradiction');
 }
 if(h<=8)for(const cs of [src,easy]){
  const aa=assignments(h+1);
  ok(aa.every(a=>!sat(cs,a)),'UNSAT exact');
  ok(aa.filter(a=>sat(cs.slice(0,-1),a)).every(a=>a[h]===1),'cut image');
 }
 const invalid=JSON.parse(JSON.stringify(c.proof_nodes.chain));
 invalid[0].parent1=['d',999];
 let fail=false;try{validate(h,'chain',invalid);}catch(e){fail=true;}ok(fail,'corrupt pointer rejected');
 invalid[0].parent1=c.proof_nodes.chain[0].parent1;
 invalid[0].clause=[999];
 fail=false;try{validate(h,'chain',invalid);}catch(e){fail=true;}ok(fail,'corrupt line rejected');
}
ok(data.cases.length===8,'eight controls');
console.log(JSON.stringify({status:'PASS',independent_assertions:checks,source_deletion_witnesses:deletions,sign_flip_witnesses:flips,exact_symbolic_minima:16}));
