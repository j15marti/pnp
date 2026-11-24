"use strict";
function runDS06(){
const D=8n, mod=(x,m)=>(x%m+m)%m, bit=(i)=>1n<<BigInt(i), par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p}, stats={orbitCalls:0,visits:0,pivots:0,subtractions:0,peakMasks:0,productEdges:0,closurePasses:0,affineEquations:0,referenceWords:0,verifiedWitnesses:0,assertions:0};
function check(x,msg){stats.assertions++;if(!x)throw Error(msg)}
function add(P,k,v,m=2n*D){let a=mod((P.get(k)||0n)+v,m);if(a)P.set(k,a);else P.delete(k)}
function sum(...ps){let p=new Map;for(let f of ps)for(let [k,v] of f)add(p,k,v);return p}
function evalP(p,z,m=2n*D){let a=0n;for(let [k,v] of p)a+=par(k&z)?-v:v;return mod(a,m)}
function out(fs,z){let a=0n;fs.forEach((f,i)=>{let v=evalP(f,z);if(v!==0n&&v!==D)throw Error("not Boolean");if(v===D)a|=bit(i)});return a}
function affineBit(k,b=0){let p=new Map;add(p,0n,D/2n);add(p,k,b?D/2n:-D/2n);return p}
function local(forms,table){let l=1<<forms.length,p=new Map;for(let s=0;s<l;s++){let c=0n,k=0n,b=0;for(let j=0;j<forms.length;j++)if(s>>j&1){k^=forms[j][0];b^=forms[j][1]}for(let u=0;u<l;u++)if(table[u])c+=par(BigInt(s&u))?-1n:1n;add(p,k,(b?-c:c)*D/BigInt(l))}return p}
function orbit(d,ks,m,visit){stats.orbitCalls++;stats.peakMasks=Math.max(stats.peakMasks,ks.length);let piv=new Map,q=[],head=0;function push(z){stats.visits++;let v=ks.map(k=>par(k&z)?m-1n:1n);if(visit(z,v))return true;for(let i=0;i<v.length;i++)while(v[i]){let low=v[i]&-v[i],key=i+":"+low,p=piv.get(key);if(!p){piv.set(key,v);q.push(z);stats.pivots++;return false}for(let j=i;j<v.length;j++)v[j]=mod(v[j]-p[j],m);stats.subtractions++}return false}if(push(0n))return 0n;while(head<q.length){let z=q[head++];for(let j=0;j<d;j++){let w=z^bit(j);if(push(w))return w}}return null}
function reduce(v,b,q){for(let i=q-1;i>=0;i--)if((v&bit(i))&&b.has(i))v^=b.get(i);return v}
function insert(v,b,q){v=reduce(v,b,q);if(v)for(let i=q-1;i>=0;i--)if(v&bit(i)){b.set(i,v);break}}
function hull(d,fs){let q=fs.length,c=out(fs,0n),A=Array.from({length:d},(_,i)=>out(fs,bit(i))^c),b=new Map,ks=[...new Set([0n,...A.map((_,i)=>bit(i)),...fs.flatMap(f=>[...f.keys()])])];orbit(d,ks,2n*D,z=>{let v=out(fs,z)^c;for(let i=0;i<d;i++)if(z&bit(i))v^=A[i];insert(v,b,q);return false});return {c,A,b,r:b.size}}
function chart(d,eq){let B=new Map;for(let [v,t] of eq){for(let i=d-1;i>=0;i--)if(v&bit(i)&&B.has(i)){let [w,s]=B.get(i);v^=w;t^=s}if(!v){if(t)return null;continue}for(let i=d-1;i>=0;i--)if(v&bit(i)){B.set(i,[v,t]);break}}
let a=[],k=0;for(let i=0;i<d;i++)if(!B.has(i))a[i]=[bit(k++),0];for(let i=0;i<d;i++)if(B.has(i)){let [v,t]=B.get(i),w=0n;for(let j=0;j<i;j++)if(v&bit(j)){w^=a[j][0];t^=a[j][1]}a[i]=[w,t]}return {a,k}}
function sub(p,a){let r=new Map;for(let [s,v] of p){let k=0n,b=0;for(let j=0;j<a.length;j++)if(s&bit(j)){k^=a[j][0];b^=a[j][1]}add(r,k,b?-v:v)}return r}
function lift(a,z){let v=0n;for(let i=0;i<a.length;i++)if(par(a[i][0]&z)^a[i][1])v|=bit(i);return v}
function product(d,fs,h){let m=2n*D**BigInt(fs.length),P=new Map([[0n,1n]]);for(let i=0;i<fs.length;i++){let f=new Map(fs[i]);add(f,0n,D*(1n+((h>>BigInt(i))&1n)),m);let R=new Map;for(let [a,v] of P)for(let [b,w] of f){stats.productEdges++;add(R,a^b,v*w,m)}P=R;if(!P.size)return null}let ks=[...P.keys()];return orbit(d,ks,m,z=>evalP(P,z,m)!==0n)}
function solve(d,fs,h,cap=20,log=[]){stats.closurePasses++;if(!fs.length)return {status:"SAT",z:0n};let {c,A,b,r}=hull(d,fs),q=fs.length;log.push({d,q,r});let rhs=reduce(h^c,b,q),cols=A.map(v=>reduce(v,b,q)),eq=[];for(let i=0;i<q;i++)if(!b.has(i)){let v=0n;for(let j=0;j<d;j++)if(cols[j]&bit(i))v|=bit(j);eq.push([v,Number((rhs>>BigInt(i))&1n)])}stats.affineEquations+=eq.length;if(r<q){let C=chart(d,eq);if(!C)return {status:"UNSAT"};let gs=[],hh=0n;for(let i=0;i<q;i++)if(b.has(i)){if(h&bit(i))hh|=bit(gs.length);gs.push(sub(fs[i],C.a))}let ret=solve(C.k,gs,hh,cap,log);if(ret.status==="SAT")ret.z=lift(C.a,ret.z);return ret}if(r>cap)return {status:"UNKNOWN"};let z=product(d,fs,h);return z===null?{status:"UNSAT"}:{status:"SAT",z}}
let labels={SAT:0,UNSAT:0,UNKNOWN:0}, groups={};function test(name,d,fs,h,expected,cap=20,brute=true){let log=[],ret=solve(d,fs,h,cap,log);labels[ret.status]++;let g=groups[name]??={tests:0,SAT:0,UNSAT:0,UNKNOWN:0};g.tests++;g[ret.status]++;if(ret.status==="SAT"){check(out(fs,ret.z)===h,"bad lift");stats.verifiedWitnesses++}if(brute){let count=0;for(let z=0n;z<bit(d);z++){stats.referenceWords++;if(out(fs,z)===h)count++}check(ret.status==="UNKNOWN"||(ret.status==="SAT")===(count>0),"brute label");if(expected!==undefined)check(count===expected,"reference count");}else check(ret.status===expected,"scale label");return {status:ret.status,log}}
let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
for(let t=0;t<100;t++){let d=3+rnd(4),q=1+rnd(6),fs=[];for(let j=0;j<q;j++){let forms=Array.from({length:3},()=>[BigInt(1+rnd((1<<d)-1)),rnd(2)]),table=Array.from({length:8},()=>rnd(2)); // use high bits for independent random table
table=table.map(()=>((rnd(65536)>>>8)&1));fs.push(sum(local(forms,table),affineBit(bit(rnd(d)),rnd(2))))}test("random",d,fs,BigInt(rnd(1<<q)))}
let cube=Array.from({length:8},(_,a)=>local([0,1,2].map(i=>[bit(i),0]),Array.from({length:8},(_,u)=>+(u===a))));
for(let mask=0;mask<256;mask++)test("cube",3,cube.filter((_,i)=>mask>>i&1),0n,8-par(BigInt(0))-(mask.toString(2).split("1").length-1));
let lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]], fano=lines.map(L=>local(L.map(i=>[bit(i),0]),[1,0,0,0,0,0,0,1]));
let hostile=[test("Fano",7,fano,0n,0)];
for(let i=0;i<7;i++)for(let v of [0,7]){let f=fano.slice();f[i]=local(lines[i].map(j=>[bit(j),0]),Array.from({length:8},(_,u)=>+(u===v)));hostile.push(test("Fano",7,f,0n,5))}
let scaling=[];for(let d of [8,16,32,64]){let nfree=d/2, a=0n,b=0n;for(let i=1;i<nfree;i++)if(i%2)a|=bit(i);else b|=bit(i);let f=local([[bit(0),0],[a,0]],[0,0,0,1]),g=local([[bit(0),1],[b,0]],[0,0,0,1]),fs=[f,g];for(let i=nfree;i<d;i++)fs.push(sum(affineBit(bit(i)),i%2?f:g));let before=stats.visits;let sat=test("scale",d,fs,1n,"SAT",2,false),unsat=test("scale",d,fs,3n,"UNSAT",2,false);scaling.push({d,q:fs.length,sat:sat.log,unsat:unsat.log,visits:stats.visits-before})}
return {seed:20261124,labels,groups,stats,scaling,hostileRanks:hostile.map(x=>x.log[0].r)}
}
console.log(JSON.stringify(runDS06(),null,2));
