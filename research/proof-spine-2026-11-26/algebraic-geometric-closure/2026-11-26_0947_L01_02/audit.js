// L01-02 deterministic standalone JS; run node audit.js.
function audit(){
  let checks=0;
  const check=(x,msg)=>{checks++;if(!x)throw Error(msg)};
  const pop=x=>{let r=0;while(x){x&=x-1;r++}return r};
  const rows=(n,edges)=>{const a=Array.from({length:n},()=>[]);for(const [i,j] of edges)a[i].push(j);return a};
  const edgesOf=a=>a.flatMap((r,i)=>r.map(j=>[i,j]));
  const permute=(n,fn)=>{const p=[],used=Array(n).fill(false);function rec(){if(p.length===n){fn(p.slice());return}for(let j=0;j<n;j++)if(!used[j]){used[j]=true;p.push(j);rec();p.pop();used[j]=false}}rec()};
  const cycle=p=>{let u=0,k=0;do{u=p[u];k++}while(u!==0&&k<=p.length);return u===0&&k===p.length};
  // Sound unary row/column closure. Original row/col IDs preserved.
  function close(input){
    const a=input.map(r=>r.slice());let changed=true;
    while(changed){
      changed=false;
      const inr=Array.from({length:a.length},()=>[]);
      for(let i=0;i<a.length;i++){if(!a[i].length)return null;for(const j of a[i])inr[j].push(i)}
      if(inr.some(r=>!r.length))return null;
      for(let i=0;i<a.length;i++)if(a[i].length===1){
        const j=a[i][0];for(const k of inr[j])if(k!==i&&a[k].includes(j)){a[k]=a[k].filter(t=>t!==j);changed=true}
      }
      if(a.some(r=>!r.length))return null;
      // Recompute incoming lists before column forcing.
      const b=Array.from({length:a.length},()=>[]);
      for(let i=0;i<a.length;i++)for(const j of a[i])b[j].push(i);
      for(let j=0;j<a.length;j++){
        if(!b[j].length)return null;
        if(b[j].length===1){const i=b[j][0];if(!a[i].includes(j))return null;if(a[i].length!==1){a[i]=[j];changed=true}}
      }
    }
    return a;
  }
  function witnesses(input,hc){
    const a=close(input);if(!a)return [];
    const p=Array(a.length).fill(-1), used=Array(a.length).fill(false), free=[];
    for(let i=0;i<a.length;i++)if(a[i].length===1){const j=a[i][0];if(used[j])return [];used[j]=true;p[i]=j}else free.push(i);
    const out=[];
    function rec(k){
      if(k===free.length){if(!hc||cycle(p))out.push(p.slice());return}
      const i=free[k];for(const j of a[i])if(!used[j]){p[i]=j;used[j]=true;rec(k+1);used[j]=false;p[i]=-1}
    }
    rec(0);return out;
  }
  function upper(a,hc,C=1){
    const n=a.length,lim=BigInt(n)**BigInt(C),inc=Array(n).fill(0);
    let q=1n;for(const r of a){if(!r.length)return false;for(const j of r)inc[j]++;q*=BigInt(r.length);if(q>lim)q=lim+1n}
    if(inc.some(d=>!d))return false;
    return q>lim||witnesses(a,hc).length>0;
  }
  // Exact coefficient on the entire edge set of input. Forced singleton rows factored.
  function coeff(a,hc){
    if(a.some(r=>!r.length))return 0;
    const W=witnesses(a,hc);if(!W.length)return 0;
    const idx=a.map(r=>new Map());let t=0;
    for(let i=0;i<a.length;i++)if(a[i].length>1)for(const j of a[i])idx[i].set(j,t++);
    if(t>20)throw Error("audit coefficient cap");
    const f=new Int32Array(1<<t);let union=0;
    for(const p of W){let mask=0;for(let i=0;i<a.length;i++)if(idx[i].has(p[i]))mask|=1<<idx[i].get(p[i]);f[mask]++;union|=mask}
    if(union!==(1<<t)-1)return 0; // any unsupported edge gives zero coefficient
    for(let i=0;i<t;i++)for(let m=0;m<f.length;m++)if(m&(1<<i))f[m]+=f[m^(1<<i)];
    let ans=0;for(let m=0;m<f.length;m++)if(f[m])ans+=((t-pop(m))&1)?-1:1;return ans;
  }
  // Independent global exhaustive truth table + full Boolean Moebius transform.
  const small=[];
  for(const [n,hc] of [[3,true],[4,true],[2,false],[3,false]]){
    const E=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(!hc||i!==j)E.push([i,j]);
    const index=new Map(E.map(([i,j],k)=>[i*n+j,k]));
    const wm=[];permute(n,p=>{if(hc&&!cycle(p))return;let m=0;for(let i=0;i<n;i++)m|=1<<index.get(i*n+p[i]);wm.push(m)});
    const size=1<<E.length,truth=Array(size),cnt=Array(size),u=Array(size);
    for(let m=0;m<size;m++){cnt[m]=wm.filter(w=>(w&m)===w).length;truth[m]=Number(cnt[m]>0)}
    const mob=truth.slice();for(let i=0;i<E.length;i++)for(let m=0;m<size;m++)if(m&(1<<i))mob[m]-=mob[m^(1<<i)];
    let layer=0,fp=0,nonminimal=0;
    for(let m=0;m<size;m++){
      const a=rows(n,E.filter((_,j)=>m&(1<<j))),v=witnesses(a,hc);
      check(v.length===cnt[m],"count");for(const p of v)check(new Set(p).size===n&&(!hc||cycle(p))&&p.every((j,i)=>a[i].includes(j)),"witness");
      const c=coeff(a,hc);check(c===mob[m],"coefficient");
      for(const q of [2,3,101])check((c-mob[m])%q===0,"field");
      u[m]=upper(a,hc);check(!truth[m]||u[m],"upper");
      if(pop(m)<=n+Math.floor(Math.log2(n))){layer++;check(u[m]===!!truth[m],"layer")}
      if(u[m]&&!truth[m])fp++;
      if(pop(m)>n&&c!==0)nonminimal++;
    }
    for(let m=0;m<size;m++)for(let i=0;i<E.length;i++)if(!(m&(1<<i)))check(!u[m]||u[m|(1<<i)],"monotonic");
    small.push({n,hc,graphs:size,layer,fp,nonminimal});
  }
  // Two internal paths per 4-vertex block; link through padding.
  function blocks(n,r){
    if(n<4*r||!r)throw Error("size");
    const E=[],p=Array(n),q=Array(n);
    for(let i=0;i<r;i++){const a=4*i,b=a+1,c=a+2,d=a+3,next=i===r-1?(4*r<n?4*r:0):a+4;
      E.push([a,b],[b,c],[c,d],[a,c],[c,b],[b,d],[d,next]);
      p[a]=b;p[b]=c;p[c]=d;p[d]=next;q[a]=c;q[c]=b;q[b]=d;q[d]=next;
    }
    for(let i=4*r;i<n;i++){const j=(i+1)%n;E.push([i,j]);p[i]=q[i]=j}
    return {a:rows(n,E),p,q};
  }
  const scales=[];
  for(const n of [32,64,128,256,512,1024]){
    const r=Math.max(1,Math.floor(Math.log2(n)/3)),{a,p,q}=blocks(n,r),w=witnesses(a,true);
    check(w.length===2**r,"block count");check(cycle(p)&&cycle(q),"block lifts");
    check(upper(a,true),"block upper");
    const c=coeff(a,true);check(c===(-1)**r,"block union coefficient");
    // Strongly connected star, with a subdivided outgoing arc; one added arc yields HC.
    const e=[[0,3],[1,0],[0,2],[2,0]];
    for(let i=3;i<n;i++)e.push([i,i+1<n?i+1:1]);
    const no=rows(n,e),yes=rows(n,e.concat([[1,2]]));
    check(witnesses(no,true).length===0,"neighbor NO");
    const wy=witnesses(yes,true);check(wy.length===1&&cycle(wy[0]),"neighbor YES");
    check(!upper(no,true)&&upper(yes,true),"neighbor upper");
    scales.push({n,r,arcs:edgesOf(a).length,witnesses:w.length,coefficient:c,neighborArcs:[e.length,e.length+1]});
  }
  const hostile=[];
  for(const n of [32,128,512,2048]){
    const r=n/4,{a,p,q}=blocks(n,r);check(cycle(p)&&cycle(q),"large lifts");
    check(p.every((j,i)=>a[i].includes(j))&&q.every((j,i)=>a[i].includes(j)),"source IDs");
    check(upper(a,true),"large upper");hostile.push({n,r,arcs:edgesOf(a).length,witnessCountSymbolic:"2^"+r,coefficientSymbolic:(-1)**r});
  }
  // Dense articulation NO, minimize spurious YES with actual upper predicate.
  const falsePos=[];
  for(const n of [9,17,25]){
    const E=[],half=(n-1)/2;
    for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j&&(i===0||j===0||((i<=half)===(j<=half))))E.push([i,j]);
    let a=rows(n,E);check(upper(a,true),"articulation false positive");
    for(const [i,j] of E){const b=a.map(r=>r.slice());b[i]=b[i].filter(t=>t!==j);if(upper(b,true))a=b}
    const minimal=edgesOf(a);check(upper(a,true),"minimal accepted");
    for(const [i,j] of minimal){const b=a.map(r=>r.slice());b[i]=b[i].filter(t=>t!==j);check(!upper(b,true),"minimality")}
    check(minimal.every(([i,j])=>i===0||j===0||((i<=half)===(j<=half))),"articulation NO certificate");
    falsePos.push({n,initialArcs:E.length,minimalArcs:minimal.length,rows:a});
  }
  return {checks,small,scales,hostile,falsePos,notes:"No Lean build, no general HC algorithm, no arithmetic circuit-size experiment. Large block counts and full coefficients symbolic; only two explicit witnesses tested per hostile graph."};
}
const result=audit(); if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
