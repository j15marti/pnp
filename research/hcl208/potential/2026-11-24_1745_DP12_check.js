"use strict";
function runDP12(){
"use strict";
const stat={gauss:0,xor:0,terms:0,matEntries:0,queries:0,closureScans:0,forced:0,referenceWords:0,witnesses:0,assertions:0,peakLabels:0,peakMatrixEntries:0};
const ok=(x)=>{stat.assertions++;if(!x)throw Error("assertion "+stat.assertions)};
const bit=i=>1n<<BigInt(i), mask=(n,off=0)=>((1n<<BigInt(n))-1n)<<BigInt(off);
const par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
const cols=(x,n)=>Array.from({length:n},(_,i)=>i).filter(i=>x&bit(i));
function basis(rows,n,first=0n){stat.gauss++;let order=[...cols(first,n),...cols(mask(n)^first,n)], b=new Map();
 for(let [x,y] of rows){for(let i of order)if(x&bit(i)){if(b.has(i)){let [u,v]=b.get(i);x^=u;y^=v;stat.xor++}else{b.set(i,[x,y]);break}}if(x===0n&&y)return null}return b}
function chr(rows,block,q,n){let b=basis(rows,n);if(!b)return 0n;let rhs=0, x=q;for(let i=0;i<n;i++)if(x&bit(i)){if(!b.has(i))return 0n;let [u,v]=b.get(i);x^=u;rhs^=v;stat.xor++}ok(x===0n);let a=1n<<BigInt(cols(block,n).length-b.size);return rhs?-a:a}
function expand(F,n,blocks){let out=[],K=0,raw=[];for(let t of F){let b=basis(t.rows,n);if(!b)continue;let marginal=blocks.map(m=>[...basis(t.rows,n,mask(n)^m).values()].filter(([x])=>(x&~m)===0n));let all=marginal.flat(), core=[...all], extra=[];
 for(let row of b.values()){let r=basis([...core,row],n);if(r.size>core.length){core.push(row);extra.push(row)}}
 let k=extra.length;ok(k===b.size-all.length);K=Math.max(K,k);if(k>12)throw Error("cap");raw.push({t,marginal,extra,k})}
 for(let {t,marginal,extra,k} of raw)for(let j=0;j<2**k;j++){let q=0n,sign=0;for(let i=0;i<k;i++)if(j&(1<<i)){q^=extra[i][0];sign^=extra[i][1]}out.push({c:BigInt(t.c)*(sign?-1n:1n)*(1n<<BigInt(K-k)),m:marginal,q});stat.terms++}
 stat.peakLabels=Math.max(stat.peakLabels,out.length);return {out,K}}
function compile(n,blocks,edges,fs){let incident=fs.map((_,i)=>blocks.map((b,j)=>({b,j})).filter(({j})=>edges[j].includes(i)));let ex=fs.map((f,i)=>expand(f,n,incident[i].map(x=>x.b)));let adj=fs.map(()=>[]),priv=fs.map(()=>[]);
 edges.forEach((e,j)=>{if(e.length===2){adj[e[0]].push([e[1],j]);adj[e[1]].push([e[0],j])}else priv[e[0]].push(j)});
 const ix=(i,j)=>incident[i].findIndex(a=>a.j===j);
 let seen=new Set(), order=[],roots=[],parent=new Map();function dfs(i,p){if(seen.has(i))throw Error("not forest");seen.add(i);for(let [j,e] of adj[i])if(j!==p){parent.set(j,[i,e]);dfs(j,i)}order.push(i)}for(let i=0;i<fs.length;i++)if(!seen.has(i)){roots.push(i);dfs(i,-1)}
 return {ex,query(pins=[],q=0n){stat.queries++;let vals=new Map(),total=1n,entries=0;
 const pin=(j)=>pins.filter(([x])=>(x&blocks[j])===x);
 for(let i of order){let m=ex[i].out.map(t=>{let v=t.c;for(let j of priv[i])v*=chr([...t.m[ix(i,j)],...pin(j)],blocks[j],(t.q^q)&blocks[j],n);return v});
 for(let [j,e] of adj[i])if(parent.get(j)?.[0]===i){let child=ex[j].out,cv=vals.get(j);
 m=m.map((v,a)=>{let t=ex[i].out[a],s=0n;for(let b=0;b<child.length;b++){let u=child[b];s+=cv[b]*chr([...t.m[ix(i,e)],...u.m[ix(j,e)],...pin(e)],blocks[e],(t.q^u.q^q)&blocks[e],n);entries++;stat.matEntries++}return v*s})}
 vals.set(i,m)}
 for(let i of roots)total*=vals.get(i).reduce((a,b)=>a+b,0n);
 let scale=1n<<BigInt(ex.reduce((a,b)=>a+b.K,0));ok(total%scale===0n);stat.peakMatrixEntries=Math.max(stat.peakMatrixEntries,entries);return total/scale}}}
const term=(rows,c=1)=>({rows,c}), mul=(a,b)=>a.flatMap(x=>b.map(y=>term([...x.rows,...y.rows],x.c*y.c))), neg=a=>a.map(t=>term(t.rows,-t.c)), one=[term([])];
function evalF(fs,x){return fs.every(f=>f.reduce((s,t)=>s+(t.rows.every(([a,b])=>par(a&x)===b)?t.c:0),0)===1)}
function ref(fs,n){let a=[];for(let i=0;i<2**n;i++){stat.referenceWords++;if(evalF(fs,BigInt(i)))a.push(BigInt(i))}return a}
function closure(C,n,candidates){let z=C.query();if(!z)return {z,forced:[]};let forced=[],changed=true;while(changed){changed=false;for(let a of candidates){if(basis([...forced,[a,0]].map(([x])=>[x,0]),n).size===forced.length)continue;stat.closureScans++;let h=C.query([],a);if(h===z||h===-z){forced.push([a,h===z?0:1]);stat.forced++;changed=true;break}}}return {z,forced}}
function witness(C,fs,n){let pins=[],x=0n;for(let i=0;i<n;i++){let a=bit(i);if(C.query([...pins,[a,0]])>0n)pins.push([a,0]);else{pins.push([a,1]);x|=a}}ok(C.query(pins)===1n);ok(evalF(fs,x));stat.witnesses++;return x}
let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
let small={sat:0,unsat:0}, fano={sat:0,unsat:0}, scaling=[];
function test(n,blocks,edges,fs,bucket){let C=compile(n,blocks,edges,fs), rr=ref(fs,n),a=closure(C,n,Array.from({length:n},(_,i)=>bit(i)));ok(a.z===BigInt(rr.length));for(let [m,b] of a.forced)ok(rr.every(x=>par(m&x)===b));if(a.z){bucket.sat++;witness(C,fs,n)}else bucket.unsat++;
 for(let k=0;k<3;k++){let q=BigInt(rnd(2**n));ok(C.query([],q)===rr.reduce((s,x)=>s+(par(q&x)?-1n:1n),0n))}}
for(let t=0;t<48;t++){let n=6,blocks=[mask(2),mask(2,2),mask(2,4)],edges=[[0,1],[1,2],[1]],fs=[];
 for(let i=0;i<3;i++){let scope=blocks.reduce((s,b,j)=>edges[j].includes(i)?s|b:s,0n), rows=[];for(let j=0;j<1+rnd(4);j++)rows.push([BigInt(rnd(64))&scope,rnd(2)]);fs.push([...one,term(rows,-1)])}
 test(n,blocks,edges,fs,small)}
const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const fclauses=triples.flatMap(a=>[0,1].map(b=>a.map(i=>[bit(i),b])));
for(let omit=-1;omit<14;omit++){let f=one;for(let i=0;i<14;i++)if(i!==omit)f=mul(f,[...one,term(fclauses[i],-1)]); // explicitly acquire expansion, small control only
 test(7,[mask(7)],[[0]],[f],fano)}
for(let [r,m] of [[4,3],[8,4],[16,6],[32,8]])for(let label of [0,1]){let n=r*m,blocks=Array.from({length:m},(_,i)=>mask(r,i*r)),edges=blocks.map((_,i)=>[i,i+1]);let P=blocks.map((b,i)=>{let a=[[bit(i*r),0],[bit(i*r+1),0]],c=Array.from({length:r-3},(_,k)=>[bit(i*r+2+k),0]);return [term(a),term(c),term([...a,...c],-1)]});
 let fs=[P[0]], forms=[];for(let i=1;i<m;i++){let a=P[i-1],b=P[i],h=bit(i*r-1)^bit((i+1)*r-1);forms.push(h);fs.push(mul([...one,...neg(a),...neg(b),...mul(a,b).map(t=>term(t.rows,2*t.c))],[term([[h,0]])]))}fs.push(label?P[m-1]:[...one,...neg(P[m-1])]);let C=compile(n,blocks,edges,fs),a=closure(C,n,forms);let want=label?2n*( (1n<<BigInt(r-3))+3n )**BigInt(m):0n;ok(a.z===want);if(label){ok(evalF(fs,0n));stat.witnesses++}scaling.push({r,m,n,label,count:String(a.z),maxLabels:Math.max(...C.ex.map(e=>e.out.length)),expanded:C.ex.reduce((s,e)=>s+e.out.length,0),forced:a.forced.length})}
return {seed:20261124,small,fano,scaling,stat};
}
console.log(JSON.stringify(runDP12(),null,2));
