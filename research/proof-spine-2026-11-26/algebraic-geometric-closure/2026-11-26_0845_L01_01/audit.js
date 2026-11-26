const result = (function audit(){
  let checks=0; const assert=(x,msg)=>{checks++;if(!x)throw Error(msg)};
  const un=(a,b)=>[...new Set([...a,...b])].sort((x,y)=>x-y), ix=(a,b)=>a.filter(x=>b.includes(x));
  function dag(){const g=[];const add=(op,a,b)=>{g.push({op,a,b});return g.length-1};const c=a=>add("c",a),x=a=>add("x",a),p=(a,b)=>add("+",a,b),m=(a,b)=>add("*",a,b);return {g,c,x,p,m}}
  function scope(g){const S=g.map(v=>v.op==="x"?[v.a]:v.op==="c"?[]:[]);g.forEach((v,i)=>{if(v.op==="+"||v.op==="*")S[i]=un(S[v.a],S[v.b])});return S}
  function frontier(g,r){const S=scope(g),B=g.map(()=>[]),live=new Set([r]);for(let i=r;i>=0;i--){if(!live.has(i))continue;let v=g[i];if(v.op==="+"||v.op==="*"){const I=v.op==="*"?ix(S[v.a],S[v.b]):[];for(const h of [v.a,v.b]){live.add(h);B[h]=un(B[h],un(ix(B[i],S[h]),I))}}}return {S,B,live,b:Math.max(...B.map(x=>x.length))}}
  function compile(g,r){
    const {S,B,live,b}=frontier(g,r);if(b>8)return {b,skipped:true};const d=dag(),T=[],memo=new Map(),xs=new Map(),cs=new Map();
    const C=k=>{if(!cs.has(k))cs.set(k,d.c(k));return cs.get(k)},X=k=>{if(!xs.has(k))xs.set(k,d.x(k));return xs.get(k)};
    const plus=(a,b)=>a===C(0)?b:b===C(0)?a:d.p(a,b), mul=(a,b)=>a===C(0)||b===C(0)?C(0):a===C(1)?b:b===C(1)?a:d.m(a,b);
    const lit=(v,w)=>w?X(v):plus(C(1),mul(C(-1),X(v)));
    const assign=(L,a)=>new Map(L.map((v,j)=>[v,(a>>j)&1]));
    function restrict(h,f){const K=B[h], key=h+":"+K.map(v=>f.has(v)?f.get(v):"*").join("");if(memo.has(key))return memo.get(key);
      let z=C(0);for(let q=0;q<2**K.length;q++){let a=assign(K,q),good=true;for(const v of K)if(f.has(v)&&f.get(v)!==a.get(v)){good=false;break}if(!good)continue;let t=T[h][q];for(const v of K)if(!f.has(v))t=mul(t,lit(v,a.get(v)));z=plus(z,t)}
      memo.set(key,z);return z}
    for(let i=0;i<=r;i++){if(!live.has(i))continue;const v=g[i],K=B[i];T[i]=[];
      for(let a=0;a<2**K.length;a++){const f=assign(K,a);let z;
        if(v.op==="c")z=C(v.a);else if(v.op==="x")z=f.has(v.a)?C(f.get(v.a)):X(v.a);
        else if(v.op==="+")z=plus(restrict(v.a,f),restrict(v.b,f));
        else{const I=ix(S[v.a],S[v.b]).filter(x=>!f.has(x));z=C(0);for(let q=0;q<2**I.length;q++){const ff=new Map([...f,...assign(I,q)]);let t=mul(restrict(v.a,ff),restrict(v.b,ff));for(const x of I)t=mul(t,lit(x,ff.get(x)));z=plus(z,t)}}T[i].push(z)}}
    return {g:d.g,r:T[r][0],b,entries:T.reduce((a,x)=>a+(x?.length||0),0)}
  }
  function ev(g,r,x,p){const a=[];for(let i=0;i<=r;i++){const v=g[i];let y=v.op==="x"?x[v.a]:v.op==="c"?v.a:v.op==="+"?a[v.a]+a[v.b]:a[v.a]*a[v.b];a[i]=(y%p+p)%p}return a[r]}
  function homogeneous(g,r,x,p,n){const A=[];for(let i=0;i<=r;i++){const v=g[i],z=Array(n+1).fill(0);if(v.op==="c")z[0]=(v.a%p+p)%p;else if(v.op==="x")z[1]=x[v.a]%p;else if(v.op==="+")for(let j=0;j<=n;j++)z[j]=(A[v.a][j]+A[v.b][j])%p;else for(let j=0;j<=n;j++)for(let k=0;k<=j;k++)z[j]=(z[j]+A[v.a][k]*A[v.b][j-k])%p;A[i]=z}return A[r][n]}
  const perms=a=>a.length?a.flatMap((v,i)=>perms(a.filter((_,j)=>j!==i)).map(w=>[v,...w])):[[]];
  function witness(n,hc){const edges=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(!hc||i!==j)edges.push([i,j]);const masks=[];for(const q of perms([...Array(n).keys()])){if(hc){let j=q[0],k=1;while(j!==0&&k<n){j=q[j];k++}if(k!==n||j!==0)continue}let m=0;for(let i=0;i<n;i++)m|=1<<edges.findIndex(e=>e[0]===i&&e[1]===q[i]);masks.push(m)}return {edges,masks}}
  function graphCircuit(n,hc,exact,square){const {edges,masks}=witness(n,hc),d=dag(),one=d.c(1),neg=d.c(-1),zero=d.c(0),X=edges.map((_,i)=>{let a=d.x(i);return square?d.m(a,a):a}),not=a=>d.p(one,d.m(neg,a));let r=exact?zero:one;for(const mask of masks){let t=one;X.forEach((a,i)=>{if((mask>>i)&1)t=d.m(t,a);else if(exact)t=d.m(t,not(a))});r=exact?d.p(r,t):d.m(r,not(t))}if(!exact)r=not(r);return {...d,r,edges,masks}}
  let seed=20261126;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
  const rows=[];let tests=0,degreeChecks=0,truthChecks=0,guardChecks=0;
  for(const [n,hc,exact,square] of [[3,true,false,true],[3,true,true,true],[4,true,true,true],[2,false,false,true],[3,false,true,true],[3,false,false,false],[4,true,false,false]]){
    const o=graphCircuit(n,hc,exact,square),m=o.edges.length,f=compile(o.g,o.r),row={n,kind:hc?"HC":"PM",exact,square,m,gates:o.g.length,width:f.b,compiled:f.skipped?null:f.g.length,entries:f.entries??null};
    const vals=[];for(let mask=0;mask<2**m;mask++){const x=Array.from({length:m},(_,j)=>(mask>>j)&1),y=Number(o.masks.some(w=>exact?w===mask:(w&mask)===w));assert(ev(o.g,o.r,x,101)===y,"truth");truthChecks++;vals.push(y)}
    if(!f.skipped)for(const p of [2,3,101])for(let j=0;j<5;j++){let x=Array.from({length:m},()=>rnd(p)),ref=0;for(let mask=0;mask<vals.length;mask++)if(vals[mask]){let z=1;for(let v=0;v<m;v++)z=z*((mask>>v)&1?x[v]:1-x[v])%p;ref=(ref+z)%p}ref=(ref+p)%p;assert(ev(f.g,f.r,x,p)===ref,"ML");tests++;let y=0;for(const w of o.masks){let z=1;for(let i=0;i<m;i++)if((w>>i)&1)z=z*x[i]%p;y=(y+z)%p}assert(homogeneous(f.g,f.r,x,p,n)===y,"minimum layer");degreeChecks++}
    if(!f.skipped){for(let u=0;u<Math.min(m,5);u++){for(let val=0;val<2;val++){const gg=o.g.map(v=>v.op==="x"&&v.a===u?{op:"c",a:val}:v),ff=compile(gg,o.r);if(ff.skipped)continue;const x=Array.from({length:m},()=>rnd(101));x[u]=val;assert(ev(ff.g,ff.r,x,101)===ev(f.g,f.r,x,101),"guard");guardChecks++}}}rows.push(row)
  }
  let randomChecks=0;for(let t=0;t<48;t++){const d=dag();for(let i=0;i<5;i++)d.x(i);d.c(-1);d.c(1);for(let i=0;i<16;i++){let a=rnd(d.g.length),b=rnd(d.g.length);(rnd(2)?d.p:d.m)(a,b)}const r=d.g.length-1,f=compile(d.g,r);for(const p of [2,3,101]){const x=Array.from({length:5},()=>rnd(p));let ref=0;for(let mask=0;mask<32;mask++){let v=Array.from({length:5},(_,j)=>(mask>>j)&1),z=ev(d.g,r,v,p);for(let j=0;j<5;j++)z=z*(v[j]?x[j]:1-x[j])%p;ref=(ref+z)%p}assert(ev(f.g,f.r,x,p)===(ref+p)%p,"random DAG");randomChecks++}}
  const scale=[];for(const m of [8,32,128,512]){const d=dag();let r=d.c(1);for(let i=0;i<m;i++){let x=d.x(i);r=d.m(r,d.m(x,x))}const f=compile(d.g,r);assert(f.b===1,"separated width");let x=Array.from({length:m},()=>rnd(101));let ref=x.reduce((a,b)=>a*b%101,1);assert(ev(f.g,f.r,x,101)===ref,"scale");const e=dag(),X=Array.from({length:m},(_,i)=>e.x(i));let q=e.c(1);for(const x of X)q=e.m(q,x);const mid=q;for(const x of X)q=e.m(q,x);const F=frontier(e.g,q);assert(F.B[mid].length===m,"cumulative overlap");scale.push({variables:m,globalCollisions:m,compiledWidth:f.b,compiledGates:f.g.length,sequentialRepeatWidth:F.b})}
  return {checks,truthChecks,interpolationChecks:tests,degreeChecks,guardChecks,randomChecks,rows,scale,seed:20261126}
})();
console.log(JSON.stringify(result,null,2));
