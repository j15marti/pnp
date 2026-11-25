"use strict";
function main(){
const stats={assertions:0,closureScans:0,forcedBits:0,dpllNodes:0,gadgetWords:0,referenceWords:0,quotientCalls:0};
const ck=(v,s)=>{stats.assertions++;if(!v)throw Error(s)};
const bits=(n,w)=>Array.from({length:n},(_,i)=>(w>>i)&1);
const R=(z,[a,b,c])=>z[a]===z[b]||z[a]===z[c];
const demand=(z,d)=>!d||d.some(v=>z[v]!==z[d[0]]);
const canon=(z)=>z[0]?z.map(x=>1-x):z;
const key=(z)=>canon(z).reduce((s,x,i)=>s+(x<<i),0);
function compile(k,S){
 let n=k,groups=[],D=null;
 const tree=(L,root,C)=>{if(L.length===1){ck(root===undefined||root===L[0],"singleton tree");return L[0]}let a=L[0],b=tree(L.slice(1),undefined,C),r=root===undefined?n++:root;C.push([r,a,b]);return r};
 for(let w=2;w<2**k;w+=2)if(!S.has(w)){
   let C=[],a=[],b=[];bits(k,w).forEach((v,i)=>(v?b:a).push(i));
   let t=a.length===1?a[0]:b.length===1?b[0]:n++;
   tree(a,t,C);tree(b,t,C);groups.push({C,variables:n});ck(C.length===k-2,"orbit gadget size");
 }
 if(!S.has(0)&&S.size){let C=[],a=tree(Array.from({length:k},(_,i)=>i),undefined,C),b=tree(Array.from({length:k},(_,i)=>i),undefined,C);D=[a,b];groups.push({C,D,variables:n})}
 return {n,groups,D,count:groups.reduce((s,g)=>s+g.C.length,0),empty:!S.size}
}
function groupOK(k,z,g){
 let used=[...new Set(g.C.flat().concat(g.D||[]))].filter(v=>v>=k);
 for(let w=0;w<2**used.length;w++){stats.gadgetWords++;let a=z.slice();used.forEach((v,i)=>a[v]=(w>>i)&1);if(g.C.every(e=>R(a,e))&&demand(a,g.D))return true}
 return false
}
function compileOK(k,z,G){return !G.empty&&G.groups.every(g=>groupOK(k,z,g))}
function solve(n,C,D,pins=[]){
 let a=Array(n).fill(-1);for(const [v,b] of pins){if(a[v]>=0&&a[v]!==b)return null;a[v]=b}
 const owners=C.map(e=>({e,kind:0}));if(D)owners.push({e:D,kind:1});
 function go(z){stats.dpllNodes++;let change=true;
  while(change){stats.closureScans++;change=false;
   for(const {e,kind} of owners){let U=[...new Set(e)],sup=U.map(()=>0);for(let w=0;w<2**U.length;w++){let v=bits(U.length,w);if(!v.every((b,i)=>z[U[i]]<0||z[U[i]]===b))continue;let t=e.map(x=>v[U.indexOf(x)]);if(kind?t.every(b=>b===t[0]):t[0]!==t[1]&&t[0]!==t[2])continue;v.forEach((b,i)=>sup[i]|=1<<b)}
    for(let i=0;i<U.length;i++){if(!sup[i])return null;if(z[U[i]]<0&&sup[i]!==3){z[U[i]]=sup[i]===1?0:1;change=true;stats.forcedBits++}}
   }
  }
  if(C.every(e=>e.every(v=>z[v]>=0)&&R(z,e))&&(!D||D.every(v=>z[v]>=0)&&demand(z,D))){return z.map(v=>v<0?0:v)}
  let score=Array(n).fill(0);for(const {e} of owners)for(const v of e)if(z[v]<0)score[v]++;
  let j=score.indexOf(Math.max(...score));if(!score[j])return null;
  for(let b of [0,1]){let t=z.slice();t[j]=b;let u=go(t);if(u)return u}return null;
 }
 return go(a)
}
function acquire(n,C,D,U){
 let S=new Map(),k=U.length;
 // Direct oriented reference queries, exact complement symmetry. Quotient version separately tested.
 for(let w=0;w<2**k;w+=2){let z=bits(k,w),p=U.map((v,i)=>[v,z[i]]);let x=solve(n,C,D,p);if(x){ck(C.every(e=>R(x,e))&&demand(x,D)&&p.every(([v,b])=>x[v]===b),"support witness");S.set(w,x)}}
 return S
}
function quotient(n,C,D,U,z){
 const pairs=D?D.flatMap((a,i)=>D.slice(i+1).map(b=>[a,b])):[[U[0],U[z.indexOf(1)]]];
 if(!D&&z.every(x=>x===0))return true;
 for(const [s,t] of pairs)for(let o=0;o<(D?2:1);o++){
   stats.quotientCalls++;let p=Array.from({length:n},(_,i)=>i);let f=x=>{while(p[x]!==x)x=p[x];return x};let union=(a,b)=>p[f(a)]=f(b);
   U.forEach((v,i)=>union(v,z[i]^o?t:s));let a=f(s),b=f(t);if(a===b)continue;
   let Q=C.map(e=>e.map(f));let x=solve(n,Q,[a,b]);if(x)return true;
 }return false
}
let all=0;
for(let k of [3,4])for(let mask=0;mask<2**(2**(k-1));mask++){let S=new Set();for(let i=0;i<2**(k-1);i++)if((mask>>i)&1)S.add(2*i);let G=compile(k,S);for(let w=0;w<2**k;w++){let z=bits(k,w);ck(compileOK(k,z,G)===S.has(key(z)),"all supports");}all++}
let state=1701;const rand=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n};
let random=0;for(let k of [5,6])for(let j=0;j<30;j++){let S=new Set();for(let i=0;i<2**(k-1);i++)if(rand(997)%2)S.add(i*2);let G=compile(k,S);for(let w=0;w<2**k;w++){let z=bits(k,w);ck(compileOK(k,z,G)===S.has(key(z)),"random support");}random++}
let qtests=0;for(let j=0;j<48;j++){let n=7,U=[0,1,2,3],C=Array.from({length:6},()=>{let a=[];while(a.length<3){let v=rand(n);if(!a.includes(v))a.push(v)}return a}),D=j%3===0?null:j%3===1?[4,5]:[0,4,6];let S=acquire(n,C,D,U);for(let w=0;w<16;w+=2){let z=bits(4,w),yes=false;for(let t=0;t<2**n;t++){stats.referenceWords++;let a=bits(n,t);if(U.every((v,i)=>a[v]===z[i])&&C.every(e=>R(a,e))&&demand(a,D))yes=true}ck(yes===S.has(w)&&yes===quotient(n,C,D,U,z),"quotient support");qtests++}}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function nae(z,e,s=0){let b=e.map((v,i)=>z[v]^((s>>i)&1));return b.some(v=>v!==b[0])}
function repair(E,w,signs=[]){let C=[],bad=[];E.forEach((e,i)=>{let t=e.map((v,j)=>w[v]^(((signs[i]||0)>>j)&1));if(t.every(v=>v===t[0]))bad.push({id:i,e});else{let k=t.findIndex((v,j)=>v!==t[(j+1)%3]&&v!==t[(j+2)%3]);C.push({id:i,e:[e[k],...e.filter((_,j)=>j!==k)]})}});return {C,bad}}
let frows=[];
for(let variant=-1;variant<21;variant++){let sg=Array(7).fill(0);if(variant>=0)sg[Math.floor(variant/3)]=1<<(variant%3);let anchor=null,rep;for(let w=0;w<128;w++){let x=bits(7,w),a=repair(fano,x,sg);if(a.bad.length===1){anchor=x;rep=a;break}}ck(anchor,"anchor");let A=rep.C.slice(2).map(x=>x.e),B=rep.C.slice(0,2).map(x=>x.e),D=rep.bad[0].e;let X=new Set(A.flat().concat(D)),U=[...new Set(B.flat())].filter(v=>X.has(v)).sort((a,b)=>a-b);let S=acquire(7,B,null,U);let G=compile(U.length,new Set(S.keys()));let original=0,combined=0;
 for(let w=0;w<128;w++){stats.referenceWords++;let z=bits(7,w);if(rep.C.every(x=>R(z,x.e))&&demand(z,D))original++;if(A.every(e=>R(z,e))&&demand(z,D)&&compileOK(U.length,U.map(v=>z[v]),G)){combined++;let ww=S.get(key(U.map(v=>z[v])));ck(!!ww,"stored witness");let flip=ww[U[0]]^z[U[0]],lift=z.slice();for(let v of new Set(B.flat()))if(!X.has(v))lift[v]=ww[v]^flip;ck(fano.every((e,i)=>nae(lift.map((v,j)=>v^anchor[j]),e,sg[i])),"source gluing")}}
 ck((original>0)===(combined>0)&&(original===0)===(variant<0),"Fano both label");frows.push({variant,original,combined,k:U.length,support:S.size,added:G.count})}
function ring(q){let L=12*q,E=[],id=(i,j)=>3*((i+L)%L)+(j+3)%3;for(let i=0;i<L;i++)for(let j=0;j<3;j++)E.push([id(i,j),id(i+1,j),id(i+1,j+1)]);for(let b=0;b<q;b++)for(let j=0;j<3;j++){let t=j===2?[[0,2,5],[1,3,10],[4,7,9],[6,8,11]]:[[0,2,5],[1,3,8],[4,7,10],[6,9,11]];if(b===0&&j===0)t=[[0,4,8],[1,3,6],[2,9,11],[5,7,10]];for(let x of t)E.push(x.map(i=>id(12*b+i,j)))}return E}
let q=2,E=ring(q),n=72,w=Array.from({length:n},(_,i)=>Math.floor(i/3)%2),a=repair(E,w);ck(a.bad.length===1,"ring anchor");let B=a.C.filter(({id})=>id<72?id>=36:id>=84).map(x=>x.e),A=a.C.filter(({id})=>id<72?id<36:id<84).map(x=>x.e),D=a.bad[0].e,X=new Set(A.flat().concat(D)),U=[...new Set(B.flat())].filter(v=>X.has(v)).sort((a,b)=>a-b);ck(U.length===6&&B.length===48,"actual seam");let S=acquire(n,B,null,U),G=compile(6,new Set(S.keys()));let Grows=G.groups.flatMap(g=>g.C).map(e=>e.map(v=>v<6?U[v]:n+v-6));let nn=n+G.n-6;let y=solve(nn,A.concat(Grows),D);ck(y,"ring combined witness");let z=U.map(v=>y[v]),ww=S.get(key(z));ck(ww,"ring seam support");let flip=ww[U[0]]^z[0],lift=y.slice(0,n);for(let v of new Set(B.flat()))if(!X.has(v))lift[v]=ww[v]^flip;ck(E.every(e=>nae(lift.map((v,i)=>v^w[i]),e)),"ring source lift");
let parity=new Set([0,6,10,12]),allowed=Array.from({length:4},(_,a)=>Array.from({length:4},(_,b)=>Array.from({length:4},(_,c)=>[a,b,c])).flat()).flat().filter(e=>[...parity].every(w=>R(bits(4,w),e)));ck(allowed.every(([a,b,c])=>a===b||a===c),"no auxiliary-free nontrivial parity owners");
let plane=[];for(let c=0;c<3;c++)plane.push([0,1,2].map(i=>3*i+c));for(let c=0;c<3;c++)plane.push([0,1,2].map(j=>3*c+j));for(let a of [1,2])for(let c=0;c<3;c++)plane.push([0,1,2].map(i=>3*i+(a*i+c)%3));let cnt=0;for(let i=0;i<512;i++){stats.referenceWords++;if(plane.every(e=>nae(bits(9,i),e)))cnt++}ck(cnt===0,"M22 plane UNSAT");
return {stats,allSupports:all,randomSupports:random,quotientChecks:qtests,fano:frows,ring:{q,n,bad:a.bad,U,small:B.length,large:A.length,support:[...S.keys()],added:G.count,sourceWitness:lift.map((v,i)=>v^w[i]).join(""),directReferenceGeneral:false},plane:{models:cnt},parity:{support:[...parity],nontrivialRawOwners:0}}
}
console.log(JSON.stringify(main(),null,2));
