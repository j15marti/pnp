// LSPV-4 STRICT22-CUBE-SPECTRUM239 independent GitHub spotcheck
// Execute: node LSPV4_STRICT22_CUBE_SPECTRUM239_check.js
"use strict";
function ring(r) {
 const out=[];
 for(let i=0;i<r;i++){
  const a=i+1,u=r+i+1,v=2*r+i+1,un=r+((i+1)%r)+1;
  out.push([a,u,v],[a,un,v],[-a,-u,-v],[-a,-un,-v]);
 }
 return out;
}
function litTrue(l,mask){return !!(mask & (1<<(Math.abs(l)-1))) === (l>0)}
function resolutions(C,n){
 const p=Array.from({length:n+1},()=>[]),q=Array.from({length:n+1},()=>[]);
 C.forEach((cl,j)=>cl.forEach(l=>(l>0?p:q)[Math.abs(l)].push(j)));
 const non=[];let raw=0,taut=0;
 for(let v=1;v<=n;v++)for(const j of p[v])for(const k of q[v]){
  raw++;
  const r=[...new Set([...C[j],...C[k]].filter(l=>Math.abs(l)!==v))];
  if(r.some(l=>r.includes(-l))){taut++;continue}
  non.push({v,j,k,r:r.sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)});
 }
 return {raw,taut,non};
}
function tr(r){
 let a=2,b=3;
 for(let j=2;j<=r;j++){const z=3*b+2*a;a=b;b=z}
 return b+1;
}
function up(C,initial){
 const a=[...initial];
 for(let t=0;t<=a.length;t++){
  let moved=false;
  for(const c of C){
   let sat=false,unknown=0,last=0;
   for(const l of c){const v=a[Math.abs(l)-1];
     if(v===-1){unknown++;last=l}
     else if(v===(l>0?1:0)){sat=true;break}
   }
   if(sat)continue;
   if(unknown===0)return null;
   if(unknown===1){const j=Math.abs(last)-1,val=last>0?1:0;
     if(a[j]!==-1 && a[j]!==val)return null;
     if(a[j]===-1){a[j]=val;moved=true}
   }
  }
  if(!moved)return a;
 }
 throw Error("UP cycles");
}
function assert(cond,msg){if(!cond)throw Error(msg)}
function main(){
 let whole=0,partial=0;const rows=[];
 for(let r=3;r<=5;r++){
  const n=3*r,C=ring(r),R=resolutions(C,n),distinct=new Set(R.non.map(x=>x.r.join(',')));
  assert(C.length===4*r && R.raw===12*r && R.taut===10*r && R.non.length===2*r,"pair geometry "+r);
  assert(distinct.size===2*r && R.non.every(z=>z.r.length===4),"distinct length4 "+r);
  for(let i=1;i<=n;i++){let pos=0,neg=0;for(const c of C)for(const l of c)if(Math.abs(l)===i){if(l>0)pos++;else neg++}assert(pos===2&&neg===2,"signed degrees")}
  const Q=Array(C.length).fill(0);let sat=0,union=0;
  for(let mask=0;mask<(1<<n);mask++){
   let falseCount=0,last=-1,N=[0,0,0,0];
   for(let j=0;j<C.length;j++){
    const h=C[j].filter(l=>litTrue(l,mask)).length;N[h]++;
    if(h===0){falseCount++;last=j}
   }
   if(falseCount===0)sat++;
   if(falseCount===1)Q[last]++;
   const E=N[0]+N[3],D=N[3]-N[0];
   assert(N[2]-N[1]===-3*D && E>=Math.abs(D) && E+3*Math.abs(D)<=C.length,"balance");
   const comp=((1<<n)-1)^mask;
   for(let h=0;h<4;h++){
    let v=0;for(const c of C)if(c.filter(l=>litTrue(l,comp)).length===h)v++;
    assert(v===N[3-h],"complement");
   }
   if(R.non.some(z=>z.r.every(l=>!litTrue(l,mask))))union++;
  }
  assert(sat===5**r+1,"SAT transfer");
  assert(Q.every(v=>v===(5**(r-1)-1)/2),"equity transfer");
  assert(union===(4**r-tr(r))*(2**r),"cube spectral");
  whole+=1<<n;
  if(r===3){
    const D=R.non.map(z=>z.r);
    const total=3**n;
    for(let code=0;code<total;code++){
      let u=code,a=[];
      for(let j=0;j<n;j++){a.push(u%3-1);u=Math.floor(u/3)}
      const x=up(C,a),y=up([...C,...D],a);
      assert(JSON.stringify(x)===JSON.stringify(y),"UP fixed point "+code);
    }
    partial+=total;
  }
  rows.push({r,n,m:C.length,sat,Q:Q[0],raw:R.raw,non:R.non.length,union_num:4**r-tr(r),union_den:4**r});
 }
 return {status:"passed",whole_assignments:whole,partial_up:partial,rows};
}
const results=main();
if(typeof console!=="undefined")console.log(JSON.stringify(results));
return results;