#!/usr/bin/env node
// LSPV2-370: independently written finite Res(XOR) checker, no dependencies.
// It validates semantic one-parent weakening and complementary affine cuts.
// It does NOT validate unrestricted Rmix341 syntax or prove optimality.
'use strict';
const fs=require('fs');
const data=JSON.parse(fs.readFileSync(process.argv[2]||'raw.json','utf8'));
let assertions=0;
function ok(t,msg){assertions++;if(!t)throw Error(msg)}
function clone(x){return JSON.parse(JSON.stringify(x))}
function validEq(e,d){return Array.isArray(e)&&e.length===2&&Number.isInteger(e[0])&&e[0]>=0&&e[0]<(1<<d)&&[0,1].includes(e[1]);}
function validC(c,d){return Array.isArray(c)&&c.every(e=>validEq(e,d))}
function v(e,a){let x=e[0]&a,c=0;while(x){x&=x-1;c++;}return (c&1)===e[1]}
function sat(C,a){return C.some(e=>v(e,a));}
function sig(C){return [...new Set(C.map(e=>e.join(':')))].sort().join(';')}
function entails(A,B,d){for(let a=0;a<(1<<d);a++)if(sat(A,a)&&!sat(B,a))return false;return true}
function cut(p,q,piv){
  let key=piv.join(':'),neg=[piv[0],1-piv[1]].join(':');
  let ia=p.findIndex(e=>e.join(':')===key),ib=q.findIndex(e=>e.join(':')===neg);
  if(ia<0||ib<0)return null;
  return p.filter((e,i)=>i!==ia).concat(q.filter((e,i)=>i!==ib));
}
function verify(c){
 const d=c.d;ok(Number.isInteger(d)&&d>=2&&d<=5,'d');
 ok(Array.isArray(c.lines),'lines');
 const rows=[];let sc=0,paid=0;
 for(let i=0;i<c.lines.length;i++){
  let z=c.lines[i];ok(validC(z.clause,d),'bad equation');
  if(z.op==='src'){
   ok(sc<c.source.length&&sig(z.clause)===sig(c.source[sc]),'source mismatch');sc++;
  } else if(z.op==='weak'){
   ok(Number.isInteger(z.parent)&&z.parent>=0&&z.parent<i,'weak parent');
   ok(entails(rows[z.parent],z.clause,d),'invalid semantic weakening');paid++;
  }else if(z.op==='cut'){
   ok(Array.isArray(z.parents)&&z.parents.length===2&&z.parents.every(j=>Number.isInteger(j)&&j>=0&&j<i),'cut parents');
   ok(validEq(z.pivot,d),'bad pivot');
   let A=rows[z.parents[0]],B=rows[z.parents[1]];
   let C=cut(A,B,z.pivot);if(C===null)C=cut(B,A,z.pivot);
   ok(C!==null&&sig(C)===sig(z.clause),'bad cut');paid++;
  }else throw Error('illegal rule');
  rows.push(z.clause);
 }
 ok(sc===c.source.length,'source register');ok(paid===c.paid,'paid count');
 let models=0;for(let a=0;a<(1<<d);a++)if(c.source.every(x=>sat(x,a)))models++;
 ok(models===c.expected_models,'SAT model count');
 if(c.kind==='opposite_parity'){
   ok(rows.length&&rows.at(-1).length===0,'no contradiction');
   for(let j=0;j<c.source.length;j++){
    let models=0;for(let a=0;a<(1<<d);a++)if(c.source.every((x,k)=>k===j||sat(x,a)))models++;
    ok(models===1,'deletion does not make SAT');
    for(let k=0;k<d;k++){
     let transformed=c.source[j].map((e,t)=>t===k?[e[0],1-e[1]]:e);
     let good=0;
     for(let a=0;a<(1<<d);a++)if(c.source.every((x,t)=>sat(t===j?transformed:x,a)))good++;
     ok(good>=1,'literal-sign control fails');
    }
   }
   let half=c.source.slice(0,c.source.length/2),count=0;
   for(let a=0;a<(1<<d);a++)if(half.every(x=>sat(x,a)))count++;
   ok(count===(1<<(d-1)),'SAT parity half');
 }else if(c.kind==='canonical_factor'){
   ok(c.lines.length>=c.output.length,'factor output');
   for(let j of c.output)ok(c.lines[j].op==='weak','output not authenticated');
   let bad=new Set([...c.bad_A,...c.bad_B]);
   ok((1<<d)-bad.size===models,'factor projection');
 }else throw Error('unknown fixture');
 return {kind:c.kind,d,paid,source:sc,models};
}
let results=data.cases.map(verify);
let neg=0;
function fails(c){try{verify(c);throw Error('corrupted record accepted')}
 catch(e){if(e.message==='corrupted record accepted')throw e;neg++;}}
let p=data.cases[0];
for(let mutate of [
 c=>{c.lines[0].clause[0][0]=-1;},
 c=>{let z=c.lines.find(t=>t.op==='weak');z.parent=999999;},
 c=>{let z=c.lines.find(t=>t.op==='weak');z.clause=[];},
 c=>{let z=c.lines.find(t=>t.op==='cut');z.pivot=[0,0];},
 c=>{let z=c.lines.find(t=>t.op==='cut');z.parents=[0,999999];},
 c=>{let z=c.lines.find(t=>t.op==='cut');z.clause=[];},
 c=>{c.lines.at(-1).clause=[[1,1]];},
 c=>{c.source[0][0][1]^=1;}
 ]){let c=clone(p);mutate(c);fails(c)}
let out={status:'PASS',cases:results.length,
 by_kind:results.reduce((r,c)=>(r[c.kind]=(r[c.kind]||0)+1,r),{}),
 paid_nodes:results.reduce((s,c)=>s+c.paid,0),assertions,negative_rejections:neg,
 opposite_parity:results.filter(c=>c.kind==='opposite_parity')};
console.log(JSON.stringify(out,null,2));
