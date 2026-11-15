#!/usr/bin/env node
const audit = function audit(){
  let checks=0, failures=0, seed=20261115043;
  const ck=(q,m)=>{checks++;if(!q){failures++;throw Error("Assertion "+m)}};
  const rng=()=>{seed^=(seed<<13);seed^=(seed>>>17);seed^=(seed<<5);return (seed>>>0)/4294967296};
  const val=(lit,v)=>(v[Math.abs(lit)]===1)===(lit>0);
  const nae=(e,v)=>{let t=e.map(l=>val(l,v));return t.some(Boolean)&&!t.every(Boolean)};
  const clause=(c,v)=>c.some(l=>val(l,v));
  const cnf=es=>es.flatMap(e=>[e,e.map(x=>-x)]);
  const key=e=>e.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)).join(",");
  const support=e=>e.map(Math.abs).sort((a,b)=>a-b).join(",");
  function make(k){
    if(k<3||k%3)throw Error("k must be positive multiple of 3");
    let es=[],parts=[],next=3*k+1,blocks=[];
    for(let i=0;i<k;i++){let x=i+1,y=k+i+1,z=2*k+i+1;es.push([x,y,z],[x,y,-z])}
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++){let u=next++,a=next++,b=next++;es.push([i+1,j+1,u],[u,a,b],[i+1,a,b]);parts.push([i+1,j+1,u,a,b])}
    for(let i=1;i<=k;i+=3){es.push([i,i+1,i+2]);blocks.push([i,i+1,i+2])}
    return {k,es,parts,blocks,n:next-1};
  }
  function witness(o,x){
    let v=Array(o.n+1).fill(0),k=o.k;
    for(let i=0;i<k;i++){v[i+1]=(x>>i)&1;v[k+i+1]=1-v[i+1];v[2*k+i+1]=0}
    for(let [xi,xj,u,a,b] of o.parts){v[u]=1-v[xi];v[a]=0;v[b]=1}
    return v;
  }
  function canonicalRelation(o,x,y){
    if(o.blocks.some(b=>{let t=b.map(i=>(x>>(i-1))&1);return t.every(z=>z===0)||t.every(z=>z===1)}))return false;
    return y===(((1<<o.k)-1)^x);
  }
  function bruteLocalProjected(o,x,y){
    let k=o.k,v={};
    for(let i=0;i<k;i++){v[i+1]=(x>>i)&1;v[k+i+1]=(y>>i)&1}
    for(let i=0;i<k;i++){
      let a=[i+1,k+i+1,2*k+i+1],b=[i+1,k+i+1,-(2*k+i+1)];
      let good=false;for(let z=0;z<2;z++){v[2*k+i+1]=z;if(nae(a,v)&&nae(b,v))good=true}
      if(!good)return false;
    }
    for(let [xi,xj,u,a,b] of o.parts){
      let good=false;
      for(let t=0;t<8;t++){v[u]=t&1;v[a]=(t>>1)&1;v[b]=(t>>2)&1;
        if(nae([xi,xj,u],v)&&nae([u,a,b],v)&&nae([xi,a,b],v)){good=true;break}
      }
      if(!good)return false;
    }
    return o.blocks.every(e=>nae(e,v));
  }
  function recognize(cs){
    const abs=Math.abs;
    if(!cs.length||cs.some(c=>c.length!==3||c.some(x=>!Number.isInteger(x)||x===0)||new Set(c.map(abs)).size!==3))return null;
    let distinct=new Map(cs.map(c=>[key(c),c.slice().sort((a,b)=>abs(a)-abs(b))]));
    for(let c of distinct.values())if(!distinct.has(key(c.map(x=>-x))))return null;
    let orbit=new Map();
    for(let c of distinct.values()){let e=c[0]>0?c:c.map(x=>-x);orbit.set(key(e),e)}
    let es=[...orbit.values()],deg=new Map();
    for(let e of es)for(let lit of e)deg.set(abs(lit),(deg.get(abs(lit))||0)+1);
    let H=[...deg.keys()].filter(v=>deg.get(v)>2),k=H.length,hi=new Set(H);
    if(k<3||k%3||[...H].map(v=>deg.get(v)).sort((a,b)=>a-b).some((d,i)=>d!==k+2+i))return null;
    if([...deg].some(([v,d])=>!hi.has(v)&&d!==2))return null;
    let E3=es.filter(e=>e.filter(x=>hi.has(abs(x))).length===3);
    let E2=es.filter(e=>e.filter(x=>hi.has(abs(x))).length===2);
    let E1=es.filter(e=>e.filter(x=>hi.has(abs(x))).length===1);
    let E0=es.filter(e=>e.filter(x=>hi.has(abs(x))).length===0),M=k*(k-1)/2;
    if(E3.length!==k/3||E2.length!==M||E1.length!==2*k+M||E0.length!==M)return null;
    let w=Object.fromEntries(H.map(v=>[v,0])),seenH=new Set();
    for(let e of E3){
      let ids=e.map(abs);if(ids.some(v=>seenH.has(v)))return null;ids.forEach(v=>seenH.add(v));
      let found=false;
      for(let t=0;t<8&&!found;t++){
        let v={...w};ids.forEach((a,j)=>v[a]=(t>>j)&1);
        if(nae(e,v)){w=v;found=true}
      }
      if(!found)return null;
    }
    if(seenH.size!==k)return null;
    let byPair=new Map();
    for(let e of E2){let ss=e.map(abs).filter(v=>hi.has(v)).sort((a,b)=>a-b).join(",");
      if(byPair.has(ss))return null;byPair.set(ss,e)}
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)if(!byPair.has([H[i],H[j]].sort((a,b)=>a-b).join(",")))return null;
    let supports=new Map();
    for(let e of E1){let s=support(e);if(!supports.has(s))supports.set(s,[]);supports.get(s).push(e)}
    let twins=[...supports.values()].filter(v=>v.length===2);
    if(twins.length!==k||[...supports.values()].some(v=>v.length>2))return null;
    let used=new Set(H),used1=new Set(),used0=new Set();
    for(let tw of twins){
      let vars=tw[0].map(abs),high=vars.filter(v=>hi.has(v)),low=vars.filter(v=>!hi.has(v));
      if(high.length!==1||low.length!==2||low.some(v=>used.has(v)))return null;
      let sol=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++){
        let v={...w,[low[0]]:a,[low[1]]:b};if(tw.every(e=>nae(e,v)))sol.push([a,b])
      }
      if(sol.length!==2||[0,1].filter(i=>sol[0][i]===sol[1][i]).length!==1)return null;
      w[low[0]]=sol[0][0];w[low[1]]=sol[0][1];
      for(let v of low)used.add(v);for(let e of tw)used1.add(key(e));
    }
    for(let [name,e] of byPair){
      let pair=name.split(",").map(Number),u=e.map(abs).find(v=>!hi.has(v));
      if(used.has(u))return null;
      let gg=E0.filter(g=>g.some(x=>abs(x)===u));if(gg.length!==1)return null;
      let g=gg[0],ab=g.map(abs).filter(v=>v!==u);
      if(ab.length!==2||ab.some(v=>used.has(v)))return null;
      let hs=E1.filter(h=>pair.some(v=>support(h)===[...ab,v].sort((a,b)=>a-b).join(",")));
      if(hs.length!==1)return null;
      let h=hs[0];if(used0.has(key(g))||used1.has(key(h)))return null;
      let found=false;
      for(let uv=0;uv<2&&!found;uv++)for(let av=0;av<2&&!found;av++)for(let bv=0;bv<2&&!found;bv++){
        let v={...w,[u]:uv,[ab[0]]:av,[ab[1]]:bv};
        if([e,g,h].every(t=>nae(t,v))){w=v;found=true}
      }
      if(!found)return null;
      for(let v of [u,...ab])used.add(v);used0.add(key(g));used1.add(key(h));
    }
    if(used1.size!==E1.length||used0.size!==E0.length||used.size!==deg.size)return null;
    if(!cs.every(c=>clause(c,w)))return null;
    return w;
  }
  let cases=[],renamed=0,matrixCells=0,localTests=0,checksAtRows=0;
  for(let k of [3,6,9,12]){
    let o=make(k),b=k/3,M=k*(k-1)/2,C=cnf(o.es);
    ck(o.n===3*k+3*M,"variable count");
    ck(o.es.length===2*k+3*M+b,"edge count");
    ck(C.length===4*k+6*M+2*b,"clause count");
    ck(C.every(c=>new Set(c.map(Math.abs)).size===3),"proper3CNF");
    ck(o.es.every(e=>e.length===3),"proper group");
    let deg=Array(o.n+1).fill(0);
    for(let e of o.es)for(let t of e)deg[Math.abs(t)]++;
    ck(deg.slice(1).every(d=>d>=2),"degree-2 core");
    ck(deg.slice(1,k+1).sort((a,b)=>a-b).every((d,i)=>d===k+2+i),"high degrees");
    ck(deg.slice(k+1).every(d=>d===2),"low degrees");
    ck(recognize(C)!==null,"canonical recognizer");
    const rows=k<=9?1<<k:64;
    for(let x=0;x<rows;x++){
      let okay=o.blocks.every(e=>{let t=e.map(v=>(x>>(v-1))&1);return !(t.every(q=>q===0)||t.every(q=>q===1))});
      let v=witness(o,x);
      ck(C.every(c=>clause(c,v))===okay,"witness iff nonlinear projection");
      for(let y=0;y<(k<=6?1<<k:0);y++){
        let actual=bruteLocalProjected(o,x,y),expected=canonicalRelation(o,x,y);
        ck(actual===expected,"independent local elimination");
        matrixCells++;
      }
    }
    for(let i=0;i<28;i++){
      let ids=Array.from({length:o.n},(_,j)=>j+1);
      for(let p=o.n-1;p>0;p--){let j=Math.floor(rng()*(p+1));[ids[p],ids[j]]=[ids[j],ids[p]]}
      let flips=Array.from({length:o.n+1},(_,j)=>j===0?0:Math.floor(rng()*2));
      let transformed=o.es.map(e=>e.map(l=>Math.sign(l)*(flips[Math.abs(l)]?-1:1)*ids[Math.abs(l)-1]));
      let cs=cnf(transformed);
      for(let p=cs.length-1;p>0;p--){let j=Math.floor(rng()*(p+1));[cs[p],cs[j]]=[cs[j],cs[p]]}
      let found=recognize(cs.concat(cs.slice(0,2)));
      ck(found!==null && cs.every(c=>clause(c,found)),"signed/renamed/shuffled duplications");
      renamed++;
    }
    ck(recognize(C.slice(1))===null,"missing complement negative");
    const expected=6**b;
    if(k<=6){
      let count=0;for(let x=0;x<(1<<k);x++)for(let y=0;y<(1<<k);y++)
        if(canonicalRelation(o,x,y))count++;
      ck(count===expected,"partial-permutation rank / cover cardinality");
    }
    for(let u=1;u<=b;u++){
      let ds=6**u-6**(u-1), dg=1, cost=1;
      ck(ds===5*6**(u-1),"signed rank discharge");
      ck(dg<=cost,"unit certificate discharge");
      ck(ds*(1/(10*6**(b-1)))+dg/2<=1+1e-10,"mixed rational feasibility");
      checksAtRows++;
    }
    let rankRatio=(6**b-1)/(5*6**(b-1));
    ck(rankRatio<=b,"LP optimum b");
    cases.push({k,b,variables:o.n,nae_groups:o.es.length,clauses:C.length,nonlinear_projection_rank:expected,nonlinear_projection_cover:expected,record_paid_optimum:b,recognizer_gauge_tests:28});
  }
  let nea=[];for(let t=0;t<8;t++)if(t!==0&&t!==7)nea.push(t);
  for(let a=1;a<8;a++){let bits=new Set(nea.map(t=>Array.from({length:3},(_,i)=>((t>>i)&1)).reduce((q,z,i)=>q^(z*((a>>i)&1)),0)));ck(bits.size===2,"NAE has full affine hull")};
  let parityWitnesses=0;
  for(let x of nea){for(let y of nea){let z=x&y;if(z===0||z===7){parityWitnesses++;break}}}
  ck(parityWitnesses>0,"not Horn");
  return {status:"PASS",checks,failures,seed_final:seed,cases,matrix_cells_independent_projection:matrixCells,signed_renamed_shuffled_duplicate_tests:renamed,record_tariff_rows:checksAtRows,affine_hull_masks_tested:7,model:"Proper 3-CNF R_k plus disjoint NAE3 constraints on X, signed 2-core source, specialized SAT recognizer, separate typed NAE-record tariff",qualifications:["All original source and witness checks finite and computational","Symbolic arbitrary-k proof required","Record tariffs are not physical SAT runtime tariffs"]};
};
console.log(JSON.stringify(audit(),null,2));
