"use strict";
function auditTwo(){
 let checks=0,seed=26112681;const ck=(p,m)=>{if(!p)throw Error(m);checks++};const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>9)%n};
 const bit=(w,i)=>(w>>i)&1,mk=(N,E,S,W)=>N+2*E+4*S+8*W;
 const tab=f=>Array.from({length:16},(_,w)=>w).filter(w=>f(bit(w,0),bit(w,1),bit(w,2),bit(w,3)));
 const holds=(cl,a)=>cl.some(l=>!!((a>>(Math.abs(l)-1))&1)===(l>0));
 function compile(n,cs){
  const m=cs.length,k=Math.max(3,n+3,m+1),r=n,c=m,A=r*k+c,B=A+k,T=[];
  for(let i=0;i<k;i++)for(let j=0;j<k;j++){
   let t=[0];
   if(i<n&&j<m)t=tab((N,E,S,W)=>E===W&&S===(N||+cs[j].some(l=>Math.abs(l)===i+1&&((l>0)===!!W)))&&(i!==0||N===0));
   else if(i<n&&j===m)t=tab((N,E,S,W)=>N===0&&E===0&&S===0);
   else if((i===r||i===r+1)&&j<m)t=tab((N,E,S,W)=>E===W&&S===(N||1-W));
   else if(i>r+1&&j<m)t=tab((N,E,S,W)=>W===0&&E===0&&S===N&&(i!==k-1||S===1));
   else if(i===r&&j===c)t=tab((N,E,S,W)=>N===0&&E===0&&(!W||!S));
   else if(i===r+1&&j===c)t=tab((N,E,S,W)=>E===0&&S===0&&(!W||N));
   T.push(t);
  }
  return {k,r,c,A,B,T};
 }
 function relax(o){const T=o.T.map(t=>t.slice());for(const [v,p] of [[o.A,2],[o.B,0]])T[v]=[...new Set(T[v].flatMap(w=>[w,w^(1<<p)]))];return {...o,T}}
 function decide(o,a,b){let states=new Set([0]);for(let v=0;v<o.T.length;v++){
  const i=Math.floor(v/o.k),j=v%o.k,next=new Set();
  for(const s of states)for(const w of o.T[v]){
   if(bit(w,0)!==bit(s,j)||j&&bit(w,3)!==bit(s,o.k))continue;
   if(j===0&&i===o.r&&bit(w,3)!==a||j===0&&i===o.r+1&&bit(w,3)!==b)continue;
   if(j===o.k-1&&bit(w,1))continue;
   next.add((s&~(1<<j)&~(1<<o.k))|(bit(w,2)<<j)|(bit(w,1)<<o.k));
  }states=next;if(!states.size)return false;
 }return !!states.size}
 function lift(o,n,cs,y,a,b,x){
  let w=Array(o.k*o.k).fill(0),m=cs.length,k=o.k,r=o.r;
  for(let j=0;j<m;j++){
   let z=0;for(let i=0;i<n;i++){let q=bit(y,i),t=z||+cs[j].some(l=>Math.abs(l)===i+1&&((l>0)===!!q));w[i*k+j]=mk(z,q,t,q);z=t}
   w[r*k+j]=mk(z,a,z||1-a,a);z=z||1-a;
   w[(r+1)*k+j]=mk(z,b,z||1-b,b);z=z||1-b;
   for(let i=r+2;i<k;i++)w[i*k+j]=mk(z,0,z,0);
  }
  for(let i=0;i<n;i++)w[i*k+m]=mk(0,0,0,bit(y,i));
  w[o.A]=mk(0,0,x,a);w[o.B]=mk(x,0,0,b);return w;
 }
 function valid(o,w){for(let v=0;v<w.length;v++){if(!o.T[v].includes(w[v]))return false;if(v>=o.k&&bit(w[v-o.k],2)!==bit(w[v],0))return false;if(v%o.k&&bit(w[v-1],1)!==bit(w[v],3))return false}return true}
 function projection(o,w,v){return v===o.A?w[v]&~4:v===o.B?w[v]&~1:w[v]}
 let result={cases:0,sat:0,unsat:0,dpCalls:0,lifts:0,extraWords:0,localSupportChecks:0,maxSide:0};
 for(let q=0;q<300;q++){
  let n=1+rnd(5),m=1+rnd(5),cs=Array.from({length:m},()=>Array.from({length:rnd(4)},()=> (rnd(2)?1:-1)*(1+rnd(n))));
  if(q%3===0)cs=[...cs,[1],[-1]];
  if(q%3===1)cs=cs.map(c=>(c.length?c:[1]).map(Math.abs));
  const sat=Array.from({length:1<<n},(_,y)=>y).some(y=>cs.every(c=>holds(c,y))),o=compile(n,cs),g=relax(o);
  result.cases++;result[sat?"sat":"unsat"]++;result.maxSide=Math.max(result.maxSide,o.k);
  for(let a=0;a<2;a++)for(let b=0;b<2;b++){
   ck(decide(o,a,b)===!(a&&b),"F projected guard");ck(decide(g,a,b)===(!(a&&b)||sat),"G projected guard");result.dpCalls+=2;
  }
  for(let y=0;y<(1<<n);y++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let x=0;x<2;x++){
   let w=lift(o,n,cs,y,a,b,x),yes=cs.every(c=>holds(c,y));
   ck(valid(o,w)===((!a||!x)&&(!b||!!x)&&(!(a&&b)||yes)),"F lift");
   ck(valid(g,w)===(!(a&&b)||yes),"G lift");result.lifts++;
   if(a&&b&&yes){
    result.extraWords++;let u=lift(o,n,cs,y,0,1,1),v=lift(o,n,cs,y,1,0,0);
    ck(valid(o,u)&&valid(o,v),"two original covers");
    for(let i=0;i<w.length;i++){let p=projection(o,w,i);ck(p===projection(o,u,i)||p===projection(o,v,i),"all local words supported");result.localSupportChecks++}
   }
  }
 }
 return {...result,checks,seedFinal:seed};
}
console.log(JSON.stringify(auditTwo(), null, 2));
