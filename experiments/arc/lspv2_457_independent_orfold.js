'use strict';
// Independent bitmask reference checker, not a native FLMV machine replay.
const assert = require('node:assert/strict');
let tests = 0, cases = 0, satCases = 0, unsatCases = 0, foldedCalls = 0, pairCalls = 0;
const check = (condition, message) => { assert.ok(condition, message); tests++; };
const bools = k => Array.from({length: 1 << k}, (_,i) => i);
const bit = (a,j) => (a >> j) & 1;
const holds = (clause, mask) => clause.some(l => bit(mask, Math.abs(l)-1) === (l>0 ? 1 : 0));
const sat = (clauses,n) => bools(n).some(mask => clauses.every(c => holds(c,mask)));
const forbid = (names,a) => names.map((v,j) => bit(a,j) ? -v : v);
function experiment(h,w,seed,contradict){
  const z = Array.from({length:h+1}, (_,i)=>i===0||i===h ? [] :
    Array.from({length:w}, (_,j)=>(i-1)*w+j+1));
  const block = [];
  for(let i=0;i<h;i++){
    const names = [...z[i],...z[i+1],h*w+2*i+1,h*w+2*i+2];
    const clauses=[];
    for(let j=0;j<5;j++){
      const shift = (j+seed)%names.length;
      const three = [names[shift],names[(shift+1)%names.length],names[(shift+2)%names.length]];
      clauses.push(three.map((v,k)=>((seed+j+k)&1)?v:-v));
    }
    block.push(clauses);
  }
  if(contradict){
    const names = [...new Set(block[0].flat().map(Math.abs))].slice(0,3);
    for(let a=0;a<8;a++) block[0].push(forbid(names,a));
  }
  const parent=block.flat();
  const n=Math.max(...parent.flat().map(Math.abs));
  check(parent.every(c=>c.length===3 && new Set(c.map(Math.abs)).size===3),'strict source ternary');
  let old=new Map([['0',true]]), fresh=new Map([['0',true]]);
  for(let i=0;i<h;i++){
    const incoming=z[i], outgoing=z[i+1], slow=new Map(), fast=new Map();
    for(const b of bools(outgoing.length)){
      const bkey=String(b);
      let v=false;
      for(const a of bools(incoming.length)){
        const oldval=old.get(String(a));
        if(oldval){
          const units=[...incoming.map((id,j)=>[bit(a,j)?id:-id]),
                       ...outgoing.map((id,j)=>[bit(b,j)?id:-id])];
          v ||= sat([...block[i],...units],n);
        }
      }
      slow.set(bkey,v);
      const disabled=bools(incoming.length).filter(a=>!fresh.get(String(a))).map(a=>forbid(incoming,a));
      const pins=outgoing.map((id,j)=>[bit(b,j)?id:-id]);
      const child=[...block[i],...disabled,...pins];
      fast.set(bkey,sat(child,n));
      foldedCalls++;
      check(fast.get(bkey)===v, 'folded call must match pair enumeration');
    }
    pairCalls+=(1 << (incoming.length+outgoing.length));
    old=slow; fresh=fast;
  }
  const label=sat(parent,n);
  check(fresh.get('0')===label,'parent vs folded decision');
  if(label)satCases++;else unsatCases++;
  cases++;
}
for(const [h,w] of [[2,1],[3,1],[3,2],[4,1],[4,2]]) {
  for(let s=0;s<4;s++) experiment(h,w,s,(s%2)===1);
}
for(let w=1;w<=3;w++) for(const a of bools(w)) for(const b of bools(w)){
  const c=forbid(Array.from({length:w},(_,i)=>i+1),a);
  check(holds(c,b)===(a!==b),'exact membership blocker');
}
check(cases===20 && satCases>0 && unsatCases>0,'both labels checked');
console.log(JSON.stringify({status:'PASS',cases,satCases,unsatCases,checks:tests,foldedCalls,pairCalls}));
