'use strict';
function check(){
  let assertions=0, vertices=0;
  const ok=(b)=>{assertions++;if(!b)throw Error("assertion "+assertions)};
  const L=4,d=8, D=284760, norms=282496;
  const vals=[-94920,28432,-7132,1656,-290,52,-7,1];
  const powers=[256,-64,16,-4,1];
  const rows=[];
  for(let h=1;h<=8;h++){
    // Build a finite incidence tree with a distinguished length-h variable path.
    const adj=Array.from({length:h+1},()=>[]);
    const add=()=>{adj.push([]);return adj.length-1};
    const edge=(a,b)=>{adj[a].push(b);adj[b].push(a)};
    const clause=(a,b,c)=>{const q=add();for(const v of [a,b,c])edge(q,v)};
    const variable=new Set(Array.from({length:h+1},(_,i)=>i));
    const nv=()=>{const v=add();variable.add(v);return v};
    function grow(v,k,depth){
      if(depth===0)return;
      for(let j=0;j<k;j++){const a=nv(),b=nv();clause(v,a,b);grow(a,d-1,depth-1);grow(b,d-1,depth-1)}
    }
    for(let j=0;j<h;j++){const w=nv();clause(j,j+1,w);grow(w,d-1,Math.max(0,L-Math.min(j+1,h-j)))}
    for(let j=0;j<=h;j++)grow(j,d-(j===0||j===h?1:2),Math.max(0,L-Math.min(j,h-j)));
    function bfs(root){const dist=new Int32Array(adj.length).fill(-1),q=[root];dist[root]=0;for(let i=0;i<q.length;i++){for(const b of adj[q[i]])if(dist[b]<0){dist[b]=dist[q[i]]+1;q.push(b)}}return dist}
    const a=bfs(0),b=bfs(h);let inner=0,na=0,nb=0,overlap=0;
    for(const v of variable){const x=a[v]/2,y=b[v]/2;if(x<=L)na+=powers[x]**2;if(y<=L)nb+=powers[y]**2;if(x<=L&&y<=L){inner+=powers[x]*powers[y];overlap++}}
    vertices+=adj.length;
    ok(na===norms&&nb===norms);ok(inner===vals[h-1]);ok(Math.abs(inner)*3<=D);if(h>1)ok(Math.abs(inner)*3<D);
    rows.push({distance:h,inner,overlap,incidence_vertices:adj.length});
  }
  ok(D>norms);ok(3*(-vals[0])===D);
  // Independent exact local-law reconstruction. Means scaled by D; pair moments -1/3.
  // Probability of minority pattern i with majority sign t is 1/6+t*(m_j+m_k)/4.
  // Work with denominator 12D.
  let laws=0, full=0, pins=0;
  const samples=[0,...vals.slice(1),...vals.slice(1).map(x=>-x),D/3,-D/3];
  for(const a of samples)for(const b of samples)for(const c of samples){
    const m=[a,b,c];if(m.filter(x=>Math.abs(x)===D/3).length>1)continue;
    checkLaw(m,null);full++;
  }
  for(const i of [0,1,2])for(const s of [-1,1]){const m=[-s*D/3,-s*D/3,-s*D/3];m[i]=s*D;checkLaw(m,[i,s]);pins++}
  function checkLaw(m,pin){
    let total=0,mean=[0,0,0],pair=[0,0,0],positive=0;
    for(let i=0;i<3;i++)for(const t of [-1,1]){
      const j=(i+1)%3,k=(i+2)%3;
      const w=2*D+3*t*(m[j]+m[k]);const x=[t,t,t];x[i]=-t;
      ok(w>=0);if(w>0){positive++;if(pin)ok(x[pin[0]]===pin[1])}
      total+=w;for(let a=0;a<3;a++){mean[a]+=w*x[a];pair[a]+=w*x[a]*x[(a+1)%3]}
    }
    ok(total===12*D);for(let a=0;a<3;a++){ok(mean[a]===12*m[a]);ok(pair[a]===-4*D)}
    ok(positive===(pin?3:6));laws++;
  }
  // Fano root and single occurrence sign neighbors: exhaustive source reference.
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  function legal(x,flip){return fano.every((v,i)=>{const y=v.map((j,k)=>((x>>j)&1)^(flip===3*i+k?1:0));return !(y[0]===y[1]&&y[1]===y[2])})}
  const counts=[];
  for(let f=-1;f<21;f++){let n=0,w=-1;for(let x=0;x<128;x++)if(legal(x,f)){n++;w=x}
    if(f===-1)ok(n===0);else {ok(n>0);ok(legal(w,f));const s=Array.from({length:7},(_,i)=>1-2*((w>>i)&1));for(let i=0;i<7;i++){let sum=0;for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){const a=fano[i][j],b=fano[i][k];sum+=s[a]*s[b]*(f===3*i+j?-1:1)*(f===3*i+k?-1:1)}ok(sum===-1)}}
    counts.push(n)
  }
  ok(7-2*7<0);ok(8*3**8<4**8);
  return {scope:"finite tree Gram counts, exact local moment distributions, Fano SAT/UNSAT references; no finite high-girth UNSAT graph generated or full solver run",rows,incidence_vertices_total:vertices,gram_denominator:D,diagonal_margin_numerator:D-norms,local_laws:laws,full_support_laws:full,pinned_laws:pins,fano_model_counts:counts,reference_words:22*128,assertions};
}
console.log(JSON.stringify(check(),null,2));
