/* run with Node: node audit.js compile.js benchmarks.json instance-registry-v1.json > results.json */
const fs=require('fs');const [c,b,r]=process.argv.slice(2);const s=fs.readFileSync(c,'utf8');const compile=new Function(s.slice(s.indexOf('function compile'),s.indexOf('function auditLocal'))+';return compile')();
const run=function run(compile,corpus,registry){
function sha(s){const K=[],H=[];for(let n=2;K.length<64;n++){let prime=true;for(let j=2;j*j<=n;j++)if(n%j===0){prime=false;break}if(prime){if(H.length<8)H.push((Math.sqrt(n)%1*4294967296)|0);K.push((Math.cbrt(n)%1*4294967296)|0)}}const rot=(x,n)=>(x>>>n)|(x<<(32-n));const len=s.length, bytes=new Uint8Array(Math.ceil((len+9)/64)*64);for(let i=0;i<len;i++){if(s.charCodeAt(i)>127)throw Error("nonascii");bytes[i]=s.charCodeAt(i)}bytes[len]=128;let l=len*8;for(let i=0;i<8;i++){bytes[bytes.length-1-i]=l%256;l=Math.floor(l/256)}const w=new Int32Array(64);for(let o=0;o<bytes.length;o+=64){for(let i=0;i<16;i++)w[i]=(bytes[o+4*i]<<24)|(bytes[o+4*i+1]<<16)|(bytes[o+4*i+2]<<8)|bytes[o+4*i+3];for(let i=16;i<64;i++){let a=w[i-15],b=w[i-2];w[i]=(w[i-16]+(rot(a,7)^rot(a,18)^(a>>>3))+w[i-7]+(rot(b,17)^rot(b,19)^(b>>>10)))|0}let[a,b,c,d,e,f,g,h]=H;for(let i=0;i<64;i++){let t=(h+(rot(e,6)^rot(e,11)^rot(e,25))+((e&f)^(~e&g))+K[i]+w[i])|0,u=((rot(a,2)^rot(a,13)^rot(a,22))+((a&b)^(a&c)^(b&c)))|0;h=g;g=f;f=e;e=(d+t)|0;d=c;c=b;b=a;a=(t+u)|0}for(let i=0;i<8;i++)H[i]=(H[i]+[a,b,c,d,e,f,g,h][i])|0}return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}
if(sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha tests");
const json=x=>JSON.stringify(x)+"\n", abs=Math.abs, uniq=x=>[...new Set(x)], order=(a,b)=>abs(a)-abs(b)||a-b;
function native(G){
 const {types,edges}=G;let p=Array.from({length:4*types.length},(_,i)=>i),d=new Uint8Array(p.length);
 function find(a){if(p[a]===a)return [a,0];let [r,t]=find(p[a]);d[a]^=t;p[a]=r;return [r,d[a]]}
 function join(a,b,s){let [r,t]=find(a),[q,u]=find(b);if(r===q){if((t^u)!==s)throw Error("inconsistent equality")}else if(r<q){p[q]=r;d[q]=t^u^s}else{p[r]=q;d[r]=t^u^s}}
 edges.forEach(([a,b,s])=>join(a,b,s));types.forEach((t,v)=>{if(t==="E")for(let j=1;j<4;j++)join(4*v,4*v+j,0)});
 const dict=new Map();types.forEach((t,v)=>{if(t!=="B")return;let a=Array.from({length:4},(_,j)=>{let[r,s]=find(4*v+j);return (r+1)*(s?-1:1)}).sort(order);let k=a.join(",");if(!dict.has(k))dict.set(k,{a,ids:[]});dict.get(k).ids.push(v)});
 let rows=[...dict.values()],occ=new Map();for(let r of rows)for(let v of uniq(r.a.map(abs)))occ.set(v,(occ.get(v)||0)+1);
 let nae=rows.map(r=>{let sl=r.a.filter(l=>occ.get(abs(l))===1&&r.a.filter(x=>abs(x)===abs(l)).length===1);if(sl.length!==1)throw Error("slack recognition");return {a:r.a.filter(l=>l!==sl[0]),ids:r.ids,sl:sl[0]}});
 let counts=new Map();nae.forEach((r,i)=>{for(let v of uniq(r.a.map(abs))){if(!counts.has(v))counts.set(v,[]);counts.get(v).push(i)}});
 let anchor=[...counts].sort((a,b)=>b[1].length-a[1].length||a[0]-b[0])[0][0],used=new Set(),sew=[];
 for(let i=0;i<nae.length;i++){if(used.has(i)||nae[i].a.some(l=>abs(l)===anchor))continue;let r=nae[i];let options=uniq(r.a.map(abs)).filter(v=>counts.get(v).length===2&&r.a.filter(l=>abs(l)===v).length===1).map(v=>[v,counts.get(v).find(j=>j!==i)]).filter(([v,j])=>!used.has(j)&&nae[j].a.some(l=>abs(l)===anchor)&&nae[j].a.filter(l=>abs(l)===v).length===1);if(options.length!==1)throw Error("ambiguous sew "+options.length);let[v,j]=options[0],s=nae[j],l=r.a.find(l=>abs(l)===v),m=s.a.find(l=>abs(l)===v);let a=r.a.filter(x=>abs(x)!==v).concat(s.a.filter(x=>abs(x)!==v).map(x=>l===m?-x:x));used.add(i);used.add(j);sew.push({a,ids:r.ids.concat(s.ids),pivot:v,parents:[r,s]})}
 if(used.size!==nae.length)throw Error("not all sewn");
 let factors=[];for(let r of sew){let anchors=r.a.filter(l=>abs(l)===anchor);if(anchors.length!==1)throw Error("anchor");let a=uniq(r.a.filter(l=>abs(l)!==anchor).map(l=>anchors[0]<0?-l:l)).sort(order);if(a.some(l=>a.includes(-l)))continue;factors.push({a,ids:r.ids,pivot:r.pivot,parents:r.parents})}
 let vars=uniq(factors.flatMap(r=>r.a.map(abs))).sort((a,b)=>a-b),index=new Map(vars.map((v,i)=>[v,i+1]));let clauses=factors.map(r=>r.a.map(l=>Math.sign(l)*index.get(abs(l))));
 return {clauses,vars,anchor,factors,rows:rows.length,nae:nae.length,sew:sew.length,portMap:vars.map(v=>v-1),anchorPort:anchor-1};
}
function runLanes(F,n){
 const cap=2000000;let count=Array(n+1).fill(0);F.flat().forEach(l=>count[abs(l)]++);let [a,b,c]=Array.from({length:n},(_,i)=>i+1).sort((i,j)=>count[j]-count[i]||i-j);
 const guards=[[ -a,-b,-c],[-a,-b,c],[-a,b],[a,-b],[a,b]];
 const fresh=()=>({events:0}),tick=(w,k=1)=>{w.events+=k;if(w.events>cap)throw Error("CAP")};
 function restrict(F,g,w){let v=new Map(g.map(l=>[abs(l),l>0]));let R=[];for(let i=0;i<F.length;i++){let cl=F[i];tick(w);if(cl.some(l=>v.has(abs(l))&&v.get(abs(l))===(l>0)))continue;R.push({a:cl.filter(l=>!v.has(abs(l))),id:i})}return R}
 function up(F,g,w){let v=new Map(g.map(l=>[abs(l),l>0])),used=new Set(),change=true;while(change){change=false;for(let i=0;i<F.length;i++){let cl=F[i];tick(w);if(cl.some(l=>v.has(abs(l))&&v.get(abs(l))===(l>0)))continue;let u=cl.filter(l=>!v.has(abs(l)));if(!u.length){used.add(i);return {conflict:true,used:[...used],g:[...v].map(([x,t])=>t?x:-x)}}if(u.length===1){used.add(i);v.set(abs(u[0]),u[0]>0);change=true}}}return {conflict:false,used:[...used],g:[...v].map(([x,t])=>t?x:-x)}}
 // independent local cardinality closure (unit clauses after exact NAE sewing).
 function local(g,w){return up(F,g,w)}
 // affine projection of every residual same-scope table; rank elimination over BigInt.
 function affine(g,w){let R=restrict(F,g,w),M=new Map();for(let {a} of R){let vs=uniq(a.map(abs)).sort((i,j)=>i-j);let k=vs.join(",");if(!M.has(k))M.set(k,{vs,cs:[]});M.get(k).cs.push(a)}
 let basis=new Map();function add(m,r){while(m){let k=m.toString(2).length-1;tick(w);if(!basis.has(k)){basis.set(k,[m,r]);return true}let [x,y]=basis.get(k);m^=x;r^=y}return r===0}
 for(let {vs,cs} of M.values()){if(vs.length>8)continue;let good=[];for(let x=0;x<2**vs.length;x++){tick(w);if(cs.every(cl=>cl.some(l=>Boolean(x&(1<<vs.indexOf(abs(l))))===(l>0))))good.push(x)}if(!good.length)return {conflict:true,rank:basis.size};for(let mask=1;mask<2**vs.length;mask++){const parity=x=>{let z=0;while(x){z^=1;x&=x-1}return z};let r=parity(good[0]&mask);tick(w,good.length);if(good.every(x=>parity(x&mask)===r)){let m=0n;vs.forEach((v,j)=>{if(mask&(1<<j))m|=1n<<BigInt(v-1)});if(!add(m,r))return {conflict:true,rank:basis.size}}}}return {conflict:false,rank:basis.size}}
 // implication graph: exact 2-SAT decision for binary-clause relaxation, distinct from affine.
 function scc(g,w){let R=restrict(F,g,w),A=new Map();const add=(u,v)=>{if(!A.has(u))A.set(u,[]);A.get(u).push(v)};for(let {a} of R){if(!a.length)return {conflict:true};if(a.length===1)add(-a[0],a[0]);if(a.length===2){add(-a[0],a[1]);add(-a[1],a[0])}}
 function reach(x,y){let q=[x],seen=new Set(q);while(q.length){let u=q.pop();tick(w);if(u===y)return true;for(let v of A.get(u)||[])if(!seen.has(v)){seen.add(v);q.push(v)}}return false}
 for(let i=1;i<=n;i++)if(reach(i,-i)&&reach(-i,i))return {conflict:true,pivot:i};return {conflict:false}}
 // bounded separator/bucket projection by resolution, exact when eliminated.
 function bucket(g,w){let R=restrict(F,g,w).map(r=>r.a),elim=[];while(true){if(R.some(a=>!a.length))return {conflict:true,eliminated:elim};let cand=[];for(let i=1;i<=n;i++){let P=R.filter(a=>a.includes(i)),Q=R.filter(a=>a.includes(-i));tick(w,R.length);if(P.length+Q.length===0)continue;let vs=uniq(P.concat(Q).flat().map(abs));if(vs.length<=6&&P.length*Q.length<=48)cand.push([i,P,Q,vs.length])}if(!cand.length)return {conflict:false,eliminated:elim};cand.sort((a,b)=>a[1].length*a[2].length-b[1].length*b[2].length||a[3]-b[3]||a[0]-b[0]);let[i,P,Q]=cand[0];elim.push(i);let out=R.filter(a=>!a.includes(i)&&!a.includes(-i));for(let p of P)for(let q of Q){tick(w);let a=uniq(p.concat(q).filter(l=>abs(l)!==i)).sort(order);if(!a.some(l=>a.includes(-l)))out.push(a)}R=[...new Map(out.map(a=>[a.join(","),a])).values()]}}
 // proof tree with propagation, independent scalar replay below.
 function tree(g,w){let U=up(F,g,w);if(U.conflict)return {leaf:true,used:U.used};let used=new Set(U.g.map(abs));let freq=Array(n+1).fill(0);for(let cl of F){tick(w);if(cl.some(l=>U.g.includes(l)))continue;for(let l of cl)if(!used.has(abs(l)))freq[abs(l)]++}let x=0;for(let i=1;i<=n;i++)if(!used.has(i)&&freq[i]>(freq[x]||0))x=i;if(!x)throw Error("SAT witness or no unresolved clause");return {x,lo:tree(g.concat(-x),w),hi:tree(g.concat(x),w)}}
 function support(t){return t.leaf?t.used:uniq(support(t.lo).concat(support(t.hi)))}
 function nodes(t){return t.leaf?1:1+nodes(t.lo)+nodes(t.hi)}
 // independent checker: use ternary array, scan reverse, verify each leaf from its selected source factors only.
 function verify(t,g,w){if(t.leaf){let A=new Int8Array(n+1);for(let l of g)A[abs(l)]=l>0?1:-1;while(true){let changed=false;for(let k=t.used.length-1;k>=0;k--){tick(w);let cl=F[t.used[k]],sat=false,z=0,last=0;for(let l of cl){let v=A[abs(l)];if(v===Math.sign(l)){sat=true;break}if(!v){z++;last=l}}if(sat)continue;if(z===0)return true;if(z===1){A[abs(last)]=Math.sign(last);changed=true}}if(!changed)return false}}if(!Number.isInteger(t.x)||t.x<1||t.x>n||g.some(l=>abs(l)===t.x))return false;return verify(t.lo,g.concat(-t.x),w)&&verify(t.hi,g.concat(t.x),w)}
 let rows=[],proofs=[];for(let g of guards){let r=[];for(let [name,fn] of [["occupancy",local],["affine",affine],["bijunctive",scc],["separator",bucket],["proofDAG",tree]]){let w=fresh();try{let o=fn(g,w);if(name==="proofDAG"){let v=fresh();if(!verify(o,g,v))throw Error("replay failed");proofs.push(o);r.push({name,conflict:true,events:w.events,check:v.events,nodes:nodes(o),core:support(o).sort((a,b)=>a-b)})}else r.push({name,conflict:o.conflict,events:w.events,detail:o.rank??o.eliminated?.length??null})}catch(e){r.push({name,conflict:false,events:w.events,error:String(e)})}}rows.push(r)}
 // guard coverage by all 31 intersections using exact BigInt cardinalities
 let total=0n,terms=[];for(let mask=1;mask<32;mask++){let m=new Map(),ok=true,k=0;for(let i=0;i<5;i++)if(mask&(1<<i)){k++;for(let l of guards[i]){if(m.has(abs(l))&&m.get(abs(l))!==Math.sign(l))ok=false;m.set(abs(l),Math.sign(l))}}let size=ok?1n<<BigInt(n-m.size):0n;terms.push(size.toString());total+=(k%2?size:-size)}
 // hybrid: import only local occupancy contradictions (independently replayed proof DAG), then check remaining branches by UP and proof tree on augmented formula? 
 // compute reclosure using negation of certified guards, without pretending missing branches solved.
 let learned=guards.filter((g,i)=>rows[i][0].conflict&&rows[i][4].conflict).map(g=>g.map(l=>-l));
 let hw=fresh(),root=up(F.concat(learned),[],hw),after=guards.map(g=>{let w=fresh();return {conflict:up(F.concat(learned),g,w).conflict,events:w.events}});
 return {n,guards,rows,proofs,coverage:{terms,total:total.toString(),carrier:(1n<<BigInt(n)).toString()},learned,hybrid:{rootConflict:root.conflict,rootFixed:root.g.length,rootEvents:hw.events,after},cap};
}
let out=[];
for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){
 let x=corpus.instances.find(i=>i.id===alias),r=registry.instances.find(i=>i.alias==="EB-"+alias),C=compile(x);
 let hashes={native:sha(json(C.network)),cnf:sha(x.dimacs),map:sha(json(C.source_map)),N:json(C.network).length*8,cnfN:x.dimacs.length*8};if(hashes.native!==r.sha256||hashes.cnf!==r.source_cnf.sha256||hashes.map!==r.source_map_sha256||hashes.N!==r.N_bits||hashes.cnfN!==r.source_cnf.N_bits)throw Error("hash mismatch");
 let t=native(C.network),nativeRes=runLanes(t.clauses,t.vars.length);
 const F=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));let cnf=runLanes(F,x.nvars);
 // record exact artifact IDs and native original port relative guard, complete source supporting B nodes
 const nativeChart={schema:"SEWN-CNF-v1",anchorPort:t.anchorPort,vars:t.portMap,clauses:t.clauses,factors:t.factors};
 const guardIDs=nativeRes.guards.map(g=>{let art={schema:"EB-RELATIVE-PORT-PINS-v1",anchor:t.anchorPort,pins:g.map(l=>[t.portMap[abs(l)-1],l>0?1:0]).sort((a,b)=>a[0]-b[0])};let h=sha(json(art));return {artifact:art,sha:h,id:"GUARD-v1:sha256:"+sha(json(["PNP-GUARD-v1",r.instance_id,art.schema,h]))}});
 const nativeCore=nativeRes.rows.map(rr=>{let core=rr[4].core||[];return uniq(core.flatMap(i=>t.factors[i].ids)).sort((a,b)=>a-b)});
 out.push({alias,registry:r,hashes,nativeChart,guardIDs,nativeCore,nativeRes,cnf});
}
return {out,shaSource:sha.toString()};
};
console.log(JSON.stringify(run(compile,JSON.parse(fs.readFileSync(b,'utf8')),JSON.parse(fs.readFileSync(r,'utf8'))).out,null,2));
