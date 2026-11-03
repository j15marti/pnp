#!/usr/bin/env node
"use strict";
// Independent verifier for published full signed XOR4 proof. No producer imports.
function verify(data){
 let checks=0;function ok(t,why){checks++;if(!t)throw Error(why)}
 const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 function canon(c){ok(Array.isArray(c),'clause');let s=new Set();for(const v of c){ok(Number.isSafeInteger(v)&&v!==0,'literal');ok(!s.has(-v),'tautology');s.add(v)}return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a)}
 function enumerate(v){let out=[];for(let mask=0;mask<2**v.length;mask++){let a={};v.forEach((x,j)=>a[x]=(mask>>(v.length-j-1))&1);out.push(a)}return out}
 function blocker(a,vs){return canon(vs.map(x=>a[x]?-x:x))}
 function parity(a,vs,p){return vs.reduce((sum,x)=>sum+a[x],0)%2===p}
 const rules=[['left',[1,2,3],0],['right',[2,3,4],1],['opposite',[1,4],0]], expected=[];
 for(const [key,vs,p] of rules)for(const a of enumerate(vs))if(!parity(a,vs,p))expected.push({op:'source',name:key,clause:blocker(a,vs)});
 ok(data.schema==='LSPV1_LOG_SUPPORT_FACTOR_ER362_FULL_SIGNED_81_NODE_PROOF','schema');
 ok(data.calculus.includes('RES+paid'),'calculus');
 ok(data.source.length===10&&data.nodes.length>=100,'record lengths');
 ok(same(expected,data.source),'source authentication');
 let clauses=new Map(),defs=new Map(),defCount=0,resCount=0,last=4;
 for(let i=0;i<data.nodes.length;i++){
  const o=data.nodes[i];ok(o&&typeof o==='object','node');
  if(o.op==='source'){ok(i<expected.length&&same(o,expected[i]),'forged source');clauses.set(i,o.clause)}
  else if(o.op==='def'){
   defCount++;ok(o.q===++last&&Array.isArray(o.inputs)&&o.inputs.length===2,'gate creation');
   const [a,b]=o.inputs;ok(Number.isSafeInteger(a)&&Number.isSafeInteger(b)&&a!==0&&b!==0&&Math.abs(a)!==Math.abs(b),'gate operand');
   ok(Math.abs(a)<o.q&&Math.abs(b)<o.q,'gate forward reference');
   let slots=[canon([-o.q,a]),canon([-o.q,b]),canon([o.q,-a,-b])];
   ok(same(o.slots,slots),'forged gate slot');defs.set(i,o);
  }else if(o.op==='slot'){
   ok(defs.has(o.def)&&o.def<i&&Number.isInteger(o.which)&&o.which>=0&&o.which<3,'slot ref');
   ok(same(o.clause,defs.get(o.def).slots[o.which]),'forged slot');clauses.set(i,o.clause);
  }else if(o.op==='res'){
   resCount++;ok(Array.isArray(o.parents)&&o.parents.length===2,'arity');
   let [l,r]=o.parents,p=o.pivot;
   ok(Number.isInteger(l)&&Number.isInteger(r)&&l<i&&r<i&&clauses.has(l)&&clauses.has(r),'parent');
   let a=clauses.get(l),b=clauses.get(r),t;
   if(a.includes(p)&&b.includes(-p))t=canon(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));
   else if(a.includes(-p)&&b.includes(p))t=canon(a.filter(x=>x!==-p).concat(b.filter(x=>x!==p)));
   else throw Error('invalid strict pivot');
   ok(same(o.clause,t),'bad resolvent');clauses.set(i,t)
  }else throw Error('invalid node opcode');
 }
 ok(defCount===24&&resCount===57&&defCount+resCount===81,'paid costs');
 let outs=data.terminals.map(i=>clauses.get(i)).map(x=>JSON.stringify(x)).sort();
 let want=[canon([1,4]),canon([-1,-4])].map(x=>JSON.stringify(x)).sort();
 ok(same(outs,want),'incorrect derived XOR factor');
 ok(clauses.has(data.final)&&clauses.get(data.final).length===0,'missing contradiction');
 let models=0,preModels=0;
 for(const a of enumerate([1,2,3,4])){
  let l=parity(a,[1,2,3],0),r=parity(a,[2,3,4],1),opp=parity(a,[1,4],0);
  if(l&&r){preModels++;ok(parity(a,[1,4],1),'wrong XOR entailment');if(opp)models++}
 }
 ok(preModels===4&&models===0,'SAT/UNSAT label mismatch');
 return {status:'PASS',checks,source_count:data.source.length,paid_def:defCount,paid_res:resCount,pre_sat_models:preModels,full_sat_models:models};
}
if(typeof require!=='undefined'&&require.main===module){
 const fs=require('fs');const file=process.argv[2];if(!file)throw Error('Usage: node verify.js proof.json');
 const d=JSON.parse(fs.readFileSync(file,'utf8'));const result=verify(d);
 // independently test deliberate source, gate, pivot and terminal corruptions
 let bad=0;const corrupt=[];
 let x=JSON.parse(JSON.stringify(d));x.source[0].clause[0]*=-1;corrupt.push(x);
 x=JSON.parse(JSON.stringify(d));x.nodes.find(n=>n.op==='def').slots[0][0]=999;corrupt.push(x);
 x=JSON.parse(JSON.stringify(d));x.nodes.find(n=>n.op==='res').pivot=999;corrupt.push(x);
 x=JSON.parse(JSON.stringify(d));x.final=-1;corrupt.push(x);
 for(const c of corrupt){try{verify(c)}catch{bad++}}if(bad!==corrupt.length)throw Error('corrupted proof accepted');
 console.log(JSON.stringify({...result,corruptions_rejected:bad},null,2));
}
