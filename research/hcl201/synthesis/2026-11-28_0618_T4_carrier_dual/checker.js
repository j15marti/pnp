// node checker.js compile.js benchmarks.json instance-registry-v1.json
const fs=require('node:fs');
function sha(s){
 let p=[],h=[],k=[];for(let n=2;k.length<64;n++)if(p.every(x=>n%x)){p.push(n);if(h.length<8)h.push((Math.sqrt(n)%1*4294967296)>>>0);k.push((Math.cbrt(n)%1*4294967296)>>>0)}
 let a=new Uint8Array(Math.ceil((s.length+9)/64)*64);for(let i=0;i<s.length;i++){if(s.charCodeAt(i)>127)throw Error("nonascii");a[i]=s.charCodeAt(i)}a[s.length]=128;let n=s.length*8;for(let j=0;j<8;j++){a[a.length-1-j]=n%256;n=Math.floor(n/256)}const R=(x,k)=>(x>>>k)|(x<<(32-k)),w=new Uint32Array(64);
 for(let o=0;o<a.length;o+=64){for(let i=0;i<16;i++)w[i]=(a[o+4*i]<<24)|(a[o+4*i+1]<<16)|(a[o+4*i+2]<<8)|a[o+4*i+3];for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(R(x,7)^R(x,18)^(x>>>3))+w[i-7]+(R(y,17)^R(y,19)^(y>>>10)))>>>0}let [A,B,C,D,E,F,G,J]=h;for(let i=0;i<64;i++){let t=(J+(R(E,6)^R(E,11)^R(E,25))+((E&F)^(~E&G))+k[i]+w[i])>>>0,u=((R(A,2)^R(A,13)^R(A,22))+((A&B)^(A&C)^(B&C)))>>>0;[A,B,C,D,E,F,G,J]=[(t+u)>>>0,A,B,C,(D+t)>>>0,E,F,G]}h=h.map((v,i)=>(v+[A,B,C,D,E,F,G,J][i])>>>0)}
 return h.map(v=>v.toString(16).padStart(8,"0")).join("")
}
function run(compile,corpus,registry,sha){
 const A=(b,m)=>{if(!b)throw Error(m)},pc=x=>{let n=0;while(x){x&=x-1;n++}return n},bit=i=>1n<<BigInt(i);
 function normalize(g){
  let n=4*g.types.length,p=Int32Array.from({length:n},(_,i)=>i),d=new Uint8Array(n),sz=new Int32Array(n).fill(1),calls=0;
  function f(a){calls++;if(p[a]===a)return [a,0];let [r,s]=f(p[a]);d[a]^=s;p[a]=r;return [r,d[a]]}
  function j(a,b,s){let [x,u]=f(a),[y,v]=f(b);if(x===y)return (u^v)===s;if(sz[x]<sz[y])[x,y]=[y,x];p[y]=x;d[y]=u^v^s;sz[x]+=sz[y];return true}
  let seen=new Set(),ports=new Set(),ok=true;for(let [a,b,s] of g.edges){let x=a>>2,y=b>>2,key=Math.min(x,y)+":"+Math.max(x,y);A(x!==y&&!seen.has(key)&&!ports.has(a)&&!ports.has(b),"native format");seen.add(key);ports.add(a);ports.add(b);ok=j(a,b,s)&&ok}A(ports.size===n,"degree");for(let i=0;i<g.types.length;i++)if(g.types[i]==="E")for(let k=1;k<4;k++)ok=j(4*i,4*i+k,0)&&ok;if(!ok)return {conflict:true,calls};
  let ids=new Map(),owners=[];for(let i=0;i<g.types.length;i++)if(g.types[i]==="B"){let c=[],s=[];for(let k=0;k<4;k++){let [r,t]=f(4*i+k);if(!ids.has(r))ids.set(r,ids.size);c.push(ids.get(r));s.push(t)}
   let words=[];for(let w=0;w<16;w++){let y=w;for(let k=0;k<4;k++)y^=s[k]<<k;if(pc(y)===2&&c.every((v,j)=>c.every((u,k)=>u!==v||((w>>j)&1)===((w>>k)&1))))words.push(w)}if(!words.length)return {conflict:true,calls};owners.push({id:i,c,words})}
  return {r:ids.size,owners,calls};
 }
 function audit(owners,r,cap=10000000){
  let work=0,xorBits=0,calls=0;function basis(rows,width){calls++;let B=new Map();for(let a of rows){if(++work>cap)throw Error("CAP");while(a){if(++work>cap)throw Error("CAP");let p=a&-a;if(!B.has(p)){B.set(p,a);break}a^=B.get(p);xorBits+=width}}return [...B.values()]}
  let rank=(rows,width)=>basis(rows,width).length,m=owners.length,AL=[],AK=[],AZ=[],D=[],K=[],occ=Array.from({length:r},()=>[]);owners.forEach((o,i)=>o.c.forEach((v,j)=>occ[v].push(4*i+j)));let star=Array(4*m).fill(0n),q=0;for(let a of occ)for(let j=1;j<a.length;j++){let b=bit(q++);star[a[0]]^=b;star[a[j]]^=b}
  function localBasis(v){return basis(v.map(BigInt),4).map(Number)}
  function eq(c,L){let t=localBasis(Array.from({length:16},(_,i)=>i).filter(i=>L.every(x=>!(pc(i&x)&1))));return t.map(x=>c.reduce((s,v,j)=>s^(((x>>j)&1)?bit(v):0n),0n)).filter(Boolean)}
  function map(i,w){return [0,1,2,3].reduce((s,j)=>s^(((w>>j)&1)?star[4*i+j]:0n),0n)}
  for(let i=0;i<m;i++){let o=owners[i],l=localBasis(o.words.map(w=>w^o.words[0])),k=localBasis(Array.from({length:16},(_,w)=>w).filter(w=>o.words.every(v=>o.words.includes(v^w))));AL.push(eq(o.c,l));AK.push(eq(o.c,k));AZ.push(eq(o.c,[]));D.push(l.map(w=>map(i,w)));K.push(k.map(w=>map(i,w)))}
  let RL=rank(AL.flat(),r),RK=rank(AK.flat(),r),RZ=rank(AZ.flat(),r),H=basis(K.flat(),q),R=rank(D.flat(),q),cuts={},checked=0;
  function oracle(P,check=false){let s=new Set(P),a=[],b=[],c=[],d=[],l=[],u=[];for(let i=0;i<m;i++){let v=s.has(i);a.push(...(v?AL[i]:AK[i]));b.push(...(v?AK[i]:AL[i]));c.push(...(v?AL[i]:AZ[i]));d.push(...(v?AZ[i]:AL[i]));(v?l:u).push(...D[i])}let raw=rank(c,r)+rank(d,r)-RL-RZ,quo=rank(a,r)+rank(b,r)-RL-RK;A(quo>=0&&quo<=raw,"range");if(check){A(raw===rank(l,q)+rank(u,q)-R,"raw mismatch");A(quo===rank([...H,...l],q)+rank([...H,...u],q)-R-H.length,"quotient mismatch");checked++}return [raw,quo]}
  let source=Array.from({length:m},(_,i)=>i),adj=source.map(()=>new Set());for(let a of occ){let v=[...new Set(a.map(x=>x>>2))];for(let i of v)for(let j of v)if(i!==j)adj[i].add(j)}
  let bfs=[],visited=new Set();for(let i of source)if(!visited.has(i)){visited.add(i);let Q=[i];for(let j=0;j<Q.length;j++){let v=Q[j];bfs.push(v);for(let u of adj[v])if(!visited.has(u)){visited.add(u);Q.push(u)}}}
  let x=source.map(i=>Math.sin((i+1)*1.618));for(let it=0;it<12;it++){let y=x.map((v,i)=>.5*v+.5*[...adj[i]].reduce((s,j)=>s+x[j],0)/Math.max(1,adj[i].size)),mu=y.reduce((s,t)=>s+t,0)/Math.max(m,1);x=y.map(t=>t-mu);let z=Math.sqrt(x.reduce((s,t)=>s+t*t,0))||1;x=x.map(t=>t/z)}
  let spectral=source.slice().sort((a,b)=>x[a]-x[b]||a-b),orders={source,bfs,spectral},tree=null,capped=false;
  try{if(m>1){let options=[];for(let [name,o] of Object.entries(orders)){let P=o.slice(0,m>>1);cuts[name]=oracle(P,name==="source"||m<=8);options.push({name,P,ranks:cuts[name]})}options.sort((a,b)=>a.ranks[1]-b.ranks[1]||a.ranks[0]-b.ranks[0]);let best=options[0],S=new Set(best.P);tree={root:best.name,ranks:best.ranks,children:[]};for(let v of [best.P,source.filter(i=>!S.has(i))])if(v.length>1){let P=v.slice(0,v.length>>1);tree.children.push({k:P.length,ranks:oracle(P,m<=8)})}}}catch(e){if(e.message!=="CAP")throw e;capped=true}
  return {r,m,q,rank:R,period:H.length,quotient:R-H.length,RL,RK,RZ,cuts,tree,checked,work,xorBits,calls,capped};
 }
 function cnf(inst){
  let F=inst.dimacs.trimEnd().split("\n").slice(1).map(s=>s.split(/\s+/).map(Number).slice(0,-1)),n=inst.nvars,reads=0,nodes=0,cnt=Array(n+1).fill(0);for(let c of F)for(let l of c)cnt[Math.abs(l)]++;
  function up(a){let change=true;while(change){change=false;for(let c of F){let u=0,l=0,sat=false;for(let z of c){reads++;if(reads>2000000)throw Error("CNF cap");let v=a[Math.abs(z)];if(!v){u++;l=z}else if(v===Math.sign(z)){sat=true;break}}if(sat)continue;if(!u)return false;if(u===1){a[Math.abs(l)]=Math.sign(l);change=true}}}return true}
  function solve(a){nodes++;if(!up(a))return {leaf:1};let v=0;for(let i=1;i<=n;i++)if(!a[i]&&(!v||cnt[i]>cnt[v]))v=i;if(!v)return {sat:[...a]};let l=a.slice();l[v]=-1;let L=solve(l);if(L.sat)return L;let r=a.slice();r[v]=1;let R=solve(r);if(R.sat)return R;return {v,L,R}}
  let tree=solve(new Int8Array(n+1)),discovery=reads;reads=0;
  function verify(t,a){if(t.sat)return F.every(c=>c.some(l=>t.sat[Math.abs(l)]===Math.sign(l)));let b=up(a);if(t.leaf)return !b;if(!b||!t.v||a[t.v])return false;let l=a.slice(),r=a.slice();l[t.v]=-1;r[t.v]=1;return verify(t.L,l)&&verify(t.R,r)}
  A(verify(tree,new Int8Array(n+1)),"CNF replay");return {status:tree.sat?"SAT":"UNSAT",nodes,discovery,verification:reads,tree};
 }
 let evidence={model:"T4-CARRIER-DUAL-v1",canonical:[],controls:[],generalized:0};
 for(let id of ["JOINT-24","RANDOM-3CNF-40"]){let inst=corpus.instances.find(x=>x.id===id),reg=registry.instances.find(x=>x.alias==="EB-"+id),g=compile(inst),s=JSON.stringify(g.network)+"\n";A(sha(s)===reg.sha256&&s.length*8===reg.N_bits&&sha(JSON.stringify(g.source_map)+"\n")===reg.source_map_sha256&&sha(inst.dimacs)===reg.source_cnf.sha256&&inst.dimacs.length*8===reg.source_cnf.N_bits,"auth "+id);let norm=normalize(g.network);A(!norm.conflict,"closure");evidence.canonical.push({id,registry:reg,uf:norm.calls,chart:audit(norm.owners,norm.r),cnf:cnf(inst)})}
 let st=24681357,rand=()=>{st=(Math.imul(st,1664525)+1013904223)>>>0;return st>>>31};
 for(let i=0;i<32;i++){let types=Array.from({length:5},()=>rand()?"B":"E"),p=Array(5).fill(0),edges=[];for(let u=0;u<5;u++)for(let v=u+1;v<5;v++)edges.push([4*u+p[u]++,4*v+p[v]++,rand()]);let g={format:"STRICT-EB4-v1",types,edges},n=normalize(g),truth=false;for(let w=0;w<1024;w++){let a=Array(20);edges.forEach(([u,v,s],j)=>{a[u]=(w>>j)&1;a[v]=a[u]^s});if(types.every((t,j)=>t==="E"?a.slice(4*j,4*j+4).every(v=>v===a[4*j]):a.slice(4*j,4*j+4).reduce((s,v)=>s+v,0)===2)){truth=true;break}}if(n.conflict)A(!truth,"false conflict");else{let b=false;for(let w=0;w<2**n.r;w++)if(n.owners.every(o=>o.words.includes(o.c.reduce((s,v,j)=>s|(((w>>v)&1)<<j),0)))){b=true;break}A(b===truth,"control")}evidence.controls.push({i,sha:sha(JSON.stringify(g)+"\n"),truth,conflict:!!n.conflict,chart:!n.conflict&&n.owners.length?audit(n.owners,n.r):null})}
 for(let i=0;i<64;i++){let r=5,O=[];for(let j=0;j<4;j++){let c=Array.from({length:4},()=>{st=(Math.imul(st,1664525)+1013904223)>>>0;return st%r}),words=[];for(let w=0;w<16;w++)if(c.every((v,a)=>c.every((u,b)=>u!==v||((w>>a)&1)===((w>>b)&1)))&&rand())words.push(w);if(!words.length)words=[0];O.push({c,words})}let a=audit(O,r);A(!a.capped&&a.checked>=3,"generic control");evidence.generalized++}
 return evidence;
}
let c=fs.readFileSync(process.argv[2],'utf8');let compile=Function(c.slice(c.indexOf("function compile("),c.indexOf("function auditLocal("))+"\nreturn compile;")();
console.log(JSON.stringify(run(compile,JSON.parse(fs.readFileSync(process.argv[3],"utf8")),JSON.parse(fs.readFileSync(process.argv[4],"utf8")),sha),null,2));
