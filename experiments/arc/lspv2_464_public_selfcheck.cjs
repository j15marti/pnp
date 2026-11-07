'use strict';
const assert = require('node:assert/strict');
function replay(ops) {
  let pos=0, max=0, work=0n, tape=new Set();
  for (const op of ops) {
    if(op==='R'){pos++;max=Math.max(max,pos);}
    else if(op==='L'){pos=Math.max(pos-1,0);}
    else if(op==='1'){tape.add(pos);}
    else if(op==='0'){tape.delete(pos);}
    else if(op==='J'){
      let address=0n;
      for(const i of tape) address+=1n<<BigInt(i);
      if(address>work) work=address;
      tape.clear();
    } else throw Error('bad guest op');
  }
  let steps=pos, writes=0;
  pos=0;
  for(let i=0;i<=max;i++){
    steps++;
    if(tape.has(i)){writes++;steps++;tape.delete(i);}
    if(i<max){pos++;steps++;}
  }
  steps+=pos;
  assert.equal(tape.size,0);
  assert.ok(steps<=4*(ops.length+1));
  return {steps,writes,work:String(work)};
}
let checks=0;
for(const L of [1,2,4,8,16,32,64,128]){
  let ops=[];
  for(let i=0;i<L;i++){ops.push('1');if(i+1<L)ops.push('R');}
  let x=replay(ops);
  assert.equal(x.writes,L);
  assert.equal(x.work,'0');checks+=3;
}
for(const n of [0,1,2,3,4,5,6]){
  const alphabet=['R','L','1','0','J'];
  const total=5**n;
  for(let num=0;num<total;num++){
    let k=num,ops=[];
    for(let i=0;i<n;i++){ops.push(alphabet[k%5]);k=Math.floor(k/5);}
    replay(ops);checks++;
  }
}
console.log(JSON.stringify({status:'PASS',checks,operationAlphabet:'RL10J',model:'direct index tape; no reset indexed jump'}));
