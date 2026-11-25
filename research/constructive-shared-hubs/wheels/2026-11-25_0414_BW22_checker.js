// Node.js, deterministic; DR22 graph and owner order reproduced from f11016d.
function run(){
let checks=0, scans=0;const ok=x=>{checks++;if(!x)throw Error("assert "+checks)},par=x=>{let a=0;while(x){a^=x&1;x>>>=1}return a},nae=(a,b,c)=>a!==b||b!==c;
function graph(m){let vs=[],id=new Map(),edges=[],stars=[];for(let i=0;i<m;i++)for(let j=0;j<m;j++)if(i!==j){id.set(i*m+j,vs.length);vs.push([i,j]);stars.push([])}
function add(u,v){let e=edges.length;edges.push([u,v]);stars[u].push(e);stars[v].push(e)}
for(let i=0;i<m;i++){let c=vs.map((v,k)=>[v,k]).filter(([v])=>v[0]===i).map(([,k])=>k);for(let k=0;k<c.length;k++)add(c[k],c[(k+1)%c.length])}
for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)add(id.get(i*m+j),id.get(j*m+i));
let n=1+edges.length,owners=[];for(let v=0;v<vs.length;v++){let[a,b,c]=stars[v].map(e=>e+1);for(let f=0;f<8;f++)if(par(f)!==Number(v===0)){let t=n++;owners.push([[a,f&1],[b,(f>>1)&1],[t,0]],[[t,1],[c,(f>>2)&1],[0,0]])}}
return {n,edges,stars,owners}}
function decode(g,owners){let occ=Array.from({length:g.n},()=>[]),used=new Set(),groups=new Map(),lifts=[];owners.forEach((o,i)=>{scans++;o.forEach(([v])=>occ[v].push(i)); // full affine hull check for each local NAE, by distinct scope
ok(new Set(o.map(x=>x[0])).size===3)});
for(let t=1;t<g.n;t++){let ids=occ[t];if(ids.length===1){let i=ids[0],o=owners[i];if(o[2][0]===t&&o[2][1]===0&&!o.some(([v])=>v===0)){ok(!used.has(i));used.add(i);lifts.push({t,a:o[0],b:o[1],single:true})}continue}
if(ids.length!==2)continue;let [i,j]=ids;if(owners[i].some(([v])=>v===0))[i,j]=[j,i];let a=owners[i],b=owners[j];if(a[2][0]!==t||a[2][1]!==0||b[0][0]!==t||b[0][1]!==1||b[2][0]!==0||b[2][1]!==0)continue;
ok(!used.has(i)&&!used.has(j));used.add(i);used.add(j);let scope=[a[0][0]-1,a[1][0]-1,b[1][0]-1],key=scope.join(","),f=a[0][1]+2*a[1][1]+4*b[1][1];if(!groups.has(key))groups.set(key,{scope,fs:[]});groups.get(key).fs.push(f);lifts.push({t,a:a[0],b:a[1],c:b[1]})}
ok(used.size===owners.length);
let rows=[...groups.values()].map(({scope,fs})=>{let R=[];for(let w=0;w<8;w++){let pass=true;for(let f of fs){let a=(w^f)&1,b=((w^f)>>1)&1,c=((w^f)>>2)&1;let yes=[0,1].some(t=>nae(a,b,t)&&nae(t^1,c,0));ok(yes===Boolean(a||b||c));pass&&=yes}if(pass)R.push(w)}let q=R.length===4&&R.every(w=>par(w)===par(R[0]))?par(R[0]):null;return {scope,R,q}});ok(rows.length===g.stars.length);for(let i=0;i<rows.length;i++)ok(rows[i].scope.join(",")===g.stars[i].join(","));
return {rows,lifts}}
function project(E,rows){let active=rows.map((r,i)=>r.q!==null?i:-1).filter(i=>i>=0),def=rows.map((r,i)=>r.q===null?i:-1).filter(i=>i>=0),obs=new Set(def.flatMap(i=>rows[i].scope)),inc=Array.from({length:E},()=>[]);rows.forEach((r,i)=>r.scope.forEach(e=>inc[e].push(i)));ok(inc.every(v=>v.length===2));let adj=rows.map(()=>[]);for(let e=0;e<E;e++)if(!obs.has(e)){let[u,v]=inc[e];ok(rows[u].q!==null&&rows[v].q!==null);adj[u].push([v,e]);adj[v].push([u,e])}
let seen=new Set(),comps=[];for(let r of active)if(!seen.has(r)){let order=[r],parent=new Map(),charge=0,boundary=new Set();seen.add(r);for(let k=0;k<order.length;k++){let u=order[k];charge^=rows[u].q;for(let e of rows[u].scope)if(obs.has(e)){if(boundary.has(e))boundary.delete(e);else boundary.add(e)}for(let [v,e] of adj[u])if(!seen.has(v)){seen.add(v);order.push(v);parent.set(v,[u,e])}}comps.push({order,parent,charge,boundary:[...boundary]})}
function lift(vals){let x=Array(E).fill(0);for(let [e,b] of vals)x[e]=b;for(let c of comps){let s=c.boundary.reduce((a,e)=>a^x[e],0);if(s!==c.charge)return null;for(let k=c.order.length-1;k>0;k--){let u=c.order[k],[v,e]=c.parent.get(u);x[e]=rows[u].q^rows[u].scope.reduce((a,f)=>a^(e===f?0:x[f]),0)}}
for(let r of rows){let w=r.scope.reduce((a,e,k)=>a|(x[e]<<k),0);ok(r.R.includes(w))}return x}
return {def,obs:[...obs],comps,lift}}
function job(m,mode){let g=graph(m),o=g.owners.map(a=>a.map(b=>b.slice())); // DR22 sole bad owner is second owner for f=0 (index 1).
if(mode==="delete")o.splice(1,1);if(mode==="flip")o[1][1][1]^=1;
let d=decode(g,o),p=project(g.edges.length,d.rows),survivors=0,witness=null;ok(p.obs.length<=3);for(let w=0;w<(1<<p.obs.length);w++){let vals=new Map(p.obs.map((e,i)=>[e,(w>>i)&1]));if(p.def.some(i=>!d.rows[i].R.includes(d.rows[i].scope.reduce((a,e,k)=>a|(vals.get(e)<<k),0))))continue;
let x=p.lift(vals);if(!x)continue;survivors++;witness=x;}
ok(Boolean(witness)===(mode!=="root"));if(witness){let a=Array(g.n).fill(0);witness.forEach((b,e)=>a[e+1]=b);for(let l of d.lifts){let v=a[l.a[0]]^l.a[1],w=a[l.b[0]]^l.b[1];let t=Number(!v&&!w);ok(nae(v,w,t));if(!l.single)ok(nae(t^1,a[l.c[0]]^l.c[1],0));a[l.t]=t;}for(let owner of o)ok(nae(...owner.map(([i,s])=>a[i]^s)));}
return {m,mode,owners:o.length,sourceVariables:g.n,edgeVariables:g.edges.length,affineRows:d.rows.length-p.def.length,nonlinearRows:p.def.length,nonlinearSupport:p.def.map(i=>d.rows[i].R),components:p.comps.length,projectedParity:p.comps.map(c=>({boundary:c.boundary,rhs:c.charge})),boundaryTrials:1<<p.obs.length,acceptedBoundaryWords:survivors,SAT:!!witness}}
let results=[];for(let m of [5,40])for(let mode of ["root","delete","flip"])results.push(job(m,mode));
// independently enumerate local K4 parity lifts for all 16 boundary words
let pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],counts=[];for(let w=0;w<16;w++){let count=0;for(let z=0;z<64;z++){let deg=Array.from({length:4},(_,i)=>(w>>i)&1);pairs.forEach(([u,v],i)=>{if((z>>i)&1){deg[u]++;deg[v]++}});if(deg.every(d=>d===2))count++;}ok(Boolean(count)===(par(w)===0));counts.push(count)}
return {checks,ownerScans:scans,results,counts,limits:"Known gauge ID 0, DR22 generator/order; no general discovery or physical network construction. Local closure full hull before grouping by distinct NAE scopes; exact projected support and source witness replay. No S27/RT26 replay."}}

console.log(JSON.stringify(run(),null,2));
