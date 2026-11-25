const fs=require('fs');
const specs=[
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
  },
  {
    "ref": "bdda062d50962d29343f7413764acfdf5edbc21b",
    "path": "research/hcl201/interfaces/2026-11-25_0120_I25_orbit_results.json"
  }
];
function run(inputs,specs){
 const bit=i=>1n<<BigInt(i), assert=(x,m)=>{if(!x)throw Error(m)}, eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 function solve(o,imports=[],orbit=null){
  let R=o.rowMap.length,n=o.ownerIDs.length,own=o.rowMap.map(x=>x[0]),g=Array.from({length:n},()=>[]),p=o.pairHex.map(x=>BigInt("0x"+x)),live=o.live.slice(),ng=[];
  own.forEach((j,i)=>g[j].push(i));let bits=Array.from({length:R+1},(_,i)=>bit(i)),C=bits[R];
  let stats={acScans:0,unitScans:0,componentPairScans:0,gaussXor:0,linearRows:0,projectionJobs:0,rowTests:0,pairTests:0,sweeps:0},deletedRows=[],deletedPairs=[];
  function rel(a,b){return !!(p[a]&bits[b])}
  function ds(){return g.map(x=>x.filter(i=>live[i]))}
  function close(){for(;;){let d=ds(),m=d.map(a=>a.reduce((s,i)=>s|bits[i],0n));if(d.some(a=>!a.length))return false;let changed=false;
   for(let a=0;a<R;a++)if(live[a])for(let j=0;j<n;j++)if(j!==own[a]){stats.acScans++;if(!(p[a]&m[j])){live[a]=false;changed=true;break}}
   for(let t of ng){stats.unitScans++;if(t.some(a=>!live[a]))continue;for(let a of t)if(t.every(b=>a===b||d[own[b]].length===1&&d[own[b]][0]===b)){live[a]=false;changed=true}}
   if(!changed)return true;
  }}
  const count=()=>live.filter(Boolean).length, comps=[];
  let ok=close(),initial=count(),flip=[];
  if(orbit){let comp=s=>s.replace(/[01]/g,x=>x==="0"?"1":"0");for(let a of g){let m=new Map(a.filter(i=>live[i]).map(i=>[o.rowMap[i][1],i]));for(let i of a)if(live[i]){flip[i]=m.get(comp(o.rowMap[i][1]));assert(flip[i]!==undefined,"missing orbit")}}}
  function invariant(){if(!orbit)return;for(let a=0;a<R;a++)if(live[a]){assert(live[flip[a]],"live flip");for(let b=a+1;b<R;b++)if(live[b]&&own[a]!==own[b])assert(rel(a,b)===rel(flip[a],flip[b]),"pair flip")}}
  invariant();
  for(let u of imports){assert(eq(o.guard,u.guard),"guard mismatch");for(let i of u.removedRows||[]){live[i]=false;if(orbit)live[flip[i]]=false}
   for(let [i,h] of u.delta||[]){let mask=BigInt("0x"+h);for(let j=0;j<R;j++)if(mask&bits[j]){p[i]&=~bits[j];p[j]&=~bits[i];if(orbit&&flip[i]!==undefined&&flip[j]!==undefined){p[flip[i]]&=~bits[flip[j]];p[flip[j]]&=~bits[flip[i]]}}}
   ok=close();invariant();comps.push(count());}
  for(let u of imports)for(let v of u.nogoods||[]){let t=v.rows;if(t.every(i=>live[i])){ng.push(t);if(orbit)ng.push(t.map(i=>flip[i]))}}
  ok=close();invariant();
  if(orbit){for(let i of orbit.anchorRows)live[i]=false;ok=close();assert(eq(live.map((x,i)=>x?i:-1).filter(i=>i>=0),orbit.liveRows),"I25 anchor row mismatch")}
  let start=count(),ranks=[];
  const high=v=>v.toString(2).length-1;
  function insert(v,P){while(v){let h=high(v),b=P.get(h);if(!b){P.set(h,v);return true}v^=b;stats.gaussXor++}return false}
  function reduce(v,P){let out=0n;while(v){let h=high(v),b=P.get(h);if(b){v^=b;stats.gaussXor++}else{out|=bits[h];v^=bits[h]}}return out}
  for(let sweep=0;ok&&sweep<3;sweep++){
   stats.sweeps++;let d=ds(),P=new Map();
   for(let a of d){insert(a.reduce((v,i)=>v|bits[i],C),P);stats.linearRows++}
   for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
    let a=d[i],b=d[j],k=a.length+b.length,par=Array.from({length:k},(_,i)=>i);
    function root(x){while(x!==par[x])x=par[x];return x}
    for(let x=0;x<a.length;x++)for(let y=0;y<b.length;y++){stats.componentPairScans++;if(rel(a[x],b[y]))par[root(x)]=root(y+a.length)}
    let cc=new Map();[...a,...b].forEach((v,t)=>{let z=root(t);cc.set(z,(cc.get(z)||0n)|bits[v])});
    if(cc.size>1)for(let v of cc.values()){insert(v,P);stats.linearRows++}
   }
   ranks.push(P.size);
   if(reduce(C,P)===0n){ok=false;break}
   let red=bits.map(v=>reduce(v,P)),rowDel=[],pairDel=[];
   function dependencies(a){stats.projectionJobs++;let Q=new Map(),D=[];for(let i of [...a,R]){let v=red[i],w=bits[i];while(v){let h=high(v),q=Q.get(h);if(!q){Q.set(h,[v,w]);break}v^=q[0];w^=q[1];stats.gaussXor++}if(!v)D.push(w)}return D}
   function evalOK(D,x,y=-1){for(let w of D){let v=!!(w&C);v=v!==!!(w&bits[x]);if(y>=0)v=v!==!!(w&bits[y]);if(v)return false}return true}
   for(let i=0;i<n;i++){let D=dependencies(d[i]);for(let a of d[i]){stats.rowTests++;if(!evalOK(D,a))rowDel.push(a)}}
   if(!rowDel.length)for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let D=dependencies([...d[i],...d[j]]);if(!D.length)continue;for(let a of d[i])for(let b of d[j])if(rel(a,b)){stats.pairTests++;if(!evalOK(D,a,b))pairDel.push([a,b])}}
   if(!rowDel.length&&!pairDel.length)break;
   for(let a of rowDel){live[a]=false;deletedRows.push(a)}
   for(let [a,b] of pairDel){p[a]&=~bits[b];p[b]&=~bits[a];deletedPairs.push([a,b])}
   ok=close();
  }
  return {id:o.id,guard:o.guard,mode:orbit?"I25-anchor":imports.length?"combined":"baseline",initial,importRows:comps,start,end:count(),status:ok?"OPEN":"UNSAT",ranks,deletedRows,deletedPairs,stats};
 }
 let results=[];
 for(let k=0;k<5;k++){let o=inputs[k],ms=inputs[5].jobs[k].combined,bh=inputs[6].jobs.find(x=>x.mode===true&&x.ref===specs[k].ref);results.push(solve(o),solve(o,[ms,bh]));let or=inputs[7].tests[k];if(or.status==="OPEN")results.push(solve(o,[ms,bh],or));}
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],perm=[0,1,2,4,3,6,5,7],feature=Array(8);perm.forEach((v,i)=>feature[v]=[i>>2&1,i>>1&1,(i>>2&1)^(i>>1&1)]);
 function control(odd){let own=Array.from({length:32},(_,i)=>i>>3),rowMap=own.map((i,r)=>[i,(r%8).toString(2).padStart(3,"0")]),inc=Array.from({length:4},(_,i)=>edges.map((e,j)=>e.includes(i)?j:-1).filter(j=>j>=0));let f=(r,e)=>feature[r%8][inc[own[r]].indexOf(e)]^(odd&&own[r]===3&&inc[3].indexOf(e)===2?1:0);
  let pairHex=own.map((i,r)=>{let v=0n;for(let s=0;s<32;s++)if(i!==own[s]){let e=edges.findIndex(a=>a.includes(i)&&a.includes(own[s]));if(f(r,e)===f(s,e))v|=bit(s)}return v.toString(16)});
  let o={id:odd?"hidden-parity-UNSAT":"hidden-parity-SAT",ownerIDs:[0,1,2,3],rowMap,pairHex,guard:[],live:Array(32).fill(true)},models=0,pathFailures=0;
  for(let a=0;a<8;a++)for(let b=8;b<16;b++)for(let c=16;c<24;c++)for(let d=24;d<32;d++){let rr=[a,b,c,d];if(rr.every((r,i)=>rr.slice(i+1).every(s=>BigInt("0x"+pairHex[r])&bit(s))))models++}
  for(let r=0;r<32;r++)for(let s=r+1;s<32;s++)if(BigInt("0x"+pairHex[r])&bit(s))for(let i=0;i<4;i++)if(i!==own[r]&&i!==own[s]){let mask=255n<<BigInt(8*i);if(!(BigInt("0x"+pairHex[r])&BigInt("0x"+pairHex[s])&mask))pathFailures++}
  for(let j=0;j<3;j++)for(let b=0;b<2;b++){let x=feature.map((f,i)=>f[j]===b?i:-1).filter(i=>i>=0);assert(x.length===4&&x.reduce((z,y)=>z^y,0)!==0,"fiber not full")}
  let result=solve(o);assert((result.status==="UNSAT")===(models===0),"wrong control");assert(pathFailures===0,"path consistency");return {models,pathFailures,result};
 }
 return {specs,results,controls:[control(true),control(false)]};
}
const inputs=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));if(inputs.length!==specs.length)throw Error('eight inputs in listed order');console.log(JSON.stringify(run(inputs,specs),null,2));
