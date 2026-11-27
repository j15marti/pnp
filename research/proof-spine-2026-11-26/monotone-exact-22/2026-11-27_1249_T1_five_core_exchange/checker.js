function sha256(s) {
  // All canonical bytes in this run are ASCII.
  const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  const H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19], n=s.length, len=Math.ceil((n+9)/64)*64, a=new Uint8Array(len);
  for(let i=0;i<n;i++){const c=s.charCodeAt(i);if(c>127)throw Error("non ASCII");a[i]=c}a[n]=128;
  let bits=BigInt(n)*8n;for(let i=0;i<8;i++){a[len-1-i]=Number(bits&255n);bits>>=8n}
  const r=(x,k)=>(x>>>k)|(x<<(32-k)),w=new Int32Array(64);
  for(let o=0;o<len;o+=64){
    for(let i=0;i<16;i++)w[i]=(a[o+4*i]<<24)|(a[o+4*i+1]<<16)|(a[o+4*i+2]<<8)|a[o+4*i+3];
    for(let i=16;i<64;i++){const x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(r(x,7)^r(x,18)^(x>>>3))+w[i-7]+(r(y,17)^r(y,19)^(y>>>10)))|0}
    let [A,B,C,D,E,F,G,J]=H;
    for(let i=0;i<64;i++){let t=(J+(r(E,6)^r(E,11)^r(E,25))+((E&F)^(~E&G))+K[i]+w[i])|0,u=((r(A,2)^r(A,13)^r(A,22))+((A&B)^(A&C)^(B&C)))|0;J=G;G=F;F=E;E=(D+t)|0;D=C;C=B;B=A;A=(t+u)|0}
    [A,B,C,D,E,F,G,J].forEach((v,i)=>H[i]=(H[i]+v)|0);
  }return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")
}
function verifyCore(network,cert,generate=false){
 const check=(b,s)=>{if(!b)throw Error(s||"assertion")}, n=network.types.length*4, adj=Array.from({length:n},()=>[]), used=new Set(), edges=new Set();
 for(const [p,q,s] of network.edges){check(p>=0&&p<n&&q>=0&&q<n&&!used.has(p)&&!used.has(q)&&(s===0||s===1),"port");used.add(p);used.add(q);let i=p>>2,j=q>>2,k=Math.min(i,j)+","+Math.max(i,j);check(i!==j&&!edges.has(k),"simple");edges.add(k);adj[p].push([q,s]);adj[q].push([p,s])}
 check(used.size===n,"degree");
 for(let v=0;v<network.types.length;v++){let t=network.types[v];check(t==="E"||t==="B","type");if(t==="E")for(let j=1;j<4;j++){adj[4*v].push([4*v+j,0]);adj[4*v+j].push([4*v,0])}}
 const root=new Int32Array(n),sign=new Uint8Array(n);
 for(let p=0;p<n;p++)if(root[p]===0){root[p]=p+1;let q=[p];for(let i=0;i<q.length;i++){let u=q[i];for(const [v,s] of adj[u]){if(root[v])check(root[v]===root[u]&&sign[v]===(sign[u]^s),"parity");else{root[v]=root[u];sign[v]=sign[u]^s;q.push(v)}}}}
 const normalize=c=>[...new Set(c)].sort((a,b)=>a-b),key=c=>c.join(","),F0=new Map();let work=0,cap=10000000;
 const charge=k=>{work+=k;if(work>cap)throw Error("event cap")};
 const add=(F,c)=>{c=normalize(c);F.set(key(c),c)};
 for(const v of cert.B_vertices){check(network.types[v]==="B","not B");let ids=[...new Set(Array.from({length:4},(_,j)=>root[4*v+j]))].sort((a,b)=>a-b);for(let t=0;t<2**ids.length;t++){let sum=0;for(let j=0;j<4;j++)sum+=((t>>ids.indexOf(root[4*v+j]))&1)^sign[4*v+j];if(sum!==2)add(F0,ids.map((v,i)=>((t>>i)&1)?-v:v));charge(4)}}
 // Uniform whole-network complement symmetry discharges the one internal gauge pin.
 check(cert.gauge_anchor_root===Math.min(...[...F0.values()].flat().map(Math.abs)),"gauge");add(F0,[-cert.gauge_anchor_root]);
 let F=[...F0.values()];
 for(const v of cert.pivots){const p=[],q=[],rest=new Map();for(const c of F){charge(c.length+1);if(c.includes(v))p.push(c);else if(c.includes(-v))q.push(c);else add(rest,c)}check(p.length+q.length>0,"unused pivot");for(const a of p)for(const b of q){charge(a.length+b.length+1);const c=normalize([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);if(!c.some(l=>c.includes(-l)))add(rest,c)}F=[...rest.values()]}
 const simplify=(F,l)=>{const m=new Map();for(const c of F){charge(c.length+1);if(!c.includes(l))add(m,c.filter(x=>x!==-l))}return [...m.values()]};
 const conflict=F=>F.some(c=>!c.length);
 function build(F){
  let us=[];
  while(!conflict(F)){let u=Infinity;for(const c of F)if(c.length===1&&c[0]<u)u=c[0];if(u===Infinity)break;us.push(u);F=simplify(F,u)}
  if(conflict(F))return ["conflict",us];check(F.length,"SAT");
  let f=new Map();for(const c of F)for(const l of c){let v=Math.abs(l);f.set(v,(f.get(v)||0)+1);charge(1)}
  let v=[...f].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];return ["split",us,v,build(simplify(F,v)),build(simplify(F,-v))]
 }
 const tree=generate?build(F):cert.tree;let nodes=0;
 function replay(F,t){nodes++;check(Array.isArray(t)&&Array.isArray(t[1]),"tree");for(const l of t[1]){check(F.some(c=>c.length===1&&c[0]===l),"bad unit");F=simplify(F,l)}if(t[0]==="conflict"){check(conflict(F),"bad leaf");return}check(t[0]==="split"&&t.length===5,"split");replay(simplify(F,t[2]),t[3]);replay(simplify(F,-t[2]),t[4])}
 replay(F,tree);return {tree,nodes,work}
}
const fs=require("node:fs");const bytes=fs.readFileSync(process.argv[2],"utf8"),c=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));if(sha256(bytes)!==c.instance_id.split(":").at(-1)||8*bytes.length!==c.original_N_bits)throw Error("native identity mismatch");const r=verifyCore(JSON.parse(bytes),c,false);console.log(JSON.stringify({nodes:r.nodes,work:r.work,status:"VERIFIED"}));
