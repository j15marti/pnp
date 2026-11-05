#!/usr/bin/env node
'use strict';
// LSPV-2/427: source authenticated guarded 3-CNF relation equivalence controls.
const assert=require('assert');let checks=0;
function check(b,m){assert.ok(b,m);checks++}
function sat(f,a){return f.every(c=>c.some(l=>Boolean(a[Math.abs(l)]||0)===(l>0)))}
function guard(f,n){const z=n+1,h=[];f.forEach(([a,b,c],i)=>{const u=n+i+2;h.push([z,a,u],[-u,b,c])});return [h,z]}
function proj(f,uni,priv){let out=[];for(let bx=0;bx<2**uni.length;bx++){let yes=false;
for(let by=0;by<2**priv.length;by++){const a={};uni.forEach((id,i)=>a[id]=(bx>>i)&1);priv.forEach((id,i)=>a[id]=(by>>i)&1);
if(sat(f,a)){yes=true;break}}out.push(Number(yes))}return out}
function relation(h,n,z,uni,priv,side){let out=[];
for(let bx=0;bx<2**uni.length;bx++){let yes=false;for(let by=0;by<2**priv.length;by++){
const a={[z]:side};uni.forEach((id,i)=>a[id]=(bx>>i)&1);priv.forEach((id,i)=>a[id]=(by>>i)&1);
let works=true;for(let j=0;j<h.length/2;j++){const u=n+j+2;
if(![0,1].some(b=>sat(h.slice(j*2,j*2+2),{...a,[u]:b}))){works=false;break}}
if(works){yes=true;break}}out.push(Number(yes))}return out}
function test(f,n,uni,priv){const [h,z]=guard(f,n);check(h.length===2*f.length);
check(h.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3));
const p0=relation(h,n,z,uni,priv,0),p1=relation(h,n,z,uni,priv,1),original=proj(f,uni,priv);
check(JSON.stringify(p0)===JSON.stringify(original));check(p1.every(x=>x===1));
const witness={[z]:1};for(let i=1;i<=n;i++)witness[i]=0;for(let i=0;i<f.length;i++)witness[n+i+2]=0;
check(sat(h,witness));return {p0,p1,equal:p0.every(Boolean),labelsSame:p0.some(Boolean)}}
const full=[];for(let b=0;b<8;b++)full.push([1,2,3].map((id,i)=>((b>>i)&1)?-id:id));
const hist={true:0,false:0,labels_same_but_relation_diff:0};
for(let mask=0;mask<256;mask++){const f=full.filter((_,i)=>(mask>>i)&1),r=test(f,3,[1],[2,3]);
hist[String(r.equal)]++;if(r.labelsSame&&!r.equal)hist.labels_same_but_relation_diff++}
check(hist.true===225&&hist.false===31&&hist.labels_same_but_relation_diff===30);
const trap=[[1,2,3],[1,-2,3],[1,2,-3],[1,-2,-3]],r=test(trap,3,[1],[2,3]);
check(r.labelsSame&&!r.equal&&r.p0.join()==='0,1');
function tseitin(edges,charges){const inc=Array.from({length:Math.max(...edges.flat())+1},()=>[]);
edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});const f=[];
inc.forEach((ids,v)=>{check(ids.length===3);for(let b=0;b<8;b++){let bits=ids.map((_,i)=>(b>>i)&1);
if((bits.reduce((s,x)=>s+x,0)&1)!==charges[v])f.push(ids.map((id,i)=>bits[i]?-id:id))}});
return f}
const K4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],Cube=[];
for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if(((i^j).toString(2).replace(/0/g,'')).length===1)Cube.push([i,j]);
for(const edges of [K4,Cube])for(const odd of [0,1]){const n=Math.max(...edges.flat())+1;
const charge=Array(n).fill(0);charge[0]=odd;
const f=tseitin(edges,charge);check(f.length===4*n);
const result=test(f,edges.length,[1],Array.from({length:edges.length-1},(_,i)=>i+2));check(result.equal===(odd===0))}
for(const f of [[[1,1,2]],[[0,2,3]],[[1,2,4]]])
check(f.some(c=>c.some(l=>Math.abs(l)<1||Math.abs(l)>3)||new Set(c.map(Math.abs)).size!==3));
console.log(JSON.stringify({status:'PASS',checks,cases:261,hist},null,2));
