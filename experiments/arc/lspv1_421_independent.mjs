#!/usr/bin/env node
import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
let checks=0;const ok=(z,m)=>{checks++;assert.ok(z,m)};
function parse(s){
 ok(s.endsWith('\n')&&/^[\x00-\x7f]*$/.test(s),'stream');
 const ls=s.slice(0,-1).split('\n');
 const h=ls[0].trim().split(/\s+/);
 ok(h.length===4&&h[0]==='p'&&h[1]==='cnf','header');
 const n=Number(h[2]),m=Number(h[3]);
 ok(Number.isInteger(n)&&Number.isInteger(m)&&n>0&&m===ls.length-1,'counts');
 const cs=ls.slice(1).map(line=>{
  const z=line.trim().split(/\s+/).map(Number);
  ok(z.length>1&&z.at(-1)===0,'terminator');
  const c=z.slice(0,-1);
  ok(c.every(v=>Number.isInteger(v)&&v!==0&&Math.abs(v)<=n),'literal');
  ok(new Set(c.map(Math.abs)).size===c.length,'no duplicate variable');
  return c;
 });
 return {n,m,cs,lines:ls.slice(1),header:ls[0]+'\n'};
}
const sat=(c,a)=>c.some(v=>a[Math.abs(v)-1]===Number(v>0));
const filename=process.argv[2]||'lspv1_421_compact_raw.json';
const raw=JSON.parse(fs.readFileSync(filename,'utf8'));
const sources=raw.fixtures||raw.sources;
let neighbors=0;
for(const f of sources){
 const t=f.source_dimacs,s=parse(t),m=f.m;
 ok(s.m===m&&m===4*f.h&&s.n===f.edge_count,'shape');
 ok(crypto.createHash('sha256').update(t).digest('hex')===f.source_sha256,'source checksum');
 ok(f.neighbors.length===m && (f.W_mix341_prior??f.claimed_native_W_min)===m-1,'prior mixed minimum');
 const allCodes=Array.from({length:s.n},(_,j)=>j);
 for(let i=0;i<m;i++){
  neighbors++;
  const a=f.neighbors[i], idx=a.index;
  ok(idx===i,'indexed neighbor');
  const blockOffset=a.offset??f.offsets[i][0];
  const replacement=a.replacement_line+'\n';
  const blockLength=s.lines[i].length+1;
  ok(replacement.length===blockLength,'padded same length');
  const nt=t.slice(0,blockOffset)+replacement+t.slice(blockOffset+blockLength);
  ok(nt.length===t.length,'whole length');
  ok(nt.slice(0,blockOffset)===t.slice(0,blockOffset),'prefix');
  ok(nt.slice(blockOffset+blockLength)===t.slice(blockOffset+blockLength),'suffix');
  const p=parse(nt);
  ok(p.m===m,'neighbor count');
  const d=4*Math.floor(i/4)+(i%4+1)%4;
  ok(p.cs[i].join(',')===s.cs[d].join(','),'duplicate source clause');
  const witness=a.witness.split('').map(Number);
  ok(witness.length===s.n&&witness.every(z=>z===0||z===1),'assignment length');
  ok(!sat(s.cs[i],witness),'must falsify deleted clause');
  ok(s.cs.every((c,j)=>j===i||sat(c,witness)),'all other original clauses');
  ok(p.cs.every(c=>sat(c,witness)),'neighbor sat');
 }
 if(s.n<=12){
  for(let mask=0;mask<(1<<s.n);mask++){
   const v=allCodes.map(j=>mask>>j&1);
   ok(!s.cs.every(c=>sat(c,v)),'original UNSAT');
  }
 }
}
ok(neighbors===320,'total neighbors');
console.log(JSON.stringify({status:'PASS',checker:'standalone Node independent validator',assertions:checks,sources:sources.length,neighbors},null,2));
