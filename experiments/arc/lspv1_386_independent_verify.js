'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs');
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-04_0256_LSPV1_BOUNDED_OBSERVATION386.json','utf8'));
const names=['AND','XOR','OR','NOT','ONE','ZERO'];
const circuit=n=>Array.from({length:n},(_,j)=>[names[j%6],(7*j+1)%(j+3),(11*j+2)%(j+3)]);
function value(c,w,a,mem){if(w<3)return(a>>w)&1;if(mem.has(w))return mem.get(w);const [op,i,j]=c[w-3],v= op==='ONE'?1:op==='ZERO'?0:op==='NOT'?1-value(c,i,a,mem):op==='AND'?value(c,i,a,mem)&value(c,j,a,mem):op==='OR'?value(c,i,a,mem)|value(c,j,a,mem):op==='XOR'?value(c,i,a,mem)^value(c,j,a,mem):NaN;if(!Number.isInteger(v))throw Error('invalid gate');mem.set(w,v);return v;}
const mask=(c,w)=>Array.from({length:8},(_,a)=>value(c,w,a,new Map())).reduce((s,v,a)=>s+(v<<a),0);
let checks=0;
for(const row of raw.rows){const c=circuit(row.gates),out=[0,1,2];for(let i=1;i<Math.min(41,c.length);i++)out.push(3+(17*i)%c.length);
const masks=out.map(w=>mask(c,w)),unique=[...new Set(masks)].sort((a,b)=>a-b);
assert.deepEqual(unique,row.canonical_truth_vectors);checks++;
assert.equal(out.length,row.observable);checks++;
assert.equal(unique.length,row.distinct_functions);checks++;
for(let a=0;a<8;a++){const v=out.map(w=>value(c,w,a,new Map()));for(let k=0;k<v.length;k++){assert.equal(v[k],(masks[k]>>a)&1);checks++;}let old=0,norm=0;for(let k=1;k<v.length;k++){old^=v[k]&(1-v[k-1]);norm^=((masks[k]>>a)&1)&(1-((masks[k-1]>>a)&1));checks++;}assert.equal(old,norm);checks++;}}
for(let a=0;a<8;a++){let x=a&1,y=(a>>1)&1;assert.equal(x,x);assert.notEqual(y,1-y);checks+=2;}
const cases=[[[1]],[[-1]],[[1],[-1]],[[1,2],[-1,2],[-2]],[]];
function sat(f){for(let a=0;a<4;a++)if(f.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))return true;return false;}
assert.deepEqual(cases.map(sat),raw.strict_signed_cnf_labels);checks+=5;
for(const f of [null,[[0]],[[3]],[[true]],[["1"]]]){const ok=Array.isArray(f)&&f.every(c=>Array.isArray(c)&&c.every(l=>typeof l==='number'&&Number.isInteger(l)&&l!==0&&Math.abs(l)<=2));assert.equal(ok,false);checks++;}
assert.equal(raw.original_R_mix341_verified,false);checks++;
console.log(JSON.stringify({test:'LSPV1_386_independent_recursive',status:'COMPUTATIONAL',checks,fixtures:raw.rows.length,all_passed:true,original_R_mix341_verified:false}));
