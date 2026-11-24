function runMS04(){
  const bit=i=>1n<<BigInt(i), unit=n=>Array.from({length:n},(_,i)=>bit(i));
  const parity=x=>{let y=0;while(x){x&=x-1n;y^=1}return y};
  let seed=0x2010430;const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};
  const zero=()=>({c:0,l:0n,t:[]});
  const val=(p,x)=>{let z=p.c^parity(p.l&x);for(const [a,b] of p.t)if((a&x)&&(b&x))z^=1;return z};
  const polar=(p,u,v)=>{let z=0;for(const [a,b] of p.t)z^=Number(Boolean(a&u)&&Boolean(b&v))^Number(Boolean(b&u)&&Boolean(a&v));return z};
  const proj=(p,u,B)=>{let r=0n;for(let i=0;i<B.length;i++)if(polar(p,u,B[i]))r|=bit(i);return r};
  function rowsBasis(rows){const b=[];for(let x of rows){for(const y of b){const h=y&-y;if(x&h)x^=y}if(x){const h=x&-x;for(let i=0;i<b.length;i++)if(b[i]&h)b[i]^=x;b.push(x)}}return b.sort((a,b)=>a===b?0:(a&-a)<(b&-b)?-1:1)}
  const combine=(mask,B)=>{let v=0n;for(let i=0;i<B.length;i++)if(mask&bit(i))v^=B[i];return v};
  function restrict(a,B,row,rhs){if(!row)return rhs?null:[a,B];let j=0;while(!(row&bit(j)))j++;const v=B[j];return [rhs?a^v:a,B.filter((_,i)=>i!==j).map((u,i)=>u^((row&bit(i<j?i:i+1))?v:0n))]}
  const rankOn=(p,B)=>rowsBasis(B.map(u=>proj(p,u,B))).length;
  function greedy(P,n){let B=unit(n),removed=[];while(true){let R=null;for(const p of P){const r=rowsBasis(B.map(u=>proj(p,u,B)));if(r.length){R=r;break}}if(!R)break;const old=B;let K=unit(B.length);for(const row of R){let L=0n;for(let i=0;i<K.length;i++)if(parity(K[i]&row))L|=bit(i);K=restrict(0n,K,L,0)[1]}B=K.map(k=>combine(k,old));removed.push(R.length)}
    const C=[];let R=rowsBasis(B);for(const u of unit(n)){const R2=rowsBasis([...R,u]);if(R2.length>R.length){C.push(u);R=R2}}
    if(C.length!==removed.reduce((a,b)=>a+b,0)||P.some(p=>rankOn(p,B)))throw Error("certificate");return {B,C,removed}}
  function gauss(p,a,B){let scale=1n;while(B.length){const z=B[B.length-1];B=B.slice(0,-1);const row=proj(p,z,B),rhs=val(p,a)^val(p,a^z);const q=restrict(a,B,row,rhs);if(!q)return 0n;[a,B]=q;scale*=2n}return val(p,a)?-scale:scale}
  function mass(P,f,n,g){let total=0n,live=0;for(let c=0;c<2**g.C.length;c++){let a=combine(BigInt(c),g.C),B=g.B.slice(),ok=true;for(const p of P){const rhs=val(p,a);let row=0n;for(let j=0;j<B.length;j++)if(val(p,a^B[j])^rhs)row|=bit(j);const q=restrict(a,B,row,rhs);if(!q){ok=false;break}[a,B]=q}if(ok){live++;total+=gauss(f,a,B)}}return {total,live}}
  function ref(P,f,n){let s=0n;for(let i=0;i<2**n;i++){const x=BigInt(i);if(P.every(p=>!val(p,x)))s+=val(f,x)?-1n:1n}return s}
  function randomP(n,density=3){const p={c:rnd(2),l:0n,t:[]};for(let i=0;i<n;i++){if(rnd(2))p.l|=bit(i);for(let j=i+1;j<n;j++)if(rnd(density)===0)p.t.push([bit(i),bit(j)])}return p}
  function allSpaces(n){const levels=[[[]]],seen=new Set([""]);for(let d=0;d<n;d++){const next=[];for(const B of levels[d])for(let i=1;i<2**n;i++){const R=rowsBasis([...B,BigInt(i)]);if(R.length!==d+1)continue;const key=R.join(",");if(!seen.has(key)){seen.add(key);next.push(R)}}levels.push(next)}return levels}
  const spaces={};for(let n=2;n<=5;n++)spaces[n]=allSpaces(n);
  let stats={seed:"0x2010430",systems:0,sat:0,unsat:0,phaseComparisons:0,optimalComparisons:0,tightApprox:0,strictCompression:0,cosets:0,liveCosets:0,scaling:[],mismatches:0,spaceCounts:Object.fromEntries(Object.entries(spaces).map(([n,L])=>[n,L.map(x=>x.length)]))};
  for(let t=0;t<240;t++){let n=2+rnd(5),P=Array.from({length:1+rnd(7)},()=>randomP(n));let g=greedy(P,n),m=mass(P,zero(),n,g);if(m.total!==ref(P,zero(),n))throw Error("count");stats.systems++;stats[m.total?"sat":"unsat"]++;stats.cosets+=2**g.C.length;stats.liveCosets+=m.live;if(g.C.length<P.length)stats.strictCompression++;
    if(n<=5){let opt=n;outer:for(let k=0;k<=n;k++)for(const B of spaces[n][n-k])if(P.every(p=>rankOn(p,B)===0)){opt=k;break outer}if(g.C.length<opt||g.C.length>2*opt)throw Error("approx");stats.optimalComparisons++;if(opt&&g.C.length===2*opt)stats.tightApprox++}
    for(let j=0;j<3;j++){let f=randomP(n,2);if(mass(P,f,n,g).total!==ref(P,f,n))throw Error("phase");stats.phaseComparisons++}
  }
  const term=(i,j,c=0)=>({c,l:0n,t:[[bit(i),bit(j)]]});
  // Independent nonlinear equations, no affine combinations. Triangle plus star.
  for(const h of [4,8,16,32,64,128]){const n=h+3;for(const sat of [true,false]){const P=[term(0,1,1),term(0,2,1),term(1,2,sat?1:0),...Array.from({length:h},(_,i)=>term(0,i+3,0))];const g=greedy(P,n),m=mass(P,zero(),n,g);if(m.total!==(sat?1n:0n))throw Error("scale");stats.scaling.push({h,n,q:P.length,backdoor:g.C.length,greedyRanks:g.removed,cosets:2**g.C.length,live:m.live,mass:m.total.toString()})}}
  // Noncoordinate dense shared linear factor: (x0+x1)(xi+xj), plus affine terms.
  for(let t=0;t<80;t++){const n=5,P=[];for(let j=2;j<n;j++){let p={c:rnd(2),l:BigInt(rnd(1<<n)),t:[[bit(0),bit(j)],[bit(1),bit(j)]]};P.push(p)}const g=greedy(P,n);if(g.C.length>2||mass(P,zero(),n,g).total!==ref(P,zero(),n))throw Error("dense");stats.denseShared=(stats.denseShared||0)+1}
  return stats;
}
console.log(JSON.stringify(runMS04(), null, 2));
