'use strict';
// LSPV-1/488 distinct paid-Tseitin+Resolution guard certificate.
// Not a certificate accepted by the historical R_mix341 checker.
const normalized=a=>{const s=new Set(a);return [...s].some(x=>s.has(-x))?null:[...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);};
const same=(a,b)=>!!a&&!!b&&a.length===b.length&&a.every((v,i)=>v===b[i]);
function source(){
 const a=[],put=x=>a.push(normalized(x));
 const and=(t,x,y)=>{put([-t,x]);put([-t,y]);put([t,-x,-y]);};
 const truth=(t,x,y,f)=>{for(let b=0;b<2;b++)for(let c=0;c<2;c++)put([b?-x:x,c?-y:y,f(b,c)?t:-t]);};
 and(4,2,3);and(5,-1,-4);truth(8,4,2,(q,u)=>q===u);and(6,1,8);
 truth(9,1,3,(p,v)=>p!==v);truth(10,4,3,(q,v)=>q===v);and(7,9,10);
 return a;
}
const axioms=source(), proof=[
[1,[2,-4]],[2,[3,-4]],[3,[-2,-3,4]],[4,[1,4,5]],
[5,[2,4,8]],[6,[-2,-4,8]],[7,[-1,6,-8]],[8,[1,-3,9]],
[9,[-1,3,9]],[10,[3,4,10]],[11,[-3,-4,10]],[12,[7,-9,-10]],
[13,[4,5,6,-8],4,7,1],[14,[3,4,5,9],4,9,1],
[15,[-3,6,-8,9],8,7,1],[16,[-2,-3,8],3,6,4],
[17,[2,8],5,1,4],[18,[3,10],10,2,4],
[19,[3,5,6,-8],13,2,4],[20,[-3,5,6,-8,10],13,11,4],
[21,[3,5,9],14,2,4],[22,[-3,8],17,16,2],
[23,[5,6,-8,10],18,20,3],[24,[8,10],18,22,3],
[25,[5,6,-8,9],19,15,3],[26,[5,8,9],21,22,3],
[27,[5,6,10],24,23,8],[28,[5,6,9],26,25,8],
[29,[5,6,7,-10],28,12,9],[30,[5,6,7],27,29,10]
];
function check(P){
 const sourceSet=new Set(axioms.map(c=>JSON.stringify(c))),known=new Map(),depth=new Map();
 let steps=0;
 for(const z of P){
  const [id,cl,a,b,p]=z;
  if(!Number.isSafeInteger(id)||known.has(id)||!Array.isArray(cl)||cl.some(v=>!Number.isInteger(v)||v===0||Math.abs(v)>10))throw Error('invalid ID/clause');
  if(!same(normalized(cl),cl))throw Error('noncanonical clause');
  let d=0;
  if(z.length===2){if(!sourceSet.has(JSON.stringify(cl)))throw Error('unauthenticated source');}
  else {
   if(z.length!==5||!known.has(a)||!known.has(b)||!Number.isInteger(p)||p<1||p>10)throw Error('bad parents');
   const A=known.get(a),B=known.get(b);
   if(!A.includes(p)||!B.includes(-p))throw Error('oriented pivot');
   const C=normalized([...A.filter(v=>v!==p),...B.filter(v=>v!==-p)]);
   if(!same(C,cl))throw Error('bad resolvent');
   d=Math.max(depth.get(a),depth.get(b))+1;steps++;
  }
  known.set(id,cl);depth.set(id,d);
 }
 if(!same(known.get(30),[5,6,7]))throw Error('no covered-case conclusion');
 return {distinct_nodes:known.size,source_ancestors:known.size-steps,RES_steps:steps,
     paid_facets:axioms.length,all_paid_facet_plus_RES_records:axioms.length+steps,
     critical_path_RES:depth.get(30),certificate_ASCII_bytes:JSON.stringify(P).length};
}
function run(){
 const metrics=check(proof);
 let models=0;
 for(let p=0;p<2;p++)for(let u=0;u<2;u++)for(let v=0;v<2;v++)for(let q=0;q<2;q++){
  const r1=Number(q===u),r2=p^v,r3=Number(q===v);
  const m={1:p,2:u,3:v,4:q,5:Number(!p&&!q),6:Number(!!p&&!!r1),7:Number(!!r2&&!!r3),8:r1,9:r2,10:r3};
  const satisfied=axioms.every(C=>C.some(l=>l>0?m[l]===1:m[-l]===0));
  if(satisfied!==(q===u*v))throw Error('source semantics error');
  if(satisfied){models++;if(!(m[5]||m[6]||m[7]))throw Error('cover misses assignment');}
 }
 const negatives=[];
 const mutate=fn=>proof.map(z=>fn([...z.slice(0,1),[...z[1]],...z.slice(2)]));
 function rejects(name,P){try{check(P);throw Error('hostile accepted: '+name);}catch(e){if(e.message.startsWith('hostile accepted:'))throw e;negatives.push(name);}}
 rejects('wrong_pivot',mutate(z=>{if(z[0]===30)z[4]=9;return z;}));
 rejects('false_source',mutate(z=>{if(z[0]===1)z[1]=[2,4];return z;}));
 rejects('missing_AND_case',proof.slice(0,-1));
 rejects('cross_branch_unsound',mutate(z=>{if(z[0]===30)z[1]=[5,7];return z;}));
 rejects('bogus_parent',mutate(z=>{if(z[0]===29)z[3]=999;return z;}));
 rejects('duplicate_record',proof.concat([proof[0]]));
 return {label:'LSPV1_488_GUARD_RES_CERT',models_checked:16,satisfying_gate_models:models,
    guard_cover:true,negative_controls:negatives,metrics,
    no_native_checker:true,status:'PROVED/RESTRICTED; no unrestricted mixed calculus or B3 result'};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
