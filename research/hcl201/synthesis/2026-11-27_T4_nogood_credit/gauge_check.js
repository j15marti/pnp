
function learn(initial, gaugeBit, width, cap, replay=null){
 let fs=initial.map(f=>({...f})),vars=[...new Set(fs.flatMap(f=>f.vs))].sort((a,b)=>a-b),root=new Map(gaugeBit===null?[]:[[gaugeBit,0]]),learned=[],metrics={tests:0,probes:0,learned:0,rootPins:0,passes:0,peakRows:0,cumulativeRows:0,closureCalls:0},seen=new Set();
 function close(pins){
   metrics.closureCalls++;let idx=new Map(),pending=fs.map((_,i)=>i),queued=new Set(pending);
   fs.forEach((f,i)=>{for(let v of f.vs){if(!idx.has(v))idx.set(v,[]);idx.get(v).push(i)}});
   metrics.peakRows=Math.max(metrics.peakRows,fs.reduce((s,f)=>s+f.ok.length,0));
   while(pending.length){let id=pending.pop();queued.delete(id);let f=fs[id],and=(1<<f.vs.length)-1,or=0,hit=false;
    for(let w of f.ok){if(++metrics.tests>cap)throw Error("CAP");if(!f.vs.every((v,i)=>!pins.has(v)||pins.get(v)===(w>>i&1)))continue;and&=w;or|=w;hit=true;}
    metrics.cumulativeRows+=f.ok.length;if(!hit)return null;
    for(let i=0;i<f.vs.length;i++){let v=f.vs[i];if(!pins.has(v)&&(and>>i&1)===(or>>i&1)){pins.set(v,and>>i&1);for(let j of idx.get(v))if(!queued.has(j)){queued.add(j);pending.push(j)}}}
   }return pins;
 }
 function add(vs,w){let k=JSON.stringify([vs,w]);if(seen.has(k))return;seen.add(k);fs.push({vs,ok:Array.from({length:2**vs.length},(_,i)=>i).filter(i=>i!==w)});learned.push({vs,w});metrics.learned++;}
 try{while(true){metrics.passes++;let p=close(new Map(root));if(p===null)return{status:"UNSAT",learned,metrics};root=p;metrics.rootPins=root.size;
 if(replay!==null){if(learned.length===replay.length)return{status:"UNKNOWN",learned,metrics};let {vs,w}=replay[learned.length];if(vs.length<1||vs.length>width||vs.some((v,i)=>!vars.includes(v)||root.has(v)||(i>0&&vs[i-1]>=v))||w<0||w>=2**vs.length||seen.has(JSON.stringify([vs,w])))throw Error("BAD STEP");let a=new Map(root);vs.forEach((v,i)=>a.set(v,w>>i&1));metrics.probes++;if(close(a)!==null)throw Error("UNJUSTIFIED");add(vs,w);continue;}
 let left=vars.filter(v=>!root.has(v)),changed=false;
 outer:for(let k=1;k<=width;k++){let scopes=k===1?left.map(v=>[v]):left.flatMap((v,i)=>left.slice(i+1).map(u=>[v,u]));for(let vs of scopes)for(let w=0;w<2**k;w++){if(seen.has(JSON.stringify([vs,w])))continue;let a=new Map(root);vs.forEach((v,i)=>a.set(v,w>>i&1));metrics.probes++;if(close(a)===null){add(vs,w);changed=true;break outer;}}}
 if(!changed)return{status:"UNKNOWN",learned,metrics};
 }}catch(e){return{status:String(e),learned,metrics}}
}
function cnfTables(dimacs){return dimacs.trim().split("\n").slice(1).map((s,id)=>{let c=s.split(/\s+/).map(Number).slice(0,-1),vs=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);if(vs.length>20)throw Error("CNF table cap");let ok=[];for(let w=0;w<2**vs.length;w++)if(c.some(l=>((w>>vs.indexOf(Math.abs(l)))&1)===Number(l>0)))ok.push(w);return{id,vs,ok}})}
function checkLearn(fs,gaugeBit,steps){
 let F=fs.map(f=>({...f})),A=new Map(gaugeBit===null?[]:[[gaugeBit,0]]),tests=0,scans=0;
 function close(a){for(;;){let change=false;for(let f of F){scans++;let rows=f.ok.filter(w=>{tests++;return f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1))});if(!rows.length)return false;for(let i=0;i<f.vs.length;i++){let v=f.vs[i],b=rows[0]>>i&1;if(!a.has(v)&&rows.every(w=>(w>>i&1)===b)){a.set(v,b);change=true}}}if(!change)return true}}
 for(let {vs,w} of steps){if(!close(A))throw Error("extra steps");if(!Array.isArray(vs)||vs.length<1||vs.length>2||vs.some((v,i)=>!F.some(f=>f.vs.includes(v))||A.has(v)||(i&&vs[i-1]>=v))||!Number.isInteger(w)||w<0||w>=2**vs.length)throw Error("step");let B=new Map(A);vs.forEach((v,i)=>B.set(v,w>>i&1));if(close(B))throw Error("false nogood");F.push({vs,ok:Array.from({length:2**vs.length},(_,i)=>i).filter(i=>i!==w)});}
 return{verified:!close(A),tests,scans}
}


function specialize(F,g){
 let out=[],keys=new Set(),tests=0;
 for(let f of F){let vs=f.vs.slice(),ok=f.ok.slice(),i=vs.indexOf(g);
 if(i>=0){vs.splice(i,1);ok=ok.filter(w=>{tests++;return !(w>>i&1)}).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i));}
 ok.sort((a,b)=>a-b);if(ok.length===2**vs.length)continue;
 const key=JSON.stringify([vs,ok]);if(!keys.has(key)){keys.add(key);out.push({vs,ok});}}
 return{fs:out,tests}
}

const fs=require("node:fs"),[compiler,corpus,registry,helper,path]=process.argv.slice(2),c=fs.readFileSync(compiler,"utf8"),p=fs.readFileSync(helper,"utf8"),compile=Function(c.slice(c.indexOf("function compile"),c.indexOf("function auditLocal"))+";return compile")(),L=Function(p.slice(0,p.indexOf('const fs=require("node:fs"),[compiler'))+";return {sha,independentNormalize,verifyTrace}")(),B=JSON.parse(fs.readFileSync(corpus)),R=JSON.parse(fs.readFileSync(registry)),raw=fs.readFileSync(path,"utf8"),q=JSON.parse(raw),e=R.instances.find(e=>e.instance_id===q.instance_id),x=B.instances.find(x=>"EB-"+x.id===e.alias),g=compile(x),s=JSON.stringify(g.network)+"\n";if(L.sha(s)!==e.sha256||s.length*8!==e.N_bits||q.original_N_bits!==e.N_bits||q.guard_id!=="EMPTY"||q.residual_id!=="ROOT")throw Error("identity");const I=L.independentNormalize(g.network),V=L.verifyTrace(I.fs,q.trace);if(!V.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1))))||!V.fs.some(f=>f.vs.includes(q.gauge)))throw Error("gauge");const z=checkLearn(specialize(V.fs,q.gauge).fs,null,q.nogoods);if(!z.verified)throw Error("not UNSAT");console.log(JSON.stringify({id:L.sha(raw),...z}));
