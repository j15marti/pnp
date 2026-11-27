function directed(src){
 const H=Function(src.hybrid.split('if(typeof require==="function"')[0]+";return {sha,canon}")(),assert=(b,s)=>{if(!b)throw Error(s)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const cap=1000000, pairCap=1200, rowCap=64, mod=n=>(n%3+3)%3;
 function epoch(P,mode){
 const M={events:0,unit:0,pairs:0,score:0,residue:0,replay:0,search:0,verify:0,other:0},tick=(key,n=1)=>{M[key]+=n;M.events+=n;if(M.events>cap)throw Error("aggregate cap")};
 function evalRow(c,x,which){let k=0,s=0;for(let l of c){tick(which);let z=x.get(Math.abs(l))===+(l>0)?(l>0?1:-1):0;k+=z*z;s+=z}return {k,km:mod(k),sm:mod(s)}}
 function up(F,guard,which="unit"){let p=new Map(guard);for(;;){let change=false;for(let c of F){let a=[],hit=false;for(let l of c){tick(which);if(!p.has(Math.abs(l)))a.push(l);else if(p.get(Math.abs(l))===+(l>0)){hit=true;break}}if(hit)continue;if(!a.length)return {p,conflict:true};if(a.length===1){p.set(Math.abs(a[0]),+(a[0]>0));change=true}}if(!change)return {p,conflict:false}}}
 function restrict(F,p){return F.filter(c=>!c.some(l=>p.get(Math.abs(l))===+(l>0))).map(c=>c.filter(l=>!p.has(Math.abs(l))))}
 function score(F,x,res){let b=0,z=0;for(let c of F){let a=evalRow(c,x,"score");if(res)tick("residue",3);if(!a.k)b++;else if(!a.sm)z++}return [b,z]}
 function flip(F,x,V,res){let init=score(F,x,res),s=init,flips=0,ties=0;for(;;){let best=null,plain=null;for(let v of V){x.set(v,1-x.get(v));let t=score(F,x,res);x.set(v,1-x.get(v));if(t[0]>=s[0])continue;if(!plain||t[0]<plain.t[0])plain={v,t};if(!best||t[0]<best.t[0]||(res&&t[0]===best.t[0]&&t[1]<best.t[1]))best={v,t}}
 if(!best)break;if(best.v!==plain.v)ties++;x.set(best.v,1-x.get(best.v));s=best.t;flips++}assert(flips<=init[0],"strict descent");return {start:init[0],end:s[0],flips,ties}}
 function search(F){let nodes=0;function dfs(p){nodes++;let u=up(F,p,"search");if(u.conflict)return 0;let f=restrict(F,u.p);if(!f.length)throw Error("SAT witness in expected UNSAT control");let a=new Map();for(let c of f)for(let l of c){tick("search");let v=Math.abs(l);a.set(v,(a.get(v)||0)+1)}let v=[...a].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];return [v,dfs([...u.p,[v,0]]),dfs([...u.p,[v,1]])]}let t=dfs([]);return {t,nodes}}
 function check(F,t,g=[]){let u=up(F,g,"verify");if(u.conflict){assert(t===0,"leaf");return}assert(Array.isArray(t)&&t.length===3&&!u.p.has(t[0])&&F.some(c=>c.some(l=>Math.abs(l)===t[0])),"branch");check(F,t[1],[...u.p,[t[0],0]]);check(F,t[2],[...u.p,[t[0],1]])}
 const F=JSON.parse(P.chart).F,results=[],started=Date.now();let peakRows=F.length,peakLits=F.flat().length;
 try{for(let [i,g] of P.guards.entries()){
 let u=up(F,g);if(u.conflict){results.push({i,early:true,nodes:1,trace:[],tree:0});continue}let D=restrict(F,u.p),V=[...new Set(D.flat().map(Math.abs))].sort((a,b)=>a-b),x=new Map(),rng=20261127;
 for(let v of V){rng=(Math.imul(rng,1664525)+1013904223)>>>0;x.set(v,rng>>>31)}
 let zero=new Map(V.map(v=>[v,0])),one=new Map(V.map(v=>[v,1]));let endpoints=D.map(c=>[evalRow(c,zero,"other"),evalRow(c,one,"other")]);let first=null,second=null;
 if(mode!=="fixed")first=flip(D,x,V,mode==="residue");
 let cand=[],seen=new Set(D.map(c=>c.join(","))),count=0;
 outer:for(let v of V){let plus=[],minus=[];for(let [j,c] of D.entries()){tick("other",c.length);if(c.includes(v))plus.push([j,c]);if(c.includes(-v))minus.push([j,c])}for(let [a,c] of plus)for(let [b,d] of minus){if(count>=pairCap)break outer;count++;tick("pairs");let r=H.canon(c.filter(l=>l!==v).concat(d.filter(l=>l!==-v)));tick("pairs",c.length+d.length);if(!r||r.length>4||seen.has(r.join(",")))continue;seen.add(r.join(","));let e=evalRow(r,x,"score");cand.push({a,b,v,r,defect:+(e.k===0),critical:+(e.k===1),serial:cand.length})}}
 // Same acquired candidates. Only the paid current assignment changes priority.
 if(mode!=="fixed")cand.sort((a,b)=>{tick("other");return b.defect-a.defect||b.critical-a.critical||a.serial-b.serial});
 let trace=cand.slice(0,rowCap).map(({a,b,v,r})=>({a,b,v,r})),E=D.slice();for(let z of trace){tick("replay",D[z.a].length+D[z.b].length);assert(D[z.a].includes(z.v)&&D[z.b].includes(-z.v)&&eq(H.canon(D[z.a].filter(l=>l!==z.v).concat(D[z.b].filter(l=>l!==-z.v))),z.r),"replay");E.push(z.r)}
 let post=up(E,[]);if(mode!=="fixed"&&!post.conflict){for(let [v,b] of post.p)x.set(v,b);second=flip(E,x,V.filter(v=>!post.p.has(v)),mode==="residue")}
 let t=search(E);check(E,t.t);peakRows=Math.max(peakRows,E.length);peakLits=Math.max(peakLits,E.flat().length);results.push({i,early:false,initialPins:u.p.size-g.length,postPins:post.p.size,candidates:cand.length,trace,tree:t.t,nodes:t.nodes,first,second,endpointRows:endpoints.length,endpointCollision:endpoints.filter(([a,b])=>a.k!==b.k&&a.km===b.km).length});
 }}catch(e){return {mode,status:"UNKNOWN",reason:String(e),M,ms:Date.now()-started,results,peakRows,peakLits}}
 return {mode,status:"UNSAT",M,ms:Date.now()-started,results,peakRows,peakLits}
 }
 let out=[];for(let key of ["joint","random"]){let P=JSON.parse(src[key]);assert(H.sha(src[key])===(key==="joint"?"166bae74cc88a481475d9865fe7b367d2b28e873f27f02c0747aece028c7c397":"2e11fc3dc7abea2375e367d75714ae8110bee9e3aca71d4101cdd0d7143a3c62"),"parent bytes");let a=["fixed","table","residue"].map(m=>epoch(P,m));out.push({instance:P.instance_id,N:P.original_N_bits,rootCertificate:H.sha(src[key]),chart:P.chart_id,guardInfo:P.guardInfo,arms:a})}return out
}
if(typeof require==='function'){const fs=require('fs');const src=Object.fromEntries(['hybrid','joint','random'].map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(directed(src),null,2));}
