// Exact pairwise flow-side envelopes via propagation; small reference enumeration only.
const inputs=[{"name":"affine_plane","n":9,"clauses":[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]]},{"name":"layered_5","n":15,"clauses":[[[0,5,10],[1,6,11],[2,7,12],[3,8,13],[4,9,14]],[[0,6,12],[1,7,13],[2,8,14],[3,9,10],[4,5,11]],[[0,7,14],[1,8,10],[2,9,11],[3,5,12],[4,6,13]],[[0,8,11],[1,9,12],[2,5,13],[3,6,14],[4,7,10]]]},{"name":"random_0","n":15,"clauses":[[[12,6,4],[1,0,3],[13,10,8],[9,14,5],[2,7,11]],[[0,2,9],[12,3,10],[8,11,4],[1,14,13],[6,7,5]],[[6,2,8],[4,10,1],[0,5,13],[3,7,9],[14,11,12]],[[6,11,0],[4,14,3],[2,5,10],[12,13,9],[7,1,8]]]},{"name":"random_5","n":15,"clauses":[[[12,14,13],[4,10,3],[0,8,11],[1,5,7],[6,9,2]],[[10,9,0],[12,11,1],[6,3,14],[5,2,13],[4,7,8]],[[0,2,14],[6,4,12],[9,11,5],[10,7,13],[8,3,1]],[[10,1,6],[3,0,5],[12,7,2],[13,4,11],[14,9,8]]]},{"name":"random_8","n":15,"clauses":[[[0,2,4],[6,5,10],[9,3,8],[11,14,7],[1,13,12]],[[14,12,8],[13,0,10],[2,11,1],[9,5,7],[6,3,4]],[[0,6,7],[14,2,10],[12,11,3],[1,8,5],[4,9,13]],[[12,6,2],[4,14,1],[10,7,8],[3,5,13],[0,11,9]]]},{"name":"archive_0","n":15,"clauses":[[[12,4,9],[6,5,2],[14,0,13],[1,8,7],[11,3,10]],[[7,0,4],[11,5,9],[2,13,8],[6,10,12],[14,1,3]],[[14,5,10],[6,9,7],[11,13,12],[2,1,4],[0,8,3]],[[7,14,2],[5,12,0],[10,1,9],[13,4,3],[8,6,11]]]},{"name":"archive_1","n":9,"clauses":[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,8],[2,5,7]],[[0,4,7],[1,5,6],[2,3,8]],[[0,5,8],[1,3,7],[2,4,6]]]},{"name":"archive_2","n":9,"clauses":[[[7,3,0],[6,1,2],[8,5,4]],[[7,5,2],[3,1,4],[0,8,6]],[[6,5,3],[8,7,1],[4,2,0]],[[8,2,3],[0,5,1],[6,7,4]]]},{"name":"archive_3","n":9,"clauses":[[[1,7,8],[3,5,4],[0,2,6]],[[6,8,4],[2,5,1],[3,7,0]],[[8,0,5],[1,6,3],[7,4,2]],[[1,0,4],[2,3,8],[7,6,5]]]},{"name":"archive_4","n":9,"clauses":[[[4,8,0],[3,6,7],[5,2,1]],[[7,1,4],[2,6,0],[5,8,3]],[[4,5,6],[3,0,1],[7,8,2]],[[5,0,7],[3,2,4],[6,8,1]]]},{"name":"archive_5","n":9,"clauses":[[[1,5,6],[2,7,0],[8,3,4]],[[2,3,1],[0,6,4],[8,5,7]],[[3,5,0],[8,2,6],[1,7,4]],[[6,3,7],[0,1,8],[4,5,2]]]},{"name":"archive_6","n":12,"clauses":[[[8,2,9],[3,4,1],[5,11,0],[10,7,6]],[[1,8,10],[9,11,6],[2,0,4],[7,3,5]],[[11,8,3],[5,6,4],[7,1,2],[0,10,9]],[[9,5,1],[2,3,10],[6,0,8],[11,4,7]]]},{"name":"archive_7","n":12,"clauses":[[[2,0,5],[6,1,9],[7,8,3],[10,11,4]],[[9,10,8],[4,0,1],[11,5,3],[2,6,7]],[[0,10,3],[11,1,7],[2,4,9],[8,5,6]],[[2,1,8],[4,3,6],[5,10,7],[9,11,0]]]},{"name":"archive_8","n":12,"clauses":[[[1,11,10],[0,4,8],[7,5,2],[3,9,6]],[[8,10,2],[5,4,6],[1,0,3],[9,11,7]],[[0,11,5],[6,8,1],[10,3,7],[2,4,9]],[[3,5,8],[7,4,1],[2,11,6],[9,10,0]]]},{"name":"archive_9","n":12,"clauses":[[[3,7,0],[9,2,4],[6,8,10],[11,5,1]],[[10,4,5],[0,1,9],[7,11,8],[3,2,6]],[[2,0,5],[9,10,7],[3,1,8],[4,11,6]],[[7,1,6],[4,0,8],[10,11,2],[5,9,3]]]},{"name":"archive_10","n":15,"clauses":[[[9,4,3],[5,11,1],[12,0,14],[7,8,6],[10,2,13]],[[14,5,9],[11,12,6],[0,13,4],[2,7,3],[10,8,1]],[[10,7,4],[13,1,14],[3,12,8],[2,11,9],[5,0,6]],[[5,7,12],[11,3,13],[8,14,2],[1,6,4],[0,9,10]]]},{"name":"archive_11","n":15,"clauses":[[[7,11,1],[5,12,2],[4,0,6],[8,13,10],[9,3,14]],[[12,10,14],[4,2,11],[9,6,8],[0,13,7],[1,3,5]],[[5,13,9],[6,14,7],[4,8,1],[3,2,10],[11,0,12]],[[1,0,14],[4,10,5],[11,8,3],[12,7,9],[13,2,6]]]},{"name":"archive_12","n":15,"clauses":[[[4,3,1],[14,7,12],[10,2,5],[8,0,6],[9,13,11]],[[8,12,5],[14,4,0],[3,2,9],[10,7,13],[11,1,6]],[[13,1,14],[5,0,9],[8,7,2],[4,10,11],[12,6,3]],[[3,5,13],[8,1,9],[10,0,12],[11,2,14],[7,6,4]]]},{"name":"archive_13","n":15,"clauses":[[[1,2,10],[4,14,3],[9,8,5],[11,12,13],[6,7,0]],[[3,9,6],[12,5,10],[13,1,4],[7,2,14],[0,8,11]],[[5,4,6],[7,10,8],[14,11,1],[12,3,2],[13,9,0]],[[13,3,10],[4,7,9],[12,0,14],[1,8,6],[5,2,11]]]}];
function audit(inputs){
 let checks=0,upCalls=0,impQueries=0,satCalls=0,rounds=0,probes=0,rows=[];
 const A=(b,m)=>{checks++;if(!b)throw Error(m)};
 const up=(cs,guard)=>{upCalls++;let p=guard.slice(),changed=true;while(changed){changed=false;for(let c of cs){let vs=c.map(i=>p[i]),z=vs.filter(v=>v===0).length,o=vs.filter(v=>v===1).length;if(z===3||o===3)return null;if(vs.includes(-1)&&(z===2||o===2)){p[c[vs.indexOf(-1)]]=z===2?1:0;changed=true}}}return p};
 const sat=(cs,w)=>cs.every(c=>c.some(i=>(w>>i&1)!==(w>>c[0]&1)));
 const lit=(i,b)=>2*i+b;
 function feas(n,C,p){
   satCalls++;let d=Array.from({length:2*n},()=>[]),r=Array.from({length:2*n},()=>[]);function edge(u,v){d[u].push(v);r[v].push(u)}for(let [u,v] of C){edge(u^1,v);edge(v^1,u)}for(let i=0;i<n;i++)if(p[i]>=0)edge(lit(i,p[i]^1),lit(i,p[i]));
   let seen=new Set(),order=[];function dfs(v){if(seen.has(v))return;seen.add(v);for(let u of d[v])dfs(u);order.push(v)}for(let i=0;i<2*n;i++)dfs(i);
   let c=Array(2*n).fill(-1),k=0;function rev(v){if(c[v]>=0)return;c[v]=k;for(let u of r[v])rev(u)}for(let v of order.reverse())if(c[v]<0){rev(v);k++}
   for(let i=0;i<n;i++)if(c[2*i]===c[2*i+1])return false;return true;
 }
 function solve(src){
   let {n,clauses}=src,all=clauses.flat(),p=Array(n).fill(-1),history=[];p=up(all,p);if(!p)return {status:"UNSAT",history};p[0]=0; // complement normalization, valid only unguarded source.
   const sides=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)sides.push(clauses[i].concat(clauses[j]));
   for(let k=0;k<=n;k++){
     rounds++;p=up(all,p);if(!p)return {status:"UNSAT",history};let C=[],keys=new Set();
     const add=(u,v)=>{let key=u<v?`${u},${v}`:`${v},${u}`;if(!keys.has(key)){keys.add(key);C.push([u,v])}};
     // Clauses satisfied by existing pins, or reduced to binary, are exact original constraints.
     for(let c of all){let vals=c.map(i=>p[i]);if(vals.includes(0)&&vals.includes(1))continue;let free=c.filter(i=>p[i]<0);if(free.length===2){let b=1-vals.find(x=>x>=0);add(lit(free[0],b),lit(free[1],b))}}
     for(let side of sides){let root=up(side,p);A(root!==null,"full UP fixed point side");for(let v=0;v<n;v++)if(p[v]<0)for(let b=0;b<2;b++){impQueries++;let q=p.slice();q[v]=b;let z=up(side,q);if(!z)add(lit(v,b^1),lit(v,b^1));else for(let u=0;u<n;u++)if(u!==v&&p[u]<0&&z[u]>=0)add(lit(v,b^1),lit(u,z[u]));}}
     if(!feas(n,C,p))return {status:"UNSAT",history};
     let newp=p.slice();for(let v=0;v<n;v++)if(p[v]<0){let a=p.slice(),b=p.slice();a[v]=0;b[v]=1;let fa=feas(n,C,a),fb=feas(n,C,b);A(fa||fb,"2CNF consistent root");if(!fa||!fb)newp[v]=fa?0:1;}
     let f=newp.filter(x=>x>=0).length-p.filter(x=>x>=0).length;history.push({binaryClauses:C.length,forced:f});
     if(f){p=newp;continue}
     // Stagnation: paid whole-source failed-literal UP, guarded, no nested search.
     for(let v=0;v<n;v++)if(p[v]<0){let a=p.slice(),b=p.slice();a[v]=0;b[v]=1;probes+=2;let u=up(all,a),w=up(all,b);if(!u&&!w)return {status:"UNSAT",history};if(!u||!w){let z=u||w;for(let i=0;i<n;i++)if(z[i]>=0){if(newp[i]>=0)A(newp[i]===z[i],"incompatible deductions");newp[i]=z[i]}}else for(let i=0;i<n;i++)if(u[i]>=0&&u[i]===w[i]){if(newp[i]>=0)A(newp[i]===u[i],"incompatible common probe");newp[i]=u[i]}}
     if(newp.some((x,i)=>x!==p[i])){p=newp;continue}
     // Try one deterministic 2CNF word, acquiring it by paid feasibility.
     let q=p.slice();for(let v=0;v<n;v++)if(q[v]<0){q[v]=0;if(!feas(n,C,q))q[v]=1;}A(feas(n,C,q),"2CNF witness");
     let w=q.reduce((s,b,v)=>s|(b<<v),0);if(sat(all,w))return {status:"SAT",witness:w,history};
     let unsafe=0;for(let c of all){let bad=false;for(let b=0;b<2;b++){let z=p.slice();if(c.some(v=>z[v]>=0&&z[v]!==b))continue;for(let v of c)z[v]=b;if(feas(n,C,z))bad=true}unsafe+=+bad}
     A(unsafe>0,"invalid word under exact envelope");return {status:"UNKNOWN",unsafe,history};
   }
   throw Error("closure cap");
 }
 for(let src of inputs){let modelCount=0,all=src.clauses.flat();for(let w=0;w<1<<src.n;w++)if(sat(all,w))modelCount++;let r=solve(src);A(r.status==="UNKNOWN"||(r.status==="SAT")===(modelCount>0),"wrong decision");if(r.status==="SAT")A(sat(all,r.witness),"bad witness");rows.push({name:src.name,n:src.n,modelCount,...r});}
 return {checks,upCalls,impQueries,satCalls,rounds,probes,rows};
}
console.log(JSON.stringify(audit(inputs),null,2));
