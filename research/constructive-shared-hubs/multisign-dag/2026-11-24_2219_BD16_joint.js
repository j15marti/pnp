"use strict";
function run(){
 let operations=0,assertions=0,rounds=0,insertions=0;
 const check=b=>{assertions++;if(!b)throw Error("assertion "+assertions)};
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const parts=[];parts.push(Array.from({length:3},(_,i)=>[0,1,2].map(j=>3*i+j)));parts.push(Array.from({length:3},(_,j)=>[0,1,2].map(i=>3*i+j)));for(let a=1;a<=2;a++)parts.push(Array.from({length:3},(_,b)=>[0,1,2].map(i=>3*i+(a*i+b)%3)));
 const plane=parts.flat(),mono=m=>1n<<BigInt(m),x=i=>mono(1<<i),pc=m=>m.toString(2).replace(/0/g,"").length;
 function terms(p){let a=[];while(p){let l=p&-p;a.push(l.toString(2).length-1);p^=l}return a}
 function timesX(p,i){operations++;let r=0n;for(let m of terms(p))r^=mono(m|(1<<i));return r}
 function v(e){let [a,b,c]=e;return 1n^x(a)^x(b)^x(c)^mono((1<<a)|(1<<b))^mono((1<<a)|(1<<c))^mono((1<<b)|(1<<c))}
 function basis(){let b=new Map();return {b,add(p){while(p){let k=p.toString(2).length-1;if(!b.has(k)){b.set(k,p);insertions++;return true}p^=b.get(k)}return false},has(p){while(p){let k=p.toString(2).length-1;if(!b.has(k))return false;p^=b.get(k)}return true}}}
 // Full degree-d polynomial calculus closure: for each variable, take the
 // intersection of its multiplication image with the low-degree subspace.
 function satSpan(n,P,d){
  let high=0n;for(let m=0;m<1<<n;m++)if(pc(m)>d)high|=mono(m);
  let S=basis();for(let p of P){check(!(p&high));S.add(p)}let change;
  do{change=false;rounds++;for(let i=0;i<n;i++){
   let H=new Map(),rows=[...S.b.values()];
   for(let p of rows){let z=timesX(p,i);while(z&high){let k=(z&high).toString(2).length-1;if(!H.has(k)){H.set(k,z);break}z^=H.get(k)}
    if(!(z&high))change=S.add(z)||change;
   }
   if(S.has(1n))return true;
  }}while(change);return S.has(1n)
 }
 function models(n,E,pin){return Array.from({length:1<<n},(_,i)=>i).filter(w=>(pin===null||(w&1)===pin)&&E.every(e=>{let k=e.reduce((s,i)=>s+((w>>i)&1),0);return k===1||k===2})).length}
 const rows=[];for(const [name,n,E] of [["Fano",7,fano],["plane",9,plane]])for(let pin of [null,0,1]){
  let P=E.map(v);if(pin!==null)P.push(x(0)^BigInt(pin));
  let d2=satSpan(n,P,2),d3=satSpan(n,P,3);check(!d2&&d3);check(models(n,E,pin)===0);
  let sides=[];if(name==="plane")for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
   let Q=[...parts[i],...parts[j]],R=Q.map(v);if(pin!==null)R.push(x(0)^BigInt(pin));
   let count=models(n,Q,pin),r=satSpan(n,R,3);check(count===(pin===null?102:51)&&!r);sides.push({i,j,count,degree3Refutes:r});
  }
  rows.push({name,pin,degree2Refutes:d2,degree3Refutes:d3,sides});
 }
 return {assertions,operations,rounds,insertions,rows};
}
console.log(JSON.stringify(run(),null,2));
