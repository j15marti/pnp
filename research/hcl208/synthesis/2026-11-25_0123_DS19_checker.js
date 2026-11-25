const fs=require('fs');
const files=[
  [
    "1fc8b6c7157cb8db0a0a9f26dee59ba74195aa9a",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_0.json"
  ],
  [
    "1e765e0e95ae0a6eeea5a1b43a5c8c525f82e5fd",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_1.json"
  ],
  [
    "80b472196e2bd606c45cd95bf2190618748d5606",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_2.json"
  ],
  [
    "37578c1135e1bade2d1c6847235cd61500092c58",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_3.json"
  ],
  [
    "33f9839bb80d205ad94af013b6141aeb119f8e87",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_4.json"
  ],
  [
    "ecbbf26c6a5d9b2b53f5942b1889131c3ebe1fce",
    "research/hcl201/multisign/2026-11-25_0028_MS24_results.json"
  ],
  [
    "ab85c853f3296c2423910ba3aee8b7db8189037c",
    "research/constructive-shared-hubs/hard-residuals/2026-11-25_0042_BH18_feedback_results.json"
  ]
];
function run(inputs,files){
 const assert=(x,m)=>{if(!x)throw Error(m||"assert")};
 function solve(o,updates=[],greedy=false,cap=1024){
  const n=o.ownerIDs.length,R=o.rowMap.length,owner=o.rowMap.map(x=>x[0]),bit=Array.from({length:R},(_,i)=>1n<<BigInt(i)),p=o.pairHex.map(x=>BigInt("0x"+x)),live=o.live.slice(),masks=Array(n).fill(0n),groups=Array.from({length:n},()=>[]);
  for(let i=0;i<R;i++){groups[owner[i]].push(i);if(live[i])masks[owner[i]]|=bit[i]}
  let stats={acScans:0,acDeletes:0,importRows:0,importPairs:0,tests:0,overflow:0,attempts:0,merges:0,peak:1},steps=[];
  function del(i){if(live[i]){live[i]=false;masks[owner[i]]&=~bit[i];return true}return false}
  function ac(){let change=true;while(change){change=false;if(masks.some(x=>!x))return false;for(let i=0;i<R;i++)if(live[i])for(let j=0;j<n;j++)if(j!==owner[i]){stats.acScans++;if(!(p[i]&masks[j])){del(i);stats.acDeletes++;change=true;break}}}return !masks.some(x=>!x)}
  function check(){for(let i=0;i<R;i++)if(live[i])for(let j=i+1;j<R;j++)if(live[j]&&owner[i]!==owner[j])assert(Boolean(p[i]&bit[j])===Boolean(p[j]&bit[i]),"asymmetric")}
  const result=(status,extra={})=>({id:o.id,guard:o.guard,greedy,cap,status,stats,steps,...extra});
  check();if(!ac())return result("UNSAT",{reason:"AC"});
  for(const u of updates){for(const i of u.removedRows||[])if(del(i))stats.importRows++;for(const [i,h] of u.delta||[]){let b=BigInt("0x"+h),x=p[i]&b;while(x){stats.importPairs++;x&=x-1n;}p[i]&=~b;}check();if(!ac())return result("UNSAT",{reason:"AC after import"})}
  const all=masks.reduce((a,b)=>a|b,0n),veto=p.map((x,i)=>all&(~x|masks[owner[i]]));
  let remaining=Array.from({length:n},(_,i)=>i),outside=all,states=new Map([[0n,[]]]);
  while(remaining.length){
   let best=null,bestOwner=-1,bestOutside=0n,counts=[];
   for(const j of greedy?remaining:[remaining[0]]){
    stats.attempts++;
    const out=outside&~masks[j],next=new Map();let over=false;
    outer:for(const [v,w] of states)for(const r of groups[j])if(live[r]){stats.tests++;if(v&bit[r])continue;const key=(v|veto[r])&out;if(next.has(key)){stats.merges++;continue;}next.set(key,[...w,r]);stats.peak=Math.max(stats.peak,next.size);if(next.size>cap){over=true;stats.overflow++;break outer}}
    counts.push([j,over?">"+cap:next.size]);
    if(over)continue;
    if(!next.size){steps.push({chosen:j,counts});return result("UNSAT",{reason:"empty exact table"})}
    if(best===null||next.size<best.size){best=next;bestOwner=j;bestOutside=out}
   }
   if(best===null){steps.push({chosen:null,counts});return result("DECLINE",{remaining,retained:states.size})}
   steps.push({chosen:bestOwner,states:best.size,counts});states=best;outside=bestOutside;remaining=remaining.filter(j=>j!==bestOwner)
  }
  const w=states.values().next().value;assert(w.length===n&&new Set(w.map(i=>owner[i])).size===n);assert(w.every(i=>live[i]&&w.every(j=>owner[i]===owner[j]||Boolean(p[i]&bit[j]))));
  return result("SAT",{witness:w.map(i=>[o.ownerIDs[owner[i]],o.rowMap[i][1],i])})
 }
 function chart(id,domains,compat){let rowMap=domains.flatMap((d,i)=>d.map(x=>[i,x]));return {id,guard:[],ownerIDs:domains.map((_,i)=>i),rowMap,live:rowMap.map(()=>true),pairHex:rowMap.map(([i,a])=>rowMap.reduce((z,[j,b],k)=>i!==j&&compat(i,a,j,b)?z|(1n<<BigInt(k)):z,0n).toString(16))}}
 function exhaustive(o){let ds=o.ownerIDs.map((_,i)=>o.rowMap.map((x,j)=>x[0]===i?j:-1).filter(x=>x>=0)),p=o.pairHex.map(x=>BigInt("0x"+x)),count=0;function f(a){if(a.length===ds.length){count++;return}for(let i of ds[a.length])if(a.every(j=>p[i]&(1n<<BigInt(j))))f([...a,i])}f([]);return count}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 let controls=[];for(let signed of [false,true]){let o=chart("Fano"+signed,fano.map((_,i)=>Array.from({length:8},(_,x)=>x).filter(x=>{let y=x^(signed&&i===0?1:0);return y!==0&&y!==7})),(i,a,j,b)=>fano[i].every((v,k)=>!fano[j].includes(v)||((a>>k)&1)===((b>>fano[j].indexOf(v))&1)));let count=exhaustive(o),fixed=solve(o),greedy=solve(o,[],true);assert(fixed.status===(count?"SAT":"UNSAT")&&greedy.status===fixed.status);controls.push({count,fixed,greedy})}
 let seed=19025;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 let random={sat:0,unsat:0,tests:0};for(let t=0;t<80;t++){let n=3+t%5,q=2+t%2,table=new Map();for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let a=0;a<q;a++)for(let b=0;b<q;b++)table.set([i,a,j,b].join(),rand()>.32);let o=chart("random"+t,Array.from({length:n},()=>Array.from({length:q},(_,i)=>i)),(i,a,j,b)=>i<j?table.get([i,a,j,b].join()):table.get([j,b,i,a].join())),count=exhaustive(o);for(let g of [false,true]){let v=solve(o,[],g);assert(v.status===(count?"SAT":"UNSAT"));random.tests+=v.stats.tests;}random[count?"sat":"unsat"]++}
 let k=12,o=chart("crossmatching",Array.from({length:2*k},()=>[0,1]),(i,a,j,b)=>!(Math.abs(i-j)===k&&a===1&&b===1));let fixed=solve(o,[],false,64),greedy=solve(o,[],true,64);assert(fixed.status==="DECLINE"&&greedy.status==="SAT");controls.push({fixed,greedy,known:"all zero"});
 const jobs=inputs.slice(0,5).map((o,i)=>{let ms=inputs[5].jobs[i].combined,bh=inputs[6].jobs.find(x=>x.mode===true&&x.ref===files[i][0]);assert(JSON.stringify(ms.guard)===JSON.stringify(o.guard)&&JSON.stringify(bh.guard)===JSON.stringify(o.guard));return {ref:files[i][0],baseline:[solve(o),solve(o,[],true)],combined:[solve(o,[ms,bh]),solve(o,[ms,bh],true)]}});
 return {files,controls,random,jobs};
}
const inputs=process.argv.slice(2).map(x=>JSON.parse(fs.readFileSync(x,'utf8')));if(inputs.length!==7)throw Error('seven files required');console.log(JSON.stringify(run(inputs,files),null,2));
