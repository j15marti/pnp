// LSPV-2/383: independent strict RES+paid-DEF checker. Does not import producer.
'use strict';
const fs=require('fs'),crypto=require('crypto');
const data=JSON.parse(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-04_0037_LSPV2_GUARDED_PARITY_ER383_raw.json','utf8'));
let checks=0,rejected=0;function assert(x,msg){checks++;if(!x)throw Error('Invalid at check '+checks+': '+msg);}
function canonical(xs){if(!Array.isArray(xs))return null;const S=new Set(xs);for(const x of S)if(!Number.isInteger(x)||!x||S.has(-x))return null;return [...S].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1));}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function val(l,v){const b=v[Math.abs(l)];assert(b===0||b===1,'valuation');return l<0?1-b:b;}
function prove(p){
 assert(p.charge===0||p.charge===1,'charge');const charge=p.charge,cc=p.clauses,gg=p.gates;
 const gated=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)if((x^y^z)!==charge)gated.push(canonical([x?-1:1,y?-2:2,z?-3:3,-4]));
 const expected=[[5,1,-2],[6,-1,2],[7,-5,-6],[8,-7,-3],[9,7,3],[10,-8,-9]];
 assert(gg.length===6&&cc.length>22,'missing gates or derivation');
 gg.forEach((g,i)=>assert(g.output===expected[i][0]&&eq(g.inputs,expected[i].slice(1)),'illegal gate definition'));
 const prior=[];
 for(let i=0;i<cc.length;i++){
  const o=cc[i];assert(eq(o.c,canonical(o.c)),'clause syntax');
  if(i<4)assert(o.kind==='source'&&eq(o.c,gated[i]),'source mismatch');
  else if(i<22){
   const j=Math.floor((i-4)/3),k=(i-4)%3,g=gg[j],a=g.inputs[0],b=g.inputs[1],z=g.output;
   const views=[canonical([-z,a]),canonical([-z,b]),canonical([z,-a,-b])];
   assert(o.kind==='view'&&o.gate===j&&o.view===k&&eq(o.c,views[k]),'definition view mismatch');
  }else{
   assert(o.kind==='res'&&Number.isInteger(o.pivot)&&o.pivot>0,'RES type');
   assert(Array.isArray(o.parents)&&o.parents.length===2,'RES parent arity');
   const [i0,i1]=o.parents;assert(Number.isInteger(i0)&&Number.isInteger(i1)&&0<=i0&&i0<i&&0<=i1&&i1<i&&i0!==i1,'RES parent indices');
   const [a,b]=[prior[i0],prior[i1]],pivot=o.pivot;
   assert(a.includes(pivot)&&b.includes(-pivot),'RES strict pivot');
   assert(eq(o.c,canonical([...a.filter(x=>x!==pivot),...b.filter(x=>x!==-pivot)])),'wrong resolvent');
  }
  prior.push(o.c);
 }
 const target=canonical([-4,charge===0?10:-10]);
 assert(eq(p.goal,target)&&p.goal_id>=22&&p.goal_id<cc.length&&eq(cc[p.goal_id].c,target),'wrong target pointer');
 assert(p.paid_res===cc.length-22&&p.paid_defs===6&&p.paid_total===cc.length-16,'incorrect charged cost');
 for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)for(let t=0;t<2;t++){
  const vals={1:x,2:y,3:z,4:t};for(const g of gg)vals[g.output]=val(g.inputs[0],vals)&val(g.inputs[1],vals);
  const sat=gated.every(c=>c.some(l=>val(l,vals)));
  assert(sat===(!t||(x^y^z)===charge),'wrong SAT label');
  assert(vals[10]===1-(x^y^z),'XOR output wrong');
  for(let i=4;i<22;i++)assert(cc[i].c.some(l=>val(l,vals)),'incorrect DEF semantics');
  if(sat)for(let i=22;i<cc.length;i++)assert(cc[i].c.some(l=>val(l,vals)),'RES failed semantically');
 }
 return {charge,paid_res:p.paid_res,paid_defs:p.paid_defs,paid_total:p.paid_total};
}
assert(data.id==='LSPV2-383'&&data.cases.length===2,'ledger');
const summary=data.cases.map(prove);
function hostile(mutate,label){const x=JSON.parse(JSON.stringify(data.cases[0]));mutate(x);try{prove(x);throw Error('UNREJECTED '+label);}catch(e){if(e.message.startsWith('UNREJECTED'))throw e;rejected++;}}
hostile(x=>{x.clauses[0].c=[-4,1,2,3];},'source');
hostile(x=>{x.gates[0].inputs=[1,2];},'gate');
hostile(x=>{x.clauses[4].c=[-5,-1];},'view');
hostile(x=>{x.clauses[22].pivot=999;},'pivot');
hostile(x=>{x.clauses[22].parents=[22,22];},'cyclic');
hostile(x=>{x.clauses[22].c=[1];},'resolvent');
hostile(x=>{x.goal=[-4,10,11];},'target');
hostile(x=>{x.clauses.pop();},'truncation');
hostile(x=>{x.charge=1;},'source polarity');
let identities=0;
for(let p=0;p<2;p++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){
 assert(((p^a)^b)===((p^b)^a),'adjacent swap');
 assert(((p^a)^a)===p,'cancellation');
 assert((p^(a^b))===((p^a)^b),'associativity');identities+=3;
}
for(let t=0;t<2;t++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let aa=0;aa<2;aa++)for(let bb=0;bb<2;bb++){
 if((!t||a===aa)&&(!t||b===bb))assert(!t||(a^b)===(aa^bb),'guarded prefix');
 identities++;
}
console.log(JSON.stringify({status:'PASS',checks,rejected,identities,summary,sha256:crypto.createHash('sha256').update(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-04_0037_LSPV2_GUARDED_PARITY_ER383_raw.json')).digest('hex')},null,2));

