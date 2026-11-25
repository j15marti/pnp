function analyze(chart,imports=[]){
  const rows=chart.rowMap, R=rows.length, M=chart.ownerIDs.length, bits=rows.map((_,i)=>1n<<BigInt(i)), owners=Array.from({length:M},()=>0n);
  const masks=chart.pairHex.map(x=>BigInt("0x"+x)), live=chart.live.slice();const stats={passes:0,supportTests:0,rowsDeleted:0,importedPairs:0,importedRows:0,k22Tests:0};
  for(let i=0;i<R;i++)if(live[i])owners[rows[i][0]]|=bits[i];
  function remove(i){if(live[i]){live[i]=false;owners[rows[i][0]]&=~bits[i];return true}return false}
  function ac(){let changed;do{changed=false;stats.passes++;if(owners.some(x=>!x))return false;for(let i=0;i<R;i++)if(live[i])for(let j=0;j<M;j++)if(j!==rows[i][0]){stats.supportTests++;if(!(masks[i]&owners[j])){remove(i);stats.rowsDeleted++;changed=true;break;}}}while(changed);return !owners.some(x=>!x)}
  let ok=ac();
  for(const d of imports){if(!ok)break;for(const i of d.removedRows??[])if(remove(i))stats.importedRows++;for(const [i,h] of d.delta??[]){let x=BigInt("0x"+h)&masks[i];for(let j=0;j<R;j++)if(x&bits[j]){if(live[i]&&live[j])stats.importedPairs++;masks[i]&=~bits[j];masks[j]&=~bits[i];}}ok=ac();}
  if(!ok)return {id:chart.id,guard:chart.guard,status:"UNSAT by AC",stats};
  const ds=Array.from({length:M},(_,j)=>rows.map((_,i)=>i).filter(i=>live[i]&&rows[i][0]===j));
  let obstruction=null;
  outer:for(let i=0;i<M;i++)for(let j=i+1;j<M;j++){const a=ds[i],b=ds[j];for(let p=0;p<a.length;p++)for(let q=p+1;q<a.length;q++){stats.k22Tests++;const t=owners[j]&~(masks[a[p]]|masks[a[q]]);if(t&&(t&(t-1n))){const v=b.filter(s=>t&bits[s]).slice(0,2);obstruction={owners:[i,j],rows:[a[p],a[q],...v],words:[a[p],a[q],...v].map(k=>rows[k])};break outer;}}}
  if(obstruction)return {id:chart.id,guard:chart.guard,status:"RENAME DECLINED (K2,2)",domainSizes:ds.map(x=>x.length),obstruction,stats};
  // Exact renamability by 2SAT. A flipped row is a positive Boolean variable.
  const active=ds.flat(), idx=new Map(active.map((v,i)=>[v,i])), n=active.length,g=Array.from({length:2*n},()=>[]),rg=Array.from({length:2*n},()=>[]);
  function clause(a,b){g[a^1].push(b);rg[b].push(a^1);g[b^1].push(a);rg[a].push(b^1)}
  for(const d of ds)for(let i=0;i<d.length;i++)for(let j=i+1;j<d.length;j++)clause(2*idx.get(d[i])+1,2*idx.get(d[j])+1);
  for(let i=0;i<M;i++)for(let j=i+1;j<M;j++)for(const a of ds[i])for(const b of ds[j])if(!(masks[a]&bits[b]))clause(2*idx.get(a),2*idx.get(b));
  const seen=new Set(),order=[];function dfs(v){seen.add(v);for(const u of g[v])if(!seen.has(u))dfs(u);order.push(v)}for(let v=0;v<2*n;v++)if(!seen.has(v))dfs(v);
  const comp=Array(2*n).fill(-1);function dfs2(v,c){comp[v]=c;for(const u of rg[v])if(comp[u]<0)dfs2(u,c)}let c=0;for(const v of order.reverse())if(comp[v]<0)dfs2(v,c++);
  if(active.some((_,i)=>comp[2*i]===comp[2*i+1]))return {id:chart.id,guard:chart.guard,status:"RENAME DECLINED (SCC)",stats};
  const flipped=active.filter((_,i)=>comp[2*i+1]>comp[2*i]);const fs=new Set(flipped);
  if(ds.some(d=>d.filter(r=>!fs.has(r)).length>1))throw Error("invalid renaming owner");
  for(let i=0;i<M;i++)for(let j=i+1;j<M;j++)for(const a of ds[i])for(const b of ds[j])if(fs.has(a)&&fs.has(b)&&!(masks[a]&bits[b]))throw Error("invalid renaming conflict");
  // Generic Horn least model in renamed coordinates. A positive literal in original becomes negative if flipped.
  const rules=[];function horn(lits){let head=-1,body=[];for(const [r,pos] of lits){const p=pos!==fs.has(r);if(p){if(head!==-1)throw Error("not Horn");head=r}else body.push(r)}rules.push({head,body})}
  for(const d of ds)horn(d.map(r=>[r,true]));
  for(let i=0;i<M;i++)for(let j=i+1;j<M;j++)for(const a of ds[i])for(const b of ds[j])if(!(masks[a]&bits[b]))horn([[a,false],[b,false]]);
  const truth=new Set();let change;do{change=false;for(const {head,body} of rules)if(body.every(r=>truth.has(r))){if(head<0)return {id:chart.id,guard:chart.guard,status:"UNSAT by Horn",stats};if(!truth.has(head)){truth.add(head);change=true}}}while(change);
  const chosen=ds.map(d=>d.find(r=>truth.has(r)!==fs.has(r)));if(chosen.some(r=>r===undefined))throw Error("empty choice");for(let i=0;i<M;i++)for(let j=i+1;j<M;j++)if(!(masks[chosen[i]]&bits[chosen[j]]))throw Error("bad lift");
  return {id:chart.id,guard:chart.guard,status:"SAT by Horn",chosen,stats};
}

function make(domains,compat,id){const rowMap=domains.flatMap((d,i)=>d.map(s=>[i,s]));const pairHex=rowMap.map(([i,a])=>rowMap.reduce((z,[j,b],k)=>z|(i!==j&&compat(i,a,j,b)?1n<<BigInt(k):0n),0n).toString(16));return {id,guard:[],ownerIDs:domains.map((_,i)=>i),rowMap,pairHex,live:rowMap.map(()=>true)}}

function brute(chart){const d=chart.ownerIDs.map((_,j)=>chart.rowMap.map((_,i)=>i).filter(i=>chart.rowMap[i][0]===j&&chart.live[i])),p=chart.pairHex.map(x=>BigInt("0x"+x));function go(i,ls){if(i===d.length)return 1;let n=0;for(const a of d[i])if(ls.every(b=>p[a]&(1n<<BigInt(b))))n+=go(i+1,[...ls,a]);return n}return go(0,[])}

function tests(){let s=19;function rnd(){s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296}const controls=[];for(let i=0;i<100;i++){const d=Array.from({length:3+i%2},()=>Array.from({length:2+i%3},(_,i)=>String(i)));let edges=new Map();for(let a=0;a<d.length;a++)for(let b=a+1;b<d.length;b++)for(const x of d[a])for(const y of d[b])edges.set(`${a}:${x}:${b}:${y}`,rnd()<.65);const chart=make(d,(a,x,b,y)=>a<b?edges.get(`${a}:${x}:${b}:${y}`):edges.get(`${b}:${y}:${a}:${x}`),"random-"+i);const n=brute(chart),r=analyze(chart);if(r.status.startsWith("SAT")&&!n||r.status.startsWith("UNSAT")&&n)throw Error("label discrepancy");controls.push({models:n,status:r.status})}
const fanoEdges=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],dom=fanoEdges.map(()=>["001","010","011","100","101","110"]);function fano(deleteLast){const es=deleteLast?fanoEdges.slice(0,-1):fanoEdges;return make(dom.slice(0,es.length),(i,a,j,b)=>es[i].every((v,k)=>!es[j].includes(v)||a[k]===b[es[j].indexOf(v)]),deleteLast?"Fano deletion":"Fano")}
const f=[fano(false),fano(true)].map(c=>({models:brute(c),result:analyze(c)}));
const horn=[];for(let k=1;k<=8;k++){let rejects=0,minimal=0;for(let mask=0;mask<1<<(2*k);mask++){let hit=true;for(let i=0;i<k;i++)if(!(mask&(3<<(2*i))))hit=false;if(hit){rejects++;let min=true;for(let i=0;i<k;i++)if((mask&(3<<(2*i)))===(3<<(2*i)))min=false;if(min)minimal++;}}if(rejects!==3**k||minimal!==2**k)throw Error("count");horn.push({k,assignments:2**(2*k),rejects,minimal})}
return {controls,fano:f,horn}}
// node checker.js [chart0.json ... chart4.json MS24.json BH18.json]
if(require.main===module){const fs=require("fs"),args=process.argv.slice(2);let out={tests:tests()};if(args.length===7){const a=args.map(p=>JSON.parse(fs.readFileSync(p)));out.jobs=a.slice(0,5).map((c,i)=>({baseline:analyze(c),combined:analyze(c,[a[5].jobs[i].combined,a[6].jobs.find(j=>j.ref===a[6].refs[i]&&j.mode===true)])}));}console.log(JSON.stringify(out,null,2));}
