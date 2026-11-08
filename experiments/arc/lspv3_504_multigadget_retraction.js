#!/usr/bin/env node
'use strict';
/* LSPV-3/504. Independent finite controls, historical full R_mix341 grammar OPEN. */
const reproduce=function reproduce(){
  "use strict";
  let checks=0, bad=0; const ck=(v,m)=>{checks++;if(!v)throw Error(m)};
  const graphs=[
    {name:"K4",n:4,e:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],ks:[0,1,2,8,16]},
    {name:"K33",n:6,e:Array.from({length:3},(_,a)=>Array.from({length:3},(_,b)=>[a,b+3])).flat(),ks:[0,1,3,12,24]},
    {name:"Cube",n:8,e:Array.from({length:8},(_,i)=>Array.from({length:3},(_,b)=>[i,i^(1<<b)]).filter(x=>x[0]<x[1])).flat(),ks:[0,1,16,32]}];
  const C=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  const eq=(a,b)=>JSON.stringify(C(a))===JSON.stringify(C(b));
  const sat=(cl,a)=>cl.some(l=>a[Math.abs(l)]===(l>0?1:0));
  const models=(F,n)=>{const out=[];for(let mask=0;mask<2**n;mask++){let a=Array.from({length:n+1},(_,i)=>i?((mask>>(i-1))&1):0);if(F.every(c=>sat(c,a)))out.push(a)}return out};
  const source=(g,parity)=>{let inc=Array.from({length:g.n},()=>[]);g.e.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});let f=[];for(let i=0;i<g.n;i++)for(let k=0;k<8;k++){let x=[k&1,(k>>1)&1,(k>>2)&1];if((x[0]^x[1]^x[2])!==parity[i])f.push(C(inc[i].map((v,j)=>x[j]?-v:v)))}return f};
  const gadget=(c,u,v)=>[C([c[0],c[1],u]),C([-u,c[2],v]),C([-u,c[2],-v])];
  const res=(a,b,p)=>{ck(a.includes(p)&&b.includes(-p),"bad pivot");let o=C([...a.filter(l=>l!==p),...b.filter(l=>l!==-p)]);ck(!o.some(l=>o.includes(-l)),"tautology");return o};
  const extender=(c,a,u,v)=>{for(let uu=0;uu<=1;uu++)for(let vv=0;vv<=1;vv++){let b=a.slice();b[u]=uu;b[v]=vv;if(gadget(c,u,v).every(d=>sat(d,b)))return b}return null};
  let records=[];
  for(let g of graphs){
    let E=g.e.length, F=source(g,Array.from({length:g.n},(_,i)=>i?0:1)), even=source(g,Array(g.n).fill(0));
    ck(F.length===4*g.n,"base size");ck(models(F,E).length===0,"odd must be UNSAT");ck(models(even,E).length===2**(E-g.n+1),"even controls");
    let missing=F.map((c,i)=>{let w=models(F.filter((_,j)=>j!==i),E)[0];ck(!!w&&!sat(c,w),"source essential");return w});
    for(let k of g.ks){
      let H=[], map=new Map(), n=E;
      for(let i=0;i<F.length;i++){if(i<k){let u=n+1,v=n+2;n+=2;map.set(i,{u,v,start:H.length});H.push(...gadget(F[i],u,v))}else H.push(F[i])}
      ck(H.length===4*g.n+2*k&&n===E+2*k,"source size");
      for(let i=0;i<F.length;i++)if(map.has(i)){
        let {u,v}=map.get(i), [A,B,D]=gadget(F[i],u,v);
        ck(eq(res(B,D,v),[-u,F[i][2]]),"first resolvent");
        ck(eq(res(A,res(B,D,v),u),F[i]),"retract original");
        for(let mask=0;mask<8;mask++){let a=Array(n+1).fill(0);F[i].forEach((lit,j)=>a[Math.abs(lit)]=(mask>>j)&1);
          ck((extender(F[i],a,u,v)!==null)===sat(F[i],a),"existential local equivalence");
        }
      }
      let essential=0;let pos=0;
      for(let i=0;i<F.length;i++){
        let choices=map.has(i)?[[0,0,0],[1,1,0],[2,1,1]]:[[0,null,null]];
        for(let [offset,uv,vv] of choices){
          let a=missing[i].slice();a.length=n+1;a.fill(0,E+1);
          for(let j=0;j<F.length;j++)if(map.has(j)){
            let {u,v}=map.get(j);
            if(j===i){a[u]=uv;a[v]=vv}else{let b=extender(F[j],a,u,v);ck(b!==null,"extension missing");a=b}
          }
          let deletion=pos+offset;
          ck(!sat(H[deletion],a),"deletion target should be false");
          ck(H.every((d,j)=>j===deletion||sat(d,a)),"deletion witness fails");
          essential++;
        }
        pos+=map.has(i)?3:1;
      }
      ck(essential===H.length,"all clauses essential");
      const q=2*k+3*g.n+(g.n-1);
      ck(q===H.length-1,"source arity exact");
      records.push({graph:g.name,h:g.n,k,originalVars:E,sourceVars:n,sourceClauses:H.length,allClausesEssential:essential,RES:2*k,AND3:3*g.n,XOR:g.n-1,paidDistinctNodes:q,depthBound:4+Math.ceil(Math.log2(g.n))});
    }
  }
  for(let [a,b,p] of [[[1,2,9],[-9,3,10],7],[[1,2,9],[-9,3,10],10],[[-9,3,10],[-9,3,-10],9]]){try{res(a,b,p);throw Error("bad pivot accepted")}catch(e){if(e.message==="bad pivot accepted")throw e;bad++}}
  return {scope:"EXPLICIT DISTINCT R_bridge503: historical R_mix341 acceptance NOT claimed",status:"PROVED/RESTRICTED symbolic plus COMPUTATIONAL finite",sources:"original odd-charge strict signed cubic Tseitin sources",checks,adversarialPivotRejects:bad,records};
};
console.log(JSON.stringify(reproduce(),null,2));
