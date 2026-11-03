#!/usr/bin/env node
'use strict';
/* Independent local ER2 certificate checker: no third-party modules.
   node lspv3_357_independent_verify.js lspv3_357_macro_certs.json
*/
const fs=require('fs'),assert=require('assert');
const file=process.argv[2]||'lspv3_357_macro_certs.json';
const data=JSON.parse(fs.readFileSync(file,'utf8'));
function canonical(a){const s=new Set(a);for(const x of s)if(s.has(-x))return null;return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||Number(x<0)-Number(y<0));}
const key=a=>JSON.stringify(canonical(a));
const lit=(mask,l)=>l>0?((mask>>(l-1))&1)===1:((mask>>(-l-1))&1)===0;
const hold=(mask,c)=>c.some(l=>lit(mask,l));
let checks=0,cases=0,totalRes=0,totalDef=0,failed=0;
function verify(name,obj){
  const values=Object.values(obj.vars);
  assert(values.length===new Set(values).size);checks++;
  const src=obj.source.map(x=>x.clause),defs=obj.defs,seen=new Map();
  assert(src.length>0);
  for(let i=0;i<src.length;i++){
    const c=src[i],tag=obj.source[i].tag;
    assert(c.length>0&&c.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=values.length));checks++;
    assert.deepStrictEqual(canonical(c),c);checks++;
    if(tag==='hyp')continue;
    const m=/^gate:(\d+):([012])$/.exec(tag);assert(m);checks++;
    const [o,a,b]=defs[+m[1]];
    const expected=[[-o,a],[-o,b],[o,-a,-b]][+m[2]];
    assert.deepStrictEqual(canonical(expected),c);checks++;
    seen.set(tag,(seen.get(tag)||0)+1);
  }
  for(let i=0;i<defs.length;i++){
    const [o,a,b]=defs[i];
    assert(o>0&&Math.abs(a)!==Math.abs(b));checks++;
    for(let j=0;j<3;j++)assert.strictEqual(seen.get('gate:'+i+':'+j),1);
    checks+=3;
  }
  const auth=new Set(src.map(key));
  for(const [c,a,b,p] of obj.steps){
    assert(auth.has(key(a))&&auth.has(key(b))&&a.includes(p)&&b.includes(-p));checks++;
    const r=canonical(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));
    assert(r!==null&&key(r)===key(c));checks++;
    auth.add(key(c));
  }
  assert(auth.has(key(obj.target)));checks++;
  let valid=0;
  for(let mask=0;mask<2**values.length;mask++){
    if(src.every(c=>hold(mask,c))){
      valid++;assert(hold(mask,obj.target));checks++;
    }
  }
  assert(valid>0);checks++;
  totalRes+=obj.steps.length;totalDef+=defs.length;cases++;
  return {definitions:defs.length,resolution:obj.steps.length,
    satisfyingCompleteAssignments:valid};
}
function rejects(f){try{f();return false}catch(e){return true}}
const out={};
for(const [name,cert] of Object.entries(data))out[name]=verify(name,cert);
const obj=data.assoc;
assert(rejects(()=>verify('corrupt',{...obj,steps:obj.steps.map((x,i)=>i===3?[[777],x[1],x[2],x[3]]:x)})));checks++;failed++;
assert(rejects(()=>verify('corrupt',{...obj,steps:obj.steps.map((x,i)=>i===3?[x[0],x[1],x[2],999]:x)})));checks++;failed++;
assert(rejects(()=>verify('malformed',{...obj,source:obj.source.map((x,i)=>i===0?{...x,clause:[0]}:x)})));checks++;failed++;
assert(rejects(()=>verify('malformed',{...obj,source:obj.source.map((x,i)=>i===0?{...x,tag:'gate:100:2'}:x)})));checks++;failed++;
assert(rejects(()=>verify('malformed',{...obj,defs:obj.defs.map((x,i)=>i===0?[x[0],x[1],x[1]]:x)})));checks++;failed++;
assert(rejects(()=>verify('malformed',{...obj,target:[999]})));checks++;failed++;
process.stdout.write(JSON.stringify({status:'COMPUTATIONAL',checkedMacros:cases,
  paidDEF:totalDef,paidRES:totalRes,malformedAndCorruptedRejections:failed,
  assertions:checks,macroCounts:out},null,2)+'\n');
