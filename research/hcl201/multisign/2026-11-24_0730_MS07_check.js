"use strict";
console.log(JSON.stringify((function experiment(){
  let seed=20261124;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  const zero=d=>Array(d).fill(0n),add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]),abs=x=>x<0n?-x:x;
  const tagvec=(t,q)=>Array.from({length:q},(_,i)=>BigInt((t>>i)&1));
  const row=(c,t=0,id=0)=>({c:c.map(BigInt),t,id});
  const eq=(a,b)=>a.every((v,i)=>v===b[i]);
  function basis(cols,d){
    let a=cols.filter(v=>v.some(x=>x!==0n)).map(v=>v.slice()),p=[];
    for(let i=0;i<d;i++){
      let j=a.findIndex(v=>v[i]!==0n);if(j<0)continue;
      [a[0],a[j]]=[a[j],a[0]];
      for(j=1;j<a.length;j++){
        while(a[j][i]!==0n){
          let q=a[0][i]/a[j][i];
          let v=a[0].map((x,k)=>x-q*a[j][k]);a[0]=a[j];a[j]=v;
        }
      }
      if(a[0][i]<0n)a[0]=a[0].map(x=>-x);
      p.push([i,a.shift()]);
    }return p;
  }
  function member(p,x){x=x.slice();for(const [i,v] of p){if(x[i]%v[i]!==0n)return false;let q=x[i]/v[i];x=x.map((a,j)=>a-q*v[j])}return x.every(v=>v===0n)}
  function info(B,d,q){
    let ref=zero(d+q),lo=zero(d),hi=zero(d),cols=[];
    for(let i=0;i<q;i++){let v=zero(d+q);v[d+i]=2n;cols.push(v)}
    for(const R of B){
      const v=R[0].c.concat(tagvec(R[0].t,q));ref=add(ref,v);
      for(let j=0;j<d;j++){lo[j]+=R.reduce((m,r)=>r.c[j]<m?r.c[j]:m,R[0].c[j]);hi[j]+=R.reduce((m,r)=>r.c[j]>m?r.c[j]:m,R[0].c[j])}
      for(const r of R.slice(1))cols.push(sub(r.c.concat(tagvec(r.t,q)),v))
    }
    return {ref,lo,hi,p:basis(cols,d+q)}
  }
  function possible(s,c,t,q,useLat=true){
    if(c.some((v,i)=>v<s.lo[i]||v>s.hi[i]))return false;
    return !useLat||member(s.p,sub(c.concat(tagvec(t,q)),s.ref))
  }
  function slack(B,K,U=K){let A=B.map(R=>R.slice());for(let i=0;i<K.length;i++){
    let rem=U[i],p=1n;while(rem>0n){let w=p<rem?p:rem;let v=zero(K.length);v[i]=w;A.push([row(zero(K.length),0,0),row(v,0,1)]);rem-=w;p*=2n}
  }return A}
  function solve(B,K,t,q,upper=false,prune=true,useLat=true){
    let d=K.length,orig=B.length,stats={checks:0,removed:0,trans:0,rangeReject:0,latReject:0,peak:1,retained:1,mid:0};
    // MS06 dual-gap row and slack closure with unit prices and all-ones.
    let A=B.map(R=>R.slice()),U=K.slice(),prices=Array.from({length:d},(_,i)=>zero(d).map((_,j)=>i===j?1n:0n)).concat([Array(d).fill(1n)]);
    const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0n);
    if(upper){
      let changed=true;while(changed){changed=false;for(const y of prices){
        let m=A.map(R=>R.reduce((v,r)=>dot(y,r.c)<v?dot(y,r.c):v,dot(y,R[0].c))),gap=dot(y,K)-m.reduce((s,v)=>s+v,0n);
        if(gap<0n)return {w:null,stats};
        for(let i=0;i<d;i++)if(y[i]&&gap/y[i]<U[i])U[i]=gap/y[i];
        A=A.map((R,b)=>{let T=R.filter(r=>dot(y,r.c)-m[b]<=gap);stats.removed+=R.length-T.length;if(T.length<R.length)changed=true;return T});
        if(A.some(R=>!R.length))return {w:null,stats}
      }}
      A=slack(A,K,U);
    }
    if(prune){
      let changed=true;while(changed){changed=false;
        stats.checks++;if(!possible(info(A,d,q),K,t,q,useLat))return {w:null,stats};
        const next=A.map((R,i)=>{
          let s=info(A.filter((_,j)=>j!==i),d,q);
          return R.filter(r=>{stats.checks++;let ok=possible(s,sub(K,r.c),t^r.t,q,useLat);if(!ok){stats.removed++;changed=true}return ok})
        });
        if(next.some(R=>!R.length))return {w:null,stats};A=next;
      }
    }
    let suffix=Array.from({length:A.length+1},(_,i)=>info(A.slice(i),d,q));
    let cur=new Map([["0",{c:zero(d),t:0,prev:null,r:null}]]);
    for(let i=0;i<A.length;i++){
      let nxt=new Map(),s=suffix[i+1];
      for(const a of cur.values())for(const r of A[i]){
        stats.trans++;let c=add(a.c,r.c),z=a.t^r.t,need=sub(K,c);
        if(!possible(s,need,t^z,q,false)){stats.rangeReject++;continue}
        if(useLat&&!possible(s,need,t^z,q,true)){stats.latReject++;continue}
        let key=c.join(",")+":"+z;if(!nxt.has(key))nxt.set(key,{c,t:z,prev:a,r});
      }
      cur=nxt;stats.peak=Math.max(stats.peak,cur.size);stats.retained+=cur.size;if(i+1===orig/2)stats.mid=cur.size;
      if(!cur.size)return {w:null,stats}
    }
    let a=cur.get(K.join(",")+":"+t);if(!a)return {w:null,stats};
    let w=[];while(a.prev){w.push(a.r);a=a.prev}w.reverse();return {w:w.slice(0,orig),stats};
  }
  function valid(w,K,t,upper){if(!w)return false;let s=zero(K.length),z=0;for(const r of w){s=add(s,r.c);z^=r.t}return z===t&&(upper?s.every((v,i)=>v<=K[i]):eq(s,K))}
  function brute(B,K,t,upper){let count=0,w=null;function rec(i,c,z,path){if(i===B.length){count++;if(z===t&&(upper?c.every((v,j)=>v<=K[j]):eq(c,K)))w=path.slice();return}for(const r of B[i])rec(i+1,add(c,r.c),z^r.t,path.concat([r]))}rec(0,zero(K.length),0,[]);return {count,w}}
  let totals={random:180,queries:0,sat:0,unsat:0,bruteTuples:0,pins:0,pinSat:0,pinUnsat:0,checks:0,removed:0,trans:0,rangeReject:0,latReject:0,peak:0,verified:0,disagreements:0},scaling=[];
  function check(B,K,t,q,upper,pin=false){
    let ref=brute(B,K,t,upper),ans=solve(B,K,t,q,upper);
    if(!!ref.w!==!!ans.w||(ans.w&&!valid(ans.w,K,t,upper)))throw Error("reference mismatch");
    totals.queries++;if(pin){totals.pins++;totals[ans.w?"pinSat":"pinUnsat"]++}else totals[ans.w?"sat":"unsat"]++;
    if(ans.w)totals.verified++;totals.bruteTuples+=ref.count;
    for(const k of ["checks","removed","trans","rangeReject","latReject"])totals[k]+=ans.stats[k];totals.peak=Math.max(totals.peak,ans.stats.peak);
  }
  for(let it=0;it<180;it++){
    let d=1+rand(3),q=rand(3),h=2+rand(5),upper=it%2===0;
    let B=Array.from({length:h},(_,i)=>Array.from({length:2+rand(3)},(_,j)=>row(Array.from({length:d},()=>rand(7)),rand(1<<q),j)));
    let chosen=B.map(R=>R[rand(R.length)]),K=chosen.reduce((s,r)=>add(s,r.c),zero(d)),t=chosen.reduce((s,r)=>s^r.t,0);
    if(it%3===1)K=K.map(v=>v? v-1n:0n);if(it%3===2){K=K.map(v=>v+BigInt(rand(3)));t=rand(1<<q)}
    check(B,K,t,q,upper);
    let i=rand(h);for(const r of B[i])check(B.map((R,j)=>i===j?[r]:R),K,t,q,upper,true)
  }
  let hostile=[4,4,5,7].map((v,i)=>[row([0,v],0,0),row([v,0],0,1)]);
  let hr=solve(hostile,[10n,10n],0,0);if(hr.w||hr.stats.removed!==0)throw Error("hostile");
  const P=1n<<100n,Q=P+1n;
  for(const h of [8,16,32,64]){
    let B=[];for(const m of [P,Q])for(let i=1;i<=h;i++){let w=m*BigInt(i);B.push([row([0n,w],0,0),row([w,0n],0,1)])}
    let total=B.reduce((s,R)=>s+R[0].c[1],0n),a=BigInt(h*(h+1)/4),target=P*a+Q*a;
    for(const sat of [true,false]){
      // UNSAT target has required Q-count residue a+1 but P-count -1 (mod Q).
      // choose P-count -1, Q-count a: positive target, outside allowed P-count.
      let k=sat?target:Q*a-P;
      let ans=solve(B,[k,total-k],0,0);
      if(!!ans.w!==sat||(ans.w&&!valid(ans.w,[k,total-k],0,false)))throw Error("scale");
      let base=null;if(h<=16){let z=solve(B,[k,total-k],0,0,false,false,false);if(!!z.w!==sat)throw Error("scale baseline");base=z.stats}
      scaling.push({h,blocks:2*h,sat,stats:ans.stats,rangeOnly:base})
    }
  }
  return {seed:20261124,totals,hostile:hr.stats,scaling,notes:"Exact BigInt; upper-budget slack via bounded binary chunks; equality and XOR decisions; suffix lattice membership via column Euclid, not polynomial-bit normal-form backend. Full intersection-basis bound not implemented. Pin queries and full tuple reference. No strict-source compiler."};
})(),null,2));
