'use strict';
// LSPV-3/481: reproducible proper 3-CNF guarded-unit projection test.
// Distinct semantic source test, NOT historical R_mix341 checker.
const assert=require('node:assert/strict');
let checks=0, negatives=0;
function ck(p,m){checks++;assert.ok(p,m);}
function valid(F,n){for(const c of F){ck(c.length===3,'strict 3');ck(new Set(c.map(Math.abs)).size===3,'proper');ck(c.every(t=>Number.isSafeInteger(t)&&Math.abs(t)>=1&&Math.abs(t)<=n),'range');}}
function guard(F,n){valid(F,n);const z=n+F.length+1,G=[];F.forEach(([a,b,c],i)=>{const h=n+i+1;G.push([a,b,h],[-h,c,z]);});return {G,z};}
function holds(C,x){return C.some(l=>x[Math.abs(l)-1]===(l>0));}
function sat(F,x){return F.every(c=>holds(c,x));}
function parityK4(q){const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],F=[];for(let v=0;v<4;v++){const is=E.map(([a,b],i)=>a===v||b===v?i+1:0).filter(Boolean);for(let t=0;t<8;t++)if(((t&1)^((t>>1)&1)^((t>>2)&1))!==q[v])F.push(is.map((i,j)=>(t&(1<<j))?-i:i));}return F;}
function test(F,n,name,full){const {G,z}=guard(F,n),tot=[0,0];for(let x=0;x<2**n;x++){const bits=Array.from({length:n},(_,j)=>!!(x&(1<<j)));const f=sat(F,bits);for(const zb of [false,true]){let possible=true;for(let j=0;j<F.length;j++){let local=false;for(const aj of [false,true]){const b=[...bits,...Array(F.length).fill(false),zb];b[n+j]=aj;if(holds(G[2*j],b)&&holds(G[2*j+1],b))local=true;checks+=2;}if(!local)possible=false;}ck(possible===(zb||f),name+' projection');tot[Number(zb)]+=Number(possible);}}ck(tot[1]===2**n,'all x, z=1');if(full){let count=[0,0];for(let a=0;a<2**z;a++){const b=Array.from({length:z},(_,j)=>!!(a&(1<<j)));if(sat(G,b))count[Number(b[z-1])]++;}ck((count[0]>0)===(tot[0]>0),'enumerated z=0');ck(count[1]>0,'enumerated z=1');}return {name,n,m:F.length,guard_vars:z,guard_clauses:G.length,source_models:tot[0],guard_z1_projection:tot[1],entails_z:tot[0]===0};}
const all8=Array.from({length:8},(_,b)=>[1,2,3].map((v,j)=>(b&(1<<j))?-v:v));
const rows=[];for(let k=0;k<=8;k++)rows.push(test(all8.slice(0,k),3,'prefix'+k,true));
rows.push(test(parityK4([1,0,0,0]),6,'k4_odd',false));
rows.push(test(parityK4([0,0,0,0]),6,'k4_even',false));
for(const bad of [[[1,1,2]],[[1,2]],[[1,2,4]],[[1,-1,2]]]){try{guard(bad,3);throw Error('malformed accepted');}catch(e){if(e.message==='malformed accepted')throw e;negatives++;}}
ck(rows[8].entails_z&&!rows[1].entails_z,'complete eight-clause control');
ck(rows[9].entails_z&&!rows[10].entails_z,'Tseitin parity controls');
console.log(JSON.stringify({artifact:'LSPV3_481_GUARDED_ONE_PORT',checks,negatives,rows,native_checker_executed:false},null,2));
