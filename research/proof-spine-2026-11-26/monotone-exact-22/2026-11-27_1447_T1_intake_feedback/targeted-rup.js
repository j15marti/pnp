module.exports=function probe(dimacs,mode,flipSeed){
 const rows=dimacs.trimEnd().split("\n"),n=+rows.shift().split(" ")[2],F=rows.map(s=>[...new Set(s.trim().split(/\s+/).map(Number).slice(0,-1))]),C=F.map(c=>c.slice());
 let work=0,checks=0,proof=[],fail=0,rounds=0,cap=1500000,known=new Set(C.map(c=>c.slice().sort((a,b)=>a-b).join(","))),a=Array(n+1).fill(0),t0=Date.now();
 // Replay deterministic local descent, compute priority from remaining original violated constraints.
 if(mode==="score"){for(const f of flipSeed){if(f.label!=="all-false")break;a[f.v]^=1}work+=F.reduce((s,c)=>s+c.length,0)}
 const s=new Map(Array.from({length:n},(_,i)=>[i+1,0]));for(const c of F)if(!c.some(l=>a[Math.abs(l)]===+(l>0)))for(const l of c){s.set(Math.abs(l),s.get(Math.abs(l))+1);work++}
 const order=Array.from({length:n},(_,i)=>i+1);if(mode==="score")order.sort((a,b)=>s.get(b)-s.get(a)||a-b);
 function close(g){const p=new Int8Array(n+1).fill(-1);let log=[];for(let l of g)p[Math.abs(l)]=+(l>0);
  for(;;){let changed=false;for(let i=0;i<C.length;i++){let u=0,L=0,sat=false;for(let l of C[i]){work++;if(p[Math.abs(l)]===+(l>0)){sat=true;break}if(p[Math.abs(l)]<0){u++;L=l}}if(sat)continue;if(u===0)return {conflict:i+1,log};if(u===1){p[Math.abs(L)]=+(L>0);log.push([i+1,L]);changed=true}}if(!changed)return null}
 }
 let status="UNKNOWN";function tryGuard(g){const learned=g.map(l=>-l).sort((a,b)=>a-b),k=learned.join(",");if(known.has(k))return false;checks++;let r=close(g);if(r){proof.push({id:C.length+1,guard:g.slice(),row:learned,trace:r});C.push(learned);known.add(k);return true}fail++;return false}
 const guards=[];for(const v of order)for(const b of [0,1])guards.push([b?v:-v]);for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(const b of [0,1])for(const c of [0,1])guards.push([b?order[i]:-order[i],c?order[j]:-order[j]]);
 while(work<cap){rounds++;let added=0;for(const g of guards){if(work>=cap)break;if(tryGuard(g)){added++;if(close([])){status="UNSAT";break}}}if(status==="UNSAT"||!added)break}
 let verification=0;
 // replay independently against immutable original rows using trace parent unit checks (no search)
 let D=F.map(c=>c.slice());for(const p of proof){let K=new Set(p.guard);for(const [id,l] of p.trace.log){let C=D[id-1];verification+=C.length;if(!C.includes(l)||C.some(x=>x!==l&&!K.has(-x))||K.has(-l))throw Error("invalid unit");K.add(l)}let c=D[p.trace.conflict-1];verification+=c.length;if(!c.every(l=>K.has(-l)))throw Error("invalid conflict");D.push(p.row)}
 const rootTrace=status==="UNSAT"?close([]):null;if(rootTrace){let K=new Set();for(const [id,l] of rootTrace.log){let c=D[id-1];verification+=c.length;if(!c.includes(l)||c.some(x=>x!==l&&!K.has(-x))||K.has(-l))throw Error("root unit");K.add(l)}const c=D[rootTrace.conflict-1];verification+=c.length;if(!c.every(l=>K.has(-l)))throw Error("root conflict")}
 return {mode,status,checks,fail,rounds,work,verification,learned:proof,rootTrace,order,elapsedMs:Date.now()-t0,peakRows:C.length,peakLiterals:C.reduce((s,c)=>s+c.length,0),note:"score arm uses previously measured strict-descent flips; add that acquisition cost to comparison"};
};
