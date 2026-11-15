'use strict';
function audit() {
  'use strict';
  let assertions=0, comparisons=0, matching=0, maxEasy=0, numeric=[];
  const ck=(p,m)=>{assertions++;if(!p)throw new Error(m)};
  const n=4,N=1<<n,mask=(1n<<BigInt(N))-1n;
  const bases=[0n,mask];
  for(let k=0;k<n;k++){let b=0n;for(let i=0;i<N;i++)if((i>>k)&1)b|=1n<<BigInt(i);bases.push(b)}
  function oneGate(xs){const y=new Set();for(const x of xs)y.add(mask^x);for(const x of xs)for(const z of xs){y.add(x&z);y.add(x|z)}return y}
  const yes=new Set(bases),one=oneGate(bases);
  for(const x of one)yes.add(x);
  for(const g of one)for(const x of oneGate(bases.concat([g])))yes.add(x);
  ck(yes.size===90,`exact two-gate count ${yes.size}`);
  let rmasks=[];
  for(let a=0;a<N;a++)for(let b=a+1;b<N;b++)for(let c=b+1;c<N;c++)for(let d=c+1;d<N;d++)
    rmasks.push((1n<<BigInt(a))|(1n<<BigInt(b))|(1n<<BigInt(c))|(1n<<BigInt(d)));
  ck(rmasks.length===1820,'sparse support combinations');
  function choose(a,b){let p=1;for(let i=1;i<=b;i++)p=p*(a-i+1)/i;return Math.round(p)}
  const entries=[...yes];
  for(let j=0;j<entries.length;j++){
    const x=entries[j];let easy=0;
    for(const flip of rmasks){if(yes.has(x^flip))easy++;comparisons++}
    maxEasy=Math.max(maxEasy,easy);
    ck(easy<=yes.size,'easy neighbors <= yes set size');
    let chosen=[...Array(N).keys()];
    let seed=(0x9e3779b9^(j*2654435761))>>>0;
    for(let i=N-1;i>0;i--){seed=(Math.imul(seed,1664525)+1013904223)>>>0;const z=seed%(i+1);[chosen[i],chosen[z]]=[chosen[z],chosen[i]]}
    for(let q=0;q<=6;q++){
      let qmask=0n;for(let k=0;k<q;k++)qmask|=1n<<BigInt(chosen[k]);
      let misses=0;for(const flip of rmasks){if((flip&qmask)===0n)misses++;matching++}
      ck(misses===choose(N-q,4),`no-hit combinatorial count j=${j} q=${q}`);
    }
  }
  ck(maxEasy/1820<.05,'uniform sparse false-hard fraction');
  function logD(n,s){return Math.log2(s+1)+Math.log2(n+s+2)+s*(Math.log2(3)+2*Math.log2(n+s+2))}
  function logC(N,r){let z=0;for(let i=1;i<=r;i++)z+=Math.log2(N-r+i)-Math.log2(i);return z}
  for(const [n0,mu,K] of [[10,.25,8],[12,.5,8],[14,.6,8],[16,.5,8]]){
    const tableN=2**n0,s=Math.floor(tableN**mu),r=Math.ceil(K*s);
    ck(r<tableN,'r<N');
    ck(K>2*mu/(1-mu),'constant-factor sufficiency');
    const u=logD(n0,s),v=logC(tableN,r),margin=v-u;
    ck(margin>100,'substantial exponential small-circuit fraction');
    const delta=1/3,eps=Math.pow(2,-Math.min(margin,1000));
    const sourceReadLB=(1-2*delta-eps)*tableN/r;
    ck(sourceReadLB>0,'expected source-read bound');
    numeric.push({n:n0,mu,K,N:tableN,s,r,log2CircuitsUpper:+u.toFixed(3),log2SparseCount:+v.toFixed(3),
      log2HardFractionMargin:+margin.toFixed(3),expectedReadLower:+sourceReadLB.toFixed(3)});
  }
  return {status:'COMPUTATIONAL',engine:'V8-executed same function as Git-published standalone JS',
    circuitBasis:'free constants/wires; AND/OR fanin2, NOT unary; <=2 gates, n=4',
    smallYesTables:yes.size,rSparseSupports:rmasks.length,maxEasyRSparseNeighbors:maxEasy,
    maxEasyFraction:+(maxEasy/1820).toFixed(6),cylinderTests:entries.length*7,
    sparseComparisonChecks:comparisons,hypergeometricChecks:matching,
    numericalAsymptoticChecks:numeric,assertions,failures:0,
    note:'Finite gate enumeration and support counts; mathematical expected-query lower bound proved separately.'};
}
const result=audit();
if (typeof process!=='undefined' && process.stdout) process.stdout.write(JSON.stringify(result)+'\n');
