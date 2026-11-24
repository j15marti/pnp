// Run: node 2026-11-24_1025_DS04_check.js
const run = function(){
"use strict";
const stats={gauss:0,xor:0,closurePasses:0,forced:0,intersections:0,pathImplications:0,treeEdges:0,witnessSteps:0,referenceWords:0};
const check=(p,msg)=>{if(!p)throw Error(msg)};
function count(n,rows){
 stats.gauss++; const piv=new Map();
 for(const row of rows){let a=row[0],b=row[1];while(a){const j=a.toString(2).length-1,old=piv.get(j);if(!old){piv.set(j,[a,b]);break}a^=old[0];b^=old[1];stats.xor++}if(!a&&b)return 0n}
 return 1n<<BigInt(n-piv.size)
}
const bit=i=>1n<<BigInt(i);
function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
const hits=(rows,x)=>rows.every(([a,b])=>parity(a&x)===b);
function closure(n,G,E){
 G=G.slice();for(;;){stats.closurePasses++;const M=count(n,G);if(!M)return null;let changed=false;
 for(const e of E){const s=count(n,G.concat(e));if(s===M)return null;if(s*2n===M){
 const row=e.find(([a,b])=>count(n,G.concat([[a,b]]))===s);
 check(!!row,"rank-one witness");G.push([row[0],row[1]^1]);stats.forced++;changed=true;break
 }}
 if(!changed)return G}
}
function analyze(n,G,E){
 const M=count(n,G),m=E.length, singles=E.map(e=>count(n,G.concat(e)));
 const sum=singles.reduce((a,b)=>a+b,0n), edges=[];let pairSum=0n;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){
 const w=count(n,G.concat(E[i],E[j]));stats.intersections++;edges.push({i,j,w});pairSum+=w}
 edges.sort((a,b)=>a.w>b.w?-1:a.w<b.w?1:a.i-b.i||a.j-b.j);
 const par=Array.from({length:m},(_,i)=>i),adj=Array.from({length:m},()=>[]),T=[];
 function root(i){while(par[i]!==i)i=par[i];return i}
 let wsum=0n;for(const e of edges){const a=root(e.i),b=root(e.j);if(a===b)continue;par[a]=b;T.push([e.i,e.j]);adj[e.i].push(e.j);adj[e.j].push(e.i);wsum+=e.w;stats.treeEdges++}
 let exact=true;
 for(const {i,j,w} of edges){if(!w||!exact)continue;
 const pred=new Map([[i,-1]]),q=[i];for(let k=0;k<q.length&&!pred.has(j);k++)for(const v of adj[q[k]])if(!pred.has(v)){pred.set(v,q[k]);q.push(v)}
 const both=G.concat(E[i],E[j]);
 for(let v=pred.get(j);v!==i;v=pred.get(v))for(const [a,b] of E[v]){
 stats.pathImplications++;if(count(n,both.concat([[a,b^1]]))!==0n){exact=false;break}
 }
 }
 return {M,sum,upper:sum-wsum,lower:sum-pairSum,T,exact}
}
function bound(n,G,E,T){
 let v=0n;for(const e of E)v+=count(n,G.concat(e));
 for(const [i,j] of T)v-=count(n,G.concat(E[i],E[j]));return v
}
function lift(n,G,E,T){
 let x=0n;
 for(let i=0;i<n;i++){
 const p=G.concat([[bit(i),0]]),q=G.concat([[bit(i),1]]);
 const good=H=>count(n,H)>bound(n,H,E,T);
 const z=good(p)?0:1,H=z?q:p;check(good(H),"no positive credit child");
 G=closure(n,H,E);check(G!==null&&good(G),"closure invalidated credit");
 if(z)x|=bit(i);stats.witnessSteps++
 }
 check(hits(G,x)&&!E.some(e=>hits(e,x)),"bad lift");return x
}
function solve(n,G,E){
 const G0=G;G=closure(n,G,E);if(G===null)return {status:"UNSAT",method:"closure",models:0n};
 const a=analyze(n,G,E),out={...a,models:a.exact?a.M-a.upper:null};
 if(a.exact&&a.upper===a.M||a.lower===a.M)return {...out,status:"UNSAT",method:a.exact?"exactTree":"Bonferroni",models:0n};
 if(a.upper<a.M){const x=lift(n,G,E,a.T);check(hits(G0,x),"source guard");return {...out,status:"SAT",method:a.exact?"exactTree":"dominance",x}}
 return {...out,status:"UNKNOWN",method:"decline"}
}
function ref(n,G,E){let s=0n;for(let x=0n;x<(1n<<BigInt(n));x++){stats.referenceWords++;if(hits(G,x)&&!E.some(e=>hits(e,x)))s++}return s}
let seed=2080425;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*k)}
const totals={};const methods={};const cases=[];
function test(label,n,G,E,expected=null,detail=false){
 const s=solve(n,G,E), r=expected===null?ref(n,G,E):expected;
 check(s.status==="UNKNOWN"||(s.status==="SAT")===(r>0n),label+" decision");
 if(s.models!==null&&s.models!==undefined)check(s.models===r,label+" count");
 if(s.x!==undefined)check(hits(G,s.x)&&!E.some(e=>hits(e,s.x)),label+" witness");
 if(s.M!==undefined){check(s.lower<=s.M-r&&s.M-r<=s.upper,label+" bounds");if(s.exact)check(s.upper===s.M-r,label+" exactness")}
 const labelStatus=(r?"SAT":"UNSAT");totals[labelStatus]=(totals[labelStatus]||0)+1;methods[s.method]=(methods[s.method]||0)+1;
 if(detail)cases.push({label,n,m:E.length,truth:labelStatus,models:r.toString(),status:s.status,method:s.method,exact:s.exact??null,ambient:s.M?.toString(),sum:s.sum?.toString(),upper:s.upper?.toString(),lower:s.lower?.toString()});
 return s
}
const cube=Array.from({length:8},(_,w)=>[0,1,2].map(i=>[bit(i),(w>>i)&1]));
for(let mask=0;mask<256;mask++)test("cube-"+mask,3,[],cube.filter((_,i)=>(mask>>i)&1),null,mask===255||mask===254);
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].flatMap(t=>[0,1].map(b=>t.map(i=>[bit(i),b])));
test("Fano",7,[],fano,null,true);for(let i=0;i<fano.length;i++)test("Fano-minus-"+i,7,[],fano.filter((_,j)=>i!==j),null,i===0);
const K5=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)K5.push([[bit(2*i)^bit(2*j),0],[bit(2*i+1)^bit(2*j+1),0]]);
test("K5",10,[],K5,null,true);for(let i=0;i<K5.length;i++)test("K5-minus-"+i,10,[],K5.filter((_,j)=>i!==j),null,i===0);
for(let t=0;t<300;t++){
 const n=2+rnd(7),m=1+rnd(11),G=Array.from({length:rnd(3)},()=>[BigInt(1+rnd((1<<n)-1)),rnd(2)]);
 const E=Array.from({length:m},()=>Array.from({length:1+rnd(4)},()=>[BigInt(1+rnd((1<<n)-1)),rnd(2)]));
 test("random-"+t,n,G,E)
}
for(const k of [1,2,3,4,5]){
 const g=1<<k,n=k+2*g,E=[];
 for(let j=0;j<g;j++){const gate=Array.from({length:k},(_,i)=>[bit(i),(j>>i)&1]),u=bit(k+2*j),v=bit(k+2*j+1);
 for(const a of [u,v,u^v])E.push(gate.concat([[a,0]]))}
 const a=test("gated-root-"+g,n,[],E,0n,true);check(a.exact&&a.method==="exactTree","root tree");
 const b=test("gated-neighbor-"+g,n,[],E.slice(1),1n<<BigInt(n-k-2),true);check(b.exact&&b.method==="exactTree"&&b.sum>=b.M,"strict improvement");
 // Probe arbitrary affine coordinate relation; exact tree property should persist.
 if(k<=3){const G=[[bit(k)^bit(n-1),1]];test("gated-guard-"+g,n,G,E.slice(1),1n<<BigInt(n-k-3),true)}
}
const independent=[0,1,2].map(i=>[[bit(2*i),0],[bit(2*i+1),0]]);
const z=test("non-tree-exact",6,[],independent,null,true);check(!z.exact&&z.status==="SAT","false exactness control");
return {seed:2080425,totals,methods,stats,cases,discrepancies:0};
};
console.log(JSON.stringify(run(),null,2));
