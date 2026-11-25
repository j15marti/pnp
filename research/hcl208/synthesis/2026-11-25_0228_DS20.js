/* Run in JS with frozen BW17 and BS19 JSON objects as inputs. */
function run(raw,bs){
  let checks=0, seed=20261125;
  const assert=(q,msg)=>{checks++;if(!q)throw Error(msg)};
  const rng=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const par=x=>{x^=x>>>16;x^=x>>>8;x^=x>>>4;return (0x6996>>>(x&15))&1};
  const bit=(x,i)=>(x>>>i)&1;
  const dot=(a,b)=>par(a&b);
  const high=x=>31-Math.clz32(x);
  function add(B,x){while(x){let h=high(x);if(B[h])x^=B[h];else{B[h]=x;return true}}return false}
  function outside(B,x){while(x){let h=high(x);if(!B[h])return true;x^=B[h]}return false}
  function nullBasis(rows,n){let B=[];for(let a of rows)add(B,a);let out=[];for(let j=0;j<n;j++)if(!B[j]){let v=1<<j;for(let h=0;h<n;h++)if(B[h]&&dot(B[h],v))v^=1<<h;out.push(v)}return out}
  function canon(P){let B=[];for(let [a,b] of P){while(a){let h=high(a);if(B[h]){a^=B[h][0];b^=B[h][1]}else{B[h]=[a,b];break}}if(!a&&b)return null}return B.filter(Boolean)}
  const mass=P=>P.reduce((s,p)=>s+p.length,0);
  const ok=(P,x)=>P.every(p=>p.some(([a,b])=>dot(a,x)!==b));
  const transform=(P,B)=>P.map(p=>p.map(([a,b])=>[B.reduce((s,v,j)=>s|(dot(a,v)<<j),0),b]));
  const lin=(B,x)=>B.reduce((s,v,j)=>bit(x,j)?s^v:s,0);
  function close(P,n){let B=Array.from({length:n},(_,i)=>1<<i),offset=0,scans=0,deductions=0;
    while(true){P=P.map(canon).filter(p=>p!==null);scans+=P.length;if(P.some(p=>!p.length))return {unsat:true,scans,deductions};
      let p=P.find(p=>p.length===1);if(!p)return {P,n,scans,deductions,lift:x=>offset^lin(B,x)};
      let [a,b]=p[0],h=high(a),base=1<<h; if(b^1)offset^=B[h]; const sub=[];
      for(let i=0;i<n;i++)if(i!==h)sub.push((1<<i)^(bit(a,i)?base:0));
      let f=(b^1)?base:0; P=transform(P.map(q=>q.map(([c,d])=>[c,d^dot(c,f)])),sub);B=sub.map(v=>lin(B,v));n--;deductions++;
    }
  }
  function image(p,v){return p.reduce((s,[a],j)=>s|(dot(a,v)<<j),0)}
  function select(P,n){let V=[],ends=[],I=P.map(()=>[]),queries=0;
    for(let i=0;i<P.length;i++)for(let j=i;j<P.length;j++){
      let Z=nullBasis(P.flatMap((p,h)=>h===i||h===j?[]:p.map(r=>r[0])),n);queries++;
      while(true){let a=0,b=0,v=0;for(let z of Z){let u=outside(I[i],image(P[i],z)),w=i===j||outside(I[j],image(P[j],z));if(u&&w){v=z;break}if(u)a=z;if(w)b=z}
        if(!v&&i!==j&&a&&b)v=a^b;if(!v)break;
        assert(add(I[i],image(P[i],v)),"i independence");if(i!==j)assert(add(I[j],image(P[j],v)),"j independence");
        V.push(v);ends.push(i===j?[i]:[i,j]);
      }
    }return {V,ends,queries}
  }
  function project(P,n,chosen){let {V,ends}=chosen,k=V.length,B=V.slice(),basis=[];for(let v of B)assert(add(basis,v),"global independence");for(let j=0;j<n;j++)if(add(basis,1<<j))B.push(1<<j);
    let Q=transform(P,B),edges=P.map(()=>[]);ends.forEach((E,e)=>E.forEach(i=>edges[i].push(e)));
    let data=Q.map((p,i)=>{let R=p.map(x=>x.slice()),pivot=0,f={};for(let e of edges[i]){let j=R.findIndex((r,j)=>j>=pivot&&bit(r[0],e));assert(j>=0,"private pivot");[R[j],R[pivot]]=[R[pivot],R[j]];for(let h=0;h<R.length;h++)if(h!==pivot&&bit(R[h][0],e)){R[h][0]^=R[pivot][0];R[h][1]^=R[pivot][1]}pivot++}edges[i].forEach((e,j)=>f[e]=[R[j][0]>>>k,R[j][1]]);return {f,active:R.slice(pivot).map(([a,b])=>[a>>>k,b])}});
    let seen=new Set(),components=[],out=[],trees=0,safe=0;
    for(let i=0;i<P.length;i++)if(!seen.has(i)){let nodes=[i],E=new Set();seen.add(i);for(let h=0;h<nodes.length;h++)for(let e of edges[nodes[h]]){E.add(e);for(let j of ends[e])if(!seen.has(j)){seen.add(j);nodes.push(j)}}
      let match={};function aug(i,vis){for(let e of edges[i])if(!vis.has(e)){vis.add(e);if(match[e]===undefined||aug(match[e],vis)){match[e]=i;return true}}return false}
      let saturated=nodes.every(i=>aug(i,new Set()));if(saturated){safe++;components.push({nodes,E:[...E],match});continue}
      assert(E.size===nodes.length-1&&[...E].every(e=>ends[e].length===2),"nonsaturated tree");trees++;
      let rows=nodes.flatMap(i=>data[i].active);
      for(let e of E){let [i,j]=ends[e],[a,b]=data[i].f[e],[c,d]=data[j].f[e];rows.push([a^c,b^d^1])}
      let r=canon(rows);if(r!==null)out.push(r);
      components.push({nodes,E:[...E],match:null});
    }
    function lift(y){let x=0;const forbidden=(i,e)=>{let [a,b]=data[i].f[e];return dot(a,y)^b};const put=(i,e)=>{if(forbidden(i,e)^1)x|=1<<e};
      for(let C of components){if(C.match){for(let e of C.E)if(C.match[e]!==undefined)put(C.match[e],e);continue}
        let roots=C.nodes.filter(i=>data[i].active.some(([a,b])=>dot(a,y)!==b)).slice(0,1),used=new Set();
        if(!roots.length){let e=C.E.find(e=>forbidden(ends[e][0],e)===forbidden(ends[e][1],e));assert(e!==undefined,"missing tree witness");roots=ends[e].slice();used.add(e);put(roots[0],e)}
        let visited=new Set(roots);for(let h=0;h<roots.length;h++)for(let e of edges[roots[h]])if(!used.has(e)){used.add(e);let j=ends[e].find(i=>!visited.has(i));if(j!==undefined){visited.add(j);roots.push(j);put(j,e)}}assert(visited.size===C.nodes.length,"tree lift traversal");
      }return lin(B,x|(y<<k))
    }
    assert(mass(out)<=mass(P)-k,"rank mass contraction");return {P:out,n:n-k,B,k,trees,safe,lift}
  }
  function compare(P,n,name){P=P.map(canon).filter(p=>p!==null);let S=select(P,n),R=project(P,n,S),tested=0,models=0;
    for(let y=0;y<(1<<R.n);y++){let a=ok(R.P,y),b=false;for(let x=0;x<(1<<R.k);x++){tested++;if(ok(P,lin(R.B,x|(y<<R.k)))){b=true;break}}assert(a===b,name+" projection");if(a){models++;assert(ok(P,R.lift(y)),name+" lift")}}
    let C=close(P,n),D;if(!C.unsat){let t=project(C.P,C.n,select(C.P,C.n));D=close(t.P,t.n);let any=false;if(!D.unsat)for(let y=0;y<(1<<D.n);y++)if(ok(D.P,y)){any=true;assert(ok(P,C.lift(t.lift(D.lift(y)))),name+" combined lift");break}assert(any===(models>0),name+" combined decision")}else assert(models===0,name+" closure");
    return {name,selected:R.k,trees:R.trees,safe:R.safe,before:mass(P),after:mass(R.P),models,tested}
  }
  function nae(L){let a=Math.abs(L[0])-1,s=L[0]<0?1:0;return L.slice(1).map(l=>[(1<<a)^(1<<(Math.abs(l)-1)),s^(l<0?1:0)])}
  let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
  const k=bs.common.find(j=>j.K===16).residual.C;
  const bw=raw.O.map(o=>o.t.map(v=>v+1));
  function common(L,n){let P=L.map(nae).map(canon).filter(p=>p!==null),C=close(P,n);if(C.unsat)return {closure:"UNSAT"};let S=select(C.P,C.n);let R=project(C.P,C.n,S);return {owners:P.length,mass:mass(P),closureScans:C.scans,closureDeductions:C.deductions,selected:S.V.length,queries:S.queries,afterMass:mass(R.P),afterOwners:R.P.length}}
  let commonResults={BW17:common(bw,24),K16:common(k,24)};
  let fixed=[
    compare([[[1,0],[4,0]],[[1,1],[8,0]]],4,"tree opposite"),
    compare([[[1,0],[4,0]],[[1,0],[8,0]]],4,"tree equal"),
    compare([[[1,0],[2,0]],[[2,1],[4,0]],[[4,1],[1,1]]],3,"cycle"),
    compare([[[1,0]],[[1,1]]],1,"UNSAT opposite units"),
    compare(fano.map(nae),7,"Fano"),
    compare(fano.map((l,i)=>nae(i===0?[-l[0],...l.slice(1)]:l)),7,"Fano neighbor")
  ];
  let random={jobs:0,sat:0,unsat:0,projected:0,treeComponents:0,safeComponents:0,tested:0};
  for(let t=0;t<100;t++){let n=4+rng(5),m=2+rng(6),P=[];for(let i=0;i<m;i++){let r=1+rng(Math.min(n,4)),p=[];for(let j=0;j<r;j++)p.push([1+rng((1<<n)-1),rng(2)]);let c=canon(p);if(c!==null)P.push(c)}let a=compare(P,n,"random "+t);random.jobs++;random[a.models?"sat":"unsat"]++;random.projected+=a.selected;random.treeComponents+=a.trees;random.safeComponents+=a.safe;random.tested+=a.tested}
  // GD26 K4: map-free discovery followed by grouping exact wide NAE affine packets.
  function cubic(charge){let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],L=[],next=8;for(let u=0;u<4;u++){let E=edges.map((e,j)=>e.includes(u)?j+1:0).filter(Boolean);for(let w=0;w<8;w++)if(par(w)!==bit(charge,u)){let A=E.map((e,j)=>bit(w,j)?-e:e),t=next++;L.push([7,A[0],t],[-t,A[1],A[2]])}}return {P:L.map(nae),n:next-1}}
  let cubicResults=[];for(let charge of [0,1]){let {P,n}=cubic(charge),C=close(P,n),S=select(C.P,C.n),R=project(C.P,C.n,S),count=0;assert(S.V.length>=16,"cubic pivots");for(let y=0;y<(1<<R.n);y++)if(ok(R.P,y)){count++;assert(ok(P,C.lift(R.lift(y))),"cubic lift")}assert(count===(charge?0:16),"cubic count");cubicResults.push({charge,privateDirections:S.V.length,free:R.n,rankMassBefore:mass(P),rankMassAfter:mass(R.P),projectedModels:count})}
  return {checks,commonResults,fixed,random,cubicResults,scope:"small tests only; integer masks n<=30; guards empty; full semantic closure not used; projected counts not source counts"}
}
// Node: node DS20.js BW17.json BS19.json
if(typeof require==='function'&&require.main===module){const fs=require('fs');console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2))}
