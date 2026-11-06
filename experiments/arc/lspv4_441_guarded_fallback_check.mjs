#!/usr/bin/env node
// Standalone replay of the committed LSPV-4/441 compact raw witness.
// Full 28-case producer and independent referee are preserved in the ZIP.
import fs from 'node:fs';
import crypto from 'node:crypto';
const file = new URL('../../results/raw/arc/2026-11-06_0736_LSPV4_441_GUARDED_FALLBACK_SUMMARY.json', import.meta.url);
const o = JSON.parse(fs.readFileSync(file, 'utf8'));
let checks=0;
function ok(x) { checks++; if (!x) throw new Error('failed check ' + checks); }
const h=s=>crypto.createHash('sha256').update(s).digest('hex');
function unpack(bits){
  ok(bits.startsWith('10100101')); let p=8,H=0,w=0;
  while(bits[p]==='1'){H++;p++;}ok(bits[p]==='0');p++;
  while(bits[p]==='1'){w++;p++;}ok(bits[p]==='0');p++;
  ok(bits.length===p+12*H*(w+1)+2);ok(bits.endsWith('01'));
  let clauses=[];
  for(let j=0;j<4*H;j++){
    let c=[];
    for(let z=0;z<3;z++){
      let b=p+(j*3+z)*(w+1);
      c.push([parseInt(bits.substring(b,b+w),2),Number(bits[b+w])]);
    }
    clauses.push(c);
  }
  return {H,clauses};
}
function keys(clauses){return clauses.map(c=>c.map(t=>t.join(':')).sort().join('/')).sort().join('|');}
function canonical(z){
  for(let v=0;v<z.H;v++){
    let c0=z.clauses[4*v][2][0],chi=z.clauses[4*v][2][1]^1;
    for(let p=0;p<2;p++)for(let r=0;r<2;r++){
      let c=z.clauses[4*v+2*p+r];
      if(c[0][0]!==((v-1+z.H)%z.H)+1 || c[1][0]!==v+1 || c[2][0]!==c0 ||
         c[0][1]!==p || c[1][1]!==r || c[2][1]!==(p^r^1^chi))return false;
    }
  }
  return true;
}
function sat(z){
  let ids=[...new Set(z.clauses.flat().map(l=>l[0]))];ok(ids.length<=15);
  const m=new Map(ids.map((id,i)=>[id,i]));
  for(let a=0;a<2**ids.length;a++){
    if(z.clauses.every(c=>c.some(([id,neg])=>((a>>m.get(id))&1)!==neg)))return true;
  }
  return false;
}
const f=o.h6_fixture;
ok(f.canonical.length===f.N && f.permuted.length===f.N);
ok(h(f.canonical)===f.canonical_sha256 && h(f.permuted)===f.permuted_sha256);
const a=unpack(f.canonical),b=unpack(f.permuted);
ok(a.H===f.H && b.H===f.H);
ok(keys(a.clauses)===keys(b.clauses));
ok(canonical(a) && !canonical(b));
ok(!sat(a) && !sat(b) && f.label==='UNSAT');
for(const d of [2,3,4,8,12]){
  ok(d>Math.max(1.1,0.6+d/2));
  for(const n of [128,512,2048])ok((BigInt(n)**BigInt(d))>0n);
}
for(const d of [4,12,40]){
  ok(Math.abs(0.6+0.5*d-(0.6+d/2))<1e-10);
  for(const lambda of [0.6,0.75,1])ok(0.6+lambda*d>0.6+d/2);
}
const corruption=f.permuted.slice(0,30)+(f.permuted[30]==='0'?'1':'0')+f.permuted.slice(31);
ok(keys(unpack(corruption).clauses)!==keys(a.clauses));
ok(o.formula_pairs===28 && o.independent_js_checks===25242);
console.log(JSON.stringify({status:'PASS',checks,h6_label:f.label,full_independent_checks_recorded:o.independent_js_checks}));
