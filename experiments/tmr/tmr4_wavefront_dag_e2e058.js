"use strict";
const REVISION="tmr4-wavefront-dag058.v1",SEED=20261115;
function audit(){
let asserts=0,gateReplays=0,comparisons=0,ranks=0;
function ok(x,m){asserts++;if(!x)throw Error("ASSERT "+m);}
function canonical(v){if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";if(v&&typeof v==="object")return "{"+Object.keys(v).sort().map(k=>JSON.stringify(k)+":"+canonical(v[k])).join(",")+"}";return JSON.stringify(v);}
function ident(v){if(typeof v!=="string"||!/^(x|g)(0|[1-9]\d*)$/.test(v))throw Error("reference");return [v[0],+v.slice(1)];}
function gate(op,a,b){return (op>>(2*a+b))&1;}
function parse(bytes){
let o=JSON.parse(bytes);if(canonical(o)!==bytes)throw Error("noncanonical bytes");if(!o||Object.keys(o).sort().join(",")!=="gates,n,out"||!Array.isArray(o.gates)||!Number.isSafeInteger(o.n)||o.n<1||o.gates.length<1)throw Error("shape");
let n=o.n,G=new Map();for(let g of o.gates){if(!g||Object.keys(g).sort().join(",")!=="a,b,id,op")throw Error("gate shape");let [t,i]=ident(g.id);if(t!=="g"||i>=o.gates.length||G.has(g.id)||!Number.isInteger(g.op)||g.op<0||g.op>15)throw Error("gate");G.set(g.id,g);}
if(G.size!==o.gates.length||!G.has(o.out))throw Error("id/output");
for(let g of G.values())for(let v of [g.a,g.b]){let [t,i]=ident(v);if(t==="g"?!G.has(v):i>=n)throw Error("operand");}
let depth=new Map(),gray=new Set();function dep(v){if(v[0]==="x")return 0;if(depth.has(v))return depth.get(v);if(gray.has(v))throw Error("cycle");gray.add(v);let g=G.get(v),d=1+Math.max(dep(g.a),dep(g.b));gray.delete(v);depth.set(v,d);return d;}
for(let v of G.keys())dep(v);
let anc=new Set();function trace(v){if(v[0]==="x"||anc.has(v))return;anc.add(v);let g=G.get(v);trace(g.a);trace(g.b);}trace(o.out);
if(anc.size!==G.size)throw Error("out-of-class dead gate");
let inputs=Array.from({length:n},()=>new Set()),layers=new Map();
for(let [v,g] of G){let d=depth.get(v);if(!layers.has(d))layers.set(d,[]);layers.get(d).push(v);for(let p of [g.a,g.b]){if(p[0]==="x")inputs[+p.slice(1)].add(d);else if(depth.get(p)!==d-1)throw Error("out-of-class long gate edge");}}
if(inputs.some(x=>x.size!==1))throw Error("out-of-class input spanning layers");
let D=depth.get(o.out),sched=[],k=0;
for(let d=1;d<=D;d++){let xs=inputs.map((levels,i)=>levels.has(d)?"x"+i:null).filter(Boolean),gs=(layers.get(d)||[]).sort((a,b)=>+a.slice(1)- +b.slice(1));k=Math.max(k,xs.length,gs.length);sched.push(...xs,...gs);}
if(sched.length!==n+G.size)throw Error("schedule incomplete");
let pos=new Map(sched.map((v,i)=>[v,i])),last=new Map(sched.map(v=>[v,-1]));
for(let [v,g] of G){let p=pos.get(v);for(let z of [g.a,g.b]){if(pos.get(z)>=p)throw Error("schedule invalid");last.set(z,Math.max(last.get(z),p));}}
last.set(o.out,sched.length);
let live=sched.map((_,i)=>sched.filter(v=>pos.get(v)<=i&&i<last.get(v))),w=Math.max(...live.map(v=>v.length));ok(w<=3*k,"wavefront bound");
let stages=[];for(let i=0;i<sched.length;i++){let v=sched[i];if(v[0]==="x"){if(stages.length)stages[stages.length-1].end=i-1;stages.push({input:v,gates:[],end:sched.length-1});}else{if(!stages.length)throw Error("stage");stages[stages.length-1].gates.push(v);}}
ok(stages.length===n,"read-once");let boundaries=stages.map(s=>live[s.end]);
return {n,G,out:o.out,bytes,sched,live,w,k,stages,boundaries,rho:stages.map(s=>s.input),D};
}
function advance(A,state,i,bit,trace){let v={...state},s=A.stages[i];v[s.input]=bit;for(let id of s.gates){let g=A.G.get(id);ok(v[g.a]===0||v[g.a]===1,"left value");ok(v[g.b]===0||v[g.b]===1,"right value");v[id]=gate(g.op,v[g.a],v[g.b]);gateReplays++;if(trace)trace.push([id,v[id]]);}
let q={};for(let id of A.boundaries[i])q[id]=v[id];return q;}
function fromKey(ids,s){let q={};for(let i=0;i<ids.length;i++)q[ids[i]]=+s[i];return q;}
function key(ids,q){return ids.map(id=>q[id]).join("");}
function direct(A,x){let q={},trace=[];for(let id of A.sched){if(id[0]==="x")q[id]=x[+id.slice(1)];else{let g=A.G.get(id);q[id]=gate(g.op,q[g.a],q[g.b]);trace.push([id,q[id]]);}}return {value:q[A.out],trace};}
function count(A){let curr=new Map([["",1n]]),vertices=0,edges=0;for(let i=0;i<A.n;i++){vertices+=curr.size;let next=new Map(),before=i?A.boundaries[i-1]:[];for(let [s,m] of curr)for(let b=0;b<=1;b++){let newval=advance(A,fromKey(before,s),i,b,null),ns=key(A.boundaries[i],newval);next.set(ns,(next.get(ns)||0n)+m);edges++;}curr=next;}
let total=0n;for(let [s,m] of curr)if(fromKey(A.boundaries[A.n-1],s)[A.out])total+=m;ok(edges===2*vertices,"two arcs");ok(vertices<=A.n*2**A.w,"node cap");return {total,vertices,edges};}
function pow(a,e,p){let r=1;while(e){if(e&1)r=r*a%p;a=a*a%p;e=Math.floor(e/2);}return r;}
function rank(A,p){let m=A.map(row=>row.slice()),h=m.length,w=m[0].length,r=0;for(let c=0;c<w&&r<h;c++){let j=r;while(j<h&&m[j][c]===0)j++;if(j===h)continue;[m[r],m[j]]=[m[j],m[r]];let iv=pow(m[r][c],p-2,p);for(let t=c;t<w;t++)m[r][t]=m[r][t]*iv%p;for(let j=0;j<h;j++)if(j!==r){let z=m[j][c];if(z)for(let t=c;t<w;t++)m[j][t]=((m[j][t]-z*m[r][t])%p+p)%p;}r++;}return r;}
function test(A){let truth=[],sat=0n,n=A.n;for(let mask=0;mask<2**n;mask++){let x=Array.from({length:n},(_,j)=>(mask>>j)&1),a=direct(A,x),state={},trace=[];for(let i=0;i<n;i++)state=advance(A,state,i,x[+A.rho[i].slice(1)],trace);ok(a.value===state[A.out],"terminal");ok(JSON.stringify(a.trace)===JSON.stringify(trace),"all-step trace");truth.push(a.value);sat+=BigInt(a.value);comparisons++;}
let bp=count(A);ok(bp.total===sat,"multiplicity");
for(let i=0;i<=n;i++){let M=[];for(let a=0;a<2**i;a++){let row=[];for(let b=0;b<2**(n-i);b++){let x=Array(n).fill(0);for(let j=0;j<i;j++)x[+A.rho[j].slice(1)]=(a>>j)&1;for(let j=i;j<n;j++)x[+A.rho[j].slice(1)]=(b>>(j-i))&1;let mask=x.reduce((s,v,j)=>s+(v<<j),0);row.push(truth[mask]);}M.push(row);}let bound=2**(i?A.boundaries[i-1].length:0);for(let p of [2,101]){ok(rank(M,p)<=bound,"cut rank");ranks++;}}
let counts=new Map();for(let g of A.G.values())for(let id of [g.a,g.b])if(id[0]==="g")counts.set(id,(counts.get(id)||0)+1);
return {n,g:A.G.size,k:A.k,w:A.w,depth:A.D,nodes:bp.vertices,arcs:bp.edges,count:String(sat),sourceBits:8*A.bytes.length,rho:A.rho,sharedGates:[...counts].filter(([id,num])=>num>1).map(([id])=>id)};}
let rng=SEED>>>0;function random(n){rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return (rng>>>0)%n;}
function make(kind,code){let g=[];function add(a,b){let id="g"+g.length;g.push({id,a,b,op:code===null?random(16):code});return id;}
if(kind===0){let z=add("x0","x0");return {n:1,gates:g,out:z};}
let a=add("x0","x1"),b=add("x2","x3"),c=add(a,b),d=add(a,b);
if(kind===1){let z=add(c,d);return {n:4,gates:g,out:z};}
g[2].b="x4";if(kind===2){let z=add(c,d);return {n:5,gates:g,out:z};}
let f=add(c,"x5"),h=add(d,"x5"),z=add(f,h);return {n:6,gates:g,out:z};}
function rejection(s,tag){let failed=false;try{parse(typeof s==="string"?s:canonical(s));}catch(e){failed=true;}ok(failed,"must reject "+tag);}
let cases=[],sources=[],counts={};for(let kind=0;kind<4;kind++){let rounds=[12,48,40,36][kind];for(let j=0;j<rounds;j++){let o=make(kind,j===0?8:j===1?7:j===2?6:null);if(j%3===2)o.gates.reverse();let src=canonical(o),A=parse(src);cases.push(test(A));sources.push(src);}counts["family"+kind]=rounds;}
let d={n:6,gates:[{id:"g0",a:"x0",b:"x3",op:7},{id:"g1",a:"x1",b:"x4",op:7},{id:"g2",a:"x2",b:"x5",op:7},{id:"g3",a:"g0",b:"g1",op:8},{id:"g4",a:"g2",b:"g2",op:8},{id:"g5",a:"g3",b:"g4",op:8}],out:"g5"},disj=parse(canonical(d));cases.push(test(disj));sources.push(canonical(d));counts.disj=1;
let M=[];for(let x=0;x<8;x++){let row=[];for(let y=0;y<8;y++){let b=[x&1,(x>>1)&1,(x>>2)&1,y&1,(y>>1)&1,(y>>2)&1];row.push(direct(disj,b).value);}M.push(row);}ok(rank(M,2)===8&&rank(M,101)===8,"DISJ grouped rank 8");
rejection({n:3,gates:[{id:"g0",a:"x0",b:"x1",op:8},{id:"g1",a:"g0",b:"x2",op:14},{id:"g2",a:"g0",b:"g1",op:6}],out:"g2"},"skip gate layer");
rejection({n:2,gates:[{id:"g0",a:"x0",b:"x1",op:8},{id:"g1",a:"g0",b:"x0",op:14}],out:"g1"},"spanning input");
rejection({n:2,gates:[{id:"g0",a:"x0",b:"x1",op:8},{id:"g1",a:"x0",b:"x1",op:14}],out:"g1"},"dead gate");
rejection({n:1,gates:[{id:"g0",a:"g1",b:"x0",op:8},{id:"g1",a:"g0",b:"x0",op:14}],out:"g1"},"cycle");
rejection({n:1,gates:[{id:"g0",a:"x0",b:"x0",op:8},{id:"g0",a:"x0",b:"x0",op:14}],out:"g0"},"duplicate gate");
rejection('{"gates":[],"n":1,"n":2,"out":"g0"}',"noncanonical duplicate key");
rejection({n:1,gates:[{id:"g0",a:"x0",b:"x0",op:16}],out:"g0"},"bad op");
return {revision:REVISION,seed:SEED,families:counts,valid:cases.length,rejected:7,assertions:asserts,comparisons,gateReplays,ranks,failures:0,disjGroupedRank:8,maxActualW:Math.max(...cases.map(x=>x.w)),maxLayerK:Math.max(...cases.map(x=>x.k)),maxNodes:Math.max(...cases.map(x=>x.nodes)),totalNodes:cases.reduce((s,x)=>s+x.nodes,0),totalArcs:cases.reduce((s,x)=>s+x.arcs,0),cases,canonicalSources:sources};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
