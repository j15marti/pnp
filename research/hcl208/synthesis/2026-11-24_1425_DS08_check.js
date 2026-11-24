"use strict";
function run(){
const log={rank:0,xor:0,closure:0,pins:0,local:0,joins:0,states:0,ref:0,lifts:0};let rng=2081425;const rand=n=>{rng=(Math.imul(rng,1664525)+1013904223)>>>0;return (rng>>>8)%n};
const bit=i=>1n<<BigInt(i),pos=x=>x.toString(2).length-1,b=(w,i)=>(w>>i)&1,vals=m=>[...m.values()],words=(n,p)=>Array.from({length:2**n},(_,i)=>i).filter(p);
function basis(xs){log.rank++;let m=new Map();for(let x of xs)while(x){let k=pos(x);if(!m.has(k)){m.set(k,x);break}x^=m.get(k);log.xor++}return m}
function has(m,x){while(x){let k=pos(x);if(!m.has(k))return false;x^=m.get(k);log.xor++}return true}
function liftLinear(xs,t){let m=new Map();for(let i=0;i<xs.length;i++){let x=xs[i],a=bit(i);while(x){let k=pos(x);if(!m.has(k)){m.set(k,[x,a]);break}let q=m.get(k);x^=q[0];a^=q[1];log.xor++}}let a=0n;while(t){let q=m.get(pos(t));if(!q)return null;t^=q[0];a^=q[1];log.xor++}return a}
function mass(f,w,full=false){let s=0n;for(let j of full?f.c.map((_,i)=>i):f.a)if(b(w,j))s^=f.c[j];return s}
function solve(input,cap=16){let t=input.t,fs=input.f.map(f=>({c:f.c.slice(),d:f.d.slice(),a:f.c.map((_,i)=>i)})),pins=0;
const cols=()=>fs.flatMap(f=>f.a.map(j=>f.c[j]));const no=()=>({sat:false,w:null,p:0,pins});
while(true){log.closure++;let change=false;
// First apply a certified local pin, restart closure after each pin.
for(let f of fs){if(!f.d.length)return no();for(let j of f.a){let v=b(f.d[0],j);if(f.d.every(w=>b(w,j)===v)){if(v)t^=f.c[j];f.a=f.a.filter(k=>k!==j);pins++;log.pins++;change=true;break}}if(change)break}
if(change)continue;
if(!has(basis(cols()),t))return no();
for(let i=0;i<fs.length;i++){let f=fs[i],out=basis(fs.flatMap((g,j)=>i===j?[]:g.a.map(k=>g.c[k]))),old=f.d.length;f.d=f.d.filter(w=>{log.local++;return has(out,t^mass(f,w))});if(!f.d.length)return no();if(f.d.length!==old)change=true}
if(!change)break;
}
if(!fs.length)return {sat:t===0n,w:0,p:1,pins,witness:[]};
let base=liftLinear(cols(),t),idx=0;if(base===null)throw Error("linear");
for(let f of fs){f.o=0n;for(let j of f.a){if(base&bit(idx++))f.o^=f.c[j]}}
function tree(l,r){if(r-l===1)return {l,r,u:vals(basis(fs[l].a.map(j=>fs[l].c[j])))};let m=(l+r)>>1,L=tree(l,m),R=tree(m,r);return {l,r,L,R,u:vals(basis([...L.u,...R.u]))}}
let root=tree(0,fs.length),width=0,credit=0n;
function ann(n,out){n.out=basis(out);n.k=n.u.length+n.out.size-basis([...n.u,...out]).size;width=Math.max(width,n.k);credit+=bit(n.k);if(n.L){ann(n.L,vals(basis([...out,...n.R.u])));ann(n.R,vals(basis([...out,...n.L.u])));credit+=bit(n.L.k+n.R.k)}}ann(root,[]);if(width>cap)return {sat:null,w:width,p:0,pins};
let peak=0;
function dp(n){n.tab=new Map();if(!n.L){let f=fs[n.l];for(let w of f.d){let s=mass(f,w)^f.o;if(has(n.out,s)&&!n.tab.has(s))n.tab.set(s,w)}}else{dp(n.L);dp(n.R);for(let x of n.L.tab.keys())for(let y of n.R.tab.keys()){log.joins++;let z=x^y;if(has(n.out,z)&&!n.tab.has(z))n.tab.set(z,[x,y])}}if(BigInt(n.tab.size)>bit(n.k))throw Error("width");peak=Math.max(peak,n.tab.size);log.states+=n.tab.size}dp(root);
let r={sat:root.tab.has(0n),w:width,p:peak,pins,credit:String(credit)};if(!r.sat)return r;let witness=[];function back(n,s){let x=n.tab.get(s);if(n.L){back(n.L,x[0]);back(n.R,x[1])}else witness[n.l]=x}back(root,0n);let v=0n;for(let i=0;i<fs.length;i++){if(!input.f[i].d.includes(witness[i]))throw Error("domain lift");v^=mass(fs[i],witness[i],true)}if(v!==input.t)throw Error("syndrome lift");log.lifts++;return {...r,witness}}
function model(desc){let occ=new Map(),f=desc.map(d=>({c:d.k.map(()=>0n),d:d.d}));desc.forEach((d,i)=>d.k.forEach((k,j)=>{if(!occ.has(k))occ.set(k,[]);occ.get(k).push([i,j])}));let rows=0;for(let a of occ.values())for(let q=1;q<a.length;q++){let [i,j]=a[q-1],[u,v]=a[q],x=bit(rows++);f[i].c[j]^=x;f[u].c[v]^=x}return {f,t:0n,rows,desc}}
function cnf(F){return model(F.map(c=>({k:c.map(l=>"x"+Math.abs(l)),d:words(c.length,w=>c.some((l,j)=>b(w,j)===(l>0?1:0)))})))}
function graph(F){let desc=[],arcs=[];F.forEach((c,i)=>{if(!c.length){desc.push({k:["cs","ct"],d:[]});arcs.push(["s","t",0]);return}c.forEach((l,j)=>{let u=j===0?"s":i+"_"+j,v=j===c.length-1?"t":i+"_"+(j+1);desc.push({k:["x"+Math.abs(l),"c"+u,"c"+v],d:words(3,w=>(u!=="s"||b(w,1)===1)&&(v!=="t"||b(w,2)===0)&&(!(b(w,1)&&!b(w,2))||b(w,0)===(l>0?1:0)))});arcs.push([u,v,l])})});return {...model(desc),arcs}}
function ref(F){let n=Math.max(0,...F.flat().map(Math.abs));for(let w=0;w<2**n;w++){log.ref++;if(F.every(c=>c.some(l=>b(w,Math.abs(l)-1)===(l>0?1:0))))return true}return false}
function verify(F,m,r){if(!r.sat)return;let x=new Map();m.desc.forEach((d,i)=>d.k.forEach((k,j)=>{if(k[0]==="x")x.set(+k.slice(1),b(r.witness[i],j))}));if(!F.every(c=>c.some(l=>x.get(Math.abs(l))===(l>0?1:0))))throw Error("CNF lift");if(m.arcs){let reach=new Set(["s"]),ch=true;while(ch){ch=false;for(let [u,v,l] of m.arcs)if(reach.has(u)&&!reach.has(v)&&(!l||x.get(Math.abs(l))!==(l>0?1:0))){reach.add(v);ch=true}}if(reach.has("t"))throw Error("graph lift")}}
let groups={},scales=[];
function test(name,F,expected=null,scale=false,doGraph=true){if(expected===null)expected=ref(F);let a=cnf(F),r=solve(a),g=doGraph?graph(F):null,s=g?solve(g):null;if(r.sat!==expected||(s&&s.sat!==expected))throw Error("decision "+name+" "+JSON.stringify({F,r,s,expected}));verify(F,a,r);if(s)verify(F,g,s);let v=groups[name]??(groups[name]={sat:0,unsat:0,graph_cases:0,max_direct:0,max_graph:0});v[expected?"sat":"unsat"]++;v.graph_cases+=!!s;v.max_direct=Math.max(v.max_direct,r.w??0);v.max_graph=Math.max(v.max_graph,s?.w??0);if(scale)scales.push({name,sat:expected,clauses:F.length,direct_rows:a.rows,graph_rows:g?.rows??null,direct_width:r.w,graph_width:s?.w??null,direct_peak:r.p,graph_peak:s?.p??null,direct_pins:r.pins,graph_pins:s?.pins??null})}
let cube=Array.from({length:8},(_,w)=>[1,2,3].map((v,j)=>b(w,j)?v:-v));for(let i=0;i<256;i++)test("cube",cube.filter((_,j)=>b(i,j)),null,false,i%8===0||i===255);
let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(x=>-x)]);test("fano",fano);for(let i=0;i<14;i++)test("fano",fano.filter((_,j)=>i!==j));
for(let i=0;i<40;i++){let n=3+rand(4),F=Array.from({length:1+rand(12)},()=>Array.from({length:3},()=> (1+rand(n))*(rand(2)?1:-1)));test("random",F)}
for(let n of [8,16,32,64])for(let bad of [false,true]){let F=[];for(let i=1;i<=n;i++){let j=i===n?1:i+1,neq=bad&&i===n;F.push(neq?[i,j]:[-i,j],neq?[-i,-j]:[i,-j])}test("cycle_"+n,F,!bad,true,n<=16)}
let affine={sat:0,unsat:0,max_width:0};for(let i=0;i<80;i++){let k=2+rand(3),f=Array.from({length:k},()=>{let n=1+rand(3);return {c:Array.from({length:n},()=>BigInt(rand(8))),d:words(n,()=>rand(4)!==0)}}),t=BigInt(rand(8)),e=false;function brute(j,s){if(j===k){log.ref++;if(s===t)e=true;return}for(let w of f[j].d)switch(0){default:{let a=0n;for(let z=0;z<f[j].c.length;z++)if(b(w,z))a^=f[j].c[z];brute(j+1,s^a)}}}brute(0,0n);let r=solve({f,t});if(r.sat!==e)throw Error("affine");affine[e?"sat":"unsat"]++;affine.max_width=Math.max(affine.max_width,r.w??0)}
return {seed:2081425,groups,affine,scales,log}
}
console.log(JSON.stringify(run(),null,2));
