'use strict';
// Independent published finite checker for LSPV-2/493. Not a native FLMV or R_mix341 checker.
function verify493(){
 let checks=0; function ok(x,msg){checks++;if(!x)throw Error(msg||'check failed')}
 const cases=[['K4',4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
 ['Prism3',6,[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]]],
 ['Cube',8,Array.from({length:8},(_,v)=>[0,1,2].map(k=>[v,v^(1<<k)])).flat().filter(e=>e[0]<e[1])]];
 const out=[];
 function build(h,edges,odd){
  let inc=Array.from({length:h},()=>[]);
  edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});
  ok(inc.every(v=>v.length===3),'not cubic');
  let cs=[];
  for(let v=0;v<h;v++)for(let z=0;z<8;z++){
   let bits=[z&1,(z>>1)&1,(z>>2)&1];
   if((bits[0]^bits[1]^bits[2])===(odd&&v===0?1:0))continue;
   cs.push(inc[v].map((e,i)=>bits[i]?-(e+1):e+1));
  }
  ok(cs.length===4*h);
  return cs;
 }
 function bads(cs,e){
  let out=[],witnesses=Array(cs.length).fill(false);
  for(let a=0;a<(1<<e);a++){
   let bad=0n;
   cs.forEach((c,j)=>{if(!c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)))bad|=1n<<BigInt(j)});
   out.push(bad);
   if(bad>0n&&(bad&(bad-1n))===0n){
    for(let j=0;j<cs.length;j++)if(bad===(1n<<BigInt(j)))witnesses[j]=true;
   }
  }
  return {out,witnesses};
 }
 function satIds(ids,bads){let m=0n;for(let i of ids)m|=1n<<BigInt(i);return bads.some(b=>(b&m)===0n)}
 function perm(ids,m){return ids.length===m && ids.every(z=>Number.isInteger(z)&&z>=0&&z<m)&&new Set(ids).size===m}
 function bins(ids,m,k){if(ids.length!==m||ids.some(z=>!Number.isInteger(z)||z<0||z>=m))return null;
  for(let lo=0;lo<m;lo+=k){let mask=0n, sz=Math.min(k,m-lo);
   for(let z of ids)if(z>=lo&&z<lo+sz){let t=1n<<BigInt(z-lo);if(mask&t)return false;mask|=t}
   if(mask!==((1n<<BigInt(sz))-1n))return false;
  }return true}
 for(let [name,h,edges] of cases){
  let cs=build(h,edges,true),m=cs.length,{out:b,witnesses:w}=bads(cs,edges.length);
  ok(!b.includes(0n),'odd UNSAT');ok(w.every(Boolean),'every deletion SAT');
  ok(bads(build(h,edges,false),edges.length).out.includes(0n),'even SAT');
  const base=Array.from({length:m},(_,i)=>i); let replacements=0;
  for(let miss=0;miss<m;miss++)for(let dup=0;dup<m;dup++)if(miss!==dup){
   let a=base.slice();a[miss]=dup;ok(!perm(a,m)&&satIds(a,b),'substitution must become SAT');
   ok(bins(a,m,1)===false);replacements++;
  }
  for(let t=0;t<40;t++){
   let a=base.slice();
   if(t%2){a[0]=t%m;a[1]=t%m}
   else a.reverse();
   ok(satIds(a,b)===!perm(a,m));
   for(let size of [1,2,Math.floor(Math.sqrt(m)),m])ok(bins(a,m,size)===perm(a,m));
  }
  let balanced=base.slice();balanced[1]=0;balanced[2]=3;
  ok(balanced.reduce((a,b)=>a+b,0)===base.reduce((a,b)=>a+b,0));
  ok(!perm(balanced,m)&&satIds(balanced,b),'same sum is insufficient');
  ok(bins([-1,...base.slice(1)],m,2)===null);
  ok(bins([m,...base.slice(1)],m,2)===null);
  out.push({name,vertices:h,edges:edges.length,clauses:m,replacements,missing_clause_witnesses:w.filter(Boolean).length});
 }
 return {run:'LSPV-2/493',passed:true,checks,cases:out,native_flmv:false,historical_Rmix341_checker:false,qualification:'Finite restricted model controls; P versus NP OPEN'};
}
const result493=verify493();
if(typeof console!=='undefined')console.log(JSON.stringify(result493));