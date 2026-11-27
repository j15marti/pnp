function paired(ctx,old,newer,E,G){
 const {chart,V,trace,n}=ctx,all=old.eligible;
 // Independently reconstruct prior core and row eligibility screen.
 let pre={rows:0,pinChecks:0,scoreReads:0,polyChecks:0,polyTerms:0,coverageChecks:0};
 const checked=[];
 for(const q of [...old.local,...old.peer]){pre.rows+=ctx.replayTree(chart.filter(f=>q.core.includes(f.i)),q.pins,q.tree,500000).rows;checked.push(q)}
 pre.rows+=ctx.replayTree(chart.filter(f=>old.root.tree.core.includes(f.i)),[],old.root.tree.s.tree,500000).rows;
 const guardVars=old.guardProjection.vs;
 const same=(a,b)=>a.slice().sort((x,y)=>x-y).join(",")===b.slice().sort((x,y)=>x-y).join(",");
 const U=new Set(),H=new Set();
 for(let mask=0;mask<2**guardVars.length;mask++){
   let pins=new Map(guardVars.map((v,j)=>[v,(mask>>j)&1]));
   const applies=q=>{pre.pinChecks+=q.pins.length;return q.pins.every(([v,b])=>pins.get(v)===b)};
   if(!old.local.some(applies)||!old.peer.some(applies))throw Error("incomplete guard partition");
   const active=checked.filter(applies);
   const eligible=i=>{let f=chart[i];return f.cost.some((z,w)=>{pre.scoreReads++;return z===2&&f.vs.every((v,j)=>!pins.has(v)||pins.get(v)===((w>>j)&1))})};
   const base=all.filter(i=>old.root.tree.core.includes(i)&&active.every(q=>q.core.includes(i))&&eligible(i));
   if(!same(base,old.guardProjection.cells.find(c=>c.mask===mask).hit))throw Error("old cover mismatch");
   base.forEach(i=>U.add(i));
   let cell=newer.cells.find(c=>c.mask===mask);
   if(!cell){base.forEach(i=>H.add(i));continue}
   let free=V.filter(v=>!pins.has(v)),at=new Map(free.map((v,i)=>[v,i])),remain=new Set(all.filter(eligible));
   for(const a of cell.attempts){
     if(a.status!=="UNSAT")continue;
     let terms=new Set(),owners=new Set();
     for(const desc of a.certificate){
       if(a.drop.includes(desc.owner))throw Error("certificate uses relaxed factor");
       let f=chart[desc.owner],poly=desc.poly.map(BigInt),m=BigInt(desc.mult);
       owners.add(desc.owner);
       for(let w=0;w<f.cost.length;w++){
         if(f.cost[w]||!f.vs.every((v,j)=>!pins.has(v)||pins.get(v)===((w>>j)&1)))continue;
         let word=0n;for(const [j,v] of f.vs.entries())if(at.has(v)&&((w>>j)&1))word|=1n<<BigInt(at.get(v));
         let z=0;for(const p of poly){pre.polyChecks++;z^=Number((p&word)===p)}if(z)throw Error("bad local parity polynomial");
       }
       for(const p of poly){let term=String(p|m);pre.polyTerms++;if(terms.has(term))terms.delete(term);else terms.add(term)}
     }
     if(terms.size!==1||!terms.has("0")||!same([...owners],a.owners))throw Error("bad parity proof");
     for(const i of remain){pre.coverageChecks++;if(!owners.has(i))remain.delete(i)}
   }
   if(!same([...remain],cell.remaining))throw Error("parity candidate mismatch");
   const join=base.filter(i=>remain.has(i));if(!same(join,cell.combined))throw Error("hybrid mismatch");join.forEach(i=>H.add(i));
 }
 if(!same([...U],old.guardProjection.projected)||!same([...H],newer.combined.candidates))throw Error("global union mismatch");
 // Same deterministic adaptive strategy, one hard meter for all counted categories. Counts retained even on thrown cap.
 const cap=5000000;
 function run(seed){
   const events={build:0,clauseScans:0,literalReads:0,branchNodes:0,checkerFactorScans:0,checkerRows:0,checkerPinReads:0,coverage:0,scoreReads:0};
   let total=0;const tick=(name,amount=1)=>{if(total+amount>cap)throw Error("cap");events[name]+=amount;total+=amount};
   let probes=0,completed=0,failed=0,proofs=[],queue=[seed.slice().sort((a,b)=>a-b)],live=new Set(seed),status="UNKNOWN",W=null,why=null;
   function cnf(fs){let C=[];for(let f of fs)for(let w=0;w<f.cost.length;w++){tick("build");if(f.cost[w]!==0){let cl=[];for(let j=0;j<f.vs.length;j++){tick("build");cl.push(((w>>j)&1)?-(f.vs[j]+1):f.vs[j]+1)}C.push(cl)}}return C}
   function search(C){
     function close(A){A=new Map(A);while(true){let change=false,score=new Map();for(let c of C){tick("clauseScans");let open=[],sat=false;for(let l of c){tick("literalReads");let x=A.get(Math.abs(l)-1);if(x===undefined)open.push(l);else if(x===Number(l>0)){sat=true;break}}if(sat)continue;if(!open.length)return {dead:true};if(open.length===1){let l=open[0];A.set(Math.abs(l)-1,Number(l>0));change=true}else for(const l of open)score.set(Math.abs(l)-1,(score.get(Math.abs(l)-1)||0)+1)}if(!change)return {A,score}}}
     function dfs(A){tick("branchNodes");let z=close(A);if(z.dead)return {tree:null};if(!z.score.size)return {assignment:[...z.A]};let v=[...z.score].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let a=dfs([...z.A,[v,0]]);if(a.assignment)return a;let b=dfs([...z.A,[v,1]]);if(b.assignment)return b;return {tree:[v+1,a.tree,b.tree]}}
     return dfs([]);
   }
   function check(fs,tree){let used=new Set();function close(A){A=new Map(A);while(true){let changed=false;for(let f of fs){tick("checkerFactorScans");let good=[];for(let w=0;w<f.cost.length;w++){tick("checkerRows");if(f.cost[w])continue;let ok=true;for(let j=0;j<f.vs.length;j++){tick("checkerPinReads");let v=f.vs[j];if(A.has(v)&&A.get(v)!==((w>>j)&1)){ok=false;break}}if(ok)good.push(w)}if(!good.length){used.add(f.i);return null}for(let j=0;j<f.vs.length;j++){let v=f.vs[j];if(A.has(v))continue;let b=(good[0]>>j)&1,force=true;for(let w of good){tick("checkerPinReads");if(((w>>j)&1)!==b){force=false;break}}if(force){A.set(v,b);used.add(f.i);changed=true}}}if(!changed)return A}}
     function visit(A,t){tick("branchNodes");let q=close(A);if(!q)return;if(!Array.isArray(t))throw Error("invalid proof leaf");let v=t[0]-1;if(q.has(v))visit([...q],t[1+q.get(v)]);else{visit([...q,[v,0]],t[1]);visit([...q,[v,1]],t[2])}}
     visit([],tree);return [...used].sort((a,b)=>a-b);
   }
   function evaluate(assignment){let A=new Map(assignment),cost=0;const full=V.map(v=>[v,A.get(v)||0]);A=new Map(full);for(const f of chart){tick("scoreReads");const w=f.vs.reduce((a,v,j)=>a|((A.get(v)||0)<<j),0);cost+=f.cost[w]}return {best:cost,assignment:full}}
   function probe(D,threshold=false){probes++;let ds=new Set(D),fs=chart.filter(f=>!ds.has(f.i));if(threshold){const f=chart[D[0]];fs.push({...f,cost:f.cost.map(c=>c<=2?0:1)})}const q=search(cnf(fs));if(q.assignment){completed++;return {feasible:true,assignment:q.assignment}}const owners=check(fs,q.tree);let subset=fs.filter(f=>owners.includes(f.i));check(subset,q.tree);completed++;return {tree:q.tree,owners,threshold,drop:D}}
   try{
     while(queue.length&&live.size){let D=queue.shift().filter(i=>live.has(i));if(!D.length)continue;let q=probe(D);
       if(q.feasible){let w=evaluate(q.assignment);if(w.best<=2){W=w;status="ENERGY_LE_2_EXISTS";break}if(D.length>1){let mid=Math.ceil(D.length/2);queue.unshift(D.slice(0,mid),D.slice(mid));continue}q=probe(D,true);if(q.feasible){W=evaluate(q.assignment);if(W.best>2)throw Error("threshold false witness");status="ENERGY_LE_2_EXISTS";break}}
       const before=live.size;if(q.threshold){for(let i of D){tick("coverage");live.delete(i)}}else{for(let i of live){tick("coverage");if(!q.owners.includes(i))live.delete(i)}}proofs.push({...q,removed:before-live.size});
     }
     if(!live.size&&status==="UNKNOWN")status="ENERGY_LE_2_REFUTED";
   }catch(e){why=String(e);failed=probes-completed}
   let lift=null;if(W){let a=E.lift(G,n,trace,W);lift={defects:a.defects,assignment:W.assignment,best:W.best}}
   return {seed:seed.length,probes,completed,failed,proofs,remaining:[...live],status,why,events,total,cap,lift}
 }
 const base=run([...U]),hybrid=run([...H]);
 return {pre,base,hybrid};
}
if(typeof module!=="undefined")module.exports={paired};
