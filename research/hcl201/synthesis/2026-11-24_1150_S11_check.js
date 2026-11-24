"use strict";
function run(){
 const stats={random:0,randomSAT:0,randomUNSAT:0,scale:[],cube:[],flowCalls:0,augmentations:0,affineCalls:0,closurePins:0,branches:0,referenceWords:0,witnesses:0,maxCore:0,maxBad:0};
 const ok=(x,m)=>{if(!x)throw Error(m)};
 let seed=11241150;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const bit=i=>1n<<BigInt(i), has=(x,i)=>!!(x&bit(i)), zeros=n=>Array(n).fill(0);
 function add(b,e,x){b[e[0]]-=x;b[e[1]]+=x}
 function flow(n,E,b,pins=[]){
  stats.flowCalls++;let d=b.slice(), adj=Array.from({length:n+2},()=>[]), refs=[],s=n,t=n+1;
  function edge(u,v,c){if(u===v)return null;let a={v,c,init:c},z={v:u,c:0,init:0};a.rev=z;z.rev=a;adj[u].push(a);adj[v].push(z);return a}
  for(let i=0;i<E.length;i++){let e=E[i],p=pins[i];if(p!==undefined){add(d,e,-p);refs.push(null)}else refs.push(edge(e[0],e[1],e[2]??1))}
  if(d.reduce((a,b)=>a+b,0)!==0)return null;
  let need=0;for(let i=0;i<n;i++){if(d[i]<0)edge(s,i,-d[i]);else if(d[i]>0){edge(i,t,d[i]);need+=d[i]}}
  while(need){let par=Array(n+2).fill(null),q=[s];par[s]=true;for(let h=0;h<q.length&&!par[t];h++)for(const a of adj[q[h]])if(a.c>0&&!par[a.v]){par[a.v]=a;q.push(a.v)}
   if(!par[t])return null;let z=need;for(let v=t;v!==s;v=par[v].rev.v)z=Math.min(z,par[v].c);for(let v=t;v!==s;v=par[v].rev.v){let a=par[v];a.c-=z;a.rev.c+=z}need-=z;stats.augmentations++}
  return E.map((e,i)=>pins[i]!==undefined?pins[i]:refs[i]?refs[i].init-refs[i].c:0)
 }
 function chart(m,eq,pins){
  stats.affineCalls++;let rows=eq.map(e=>e.slice());for(let i=0;i<m;i++)if(pins[i]!==undefined)rows.push([bit(i),pins[i]]);
  let piv=[],r=0;for(let j=0;j<m;j++){let k=rows.findIndex((e,i)=>i>=r&&has(e[0],j));if(k<0)continue;[rows[r],rows[k]]=[rows[k],rows[r]];for(let i=0;i<rows.length;i++)if(i!==r&&has(rows[i][0],j)){rows[i][0]^=rows[r][0];rows[i][1]^=rows[r][1]}piv.push(j);r++}
  if(rows.some(e=>e[0]===0n&&e[1]))return null;
  let free=Array.from({length:m},(_,i)=>i).filter(i=>!piv.includes(i)),f=zeros(m).map(()=>0n),a=zeros(m);
  free.forEach((j,i)=>f[j]=bit(i));piv.forEach((j,i)=>{a[j]=rows[i][1];free.forEach((k,h)=>{if(has(rows[i][0],k))f[j]^=bit(h)})});return {a,f,d:free.length}
 }
 function basis(xs){let B=[];for(let x of xs){for(const v of B){if((x^v)<x)x^=v}if(x){B.push(x);B.sort((a,b)=>a>b?-1:1)}}return B}
 function coords(xs){let P=[];xs.forEach((x,i)=>{let c=bit(i);for(const [v,w] of P)if((x^v)<x){x^=v;c^=w}ok(x!==0n,"dependent basis");P.push([x,c]);P.sort((a,b)=>a[0]>b[0]?-1:1)});return x=>{let c=0n;for(const [v,w] of P)if((x^v)<x){x^=v;c^=w}ok(x===0n,"outside basis");return c}}
 function verify(F,x){if(!x||x.length!==F.E.length)return false;let b=zeros(F.n);for(let i=0;i<x.length;i++){if(x[i]!==0&&x[i]!==1)return false;add(b,F.E[i],x[i])}return b.every((v,i)=>v===F.b[i])&&F.eq.every(([mask,t])=>{let z=0;for(let i=0;i<F.m;i++)if(has(mask,i))z^=x[i];return z===t})}
 function solve(F){
  let {n,E,b,m,eq}=F,pins=Array(E.length),ch;
  // Certified untagged flow and affine coordinate closure; repeat after each deduction.
  while(true){
   if(!flow(n,E,b,pins))return {sat:false,stage:"flow"};
   ch=chart(m,eq,pins);if(!ch)return {sat:false,stage:"affine"};
   let change=false;for(let i=0;i<m;i++)if(pins[i]===undefined&&ch.f[i]===0n){pins[i]=ch.a[i];stats.closurePins++;change=true;break}if(change)continue;
   for(let i=0;i<E.length;i++)if(pins[i]===undefined){let p=pins.slice();p[i]=0;let z=flow(n,E,b,p);p[i]=1;let o=flow(n,E,b,p);if(!z||!o){ok(z||o,"both pin values infeasible");pins[i]=z?0:1;stats.closurePins++;change=true;break}}if(!change)break
  }
  let U=[...new Set(ch.f.filter(x=>x!==0n))],col=U.filter((v,i)=>basis(U.filter((_,j)=>j!==i)).length<ch.d),core=U.filter(v=>!col.includes(v)),B=basis(core),p=B.length;B.push(...col);ok(B.length===ch.d,"basis dimension");let coordinate=coords(B),f=ch.f.map(coordinate);
  let groups=col.map((_,j)=>{let v=zeros(n),ix=[];for(let i=0;i<m;i++)if(f[i]===bit(p+j)){ix.push(i);add(v,E[i],ch.a[i]?-1:1)}let neg=v.indexOf(-1),pos=v.indexOf(1),nz=v.filter(x=>x!==0).length;return {v,ix,arc:nz===0?[]:nz===2&&neg>=0&&pos>=0?[neg,pos,1]:null}});
  let bad=groups.map((g,i)=>g.arc===null?i:-1).filter(i=>i>=0);stats.maxCore=Math.max(stats.maxCore,p);stats.maxBad=Math.max(stats.maxBad,bad.length);
  let branchBits=[...Array.from({length:p},(_,i)=>i),...bad.map(i=>p+i)],a=ch.a;ok(branchBits.length<20,"test branch cap");
  for(let w=0;w<2**branchBits.length;w++){stats.branches++;let z=0n;branchBits.forEach((i,j)=>{if((w>>j)&1)z|=bit(i)});let base=a.map((v,i)=>{let u=f[i]&z;while(u){v^=1;u&=u-1n}return v});
   let d=b.slice();for(let i=0;i<m;i++)add(d,E[i],-base[i]);let Q=[],ids=[];
   for(let i=m;i<E.length;i++){if(pins[i]!==undefined)add(d,E[i],-pins[i]);else{ids.push(i);Q.push(E[i])}}
   let active=[];groups.forEach((g,j)=>{if(!bad.includes(j)&&g.arc.length){active.push(j);Q.push(g.arc)}});
   let v=flow(n,Q,d);if(!v)continue;let x=base.concat(Array(E.length-m).fill(0));for(let i=m;i<E.length;i++)if(pins[i]!==undefined)x[i]=pins[i];ids.forEach((i,j)=>x[i]=v[j]);active.forEach((j,k)=>{if(v[ids.length+k])for(const i of groups[j].ix)x[i]^=1});
   ok(verify(F,x),"lift");stats.witnesses++;return {sat:true,p,q:bad.length,d:ch.d,x}
  }
  return {sat:false,p,q:bad.length,d:ch.d}
 }
 function brute(F){for(let w=0;w<2**F.E.length;w++){stats.referenceWords++;let x=F.E.map((_,i)=>(w>>i)&1);if(verify(F,x))return true}return false}
 for(let it=0;it<240;it++){let n=3+rnd(3),m=2+rnd(6),E=Array.from({length:m+2},()=>{let u=rnd(n),v=rnd(n-1);if(v>=u)v++;return [u,v,1]});let x=E.map(()=>rnd(17)%2),b=zeros(n);E.forEach((e,i)=>add(b,e,x[i]));let eq=Array.from({length:1+rnd(5)},()=>{let mask=BigInt(rnd(2**m)),t=0;for(let i=0;i<m;i++)if(has(mask,i))t^=x[i];return [mask,t]});if(it%3===0)eq[0][1]^=1;if(it%7===0){b[0]--;b[1]++}let F={n,m,E,b,eq},s=solve(F),r=brute(F);ok(s.sat===r,"random mismatch");stats.random++;stats[r?"randomSAT":"randomUNSAT"]++}
 // Equal switch pairs on two-edge paths; dense invertible row mixing, unit arcs.
 for(const r of [4,8,16,32,64,128])for(const hostile of [false,true]){
  let E=[],eq=[],b=zeros(r+2);b[0]=-Math.floor(r/2);b[1]=-b[0];for(let i=0;i<r;i++){E.push([0,i+2,1],[i+2,1,1]);eq.push([bit(2*i)|bit(2*i+1),hostile&&i===0?1:0])}for(let i=1;i<r;i++){eq[i][0]^=eq[i-1][0];eq[i][1]^=eq[i-1][1]}
  let start=stats.branches,s=solve({n:r+2,m:E.length,E,b,eq});ok(s.sat===!hostile,"scale");stats.scale.push({r,hostile,sat:s.sat,p:s.p,q:s.q,d:s.d,branchCalls:stats.branches-start})
 }
 // 3SAT compiler: each false occurrence is a unit switch from reservoir to clause.
 // Each clause has two unit slack arcs, demand 2. Equal/complement occurrence equations.
 function compile(clauses){let n=clauses.length+1,E=[],eq=[],first=new Map(),b=zeros(n);b[0]=-2*clauses.length;
  clauses.forEach((c,j)=>{b[j+1]=2;for(let lit of c){let i=E.length,v=Math.abs(lit),sign=lit<0?1:0;E.push([0,j+1,1]);if(first.has(v)){let [k,a]=first.get(v);eq.push([bit(k)|bit(i),a^sign])}else first.set(v,[i,sign])}});let m=E.length;clauses.forEach((_,j)=>E.push([0,j+1,1],[0,j+1,1]));return {n,m,E,b,eq}}
 let clauses=Array.from({length:8},(_,w)=>[1,2,3].map((v,i)=>(w>>i)&1?-v:v));
 for(let i=-1;i<8;i++){let C=clauses.filter((_,j)=>i!==j),F=compile(C),s=solve(F);ok(s.sat===(i>=0),"cube");stats.cube.push({deleted:i,sat:s.sat,p:s.p,q:s.q,d:s.d})}
 // Fractional collapse counterexample: same value on two parallel switches, demand one.
 let h=solve({n:2,m:2,E:[[0,1,1],[0,1,1]],b:[-1,1],eq:[[3n,0]]});ok(!h.sat&&h.q===1,"nonincidence");
 stats.fractionalControl={sat:h.sat,p:h.p,q:h.q};return stats
}
console.log(JSON.stringify(run(),null,2));
