#!/usr/bin/env node
"use strict";
/*
LSPV-4 350, fixed Rmix341 with source-independent VARDEF.
Exhaustive source-once binary-tree lower bounds for G342 and fresh splits.
Zero-premise DEF and unary conversions are excluded from a hypothetical
q=m-1 proof by the source-ancestry Euler identity.
This is a LOWER-BOUND RELAXATION: free exact aliases and output-support
AND3 (even if the premise-union has >3 variables).
Node cost is NOT computational/search cost. No B3 or P-vs-NP proof.
Run: node experiments/arc/lspv4_350_mixed_split_floor_primary.js [output.json]
*/
const fs=require("fs"), assert=require("assert");
const V=7, N=1<<V;
const G=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]];
function cvalue(c,a) { return c.some(l=>((a>>>(Math.abs(l)-1))&1)===(l>0?1:0)); }
function fvalue(f,a) { return f.every(c=>cvalue(c,a)); }
function models(f) { let n=0;for(let a=0;a<N;a++)if(fvalue(f,a))n++;return n; }
function truth(c) {let s="";for(let a=0;a<N;a++)s+=cvalue(c,a)?"1":"0";return s;}
const clause=new Map(), affine=new Map(), affineReverse=new Map(), supportCache=new Map(), mergeCache=new Map();
for(let mask=0;mask<3**V;mask++){let p=mask,c=[];for(let v=1;v<=V;v++){let digit=p%3;p=(p-digit)/3;if(digit)c.push(digit===1?v:-v);}clause.set(truth(c),c);}
for(let coeff=0;coeff<N;coeff++)for(let rhs=0;rhs<2;rhs++){
 let s="";for(let a=0;a<N;a++){let b=0;for(let v=0;v<V;v++)if(coeff&(1<<v))b^=(a>>v)&1;s+=b===rhs?"1":"0";}
 affine.set(s,[coeff,rhs]);affineReverse.set(coeff+","+rhs,s);
}
function essentialSupport(s){
 if(supportCache.has(s))return supportCache.get(s);
 let w=0;for(let v=0;v<V;v++){for(let a=0;a<N;a++){if(s[a]!==s[a^(1<<v)]){w++;break;}}}
 supportCache.set(s,w);return w;
}
function merge(a,b){
 const key=a+"/"+b; if(mergeCache.has(key))return mergeCache.get(key);
 const out=new Set(), meet=Array.from({length:N},(_,i)=>a[i]==="1"&&b[i]==="1"?"1":"0").join("");
 if(essentialSupport(meet)<=3)out.add(meet);
 const ax=affine.get(a),bx=affine.get(b);
 if(ax&&bx)out.add(affineReverse.get((ax[0]^bx[0])+","+(ax[1]^bx[1])));
 const ca=clause.get(a),cb=clause.get(b);
 if(ca&&cb)for(let p=1;p<=V;p++){
  if(!(ca.includes(p)&&cb.includes(-p)||ca.includes(-p)&&cb.includes(p)))continue;
  const r=Array.from(new Set(ca.concat(cb).filter(l=>Math.abs(l)!==p)));
  if(r.some(l=>r.includes(-l)))continue; // reject tautological resolvent
  out.add(truth(r));
 }
 const result=Array.from(out);mergeCache.set(key,result);return result;
}
function allTreeOutcomes(f){
 const m=f.length, lim=1<<m, d=Array.from({length:lim},()=>new Set());
 for(let i=0;i<m;i++)d[1<<i].add(truth(f[i]));
 const levels=[];for(let k=2;k<=m;k++){let states=0,pairs=0;
  for(let s=1;s<lim;s++){let t=s,n=0;while(t){t&=t-1;n++;}if(n!==k)continue;
   for(let l=(s-1)&s;l;l=(l-1)&s){const r=s^l;if(l>=r)continue;
    for(const a of d[l])for(const b of d[r]){pairs++;for(const x of merge(a,b))d[s].add(x);}
   }
   states+=d[s].size;
  }
  levels.push([k,states,pairs]);
 }
 return {has_false:d[lim-1].has("0".repeat(N)),root_state_count:d[lim-1].size,
    total_states:d.reduce((z,s)=>z+s.size,0),layers:levels,
    candidate_pairs:levels.reduce((z,r)=>z+r[2],0)};
}
function firstSplit(i){const f=G.filter((_,j)=>j!==i).map(c=>[...c]);f.push([...G[i],5],[...G[i],-5]);return f;}
function nested(t){const f=G.slice(1).map(c=>[...c]);let c=[...G[0]];for(let i=0;i<t;i++){f.push([...c,-(5+i)]);c=[...c,5+i];}f.push(c);return f;}
const gamma=x=>2*Math.floor(Math.log2(x))+1;
function encodedBits(f,n){const idbits=Math.ceil(Math.log2(n+1));return gamma(n+1)+gamma(f.length+1)+f.reduce((z,c)=>z+gamma(c.length+1)+c.length*(1+idbits),0);}
function controls(f){const deletion=f.map((_,i)=>models(f.filter((_,j)=>j!==i)));
 let flips=0,sign_fields=0;for(let i=0;i<f.length;i++)for(let j=0;j<f[i].length;j++){
  sign_fields++;const h=f.map(c=>[...c]);h[i][j]*=-1;if(models(h)>0)flips++;
 }
 return {models:models(f),deletion_models:deletion,all_deletions_sat:deletion.every(x=>x>0),signed_occurrences:sign_fields,flip_neighbors_sat:flips,all_sign_flips_sat:flips===sign_fields};
}
function genuineResolution(a,b,p){
 let pa,pb;if(a.includes(p)&&b.includes(-p)){pa=p;pb=-p;}
 else if(a.includes(-p)&&b.includes(p)){pa=-p;pb=p;}
 else throw Error("invalid pivot");
 const r=Array.from(new Set(a.filter(x=>x!==pa).concat(b.filter(x=>x!==pb))));
 if(r.some(l=>r.includes(-l)))throw Error("tautological resolvent");return r.sort((x,y)=>x-y);
}
const resG=[[["S",0],["S",3],4],[["D",0],["S",2],3],
 [["S",5],["S",3],4],[["D",2],["S",4],3],
 [["D",3],["S",1],2],[["D",1],["D",4],1]];
function verifyBase(){
 const D=[];for(const [a,b,p] of resG)D.push(genuineResolution(a[0]==="S"?G[a[1]]:D[a[1]],b[0]==="S"?G[b[1]]:D[b[1]],p));
 assert.deepStrictEqual(D.map(r=>[...r]),[[-3,1],[1],[-3,-2],[-2,-1],[-1],[]]);return D;
}
function liftedProof(f,sourceMap,reverseSplits){
 const d=[];for(const [a,b,p]of reverseSplits)d.push(genuineResolution(a[0]==="S"?f[a[1]]:d[a[1]],b[0]==="S"?f[b[1]]:d[b[1]],p));
 const C=reverseSplits.length-1;const provenance=[];
 for(const [a,b,p]of resG){
  const l=a[0]==="S"?(a[1]===sourceMap.replaced?d[C]:f[sourceMap.originalToNew[a[1]]]):provenance[a[1]];
  const r=b[0]==="S"?(b[1]===sourceMap.replaced?d[C]:f[sourceMap.originalToNew[b[1]]]):provenance[b[1]];
  provenance.push(genuineResolution(l,r,p));
 }
 assert.equal(provenance.at(-1).length,0);
 return {derivation_count:d.length+provenance.length,contradiction:true};
}
verifyBase();
const singles=G.map((_,i)=>{const f=firstSplit(i),t=allTreeOutcomes(f),ctl=controls(f);
 assert.equal(t.has_false,false);assert.equal(ctl.models,0);assert(ctl.all_deletions_sat&&ctl.all_sign_flips_sat);
 return {split_index:i,formula:f,encoded_bits:encodedBits(f,5),...ctl,...t,exact_minimum:7};
});
const nestedRows=[];for(const t of [0,1,2,3]){
 const f=nested(t),r=allTreeOutcomes(f),ctl=controls(f);
 assert.equal(ctl.models,0);assert(ctl.all_deletions_sat&&ctl.all_sign_flips_sat);
 assert.equal(r.has_false,false);
 nestedRows.push({splits:t,formula:f,encoded_bits:encodedBits(f,4+t),...ctl,...r,exact_minimum:6+t});
}
const positive=allTreeOutcomes([[1],[-1,2],[-2,3],[-3,4],[-4,5],[-5]]);
assert(positive.has_false);
assert.equal(models(G),0);
assert.equal(controls(G).all_deletions_sat,true);
assert.deepStrictEqual(genuineResolution([1,-1],[-1],1),[-1]); // tautology SAT firewall
function parseDimacs(text){
 const parts=text.trim().split(/\s+/);
 if(parts[0]!=="p"||parts[1]!=="cnf"||!/^(\d+)$/.test(parts[2]||"")||!/^(\d+)$/.test(parts[3]||""))throw Error("bad header");
 const n=+parts[2],m=+parts[3];if(n>1000||m>10000)throw Error("outside test grammar");
 const result=[];let clause=[];
 for(const w of parts.slice(4)){if(!/^-?\d+$/.test(w))throw Error("bad token");const v=+w;if(v===0){result.push(clause);clause=[];}else{if(Math.abs(v)>n||v===0)throw Error("out-of-range");clause.push(v);}}
 if(clause.length||result.length!==m)throw Error("count or terminator mismatch");return result;
}
const invalid=["p cnf 2 1\n1 -2","p cnf 1 1\n2 0","p cnf 1 2\n1 0",
 "p cnf 1 1\nX 0","p cnf 1 -1\n1 0","garbage",
 "p cnf 1 1\n1 0 0","p cnf 1 1\n1 0 3"];
let rejected=0;for(const s of invalid){try{parseDimacs(s);}catch(e){rejected++}}assert.equal(rejected,invalid.length);
assert.equal(models([[1],[-1]]),0);
const report={version:"350",model:"fixed Rmix341 strict source-independent VARDEF, lower-bound relaxation with output-support AND3 and free exact clause/affine aliases",original:G,
  original_encoded_bits:encodedBits(G,4),base_resolution_proof:verifyBase(),
  singles,nested:nestedRows,
  positive_source_once_tree:positive.has_false,malformed_rejected:rejected,
  limits:"Only exact finite minima. B1 B2 B3 and unbounded mixed lower bound remain open. Optimizer not charged to W. Host peak space not measured."};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(report,null,2)+"\n");
console.log(JSON.stringify({single_costs:singles.map(x=>x.exact_minimum),nested_costs:nestedRows.map(x=>x.exact_minimum),split_pair_counts:singles.map(x=>x.candidate_pairs),nested_pair_counts:nestedRows.map(x=>x.candidate_pairs),malformed_rejected:rejected},null,2));
