// LSPV-3/451, independent compact semantic regression, 2026-11-06 PST.
// Usage: node lspv3_451_multiassumption_check.mjs
// This checks a declared semantic rule-level model, NOT the historical native byte checker.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const charge=[1,1,0,0];
const clauses=[];
for(let v=0;v<4;v++){
 const inc=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
 for(let z=0;z<8;z++){
  const b=[(z>>2)&1,(z>>1)&1,z&1];
  if((b[0]^b[1]^b[2])!==charge[v])clauses.push(inc.map((j,i)=>(b[i]?-(j+1):j+1)));
 }
}
assert.equal(clauses.length,16);
const dimacs='p cnf 6 16\n'+clauses.map(c=>c.join(' ')+' 0\n').join('');
const sha=crypto.createHash('sha256').update(dimacs).digest('hex');
assert.equal(dimacs.length,163);
assert.equal(sha,'061ee272d1e2e6167ae91c2adf9ab360c7b791e786e274a89a49dcd5164da115');
let tests=0;
const ck=(p)=>{assert.ok(p);tests++;};
const csat=(cl,v)=>cl.some(x=>v[Math.abs(x)-1]===(x>0?1:0));
const all6=Array.from({length:64},(_,i)=>Array.from({length:6},(_,k)=>(i>>k)&1));
const sat=(v)=>clauses.every(c=>csat(c,v));
ck(all6.filter(sat).length===8);
for(let v of [0,2]){
 const inc=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
 let leaf=clauses.slice(4*v,4*v+4).map(cl=>{
  let t=0;for(let z=0;z<8;z++){
   const bits=Array(6).fill(0);inc.forEach((id,j)=>bits[id]=(z>>j)&1);
   if(csat(cl,bits))t|=1<<z;
  }return t;
 });
 const gate=(leaf[0]&leaf[1])&(leaf[2]&leaf[3]);
 let parity=0;for(let z=0;z<8;z++)if(((z&1)^((z>>1)&1)^((z>>2)&1))===charge[v])parity|=1<<z;
 ck(gate===parity);
}
const row=(mask,rhs)=>({mask,rhs});
const xor=(a,b)=>row(a.mask^b.mask,a.rhs^b.rhs);
const E0=row(7,1),E2=row(42,0);
const A=[0,2,3,5].map(x=>row(1<<x,0));
let orig=xor(E0,E2);
let tags=0,proj=orig,real=1;
for(let i=0;i<4;i++){orig=xor(orig,A[i]);tags^=1<<i; /* context assumption projects to virtual zero */ }
ck(orig.mask===0&&orig.rhs===1);
ck(proj.mask===45&&proj.rhs===1&&tags===15&&real===1);
ck(!all6.some(v=>sat(v)&&[0,2,3,5].every(i=>v[i]===0)));
ck(all6.some(v=>sat(v)&&[0,2,3].every(i=>v[i]===0)&&v[5]===1));
const rows=Array.from({length:16},(_,i)=>row(i>>1,i&1));
const val=(r,v)=>{let s=r.rhs;for(let k=0;k<3;k++)s^=((r.mask>>k)&1)*((v>>k)&1);return s;};
let ok=0,bad=0;
for(let e1 of rows)for(let e2 of rows)for(let a of rows)for(let b of rows){
 const p=xor(e1,e2),q=xor(a,b),final=xor(p,q);
 if(final.mask!==0||final.rhs!==1)continue;
 const consistent=Array.from({length:8},(_,i)=>i).some(v=>!val(a,v)&&!val(b,v));
 if(!consistent){bad++;continue;}
 ok++;ck(p.mask!==0||p.rhs!==0);
 for(let v=0;v<8;v++)if(!val(a,v)&&!val(b,v))ck(val(p,v)===1);
}
ck(ok===3376&&bad===720);
console.log(JSON.stringify({status:'COMPUTATIONAL',source_sha256:sha,source_models:8,independent_assertions:tests,exhaustive_quadruples:65536,consistent_assumption_contradictions:ok,inconsistent_assumption_contradictions:bad,paid_AND3:6,paid_contextual_XOR:5,paid_projected_XOR:1,P_vs_NP:'OPEN'}));
