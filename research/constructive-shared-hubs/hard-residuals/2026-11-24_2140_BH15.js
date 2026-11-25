function runBH15(){
  const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const C=(v,s=[0,0,0])=>({v,s});
  const fano=lines.map(v=>C(v));
  const word=(w,n)=>Array.from({length:n},(_,i)=>(w>>i)&1);
  const literal=(c,x,i)=>x[c.v[i]]^c.s[i];
  const ok=(c,x)=>literal(c,x,0)!==literal(c,x,1)||literal(c,x,0)!==literal(c,x,2);
  const sat=(F,x)=>F.every(c=>ok(c,x));
  const res={assertions:0,sourceControls:0,sourceSAT:0,sourceUNSAT:0,baseWords:0,sourceWords:0,baseLiftChecks:0,physicalLifts:0,gadgetWords:0,closureScans:0,forcedPins:0,rootClosureChecks:0,guardedFanoChecks:0,guardedFanoRejects:0,budgetNeighborCounts:[],signNeighborCounts:[],maxCompiledVariables:0,maxCompiledClauses:0,smallExhaustiveBaseControls:0};
  const check=(b)=>{res.assertions++;if(!b)throw Error("assert "+res.assertions);};
  const R=(a,b,c)=>C([a,b,c],[1,0,0]);
  const base=(F,n)=>{
    const G=[C([2*n,2*n+1,2*n+2])];
    for(let x=0;x<n;x++)for(let i=0;i<3;i++)G.push(R(2*n+i,x,x+n));
    for(const c of F){let v=c.v.map((x,i)=>x+n*c.s[i]);let a=(v[0]+n)%(2*n);G.push(R(a,v[1],v[2]));}
    return {G,n:2*n+3};
  };
  const liftBase=(x,a)=>[...x,...x.map(b=>1-b),...a];
  function split(B){
    const G=[],dict=[],gads=[];
    let N=B.n;
    const alloc=()=>N++;
    const occ=Array.from({length:B.n},()=>[]);
    // All external occurrences are distinct leaves.
    for(const c of B.G){const v=c.v.map(x=>{let t=alloc();occ[x].push(t);dict.push([t,x]);return t;});G.push(C(v,c.s.slice()));}
    for(let x=0;x<B.n;x++){
      let prev=x;
      for(const t of occ[x]){
        const next=alloc(),g=[prev,next,t,alloc(),alloc(),alloc(),alloc()];
        // Fano minus line 012, switched by (0,0,0,1,1,1,1).
        for(const l of lines.slice(1))G.push(C(l.map(i=>g[i]),l.map(i=>+(i>=3))));
        gads.push({g,x});prev=next;
      }
    }
    return {G,N,dict,gads};
  }
  function lift(P,b){
    const x=Array(P.N).fill(0);b.forEach((v,i)=>x[i]=v);
    for(const [t,i] of P.dict)x[t]=b[i];
    for(const {g,x:i} of P.gads)for(const v of g)x[v]=b[i];
    return x;
  }
  function geometry(P){
    let deg=Array(P.N).fill(0),pairs=new Set();
    for(const c of P.G){check(new Set(c.v).size===3);for(const v of c.v)deg[v]++;
      for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=[c.v[i],c.v[j]].sort((a,b)=>a-b).join(",");check(!pairs.has(k));pairs.add(k);}
    }check(Math.max(...deg)<=4);
  }
  function close(F,n,pins=[]){
    const d=Array(n).fill(3);for(const [v,b] of pins)d[v]=1<<b;
    let change=true;while(change){change=false;res.closureScans++;
      for(const c of F){const m=[0,0,0];for(let w=0;w<8;w++){const b=word(w,3);if(!b.every((v,i)=>d[c.v[i]]&(1<<v)))continue;
          const t=b.map((v,i)=>v^c.s[i]);if(t[0]===t[1]&&t[1]===t[2])continue;
          for(let i=0;i<3;i++)m[i]|=1<<b[i];}
        if(m.some(v=>!v))return {bad:true,d};
        for(let i=0;i<3;i++)if(m[i]!==d[c.v[i]]){d[c.v[i]]=m[i];res.forcedPins++;change=true;}
      }
    }return {bad:false,d};
  }
  // Exhaust every equality gadget word, including both endpoint polarities.
  const eq=lines.slice(1).map(v=>C(v,v.map(i=>+(i>=3))));
  let es=0;for(let w=0;w<128;w++){let x=word(w,7);res.gadgetWords++;if(sat(eq,x)){es++;check(x[0]===x[1]&&x[1]===x[2]);}}
  check(es===10);check(sat(eq,Array(7).fill(0)));check(sat(eq,Array(7).fill(1)));
  const controls=[{F:fano,n:7,kind:"fano"}];
  for(let i=0;i<7;i++)for(let j=0;j<3;j++){const F=fano.map(c=>C(c.v.slice(),c.s.slice()));F[i].s[j]^=1;controls.push({F,n:7,kind:"sign"});}
  let seed=20815;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
  for(let k=0;k<30;k++){let n=3+k%2,F=[];for(let i=0;i<1+k%9;i++){let v=Array.from({length:n},(_,j)=>j);for(let j=n-1;j;j--){let t=rand()%(j+1);[v[j],v[t]]=[v[t],v[j]];}F.push(C(v.slice(0,3),word(rand()&7,3)));}controls.push({F,n,kind:"small"});}
  // Guaranteed opposite labels (all 4 distinct signed forbidden words on one plane).
  controls.push({F:[C([0,1,2]),C([0,1,2],[1,0,0]),C([0,1,2],[0,1,0]),C([0,1,2],[0,0,1])],n:3,kind:"small"});
  for(const {F,n,kind} of controls){
    const B=base(F,n),P=split(B);
    res.sourceControls++;res.maxCompiledVariables=Math.max(res.maxCompiledVariables,P.N);res.maxCompiledClauses=Math.max(res.maxCompiledClauses,P.G.length);
    geometry(P);
    const z=Array(P.N).fill(0);check(P.G.filter(c=>!ok(c,z)).length===1);check(!ok(P.G[0],z));
    check(sat(P.G.slice(1),z));
    const cl=close(P.G,P.N);check(!cl.bad&&cl.d.every(v=>v===3));res.rootClosureChecks++;
    let count=0;
    for(let w=0;w<(1<<n);w++){
      const x=word(w,n);const good=sat(F,x);res.sourceWords++;if(good)count++;
      for(let a=1;a<7;a++){const b=liftBase(x,word(a,3));check(sat(B.G,b)===good);res.baseLiftChecks++;
        if(good){const y=lift(P,b);check(sat(P.G,y));check(y.slice(0,n).every((v,i)=>v===x[i]));res.physicalLifts++;}}
    }
    if(n<=4){let bc=0;for(let w=0;w<(1<<B.n);w++){let b=word(w,B.n);res.baseWords++;if(sat(B.G,b)){bc++;check(sat(F,b.slice(0,n)));check(b.slice(n,2*n).every((v,i)=>v===1-b[i]));}}check(bc===6*count);res.smallExhaustiveBaseControls++;}
    if(kind==="fano")check(count===0);
    if(kind==="sign"){check(count===10);res.signNeighborCounts.push(count);}
    if(count)res.sourceSAT++;else res.sourceUNSAT++;
  }
  // DO01 single-budget neighbors: independently enumerate each one-sided relaxation,
  // use an actual supplied witness, switch all other clauses to the convexity R relation,
  // and compare every flip word with the original restored formula.
  for(let e=0;e<7;e++)for(let b=0;b<2;b++){
    const budget=x=>fano.every((c,i)=>i===e?(ok(c,x)||c.v.every(v=>x[v]===b)):ok(c,x));
    const models=[];for(let w=0;w<128;w++){let x=word(w,7);if(budget(x))models.push(x);}
    res.budgetNeighborCounts.push(models.length);check(models.length===5);
    for(const x of models){
      const shifted=fano.map(c=>C(c.v,c.v.map((v,i)=>c.s[i]^x[v])));
      check(!ok(shifted[e],Array(7).fill(0)));
      for(let i=0;i<7;i++)if(i!==e){let c=shifted[i],a=c.s.findIndex(v=>c.s.filter(t=>t===v).length===1);check(a>=0);let tail=[0,1,2].filter(j=>j!==a);let rr=R(c.v[a],c.v[tail[0]],c.v[tail[1]]);
        for(let w=0;w<8;w++){let y=Array(7).fill(0);c.v.forEach((v,j)=>y[v]=(w>>j)&1);check(ok(c,y)===ok(rr,y));}}
      for(let w=0;w<128;w++){let y=word(w,7);check(sat(shifted,y)===sat(fano,y.map((v,i)=>v^x[i])));}
      // Pin unequal two variables in the bad owner (six oriented choices).
      for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)for(let a=0;a<2;a++){
        let cl=close(shifted,7,[[lines[e][i],a],[lines[e][j],1-a]]);
        res.guardedFanoChecks++;if(cl.bad)res.guardedFanoRejects++;
      }
    }
  }
  return res;
}
console.log(JSON.stringify(runBH15(),null,2));
