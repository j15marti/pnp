// FP53 replay kernel. Use pinned FP51 energy.js, FP52 five_lanes.js and shared compile.js; build ctx exactly as documented in report.
function runNew(ctx,E,prior,entry,G,sha){
 const {chart,F,V,guards,core,support,affine,matching,bucket,replayTree}=ctx;
 if(!F.every(f=>f.cost.every(c=>Number.isInteger(c)&&c>=0&&c%2===0)))throw Error("even chart");
 const eligible=chart.filter(f=>f.cost.includes(2)).map(f=>f.i);
 const all=new Set(eligible);
 // Five independent root lanes, before learning or imports.
 const root={occupancy:support(chart),affine:affine(chart,[]),matching:matching(chart,[]),bucket:bucket(chart,[]),tree:core(chart,[],100000)};
 if(root.tree.s.status!=="UNSAT")throw Error("root refutation not found");
 const initialCore=root.tree.core;
 // Conditional imports: replay all own exact core proofs, reprove peer projections on same chart.
 const local=[],peer=[];
 let importRows=0,importScans=0,importLits=0;
 for(const l of prior.lanes){
   const chosen=chart.filter(f=>l.tree.core.includes(f.i));
   const ck=replayTree(chosen,l.guard,l.tree.s.tree,500000);importRows+=ck.rows;
   local.push({pins:l.guard,core:l.tree.core,tree:l.tree.s.tree,rows:ck.rows});
 }
 for(const p of prior.peer.reproofs){
   const owners=new Set(p.owners);const chosen=chart.filter(f=>f.ids.some(x=>owners.has(x)));
   if(!p.ps.every(([v,b])=>V.includes(v)&&(b===0||b===1)))throw Error("peer guard mismatch");
   // Independent direct reproof on an original-owner-containing factor superset.
   const z=core(chosen,p.ps,100000);importScans+=z.s.scans;importLits+=z.s.lits;importRows+=(z.ck?.rows||0)+(z.ck2?.rows||0);
   if(z.s.status!=="UNSAT")throw Error("peer consequence not reproved");
   peer.push({pins:p.ps,core:z.core,tree:z.s.tree,selected:chosen.map(f=>f.i),owners:p.owners,rows:(z.ck?.rows||0)+(z.ck2?.rows||0)});
 }
 // Exact projection of the union of guards onto their used pin coordinates.
 const vs=[...new Set([...local,...peer].flatMap(g=>g.pins.map(p=>p[0])))].sort((a,b)=>a-b);
 const relevant=[...local,...peer];
 let candidateVisits=0,checks=0,guardRows=0;
 const projected=new Set(), cells=[];
 for(let mask=0;mask<2**vs.length;mask++){
   const pin=new Map(vs.map((v,i)=>[v,(mask>>i)&1]));
   const A=relevant.filter(g=>{checks+=g.pins.length;return g.pins.every(([v,b])=>pin.get(v)===b)});
   if(!local.some(g=>g.pins.every(([v,b])=>pin.get(v)===b))||!peer.some(g=>g.pins.every(([v,b])=>pin.get(v)===b)))throw Error("cover failure");
   const hit=eligible.filter(i=>{candidateVisits++;return A.every(g=>g.core.includes(i))&&initialCore.includes(i)});
   const actual=hit.filter(i=>{const f=chart[i];return f.cost.some((c,w)=>{guardRows++;return c===2&&f.vs.every((v,j)=>!pin.has(v)||pin.get(v)===((w>>j)&1))})});
   actual.forEach(i=>projected.add(i));cells.push({mask,hit:actual});
 }
 // Compare exact singleton scan to root core learning and batched exclusions.
 // Mixed-event cap per method: proof scans+literals+independent row replays. Not bit-time.
 const cap=5000000;
 function lane(mode,seed){
   let remain=new Set(seed), scans=0,lits=0,rows=0,nodes=0,attempts=0,blocks=[],queue=[],learned=[],status="UNKNOWN",terminal=null,unknown=[];
   const used=()=>scans+lits+rows;
   const query=(D,threshold=false)=>{
     const drop=new Set(D);
     let fs=chart.filter(f=>!drop.has(f.i));
     if(threshold){if(D.length!==1)throw Error("threshold only singleton");const f=chart[D[0]];fs=[...fs,{...f,cost:f.cost.map(c=>c<=2?0:1)}]}
     attempts++;
     let s=E.proofSearch(E.asCNF(fs).clauses,Math.max(1,Math.min(100000,cap-used())));
     scans+=s.scans;lits+=s.lits;nodes+=s.nodes;
     if(s.status!=="UNSAT")return {status:s.status,tree:null,drop:D};
     const ck=replayTree(fs,[],s.tree,Math.max(1,Math.min(500000,cap-used())));rows+=ck.rows;
     const C=ck.used;const sub=fs.filter(f=>C.includes(f.i));const ck2=replayTree(sub,[],s.tree,Math.max(1,Math.min(500000,cap-used())));rows+=ck2.rows;
     return {status:"UNSAT",drop:D,threshold,core:C,tree:s.tree};
   };
   try {
     if(mode==="batch"){queue=[[...remain]];}
     while(remain.size&&used()<cap){
       let D;
       if(mode==="batch"){
         while(queue.length&&!queue[0].some(i=>remain.has(i)))queue.shift();
         if(!queue.length){if(unknown.length)break;queue=[[...remain]]}
         D=queue.shift().filter(i=>remain.has(i));
       }else D=[[...remain][0]];
       if(!D.length)break;
       const q=query(D,false);
       if(q.status==="UNSAT"){
         if(q.core.some(i=>D.includes(i)))throw Error("drop/core conflict");
         const before=remain.size;
         if(mode==="single"){for(const i of D)remain.delete(i)}else{for(const i of remain)if(!q.core.includes(i))remain.delete(i)}
         blocks.push({...q,removed:before-remain.size});learned.push(q.core);
       }else if(q.status==="zero witness"&&D.length>1&&mode==="batch"){
         const mid=Math.ceil(D.length/2);queue.unshift(D.slice(0,mid),D.slice(mid));blocks.push({drop:D,status:"RELAXATION_FEASIBLE"});
       }else if(q.status==="zero witness"&&D.length===1){
         const t=query(D,true);
         if(t.status==="UNSAT"){remain.delete(D[0]);blocks.push({...t,removed:1})}
         else if(t.status==="zero witness"){status="ENERGY_LE_2_EXISTS";terminal={candidate:D[0],note:"exact feasibility via complete DPLL; independent native upper-bound witness separately required"};blocks.push({drop:D,status:t.status});break}
         else {unknown.push(...D);remain.delete(D[0]);blocks.push({drop:D,status:t.status});}
       }else{
         unknown.push(...D);for(const i of D)remain.delete(i);blocks.push({drop:D,status:q.status});
       }
     }
     if(!remain.size&&!unknown.length&&status!=="ENERGY_LE_2_EXISTS")status="ENERGY_LE_2_REFUTED";
   }catch(e){status="UNKNOWN";terminal={error:String(e)}}
   return {mode,status,seed:seed.length,remaining:[...remain],unknown,terminal,scans,lits,rows,nodes,attempts,events:used(),cap,blocks};
 }
 const base=lane("single",eligible);
 const learn=lane("learn",eligible.filter(i=>initialCore.includes(i)));
 const batch=lane("batch",[...projected].sort((a,b)=>a-b));
 // Independent certificate coverage replay for every excluded candidate.
 function verifyCoverage(res,seed){let live=new Set(seed),rows=0,removed=0;for(const p of res.blocks){if(p.status!=="UNSAT")continue;let ds=new Set(p.drop);let fs=chart.filter(f=>!ds.has(f.i));if(p.threshold){let f=chart[p.drop[0]];fs.push({...f,cost:f.cost.map(c=>c<=2?0:1)})}fs=fs.filter(f=>p.core.includes(f.i));let ck=replayTree(fs,[],p.tree,500000);rows+=ck.rows;let before=live.size;if(p.threshold||res.mode==="single"){p.drop.forEach(i=>live.delete(i))}else for(const i of live)if(!p.core.includes(i))live.delete(i);if(before-live.size!==p.removed)throw Error("coverage mismatch");removed+=before-live.size}
 if(res.status==="ENERGY_LE_2_REFUTED"&&live.size)throw Error("uncovered candidate");
 return {rows,removed,remaining:[...live]};
 }
 const checksFinal=[verifyCoverage(base,eligible),verifyCoverage(learn,eligible.filter(i=>initialCore.includes(i))),verifyCoverage(batch,[...projected].sort((a,b)=>a-b))];
 // Independent upper-bound check via randomized search only; no search proof oracle.
 let w=E.witness(F,200000,2,137);let lift=E.lift(G,ctx.n,ctx.trace,w);
 if([base,learn,batch].some(x=>x.status==="ENERGY_LE_2_REFUTED")&&w.best<=2)throw Error("false refutation");
 return {eligible,root,local,peer,guardProjection:{vs,cells,candidateVisits,checks,guardRows,projected:[...projected]},importCosts:{rows:importRows,scans:importScans,lits:importLits},base,learn,batch,checksFinal,witness:{...w,defects:lift.defects},chartHash:ctx.chartHash,mapHash:ctx.mapHash,normalCost:ctx.normalCost,gauge:ctx.gauge,ownerMap:chart.map(f=>f.ids)};
}
if(typeof module!=="undefined")module.exports={runNew};
