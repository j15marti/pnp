#!/usr/bin/env node
'use strict';
// LSPV-1/440: independent strict-Resolution closure certificate.
// Derived-port quotient, NOT historical R_mix341 or an original-source checker.
const assert=require('node:assert/strict');
let checks=0;const ok=(p,m)=>{assert.ok(p,m);checks++};
const neg=(i,b)=>b? -i:i, ser=a=>Array.from(new Set(a)).sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);
const key=a=>ser(a).join(','), taut=a=>a.some(x=>a.includes(-x));
const val=(a,m)=>a.some(x=>Boolean(m&(1<<(Math.abs(x)-1)))===(x>0));
const cube=Array.from({length:8},(_,k)=>[(k>>2)&1,(k>>1)&1,k&1]);
const B=cube.filter(b=>(b[0]^b[1]^b[2])===0).map(b=>ser([1,neg(2,b[0]),neg(3,b[1]),neg(4,b[2])]));
const Z=[2,3,4].map(i=>ser([-1,-i]));
const X=cube.filter(b=>(b[0]^b[1])!==b[2]).map(b=>ser([neg(2,b[0]),neg(3,b[1]),neg(5,b[2])]));
function allRes(A) {
 let C=new Map(A.map(c=>[key(c),c])), rounds=[];
 for(let round=0;round<30;round++){
   const known=[...C.values()],news=new Map();
   for(let i=0;i<known.length;i++)for(let j=0;j<i;j++){
     const a=known[i],b=known[j];
     for(const [u,v] of [[a,b],[b,a]])for(const p of u) {
       if(!v.includes(-p))continue;
       const c=ser([...u.filter(x=>x!==p),...v.filter(x=>x!==-p)]);
       if(!taut(c)&&!C.has(key(c)))news.set(key(c),c);
     }
   }
   rounds.push(news.size);for(const [k,v] of news)C.set(k,v);
   if(!news.size)break;
 }
 // Certify closure under every ordered pair and every complementary pivot.
 for(const a of C.values())for(const b of C.values())for(const p of a){
   if(!b.includes(-p))continue;
   const c=ser([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
   if(!taut(c))ok(C.has(key(c)),'missing resolvent');
 }
 return {C,rounds};
}
const a=allRes([...B,...Z]),b=allRes([...B,...Z,...X]);
ok(a.C.size===13&&JSON.stringify(a.rounds)==='[3,3,0]','4var');
ok(b.C.size===87&&JSON.stringify(b.rounds)==='[15,36,25,0]','5var');
const t4=cube.filter(v=>(v[0]^v[1]^v[2])===1).map(v=>ser([-1,neg(2,v[0]),neg(3,v[1]),neg(4,v[2])]));
const t3=cube.filter(v=>(v[0]^v[1]^v[2])===0).map(v=>ser([neg(1,v[0]),neg(4,v[1]),neg(5,v[2])]));
ok(t4.every(c=>!a.C.has(key(c))),'4 missing');
ok(t3.filter(c=>!b.C.has(key(c))).length===1,'5 missing count');
ok(!b.C.has(key([-1,-4,5])),'target absent');
let models4=0,models5=0;
for(let m=0;m<16;m++){
 if(![...B,...Z].every(c=>val(c,m)))continue;
 models4++;ok(t4.every(c=>val(c,m)),'row4 entailment');
}
for(let m=0;m<32;m++){
 if(X.every(c=>val(c,m)))ok(Boolean(m&16)===(Boolean(m&2)!==Boolean(m&4)),'X exact');
 if(![...B,...Z,...X].every(c=>val(c,m)))continue;
 models5++;ok(t3.every(c=>val(c,m)),'row3 entailment');
}
ok(models4===5&&models5===5,'models');
ok(!val([-1,-4],9),'corruption assignment'); // g=1,w3=1 invalidates owner facet
console.log(JSON.stringify({status:'PASS',checks,axioms4:7,closure4:a.C.size,rounds4:a.rounds,axioms5:11,closure5:b.C.size,rounds5:b.rounds,models4,models5,missingCanonical:[-1,-4,5],closure4Clauses:[...a.C.values()].sort((x,y)=>key(x).localeCompare(key(y))),closure5Clauses:[...b.C.values()].sort((x,y)=>key(x).localeCompare(key(y))),scope:'restricted strict RES only; historical mixed checker NOT executed'},null,2));
