const result = (function main(){
"use strict";
let seed=2080646,checks=0,rankCalls=0,xors=0;const ok=(v,m)=>{checks++;if(!v)throw Error(m);};
function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n);}
const bit=i=>1n<<BigInt(i);
function rank(cols){rankCalls++;const p=new Map();for(let v of cols){while(v){const k=v.toString(2).length-1;if(!p.has(k)){p.set(k,v);break;}v^=p.get(k);xors++;}}return p.size;}
function compile(n){const cs=[],pairs=[];let v=n;for(let u=0;u<n;u++)for(let w=u+1;w<n;w++){const z=v++;pairs.push([u,w,z]);cs.push([u+1,w+1,z+1],[-u-1,-w-1,-z-1]);}
let coord=0;const regions=[],occ=Array.from({length:v},()=>[]);for(let j=0;j<cs.length;j++){const h=bit(coord++),cols=[h];for(const lit of cs[j]){const t=bit(coord++);cols.push(t);occ[Math.abs(lit)-1].push([j,t]);}regions.push(cols);}
for(const o of occ)regions.push([o.reduce((s,x)=>s^x[1],0n)]);
return {n,v,cs,pairs,regions,occ};}
function width(x,side){const S=new Set(side),a=[],b=[];x.regions.forEach((r,i)=>(S.has(i)?a:b).push(...r));let w=rank(a)+rank(b)-rank([...a,...b]);let split=0;for(let i=0;i<x.v;i++){const loc=S.has(x.cs.length+i);if(x.occ[i].some(([j])=>S.has(j)!==loc))split++;}ok(w===split,"cut rank identity");return w;}
const cuts=[];for(const n of [4,6,8,12]){const x=compile(n);let min=Infinity,max=0;for(let t=0;t<32;t++){const side=x.regions.map((_,i)=>i).filter(()=>rand(2));width(x,side);}
for(let t=0;t<8;t++){let ids=x.regions.map((_,i)=>i);for(let i=ids.length-1;i>0;i--){const j=rand(i+1);[ids[i],ids[j]]=[ids[j],ids[i]];}
function find(a){const k=a.filter(i=>i>=x.cs.length&&i<x.cs.length+n).length;if(k>=n/3&&k<=2*n/3)return a;if(k<n/3||a.length<2)return null;const h=Math.floor(a.length/2);return find(a.slice(0,h))||find(a.slice(h));}
const s=find(ids);ok(s!==null,"balanced original variable cut");const w=width(x,s);ok(w>=Math.ceil(n/3),"all-tree lower bound");min=Math.min(min,w);max=Math.max(max,w);}
cuts.push({n,regions:x.regions.length,randomCuts:32,balancedTrees:8,minBalancedWidth:min,maxBalancedWidth:max,theoremLowerBound:Math.ceil(n/3)});}
const supports=[];for(const n of [3,4,5]){const x=compile(n),marks=x.cs.map(c=>c.map(()=>new Set())),vars=Array.from({length:x.v},()=>new Set());let models=0;for(let a=0;a<2**x.v;a++){const truth=l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0);if(!x.cs.every(c=>c.some(truth)))continue;models++;vars.forEach((s,i)=>s.add((a>>i)&1));x.cs.forEach((c,j)=>c.forEach((l,k)=>{if(!truth(l))marks[j][k].add(0);else{marks[j][k].add(2);if(c.some((ll,i)=>i!==k&&truth(ll)))marks[j][k].add(1);}}));}
for(const s of vars)ok(s.size===2,"variable support");for(const a of marks)for(const s of a)ok(s.size===3,"triple support");supports.push({n,variables:x.v,clauses:x.cs.length,sourceModels:models,supportedRows:2*x.v+9*x.cs.length});}
return {seed:2080646,cuts,supports,checks,rankCalls,xors,notes:"Rank-only sampled region trees; all-tree lower bound proved symbolically. Source enumeration verifies actual row support via explicit single-clause repair choices. No claim to enumerate expanded global repair assignments."};
})();
console.log(JSON.stringify(result,null,2));
