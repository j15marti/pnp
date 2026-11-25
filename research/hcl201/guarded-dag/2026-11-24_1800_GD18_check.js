"use strict";
function run(){
const metrics={gaussian:0,xors:0,transitions:0,positive:0,merges:0,peakStates:0,closureScans:0,pins:0,assertions:0,referenceWords:0,verifiedWitnesses:0,probes:0};
const assert=(c,msg)=>{metrics.assertions++;if(!c)throw Error(msg)};
const bit=i=>1n<<BigInt(i), pivot=x=>x.toString(2).length-1;
function par(x){let p=0;while(x){x&=x-1n;p^=1}return p}
function solve(eq){metrics.gaussian++;let M=new Map();for(let [a,b] of eq){while(a){let p=pivot(a);if(!M.has(p)){M.set(p,[a,b]);break}let [v,c]=M.get(p);a^=v;b^=c;metrics.xors++}if(!a&&b)return null}let x=0n;for(let p of [...M.keys()].sort((a,b)=>a-b)){let [v,c]=M.get(p);if(par(v&x)!==c)x|=bit(p)}return {rank:M.size,x,M}}
const span=rows=>[...solve(rows.map(a=>[a,0])).M.values()].map(r=>r[0]);
function inter(A,B){let bm=span(B).sort((a,b)=>pivot(b)-pivot(a)),R=new Map(),out=[];for(let a of span(A)){let z=a,t=a;for(let b of bm){if(z&bit(pivot(b))){z^=b;metrics.xors++}}while(z){let p=pivot(z);if(!R.has(p)){R.set(p,[z,t]);break}let [v,u]=R.get(p);z^=v;t^=u;metrics.xors+=2}if(!z)out.push(t)}return span(out)}
const eqword=(W,w)=>W.map((a,j)=>[a,(w>>j)&1]);
const eqx=(W,x)=>W.map(a=>[a,par(a&x)]);
const holds=(g,x)=>g.every(([a,b])=>par(a&x)===b);
const E=(u,v,g)=>({u,v,g});
function reach(edges,s,x){let R=bit(s);for(let e of edges)if((R&bit(e.u))&&holds(e.g,x))R|=bit(e.v);return R}
function closure(edges,s,t,H=[]){H=H.slice();while(true){metrics.closureScans++;let base=solve(H);if(!base)return {H,unsat:true};let poss=[],mand=[];for(let e of edges){let z=solve(H.concat(e.g));poss.push(!!z);mand.push(!!z&&z.rank===base.rank)}
let R=bit(s),P=bit(s),B=bit(t);for(let i=0;i<edges.length;i++){let e=edges[i];if(mand[i]&&(R&bit(e.u)))R|=bit(e.v);if(poss[i]&&(P&bit(e.u)))P|=bit(e.v)}
if(R&bit(t))return {H,unsat:true};if(!(P&bit(t)))return {H,unsat:false};
for(let i=edges.length-1;i>=0;i--){let e=edges[i];if(mand[i]&&(B&bit(e.v)))B|=bit(e.u)}
let pin=null;for(let i=0;i<edges.length;i++){let e=edges[i];if(!poss[i]||mand[i]||!(R&bit(e.u))||!(B&bit(e.v)))continue;let z=solve(H.concat(e.g));if(z.rank!==base.rank+1)continue;for(let [a,b] of e.g){let q=solve(H.concat([[a,b]]));if(q&&q.rank===base.rank+1){pin=[a,b^1];break}}if(pin)break}
if(!pin)return {H,unsat:false};H.push(pin);metrics.pins++}}
function kernel(n,edges,sources,sinks,accept,probe=null){
let events=edges.slice();if(probe)events.push({g:[probe],query:true});let m=events.length;
let U=events.map(e=>span(e.g.map(r=>r[0]))),P=[[]],S=Array(m+1);S[m]=[];
for(let i=0;i<m;i++)P.push(span(P[i].concat(U[i])));
for(let i=m-1;i>=0;i--)S[i]=span(S[i+1].concat(U[i]));
let W=P.map((p,i)=>inter(p,S[i]));
let endmask=0n,srcmask=0n;for(let s of sources)srcmask|=bit(s);for(let s of sources.concat(sinks))endmask|=bit(s);
let first=new Map(),last=new Map();for(let i=0;i<m;i++){let e=events[i];if(e.query)continue;for(let v of [e.u,e.v]){if(!first.has(v))first.set(v,i);last.set(v,i)}}
let live=Array.from({length:m+1},(_,i)=>{let mask=endmask;for(let [v,f] of first)if(f<i&&last.get(v)>=i)mask|=bit(v);return mask});
let widths=W.map(w=>w.length),maxW=Math.max(...widths),maxR=Math.max(0,...U.map(u=>u.length));if(maxW>12)throw Error("test width cap");
let D=new Map([["0:"+srcmask,{syn:0,R:srcmask,c:1n,x:0n}]]),peak=1,work=0;
for(let i=0;i<m;i++){let e=events[i],next=new Map(),delta=P[i+1].length-P[i].length;
for(let state of D.values())for(let z=0;z<2**W[i+1].length;z++){
let rows=eqword(W[i],state.syn).concat(eqword(W[i+1],z)),base=solve(rows);metrics.transitions++;work++;if(!base)continue;
let exp=delta+W[i].length-base.rank;assert(exp>=0,"base exponent");let all=1n<<BigInt(exp),yesS=solve(rows.concat(e.g)),yes=0n;
if(yesS){let ex=delta+W[i].length-yesS.rank;assert(ex>=0,"yes exponent");yes=1n<<BigInt(ex)}
assert(yes<=all,"subset");for(let truth of [0,1]){if(e.query&&!truth)continue;let cnt=truth?yes:all-yes;if(!cnt)continue;metrics.positive++;
let R=state.R;if(!e.query&&truth&&(R&bit(e.u)))R|=bit(e.v);R&=live[i+1];let key=z+":"+R,existing=next.get(key);
if(existing){existing.c+=state.c*cnt;metrics.merges++;continue}
let fixed=eqx(P[i],state.x).concat(eqword(W[i+1],z)),wit=null;
if(truth)wit=solve(fixed.concat(e.g));else for(let [a,b] of e.g){wit=solve(fixed.concat([[a,b^1]]));if(wit)break}
assert(!!wit,"positive transition must lift");assert(holds(eqx(P[i],state.x),wit.x),"prefix preserved");assert(holds(e.g,wit.x)===!!truth,"truth lift");
next.set(key,{syn:z,R,c:state.c*cnt,x:wit.x})}}
D=next;peak=Math.max(peak,D.size);metrics.peakStates=Math.max(metrics.peakStates,D.size)}
let total=0n,x=null;for(let a of D.values())if(accept(a.R)){total+=a.c;if(x===null)x=a.x}
total*=1n<<BigInt(n-P[m].length);if(x!==null){let R=0n;for(let s of sources)R|=bit(s);for(let e of edges)if((R&bit(e.u))&&holds(e.g,x))R|=bit(e.v);assert(accept(R)&&(!probe||holds([probe],x)),"final witness");metrics.verifiedWitnesses++}
return {total,x,maxW,maxR,peak,work}}
function nullbasis(A,n){let b=solve(A.map(a=>[a,0]));let free=Array.from({length:n},(_,i)=>i).filter(i=>!b.M.has(i));return free.map(k=>solve(A.map(a=>[a,0]).concat(free.map(j=>[bit(j),j===k?1:0]))).x)}
function hull(n,edges,s,t,root,H){if(!root.total)return {rank:null,pins:H.length};let dif=[],origin=root.x,archive=H.slice(),checked=new Set();
while(true){let grow=false;for(let a of nullbasis(dif,n)){let key=a.toString();if(checked.has(key))continue;metrics.probes++;let b=par(a&origin),q=kernel(n,edges,[s],[t],R=>!(R&bit(t)),[a,b^1]);if(q.total){dif=span(dif.concat([q.x^origin]));grow=true;break}checked.add(key);let z=solve(archive.concat([[a,b]]));if(z.rank>solve(archive).rank){archive.push([a,b]);metrics.pins++;let c=closure(edges,s,t,archive);assert(!c.unsat,"closure after proved pin");archive=c.H}}
if(!grow)break}
assert(solve(archive).rank===n-dif.length,"hull completeness rank");return {rank:dif.length,pins:archive.length,archive}}
let seed=180024;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
let results={seed:180024,random:{sat:0,unsat:0},fano:[],scaling:[],identity:[],metrics};
function small(n,edges,t,full=true){let c=closure(edges,0,t),r=kernel(n,edges,[0],[t],R=>!(R&bit(t)));let words=[];for(let x=0n;x<(1n<<BigInt(n));x++){metrics.referenceWords++;if(!(reach(edges,0,x)&bit(t)))words.push(x)}
assert(r.total===BigInt(words.length),"reference count");assert(!c.unsat||!r.total,"closure sound");for(let x of words)assert(holds(c.H,x),"closure pin sound");if(full&&words.length){let h=hull(n,edges,0,t,r,c.H);assert(h.rank===span(words.map(x=>x^words[0])).length,"full hull");for(let x of words)assert(holds(h.archive,x),"global pin sound")}
return r}
for(let j=0;j<72;j++){let n=3+rnd(5),v=3+rnd(4),edges=[];for(let u=0;u<v-1;u++)for(let w=u+1;w<v;w++){if(rnd(5)<2)continue;let g=[];for(let k=0,l=rnd(5);k<l;k++)g.push([BigInt(rnd(2**n)),rnd(2)]);edges.push(E(u,w,g))}let r=small(n,edges,v-1,j<24);results.random[r.total?"sat":"unsat"]++}
let triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],f=[];for(let tr of triples)for(let b of [0,1])f.push(E(0,1,tr.map(i=>[bit(i),b])));
for(let i=-1;i<f.length;i++){let es=f.filter((_,j)=>j!==i),r=small(7,es,1,true);assert(r.total===BigInt(i<0?0:5),"Fano");results.fano.push(Number(r.total))}
for(let r of [8,32,64,128])for(let sat of [false,true]){let k=3,n=k*r,es=[];for(let i=0;i<k;i++){let a=bit(i*r);if(!sat||i<k-1){es.push(E(i,i+1,[[a,0]]));es.push(E(i,i+1,[[a,0]]))}es.push(E(i,i+1,[[a,1]]));es.push(E(i,i+1,[[a,1]]));es.push(E(i,i+1,Array.from({length:r},(_,j)=>[bit(i*r+j),0])))}
let c=closure(es,0,k),z=kernel(n,es,[0],[k],R=>!(R&bit(k))),expect=sat?((1n<<BigInt(r-1))-1n)*(1n<<BigInt((k-1)*r)):0n;
assert(z.total===expect,"scaling count");assert(!c.unsat||!z.total,"scaling closure");
results.scaling.push({n,sat,count:z.total.toString(),localRank:z.maxR,cutRank:z.maxW,peakStates:z.peak,transitions:z.work})}
for(let j=0;j<12;j++){let n=5,ga=[E(0,1,[[1n,0],[2n,1]]),E(0,1,[[4n,1]])],gb=ga.map(e=>E(2,3,e.g));if(j%2)gb[0]=E(2,3,[[1n,1],[2n,1]]);let es=ga.concat(gb);let z=kernel(n,es,[0,2],[1,3],R=>!!(R&2n)!==!!(R&8n));let ref=0n;for(let x=0n;x<32n;x++){metrics.referenceWords++;if(!!(reach(ga,0,x)&2n)!==!!(reach(gb,2,x)&8n))ref++}assert(z.total===ref,"identity count");results.identity.push(Number(z.total))}
return results;
}
console.log(JSON.stringify(run(),null,2));
