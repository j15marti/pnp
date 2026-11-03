'use strict';
// LSPV-4 371. Deterministic, dependency-free independent compact control.
// node lspv4_371_tseitin_virtual_hamming_compact.js
const assert=require('node:assert/strict');
function K4(){let e=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);return [4,e];}
function K33(){let e=[];for(let a=0;a<3;a++)for(let b=3;b<6;b++)e.push([a,b]);return [6,e];}
function cube(){let e=[];for(let a=0;a<8;a++)for(let j=0;j<3;j++){let b=a^(1<<j);if(a<b)e.push([a,b]);}return [8,e];}
function prism(k){let e=[];for(let s=0;s<2;s++)for(let j=0;j<k;j++)e.push([s*k+j,s*k+(j+1)%k]);for(let j=0;j<k;j++)e.push([j,k+j]);return [2*k,e];}
function make(h,E,odd){let inc=Array.from({length:h},()=>[]);E.forEach(([u,v],id)=>{inc[u].push(id+1);inc[v].push(id+1);});
let clauses=[];
for(let v=0;v<h;v++){let ids=inc[v].sort((a,b)=>a-b);assert.equal(ids.length,3);
for(let a=0;a<8;a++){let bits=[a>>2&1,a>>1&1,a&1];
if((bits[0]^bits[1]^bits[2])===(odd&&v===0?1:0))continue;
clauses.push(ids.map((id,i)=>bits[i]?-id:id));}}return clauses;}
function encode(n,C){let w=Math.ceil(Math.log2(n+1));
let out='1'.repeat(w)+'0'+n.toString(2).padStart(w,'0')+C.length.toString(2).padStart(2*w,'0');
for(let cl of C)for(let l of cl)out+=Math.abs(l).toString(2).padStart(w,'0')+(l<0?'1':'0');return out;}
function sat(C,x){return C.every(cl=>cl.some(l=>Boolean((x>>(Math.abs(l)-1))&1)===(l>0)));}
let cases=[],checks=0;
for(let [name,[h,E]] of [['K4',K4()],['K33',K33()],['cube',cube()],['prism5',prism(5)],['prism6',prism(6)]]) {
  let n=E.length,F0=make(h,E,false),F1=make(h,E,true);
  let bits0=encode(n,F0),bits1=encode(n,F1);
  assert.equal(bits0.length,bits1.length);
  assert.equal([...bits0].filter((c,i)=>c!==bits1[i]).length,4);checks+=2;
  let even=0,odd=0,modelHamming=0;
  for(let x=0;x<2**n;x++){let a=sat(F0,x),b=sat(F1,x);
    even+=a;odd+=b;modelHamming+=(a!==b);checks++;}
  let expected=2**(n-h+1);
  assert.equal(even,expected);assert.equal(odd,0);assert.equal(modelHamming,expected);checks+=3;
  cases.push({name,h,n,clauses:4*h,binary_source_bits:bits0.length,
    source_polarity_bit_edits:4,even_models:even,odd_models:odd,
    model_vector_Hamming:expected,exact_mixed_cost_from_prior_341:4*h-1});
}
console.log(JSON.stringify({status:'COMPUTATIONAL, exact proof in report',checks,cases,
B1:'OPEN',B2:'OPEN',B3:'OPEN',P_versus_NP:'OPEN'},null,2));