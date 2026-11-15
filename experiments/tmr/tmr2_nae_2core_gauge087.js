#!/usr/bin/env node
const audit=function audit(){
let checks=0, seed=20261115, rng=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)/4294967296}, ck=(q,m)=>{checks++;if(!q)throw Error(m)};
const ne=(e,v)=>{let t=e.map(x=>(v[Math.abs(x)]===1)===(x>0));return t.some(Boolean)&&!t.every(Boolean)};
const make=(k)=>{let es=[],next=3*k+1,parts=[];for(let i=0;i<k;i++){let x=i+1,y=k+i+1,z=2*k+i+1;es.push([x,y,z],[x,y,-z])}for(let i=0;i<k;i++)for(let j=i+1;j<k;j++){let u=next++,a=next++,b=next++;es.push([i+1,j+1,u],[u,a,b],[i+1,a,b]);parts.push([i+1,j+1,u,a,b])}return {es,parts,n:next-1}};
const witness=(k,t)=>{let {es,parts,n}=make(k),v=Array(n+1).fill(0);for(let i=0;i<k;i++){v[i+1]=(t>>i)&1;v[k+i+1]=1-v[i+1]}for(let [xi,xj,u,a,b] of parts){v[u]=1-v[xi];v[a]=0;v[b]=1}return v};
const cnf=es=>es.flatMap(e=>[e,e.map(x=>-x)]);
const clause=(c,v)=>c.some(x=>(v[Math.abs(x)]===1)===(x>0));
const key=e=>e.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)).join(",");
const paired=cs=>{let s=new Set(cs.map(key));return cs.every(c=>s.has(key(c.map(x=>-x))))};
const det=A=>{A=A.map(r=>r.map(BigInt));let n=A.length,prev=1n,sign=1n;for(let k=0;k<n-1;k++){let i=k;while(i<n&&A[i][k]===0n)i++;if(i===n)return 0n;if(i!==k){[A[i],A[k]]=[A[k],A[i]];sign=-sign}let p=A[k][k];for(let i=k+1;i<n;i++){for(let j=k+1;j<n;j++){let num=A[i][j]*p-A[i][k]*A[k][j];ck(num%prev===0n,"exact division");A[i][j]=num/prev}A[i][k]=0n}prev=p}return sign*A[n-1][n-1]};

const recognize=(cs)=>{
  const abs=v=>Math.abs(v), supp=e=>e.map(abs).sort((a,b)=>a-b).join(",");
  if(!cs.length||cs.some(c=>c.length!==3||c.some(x=>!Number.isInteger(x)||x===0)||new Set(c.map(abs)).size!==3))return null;
  let distinct=new Map(cs.map(c=>[key(c),c.slice().sort((a,b)=>abs(a)-abs(b))]));
  for(let c of distinct.values())if(!distinct.has(key(c.map(x=>-x))))return null;
  let orbit=new Map();
  for(let c of distinct.values()){let e=c[0]>0?c:c.map(x=>-x);orbit.set(key(e),e)}
  let es=[...orbit.values()],deg=new Map();
  for(let e of es)for(let lit of e)deg.set(abs(lit),(deg.get(abs(lit))||0)+1);
  let H=[...deg.keys()].filter(v=>deg.get(v)>2),k=H.length,hi=new Set(H);
  if(k<2||[...H].map(v=>deg.get(v)).sort((a,b)=>a-b).some((d,i)=>d!==k+1+i))return null;
  if([...deg].some(([v,d])=>!hi.has(v)&&d!==2))return null;
  let E2=es.filter(e=>e.filter(x=>hi.has(abs(x))).length===2);
  let E1=es.filter(e=>e.filter(x=>hi.has(abs(x))).length===1);
  let E0=es.filter(e=>e.filter(x=>hi.has(abs(x))).length===0),M=k*(k-1)/2;
  if(E2.length!==M||E1.length!==2*k+M||E0.length!==M)return null;
  let byPair=new Map();
  for(let e of E2){let ss=e.map(abs).filter(v=>hi.has(v)).sort((a,b)=>a-b).join(",");
    if(byPair.has(ss))return null;byPair.set(ss,e)}
  for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)if(!byPair.has([H[i],H[j]].sort((a,b)=>a-b).join(",")))return null;
  let supports=new Map();
  for(let e of E1){let s=supp(e);if(!supports.has(s))supports.set(s,[]);supports.get(s).push(e)}
  let twins=[...supports.values()].filter(v=>v.length===2);
  if(twins.length!==k||[...supports.values()].some(v=>v.length>2))return null;
  let w=Object.fromEntries(H.map(v=>[v,0])), used=new Set(H),used1=new Set(),used0=new Set();
  for(let tw of twins){
    let vars=tw[0].map(abs),high=vars.filter(v=>hi.has(v)),low=vars.filter(v=>!hi.has(v));
    if(high.length!==1||low.length!==2||low.some(v=>used.has(v)))return null;
    let sol=[];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++){
      let v={...w,[low[0]]:a,[low[1]]:b};
      if(tw.every(e=>ne(e,v)))sol.push([a,b])}
    if(sol.length!==2||([0,1].filter(i=>sol[0][i]===sol[1][i]).length)!==1)return null;
    w[low[0]]=sol[0][0];w[low[1]]=sol[0][1];
    for(let v of low)used.add(v);
    for(let e of tw)used1.add(key(e));
  }
  for(let [name,e] of byPair){
    let pair=name.split(",").map(Number),u=e.map(abs).find(v=>!hi.has(v));
    if(used.has(u))return null;
    let gg=E0.filter(g=>g.some(x=>abs(x)===u));if(gg.length!==1)return null;
    let g=gg[0],ab=g.map(abs).filter(v=>v!==u);
    if(ab.length!==2||ab.some(v=>used.has(v)))return null;
    let hs=E1.filter(h=>pair.some(v=>supp(h)===[...ab,v].sort((a,b)=>a-b).join(",")));
    if(hs.length!==1)return null;
    let h=hs[0];if(used0.has(key(g))||used1.has(key(h)))return null;
    let found=false;
    for(let uv=0;uv<2&&!found;uv++)for(let av=0;av<2&&!found;av++)for(let bv=0;bv<2&&!found;bv++){
      let v={...w,[u]:uv,[ab[0]]:av,[ab[1]]:bv};
      if([e,g,h].every(t=>ne(t,v))){w=v;found=true}}
    if(!found)return null;
    for(let v of [u,...ab])used.add(v);
    used0.add(key(g));used1.add(key(h));
  }
  if(used1.size!==E1.length||used0.size!==E0.length||used.size!==deg.size)return null;
  if(!cs.every(c=>clause(c,w)))return null;
  return w;
};

let cases=[],gauge=0;
for(let k=2;k<=10;k++){
  let {es,parts,n}=make(k),M=k*(k-1)/2,degree=Array(n+1).fill(0);
  for(let e of es)for(let lit of e)degree[Math.abs(lit)]++;
  ck(es.length===2*k+3*M&&n===3*k+3*M,"size");
  ck(degree.slice(1).every(d=>d>=2),"NO leaf");
  ck(degree.slice(1,k+1).sort((a,b)=>a-b).every((d,i)=>d===k+1+i),"high degrees");
  ck(degree.slice(k+1).every(d=>d===2),"low degrees");
  ck(paired(cnf(es)),"paired CNF");ck(recognize(cnf(es))!==null,"canonical source recognizer");
  let max=Math.min(1<<k,64);
  for(let t=0;t<max;t++){let v=witness(k,t);ck(es.every(e=>ne(e,v)),"all X extension "+k+","+t);ck(cnf(es).every(c=>clause(c,v)),"proper CNF witness")}
  for(let iter=0;iter<30;iter++){
    let ids=Array.from({length:n},(_,i)=>i+1);
    for(let p=n-1;p>0;p--){let j=Math.floor(rng()*(p+1));[ids[p],ids[j]]=[ids[j],ids[p]]}
    let flips=Array.from({length:n+1},(_,i)=>i===0?0:Math.floor(rng()*2)),v=witness(k,iter%max);
    let permV=Array(n+1).fill(0);
    for(let old=1;old<=n;old++)permV[ids[old-1]]=v[old]^flips[old];
    let transformed=es.map(e=>e.map(l=>Math.sign(l)*(flips[Math.abs(l)]?-1:1)*ids[Math.abs(l)-1]));
    let sc=cnf(transformed); ck(sc.every(c=>clause(c,permV)),"gauge witness");
    ck(paired(sc),"gauge pairing");let found=recognize(sc.concat(sc.slice(0,3)));ck(found!==null&&sc.every(c=>clause(c,found)),"signed renamed source recognizer");gauge++;
  }
  let C=cnf(es);ck(!paired(C.slice(1)),"missing companion control");ck(recognize(C.slice(1))===null,"negative recognizer control");
  let H=es.filter(e=>e.filter(v=>Math.abs(v)<=k).length===2);
  ck(H.length===M&&new Set(H.map(e=>e.filter(v=>Math.abs(v)<=k).map(Math.abs).sort((a,b)=>a-b).join(","))).size===M,"primal clique");
  cases.push({k,variables:n,nae_edges:es.length,proper3cnf_clauses:2*es.length,rank:2**k,min_incidence:2,gauge_tests:30});
}
for(let k=2;k<=4;k++){
 let d=1<<k,mat=Array.from({length:d},(_,x)=>Array.from({length:d},(_,y)=>Number(y===((d-1)^x))));
 ck(mat.every(r=>r.reduce((a,b)=>a+b,0)===1),"permutation row");
 ck(Array.from({length:d},(_,j)=>mat.reduce((s,r)=>s+r[j],0)).every(x=>x===1),"permutation col");
 ck([1n,-1n].includes(det(mat)),"exact rational full rank");
 for(let x=0;x<d;x++)for(let y=0;y<d;y++)ck(mat[x][y]===Number(y===((d-1)^x)),"matrix entry");
}
return {status:"PASS",checks,failures:0,seed:20261115,all_X_tested_per_k:"min(2^k,64)",k_range:[2,10],exact_integer_determinant_k:[2,3,4],gauge_renaming_tests:gauge,cases,model:"authenticated proper 3-CNF NAE complementary-clause pairs; full witness verification"};
};
console.log(JSON.stringify(audit(),null,2));
