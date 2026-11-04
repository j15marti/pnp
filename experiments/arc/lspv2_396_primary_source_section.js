'use strict';
// Independent direct construction, finite controls. Node.js 18+. No external packages.
function php(h) {
  const x=(i,j)=>i*h+j+1, rows=[];
  for(let i=0;i<=h;i++) rows.push(Array.from({length:h},(_,j)=>x(i,j)));
  for(let j=0;j<h;j++) for(let i=0;i<=h;i++) for(let k=i+1;k<=h;k++) rows.push([-x(i,j),-x(k,j)]);
  return rows;
}
function bank(h) {
  const n=h*(h+1),u=n+1,out=[];
  for(let i=1;i<=n;i++) { const y=u+i; out.push([-y,u],[-y,i],[y,-u,-i]); }
  return out;
}
function check(cnf,asgn) {return cnf.every(C=>C.some(l=>Boolean(asgn[Math.abs(l)])===(l>0)));}
function section(cnf,a) {return cnf.map(C=>{
  const r=[];
  for(let l of C) {const k=Math.abs(l);if(k in a){if(a[k]===(l>0))return null;}else r.push(l);}
  return r;
}).filter(x=>x!==null);}
let trials=0, failureControls=0, output=[];
for (const h of [1,2,3]) {
  const P=php(h),D=bank(h),n=h*(h+1),u=n+1;
  const sec=section(D,Object.fromEntries(Array.from({length:n},(_,i)=>[u+i+1,false])));
  if (sec.length!==n || sec.some(C=>!C.includes(-u))) throw Error('non-subsumed section');
  const count=h<=2?2**u:1024;
  for(let k=0;k<count;k++) {
    const a={};for(let i=1;i<=u;i++) a[i]=Boolean((k>>(i-1))&1);
    const y={};for(let i=1;i<=n;i++) y[u+i]=a[u]&&a[i];
    if(!check(D,{...a,...y}))throw Error('missing extension');trials++;
    for(let i=1;i<=n;i++){
      const corrupted={...y,[u+i]:!y[u+i]};
      if(check(D.slice(3*(i-1),3*i),{...a,...corrupted}))throw Error('nonunique gate');trials++;
    }
  }
  if(h<=2) {
    for(let k=0;k<2**u;k++){
      const a={};for(let i=1;i<=u;i++)a[i]=Boolean((k>>(i-1))&1);
      if(check([...P,[-u]],a))throw Error('false UNSAT');trials++;
    }
    let a={};for(let i=1;i<=u;i++)a[i]=false;
    for(let i=0;i<h;i++)a[i*h+i+1]=true;
    const omit=P.filter((_,j)=>j!==h);
    const y={};for(let i=1;i<=n;i++)y[u+i]=a[u]&&a[i];
    if(!check([...omit,[-u],...D],{...a,...y}))throw Error('lost SAT control');trials++;
  }
  // Every fixed auxiliary section is non-neutral: at u=0 all outputs 0,
  // at u=1 with all x_i=1 all outputs 1.
  const zero=Object.fromEntries(Array.from({length:u+n},(_,i)=>[i+1,false]));
  const one=Object.fromEntries(Array.from({length:u+n},(_,i)=>[i+1,true]));
  if(!check(D,zero)||!check(D,one))throw Error('non-total');trials+=2;
  output.push({holes:h,phpClauses:P.length,bankClauses:D.length,aux:n,subsumedSection:sec.length,assignments:count});
}
let P1=php(1);if(JSON.stringify(P1)!==JSON.stringify([[1],[2],[-1,-2]]))throw Error('h=1 source mismatch');
if(check(bank(1).slice(1),{1:true,2:false,3:false,4:true,5:false})!==true)throw Error('negative control missing');failureControls++;
console.log(JSON.stringify({status:'COMPUTATIONAL',checks:trials,malformedOrCorruptRejections:failureControls,cases:output,logicalMinimumAtH1:2,scope:'h<=2 old assignments exhaustive, h=3 first 1024 deterministic; not a global optimizer or B3 certificate'},null,2));
