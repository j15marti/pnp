function refine(ctx,prior,sha,entry){
 const {chart,gauge}=ctx;
 let events={discoveryReads:0,replayReads:0,rowWrites:0,replayWrites:0,scopeIndexReads:0,plans:0,guardCoverageChecks:0,peakRows:0,failed:0},cap=3000000;
 function evalPlan(t,pins,check){
  const P=new Map(t.pins),G=new Map(pins),Q=new Map();let bound=0,localReads=0,created=0,peak=0;
  function read(f,w){let field=check?"replayReads":"discoveryReads";if(events.discoveryReads+events.replayReads>=cap)throw Error("refinement cap");events[field]++;localReads++;return f.cost[w]}
  function put(id,vs,cost){events[check?"replayWrites":"rowWrites"]+=cost.length;created+=cost.length;Q.set(id,{vs,cost});peak=Math.max(peak,[...Q.values()].reduce((a,f)=>a+f.cost.length,0));events.peakRows=Math.max(events.peakRows,peak)}
  const idx=(vs,U,w)=>{events.scopeIndexReads+=vs.length;return vs.reduce((a,v,j)=>a|(((w>>U.indexOf(v))&1)<<j),0)};
  for(const f of chart){let vs=f.vs.filter(v=>!P.has(v)),cost=Array.from({length:2**vs.length},(_,w)=>{let i=f.vs.reduce((a,v,j)=>a|((P.has(v)?P.get(v):((w>>vs.indexOf(v))&1))<<j),0);return check?read(f,i)/2:Math.min(2,read(f,i)/2)});put(f.i,vs,cost)}
  const records=[];
  for(const s of t.plan.steps){let fs=s.in.map(i=>Q.get(i)),c=Array(2**s.S.length).fill(Infinity);
   if(fs.some(f=>!f)||!s.U.includes(s.v))throw Error("bad plan");
   if(check){for(let w=0;w<2**s.U.length;w++){if(G.has(s.v)&&((w>>s.U.indexOf(s.v))&1)!==G.get(s.v))continue;let z=0;for(const f of fs)z+=read(f,idx(f.vs,s.U,w));let j=idx(s.S,s.U,w);c[j]=Math.min(c[j],z)}}
   else {const U=[...s.S,s.v];for(let w=0;w<c.length;w++){for(const b of G.has(s.v)?[G.get(s.v)]:[0,1]){let z=0;for(const f of fs){z=Math.min(2,z+read(f,idx(f.vs,U,w|(b<<s.S.length))));if(z===2)break}c[w]=Math.min(c[w],z);if(!c[w])break}}}
   for(const i of s.in)Q.delete(i);put(s.id,s.S,c);records.push({id:s.id,cost:c.map(v=>Math.min(2,v))});
  }
  for(const f of Q.values()){if(f.vs.length)throw Error("nonconstant");bound+=read(f,0)}events.plans++;
  return {bound,clipped:Math.min(2,bound),localReads,created,peak,records};
 }
 let rows=[];
 for(const t of prior.tests){
  const counts=new Map();for(const s of t.plan.steps)counts.set(s.v,(counts.get(s.v)||0)+1);
  const split=[...counts].filter(([v,c])=>c>1).sort((a,b)=>b[1]-a[1]||a[0]-b[0]);
  let row={pins:t.pins,split,base:t.compressed.bound,levels:[]};
  let bound=t.compressed.bound,front=[{pins:[],bound}];
  // Three binary synchronization choices at root, two per guard. Reuse certified positive leaves and refine only subthreshold leaves.
  try{for(let k=0;k<Math.min(split.length,t.pins.length?2:3)&&bound<2;k++){
    let [v,degree]=split[k],next=[],newly=0;
    for(const z of front){if(z.bound>=2){next.push(z);continue}for(let b=0;b<2;b++){
      const pins=[...z.pins,[v,b]],a=evalPlan(t,pins,false),q=evalPlan(t,pins,true);
      if(a.clipped!==q.clipped||JSON.stringify(a.records)!==JSON.stringify(q.records)||a.clipped<z.bound)throw Error("bad refinement or monotonicity");
      const orig=[[gauge,0],...t.pins,...pins].sort((a,b)=>a[0]-b[0]),h=sha(JSON.stringify(orig)+"\n"),gid="GUARD-v1:sha256:"+sha(JSON.stringify(["PNP-GUARD-v1",entry.instance_id,"EB-PORT-PINS-v1",h])+"\n");
      const rid="RESIDUAL-v1:sha256:"+sha(JSON.stringify(["PNP-RESIDUAL-v1",entry.instance_id,gid,"FP51-ENERGY-TABLE-v1",ctx.chartHash,ctx.mapHash])+"\n");
      next.push({pins,bound:a.clipped,exactRelaxed:q.bound,reads:a.localReads,checkReads:q.localReads,guard_id:gid,residual_id:rid,rowHash:sha(JSON.stringify(a.records)+"\n")});newly++;
    }}
    // The two children replace exactly one parent cube; verify complete cover without materializing free original variables.
    const vars=split.slice(0,k+1).map(x=>x[0]);for(let m=0;m<2**vars.length;m++){let n=0;for(const z of next){events.guardCoverageChecks++;n+=Number(z.pins.every(([v,b])=>((m>>vars.indexOf(v))&1)===b))}if(n!==1)throw Error("coverage failure")}
    let q=Math.min(...next.map(x=>x.bound));if(q<bound)throw Error("nonmonotone");bound=q;front=next;row.levels.push({v,degree,bound,newly,front});
   }}catch(e){events.failed++;row.reason=String(e);if(!String(e).includes("cap"))throw e}
  rows.push(row)
 }
 return {rows,events,cap};
}
if(typeof module!=="undefined")module.exports={refine};
