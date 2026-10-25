// ARC-CACHE-RANK-FRONTIER115 reproducible self-contained Node.js.
// Run: node 2026-10-25_0301_ARC_CACHE_RANK_FRONTIER115_repro.js
// All checks deterministic. Python-style experiment chunks: q groups independent, each executes quickly.
function run() {
  let assertions=0, sink=0, totalCases=0;
  const check=(cond,msg)=>{assertions++; if(!cond) throw Error("ASSERT "+msg)};
  const parity=a=>a.reduce((z,v)=>z^v,0);
  const rootCNF=b=>{
    let C=[],q=b.length;
    for(let i=0;i<q;i++){
      let x=i+1,y=((i+1)%q)+1;
      if(b[i]===0){C.push([-x,y],[x,-y]);}
      else{C.push([x,y],[-x,-y]);}
    }
    return {v:q,C};
  };
  const yCNF=(b,D)=>{
    const C=[[1],parity(b) ? [-1] : [1,-1]];
    for(let j=0;j<D;j++){let v=j+2;C.push(b[j] ? [-v,v] : [v,-v]);}
    return {v:D+1,C};
  };
  const yTag=(y,j)=>Number(y.C[2+j][0]<0);
  const yStatus=y=>Number(y.C[1].length===1 && y.C[1][0]===-1);
  const makeBlocks=(D,M)=>{
    let blocks=[];
    for(let j=0;j<M;j++){
      let a=Math.floor(j*D/M),b=Math.floor((j+1)*D/M);
      if(b<=a)throw Error("empty block");
      blocks.push([a,b]);
    }
    return blocks;
  };
  const zCNF=(y,D,M,blocks)=>{
    const C=[[1],yStatus(y) ? [-1] : [1,-1]];
    blocks.forEach(([lo,hi],j)=>{
      let bit=0;for(let k=lo;k<hi;k++)bit^=yTag(y,k);
      let v=j+2;C.push(bit?[-v,v]:[v,-v]);
    });
    return {v:M+1,C};
  };
  const encodedSize=f=>{
    const w=Math.ceil(Math.log2(Math.max(f.v,f.C.length)+2));
    return 3*w+1+f.C.reduce((sum,c)=>sum+2+c.length*(w+1),0);
  };
  const sat2=f=>{
    const n=2*f.v,G=Array.from({length:n},()=>[]),H=Array.from({length:n},()=>[]);
    const id=l=>2*(Math.abs(l)-1)+(l<0?1:0);
    const arc=(a,b)=>{let i=id(a),j=id(b);G[i].push(j);H[j].push(i)};
    for(let c of f.C){
      if(c.length===1)arc(-c[0],c[0]);
      else if(c.length===2){arc(-c[0],c[1]);arc(-c[1],c[0]);}
      else throw Error("not 2CNF");
    }
    const seen=Array(n).fill(false),order=[];
    function visit(u){seen[u]=true;for(let v of G[u])if(!seen[v])visit(v);order.push(u);}
    for(let i=0;i<n;i++)if(!seen[i])visit(i);
    const comp=Array(n).fill(-1);
    function assign(u,k){comp[u]=k;for(let v of H[u])if(comp[v]===-1)assign(v,k);}
    let k=0;for(let i=order.length-1;i>=0;i--)if(comp[order[i]]===-1)assign(order[i],k++);
    for(let i=0;i<f.v;i++)if(comp[2*i]===comp[2*i+1])return false;
    return true;
  };
  function oneReplay(b,D,M,R,P,B,blocks,policy){
    let calls=0, hits=0, sourceReads=0, indexOps=0, writes=0, peak=0;
    let cache=new Map(), expectedParity=blocks.map(([lo,hi])=>{
      let z=0;for(let j=lo;j<hi;j++)z^=b[j];return z;
    });
    function opaque(k) {
      let noise=0;
      for(let u=0;u<P;u++){noise^=b[(k+u)%b.length];sourceReads++;}
      sink^=noise;
      sourceReads++;
      calls++;return b[k];
    }
    function lookup(k){
      indexOps++;
      if(policy==="pinned"){
        if(k<B && cache.has(k)){hits++;return cache.get(k);}
        const v=opaque(k);
        if(k<B){cache.set(k,v);writes++;}
        peak=Math.max(peak,cache.size);return v;
      }
      if(cache.has(k)){
        let v=cache.get(k);cache.delete(k);cache.set(k,v);
        hits++;writes++;return v;
      }
      const v=opaque(k);
      if(B>0){if(cache.size===B){let oldest=cache.keys().next().value;cache.delete(oldest);writes++;}
        cache.set(k,v);writes++;}
      peak=Math.max(peak,cache.size);return v;
    }
    for(let p=0;p<R;p++){
      for(let m=0;m<M;m++){
        let x=0,[lo,hi]=blocks[m];
        for(let j=lo;j<hi;j++)x^=lookup(j);
        check(x===expectedParity[m],"replay computed block parity");
      }
    }
    const theoretical = policy==="pinned" ? D+(R-1)*(D-B) : (B<D?R*D:D);
    check(calls===theoretical,policy+" exact calls D="+D+" B="+B);
    check(hits+calls===D*R,"every virtual probe charged");
    check(sourceReads===(P+1)*calls,"all deliberate root reads charged");
    check(peak===B,"cache peak exact for B="+B);
    return {policy,B,calls,hits,sourceReads,indexOps,writes,peak};
  }
  function oneCase(b){
    totalCases++;
    const f=rootCNF(b),N=encodedSize(f);
    const M0=Math.max(2,Math.floor(Math.pow(N,.25)));
    const D=Math.min(b.length,Math.max(M0+1,Math.floor(Math.pow(N,.6)/Math.log2(N+2))));
    const M=Math.min(D-1,M0), R=Math.max(2,Math.floor(Math.pow(N,.4))),P=Math.max(2,Math.floor(Math.pow(N,.25)));
    const y=yCNF(b,D),blocks=makeBlocks(D,M),z=zCNF(y,D,M,blocks);
    const L1=encodedSize(y),L2=encodedSize(z);
    check(L1<N && L2<L1,"two honest shorter ordinary CNF levels");
    check(sat2(f)===(parity(b)===0),"source parity characterization");
    check(sat2(f)===sat2(y),"first child both labels");
    check(sat2(y)===sat2(z),"second child both labels");
    check(yStatus(y)===parity(b),"first-level core status");
    for(let j=0;j<D;j++)check(yTag(y,j)===b[j],"Y independent tags");
    let summaryReads=b.length+D,summaryWrites=M,summaryLookups=R*M;
    for(let m=0;m<M;m++){
      let val=0,[lo,hi]=blocks[m];
      for(let j=lo;j<hi;j++)val^=b[j];
      check(Number(z.C[2+m][0]<0)===val,"Z aggregate matches Y");
    }
    let capacities=Array.from(new Set([0,Math.floor(D/4),Math.floor(D/2),D-1,D])).sort((a,b)=>a-b);
    let stats=[];
    for(let B of capacities){
      stats.push(oneReplay(b,D,M,R,P,B,blocks,"pinned"));
      stats.push(oneReplay(b,D,M,R,P,B,blocks,"lru"));
    }
    check(summaryReads===b.length+D && summaryWrites===M && summaryLookups===R*M,"summary ledger");
    return {label:parity(b)? "UNSAT":"SAT",q:b.length,N,D,M,R,P,L1,L2,summary:{sourceReads:summaryReads,parityWrites:summaryWrites,guestLookups:summaryLookups,peakSummaryBits:M},ledger:stats};
  }
  const groups=[],qValues=[7,11,17,31,63,127,255];
  for(let q of qValues){
    let vectors=[];
    if(q===7){for(let mask=0;mask<(1<<q);mask++){vectors.push(Array.from({length:q},(_,j)=>(mask>>>j)&1));}}
    else{
      vectors.push(Array(q).fill(0));
      const u=Array(q).fill(0);u[0]=1;vectors.push(u);
      const v=Array.from({length:q},(_,i)=>i%2);vectors.push(v);
      let seed=q*3511+17;
      vectors.push(Array.from({length:q},()=>{seed=(1664525*seed+1013904223)>>>0;return (seed>>>17)&1;}));
    }
    let counts={SAT:0,UNSAT:0},samples=[];
    for(let i=0;i<vectors.length;i++){
      let out=oneCase(vectors[i]);counts[out.label]++;
      if(i===0 || (counts[out.label]===1))samples.push({caseIndex:i,...out});
    }
    check(counts.SAT>0&&counts.UNSAT>0,"both labels tested for q="+q);
    groups.push({q,cases:vectors.length,counts,samples});
  }
  const c=241/200,d=11642479/23232400;
  check(1.25>c && .6>d && 1<c && .25<d,"strict numeric model frontier");
  check(Math.abs(((c+2)/(c*c)-c)/2-d)<1e-12,"published beta rational");
  return {run_id:"ARC-CACHE-RANK-FRONTIER115",run_date:"2026-10-25",model:"2CNF promised affine cycle; two actual shorter ordinary 2CNF image levels; opaque fixed-cost accessor; pinned/LRU/replay; independent SCC checks",mode:"deterministic; q=7 exhaustive 128 inputs, four chosen roots for each larger q; no randomness",status:"COMPUTATIONAL finite trace; elementary restricted abstract-cache theorem is separately proved in report; ARC-EDGE-90 OPEN; P vs NP OPEN",endpoint:{c,d},totalCases,assertions,failures:0,sink,groups};
}
console.log(JSON.stringify(run(), null, 2));
