console.log(JSON.stringify((function audit(){
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function base(k,no){let n=1,C=[],witness=[0],tests=0;for(let j=0;j<k;j++){const v=[0,...Array.from({length:6},()=>n++)];let l=lines.filter((_,i)=>i!==0||(no&&j===0));let sol=null;for(let mask=0;mask<128;mask++){tests++;let b=Array.from({length:7},(_,i)=>(mask>>i)&1);if(b[0]===0&&l.every(t=>{let s=t.reduce((a,i)=>a+b[i],0);return s===1||s===2}))sol=b;}if(sol)for(let i=1;i<7;i++)witness[v[i]]=sol[i];for(const t of l){let a=t.map(i=>v[i]),p=n++;C.push([...a,p]);if(sol)witness[p]=2-t.reduce((s,i)=>s+sol[i],0);}}return{n,C,witness:no?null:witness,tests}}
 function compile(F){const g=0;let next=1,eq=[],X=[],U=[],V=[],P=[];for(let i=0;i<F.n;i++){let x=next++,u=next++,v=next++;X.push(x);U.push(u);V.push(v);eq.push([[x,1],[g,1],[u,-1]],[[u,1],[x,1],[v,-1]])}
 for(let c of F.C){let [a,b,d,e]=c,p=next++,q=next++;P.push([p,q]);eq.push([[U[a],1],[X[b],1],[p,-1]],[[U[d],1],[X[e],1],[q,-1]],[[p,1],[q,1]])}
 let rows=[],color=[],alias=[],occ=Array.from({length:next},()=>[]),zero=[],links=[];
 function vertex(c){let id=color.length;color.push(c);return id}
 function row(a){assert(new Set(a).size===3,"proper row");rows.push(a)}
 function link(a,b){let c=color[a]===color[b]?1-color[a]:0;let z=Array.from({length:8},(_,i)=>vertex(c^(i%2)));zero.push(z);for(let i=0;i<8;i++)row([z[i],z[(i+1)%8],z[(i+3)%8]]);row([a,b,z[0]]);links.push([a,b]);}
 for(let e of eq){let a=e.map(([v,s],j)=>{let i=vertex(e.length===3?(j===2?1:0):j);alias.push([i,v,s]);occ[v].push([i,s]);return i});if(a.length===3)row(a);else link(a[0],a[1]);}
 for(let o of occ){assert(o.length>0,"unused abstract symbol");if(o.length===1){let a=o[0][0],b=vertex(0),c=vertex(0),d=vertex(0);link(a,b);link(b,c);link(c,d);link(d,a)}else for(let j=1;j<o.length;j++){let [a,s]=o[j-1],[b,t]=o[j];if(s!==t)link(a,b);else{let r=vertex(0);link(a,r);link(r,b)}}}
 const n=color.length,degree=Array(n).fill(0),pairs=new Set();for(let r of rows){assert(r.reduce((s,i)=>s+color[i],0)%3!==0,"known NAE witness");for(let i of r)degree[i]++;for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){let a=Math.min(r[j],r[k]),b=Math.max(r[j],r[k]),p=a*n+b;assert(!pairs.has(p),"linearity");pairs.add(p)}}
 assert(degree.every(d=>d>=2&&d<=4),"degree promise");
 const ex=rows.map((r,i)=>[...r,n+i]);const model=[...color,...rows.map(r=>2-r.reduce((s,i)=>s+color[i],0))];
 assert(ex.every(r=>r.reduce((s,i)=>s+model[i],0)===2),"EX22 known SAT");assert(ex.every(r=>r.reduce((s,i)=>s+1-model[i],0)===2),"complement");
 function abstract(bits,scale){let a=Array(next).fill(0);a[g]=scale;for(let i=0;i<F.n;i++){a[X[i]]=-bits[i];a[U[i]]=a[X[i]]+scale;a[V[i]]=a[U[i]]+a[X[i]]}for(let j=0;j<F.C.length;j++){let [i,k,l,m]=F.C[j],[p,q]=P[j];a[p]=a[U[i]]+a[X[k]];a[q]=a[U[l]]+a[X[m]]}assert(eq.every(r=>r.reduce((s,[v,t])=>s+t*a[v],0)===0),"abstract sums");return a}
 function lift(a){let d=Array(n).fill(null);for(let z of zero)for(let i of z)d[i]=0;for(let [i,v,s] of alias)d[i]=a[v]*s;let change=true;while(change){change=false;for(let [i,j] of links){if(d[i]===null&&d[j]!==null){d[i]=-d[j];change=true}if(d[j]===null&&d[i]!==null){d[j]=-d[i];change=true}}}assert(d.every(x=>x!==null),"lift complete");assert(rows.every(r=>r.reduce((s,i)=>s+d[i],0)===0),"physical integer sums");return d}
 return{n,rows,ex,model,degree,zero,alias,occ,g,X,lift,abstract,links}}
 function ternary(G){let nodes=0,scans=0;const adj=Array.from({length:G.n},()=>[]);for(let i=0;i<G.rows.length;i++)for(let v of G.rows[i])adj[v].push(i);
 const vals=[-1,0,1];function prop(d,initial){let q=[...initial],inq=new Uint8Array(G.rows.length);for(let i of q)inq[i]=1;for(let h=0;h<q.length;h++){let i=q[h];inq[i]=0;scans++;let r=G.rows[i],s=[0,0,0];for(let a=0;a<3;a++)if(d[r[0]]&(1<<a))for(let b=0;b<3;b++)if(d[r[1]]&(1<<b))for(let c=0;c<3;c++)if((d[r[2]]&(1<<c))&&vals[a]+vals[b]+vals[c]===0){s[0]|=1<<a;s[1]|=1<<b;s[2]|=1<<c}for(let j=0;j<3;j++){let v=r[j];if(!s[j])return false;if(s[j]!==d[v]){d[v]=s[j];for(let e of adj[v])if(!inq[e]){inq[e]=1;q.push(e)}}}}return true}
 let d=new Uint8Array(G.n).fill(7);for(let z of G.zero)for(let i of z)d[i]=2;let [gi,sg]=G.occ[G.g][0];d[gi]=sg===1?4:1;
 const order=[...G.X.map(x=>G.occ[x][0][0]),...Array.from({length:G.n},(_,i)=>i)];
 function dfs(d,initial){nodes++;if(!prop(d,initial))return null;let v=order.find(i=>(d[i]&(d[i]-1))!==0);if(v===undefined)return Array.from(d,m=>vals[Math.log2(m)]);for(let j=0;j<3;j++)if(d[v]&(1<<j)){let c=d.slice();c[v]=1<<j;let r=dfs(c,adj[v]);if(r)return r}return null}
 let w=dfs(d,G.rows.map((_,i)=>i));if(w){assert(G.rows.every(r=>r.reduce((s,i)=>s+w[i],0)===0),"exact solver witness");assert(w[gi]===sg,"activation");}return{yes:!!w,nodes,scans}}
 function bip(G,d){let adj=Array.from({length:G.n},()=>[]);for(let r of G.rows){let a=r.filter(i=>d[i]);assert(a.length===0||a.length===2,"even support");if(a.length){adj[a[0]].push(a[1]);adj[a[1]].push(a[0])}}let col=new Int8Array(G.n).fill(-1);for(let i=0;i<G.n;i++)if(d[i]&&col[i]<0){col[i]=0;let q=[i];for(let h=0;h<q.length;h++)for(let j of adj[q[h]]){if(col[j]===col[q[h]])return false;if(col[j]<0){col[j]=1-col[q[h]];q.push(j)}}}return true}
 let out=[];for(let k of [1,2,4,8,16])for(let no of [false,true]){let F=base(k,no),G=compile(F);let frac=G.lift(G.abstract(Array(F.n).fill(1),2));assert(frac.every(x=>Math.abs(x)<=2)&&frac.some(x=>x),"fractional direction");let parity=frac.map(x=>Math.abs(x)%2);assert(parity.some(x=>x),"parity nonzero");assert(!bip(G,parity),"parity obstruction");let selected=0,removed=0;
 if(!no){assert(F.C.every(r=>r.reduce((s,i)=>s+F.witness[i],0)===2),"base witness");let d=G.lift(G.abstract(F.witness,1));assert(d.every(x=>Math.abs(x)<=1)&&d.some(x=>x),"actual pair vector");assert(bip(G,d.map(x=>x!==0)),"actual bipartite");selected=d.filter(x=>x).length;removed=G.rows.filter(r=>r.some(i=>d[i])).length;
 for(let bit of [0,1]){let m=G.model.slice();for(let i=0;i<G.n;i++)if(d[i])m[i]=d[i]===1?1:0;else m[i]=bit;for(let j=0;j<G.rows.length;j++)if(G.rows[j].some(i=>d[i])){let s=G.rows[j].reduce((s,i)=>s+m[i],0);assert(s===1||s===2,"universal lift");m[G.n+j]=2-s;assert(G.ex[j].reduce((s,i)=>s+m[i],0)===2,"lift native");}}
 }
 let exact=k<=2?ternary(G):null;if(exact)assert(exact.yes===!no,"independent ternary search");
 out.push({k,base:no?"UNSAT":"SAT",baseVariables:F.n,baseClauses:F.C.length,baseEnumeration:F.tests,compiledVariables:G.model.length,compiledClauses:G.rows.length,maxDegree:Math.max(...G.degree),knownCompiledSAT:true,fractionalDirection:true,parityBipartite:false,selected,removed,exact});
 }return out;
})(),null,2));
