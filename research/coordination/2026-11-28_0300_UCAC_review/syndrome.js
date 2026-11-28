function sha(s){const p=[],h=[],k=[];for(let i=2;k.length<64;i++){if(p.some(q=>i%q===0))continue;p.push(i);if(h.length<8)h.push((Math.sqrt(i)%1*4294967296)|0);k.push((Math.cbrt(i)%1*4294967296)|0)}const a=Array.from(s,c=>c.charCodeAt(0));if(a.some(x=>x>127))throw Error("ASCII");const l=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let j=7;j>=0;j--)a.push(Math.floor(l/2**(8*j))%256);const R=(x,n)=>(x>>>n)|(x<<(32-n));for(let i=0;i<a.length;i+=64){let w=[];for(let j=0;j<16;j++)w.push((a[i+4*j]<<24)|(a[i+4*j+1]<<16)|(a[i+4*j+2]<<8)|a[i+4*j+3]);for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(R(x,7)^R(x,18)^(x>>>3))+w[j-7]+(R(y,17)^R(y,19)^(y>>>10)))|0}let [A,B,C,D,E,F,G,H]=h;for(let j=0;j<64;j++){let t=(H+(R(E,6)^R(E,11)^R(E,25))+((E&F)^(~E&G))+k[j]+w[j])|0,u=((R(A,2)^R(A,13)^R(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,H]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}[A,B,C,D,E,F,G,H].forEach((v,j)=>h[j]=(h[j]+v)|0)}return h.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}

function analyze(g){
 const counts={union:0,geTests:0,geXor:0,rows:0,coverBranches:0,subsetTests:0,checks:0};
 const n=g.types.length*4,pa=Array.from({length:n},(_,i)=>i),sz=Array(n).fill(1),sg=Array(n).fill(0);
 function find(x){let s=0;while(pa[x]!==x){s^=sg[x];x=pa[x];counts.union++}return [x,s]}
 function join(a,b,s){let [u,x]=find(a),[v,y]=find(b);if(u===v)return (x^y)===s;if(sz[u]<sz[v])[u,v]=[v,u];pa[v]=u;sg[v]=s^x^y;sz[u]+=sz[v];return true}
 for(const [a,b,s] of g.edges)if(!join(a,b,s))return {decision:"NO",reason:"signed edge conflict",counts};
 for(let i=0;i<g.types.length;i++)if(g.types[i]==="E")for(let j=1;j<4;j++)if(!join(4*i,4*i+j,0))return {decision:"NO",reason:"equality conflict",counts};
 const roots=new Map(),port=pa.map((_,i)=>{let [r,s]=find(i);if(!roots.has(r))roots.set(r,roots.size+1);return (1n<<BigInt(roots.get(r)))^BigInt(s)});
 const rows=[];for(let i=0;i<g.types.length;i++)if(g.types[i]==="B")rows.push(port.slice(4*i,4*i+4));
 const basis=new Map(),low=x=>x&-x;
 function insert(B,x){while(x&~1n){let p=low(x&~1n);counts.geTests++;if(!B.has(p)){B.set(p,x);return 1}x^=B.get(p);counts.geXor++}return x===1n?-1:0}
 function reduce(B,x){for(const [p,v] of B){counts.geTests++;if(x&p){x^=v;counts.geXor++}}return x}
 function sorted(B){return new Map([...B].sort((a,b)=>a[0]<b[0]?-1:1))}
 for(const row of rows)if(insert(basis,row.reduce((a,b)=>a^b,0n))<0)return {decision:"NO",reason:"affine parity",counts};
 const parityRank=basis.size;let pair=[],forced=0;
 for(;;){const B=sorted(basis);pair=[];let changed=false;for(const [a,b,c,d] of rows){let p=reduce(B,a^b),q=reduce(B,a^c);counts.rows++;if(p===1n||q===1n||(p^q)===1n)continue;if(!p&&!q)return {decision:"NO",reason:"forced all equal",counts};if(!p||!q||p===q){const v=p||q,add=insert(basis,v^1n);if(add<0)return {decision:"NO",reason:"forced difference conflict",counts};if(add){forced++;changed=true}continue}pair.push([p,q])}if(!changed)break}
 const forms=[],ids=new Map(),edges=[],es=new Set();function id(p){if(!ids.has(p)){ids.set(p,forms.length);forms.push(p)}return ids.get(p)}
 for(const [p,q] of pair){const a=id(p),b=id(q),k=[Math.min(a,b),Math.max(a,b)].join(",");if(!es.has(k)){es.add(k);edges.push([a,b])}}
 const dep=new Map(),H=[];for(let i=0;i<forms.length;i++){let v=forms[i],t=1n<<BigInt(i+1);while(v&~1n){const p=low(v&~1n);counts.geTests++;if(!dep.has(p)){dep.set(p,[v,t]);break}let [a,b]=dep.get(p);v^=a;t^=b;counts.geXor++}if(!(v&~1n)){let parity=0;for(let s=t;s;s&=s-1n)parity^=1;H.push(t^BigInt(Number(v)^parity))}}
 const m=forms.length,par=Array.from({length:m},(_,i)=>i);function root(i){while(par[i]!==i)i=par[i];return i}function merge(a,b){par[root(a)]=root(b)}
 const indices=x=>{const a=[];for(let i=0;i<m;i++)if(x&(1n<<BigInt(i+1)))a.push(i);return a};
 for(const [a,b] of edges)merge(a,b);const hi=H.map(indices);for(const a of hi)for(let j=1;j<a.length;j++)merge(a[0],a[j]);
 const groups=new Map();for(let i=0;i<m;i++){let r=root(i);if(!groups.has(r))groups.set(r,{vars:[],edges:[],H:[]});groups.get(r).vars.push(i)}for(const e of edges)groups.get(root(e[0])).edges.push(e);for(let i=0;i<H.length;i++)groups.get(root(hi[i][0])).H.push(H[i]);
 function solve(B){let x=0n;for(const [p,row] of [...sorted(B)].reverse()){let t=row&x,parity=Number(row&1n);while(t){t&=t-1n;parity^=1}if(parity)x|=p}return x}
 const report=[];let zeros=0n,unknown=false,no=false;
 for(const C of groups.values()){
  const cover=new Set();for(const [a,b] of C.edges)if(!cover.has(a)&&!cover.has(b)){cover.add(a);cover.add(b)}
  const cv=[...cover],k=C.H.length,B=new Map();for(const h of C.H)if(insert(B,h)<0)throw Error("dependent H");
  let witness=null,method="cap",attempts=0;
  const check=z=>{counts.checks++;return C.edges.every(([a,b])=>!((z>>BigInt(a+1)&1n)&&(z>>BigInt(b+1)&1n)))&&C.H.every(h=>{let t=h&z,p=Number(h&1n);while(t){t&=t-1n;p^=1}return !p})};
  if(check(0n)){witness=0n;method="zero syndrome"}
  else if(cv.length<=10){method="cover";for(let s=0;s<2**cv.length;s++){attempts++;counts.coverBranches++;const T=new Map(B),one=new Set(cv.filter((_,i)=>s>>i&1));let ok=true;for(const i of cv)if(insert(T,(1n<<BigInt(i+1))^BigInt(one.has(i)))<0){ok=false;break}if(!ok)continue;for(const [a,b] of C.edges){if(one.has(a)&&one.has(b)){ok=false;break}if(one.has(a)&&insert(T,1n<<BigInt(b+1))<0){ok=false;break}if(one.has(b)&&insert(T,1n<<BigInt(a+1))<0){ok=false;break}}if(ok){const z=solve(T);if(!check(z))throw Error("cover witness");witness=z;break}}}
  else if(k<=2){method="rank enumeration";outer:for(let i=-1;i<C.vars.length;i++)for(let j=-1;j<i;j++){if(k===1&&j!==-1)continue;attempts++;counts.subsetTests++;let z=(i<0?0n:1n<<BigInt(C.vars[i]+1))^(j<0?0n:1n<<BigInt(C.vars[j]+1));if(check(z)){witness=z;break outer}}}
  if(witness!==null)zeros|=witness;else if(method==="cap")unknown=true;else no=true;
  report.push({variables:C.vars.length,edges:C.edges.length,syndromeRank:k,cover:cv.length,method,attempts,status:witness!==null?"YES":method==="cap"?"UNKNOWN":"NO"});
 }
 let decision=no?"NO":unknown?"UNKNOWN":"YES",verified=false;
 if(decision==="YES"){const T=new Map(basis);for(let i=0;i<m;i++)if(insert(T,forms[i]^1n^(zeros>>BigInt(i+1)&1n))<0)throw Error("lift failed");const x=solve(T);const vals=port.map(p=>{let t=p&x,b=Number(p&1n);while(t){t&=t-1n;b^=1}return b});verified=g.edges.every(([a,b,s])=>(vals[a]^vals[b])===s)&&g.types.every((t,i)=>{let a=vals.slice(i*4,i*4+4);return t==="E"?a.every(x=>x===a[0]):a.reduce((x,y)=>x+y,0)===2});if(!verified)throw Error("native witness")}
 return {decision,verified,carriers:roots.size,balance:rows.length,parityRank,forced,finalRank:basis.size,forms:m,formRank:dep.size,syndromeRank:H.length,edges:edges.length,components:report,counts}
}

function cnfSolve(dimacs){const F=dimacs.trim().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),n=Number(dimacs.split(/\s+/)[2]);let visits=0,nodes=0,forced=0;function go(a){nodes++;if(nodes>100000)return "UNKNOWN";for(;;){let changed=false,done=true;for(const c of F){let sat=false,u=[];for(const l of c){visits++;let v=a[Math.abs(l)];if(v===undefined)u.push(l);else if(v===(l>0)){sat=true;break}}if(sat)continue;done=false;if(!u.length)return "NO";if(u.length===1){a[Math.abs(u[0])]=u[0]>0;forced++;changed=true}}if(done)return "YES";if(!changed)break}let v=0;for(let i=1;i<=n;i++)if(a[i]===undefined){v=i;break}if(!v)throw Error("unresolved");let x=a.slice();x[v]=false;let l=go(x);if(l==="YES")return l;x=a.slice();x[v]=true;let r=go(x);return r==="YES"?"YES":l==="NO"&&r==="NO"?"NO":"UNKNOWN"}return {decision:go([]),visits,nodes,forced}}

module.exports={sha,analyze,cnfSolve};
