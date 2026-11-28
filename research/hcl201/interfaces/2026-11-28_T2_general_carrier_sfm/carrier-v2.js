function sha(s){
 const K=[],H=[],pr=[];for(let n=2;K.length<64;n++){if(pr.some(p=>n%p===0))continue;pr.push(n);K.push((Math.cbrt(n)%1*4294967296)|0);if(H.length<8)H.push((Math.sqrt(n)%1*4294967296)|0)}
 let a=Array.from(s,c=>{let x=c.charCodeAt(0);if(x>127)throw Error("ASCII");return x});let l=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);a.push(0,0,0,0,(l>>>24)&255,(l>>>16)&255,(l>>>8)&255,l&255);
 const rr=(x,n)=>(x>>>n)|(x<<(32-n));let w=new Int32Array(64);
 for(let o=0;o<a.length;o+=64){for(let i=0;i<16;i++)w[i]=(a[o+4*i]<<24)|(a[o+4*i+1]<<16)|(a[o+4*i+2]<<8)|a[o+4*i+3];for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[i-7]+(rr(y,17)^rr(y,19)^(y>>>10)))|0}let [A,B,C,D,E,F,G,J]=H;for(let i=0;i<64;i++){let t=(J+(rr(E,6)^rr(E,11)^rr(E,25))+((E&F)^(~E&G))+K[i]+w[i])|0,u=((rr(A,2)^rr(A,13)^rr(A,22))+((A&B)^(A&C)^(B&C)))|0;J=G;G=F;F=E;E=(D+t)|0;D=C;C=B;B=A;A=(t+u)|0} [A,B,C,D,E,F,G,J].forEach((x,i)=>H[i]=(H[i]+x)|0)}
 return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
}
function study(g, pin=null){
 const cost={uf:0,localRows:0,rankProbes:0,xors:0,cutQueries:0,pairs:0,remainders:0}, max=10000000;
 const tick=(key,n=1)=>{cost[key]+=n;if(cost.rankProbes+cost.pairs+cost.remainders>max)throw Error("CAP")};
 const bit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 function uf(n){let p=Array.from({length:n},(_,i)=>i),z=Array(n).fill(0),sz=Array(n).fill(1);function find(i){let t=0;while(i!==p[i]){t^=z[i];i=p[i];cost.uf++}return [i,t]}function merge(i,j,s=0){let [a,x]=find(i),[b,y]=find(j);if(a===b){if((x^y)!==s)throw Error("inconsistent equality");return}if(sz[a]<sz[b])[a,b]=[b,a];p[b]=a;z[b]=x^y^s;sz[a]+=sz[b]}return {find,merge}}
 function basis(rows){let B=new Map();for(let x of rows)while(x){let b=x&-x;tick("rankProbes");if(!B.has(b)){B.set(b,x);break}x^=B.get(b);cost.xors++}return B}
 const rank=a=>basis(a).size;
 function rem(x,B){let y=0n;while(x){let b=x&-x;tick("remainders");if(B.has(b))x^=B.get(b);else{x^=b;y^=b}}return y}
 const u=uf(g.types.length*4);for(const [a,b,s] of g.edges)u.merge(a,b,s);g.types.forEach((t,i)=>{if(t==="E")for(let j=1;j<4;j++)u.merge(4*i,4*i+j,0)});
 const ids=new Map(),O=[],occ=[];let repeats=0;
 g.types.forEach((t,i)=>{if(t!=="B")return;let ps=[0,1,2,3].map(j=>u.find(4*i+j));let a=ps.map(([r])=>{if(!ids.has(r)){ids.set(r,ids.size);occ.push([])}return ids.get(r)}), signs=ps.reduce((s,p,j)=>s|(p[1]<<j),0);
 if(new Set(a).size<4)repeats++;
 let words=[];for(let w=0;w<16;w++){cost.localRows++;if([0,1,2,3].reduce((s,j)=>s+(((w^signs)>>j)&1),0)!==2)continue;let ok=true;for(let j=0;j<4;j++){for(let k=0;k<j;k++)if(a[j]===a[k]&&((w>>j)&1)!==((w>>k)&1))ok=false;if(pin&&a[j]===pin[0]&&((w>>j)&1)!==pin[1])ok=false}if(ok)words.push(w)}
 if(!words.length)throw Error("local contradiction");let diff=words.map(w=>BigInt(w^words[0])),d=rank(diff),eq=[];for(let h=1;h<16;h++)if(diff.every(x=>!parity(Number(x)&h)))eq.push(h);
 let H=eq.map(h=>a.reduce((s,c,j)=>(h>>j)&1?s^bit(c):s,0n));a.forEach((c,j)=>occ[c].push([O.length,j]));O.push({v:i,a,signs,words,d,H,closed:words.every(w=>words.includes(w^15))})});
 const m=O.length,r=ids.size,ix=O.map((_,i)=>i),closed=O.every(o=>o.closed),allH=O.flatMap(o=>o.H),R=rank(allH);
 let coord=0;const col=O.map(()=>[0n,0n,0n,0n]);for(let a of occ){let [i,j]=a[0];for(let [k,l] of a.slice(1)){let b=bit(coord++);col[i][j]^=b;col[k][l]^=b}}
 const image=(i,w)=>col[i].reduce((s,b,j)=>(w>>j)&1?s^b:s,0n);
 const D=O.map((o,i)=>o.words.map(w=>image(i,w))),V=D.map(a=>a.map(x=>x^a[0])),K=closed?ix.map(i=>image(i,15)):[],KB=basis(K),rawRank=rank(V.flat()),qRank=rank(K.concat(V.flat()))-KB.size;
 const dsum=a=>a.reduce((s,i)=>s+O[i].d,0);
 function collapse(I){let v=uf(r);for(let i of I)for(let j=1;j<4;j++)v.merge(O[i].a[0],O[i].a[j]);let roots=Array.from({length:r},(_,j)=>v.find(j)[0]);let h=O.flatMap(o=>o.H.map(x=>{let s=0n;for(let j=0;j<r;j++)if(x&bit(j))s^=bit(roots[j]);return s}));return {c:new Set(roots).size,rank:rank(h)}}
 // Faster sparse collapse for production calls: carrier equations have at most four entries.
 function collapseSparse(I){let v=uf(r);for(let i of I)for(let j=1;j<4;j++)v.merge(O[i].a[0],O[i].a[j]);let roots=Array.from({length:r},(_,j)=>v.find(j)[0]);let map=new Map(Array.from({length:r},(_,j)=>[bit(j),bit(roots[j])]));let h=allH.map(x=>{let s=0n;while(x){let b=x&-x;s^=map.get(b);x^=b}return s});return {c:new Set(roots).size,rank:rank(h)}}
 const C=collapseSparse(ix).c;
 if(rawRank!==dsum(ix)-r+R)throw Error("raw total identity");
 if(closed&&(KB.size!==m-C||qRank!==dsum(ix)-m-r+R+C))throw Error("quot total identity");
 function cut(P,verify=true){tick("cutQueries");let set=new Set(P),Q=ix.filter(i=>!set.has(i)),ip=0n,iq=0n,nP=0,nQ=0;occ.forEach((a,j)=>{if(a.every(([i])=>set.has(i))){ip|=bit(j);nP++}else if(a.every(([i])=>!set.has(i))){iq|=bit(j);nQ++}});
 let vP=P.flatMap(i=>O[i].H.map(x=>x&ip)),vQ=Q.flatMap(i=>O[i].H.map(x=>x&iq)),raw=r-nP-nQ+rank(vP)+rank(vQ)-R,quot=null;
 if(closed){let p=collapseSparse(P),q=collapseSparse(Q);quot=r-p.c-q.c+p.rank+q.rank-R+C}
 if(verify){let a=P.flatMap(i=>V[i]),b=Q.flatMap(i=>V[i]);if(raw!==rank(a)+rank(b)-rawRank)throw Error("raw cut mismatch");if(closed&&quot!==rank(K.concat(a))+rank(K.concat(b))-2*KB.size-qRank)throw Error("quot cut mismatch")}
 return [raw,quot]}
 let cuts=[];let order=ix.slice();let adj=O.map(()=>new Set());for(let a of occ)for(let [i] of a.slice(1)){adj[a[0][0]].add(i);adj[i].add(a[0][0])}let bfs=[],seen=new Set();for(let i of ix)if(!seen.has(i)){let q=[i];seen.add(i);for(let j=0;j<q.length;j++){bfs.push(q[j]);for(let v of [...adj[q[j]]].sort((a,b)=>a-b))if(!seen.has(v)){seen.add(v);q.push(v)}}}
 for(let [name,a] of [["source",order],["incidenceBFS",bfs]])for(let p of [0.25,0.5,0.75]){let P=a.slice(0,Math.max(1,Math.floor(m*p)));try{let [raw,quot]=cut(P);cuts.push({name,p,raw,quot})}catch(e){if(e.message!=="CAP")throw e;cuts.push({name,p,status:"UNKNOWN_CAP"});break}}
 let exactSFM=null;
 if(m<=12){let vals=[];for(let mask=0;mask<2**m;mask++)vals.push(cut(ix.filter(i=>(mask>>i)&1))[0]);let tests=0;for(let a=0;a<vals.length;a++)for(let b=0;b<vals.length;b++){if(vals[a]+vals[b]<vals[a&b]+vals[a|b]||vals[a]!==vals[(vals.length-1)^a])throw Error("SFM axiom");tests++}let best=Infinity,maskBest=0;for(let a=0;a<vals.length;a++)if((a&1)&&!(a&(1<<(m-1)))&&vals[a]<best){best=vals[a];maskBest=a}let greedy=[],prev=vals[1],mask=1;for(let i=1;i<m-1;i++){let n=mask|(1<<i);greedy.push(vals[n]-prev);prev=vals[n];mask=n}let lb=vals[1]+greedy.reduce((s,x)=>s+Math.min(x,0),0);exactSFM={tests,constrainedMin:best,minMask:maskBest,singleGreedyLowerBound:lb};}
 // Target-conditioned exact DP, raw or quotient. Small controls and capped native runs.
 function solve(order,quot){
 let B=quot?KB:new Map(),DD,VV,peak=0,states=0,steps=0,terminal="UNKNOWN",witness=null;const capStates=512,capPairs=100000;
 function go(I){let set=new Set(I),ext=ix.filter(i=>!set.has(i)),EB=basis(ext.flatMap(i=>VV[i])),offset=ext.reduce((s,i)=>s^DD[i][0],0n),out=new Map();
 const accept=(x,tag)=>{if(rem(x^offset,EB)===0n&&!out.has(x)){out.set(x,tag);states++;peak=Math.max(peak,out.size);if(out.size>capStates)throw Error("STATE_CAP")}};
 if(I.length===1){let i=I[0];DD[i].forEach((x,j)=>accept(x,[i,j]));return out}
 let mid=I.length>>1,L=go(I.slice(0,mid)),R=go(I.slice(mid));for(let [x,a] of L)for(let [y,b] of R){tick("pairs");if(++steps>capPairs)throw Error("PAIR_CAP");accept(x^y,[a,b])}return out}
 try{DD=D.map(a=>a.map(x=>rem(x,B)));VV=DD.map(a=>a.map(x=>x^a[0]));let final=go(order);terminal=final.has(0n)?"SAT":"UNSAT";if(terminal==="SAT"){let ws=Array(m);function recover(t){if(typeof t[0]==="number"){ws[t[0]]=O[t[0]].words[t[1]];return}recover(t[0]);recover(t[1])}recover(final.get(0n));if(quot){let diff=ws.reduce((s,w,i)=>s^image(i,w),0n),T=new Map();for(let i of ix){let x=K[i],tag=bit(i);while(x){let b=x&-x;tick("rankProbes");if(!T.has(b)){T.set(b,[x,tag]);break}let [v,t]=T.get(b);x^=v;tag^=t}}let flips=0n;while(diff){let b=diff&-diff;if(!T.has(b))throw Error("lift");let [v,t]=T.get(b);diff^=v;flips^=t;tick("rankProbes")}ws=ws.map((w,i)=>flips&bit(i)?w^15:w)}
 let assigned=new Map();for(let i of ix)O[i].a.forEach((c,j)=>{let b=(ws[i]>>j)&1;if(assigned.has(c)&&assigned.get(c)!==b)throw Error("bad lift");assigned.set(c,b)});let bits=Array.from({length:g.types.length*4},(_,p)=>{let [root,s]=u.find(p);return (assigned.get(ids.get(root))??0)^s});if(!g.edges.every(([a,b,s])=>(bits[a]^bits[b])===s)||!g.types.every((t,i)=>{let a=bits.slice(4*i,4*i+4);return t==="E"?a.every(x=>x===a[0]):a.reduce((s,x)=>s+x,0)===2}))throw Error("original witness fail");witness=bits.join("")}}
 catch(e){if(!["STATE_CAP","PAIR_CAP","CAP"].includes(e.message))throw e;terminal="UNKNOWN"}
 return {terminal,peak,states,pairs:steps,witness}}
 let dp=[];if(m>0&&cost.rankProbes+cost.remainders+cost.pairs<max){dp.push({mode:"raw",...solve(order,false)});if(closed)dp.push({mode:"quotient",...solve(order,true)})}
 return {m,r,repeats,closed,R,C,rawRank,qRank,periodRank:KB.size,rawSingletonUpper:Math.max(...O.map(o=>o.d)),quotSingletonUpper:closed?Math.max(...O.map(o=>o.d-1)):null,cuts,exactSFM,dp,cost};
}
module.exports={sha,study};

function cnfRun(dimacs){
 const lines=dimacs.trim().split("\n"),n=Number(lines.shift().split(" ")[2]),F=lines.map(x=>x.trim().split(/\s+/).map(Number).slice(0,-1));
 let visits=0,checkVisits=0,nodes=0;const max=1000000;
 function prop(a,checking=false){let change=true;while(change){change=false;for(let c of F){let sat=false,free=0,last=0;for(let l of c){if(checking)checkVisits++;else if(++visits>max)throw Error("CAP");let v=a[Math.abs(l)];if(v===-1){free++;last=l}else if(v===Number(l>0)){sat=true;break}}if(sat)continue;if(!free)return false;if(free===1){a[Math.abs(last)]=Number(last>0);change=true}}}return true}
 const root=Array(n+1).fill(-1);prop(root);const rootForced=root.slice(1).filter(x=>x!==-1).length;
 function go(a){nodes++;if(!prop(a))return ["NO"];let i=a.findIndex((x,i)=>i>0&&x===-1);if(i<0)return ["YES",a.slice(1)];let b=a.slice(),c=a.slice();b[i]=0;c[i]=1;let t=go(b);if(t[0]==="YES")return t;let u=go(c);if(u[0]==="YES")return u;return ["SPLIT",i,t,u]}
 function verify(t,a){if(t[0]==="YES")return F.every(c=>c.some(l=>t[1][Math.abs(l)-1]===Number(l>0)));let ok=prop(a,true);if(t[0]==="NO")return !ok;if(!ok)return true;let i=t[1];if(a[i]!==-1)return false;let b=a.slice(),c=a.slice();b[i]=0;c[i]=1;return verify(t[2],b)&&verify(t[3],c)}
 try{let t=go(Array(n+1).fill(-1));let verified=verify(t,Array(n+1).fill(-1));if(!verified)throw Error("replay");return {n,clauses:F.length,rootForced,terminal:t[0]==="YES"?"SAT":"UNSAT",nodes,visits,checkVisits,verified,tree:t}}catch(e){if(e.message!=="CAP")throw e;return {n,clauses:F.length,rootForced,terminal:"UNKNOWN",nodes,visits,checkVisits}}
}
module.exports.cnfRun=cnfRun;
