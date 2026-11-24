function runBA01(){
const assert=(b,m)=>{if(!b)throw Error(m)};
const uniq=a=>[...new Set(a)];
const xor=a=>a.reduce((x,y)=>x^y,0n);
function basis(a){let b=[];for(let x of a){for(const y of b)if((x^y)<x)x^=y;if(x){b.push(x);b.sort((u,v)=>u>v?-1:u<v?1:0)}}return b}
function red(x,b){for(const y of b)if((x^y)<x)x^=y;return x}
function period(a){let s=new Set(a);return basis(a.map(x=>x^a[0]).filter(p=>a.every(x=>s.has(x^p))))}
function hull(fs){return [xor(fs.map(a=>a[0])),basis(fs.flatMap(a=>a.map(x=>x^a[0])))]}
function cutwidth(fs){let v=fs.map(a=>a.map(x=>x^a[0])),r=basis(v.flat()).length,w=0;for(let i=0;i<=fs.length;i++)w=Math.max(w,basis(v.slice(0,i).flat()).length+basis(v.slice(i).flat()).length-r);return w}
function solve(original,originalTarget,cap=8){
 let fs=original.map(uniq),target=originalTarget,trace=[];
 let stats={deleted:0,quotients:0,removedRank:0,merges:0,pairTrials:0,periodTrials:0,dpEdges:0,dpStates:0,maxStates:0,initialWidth:0,finalWidth:0};
 const finish=w=>({w,stats});
 if(fs.some(a=>!a.length))return finish(null);
 stats.initialWidth=cutwidth(fs);
 for(;;){
  let changed=true;
  while(changed){changed=false;
   for(let i=0;i<fs.length;i++){
    let [a,b]=hull(fs.filter((_,j)=>j!==i));
    let keep=fs[i].filter(x=>red(target^a^x,b)===0n);
    stats.deleted+=fs[i].length-keep.length;
    if(!keep.length)return finish(null);
    if(keep.length<fs[i].length){fs[i]=keep;changed=true;break}
   }
  }
  let chosen=-1,p=[];
  for(let i=0;i<fs.length;i++){stats.periodTrials++;let q=period(fs[i]);if(q.length){chosen=i;p=q;break}}
  if(chosen>=0){
   trace.push({type:"quotient",fs:fs.map(a=>a.slice()),target,i:chosen,p});
   target=red(target,p);fs=fs.map(a=>uniq(a.map(x=>red(x,p))));stats.quotients++;stats.removedRank+=p.length;continue
  }
  let merged=false;
  outer:for(let i=0;i<fs.length;i++)for(let j=i+1;j<fs.length;j++){
   stats.pairTrials++;
   let pairs=new Map();for(let x of fs[i])for(let y of fs[j]){let z=x^y;if(!pairs.has(z))pairs.set(z,[x,y])}
   let a=[...pairs.keys()];if(a.length>cap||!period(a).length)continue;
   trace.push({type:"merge",i,j,pairs});fs[i]=a;fs.splice(j,1);stats.merges++;merged=true;break outer
  }
  if(!merged)break;
 }
 stats.finalWidth=cutwidth(fs);
 let dp=new Map([[0n,[]]]);
 for(let i=0;i<fs.length;i++){
  let [a,b]=hull(fs.slice(i+1)),next=new Map();
  for(let [s,w] of dp)for(let x of fs[i]){
   stats.dpEdges++;let t=s^x;
   if(red(target^t^a,b)===0n&&!next.has(t))next.set(t,[...w,x])
  }
  dp=next;stats.dpStates+=dp.size;stats.maxStates=Math.max(stats.maxStates,dp.size);
  assert(dp.size<=2**stats.finalWidth,"cut width");
  if(!dp.size)return finish(null)
 }
 let w=dp.get(target);if(w===undefined)return finish(null);
 for(let k=trace.length-1;k>=0;k--){
  let t=trace[k];
  if(t.type==="merge"){let [x,y]=t.pairs.get(w[t.i]);w[t.i]=x;w.splice(t.j,0,y)}
  else{
   let v=w.map((x,i)=>t.fs[i].find(y=>red(y,t.p)===x));
   assert(v.every(x=>x!==undefined),"quotient representatives");
   let d=t.target^xor(v);assert(red(d,t.p)===0n,"delta in period");
   v[t.i]^=d;assert(t.fs[t.i].includes(v[t.i]),"period lift");w=v
  }
 }
 assert(w.length===original.length&&w.every((x,i)=>original[i].includes(x))&&xor(w)===originalTarget,"original witness");
 return finish(w)
}
let seed=0xBA010730;
function rng(n){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}
function brute(fs,t){let found=false,count=0;function rec(i,s){if(i===fs.length){count++;if(s===t)found=true;return}for(let x of fs[i])rec(i+1,s^x)}rec(0,0n);return{found,count}}
let totals={cases:0,sat:0,unsat:0,referenceTuples:0,deleted:0,quotients:0,removedRank:0,merges:0,pairTrials:0,periodTrials:0,dpEdges:0,dpStates:0};
function compare(fs,t){let r=solve(fs,t),b=brute(fs,t);assert((r.w!==null)===b.found,"random decision");totals.cases++;totals[b.found?"sat":"unsat"]++;totals.referenceTuples+=b.count;for(let k of Object.keys(r.stats))if(k in totals)totals[k]+=r.stats[k];return r}
for(let k=0;k<240;k++){let d=3+rng(5),n=2+rng(5),fs=Array.from({length:n},()=>uniq(Array.from({length:1+rng(5)},()=>BigInt(rng(2**d)))));let t=k%2?xor(fs.map(a=>a[rng(a.length)])):BigInt(rng(2**d));compare(fs,t)}
function compile(n,clauses){
 let occurrences=Array.from({length:n},()=>[]),tags=clauses.map(()=>[0n,0n,0n]);for(let i=0;i<clauses.length;i++)for(let j=0;j<3;j++)occurrences[clauses[i].v[j]].push([i,j]);
 let q=0;for(let os of occurrences)for(let k=1;k<os.length;k++){let [i,j]=os[0],[u,v]=os[k],b=1n<<BigInt(q++);tags[i][j]^=b;tags[u][v]^=b}
 let maps=clauses.map((c,i)=>{let m=new Map();for(let z=0;z<8;z++)if(c.allowed.includes(z)){let tag=xor(tags[i].filter((_,j)=>(z>>j)&1));if(!m.has(tag))m.set(tag,z)}return m});
 return {fs:maps.map(m=>[...m.keys()]),maps,q}
}
function verifyFormula(n,clauses,label){let {fs,maps,q}=compile(n,clauses),r=solve(fs,0n),count=0;for(let x=0;x<2**n;x++)if(clauses.every(c=>c.allowed.includes(c.v.reduce((z,v,j)=>z|(((x>>v)&1)<<j),0))))count++;
 assert((r.w!==null)===(count>0),"formula decision");
 if(r.w){let x=Array(n).fill(null);for(let i=0;i<clauses.length;i++){let z=maps[i].get(r.w[i]);for(let j=0;j<3;j++){let v=clauses[i].v[j],b=(z>>j)&1;assert(x[v]===null||x[v]===b,"occurrence lift");x[v]=b}}assert(clauses.every(c=>c.allowed.includes(c.v.reduce((z,v,j)=>z|(x[v]<<j),0))),"lift verification")}
 return {label,n,m:clauses.length,q,models:count,sat:r.w!==null,...r.stats}
}
const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const fano=lines.map(v=>({v,allowed:[1,2,3,4,5,6]}));
const controls=[verifyFormula(7,fano,"Fano UNSAT")];
for(let i=0;i<7;i++)for(let z of [0,7])controls.push(verifyFormula(7,fano.map((c,j)=>j===i?{v:c.v,allowed:[...c.allowed,z]}:c),"Fano relax "+i+" "+z));
let signed=[];for(let i=0;i<40;i++){let n=4+rng(4),m=3+rng(7),cs=[];for(let j=0;j<m;j++){let v=[];while(v.length<3){let k=rng(n);if(!v.includes(k))v.push(k)}let mask=rng(8);cs.push({v,allowed:Array.from({length:8},(_,z)=>z).filter(z=>z!==mask&&z!==(mask^7))})}signed.push(verifyFormula(n,cs,"signed NAE "+i))}
let scaling=[];for(let k of [2,4,8,16,32]){let a=Array.from({length:k},(_,i)=>{let u=1n<<BigInt(2*i),v=u<<1n;return [0n,u,v]});let fs=[...a,...a.map(x=>x.slice()),...a.map(x=>x.slice())],t=(1n<<BigInt(2*k))-1n;let r=solve(fs,t);assert(r.w!==null&&r.stats.removedRank===2*k&&r.stats.finalWidth===0,"three-copy scaling");scaling.push({k,blocks:3*k,rawRank:2*k,...r.stats})}
let two=solve([[0n,1n,2n],[0n,1n,2n]],3n);assert(two.w!==null&&two.stats.merges===1&&two.stats.finalWidth===0,"two-copy saturation");
let hostile=compare([[0n,1n,2n],[0n,4n,8n]],15n);assert(hostile.w===null,"hull false positive");
let unpinned=compare([[0n,1n],[0n]],1n),pinned=compare([[0n],[0n]],1n);assert(unpinned.w!==null&&pinned.w===null,"guard period invalidation");
return {seed:"0xBA010730",totals,controls,signed:{cases:signed.length,sat:signed.filter(x=>x.sat).length,unsat:signed.filter(x=>!x.sat).length,referenceAssignments:signed.reduce((a,x)=>a+2**x.n,0),details:signed},scaling,two:two.stats,hostile:hostile.stats,guard:{unpinned:unpinned.stats,pinned:pinned.stats},discrepancies:0}
}
console.log(JSON.stringify(runBA01(),null,2));
