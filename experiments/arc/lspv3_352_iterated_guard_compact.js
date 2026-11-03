"use strict";
// LSPV-3 352. Independent finite enumerator and exact guard-resolution DAG checker.
function assert(x,s){if(!x)throw Error(s)}
function graph(kind,k){let h=kind==="K4"?4:2*k,E=[];
function edge(a,b){E.push([a,b])}
if(kind==="K4"){for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edge(a,b)}
else for(let a=0;a<k;a++){edge(a,(a+1)%k);edge(k+a,k+(a+1)%k);edge(a,k+a)}
let inc=Array.from({length:h},()=>[]);
E.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});
assert(inc.every(x=>x.length===3),"not cubic");return {h,E,inc}}
function evalC(C,a){return C.some(l=>a[Math.abs(l)-1]===Number(l>0))}
function sources(g,odd){let out=[];
for(let v=0;v<g.h;v++)for(let p=0;p<8;p++){
let parity=((p&1)+((p>>1)&1)+((p>>2)&1))%2;
if(parity===Number(odd&&v===0))continue;
out.push(g.inc[v].map((i,j)=>p&(1<<j)?-i:i))}
return out}
function solve(F,n){let M=[];for(let a=0;a<(1<<n);a++){
let bits=Array.from({length:n},(_,i)=>(a>>i)&1);
if(F.every(c=>evalC(c,bits)))M.push(bits)}return M}
function one(kind,k,t){
let g=graph(kind,k),n=g.E.length,F=sources(g,true),even=sources(g,false),m=F.length;
assert(solve(F,n).length===0,"odd SAT");
let evenModels=solve(even,n).length;
assert(evenModels===Math.pow(2,n-g.h+1),"even models");
let guards=1<<t,G=[],map=new Map();
for(let i=0;i<m;i++)for(let s=0;s<guards;s++){
let C=Array.from({length:t},(_,j)=>s&(1<<j)?-(n+j+1):n+j+1).concat(F[i]);
map.set(i+":"+s,C);G.push(C)}
let sign=0;
for(let i=0;i<m;i++){
let w=solve(F.filter((_,j)=>i!==j),n)[0];assert(!!w,"not minimal");
for(let s=0;s<guards;s++){
let C=map.get(i+":"+s),a=w.concat(Array.from({length:t},(_,j)=>(s>>j)&1));
assert(G.filter(D=>!evalC(D,a)).length===1 && !evalC(C,a),"deletion witness");
for(let j=0;j<C.length;j++){let changed=C.slice();changed[j]=-changed[j];
assert(evalC(changed,a),"sign witness");sign++}}}
let res=0;
for(let j=t-1;j>=0;j--){let next=new Map(),p=n+j+1;
for(let i=0;i<m;i++)for(let s=0;s<(1<<j);s++){
let A=map.get(i+":"+s),B=map.get(i+":"+(s+(1<<j)));
assert(A.includes(p)&&B.includes(-p),"guard resolution pivot");
let D=A.filter(x=>x!==p),E=B.filter(x=>x!==-p);
assert(JSON.stringify(D)===JSON.stringify(E),"wrong resolvent");
next.set(i+":"+s,D);res++}
map=next}
for(let i=0;i<m;i++)assert(JSON.stringify(map.get(i+":0"))===JSON.stringify(F[i]),"failed strip");
let and=3*g.h,xor=g.h-1;
for(let v=0;v<g.h;v++)for(let p=0;p<8;p++){
let bits=Array(n).fill(0);
g.inc[v].forEach((e,j)=>bits[e-1]=(p>>j)&1);
assert(F.slice(4*v,4*v+4).every(C=>evalC(C,bits))===
((((p&1)+((p>>1)&1)+((p>>2)&1))%2)===Number(v===0)),"AND3 row")}
let mask=0,rhs=0;
for(let v=0;v<g.h;v++){
for(let e of g.inc[v])mask^=1<<(e-1);
rhs^=Number(v===0)}
assert(mask===0&&rhs===1,"XOR contradiction");
let lines="p cnf "+(n+t)+" "+G.length+"\n"+G.map(C=>C.join(" ")+" 0\n").join("");
let q=res+and+xor;
assert(q===G.length-1,"source floor not attained");
return {graph:kind==="K4"?"K4":"prism"+k,t,h:g.h,m:G.length,n:n+t,
dimacs_bytes:lines.length,odd_models:0,even_models:evenModels*guards,
source_deletion_sat:G.length,sign_flip_sat:sign,
guard_res:res,and3:and,xor:xor,minimum:q}}
function run(){let a=[];for(let t=0;t<=3;t++)a.push(one("K4",0,t));
for(let t=0;t<=2;t++)a.push(one("prism",3,t));
for(let t=0;t<=1;t++)a.push(one("prism",4,t));
return {claim:"GUARD-REPLICATION352",cases:a}}
if(typeof require!=="undefined" && typeof module!=="undefined" && require.main===module)
console.log(JSON.stringify(run(),null,2));
