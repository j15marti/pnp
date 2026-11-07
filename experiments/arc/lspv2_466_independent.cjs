#!/usr/bin/env node
'use strict';
// Independent model checker of two-call shifted index and epoch-stamped work cells.
// Abstract sparse host semantics only; not native FLMV instruction execution.
const assert=require('node:assert/strict');
const Q=2, epochBits=2, offset=2, stride=4;
let assertions=0, traces=0, operations=0;
function execute(seq1,seq2){
  const memory=new Map();
  let physicalHead=0, currentEpoch=0, physicalIndex=new Set(), logicalIndex=new Set(), hostIndexHead=offset, guestIndexHead=0;
  let guestWork=new Map(),guestHead=0,peakGuest=0,peakHost=0;
  function setOne(map,pos,bit){if(bit)map.set(pos,1);else map.delete(pos)}
  function getTag(){let tag=0;for(let k=0;k<epochBits;k++)tag+=(memory.get(physicalHead+k)||0)*(2**k);return tag}
  function read(){let v=getTag()===currentEpoch?(memory.get(physicalHead+epochBits)||0):0;let w=guestWork.get(guestHead)||0;assert.equal(v,w);assertions++;}
  function check(){assert.equal(physicalHead,guestHead*stride);assertions++;assert.equal(hostIndexHead,guestIndexHead+offset);assertions++;
    assert.equal(physicalIndex.size,logicalIndex.size);assertions++;
    for(const j of logicalIndex){assert(physicalIndex.has(j+offset));assertions++}
    assert(peakHost<(peakGuest+1)*stride);assertions++;
  }
  for(const sq of [seq1,seq2]){
    currentEpoch++;
    // Paid sequential index clearing, then a native zero-address work jump.
    physicalIndex=new Set();logicalIndex=new Set();hostIndexHead=offset;guestIndexHead=0;
    physicalHead=0;guestWork=new Map();guestHead=0;
    for(const op of sq){
      if(op==='r')read();
      if(op==='1'||op==='0'){
        const value=op==='1'?1:0;
        for(let k=0;k<epochBits;k++)setOne(memory,physicalHead+k,(currentEpoch>>k)&1);
        setOne(memory,physicalHead+epochBits,value);setOne(guestWork,guestHead,value);
      }
      if(op==='>'){physicalHead+=stride;guestHead++;}
      if(op==='<') {if(guestHead>0){physicalHead-=stride;guestHead--;}}
      if(op==='i') {physicalIndex.add(hostIndexHead);logicalIndex.add(guestIndexHead);}
      if(op==='z') {physicalIndex.delete(hostIndexHead);logicalIndex.delete(guestIndexHead);}
      if(op==='I') {hostIndexHead++;guestIndexHead++;}
      if(op==='J') {if(guestIndexHead>0){hostIndexHead--;guestIndexHead--;}}
      if(op==='!'){
        const guestAddr=[...logicalIndex].reduce((sum,p)=>sum+2**p,0);
        const hostAddr=[...physicalIndex].reduce((sum,p)=>sum+2**p,0);
        assert.equal(hostAddr,guestAddr*stride);assertions++;
        physicalHead=hostAddr;guestHead=guestAddr;
        physicalIndex.clear();logicalIndex.clear();
      }
      peakGuest=Math.max(peakGuest,guestHead);
      peakHost=Math.max(peakHost,physicalHead+epochBits);
      read();check();operations++;
    }
  }
  traces++;
}
const ops=['1','0','r','>','<','i','z','I','J','!'];
// Exhaustively check 10^4 two-call traces with 2 operations in each call.
for(let a=0;a<ops.length;a++) for(let b=0;b<ops.length;b++)
 for(let c=0;c<ops.length;c++) for(let d=0;d<ops.length;d++)
  execute([ops[a],ops[b]],[ops[c],ops[d]]);
console.log(JSON.stringify({status:'PASS',traces,operations,assertions,model:'independent finite sparse work/index semantics',epochBits,stride}));
