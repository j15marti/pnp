"use strict";
function runMS16(){
  "use strict";
  const C={assertions:0,rankBuilds:0,reductions:0,xors:0,augmentations:0,exchangeScans:0,closureSweeps:0,pins:0,referenceWords:0,subsetChecks:0,lifts:0,coreNodes:0,peakOwners:0,psdMoments:0};
  const check=(v,msg)=>{C.assertions++;if(!v)throw Error(msg)};
  const bit=i=>1n<<BigInt(i);
  const parity=x=>{let t=0;while(x){x&=x-1n;t^=1}return t};
  const hi=x=>x.toString(2).length-1;
  // row-vector basis with a bit-mask or bit RHS transported along XORs
  function reduce(a,b,B){C.reductions++;for(const [p,r,s] of B){if(a&bit(p)){a^=r;b^=s;C.xors++}}return [a,b]}
  function add(B,a,b){[a,b]=reduce(a,b,B);if(!a)return {ok:!b,ind:false};B.push([hi(a),a,b]);B.sort((x,y)=>y[0]-x[0]);return {ok:true,ind:true}}
  function basis(rows){C.rankBuilds++;const B=[];for(const [a,b] of rows){if(!add(B,a,b).ok)return null}return B}
  const rank=rows=>basis(rows.map(a=>[a,0n])).length;
  function rowsB(B){return B.map(([,a,b])=>[a,b])}
  function canon(rows){const B=basis(rows);if(B===null)return null;for(let i=B.length-1;i>=0;i--)for(let j=0;j<i;j++)if(B[j][1]&bit(B[i][0])){B[j][1]^=B[i][1];B[j][2]^=B[i][2];C.xors++}return rowsB(B)}
  function solve(rows){const B=basis(rows);if(B===null)return null;let x=0n;for(let i=B.length-1;i>=0;i--){const [p,a,b]=B[i];if(parity(a&x)!==Number(b))x|=bit(p)}return x}
  const holds=(rows,x)=>rows.every(([a,b])=>parity(a&x)===Number(b));
  const legal=(E,x)=>E.every(e=>!holds(e.rows,x));
  function close(G,E){
    G=G.slice();
    while(true){C.closureSweeps++;const B=basis(G);if(B===null)return null;let A=[],pin=null,seen=new Set;
      for(const e of E){const r=canon(e.rows.map(([a,b])=>reduce(a,b,B)));if(r===null)continue;if(!r.length)return null;if(r.length===1){pin=[r[0][0],r[0][1]^1n];break}const key=r.map(([a,b])=>a+":"+b).join(";");if(!seen.has(key)){seen.add(key);A.push({id:e.id,rows:r})}}
      if(pin){G.push(pin);C.pins++;continue}return {G,E:A};
    }
  }
  // Multi-source shortest owner augmentation and final reachable core.
  function transversal(E,W){
    const P=basis(W.map(a=>[a,0n]));
    const U=E.map(e=>e.rows.map(([a])=>reduce(a,0n,P)[0]));
    const m=E.length, sel=Array(m).fill(-1);C.peakOwners=Math.max(C.peakOwners,m);
    while(true){
      const B=[];for(let i=0;i<m;i++)if(sel[i]>=0)check(add(B,U[i][sel[i]],bit(i)).ind,"dependent selected reps");
      const prev=Array(m).fill(-2),via=Array(m).fill(-1),q=[];
      for(let i=0;i<m;i++)if(sel[i]<0){prev[i]=-1;q.push(i)}
      let end=-1,last=-1;
      outer:for(let j=0;j<q.length;j++){const i=q[j];for(let k=0;k<U[i].length;k++){
        C.exchangeScans++;const [r,c]=reduce(U[i][k],0n,B);
        if(r){end=i;last=k;break outer}
        for(let l=0;l<m;l++)if((c&bit(l))&&prev[l]===-2){prev[l]=i;via[l]=k;q.push(l)}
      }}
      if(end<0){return {sel,core:q.slice().sort((a,b)=>a-b),U,def:sel.filter(k=>k<0).length}}
      sel[end]=last;while(prev[end]>=0){let p=prev[end];sel[p]=via[end];end=p}C.augmentations++;
    }
  }
  function extract(E,W){
    const t=transversal(E,W), S=new Set(t.core), K=t.core.map(i=>E[i]), outside=E.filter((_,i)=>!S.has(i));
    const CR=K.flatMap(e=>e.rows.map(r=>r[0]));
    const cRank=rank(W.concat(CR))-rank(W), allRank=rank(W.concat(E.flatMap(e=>e.rows.map(r=>r[0]))))-rank(W);
    check(t.def===K.length-cRank,"deficiency certificate");
    const u=transversal(outside,W.concat(CR));check(u.def===0,"outside transversal");
    check(allRank-cRank>=outside.length,"rank removed");
    const pins=outside.map((e,i)=>{const [a,b]=e.rows[u.sel[i]];return [a,b^1n]});
    const cb=[], R=basis(W.map(a=>[a,0n]));
    for(const a of CR)if(add(R,a,0n).ind)cb.push(a);
    check(cb.length===cRank,"core basis size");
    return {K,outside,pins,cb,cRank,allRank,t};
  }
  function bruteCore(E,W,X){
    const m=E.length;let d=-1,I=(1<<m)-1;const rW=rank(W);
    for(let mask=0;mask<(1<<m);mask++){C.subsetChecks++;let rows=W.slice(),s=0;for(let i=0;i<m;i++)if(mask&(1<<i)){s++;rows.push(...E[i].rows.map(r=>r[0]))}let v=s-(rank(rows)-rW);if(v>d){d=v;I=mask}else if(v===d)I&=mask}
    let actual=X.t.core.reduce((a,i)=>a|(1<<i),0);check(actual===I&&d===X.t.def,"minimum maximizer");
  }
  function coreSearch(K,G,cb,idx=0){
    C.coreNodes++;const Q=close(G,K);if(!Q)return null;
    if(!Q.E.length||idx===cb.length){const x=solve(Q.G);check(x!==null&&legal(K,x),"core search leaf");return x}
    const a=cb[idx], B=basis(Q.G);
    if(!reduce(a,0n,B)[0])return coreSearch(K,Q.G,cb,idx+1);
    for(const b of [0n,1n]){let x=coreSearch(K,Q.G.concat([[a,b]]),cb,idx+1);if(x!==null)return x}return null;
  }
  function lift(X,G,x,orig,OG){
    const P=X.cb.map(a=>[a,BigInt(parity(a&x))]);let y=solve(G.concat(P,X.pins));check(y!==null&&holds(G,y)&&holds(OG,y)&&legal(orig,y),"original lift");C.lifts++;return y
  }
  function setup(E,G,W){let Q=close(G,E);if(!Q)return null;let X=extract(Q.E,Q.G.map(r=>r[0]).concat(W));return {Q,X}}
  function query(set,ext,E,G){
    if(!set)return null;const {Q,X}=set;const H=Q.G.concat(ext);if(solve(H)===null)return null;
    const x=coreSearch(X.K,H,X.cb);return x===null?null:lift(X,H,x,E,G);
  }
  function reference(n,E,G,ext){for(let x=0n;x<bit(n);x++){C.referenceWords++;if(holds(G,x)&&holds(ext,x)&&legal(E,x))return x}return null}
  let state=20261124;const rnd=k=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%k};
  const randomRows=(n,k)=>Array.from({length:k},()=>[BigInt(rnd(1<<n)),BigInt(rnd(2))]);
  const event=(id,rows)=>({id,rows});
  let counts={randomSystems:0,randomQueries:0,randomSAT:0,randomUNSAT:0,closureRejected:0,coreChecks:0,properPeels:0,emptyCores:0,randomGuardedLifts:0};
  for(let t=0;t<180;t++){
    let n=3+rnd(5),m=1+rnd(9),q=rnd(3),G=randomRows(n,rnd(3)),W=Array.from({length:q},()=>BigInt(rnd(1<<n))),E=Array.from({length:m},(_,i)=>event(i,randomRows(n,1+rnd(4))));
    const S=setup(E,G,W);counts.randomSystems++;
    if(!S)counts.closureRejected++;else{bruteCore(S.Q.E,S.Q.G.map(r=>r[0]).concat(W),S.X);counts.coreChecks++;if(S.X.outside.length)counts.properPeels++;if(!S.X.K.length)counts.emptyCores++}
    for(let j=0;j<(1<<q);j++){
      const ext=W.map((a,i)=>[a,BigInt((j>>i)&1)]),x=query(S,ext,E,G),r=reference(n,E,G,ext);counts.randomQueries++;check((x!==null)===(r!==null),"random SAT/UNSAT mismatch");if(r===null)counts.randomUNSAT++;else{counts.randomSAT++;counts.randomGuardedLifts++}
      // Verify the universal completion property on every legal core word in this small fiber.
      if(S){for(let v=0n;v<bit(n);v++)if(holds(S.Q.G.concat(ext),v)&&legal(S.X.K,v))lift(S.X,S.Q.G.concat(ext),v,E,G)}
    }
  }
  // Affine line in the 3-bit gauge-shifted chart given its two endpoints.
  function line(id,a,b,forms){let rows=[];for(let u=1;u<8;u++)if(!parity(BigInt(u&(a^b)))){let r=0n;for(let j=0;j<3;j++)if(u&(1<<j))r^=forms[j];rows.push([r,BigInt(parity(BigInt(u&a)))])}return event(id,canon(rows))}
  // Exact PSD pair coefficients on the complete small core observation basis;
  // acquire only single-event values, then square their summed Walsh coefficients.
  function credit(X,G){
    const r=X.cb.length,M=1<<r,A=X.K.map(()=>Array(M).fill(0));
    for(let y=0;y<M;y++){const v=solve(G.concat(X.cb.map((a,i)=>[a,BigInt((y>>i)&1)])));check(v!==null,"core word consistent");X.K.forEach((e,i)=>A[i][y]=holds(e.rows,v)?1:0)}
    const F=A.map(a=>Array.from({length:M},(_,w)=>{C.psdMoments++;return a.reduce((s,v,y)=>s+v*(parity(BigInt(w&y))?-1:1),0)}));
    let edges=[];for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){let sq=0;for(let w=0;w<M;w++)sq+=(F[i][w]+F[j][w])**2;edges.push([i,j,sq-M*(F[i][0]+F[j][0])])}
    edges.sort((a,b)=>b[2]-a[2]);let p=F.map((_,i)=>i),find=i=>p[i]===i?i:find(p[i]);let num=2*M*M-2*M*F.reduce((s,v)=>s+v[0],0);const union=num;
    for(const [i,j,w] of edges){const a=find(i),b=find(j);if(a!==b&&w>0){p[a]=b;num+=w}}
    return {numerator:num,denominator:2*M*M,unionNumerator:union};
  }
  let scales=[];
  for(let h of [0,4,16,32,64]){
    let n=6+2*h,W=Array.from({length:h+3},(_,i)=>bit(h+3+i));
    let forms=[0,1,2].map(i=>bit(i)^W[i]);
    for(const sat of [true,false]){
      let pairs=sat?[[0,1],[0,2],[0,4],[1,2]]:[[0,1],[2,3],[4,6],[5,7]];
      let E=pairs.map(([a,b],i)=>line(i,a,b,forms));
      for(let i=0;i<h;i++)E.push(event(4+i,[[bit(3+i)^W[3+i],0n],[forms[i%3],0n]]));
      const S=setup(E,[],W);check(S!==null,"scale closure stagnant");check(S.X.K.length===4&&S.X.cRank===3&&S.X.outside.length===h&&S.X.t.def===1,"same core scaling");
      let cr=null;for(let j=0;j<4;j++){
        const ext=W.map((a,i)=>[a,BigInt((i+j)%3===0?1:0)]);
        const v=query(S,ext,E,[]);check((v!==null)===sat,"scale label");let c=credit(S.X,ext);check((c.numerator>0)===sat,"PSD control");if(cr)check(c.numerator===cr.numerator,"gauge constant");cr=c;
      }
      scales.push({halo:h,externalBits:W.length,fullPrivateRank:S.X.allRank,coreRank:S.X.cRank,retained:S.X.K.length,deficiency:S.X.t.def,peeled:S.X.outside.length,sat,credit:cr});
    }
  }
  // Deficiency-one core can be arbitrarily large, even though all-ones is legal.
  const hostile=[];
  for(const n of [4,8,16,32,64]){
    const E=Array.from({length:n},(_,i)=>event(i,[[bit(i),0n],[bit((i+1)%n),0n]]));
    E.push(event(n,[[bit(0),1n],[bit(1),1n]]));
    const S=setup(E,[],[]);check(S&&S.X.t.def===1&&S.X.K.length===n+1&&S.X.cRank===n,"large critical core");
    const x=bit(n)-1n-bit(0);check(legal(E,x),"hostile direct witness");hostile.push({n,owners:n+1,deficiency:1,coreRank:n});
  }
  return {seed:20261124,counts,scales,hostile,counters:C,limitations:"Small explicit affine rejection adapters; scoped local closure, complete tiny core rank enumeration, full-feature marginal PSD only on rank-three structured cores. No strict physical compiler, arbitrary factored predicates, all-portfolio closure, measured byte peak or CM."};
}
console.log(JSON.stringify(runMS16(), null, 2));
