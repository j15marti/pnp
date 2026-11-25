"use strict";
function run(){
const L={gauss:0,xor:0,closure:0,pins:0,fusions:0,drops:0,pairs:0,forest:0,raw:0,matchAttempts:0,matchSuccess:0,augment:0,regions:0,branches:0,nodes:0,counts:0,probes:0,reference:0,assertions:0};
const ck=(v,msg)=>{L.assertions++;if(!v)throw Error(msg)},bit=i=>1n<<BigInt(i),pv=a=>a.toString(2).length-1;
function basis(E){L.gauss++;const B=new Map();let bad=false;for(let [a,b] of E){while(a){let p=pv(a),v=B.get(p);if(!v){B.set(p,[a,b]);break}a^=v[0];b^=v[1];L.xor++}if(!a&&b)bad=true}return {B,bad}}
function red([a,b],B){for(const p of [...B.keys()].sort((x,y)=>y-x))if(a&bit(p)){const v=B.get(p);a^=v[0];b^=v[1];L.xor++}return [a,b]}
const rows=B=>[...B.values()];
function canonical(B){const out=[];for(const p of [...B.keys()].sort((a,b)=>a-b)){let [a,b]=B.get(p);for(let i=out.length-1;i>=0;i--){let [c,d]=out[i];if(a&bit(pv(c))){a^=c;b^=d;L.xor++}}out.push([a,b])}return out}
function dot(a,x){let t=a&x,b=0;while(t){b^=1;t&=t-1n}return b}
const hit=(P,x)=>P.every(([a,b])=>dot(a,x)===b),sat=(F,G,x)=>hit(G,x)&&F.every(P=>!hit(P,x));
function model(B){let x=0n;for(const p of [...B.keys()].sort((a,b)=>a-b)){const [a,b]=B.get(p);if(dot(a,x)!==b)x|=bit(p)}return x}
function count(n,E){L.counts++;const b=basis(E);return b.bad?0n:bit(n-b.B.size)}
function close(F,G){F=F.slice();G=G.slice();for(;;){L.closure++;const g=basis(G);if(g.bad)return null;let next=[],pin=null;for(const P of F){const v=basis(P.map(q=>red(q,g.B)));if(v.bad){L.drops++;continue}if(!v.B.size)return null;if(v.B.size===1){let [a,b]=rows(v.B)[0];pin=[a,b^1];break}next.push(canonical(v.B))}
if(pin){G.push(pin);L.pins++;continue}
let fused=false;const map=new Map();for(let i=0;i<next.length;i++){let P=next[i],k=P.map(([a])=>a.toString()).join(",");if(!map.has(k)){map.set(k,i);continue}let j=map.get(k),Q=next[j],d=P.findIndex((e,t)=>e[1]!==Q[t][1]),H=[];if(d<0)H=P;else for(let t=0;t<P.length;t++)if(t!==d){let [a,b]=P[t];if(b!==Q[t][1]){a^=P[d][0];b^=P[d][1]}H.push([a,b])}F=next.filter((_,t)=>t!==i&&t!==j);F.push(H);L.fusions++;fused=true;break}
if(fused)continue;return {F:next,G:canonical(g.B)}}}
// Projection onto homogeneous protected R: eliminate quotient rows while carrying original augmented combinations.
function project(P,R){const Q=new Map(),ext=[];for(const [a,b] of P){let z=red([a,0],R)[0],u=a,v=b;while(z){let p=pv(z),e=Q.get(p);if(!e){Q.set(p,[z,u,v]);break}z^=e[0];u^=e[1];v^=e[2];L.xor++}if(!z)ext.push([u,v])}return {rank:Q.size,ext}}
function cert(n,F,Rrows){
const R=basis(Rrows.map(([a])=>[a,0])).B,pr=F.map(P=>project(P,R)),p=pr.map(v=>bit(n-v.rank)),raw=p.reduce((a,b)=>a+b,0n),E=[];
for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){L.pairs++;const z=project([...F[i],...F[j]],R),b=basis([...pr[i].ext,...pr[j].ext]);if(b.bad)continue;if(z.ext.every(e=>{let [a,c]=red(e,b.B);return a===0n&&c===0}))E.push([i,j,bit(n-z.rank)])}
E.sort((a,b)=>a[2]===b[2]?a[0]-b[0]||a[1]-b[1]:a[2]>b[2]?-1:1);
function forest(cap){let par=F.map((_,i)=>i),root=i=>{while(par[i]!==i)i=par[i];return i},tree=[],adj=F.map(()=>[]);for(let [i,j,q] of E){let a=root(i),b=root(j);if(a===b||adj[i].length>=cap||adj[j].length>=cap)continue;par[a]=b;tree.push([i,j,q]);adj[i].push([j,q]);adj[j].push([i,q])}
const seen=new Set(),mx=(a,b)=>a>b?a:b;function dp(i,prev){seen.add(i);let a=0n,b=p[i];for(const [j,q] of adj[i])if(j!==prev){let [c,d]=dp(j,i);a+=mx(c,d);b+=mx(c,d-q)}return [a,b]}
let bound=0n;for(let i=0;i<F.length;i++)if(!seen.has(i)){let [a,b]=dp(i,-1);bound+=mx(a,b)}return {tree,bound}}
const a=forest(F.length),b=forest(2),v=a.bound<=b.bound?a:b;return {...v,raw,accepted:v.bound<bit(n)}}
function cost(n,F,tree,G){let z=0n;for(const P of F)z+=count(n,[...G,...P]);for(const [i,j] of tree)z-=count(n,[...G,...F[i],...F[j]]);ck(z>=0n,"negative forest");return z}
function lift(n,F,G,tree){G=G.slice();let b=basis(G);ck(!b.bad&&cost(n,F,tree,G)<bit(n-b.B.size),"bad lift premise");for(let i=0;i<n;i++){let a=bit(i);if(!red([a,0],b.B)[0])continue;L.probes++;let H=[...G,[a,0]],J=[...G,[a,1]];G=cost(n,F,tree,H)<=cost(n,F,tree,J)?H:J;b=basis(G)}let x=model(b.B);ck(sat(F,G,x),"bad lift");return x}
// Escape matching (unit capacity integral flow): distinct free singleton observations.
function matching(F,G){L.matchAttempts++;let edges=F.map(P=>P.filter(([a])=>a&&(a&(a-1n))===0n).map(([a,b])=>[pv(a),b^1])),owner=new Map();function aug(i,seen){for(let [j,v] of edges[i]){if(seen.has(j))continue;seen.add(j);if(!owner.has(j)||aug(owner.get(j)[0],seen)){owner.set(j,[i,v]);L.augment++;return true}}return false}
for(let i=0;i<F.length;i++)if(!aug(i,new Set()))return null;let b=basis([...G,...[...owner].map(([j,[i,v]])=>[bit(j),v])]);ck(!b.bad,"match guard");let x=model(b.B);ck(sat(F,G,x),"match witness");L.matchSuccess++;return x}
function ie(n,F,G){let z=0n;function rec(i,E,s){if(i===F.length){z+=BigInt(s)*count(n,E);return}rec(i+1,E,s);rec(i+1,[...E,...F[i]],-s)}rec(0,G,1);return z}
function countLift(n,F,G){if(!ie(n,F,G))return null;G=G.slice();for(let i=0;i<n;i++){let a=bit(i);if(!red([a,0],basis(G).B)[0])continue;L.probes++;let H=[...G,[a,0]];G=ie(n,F,H)>0n?H:[...G,[a,1]]}return model(basis(G).B)}
const support=P=>P.reduce((s,[a])=>s|a,0n);
function solve(n,F,G=[]){L.nodes++;let c=close(F,G);if(!c)return null;F=c.F;G=c.G;if(!F.length)return model(basis(G).B);let all=cert(n,F,G);
if(all.accepted){L.forest++;if(all.raw<bit(n))L.raw++;return lift(n,F,G,all.tree)}
let ma=matching(F,G);if(ma!==null)return ma;
let supports=F.map(support),seen=new Set();for(let i=0;i<F.length;i++){let a=[];for(let j=0;j<F.length;j++)if(supports[i]&supports[j])a.push(j);let key=a.join(",");if(!a.length||a.length>=F.length||a.length>12||seen.has(key))continue;seen.add(key);let S=new Set(a),D=F.filter((_,i)=>S.has(i)),K=F.filter((_,i)=>!S.has(i)),v=cert(n,D,[...G,...K.flat()]);if(!v.accepted)continue;L.regions++;let x=solve(n,K,G);if(x===null)return null;let H=[...G,...K.flat().map(([b])=>[b,dot(b,x)])],y=lift(n,D,H,v.tree);ck(sat(F,G,y),"regional lift");return y}
if(F.length<=8)return countLift(n,F,G);
// Stagnation has already been checked; these are conditional guards, not unconditional deductions.
let a=F[0][0][0];ck(!!red([a,0],basis(G).B)[0],"branch independent");L.branches++;let x=solve(n,F,[...G,[a,0]]);return x!==null?x:solve(n,F,[...G,[a,1]])}
const cnf=cs=>cs.map(C=>C.map(l=>[bit(Math.abs(l)-1),l>0?0:1])),nae=(a,b,c)=>[[bit(a)^bit(b),0],[bit(a)^bit(c),0]];
const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],fc=lines.flatMap(C=>[C.map(i=>i+1),C.map(i=>-i-1)]);
const results={ledger:L,decisions:[],fibers:[],scaling:[],firewall:{}};
function ref(n,F,G=[]){let k=0;for(let x=0n;x<bit(n);x++){L.reference++;if(sat(F,G,x))k++}return k}
function test(name,n,F,G=[]){let k=ref(n,F,G),x=solve(n,F,G);ck((x!==null)===(k>0),name+" label");if(x!==null)ck(sat(F,G,x),name+" source witness");results.decisions.push({name,n,m:F.length,models:k,solver:x===null?"UNSAT":"SAT"})}
test("Fano NAE",7,lines.map(C=>nae(...C)));test("Fano CNF",7,cnf(fc));for(let i=0;i<14;i++)test("Fano neighbor "+i,7,cnf(fc.filter((_,j)=>j!==i)));
for(let n of [3,5,9]){let cs=[];for(let i=0;i<n;i++){let a=i+1,b=(i+1)%n+1;cs.push([a,b],[-a,-b])}test("odd parity rim "+n,n,cnf(cs));test("rim neighbor "+n,n,cnf(cs.slice(1)))}
const edge=(u,v,s)=>[[bit(2*u)^bit(2*v),s&1],[bit(2*u+1)^bit(2*v+1),s>>1]];
let K5=[];for(let u=0;u<5;u++)for(let v=u+1;v<5;v++)K5.push(edge(u,v,0));test("tetra K5",10,K5);test("tetra K5 edge deletion",10,K5.slice(1));
let seed=2081850;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
for(let t=0;t<100;t++){let n=5+rand(3),m=3+rand(17),F=[];for(let i=0;i<m;i++){let P=[];let k=1+rand(3);for(let j=0;j<k;j++)P.push([BigInt(1+rand((1<<n)-1)),rand(2)]);F.push(P)}test("random "+t,n,F)}
function overlay(e){let d=[bit(e),bit(e+1),bit(e+2)];for(let i=0;i<e;i++)d[i%3]^=bit(i);let pairs=[[1,2],[1,4],[2,4],[3,4],[1,6]],row=k=>d.reduce((s,v,i)=>k&(1<<i)?s^v:s,0n);return pairs.map(([a,b])=>[[row(a),0],[row(b),0]])}
for(let e of [0,1,2,3,4]){let n=e+3,F=overlay(e),R=Array.from({length:e},(_,i)=>[bit(i),0]),v=cert(n,F,R);ck(v.accepted&&v.raw>=bit(n),"strict gain");for(let z=0n;z<bit(e);z++){let G=R.map(([a])=>[a,dot(a,z)]),x=lift(n,F,G,v.tree);ck(sat(F,G,x),"fiber");ck(ref(n,F,G)>0,"fiber ref");results.fibers.push({e,z:Number(z),raw:Number(v.raw)/2**n,bound:Number(v.bound)/2**n})}}
for(let e of [8,32,64,128]){let n=e+3,F=overlay(e),R=Array.from({length:e},(_,i)=>[bit(i),0]),v=cert(n,F,R);ck(v.accepted,"large cert");let G=R.map(([a],i)=>[a,i%2]),x=lift(n,F,G,v.tree);ck(sat(F,G,x),"large lift");results.scaling.push({e,n,raw:Number(v.raw)/2**n,bound:Number(v.bound)/2**n,edges:v.tree.length})}
let O=overlay(0).map(P=>P.map(([a,b])=>[a<<7n,b]));test("Fano with overlap overlay",10,[...cnf(fc),...O]);test("Fano neighbor with overlap overlay",10,[...cnf(fc.slice(1)),...O]);
let P=[[[1n,0]],[[3n,0]]],v=cert(2,P,[[2n,0]]);ck(v.tree.length===0&&!v.accepted,"conditional overlap falsely subtracted");results.firewall={raw:Number(v.raw)/4,bound:Number(v.bound)/4,edges:v.tree.length};
for(let t=0;t<100;t++){let F=[];for(let i=0;i<5;i++){let P=[];for(let j=0;j<2;j++)P.push([BigInt(1+rand(31)),rand(2)]);F.push(P)}let R=[[1n,0],[2n,0]],v=cert(5,F,R);for(let z=0;z<4;z++){let G=[[1n,z&1],[2n,z>>1]],bad=0;for(let x=0n;x<32n;x++)if(hit(G,x)&&F.some(P=>hit(P,x)))bad++;ck(BigInt(bad)*4n<=v.bound,"uniform bound");if(v.accepted){let x=lift(5,F,G,v.tree);ck(sat(F,G,x),"random fiber lift")}}}
results.totals={decisions:results.decisions.length,SAT:results.decisions.filter(x=>x.models>0).length,UNSAT:results.decisions.filter(x=>x.models===0).length};return results
}
console.log(JSON.stringify(run(),null,2));
