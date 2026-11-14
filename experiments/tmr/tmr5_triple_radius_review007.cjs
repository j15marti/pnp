'use strict';
// TMR-5/007 standalone exact-source companion to independent native Python.
const audit = function audit(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const ones=x=>{let k=0;while(x){k+=x&1;x>>=1}return k};
 const rep=i=>2*i+(ones(i)&1);
 const flip=(s,p)=>s.slice(0,p)+(s[p]==="0"?"1":"0")+s.slice(p+1);
 function make(r,extra){
  const t=3*r,w=Math.ceil(Math.log2(2*t+2)),N=2**w-1;
  const core=Array.from({length:t},(_,j)=>rep(j+1)),coreSet=new Set(core),spare=[];
  for(let i=1;i<=N;i++)if(!coreSet.has(i))spare.push(i);
  const rows=[],obs=[];
  for(let g=0;g<r;g++){for(const mask of [1,2,3,4,5,6,7,extra])rows.push(Array.from({length:3},(_,j)=>[core[3*g+j],(mask>>j)&1]));obs.push(rows.length-1)}
  for(let i=0;i<spare.length;i+=3){
   const ids=spare.slice(i,i+3);
   for(const j of spare){if(ids.length===3)break;if(!ids.includes(j))ids.push(j)}
   assert(ids.length===3,"filler");rows.push(ids.map(j=>[j,0]));
  }
  const M=rows.length;let bits="1".repeat(N)+"0"+"1".repeat(M)+"0";const signs=[],ids=[];
  for(let ci=0;ci<M;ci++)for(let li=0;li<3;li++){
   const [v,s]=rows[ci][li];signs.push([bits.length,ci,li]);bits+=s;
   for(let b=0;b<w;b++)ids.push([bits.length+b,ci,li]);
   bits+=v.toString(2).padStart(w,"0");
  }
  return {r,w,N,M,core,spare,rows,bits,signs,ids,obs};
 }
 function parse(s,d){
  if(s.length!==d.bits.length)return null;
  const h="1".repeat(d.N)+"0"+"1".repeat(d.M)+"0";if(!s.startsWith(h))return null;
  const rows=[],occ=Array(d.N+1).fill(0);let p=h.length;
  for(let i=0;i<d.M;i++){
   let r=[];for(let j=0;j<3;j++){
    const sign=+s[p++],v=parseInt(s.slice(p,p+d.w),2);p+=d.w;
    if(!v||v>d.N||r.some(z=>z[0]===v))return null;
    r.push([v,sign]);occ[v]++;
   }
   rows.push(r);
  }
  if(occ.slice(1).some(x=>!x))return null;
  return rows;
 }
 function localSAT(rows,r){
  for(let g=0;g<r;g++){
   const br=rows.slice(8*g,8*g+8),ids=[...new Set(br.flatMap(a=>a.map(x=>x[0])))];
   if(ids.length>3)return false;
   let found=false;
   for(let bits=0;bits<(1<<ids.length);bits++){
    const a={};ids.forEach((v,j)=>a[v]=(bits>>j)&1);
    if(br.every(cl=>cl.some(([v,s])=>(a[v]^s)===1))){found=true;break}
   }
   if(!found)return false;
  }
  return true;
 }
 const cases=[];
 for(const r of [1,2,3,4,6,8,12]){
  const d=make(r,7);assert(parse(d.bits,d),"source parser");
  const stats={r,L:d.bits.length,N:d.N,M:d.M,sign1:0,sign2:0,id1:0,threeBitUnsat:0,pair008Unsat:0};
  const signs=d.signs.map(x=>x[0]);
  for(const p of signs){const a=parse(flip(d.bits,p),d);assert(a&&localSAT(a,r),"one-sign");stats.sign1++}
  if(r<=4){
   for(let i=0;i<signs.length;i++)for(let j=i+1;j<signs.length;j++){
    const a=parse(flip(flip(d.bits,signs[i]),signs[j]),d);
    assert(a&&localSAT(a,r),"two-sign");
    stats.sign2++;
   }
  }
  const base={};d.core.forEach(v=>base[v]=0);d.spare.forEach(v=>base[v]=1);
  const holds=rows=>rows.every(cl=>cl.some(([v,s])=>((base[v]||0)^s)===1));
  for(const [p,ci,li] of d.ids){
   if(ci>=8*r)continue;
   const a=parse(flip(d.bits,p),d);assert(a,"one ID parser");
   const v=a[ci][li][0],s=a[ci][li][1];assert(d.spare.includes(v),"ID fresh");
   const backup=base[v];base[v]=1-s;assert(holds(a),"one ID SAT witness");base[v]=backup;
   stats.id1++;
  }
  for(let g=0;g<r;g++){
   const s=d.signs.filter(x=>x[1]===d.obs[g]).map(x=>x[0]);
   let x=d.bits;for(const p of s)x=flip(x,p);
   const a=parse(x,d);assert(a&&!localSAT(a,r),"three-bit UNSAT");
   const forbidden=new Set(a.slice(8*g,8*g+8).map(row=>row.reduce((z,[_,s],j)=>z+(s<<j),0)));
   assert(forbidden.size===8,"complete forbidden tuples");stats.threeBitUnsat++;
  }
  const old=make(r,3);assert(parse(old.bits,old),"original source");
  for(const p of old.signs.map(x=>x[0])){const a=parse(flip(old.bits,p),old);assert(a&&localSAT(a,r),"original one-sign")}
  for(let g=0;g<r;g++){
   const s=old.signs.filter(x=>x[1]===old.obs[g]&&x[2]<=1).map(x=>x[0]);
   let x=old.bits;for(const p of s)x=flip(x,p);
   const a=parse(x,old);assert(a&&!localSAT(a,r),"original 2bit UNSAT");stats.pair008Unsat++;
  }
  cases.push(stats);
 }
 const totals={};for(const k of ["sign1","sign2","id1","threeBitUnsat","pair008Unsat"])totals[k]=cases.reduce((a,c)=>a+c[k],0);
 return {tag:"TMR5-TRIPLE-RADIUS-007",language:"javascript",execution:"direct hosted V8 audit function, no wrappers",status:"COMPUTATIONAL",model:"strict proper 3CNF all declared IDs occurring",cases,totals,failures:0};
};
console.log(JSON.stringify(audit(),null,2));
