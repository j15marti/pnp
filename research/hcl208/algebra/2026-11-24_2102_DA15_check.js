"use strict";
function main(){
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 const wt=x=>{let p=0;while(x){p++;x&=x-1}return p};
 const reduce=(row,B)=>{let [a,b]=row;for(let i=B.length-1;i>=0;i--)if(B[i]&&(a&(1<<i))){a^=B[i][0];b^=B[i][1]}return [a,b]};
 const add=(row,B)=>{let [a,b]=reduce(row,B);if(!a)return b?-1:0;B[31-Math.clz32(a)]=[a,b];return 1};
 const rank=B=>B.filter(Boolean).length;
 const packet=(e,sign=0)=>{let [a,b,c]=e;return [[(1<<a)^(1<<b),((sign&1)^((sign>>1)&1))],[(1<<a)^(1<<c),((sign&1)^((sign>>2)&1))]]};
 const hit=(P,x)=>P.every(([a,b])=>parity(a&x)===b);
 const assert=(v,msg)=>{if(!v)throw Error(msg);checks++};
 let checks=0,seed=20261124;
 const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
 function close(n,packets,guards){
  let G=Array(n).fill(null),q=0,scans=0,live=[];
  for(const r of guards)if(add(r,G)===-1)return {bad:true,q,scans,G,live};
  while(true){
   scans++;live=[];let change=false;
   for(let i=0;i<packets.length;i++){
    const P=packets[i], B=Array(n).fill(null);
    let inactive=false;
    for(const r of P)if(add(reduce(r,G),B)===-1){inactive=true;break}
    if(inactive)continue;
    const rr=rank(B);
    if(rr===0)return {bad:true,q,scans,G,live:[]};
    if(rr===1){
     const orig=P.find(r=>reduce(r,G)[0]!==0);
     assert(add([orig[0],orig[1]^1],G)===1,"forced row independent");
     q++;change=true;break;
    }
    live.push({i,rows:B.filter(Boolean)});
   }
   if(!change)return {bad:false,q,scans,G,live};
  }
 }
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const masks=P=>P.map(r=>r[0]);
 const plane=P=>{let [a,b]=masks(P);return [a,b,a^b].sort((x,y)=>x-y).join(",")};
 const results={fano:{sources:0,charts:0,actualSATCharts:0,actualUNSATCharts:0,closureTerminals:0,maxForces:0,minMass:999,modelChecks:0},cycles:{sources:0,charts:0,actualSATCharts:0,actualUNSATCharts:0,closureTerminals:0,maxForces:0,maxGuardRank:0,modelChecks:0},closureScans:0};
 function checkChart(n,packets,guards,stats,k,D,single){
  let out=close(n,packets,guards), originalCount=0, reducedCount=0;
  stats.charts++;results.closureScans+=out.scans;
  stats.maxForces=Math.max(stats.maxForces,out.q);
  assert(out.q<=2*k-1,"girth propagation bound");
  if(!out.bad){
   let G=out.G.filter(Boolean);
   let B=0;for(let a=1;a<(1<<n);a++)if(wt(a)<=4&&reduce([a,0],out.G)[0]===0)B|=a;
   assert(wt(B)<=4*rank(out.G),"low weight support bound");
   let mass=2*out.live.length;
   const keys=new Set(out.live.map(p=>plane(p.rows)));
   assert(2*keys.size>=2*Math.max(0,packets.length-4*D*rank(out.G)),"distinct rank bound");
   if(single){
    assert(keys.size===out.live.length,"no identical projected planes");
    assert(mass===2*packets.length || mass===2*packets.length-2,"exact mass");
    stats.minMass=Math.min(stats.minMass,mass);
   }else stats.maxGuardRank=Math.max(stats.maxGuardRank,rank(out.G));
  }else stats.closureTerminals++;
  if(single)assert(!out.bad,"rank-one not locally terminal");
  for(let x=0;x<(1<<n);x++){
   const a=hit(guards,x)&&packets.every(p=>!hit(p,x));
   const b=!out.bad&&hit(out.G.filter(Boolean),x)&&out.live.every(p=>!hit(p.rows,x));
   assert(a===b,"guarded closure equivalence");
   originalCount+=+a;reducedCount+=+b;stats.modelChecks++;
  }
  assert(originalCount===reducedCount,"count");
  if(originalCount)stats.actualSATCharts++;else stats.actualUNSATCharts++;
  return originalCount;
 }
 const sources=[fano.map(e=>packet(e))];
 for(let i=0;i<7;i++)for(let s of [1,2,4])sources.push(fano.map((e,j)=>packet(e,j===i?s:0)));
 for(let i=0;i<sources.length;i++){
  const P=sources[i],st=results.fano;st.sources++;
  let root=close(7,P,[]);results.closureScans+=root.scans;assert(!root.bad&&root.q===0&&root.live.length===7,"root closure");
  let cnt=0;for(let x=0;x<128;x++)cnt+=+P.every(p=>!hit(p,x));
  assert(cnt===(i?10:0),"Fano source count");
  for(let a=1;a<128;a++){let c=0;for(let b=0;b<2;b++)c+=checkChart(7,P,[[a,b]],st,1,3,true);assert(c===cnt,"both children partition");}
 }
 for(let len of [5,6,7]){
  let n=2*len,es=Array.from({length:len},(_,i)=>[i,(i+1)%len,i+len]);
  for(let variant=0;variant<2;variant++){
   const P=es.map(e=>packet(e,variant?rng()%8:0)),st=results.cycles;st.sources++;
   let root=close(n,P,[]);results.closureScans+=root.scans;assert(!root.bad&&root.q===0,"cycle root");
   for(let t=0;t<120;t++){
    let a,b;
    if(t%3===0){a=P[rng()%len][rng()%2][0];b=P[rng()%len][rng()%2][0]}else if(t%3===1){a=P[rng()%len][rng()%2][0];b=(rng()&((1<<n)-1))^a}else{a=rng()&((1<<n)-1);b=rng()&((1<<n)-1)}
    if(!a||!b||a===b){t--;continue}
    const rhs=rng()&3;
    checkChart(n,P,[[a,rhs&1],[b,(rhs>>1)&1]],st,2,2,false);
   }
  }
 }
 return {seed:20261124,...results,assertions:checks};
}
console.log(JSON.stringify(main(),null,2));
