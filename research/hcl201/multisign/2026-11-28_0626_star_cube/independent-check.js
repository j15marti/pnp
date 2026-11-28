module.exports=function independent(G){
let count={walk:0,xor:0,rank:0,projection:0};let n=4*G.types.length,p=Array.from({length:n},(_,i)=>i),phase=new Uint8Array(n),sz=Array(n).fill(1);
function find(a){let s=0;while(p[a]!==a){s^=phase[a];a=p[a];count.walk++}return[a,s]}
function merge(a,b,s){let[x,u]=find(a),[y,v]=find(b);if(x===y){if((u^v)!==s)throw Error("signed conflict");return}if(sz[x]<sz[y]){[x,y]=[y,x];[u,v]=[v,u]}p[y]=x;phase[y]=u^v^s;sz[x]+=sz[y]}
for(let [a,b,s]of G.edges)merge(a,b,s);for(let i=0;i<G.types.length;i++)if(G.types[i]==="E")for(let j=1;j<4;j++)merge(4*i,4*i+j,0);
const owners=G.types.flatMap((t,i)=>t==="B"?[i]:[]),ports=owners.map(v=>[0,1,2,3].map(j=>find(4*v+j))),carriers=[...new Set(ports.flat().map(x=>x[0]))].sort((a,b)=>a-b),r=carriers.length,ix=new Map(carriers.map((x,i)=>[x,i])),bit=i=>1n<<BigInt(i),mask=bit(r)-1n;
const low=x=>{count.rank++;return x&-x};let E=new Map;
function norm(x){let a=x&mask,z=x&~mask;while(a){let l=low(a),v=E.get(l);if(v===undefined){z^=l;a^=l}else{z^=v&~mask;a^=v&mask;count.xor++}}return z}
for(let row of ports){let x=row.reduce((s,[a,b])=>s^bit(ix.get(a))^(b?bit(r):0n),0n),y=norm(x);if(y&mask)E.set(low(y&mask),y);else if(y)throw Error("parity")}
let M=new Map;
for(let j=0;j<ports.length;j++){let x=ports[j].map(([a,b])=>bit(ix.get(a))^(b?bit(r):0n)),a=norm(x[0]^x[1]),b=norm(x[0]^x[2]),l=[a&mask,b&mask,(a^b)&mask].sort((a,b)=>a<b?-1:1);if(!l[0]||l[1]===l[2])throw Error("nontriangle");let key=l.map(x=>x.toString(16)).join(","),g=M.get(key)||{l,ids:[],bad:0};g.ids.push(owners[j]);function val(f,w){let v=f&mask,c=Number(Boolean(f&bit(r)));return c^(v===l[0]?(w&1):v===l[1]?(w>>1):((w&1)^(w>>1)))}for(let w=0;w<4;w++)if(!val(a,w)&&!val(b,w))g.bad|=1<<w;M.set(key,g)}
let groups=[...M.values()],freq=new Map;for(let g of groups){if(![1,2,4,8].includes(g.bad))throw Error("not single forbidden");for(let f of g.l)freq.set(f,(freq.get(f)||0)+1)}
let chosen=new Set,three=0;for(let g of groups){let s=g.l.filter(f=>freq.get(f)>1);if(s.length===3)three++;for(let f of g.l)if(s.length<2&&!s.includes(f))s.push(f);for(let f of s)chosen.add(f)}
function rank(xs){let B=new Map;for(let x of xs)while(x){let z=low(x);if(!B.has(z)){B.set(z,x);break}x^=B.get(z);count.xor++}return B.size}
let tags=new Map,seen=Array(groups.length).fill(0),i=0;
for(let g of groups)for(let x of g.l.slice(0,2)){let t=bit(i++);while(x){let z=low(x),q=tags.get(z);if(!q){tags.set(z,[x,t]);break}x^=q[0];t^=q[1];count.xor+=2}if(!x){for(let j=0;j<groups.length;j++){let a=Number((t>>BigInt(2*j))&3n);if(a)seen[j]|=1<<a;count.projection++}}}
let peel=seen.filter(x=>[0,2,4,8].includes(x)).length;
let left=groups.filter(g=>g.ids[0]<owners[Math.floor(owners.length/2)]),right=groups.filter(g=>g.ids[0]>=owners[Math.floor(owners.length/2)]),span=rank([...chosen]),cut=rank(left.flatMap(g=>g.l))-0+rank(right.flatMap(g=>g.l))-span;
return {owners:owners.length,carriers:r,parityRank:E.size,groups:groups.length,allPaired:groups.every(g=>g.ids.length===2),three,chosen:chosen.size,rank:span,defect:chosen.size-span,peel,cut,count}
};
