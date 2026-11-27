"use strict";
function main(){
const assert=(b,m)=>{if(!b)throw Error(m||"assertion")};
let seed=2026112706; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const words=(d)=>Array.from({length:4**d},(_,i)=>Array.from({length:d},(_,j)=>(i>>(2*j))&3));
const index=z=>z.reduce((s,t,i)=>s+t*4**i,0);
const xor=a=>a.reduce((x,y)=>x^y,0);
const F=[0,0,0,1],G=[0,0,1,0];
function build(v,E,fn,c){const inc=Array.from({length:v},()=>[]);E.forEach(([u,w],i)=>{inc[u].push([i,0]);inc[w].push([i,1])});return {v,E,inc,T:inc.map((es,u)=>words(es.length).map(z=>c[u]^xor(es.map(([e,s],j)=>fn[e][s][z[j]]))))}}
function facts(I){return I.T.map((T,u)=>{let c=T[0],fs=I.inc[u].map((_,j)=>[0,1,2,3].map(t=>T[t*4**j]^c));return words(fs.length).every(z=>T[index(z)]===(c^xor(z.map((t,j)=>fs[j][t]))))?{c,fs}:null})}
function solve(I,pins={}){const A=facts(I);if(A.some(x=>x===null))return undefined;let c=A.map(a=>a.c);let map=I.E.map(()=>[]);I.inc.forEach((es,u)=>es.forEach(([e,s],j)=>map[e][s]=A[u].fs[j]));
let p=Array.from({length:I.v},(_,i)=>i),root=u=>{while(p[u]!==u)u=p[u];return u};
let out=I.E.map(()=>[0,0]),cor=[],res=[],rels=[];
for(let e=0;e<I.E.length;e++){let [u,v]=I.E[e],D=e in pins?[pins[e]]:[0,1,2,3],R=[...new Set(D.map(t=>2*map[e][0][t]+map[e][1][t]))];rels.push(R);let S=[0,1].map(s=>[...new Set(R.map(t=>s?t&1:t>>1))]);
if(R.length===3){let m=[0,1,2,3].find(t=>!R.includes(t));out[e]=[1^(m>>1),1^(m&1)];res.push([[e,0,u],[e,1,v]])}
else if(R.length===2&&S.every(a=>a.length===2)){out[e]=[0,R.find(t=>t<2)&1];cor.push(e);p[root(v)]=root(u)}
else {for(let s=0;s<2;s++){if(S[s].length===1)out[e][s]=S[s][0];else res.push([[e,s,s?v:u]])}}
c[u]^=out[e][0];c[v]^=out[e][1];
}
let charge=new Map();for(let u=0;u<I.v;u++)charge.set(root(u),(charge.get(root(u))||0)^c[u]);
let opts=new Map([...charge.keys()].map(u=>[u,[]]));res.forEach((r,i)=>r.forEach(([e,s,u])=>opts.get(root(u)).push([i,e,s])));
let owner=Array(res.length).fill(null);function aug(u,seen){for(let [i,e,s] of opts.get(u)){if(seen.has(i))continue;seen.add(i);if(!owner[i]||aug(owner[i][0],seen)){owner[i]=[u,e,s];return true}}return false}
let ok=true;for(let [u,b] of charge)if(b&&!aug(u,new Set())){ok=false;break}
// independent component obstruction: no spare resource, all odd, quotient is a tree.
let adj=new Map([...charge.keys()].map(u=>[u,[]])),free=new Set();res.forEach(r=>{let a=root(r[0][2]);if(r.length===1)free.add(a);else{let b=root(r[1][2]);adj.get(a).push(b);adj.get(b).push(a)}});
let seen=new Set(),bad=false;for(let u of charge.keys()){if(seen.has(u))continue;let Q=[u];seen.add(u);for(let j=0;j<Q.length;j++)for(let w of adj.get(Q[j]))if(!seen.has(w)){seen.add(w);Q.push(w)}let edges=Q.reduce((s,w)=>s+adj.get(w).length,0)/2;if(Q.every(w=>charge.get(w)===1&&!free.has(w))&&edges===Q.length-1)bad=true}
assert(ok===!bad,"matching vs tree criterion");if(!ok)return null;
for(let z of owner)if(z){let [,e,s]=z;out[e][s]^=1}
let rem=A.map(a=>a.c);I.E.forEach(([u,v],e)=>{rem[u]^=out[e][0];rem[v]^=out[e][1]});
let ca=Array.from({length:I.v},()=>[]);cor.forEach(e=>{let[u,v]=I.E[e];ca[u].push([v,e]);ca[v].push([u,e])});
seen=new Set();for(let u=0;u<I.v;u++){if(seen.has(u))continue;let Q=[u],par=new Map();seen.add(u);for(let j=0;j<Q.length;j++)for(let [w,e] of ca[Q[j]])if(!seen.has(w)){seen.add(w);par.set(w,[Q[j],e]);Q.push(w)}for(let j=Q.length-1;j>0;j--){let w=Q[j],[a,e]=par.get(w);if(rem[w]){out[e][0]^=1;out[e][1]^=1;rem[a]^=1;rem[w]=0}}assert(!rem[u],"residual charge")}
let z=out.map(([a,b],e)=> (e in pins?[pins[e]]:[0,1,2,3]).find(t=>map[e][0][t]===a&&map[e][1][t]===b));assert(z.every(t=>t!==undefined)&&valid(I,z),"witness");return z}
function valid(I,z){return I.T.every((T,u)=>T[index(I.inc[u].map(([e])=>z[e]))]===0)}
function brute(I,pins={}){for(let z of words(I.E.length))if(Object.entries(pins).every(([e,t])=>z[e]===t)&&valid(I,z))return true;return false}
function path(h){let E=Array.from({length:h-1},(_,i)=>[i,i+1]);return build(h,E,E.map(()=>[F,G]),Array(h).fill(1))}
function cnf(I){let clauses=[];I.T.forEach((T,u)=>words(I.inc[u].length).forEach(z=>{if(T[index(z)]){let mask=0,val=0;I.inc[u].forEach(([e],j)=>{mask|=3<<(2*e);val|=z[j]<<(2*e)});clauses.push([mask,val])}}));return clauses}
function opt(C,n){let M=new Map();function dp(mask,val){let k=mask+val*2**n;if(M.has(k))return M.get(k);if(C.some(([m,v])=>(m&mask)===m&&(val&m)===v))return [1,0];if(mask===(1<<n)-1)return [Infinity,Infinity];let L=Infinity,D=Infinity;for(let i=0;i<n;i++)if(!(mask>>i&1)){let a=dp(mask|1<<i,val),b=dp(mask|1<<i,val|1<<i);L=Math.min(L,a[0]+b[0]);D=Math.min(D,1+Math.max(a[1],b[1]))}let r=[L,D];M.set(k,r);return r}return dp}
function pop(x){let k=0;while(x){x&=x-1;k++}return k}
function size(I){let n=2*I.E.length,m=I.T.reduce((s,T)=>s+T.reduce((a,b)=>a+b,0),0),ell=I.T.reduce((s,T,u)=>s+2*I.inc[u].length*T.reduce((a,b)=>a+b,0),0),w=Math.ceil(Math.log2(n+1));return {n,m,ell,N:n+2*m+2+(w+2)*ell}}
let lines=[],rand={SAT:0,UNSAT:0,pinned:0};
let K=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
for(let i=0;i<240;i++){let E=i%2?K:[[0,1],[1,2],[2,0],[2,3]],fn=E.map(()=>[0,1].map(()=>Array.from({length:4},()=>rnd(7)<3?1:0))),I=build(4,E,fn,Array.from({length:4},()=>rnd(11)<5?1:0)),pins=i%3===0?{[rnd(E.length)]:rnd(4)}:{};let x=solve(I,pins),b=brute(I,pins);assert((x!==null)===b,"random brute");rand[b?"SAT":"UNSAT"]++;if(i%3===0)rand.pinned++}
lines.push("random "+JSON.stringify(rand));
for(let h=2;h<=6;h++){let I=path(h),C=cnf(I),n=2*(h-1),dp=opt(C,n);assert(solve(I)===null&&!brute(I));for(let u=0;u<h;u++){let J={...I,T:I.T.map((T,v)=>v===u?T.map(()=>0):T)};assert(solve(J)!==null&&brute(J),"deletion")}let rev=[];if(h===5)for(let k=0;k<=n;k++)rev.push(dp(((1<<n)-1)^((1<<k)-1),0));lines.push("path "+h+" "+JSON.stringify(size(I))+" DP "+JSON.stringify(dp(0,0))+" cover "+Math.floor(h/2)+" reverse "+JSON.stringify(rev))}
function prism(h){let E=[];for(let r=0;r<2;r++)for(let j=0;j<h;j++)E.push([r*h+j,r*h+(j+1)%h]);for(let j=0;j<h;j++)E.push([j,h+j]);return E}
function hybrid(v,E,h){let [u,w]=E[0];E=E.slice(1).concat([[u,v],[v,w],[v,v+1]],Array.from({length:h-1},(_,i)=>[v+1+i,v+2+i]));let fn=E.map((_,i)=>i<E.length-h?[F,F]:[F,G]);let c=Array(v+1+h).fill(0);c[0]=1;for(let i=v+1;i<c.length;i++)c[i]=1;return build(c.length,E,fn,c)}
let del=0,flips=0;
for(let v of [4,6,12,32,64]){let I=hybrid(v,v===4?K:prism(v/2),v);assert(solve(I)===null);for(let u=0;u<I.v;u++){let J={...I,T:I.T.map((T,w)=>w===u?T.map(()=>0):T)};assert(solve(J)!==null,"hybrid deletion");del++}for(let u=0;u<I.v;u++){let J={...I,T:I.T.map((T,w)=>w===u?T.map(b=>b^1):T)};assert(solve(J)!==null,"charge flip");flips++}lines.push("hybrid "+v+" "+JSON.stringify(size(I))+" cover "+Math.floor((v+1)/2))}
lines.push("hybrid deletions "+del+" charge flips "+flips);
return lines.join("\n")+"\n";
}
console.log(main().trimEnd());
