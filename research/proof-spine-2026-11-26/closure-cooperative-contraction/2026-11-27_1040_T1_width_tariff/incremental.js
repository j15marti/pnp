function incremental(F,cap,limit){
 let db=new Map(),inc=new Map(),queue=[],head=0,pins=new Map(),trace=[],next=0,m={index:0,tests:0,closure:0,choices:0,rowCreates:0,peakRows:0,max:0},rows=0;
 const work=()=>m.index+m.tests+m.closure+m.choices+m.rowCreates;
 const add=f=>{if(f.ok.length===2**f.vs.length)return;let i=next++;db.set(i,f);queue.push(i);rows+=f.ok.length;m.rowCreates+=f.ok.length;m.peakRows=Math.max(m.peakRows,rows);for(let v of f.vs){m.index++;if(!inc.has(v))inc.set(v,new Set());inc.get(v).add(i)}};
 const del=i=>{let f=db.get(i);if(!f)return;for(let v of f.vs){m.index++;inc.get(v).delete(i);if(!inc.get(v).size)inc.delete(v)}rows-=f.ok.length;db.delete(i)};
 const gauge=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b).reduce((best,v)=>best,0); // gauge is chosen below by max native incidence
 F.forEach(add);let g=[...inc].sort((a,b)=>b[1].size-a[1].size||a[0]-b[0])[0][0];add({vs:[g],ok:[0]});
 function close(){while(head<queue.length){let i=queue[head++],f=db.get(i);if(!f)continue;if(!f.ok.length)return false;let bit=null;for(let j=0;j<f.vs.length;j++){let a=(f.ok[0]>>j)&1;m.closure+=f.ok.length;if(f.ok.every(w=>((w>>j)&1)===a)){bit=[f.vs[j],a];break}}if(!bit)continue;let [v,a]=bit;if(pins.has(v)&&pins.get(v)!==a)return false;pins.set(v,a);trace.push(["pin",v,a]);for(let k of [...inc.get(v)]){let z=db.get(k),j=z.vs.indexOf(v),vs=z.vs.filter(u=>u!==v),ok=z.ok.filter(w=>((w>>j)&1)===a).map(w=>(w&((1<<j)-1))|((w>>(j+1))<<j));m.closure+=z.ok.length;del(k);add({vs,ok})}}return true}
 while(true){if(!close())return {status:"UNSAT",g,trace,m,F:[...db.values()]};if(!inc.size)return {status:"FEASIBLE",g,trace,m,F:[...db.values()]};if(work()>limit)return {status:"UNKNOWN_CAP",g,trace,m,F:[...db.values()]};let best=null;
 // Stop as soon as a minimum-width candidate of width <=4 is found. This is a deterministic heuristic, not an optimal order oracle.
 for(let [v,set] of inc){let ids=[...set],U=[...new Set(ids.flatMap(i=>db.get(i).vs))].sort((a,b)=>a-b);m.choices+=ids.length;if(U.length<=cap&&(!best||U.length<best.U.length))best={v,ids,U};if(best&&best.U.length<=4)break}
 if(!best)return {status:"UNKNOWN_WIDTH",g,trace,m,F:[...db.values()]};let {v,ids,U}=best,vs=U.filter(u=>u!==v),ok=[],S=ids.map(i=>new Set(db.get(i).ok)),I=ids.map(i=>db.get(i).vs.map(u=>U.indexOf(u)));
 for(let w=0;w<2**U.length;w++){let yes=true;for(let j=0;j<ids.length;j++){m.tests++;let z=I[j].reduce((a,k,t)=>a|(((w>>k)&1)<<t),0);if(!S[j].has(z)){yes=false;break}}if(yes){let y=vs.reduce((a,u,t)=>a|(((w>>U.indexOf(u))&1)<<t),0);if(!ok.includes(y))ok.push(y)}}
 m.max=Math.max(m.max,U.length);trace.push(["elim",v]);ids.forEach(del);add({vs,ok});
 }
}

function independentReplay(F,g,trace,cap=12){
 let D=F.map(f=>({vs:f.vs.slice(),ok:f.ok.slice()}));D.push({vs:[g],ok:[0]});let checks=0;
 for(let step of trace){let [kind,v,b]=step;if(kind==="pin"){if(!D.some(f=>{let j=f.vs.indexOf(v);return j>=0&&f.ok.length>0&&f.ok.every(w=>{checks++;return ((w>>j)&1)===b})}))throw Error("unsupported pin");D=D.map(f=>{let j=f.vs.indexOf(v);if(j<0)return f;let vs=f.vs.filter(u=>u!==v),ok=[];for(let w of f.ok){checks++;if(((w>>j)&1)===b)ok.push((w&((1<<j)-1))|((w>>(j+1))<<j))}return {vs,ok}}).filter(f=>f.ok.length!==2**f.vs.length)}
 else{let B=D.filter(f=>f.vs.includes(v));if(!B.length)throw Error("empty bucket");let U=[...new Set(B.flatMap(f=>f.vs))].sort((a,b)=>a-b),vs=U.filter(u=>u!==v),ok=[];if(U.length>cap)throw Error("cap");for(let w=0;w<2**vs.length;w++){let a=new Map(vs.map((u,j)=>[u,(w>>j)&1]));for(let b of [0,1]){a.set(v,b);let hit=true;for(let f of B){checks++;let x=f.vs.reduce((s,u,j)=>s+(a.get(u)<<j),0);if(!f.ok.includes(x)){hit=false;break}}if(hit){ok.push(w);break}}}D=D.filter(f=>!f.vs.includes(v));if(ok.length!==2**vs.length)D.push({vs,ok})}}
 return {checks,empty:D.some(f=>!f.ok.length),F:D};
}

function conflict(C,lits,m){let A=new Set(lits);if([...A].some(l=>A.has(-l)))return true;for(;;){let change=false;for(let c of C){m.scans++;if(c.some(l=>A.has(l)))continue;let u=c.filter(l=>!A.has(-l));if(!u.length)return true;if(u.length===1){A.add(u[0]);change=true}}if(!change)return false}}

function peerReplay(F,C){let D=new Map(F.map((f,i)=>[i,f])),checks=0;for(let t of C.trace){let B=[...D].filter(([i,f])=>f.vs.includes(t.v)),ids=B.map(x=>x[0]).sort((a,b)=>a-b);if(JSON.stringify(ids)!==JSON.stringify(t.in.slice().sort((a,b)=>a-b))||D.has(t.out))throw Error("peer bucket IDs");let vs=[...new Set(B.flatMap(x=>x[1].vs))].filter(v=>v!==t.v).sort((a,b)=>a-b),ok=[];if(vs.length>12)throw Error("peer width");for(let w=0;w<2**vs.length;w++){let a=new Map(vs.map((v,i)=>[v,(w>>i)&1]));for(let b=0;b<2;b++){a.set(t.v,b);let good=true;for(let [,f] of B){checks++;let x=f.vs.reduce((s,v,j)=>s+(a.get(v)<<j),0);if(!f.ok.includes(x)){good=false;break}}if(good){ok.push(w);break}}}if(JSON.stringify(vs)!==JSON.stringify(t.vs)||JSON.stringify(ok)!==JSON.stringify(t.ok.slice().sort((a,b)=>a-b)))throw Error("peer projection");ids.forEach(i=>D.delete(i));D.set(t.out,{vs,ok})}
 let baseChecks=0,db=[...D.values()];for(let c of C.base){if(c.length===1&&c[0]===-C.gauge)continue;if(!db.some(f=>c.every(l=>f.vs.includes(Math.abs(l)))&&f.ok.every(w=>{baseChecks++;return c.some(l=>((w>>f.vs.indexOf(Math.abs(l)))&1)===Number(l>0))})))throw Error("base not implied")}
 let Q=C.base.slice(),m={scans:0};for(let c of C.proof){if(!conflict(Q,c.map(l=>-l),m))throw Error("RUP invalid");Q.push(c)}if(C.proof.at(-1).length)throw Error("missing empty");return {checks,baseChecks,scans:m.scans,additions:C.proof.length};
}
module.exports={incremental,independentReplay,peerReplay};
