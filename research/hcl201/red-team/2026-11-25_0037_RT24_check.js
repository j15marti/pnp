function analyze(d,delta=[]){
 const n=d.rowMap.length, live=d.live.slice(), masks=d.pairHex.map(s=>BigInt("0x"+(s||"0"))), bit=Array.from({length:n},(_,i)=>1n<<BigInt(i)), groups=d.ownerIDs.map((_,i)=>d.rowMap.map((v,j)=>v[0]===i?j:-1).filter(j=>j>=0&&live[j]));
 for(const [r,h] of delta){const v=BigInt("0x"+h);if((masks[r]&v)!==v)throw Error("non-subset delta");masks[r]&=~v;}
 let checks=0,removed=0,rounds=0,xors=0,eqs=0,components=0,probes=0;
 const has=(r,s)=>(masks[r]&bit[s])!==0n;
 for(let r=0;r<n;r++)if(live[r])for(let s=r+1;s<n;s++)if(live[s]&&d.rowMap[r][0]!==d.rowMap[s][0]){checks++;if(has(r,s)!==has(s,r))throw Error("asymmetry");}
 const rhs=1n<<BigInt(n);
 function closure(){let change=true;while(change){change=false;rounds++;const gm=groups.map(g=>g.reduce((a,j)=>live[j]?a|bit[j]:a,0n));for(let i=0;i<groups.length;i++){if(!gm[i])return false;for(const r of groups[i])if(live[r])for(let j=0;j<groups.length;j++)if(i!==j){checks++;if(!(masks[r]&gm[j])){live[r]=false;removed++;change=true;break;}}}}return true}
 if(!closure())return {label:"UNSAT",removed,rounds,checks};
 const B=new Map();let bad=false;
 function add(a,b){eqs++;let v=a|(b?rhs:0n);while(v& (rhs-1n)){const p=(v&(rhs-1n)).toString(2).length-1;if(B.has(p)){v^=B.get(p);xors++;}else{B.set(p,v);return;}}if(v&rhs)bad=true;}
 const g=groups.map(a=>a.filter(r=>live[r]));
 for(const a of g)add(a.reduce((v,r)=>v|bit[r],0n),1);
 for(let i=0;i<g.length;i++)for(let j=i+1;j<g.length;j++){
   const a=g[i],b=g[j], bm=b.reduce((v,r)=>v|bit[r],0n);
   const parent=new Map([...a,...b].map(r=>[r,r]));function find(x){while(parent.get(x)!==x){parent.set(x,parent.get(parent.get(x)));x=parent.get(x);}return x;}
   for(const r of a){let x=masks[r]&bm;while(x){const low=x&-x,s=low.toString(2).length-1;checks++;const p=find(r),q=find(s);if(p!==q)parent.set(p,q);x^=low;}}
   const cm=new Map();for(const r of [...a,...b]){const p=find(r);cm.set(p,(cm.get(p)||0n)|bit[r]);}
   components+=cm.size;for(const v of cm.values())add(v,0);
 }
 if(bad)return {label:"UNSAT",n,live:live.filter(Boolean).length,rank:B.size,eqs,components,checks,xors,removed,rounds};
 // Extract affine expressions for selectors in free selectors, then test impossible singleton/pair choices.
 const expr=Array(n);for(let r=0;r<n;r++){if(!live[r]){expr[r]=0n;continue;}if(!B.has(r)){expr[r]=bit[r];continue;}let v=B.get(r)^bit[r],z=v&rhs;v&=rhs-1n;while(v){const low=v&-v,j=low.toString(2).length-1;z^=expr[j];xors++;v^=low;}expr[r]=z;}
 const forced0=[],forced1=[];for(let r=0;r<n;r++)if(live[r]){if(expr[r]===0n)forced0.push(r);if(expr[r]===rhs)forced1.push(r);}
 const pairImpossible=[];for(let r=0;r<n;r++)if(live[r])for(let s=r+1;s<n;s++)if(live[s]&&d.rowMap[r][0]!==d.rowMap[s][0]&&has(r,s)){probes++;if(expr[r]===0n||expr[s]===0n||(expr[r]^expr[s])===rhs)pairImpossible.push([r,s]);}
 return {label:"OPEN",n,live:live.filter(Boolean).length,rank:B.size,eqs,components,checks,xors,removed,rounds,probes,forced0,forced1,pairImpossible};
}

function wheel(k,drop=-1){const n=k+1, edges=[];for(let i=0;i<k;i++){edges.push([i,(i+1)%k]);edges.push([i,k]);}const es=edges.filter((_,i)=>i!==drop);const adj=new Set(es.map(([a,b])=>[Math.min(a,b),Math.max(a,b)].join(",")));const rowMap=Array.from({length:3*n},(_,i)=>[Math.floor(i/3),String(i%3)]);const pairHex=rowMap.map(([a,c])=>rowMap.reduce((v,[b,d],j)=>a!==b&&(!adj.has([Math.min(a,b),Math.max(a,b)].join(","))||c!==d)?v|(1n<<BigInt(j)):v,0n).toString(16));return {ownerIDs:Array.from({length:n},(_,i)=>i),rowMap,live:rowMap.map(()=>true),pairHex,edges:es};}

function wheelCount(d){let z=0,visits=0;const n=d.ownerIDs.length;for(let t=0;t<3**n;t++){let q=t;const x=[];for(let i=0;i<n;i++){x.push(q%3);q=Math.floor(q/3);}visits++;if(d.edges.every(([a,b])=>x[a]!==x[b]))z++;}return {z,visits};}

function majorityGraph(k,odd){ // prism, 2k nodes, degree 3
 const n=2*k,edges=[];for(let i=0;i<k;i++){edges.push([i,(i+1)%k]);edges.push([i+k,((i+1)%k)+k]);edges.push([i,i+k]);}
 const inc=Array.from({length:n},()=>[]);edges.forEach(([a,b],j)=>{inc[a].push(j);inc[b].push(j)});
 const maj=w=>(((w&1)+((w>>1)&1)+((w>>2)&1))>=2?1:0);
 const rowMap=[],words=[];for(let i=0;i<n;i++)for(let w=0;w<512;w++)if((maj(w&7)^maj((w>>3)&7)^maj((w>>6)&7))===(i===0?odd:0)){rowMap.push([i,w.toString(2).padStart(9,"0")]);words.push(w);}
 const g=inc.map((_,i)=>rowMap.map((r,j)=>r[0]===i?j:-1).filter(j=>j>=0));const bits=rowMap.map((_,i)=>1n<<BigInt(i));const gm=g.map(a=>a.reduce((v,r)=>v|bits[r],0n));
 const pairHex=rowMap.map(([i],r)=>{let z=0n;for(let j=0;j<n;j++)if(i!==j){const p=inc[i].findIndex(e=>inc[j].includes(e));if(p<0)z|=gm[j];else{const q=inc[j].indexOf(inc[i][p]);for(const s of g[j])if(((words[r]>>(3*p))&7)===((words[s]>>(3*q))&7))z|=bits[s];}}return z.toString(16)});
 // exact phase enumeration, with multiplicity 4 per edge, independently of selector solver
 let phaseCount=0;for(let x=0;x<2**edges.length;x++)if(inc.every((a,i)=>a.reduce((v,j)=>v^((x>>j)&1),0)===(i===0?odd:0)))phaseCount++;
 return {ownerIDs:inc.map((_,i)=>i),rowMap,live:rowMap.map(()=>true),pairHex,phaseCount,modelCount:(BigInt(phaseCount)*4n**BigInt(edges.length)).toString(),edgeCount:edges.length};
}
// node 2026-11-25_0037_RT24_check.js <directory containing immutable inputs named pairs_0.json ... pairs_4.json, ms.json>
const fs=require("fs"), dir=process.argv[2];
const refs=["1fc8b6c7157cb8db0a0a9f26dee59ba74195aa9a","1e765e0e95ae0a6eeea5a1b43a5c8c525f82e5fd","80b472196e2bd606c45cd95bf2190618748d5606","37578c1135e1bade2d1c6847235cd61500092c58","33f9839bb80d205ad94af013b6141aeb119f8e87"];
const peer=JSON.parse(fs.readFileSync(dir+"/ms.json","utf8"));const jobs=[];for(let i=0;i<5;i++){const d=JSON.parse(fs.readFileSync(dir+"/pairs_"+i+".json","utf8"));jobs.push({id:d.id,guard:d.guard,ref:refs[i],before:analyze(d),after:analyze(d,peer.jobs[i].combined.delta)});}const controls=[];for(const k of [3,5,7])for(const drop of [-1,0,1]){const d=wheel(k,drop);controls.push({kind:"wheel",k,drop,reference:wheelCount(d),analysis:analyze(d)});}for(const odd of [0,1]){const d=majorityGraph(3,odd);controls.push({kind:"majority-prism",odd,phaseCount:d.phaseCount,modelCount:d.modelCount,analysis:analyze(d)});}console.log(JSON.stringify({refs,msRef:"ecbbf26c6a5d9b2b53f5942b1889131c3ebe1fce",jobs,controls},null,2));
