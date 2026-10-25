"use strict";
// ARC-CNF-CONTINUATION121 reproducible semantic and proper-3CNF audit.
// Run: node 2026-10-25_0927_ARC_CNF_CONTINUATION121_repro.js
// No external dependencies; symbolic finite checker; not an FLMV machine implementation.
function runAudit() {
  "use strict";
  const seed = 20261025;
  let state=seed>>>0, checks=0;
  const assert=(x,msg)=>{checks++;if(!x)throw Error(msg||("failed assertion "+checks));};
  const rng=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state;};
  const bits=(n,k)=>Array.from({length:k},(_,i)=>(n>>i)&1);
  const members=(mask,U)=>Array.from({length:U},(_,i)=>i).filter(i=>(mask>>>i)&1);
  const sharedLabel=(P,R,h,S)=>P.some(u=>S.includes(u)&&R.some(v=>S.includes(v)&&h[u]===h[v]));
  const actual=(P,R,S)=>P.some(u=>S.includes(u)&&R.includes(u));
  const criterion=(P,R,h)=>!P.some(u=>!R.includes(u)&&R.some(v=>!P.includes(v)&&h[u]===h[v]));
  let exhaustiveCases=0, filterComparisons=0;
  for(let k=1;k<=2;k++) {
    const U=1<<k, V=1<<U;
    for(let p=0;p<V;p++) for(let q=0;q<V;q++) for(let hm=0;hm<V;hm++) {
      const P=members(p,U),R=members(q,U),h=Array.from({length:U},(_,i)=>(hm>>>i)&1);
      let all=true;
      for(let f=0;f<V;f++){
        const S=members(f,U),a=actual(P,R,S),b=sharedLabel(P,R,h,S);
        if(a!==b)all=false;
        filterComparisons++;
      }
      assert(all===criterion(P,R,h),"exhaustive filter iff k="+k+" p="+p+" q="+q+" h="+hm);
      exhaustiveCases++;
    }
  }
  let sampledK3=0,sampledComparisons=0;
  for(let j=0;j<360;j++){
    const P=members(rng()&255,8),R=members(rng()&255,8),
      h=Array.from({length:8},()=>rng()&3);
    let all=true;
    for(let f=0;f<256;f++){
      const S=members(f,8);
      const a=actual(P,R,S),b=sharedLabel(P,R,h,S);
      if(a!==b)all=false;
      sampledComparisons++;
    }
    assert(all===criterion(P,R,h),"sampled k3 mismatch");
    sampledK3++;
  }
  function builder(start=3){return {next:start,clauses:[]};}
  function add(b,c) {
    assert(c.length===3&&new Set(c.map(x=>Math.abs(x))).size===3&&c.every(x=>x!==0),"bad proper 3CNF");
    b.clauses.push(c);
  }
  function unit(b,l) {
    const a=++b.next,c=++b.next;
    for(const s of [1,-1])for(const t of [1,-1])add(b,[l,s*a,t*c]);
  }
  function binary(b,l,m) {
    assert(Math.abs(l)!==Math.abs(m),"binary same name");
    const a=++b.next;add(b,[l,m,a]);add(b,[l,m,-a]);
  }
  function holds(cs,mask){return cs.every(c=>c.some(l=>((mask>>>(Math.abs(l)-1))&1)===(l>0?1:0)));}
  function sat(cs,n,modulo=0,word=0) {
    for(let a=0;a<Math.pow(2,n);a++)if((a&((1<<modulo)-1))===word&&holds(cs,a))return true;
    return false;
  }
  function serialize(cs,n){return "p cnf "+n+" "+cs.length+"\n"+cs.map(c=>c.join(" ")+" 0").join("\n")+"\n";}
  function parse(s) {
    const l=s.trim().split(/\r?\n/),m=/^p cnf (\d+) (\d+)$/.exec(l[0]);assert(!!m,"bad header");
    const n=+m[1],count=+m[2],cs=l.slice(1).map(row=>row.trim().split(/\s+/).map(Number));
    assert(cs.length===count,"wrong clause count");
    assert(cs.every(c=>c.length===4&&c[3]===0&&new Set(c.slice(0,3).map(x=>Math.abs(x))).size===3&&c.slice(0,3).every(x=>x!==0&&Math.abs(x)<=n)),"invalid literal/body");
    return {n,cs:cs.map(c=>c.slice(0,3))};
  }
  let pointsChecked=0,encodedTwoPointBits=[];
  for(let u=0;u<8;u++)for(let v=0;v<8;v++) {
    const f=builder(4);
    for(let i=0;i<3;i++){
      const lit=i+1,lu=(u&(1<<i))?lit:-lit,lv=(v&(1<<i))?lit:-lit;
      binary(f,4,lu);
      binary(f,-4,lv);
    }
    const str=serialize(f.clauses,f.next),p=parse(str);
    encodedTwoPointBits.push(str.length);
    for(let w=0;w<8;w++)assert(sat(p.cs,p.n,3,w)===(w===u||w===v),
      "two-point filter wrong u,v,w="+[u,v,w].join(","));
    pointsChecked++;
  }
  const p=builder();
  unit(p,-1);binary(p,-2,-3);
  const q=builder(p.next);
  unit(q,-2);binary(q,-1,-3);
  const D=p.clauses,R=q.clauses;
  const P=Array.from({length:8},(_,i)=>i).filter(w=>sat(D,p.next,3,w));
  const Q=Array.from({length:8},(_,i)=>i).filter(w=>sat(R,q.next,3,w));
  assert(JSON.stringify(P)==='[0,2,4]',"P wrong");
  assert(JSON.stringify(Q)==='[0,1,4]',"Q wrong");
  const h=Array.from({length:8},(_,i)=>i+1);h[2]=0;h[1]=0;
  assert(criterion(P,Q,h)===false,"must violate all-filter criterion");
  function pinsSet(word){
    return Array.from({length:8},(_,j)=>j).filter(w=>{
      for(let i=0;i<3;i++){
        const t=word[i];if(t!==-1&&((w>>i)&1)!==t)return false;
      }return true;
    });
  }
  let pins=0;
  for(let pin=0;pin<27;pin++) {
    let qn=pin,arr=[];
    for(let i=0;i<3;i++){const x=qn%3;qn=Math.floor(qn/3);arr.push(x===0?-1:x-1);}
    const S=pinsSet(arr);
    assert(actual(P,Q,S)===sharedLabel(P,Q,h,S),"pin compatibility failed "+pin);
    pins++;
  }
  const root=[...D,...R];
  const first=builder(q.next);first.clauses=root.slice();unit(first,-3);
  const second=builder(first.next);second.clauses=first.clauses.slice();binary(second,1,2);
  const encs=[
    serialize(root,q.next),
    serialize(first.clauses,first.next),
    serialize(second.clauses,second.next)
  ];
  const actualLabels=[],parsedLengths=[],headers=[];
  for(let i=0;i<3;i++){
    const x=parse(encs[i]);headers.push({variables:x.n,clauses:x.cs.length});
    parsedLengths.push(encs[i].length);
    actualLabels.push(sat(x.cs,x.n));
  }
  assert(JSON.stringify(actualLabels)==='[true,true,false]',"expected SAT SAT UNSAT");
  const Sroot=Array.from({length:8},(_,i)=>i);
  const Sfirst=Sroot.filter(x=>(x&4)===0);
  const Ssecond=Sfirst.filter(x=>(x&1)!==0||(x&2)!==0);
  const quotientLabels=[Sroot,Sfirst,Ssecond].map(S=>sharedLabel(P,Q,h,S));
  assert(JSON.stringify(quotientLabels)==='[true,true,true]',"expected false SAT grandchild quotient");
  assert(encs[0].length<encs[1].length&&encs[1].length<encs[2].length,"children are larger");
  assert([...new Set(D.flat().map(Math.abs).filter(x=>x>3))].every(x=>!new Set(R.flat().map(Math.abs)).has(x)),
    "private auxiliaries alias across modules");
  for(const cs of [D,R])assert(cs.every(c=>c.filter(x=>Math.abs(x)<=3).every(x=>[1,2,3].includes(Math.abs(x)))),"source-name mismatch");
  // Both-label hostile controls, ordinary proper 3CNF
  const plus=(x,y,z)=>[x,y,z];
  const cube=Array.from({length:8},(_,j)=>[1,2,3].map((v,i)=>(j>>i)&1?-v:v));
  assert(!sat(cube,3),"8-clause UNSAT core");
  assert(sat([plus(1,2,3)],3),"Horn/easy SAT");
  const parity=(odd)=>cube.filter((_,j)=>(bits(j,3).reduce((a,b)=>a+b,0)&1)!==odd);
  const even=parity(0),odd=parity(1);
  assert(sat(even,3)&&sat(odd,3),"affine both SAT");
  assert(!sat([...even,...odd],3),"affine conflict UNSAT");
  const graph=[[1,2,3],[4,5,6]];
  assert(sat(graph,6),"disconnected graph SAT");
  assert(!sat([...graph,...cube],6),"disconnected UNSAT core");
  const alias=builder(1);unit(alias,1); const other=builder(alias.next);unit(other,-1);
  assert(!sat([...alias.clauses,...other.clauses],other.next),"correct source alias UNSAT");
  const badRenamed=other.clauses.map(c=>c.map(l=>Math.abs(l)===1?(l>0?other.next+1:-(other.next+1)):l));
  assert(sat([...alias.clauses,...badRenamed],other.next+1),"invalid alias causes false SAT");
  let malformedRejected=false;
  try{parse(encs[2].replace(/^p cnf \d+ \d+/, 'p cnf 12 17'));}catch(e){malformedRejected=true;}
  assert(malformedRejected,"malformed header not rejected");
  return {
    run_id:"ARC-CNF-CONTINUATION121",seed,checks,failures:0,exhaustiveCases,filterComparisons,
    sampledK3,sampledComparisons,pointsChecked,twoPointBitSizes:[Math.min(...encodedTwoPointBits),Math.max(...encodedTwoPointBits)],
    pinPatternsTested:pins,commonBoundaryNames:[1,2,3],
    projectedP:P,projectedR:Q,rootFirstGrandchildActual:actualLabels,rootFirstGrandchildReusedQuotient:quotientLabels,
    properEncodedSizesBytes:parsedLengths,headers,controls:["Horn SAT","8-clause UNSAT","affine SAT both phases","affine UNSAT","disconnected SAT/UNSAT","source-name alias false SAT","malformed header rejection"],
    implementation:"pure deterministic JS, full k<=2 enumeration and seeded k=3 samples; brute force proper ordinary CNF finite cases",
    disclaimer:"NO FLMV asymptotic lower bound, no all-input favorable A-assisted transition, no assertion about physical flip or bit-time"
  };
}
console.log(JSON.stringify(runAudit(),null,2));
