// M26: local subcubic matching compiler and actual GD26 gate check.
// node checker.js path-to-BS19_results.json
function run(data){
let checks=0; const assert=(x,msg)=>{checks++;if(!x)throw Error(msg)};
const types={AND:[[0,0,0],[0,1,0],[1,0,0],[1,1,1]],OR:[[0,0,0],[0,1,1],[1,0,1],[1,1,1]],NOT:[[0,1],[1,0]],IN:[[0],[1]],ONE:[[1]],ZERO:[[0]]};
function ladder(r){
 const l=2*r-1, edges=[];
 for(let j=0;j<l-1;j++){edges.push([j,j+1,-1]);edges.push([l+j,l+j+1,-1])}
 for(let j=0;j<r;j++)edges.push([2*j,l+2*j,j]);
 return {n:2*l,edges};
}
function enumMatch(G){
 const incident=Array.from({length:G.n},()=>[]);
 G.edges.forEach(([a,b,k],i)=>{incident[a].push([b,k,i]);incident[b].push([a,k,i])});
 const out=[];
 function rec(mask,rows){
  if(mask===0){out.push(rows);return}
  const a=31-Math.clz32(mask&-mask);
  for(const [b,k] of incident[a])if(mask&(1<<b))rec(mask^(1<<a)^(1<<b),k<0?rows:rows.concat(k));
 }
 rec((1<<G.n)-1,[]);return out;
}
const local={};
for(let r=1;r<=7;r++){
 const G=ladder(r), ms=enumMatch(G);
 assert(ms.length===r,'count');assert(ms.every(x=>x.length===1),'one cross');
 assert(new Set(ms.map(x=>x[0])).size===r,'unique');
 const d=Array(G.n).fill(0);for(const [a,b] of G.edges){d[a]++;d[b]++}assert(Math.max(...d)<=3,'degree');
}
for(const [k,rows] of Object.entries(types))local[k]=enumMatch(ladder(rows.length)).map(x=>rows[x[0]]);
function compile(C,pivot){
 const b=[],rest=[];
 for(const L of C){const hit=L.find(x=>Math.abs(x)===pivot);
 if(!hit)rest.push(L);else b.push(L.filter(x=>Math.abs(x)!==pivot).map(x=>hit>0?x:-x))}
 const ext=[...new Set(C.flat().map(Math.abs))].filter(v=>v!==pivot).sort((a,b)=>a-b);
 const owners=[];let next=Math.max(...ext)+1;
 function add(type,vars){owners.push({type,vars});return vars.at(-1)}
 function gate(type,...a){return add(type,[...a,next++])}
 const neg=new Map();
 function lit(x){if(x>0)return x; if(!neg.has(-x))neg.set(-x,gate('NOT',-x));return neg.get(-x)}
 function fold(type,A){assert(A.length>0,'nonempty');return A.reduce((a,b)=>gate(type,a,b))}
 ext.forEach(x=>add('IN',[x]));
 function flags(L){const a=L.map(lit);return [fold('AND',a.map(x=>lit(-x))),fold('AND',a)]}
 const fs=b.map(flags);const reject=gate('AND',fold('OR',fs.map(x=>x[0])),fold('OR',fs.map(x=>x[1])));
 add('ZERO',[reject]);const gateOnly=owners.slice();
 for(const L of rest){const [z,o]=flags(L);add('ZERO',[z]);add('ZERO',[o])}
 // occurrence-star syndrome (one independent row per non-reference occurrence)
 const occ=new Map();owners.forEach((o,i)=>o.vars.forEach((v,j)=>{if(!occ.has(v))occ.set(v,[]);occ.get(v).push([i,j])}));
 let q=0;const masks=owners.map(o=>o.vars.map(()=>0n));
 for(const a of occ.values())for(let i=1;i<a.length;i++){
  const [u,j]=a[0],[v,k]=a[i],bit=1n<<BigInt(q++);
  masks[u][j]^=bit;masks[v][k]^=bit;
 }
 const labels=owners.map((o,i)=>local[o.type].map(row=>row.reduce((s,x,j)=>s^(x?masks[i][j]:0n),0n)));
 const graphVertices=owners.reduce((s,o)=>s+ladder(local[o.type].length).n,0);
 const graphEdges=owners.reduce((s,o)=>s+ladder(local[o.type].length).edges.length,0);
 return {b,rest,ext,owners,gateOnly,q,labels,graphVertices,graphEdges};
}
function ac(owners,pins){
 let dom=new Map(),changes=0,scans=0;
 for(const o of owners)for(const v of o.vars)if(!dom.has(v))dom.set(v,3);
 for(const [v,x] of pins)dom.set(v,1<<x);
 for(;;){let changed=false;
  for(const o of owners){
   const rows=local[o.type].filter(r=>r.every((x,j)=>dom.get(o.vars[j])&(1<<x)));scans++;
   if(!rows.length)return {ok:false,changes,scans};
   o.vars.forEach((v,j)=>{let m=0;for(const r of rows)m|=1<<r[j];const old=dom.get(v),nv=old&m;if(nv!==old){dom.set(v,nv);changes++;changed=true}});
  }
  if(!changed)return {ok:true,changes,scans,dom};
 }
}
// Direct deterministic gate replay, choosing the unique actual matching row at each owner.
// Input owners take externally assigned bits; output pins are checked, not overwritten.
function replay(H,pins,limit=H.owners.length){
 const a=new Map(pins);let sy=0n;
 for(let i=0;i<limit;i++){
  const o=H.owners[i], rows=local[o.type];
  const hits=rows.map((r,k)=>[r,k]).filter(([r])=>r.every((x,j)=>!a.has(o.vars[j])||a.get(o.vars[j])===x));
  if(!hits.length)return false;
  assert(hits.length===1,'functional row');
  const [r,k]=hits[0];r.forEach((x,j)=>a.set(o.vars[j],x));sy^=H.labels[i][k];
 }
 if(limit===H.owners.length)assert(sy===0n,'joint syndrome');
 return true;
}
const nae=(L,a)=>{const bits=L.map(x=>a.get(Math.abs(x))^(x<0?1:0));return bits.some(x=>x!==bits[0])};
const K=data.common.find(x=>x.K===16).residual;
const H=compile(K.C,19);
const init=ac(H.owners,[]);
assert(init.ok,'root closure');
let gateOK=0,fullOK=0,sourceWord=null,gateReject=null,accepted=[],samples=0,acScans=0;
for(let w=0;w<1<<H.ext.length;w++){
 const pins=H.ext.map((v,i)=>[v,(w>>i)&1]),a=new Map(pins);
 let possible=false;
 for(let x=0;x<2;x++){a.set(19,x);if(H.b.every(L=>nae([19,...L],a)))possible=true}
 a.delete(19);
 const g=replay(H,pins,H.gateOnly.length),full=replay(H,pins);
 assert(g===possible,'gate');assert(full===(possible&&H.rest.every(L=>nae(L,a))),'whole');
 if(g){gateOK++;accepted.push(w)}else if(gateReject===null)gateReject=w;
 if(w%127===0){const c=ac(H.owners,pins);assert(c.ok===full,'AC complete input');samples++;acScans+=c.scans}
 if(full){
  fullOK++;
  if(sourceWord===null){
   for(let x=0;x<2;x++){a.set(19,x);if(H.b.every(L=>nae([19,...L],a)))break}
   for(const {v,bucket} of K.log.slice().reverse()){
    let found=false;for(let x=0;x<2;x++){a.set(v,x);if(bucket.every(L=>nae([v,...L],a))){found=true;break}}assert(found,'lift')
   }
   const n=data.source.n;
   assert(data.source.O.every(o=>{const r=o.t.reduce((s,v,j)=>s+(a.get(v+1)<<j),0);return !o.bad.includes(r)}),'source');
   sourceWord=Array.from({length:n},(_,i)=>a.get(i+1)*2**i).reduce((s,x)=>s+x,0);
  }
 }
}
const set=new Set(accepted);let obstruction=null;
outer:for(const x of accepted)for(const y of accepted){let d=x^y;for(let i=0;i<H.ext.length;i++)if((d&(1<<i))&&!set.has(x^(1<<i))){obstruction={x,y,flipped:H.ext[i],forbidden:x^(1<<i)};break outer}}
assert(obstruction!==null,'nonproduct');
function small(C,pivot){const h=compile(C,pivot);const init=ac(h.owners,[]);let count=0;for(let w=0;w<1<<h.ext.length;w++){const p=h.ext.map((v,i)=>[v,(w>>i)&1]),a=new Map(p);let exp=false;for(let x=0;x<2;x++){a.set(pivot,x);if(C.every(L=>nae(L,a)))exp=true}assert(replay(h,p)===exp,'control');if(exp)count++}return {count,initial: init.ok}}
// Two opposite binary owners are unsatisfiable; same owner duplicate is SAT.
const controls=[small([[1,2],[1,-2]],1),small([[1,2],[1,2]],1),small([[1,2,3],[1,-2,-3]],1)];
assert(controls[0].count===0&&controls[1].count===2,'opposite labels');
return {checks,localLadders:7,controls,sourceBlob:'cda85d10e150d823501fe6102408455d4fe2a',pivot:19,ext:H.ext,gateOwners:H.gateOnly.length,owners:H.owners.length,graphVertices:H.graphVertices,graphEdges:H.graphEdges,syndromeRows:H.q,rootClosure:{ok:init.ok,changes:init.changes,scans:init.scans,forcedSource:H.ext.filter(v=>init.dom.get(v)!==3)},exteriorWords:2**H.ext.length,gateOK,fullOK,sourceWord,gateReject,obstruction,samples,acScans};
}
if(typeof require!=='undefined'&&typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'))),null,2));
