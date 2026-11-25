function compare(b,ms,bh,combined){
let n=b.rowMap.length,O=b.ownerIDs.length,L=b.live.slice(),P=b.pairHex.map(v=>BigInt("0x"+v)),bits=Array.from({length:n},(_,i)=>1n<<BigInt(i));let stats={scans:0,support:0,removed:0,edges:0,deltaReads:0};
const own=Array.from({length:O},()=>[]);b.rowMap.forEach(([j],i)=>own[j].push(i));
let masks=()=>own.map(a=>a.reduce((v,i)=>L[i]?v|bits[i]:v,0n));
function ac(){let again=true;while(again){again=false;stats.scans++;let M=masks();if(M.some(x=>!x))return false;for(let i=0;i<n;i++)if(L[i])for(let j=0;j<O;j++)if(j!==b.rowMap[i][0]){stats.support++;if(!(P[i]&M[j])){L[i]=false;stats.removed++;again=true;break}}}return true}
function delta(d){for(const i of d.removedRows||[]){L[i]=false;stats.deltaReads++}for(const [i,s] of d.delta||[]){P[i]&=~BigInt("0x"+s);stats.deltaReads++}}
if(!ac())return {id:b.id,guard:b.guard,combined,status:"UNSAT",stats};
if(combined){delta(ms);if(!ac())return {id:b.id,guard:b.guard,combined,status:"UNSAT",stats};delta(bh);if(!ac())return {id:b.id,guard:b.guard,combined,status:"UNSAT",stats}}
let M=masks(),adj=Array.from({length:O},()=>[]),asym=0;
for(let i=0;i<n;i++)if(L[i])for(let j=i+1;j<n;j++)if(L[j]&&b.rowMap[i][0]!==b.rowMap[j][0]){if(Boolean(P[i]&bits[j])!==Boolean(P[j]&bits[i]))asym++}
if(asym)throw Error("asymmetric live pair");
for(let i=0;i<O;i++)for(let j=i+1;j<O;j++){let blocked=own[i].some(r=>L[r]&&(P[r]&M[j])!==M[j]);stats.edges++;if(blocked){adj[i].push(j);adj[j].push(i)}}
let left=new Set(Array.from({length:O},(_,i)=>i)),components=[];
while(left.size){let i=left.values().next().value,q=[i];left.delete(i);for(let j=0;j<q.length;j++)for(let k of adj[q[j]])if(left.delete(k))q.push(k);components.push(q.map(i=>b.ownerIDs[i]))}
return {id:b.id,guard:b.guard,combined,live:L.filter(Boolean).length,components,constrainedEdges:adj.reduce((a,b)=>a+b.length,0)/2,status:components.length>1?"EXACT AND SPLIT":"OPEN",stats}
}
// Run node with five immutable BD18 JSON files in order, followed by MS24 and BH18 result JSON.
const fs=require('fs');const a=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));const ms=a[5],bh=a[6];const result=[];for(let i=0;i<5;i++){const d=bh.jobs.find(j=>j.ref===ms.refs[i]&&j.mode===true);if(JSON.stringify(a[i].guard)!==JSON.stringify(ms.jobs[i].combined.guard)||JSON.stringify(a[i].guard)!==JSON.stringify(d.guard))throw Error('guard mismatch');result.push(compare(a[i],ms.jobs[i].combined,d,false),compare(a[i],ms.jobs[i].combined,d,true))}console.log(JSON.stringify(result,null,2));
