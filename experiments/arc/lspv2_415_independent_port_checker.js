#!/usr/bin/env node
// Independent no-producer-import checker for explicitly CONDITIONAL Splus facet grammar.
const fs = require('fs');
const raw = JSON.parse(fs.readFileSync(process.argv[2] || 'results/raw/arc/2026-11-05_0336_LSPV2_COOK_ER_PORT_FORK415_full.json','utf8'));
let checks=0;
function check(x,msg='assertion') { checks++; if(!x) throw Error(msg); }
const inv=s=>s.startsWith('~')?s.slice(1):'~'+s;
const norm=cl=>[...new Set(cl)].sort();
const eq=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
const lit=(s,a)=>s.startsWith('~')?!a[s.slice(1)]:a[s];
const holds=(cl,a)=>cl.some(x=>lit(x,a));
const funcs={AND:(a,b)=>a&&b, OR:(a,b)=>a||b, XOR:(a,b)=>a!==b};
function gateFacets(d){
 const [a,b]=d.inputs,v=d.out;
 if(d.op==='AND')return [[inv(a),inv(b),v],[a,inv(v)],[b,inv(v)]];
 if(d.op==='OR')return [[a,b,inv(v)],[inv(a),v],[inv(b),v]];
 if(d.op==='XOR')return [[a,b,inv(v)],[a,inv(b),v],[inv(a),b,v],[inv(a),inv(b),inv(v)]];
 throw Error('bad gate');
}
function checkOne(rec){
 const seen=new Set(rec.source.flat().map(x=>x.replace(/^~/,''))),def=[];
 for(const d of rec.definitions){
  check(!seen.has(d.out),'not fresh');
  for(const p of d.inputs)check(seen.has(p),'missing input');
  seen.add(d.out);def.push(gateFacets(d));
 }
 function ref(r,k){
  if(r[0]==='S')return rec.source[r[1]];
  if(r[0]==='D')return def[r[1]][r[2]];
  if(r[0]==='R'){check(r[1]<k,'future reference');return rec.resolutions[r[1]].clause;}
  throw Error('bad ref');
 }
 for(let i=0;i<rec.resolutions.length;i++){
  const row=rec.resolutions[i],a=ref(row.parents[0],i),b=ref(row.parents[1],i),pv=row.pivot;
  check((a.includes(pv)&&b.includes(inv(pv)))||(a.includes(inv(pv))&&b.includes(pv)),'invalid pivot');
  const c=[...a.filter(x=>x!==pv&&x!==inv(pv)),...b.filter(x=>x!==pv&&x!==inv(pv))];
  check(eq(c,row.clause),'invalid resolvent');
 }
 const original=[...new Set(rec.source.flat().map(x=>x.replace(/^~/,'')))].sort();let originalSat=0;
 for(let mask=0;mask<2**original.length;mask++){
  const a=Object.fromEntries(original.map((s,j)=>[s,!!(mask&(1<<j))]));
  for(let i=0;i<rec.definitions.length;i++){
   const d=rec.definitions[i];a[d.out]=funcs[d.op](a[d.inputs[0]],a[d.inputs[1]]);
   for(const f of def[i])check(holds(f,a),'invalid defining facet');
  }
  for(let j=0;j<rec.resolutions.length;j++){
   const rs=rec.resolutions[j],v0=ref(rs.parents[0],j),v1=ref(rs.parents[1],j);
   check(!holds(v0,a)||holds(rs.clause,a)||!holds(v1,a),'resolution unsound');
  }
  const srcSat=rec.source.every(c=>holds(c,a));
  if(srcSat){originalSat++;for(const rs of rec.resolutions)check(holds(rs.clause,a),'soundness failure');}
 }
 return originalSat;
}
function validateDIMACS(text){
 if(!text.endsWith('\n'))return false;
 const lines=text.trim().split('\n'),h=/^p cnf (\d+) (\d+)$/.exec(lines[0]);
 if(!h)return false;
 const n=Number(h[1]),m=Number(h[2]);if(lines.length-1!==m)return false;
 for(const line of lines.slice(1)){
  if(!/^(?:-?\d+\s+)*0$/.test(line))return false;
  const nums=line.trim().split(/\s+/).map(Number);
  if(nums.slice(0,-1).some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n))return false;
 }
 return true;
}
check(validateDIMACS(raw.original_dimacs),'valid source DIMACS');
const mut=raw.original_dimacs;
for(const bad of [mut.replace('3 1 0','3 1'),mut.replace('3 4','3 5'),mut.replace('3 1 0','4 1 0'),mut.replace('3 1 0','r 1 0'),mut.trimEnd()])check(!validateDIMACS(bad),'malformed source accepted');
const f=raw.source_fixture;
check(f.definitions.length===2&&f.resolutions.length===5,'fixture cost');
check(f.resolutions.at(-1).clause.length===0,'not contradiction');
check(checkOne(f)===0,'fixture must be UNSAT');
for(let j of [0,1]){const other=structuredClone(f);other.source.splice(j,1);other.resolutions=[];check(checkOne(other)>0,'deletion not SAT');}
for(const n of [1,2,3,4,6]){
 let rows=['p','q','r'];let all=[];
 for(let i=0;i<n;i++){
  const [p,q,r]=rows,t='t_'+i,z='z_'+i;
  const fa=gateFacets({out:t,op:'AND',inputs:[q,r]});
  const fb=gateFacets({out:z,op:'OR',inputs:[p,t]});
  const res=(a,b,piv)=>norm([...a.filter(x=>x!==piv&&x!==inv(piv)),...b.filter(x=>x!==piv&&x!==inv(piv))]);
  const three=[res(fa[0],fb[2],t),res(fb[0],fa[1],t),res(fb[0],fa[2],t)];
  check(eq(three[0],[inv(q),inv(r),z]),'ext clause 1');
  check(eq(three[1],[p,q,inv(z)]),'ext clause 2');
  check(eq(three[2],[p,r,inv(z)]),'ext clause 3');
  for(let mask=0;mask<8;mask++){
   const A={p:!!(mask&1),q:!!(mask&2),r:!!(mask&4)};
   for(const prev of all){A[prev.t]=A[prev.q]&&A[prev.r];A[prev.z]=A[prev.p]||A[prev.t];}
   A[t]=A[q]&&A[r];A[z]=A[p]||A[t];
   check(A[z]===(A[p]||(A[q]&&A[r])),'gate mismatch');
   for(const c of [fb[1],...three])check(holds(c,A),'extension clause false');
  }
  all.push({p,q,r,t,z});rows=[z,'q','r'];
 }
 const count=raw.macro_counts[String(n)];
 check(count.charged_def===2*n&&count.charged_res===3*n&&count.charged_total===5*n,'charge mismatch');
}
check(f.resolutions.some(r=>r.parents.some(p=>p[0]==='D')),'Sminus must reject');
console.log(JSON.stringify({independent_assertions:checks,fixture_paid_nodes:7,validated_macros:[1,2,3,4,6],sat_unsat_malformed_controls:'passed',native_facet_legality:'conditional Splus; Sminus rejects',status:'PASS'},null,2));
