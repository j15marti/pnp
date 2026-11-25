"use strict";
function main(){
const stats={checks:0,oracleCalls:0,referenceWords:0,closureScans:0,separatorTriples:0,creditChecks:0}, rows=[];
function ck(v,msg){stats.checks++;if(!v)throw Error(msg)}
const bits=(n,w)=>Array.from({length:n},(_,i)=>(w>>i)&1);
const legal=(x,R,D)=>R.every(([a,b,c])=>x[a]===x[b]||x[a]===x[c])&&(!D||D.some(v=>x[v]!==x[D[0]]));
const key=(x,U)=>U.map(v=>x[v]^x[U[0]]).join("");
const pat=["000","001","010","011"];
function solve(n,R,D,eq=[],ref=false){
 if(!ref)stats.oracleCalls++;
 const p=Array.from({length:n},(_,i)=>i);
 function find(a){while(p[a]!==a)a=p[a];return a}
 function join(a,b){a=find(a);b=find(b);if(a===b)return false;p[b]=a;return true}
 eq.forEach(([a,b])=>join(a,b));
 let change=true;
 while(change){stats.closureScans++;change=false;for(const [a,b,c] of R)if(find(b)===find(c))change=join(a,b)||change;}
 if(D&&D.every(v=>find(v)===find(D[0])))return null;
 const reps=[...new Set([...R.flat(),...(D||[]),...eq.flat()].map(find))];
 const I=new Map(reps.map((v,i)=>[v,i]));
 for(let w=0;w<2**reps.length;w++){stats.referenceWords++;const x=Array.from({length:n},(_,v)=>I.has(find(v))?(w>>I.get(find(v)))&1:0);if(legal(x,R,D)&&eq.every(([a,b])=>x[a]===x[b]))return x;}
 return null;
}
function project(n,R,D,U){
 let S=new Map(); // exact relative support; every successful query retains an actual witness
 if(!D)S.set("000",Array(n).fill(0));
 for(const k of pat){
  if(S.has(k))continue;
  if(!D){const a=U[0],b=U[k.indexOf("1")],eq=U.map((v,i)=>[v,k[i]==="0"?a:b]);const x=solve(n,R,[a,b],eq);if(x)S.set(k,x);continue;}
  outer:for(let i=0;i<D.length;i++)for(let j=i+1;j<D.length;j++)for(let o=0;o<2;o++){
   const a=D[i],b=D[j],eq=U.map((v,h)=>[v,(Number(k[h])^o)?b:a]);
   const x=solve(n,R,[a,b],eq);if(x){S.set(k,x);break outer;}
  }
 }
 return S;
}
function combine(n,A,B,D,where,U){
 const S=project(n,B,where==="B"?D:null,U); let x=null;
 if(where==="A"){
  const add=pat.slice(1).filter(k=>!S.has(k)).map(k=>{const v=U.find((_,i)=>k[i]!==k[(i+1)%3]&&k[i]!==k[(i+2)%3]);return [v,...U.filter(u=>u!==v)]});
  x=solve(n,A.concat(add),D);
 }else if(S.has("000"))x=Array(n).fill(0);
 else{
  let K=[...S.keys()];if(K.length===3)x=solve(n,A,U);
  if(K.length===2){const pairs=[[0,1],[0,2],[1,2]];const [a,b]=pairs.find(([i,j])=>K.every(k=>k[i]!==k[j]));x=solve(n,A,[U[a],U[b]]);}
  if(K.length===1){const k=K[0],a=U[0],b=U[k.indexOf("1")];x=solve(n,A,[a,b],U.map((v,i)=>[v,k[i]==="0"?a:b]));}
 }
 if(!x)return {x:null,S:[...S.keys()]};
 let k=key(x,U),y=S.get(k);ck(!!y,"interface support");
 if(y[U[0]]!==x[U[0]])y=y.map(v=>v^1);
 const BV=new Set([...B.flat(),...(where==="B"?D:[]),...U]);
 const z=x.map((v,i)=>BV.has(i)?y[i]:v);ck(legal(z,A.concat(B),D),"lift");
 return {x:z,S:[...S.keys()]};
}
let seed=9517;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function gen(V){let out=[],seen=new Set();while(out.length<8){let a=V[rand(V.length)],b=V[rand(V.length)],c=V[rand(V.length)];if(new Set([a,b,c]).size<3)continue;let k=[a,...[b,c].sort((x,y)=>x-y)].join();if(!seen.has(k)){seen.add(k);out.push([a,b,c]);}}return out}
let random={sat:0,unsat:0,supports:{}};for(let i=0;i<120;i++){const U=[0,1,2],A=gen([0,1,2,3,4]),B=gen([0,1,2,5,6]),where=i%2?"A":"B",D=where==="A"?[3,4,0]:[5,6,0];const o=combine(7,A,B,D,where,U);const truth=solve(7,A.concat(B),D,[],true);ck(!!truth===!!o.x,"random decision");random[truth?"sat":"unsat"]++;let k=o.S.sort().join("/");random.supports[k]=(random.supports[k]||0)+1;}rows.push({name:"random two-side",...random});
const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function repair(E,w,signs=[]){let R=[],bad=[];E.forEach((e,i)=>{let t=e.map((v,j)=>w[v]^(((signs[i]||0)>>j)&1));if(t.every(b=>b===t[0]))bad.push(e);else{let j=t.findIndex((v,k)=>v!==t[(k+1)%3]&&v!==t[(k+2)%3]);R.push([e[j],...e.filter((_,k)=>k!==j)]);}});return{R,bad}}
let f={sat:0,unsat:0};
for(let e=-1;e<21;e++){
 let signs=Array(7).fill(0);if(e>=0)signs[Math.floor(e/3)]=1<<(e%3);let r;for(let w=0;w<128;w++){r=repair(F,bits(7,w),signs);if(r.bad.length===1)break;}
 ck(r.bad.length===1,"anchor");
 const U=r.bad[0],B=r.R.concat([[U[0],7,8],[U[1],7,9]]),A=gen([...U,10,11]);
 // A neutralize using constants if any boundary pattern; replace generated side by free wedges for label preservation.
 const free=Array.from({length:8},(_,i)=>[U[i%3],10+2*i,11+2*i]);
 // Reference only B and exact free side (all assignments extend); avoid enumerating 26 vars.
 const o=combine(26,free,B,U,"B",U);const truth=solve(10,B,U,[],true);ck(!!o.x===!!truth&&!!truth===(e>=0),"Fano label");f[truth?"sat":"unsat"]++;
}
rows.push({name:"same Fano / 21 sign neighbors plus transparent 3-interface padding",...f});
// every complement-invariant 3-bit relation and its exact residual encoding.
for(let mask=0;mask<16;mask++){let K=pat.filter((_,i)=>(mask>>i)&1);if(K.includes("000")){let R=pat.slice(1).filter(k=>!K.includes(k)).map(k=>{let i=[0,1,2].find(i=>k[i]!==k[(i+1)%3]&&k[i]!==k[(i+2)%3]);return[i,...[0,1,2].filter(j=>j!==i)]});for(let w=0;w<8;w++)ck(legal(bits(3,w),R,null)===K.includes(key(bits(3,w),[0,1,2])),"all constant valid supports");}else if(K.length){let D,eq=[];if(K.length===3)D=[0,1,2];if(K.length===2)D=[[0,1],[0,2],[1,2]].find(([i,j])=>K.every(k=>k[i]!==k[j]));if(K.length===1){let k=K[0],b=k.indexOf("1");D=[0,b];eq=[0,1,2].map(i=>[i,k[i]==="0"?0:b]);}for(let w=0;w<8;w++){let x=bits(3,w);ck((legal(x,[],D)&&eq.every(([a,b])=>x[a]===x[b]))===K.includes(key(x,[0,1,2])),"all nonconstant supports");}}}
for(let m=16;m<=160;m++)for(let b=8;b<=m/2;b++){let P=BigInt(m+1)**8n,C=24n*BigInt(b+1)**8n+BigInt(m-b+4)**8n;ck(C<P,"credit");stats.creditChecks++;}
return{stats,rows};
}
console.log(JSON.stringify(main(),null,2));
