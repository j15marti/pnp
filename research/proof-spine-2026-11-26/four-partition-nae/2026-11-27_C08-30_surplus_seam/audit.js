function audit(){
const rows=[[3,4,2],[2,1,0],[3,0,5],[1,0,4],[1,3,0],[0,5,4],[5,0,2]], signs=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,1],[1,0,0],[0,1,0]], n=6;
const g12=[[0,4,11],[1,5,7],[2,6,8],[3,9,10],[0,1,6],[8,9,11],[2,7,10],[3,4,5],[1,8,10],[4,6,9],[2,5,11],[0,3,7],[4,7,8],[5,6,10],[1,3,11],[0,2,9]];
const ag=[...Array.from({length:3},(_,r)=>[3*r,3*r+1,3*r+2]),...Array.from({length:3},(_,c)=>[c,c+3,c+6]),...Array.from({length:3},(_,c)=>Array.from({length:3},(_,r)=>3*r+(r+c)%3)),...Array.from({length:3},(_,c)=>Array.from({length:3},(_,r)=>3*r+(c-r+3)%3))];
let checks=0,trials=0,graphWork=0,cap=10000000;
function tick(){if(++trials+checks+graphWork>cap)throw Error("cap")}
function ck(x,m){checks++;if(!x)throw Error(m)}
function nae(a){return a.some(x=>x!==a[0])}
function bit(w,v){return (w>>v)&1}
function table(R,N,B){let t=Array(1<<B.length).fill(0);for(let w=0;w<1<<N;w++){tick();if(R.every(r=>nae(r.map(v=>bit(w,v))))){let p=B.reduce((s,v,j)=>s|(bit(w,v)<<j),0);t[p]++}}return t}
const capTable=table(ag.slice(2),9,[0,1,2,3,4,5]),gTable=table(g12.filter((_,i)=>i!==5),12,[8,9,11]);ck(capTable.every((x,i)=>x===(i===7||i===56?6:0)),"cap");ck(gTable.every((x,i)=>x===(i===0||i===7?7:0)),"g12");
let native=[],partition=[],portLists=[[ [0,1,2],[3,4,5] ]],parts=[];
for(let i=2;i<12;i++){native.push(ag[i]);partition.push([1,0,2,3][Math.floor(i/3)])}
parts.push({vars:Array.from({length:9},(_,i)=>i),ports:[0,1,2,3,4,5]});
for(let v=1;v<n;v++){let o=9+12*(v-1);portLists.push([[8+o,9+o,11+o],[]]);parts.push({vars:Array.from({length:12},(_,i)=>i+o),ports:portLists[v][0]});g12.forEach((r,i)=>{if(i!==5){native.push(r.map(x=>x+o));partition.push(Math.floor(i/4))}})}
let pos=Array.from({length:n},()=>[0,0]),cross=[];
rows.forEach((r,i)=>{let R=r.map((v,j)=>portLists[v][signs[i][j]][pos[v][signs[i][j]]++]);cross.push(native.length);native.push(R);partition.push(1)});
let N=69;ck(native.length===92,"native m");let pairs=new Set();
for(let r of native){ck(r.length===3&&new Set(r).size===3&&r.every(v=>v>=0&&v<N),"row");for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=[r[i],r[j]].sort((a,b)=>a-b).join(",");ck(!pairs.has(k),"linearity");pairs.add(k)}}
for(let p=0;p<4;p++){let a=native.flatMap((r,i)=>partition[i]===p?r:[]);ck(a.length===N&&new Set(a).size===N,"partition")}
function components(R,n){let adj=Array.from({length:n},()=>new Set());for(let r of R)for(let v of r)for(let w of r)adj[v].add(w);let seen=new Set(),out=[];for(let v=0;v<n;v++)if(!seen.has(v)){let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(let w of adj[q[i]]){graphWork++;if(!seen.has(w)){seen.add(w);q.push(w)}}out.push(q.sort((a,b)=>a-b))}return out}
ck(components(native,N).length===1,"connected");
let acquired=[];for(let p=0;p<4;p++){let C=components(native.filter((_,i)=>partition[i]!==p),N),lab=Array(N);C.forEach((r,i)=>r.forEach(v=>lab[v]=i));let S=native.flatMap((r,i)=>partition[i]===p&&new Set(r.map(v=>lab[v])).size>1?[i]:[]);let c=components(native.filter((_,i)=>!S.includes(i)),N);acquired.push({p,k:S.length,c:c.length,cut:S,componentSizes:c.map(r=>r.length)})}
ck(JSON.stringify(acquired[1].cut)===JSON.stringify(cross)&&acquired[1].c===6,"cut");
function phase(R,S,N,skip=-1){let solutions=[];for(let w=0;w<1<<N;w+=2){tick();if(R.every((r,i)=>i===skip||nae(r.map((v,j)=>bit(w,v)^S[i][j]))))solutions.push(w)}return solutions}
ck(phase(rows,signs,n).length===0,"core NO");let deletion=rows.map((_,i)=>phase(rows,signs,n,i));ck(deletion.every(x=>x.length>0),"minimal");
let splits=[];for(let mask=1;mask<64;mask+=2){if(mask.toString(2).replace(/0/g,"").length!==3)continue;let j=0,R=rows.map(r=>r.map(v=>v===0?((mask>>j++)&1?0:6):v));let sol=phase(R,signs,7);ck(sol.length>0&&sol.every(w=>bit(w,6)===1),"split control");splits.push({mask,rows:R,solutions:sol})}
ck(splits.length===10,"splits");
// Independent 2SAT implication closure on six rows touching heavy phase, fixed phase 0.
let adj=Array.from({length:12},()=>new Set());function lit(v,value){return 2*v+value}
for(let i=0;i<rows.length;i++){let j=rows[i].indexOf(0);if(j<0)continue;let other=rows[i].map((v,l)=>[v,l]).filter(x=>x[0]!==0);let [a,b]=other.map(([v,l])=>lit(v,1^signs[i][j]^signs[i][l]));adj[a^1].add(b);adj[b^1].add(a)}
let reach=adj.map((a,i)=>new Set([i,...a]));for(let k=0;k<12;k++)for(let i=0;i<12;i++)if(reach[i].has(k))for(let j of reach[k]){graphWork++;reach[i].add(j)}
let eq=[];for(let a=1;a<6;a++)for(let b=a+1;b<6;b++)for(let p=0;p<2;p++)if([0,1].every(t=>reach[lit(a,t)].has(lit(b,t^p))&&reach[lit(b,t^p)].has(lit(a,t))))eq.push([a,b,p]);
ck(eq.some(([a,b,p])=>a===2&&b===3&&p===0)&&eq.some(([a,b,p])=>a===2&&b===4&&p===0),"closure");
let rest=phase(rows,signs,n,0);ck(rest.every(w=>bit(w,2)===bit(w,3)&&bit(w,2)===bit(w,4)),"independent relation");
// All-signing quotient via a spanning tree in incidence graph, one fixed reference per class.
let parent=Array.from({length:13},(_,i)=>i);function root(x){while(parent[x]!==x)x=parent[x];return x}
let free=[];rows.forEach((r,i)=>r.forEach((v,j)=>{let a=root(i),b=root(7+v);if(a!==b)parent[a]=b;else free.push([i,j])}));ck(free.length===9,"gauge dimension");let no=0,covered=0,missed=0,first=null;
for(let w=0;w<1<<free.length;w++){let S=rows.map(r=>r.map(()=>0));free.forEach(([i,j],l)=>S[i][j]=bit(w,l));if(phase(rows,S,n).length)continue;no++;let ref=false;for(let s of splits)if(phase(s.rows,S,7).length===0){ref=true;break}if(ref)covered++;else{missed++;if(!first)first={word:w,signs:S}}}
ck(missed>0&&covered+missed===no,"classification");
return {native:{variables:N,clauses:native,partition,cut:cross,components:parts,encodedJSONBytes:JSON.stringify({clauses:native,partition}).length},rows,signs,capTable,gTable,acquired,deletion,splits,eq,binaryResidualSolutions:rest,allSigning:{dimension:free.length,free,NO:no,coveredBySomeSplit:covered,missed,first},counts:{checks,trials,graphWork,cap}};
}
console.log(JSON.stringify(audit(),null,2));
