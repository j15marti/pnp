// LSPV-4/513 independent JavaScript read-transcript and source authentication control.
// Node 16+; NOT an FLMV interpreter and NOT the historical R_mix341 checker.
'use strict';
const assert = require('assert');
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function gamma(x){assert(x>0);let b=x.toString(2);return '0'.repeat(b.length-1)+b;}
function core(){let out=[];for(let v=0;v<4;v++){
 const ids=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
 for(let a=0;a<8;a++){const t=[(a>>2)&1,(a>>1)&1,a&1];if((t[0]^t[1]^t[2])!==(v===0?1:0))out.push(ids.map((id,i)=>[id,t[i]]));}}
 return out;}
const CORE=core();
function sat(phi,z){return phi.every(cl=>cl.some(([i,p])=>p?z[i]:!z[i]));}
function encode(phi,d){let n=d.length-1,m=phi.length;let cls=CORE.map(cl=>cl.map(pair=>pair.slice()));
 for(let j=0;j<m;j++){let c=phi[j];let violated=!c.some(([i,p])=>p?d[1+i]:!d[1+i]);let w=Number(Boolean(d[0]&&violated));let b=7+3*j;cls.push([[b,w],[b+1,0],[b+2,0]]);}
 for(let i=0;i<d.length;i++){let b=7+3*m+3*i;cls.push([[b,d[i]],[b+1,0],[b+2,0]]);}
 let nv=6+3*(m+n+1),W=nv.toString(2).length;
 let head='10100101'+gamma(m)+gamma(n+1)+gamma(nv)+gamma(cls.length);
 let s=head, tags=[],pads=[],p=head.length;
 cls.forEach((cl,j)=>cl.forEach(([v,sign],i)=>{s+=v.toString(2).padStart(W,'0')+sign;
 if(i===0&&j>=16+m)tags.push(p+W);
 if(i===0&&j>=16&&j<16+m)pads.push(p+W);
 p+=W+1;}));
 s+='01';return {s,tags,pads,clauses:cls};}
function bits(k){let out=[];for(let mask=0;mask<(1<<k);mask++){out.push(Array.from({length:k},(_,j)=>(mask>>(k-j-1))&1));}return out;}
function countModels(clauses,n){let s=0;for(const z of bits(n)){if(clauses.every(cl=>cl.some(([v,sign])=>sign?!z[v-1]:!!z[v-1])))s++;}return s;}
function runCase(name,phi){let n=1+Math.max(...phi.flat().map(x=>x[0])),z=Array(n+1).fill(0);
 const anchor=encode(phi,z), skip=new Set(anchor.tags), observed=Array.from({length:anchor.s.length},(_,i)=>i).filter(i=>!skip.has(i));
 let allowed=new Set([...anchor.tags,...anchor.pads]);let compatible=0,distinct=new Set();
 for(let d of bits(n+1)){let src=encode(phi,d);distinct.add(src.s);assert.equal(src.s.length,anchor.s.length);
 for(let j=0;j<src.s.length;j++)if(!allowed.has(j))assert.equal(src.s[j],anchor.s[j]);
 if(observed.every(i=>src.s[i]===anchor.s[i]))compatible++;}
 let count=bits(n).filter(z=>sat(phi,z)).length;
 assert.equal(distinct.size,1<<(n+1));assert.equal(compatible,(1<<n)+count);
 assert.equal(anchor.tags.length,n+1);assert.equal(anchor.pads.length,phi.length);
 let bad=anchor.s.slice(0,-1);assert.notEqual(bad.length,anchor.s.length);
 let corrupted=anchor.s.split('');corrupted[0]=corrupted[0]==='0'?'1':'0';
 assert.notEqual(corrupted.join(''),anchor.s);
 return {name,n,m:phi.length,bits:anchor.s.length,sat:count,compatible,q:1<<(n+1),non_affine:(compatible&(compatible-1))!==0};}
const cases=[
 ['one_z',[[[0,1]]]],['contradiction',[[[0,1]],[[0,0]]]],
 ['two_or',[[[0,1],[1,1]]]],['two_units',[[[0,1]],[[1,1]]]],
 ['xor_unsat_2',[[[0,1],[1,1]],[[0,0],[1,1]],[[0,1],[1,0]],[[0,0],[1,0]]]]
];
let r=cases.map(([name,f])=>runCase(name,f));
assert.equal(CORE.length,16);assert.equal(countModels(CORE,6),0);
let changed=CORE.map(cl=>cl.map(v=>v.slice()));changed[0][0][1]^=1;
assert.equal(countModels(changed,6),2);assert.equal(r[0].compatible,3);
console.log(JSON.stringify({status:'PASS',cases:r,corrupt_core_models:2,method:'Independent original strict3 source encoding and literal read-value transcript enumeration',limitations:'symbolic reads; not native FLMV execution'},null,2));
