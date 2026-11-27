function pin(F,g){if(!F.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))))throw Error("not complement invariant");return F.map(f=>{let i=f.vs.indexOf(g);if(i<0)return f;return {...f,vs:f.vs.filter(v=>v!==g),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}})}
function projection(F,g,trace=null){
 F=pin(F,g);let seq=F.length,steps=[],tests=0,scans=0;
 for(;;){let m=new Map();for(let f of F)for(let v of f.vs){scans++;if(!m.has(v))m.set(v,[]);m.get(v).push(f)}
 let v;if(trace){if(steps.length===trace.length)break;v=trace[steps.length].v}else{let opts=[...m].filter(([v,B])=>B.length<=2&&new Set(B.flatMap(f=>f.vs)).size<=7).sort((a,b)=>new Set(a[1].flatMap(f=>f.vs)).size-new Set(b[1].flatMap(f=>f.vs)).size||a[1].length-b[1].length||a[0]-b[0]);if(!opts.length)break;v=opts[0][0]}
 let B=m.get(v);if(!B||B.length>2)throw Error("bucket");let U=[...new Set(B.flatMap(f=>f.vs))].sort((a,b)=>a-b),V=U.filter(x=>x!==v);if(U.length>7)throw Error("scope");let ok=[];
 for(let w=0;w<2**V.length;w++){let hit=false;for(let b=0;b<2;b++){let a=new Map(V.map((x,i)=>[x,w>>i&1]));a.set(v,b);if(B.every(f=>{tests++;return f.ok.includes(f.vs.reduce((z,x,i)=>z+(a.get(x)<<i),0))}))hit=true}if(hit)ok.push(w)}
 let t={v,in:B.map(f=>f.id),out:trace?trace[steps.length].out:seq,vs:V,ok};if(trace&&(t.in.join()!==trace[steps.length].in.join()||V.join()!==trace[steps.length].vs.join()||ok.join()!==trace[steps.length].ok.join()||F.some(f=>f.id===t.out)))throw Error("projection mismatch "+steps.length);
 steps.push(t);F=F.filter(f=>!B.includes(f));if(ok.length!==2**V.length)F.push({id:t.out,vs:V,ok});seq++;
 }return{fs:F,trace:steps,tests,scans}
}
function localRows(initial,imports,mode,proof=null,cap=10000000){
 let F=initial.map(f=>({id:f.id,vs:f.vs.slice(),ok:f.ok.slice()})),seq=Math.max(0,...F.map(f=>f.id))+1;
 for(let C of imports){let vs=[...new Set(C.map(Math.abs))].sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++)if(C.some(l=>(w>>vs.indexOf(Math.abs(l))&1)===+(l>0)))ok.push(w);F.push({id:seq++,vs,ok})}
 let M={events:0,forced:0,arcs:0,scc:0,binaryConflicts:0,probes:0,deletions:0,rootClosures:0},trace=[];function tick(n=1){M.events+=n;if(M.events>cap)throw Error("cap")}
 function close(pins){
 let a=new Map(pins);for(;;){let live=[],change=false;for(let f of F){let ok=f.ok.filter(w=>{tick(f.vs.length+1);return f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1))});if(!ok.length)return null;live.push({...f,ok});for(let i=0;i<f.vs.length;i++){let b=ok[0]>>i&1;tick(ok.length);if(!a.has(f.vs[i])&&ok.every(w=>(w>>i&1)===b)){a.set(f.vs[i],b);M.forced++;change=true}}}if(change)continue;
 if(mode){let adj=new Map(),rev=new Map();function arc(x,y){if(!adj.has(x))adj.set(x,[]);if(!adj.has(y))adj.set(y,[]);if(!rev.has(x))rev.set(x,[]);if(!rev.has(y))rev.set(y,[]);adj.get(x).push(y);rev.get(y).push(x);M.arcs++;tick()}
 for(let f of live)for(let i=0;i<f.vs.length;i++)for(let j=i+1;j<f.vs.length;j++){let x=f.vs[i],y=f.vs[j];if(a.has(x)||a.has(y))continue;let mask=0;for(let w of f.ok){tick();mask|=1<<((w>>i&1)+2*(w>>j&1))}for(let t=0;t<4;t++)if(!(mask>>t&1)){let l=t&1?x:-x,m=t&2?y:-y;arc(l,-m);arc(m,-l)}}
 if(proof){ // independent verifier: mutual reachability rather than SCC
 function reach(x,y){let S=new Set([x]),Q=[x];for(let i=0;i<Q.length;i++){tick();for(let z of adj.get(Q[i])||[]){tick();if(z===y)return true;if(!S.has(z)){S.add(z);Q.push(z)}}}return false}
 for(let v of adj.keys())if(v>0&&reach(v,-v)&&reach(-v,v)){M.binaryConflicts++;return null}
 }else{let seen=new Set(),order=[],comp=new Map();function visit(v){seen.add(v);tick();for(let x of adj.get(v)||[]){tick();if(!seen.has(x))visit(x)}order.push(v)}for(let v of adj.keys())if(!seen.has(v))visit(v);function back(v,c){comp.set(v,c);tick();for(let x of rev.get(v)||[]){tick();if(!comp.has(x))back(x,c)}}let c=0;for(let v of order.reverse())if(!comp.has(v))back(v,c++);M.scc++;for(let v of adj.keys())if(v>0&&comp.has(-v)&&comp.get(v)===comp.get(-v)){M.binaryConflicts++;return null}}
 }return{a,live}
 }}
 function test(f,w,a){let pins=new Map(a);for(let i=0;i<f.vs.length;i++){let v=f.vs[i],b=w>>i&1;if(pins.has(v)&&pins.get(v)!==b)return true;pins.set(v,b)}M.probes++;return close(pins)===null}
 try{for(;;){M.rootClosures++;let c=close([]);if(c===null){if(proof&&trace.length!==proof.length)throw Error("unused proof");return {status:"UNSAT",trace,...M}}let f,w;if(proof){if(trace.length>=proof.length)return{status:"UNKNOWN",trace,...M};let [id,b]=proof[trace.length];f=c.live.find(x=>x.id===id);w=b;if(!f||!f.ok.includes(w)||!test(f,w,c.a))throw Error("invalid row proof")}else{let found=false;for(let t of c.live){for(let b of t.ok){if(test(t,b,c.a)){f=t;w=b;found=true;break}}if(found)break}if(!found)return{status:"UNKNOWN",reason:"fixed point",trace,...M}}
 let orig=F.find(t=>t.id===f.id);orig.ok=orig.ok.filter(x=>x!==w);trace.push([f.id,w]);M.deletions++;
 }}catch(e){return{status:"UNKNOWN",reason:String(e),trace,...M}}
}
if(typeof module!=='undefined')module.exports={pin,projection,localRows};
