'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
let checks=0;
function yes(b){assert.equal(b,true);checks++;}
function B(t,u,z,x){let C=false;for(let i=0;i<t;i++)C ||= (((z>>i)&1)!==((u>>i)&1));return (C||x)&&(C||!x);}
function bad(t,u,p){for(let z=0;z<(1<<t);z++){if(p.some(([i,v])=>((z>>i)&1)!==v))continue;for(let x=0;x<2;x++)if(B(t,u,z,Boolean(x)))return false;}return true;}
function verify(t,A,v,p=[]){
 if(v[0]==='L')return A.has(v[1])&&bad(t,v[1],p);
 if(v[0]!=='S'||!Number.isInteger(v[1])||v[1]<0||v[1]>=t||p.some(([i])=>i===v[1]))return false;
 return verify(t,A,v[2],[...p,[v[1],0]])&&verify(t,A,v[3],[...p,[v[1],1]]);
}
function tree(t,d=0,u=0){return d===t?['L',u]:['S',d,tree(t,d+1,u),tree(t,d+1,u+(1<<d))];}
function count(v){if(v[0]==='L')return [0,1];let a=count(v[2]),b=count(v[3]);return [a[0]+b[0]+1,a[1]+b[1]];}
const rows=[];
for(let t=1;t<=8;t++){
 const q=1<<t,A=new Set(Array.from({length:q},(_,i)=>i)),v=tree(t);
 yes(verify(t,A,v));
 const [internal,leaves]=count(v);yes(internal===q-1&&leaves===q);
 for(let u=0;u<q;u++){
  const p=Array.from({length:t},(_,i)=>[i,(u>>i)&1]);
  yes(bad(t,u,p));
  for(let i=0;i<t;i++)yes(!bad(t,u,p.filter(([k])=>k!==i)));
  const sub=new Set(A);sub.delete(u);
  yes(!verify(t,sub,v));
  yes(Array.from(sub).every(j=>B(t,j,u,false)));
 }
 rows.push({t,q,internal,leaves,certificate_utf8_bytes:Buffer.byteLength(JSON.stringify(v))});
}
yes(!verify(6,new Set([0]),['L',0]));
const result={status:'COMPUTATIONAL',scope:'restricted cube-leaf UNSAT coverage',checks,failures:0,rows,
 limitation:'Not an unrestricted SAT time or proof-size lower bound'};
const raw=JSON.stringify(result,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],raw);
process.stdout.write(raw);
