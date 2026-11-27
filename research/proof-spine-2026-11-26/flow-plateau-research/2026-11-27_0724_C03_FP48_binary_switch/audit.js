function audit() {
 const assert=(b)=>{if(!b)throw Error("audit failed")};
 function source(sizes,seams) {
  let n=0, edges=[], cycles=[],neg=[];
  for(const k of sizes){let c=Array.from({length:k},(_,j)=>n+j);cycles.push(c);for(let j=0;j<k;j++)edges.push([c[j],c[(j+1)%k],1]);n+=k;}
  for(const [u,v,s] of seams){if(s){let w=n++;neg.push(w);edges.push([u,w,0],[v,w,0]);}else edges.push([u,v,0]);}
  assert(neg.length%2===0);for(let i=0;i<neg.length;i+=2)edges.push([neg[i],neg[i+1],1]);
  let deg=Array(n).fill(0), keys=new Set();for(let [u,v] of edges){assert(u!==v);let key=[Math.min(u,v),Math.max(u,v)].join(",");assert(!keys.has(key));keys.add(key);deg[u]++;deg[v]++;}assert(deg.every(d=>d===3));
  return {n,edges,cycles};
 }
 function ring(r,control=false){let seams=[],O=[[0,1],[5,6]],I=[[2,3],[7,8]];
  for(let i=0;i<r;i++){let j=(i+1)%r;for(let a=0;a<2;a++){let b=i===r-1?a:1-a;seams.push([12*i+O[a][0],12*j+I[b][0],0],[12*i+O[a][1],12*j+I[b][1],control?0:1]);}j=(i+2)%r;seams.push([12*i+4,12*j+10,0],[12*i+9,12*j+11,0]);}return source(Array(r).fill(12),seams);
 }
 function triple(){let seams=[],used=Array.from({length:3},()=>new Set());for(let j=0;j<8;j++){let p=Array.from({length:3},(_,i)=>48*i+6*j+((j>>(2-i))&1));for(let i=0;i<3;i++){used[i].add(p[i]);used[i].add(p[i]+1);seams.push([p[i]+1,p[(i+1)%3],i===2?1:0]);}}
  let spare=used.map((s,i)=>Array.from({length:48},(_,j)=>48*i+j).filter(v=>!s.has(v)));for(let j=0;j<32;j++)for(let i=0;i<3;i++)seams.push([spare[i][j],144+3*j+i,0]);return source([48,48,48,96],seams);
 }
 function check(G,pins){let adj=Array.from({length:G.n},()=>[]), add=(u,v)=>{adj[u].push(v);adj[v].push(u);};for(let [u,v,a] of G.edges)if(!a)add(u,v);for(let [i,b] of pins){let c=G.cycles[i];for(let j=b;j<c.length;j+=2)add(c[j],c[(j+1)%c.length]);}let color=Array(G.n).fill(-1);for(let i=0;i<G.n;i++)if(color[i]<0){color[i]=0;let q=[i];for(let u of q)for(let v of adj[u]){if(color[v]<0){color[v]=1-color[u];q.push(v);}else if(color[u]===color[v])return false;}}return true;}
 function scan(G){let r=G.cycles.length, I=Array.from({length:2*r},()=>[]),unary=0,binary=0,probes=0;
  for(let i=0;i<r;i++)for(let a=0;a<2;a++){probes++;if(!check(G,[[i,a]])){unary++;I[2*i+a].push(2*i+1-a);}}
  for(let i=0;i<r;i++)for(let j=i+1;j<r;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){probes++;if(!check(G,[[i,a],[j,b]])){binary++;I[2*i+a].push(2*j+1-b);I[2*j+b].push(2*i+1-a);}}
  const reach=(u,v)=>{let seen=new Set([u]),q=[u];for(let x of q){if(x===v)return true;for(let y of I[x])if(!seen.has(y)){seen.add(y);q.push(y);}}return false;};
  let no=Array.from({length:r},(_,i)=>i).some(i=>reach(2*i,2*i+1)&&reach(2*i+1,2*i));
  let good=0,seen=Math.min(256,2**r);for(let j=0;j<seen;j++){let pins=Array.from({length:r},(_,i)=>[i,Math.floor(j/2**(r-1-i))%2]);if(check(G,pins))good++;}
  return {n:G.n,r,unary,binary,probes,no,seen,good};
 }
 let result={};for(let r of [5,8,16,32,64]){let z=scan(ring(r));assert(z.no&&z.binary===2*r&&z.unary===0&&z.good===0);result["ring"+r]=z;}
 let T=triple(),z=scan(T);assert(!z.no&&!z.binary&&!z.unary&&z.good===0&&z.seen===16);let fail=0;for(let j=0;j<8;j++)if(!check(T,Array.from({length:3},(_,i)=>[i,(j>>(2-i))&1])))fail++;assert(fail===8);result.triple={...z,tripleFailures:fail};let C=scan(ring(5,true));assert(!C.no&&C.good===32);result.control=C;return result;
}
console.log(JSON.stringify(audit(),null,2));
