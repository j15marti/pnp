// Run: node independent_audit.js
const audit = function audit(){
 const assert=(x,msg)=>{if(!x)throw Error(msg)};
 const pop=x=>x.toString(2).replace(/0/g,"").length;
 const tab=Array.from({length:16},()=>[]);
 const bits=i=>[(i>>2)&1,(i>>1)&1,i&1];
 for(let w=0;w<16;w++)for(let s=0;s<256;s++){
  if((s&3)!=(w&3))continue;
  let row=[pop(w>>2),0,0,0,0,0];
  for(let i=0;i<8;i++)if(s>>i&1){let [x,y,z]=bits(i);if(i>=2)row[x]++;row[2+y]++;row[4+z]++}
  if(row.every(v=>v===1))tab[w].push(s);
 }
 assert(tab[0].length===2&&[5,6,9,10].every(w=>tab[w].length===1)&&tab.reduce((s,v)=>s+v.length,0)===6,"local table");
 // Perfect matching signature of six-cycle 0--4--1--2--5--3--0
 const adj=Array(6).fill(0);for(const [a,b] of [[0,4],[4,1],[1,2],[2,5],[5,3],[3,0]]){adj[a]|=1<<b;adj[b]|=1<<a}
 function pm(mask){if(!mask)return 1;let i=0;while(!(mask>>i&1))i++;let n=0;for(let j=i+1;j<6;j++)if((mask>>j&1)&&(adj[i]>>j&1))n+=pm(mask^(1<<i)^(1<<j));return n}
 for(let w=0;w<16;w++)assert(pm(63^w)===tab[w].length,"six cycle");
 function grid(l){
  let n=l*l,edges=[],id=(i,j)=>i+l*j;
  for(let i=0;i<l;i++)for(let j=0;j<l;j++){
   if(i+1<l)edges.push([id(i,j),0,id(i+1,j),0]);
   if(j+1<l)edges.push([id(i,j),1,id(i,j+1),1]);
  }
  let out=[],inc=[];
  for(let i=0;i<l;i++)out.push([id(i,l-1),1]);
  for(let j=l-1;j>=0;j--)out.push([id(l-1,j),0]);
  for(let i=l-1;i>=0;i--)inc.push([id(i,0),1]);
  for(let j=0;j<l;j++)inc.push([id(0,j),0]);
  inc.reverse();for(let i=0;i<out.length;i++)edges.push([...out[i],...inc[i]]);
  let T=[];for(let a=0;a<n;a++)for(let i=0;i<8;i++)T.push(bits(i).map(v=>2*a+v));
  for(const [a,p,b,q] of edges)T[8*a+p][0]=2*b;
  return {n,edges,T};
 }
 function rank(rows){let piv=new Map;for(let x of rows){while(x){let k=x.toString(2).length;if(piv.has(k))x^=piv.get(k);else{piv.set(k,x);break}}}return piv.size}
 function check(l){
  let {n,edges,T}=grid(l);assert(new Set(T.map(t=>t.join(","))).size===T.length,"distinct");
  let rows=Array(6*n).fill(0n);for(let i=0;i<T.length;i++)for(let c=0;c<3;c++)rows[2*n*c+T[i][c]]|=1n<<BigInt(i);
  let D=edges.reduce((x,[a,p])=>x|(1n<<BigInt(8*a+p)),0n);
  let projection=2*n-rank(rows)+rank(rows.map(x=>x&~D));assert(projection===n+1,"cycle dimension");
  const selected=Array(T.length).fill(false),omitted=selected.slice(),out=Array.from({length:n},()=>[]);
  edges.forEach((e,i)=>out[e[0]].push(i));
  function lift(ids,alt=0){
   let w=Array(n).fill(0);for(let i of ids){let[a,p,b,q]=edges[i];w[a]|=1<<p;w[b]|=1<<(2+q)}
   let cover=[];for(let a=0;a<n;a++){let s=tab[w[a]][w[a]===0?alt:0];assert(s!==undefined,"missing word");for(let i=0;i<8;i++)if(s>>i&1)cover.push(8*a+i)}
   for(let c=0;c<3;c++)assert(new Set(cover.map(i=>T[i][c])).size===2*n&&cover.length===2*n,"invalid witness");
   let mask=new Set(cover);for(let i=0;i<T.length;i++){if(mask.has(i))selected[i]=true;else omitted[i]=true}
  }
  lift([],0);lift([],1);
  for(let i=0;i<edges.length;i++){
   let [a,p,b,q]=edges[i],prev=new Map([[b,-1]]),queue=[b];for(let k=0;k<queue.length&&!prev.has(a);k++){let v=queue[k];for(let j of out[v]){let u=edges[j][2];if(!prev.has(u)){prev.set(u,j);queue.push(u)}}}
   assert(prev.has(a),"not Eulerian connected");let cycle=[i],v=a;while(v!==b){let j=prev.get(v);cycle.push(j);v=edges[j][0]}lift(cycle);
  }
  assert(selected.every(Boolean)&&omitted.every(Boolean),"full support");
  let count=null;
  if(l<=3){let by=Array.from({length:2*n},()=>[]);T.forEach(([x,y,z])=>by[x].push([y,z]));let f=(i,Y,Z)=>i===2*n?1:by[i].reduce((a,[y,z])=>a+((Y>>y&1)||(Z>>z&1)?0:f(i+1,Y|(1<<y),Z|(1<<z))),0);count=f(0,0,0)}
  return {l,triples:T.length,edges:edges.length,projected_kernel_rank:projection,verified_cover_lifts:edges.length+2,full_unary_support:true,brute_count:count};
 }
 // All 512 parity support patterns: criterion and disjoint two-layer decomposition.
 let accepted=[0,0],layers=0;for(let p=0;p<2;p++){
  let W=Array.from({length:16},(_,i)=>i).filter(i=>pop(i)%2===p);
  for(let s=0;s<256;s++){
   let f=Array(16).fill(0);W.forEach((w,i)=>f[w^(p?1:0)]=(s>>i)&1);
   let L=f[0]*f[15]+f[5]*f[10],R=f[3]*f[12]+f[9]*f[6];if(!!L===!!R)accepted[p]++;
   let h=[Array(16).fill(0),Array(16).fill(0)];
   for(let w=0;w<16;w++)if(f[w])h[w< (15^w)?0:1][w]=1;
   for(let v of h){assert(v[0]*v[15]+v[5]*v[10]===v[3]*v[12]+v[9]*v[6],"layer");layers++}
   assert(f.every((x,i)=>x===h[0][i]+h[1][i]),"partition");
  }
 }
 return {local_table:tab.map(x=>x.length),parity_patterns_accepted:accepted,layer_checks:layers,grid:[2,3,4,6,8,12].map(check)};
};
console.log(JSON.stringify(audit(),null,2));
