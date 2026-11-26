function fourPrimeAudit(){
const A=(x,m)=>{if(!x)throw Error(m)},mod=x=>(x%3+3)%3,R=n=>Array.from({length:n},(_,i)=>i),out=[];
function make(k){const L=24,V=R(48*k),rot=V.map(v=>{let i=v%24,l=Math.floor(v%48/24),b=v-v%48;let a=b+l*24+(i+23)%24,c=b+l*24+(i+1)%24,d=b+(1-l)*24+i;return l?[c,a,d]:[a,c,d]});
function replace(u,old,ne){let j=rot[u].indexOf(old);A(j>=0,"old edge");rot[u][j]=ne}
for(let j=0;j<k-1;j++){let a=48*j,b=a+48,P=[[a+12,a+13,b+7,b+6],[a+18,a+19,b+1,b]];for(let [u,v,w,z] of P){replace(u,v,w);replace(v,u,z);replace(w,z,u);replace(z,w,v)}}
const kind=v=>(v%24+Math.floor(v%48/24))%2,vars=V.filter(v=>kind(v)===0),clauses=V.filter(v=>kind(v)===1),E=[];for(let v of V){A(rot[v].length===3&&new Set(rot[v]).size===3,"degree");for(let w of rot[v]){A(rot[w].includes(v)&&kind(v)!==kind(w),"bipartite");if(v<w)E.push([v,w])}}
let seen=new Set(),f=0;for(let v of V)for(let w of rot[v])if(!seen.has(v+","+w)){f++;let a=v,b=w;do{let z=a+","+b;A(!seen.has(z),"face");seen.add(z);let c=rot[b][(rot[b].indexOf(a)+1)%3];a=b;b=c}while(a!==v||b!==w)}A(V.length-E.length+f===2,"Euler");
let idx=new Map(vars.map((v,i)=>[v,i])),mat=clauses.map(v=>{let r=R(vars.length+1).map(()=>0);rot[v].forEach(w=>r[idx.get(w)]=1);r[vars.length]=1;return r});
function witness(ph){let x=Object.fromEntries(vars.map(v=>[v,Number((v%24)%3===ph[Math.floor(v/48)])]));A(clauses.every(v=>rot[v].reduce((s,w)=>s+x[w],0)===1),"native exact witness");return x}
let phases=[0,1,2].map(p=>witness(R(k).map(()=>p)));A(vars.every(v=>phases.some(x=>x[v]===1)&&phases.some(x=>x[v]===0)),"full coordinate support");
let base=witness(R(k).map(()=>1));for(let j=0;j<k;j++){let p=R(k).map(()=>1);p[j]=2;let w=witness(p);A(vars.every(v=>Math.floor(v/48)===j||w[v]===base[v]),"independent phase support")}
let rank=0,n=vars.length;for(let c=0;c<n&&rank<n;c++){let j=mat.findIndex((r,i)=>i>=rank&&r[c]);if(j<0)continue;[mat[rank],mat[j]]=[mat[j],mat[rank]];if(mat[rank][c]===2)mat[rank]=mat[rank].map(x=>mod(2*x));for(let i=rank+1;i<n;i++)if(mat[i][c]){let q=mat[i][c];for(let l=c;l<=n;l++)mat[i][l]=mod(mat[i][l]-q*mat[rank][l])}rank++}A(n-rank>=k,"rank lower bound");
let top=V.filter(v=>v%48<24),vis=new Set(),cycles=[];for(let u of top)if(!vis.has(u)){let Q=[u];vis.add(u);for(let i=0;i<Q.length;i++)for(let v of rot[Q[i]])if(v%48<24&&!vis.has(v)){vis.add(v);Q.push(v)}cycles.push(Q)}A(cycles.length===k,"top cycle count");A(cycles.filter(a=>a.length===12).length===k-1,"small cycles");let big=cycles.find(a=>a.length!==12);A(big&&R(k).every(j=>big.filter(v=>Math.floor(v/48)===j).length>=12),"big cycle");
let scans=0;if(k<=4){let ad=V.map(()=>[]);E.forEach(([u,v],i)=>{ad[u].push([v,i]);ad[v].push([u,i])});function scan(a,b){scans++;let ti=0,dis=R(V.length).map(()=>-1),low=[],size=[];function dfs(u,p){dis[u]=low[u]=ti++;size[u]=1;for(let [v,id] of ad[u])if(id!==a&&id!==b&&id!==p){if(dis[v]<0){dfs(v,id);size[u]+=size[v];low[u]=Math.min(low[u],low[v]);if(low[v]>dis[u])A(size[v]===1||size[v]===V.length-1,"nontrivial <=3 cut")}else low[u]=Math.min(low[u],dis[v])}}dfs(0,-1);A(ti===V.length,"no <=2 cut")}
scan(-1,-1);for(let i=0;i<E.length;i++){scan(i,-1);for(let j=0;j<i;j++)scan(i,j)}}
return{blocks:k,variables:n,faces:f,affineDimension:n-rank,actualAffineDimensionLower:k,verifiedPhaseWitnesses:k+4,cutScans:scans,topCycleLengths:cycles.map(a=>a.length).sort((a,b)=>a-b)}}
for(let k of [1,2,4,8,16])out.push(make(k));return out}
console.log(JSON.stringify(fourPrimeAudit(),null,2));
