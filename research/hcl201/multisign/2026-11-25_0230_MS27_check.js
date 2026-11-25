const fs=require('fs');
const specs=[
  [
    "9164cb11c6fcdf96d470de9d86b061e3201a591f",
    "research/constructive-shared-hubs/wheels/2026-11-24_2315_BW17_frozen.json"
  ],
  [
    "ff92a1c3d44e4b48dc9a7bf215825075396cae5a",
    "research/constructive-shared-hubs/solver/2026-11-25_0155_BS19_results.json"
  ]
];
function run(inputs){
 const ck=(x,m)=>{if(!x)throw Error(m)}, key=(a,b)=>a<b?a+","+b:b+","+a;
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function triples(n){let T=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++)T.push([i,j,k]);return T}
 function edges(t){return [key(t[0],t[1]),key(t[0],t[2]),key(t[1],t[2])]}
 function ref(n,O){let count=0,word=null;for(let x=0;x<2**n;x++)if(O.every(t=>{let a=t.map(i=>x>>i&1);return a.some(Boolean)&&a.some(b=>!b)})){count++;if(word===null)word=x}return {count,word}}
 function unitSolve(A,b,n){let M=A.map((r,i)=>[...r.map(BigInt),BigInt(b[i])]),piv=[],unused=new Set(Array.from({length:n},(_,i)=>i));
  while(M.length){let z=M.findIndex(r=>[...unused].some(j=>r[j]===1n||r[j]===-1n));
   if(z<0){if(M.some(r=>[...unused].every(j=>r[j]===0n)&&r[n]!==0n))return {status:"inconsistent-unit"};if(M.every(r=>[...unused].every(j=>!r[j])))break;return {status:"DECLINE-nonunit",remaining:M.length,pivots:piv.length}}
   let r=M.splice(z,1)[0],j=[...unused].find(j=>r[j]===1n||r[j]===-1n);if(r[j]===-1n)r=r.map(x=>-x);unused.delete(j);piv.push([j,r]);for(let k=0;k<M.length;k++){let x=M[k][j];if(x)M[k]=M[k].map((v,l)=>v-x*r[l])}
  }
  let v=Array(n).fill(0n);for(let [j,r] of piv.reverse()){v[j]=r[n]-r.slice(0,n).reduce((s,x,k)=>s+(k===j?0n:x*v[k]),0n)}
  ck(A.every((r,i)=>r.reduce((s,x,j)=>s+BigInt(x)*v[j],0n)===BigInt(b[i])),"integer solution replay");
  return {status:"PASS",v:v.map(String),pivots:piv.length}
 }
 function chart(name,n,O,reference=null,knownWord=null){
  const em=new Map();for(let i=0;i<O.length;i++)for(let e of edges(O[i])){ck(!em.has(e),"nonlinear source");em.set(e,i)}
  let E=[...em.keys()],T=triples(n),cliques=T.filter(t=>edges(t).every(e=>em.has(e))),own=new Set(O.map(t=>t.slice().sort((a,b)=>a-b).join(",")));
  let es=E.map(e=>cliques.filter(t=>edges(t).includes(e)).length);
  let balanced=O.every(t=>{let z=edges(t).map(e=>es[E.indexOf(e)]);return z.every(x=>x===z[0])});
  let lambda=O.map(t=>es[E.indexOf(edges(t)[0])]);
  let forceCert=balanced?{ownerMultipliers:lambda,triangles:cliques,identity:lambda.reduce((a,b)=>a+b,0)===cliques.length}:null;
  if(balanced)ck(forceCert.identity,"dual count");
  let LPchecks=0,positive=0,zeros=0;
  for(let t of T){let w=[];for(let x=0;x<8;x++){let s=[0,1,2].map(i=>x>>i&1? -1:1);let a=3;[[0,1],[0,2],[1,2]].forEach(([i,j])=>{if(em.has(key(t[i],t[j])))a-=s[i]*s[j]});ck(a>=0,"LP negative");w.push(a);a?positive++:zeros++}
   ck(w.reduce((a,b)=>a+b,0)===24,"LP norm");if(own.has(t.join(",")))ck(!w[0]&&!w[7],"owner LP");
   for(let i=0;i<3;i++){ck(w.reduce((s,x,k)=>s+((k>>i&1)?x:0),0)===12,"single");LPchecks++}
   for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){ck(w.reduce((s,x,k)=>s+(((k>>i&1)!==(k>>j&1))?x:0),0)===(em.has(key(t[i],t[j]))?16:12),"pair");LPchecks++}
  }
  const before=Array(E.length).fill(0n);for(let t of O)before[E.indexOf(edges(t)[0])]=1n;
  function verifyMass(v,strict){let checks=0,neg=0;for(let t of T){let p=edges(t).map(e=>em.has(e)?-v[E.indexOf(e)]:0n),w=[1n+p[0]+p[1]+p[2],-p[0]-p[1],-p[0]-p[2],p[0],-p[1]-p[2],p[1],p[2],0n];ck(w.reduce((a,b)=>a+b,0n)===1n,"int mass");
   for(let i=0;i<3;i++){ck(w.reduce((s,x,k)=>s+((k>>i&1)?x:0n),0n)===0n,"int single");checks++}
   [[0,1],[0,2],[1,2]].forEach(([i,j],h)=>{ck(w.reduce((s,x,k)=>s+((k>>i&1)&&(k>>j&1)?x:0n),0n)===p[h],"int pair");checks++});
   if(own.has(t.join(","))||strict&&edges(t).every(e=>em.has(e)))ck(!w[0]&&!w[7],"int support");
   neg+=w.filter(x=>x<0n).length;
  }return {checks,neg}}
  const standalone=verifyMass(before,false);
  const A=cliques.map(t=>E.map(e=>edges(t).includes(e)?1:0));
  const candidate=unitSolve(A,A.map(()=>1),E.length);let coupled=null;
  if(candidate.status==="PASS")coupled=verifyMass(candidate.v.map(BigInt),true);
  // Exact rational obstruction: if all triangles are forced, a K5 clique forces each edge mismatch to 2/3.
  let K5=null;if(balanced){outer:for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++)for(let d=c+1;d<n;d++)for(let e=d+1;e<n;e++){let s=[a,b,c,d,e];if(s.every((u,i)=>s.slice(i+1).every(v=>em.has(key(u,v))))){K5=s;break outer}}}
  if(knownWord!==null)ck(O.every(t=>{let a=t.map(i=>knownWord>>i&1);return a.some(Boolean)&&a.some(b=>!b)}),"peer source witness");
  return {name,n,owners:O.length,edges:E.length,triples:T.length,cliques:cliques.length,balanced,forceCert,K5,status:K5?"UNSAT":coupled?"RELAXATION-PASSES":"DECLINE",LPchecks,positive,zeros,standalone,candidate,coupled,reference,knownWord};
 }
 let f=chart("Fano",7,F,ref(7,F)),fd=chart("Fano deletion",7,F.slice(0,-1),ref(7,F.slice(0,-1)));
 ck(f.status==="UNSAT"&&f.reference.count===0&&fd.reference.count===10,"controls");
 let T=[[0,1,2],[2,3,4],[4,5,6],[6,7,8],[8,9,0]];
 let cycle=chart("linear loose cycle",10,T,ref(10,T));ck(cycle.status==="RELAXATION-PASSES"&&cycle.reference.count>0,"cycle");
 let bw=inputs[0],BW=chart("BW17 raw",bw.n,bw.O.map(o=>o.t),null,12130883);
 let k=inputs[1].common.find(x=>x.K===16),ids=[...new Set(k.residual.C.flat().map(Math.abs))].sort((a,b)=>a-b);
 let count=0,lifts=0,first=null;function good(w,C){return C.every(t=>{let a=t.map(l=>(w>>(Math.abs(l)-1)&1)^(l<0?1:0));return a.some(Boolean)&&a.some(b=>!b)})}
 // Reference only, using complete actual K16 wide-owner registry and reverse logs.
 for(let x=0;x<2**ids.length;x++){let w=ids.reduce((s,v,i)=>s|((x>>i&1)<<(v-1)),0);if(!good(w,k.residual.C))continue;count++;
  for(let l of k.residual.log.slice().reverse()){let v=l.v,cs=l.bucket.map(t=>[v,...t]);let z=w&~(1<<(v-1));if(good(z,cs))w=z;else{w=z|(1<<(v-1));ck(good(w,cs),"reverse")}}
  ck(good(w,bw.O.map(o=>o.t.map(v=>v+1))),"original replay");lifts++;if(first===null)first=w
 }ck(count===246&&lifts===246,"K16 reference");
 return {controls:[f,fd,cycle],BW,K16:{ids,owners:k.residual.C.length,wideOwners:k.residual.C.filter(c=>c.length!==3).length,referenceCount:count,lifts,first,scope:"reference replay only; triple-source terminal not applied to wide factors"}};
}
const inputs=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));if(inputs.length!==specs.length)throw Error('two inputs in listed order');console.log(JSON.stringify(run(inputs),null,2));
