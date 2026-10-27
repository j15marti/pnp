'use strict';
// ARC206 restricted sequential-input control. Host JS indices instrument physical head positions.
// All model decisions are based only on scanned symbols and fixed-control phases.
const assert = require('assert');
let checks = 0;
function must(v, why) { checks++; assert.ok(v, why); }
function disj(a,b) {return !a.some((v,i)=>v && b[i]);}
function encode(a,b){const m=a.length;return '^'+a.join('')+'#'+'X'.repeat(8*m)+'#'+b.join('')+'$';}
function unary(a,b){
 const src=encode(a,b); const m=a.length;
 let ip=1,wp=0,maxwp=0,moves=0,reversals=0,lastDir=0,accept=true,queries=0;
 const move=(dir)=>{ip+=dir; moves++; if(lastDir && lastDir!==dir)reversals++;lastDir=dir;must(ip>=0 && ip<src.length,'input head off tape');};
 const seekBob=()=>{let delim=0;while(delim<2){if(src[ip]==='#')delim++;move(1);} };
 const backAlice=()=>{while(src[ip-1]!=='^') move(-1);};
 const readIndexed=()=>{
   const start=ip;
   while(wp>0 && (src[ip]==='0'||src[ip]==='1')) {wp--;move(1);}
   if(!(src[ip]==='0'||src[ip]==='1')) {
      while(ip>start){move(-1);wp++;}
      return {overflow:true};
   }
   const bit=Number(src[ip]);queries++;
   while(ip>start){move(-1);wp++;}
   return {overflow:false,bit};
 };
 let safe=0;
 while(++safe<=m+1){
   const A=readIndexed();
   if(A.overflow) break;
   seekBob();
   const B=readIndexed();
   if(!B.overflow && A.bit && B.bit) {accept=false;break;}
   backAlice();
   wp++; if(wp>maxwp)maxwp=wp;
 }
 must(safe<=m+1,'unary terminated');
 return {accept,D:0,S:maxwp+1,T:moves+queries,move:moves,R:reversals,queries,length:src.length};
}
function buffered(a,b){
 const src=encode(a,b);const m=a.length;let mem=Array(m).fill('_');
 let ip=1,wp=0,T=0,D=0,maxwp=0;
 for(let i=0;i<m;i++){
   const bit=src[ip];must(bit==='0'||bit==='1','buffer source bits');
   if(mem[wp]!==bit){mem[wp]=bit;D++;} T++;
   if(i<m-1){wp++;maxwp=Math.max(maxwp,wp);}ip++;T++;
 }
 while(wp>0){wp--;T++;}
 while(src[ip]!=='#'){ip++;T++;}ip++;T++;
 while(src[ip]!=='#'){ip++;T++;}ip++;T++;
 let accept=true;
 for(let i=0;i<m;i++){
   must(src[ip]==='0'||src[ip]==='1','Bob source bits');
   if(mem[wp]==='1' && src[ip]==='1'){accept=false;break;}
   ip++;wp++;maxwp=Math.max(maxwp,wp);T+=2;
 }
 return {accept,D,S:maxwp+1,T,length:src.length};
}
function run(){let unaryRuns=0,bufferRuns=0,crosses=0,headcase=0;
 let maxSlowRatio=0,maxFastRatio=0;
 for(let m=1;m<=6;m++)for(let aa=0;aa<(1<<m);aa++)for(let bb=0;bb<(1<<m);bb++){
   const a=Array.from({length:m},(_,i)=>(aa>>i)&1),b=Array.from({length:m},(_,i)=>(bb>>i)&1),truth=disj(a,b);
   const u=unary(a,b),f=buffered(a,b);
   must(u.accept===truth,'zero-write comparator soundness');
   must(f.accept===truth,'buffer comparator soundness');
   must(u.D===0 && u.S<=m+1,'zero-write budget');
   must(f.D<=m && f.S<=m+1,'buffer budget');
   must(u.T<=6*m*u.length,'one-head unary O(mN) control');
   must(f.T<=4*f.length,'full buffer O(N) control');
   maxSlowRatio=Math.max(maxSlowRatio,u.T/(m*u.length));
   maxFastRatio=Math.max(maxFastRatio,f.T/f.length);
   unaryRuns++;bufferRuns++;
 }
 for(let m=1;m<=8;m++) for(let x=0;x<(1<<m);x++)for(let y=0;y<(1<<m);y++){
   if(x===y) continue;
   const ax=Array.from({length:m},(_,i)=>(x>>i)&1),ay=Array.from({length:m},(_,i)=>(y>>i)&1);
   const notx=ax.map(v=>1-v),noty=ay.map(v=>1-v);
   must(!disj(ax,noty) || !disj(ay,notx),'fooling-cross soundness');crosses++;
 }
 for(let m=1;m<=6;m++){
   const all1=Array(m).fill(1),all0=Array(m).fill(0);
   const N=encode(all1,all0).length;
   const twoHeadTransitions=N+2*m;
   must(twoHeadTransitions<=2*N,'two-input-head linearity');headcase++;
 }
 let horizonRows=[];
 for(let k of [1,2,4,8])for(let N of [128,1024,16384,1048576]){
   const threshold=N*N;
   const Smax=k*(threshold+1);
   let ratio=Math.log2(Smax+2)/Math.log2(N);
   must(ratio<=2+Math.log2(3*k)/Math.log2(N),'subquadratic log-S cap');
   horizonRows.push({k,N,logS_over_logN:Number(ratio.toFixed(6))});
 }
 return {status:'PASS',assertions:checks,unaryRuns,bufferRuns,crossedPairs:crosses,twoInputControls:headcase,
   maxSlowRatio,maxFastRatio,horizonRows,
   statement:'Finite model controls and elementary inequalities only. This does not prove the asymptotic event-code injection or simulate exact22 clause records.',
   models:'One sequential input head plus one blank read-write work tape; two-input-head control is deliberately outside theorem.'};
}
const raw=run();console.log(JSON.stringify(raw,null,2));
