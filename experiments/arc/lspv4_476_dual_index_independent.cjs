'use strict';
// Independent host-language source-read verifier. No native FLMV execution.
const assert = require('node:assert/strict');
const graph = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function clauses(odd){
  const output=[];
  for(let vertex=0;vertex<4;vertex++){
    const incidence=graph.map(([a,b],i)=>(a===vertex||b===vertex)?i+1:0).filter(Boolean);
    for(let code=0;code<8;code++){
      const p=((code&1)!==0)+((code&2)!==0)+((code&4)!==0);
      if ((p&1)===(vertex===0 ? odd:0))continue;
      output.push(incidence.map((id,j)=>(code&(1<<j))?-id:id));
    }
  }
  assert.equal(output.length,16);return output;
}
function dimacs(clauses){return 'p cnf 6 16\n'+clauses.map(a=>a.join(' ')+' 0\n').join('');}
function countModels(cl){let n=0;for(let mask=0;mask<64;mask++)if(cl.every(c=>c.some(l=>((mask>>(Math.abs(l)-1))&1)===(l>0?1:0))))n++;return n;}
function sourceBits(text){const out=[];for(const byte of Buffer.from(text,'utf8'))for(let j=0;j<8;j++)out.push((byte>>j)&1);return out;}
function sourceRead(tape,bits,address){
  assert.equal(tape.pos,0);
  let k=0,encoded=0;
  do{const b=Math.floor(address/2**k)%2;
    if(b){encoded+=2**k;tape.writes++;}
    if(address>=2**(k+1)){tape.pos++;tape.moves++;}
    k++;
  }while(2**k<=address);
  assert.equal(encoded,address);
  const value=bits[address];tape.jumps++;tape.moves+=tape.pos;tape.pos=0;
  return value;
}
function singleTrace(H,requestAddresses,repeat,bits){
  const sourceIndex={pos:0,moves:0,writes:0,jumps:0};
  const guestIndex={pos:H,moves:0,writes:0,jumps:0};
  const singleIndex={pos:H,moves:0,writes:0,jumps:0};
  let q=0;
  for(let cycle=0;cycle<repeat;cycle++)for(const p of requestAddresses){
    const expected=bits[p];const a=sourceRead(sourceIndex,bits,p);
    assert.equal(guestIndex.pos,H);
    singleIndex.moves+=H;singleIndex.pos=0;
    const b=sourceRead(singleIndex,bits,p);
    singleIndex.moves+=H;singleIndex.pos=H;
    assert.equal(a,expected);assert.equal(b,expected);q++;
  }
  assert.equal(sourceIndex.jumps,q);assert.equal(singleIndex.jumps,q);
  assert.equal(singleIndex.moves-sourceIndex.moves,2*H*q);
  return {q,sourceMoves:sourceIndex.moves,sharedMoves:singleIndex.moves,avoided:2*H*q};
}
let checks=0,totalRead=0,totalSrc=0,totalSingle=0,totalAvoid=0,cases=0;
for(const odd of [0,1]){
  const cnf=clauses(odd);assert.equal(countModels(cnf),odd?0:8);checks++;
  const doc=dimacs(cnf);assert.equal(doc.split('\n').length,18);checks++;
  const bits=sourceBits(doc);
  for(const head of [0,1,8,32,128,512])for(const d of [1,3,8,16])for(const r of [1,2,5]){
    const req=Array.from({length:d},(_,i)=>(7+29*i)%bits.length);
    const result=singleTrace(head,req,r,bits);
    const expectedMoves=req.reduce((sum,p)=>sum+2*(Math.floor(Math.log2(p||1))),0)*r;
    assert.equal(result.sourceMoves,expectedMoves);
    checks+=result.q*4+4;
    totalRead+=result.q;totalSrc+=result.sourceMoves;
    totalSingle+=result.sharedMoves;totalAvoid+=result.avoided;cases++;
  }
}
assert.equal(cases,144);
console.log(JSON.stringify({cases,checks,totalRead,totalSrc,totalSingle,totalAvoid,
 meaning:'independent finite JavaScript source-index emulation; exact guest-high-head comparisons; not native FLMV'},null,2));
