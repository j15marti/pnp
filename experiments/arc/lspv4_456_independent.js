/* LSPV-4/456 independently written finite OR-fold virtual-guest byte test.
 * This host JavaScript reconstructs bytes for verification, not in the claimed FLMV wrapper.
 * Run: node lspv4_456_independent.js */
const assert=require('assert');
let checks=0, guestCalls=0, reads=0, labels=[];
const checked=(a,b)=>{assert.deepStrictEqual(a,b);checks++};
function rec(C) {let a=[C.length];for(let l of C){a.push(l<0?1:0,(Math.abs(l)>>8)&255,Math.abs(l)&255)}return a}
function pin(l,u,v){return [[l,u,v],[l,u,-v],[l,-u,v],[l,-u,-v]]}
function gate(p,q,r){return [[p,q,r],[p,q,-r]]}
function sat(clauses){let ids=[...new Set(clauses.flat().map(Math.abs))];for(let m=0;m<2**ids.length;m++){
let vals={};ids.forEach((x,i)=>vals[x]=(m>>i)&1);
if(clauses.every(C=>C.some(x=>vals[Math.abs(x)]===+(x>0))))return true;
}return false}
function caseBlocks(a,t,b) {return [pin(a?1:-1,3,4),
(t?gate(1,2,5).concat(gate(-1,-2,6)):gate(1,-2,5).concat(gate(-1,2,6))),
pin(b?2:-2,7,8)]}
function packedSource(blocks) {let raw=[80,84,72,49,3,1];for(const b of blocks)raw.push(0,2,0,b.length);
let spans=[];for(const B of blocks){let lo=raw.length;for(const C of B)raw.push(...rec(C));spans.push([lo,raw.length])}
return {raw,spans}}
function virtual(root,span,baseCount,extra){let head=[67,78,70,49,0,8,0,baseCount+extra.length],append=extra.flatMap(rec);let size=head.length+span[1]-span[0]+append.length;
return {size,read(j){checks++;reads++;assert(j>=0&&j<size);if(j<8)return head[j];j-=8;
if(j<span[1]-span[0])return root[span[0]+j];return append[j-(span[1]-span[0])];}}}
function run(){for(let a=0;a<2;a++)for(let t=0;t<2;t++)for(let b=0;b<2;b++){
 let blocks=caseBlocks(a,t,b),{raw,spans}=packedSource(blocks);
 let prev={'':true};for(let i=0;i<3;i++){
  let next={};for(const out of (i===2?['']:[0,1])){
    let blockers=[];
    if(i===0){if(!prev[''])blockers=[[]]}
    else for(let v=0;v<2;v++)if(!prev[String(v)])blockers.push([v?-(i===1?1:2):(i===1?1:2)]);
    const pins=out===''?[]:[[out?(i===0?1:2):-(i===0?1:2)]];
    const extra=blockers.concat(pins),v=virtual(raw,spans[i],blocks[i].length,extra);
    const ordinary=[67,78,70,49,0,8,0,blocks[i].length+extra.length,...blocks[i].flatMap(rec),...extra.flatMap(rec)];
    for(let j=v.size-1;j>=0;j--)checked(v.read(j),ordinary[j]);
    for(let j=0;j<v.size;j+=7)checked(v.read(j),ordinary[j]);
    next[String(out)]=sat(blocks[i].concat(extra));guestCalls++;
  }prev=next;
 }
 let expect=sat(blocks.flat()),result=prev[''];checked(result,expect);checked(result,Boolean((a^t)===b));
 labels.push({a,t,b,SAT:result});
}}
run();console.log(JSON.stringify({status:'PASS',cases:labels.length,checks,guestCalls,byteReadOperations:reads,SAT:labels.filter(x=>x.SAT).length,UNSAT:labels.filter(x=>!x.SAT).length,labels},null,2));