// I18: exact cardinality-filtered Walsh contraction; small GF(2) masks, BigInt counts.
// node 2026-11-24_1820_I18_check.js
function main(){
let seed=18201124, checks=0, calls=0, joins=0, butterflies=0, quotients=0, peak=0, maxWidth=0, pinsFound=0;
const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const ok=(v)=>{checks++;if(!v)throw Error("assert "+checks)};
const basis=vs=>{let b=[];for(let x of vs){for(const y of b)x=Math.min(x,x^y);if(x){b.push(x);b.sort((a,b)=>b-a)}}return b};
const rem=(x,b)=>{for(const y of b)x=Math.min(x,x^y);return x};
const words=b=>{let a=[0];for(const x of b)a=a.concat(a.map(y=>y^x));return a};
function inter(a,b){ // track A-side combination through Gaussian elimination of A+B
 let piv=[];let out=[];
 for(const [x0,p0] of [...a.map(x=>[x,x]),...b.map(x=>[x,0])]){
 let x=x0,p=p0;for(const [v,q] of piv)if((x^v)<x){x^=v;p^=q}
 if(x){piv.push([x,p]);piv.sort((a,b)=>b[0]-a[0])}else out.push(p);
 }return basis(out)
}
function compatiblePairs(a,b,c){ // basis of (u,v) with u+v in c, using packed disjoint masks in BigInt
 let piv=[],out=[];for(const [x0,p0,q0] of [...a.map(x=>[x,x,0]),...b.map(x=>[x,0,x]),...c.map(x=>[x,0,0])]){
 let x=x0,p=p0,q=q0;for(const [v,r,s] of piv)if((x^v)<x){x^=v;p^=r;q^=s}
 if(x){piv.push([x,p,q]);piv.sort((a,b)=>b[0]-a[0])}else out.push([p,q]);
 }let w=[[0,0]];for(const [p,q] of out)w=w.concat(w.map(([u,v])=>[u^p,v^q]));return w
}
function fw(a){for(let h=1;h<a.length;h*=2)for(let i=0;i<a.length;i+=2*h)for(let j=i;j<i+h;j++){let u=a[j],v=a[j+h];a[j]=u+v;a[j+h]=u-v;butterflies++}return a}
function solve(n,E,target,fix={},phase=0){
 calls++;const m=E.length,B=1n<<BigInt(m+2),power=Array.from({length:m+1},(_,i)=>B**BigInt(i)),all=(1<<n)-1;
 if(n%2)return 0n;
 let a=E.map(([u,v,g])=>(1<<u)^(1<<v)^(g<<n)),goal=all^(target<<n);
 // one reference linear subset, not assumed a matching, via tracked elimination
 let p=[];for(let i=0;i<m;i++){let x=a[i],s=1<<i;for(const [v,t] of p)if((x^v)<x){x^=v;s^=t}if(x){p.push([x,s]);p.sort((a,b)=>b[0]-a[0])}}
 let ref=0,r=goal;for(const [v,t] of p)if((r^v)<r){r^=v;ref^=t}if(r)return 0n;
 function rec(lo,hi){
  let u=basis(a.slice(lo,hi)),v=basis(a.slice(0,lo).concat(a.slice(hi))),W=inter(u,v);maxWidth=Math.max(maxWidth,W.length);
  if(hi-lo===1){let F=new Map();for(let x=0;x<2;x++){if(fix[lo]!==undefined&&fix[lo]!==x)continue;
   let k=(x^((ref>>lo)&1))?a[lo]:0;if(rem(k,W))continue;
   F.set(k,(F.get(k)||0n)+(x&&((phase>>lo)&1)?-1n:1n)*power[x]);
  }peak=Math.max(peak,F.size);return [W,F]}
  let mid=(lo+hi)>>1,[A,f]=rec(lo,mid),[C,g]=rec(mid,hi),D=inter(inter(A,C),W),dw=words(D);
  let Aq=basis(A.map(x=>rem(x,D))),Cq=basis(C.map(x=>rem(x,D))),Wq=basis(W.map(x=>rem(x,D)));
  let F=new Map();joins++;
  for(const [x,y] of compatiblePairs(Aq,Cq,Wq)){quotients++;
   let p=fw(dw.map(z=>f.get(x^z)||0n)),q=fw(dw.map(z=>g.get(y^z)||0n));
   let h=fw(p.map((v,i)=>v*q[i]));for(let i=0;i<h.length;i++){ok(h[i]%BigInt(dw.length)===0n);let k=x^y^dw[i],v=h[i]/BigInt(dw.length);if(v)F.set(k,(F.get(k)||0n)+v)}
  }peak=Math.max(peak,F.size);return [W,F]
 }
 let value=m?rec(0,m)[1].get(0)||0n:goal===0?1n:0n;
 // balanced base-B digits permit signed characters without borrowing ambiguity
 for(let i=0;i<=n/2;i++){let digit=((value%B)+B)%B;if(digit>B/2n)digit-=B;if(i===n/2)return digit;value=(value-digit)/B}
}
function oracle(n,E,t,fix={},phase=0){
 let m=E.length,total=0n,sol=[];
 for(let s=0;s<(1<<m);s++){
 let deg=Array(n).fill(0),g=0,sign=1,good=true;
 for(let i=0;i<m;i++){let x=(s>>i)&1;if(fix[i]!==undefined&&fix[i]!==x){good=false;break}if(x){let [u,v,k]=E[i];deg[u]++;deg[v]++;g^=k;if((phase>>i)&1)sign=-sign}}
 if(good&&g===t&&deg.every(x=>x===1)){total+=BigInt(sign);sol.push(s)}
 }return [total,sol]
}
let sat=0,unsat=0,moments=0,lifts=0,controls=[];
function test(n,E,t,label){
 // Cheap untagged coordinate closure on the same tree first; test oracle uses separate degree check.
 let zero=E.map(([u,v])=>[u,v,0]),fix={},base=solve(n,zero,0);
 ok(base===oracle(n,zero,0)[0]);
 if(base){let changed=true;while(changed){changed=false;for(let i=0;i<E.length;i++)if(fix[i]===undefined){
 let M=solve(n,zero,0,fix,1<<i);if(M===base||M===-base){fix[i]=M===base?0:1;changed=true;pinsFound++;break}
 }}}
 let [expected,sol]=oracle(n,E,t),c=solve(n,E,t,fix);ok(c===expected);if(!c){unsat++;return c}
 sat++;let changed=true;
 while(changed){changed=false;for(let i=0;i<E.length;i++)if(fix[i]===undefined){let M=solve(n,E,t,fix,1<<i);ok(M===oracle(n,E,t,{},1<<i)[0]);moments++;if(M===c||M===-c){fix[i]=M===c?0:1;pinsFound++;changed=true;break}}}
 for(let k=0;k<4;k++){let ph=rnd(1<<E.length);ok(solve(n,E,t,fix,ph)===oracle(n,E,t,{},ph)[0]);moments++}
 // witness selection: after each guarded choice rerun coordinate closure before next choice.
 let mass=c;
 while(Object.keys(fix).length<E.length){
  let progress=false;for(let i=0;i<E.length;i++)if(fix[i]===undefined){let M=solve(n,E,t,fix,1<<i);if(M===mass||M===-mass){fix[i]=M===mass?0:1;progress=true;pinsFound++;break}}
  if(progress)continue;
  let i=Array.from({length:E.length},(_,i)=>i).find(i=>fix[i]===undefined);
  let M=solve(n,E,t,fix,1<<i);fix[i]=0;mass=(mass+M)/2n;ok(mass>0n);ok(solve(n,E,t,fix)===mass)
 }
 let word=0;for(let i=0;i<E.length;i++)word|=fix[i]<<i;ok(sol.includes(word));lifts++;return c
}
for(let trial=0;trial<56;trial++){
 let n=2+2*rnd(4),m=1+rnd(Math.min(12,n*(n-1)/2)),E=[];
 for(let j=0;j<m;j++){let u=rnd(n),v=rnd(n-1);if(v>=u)v++;E.push([u,v,rnd(4)])}
 if(trial%2===0)for(let u=0;u<n;u+=2)if(E.length<15)E.push([u,u+1,rnd(4)]);
 test(n,E,rnd(4),"random");
}
// Independent K4 matching, degree-three star obstruction, and parallel-ID common-fiber control
let K=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)K.push([u,v,(u+v)%4]);
for(let t=0;t<4;t++)controls.push(["K4",t,String(test(4,K,t))]);
controls.push(["star",0,String(test(4,[[0,1,0],[0,2,0],[0,3,0]],0))]);
for(let t=0;t<4;t++)controls.push(["parallel",t,String(test(2,[[0,1,0],[0,1,1],[0,1,2],[0,1,3],[0,1,0],[0,1,1]],t))]);
return {seed:18201124,tests:sat+unsat,sat,unsat,moments,lifts,pinsFound,calls,joins,butterflies,quotients,peak,maxWidth,checks,controls};
}
const result=main(); if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2)); result;
