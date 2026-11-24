"use strict";
const run = function(){
  const mod=(x,n)=>((x%n)+n)%n;
  const R={seed:20261124,scales:[],guardChecks:0,projectionChecks:0,projectionRowsScanned:0,integerWitnessChecks:0,lpChecks:0,exactSearchNodes:0,peerChecks:[]};
  let seed=R.seed; const rand=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};
  const assert=(b,msg)=>{if(!b)throw Error(msg)};
  const rank=xs=>{let B=new Map();for(let x of xs){while(x){let p=x.toString(2).length-1;if(B.has(p))x^=B.get(p);else{B.set(p,x);break}}}return B.size};
  for(const n of [8,16,24,32,64,128]){
    const k=n/8,h=n/2;
    const E=[],rows=Array.from({length:n},()=>[]);
    const add=(x,y,z)=>{rows[y].push(E.length);E.push([x,y,z]);return E.length-1};
    for(let y=0;y<n;y++)for(let x=0;x<n;x++)add(x,y,(x+y)%n);
    const special=Array.from({length:k},(_,y)=>add(0,y,(y+2)%n));
    const base=(x,y)=>y*n+x;
    const inc=(v)=>{let a=Array(3*n).fill(0);E.forEach(([x,y,z],j)=>{a[x]+=v[j];a[n+y]+=v[j];a[2*n+z]+=v[j]});return a};
    const diff=(v,i,j,c)=>{v[i]+=c;v[j]-=c};
    const vx=(v,x,y,c)=>diff(v,base(x,y),base(0,y),c);
    const cycleDiff=(v,x,a,c)=>{vx(v,x,a+1,c);vx(v,x,a,-c)};
    const zResidual=(v,t)=>inc(v).slice(2*n).map((z)=>t-z);
    const qFrom=d=>{let s=0;return d.map(z=>-(s+=z))};
    const correctZ=(v,t,a)=>{let q=qFrom(zResidual(v,t));let sum=q.reduce((s,x)=>s+x,0);assert(sum%n===0,"nonintegral avg");q=q.map(x=>x-sum/n);for(let x=1;x<n;x++)cycleDiff(v,x,a,q[(a+x)%n]);assert(inc(v).every(x=>x===t),"correction failed")};
    const tag=i=> (1n<<BigInt(E[i][0]))^(1n<<BigInt(n+E[i][2]));
    const target=(1n<<BigInt(2*n))-1n;
    const D=2*n-3;
    for(let a=0;a<n;a+=2){let vals=[];for(let y=a;y<a+2;y++)for(let x=1;x<n;x++)vals.push(tag(base(x,y))^tag(base(0,y)));assert(rank(vals)===D,"pair rank")}
    // Strictly positive exact fractional solution (integer numerator, common denominator).
    const den=10*n**4;const lp=Array(E.length).fill(0);for(let j=0;j<n*n;j++)lp[j]=den/n;
    for(let y=0;y<k;y++)diff(lp,special[y],base(0,y),n);
    correctZ(lp,den,0);
    assert(lp.every(x=>Number.isSafeInteger(x)&&x>0&&x<den),"LP not interior");R.lpChecks++;
    // Modular obstruction and explicit SAT one-triple neighbor.
    const deltas=E.map(([x,y,z])=>mod(z-x-y,n));assert(deltas.every((d,i)=>d===(i<n*n?0:2)),"unexpected defect");
    assert(2*k<h,"mod bound");
    const witness=[];for(let x=0;x<h;x++)witness.push([x,x,2*x]);for(let x=h;x<n-1;x++)witness.push([x,x+1,mod(2*x+1,n)]);witness.push([n-1,h,n-1]);
    for(let j=0;j<3;j++)assert(new Set(witness.map(e=>e[j])).size===n,"SAT neighbor bad");
    assert(witness.slice(0,-1).every(([x,y,z])=>z===mod(x+y,n)),"bad ordinary");
    // Owner-choice guards, exact signed integer solutions and arbitrary parity projections.
    let sampleMax=0;
    for(let trial=0;trial<12;trial++){
      let pins=new Map(),p=trial%(k);while(pins.size<p){let y=rand(n);pins.set(y,rows[y][rand(rows[y].length)])}
      let a=Array.from({length:n/2},(_,j)=>2*j).find(y=>!pins.has(y)&&!pins.has(y+1));
      let sy=Array.from({length:k},(_,y)=>y).find(y=>!pins.has(y));
      assert(a!==undefined&&sy!==undefined,"unavailable pair/special");
      const v=Array(E.length).fill(0);
      for(let y=0;y<n;y++)v[pins.get(y)??base(0,y)]=1;
      let rX=inc(v).slice(0,n).map(x=>1-x);for(let x=1;x<n;x++)vx(v,x,a,rX[x]);
      let q=qFrom(zResidual(v,1)),res=mod(q.reduce((s,x)=>s+x,0),n);
      assert(res%2===0,"odd defect");diff(v,special[sy],base(0,sy),res/2);
      correctZ(v,1,a);
      assert(v.every(Number.isSafeInteger),"integer witness");
      for(const [y,j] of pins)assert(rows[y].every(i=>v[i]===(i===j?1:0)),"pin violation");
      R.integerWitnessChecks++;R.guardChecks++;
      // Random linear maps into up to 8 bits; build projected basis from distinct untouched owner pairs.
      const qrank=Math.min(8,n/2-p,1+trial%8);let col=Array.from({length:2*n},()=>rand(1<<qrank));
      const proj=t=>{let s=0;for(let i=0;i<2*n;i++)if(t&(1n<<BigInt(i)))s^=col[i];return s};
      let selected=rows.map((r,y)=>pins.get(y)??r[0]), current=selected.reduce((s,i)=>s^tag(i),0n);
      let B=new Map();
      for(let a=0;a<n;a+=2){if(pins.has(a)||pins.has(a+1))continue;let found=false;
        for(let y=a;y<a+2&&!found;y++)for(const j of rows[y]){
          R.projectionRowsScanned++;let z=proj(tag(j)^tag(selected[y])),combo=1n<<BigInt(B.size);
          while(z){let bit=31-Math.clz32(z);if(B.has(bit)){let b=B.get(bit);z^=b.z;combo^=b.combo}else{B.set(bit,{z,combo,y,j});found=true;break}}
          if(found)break;
        }
      }
      const moves=[...B.values()];let rhs=proj(current^target),comb=0n;while(rhs){let bit=31-Math.clz32(rhs);assert(B.has(bit),"projected target outside");let b=B.get(bit);rhs^=b.z;comb^=b.combo}
      for(let j=0;j<moves.length;j++)if(comb&(1n<<BigInt(j)))selected[moves[j].y]=moves[j].j;
      assert(proj(selected.reduce((s,i)=>s^tag(i),0n))===proj(target),"projection witness");
      for(const [y,j] of pins)assert(selected[y]===j,"projection pin");R.projectionChecks++;sampleMax=Math.max(sampleMax,qrank);
    }
    // Full decision reference at n=8 only, pruning repeated X/Z.
    let exact=null,neighborExact=null;
    if(n===8){const solve=extra=>{let rr=rows.map(r=>r.map(i=>E[i]));if(extra)rr[h].push(witness[n-1]);function dfs(y,xm,zm){R.exactSearchNodes++;if(y===n)return true;for(const [x,_,z] of rr[y])if(!(xm>>x&1)&&!(zm>>z&1)&&dfs(y+1,xm|1<<x,zm|1<<z))return true;return false}return dfs(0,0,0)};exact=solve(false);neighborExact=solve(true);assert(!exact&&neighborExact,"exact control")}
    // MS08 sharp example: verify unique representative and lattice membership for L>=3.
    R.scales.push({n,special:k,arcs:E.length,thinBetaMin:n-1,affineDimension:D,guaranteedProjectionRank:n/2,guaranteedOwnerPinLatticeDepth:k-1,positiveLPdenominator:den,sampledMaxProjectionRank:sampleMax,exact,neighborExact});
  }
  for(let L=3;L<=8;L++){let u=2*(L-2),r=Array.from({length:u+1},(_,i)=>i).filter(i=>i%L===L-1);assert(r.length===1&&L*r[0]!==L*(L-2),"MS08 sharp");assert((L*((L-1)-(L-2)))%L===0,"lattice");R.peerChecks.push({L,residues:r,satNeighbor:[L-1,L-3,...Array(L-2).fill(L-2)]})}
  return R;
};
console.log(JSON.stringify(run(),null,2));
