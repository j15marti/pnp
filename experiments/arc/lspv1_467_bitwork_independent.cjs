#!/usr/bin/env node
// LSPV-1/467 independent replay; ENUM rule belongs ONLY to foreign R_enum_or_res.
'use strict';
const assert=require('node:assert/strict'),crypto=require('node:crypto');
const H=s=>crypto.createHash('sha256').update(s,'utf8').digest('hex');
function edges(kind){
 let h=kind==='K4'?4:kind==='K33'?6:8,es=[];
 for(let a=0;a<h;a++)for(let b=a+1;b<h;b++){
  if(kind==='K4'||(kind==='K33'&&a<3&&b>=3)||(kind==='cube'&&((a^b).toString(2).match(/1/g)||[]).length===1))es.push([a,b]);
 }
 return [h,es];
}
function source(kind,odd){
 const [h,es]=edges(kind);let cs=[];
 for(let v=0;v<h;v++){
  let ids=[];es.forEach(([a,b],i)=>{if(a===v||b===v)ids.push(i+1)});
  assert.equal(ids.length,3);
  for(let m=0;m<8;m++){
   let bits=[(m>>2)&1,(m>>1)&1,m&1];
   if((bits[0]^bits[1]^bits[2])!==(odd&&v===0?1:0))
    cs.push(ids.map((id,j)=>bits[j]?-id:id));
  }
 }
 return [es.length,cs];
}
function satisfies(c,b){return c.some(l=>(b[Math.abs(l)-1]==='1')===(l>0))}
function enumerate(n,cs){
 let ret='';
 for(let i=0;i<2**n;i++){
  let bits=i.toString(2).padStart(n,'0'),j=cs.findIndex(c=>!satisfies(c,bits));
  if(j<0)return null;
  ret+=bits+' '+(j+1)+'\n';
 }
 return ret;
}
function check(n,cs,cert){
 if(typeof cert!=='string'||!cert.endsWith('\n'))return false;
 let lines=cert.slice(0,-1).split('\n');
 if(lines.length!==2**n)return false;
 for(let i=0;i<lines.length;i++){
  let a=/^([01]+) ([1-9][0-9]*)$/.exec(lines[i]);
  if(!a||a[1]!==i.toString(2).padStart(n,'0'))return false;
  let j=Number(a[2]);
  if(!Number.isSafeInteger(j)||j<1||j>cs.length||satisfies(cs[j-1],a[1]))return false;
 }
 return true;
}
function dimacs(n,cs){return 'p cnf '+n+' '+cs.length+'\n'+cs.map(c=>c.join(' ')+' 0\n').join('')}
let results=[],checks=0;
for(let kind of ['K4','K33','cube']){
 const [n,cs]=source(kind,true),cert=enumerate(n,cs);
 assert.ok(cert&&check(n,cs,cert));checks++;
 assert.equal(enumerate(...source(kind,false)),null);checks++;
 let lines=cert.trimEnd().split('\n'),satisfyingIndex=cs.findIndex(c=>satisfies(c,lines[0].split(' ')[0]));
 let corrupt=[
 lines.slice(0,-1).join('\n')+'\n',
 [lines[0],lines[0],...lines.slice(2)].join('\n')+'\n',
 [lines[0],lines[2],lines[1],...lines.slice(3)].join('\n')+'\n',
 lines[0].split(' ')[0]+' 0\n'+lines.slice(1).join('\n')+'\n',
 lines[0].split(' ')[0]+' '+(cs.length+1)+'\n'+lines.slice(1).join('\n')+'\n',
 lines[0].split(' ')[0]+' '+(satisfyingIndex+1)+'\n'+lines.slice(1).join('\n')+'\n'
 ];
 for(let b of corrupt){assert.equal(check(n,cs,b),false);checks++}
 for(let omit=0;omit<cs.length;omit++){
  let witness=false;
  for(let i=0;i<2**n;i++){
   let b=i.toString(2).padStart(n,'0');
   if(cs.every((c,j)=>j===omit||satisfies(c,b))){witness=true;break}
  }
  assert.ok(witness);checks++;
 }
 results.push({graph:kind,n,original_clauses:cs.length,source_sha256:H(dimacs(n,cs)),certificate_sha256:H(cert),enum_lines:lines.length,enum_bits:8*Buffer.byteLength(cert),corruptions_rejected:corrupt.length,all_clause_deletions_SAT:true});
}
console.log(JSON.stringify({system:'R_enum_or_res (distinct artificial control)',assertions_passed:checks,results},null,2));
