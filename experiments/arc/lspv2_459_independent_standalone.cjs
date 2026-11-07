#!/usr/bin/env node
/* LSPV-2/459: independent standalone binary-tree OR-fold SAT verifier.
 * Runs self-contained original-source reconstruction and independent DPLL.
 * No Python imports or fixture file; NOT a native FLMV machine execution.
 */
'use strict';
const crypto = require('node:crypto');
let checks=0,guestCalls=0,fixtures=0;
function ck(x,why){checks++;if(!x)throw new Error(why);}
function bits(n){return Array.from({length:1<<n},(_,i)=>Array.from({length:n},(_,j)=>(i>>>(n-j-1))&1));}
function parity(vs,rhs){return bits(vs.length).filter(v=>v.reduce((a,b)=>a^b,0)!==rhs).map(v=>vs.map((x,j)=>v[j]?-x:x));}
function pin(x,value,p,q){let lit=value?x:-x;return [[lit,p,q],[lit,p,-q],[lit,-p,q],[lit,-p,-q]];}
function xor2(x,y,r,p){return parity([x,y],r).flatMap(c=>[c.concat([p]),c.concat([-p])]);}
function fixture(h,seed,unsat){
  let l=Array.from({length:h+1},()=>[]),leaves=[];
  for(let v=1;v<=h;v++)if(2*v>h)leaves.push(v);
  let next=h,lh=0,ix=0;
  for(const v of leaves){const b=(v*7+seed*3+Math.floor(v/3))&1;lh^=b;let p=next++,q=next++;l[v].push(...pin(v-1,b,p,q));}
  for(let v=2;v<=h;v++)if(2*v<=h){let r=(v+seed)&1;ix^=r;l[v].push(...parity([v-1,2*v-1,2*v],r));}
  let root=lh^ix^(unsat?1:0);l[1].push(...xor2(1,2,root,next++));
  let flat=l.slice(1).flat(),serial=flat.map(c=>c.join(',')).join(';');
  return {l,flat,sha:crypto.createHash('sha256').update(serial).digest('hex'),vars:next-1,root};
}
function sat(cnf){
 function rec(clauses,assign){
  for(;;){let simplified=[],forced=0;
   for(const clause of clauses){let pending=[],ok=false;
    for(const lit of clause){let x=Math.abs(lit);if(assign.has(x)){if(assign.get(x)===(lit>0)){ok=true;break;}}else pending.push(lit);}
    if(ok)continue;
    if(!pending.length)return false;
    if(pending.length===1)forced=pending[0];
    simplified.push(pending);
   }
   if(!simplified.length)return true;
   if(!forced){let x=Math.abs(simplified[0][0]);return rec(simplified,new Map([...assign,[x,true]]))||rec(simplified,new Map([...assign,[x,false]]));}
   assign.set(Math.abs(forced),forced>0);clauses=simplified;
  }
 }
 return rec(cnf,new Map());
}
function tableCheck(v,h,local){
 const children=[2*v,2*v+1].filter(k=>k<=h);
 const sub=new Map(children.map(c=>[c,tableCheck(c,h,local)]));
 const pins=v===1?[null]:[0,1],out=[];
 for(const b of pins){
  let pairAnswer=false;
  for(const childBits of bits(children.length)){
   if(children.some((c,j)=>!sub.get(c)[childBits[j]]))continue;
   let all=local[v].map(x=>x.slice());
   if(b!==null)all.push([b?(v-1):-(v-1)]);
   children.forEach((c,j)=>all.push([childBits[j]?(c-1):-(c-1)]));
   if(sat(all))pairAnswer=true;
  }
  let guest=local[v].map(x=>x.slice());
  for(const c of children)for(let a=0;a<2;a++)if(!sub.get(c)[a])guest.push([a?-(c-1):(c-1)]);
  if(b!==null)guest.push([b?(v-1):-(v-1)]);
  let folded=sat(guest);guestCalls++;
  ck(folded===pairAnswer,'OR fold versus full child compatibility at h='+h+' v='+v);
  out.push(folded);
 }
 return out;
}
const hashes={
  3:[
   ['4162a57b48949855d85398184618392a9952e3f5c36eb9e472d3890ab0631576','30f49531852caef453cf8b6f4f8f61c74fe65a075715cfc68c0636e71d318328'],
   ['eb73978ce4b92fbd89c906bb2482dafbc5ed5d044dcd0b6057724067a04cbecb','6471966065ae316e5f38f20fe1578e2414753b7c97cdb84c51db55af9a903158']
  ],
  7:[
   ['6a12d8aff5718335f82eff1a69fde93d6772e497666b1c817b0fcbcb31cafeda','38f8b15e909e476942156e49975b58f34bd76e17ae5237d013129a150b889848'],
   ['bba85ea57449d6b274f7a943107a662049ab98afe4534f627a1c5238977e9bb5','7bc9f8b8a53d2732cfd14cc380cd86d964463d73153ac32e658c38d172de1c63']
  ],
  15:[
   ['46f74141a50540ece08dc6249416a147e32fafe6b0322a44d014fbc92885f346','9e0cfb60f03f3558365679bbc03f1af8ef07baa1502b129754a17a81245ebda8'],
   ['cf264b35c2c23c9b296748b9de3cf82663afbace13101da149ed5030efa15239','3dd07da69835ca8c37518c60d53cdf85800f3ad8ee60ca49d53f2cd4fc50c86c']
  ]
};
for(const h of [3,7,15])for(let seed=0;seed<6;seed++)for(const unsat of [false,true]){
 fixtures++;const f=fixture(h,seed,unsat);
 ck(f.sha===hashes[h][seed%2][unsat?1:0],'independently computed original source SHA');
 ck(f.vars===2*h+1,'source variable count');
 ck(f.flat.length===4*h,'source clause count');
 for(const c of f.flat){ck(c.length===3,'source clause not width three');ck(new Set(c.map(x=>Math.abs(x))).size===3,'source clause repeated variable');}
 const joined=tableCheck(1,h,f.l)[0],whole=sat(f.flat);
 ck(joined===whole,'join differs from whole formula SAT');
 ck(whole===!unsat,'expected SAT/UNSAT parity polarity differs');
}
const f=fixture(3,0,true);
ck(!sat(f.flat),'UNSAT parent negative control');
ck(sat(f.l[2])&&sat(f.l[3]),'each child-local formula should be SAT');
ck(sat(f.l[1]),'a forged all-true child interface changes the root result');
ck(guestCalls===564,'guest call count must be 564');
console.log(JSON.stringify({status:'PASS',assertions:checks,original_strict3cnf_sources:fixtures,sat_sources:18,unsat_sources:18,OR_folded_guest_calls:guestCalls,native_FLMV_execution:false},null,2));
