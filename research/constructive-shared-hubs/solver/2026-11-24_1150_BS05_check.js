function BS05(input, options={}) {
  const A=(v,m)=>{if(!v)throw Error(m||"assertion");}, M={closurePasses:0,rowTests:0,deletions:0,basisXors:0,blocks:0,articulations:0,tuples:0,joins:0,peakMessage:0,verified:0,maxBlockVolume:"0",sumBlockVolume:"0"};
  const n0=input.cnf?.n??input.graph?.n;
  if(n0!==undefined)A(Number.isSafeInteger(n0)&&n0>=0,"explicit output size");
  let raw=input;
  if(input.cnf){const {n,clauses}=input.cnf;A(clauses.every(c=>c.length<=3&&c.every(l=>Number.isSafeInteger(l)&&l&&Math.abs(l)<=n)),"CNF");raw={...input,K:clauses.map(c=>c.length-1),factors:Array.from({length:n},(_,i)=>[0,1].map(x=>({c:clauses.map(c=>c.filter(l=>Math.abs(l)===i+1&&x!==Number(l>0)).length)})))};}
  if(input.graph){const {n,edges}=input.graph;A(edges.every(([u,v,s])=>Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v>=0&&u<n&&v<n&&u!==v&&Number.isInteger(s)&&s>=0&&s<4),"signed graph");raw={...input,K:edges.flatMap(()=>[1,1,1,1]),factors:Array.from({length:n},(_,i)=>[0,1,2,3].map(x=>({c:edges.flatMap(([u,v,s])=>[0,1,2,3].map(a=>Number(i===u&&x===a)+Number(i===v&&x===(a^s))))})))};}
  const K=raw.K.map(BigInt), b=BigInt(raw.b??0), h=BigInt(raw.h??0), q=raw.q??0, O=K.length;
  A(Number.isSafeInteger(q)&&q>=0&&b>=0n&&h>=0n&&h<(1n<<BigInt(q)),"target");
  const F=raw.factors.map(f=>f.map((r,id)=>({id,t:BigInt(r.t??0),g:BigInt(r.g??0),c:(r.c??Array(O).fill(0)).map(BigInt)})));
  A(F.every(f=>f.every(r=>r.t>=0n&&r.g>=0n&&r.g<(1n<<BigInt(q))&&r.c.length===O&&r.c.every(x=>x>=0n))),"rows");
  const ans=(status,w=null)=>({status,w,counters:M});
  if(raw.allGuards)return ans("UNKNOWN");
  const min=(a,b)=>a<b?a:b, N=F.length;
  let R=F.map(f=>f.slice());
  const high=x=>x.toString(2).length-1;
  function basis(vs){const p=new Map();const red=x=>{while(x){const y=p.get(high(x));if(y===undefined)break;x^=y;M.basisXors++;}return x;};for(let x of vs){x=red(x);if(x)p.set(high(x),x);}return red;}
  const pack=r=>(r.t<<BigInt(q))|r.g, target=(b<<BigInt(q))|h;
  while(true){
    M.closurePasses++;if(R.some(f=>!f.length)||K.some(x=>x<0n))return ans("UNSAT");
    const m=R.map(f=>K.map((_,j)=>f.reduce((z,r)=>min(z,r.c[j]),f[0].c[j])));
    const total=K.map((_,j)=>m.reduce((z,a)=>z+a[j],0n));
    if(total.some((x,j)=>x>K[j]))return ans("UNSAT");
    let changed=false;
    outer:for(let i=0;i<N;i++){
      let a=0n;const vs=[];
      for(let j=0;j<N;j++)if(i!==j){const z=pack(R[j][0]);a^=z;for(const r of R[j])vs.push(pack(r)^z);}
      const red=basis(vs);
      for(let k=0;k<R[i].length;k++){const r=R[i][k];M.rowTests++;if(r.c.some((x,j)=>total[j]-m[i][j]+x>K[j])||red(target^a^pack(r))){R[i].splice(k,1);M.deletions++;changed=true;break outer;}}
    }
    if(!changed)break;
  }
  if(q>(options.guardCap??12))return ans("UNKNOWN");
  let bt=b, cap=K.slice();
  R=R.map(f=>{const a=f[0].t, m=K.map((_,j)=>f.reduce((z,r)=>min(z,r.c[j]),f[0].c[j]));bt^=a;cap=cap.map((x,j)=>x-m[j]);return f.map(r=>({...r,t:r.t^a,c:r.c.map((x,j)=>x-m[j])}));});
  let mask=bt;for(const f of R)for(const r of f)mask|=r.t;
  const D=mask?high(mask)+1:0, V=N+O+D, adj=Array.from({length:V},()=>[]), es=[];
  const edge=(u,v)=>{const k=es.length;es.push([u,v]);adj[u].push([v,k]);adj[v].push([u,k]);};
  for(let i=0;i<N;i++){
    for(let j=0;j<O;j++)if(R[i].some(r=>r.c[j]))edge(i,N+j);
    for(let j=0;j<D;j++)if(R[i].some(r=>(r.t>>BigInt(j))&1n))edge(i,N+O+j);
  }
  const isFactor=v=>v<N, isCost=v=>v>=N&&v<N+O;
  const contribution=(r,v)=>isCost(v)?r.c[v-N]:(r.t>>BigInt(v-N-O))&1n;
  const combine=(v,a,b)=>isCost(v)?a+b:a^b;
  const valid=(v,a)=>isCost(v)?a<=cap[v-N]:a===((bt>>BigInt(v-N-O))&1n);
  const disc=Array(V).fill(0),low=Array(V).fill(0),stack=[],blocks=[];let tick=0;
  function dfs(u,pe){disc[u]=low[u]=++tick;for(const [v,e] of adj[u]){if(e===pe)continue;if(!disc[v]){stack.push(e);dfs(v,e);low[u]=Math.min(low[u],low[v]);if(low[v]>=disc[u]){const E=[];let x;do{x=stack.pop();E.push(x);}while(x!==e);blocks.push({E,vs:[...new Set(E.flatMap(k=>es[k]))]});}}else if(disc[v]<disc[u]){stack.push(e);low[u]=Math.min(low[u],disc[v]);}}}
  for(let v=0;v<V;v++)if(!disc[v]){dfs(v,-1);if(!adj[v].length)blocks.push({E:[],vs:[v]});}
  const membership=Array.from({length:V},()=>[]);blocks.forEach((B,k)=>B.vs.forEach(v=>membership[v].push(k)));
  const art=v=>membership[v].length>1;
  M.blocks=blocks.length;M.articulations=membership.filter(a=>a.length>1).length;
  const volumes=blocks.map(B=>B.vs.filter(isFactor).reduce((p,i)=>p*BigInt(R[i].length),1n));
  M.maxBlockVolume=String(volumes.reduce((a,b)=>a>b?a:b,0n));M.sumBlockVolume=String(volumes.reduce((a,b)=>a+b,0n));
  if(volumes.some(x=>x>BigInt(options.blockCap??100000)))return ans("UNKNOWN");
  const identity=()=>[{g:0n,v:0n,w:[]}];
  function insert(map,entry,kind){const key=kind==="cost"?String(entry.g):`${entry.g}/${entry.v}`;const old=map.get(key);if(!old||(kind==="cost"&&entry.v<old.v))map.set(key,entry);}
  function join(A0,B0,kind,op=(a,b)=>0n){const m=new Map();for(const a of A0)for(const b of B0){M.joins++;insert(m,{g:a.g^b.g,v:op(a.v,b.v),w:a.w.concat(b.w)},kind);}M.peakMessage=Math.max(M.peakMessage,m.size);return [...m.values()];}
  const plain=(a,b)=>join(a,b,"exact");
  const visited=new Set();
  function atArt(v,parent){
    const children=membership[v].filter(k=>k!==parent).map(k=>atBlock(k,v));
    if(isFactor(v)){const out=[];for(const r of R[v]){let z=[{g:r.g,v:0n,w:[[v,r.id]]}];for(const msg of children)z=plain(z,msg.filter(x=>x.v===BigInt(r.id)));for(const x of z)out.push({...x,v:BigInt(r.id)});}M.peakMessage=Math.max(M.peakMessage,out.length);return out;}
    const kind=isCost(v)?"cost":"exact";let z=identity();
    for(const msg of children)z=join(z,msg,kind,(a,b)=>combine(v,a,b));
    if(isCost(v))z=z.filter(x=>x.v<=cap[v-N]);return z;
  }
  function atBlock(k,parent=-1){
    A(!visited.has(k),"block-cut cycle");visited.add(k);
    const B=blocks[k], fs=B.vs.filter(isFactor), os=B.vs.filter(v=>!isFactor(v)), kids=new Map(B.vs.filter(v=>art(v)&&v!==parent).map(v=>[v,atArt(v,k)]));
    const out=new Map(), picks=new Map(), kind=parent>=0&&isCost(parent)?"cost":"exact";
    function evaluate(){
      M.tuples++;
      const loads=new Map(os.map(v=>[v,0n]));
      for(const e of B.E){const [i,o]=es[e];loads.set(o,combine(o,loads.get(o),contribution(picks.get(i),o)));}
      let g=0n,w=[];for(const i of fs){const r=picks.get(i);w.push([i,r.id]);if(!art(i))g^=r.g;}
      let msg=[{g,v:0n,w}];
      for(const i of fs)if(kids.has(i))msg=plain(msg,kids.get(i).filter(x=>x.v===BigInt(picks.get(i).id)));
      for(const o of os){if(o===parent)continue;const load=loads.get(o);if(kids.has(o)){msg=plain(msg,kids.get(o).filter(x=>valid(o,combine(o,load,x.v))));}else if(!valid(o,load))return;if(!msg.length)return;}
      const value=parent<0?0n:isFactor(parent)?BigInt(picks.get(parent).id):loads.get(parent);
      if(parent>=0&&isCost(parent)&&value>cap[parent-N])return;
      for(const x of msg)insert(out,{...x,v:value},kind);
    }
    function enumerate(j){if(j===fs.length){evaluate();return;}const i=fs[j];for(const r of R[i]){picks.set(i,r);enumerate(j+1);}}
    enumerate(0);M.peakMessage=Math.max(M.peakMessage,out.size);return [...out.values()];
  }
  let all=identity();for(let k=0;k<blocks.length;k++)if(!visited.has(k))all=plain(all,atBlock(k));
  const hit=all.find(x=>x.g===h);if(!hit)return ans("UNSAT");
  const w=Array(N);for(const [i,id] of hit.w){A(w[i]===undefined||w[i]===id,"inconsistent lift");w[i]=id;}
  let t=0n,g=0n,c=K.map(()=>0n);for(let i=0;i<N;i++){const r=F[i][w[i]];A(r,"missing lift");t^=r.t;g^=r.g;c=c.map((x,j)=>x+r.c[j]);M.verified++;}
  A(t===b&&g===h&&c.every((x,j)=>x<=K[j]),"original row verification");
  return ans("SAT",w);
}
function controls(){
 const A=(v,m)=>{if(!v)throw Error(m);};let seed=261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n);};
 const out={seed:261124,random:{SAT:0,UNSAT:0},cube:{SAT:0,UNSAT:0},fano:[],graphs:[],scale:[],articulation:[],counters:{},referenceTuples:0};
 function brute(x){let found=false;const K=x.K.map(BigInt);function rec(i,t,g,c){if(i===x.factors.length){out.referenceTuples++;if(t===BigInt(x.b??0)&&g===BigInt(x.h??0)&&c.every((v,j)=>v<=K[j]))found=true;return;}for(const r of x.factors[i])rec(i+1,t^BigInt(r.t??0),g^BigInt(r.g??0),c.map((v,j)=>v+BigInt(r.c?.[j]??0)));}rec(0,0n,0n,K.map(()=>0n));return found;}
 function test(x,expected,category){const z=BS05(x);A(z.status===(expected?"SAT":"UNSAT"),"mismatch "+category+" "+JSON.stringify(x));for(const [k,v] of Object.entries(z.counters))if(typeof v==="number")out.counters[k]=k==="peakMessage"?Math.max(out.counters[k]??0,v):(out.counters[k]??0)+v;return z;}
 for(let i=0;i<220;i++){
  const n=1+rnd(6),m=1+rnd(4),factors=Array.from({length:n},()=>Array.from({length:1+rnd(3)},()=>({t:rnd(8),g:rnd(4),c:Array.from({length:m},()=>rnd(4))}))),x={factors,K:Array.from({length:m},()=>rnd(9)),b:rnd(8),h:rnd(4),q:2};
  if(i%2===0){const rs=factors.map(f=>f[rnd(f.length)]);x.b=rs.reduce((v,r)=>v^r.t,0);x.h=rs.reduce((v,r)=>v^r.g,0);x.K=x.K.map((_,j)=>rs.reduce((v,r)=>v+r.c[j],0)+rnd(2));}
  const z=test(x,brute(x),"random "+i);out.random[z.status]++;
 }
 const cube=Array.from({length:8},(_,w)=>[1,2,3].map((i,j)=>w>>j&1?i:-i));
 for(let mask=0;mask<256;mask++){const clauses=cube.filter((_,i)=>mask>>i&1);const truth=Array.from({length:8},(_,x)=>x).some(x=>clauses.every(c=>c.some(l=>Boolean(x>>(Math.abs(l)-1)&1)===(l>0))));const z=test({cnf:{n:3,clauses}},truth,"cube");out.cube[z.status]++;}
 const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],f=lines.flatMap(c=>[c,c.map(x=>-x)]);
 for(let i=-1;i<14;i++){const clauses=f.filter((_,j)=>j!==i),z=test({cnf:{n:7,clauses}},i>=0,"Fano");out.fano.push({removed:i,status:z.status,volume:z.counters.maxBlockVolume});}
 const edges=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)edges.push([i,j,0]);
 for(let i=-1;i<edges.length;i++){const z=test({graph:{n:5,edges:edges.filter((_,j)=>j!==i)}},i>=0,"K5");out.graphs.push({removed:i,status:z.status,volume:z.counters.maxBlockVolume});}
 for(const k of [4,16,64,128]){
   const B=1n<<80n;
   for(const delta of [-1n,0n]){
    const factors=Array.from({length:2*k},(_,i)=>[0,1].map(x=>({g:i===0&&x===1?1:0,c:Array.from({length:k+1},(_,j)=>String((x===0&&j===0||x===1&&j===1+Math.floor(i/2))?B:0n))})));
    const x={factors,K:[String(BigInt(k)*B+delta),...Array(k).fill(String(B))],q:1,h:1};
    const z=test(x,delta===0n,"budget articulation");out.scale.push({k,status:z.status,...z.counters});
   }
 }
 for(let j=0;j<80;j++){
   const n=5,O=4;const scope=[[0,1],[0,1],[0,1,2,3],[2,3],[2,3]];
   const factors=Array.from({length:n},(_,i)=>Array.from({length:2},()=>({g:rnd(4),c:Array.from({length:O},(_,o)=>scope[i].includes(o)?rnd(4):0),t:0})));
   const x={factors,K:Array.from({length:O},()=>2+rnd(6)),q:2,h:rnd(4)};
   const z=test(x,brute(x),"factor articulation");out.articulation.push({type:"factor",status:z.status,blocks:z.counters.blocks,art:z.counters.articulations});
   const fs=Array.from({length:4},(_,i)=>[0,1].map(v=>({t:v,g:rnd(4),c:Array.from({length:2},(_,o)=>o===Math.floor(i/2)?v:0)})));
   const y={factors:fs,K:[1,1],b:rnd(2),q:2,h:rnd(4)};const w=test(y,brute(y),"parity articulation");out.articulation.push({type:"parity",status:w.status,blocks:w.counters.blocks,art:w.counters.articulations});
 }
 const decline=BS05({cnf:{n:7,clauses:f}},{blockCap:4});A(decline.status==="UNKNOWN","cap decline");
 out.decline=decline;return out;
}
module.exports=BS05;
if(require.main===module){const fs=require('fs');const arg=process.argv[2];if(!arg){console.log(JSON.stringify(controls(),null,2));}else{const input=JSON.parse(fs.readFileSync(arg,'utf8'));const z=BS05(input);if(z.status==='UNKNOWN'){if(input.graph){const {n,edges}=input.graph;const rowInput={...input,K:edges.flatMap(()=>[1,1,1,1]),factors:Array.from({length:n},(_,i)=>[0,1,2,3].map(x=>({c:edges.flatMap(([u,v,s])=>[0,1,2,3].map(a=>Number(i===u&&x===a)+Number(i===v&&x===(a^s))))})))};delete rowInput.graph;console.log(JSON.stringify({blockCut:z,fallback:require('./2026-11-24_1050_BS04_check.js')(rowInput)},null,2));}else{console.log(JSON.stringify({blockCut:z,fallback:require('./2026-11-24_1050_BS04_check.js')(input)},null,2));}}else console.log(JSON.stringify(z,null,2));}}
