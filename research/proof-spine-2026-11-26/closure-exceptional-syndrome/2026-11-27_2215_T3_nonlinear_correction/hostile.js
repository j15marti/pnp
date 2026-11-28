function sha(s){let k=[],h=[],p=2;while(k.length<64){if(!Array.from({length:Math.floor(Math.sqrt(p))-1},(_,i)=>i+2).some(i=>p%i===0)){if(h.length<8)h.push((Math.sqrt(p)%1*4294967296)|0);k.push((Math.cbrt(p)%1*4294967296)|0)}p++}const a=Array.from(s,ch=>ch.charCodeAt(0));if(a.some(x=>x>127)||a.length*8>=2**32)throw Error("hash input cap");const n=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);a.push(0,0,0,0,(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255);const rr=(v,n)=>(v>>>n)|(v<<(32-n));for(let i=0;i<a.length;i+=64){let w=[];for(let j=0;j<16;j++)w[j]=(a[i+4*j]<<24)|(a[i+4*j+1]<<16)|(a[i+4*j+2]<<8)|a[i+4*j+3];for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[j-7]+(rr(y,17)^rr(y,19)^(y>>>10)))|0}let [A,B,C,D,E,F,G,H]=h;for(let j=0;j<64;j++){let t=(H+(rr(E,6)^rr(E,11)^rr(E,25))+((E&F)^(~E&G))+k[j]+w[j])|0,u=((rr(A,2)^rr(A,13)^rr(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,H]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}h=h.map((v,j)=>(v+[A,B,C,D,E,F,G,H][j])|0)}return h.map(v=>(v>>>0).toString(16).padStart(8,"0")).join("")}
function compile(instance){
 const lines=instance.dimacs.trimEnd().split("\n"),h=lines.shift().split(" ").map((s,i)=>i>=2?Number(s):s);
 if(h[0]!=="p"||h[1]!=="cnf"||h[2]!==instance.nvars||h[3]!==lines.length)throw Error("header");
 const n=instance.nvars,F=[],parents=[];let next=n;
 const add=(a,id)=>{F.push(a);parents.push(id)};
 lines.forEach((line,i)=>{const a=line.split(/\s+/).map(Number);if(a.pop()!==0||a.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>n))throw Error("bad clause");const id=i+1;if(a.length===0){let v=++next;add([v,v,v],id);add([-v,-v,-v],id)}else if(a.length<=3){while(a.length<3)a.push(a[a.length-1]);add(a,id)}else{let prev=++next;add([a[0],a[1],prev],id);for(let j=2;j<a.length-2;j++){let t=++next;add([-prev,a[j],t],id);prev=t}add([-prev,a[a.length-2],a[a.length-1]],id)}});
 const types=[],used=[],edges=[],groups=new Map(),reps={},owners=[];
 const V=(t,owner)=>{types.push(t);used.push(0);owners.push(owner);return types.length-1};
 const P=v=>{if(used[v]>=4)throw Error("port overflow");return 4*v+used[v]++};
 const E=(a,b,s=0)=>edges.push([a,b,s]);
 const wire=(a,b,s)=>{const v=Array.from({length:5},()=>V("E",["wire",a,b]));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)};
 const occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};
 F.forEach(([a,b,c],i)=>{const L=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let k=0;k<2;k++){let v=V("B",["clause",parents[i],i,j,k]);for(const [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v))}});
 for(const [id,O] of groups){if(O.length%2||O.length<2)throw Error("occurrence parity");reps[id]=O[0];if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}const a=Array.from({length:(O.length-2)/2},()=>V("E",["carrier",id]));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(const v of a)while(used[v]<4){const [p,s]=O[k++];wire(P(v),p,s)}if(k!==O.length)throw Error("fanout")}
 const seen=new Set(),ports=new Set();for(const [a,b,s] of edges){let u=Math.floor(a/4),v=Math.floor(b/4),key=Math.min(u,v)+":"+Math.max(u,v);if(u===v||seen.has(key)||ports.has(a)||ports.has(b)||![0,1].includes(s))throw Error("not simple signed 4-regular");seen.add(key);ports.add(a);ports.add(b)}
 if(used.some(x=>x!==4)||ports.size!==4*types.length)throw Error("degree");
 const network={format:"STRICT-EB4-v1",types,edges};
 return {network,source_map:{original_n:n,ternary_clauses:F,original_clause_ids:parents,representative_ports:reps,vertex_provenance:owners}};
}

function hostile(sha,compile){
const ck=(x,m)=>{if(!x)throw Error(m||"assert")},T=[[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],xor=(a,b)=>{let c=new Set(a);for(let v of b)c.has(v)?c.delete(v):c.add(v);return c},par=(x)=>{let b=0;while(x){x&=x-1;b^=1}return b},wt=x=>{let b=0;while(x){x&=x-1;b++}return b};
function certificate(scopes,vars,clauses,target,d){
let basis=new Map(),generators=[],ops=0;
function violation(c){let P=new Set([0]);for(let l of c){let m=1<<vars.indexOf(Math.abs(l)),Q=new Set();for(let a of P){if(l>0)Q=xor(Q,[a]);Q=xor(Q,[a|m])}P=Q}return P}
let groups=scopes.map(([a,b])=>xor(violation(clauses[a]),violation(clauses[b])));
function reduce(p,parents,insert){let q=new Set(p),c=new Set(parents);while(q.size){let k=Math.max(...q);ops++;if(!basis.has(k)){if(insert)basis.set(k,{q,c});return{q,c}}let z=basis.get(k);q=xor(q,z.q);c=xor(c,z.c)}return{q,c}}
for(let i=0;i<groups.length;i++)for(let m=0;m<128;m++)if(wt(m)<=d-2){let p=new Set();for(let a of groups[i])p=xor(p,[a|m]);let id=generators.length;generators.push({scope:i,m});reduce(p,[id],true)}
let p=new Set(target.b?[0]:[]);p.add(1<<vars.indexOf(target.u));p.add(1<<vars.indexOf(target.v));let q=reduce(p,[],false);let proof=q.q.size?null:[...q.c].map(i=>generators[i]);return{d,rank:basis.size,rows:generators.length,ops,proof}
}
function make(t,twist=true){
let C=[],blocks=[];for(let i=0;i<t;i++){let V=[i+1,(i+1)%t+1,t+5*i+1,t+5*i+2,t+5*i+3,t+5*i+4,t+5*i+5];let ids=[];for(let a of T){let c=a.map(j=>V[j]*(twist&&i===t-1&&j===1?-1:1));ids.push(C.length);C.push(c,c.map(x=>-x))}blocks.push({V,ids})}let dimacs=`p cnf ${6*t} ${C.length}\n`+C.map(c=>c.join(" ")+" 0\n").join("");return{C,blocks,dimacs,nvars:6*t}
}
function discover(C,n){
let groups=new Map();for(let i=0;i<C.length;i++){let k=C[i].map(Math.abs).sort((a,b)=>a-b).join(",");if(!groups.has(k))groups.set(k,[]);groups.get(k).push(i)}let scopes=[...groups.values()];ck(scopes.every(g=>g.length===2&&C[g[0]].every(l=>C[g[1]].includes(-l))),"paired clauses");let degree=Array(n+1).fill(0);for(let g of scopes)for(let l of C[g[0]])degree[Math.abs(l)]++;
let adj=Array.from({length:n+1},()=>[]),P=scopes.map(g=>C[g[0]].map(Math.abs));for(let a of P){let p=a.filter(v=>degree[v]===3);ck(p.length===2);adj[p[0]].push(p[1]);adj[p[1]].push(p[0])}
let seen=new Set(),found=[];for(let v=1;v<=n;v++)if(degree[v]===3&&!seen.has(v)){let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(let z of adj[q[i]])if(!seen.has(z)){seen.add(z);q.push(z)}ck(q.length===4);let ids=scopes.filter((g,i)=>P[i].some(v=>q.includes(v))),vars=[...new Set(ids.flatMap(g=>C[g[0]].map(Math.abs)))].sort((a,b)=>a-b),ports=vars.filter(v=>!q.includes(v)),shared=ports.filter(v=>degree[v]===4);ck(ids.length===6&&vars.length===7&&shared.length===2);found.push({ids,vars,shared})}return found
}
function up(C,guard,n,stats){let a=new Int8Array(n+1);for(let l of guard)a[Math.abs(l)]=Math.sign(l);for(;;){let ch=false;for(let c of C){stats.rows++;let free=0,last=0,hit=false;for(let l of c){let x=a[Math.abs(l)];if(x===Math.sign(l)){hit=true;break}if(!x){free++;last=l}}if(hit)continue;if(!free)return false;if(free===1){a[Math.abs(last)]=Math.sign(last);ch=true}}if(!ch)return true}}
function checkWord(C,vars,w){return C.every(c=>c.some(l=>Boolean(w>>vars.indexOf(Math.abs(l))&1)===(l>0)))}
let output=[];for(let t of [3,6,12]){
 let F=make(t),n=F.nvars,C=F.C,m=C.length,stats={rows:0,probes:0,conflicts:0};let tryGuard=g=>{stats.probes++;if(!up(C,g,n,stats))stats.conflicts++};tryGuard([]);for(let i=1;i<=n;i++){tryGuard([i]);tryGuard([-i]);for(let j=i+1;j<=n;j++)for(let a of [-1,1])for(let b of [-1,1])tryGuard([a*i,b*j])}ck(!stats.conflicts,"width2");
 let D=discover(C,n),certs=[],checkRows=0,identityChecks=0,groupPairs=new Set(),scopes=new Set();for(let g of D){let {ids,vars,shared}=g,[u,v]=shared,local=ids.flatMap(i=>i.map(j=>C[j])),valid=[];for(let w=0;w<128;w++){checkRows++;if(checkWord(local,vars,w))valid.push(w)}ck(valid.length>0);let b=((valid[0]>>vars.indexOf(u))^(valid[0]>>vars.indexOf(v)))&1;ck(valid.every(w=>(((w>>vars.indexOf(u))^(w>>vars.indexOf(v)))&1)===b));let target={u,v,b},ranks=[2,3,4].map(d=>certificate(ids,vars,C,target,d));ck(!ranks[0].proof&&!ranks[1].proof&&ranks[2].proof,"degree");
 for(let w=0;w<128;w++){let lhs=0;for(let p of ranks[2].proof){let a=ids[p.scope].map(i=>C[i]),val=a.reduce((s,c)=>s^+(!checkWord([c],vars,w)),0);if((w&p.m)===p.m)lhs^=val}let rhs=b^((w>>vars.indexOf(u))&1)^((w>>vars.indexOf(v))&1);ck(lhs===rhs,"truth identity");identityChecks++}
 for(let p of ids){let v=C[p[0]].map(Math.abs).sort((a,b)=>a-b);ck(!scopes.has(v.join()));scopes.add(v.join());for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=v[i]+":"+v[j];ck(!groupPairs.has(k));groupPairs.add(k)}}
 certs.push({...g,target,ranks,validWords:valid})}
 let sum=new Set(),b=0;for(let c of certs){sum=xor(sum,[c.target.u,c.target.v]);b^=c.target.b}ck(!sum.size&&b===1,"cycle");
 // Proper-block deletion witnesses: assign cycle from one endpoint of omitted block, choose local extension from the actual enumerated table.
 let deletionChecks=0;for(let skip=0;skip<t;skip++){let a=new Map([[certs[skip].target.u,0]]);for(let iter=0;iter<t;iter++)for(let j=0;j<t;j++)if(j!==skip){let {u,v,b}=certs[j].target;if(a.has(u))a.set(v,a.get(u)^b);else if(a.has(v))a.set(u,a.get(v)^b)}for(let j=0;j<t;j++)if(j!==skip){let c=certs[j],w=c.validWords.find(w=>c.shared.every(v=>a.get(v)===((w>>c.vars.indexOf(v))&1)));ck(w!==undefined,"deletion");c.vars.forEach((v,i)=>a.set(v,w>>i&1));for(let p of c.ids)for(let i of p){ck(C[i].some(l=>a.get(Math.abs(l))===+(l>0)));deletionChecks++}}}
 let G=compile(F),native=JSON.stringify(G.network)+"\n",map=JSON.stringify(G.source_map)+"\n",dig=sha(F.dimacs),nd=sha(native);
 output.push({alias:"T3-TWISTED-FANO-RING-"+t,instance_id:"DIMACS-CNF-v1:sha256:"+dig,short_id:"T3-TWISTED-FANO-RING-"+t+"@"+dig.slice(0,12),original_N_bits:F.dimacs.length*8,dimacs:F.dimacs,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{variables:[1,n],clauses:[1,m]},native:{instance_id:"STRICT-EB4-v1:sha256:"+nd,N_bits:native.length*8,vertices:G.network.types.length,edges:G.network.edges.length,map_sha256:sha(map)},n,m,stats,groupedRank:6*t,rawRank:12*t,groupedAffineRank:0,checkRows,identityChecks,deletionChecks,certs});
}
return output
}
console.log(JSON.stringify(hostile(sha,compile),null,2));
