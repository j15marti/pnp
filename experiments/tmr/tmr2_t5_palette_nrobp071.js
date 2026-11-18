function audit071(){
  const R=(a,b)=>[1,3].includes((b-a+10)%5);let checks=0;
  const ok=(b,where)=>{checks++;if(!b)throw Error(where)};
  const P=[[0,3],[1,3]],t=P[0].map(x=>P[1].map(y=>+R(x,y)));
  ok(JSON.stringify(t)==="[[1,1],[1,0]]","palette matrix");
  let triples=0;
  for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)for(let c=0;c<5;c++)for(let d=c+1;d<5;d++)triples+=([R(a,c),R(a,d),R(b,c),R(b,d)].filter(Boolean).length===3);
  ok(triples===10,"all two-by-two palettes");
  const encode=(n,E)=>[`p t5 ${n} ${E.length}`,...Array.from({length:n},(_,i)=>`v ${i}`),...E.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]).map(([a,b])=>`a ${a} ${b}`)].join("\n")+"\n";
  function decode(s){
    if(!s.endsWith("\n"))throw Error("terminator");
    const l=s.trimEnd().split("\n"),h=/^p t5 (0|[1-9]\d*) (0|[1-9]\d*)$/.exec(l[0]);
    if(!h)throw Error("header");const n=+h[1],m=+h[2];
    if(!Number.isSafeInteger(n)||!Number.isSafeInteger(m)||n>l.length||l.length!==n+m+1)throw Error("header count");
    for(let i=0;i<n;i++)if(l[i+1]!==`v ${i}`)throw Error("vertex");
    const E=[],seen=new Set();
    for(let j=0;j<m;j++){
      const a=/^a (0|[1-9]\d*) (0|[1-9]\d*)$/.exec(l[n+1+j]);
      if(!a)throw Error("arc");const u=+a[1],v=+a[2],key=`${u},${v}`;
      if(!Number.isSafeInteger(u)||!Number.isSafeInteger(v)||u>=n||v>=n||seen.has(key))throw Error("arc invalid");
      seen.add(key);E.push([u,v]);
    }
    if(encode(n,E)!==s)throw Error("noncanonical");
    return {n,m,E,loop:E.some(([u,v])=>u===v)};
  }
  const defs=[
    ["K2_2",2,2,[[0,2],[0,3],[1,2],[1,3]]],
    ["K3_3",3,3,Array.from({length:9},(_,k)=>[Math.floor(k/3),3+k%3])],
    ["K4_crown_double_cover",4,4,Array.from({length:16},(_,k)=>Math.floor(k/4)===k%4?null:[Math.floor(k/4),4+k%4]).filter(Boolean)],
    ["oriented_C6",3,3,[[0,3],[0,5],[1,3],[1,4],[2,4],[2,5]]],
    ["two_disjoint_edges",2,2,[[0,2],[1,3]]]
  ];
  const out={};
  function assignments(n,dom,fn){const x=Array(n).fill(0);function rec(i){if(i===n){fn(x);return;}for(const v of dom){x[i]=v;rec(i+1)}}rec(0)}
  for(const [name,L,V,E] of defs){
    const n=L+V,src=encode(n,E),s=decode(src);
    ok(s.n===n&&s.m===E.length&&!s.loop,"source");
    let cnt5=0,cnt2=0;
    assignments(n,[0,1,2,3,4],x=>{if(E.every(([u,v])=>R(x[u],x[v])))cnt5++});
    assignments(n,[0,1],x=>{
      const labels=x.map((v,i)=>i<L?(v?0:3):(v?1:3));
      const a=E.every(([u,v])=>R(labels[u],labels[v]));
      const b=E.every(([u,v])=>!!(x[u]||x[v]));
      ok(a===b,"pointwise "+name);cnt2+=+a;
    });
    ok(cnt5>0&&cnt2>0,"counts");out[name]={vertices:n,arcs:E.length,sourceBytes:src.length,T5_count:cnt5,restricted_CNF_count:cnt2};
  }
  ok(out.K2_2.T5_count===30&&out.K2_2.restricted_CNF_count===7,"K22");
  ok(out.K3_3.T5_count===70&&out.K3_3.restricted_CNF_count===15,"K33");
  const words=Array.from({length:125},(_,k)=>[k%5,Math.floor(k/5)%5,Math.floor(k/25)%5]);
  const masks=new Set(),mat=[];
  for(const p of words){
    let mask=31;
    for(const a of p){let o=0;for(let b=0;b<5;b++)if(R(a,b))o|=1<<b;mask&=o}
    masks.add(mask);mat.push(words.map(q=>+q.every(a=>mask&(1<<a))));
  }
  ok(masks.size===11&&masks.has(0),"11 mask states");
  function rankMod(a,p=101){
    a=a.map(row=>row.slice());let r=0;
    for(let j=0;j<a[0].length&&r<a.length;j++){
      let k=r;while(k<a.length&&!a[k][j])k++;if(k===a.length)continue;
      [a[k],a[r]]=[a[r],a[k]];let inv=1;while(inv*a[r][j]%p!==1)inv++;
      for(let h=j;h<a[r].length;h++)a[r][h]=a[r][h]*inv%p;
      for(let h=r+1;h<a.length;h++)if(a[h][j]){const c=a[h][j];for(let v=j;v<a[h].length;v++)a[h][v]=(a[h][v]-c*a[r][v]%p+p)%p}r++;
    }return r;
  }
  const rank=rankMod(mat);ok(rank===10,"prefix rank");
  function exactMW(n,E){
    const adj=Array(n).fill(0);for(const [u,v] of E){adj[u]|=1<<v;adj[v]|=1<<u}
    const full=(1<<n)-1,cut=Array(1<<n).fill(0);
    for(let S=0;S<=full;S++){
      const A=Array.from({length:n},(_,i)=>i).filter(i=>S&(1<<i)),D=full^S,cache=new Map();
      function f(i,used){if(i===A.length)return 0;const key=i*256+used;if(cache.has(key))return cache.get(key);let z=f(i+1,used),mask=adj[A[i]]&D&~used;while(mask){const x=mask&-mask;mask-=x;z=Math.max(z,1+f(i+1,used|x))}cache.set(key,z);return z}
      cut[S]=f(0,0);
    }
    const dp=Array(1<<n).fill(Infinity);dp[full]=0;
    for(let S=full-1;S>=0;S--)for(let i=0;i<n;i++)if(!(S&(1<<i))){const t=S|1<<i;dp[S]=Math.min(dp[S],Math.max(cut[t],dp[t]))}
    return {allOrderMinimum:dp[0],fixedBipartitionCut:cut[(1<<(n/2))-1]};
  }
  const MW=exactMW(8,defs[2][3]);ok(MW.allOrderMinimum===3&&MW.fixedBipartitionCut===4,"matching width");
  out.K3_3.cofactorMasks=masks.size;out.K3_3.prefixRank101=rank;out.K4_crown_double_cover.matchingWidth=MW;
  const bad=["p t5 1 0\nv 0","p t5 2 2\nv 0\nv 1\na 1 0\na 0 1\n","p t5 2 2\nv 0\nv 1\na 0 1\na 0 1\n","p t5 2 1\nv 0\nv 1\na 0 2\n"];
  for(const s of bad){let rejects=false;try{decode(s)}catch(e){rejects=true}ok(rejects,"negative parser")}
  ok(decode("p t5 1 1\nv 0\na 0 0\n").loop,"legal loop count zero");
  return {revision:"tmr2-t5-palette-nrobp071.v1",seed:null,assertions:checks,failures:0,palette:{left:P[0],right:P[1],truthTable:t,allThreeOneTables:triples},cases:out,limits:["No LPS p=5 q>125 generated or measured","Asymptotic branching-program theorem relies on primary Razgon 2014 and LPS 1988","No general SAT-decision work lower bound","Finite audit is COMPUTATIONAL; no checkout preflight, LaTeX, physical TM replay"]};
}
const r=audit071();if(typeof console!=='undefined')console.log(JSON.stringify(r,null,2));
