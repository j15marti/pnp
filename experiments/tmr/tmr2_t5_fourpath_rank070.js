function audit070() {
  const R=(a,b)=>((b-a+5)%5===1||(b-a+5)%5===3);
  let checks=0;
  const A=Array.from({length:5},(_,i)=>Array.from({length:5},(_,j)=>+R(i,j)));
  const tr=M=>M[0].map((_,i)=>M.map(row=>row[i]));
  const mul=(P,Q)=>P.map(row=>Q[0].map((_,j)=>row.reduce((s,a,k)=>s+a*Q[k][j],0)));
  const W=mul(mul(mul(A,A),tr(A)),tr(A));
  const expect=[[6,1,4,4,1],[1,6,1,4,4],[4,1,6,1,4],[4,4,1,6,1],[1,4,4,1,6]];
  const assert=(b,msg)=>{checks++;if(!b)throw Error(msg);};
  for(let i=0;i<5;i++)for(let j=0;j<5;j++)assert(W[i][j]===expect[i][j],"matrix W");
  const rankMod=(M,p=101)=>{
    const B=M.map(row=>row.map(x=>(x%p+p)%p)),h=B.length,w=B[0].length;
    let r=0;
    const power=(a,n)=>{let b=1;while(n){if(n&1)b=b*a%p;a=a*a%p;n>>=1;}return b;};
    for(let j=0;j<w&&r<h;j++){
      let k=r;while(k<h&&!B[k][j])k++;
      if(k===h)continue;
      [B[k],B[r]]=[B[r],B[k]];
      const inv=power(B[r][j],p-2);
      for(let t=j;t<w;t++)B[r][t]=B[r][t]*inv%p;
      for(let k2=r+1;k2<h;k2++)if(B[k2][j]){
        const a=B[k2][j];for(let t=j;t<w;t++)B[k2][t]=(B[k2][t]-a*B[r][t]%p+p)%p;
      }
      r++;
    }
    return r;
  };
  assert(rankMod(A)===5,"rank A");
  assert(rankMod(W)===5,"rank W");
  let witness=null;
  for(let x=0;x<5;x++)for(let y=0;y<5;y++){
    let z=0;
    for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){
      if(R(x,a)&&R(a,b)&&R(y,c)&&R(c,b)){
        z++;if(x===0&&y===0&&!witness)witness=[a,b,c];
      }
    }
    assert(z===W[x][y],"path count for endpoints");
  }
  assert(witness!==null,"witness zero to zero");
  const cases=[
    {name:"one_edge",n:2,e:[[0,1]]},
    {name:"two_disjoint_edges",n:4,e:[[0,1],[2,3]]},
    {name:"P3",n:3,e:[[0,1],[1,2]]},
    {name:"C4",n:4,e:[[0,1],[1,2],[2,3],[0,3]]},
    {name:"P5",n:5,e:[[0,1],[1,2],[2,3],[3,4]]}
  ];
  const weight=(edges,x)=>edges.reduce((v,[u,w])=>v*W[x[u]][x[w]],1);
  const count=(n,edges)=>{
    let sum=0;
    function rec(x){if(x.length===n){sum+=weight(edges,x);return;}for(let a=0;a<5;a++)rec([...x,a]);}
    rec([]);return sum;
  };
  const counts={};const bytes={};
  function buildSource(n,edges){
    const arcs=[];
    edges.forEach(([u,v],i)=>{const a=n+3*i,b=a+1,c=a+2;arcs.push([u,a],[a,b],[c,b],[v,c]);});
    const n2=n+3*edges.length;
    arcs.sort((x,y)=>x[0]-y[0]||x[1]-y[1]);
    const src=`p t5 ${n2} ${arcs.length}\n`+Array.from({length:n2},(_,i)=>`v ${i}\n`).join("")+arcs.map(([u,v])=>`a ${u} ${v}\n`).join("");
    return {n:n2,arcs,src};
  }
  function parseSource(src) {
    if(!src.endsWith("\n"))throw Error("newline");
    const lines=src.slice(0,-1).split("\n");
    const h=lines[0].match(/^p t5 (0|[1-9]\d*) (0|[1-9]\d*)$/);
    if(!h)throw Error("header");
    const n=Number(h[1]),m=Number(h[2]);
    if(n>lines.length||m>lines.length||lines.length!==n+m+1)throw Error("size");
    for(let i=0;i<n;i++)if(lines[i+1]!==`v ${i}`)throw Error("vertex");
    const arcs=[];
    for(let i=0;i<m;i++){
      const g=lines[i+1+n].match(/^a (0|[1-9]\d*) (0|[1-9]\d*)$/);
      if(!g)throw Error("arc");
      const u=Number(g[1]),v=Number(g[2]);
      if(u===v||u>=n||v>=n)throw Error("range");
      if(arcs.length&&(u<arcs.at(-1)[0]||(u===arcs.at(-1)[0]&&v<=arcs.at(-1)[1])))throw Error("order");
      arcs.push([u,v]);
    }
    return {n,arcs};
  }
  function recognize(n,arcs){
    const ins=Array.from({length:n},()=>[]),outs=Array.from({length:n},()=>[]);
    for(const [u,v] of arcs){ins[v].push(u);outs[u].push(v);}
    const core=[],near=[],mid=[];
    for(let v=0;v<n;v++){
      if(ins[v].length===0&&outs[v].length>0)core.push(v);
      else if(ins[v].length===1&&outs[v].length===1)near.push(v);
      else if(ins[v].length===2&&outs[v].length===0)mid.push(v);
      else return null;
    }
    const cr=new Set(core),nr=new Set(near),mr=new Set(mid),edges=[];
    for(const b of mid){
      const [a,c]=ins[b];
      if(a===c||!nr.has(a)||!nr.has(c))return null;
      const u=ins[a][0],v=ins[c][0];
      if(!cr.has(u)||!cr.has(v)||u===v)return null;
      edges.push([Math.min(u,v),Math.max(u,v)]);
    }
    if(near.length!==2*mid.length||arcs.length!==4*mid.length)return null;
    for(const a of near)if(!cr.has(ins[a][0])||!mr.has(outs[a][0]))return null;
    for(const u of core)if(outs[u].some(v=>!nr.has(v)))return null;
    const keys=edges.map(x=>x.join("-"));
    if(new Set(keys).size!==keys.length)return null;
    return {core:core.length,edges:edges.length};
  }
  for(const t of cases){
    const z=count(t.n,t.e);counts[t.name]=String(z);
    assert(z>=5**t.n&&z<=5**t.n*6**t.e.length,"count bounds");
    const b=buildSource(t.n,t.e);bytes[t.name]=b.src.length;
    const p=parseSource(b.src);
    assert(p.n===b.n&&p.arcs.length===b.arcs.length,"source parse");
    const rec=recognize(p.n,p.arcs);
    assert(rec!==null&&rec.core===t.n&&rec.edges===t.e.length,"source recon");
    const incoming=Array.from({length:p.n},()=>0),outgoing=Array.from({length:p.n},()=>0);
    for(const [u,v] of p.arcs){incoming[v]++;outgoing[u]++;}
    const x=incoming.map((v,i)=>v===0?0:(outgoing[i]===0?2:1));
    assert(p.arcs.every(([u,v])=>R(x[u],x[v])),"fixed 3-level SAT witness");
  }
  assert(counts.one_edge==="80"&&counts.two_disjoint_edges==="6400","product control");
  const bad=buildSource(3,[[0,1],[1,2]]).src;
  for(const src of [bad.replace("v 0\n","v 00\n"),bad+"\na 0 1\n",bad.slice(0,-1)]){
    let fail=false;try{parseSource(src);}catch(e){fail=true;}assert(fail,"bad canonical source");
  }
  const values=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++)values.push([a,b]);
  const path=[[0,1],[1,2],[2,3],[3,4]];
  const F=values.map(([la,lb])=>values.map(([ra,rb])=>weight(path,[la,ra,0,lb,rb])));
  for(let i=0;i<25;i++)for(let j=0;j<25;j++){
    const [la,lb]=values[i],[ra,rb]=values[j];
    assert(F[i][j]===W[la][ra]*W[ra][0]*W[0][lb]*W[lb][rb],"P5 factor");
  }
  assert(rankMod(F)===25,"P5 conditional rank 25 modulo 101");
  const raw=Array.from({length:25},()=>Array(125).fill(0));
  for(let a=0;a<5;a++)for(let u=0;u<5;u++)for(let b=0;b<5;b++)for(let c=0;c<5;c++)for(let v=0;v<5;v++){
    raw[5*a+u][25*b+5*c+v]=+(R(u,a)&&R(a,b)&&R(v,c)&&R(c,b));
  }
  const marginalized=Array.from({length:5},()=>Array(5).fill(0));
  for(let a=0;a<5;a++)for(let u=0;u<5;u++)for(let b=0;b<5;b++)for(let c=0;c<5;c++)for(let v=0;v<5;v++)marginalized[u][v]+=raw[5*a+u][25*b+5*c+v];
  for(let u=0;u<5;u++)for(let v=0;v<5;v++)assert(marginalized[u][v]===W[u][v],"interleaved raw marginal");
  assert(rankMod(raw)===5,"raw tensor rank");
  return {
    revision:"tmr2-fourpath-expanded-cofactor070.js.v1",seed:null,assertions:checks,failures:0,
    W,rank_mod101_W:rankMod(W),witness_zero_to_zero:witness,
    exact_counts:counts,canonical_source_bytes:bytes,P5_induced_matching:2,
    P5_conditioned_rank_mod101:rankMod(F),onepath_interleaved_raw_rank_mod101:rankMod(raw),
    infinite_statement:"LPS p=5 q prime>125 q=1 mod20; symbolic rank >=5^{c n} for all OBDD orders; not empirically tested",
    limitations:["No LPS q>125 instance generated in this executable","No full PC executed","No unrestricted decision lower bound","No physical TM microtrace"]
  };
}

const result = audit070();
process.stdout.write(JSON.stringify(result,null,2) + '\n');
