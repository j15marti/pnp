"use strict";
function main(){
 const L={assertions:0,gaussian:0,xors:0,closureScans:0,forcedEquations:0,peelAttempts:0,exceptionSets:0,featureCandidates:0,featureTests:0,featureXors:0,maxBasis:0,referenceWords:0,verifiedLifts:0};
 const ck=(b,msg)=>{L.assertions++;if(!b)throw Error(msg)};
 const bit=i=>1n<<BigInt(i), parity=a=>{let p=0;while(a){a&=a-1n;p^=1}return p}, dot=(a,b)=>parity(a&b);
 function chart(n,eqs){
  L.gaussian++;let piv=new Map();
  for(let [a,b] of eqs){while(a){let p=a&-a;if(!piv.has(p)){piv.set(p,[a,b]);break}let [c,d]=piv.get(p);a^=c;b^=d;L.xors++}if(a===0n&&b)return null}
  let free=[];for(let i=0;i<n;i++)if(!piv.has(bit(i)))free.push(bit(i));
  let ps=[...piv.keys()].sort((a,b)=>a>b?-1:1);
  function extend(w,hom){for(let p of ps){let [a,b]=piv.get(p);if(dot(a,w)^(hom?0:b))w^=p}return w}
  return {off:extend(0n,false),dirs:free.map(p=>extend(p,true))};
 }
 function transform([a,b],C){let m=0n;C.dirs.forEach((v,i)=>{if(dot(a,v))m|=bit(i)});return [m,b^dot(a,C.off)]}
 function lift(C,w){let x=C.off;C.dirs.forEach((v,i)=>{if(w&bit(i))x^=v});return x}
 function sat(F,w){return F.every(f=>f.some(([a,b])=>dot(a,w)===b))}
 function close(n,F){
  let eqs=[];
  for(;;){
   let C=chart(n,eqs);if(!C)return null;
   let fs=[],changed=false;
   for(let id=0;id<F.length;id++){
    L.closureScans++;let seen=new Map(),taut=false;
    for(let orig of F[id]){
     let [a,b]=transform(orig,C);
     if(a===0n){if(b===0){taut=true;break}continue}
     if(seen.has(a)){if(seen.get(a).b!==b){taut=true;break}}else seen.set(a,{a,b,orig});
    }
    if(taut)continue;let vals=[...seen.values()];
    if(!vals.length)return null;
    if(vals.length===1){eqs.push(vals[0].orig);L.forcedEquations++;changed=true;break}
    fs.push({id,terms:vals.map(t=>[t.a,t.b])});
   }
   if(!changed)return {C,fs};
  }
 }
 function triangular(n,fs){
  let rest=fs.slice(),picks=[],dirs=[];
  while(rest.length){
   let chosen=null;
   for(let i=0;i<rest.length&&!chosen;i++){
    let f=rest[i];if(f.terms.length!==2)continue;
    let eq=rest.flatMap((g,j)=>i===j?[]:g.terms.map(([a])=>[a,0]));
    for(let j=0;j<2;j++){
     L.peelAttempts++;let v=chart(n,eq.concat([[f.terms[j][0],1]]));
     if(v){chosen={i,j,v:v.off};break}
    }
   }
   if(!chosen)return null;
   let {i,j,v}=chosen,f=rest.splice(i,1)[0];
   picks.push([f.terms[j],f.terms[1-j]]);dirs.push(v);
  }
  let free=chart(n,dirs.map(v=>[v,0])).dirs;
  let obs=picks.map(p=>p[0]).concat(free.map(a=>[a,0]));
  ck(obs.length===n,"dual basis length");
  let base=chart(n,obs);ck(base&&base.dirs.length===0,"observation invertible");
  let C={off:base.off,dirs:obs.map((_,i)=>chart(n,obs.map(([a],j)=>[a,+(i===j)])).off)};
  let gates=picks.map((p,i)=>{
   let first=transform(p[0],C);ck(first[0]===bit(i)&&first[1]===0,"first pivot");
   let [a,b]=transform(p[1],C);ck((a&(bit(i)-1n))===0n,"triangular gate");
   return [a&~bit(i),b^+(Boolean(a&bit(i)))];
  });
  while(gates.length<n)gates.push([0n,0]);
  return {C,gates,p:picks.length};
 }
 function mons(n,D){
  let arr=[];function go(i,left,a){arr.push(a);if(left)for(let j=i;j<n;j++)go(j+1,left-1,a|bit(j))}go(0,Math.min(n,D),0n);return arr;
 }
 function feature(w,M){let v=0n;for(let i=0;i<M.length;i++){L.featureTests++;if((w&M[i])===M[i])v|=bit(i)}return v}
 function reduce(words,M){
  let basis=new Map(),keep=[];
  for(let w of words){L.featureCandidates++;let a=feature(w,M);while(a){let p=a&-a;if(!basis.has(p)){basis.set(p,a);keep.push(w);break}a^=basis.get(p);L.featureXors++}}
  L.maxBasis=Math.max(L.maxBasis,keep.length);return keep;
 }
 function rep(n,gates,D){
  let M=mons(n,D),R=[0n];
  for(let i=n-1;i>=0;i--){let [a,b]=gates[i],out=[];for(let w of R){out.push(w);if(dot(a,w)===b)out.push(w|bit(i))}R=reduce(out,M)}
  return {R,M};
 }
 function ref(n,F){let a=[];for(let i=0;i<2**n;i++){L.referenceWords++;let w=BigInt(i);if(sat(F,w))a.push(w)}return a}
 function* combos(n,k,s=0,p=[]){if(k===0){yield p;return}for(let i=s;i<=n-k;i++)yield* combos(n,k-1,i+1,p.concat([i]))}
 function solve(n,F,maxExc){
  let c=close(n,F);if(!c)return {label:"UNSAT",closure:true};
  let d=c.C.dirs.length,fs=c.fs,chosen=null;
  for(let k=0;k<=Math.min(maxExc,fs.length)&&!chosen;k++)for(let is of combos(fs.length,k)){
   L.exceptionSets++;let set=new Set(is),base=fs.filter((_,i)=>!set.has(i)),exceptions=fs.filter((_,i)=>set.has(i));
   let tr=triangular(d,base);if(tr){chosen={tr,exceptions,k};break}
  }
  if(!chosen)return {label:"UNKNOWN"};
  let {tr,exceptions,k}=chosen;
  let D=Math.min(d,exceptions.reduce((s,f)=>s+f.terms.length,0));
  let E=exceptions.map(f=>f.terms.map(t=>transform(t,tr.C)));
  let {R}=rep(d,tr.gates,D);
  for(let w of R)if(sat(E,w)){let x=lift(c.C,lift(tr.C,w));ck(sat(F,x),"source witness");L.verifiedLifts++;return {label:"SAT",k,D,states:R.length,w:x.toString()}}
  return {label:"UNSAT",k,D,states:R.length};
 }
 const nae=([u,v,w],s=[0,0,0])=>[[bit(u)|bit(v),1^s[0]^s[1]],[bit(u)|bit(w),1^s[0]^s[2]]];
 const owner=(e,b)=>e.map(i=>[bit(i),b]);
 let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 let K5=[...combos(5,3)];
 let common={};
 for(let [name,n,H] of [["Fano",7,fano],["K5_triples",5,K5]]){
  let rows=[];
  for(let j=-1;j<H.length*2;j++){
   let F=H.map((e,i)=>j>=0&&i===Math.floor(j/2)?owner(e,j%2):nae(e)),reference=ref(n,F);
   let a=solve(n,F,H.length);ck(a.label===(reference.length?"SAT":"UNSAT"),"common label");rows.push({owner:j,models:reference.length,...a});
  }
  common[name]=rows;
 }
 let state=20261124;const rng=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n};
 let random={SAT:0,UNSAT:0,UNKNOWN:0,spanChecks:0};
 for(let z=0;z<90;z++){
  let n=3+rng(5),F=[];
  for(let j=0;j<3+rng(5);j++){let a=BigInt(1+rng(2**n-1)),b=BigInt(1+rng(2**n-1));F.push([[a,rng(2)],[b,rng(2)]])}
  if(z%3===0)F.push([[bit(rng(n)),rng(2)]]);
  let refWords=ref(n,F),a=solve(n,F,Math.min(5,F.length));random[a.label]++;
  ck(a.label==="UNKNOWN"||a.label===(refWords.length?"SAT":"UNSAT"),"random formula");
 }
 for(let z=0;z<70;z++){
  let n=2+rng(6),gates=[];
  for(let i=0;i<n;i++){let m=0n;for(let j=i+1;j<n;j++)if(rng(3)===0)m|=bit(j);gates.push([m,rng(2)])}
  let D=1+rng(Math.min(3,n)),{R,M}=rep(n,gates,D);
  let all=[];for(let i=0;i<2**n;i++){L.referenceWords++;let w=BigInt(i);if(gates.every(([a,b],j)=>!(w&bit(j))||dot(a,w)===b))all.push(w)}
  ck(R.every(w=>all.includes(w)),"actual rep");let ar=reduce(all,M);ck(ar.length===R.length,"full span rank");random.spanChecks++;
 }
 let scaling=[];
 for(let n of [8,16,24,32]){
  let gates=[];for(let i=0;i<n;i++){let a=0n;for(let j=i+1;j<n;j++)a|=bit(j);gates.push([a,i===n-1?0:1])}
  let {R}=rep(n,gates,2);
  const q=(w,b)=>Boolean(w&1n)&&dot(gates[0][0],w)===b;
  ck(!R.some(w=>q(w,0)),"forbidden pair");let y=R.find(w=>q(w,1));ck(y!==undefined,"positive pair");ck(gates.every(([a,b],j)=>!(y&bit(j))||dot(a,y)===b),"dense lift");L.verifiedLifts++;
  scaling.push({n,states:R.length,featureCapacity:1+n+n*(n-1)/2,SAT:true,UNSAT:true});
 }
 let loose=[];
 for(let m of [4,8,12,16]){
  let H=Array.from({length:m},(_,i)=>[i,(i+1)%m,m+i]),F=H.map(e=>nae(e));
  let c=close(2*m,F),tr=triangular(2*m,c.fs);ck(tr,"loose cycle peel");
  let {R}=rep(2*m,tr.gates,2),orig=R.map(w=>lift(c.C,lift(tr.C,w)));
  ck(orig.every(w=>sat(F,w)),"cycle witnesses");
  ck(orig.some(w=>dot(bit(0)|bit(1),w)===0)&&orig.some(w=>dot(bit(0)|bit(1),w)===1),"both relative colors");
  loose.push({n:2*m,m,BergeGirth:m,states:R.length});
 }
 // Nonlinear gate counterexample: 00,10,01 span degree 1, but miss 11.
 let M=mons(2,1),basis=reduce([0n,1n,2n],M);ck(basis.length===3,"affine basis");
 ck(!basis.some(w=>w===3n)&&reduce([0n,1n,2n,3n],M).length===3,"quadratic gate failure");
 // Full critical roots have no first private pivot.
 for(let [n,H] of [[7,fano],[5,K5]]){let c=close(n,H.map(e=>nae(e)));ck(triangular(n,c.fs)===null,"critical no pivot")}
 return {seed:20261124,common,random,scaling,loose,ledger:L,negative:{quadraticGate:true,criticalNoFirstPivot:true}};
}
console.log(JSON.stringify(main(),null,2));
