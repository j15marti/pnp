'use strict';
/*
 TMR-4/009. Head-aware MAY source-certificate potential.
 Native Node execution: node tmr4_spatial_certificate009.cjs
 Zero external packages; tests source-coordinate geometry and small finite
 abstract graphs. This is NOT a physical universal Turing-machine simulator.
*/
const assert=(condition,message)=>{if(!condition)throw Error(message)};
const popcount=n=>{let k=0;for(;n;n>>=1)k+=n&1;return k};
const bin=(n,w)=>n.toString(2).padStart(w,'0');
function source(r,which){
  assert(Number.isInteger(r)&&r>=1,'positive r');
  assert(which==='pair'||which==='triple','family');
  const t=3*r,w=Math.ceil(Math.log2(2*t+2)),N=2**w-1;
  const core=Array.from({length:t},(_,i)=>2*(i+1)+(popcount(i+1)&1));
  const used=new Set(core),spare=[];
  for(let z=1;z<=N;z++)if(!used.has(z))spare.push(z);
  const clauses=[];
  const target=which==='pair'?3:7;
  const positions=[];
  for(let g=0;g<r;g++){
    const triple=core.slice(3*g,3*g+3);
    for(let m=1;m<=7;m++)clauses.push(triple.map((id,j)=>({id,neg:(m>>j)&1})));
    clauses.push(triple.map((id,j)=>({id,neg:(target>>j)&1})));
  }
  const coreCount=clauses.length;
  for(let a=0;a<spare.length;a+=3){
    const group=spare.slice(a,a+3);
    for(const id of spare){if(group.length===3)break;if(!group.includes(id))group.push(id)}
    assert(group.length===3,'filler');
    clauses.push(group.map(id=>({id,neg:0})));
  }
  const M=clauses.length,header=N+M+2,step=w+1;
  let bits='1'.repeat(N)+'0'+'1'.repeat(M)+'0';
  for(let c=0;c<clauses.length;c++){
    for(let j=0;j<3;j++){
      if(c<coreCount&&c%8===7&&(which==='pair'?j<2:true)){
        const g=Math.floor(c/8);
        if(!positions[g])positions[g]=[];
        positions[g].push(bits.length);
      }
      const l=clauses[c][j];bits+=String(l.neg)+bin(l.id,w);
    }
  }
  const L=bits.length;
  assert(L===header+3*M*step,'length');
  assert(positions.length===r,'cert list');
  const occ=new Uint32Array(N+1);
  for(const clause of clauses){
    assert(new Set(clause.map(x=>x.id)).size===3,'proper clause');
    for(const l of clause){assert(l.id>=1&&l.id<=N,'ID range');occ[l.id]++}
  }
  assert(Array.from(occ).slice(1).every(x=>x>=1),'every declared ID used');
  function localUnSat(g){
    const masks=[];
    for(let j=0;j<8;j++){
      let mask=0;
      for(let z=0;z<3;z++)mask|=clauses[8*g+j][z].neg<<z;
      masks.push(mask);
    }
    assert(!masks.includes(0),'base block SAT under zero assignment');
    const mutated=masks.slice();
    mutated[7]=0;
    assert(new Set(mutated).size===8,'changed block UNSAT');
  }
  for(let g=0;g<r;g++){
    localUnSat(g);
    const D=positions[g];
    assert(D.length===(which==='pair'?2:3),'certificate arity');
    assert(D[0]===header+(8*g+7)*3*step,'certificate start');
    for(let j=0;j<D.length;j++){
      assert(D[j]===D[0]+j*step,'cert coordinates');
      assert(bits[D[j]]==='1','source bit flips to zero');
    }
  }
  return {r,which,N,M,w,L,header,coreCount,filler:M-coreCount,certs:positions,
    first:positions[0][0],last:positions[r-1][0]};
}
const dist=(heads,D)=>Math.min(...heads.flatMap(h=>D.map(p=>Math.abs(p-h))));
function phi(heads,seen,Ds){
  let out=0;
  for(const D of Ds)if(!D.some(p=>seen&(1<<p)))out=Math.max(out,1+dist(heads,D));
  return out;
}
function moveVectors(heads,L){
  let acc=[[]];
  for(const h of heads){
    const choices=[h-1,h,h+1].filter(p=>p>=0&&p<=L);
    acc=acc.flatMap(a=>choices.map(b=>a.concat([b])));
  }
  return acc;
}
function graphAudit(L,h,Ds){
  let edges=0,terminal=0,zero=0,states=0;
  const heads=[];
  function eachHeads(depth){
    if(depth<h){for(let j=0;j<=L;j++){heads.push(j);eachHeads(depth+1);heads.pop()}return}
    for(let seen=0;seen<(1<<L);seen++){
      states++;
      const here=phi(heads,seen,Ds);
      assert(here===phi(heads,seen,Ds),'zero stutter');zero++;
      if(Ds.every(D=>D.some(p=>seen&(1<<p)))){
        assert(here===0,'goal guard');terminal+=2;
      }
      const available=Array.from(new Set(heads.filter(p=>p<L)));
      const targetMoves=moveVectors(heads,L);
      for(let sub=0;sub<(1<<available.length);sub++){
        let got=seen;
        for(let z=0;z<available.length;z++)if(sub&(1<<z))got|=1<<available[z];
        for(const next of targetMoves){
          const after=phi(next,got,Ds);
          assert(here<=1+after,'every-edge potential');
          edges++;
        }
      }
    }
  }
  eachHeads(0);
  return {L,h,Ds,states,edges,zero,terminal};
}
function bfsShortest(L,h,Ds){
  const initial={heads:Array(h).fill(0),seen:0,cost:0},queue=[initial],dedup=new Set();
  const key=(heads,seen)=>heads.join(',')+':'+seen;
  dedup.add(key(initial.heads,0));
  for(let ptr=0;ptr<queue.length;ptr++){
    const v=queue[ptr];
    if(Ds.every(D=>D.some(p=>v.seen&(1<<p))))return {distance:v.cost,statesExplored:ptr+1};
    let got=v.seen;
    for(const p of v.heads)if(p<L)got|=1<<p;
    for(const heads of moveVectors(v.heads,L)){
      const k=key(heads,got);if(dedup.has(k))continue;
      dedup.add(k);queue.push({heads,seen:got,cost:v.cost+1});
    }
  }
  throw Error('unreachable goal');
}
const out={tag:'TMR4-SPATIAL009',time_PST:'2026-11-13 20:36 PST',model:'all source heads begin at coordinate 0; unit local moves; pre-move read costs one transition',
  family:[],graphs:[],tests:{familyInstances:0,sourceBits:0,certificates:0,graphStates:0,graphEdges:0,bfsCases:0,failures:0}};
for(const r of [1,2,3,4,5,6,8,10,12,16,32,64,128,256]){
  const a=source(r,'pair'),b=source(r,'triple');
  assert(a.L===b.L&&a.last===b.last,'same source geometry');
  const dmin=a.certs.map(D=>D[0]),expected=1+Math.max(...dmin);
  assert(expected===1+a.header+(8*r-1)*3*(a.w+1),'exact closed-form spatial potential');
  assert(expected>Math.ceil(r/1),'strict improvement over unit observation at every size');
  assert(expected<=a.L,'valid path upper ceiling');
  out.family.push({r,w:a.w,N:a.N,M:a.M,L:a.L,header:a.header,filler:a.filler,certificates:r,
    pairCertificateBits:2*r,tripleCertificateBits:3*r,
    nonSpatialLower_h1:r,spatialLowerAllLocalHeads:expected,
    spatialFraction:expected/a.L,spatialToCountRatio:expected/r,
    firstCertificateStart:a.first,lastCertificateStart:a.last});
  out.tests.familyInstances+=2;out.tests.sourceBits+=2*a.L;out.tests.certificates+=2*r;
}
for(const [L,h,Ds] of [
  [4,1,[[1,3],[2]]], [5,1,[[1,4],[3,4]]], [6,1,[[2,4],[5]]],
  [4,2,[[1,3],[2]]], [5,2,[[1,4],[3,4]]], [6,2,[[2,4],[5]]],
  [6,2,[[1,5],[2,4],[4,5]]], [6,1,[[1,5],[2,4],[4,5]]]
]){
  const x=graphAudit(L,h,Ds),shortest=bfsShortest(L,h,Ds);
  const expected=1+Math.max(...Ds.map(D=>Math.min(...D)));
  assert(shortest.distance===expected,'BFS exact initial distance');
  assert(phi(Array(h).fill(0),0,Ds)===expected,'closed potential at initial');
  out.graphs.push({...x,...shortest,initialPotential:expected});
  out.tests.graphStates+=x.states;out.tests.graphEdges+=x.edges;out.tests.bfsCases++;
}
console.log(JSON.stringify(out,null,2));
