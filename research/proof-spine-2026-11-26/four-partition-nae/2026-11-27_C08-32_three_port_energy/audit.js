'use strict';
function audit(){
const assert=(x,msg)=>{if(!x)throw Error(msg||"assert")};
const CAP=[[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[1,5,6],[2,3,7],[0,5,7],[1,3,8],[2,4,6]];
const GAD=[[0,4,11],[1,5,7],[2,6,8],[3,9,10],[0,1,6],[2,7,10],[3,4,5],[1,8,10],[4,6,9],[2,5,11],[0,3,7],[4,7,8],[5,6,10],[1,3,11],[0,2,9]];
const CUT=[[41,53,29],[30,17,0],[42,1,65],[18,2,54],[20,44,3],[4,66,56],[68,5,32]];
const C=CAP.concat(Array.from({length:5},(_,j)=>GAD.map(r=>r.map(v=>9+12*j+v))).flat(),CUT);
const P=[1,0,0,0,2,2,2,3,3,3].concat(Array.from({length:5},()=>[0,0,0,0,1,1,1,2,2,2,2,3,3,3,3]).flat(),Array(7).fill(1));
const rows=[[[3,0],[4,0],[2,0]],[[2,0],[1,0],[0,0]],[[3,0],[0,0],[5,0]],[[1,0],[0,0],[4,0]],[[1,0],[3,0],[0,1]],[[0,1],[5,0],[4,0]],[[5,0],[0,1],[2,0]]];
const bits=(n,i)=>Array.from({length:n},(_,j)=>(i>>j)&1);
const words=(n)=>Array.from({length:2**n},(_,i)=>bits(n,i));
const range=n=>Array.from({length:n},(_,i)=>i);
const nae=(r,x)=>new Set(r.map(([v,s])=>x[v]^s)).size>1;
const pairEnergy=(r,x)=>{let t=0;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)t+=((x[r[i][0]]^r[i][1])===(x[r[j][0]]^r[j][1]));return t};
function auth(L){
 let n=69*L,cs=Array.from({length:L},(_,j)=>C.map(r=>r.map(v=>69*j+v))).flat(),ps=Array.from({length:L},()=>P).flat(),seen=new Set();
 for(let k=0;k<4;k++){let d=new Int8Array(n);cs.forEach((r,i)=>{if(ps[i]===k)r.forEach(v=>d[v]++)});assert(d.every(x=>x===1),"partition")}
 for(const r of cs){assert(new Set(r).size===3);for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let key=[r[i],r[j]].sort((a,b)=>a-b).join(",");assert(!seen.has(key),"linearity");seen.add(key)}}
 return cs.length;
}
let tables=[],map={};let localWords=0;
for(let j=0;j<6;j++){
 let rs=j?GAD:CAP,n=j?12:9,ports=j?[8,9,11]:[0,1,2,3,4,5],off=j?9+12*(j-1):0,tab={};
 for(const x of words(n)){localWords++;if(rs.every(r=>new Set(r.map(v=>x[v])).size>1)){let k=ports.map(v=>x[v]).join("");tab[k]=(tab[k]||0)+1}}
 assert(JSON.stringify(tab,Object.keys(tab).sort())===JSON.stringify(j?{"000":7,"111":7}:{"000111":6,"111000":6},Object.keys(tab).sort()),"port table");
 tables.push(tab);ports.forEach(v=>map[off+v]=[j,+(j===0&&v>=3)]);
}
assert(JSON.stringify(CUT.map(r=>r.map(v=>map[v])))===JSON.stringify(rows),"adapter");auth(1);
function pairFactors(rs){
 const d=new Map();let c=0;
 for(const r of rs)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){
  let [u,a]=r[i],[v,b]=r[j];if(u===v){c+=+(a===b);continue}let k=[u,v].sort((x,y)=>x-y).join(","),t=d.get(k)||[0,0];t[a^b]++;d.set(k,t)
 }
 let out=[];for(const [k,t] of d){if(t[0]===t[1])c+=t[0];else out.push({s:k.split(",").map(Number),t})}
 if(c)out.push({s:[],t:[c]});return out;
}
const index=(S,x)=>S.slice(1).reduce((a,v,j)=>a+((x.get(v)^x.get(S[0]))<<j),0);
const value=(F,x)=>F.reduce((a,f)=>a+f.t[index(f.s,x)],0);
function components(V,adj,T){
 let rem=new Set(V.filter(v=>!T.has(v))),out=[];
 while(rem.size){let a=rem.values().next().value;rem.delete(a);let q=[a];for(let i=0;i<q.length;i++)for(const b of adj.get(q[i]))if(rem.delete(b))q.push(b);out.push(q)}
 return out;
}
function* combinations(V,k,start=0,pre=[]){if(!k){yield pre;return}for(let i=start;i<=V.length-k;i++)yield* combinations(V,k-1,i+1,pre.concat(V[i]))}
function solve(V,F,S,st,L=5){
 st.calls++;st.maxBag=Math.max(st.maxBag,V.length);if(st.calls+st.scans+st.words+st.factorEvals>st.cap)throw Error("CAP");
 if(V.length<=L){
  let tab=Array(2**Math.max(0,S.length-1)).fill(Infinity);
  for(const w of words(V.length)){st.words++;st.factorEvals+=F.length;let x=new Map(V.map((v,i)=>[v,w[i]])),i=index(S,x);tab[i]=Math.min(tab[i],value(F,x))}
  st.terminals++;assert(tab.every(Number.isFinite));return {s:S,t:tab};
 }
 let adj=new Map(V.map(v=>[v,new Set()]));for(const s of F.map(f=>f.s).concat([S]))for(let i=0;i<s.length;i++)for(let j=i+1;j<s.length;j++){adj.get(s[i]).add(s[j]);adj.get(s[j]).add(s[i])}
 let choice=null;
 outer:for(let k=0;k<=3;k++)for(const a of combinations(V,k)){
  st.scans++;if(st.calls+st.scans+st.words+st.factorEvals>st.cap)throw Error("CAP");
  let T=new Set(a),cc=components(V,adj,T);if(cc.length<2)continue;
  let B=cc.find(r=>!r.some(v=>S.includes(v)));if(!B)continue;choice=[a,B];break outer;
 }
 if(!choice)return null;
 let [T,B]=choice,BS=new Set(B),va=V.filter(v=>!BS.has(v)),vb=B.concat(T).sort((a,b)=>a-b);
 let fa=[],fb=[];for(const f of F){if(f.s.some(v=>BS.has(v))){assert(f.s.every(v=>vb.includes(v)),"split factor");fb.push(f)}else fa.push(f)}
 st.splits++;st.maxSeam=Math.max(st.maxSeam,T.length);
 let msg=solve(vb,fb,T,st,L);if(msg===null)return null;fa.push(msg);
 return solve(va,fa,S,st,L);
}
const stats=n=>({calls:0,scans:0,words:0,factorEvals:0,terminals:0,splits:0,maxBag:0,maxSeam:0,cap:Math.max(100000,n*n*n)});
function direct(rs,n,guard=()=>true){
 let min=Infinity,hist={};for(const x of words(n))if(guard(x)){let u=rs.filter(r=>!nae(r,x)).length;let e=rs.length+2*u;assert(rs.reduce((s,r)=>s+pairEnergy(r,x),0)===e);hist[u]=(hist[u]||0)+1;min=Math.min(min,e)}return {min,hist}
}
let orig=direct(rows,6),F=pairFactors(rows),st=stats(69),got=solve(range(6),F,[],st);assert(orig.min===9&&got.t[0]===orig.min);
for(const x of words(6))assert(value(F,new Map(x.map((v,i)=>[i,v])))===rows.reduce((a,r)=>a+pairEnergy(r,x),0),"pair");
let split=[];let ids=range(7).filter(i=>rows[i].some(([v])=>v===0));
for(const a of combinations(ids,3)){if(!a.includes(ids[0]))continue;let rs=rows.map((r,i)=>r.map(([v,s])=>[v===0&&a.includes(i)?6:v,s]));let loose=direct(rs,7),guard=direct(rs,7,x=>x[0]===x[6]);assert(loose.min===7&&guard.min===9);let contracted=rs.map(r=>r.map(([v,s])=>[v===6?0:v,s]));assert(JSON.stringify(contracted)===JSON.stringify(rows));let ss=stats(69);assert(solve(range(6),pairFactors(contracted),[],ss).t[0]===9);split.push({owners:a,relaxedMinimum:loose.min,guardedMinimum:guard.min,stats:ss})}
let family=[];
for(const L of [1,2,4,8,16,32,64]){
 let nr=auth(L),rs=Array.from({length:L},(_,j)=>rows.map(r=>r.map(([v,s])=>[v?5*j+v:0,s]))).flat(),n=5*L+1;
 let ss=stats(69*L),ff=pairFactors(rs),r=solve(range(n),ff,[],ss);assert(r&&r.t[0]===9*L);
 if(L<=2)assert(direct(rs,n).min===9*L);
 family.push({L,nativeVariables:69*L,nativeOwners:nr,physicalGuards:Array.from({length:L-1},(_,j)=>[0,69*(j+1),0]),phaseVariables:n,interactionEdges:ff.filter(f=>f.s.length===2).length,globalPlanarDeletionLowerBound:L,minimum:r.t[0],threshold:7*L,stats:ss,globalDirect:L<=2?"executed":"not admitted under 4096-word reference cap"})
}
// All possible relative-port costs over a small value range: exact quadratic interpolation.
let interp=0;
for(let f0=0;f0<4;f0++)for(let f1=0;f1<4;f1++)for(let f2=0;f2<4;f2++)for(let f3=0;f3<4;f3++){
 let t=[f0,f1,f2,f3],a=(f1+f3-f2-f0)/2,b=(f2+f3-f1-f0)/2,d=(f1+f2-f3-f0)/2;
 for(const x of words(3)){let y=x[0]^x[1],z=x[0]^x[2];assert(f0+a*y+b*z+d*(y^z)===t[y+2*z]);interp++}
}
// Four-port hostile control: two NAE owners sharing v; min number of violations over v.
let quartic=0,portTable=[];
for(const x of words(4)){let u=Math.min(...[0,1].map(v=>+(!nae([[0,0],[1,0],[4,0]],x.concat(v)))+ +(!nae([[2,0],[3,0],[4,0]],x.concat(v)))));quartic+=u*(-1)**x.reduce((a,b)=>a+b,0);portTable.push(u)}
assert(quartic===2,"nonzero quartic");
let hostile=direct(rows.slice(1),6);assert(hostile.min===6);let hs=stats(69);assert(solve(range(6),pairFactors(rows.slice(1)),[],hs).t[0]===6);
// Dense native AG9 control: verified NO independently; small-torso terminal declines.
let ag=CAP.concat([[0,1,2],[3,4,5]]).map(r=>r.map(v=>[v,0]));let ar=direct(ag,9),as=stats(69);assert(ar.min>ag.length);assert(solve(range(9),pairFactors(ag),[],as)===null);
return {source:{C,P,localTables:tables,localWords,cutOwners:range(7).map(i=>85+i),portMap:map},original:{direct:orig,minimum:got.t[0],stats:st},split,family,controls:{interpolationChecks:interp,fourPortViolationTable:portTable,quarticCoefficient:quartic/16,ownerDeletionMinimum:hostile.min,denseAG9Minimum:ar.min,denseTerminal:"UNKNOWN",denseStats:as}};
}
console.log(JSON.stringify(audit(),null,2));
