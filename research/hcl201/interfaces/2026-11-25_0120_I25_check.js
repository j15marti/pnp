// Node.js: seven immutable JSON inputs, ordered as results.files.
const fs=require('fs');
const files=[
  {
    "ref": "1fc8b6c7157cb8db0a0a9f26dee59ba74195aa9a",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_0.json"
  },
  {
    "ref": "1e765e0e95ae0a6eeea5a1b43a5c8c525f82e5fd",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_1.json"
  },
  {
    "ref": "80b472196e2bd606c45cd95bf2190618748d5606",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_2.json"
  },
  {
    "ref": "37578c1135e1bade2d1c6847235cd61500092c58",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_3.json"
  },
  {
    "ref": "33f9839bb80d205ad94af013b6141aeb119f8e87",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_4.json"
  },
  {
    "ref": "ecbbf26c6a5d9b2b53f5942b1889131c3ebe1fce",
    "path": "research/hcl201/multisign/2026-11-25_0028_MS24_results.json"
  },
  {
    "ref": "ab85c853f3296c2423910ba3aee8b7db8189037c",
    "path": "research/constructive-shared-hubs/hard-residuals/2026-11-25_0042_BH18_feedback_results.json"
  }
];
function run(inputs,files){
 const assert=(x,m)=>{if(!x)throw Error(m||"assertion")};
 const bit=i=>1n<<BigInt(i),par=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
 const comp=s=>s.replace(/[01]/g,c=>c==="0"?"1":"0");
 function analyze(o,updates=[],nogoods=[],exhaust=false){
  const n=o.ownerIDs.length,R=o.rowMap.length,own=o.rowMap.map(a=>a[0]),live=o.live.slice(),p=o.pairHex.map(x=>BigInt("0x"+x)),groups=Array.from({length:n},()=>[]);
  own.forEach((x,i)=>groups[x].push(i));const stats={acChecks:0,ternaryChecks:0,symmetryChecks:0,gaussXor:0,upstreamRows:0,importedBits:0,closureRemoved:0,anchorRemoved:0};
  let ng=[],steps=[];
  function rel(a,b){return !!(p[a]&bit(b))}
  function check(){for(let a=0;a<R;a++)if(live[a])for(let b=a+1;b<R;b++)if(live[b]&&own[a]!==own[b])assert(rel(a,b)===rel(b,a),"pair symmetry")}
  function closure(){let ch=true;while(ch){ch=false;let g=groups.map(a=>a.filter(i=>live[i]));if(g.some(a=>!a.length))return false;let gm=g.map(a=>a.reduce((z,i)=>z|bit(i),0n));for(let a=0;a<R;a++)if(live[a])for(let j=0;j<n;j++)if(j!==own[a]){stats.acChecks++;if(!(p[a]&gm[j])){live[a]=false;stats.closureRemoved++;ch=true;break}}
   for(const t of ng){stats.ternaryChecks++;if(t.some(a=>!live[a]))continue;for(const a of t){if(t.every(b=>a===b||g[own[b]].length===1&&g[own[b]][0]===b)){live[a]=false;stats.closureRemoved++;ch=true;break}}}
  }return groups.every(a=>a.some(i=>live[i]))}
  function count(){let z=0;let ds=groups.map(a=>a.filter(i=>live[i]));function rec(a){if(a.length===n){if(!ng.some(t=>t.every(i=>a.includes(i))))z++;return}for(let i of ds[a.length])if(a.every(j=>rel(i,j)))rec([...a,i])}rec([]);return z}
  check();let initial=live.filter(Boolean).length;if(!closure())return {id:o.id,guard:o.guard,status:"UNSAT",initial,stats,steps};
  for(const u of updates){for(const i of u.removedRows||[])if(live[i]){live[i]=false;stats.upstreamRows++}for(const [i,h] of u.delta||[]){const b=BigInt("0x"+h);let x=p[i]&b;while(x){stats.importedBits++;x&=x-1n}p[i]&=~b}check();if(!closure())return {id:o.id,guard:o.guard,status:"UNSAT",initial,stats,steps}}
  ng=nogoods.map(x=>x.rows.slice());for(const t of ng)assert(t.length===3&&new Set(t.map(i=>own[i])).size===3&&t.every(i=>i>=0&&i<R),"bad nogood");
  if(!closure())return {id:o.id,guard:o.guard,status:"UNSAT",initial,stats,steps};
  const pre=live.filter(Boolean).length,initialCount=exhaust?count():null;
  function gauge(){
   const g=groups.map(a=>a.filter(i=>live[i])),flip=Array(R).fill(-1),eligible=g.map(a=>{let m=new Map(a.map(i=>[o.rowMap[i][1],i]));if(m.size!==a.length)return false;for(const i of a){let s=o.rowMap[i][1],j=m.get(comp(s));if(!/^[01]+$/.test(s)||j===undefined||j===i)return false;flip[i]=j}return true});
   let eq=[],localFailures=0;
   for(let i=0;i<n;i++)if(!eligible[i])eq.push(bit(i));
   // Convert each finite local stabilizer to its annihilator; verify subgroup cardinality.
   function add(scope,H){assert(H.includes(0));for(const a of H)for(const b of H)assert(H.includes(a^b),"not subgroup");for(let y=1;y<(1<<scope.length);y++)if(H.every(x=>par(BigInt(x&y))===0)){let z=0n;scope.forEach((v,k)=>{if(y&(1<<k))z|=bit(v)});eq.push(z)}}
   for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let H=[];for(let m=0;m<4;m++){if((m&1)&&!eligible[i]||(m&2)&&!eligible[j])continue;let ok=true;outer:for(const a of g[i])for(const b of g[j]){stats.symmetryChecks++;if(rel(a,b)!==rel(m&1?flip[a]:a,m&2?flip[b]:b)){ok=false;break outer}}if(ok)H.push(m)}if(H.length===1)localFailures++;add([i,j],H)}
   const scopes=new Map();for(const t of ng){if(t.some(i=>!live[i]))continue;let z=t.slice().sort((a,b)=>own[a]-own[b]),s=z.map(i=>own[i]),key=s.join(",");if(!scopes.has(key))scopes.set(key,{s,T:new Set()});scopes.get(key).T.add(z.join(","))}
   for(const {s,T} of scopes.values()){let H=[];for(let m=0;m<8;m++){if(s.some((i,k)=>m&(1<<k)&&!eligible[i]))continue;let ok=true;for(const v of T){let z=v.split(",").map(Number).map((i,k)=>m&(1<<k)?flip[i]:i);stats.symmetryChecks++;if(!T.has(z.join(","))){ok=false;break}}if(ok)H.push(m)}add(s,H)}
   let rows=eq.slice(),rank=0,piv=[];for(let j=0;j<n;j++){let k=rows.findIndex((a,i)=>i>=rank&&!!(a&bit(j)));if(k<0)continue;[rows[k],rows[rank]]=[rows[rank],rows[k]];for(let i=0;i<rows.length;i++)if(i!==rank&&rows[i]&bit(j)){rows[i]^=rows[rank];stats.gaussXor++}piv.push(j);rank++}
   const free=Array.from({length:n},(_,i)=>i).filter(i=>!piv.includes(i));
   const basis=free.map(j=>{let z=bit(j);piv.forEach((i,k)=>{if(rows[k]&bit(j))z|=bit(i)});assert(eq.every(a=>par(a&z)===0),"basis invalid");return z});
   assert(free.every(i=>eligible[i]));
   return {eligible:eligible.filter(Boolean).length,rank:free.length,anchors:free,basis:basis.map(x=>x.toString(16)),localFailures,eqCount:eq.length,flip};
  }
  for(let round=0;round<=R;round++){
   let z=gauge(),before=exhaust?count():null;const {flip,...cert}=z;steps.push({...cert,before,live:live.filter(Boolean).length});
   if(!z.rank)break;
   for(const i of z.anchors){for(const a of groups[i])if(live[a]&&o.rowMap[a][1]>o.rowMap[flip[a]][1]){live[a]=false;stats.anchorRemoved++}}
   let ok=closure(),after=exhaust?count():null;steps.at(-1).after=after;
   if(exhaust)assert(BigInt(before)===BigInt(after)*(1n<<BigInt(z.rank)),"orbit count");
   if(!ok)return {id:o.id,guard:o.guard,status:"UNSAT",initial,pre,stats,steps,initialCount,finalCount:after};
   if(round===R)throw Error("round cap");
  }
  const g=groups.map(a=>a.filter(i=>live[i])),word=g.every(a=>a.length===1)?g.map(a=>a[0]):null;
  if(word)assert(word.every(a=>word.every(b=>own[a]===own[b]||rel(a,b)))&&!ng.some(t=>t.every(i=>word.includes(i))));
  return {id:o.id,guard:o.guard,status:word?"SAT":"OPEN",initial,pre,final:live.filter(Boolean).length,stats,steps,initialCount,finalCount:exhaust?count():null,word,nogoods:ng.length};
 }
 function chart(id,domains,compat){const rowMap=domains.flatMap((d,i)=>d.map(s=>[i,s]));return {id,guard:[],ownerIDs:domains.map((_,i)=>i),rowMap,live:rowMap.map(()=>true),pairHex:rowMap.map(([i,a])=>rowMap.reduce((z,[j,b],k)=>i!==j&&compat(i,a,j,b)?z|bit(k):z,0n).toString(16))}}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 let controls=[];
 for(const signed of [false,true]){const o=chart("Fano"+signed,fano.map((_,i)=>Array.from({length:8},(_,x)=>x.toString(2).padStart(3,"0")).filter(s=>{let t=parseInt(s,2)^(signed&&i===0?1:0);return t!==0&&t!==7})),(i,a,j,b)=>fano[i].every((v,k)=>!fano[j].includes(v)||a[k]===b[fano[j].indexOf(v)]));let z=analyze(o,[],[],true);assert(z.initialCount===(signed?10:0));controls.push(z)}
 for(let n of [3,4,5,6])for(let odd of [false,true]){const o=chart(`cycle${n}-${odd}`,Array.from({length:n},()=>["0","1"]),(i,a,j,b)=>Math.abs(i-j)===1?a===b:Math.abs(i-j)===n-1?((a!==b)===odd):true);let z=analyze(o,[],[],true);assert(z.initialCount===(odd?0:2));controls.push(z)}
 // All orbit pairs are nonempty, and a fixed orbit word gives XOR edges only.
 // reference owner 0, variable owners 1..n, clause owners n+1..n+m.
 function phaseCNF(n,clauses){const dom=[["0","1"],...Array.from({length:n},()=>["0","1"]),...clauses.map(c=>c.flatMap((_,k)=>{let s=(k+1).toString(2).padStart(2,"0")+"0";return [s,comp(s)]}))];return chart("phaseCNF",dom,(i,a,j,b)=>{if(i>j)return compatible(j,b,i,a);return compatible(i,a,j,b)});function compatible(i,a,j,b){if(j<=n)return true;const phase=Number(b.at(-1)),base=phase?comp(b):b,k=parseInt(base.slice(0,2),2)-1,lit=clauses[j-n-1][k];if(i===0)return Number(a)===phase;if(i<=n&&Math.abs(lit)===i)return (Number(a)^phase)===(lit>0?1:0);return true}}
 for(const unsat of [false,true]){let cls=Array.from({length:unsat?8:7},(_,k)=>[1,2,3].map((x,j)=>(k&(1<<j))?-x:x));const o=phaseCNF(3,cls),z=analyze(o,[],[],true);assert((z.initialCount>0)===!unsat);controls.push(z)}
 let jobs=inputs.slice(0,5).map((o,i)=>{let ms=inputs[5].jobs[i].combined,bh=inputs[6].jobs.find(x=>x.mode===true&&x.ref===files[i].ref);assert(JSON.stringify(ms.guard)===JSON.stringify(o.guard)&&JSON.stringify(bh.guard)===JSON.stringify(o.guard));return {ref:files[i].ref,baseline:analyze(o),combined:analyze(o,[ms,bh],bh.nogoods||[])}});
 return {files,controls,jobs};
}
const inputs=process.argv.slice(2).map(x=>JSON.parse(fs.readFileSync(x,'utf8')));if(inputs.length!==7)throw Error('seven inputs required');console.log(JSON.stringify(run(inputs,files),null,2));
