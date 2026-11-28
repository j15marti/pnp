// Node: node rank-tree.js compile.js benchmarks.json instance-registry-v1.json
// V8 isolate: call run(compile, corpus, registry). No external dependencies.
// Pure SHA256 for ASCII source; standard vectors checked before authentication.
function sha(s){
 const K=Array.from({length:64},(_,i)=>{let p=2,n=-1;for(;;p++){let prime=true;for(let j=2;j*j<=p;j++)if(p%j===0){prime=false;break}if(prime&&++n===i)return Math.floor((Math.cbrt(p)%1)*2**32)>>>0}});
 let H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],l=s.length;
 const len=Math.ceil((l+9)/64)*64;const a=new Uint8Array(len);for(let i=0;i<l;i++){let c=s.charCodeAt(i);if(c>127)throw Error("nonascii");a[i]=c}a[l]=128;const dv=new DataView(a.buffer);dv.setUint32(len-8,Math.floor(l*8/2**32));dv.setUint32(len-4,l*8>>>0);
 const R=(x,n)=>(x>>>n)|(x<<(32-n));const W=new Uint32Array(64);
 for(let off=0;off<len;off+=64){for(let i=0;i<16;i++)W[i]=dv.getUint32(off+4*i);for(let i=16;i<64;i++){let x=W[i-15],y=W[i-2];W[i]=(W[i-16]+(R(x,7)^R(x,18)^(x>>>3))+W[i-7]+(R(y,17)^R(y,19)^(y>>>10)))>>>0}
 let [a,b,c,d,e,f,g,h]=H;for(let i=0;i<64;i++){let t=(h+(R(e,6)^R(e,11)^R(e,25))+((e&f)^(~e&g))+K[i]+W[i])>>>0,u=((R(a,2)^R(a,13)^R(a,22))+((a&b)^(a&c)^(b&c)))>>>0;[a,b,c,d,e,f,g,h]=[(t+u)>>>0,a,b,c,(d+t)>>>0,e,f,g]}H=H.map((x,i)=>(x+[a,b,c,d,e,f,g,h][i])>>>0)}
 return H.map(x=>x.toString(16).padStart(8,"0")).join("")
}
function nativeChart(net){
 const n=4*net.types.length,p=Int32Array.from({length:n},(_,i)=>i),q=new Uint8Array(n),sz=new Int32Array(n).fill(1);
 let merges=0,finds=0;
 function find(x){finds++;let b=0;while(p[x]!==x){b^=q[x];x=p[x];finds++}return [x,b]}
 function union(a,b,s){let [r,x]=find(a),[t,y]=find(b);if(r===t){if((x^y)!==s)throw Error("inconsistent signed equality");return}if(sz[r]<sz[t])[r,t]=[t,r];p[t]=r;q[t]=x^y^s;sz[r]+=sz[t];merges++}
 for(const [a,b,s] of net.edges)union(a,b,s);for(let v=0;v<net.types.length;v++)if(net.types[v]==="E")for(let j=1;j<4;j++)union(4*v,4*v+j,0);
 const map=Array.from({length:n},(_,i)=>find(i)),seen=new Set(),F=[];let probes=0;
 for(let v=0;v<net.types.length;v++)if(net.types[v]==="B"){let ps=map.slice(4*v,4*v+4),vs=[...new Set(ps.map(x=>x[0]))].sort((a,b)=>a-b),rows=[];for(let w=0;w<2**vs.length;w++){probes++;if(ps.reduce((a,[r,b])=>a+(((w>>vs.indexOf(r))&1)^b),0)===2)rows.push(w)}let k=JSON.stringify([vs,rows]);if(!seen.has(k)){seen.add(k);F.push({vs,rows,id:v})}}
 return {F,map,merges,finds,probes,check:(a)=>{let bits=map.map(([r,b])=>(a.get(r)??0)^b);let ok=net.edges.every(([p,q,s])=>(bits[p]^bits[q])===s)&&net.types.every((t,v)=>{let x=bits.slice(v*4,v*4+4);return t==="E"?x.every(y=>y===x[0]):x.reduce((a,b)=>a+b,0)===2});return {ok,bits}}}
}
function cnfChart(s){let lines=s.trimEnd().split("\n");let F=lines.slice(1).map((l,i)=>{let lits=l.split(/\s+/).map(Number).slice(0,-1),vs=[...new Set(lits.map(Math.abs))].sort((a,b)=>a-b),rows=[];for(let w=0;w<2**vs.length;w++)if(lits.some(l=>((w>>vs.indexOf(Math.abs(l)))&1)===+(l>0)))rows.push(w);return {vs,rows,id:i+1}});return {F,check:a=>({ok:lines.slice(1).every(l=>l.split(/\s+/).map(Number).slice(0,-1).some(x=>(a.get(Math.abs(x))??0)===+(x>0)))})}}
function early(F){let fixed=new Map(),visits=0,rounds=0,change=true;while(change){change=false;rounds++;for(let f of F){f.rows=f.rows.filter(w=>{visits++;return f.vs.every((v,j)=>!fixed.has(v)||fixed.get(v)===((w>>j)&1))});if(!f.rows.length)return {fixed,visits,rounds,no:true};for(let j=0;j<f.vs.length;j++){let v=f.vs[j],b=(f.rows[0]>>j)&1;if(!fixed.has(v)&&f.rows.every(w=>((w>>j)&1)===b)){fixed.set(v,b);change=true}}}}return {fixed,visits,rounds,no:false}}
function blocks(F){let occ=new Map();F.forEach((f,i)=>f.vs.forEach((v,j)=>{if(!occ.has(v))occ.set(v,[]);occ.get(v).push([i,j])}));let masks=F.map(f=>f.vs.map(()=>0n)),adj=F.map(()=>new Map()),d=0;for(let O of occ.values())for(let j=1;j<O.length;j++){let [a,x]=O[j-1],[b,y]=O[j],bit=1n<<BigInt(d++);masks[a][x]^=bit;masks[b][y]^=bit;adj[a].set(b,(adj[a].get(b)||0)+1);adj[b].set(a,(adj[b].get(a)||0)+1)}
 let target=0n;let B=F.map((f,i)=>{let M=new Map();for(let w of f.rows){let v=0n;for(let j=0;j<f.vs.length;j++)if((w>>j)&1)v^=masks[i][j];if(!M.has(v))M.set(v,w)}let a=M.keys().next().value;target^=a;return [...M].map(([v,w])=>[v^a,w])});return {B,adj,d,target}}
function trial(F,Z,mode,check){
 let {B,adj,d,target}=Z,n=B.length;let cnt={xor:0,rankTests:0,candidates:0,transition:0,peak:0,diffusionEdges:0,treeWidth:0,completedNodes:0},CAP=8000000;
 function tick(){if(++cnt.xor>CAP)throw Error("rank-work-cap")}
 function insert(M,v){while(v){let k=v.toString(2).length-1;if(!M.has(k)){M.set(k,v);return}tick();v^=M.get(k)}}
 function contains(M,v){cnt.rankTests++;while(v){let k=v.toString(2).length-1;if(!M.has(k))return false;tick();v^=M.get(k)}return true}
 function span(ids){let m=new Map();for(let i of ids)for(let [v] of B[i])insert(m,v);return m}
 const all=Array.from({length:n},(_,i)=>i);let global=span(all),r=global.size;if(!contains(global,target))return {status:"NO-affine",cnt};
 // Fixed-point diffusion is a deterministic spectral proposal, not an eigenvector certificate.
 let v=all.map(i=>Math.trunc(1e6*(2*i-Math.max(1,n-1))/Math.max(1,n-1)));for(let k=0;k<24;k++){v=v.map((x,i)=>{let sum=x,deg=1;for(let [j,w] of adj[i]){sum+=w*v[j];deg+=w;cnt.diffusionEdges++}return Math.trunc(sum/deg)})}
 const spec=[...all].sort((a,b)=>v[a]-v[b]||a-b),pos=new Map(spec.map((x,i)=>[x,i]));
 const cache=new Map();
 function cut(ids){let key=[...ids].sort((a,b)=>a-b).join(",");if(cache.has(key))return cache.get(key);let set=new Set(ids),P=span(ids),Q=span(all.filter(i=>!set.has(i))),z={width:P.size+Q.size-r,Q};cache.set(key,z);return z}
 function tree(ids){let cur=cut(ids);cnt.treeWidth=Math.max(cnt.treeWidth,cur.width);if(ids.length===1)return {ids,cur};let options=[...new Set([mode==="spectral"?"spectral":"source",...(mode==="hybrid"?["spectral"]:[])])];let best=null;for(let order of options){let z=[...ids].sort(order==="source"?(a,b)=>a-b:(a,b)=>pos.get(a)-pos.get(b)),h=z.length>>1,L=z.slice(0,h),R=z.slice(h),score=Math.max(cut(L).width,cut(R).width);cnt.candidates++;if(!best||score<best.score)best={L,R,score}}return {ids,cur,left:tree(best.L),right:tree(best.R)}}
 function solve(T){let states=new Map();function put(s,ptr){if(!contains(T.cur.Q,target^s))return;if(!states.has(s)){states.set(s,ptr);cnt.peak=Math.max(cnt.peak,states.size);if(states.size>4096)throw Error("state-cap")}}
 if(!T.left){let i=T.ids[0];for(let [s,w] of B[i])put(s,{i,w})}else{let a=solve(T.left),b=solve(T.right);for(let [s,x] of a)for(let [t,y] of b){if(++cnt.transition>250000)throw Error("transition-cap");put(s^t,{x,y})}}cnt.completedNodes++;return states}
 let start=Date.now();try{if(!n)return {status:"YES",cnt,ms:0};let T=tree(all),S=solve(T);if(!S.has(target))return {status:"NO-tree",cnt,ms:Date.now()-start};let a=new Map();function lift(p){if(p.x){lift(p.x);lift(p.y)}else{let f=F[p.i];f.vs.forEach((v,j)=>{let b=(p.w>>j)&1;if(a.has(v)&&a.get(v)!==b)throw Error("inconsistent-lift");a.set(v,b)})}}lift(S.get(target));let witness=check(a);if(!witness.ok)throw Error("bad-lift");return {status:"YES",cnt,ms:Date.now()-start,witness:witness.bits??[...a]}}catch(e){return {status:"UNKNOWN",reason:String(e),cnt,ms:Date.now()-start}}
}
function run(compile,corpus,registry){
 if(sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("SHA controls");
 let out=[];let cases=["JOINT-24","RANDOM-3CNF-40"].map(id=>corpus.instances.find(x=>x.id===id));cases.push({id:"SAT-RANK-TREE-CONTROL",nvars:4,dimacs:"p cnf 4 3\n1 -2 3 0\n-1 2 4 0\n-3 -4 2 0\n"});cases.push({id:"NO-RANK-TREE-CONTROL",nvars:1,dimacs:"p cnf 1 2\n1 0\n-1 0\n"});
 for(let I of cases){let G=compile(I),s=JSON.stringify(G.network)+"\n",m=JSON.stringify(G.source_map)+"\n",hash=sha(s),mapHash=sha(m),cnfHash=sha(I.dimacs),reg=registry.instances.find(x=>x.alias==="EB-"+I.id);if(reg&&(reg.sha256!==hash||reg.N_bits!==s.length*8||reg.source_map_sha256!==mapHash||reg.source_cnf.sha256!==cnfHash||reg.source_cnf.N_bits!==I.dimacs.length*8))throw Error("authentication failed "+I.id);
 let result={id:I.id,hash,mapHash,cnfHash,N:s.length*8,cnfN:I.dimacs.length*8,vertices:G.network.types.length,edges:G.network.edges.length,controlDIMACS:reg?undefined:I.dimacs,charts:[]};
 for(let kind of ["native","cnf"]){let C=kind==="native"?nativeChart(G.network):cnfChart(I.dimacs),E=early(C.F),row={kind,factors:C.F.length,forced:E.fixed.size,visits:E.visits,rounds:E.rounds,merges:C.merges,finds:C.finds,probes:C.probes,arms:[]};if(E.no){row.status="NO-early";result.charts.push(row);continue}let Z=blocks(C.F);row.d=Z.d;for(let mode of ["source","spectral","hybrid"]){let a=trial(C.F,Z,mode,C.check);row.arms.push({mode,...a})}result.charts.push(row)}out.push(result)}return out
}
if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module){const fs=require("fs"),src=fs.readFileSync(process.argv[2],"utf8"),compile=new Function(src.slice(src.indexOf("function compile("),src.indexOf("function auditLocal("))+";return compile")();console.log(JSON.stringify(run(compile,JSON.parse(fs.readFileSync(process.argv[3])),JSON.parse(fs.readFileSync(process.argv[4]))),null,2))}
