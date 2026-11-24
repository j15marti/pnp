"use strict";
function main(){
  const C={guardCases:0,sat:0,unsat:0,bruteChecks:0,bruteNodes:0,dpChecks:0,dpArcTests:0,witnessChecks:0,compiledGuards:0,compiledRows:0,closurePasses:0,closureGuardChecks:0,forced:0,merges:0,branchNodes:0,parallelTests:0};
  let seed=208031;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
  const rr=rows=>{let a=rows.map(r=>r.slice()),j=0;for(let bit=0;bit<20;bit++){let k=a.findIndex((r,i)=>i>=j&&(r[0]&(1<<bit)));if(k<0)continue;[a[j],a[k]]=[a[k],a[j]];for(let i=0;i<a.length;i++)if(i!==j&&(a[i][0]&(1<<bit))){a[i][0]^=a[j][0];a[i][1]^=a[j][1]}j++}return a.some(r=>r[0]===0&&r[1])?null:a.slice(0,j)};
  const holds=(g,x)=>g!==null&&g.every(([m,b])=>parity(m&x)===b);
  const constant=c=>[[-0,c&1],[0,c>>1]];
  const hub=(i,s=0)=>[[1<<(2*i),s&1],[1<<(2*i+1),s>>1]];
  const bool=(i,s=0)=>[[1<<i,s&1],[0,s>>1]];
  const val=(e,x)=>e.reduce((a,[m,b],i)=>a|((parity(m&x)^b)<<i),0);
  const X=(a,b)=>[a[0]^b[0],a[1]^b[1]];
  const compile=(A,B,S)=>{
    let k=S.length,H=S.reduce((a,b)=>a^b,0),out=[];
    for(let p=0;p<4;p++)for(let q=p+1;q<4;q++){
      let d=p^q;if(H!==0&&H!==d)continue;if(H===((k%2)?d:0))continue;
      let normal=[1,2,3].find(v=>parity(v&d)===0),prefix=0,rows=[];
      for(let i=0;i<k;i++){
        for(let t=0;t<2;t++){let z=X(A[i][t],B[i][t]);rows.push([z[0],z[1]^((d>>t)&1)])}
        let z=[0,0];for(let t=0;t<2;t++)if(normal&(1<<t))z=X(z,A[i][t]);
        rows.push([z[0],z[1]^parity(normal&(p^prefix))]);prefix^=S[i];
      }
      let g=rr(rows);if(g!==null){out.push(g);C.compiledGuards++;C.compiledRows+=g.length}
    }return out
  };
  const lists=(A,B,x)=>A.map((a,i)=>[0,1,2,3].filter(c=>c!==val(a,x)&&c!==val(B[i],x)));
  const witness=(L,S,w)=>w!==null&&w.every((v,i)=>L[i].includes(v)&&w[(i+1)%w.length]!==(v^S[i]));
  function dp(L,S){
    C.dpChecks++;let k=L.length;
    for(const start of L[0]){
      let prev=new Set([start]),parents=[null];
      for(let i=1;i<k;i++){let p=new Map();for(const v of L[i])for(const u of prev){C.dpArcTests++;if(v!==(u^S[i-1])){p.set(v,u);break}}parents.push(p);prev=new Set(p.keys())}
      for(const end of prev){C.dpArcTests++;if(start===(end^S[k-1]))continue;let w=Array(k);w[k-1]=end;for(let i=k-1;i>0;i--)w[i-1]=parents[i].get(w[i]);return w}
    }return null;
  }
  function brute(L,S){C.bruteChecks++;let w=[];function go(i){C.bruteNodes++;if(i===L.length)return w[0]!==(w[i-1]^S[i-1]);for(const v of L[i])if(!i||v!==(w[i-1]^S[i-1])){w.push(v);if(go(i+1))return true;w.pop()}return false}return go(0)}
  function check(A,B,S,x,G,ref=true){C.guardCases++;let L=lists(A,B,x),w=dp(L,S),reject=G.some(g=>holds(g,x));if(reject===(w!==null))throw Error("guard/dp disagreement");if(ref&&brute(L,S)!==(w!==null))throw Error("brute disagreement");if(w){if(!witness(L,S,w))throw Error("bad lift");C.sat++;C.witnessChecks++}else C.unsat++;return w!==null}
  // Enumerate every constant forbidden-pair profile (including equal spokes) for 3 rims,
  // all 4 final twists; initial two edge labels zero without loss for these profiles.
  for(let a=0;a<16;a++)for(let b=0;b<16;b++)for(let c=0;c<16;c++)for(let h=0;h<4;h++){
    let p=[a,b,c],A=p.map(v=>constant(v&3)),B=p.map(v=>constant(v>>2)),S=[0,0,h];check(A,B,S,0,compile(A,B,S));
  }
  // Arbitrary signed, correlated hubs; every assignment of three two-bit hubs.
  for(let t=0;t<150;t++){let k=3+(t%5),A=[],B=[],S=[];for(let i=0;i<k;i++){A.push(hub(rnd(3),rnd(4)));B.push(hub(rnd(3),rnd(4)));S.push(rnd(4))}let G=compile(A,B,S);for(let x=0;x<64;x++)check(A,B,S,x,G)}
  // Signed odd-wheel equality: two shared tips, constant rim shift zero, arbitrary spoke shift.
  let equality=[];
  for(let k of [3,5,31,257,4097]){let A=Array(k).fill(hub(0)),B=Array(k).fill(hub(1,2)),S=Array(k).fill(0),G=compile(A,B,S),ok=0;for(let x=0;x<16;x++){let sat=check(A,B,S,x,G,k<=5);if(sat!==((x&3)===((x>>2)^2)))throw Error("equality");ok+=sat}equality.push({rim:k,guards:G.length,accepted:ok})}
  function merge(a,b){if(a.length!==b.length||a.some((r,i)=>r[0]!==b[i][0]))return undefined;let p=a.findIndex((r,i)=>r[1]!==b[i][1]);if(p<0)return a;return rr(a.flatMap((r,i)=>i===p?[]:[r[1]===b[i][1]?r:X(r,a[p])]))}
  for(let i=0;i<400;i++){let masks=rr(Array.from({length:1+rnd(4)},()=>[1+rnd(15),0]));let x=rnd(16),y=rnd(16),a=masks.map(([m])=>[m,parity(m&x)]),b=masks.map(([m])=>[m,parity(m&y)]),u=merge(a,b);if(!u)throw Error("parallel merge");for(let z=0;z<16;z++){C.parallelTests++;if(holds(u,z)!==(holds(a,z)||holds(b,z)))throw Error("union")}}
  function residual(g,K){let out=[];for(let r of g){r=r.slice();for(const k of K){let pivot=k[0]&-k[0];if(r[0]&pivot)r=X(r,k)}out.push(r)}return rr(out)}
  function close(G,K){for(;;){C.closurePasses++;let H=[];for(const g of G){C.closureGuardChecks++;let r=residual(g,K);if(r===null)continue;if(!r.length)return null;H.push(r)}
      let changed=true;while(changed){changed=false;outer:for(let i=0;i<H.length;i++)for(let j=i+1;j<H.length;j++){let u=merge(H[i],H[j]);if(u!==undefined){C.merges++;H.splice(j,1);H[i]=u;changed=true;break outer}}}
      if(H.some(g=>!g.length))return null;let u=H.find(g=>g.length===1);if(!u)return {G:H,K};C.forced++;K=rr(K.concat([[u[0][0],u[0][1]^1]]));if(K===null)return null;G=H;
    }}
  function solve(G,K,n){C.branchNodes++;let z=close(G,K);if(!z)return [];if(z.K.length===n){let x=0;for(const [m,b] of z.K)if(b)x|=m;return [x]}
    let p=0;while(z.K.some(r=>(r[0]&-r[0])===(1<<p)))p++;
    // Branch only after certified closure at stagnation, keep full guard context.
    return [0,1].flatMap(b=>solve(z.G,rr(z.K.concat([[1<<p,b]])),n))
  }
  // Monotone NAE owners: two opposite signed wheels per triple. Remove one owner.
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const owners=fano.flatMap(v=>[0,1].map(s=>({v,s})));
  let fanoResults=[];
  for(let deleted=-1;deleted<14;deleted++){
    let active=owners.filter((_,i)=>i!==deleted),G=active.flatMap(({v,s})=>compile(v.map(()=>constant(0)),v.map(i=>bool(i,s)),[0,0,0]));
    let models=solve(G,[],7).sort((a,b)=>a-b),ref=[];for(let x=0;x<128;x++)if(active.every(({v,s})=>v.some(i=>(((x>>i)&1)^s)===0)))ref.push(x);
    if(JSON.stringify(models)!==JSON.stringify(ref))throw Error("Fano source mismatch");
    for(const x of models)for(const {v,s} of active){let A=v.map(()=>constant(0)),B=v.map(i=>bool(i,s));let L=lists(A,B,x),w=dp(L,[0,0,0]);if(!witness(L,[0,0,0],w))throw Error("Fano lift");C.witnessChecks++}
    fanoResults.push({deleted,models:models.length});
  }
  // Explicit hostile cancellation: three pairwise nonparallel lines cover F2^2.
  let hostile=[[[1,0]],[[2,0]],[[3,0]]];if(![0,1,2,3].every(x=>hostile.some(g=>holds(g,x))))throw Error("hostile");
  return {seed:208031,counts:C,equality,fanoResults,hostile:"three nonparallel lines cover all four words; pair-parallel merge alone stalls",discrepancies:0};
}
console.log(JSON.stringify(main(),null,2));
