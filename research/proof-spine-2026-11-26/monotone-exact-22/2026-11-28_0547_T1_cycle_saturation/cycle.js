// Deterministic alternating-cycle affine saturation; run: node cycle.js match-period.js
function engine(F,mode="hybrid"){
 const n=F.rows.length,ct={matching:0,reach:0,path:0,label:0,xor:0,cycle:0,spectral:0,check:0},hex=x=>x.toString(16),val=x=>BigInt("0x"+x),target=val(F.target);
 const rows=F.rows.map(r=>{const a=new Map();for(const e of r){ct.label++;if(!a.has(e.j))a.set(e.j,[]);const v=val(e.v);if(!a.get(e.j).includes(v))a.get(e.j).push(v)}return a});
 function basis(xs=[]){const b=new Map();function ins(x,tag=0n){while(x){const k=x.toString(2).length-1;if(!b.has(k)){b.set(k,[x,tag]);return true}const [y,t]=b.get(k);x^=y;tag^=t;ct.xor++}return false}function red(x){let tag=0n;while(x){const k=x.toString(2).length-1;if(!b.has(k))break;const [y,t]=b.get(k);x^=y;tag^=t;ct.xor++}return [x,tag]}for(const x of xs)ins(x);return {b,ins,red,vec:()=>[...b.values()].map(x=>x[0])}}
 function match(){const own=Array(n).fill(-1);function aug(i,seen){for(const j of rows[i].keys()){ct.matching++;if(own[j]<0&&!seen.has(j)){own[j]=i;return true}}for(const j of rows[i].keys()){ct.matching++;if(seen.has(j))continue;seen.add(j);if(aug(own[j],seen)){own[j]=i;return true}}return false}for(let i=0;i<n;i++)if(!aug(i,new Set()))return null;const M=Array(n);own.forEach((i,j)=>M[i]=j);return M}
 const M=match();if(!M)return {status:"NO_MATCHING",ct};const inv=Array(n);M.forEach((j,i)=>inv[j]=i);
 const base=rows.map((a,i)=>a.get(M[i])[0]),origin=base.reduce((s,x)=>s^x,0n);
 const adj=rows.map((a,i)=>[...a.keys()].map(j=>inv[j]).filter(v=>v!==i)),paths=adj.map((a,i)=>{const par=Array(n).fill(-1),Q=[i];par[i]=i;for(const u of Q)for(const v of adj[u]){ct.reach++;if(par[v]<0){par[v]=u;Q.push(v)}}return par});
 const keep=(i,j)=>i===j||(paths[i][j]>=0&&paths[j][i]>=0);
 const S=adj.map((a,i)=>a.filter(j=>keep(i,j)));
 function path(a,b){const p=[b];while(p.at(-1)!==a){ct.path++;let u=paths[a][p.at(-1)];if(u<0)throw Error("path");p.push(u)}return p.reverse()}
 const root=Array.from({length:n},(_,i)=>paths[i].findIndex((p,j)=>p>=0&&paths[j][i]>=0));
 const w=(i,j)=>rows[i].get(M[j])[0]^base[i],P=root.map((r,i)=>path(r,i));
 const pot=P.map(p=>p.slice(1).reduce((z,v,i)=>z^w(p[i],v),0n));
 const upper=basis();let allowed=0;
 for(let i=0;i<n;i++){for(const j of [i,...S[i]]){allowed++;const A=rows[i].get(M[j]);for(const x of A){ct.label++;upper.ins(x^A[0])}if(i!==j)upper.ins(pot[i]^w(i,j)^pot[j])}}
 const cycles=new Map();function add(C){if(C.length<2)return;const min=Math.min(...C),k=C.indexOf(min),p=C.slice(k).concat(C.slice(0,k)),key=p.join(",");if(!cycles.has(key))cycles.set(key,p)}
 function split(walk){const stack=[],where=new Map();for(const v of walk){ct.cycle++;if(where.has(v)){const k=where.get(v);add(stack.slice(k));while(stack.length>k+1)where.delete(stack.pop())}else{where.set(v,stack.length);stack.push(v)}}if(stack.length!==1)throw Error("closed walk")}
 for(let i=0;i<n;i++){let r=root[i];split(P[i].concat(path(i,r).slice(1)));for(const j of S[i]){split(P[i].concat([j],path(j,r).slice(1)));if(S[j].includes(i))add([i,j]);}}
 // Exact set if explicit cardinality equals 2^rank; otherwise keep a singleton.
 function local(i,j){const A=rows[i].get(M[j]),a=A[0],B=basis(A.map(x=>x^a)),ok=BigInt(A.length)===(1n<<BigInt(B.b.size));return {i,j,a,A,vec:ok?B.vec():[],affine:ok}}
 function orient(C,flip){return C.map((i,k)=>local(i,flip?C[(k+1)%C.length]:i))}
 function aggregate(L){return {a:L.reduce((z,e)=>z^e.a,0n),B:basis(L.flatMap(e=>e.vec)),L}}
 const baseBlocks=Array.from({length:n},(_,i)=>{const z=aggregate(orient([i],false));return {C:[i],z,alt:null,delta:0n}});
 const lower=basis(baseBlocks.flatMap(b=>b.z.B.vec()));
 let eligible=[];
 for(const C of cycles.values()){const z=aggregate(orient(C,false)),alt=aggregate(orient(C,true));const delta=z.a^alt.a;if(z.B.vec().every(x=>alt.B.red(x)[0]===0n)){eligible.push({C,z,alt,delta})}}
 // Exact integer Laplacian diffusion on the supported undirected graph, used only for ordering.
 const U=S.map((a,i)=>[...new Set([...a,...S.map((b,j)=>b.includes(i)?j:-1).filter(j=>j>=0)])]);let score=Array.from({length:n},(_,i)=>BigInt(2*i-n+1)),D=Math.max(1,...U.map(a=>a.length));
 if(mode==="spectral"||mode==="hybrid")for(let t=0;t<8;t++)score=score.map((x,i)=>{let y=BigInt(2*D-U[i].length)*x;for(const j of U[i]){ct.spectral++;y+=score[j]}return y});
 const spread=C=>C.reduce((s,i)=>s+(score[i]<0n?-score[i]:score[i]),0n);
 if(mode==="spectral")eligible.sort((a,b)=>spread(a.C)<spread(b.C)?-1:spread(a.C)>spread(b.C)?1:a.C.length-b.C.length);
 else if(mode==="hybrid")eligible.sort((a,b)=>a.C.length-b.C.length|| (spread(a.C)<spread(b.C)?-1:spread(a.C)>spread(b.C)?1:0));
 const used=new Set(),selected=[];
 if(mode!=="base")for(const c of eligible){ct.cycle++;if(c.C.some(i=>used.has(i))||lower.red(c.delta)[0]===0n)continue;lower.ins(c.delta);c.C.forEach(i=>used.add(i));selected.push(c)}
 const blocks=baseBlocks.filter(b=>!used.has(b.C[0])).concat(selected),G=basis(),generators=[];
 for(let b=0;b<blocks.length;b++){const z=blocks[b];for(const v of [...z.z.B.vec(),...(z.alt?[z.delta]:[])]){const tag=1n<<BigInt(generators.length);generators.push({b,v});G.ins(v,tag)}}
 if(G.b.size!==lower.b.size||G.vec().some(v=>upper.red(v)[0]))throw Error("lower/upper");
 const [rest,tag]=G.red(target^origin);const [outside]=upper.red(target^origin);
 let status=outside?"NO_AFFINE":rest?"UNKNOWN":"YES",witness=null;
 if(status==="YES"){
   const want=blocks.map(()=>0n);generators.forEach(({b,v},k)=>{if(tag&(1n<<BigInt(k)))want[b]^=v});
   witness=[];
   for(let k=0;k<blocks.length;k++){
    const b=blocks[k];let L=b.z.L,goal=want[k];if(b.z.B.red(goal)[0]){if(!b.alt)throw Error("unlift");L=b.alt.L;goal^=b.delta}
    const T=basis(),vars=[];for(let j=0;j<L.length;j++)for(const v of L[j].vec){T.ins(v,1n<<BigInt(vars.length));vars.push([j,v])}
    const [e,t]=T.red(goal);if(e)throw Error("local lift");const lab=L.map(e=>e.a);vars.forEach(([j,v],i)=>{if(t&(1n<<BigInt(i)))lab[j]^=v});
    L.forEach(({i,j,A},k)=>{ct.check++;if(!A.includes(lab[k]))throw Error("label lift");witness.push({i,j:M[j],v:hex(lab[k])})});
   }
   if(new Set(witness.map(x=>x.i)).size!==n||new Set(witness.map(x=>x.j)).size!==n||witness.reduce((z,e)=>z^val(e.v),0n)!==target)throw Error("bad lift");
   witness.sort((a,b)=>a.i-b.i);
 }
 return {status,exact:G.b.size===upper.b.size,upperRank:upper.b.size,lowerRank:G.b.size,allowed,cycleCandidates:cycles.size,eligible:eligible.length,selected:selected.map(z=>z.C),base:M,origin:hex(origin),upper:upper.vec().map(hex),lower:G.vec().map(hex),witness,ct};
}
function independent(F,R,forceAll=true){
 const n=F.rows.length,ct={force:0,arcs:0,xors:0,checks:0},v=x=>BigInt("0x"+x);
 const row=F.rows.map(r=>[...new Set(r.map(e=>e.j))]);
 function match(fi=-1,fj=-1){ct.force++;const a=Array(n).fill(-1);if(fi>=0)a[fj]=fi;function dfs(i,S){for(const j of row[i]){ct.arcs++;if(j===fj||S.has(j))continue;S.add(j);if(a[j]<0||dfs(a[j],S)){a[j]=i;return true}}return false}for(let i=0;i<n;i++)if(i!==fi&&!dfs(i,new Set()))return false;return true}
 if(!match()){if(R.status!=="NO_MATCHING")throw Error("missing match NO");return ct}
 if(R.status==="NO_MATCHING")throw Error("false match NO");
 const M=R.base,inv=Array(n);M.forEach((j,i)=>{if(!row[i].includes(j)||inv[j]!==undefined)throw Error("base");inv[j]=i});
 const A=F.rows.map((r,i)=>r.find(e=>e.j===M[i]).v).map(v);if(A.reduce((z,x)=>z^x,0n)!==v(R.origin))throw Error("origin");
 const b=new Map();function add(x){while(x){let k=x.toString(2).length-1;if(!b.has(k)){b.set(k,x);return}x^=b.get(k);ct.xors++}}function reduce(x){while(x){let k=x.toString(2).length-1;if(!b.has(k))break;x^=b.get(k);ct.xors++}return x}
 // Independently force each possible edge; use an undirected spanning forest of the allowed contracted multigraph.
 const par=Array.from({length:n},(_,i)=>i),find=i=>{while(par[i]!==i)i=par[i];return i},forest=Array.from({length:n},()=>[]),other=[];
 let allowed=0;
 for(let i=0;i<n;i++)for(const j of row[i])if(match(i,j)){
  allowed++;const L=F.rows[i].filter(e=>e.j===j).map(e=>v(e.v));for(const x of L)add(x^L[0]);const h=inv[j],w=L[0]^A[i];if(i===h)continue;
  const a=find(i),z=find(h);if(a!==z){par[a]=z;forest[i].push([h,w]);forest[h].push([i,w])}else other.push([i,h,w]);
 }
 for(const [a,z,w] of other){const seen=new Set([a]),Q=[[a,0n]];let found=false;for(const [i,t] of Q){if(i===z){add(w^t);found=true;break}for(const [j,y] of forest[i]){ct.checks++;if(!seen.has(j)){seen.add(j);Q.push([j,t^y])}}}if(!found)throw Error("forest")}
 if(allowed!==R.allowed||b.size!==R.upperRank||R.upper.some(x=>reduce(v(x))))throw Error("independent upper mismatch");
 if(R.status==="NO_AFFINE"&&!reduce(v(F.target)^v(R.origin)))throw Error("false affine NO");
 if(R.witness){let sum=0n;if(new Set(R.witness.map(e=>e.i)).size!==n||new Set(R.witness.map(e=>e.j)).size!==n)throw Error("witness collision");for(const e of R.witness){ct.checks++;if(!F.rows[e.i].some(a=>a.j===e.j&&v(a.v)===v(e.v)))throw Error("bad witness");sum^=v(e.v)}if(sum!==v(F.target))throw Error("target")}
 return ct;
}
function experiment(family,sha){
 const enc=x=>JSON.stringify(x)+"\n",mode=["base","lex","spectral","hybrid"],tests=[],summary={graphs:0,feasible:0,affine:0,exact:0,oracleWords:0,fail:0};
 function enumerate(F){let S=new Set(),n=F.rows.length;function go(i,U,x){if(i===n){S.add(x.toString(16));summary.oracleWords++;return}for(const e of F.rows[i])if(!U.has(e.j)){U.add(e.j);go(i+1,U,x^BigInt("0x"+e.v));U.delete(e.j)}}go(0,new Set(),0n);return S}
 function verifySmall(F,R,S){if(!S.size){if(R.status!=="NO_MATCHING")throw Error("empty");return}if(R.status==="NO_MATCHING")throw Error("false empty");const vals=[...S].map(x=>BigInt("0x"+x)),a=vals[0],rank=new Map();for(let x of vals){x^=a;while(x){let k=x.toString(2).length-1;if(!rank.has(k)){rank.set(k,x);break}x^=rank.get(k)}}if(rank.size!==R.upperRank)throw Error("hull oracle");if(R.exact&&BigInt(S.size)!==(1n<<BigInt(rank.size)))throw Error("false saturation");if(R.status==="YES"&&!S.has(F.target)||R.status==="NO_AFFINE"&&S.has(F.target))throw Error("false decision");if(R.exact&&R.status==="UNKNOWN")throw Error("exact unknown")}
 function dense(n,target,kind){let rows=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>({j,v:(kind==="nonaffine"?(i===0?j:0):((i===0&&j===1)?1:((i===2&&j===3)?2:0))).toString(16)})));return {format:"MATCH-SYNDROME-v1",dimension:3,rows,target:target.toString(16)}}
 for(let mask=0;mask<512;mask++){let rows=Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>({j,v:((i*7+j*3+i*j)%8).toString(16)})).filter(e=>mask&(1<<(3*i+e.j))));const F={format:"MATCH-SYNDROME-v1",dimension:3,rows,target:(mask%8).toString(16)};const S=enumerate(F),R=engine(F,"hybrid");independent(F,R);verifySmall(F,R,S);summary.graphs++;if(S.size){summary.feasible++;summary.affine+=Number(BigInt(S.size)===(1n<<BigInt(R.upperRank)));summary.exact+=Number(R.exact)}}
 function record(name,F,origin,oracle=false){const S=oracle?enumerate(F):null,arms=mode.map(m=>{const R=engine(F,m),check=independent(F,R);if(S)verifySmall(F,R,S);return {mode:m,...R,independent:check}});const bytes=enc(F),digest=sha(bytes);let result={name,problem_id:"MATCH-SYNDROME-v1",instance_id:"MATCH-SYNDROME-v1:sha256:"+digest,short_id:name+"@"+digest.slice(0,12),N_bits:bytes.length*8,source:F,source_origin:origin,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{rows:[0,F.rows.length-1],resources:[0,F.rows.length-1],records:"row-local zero based"},parents:[],oracle:S?[...S]:null,arms};tests.push({certificate_id:"CERT-v1:sha256:"+sha(enc(result)),result})}
 for(let n of [2,4,8,16])for(let t of [0,3,4])record("DENSE-CYCLE-"+n+"-TARGET-"+t,dense(n,t,"normal"),"new generator",n<=4);
 for(let t of [1,3,4])record("NONAFFINE-3-TARGET-"+t,dense(3,t,"nonaffine"),"new generator",true);
 for(let q of [2,4,8,16,32,64])for(const yes of [true,false])record("MATCH-PERIOD-"+q+"-"+(yes?"YES":"NO"),family(q,yes),"peer pinned generator; no answer or order injected",q===2);
 return {summary,tests};
}
const fs=require('node:fs'),crypto=require('node:crypto');const p=fs.readFileSync(process.argv[2],'utf8');const family=new Function(p.slice(0,p.indexOf('function solve'))+';return family')();const sha=s=>crypto.createHash('sha256').update(s).digest('hex');console.log(JSON.stringify(experiment(family,sha))); 
