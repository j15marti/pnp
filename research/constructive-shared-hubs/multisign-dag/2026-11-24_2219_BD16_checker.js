"use strict";
function run(){
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const plane=[];for(let i=0;i<3;i++)plane.push([0,1,2].map(j=>3*i+j));for(let j=0;j<3;j++)plane.push([0,1,2].map(i=>3*i+j));for(let a=1;a<=2;a++)for(let b=0;b<3;b++)plane.push([0,1,2].map(i=>3*i+(a*i+b)%3));
 let assertions=0,products=0,scans=0,changes=0,insertions=0; const check=(b)=>{assertions++;if(!b)throw Error("assertion "+assertions)};
 function terms(p){let a=[];while(p){let l=p&-p; a.push(l.toString(2).length-1);p^=l}return a}
 const mono=m=>1n<<BigInt(m), x=i=>mono(1<<i), pc=m=>m.toString(2).replace(/0/g,"").length;
 function mul(p,q){products++;let z=0n;for(let a of terms(p))for(let b of terms(q))z^=mono(a|b);return z}
 function deg(p){return Math.max(0,...terms(p).map(pc))}
 function ev(p,w){let a=0;for(let m of terms(p))if((m&w)===m)a^=1;return a}
 function violation(e,sg=0,budget=-1){let l=e.map((i,j)=>x(i)^BigInt((sg>>j)&1));if(budget===0)return mul(mul(1n^l[0],1n^l[1]),1n^l[2]);if(budget===1)return mul(mul(l[0],l[1]),l[2]);return mul(1n^l[0]^l[1],1n^l[0]^l[2])}
 function basis(){let b=new Map();return {add(p){while(p){let k=p.toString(2).length-1;if(!b.has(k)){b.set(k,p);insertions++;return true}p^=b.get(k)}return false},has(p){while(p){let k=p.toString(2).length-1;if(!b.has(k))return false;p^=b.get(k)}return true}}}
 function macaulay(n,P,d){let b=basis();for(let p of P){for(let m=0;m<1<<n;m++){if(pc(m)+deg(p)>d)continue;b.add(mul(p,mono(m)))}}return b}
 // Exact singleton affine hull closure on small explicit finite controls only.
 // Every owner is tested separately against accumulated necessary affine forms.
 function local(n,P,G){let ws=Array.from({length:1<<n},(_,i)=>i).filter(w=>ev(G,w));let old; do{scans++;old=ws.length;for(let p of P){let keep=ws.filter(w=>!ev(p,w));if(!keep.length)return [];const a=keep[0],b=basis();for(let w of keep)b.add(BigInt(w^a));let next=ws.filter(w=>b.has(BigInt(w^a)));if(next.length<ws.length)changes++;ws=next;}}while(ws.length!==old);return ws}
 let rows=[];
 function job(name,n,E,idx=-1,sign=0,budget=-1){
  const P=E.map((e,i)=>violation(e,i===idx?sign:0,i===idx?budget:-1));let models=Array.from({length:1<<n},(_,i)=>i).filter(w=>P.every(p=>!ev(p,w)));
  const root=local(n,P,1n);check(models.every(w=>root.includes(w)));
  let pins=[];for(let bit of [0,1]){let G=x(0)^BigInt(1^bit),l=local(n,P,G);check(models.filter(w=>ev(G,w)).every(w=>l.includes(w)));pins.push({bit,remaining:l.length})}
  let direct2=macaulay(n,P,2).has(1n),direct3=macaulay(n,P,3).has(1n),direct4=macaulay(n,P,4).has(1n);check(!models.length||!direct2&&!direct3&&!direct4);
  // Same actual variables; nonaffine two-way query q and shared leaves guarded by C_b.
  let q=mul(x(0),x(1)),p0=P[0],C=[mul(1n^q,1n^p0),mul(q,1n^p0)],parents=[1n^x(2),x(2)];
  let edges=0,sourceDependent=0,leafRefute=[];
  let Bproof=macaulay(n,P,6);
  for(let g of parents){
   let localWords=local(n,P,g);check(models.filter(w=>ev(g,w)).every(w=>localWords.includes(w)));
   let e=0n, rhs=0n;
   for(let b=0;b<2;b++){
    let B=mul(g,b?q:1n^q), err=mul(B,1n^C[b]);e^=err;rhs^=mul(B,C[b]);
    check(err===mul(B,p0));check(Bproof.has(err));edges++;
    if(err)sourceDependent++;
    for(let w of models)check(!ev(B,w)||ev(C[b],w));
   }
   check(g===(e^rhs));
  }
  for(let c of C){let l=local(n,P,c);let v=models.filter(w=>ev(c,w));check(v.every(w=>l.includes(w)));let d=macaulay(n,[...P,1n^c],4).has(1n);leafRefute.push(d);check(!v.length||!d)}
  if(leafRefute.every(Boolean))check(models.length===0);
  rows.push({name,n,models:models.length,rootRemaining:root.length,pins,direct2,direct3,direct4,leafRefute,edges,sourceDependent,maxGuardDegree:Math.max(...C.map(deg))});
 }
 job("Fano",7,fano);job("plane",9,plane);
 for(let i=0;i<7;i++)for(let j=0;j<3;j++)job("Fano sign "+i+":"+j,7,fano,i,1<<j);
 for(let i=0;i<7;i++)for(let j=0;j<2;j++)job("Fano budget "+i+":"+j,7,fano,i,0,j);
 check(rows[0].models===0&&rows[1].models===0);check(rows.slice(2,23).every(r=>r.models===10));check(rows.slice(23).every(r=>r.models===5));
 return {assertions,products,scans,changes,insertions,rows};
}
console.log(JSON.stringify(run(),null,2));
