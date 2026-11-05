"use strict";
function run(){
 const F=[[1],[1,3],[-2]], n=3;
 const evcl=(c,a)=>c.some(l=>a[Math.abs(l)]===(l>0));
 const sat=(cnf,n)=>{let k=0;for(let b=0;b<2**n;b++){let a={};for(let j=1;j<=n;j++)a[j]=!!(b&(1<<(j-1)));if(cnf.every(c=>evcl(c,a)))k++;}return k;};
 function check(steps){let nd=F.map(c=>({k:"cl",c}));for(let r of steps){
  const get=i=>{if(!Number.isInteger(i)||i<0||i>=nd.length)throw Error("bad reference");return nd[i];};
  if(r.op==="AND3"){let a=get(r.p),b=get(r.q),vars=[...new Set([...a.c,...b.c].map(Math.abs))].sort((x,y)=>x-y);
   if(vars.length>3||r.bits.length!==2**vars.length)throw Error("support");
   for(let i=0;i<r.bits.length;i++){let A={};vars.forEach((v,j)=>A[v]=!!(i&(1<<(vars.length-1-j))));if(!!r.bits[i] !== (evcl(a.c,A)&&evcl(b.c,A)))throw Error("AND3");}
   nd.push({k:"factor",vars,bits:r.bits});
  }else if(r.op==="LOCAL"){let a=get(r.p);if(a.k!=="factor")throw Error("LOCAL type");
   let vars=[...new Set([...a.vars,...r.c.map(Math.abs)])].sort((x,y)=>x-y);if(vars.length>3)throw Error("LOCAL support");
   for(let i=0;i<2**vars.length;i++){let A={};vars.forEach((v,j)=>A[v]=!!(i&(1<<(vars.length-1-j))));let j=0;for(const v of a.vars)j=2*j+Number(A[v]);if(a.bits[j]&&!evcl(r.c,A))throw Error("LOCAL implication");}
   nd.push({k:"cl",c:r.c});
  }else if(r.op==="RES"){let a=get(r.p),b=get(r.q);if(a.k!=="cl"||b.k!=="cl"||!a.c.includes(r.pivot)||!b.c.includes(-r.pivot))throw Error("bad pivot");
   let c=[...new Set([...a.c,...b.c].filter(l=>Math.abs(l)!==Math.abs(r.pivot)))].sort((x,y)=>x-y);
   if(JSON.stringify(c)!==JSON.stringify(r.c))throw Error("wrong resolvent");nd.push({k:"cl",c});
  }else throw Error("invalid op");
 }return nd;}
 const P=[{op:"AND3",p:0,q:1,bits:[0,0,1,1]},{op:"LOCAL",p:3,c:[1,2]},{op:"RES",p:4,q:2,pivot:2,c:[1]}];
 if(check(P).length!==6||sat(F,n)!==2)throw Error("baseline");
 let p=JSON.parse(JSON.stringify(P));p[1].c=[1];let fail="";try{check(p);}catch(e){fail=e.message;}if(fail!=="bad pivot")throw Error("expected pivot failure");
 p=JSON.parse(JSON.stringify(P));p[1].c=[1,2,3];p[2].c=[1,3];check(p);
 p=JSON.parse(JSON.stringify(P));p[1].c=[-1,2];let unsafe="";try{check(p);}catch(e){unsafe=e.message;}if(unsafe!=="LOCAL implication")throw Error("expected implication failure");
 p=JSON.parse(JSON.stringify(P));p[0].bits=[0,1,1,1];let mutate="";try{check(p);}catch(e){mutate=e.message;}if(mutate!=="AND3")throw Error("expected AND3 failure");
 function parityCNF(edges,charge){let cl=[];for(let v=0;v<4;v++){let vars=[];edges.forEach((e,i)=>{if(e.includes(v))vars.push(i+1)});for(let b=0;b<8;b++){let par=((b&1)?1:0)^((b&2)?1:0)^((b&4)?1:0);if(par!==charge[v])cl.push(vars.map((x,i)=>(b&(1<<i))?-x:x));}}return cl;}
 let E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], parity=[sat(parityCNF(E,[1,0,0,0]),6),sat(parityCNF(E,[0,0,0,0]),6)];
 if(parity[0]!==0||parity[1]!==8)throw Error("parity");
 return {q:3,original_sat_models:2,canonicalization_replay_breaks_pivot:true,valid_weakening_with_repaired_resolvent:true,invalid_LOCAL_rejected:true,invalid_AND3_rejected:true,tseitin_odd_even_models:parity,source_bytes:JSON.stringify(F).length,proof_bytes:JSON.stringify(P).length};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
