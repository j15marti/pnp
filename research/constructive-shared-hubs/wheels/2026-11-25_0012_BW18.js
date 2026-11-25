'use strict';
const fs=require('fs');
function run(gd,bs){
let assertions=0, scans=0, shiftChecks=0, nodes=0, rowChecks=0;
function check(x){assertions++;if(!x)throw Error("assert "+assertions)}
const word=(v,x)=>v.map(i=>x[i]).join("");
const invert=s=>s.replace(/[01]/g,c=>c==="0"?"1":"0");
function closure(t,p){while(true){scans++;let change=false;for(const o of t){const a=o.a.filter(w=>{rowChecks++;return o.v.every((v,i)=>p[v]<0||p[v]===+w[i])});if(!a.length)return false;for(let i=0;i<o.v.length;i++)if(p[o.v[i]]<0&&a.every(w=>w[i]===a[0][i])){p[o.v[i]]=+a[0][i];change=true}}if(!change)return true}}
function solve(t,p){nodes++;p=p.slice();if(!closure(t,p))return null;let v=t.flatMap(o=>o.v).find(v=>p[v]<0);if(v===undefined)return p;for(let b=0;b<2;b++){let q=p.slice();q[v]=b;let z=solve(t,q);if(z)return z}return null}
function shifts(A,B){if(A.a.length!==B.a.length||!A.a.length)return [];const set=new Set(B.a), x=A.a[0], xor=(a,b)=>a.split("").map((c,i)=>+c^+b[i]).join("");return B.a.map(y=>xor(x,y)).filter(d=>A.a.every(w=>{shiftChecks++;return set.has(xor(w,d))}))}
function parity(x){let p=0;while(x){p^=1;x&=x-1n}return p}
function localEqs(v,S){if(!S.length)return null;const k=v.length; // exhaustive orthogonal masks in this checker only; theorem uses nullspace
let out=[];for(let a=1;a<2**k;a++){const f=s=>s.split("").reduce((p,c,i)=>p^((a>>i&1)&+c),0),b=f(S[0]);if(S.every(s=>f(s)===b)){let mask=0n;v.forEach((q,i)=>{if(a>>i&1)mask|=1n<<BigInt(q)});out.push([mask,b])}}return out}
function linear(E,n){let B=new Map();for(let [a,b] of E){while(a){let i=a.toString(2).length-1;if(B.has(i)){let z=B.get(i);a^=z[0];b^=z[1]}else{B.set(i,[a,b]);break}}if(!a&&b)return null}let x=0n;for(let [i,[a,b]] of [...B].sort((a,b)=>a[0]-b[0]))if(parity(a&x)!==b)x|=1n<<BigInt(i);return {rank:B.size,x:Array.from({length:n},(_,i)=>Number(x>>BigInt(i)&1n))}}
function equiv(A,B,p,q){if(A.length!==B.length)return null;let E=[];for(let a of A){let b=B.find(z=>z.id===a.id);if(!b||String(a.v)!==String(b.v))return null;let s=localEqs(a.v,shifts(a,b));if(!s)return null;E.push(...s)}for(let i=0;i<p.length;i++){if((p[i]<0)!==(q[i]<0))return null;if(p[i]>=0)E.push([1n<<BigInt(i),p[i]^q[i]])}return linear(E,p.length)}
// Acyclic AND/OR circuit, raw signed literals, per-table reference.
function compile(t,p,local){let n=p.length,r=n+1,next=r,trip=[],gates=[],refs=0,localCount=0,owners=[];
function and(a,b,h){let z=++next;gates.push([a,b,h,z]);trip.push([a,b,-z],[-z,a,h],[-z,b,h]);return z}
function or(a,b,h){return -and(-a,-b,h)}
for(const o of t){let start=gates.length,ts=trip.length;const inv=o.v.length>0&&o.a.every(s=>o.a.includes(invert(s))),h=local&&inv?o.v[0]+1:r;let v=o.v.map(i=>i+1),rows=o.a;if(local&&inv){localCount++;v=v.slice(1);rows=rows.filter(w=>w[0]==="0").map(w=>w.slice(1))}else refs++;
// prefix sharing
let prefixes=new Map([["",-h]]);let out=h;for(const w of rows){for(let j=1;j<=w.length;j++){let key=w.slice(0,j);if(!prefixes.has(key)){let a=prefixes.get(key.slice(0,-1)),b=w[j-1]==="1"?v[j-1]:-v[j-1];prefixes.set(key,j===1?b:and(a,b,h))}}let a=prefixes.get(w);out=out===h?a:or(out,a,h)}trip.push([out,h,h]);owners.push({id:o.id,h,inv,g0:start,g1:gates.length,t0:ts,t1:trip.length})}
for(let i=0;i<n;i++)if(p[i]>=0)trip.push([p[i]?i+1:-(i+1),r,r]);
return {n,r,next,trip,gates,owners,refs,localCount}}
function value(a,z){return z[Math.abs(a)]^(a<0?1:0)}
function evalGate(g,z){let [a,b,h,o]=g;z[o]=((value(a,z)^z[h])&(value(b,z)^z[h]))^z[h]}
function nae(t,z){let a=value(t[0],z),b=value(t[1],z),c=value(t[2],z);return a!==b||b!==c}
function physical(c,z){let vertices=[],edges=[],occ=new Map();function vert(kind,b){vertices.push({kind,b});return vertices.length-1}function edge(u,pu,v,pv,s){edges.push([u,pu,v,pv,s])}
for(const t of c.trip){let bits=t.map(a=>value(a,z)),d=2-bits.reduce((a,b)=>a+b,0);check(d===0||d===1);let di=++c.next;z[di]=d;for(let k=0;k<2;k++){let u=vert("B",[...bits,d]);[...t,di].forEach((a,p)=>{let i=Math.abs(a);if(!occ.has(i))occ.set(i,[]);occ.get(i).push([u,p,a<0?1:0])})}}
for(const [i,L] of occ){check(L.length%2===0);if(L.length===2){let [a,b]=L;edge(a[0],a[1],b[0],b[1],a[2]^b[2]);continue}let k=L.length/2-1,vs=Array.from({length:k},()=>vert("E",Array(4).fill(z[i]))),free=[];for(let j=0;j<k;j++){if(j+1<k)edge(vs[j],3,vs[j+1],0,0);for(let p=0;p<4;p++)if(!(j>0&&p===0)&&!(j+1<k&&p===3))free.push([vs[j],p])}check(free.length===L.length);L.forEach((a,j)=>edge(a[0],a[1],free[j][0],free[j][1],a[2]))}
let old=edges;edges=[];for(const [u,pu,v,pv,s] of old){let bit=vertices[v].b[pv],q=Array.from({length:5},()=>vert("E",Array(4).fill(bit))),used=Array(5).fill(0);for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)edge(q[i],used[i]++,q[j],used[j]++,0);edge(u,pu,q[0],used[0]++,s);edge(q[1],used[1]++,v,pv,0)}
let seen=new Set(),pairs=new Set();for(let [u,a,v,b,s] of edges){check(u!==v);let key=[Math.min(u,v),Math.max(u,v)].join(",");check(!pairs.has(key));pairs.add(key);check(!seen.has(4*u+a)&&!seen.has(4*v+b));seen.add(4*u+a);seen.add(4*v+b);check((vertices[u].b[a]^vertices[v].b[b])===s)}check(seen.size===4*vertices.length);for(let v of vertices)check(v.kind==="E"?v.b.every(b=>b===v.b[0]):v.b.reduce((a,b)=>a+b,0)===2);return {vertices:vertices.length,wires:edges.length}}
function test(c,t,p,w){let z=Array(c.next+1).fill(0);for(let i=0;i<p.length;i++)z[i+1]=Math.max(0,w[i]);for(const g of c.gates)evalGate(g,z);check(c.trip.every(a=>nae(a,z)));let localWords=0;for(let j=0;j<t.length;j++){let o=t[j],a=c.owners[j],set=new Set(o.a);for(let k=0;k<2**o.v.length;k++){let w=o.v.map((_,i)=>String(k>>i&1)).join("");o.v.forEach((v,i)=>z[v+1]=+w[i]);for(let i=a.g0;i<a.g1;i++)evalGate(c.gates[i],z);check(c.trip.slice(a.t0,a.t1).every(t=>nae(t,z))===set.has(w));localWords++}}for(let i=0;i<p.length;i++)z[i+1]=Math.max(0,w[i]);for(const g of c.gates)evalGate(g,z);return {localWords,...physical(c,z)}}
let jobs=[];
for(let i=0;i<gd.jobs.length;i++){let j=gd.jobs[i],s=bs.snapshots[i];check(j.id===s.id&&JSON.stringify(j.guard)===JSON.stringify(s.guard));let p=j.p.slice(),t=j.final,w=solve(t,p);check(!!w);let n1=compile(t,p,false),n2=compile(t,p,true);let g1=n1.gates.length,g2=n2.gates.length,tr1=n1.trip.length,tr2=n2.trip.length;let f=test(n2,t,p,w);let lift=w.slice();for(const m of [...j.merges].reverse()){let z=m.rows.find(a=>a[0]===word(m.scope,lift));check(!!z);m.private.forEach((v,i)=>lift[v]=+z[1][i])}check(s.remaining.every(o=>o.a.includes(o.v.reduce((a,v,i)=>a+(lift[v]<<i),0))));for(let e of [...s.eliminations].reverse()){let k=e.u.reduce((a,v,i)=>a+(lift[v]<<i),0),z=e.lift.find(a=>a[0]===k);check(!!z);lift[e.v]=z[1]}check(j.guard.every(([v,b])=>lift[v]===b));let eq=equiv(t,t,p,p);check(!!eq);jobs.push({id:j.id,guard:j.guard,rows:t.reduce((s,o)=>s+o.a.length,0),globalGates:g1,localGates:g2,globalTriples:tr1,localTriples:tr2,localOwners:n2.localCount,globalOwners:n2.refs,activeShiftRank:eq.rank,freeShiftDimension:p.length-eq.rank,...f,witness:lift})}
let A=gd.jobs[3],B=gd.jobs[4],e=equiv(A.final,B.final,A.p,B.p);check(!!e);for(let a of A.final){let b=B.final.find(z=>z.id===a.id);let shift=word(a.v,e.x);check(shifts(a,b).includes(shift))}
let control=[{id:0,v:[0,1,2],a:["001","010","011","100","101","110"]}];let no=equiv(control,[{...control[0],a:["000","001","010","011","100","101"]}],[-1,-1,-1],[-1,-1,-1]);check(!no);
for(let h=0;h<2;h++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){let legal=[];for(let z=0;z<2;z++){let w=[0,a,b,h,z];if([[1,2,-4],[-4,1,3],[-4,2,3]].every(t=>nae(t,w)))legal.push(z)}check(legal.length===1&&legal[0]===(((a^h)&(b^h))^h))}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map((v,id)=>({id,v,a:control[0].a}));check(!solve(fano,Array(7).fill(-1)));check(!!solve(fano.slice(1),Array(7).fill(-1)));
return {jobs,pinTransport:e,assertions,scans,shiftChecks,nodes,rowChecks,limitations:"local orthogonal-mask enumeration used for tests only; no general polynomial solver; source lift checked against BS17 tables and pins, original source owners not yet checked"}
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
