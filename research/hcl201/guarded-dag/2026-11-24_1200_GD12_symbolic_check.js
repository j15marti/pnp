"use strict";
function symbolic(){
 const ledger={calls:0,closureSweeps:0,rowTests:0,deletions:0,transitions:0,peakStates:0,assertions:0};
 const assert=(p,m)=>{ledger.assertions++;if(!p)throw Error(m)};
 // Independent source bits; each used twice in correlated guarded edges.
 function make(k){
  const D=[[[0,0]]], F=[], bits=[];let prev=0;
  const add=d=>{D.push(d);return D.length-1};
  const lab=()=>[[-1,0],[0,0],[0,1],[1,0],[1,1]];
  function arc(u,v,cross,weight,x=null){
   const scope=[u,v,...(x===null?[]:[x])];
   F.push({scope,ok:a=>{const [p,q,g]=a;if(x!==null&&g===0)return true;if(p[0]<0)return true;if(q[0]<0)return false;const cap=cross?0:p[0]+weight;return q[0]<=cap&&!(q[1]&&q[0]===cap)}});
  }
  for(let i=0;i<k;i++){const x=add([0,1]),a=add(lab()),b=add(lab());bits.push(x);arc(prev,a,true,0,x);arc(a,b,false,0,x);arc(b,a,false,1);prev=b}
  const t=add([[-1,0]]);arc(prev,t,true,0);
  return {D,F,bits};
 }
 function count(P,pins){
  ledger.calls++;const D=P.D.map((d,i)=>pins.has(i)?d.filter(x=>x===pins.get(i)):d.slice()),F=P.F;
  const rowOK=(f,at,val)=>{
   const a=Array(f.scope.length);
   function go(j){if(j===a.length){ledger.rowTests++;return f.ok(a)}const u=f.scope[j];for(const b of u===at?[val]:D[u]){a[j]=b;if(go(j+1))return true}return false}
   return go(0);
  };
  if(D.some(d=>!d.length))return 0n;
  // Unconditional structural closure at root, restart after each certified deletion.
  // Under pins, closure is conditional and all pins remain in domains.
  for(;;){ledger.closureSweeps++;let changed=false;
   outer:for(const f of F)for(const u of f.scope)for(let j=0;j<D[u].length;j++)if(!rowOK(f,u,D[u][j])){
    D[u].splice(j,1);ledger.deletions++;changed=true;if(!D[u].length)return 0n;break outer;
   }
   if(!changed)break;
  }
  const last=D.map((_,v)=>Math.max(v,...F.filter(f=>f.scope.includes(v)).map(f=>Math.max(...f.scope))));
  const ends=D.map((_,v)=>F.filter(f=>Math.max(...f.scope)===v));
  let frontier=[],S=new Map([["",1n]]);
  for(let v=0;v<D.length;v++){
   const next=frontier.filter(u=>last[u]>v);if(last[v]>v)next.push(v);const O=new Map();
   for(const [key,w] of S){
    const old=key===""?[]:key.split(",").map(Number);
    for(let j=0;j<D[v].length;j++){
     ledger.transitions++;const get=u=>u===v?D[v][j]:D[u][old[frontier.indexOf(u)]];
     if(!ends[v].every(f=>f.ok(f.scope.map(get))))continue;
     const nk=next.map(u=>u===v?j:old[frontier.indexOf(u)]).join(",");
     const a=D[v][j],sign=Array.isArray(a)&&a[1]?-1n:1n;
     O.set(nk,(O.get(nk)??0n)+sign*w);
    }
   }
   for(const [key,w] of O)if(w===0n)O.delete(key);
   frontier=next;S=O;ledger.peakStates=Math.max(ledger.peakStates,S.size);
  }
  return S.get("")??0n;
 }
 const results=[];
 for(const k of [1,4,16,64,128]){
  const P=make(k),start=ledger.transitions,uncond=count(P,new Map());
  assert(uncond===(1n<<BigInt(k))-1n,"exact source count");
  const all1=new Map(P.bits.map(i=>[i,1]));assert(count(P,all1)===0n,"UNSAT pin");
  const one0=new Map([[P.bits[0],0]]);assert(count(P,one0)===(1n<<BigInt(k-1)),"SAT pin");
  const attempts=ledger.transitions-start;
  // Reconstruct by positive counts, preferring 1 so the last bit must flip.
  let pins=new Map();for(const i of P.bits){pins.set(i,1);if(count(P,pins)===0n){pins.set(i,0);assert(count(P,pins)>0n,"positive child")}}
  assert([...pins.values()].some(x=>x===0),"source witness");
  results.push({k,count:String(uncond),decisionAndTwoPinsTransitions:attempts,witness:[...pins.values()].join("")});
 }
 return {results,ledger};
}
console.log(JSON.stringify(symbolic(),null,2));
