function run(){
const stats={assertions:0,closurePasses:0,edgeScans:0,domainDeletions:0,bruteAssignments:0,verifiedLifts:0,periodCandidates:0,periodWordChecks:0,shapes:[],scale:[],signed:0};
function ck(x){stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)}
function tree(t,shape){
 const ch=Array.from({length:t},()=>[-1,-1,-1]);let slots=[[0,0],[0,1],[0,2]];
 for(let i=1;i<t;i++){let k=shape==="path"?slots.length-1:0;let [p,j]=slots.splice(k,1)[0];ch[p][j]=i;slots.push([i,0],[i,1],[i,2]);}
 let b=1;for(let i=0;i<t;i++)for(let j=0;j<3;j++)if(ch[i][j]<0)ch[i][j]=t+b++;
 const edges=[[0,t],...ch.flatMap((a,i)=>a.map(j=>[i,j]))];return {t,ch,b,edges}
}
function close(g,bound,signs){let m=Array(g.t+g.b).fill(15);if(bound)bound.forEach((c,j)=>m[g.t+j]=1<<c);let change=true;while(change){change=false;stats.closurePasses++;for(let k=0;k<g.edges.length;k++){let [u,v]=g.edges[k],s=signs[k];stats.edgeScans++;for(let [a,b] of [[u,v],[v,u]]){if(!m[b])return null;if((m[b]&(m[b]-1))===0){let next=m[a]&~(1<<((31-Math.clz32(m[b]))^s));if(next!==m[a]){stats.domainDeletions++;m[a]=next;change=true;}if(!next)return null}}}}return m}
function lift(g,m,signs){let a=Array(m.length).fill(-1);a[0]=[0,1,2,3].find(c=>m[0]&(1<<c));for(let k=0;k<g.edges.length;k++){let [u,v]=g.edges[k];a[v]=[0,1,2,3].find(c=>(m[v]&(1<<c))&&c!==(a[u]^signs[k]));ck(a[v]!==undefined)}ck(g.edges.every(([u,v],k)=>(a[u]^a[v])!==signs[k]));stats.verifiedLifts++;return a}
function brute(g,bound,signs){for(let w=0;w<4**g.t;w++){stats.bruteAssignments++;const a=Array.from({length:g.t},(_,i)=>(w>>(2*i))&3).concat(bound);if(g.edges.every(([u,v],k)=>(a[u]^a[v])!==signs[k]))return true}return false}
function classify(g,bound){const a=Array(g.t).fill(0),keys=Array(g.t);let ok=true;for(let i=g.t-1;i>=0;i--){let x=g.ch[i].map(j=>j<g.t?a[j]:bound[j-g.t]);a[i]=x[0]^x[1]^x[2];if(new Set(x).size!==3)ok=false;keys[i]=x.findIndex(c=>c===(a[i]^1))}if(a[0]!==bound[0])ok=false;return {bad:ok,key:keys.join("")}}
function rank(vs){let b=new Map();for(let v of vs){while(v){let p=31-Math.clz32(v);if(b.has(p))v^=b.get(p);else{b.set(p,v);break}}}return b.size}
const perms=[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]];
function planted(g){let a=Array(g.t+g.b).fill(0);a[0]=a[g.t]=0;for(let i=0;i<g.t;i++)g.ch[i].forEach((j,k)=>a[j]=a[i]^perms[i%6][k]);return a.slice(g.t)}
for(let t=1;t<=3;t++)for(let shape of t===3?["path","branch"]:["path"]){
 const g=tree(t,shape),signs=g.edges.map(()=>0),all=close(g,null,signs);ck(all.every(x=>x===15));
 const bad=new Set(),parts=new Map(),total=4**g.b;
 for(let w=0;w<total;w++){let bound=Array.from({length:g.b},(_,i)=>(w>>(2*i))&3);let c=classify(g,bound),m=close(g,bound,signs),ref=brute(g,bound,signs);ck(!!m===ref);ck(c.bad===!ref);if(c.bad){bad.add(w);if(!parts.has(c.key))parts.set(c.key,[]);parts.get(c.key).push(w)}else if(w%257===0)lift(g,m,signs)}
 ck(bad.size===4*6**t);ck(parts.size===3**t);
 for(let p of parts.values()){ck(p.length===2**(t+2));ck(rank(p.map(x=>x^p[0]))===t+2)}
 let base=bad.values().next().value,periods=[];for(let b of bad){let d=b^base;stats.periodCandidates++;let valid=true;for(let w of bad){stats.periodWordChecks++;if(!bad.has(w^d)){valid=false;break}}if(valid)periods.push(d)}
 ck(periods.length===4);for(let d of periods)ck(Array.from({length:g.b},(_,i)=>(d>>(2*i))&3).every(c=>c===(d&3)));
 stats.shapes.push({t,shape,boundaryWords:total,bad:bad.size,parts:parts.size,partSize:2**(t+2),periods:periods.length})
}
for(let t of [1,8,32,128,512]){let g=tree(t,"branch"),z=g.edges.map(()=>0),b=planted(g);ck(!close(g,b,z));ck(classify(g,b).bad);let n=b.slice();n[n.length-1]^=1;let m=close(g,n,z);ck(!!m);ck(!classify(g,n).bad);lift(g,m,z);stats.scale.push({t,boundary:g.b,badWords:(4n*6n**BigInt(t)).toString(),flatPieces:(3n**BigInt(t)).toString(),minRank:4*t+2})}
let seed=20261124;function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
for(let k=0;k<240;k++){let g=tree(1+rng(3),k%2?"path":"branch"),z=g.edges.map(()=>rng(4)),gauge=Array(g.t+g.b).fill(0);g.edges.forEach(([u,v],i)=>gauge[v]=gauge[u]^z[i]);let b=k%2?planted(g):Array.from({length:g.b},()=>rng(4));if(k%4===1)b[b.length-1]^=1;let signed=b.map((x,i)=>x^gauge[g.t+i]);let m=close(g,signed,z);ck(!!m===!classify(g,b).bad);ck(!!m===brute(g,signed,z));if(m)lift(g,m,z);stats.signed++}
const local=perms.map(p=>p[0]|(p[1]<<2)|(p[2]<<4));let allxor=local.reduce((a,b)=>a^b,0);ck(allxor===0);for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)ck((allxor^local[i]^local[j])!==0);
return stats}
console.log(JSON.stringify(run(),null,2));
