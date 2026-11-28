function weighted(ctx,old,parity,pair,mini,K){
 const {chart,V}=ctx;let ledger={treeRows:0,polyChecks:0,polyTerms:0,eligibilityRows:0,greedyChecks:0,coefficientChecks:0,miniReplayReads:0};let base=[];
 function treeCore(name,owners,pins,t){let sub=chart.filter(f=>owners.includes(f.i));let c=ctx.replayTree(sub,pins,t,500000);ledger.treeRows+=c.rows;base.push({name,owners,pins});}
 treeCore("root",old.root.tree.core,[],old.root.tree.s.tree);
 for(const [i,q] of [...old.local,...old.peer].entries())treeCore("old"+i,q.core,q.pins,q.tree);
 for(const [i,q] of pair.hybrid.proofs.entries()){if(q.threshold)throw Error("not zero core");treeCore("batch"+i,q.owners,[],q.tree)}
 for(const cell of parity.cells){let P=new Map(cell.pins),free=V.filter(v=>!P.has(v)),at=new Map(free.map((v,i)=>[v,i]));for(const [j,a] of cell.attempts.entries()){if(a.status!=="UNSAT")continue;let out=new Set(),own=new Set();for(const t of a.certificate){let f=chart[t.owner],poly=t.poly.map(BigInt),m=BigInt(t.mult);if(a.drop.includes(t.owner))throw Error("drop");own.add(t.owner);for(let w=0;w<f.cost.length;w++){if(f.cost[w]||!f.vs.every((v,i)=>!P.has(v)||P.get(v)===((w>>i)&1)))continue;let x=0n;f.vs.forEach((v,i)=>{if(at.has(v)&&((w>>i)&1))x|=1n<<BigInt(at.get(v))});let z=0;for(let p of poly){ledger.polyChecks++;z^=Number((p&x)===p)}if(z)throw Error("poly local");}for(const p of poly){let s=String(p|m);ledger.polyTerms++;if(out.has(s))out.delete(s);else out.add(s)}}if(out.size!==1||!out.has("0")||[...own].some(i=>!a.owners.includes(i))||own.size!==a.owners.length)throw Error("poly certificate");base.push({name:"parity"+cell.mask+"."+j,owners:[...own],pins:cell.pins});}}
 let rows=[];const vars=old.guardProjection.vs;
 for(let mask=0;mask<2**vars.length;mask++){let pins=vars.map((v,j)=>[v,(mask>>j)&1]),P=new Map(pins),applies=q=>q.pins.every(([v,b])=>P.get(v)===b);
 let active=base.filter(applies),eligible=chart.filter(f=>f.cost.some((c,w)=>{ledger.eligibilityRows++;return c===2&&f.vs.every((v,i)=>!P.has(v)||P.get(v)===((w>>i)&1))})).map(f=>f.i);
 // Test exact mini bucket imports before coefficient selection.
 let mi=mini.results.find(r=>r.label!=="root"&&applies(r));let m=mi?.arms.filter(a=>a.status==="BOUND"&&a.bound>=4).sort((a,b)=>Object.values(a.events).reduce((s,x)=>s+x,0)-Object.values(b.events).reduce((s,x)=>s+x,0))[0];
 if(m){let ck=K.verify(chart,mi.pins,m);ledger.miniReplayReads+=ck.reads+ck.bitreads+ck.rows;rows.push({mask,pins,method:"mini",guard:mi.label,bound:m.bound,check:ck});continue}
 // Cover candidate owners by complements of cores. Empty candidate set still needs an explicit root core to exclude energy zero.
 let live=new Set(eligible),chosen=[];while(live.size){let best=null,gain=0;for(const q of active){let g=0;for(let i of live){ledger.greedyChecks++;g+=!q.owners.includes(i)}if(g>gain){gain=g;best=q}}if(!best)throw Error("uncovered support");chosen.push(best);for(let i of live)if(!best.owners.includes(i))live.delete(i)}
 if(!chosen.length)chosen.push(active[0]);
 // If K=1 the coefficient rule uses ratio M=max_i 2 a_i/c_i; calculate using doubled integer inequality to avoid floats.
 const k=chosen.length,counts=chart.map(f=>chosen.reduce((s,q)=>s+Number(q.owners.includes(f.i)),0));let maxNum=0,maxDen=1;
 for(const f of chart){for(let w=0;w<f.cost.length;w++){ledger.coefficientChecks++;let c=f.cost[w];if(!c||!f.vs.every((v,i)=>!P.has(v)||P.get(v)===((w>>i)&1)))continue;let a=counts[f.i];if(a*maxDen>maxNum*(c/2)){maxNum=a;maxDen=c/2}}}
 if(maxNum===0)throw Error("zero coefficient unexpected");
 // k <= (maxNum/maxDen) E/2. E is even.
 let bound=2*Math.ceil(k*maxDen/maxNum);if(bound<4)throw Error("weak coefficient bound");rows.push({mask,pins,method:"weighted",eligible:eligible.length,selected:chosen.map(q=>q.name),k,maxNum,maxDen,bound,counts});
 }
 return {ledger,rows,allCores:base.map(x=>({name:x.name,owners:x.owners,pins:x.pins})),bound:Math.min(...rows.map(x=>x.bound))};
}
module.exports={weighted};
