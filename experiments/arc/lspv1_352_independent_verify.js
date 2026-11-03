#!/usr/bin/env node
'use strict';
// Independent parent/pivot and source-model referee, no imports from producer.
// Run in folder containing summary.json and the nine complete trace JSON files.
const fs=require('fs'),crypto=require('crypto');
function verify(data) {
  if(!Array.isArray(data.source)||!Array.isArray(data.rows)||!Array.isArray(data.order))throw Error('bad fields');
  const canonical=items=>{
    if(!Array.isArray(items))throw Error('not array');
    const ss=new Set(items);
    if([...ss].some(z=>!Number.isSafeInteger(z)||z===0||ss.has(-z)))throw Error('tautology/nonint');
    if(ss.size!==items.length)throw Error('duplicate literal');
    return [...ss].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  };
  let assertions=0,ca=data.source.length;
  for(let i=0;i<ca;i++) {
    const rr=data.rows[i];
    if(rr.kind!=='source'||JSON.stringify(canonical(rr.clause))!==JSON.stringify(canonical(data.source[i])))throw Error('source forgery');
    assertions++;
  }
  for(let i=ca;i<data.rows.length;i++) {
    const z=data.rows[i];
    if(z.kind!=='RES'||!Number.isInteger(z.pivot)||z.pivot<=0||
       !Number.isInteger(z.parent_pos)||!Number.isInteger(z.parent_neg)||
       z.parent_pos>=i||z.parent_neg>=i||z.parent_pos<0||z.parent_neg<0)throw Error('bad rule');
    const a=canonical(data.rows[z.parent_pos].clause),b=canonical(data.rows[z.parent_neg].clause);
    if(!a.includes(z.pivot)||!b.includes(-z.pivot))throw Error('bad pivot');
    const result=new Set([...a.filter(t=>t!==z.pivot),...b.filter(t=>t!==-z.pivot)]);
    if([...result].some(t=>result.has(-t)))throw Error('taut resolvent');
    if(JSON.stringify(canonical(z.clause))!==JSON.stringify(canonical([...result])))throw Error('wrong resolvent');
    assertions++;
  }
  if(data.root!==null) {
    if(!Number.isInteger(data.root)||data.root<0||data.root>=data.rows.length||data.rows[data.root].clause.length!==0)throw Error('invalid final root');
    const seen=new Set(),stack=[data.root];
    while(stack.length){let i=stack.pop();if(seen.has(i))continue;seen.add(i);let r=data.rows[i];if(r.kind==='RES')stack.push(r.parent_pos,r.parent_neg);}
    let cost=[...seen].filter(i=>data.rows[i].kind==='RES').length;
    if(cost!==data.root_ancestry_paid)throw Error('wrong paid count');
    assertions++;
  }
  if(data.derived!==data.rows.length-ca)throw Error('derived count');
  const n=data.n_vars,vs=[...new Set(data.source.flat().map(Math.abs))];
  if(vs.length!==n)throw Error('var count');
  if(n<=15){
   let models=0;
   for(let t=0;t<(2**n);t++) {
      const val=new Map(vs.map((v,i)=>[v,((t>>i)&1)===1]));
      if(data.source.every(c=>c.some(l=>val.get(Math.abs(l))===(l>0))))models++;
   }
   if((models>0)!==data.satisfiable)throw Error('bad SAT label');
   if((data.root===null)!==data.satisfiable)throw Error('bad root/SAT');
   assertions++;
  }
  return assertions;
}
function strictDimacs(txt){
 const ls=txt.trimEnd().split('\n');
 if(!/^p cnf [1-9]\d* [1-9]\d*$/.test(ls[0]))throw Error('bad header');
 let [,,vn,cn]=ls[0].split(' ');vn=+vn;cn=+cn;
 if(cn!==ls.length-1)throw Error('bad clause count');
 for(const line of ls.slice(1)){
  if(!/^(?:-?[1-9]\d* )*0$/.test(line))throw Error('bad literal syntax');
  const c=line.split(' ').slice(0,-1).map(Number);
  if(c.some(z=>Math.abs(z)>vn||c.includes(-z)))throw Error('bad var/tautology');
 }
 return true;
}
const summary=JSON.parse(fs.readFileSync('summary.json','utf8'));
let total=0,checks=[];
for(const entry of summary.cases){
 const s=fs.readFileSync(entry.proof_file,'utf8'), d=JSON.parse(s);
 const got=crypto.createHash('sha256').update(s).digest('hex');
 if(got!==entry.proof_sha256)throw Error('sha mismatch '+entry.name);
 if(d.width!==entry.width||d.derived!==entry.derived||d.root_ancestry_paid!==entry.paid_ancestry)throw Error('summary forgery');
 let num=verify(d);total+=num;
 let serial='p cnf '+d.n_vars+' '+d.source.length+'\n'+d.source.map(c=>c.join(' ')+' 0\n').join('');
 strictDimacs(serial);num++;total++;
 for(const s of [serial.replace('p cnf','p cfn'),serial.replace(/ 0\n/,'\n'),serial+'1 0\n',serial.replace(/p cnf (\d+) (\d+)/,'p cnf $1 999')]){
  let failed=false;try{strictDimacs(s)}catch(e){failed=true}
  if(!failed)throw Error('malformed accepted');num++;total++;
 }
 if(d.root!==null){
  const a=JSON.parse(JSON.stringify(d));const r=a.rows.find(z=>z.kind==='RES');r.pivot=999999;
  let failed=false;try{verify(a)}catch(e){failed=true}
  if(!failed)throw Error('wrong pivot accepted');num++;total++;
 }
 checks.push({name:entry.name,assertions:num});
}
console.log(JSON.stringify({status:'COMPUTATIONAL',verified_cases:checks.length,assertions:total,
 malformed_rejections:4*checks.length,rows:summary.cases.reduce((a,c)=>a+c.derived,0),checks},null,2));
