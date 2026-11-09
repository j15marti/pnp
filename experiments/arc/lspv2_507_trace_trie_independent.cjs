'use strict';
/* Independent JS finite replay of LSPV-2/507 trace-cylinder partition.
 * Model is a special compact K4 Tseitin grammar; not a general SAT solver.
 */
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const E = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const HEADER = [1,0,1,0];
let checked=0;
function signedCNF(charges) {
  const cs=[];
  for(let v=0;v<4;v++) {
    const incidence=[];
    for(let j=0;j<6;j++) if(E[j].includes(v)) incidence.push(j+1);
    assert.equal(incidence.length,3);
    for(let state=0;state<8;state++) {
      const bits=[(state>>2)&1,(state>>1)&1,state&1];
      if(((bits[0]^bits[1]^bits[2])!==charges[v])) cs.push(bits.map((b,i)=>b?-incidence[i]:incidence[i]));
    }
  }
  assert.equal(cs.length,16);return cs;
}
function brute(clauses) {
 for(let a=0;a<64;a++) {
  let sat=true;
  for(const c of clauses) {
    if(!c.some(l=>{const x=((a>>(Math.abs(l)-1))&1)===1;return l>0?x:!x;})) {sat=false;break;}
  }
  if(sat)return true;
 }
 return false;
}
function nativeGuest(source, scan=false) {
  const observations=[];
  const n=source.length;
  const read=pos=>{
    if(pos>=n)return 0; // source-invariant blank, no literal address evidence
    const bit=source[pos];observations.push([pos,bit]);return bit;
  };
  if(n<8)return {out:'MALFORMED',observations};
  for(let j=0;j<HEADER.length;j++)if(read(j)!==HEADER[j])return {out:'MALFORMED',observations};
  const first=read(4);
  const order=first?[7,6,5]:[5,6,7];
  let parity=first;
  for(const j of order) parity^=read(j);
  assert.equal(read(4),first);
  assert.equal(read(2**52),0); // safely huge for JS exact integer
  if(scan)for(let j=8;j<n;j++)read(j);
  return {out:parity?'UNSAT':'SAT',observations};
}
class Trie {
 constructor(){this.roots=new Map();this.hits=0;this.misses=0;this.anchors=0;this.lookups=0;this.nodeCount=0;}
 freshNode(){this.nodeCount++;return {p:null,kids:[null,null],out:null,done:false};}
 getOrInsert(len){if(!this.roots.has(len))this.roots.set(len,this.freshNode());return this.roots.get(len);}
 lookup(src){let t=this.roots.get(src.length);while(t){if(t.done){this.hits++;return t.out;}if(t.p===null)break;this.lookups++;t=t.kids[src[t.p]];}this.misses++;return null;}
 insert(len,obs,out,trust){if(!trust)throw new Error('UNAUTHENTICATED');let t=this.getOrInsert(len);
  for(const [p,b] of obs){assert(p<len && p>=0);if(t.done)throw Error('SHORT_TRUSTED');if(t.p===null)t.p=p;if(t.p!==p)throw Error('BAD_NEXT_ADDRESS');if(!t.kids[b])t.kids[b]=this.freshNode();t=t.kids[b];}
  if(t.kids[0]||t.kids[1])throw Error('LATE_TRUSTED');if(t.done)assert.equal(t.out,out);else {t.done=true;t.out=out;this.anchors++;}}
 run(src,scan=false){const cached=this.lookup(src);if(cached!==null)return cached;const {out,observations}=nativeGuest(src,scan);this.insert(src.length,observations,out,true);return out;}
}
function main(){
 for(let charge=0;charge<16;charge++){
   const bit=[0,1,2,3].map(i=>(charge>>i)&1);
   const cnf=signedCNF(bit);assert.equal(brute(cnf),(bit.reduce((x,y)=>x^y,0)===0));checked++;
 }
 const cache=new Trie();const seen=[];
 for(let charge=0;charge<16;charge++){
  const cb=[0,1,2,3].map(i=>(charge>>i)&1);
  for(let suffix=0;suffix<32;suffix++){
   const tail=Array.from({length:16},(_,j)=>((suffix>>j)&1));
   const src=HEADER.concat(cb,tail);
   const actual=cache.run(src), exp=(cb.reduce((x,y)=>x^y,0)===0)?'SAT':'UNSAT';
   assert.equal(actual,exp);seen.push(src);checked++;
  }
 }
 for(const src of seen) {assert.equal(cache.run(src),nativeGuest(src).out);checked++;}
 for(let p=0;p<4;p++) {const src=HEADER.concat([0,0,0,0],Array(16).fill(0));src[p]^=1;assert.equal(cache.run(src),'MALFORMED');checked++;}
 for(const src of [[],[1],[1,0,1],[1,0,1,0,1,0,1]]) {assert.equal(cache.run(src),'MALFORMED');checked++;}
 const misses=cache.misses,hits=cache.hits;
 assert(cache.anchors<=24 && hits>1000);checked+=2;
 const anti=new Trie();
 for(let i=0;i<128;i++){
  const src=HEADER.concat([1,0,0,0],Array.from({length:16},(_,j)=>((i>>j)&1)));
  assert.equal(anti.run(src,true),'UNSAT');checked++;
 }
 assert.equal(anti.hits,0);assert.equal(anti.anchors,128);checked+=2;
 const bad=new Trie();bad.insert(24,[[0,1],[1,0]],'SAT',true);
 assert.throws(()=>bad.insert(24,[[0,1],[2,0]],'UNSAT',true),/BAD_NEXT_ADDRESS/);checked++;
 assert.throws(()=>bad.insert(24,[[0,1]],'SAT',false),/UNAUTHENTICATED/);checked++;
 return {run:507,independent_js_pass:true,checks:checked,source_original_strict3_checks:16,
    cache:{hits:cache.hits,misses:cache.misses,anchor_paths:cache.anchors,explicit_trie_nodes:cache.nodeCount,charged_read_comparisons:cache.lookups},
    fullscan:{anchors:anti.anchors,hits:anti.hits,nodes:anti.nodeCount},
    native_flmv_executed:false,all_input_general_sat:false};
}
console.log(JSON.stringify(main(),null,2));
