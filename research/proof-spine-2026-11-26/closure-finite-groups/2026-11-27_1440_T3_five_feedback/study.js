// Requires Node.js, pinned gauge.js and compile.js; study(L,G,q,g,p,C,seedClauses,[],cnf,caseName). Exported function; exact prior helper extraction described in report.
function study(L,G,q,g,p,C,seedClauses,peerPins,cnf,caseName){
 const {canon,up,tree,replay,project,clauses}=L;
 const vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),rank=vs=>vs.map(v=>[v,C.filter(c=>c.includes(v)||c.includes(-v)).length]).sort((a,b)=>b[1]-a[1]||a[0]-b[0]).map(a=>a[0]);
 const top=rank(vars).slice(0,4);
 const guards=top.map((v,i)=>top.slice(0,i).map(x=>-x).concat(v)).concat([top.map(x=>-x)]);
 const pins=h=>new Map(h.map(l=>[Math.abs(l),+(l>0)]));
 function occupancy(F,h){let A=pins(h),visits=0,rounds=0,change=true;while(change){change=false;rounds++;for(const f of F){let rows=f.a.filter(t=>{visits++;return f.s.every((v,j)=>!A.has(v)||A.get(v)===(t>>j&1))});if(!rows.length)return {bad:true,visits,rounds,forced:A.size-h.length};for(let j=0;j<f.s.length;j++)if(!A.has(f.s[j])&&rows.every(t=>(t>>j&1)===(rows[0]>>j&1))){A.set(f.s[j],rows[0]>>j&1);change=true}}}return{bad:false,visits,rounds,forced:A.size-h.length,assign:[...A]}}
 function affine(F,h){const V=[...new Set(F.flatMap(f=>f.s))].sort((a,b)=>a-b),idx=new Map(V.map((v,i)=>[v,i])),A=pins(h),basis=new Map();let tests=0,xors=0,eqs=0;function insert(row,b){eqs++;while(row){let j=row.toString(2).length-1;if(!basis.has(j)){basis.set(j,[row,b]);return true}let [r,t]=basis.get(j);row^=r;b^=t;xors++}return !b}for(let [v,b] of A)if(idx.has(v)&&!insert(1n<<BigInt(idx.get(v)),b))return{bad:true,tests,xors,eqs};for(const f of F){let rows=f.a.filter(t=>f.s.every((v,j)=>!A.has(v)||A.get(v)===(t>>j&1)));if(!rows.length)return{bad:true,tests,xors,eqs};for(let k=1;k<2**f.s.length;k++){let par=x=>{let a=0;while(x){a^=1;x&=x-1}return a};let b=par(k&rows[0]);let same=rows.every(t=>{tests++;return par(k&t)===b});if(same){let mask=0n;f.s.forEach((v,j)=>{if(k>>j&1)mask|=1n<<BigInt(idx.get(v))});if(!insert(mask,b))return{bad:true,tests,xors,eqs,rank:basis.size}}}}return{bad:false,tests,xors,eqs,rank:basis.size}}
 function flow(h){let A=pins([ -g.g,...h ]),bs=[],root=new Map(),scans=0;for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let counts=new Map();for(let j=0;j<4;j++){let i=4*v+j,r=q.R[i]+1,s=q.Q[i];if(!counts.has(r))counts.set(r,[0,0]);counts.get(r)[s]++}bs.push([v,counts]);for(let [r,c] of counts){if(!root.has(r))root.set(r,[0,0]);root.get(r)[0]+=c[0];root.get(r)[1]+=c[1]}}let roots=[...root.keys()],rr=new Map(roots.map((v,i)=>[v,i+1])),sink=1+roots.length+bs.length,adj=Array.from({length:sink+1},()=>[]);function edge(a,b,c){let e=[b,c,adj[b].length],f=[a,0,adj[a].length];adj[a].push(e);adj[b].push(f)}function max(r,c){return A.has(r)?c[1-A.get(r)]:Math.max(...c)}for(let r of roots)edge(0,rr.get(r),max(r,root.get(r)));bs.forEach(([v,counts],j)=>{let b=1+roots.length+j;edge(b,sink,2);for(let [r,c] of counts)edge(rr.get(r),b,max(r,c))});let value=0;while(true){let level=new Int32Array(sink+1).fill(-1),queue=[0];level[0]=0;for(let i=0;i<queue.length;i++)for(let e of adj[queue[i]]){scans++;if(e[1]>0&&level[e[0]]<0){level[e[0]]=level[queue[i]]+1;queue.push(e[0])}}if(level[sink]<0)break;let it=new Int32Array(sink+1);function dfs(v,f){if(v===sink)return f;for(;it[v]<adj[v].length;it[v]++){let e=adj[v][it[v]];scans++;if(e[1]&&level[e[0]]===level[v]+1){let x=dfs(e[0],Math.min(f,e[1]));if(x){e[1]-=x;adj[e[0]][e[2]][1]+=x;return x}}}return 0}let z;while(z=dfs(0,1e9))value+=z}return{bad:value<2*bs.length,value,demand:2*bs.length,scans}}
 function sep(F,h){let A=pins(h),F1=F.map(f=>{let s=f.s.filter(v=>!A.has(v)),a=[];for(let t of f.a)if(f.s.every((v,j)=>!A.has(v)||A.get(v)===(t>>j&1))){let z=s.reduce((z,v,j)=>z|((t>>f.s.indexOf(v)&1)<<j),0);if(!a.includes(z))a.push(z)}return{s,a}});if(F1.some(f=>!f.a.length))return{bad:true,pivots:0,scans:0,rows:0};let z=project(F1);return{bad:z.F.some(f=>!f.a.length),pivots:z.trace.length,scans:z.scans,rows:z.rows}}
 const early={occupancy:occupancy(g.F,[]),affine:affine(g.F,[]),flow:flow([]),unit:up(clauses(g.F),[],{visits:0},1e7).A.size};delete early.occupancy.assign;
 const lanes=[],local=[],rejects=[];
 for(const h of guards){let O=occupancy(p.F,h),A=affine(p.F,h),M=flow(h),S=sep(p.F,h),counter={visits:0},D=up(C,h,counter,1e7);delete O.assign;let row={h,occupancy:O,affine:A,flow:M,separator:S,dag:{bad:D.bad,forced:D.A.size-h.length,visits:counter.visits}};lanes.push(row);if([O,A,M,S,D].some(x=>x.bad)){let c=canon(h.map(x=>-x));try{let r=replay(C,[c]);local.push({c,check:r.visits})}catch(e){rejects.push({c,reason:"not independently RUP; retained as unimported lead"})}}}
 // Coverage counts for verified local exclusions only. Exact counts on four guard variables.
 let covered=0;for(let t=0;t<16;t++)if(local.some(({c})=>c.every(l=>((t>>top.indexOf(Math.abs(l)))&1)!==+(l>0))))covered++;
 // Independent replay of a limited peer prefix; do not import complete proof.
 let peer=L.importPrefix(C.concat(local.map(x=>x.c)),seedClauses),X=C.concat(local.map(x=>x.c),peer.good);
 let cl={visits:0},closed=up(X,[],cl,1e7);
 function feedback(base,w,mode,limit=12000){
  let F=base.map(c=>c.slice()),seen=new Set(F.map(c=>c.join(","))),T=[],pairs=0,scoreVisits=0,flips=0,checks=0,peakLits=F.reduce((a,c)=>a+c.length,0),start=Date.now(),found=false;
  let V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);let vindex=new Map(V.map((v,i)=>[v,i]));let a=V.map(()=>0);
  function score(f,b){let n=0;for(let l of f){scoreVisits++;if(b[vindex.get(Math.abs(l))]===+(l>0))n++}return n}
  let counts0=F.map(c=>score(c,a)),counts1=F.map(c=>score(c,V.map(()=>1)));let init=[counts0.filter(x=>!x).length,counts1.filter(x=>!x).length];if(init[1]<init[0])a.fill(1);
  function improve(){for(let iter=0;iter<100;iter++){let cnt=F.map(c=>score(c,a)),delta=new Int32Array(V.length);for(let i=0;i<F.length;i++)for(let l of F[i]){scoreVisits++;let j=vindex.get(Math.abs(l)),yes=a[j]===+(l>0);if(!cnt[i])delta[j]++;else if(cnt[i]===1&&yes)delta[j]--}let best=-1;for(let j=0;j<V.length;j++)if(delta[j]>0&&(best<0||delta[j]>delta[best]))best=j;if(best<0)break;a[best]^=1;flips++}}
  if(mode==="flip"||mode==="feedback")improve();
  if(mode==="deduce"||mode==="feedback"){
   let queue=[],done=new Set();function push(i,j){for(let l of F[i])if(F[j].includes(-l))queue.push([i,j,Math.abs(l)])}
   for(let j=0;j<F.length;j++)for(let i=0;i<j;i++)push(i,j);
   if(mode==="feedback"){let c=F.map(x=>score(x,a));queue.sort((x,y)=>(c[x[0]]+c[x[1]])-(c[y[0]]+c[y[1]])||x[1]-y[1]||x[0]-y[0]||x[2]-y[2])}
   for(let z=0;z<queue.length&&pairs<limit;z++){let [i,j,v]=queue[z];pairs++;let u=canon(F[i].concat(F[j]).filter(l=>Math.abs(l)!==v));if(u.length>w||u.some(l=>u.includes(-l))||seen.has(u.join(",")))continue;let check=canon([...F[i].filter(l=>Math.abs(l)!==v),...F[j].filter(l=>Math.abs(l)!==v)]);checks+=F[i].length+F[j].length+u.length;if(check.join(",")!==u.join(",")||!((F[i].includes(v)&&F[j].includes(-v))||(F[i].includes(-v)&&F[j].includes(v))))throw Error("resolution");seen.add(u.join(","));T.push({i,j,v,u});let k=F.length;F.push(u);peakLits+=u.length;if(!u.length){found=true;break}for(let x=0;x<k;x++)push(x,k);if(mode==="feedback"&&T.length%8===0)improve()}
   if(mode==="feedback")improve();
  }
  let rr=replay(base,T.map(t=>t.u)),search=found?{status:"UNSAT",nodes:0,visits:0,proof:[]}:tree(F,[],700000),verification=replay(F,search.proof);if(search.status==="UNSAT"&&!found&&!verification.unsat)throw Error("no empty");
  let final=F.map(c=>score(c,a)).filter(x=>!x).length;return{mode,w,init,final,flips,pairs,learned:T.length,checks,scoreVisits,peakLits,search:{status:search.status,nodes:search.nodes,visits:search.visits},verify:rr.visits+verification.visits,ms:Date.now()-start,trace:T,proof:search.proof}
 }
 const modes=[["baseline",2],["flip",2],["deduce",2],["feedback",2],["deduce",4],["feedback",4]];
 let native=modes.map(([mode,w])=>feedback(X,w,mode)),companion=modes.map(([mode,w])=>feedback(cnf,w,mode));
 let fano=[];for(let line of [[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]]){fano.push(line,line.map(x=>-x))}
 let fanoTest=caseName==="JOINT-24"?[feedback(fano,2,"deduce"),feedback(fano,4,"deduce"),feedback(fano,4,"feedback")]:[];
 return{early,top,guards,lanes,local,rejects,covered,peer,closed:{bad:closed.bad,forced:closed.A.size,visits:cl.visits},native,companion,fanoTest}
}
module.exports=study;
