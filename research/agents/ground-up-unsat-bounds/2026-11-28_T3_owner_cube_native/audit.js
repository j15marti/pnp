const fs=require('node:fs');
const pins={"runner":["research/agents/ground-up-unsat-bounds/2026-11-28_T3_owner_cube_native/run.js","7fb35af63bcc0f88a5045a073ff7d06cfd5b19a5"],"results":["research/agents/ground-up-unsat-bounds/2026-11-28_T3_owner_cube_native/results.json","d9beb1519cd8f6b924da0af0fa4171e890243788"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"peer":["research/proof-spine-2026-11-26/closure-exceptional-syndrome/2026-11-28_0452_T3_seed_rank_replay/joint-rank-certificate.json","97297a0e530965297aaae1b6f7197887448a5939"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const audit=function audit(data,pins){
 const expr=data.runner.slice(data.runner.indexOf("const run=")+10,data.runner.lastIndexOf(";\nconsole.log(")).replace("let roots=[];","return {makeNative,chart,evaluate};let roots=[];");
 const {makeNative,chart,evaluate}=new Function("return ("+expr+")")()(data,pins);
 const {sha,norm,replay,up,solve,check}=new Function(data.native+";return {sha,norm,replay,up,solve,check};")();
 const compile=new Function(data.compiler.slice(data.compiler.indexOf("function compile("),data.compiler.indexOf("function auditLocal"))+";return compile;")();
 const enc=x=>JSON.stringify(x)+"\n",A=(b,s)=>{if(!b)throw Error(s)},meter=()=>({scans:0,lits:0,nodes:0,cap:10000000});
 const prior=JSON.parse(data.results);
 function highAdd(B,x,m){while(x){m.rank++;let p=x.toString(2).length-1;if(!B.has(p)){B.set(p,x);return}x^=B.get(p);m.xor++}}
 function rem(B,x,m){while(x){m.rank++;let p=x.toString(2).length-1;if(!B.has(p))return x;x^=B.get(p);m.xor++}return 0n}
 // Target-conditioned prefix DP; exact state bound is cut rank, not total ambient rank.
 function trellis(T,order,cap=512){let M={rank:0,xor:0,trans:0},suffix=Array(order.length+1),B=new Map();suffix[order.length]=B;
 for(let j=order.length-1;j>=0;j--){B=new Map(B);for(let s of T.blocks[order[j]].S)highAdd(B,s^T.blocks[order[j]].S[0],M);suffix[j]=B}
 let anchor=T.blocks.reduce((a,o)=>a^o.S[0],0n),total=B.size,prefix=new Map(),widths=[],peak=1,D=new Map([[0n,[]]]),status="UNKNOWN",witness=null;
 // Compute all cut widths independently of early DP abort.
 for(let j=0;j<order.length;j++){let o=T.blocks[order[j]];for(let x of o.S)highAdd(prefix,x^o.S[0],M);widths.push(prefix.size+suffix[j+1].size-total)}
 if(rem(suffix[0],anchor,M)!==0n)return {status:"NO-affine",width:Math.max(0,...widths),peak:0,M};
 for(let j=0;j<order.length;j++){let o=T.blocks[order[j]],R=new Map();for(let [a,w] of D)for(let i=0;i<o.S.length;i++){M.trans++;let x=a^o.S[i]^o.S[0];if(rem(suffix[j+1],anchor^x,M)!==0n)continue;if(!R.has(x))R.set(x,[...w,[o.id,i]]);if(R.size>cap)return {status:"UNKNOWN",width:Math.max(0,...widths),peak:R.size,M}}
 D=R;peak=Math.max(peak,D.size);if(!D.size)return {status:"NO",width:Math.max(0,...widths),peak,M}}
 status=D.has(anchor)?"YES":"NO";witness=D.get(anchor)||null;if(witness)A(witness.reduce((a,[i,j])=>a^T.blocks[i].S[j],0n)===0n,"trellis lift");
 return {status,width:Math.max(0,...widths),peak,M,witness}
 }
 // Independent signed DSU normalization and direct enumeration, not relying on prior local tables.
 function independentNative(g,cert){let n=4*g.types.length,P=Array.from({length:n},(_,i)=>i),S=Array(n).fill(0),sizes=Array(n).fill(1),work=0;
 function find(a){let t=0;while(a!==P[a]){work++;t^=S[a];a=P[a]}return [a,t]}
 function join(a,b,s){let [u,x]=find(a),[v,y]=find(b);if(u===v){A((x^y)===s,"sign");return}if(sizes[u]<sizes[v])[u,v]=[v,u];P[v]=u;S[v]=s^x^y;sizes[u]+=sizes[v]}
 let seen=new Set(),pair=new Set();for(let [a,b,s] of g.edges){let u=a>>2,v=b>>2,k=[Math.min(u,v),Math.max(u,v)].join(",");A(a>=0&&a<n&&b>=0&&b<n&&u!==v&&!seen.has(a)&&!seen.has(b)&&!pair.has(k)&&(s===0||s===1),"strict graph");seen.add(a);seen.add(b);pair.add(k);join(a,b,s)}
 A(seen.size===n,"strict ports");for(let i=0;i<g.types.length;i++)if(g.types[i]==="E")for(let j=1;j<4;j++)join(4*i,4*i+j,0);else{} 
 let [gr,gs]=find(cert.gauge-1);let owners=[];for(let i=0;i<g.types.length;i++)if(g.types[i]==="B")owners.push(i);
 if(cert.status==="YES"){let w=cert.witness;A(w.length===n&&w.every(x=>x===0||x===1),"witness");for(let [a,b,s] of g.edges)A((w[a]^w[b])===s,"w edge");for(let i=0;i<g.types.length;i++){let x=w.slice(4*i,4*i+4);A(g.types[i]==="E"?x.every(y=>y===x[0]):x.reduce((a,b)=>a+b,0)===2,"w owner")}return {status:"YES",work,ports:n,edges:g.edges.length,owners:g.types.length}}
 let q=cert.certificates.at(-1),ids=q.ids.map(i=>owners[i]),rows=ids.map(i=>Array.from({length:4},(_,j)=>find(4*i+j))),vs=[...new Set(rows.flat().map(x=>x[0]).filter(v=>v!==gr))];A(vs.length<=16,"audit cap");let tests=0,models=0;
 for(let w=0;w<2**vs.length;w++){let ok=true;for(let row of rows){tests++;let sum=row.reduce((a,[v,s])=>a+((v===gr?gs:(w>>vs.indexOf(v)&1))^s),0);if(sum!==2){ok=false;break}}if(ok)models++}
 A(models===0,"false NO");return {status:"NO",work,vars:vs.length,tests,models,originalOwners:ids}
 }
 let controls=[];
 for(let r of prior.controls){let g=makeNative(r.k,r.no);A(sha(enc(g))===r.entry.sha256&&enc(g).length*8===r.entry.N_bits&&sha(enc(r.cert))===r.certHash,"auth");let b=norm(g),T=chart(g,b),orig=T.blocks.map(o=>o.id),a=evaluate(g,b,T);
 let x=trellis(T,orig),y=trellis(T,a.spectralOrder),z=trellis(T,a.certificates.flatMap(q=>q.ids)); // group concatenation from checked structural decomposition
 A(z.status===r.cert.status,"group order");let ind=independentNative(g,r.cert);controls.push({entry:r.entry,k:r.k,no:r.no,source:x,spectral:y,decomposed:z,independent:ind,certHash:r.certHash});
 }
 // Partner proposal is not trusted. Independently derive the relative parity equations on the full projected source formula.
 let raw=data.peer,Apeer=JSON.parse(raw);A(sha(raw)==="25ec26fee03f7e0a2fd13941c3de15eb7c1adc4e184625d57b38e500130dcaea","peer hash");
 let r=prior.roots[0],s=JSON.parse(data.corpus).instances.find(x=>x.id==="JOINT-24"),g0=compile(s),g=g0.network;A(sha(enc(g))===r.entry.sha256&&enc(g).length*8===r.entry.N_bits&&sha(enc(g0.source_map))===r.entry.source_map_sha256,"peer source auth");
 let b=norm(g),p=replay(b.C,r.projection.trace),C=p.C;A(sha(enc(C))===r.residualSha,"residual");
 let vs=new Set(C.flat().map(Math.abs)), proposals=[[0,433,0],[0,561,0],[0,960,1],[0,969,0]],accepted=[],failed=[];
 function reverseUP(D,pins){let a=new Map(pins),m={scans:0,lits:0};if(a.size!==pins.length&&pins.some(([v,x])=>a.get(v)!==x))return {...m,conflict:true};for(;;){let changed=false;for(let i=D.length-1;i>=0;i--){m.scans++;let sat=false,free=[];for(let l of D[i]){m.lits++;let t=a.get(Math.abs(l));if(t===undefined)free.push(l);else if(t===+(l>0))sat=true}if(sat)continue;if(!free.length)return {...m,conflict:true};if(free.length===1){let l=free[0];a.set(Math.abs(l),+(l>0));changed=true}}if(!changed)return {...m,conflict:false}}}
 for(let [a0,z0,s0] of proposals){let a=b.root[a0],z=b.root[z0],s1=s0^b.sign[a0]^b.sign[z0];if(!vs.has(a)||!vs.has(z)||a===z){failed.push({original:[a0,z0,s0],mapped:[a,z,s1],reason:"not admitted on projected chart"});continue}
 let pins0=[[a,0],[z,1^s1]],pins1=[[a,1],[z,s1]],c0=reverseUP(C,pins0),c1=reverseUP(C,pins1);let ok=c0.conflict&&c1.conflict;
 let clauses=s1?[[a,z],[-a,-z]]:[[a,-z],[-a,z]];
 (ok?accepted:failed).push({original:[a0,z0,s0],mapped:[a,z,s1],c0,c1,clauses});
 }
 let arms=[];for(let subset of [[],accepted,...accepted.map((_,i)=>accepted.filter((_,j)=>i!==j))]){let D=[...C,...subset.flatMap(x=>x.clauses)],u=up(D,[],meter()),v=solve(D,500000),w=v.status==="UNSAT"?check(D,v.tree):null;arms.push({parents:subset.map(x=>x.original),status:v.status,discovery:{nodes:v.nodes,scans:v.scans,lits:v.lits},tree:v.tree,check:w,forced:u.conflict?null:[...u.A]})}
 return {controls,peer:{parentSha:sha(raw),entry:r.entry,projectedSha:r.residualSha,accepted,failed,arms}};
};
console.log(JSON.stringify(audit(data,pins),null,2));
