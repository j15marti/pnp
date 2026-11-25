"use strict";
function run(){
 const stats={checks:0,closureScans:0,matroidCalls:0,augmentations:0,rowReductions:0,referenceWords:0,lifts:0};
 const assert=(v,msg)=>{stats.checks++;if(!v)throw Error(msg)};
 const bit=i=>1n<<BigInt(i);
 const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 function basis(rows){const B=new Map();for(let v of rows){while(v){let p=v.toString(2).length-1;if(B.has(p))v^=B.get(p);else{B.set(p,v);break}}}return B}
 function reduce(v,B){for(const p of [...B.keys()].sort((a,b)=>b-a))if(v&bit(p))v^=B.get(p);return v}
 function valid(P,x){return P.every(o=>o.a.some((r,i)=>parity(r&x)!==o.b[i]))}
 function close(P){stats.closureScans++;for(const o of P)assert(basis(o.a).size===2&&o.a.length===2,"rank-two control required");return P}
 // Matroid intersection: partition by owner, binary linear independence.
 function mi(P,B=new Map()){
  stats.matroidCalls++;
  const E=P.flatMap((o,i)=>o.a.map((a,j)=>({i,j,v:reduce(a,B)})));
  let I=new Set();
  while(true){
   const selected=[...I], chosen=new Map(selected.map(k=>[E[k].i,k])), L=new Map();
   for(let t=0;t<selected.length;t++){
    let v=E[selected[t]].v,c=bit(t);
    while(v){let p=v.toString(2).length-1;if(L.has(p)){v^=L.get(p)[0];c^=L.get(p)[1]}else{L.set(p,[v,c]);break}}
    assert(v!==0n,"independent selection");
   }
   const prev=new Map(),q=[];
   for(let k=0;k<E.length;k++)if(!I.has(k)&&!chosen.has(E[k].i)){prev.set(k,-1);q.push(k)}
   let sink=-1;
   for(let h=0;h<q.length&&sink<0;h++){
    const k=q[h];let edges=[];
    if(I.has(k)){for(let l=0;l<E.length;l++)if(!I.has(l)&&E[l].i===E[k].i)edges.push(l)}
    else{
     let v=E[k].v,c=0n;
     for(const p of [...L.keys()].sort((a,b)=>b-a))if(v&bit(p)){v^=L.get(p)[0];c^=L.get(p)[1];stats.rowReductions++}
     if(v){sink=k;break}
     edges=selected.filter((_,t)=>(c&bit(t))!==0n);
    }
    for(const l of edges)if(!prev.has(l)){prev.set(l,k);q.push(l)}
   }
   if(sink<0)break;
   for(let k=sink;k!==-1;k=prev.get(k)){if(I.has(k))I.delete(k);else I.add(k)}
   stats.augmentations++;
   assert(new Set([...I].map(k=>E[k].i)).size===I.size,"partition");
   assert(basis([...I].map(k=>E[k].v)).size===I.size,"linear");
  }
  return [...I].map(k=>E[k]);
 }
 const deficit=P=>P.length-mi(P).length;
 function core(P){
  close(P);const d=deficit(P);
  const C=d===0?[]:P.filter((_,i)=>deficit(P.filter((_,j)=>i!==j))<d);
  assert(C.length-basis(C.flatMap(o=>o.a)).size===d,"core max");
  const ids=new Set(C);const O=P.filter(o=>!ids.has(o));const B=basis(C.flatMap(o=>o.a));
  const rep=mi(O,B);assert(rep.length===O.length,"quotient Hall");
  close(C);
  return {C,O,B,rep,d};
 }
 function solve(rows){
  const B=new Map();
  for(let [v,b] of rows){while(v){const p=v.toString(2).length-1;if(B.has(p)){v^=B.get(p)[0];b^=B.get(p)[1]}else{B.set(p,[v,b]);break}}if(!v&&b)throw Error("inconsistent lift")}
  let x=0n;for(const p of [...B.keys()].sort((a,b)=>a-b)){const [v,b]=B.get(p);if(parity(v&x)!==b)x|=bit(p)}return x;
 }
 function lift(P,k,x){assert(valid(k.C,x),"core witness");const rows=[...k.B.values()].map(a=>[a,parity(a&x)]);for(const e of k.rep){const o=k.O[e.i];rows.push([o.a[e.j],o.b[e.j]^1])}const y=solve(rows);assert(valid(P,y),"lift valid");assert([...k.B.values()].every(a=>parity(a&x)===parity(a&y)),"preserve core observations");stats.lifts++;return y}
 function enumerate(P,n){const models=[];for(let i=0;i<2**n;i++){stats.referenceWords++;if(valid(P,BigInt(i)))models.push(BigInt(i))}return models}
 function bruteD(P){let d=0;for(let s=0;s<2**P.length;s++){const A=P.filter((_,i)=>(s>>i)&1);d=Math.max(d,A.length-basis(A.flatMap(o=>o.a)).size)}return d}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(([a,b,c])=>({a:[bit(a)^bit(b),bit(a)^bit(c)],b:[0,0]}));
 function mod(start){const a=bit(start),b=bit(start+1),c=bit(start+2),d=bit(start+3),g=bit(0)^bit(1);return [[a,b],[c,d],[a^c,b^d],[a^d,b^c^d]].map(([u,v])=>({a:[u^g,v],b:[0,0]}))}
 let seed=20815;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const details=[];let sat=0,unsat=0;
 function check(name,P,n,brute=true){const k=core(P),models=enumerate(P,n),cm=enumerate(k.C,n);assert(!!models.length===!!cm.length,"equivalence "+name);for(const x of cm)lift(P,k,x);if(brute)assert(bruteD(P)===k.d,"deficiency oracle");if(models.length)sat++;else unsat++;details.push({name,n,m:P.length,core:k.C.length,deficiency:k.d,models:models.length})}
 check("Fano UNSAT",fano,7);for(let i=0;i<7;i++)for(const b of [[1,0],[0,1],[1,1]])check("Fano sign "+i+"/"+b,fano.map((o,j)=>j===i?{a:o.a,b}:o),7);
 for(let i=0;i<7;i++)check("Fano deletion "+i,fano.filter((_,j)=>j!==i),7);
 for(let t=0;t<60;t++){const n=3+rnd(5),m=1+rnd(9),P=[];for(let j=0;j<m;j++){let a=1+rnd(2**n-1),b;do{b=1+rnd(2**n-1)}while(a===b);P.push({a:[BigInt(a),BigInt(b)],b:[rnd(2),rnd(2)]})}check("random "+t,P,n)}
 const neighbor=fano.map((o,i)=>i===0?{a:o.a,b:[1,0]}:o);
 for(const [name,F] of [["UNSAT",fano],["SAT",neighbor]]){const P=[...F,...mod(7)];check("MDS attached "+name,P,11);let min=Infinity;for(let v=1n;v<1n<<11n;v++){const hits=P.filter(o=>o.a.some(a=>parity(a&v))).length;if(hits)min=Math.min(min,hits)}assert(min>=3,"no private pair");details[details.length-1].minimumVisibleOwners=min;}
 const scales=[];
 for(const t of [1,4,12])for(const [name,F] of [["UNSAT",fano],["SAT",neighbor]]){const P=[...F,...Array.from({length:t},(_,i)=>mod(7+4*i)).flat()];const k=core(P);assert(k.C.length===7&&k.d===1,"scaled core");const cm=enumerate(k.C,7);assert(!!cm.length===(name==="SAT"),"core label");if(cm.length)lift(P,k,cm[0]);scales.push({name,modules:t,variables:7+4*t,owners:P.length,core:k.C.length,rankMassBefore:2*P.length,rankMassAfter:2*k.C.length,sourceModelsEnumerated:false});}
 return {seed:20815,stats,sat,unsat,details,scales,note:"Small references enumerate; scaling uses proved reduction and exhaustive seven-variable core, not a general SAT terminal. No physical S/CM measurement. Only rank-two, unguarded controls; guard absorption and singleton deductions beyond stagnation unexecuted."};
}
console.log(JSON.stringify(run(),null,2));
