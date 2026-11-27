// Reproduce: node sewing.js benchmarks.json compile.js registry.json
const fs=require('node:fs'),crypto=require('node:crypto');
const run=function run(network,dimacs,cap=1000000){
 const {types,edges}=network, P=4*types.length, adj=Array.from({length:P},()=>[]), seen=new Set(),ports=new Set(); 
 function link(a,b,s){adj[a].push([b,s]);adj[b].push([a,s])}
 for(const [a,b,s] of edges){let u=a>>2,v=b>>2,key=[Math.min(u,v),Math.max(u,v)].join(":");if(a<0||b<0||a>=P||b>=P||u===v||seen.has(key)||ports.has(a)||ports.has(b)||s!==0&&s!==1)throw Error("invalid source");seen.add(key);ports.add(a);ports.add(b);link(a,b,s)}if(ports.size!==P)throw Error("degree");
 types.forEach((t,v)=>{if(t==="E"){for(let j=1;j<4;j++)link(4*v,4*v+j,0)}else if(t!=="B")throw Error("type")});
 const root=new Int32Array(P).fill(-1),sign=new Uint8Array(P);let roots=0;
 for(let p=0;p<P;p++)if(root[p]<0){roots++;root[p]=p;let Q=[p];for(let k=0;k<Q.length;k++){let a=Q[k];for(let [b,s] of adj[a]){if(root[b]<0){root[b]=p;sign[b]=sign[a]^s;Q.push(b)}else if(root[b]!==p||sign[b]!== (sign[a]^s))throw Error("signed cycle")}}}
 // Independent transport audit using parity union-find; representative is always minimum.
 let par=Int32Array.from({length:P},(_,i)=>i),off=new Uint8Array(P);
 function find(a){let r=a,t=0;while(par[r]!==r){t^=off[r];r=par[r]}while(par[a]!==a){let b=par[a],s=off[a];par[a]=r;off[a]=t;t^=s;a=b}return r}
 function unite(a,b,s){let u=find(a),v=find(b),z=off[a]^off[b]^s;if(u===v){if(z)throw Error("DSU cycle");return}if(u>v)[u,v]=[v,u];par[v]=u;off[v]=z}
 for(const [a,b,s] of edges)unite(a,b,s);types.forEach((t,v)=>{if(t==="E")for(let j=1;j<4;j++)unite(4*v,4*v+j,0)});
 for(let p=0;p<P;p++)if(find(p)!==root[p]||off[p]!==sign[p])throw Error("normalization disagree");
 const norm=a=>{let s=new Set(a);for(let x of s)if(s.has(-x))return null;return [...s].sort((a,b)=>a-b)},uniq=F=>[...new Map(F.filter(x=>x!==null).map(x=>[x.join(","),x])).values()];
 let F=[],rows=[],freq=new Map(),parity=new Map();
 for(let v=0;v<types.length;v++)if(types[v]==="B"){let a=Array.from({length:4},(_,j)=>(root[4*v+j]+1)*(sign[4*v+j]?-1:1));rows.push(a);for(let x of a)freq.set(Math.abs(x),(freq.get(Math.abs(x))||0)+1);let scope=[...new Set(a.map(Math.abs))].sort((a,b)=>a-b);let good=[];for(let w=0;w<2**scope.length;w++){let sum=a.reduce((s,l)=>s+(((w>>scope.indexOf(Math.abs(l)))&1)^(l<0?1:0)),0);if(sum===2)good.push(w)}
 let clauses=[];for(let w=0;w<3**scope.length;w++){let t=w,C=[];for(let j=0;j<scope.length;j++){let d=t%3;t=Math.floor(t/3);if(d)C.push(d===1?scope[j]:-scope[j])}if(good.every(z=>C.some(l=>((z>>scope.indexOf(Math.abs(l)))&1)===Number(l>0))))clauses.push(norm(C))}
 clauses.sort((a,b)=>a.length-b.length);let min=[];for(let C of clauses)if(!min.some(D=>D.every(l=>C.includes(l))))min.push(C);for(let w=0;w<2**scope.length;w++)if(good.includes(w)!==min.every(C=>C.some(l=>((w>>scope.indexOf(Math.abs(l)))&1)===Number(l>0))))throw Error("prime table audit");F.push(...min) // GF2 parity relaxation
 let z=0n,b=0;for(let l of a){z^=1n<<BigInt(Math.abs(l)-1);b^=Number(l<0)}while(z){let p=z.toString(2).length-1;if(!parity.has(p)){parity.set(p,[z,b]);break}let [zz,bb]=parity.get(p);z^=zz;b^=bb}if(!z&&b)throw Error("affine contradiction found");
 }
 F=uniq(F);const gauge=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0]; // global complement exact
 function restrict(F,v,b){let l=b?v:-v;return F.filter(c=>!c.includes(l)).map(c=>c.filter(x=>x!==-l))}
 function close(F,m){let A=[];while(true){let u=F.find(c=>c.length<=1);m.events+=F.length;if(m.events>cap)throw Error("CAP");if(!u)return {F,A};if(!u.length)return {F,A};A.push(u[0]);F=restrict(F,Math.abs(u[0]),Number(u[0]>0));}}
 function tree(F,m){let cl=close(F,m);F=cl.F;m.nodes++;if(F.some(c=>!c.length))return ["X"];if(!F.length)return ["S"];let counts=new Map();for(let c of F)for(let l of c){let v=Math.abs(l);counts.set(v,(counts.get(v)||0)+(c.length===2?4:1));m.events++}if(m.events>cap)throw Error("CAP");let v=[...counts].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let a=tree(restrict(F,v,0),m);if(a[0]==="S")return a;let b=tree(restrict(F,v,1),m);if(b[0]==="S")return b;return [v,a,b]}
 function replay(F,t,m){let cl=close(F,m);F=cl.F;if(t[0]==="X")return F.some(c=>!c.length);if(!Number.isInteger(t[0])||t.length!==3||!F.some(c=>c.some(l=>Math.abs(l)===t[0])))return false;return replay(restrict(F,t[0],0),t[1],m)&&replay(restrict(F,t[0],1),t[2],m)}
 const initial=restrict(F,gauge,0);let pre=close(initial,{events:0});let G=pre.F, steps=[], meter={events:0,checks:0,retirements:0, maxScope:0};
 // Lane A: bounded signed hub sewing by resolution. All clauses mentioning pivot must be included.
 function sew(G,m){m.rounds=0;while(!G.some(c=>!c.length)){
 let occ=new Map();for(const c of G)for(const l of c){let v=Math.abs(l);if(!occ.has(v))occ.set(v,[[],[]]);occ.get(v)[Number(l<0)].push(c);m.events++}
 if(m.events>cap)throw Error("CAP");let cand=[...occ].filter(([v,[a,b]])=>a.length*b.length<=36).sort((a,b)=>a[1][0].length*a[1][1].length-b[1][0].length*b[1][1].length||a[0]-b[0]);let taken=new Set(),added=[];
 for(const [v,[a,b]] of cand){if([...a,...b].some(c=>taken.has(c)))continue;const scope=[...new Set([...a,...b].flat().map(Math.abs))].filter(x=>x!==v);m.events+=a.length+b.length;if(scope.length>8)continue;
 let R=uniq(a.flatMap(c=>b.map(d=>norm([...c.filter(l=>l!==v),...d.filter(l=>l!==-v)]))));m.events+=a.length*b.length;R.sort((a,b)=>a.length-b.length);let min=[];for(let C of R)if(!min.some(D=>D.every(l=>C.includes(l))))min.push(C);R=min;if(R.length>a.length+b.length||R.some(c=>c.length>5))continue;
 for(let w=0;w<2**scope.length;w++){let evalC=(c,z)=>c.some(l=>((Math.abs(l)===v?z:(w>>scope.indexOf(Math.abs(l)))&1)===Number(l>0)));let exact=[0,1].some(z=>[...a,...b].every(c=>evalC(c,z)));let projected=R.every(c=>evalC(c,0));m.checks++;if(exact!==projected)throw Error("sewing checker");}
 m.maxScope=Math.max(m.maxScope,scope.length);steps.push({v,positive:a,negative:b,resolvents:R});for(let c of [...a,...b])taken.add(c);added.push(...R);m.retirements++}
 if(!taken.size)break;G=uniq([...G.filter(c=>!taken.has(c)),...added]);m.rounds++;
 }return G}
 let localStatus="UNKNOWN",localError=null,hybrid={events:0,nodes:0},t=null,replayMeter={events:0},localReplay=false;
 try{G=sew(G,meter);t=tree(G,hybrid);if(t[0]!=="S"){localReplay=replay(G,t,replayMeter);if(!localReplay)throw Error("tree replay");localStatus="UNSAT"}else localStatus="SAT"}catch(e){localError=String(e)}
 // Lane B: independently derived native balance parity relaxation and direct support-closed DPLL (no sewing).
 let direct={events:0,nodes:0},directStatus="UNKNOWN";directStatus="NOT_RERUN"
 // Provenance-assisted baseline only: original clauses, independently searched, no reference tree.
 let C=dimacs.trimEnd().split("\n").slice(1).map(s=>s.trim().split(/\s+/).map(Number).slice(0,-1)),assisted={events:0,nodes:0},assistedStatus="UNKNOWN";assistedStatus="NOT_RERUN"
 return {metrics:{roots, B:rows.length,nativeClauses:F.length,gauge,initialUnitPins:pre.A.length,parityRank:parity.size,initialClausesAfterGauge:initial.length,remainingClauses:G.length,remainingVariables:new Set(G.flat().map(Math.abs)).size,meter,hybrid,localStatus,localError,localReplay,replayMeter,direct,directStatus,assisted,assistedStatus},proof:{gauge,initialUnits:pre.A,steps,tree:t}};
};
const code=fs.readFileSync(process.argv[3],'utf8');const compile=new Function(code.slice(code.indexOf('function compile'),code.indexOf('function auditLocal'))+';return compile')();
const corpus=JSON.parse(fs.readFileSync(process.argv[2],'utf8')).instances, registry=JSON.parse(fs.readFileSync(process.argv[4],'utf8')).instances;const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
for(const id of ['JOINT-24','RANDOM-3CNF-40']){const x=corpus.find(x=>x.id===id),r=registry.find(r=>r.alias==='EB-'+id);const {network,source_map}=compile(x);const native=JSON.stringify(network)+'\n',map=JSON.stringify(source_map)+'\n';if(sha(native)!==r.sha256||native.length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(map)!==r.source_map_sha256)throw Error('registry mismatch');console.log(JSON.stringify({id,...run(network,x.dimacs)}));}
