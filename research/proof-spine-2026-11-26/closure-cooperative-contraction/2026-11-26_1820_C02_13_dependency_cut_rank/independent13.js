// Independent exhaustive audit. No Python linear algebra or solver imported.
'use strict';
const assert=(p)=>{if(!p)throw Error('assertion')};
let seed=2611261313,checks=0,systems=0,shortening=0,cutchecks=0;
function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function dot(a,b){let x=a&b,t=0;while(x){t^=1;x&=x-1}return t}
function span(v){let s=new Set([0]);for(const x of v)for(const y of [...s])s.add(x^y);return s}
function combine(v,w){let z=0;v.forEach((x,i)=>{if(w>>i&1)z^=x});return z}
for(let t=0;t<400;t++){
  const k=1+rnd(5),q=1+rnd(5),L=[],groups=[];
  for(let i=0;i<q;i++){
    let g=[],r=1+rnd(Math.min(2,k));let V=[];
    while(g.length<r){let a=1+rnd((1<<k)-1);if(span(V).has(a))continue;g.push(L.length);L.push(a);V.push(a)}groups.push(g);
  }
  const R=L.length,D=[];for(let w=0;w<1<<R;w++)if(combine(L,w)===0)D.push(w);
  let B=[];for(const w of D)if(!span(B).has(w))B.push(w);
  assert(D.length==1<<B.length);checks++;
  const Q=L.map((_,i)=>B.reduce((s,v,j)=>s|(((v>>i)&1)<<j),0));
  const h=rnd(1<<R),active=rnd(1<<q),target=combine(Q,h);
  const allowed=(w,A)=>groups.every((g,i)=>!(A>>i&1)||g.some(j=>w>>j&1));
  const W=[];for(let x=0;x<1<<k;x++){let w=h;L.forEach((v,i)=>w^=dot(v,x)<<i);W.push(w)}
  const direct=W.some(w=>allowed(w,active));
  let mask=0;groups.forEach((g,i)=>{if(active>>i&1)for(const j of g)mask|=1<<j});
  let supp=0;for(const w of D)if((w&~mask)===0)supp|=w;
  let J=0;groups.forEach((g,i)=>{if(g.some(j=>supp>>j&1))J|=1<<i});
  assert(direct===W.some(w=>allowed(w,J)));checks++;shortening++;
  // Explicit prefix word enumeration, not the Python recurrence.
  for(let p=0;p<=R;p++){
    const U=span(Q.slice(0,p)),V=span(Q.slice(p));const lam=Math.log2(span(L.slice(0,p)).size)+Math.log2(span(L.slice(p)).size)-Math.log2(span(L).size);
    const I=[...U].filter(z=>V.has(z^target));assert(I.length===2**lam);checks++;cutchecks++;
    for(let w=0;w<1<<p;w++){
      if(!groups.every((g,i)=>g[g.length-1]>=p||!(active>>i&1)||g.some(j=>w>>j&1)))continue;
      const s=combine(Q.slice(0,p),w);if(!V.has(s^target))continue;assert(I.includes(s));checks++;
    }
  }
  const dual=[];for(let w=0;w<1<<R;w++)if(combine(Q,w)===target&&allowed(w,active))dual.push(w);
  assert(direct===(dual.length>0));checks++;systems++;
}
console.log(JSON.stringify({seed:2611261313,systems,checks,shortening,cutchecks},null,2));
