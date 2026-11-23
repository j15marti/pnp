"use strict";
// Standalone Node reproducer. Seed 20261123.
function audit(){
  const perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]],I=perms[0],T=perms[1];
  const compose=(p,q)=>q.map(x=>p[x]), inv=p=>[0,1,2].map(x=>p.indexOf(x)), parity=x=>{let a=0;for(;x;x&=x-1)a^=1;return a};
  const check=(v,msg)=>{if(!v)throw Error(msg)};
  let state=20261123;const rnd=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return (state>>>8)%n};
  function brute(ps,forbid){let r=ps.length, a=[];function dfs(i){if(i===r)return a[0]!==ps[r-1][a[r-1]];for(let c=0;c<3;c++)if(c!==forbid[i]&&(i===0||c!==ps[i-1][a[i-1]])){a[i]=c;if(dfs(i+1))return true}return false}return dfs(0)}
  function transported(ps){let P=I, frames=[];for(const p of ps){frames.push(inv(P));P=compose(p,P)}return [frames,P]}
  function forbidden(ps, f){const [frames,P]=transported(ps);let q=frames[0][f[0]];return f.every((x,i)=>frames[i][x]===q)&&P[q]===q&&((ps.length%2)!==(P.filter((x,i)=>x!==i).length===2?1:0))}
  function rref(rows,d){let A=rows.map(x=>x.slice()),k=0;for(let j=0;j<d;j++){let i=A.findIndex((x,i)=>i>=k&&((x[0]>>j)&1));if(i<0)continue;[A[k],A[i]]=[A[i],A[k]];for(let t=0;t<A.length;t++)if(t!==k&&((A[t][0]>>j)&1)){A[t][0]^=A[k][0];A[t][1]^=A[k][1]}k++}return A.some(x=>x[0]===0&&x[1])?null:A.slice(0,k)}
  // Each spoke is [linear mask, affine constant, color at bit 0, color at bit 1].
  function project(ps,sp,d){const [frames,P]=transported(ps),c=sp.map((x,i)=>[frames[i][x[2]],frames[i][x[3]]]);const qs=[0,1,2].filter(q=>P[q]===q&&((ps.length%2)!==(P.filter((x,i)=>x!==i).length===2?1:0))&&c.every(x=>x.includes(q)));
    if(!qs.length)return null;
    let rows;
    if(qs.length===1)rows=sp.map((x,i)=>[x[0],x[1]^c[i].indexOf(qs[0])]);
    else rows=sp.slice(1).map((x,j)=>[x[0]^sp[0][0],x[1]^sp[0][1]^c[j+1].indexOf(qs[0])^c[0].indexOf(qs[0])]);
    return rref(rows,d)
  }
  const evalRows=(rows,u)=>rows!==null&&rows.every(([a,b])=>parity(a&u)===b);
  let stats={raw:{tests:0,unsat:0,byParityType:{}},affine:{instances:0,tests:0,ranks:{},byParityRank:{},empty:0,universal:0},cnf:{subformulas:0,rootsSAT:0,rootsUNSAT:0,assignments:0,deletionNeighbors:0},closure:{tests:0,rankOneDeductions:0,contradictions:0}};
  // Exhaust all forbidden color vectors for each net permutation, both length parities.
  for(let r=3;r<=7;r++)for(const h of perms){let ps=Array.from({length:r},()=>perms[rnd(6)]);let p=I;for(let i=0;i<r-1;i++)p=compose(ps[i],p);ps[r-1]=compose(h,inv(p));let type=h.filter((x,i)=>x!==i).length,key=`${r%2}:${type}`;stats.raw.byParityType[key]??=[0,0];for(let u=0;u<3**r;u++){let v=u,f=[];for(let j=0;j<r;j++){f.push(v%3);v=Math.floor(v/3)}let b=!brute(ps,f);check(b===forbidden(ps,f),"raw");stats.raw.tests++;stats.raw.unsat+=+b;stats.raw.byParityType[key][0]++;stats.raw.byParityType[key][1]+=+b}}
  for(let t=0;t<1200;t++){let d=1+rnd(7),r=3+rnd(7),ps=Array.from({length:r},()=>perms[rnd(6)]),sp=Array.from({length:r},()=>{let p=perms[rnd(6)];return [rnd(1<<d),rnd(2),p[0],p[1]]});let rows=project(ps,sp,d),key=rows===null?"empty":String(rows.length);stats.affine.ranks[key]=(stats.affine.ranks[key]||0)+1;let pk=`${r%2}:${d%2}:${rows===null?"empty":rows.length%2}`;stats.affine.byParityRank[pk]=(stats.affine.byParityRank[pk]||0)+1;stats.affine.empty+=+(rows===null);stats.affine.universal+=+(rows!==null&&rows.length===0);stats.affine.instances++;
    for(let u=0;u<1<<d;u++){let f=sp.map(x=>x[2+(parity(x[0]&u)^x[1])]);check(!brute(ps,f)===evalRows(rows,u),"affine");stats.affine.tests++}}
  // Three independent Boolean hubs, four-rim twisted cycle, repeated first spoke.
  const wheel=(mask,r=4)=>{let idx=Array.from({length:r},(_,i)=>i%3),ps=Array.from({length:r},()=>I);ps[r-1]=T;let sp=idx.map(i=>[1<<i,(mask>>i)&1,0,1]);return {ps,sp}};
  const ws=Array.from({length:8},(_,i)=>wheel(i));
  const exact=ws.map(({ps,sp},mask)=>Array.from({length:8},(_,u)=>{let f=sp.map(x=>x[2+(parity(x[0]&u)^x[1])]);let ok=brute(ps,f);check(ok===(u!==mask),"3SAT reduction");return ok}));
  for(let subset=0;subset<256;subset++){let a=0,b=0;for(let u=0;u<8;u++){a+=+(ws.every((_,i)=>!(subset>>i&1)||exact[i][u]));b+=+(!(subset>>u&1));stats.cnf.assignments++}check(a===b,"network");stats.cnf.subformulas++;stats.cnf.rootsSAT+=+(a>0);stats.cnf.rootsUNSAT+=+(a===0);if(a===1&&subset.toString(2).replace(/0/g,"").length===7)stats.cnf.deletionNeighbors++}
  // Closure on certified affine obstructions. Add rank-one complement and reproject in a quotient.
  // Use exact small linear solution sets only as an independent test of the substitution/closure implementation.
  function restrict(rows,d){let R=rref(rows,d);if(R===null)return null;let pivot=R.map(([a])=>Math.clz32(a&-a)^31),free=Array.from({length:d},(_,i)=>i).filter(i=>!pivot.includes(i));let forms=Array.from({length:d},()=>[0,0]);free.forEach((j,i)=>forms[j]=[1<<i,0]);R.forEach(([a,b],i)=>{let mask=0;free.forEach((j,k)=>{if(a>>j&1)mask^=1<<k});forms[pivot[i]]=[mask,b]});return [forms,free.length]}
  function pull(mask,b,forms){let a=0;for(let j=0;j<forms.length;j++)if(mask>>j&1){a^=forms[j][0];b^=forms[j][1]}return [a,b]}
  for(let t=0;t<200;t++){let d=4, w=Array.from({length:5},()=>{let r=3+rnd(4),ps=Array.from({length:r},()=>I);ps[r-1]=r%2?I:T;let sp=Array.from({length:r},()=>[1<<rnd(d),rnd(2),0,1]);return {ps,sp}}),base=Array.from({length:rnd(3)},()=>[1<<rnd(d),rnd(2)]),orig=Array.from({length:16},(_,u)=>evalRows(base,u)&&w.every(({ps,sp})=>!evalRows(project(ps,sp,d),u)));
    let dim=d, W=w, rows=base, map=Array.from({length:d},(_,i)=>[1<<i,0]),reject=false;
    while(true){let R=restrict(rows,dim);if(!R){reject=true;break}let [forms,next]=R;map=map.map(([a,b])=>pull(a,b,forms));W=W.map(({ps,sp})=>({ps,sp:sp.map(([a,b,c,e])=>[...pull(a,b,forms),c,e])}));dim=next;rows=[];for(const {ps,sp} of W){let p=project(ps,sp,dim);if(p===null)continue;if(!p.length){reject=true;break}if(p.length===1){rows.push([p[0][0],p[0][1]^1]);stats.closure.rankOneDeductions++}}if(reject||!rows.length)break}
    let out=Array(16).fill(false);if(!reject)for(let u=0;u<1<<dim;u++)if(W.every(({ps,sp})=>!evalRows(project(ps,sp,dim),u))){let x=0;map.forEach(([a,b],j)=>x|=(parity(a&u)^b)<<j);out[x]=true}
    check(orig.every((v,i)=>v===out[i]),"closure");stats.closure.tests++;stats.closure.contradictions+=+reject}
  return stats;
}
console.log(JSON.stringify(audit(),null,2));
